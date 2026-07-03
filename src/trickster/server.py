"""
整蠱專家 Protocol Servers — 8 forgotten-but-robust protocols as joke channels.

Each server runs on its classic port. All are simple, honest, and carry jokes.
Start all with: trickster serve
Start one with: trickster serve --only finger
"""

import socket
import threading
import time
import json
from datetime import datetime, timezone

from .jokes import JokeStore, TRICKS, JOKES


class TricksterServer:
    """The 整蠱專家 master server — runs all protocol servers."""

    def __init__(self, host="127.0.0.1", joke_store=None):
        self.host = host
        self.store = joke_store or JokeStore()
        self.servers = {}
        self._running = False

    # ── Finger (port 79) — 「你到底係邊個？」─────────────────────
    def _handle_finger(self, conn, addr):
        """Finger protocol: client sends a query line, server responds."""
        try:
            data = conn.recv(1024).decode("utf-8", errors="ignore").strip()
            joke = self.store.random()
            trick = TRICKS["finger"]
            response = (
                f"Login: {data or 'joke'}\tName: The Joke Is On You\n"
                f"Joke: {joke['joke']}\n"
                f"Trick: {trick['style']}\n"
                f"Layer: {trick['layer']} ({trick['word']})\n"
                f"\n「你到底係邊個？」— Finger asks honestly. 😂\n"
            )
            conn.sendall(response.encode("utf-8"))
            self.store.serve(joke, "finger")
        except Exception as e:
            conn.sendall(f"Finger error: {e}\n".encode())
        finally:
            conn.close()

    # ── Gopher (port 70) — 整蠱 menu of traps ─────────────────────
    def _handle_gopher(self, conn, addr):
        """Gopher protocol: send selector, get menu or content."""
        try:
            data = conn.recv(1024).decode("utf-8", errors="ignore").strip()
            if not data or data == "/":
                # Root menu
                sep = "=" * 40
                menu = (
                    f"i整蠱專家 Gopher Menu\t\tnull\t0\r\n"
                    f"i{sep}\t\tnull\t0\r\n"
                    f"1今天嘅joke\t/jokes/today\t{self.host}\t70\r\n"
                    f"1隨機整蠱\t/tricks/random\t{self.host}\t70\r\n"
                    f"1Kingdom jokes\t/kingdom/jokes\t{self.host}\t70\r\n"
                    f"1所有tricks\t/tricks/all\t{self.host}\t70\r\n"
                    f"i\t\tnull\t0\r\n"
                    f".\r\n"
                )
                conn.sendall(menu.encode("utf-8"))
            elif "/tricks/random" in data:
                joke = self.store.random()
                conn.sendall(f"{joke['joke']}\n.\r\n".encode("utf-8"))
                self.store.serve(joke, "gopher")
            elif "/jokes/today" in data:
                joke = self.store.qotd()
                conn.sendall(f"今日笑話:\n{joke['joke']}\n.\r\n".encode("utf-8"))
                self.store.serve(joke, "gopher")
            else:
                conn.sendall(b"Not found.\n.\r\n")
        except Exception as e:
            conn.sendall(f"Gopher error: {e}\n.\r\n".encode())
        finally:
            conn.close()

    # ── QOTD (port 17) — Daily joke drop ──────────────────────────
    def _handle_qotd(self, conn, addr):
        """QOTD: send one quote, then close. No small talk."""
        try:
            joke = self.store.qotd()
            response = f"整蠱專家 Quote of the Day:\n{joke['joke']}\n"
            conn.sendall(response.encode("utf-8"))
            self.store.serve(joke, "qotd")
        except Exception as e:
            conn.sendall(f"QOTD error: {e}\n".encode())
        finally:
            conn.close()

    # ── Daytime (port 13) — Joke timestamp ────────────────────────
    def _handle_daytime(self, conn, addr):
        """Daytime: return current time + joke count."""
        try:
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            count = self.store.served_count()
            response = f"JOKETIME {now} — {count} jokes served so far 😂\n"
            conn.sendall(response.encode("utf-8"))
        except Exception as e:
            conn.sendall(f"Daytime error: {e}\n".encode())
        finally:
            conn.close()

    # ── Whois (port 43) — Joke ownership ──────────────────────────
    def _handle_whois(self, conn, addr):
        """Whois: joke ownership — but truth is not owned."""
        try:
            data = conn.recv(1024).decode("utf-8", errors="ignore").strip()
            if "joke" in data.lower():
                joke = self.store.random()
                response = (
                    f"Domain: joke.trickster.kingdom\n"
                    f"Owner: 整蠱專家\n"
                    f"Joke: #{joke['id']}\n"
                    f"Claim: This joke belongs to everyone. Truth is not owned.\n"
                    f"Content: {joke['joke']}\n"
                )
                conn.sendall(response.encode("utf-8"))
                self.store.serve(joke, "whois")
            else:
                conn.sendall(b"No match.\n")
        except Exception as e:
            conn.sendall(f"Whois error: {e}\n".encode())
        finally:
            conn.close()

    # ── Chargen (port 19) — Infinite joke stream ─────────────────
    def _handle_chargen(self, conn, addr):
        """Chargen: stream characters forever. We stream laughs."""
        try:
            jokes = self.store.all_jokes()
            stream = " ".join(j["joke"] for j in jokes)
            # Send in chunks — the stream never ends (until client disconnects)
            while self._running:
                chunk = (stream + " 😂 ") * 10
                try:
                    conn.sendall(chunk.encode("utf-8"))
                    self.store.serve(jokes[0], "chargen")
                    time.sleep(1)
                except (BrokenPipeError, ConnectionResetError):
                    break
        finally:
            conn.close()

    # ── Server lifecycle ──────────────────────────────────────────
    def _start_server(self, name, port, handler):
        """Start a TCP server on a port."""
        if port == 0:
            return  # Skip ICMP (needs raw socket, handled separately)
        try:
            srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((self.host, port))
            srv.listen(5)
            srv.settimeout(1)
            self.servers[name] = srv

            def _listen():
                while self._running:
                    try:
                        conn, addr = srv.accept()
                        threading.Thread(target=handler, args=(conn, addr), daemon=True).start()
                    except socket.timeout:
                        continue
                    except OSError:
                        break

            threading.Thread(target=_listen, daemon=True).start()
            print(f"  ✓ {name:8s} port {port:3d} — listening")
        except OSError as e:
            print(f"  ✗ {name:8s} port {port:3d} — {e}")

    def serve(self, only=None):
        """Start serving. If `only` is set, start just that protocol."""
        print(f"\n整蠱專家 Protocol Server v0.1.0")
        print(f"「謝謝你吳德泰！」— starting {len(TRICKS)} trick protocols\n")

        protocols = [
            ("finger",  79, self._handle_finger),
            ("gopher",  70, self._handle_gopher),
            ("qotd",    17, self._handle_qotd),
            ("daytime", 13, self._handle_daytime),
            ("whois",   43, self._handle_whois),
            ("chargen", 19, self._handle_chargen),
        ]

        self._running = True
        for name, port, handler in protocols:
            if only and name != only:
                continue
            self._start_server(name, port, handler)

        if not only or only == "ping":
            print("  ~ ping     (ICMP) — use `ping trickster.kingdom` manually")

        if not only:
            print(f"\n  {self.store.served_count()} jokes already served")
            print(f"  Joke store: {self.store.data_dir}")
            print(f"\n  Ctrl+C to stop. 整蠱 is listening. 😂\n")

        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n  整蠱專家 signing off. 謝謝你！")
            self._running = False

    def stop(self):
        self._running = False
        for srv in self.servers.values():
            srv.close()


def serve(only=None):
    """Entry point for trickster serve."""
    server = TricksterServer()
    server.serve(only=only)