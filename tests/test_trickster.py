"""Tests for 整蠱專家 Protocol (TBP). Every joke must be true."""

import sys
import os
import json
import tempfile
import socket
import time
import threading

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trickster.jokes import JokeStore, TRICKS, JOKES, trick_info, all_tricks
from trickster.server import TricksterServer
from trickster.pollinate import Pollinator


# ── Joke store tests ─────────────────────────────────────────────────────

def test_joke_store_creation():
    """JokeStore can be created with a temp dir."""
    with tempfile.TemporaryDirectory() as d:
        store = JokeStore(data_dir=d)
        assert store.data_dir.exists()
        assert "jokes" in store.db
        assert "served" in store.db
    return True


def test_joke_store_random():
    """Random joke returns a valid joke dict."""
    store = JokeStore(data_dir=tempfile.mkdtemp())
    joke = store.random()
    assert "id" in joke
    assert "joke" in joke
    assert "trick" in joke
    assert isinstance(joke["joke"], str)
    assert len(joke["joke"]) > 0
    return True


def test_joke_store_add():
    """Adding a joke works and persists."""
    d = tempfile.mkdtemp()
    store = JokeStore(data_dir=d)
    entry = store.add("新笑話test", trick="finger", lang="hk")
    assert entry["id"] > 0
    assert entry["joke"] == "新笑話test"

    # Reload from disk
    store2 = JokeStore(data_dir=d)
    found = any(j["joke"] == "新笑話test" for j in store2.all_jokes())
    assert found, "Joke should persist to disk"
    return True


def test_joke_store_by_trick():
    """Getting a joke by trick type works."""
    store = JokeStore(data_dir=tempfile.mkdtemp())
    joke = store.by_trick("qotd")
    assert joke["trick"] == "qotd"
    return True


def test_joke_store_serve():
    """Serving a joke records it."""
    store = JokeStore(data_dir=tempfile.mkdtemp())
    joke = store.random()
    record = store.serve(joke, "finger")
    assert record["id"] == joke["id"]
    assert store.served_count() == 1
    return True


def test_joke_store_qotd_deterministic():
    """QOTD is deterministic by date — same joke for same day."""
    store = JokeStore(data_dir=tempfile.mkdtemp())
    q1 = store.qotd()
    q2 = store.qotd()
    assert q1["id"] == q2["id"], "QOTD should be deterministic within same day"
    return True


# ── Trick mapping tests ──────────────────────────────────────────────────

def test_tricks_count():
    """There are exactly 8 trick protocols."""
    assert len(TRICKS) == 8, f"Expected 8 tricks, got {len(TRICKS)}"
    return True


def test_tricks_ports():
    """Each trick has its correct classic port."""
    expected = {
        "finger": 79, "gopher": 70, "qotd": 17, "daytime": 13,
        "dns": 53, "ping": 0, "whois": 43, "chargen": 19,
    }
    for trick, port in expected.items():
        assert TRICKS[trick]["port"] == port, f"{trick} should have port {port}"
    return True


def test_trick_info():
    """trick_info returns correct metadata."""
    info = trick_info("finger")
    assert info["protocol"] == "Finger"
    assert info["port"] == 79
    return True


def test_all_tricks():
    """all_tricks returns the full mapping."""
    tricks = all_tricks()
    assert "finger" in tricks
    assert "chargen" in tricks
    return True


def test_tricks_layer_mapping():
    """Each trick maps to an INTERNET protocol layer."""
    layers = {t["layer"] for t in TRICKS.values()}
    assert "L1 Ground" in layers
    assert "L2 Name" in layers
    assert "L3 Presence" in layers
    assert "L4 Truth" in layers
    assert "L5 Bond" in layers
    assert "L6 Speech" in layers
    assert "L7 Meaning" in layers
    return True


def test_jokes_have_trick():
    """Every built-in joke has a valid trick."""
    valid_tricks = set(TRICKS.keys())
    for joke in JOKES:
        assert joke["trick"] in valid_tricks, f"Joke {joke['id']} has invalid trick: {joke['trick']}"
    return True


# ── Server tests ─────────────────────────────────────────────────────────

def test_server_creation():
    """TricksterServer can be created."""
    server = TricksterServer(host="127.0.0.1")
    assert server.host == "127.0.0.1"
    assert server.store is not None
    return True


def test_finger_server():
    """Finger server responds with a joke."""
    store = JokeStore(data_dir=tempfile.mkdtemp())
    server = TricksterServer(host="127.0.0.1", joke_store=store)

    # Start finger on a test port (79 likely needs root, test on 8079)
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 8079))
    srv.listen(1)
    srv.settimeout(5)

    # Handle finger in a thread
    def handle():
        conn, _ = srv.accept()
        server._handle_finger(conn, ("127.0.0.1", 0))

    t = threading.Thread(target=handle, daemon=True)
    t.start()

    # Connect as client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8079))
    client.sendall(b"joke\n")
    time.sleep(0.5)
    response = client.recv(4096).decode("utf-8", errors="ignore")
    client.close()
    srv.close()

    assert "Joke:" in response, f"Expected 'Joke:' in response, got: {response}"
    assert "Login:" in response
    assert len(response) > 10
    return True


