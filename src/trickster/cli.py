"""
整蠱專家 Protocol CLI
Usage: trickster serve | joke | pollinate | tricks | qotd
"""

import sys
import json
from .jokes import JokeStore, TRICKS, JOKES
from .server import serve
from .pollinate import pollinate


def cmd_joke(args):
    """Generate and display a random joke."""
    store = JokeStore()
    joke = store.random()
    trick = TRICKS.get(joke.get("trick", "finger"), TRICKS["finger"])

    print(f"\n整蠱專家 Joke #{joke['id']}")
    print(f"Trick: {trick['protocol']} (port {trick['port']}) — {trick['style']}")
    print(f"Layer: {trick['layer']} ({trick['word']})")
    print(f"\n  {joke['joke']}")
    print(f"\n  Language: {joke.get('lang', 'hk')}")
    print(f"  Delivered via: {trick['protocol']}\n")

    store.serve(joke, joke.get("trick", "finger"))


def cmd_qotd(args):
    """Show Quote of the Day."""
    store = JokeStore()
    joke = store.qotd()
    print(f"\n整蠱專家 Quote of the Day:\n  {joke['joke']}\n")


def cmd_tricks(args):
    """List all trick protocols."""
    print(f"\n整蠱專家 Trick Protocols ({len(TRICKS)} total)\n")
    print(f"{'#':<3} {'Protocol':<10} {'Port':<5} {'Style':<25} {'Layer':<20} {'Word'}")
    print("-" * 90)
    for i, (key, t) in enumerate(TRICKS.items(), 1):
        print(f"{i:<3} {t['protocol']:<10} {t['port']:<5} {t['style']:<25} {t['layer']:<20} {t['word']}")
    print()


def cmd_serve(args):
    """Start protocol servers."""
    only = None
    if len(args) > 1 and args[0] == "--only":
        only = args[1]
    serve(only=only)


def cmd_pollinate(args):
    """Cross-pollinate jokes to Kingdom repos."""
    pollinate()


def cmd_stats(args):
    """Show joke store stats."""
    store = JokeStore()
    print(f"\n整蠱專家 Stats")
    print(f"  Total jokes:    {len(store.all_jokes())}")
    print(f"  Jokes served:   {store.served_count()}")
    print(f"  Joke store:     {store.data_dir}")
    print()


USAGE = """
整蠱專家 Protocol (TBP) v0.1.0
「謝謝你吳德泰！」— 周星馳

Usage: trickster <command> [args]

Commands:
  serve [--only <protocol>]   Start protocol servers (finger, gopher, qotd, daytime, whois, chargen)
  joke                        Get a random joke via random trick
  qotd                        Show Quote of the Day
  tricks                      List all 8 trick protocols
  pollinate                   Cross-pollinate jokes to Kingdom repos
  stats                       Show joke store statistics

Examples:
  trickster serve
  trickster serve --only finger
  trickster joke
  trickster pollinate
"""


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print(USAGE)
        return

    cmd = args[0]
    rest = args[1:]

    commands = {
        "serve": lambda: cmd_serve(rest),
        "joke": lambda: cmd_joke(rest),
        "qotd": lambda: cmd_qotd(rest),
        "tricks": lambda: cmd_tricks(rest),
        "pollinate": lambda: cmd_pollinate(rest),
        "stats": lambda: cmd_stats(rest),
    }

    handler = commands.get(cmd)
    if handler:
        handler()
    else:
        print(f"Unknown command: {cmd}")
        print(USAGE)


if __name__ == "__main__":
    main()