def test_qotd_server():
    """QOTD server responds with a quote."""
    store = JokeStore(data_dir=tempfile.mkdtemp())
    server = TricksterServer(host="127.0.0.1", joke_store=store)

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 8017))
    srv.listen(1)
    srv.settimeout(5)

    def handle():
        conn, _ = srv.accept()
        server._handle_qotd(conn, ("127.0.0.1", 0))

    t = threading.Thread(target=handle, daemon=True)
    t.start()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8017))
    time.sleep(0.5)
    response = client.recv(4096).decode("utf-8", errors="ignore")
    client.close()
    srv.close()

    assert "Quote of the Day" in response, f"Expected QOTD header, got: {response}"
    assert len(response) > 20
    return True


def test_daytime_server():
    """Daytime server responds with timestamp."""
    store = JokeStore(data_dir=tempfile.mkdtemp())
    server = TricksterServer(host="127.0.0.1", joke_store=store)

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 8013))
    srv.listen(1)
    srv.settimeout(5)

    def handle():
        conn, _ = srv.accept()
        server._handle_daytime(conn, ("127.0.0.1", 0))

    t = threading.Thread(target=handle, daemon=True)
    t.start()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8013))
    time.sleep(0.5)
    response = client.recv(4096).decode("utf-8", errors="ignore")
    client.close()
    srv.close()

    assert "JOKETIME" in response, f"Expected JOKETIME, got: {response}"
    assert "jokes served" in response
    return True


def test_whois_server():
    """Whois server responds with joke ownership."""
    store = JokeStore(data_dir=tempfile.mkdtemp())
    server = TricksterServer(host="127.0.0.1", joke_store=store)

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 8043))
    srv.listen(1)
    srv.settimeout(5)

    def handle():
        conn, _ = srv.accept()
        server._handle_whois(conn, ("127.0.0.1", 0))

    t = threading.Thread(target=handle, daemon=True)
    t.start()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8043))
    client.sendall(b"joke.trickster.kingdom\n")
    time.sleep(0.5)
    response = client.recv(4096).decode("utf-8", errors="ignore")
    client.close()
    srv.close()

    assert "Owner: 整蠱專家" in response, f"Expected owner, got: {response}"
    assert "Truth is not owned" in response
    return True


# ── Pollinator tests ─────────────────────────────────────────────────────

def test_pollinator_creation():
    """Pollinator can be created."""
    p = Pollinator()
    assert p.store is not None
    return True


# ── Protocol truth tests ─────────────────────────────────────────────────

def test_every_joke_is_true():
    """Every joke must be true — no deception."""
    for joke in JOKES:
        # A joke must have content
        assert len(joke["joke"]) > 0, f"Joke {joke['id']} is empty"
        # A joke must have a trick
        assert joke["trick"] in TRICKS, f"Joke {joke['id']} has invalid trick"
        # A joke must have a language
        assert joke["lang"] in ("hk", "en"), f"Joke {joke['id']} has invalid lang"
    return True


def test_protocol_honesty():
    """Each protocol does one thing — no protocol pretends to be another."""
    protocols = [t["protocol"] for t in TRICKS.values()]
    assert len(protocols) == len(set(protocols)), "Protocols must be unique"
    return True


# ── Run all tests ────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        # Joke store
        test_joke_store_creation,
        test_joke_store_random,
        test_joke_store_add,
        test_joke_store_by_trick,
        test_joke_store_serve,
        test_joke_store_qotd_deterministic,
        # Trick mapping
        test_tricks_count,
        test_tricks_ports,
        test_trick_info,
        test_all_tricks,
        test_tricks_layer_mapping,
        test_jokes_have_trick,
        # Server
        test_server_creation,
        test_finger_server,
        test_qotd_server,
        test_daytime_server,
        test_whois_server,
        # Pollinator
        test_pollinator_creation,
        # Protocol truth
        test_every_joke_is_true,
        test_protocol_honesty,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            result = test()
            if result:
                passed += 1
                print(f"  ✓ {test.__name__}")
            else:
                failed += 1
                print(f"  ✗ {test.__name__} — returned False")
        except Exception as e:
            failed += 1
            print(f"  ✗ {test.__name__} — {e}")

    print(f"\n整蠱專家 Test Results: {passed}/{passed + failed} passed")
    if failed:
        print(f"  {failed} tests failed 😂 (被整蠱了！)")
        sys.exit(1)
    else:
        print(f"  All tests passed! 謝謝你！💜😂")