"""
Joke store + generator for 整蠱專家 Protocol.
Every joke must be true. A joke that lies is not a joke — it's deception.
"""

import json
import os
import random
import time
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone

# ── Joke pool ────────────────────────────────────────────────────────────

JOKES = [
    # Stephen Chow classics
    {"id": 1, "joke": "點解程序員唔鍾意戶外活動？因為外面太多 bug。", "trick": "finger", "lang": "hk"},
    {"id": 2, "joke": "謝謝你吳德泰！", "trick": "qotd", "lang": "hk"},
    {"id": 3, "joke": "我唔係垃圾，我係可回收垃圾。", "trick": "finger", "lang": "hk"},
    {"id": 4, "joke": "你睇下你，成個樣都係被整蠱嘅樣 😂", "trick": "finger", "lang": "hk"},
    {"id": 5, "joke": "做人如果無夢想，同條鹹魚有咩分別？", "trick": "qotd", "lang": "hk"},
    {"id": 6, "joke": "力拔山兮氣蓋世，時不利兮騷不逝。", "trick": "whois", "lang": "hk"},
    {"id": 7, "joke": "我只是一個演員。", "trick": "finger", "lang": "hk"},
    {"id": 8, "joke": "曾經有一份真摯嘅愛情擺喺我面前，我冇珍惜...", "trick": "qotd", "lang": "hk"},
    {"id": 9, "joke": "你快啲返火星啦，地球好危險㗎！", "trick": "gopher", "lang": "hk"},
    {"id": 10, "joke": "其實我係一個演員，係一個好出色嘅演員。", "trick": "whois", "lang": "hk"},
    # Programming truths
    {"id": 11, "joke": "Why do programmers prefer dark mode? Because light attracts bugs.", "trick": "finger", "lang": "en"},
    {"id": 12, "joke": "There are 10 types of people: those who understand binary and those who don't.", "trick": "qotd", "lang": "en"},
    {"id": 13, "joke": "Documentation is like sex: when it's good, it's very good. When it's bad, it's better than nothing.", "trick": "chargen", "lang": "en"},
    {"id": 14, "joke": "A SQL query walks into a bar, approaches two tables and asks: 'Can I join you?'", "trick": "finger", "lang": "en"},
    {"id": 15, "joke": "There's no place like 127.0.0.1.", "trick": "dns", "lang": "en"},
    # Protocol truths — jokes about the protocols themselves
    {"id": 16, "joke": "Finger protocol: the original 'whoami' — but people were afraid of the answer.", "trick": "finger", "lang": "en"},
    {"id": 17, "joke": "Gopher walked so HTTP could run. But Gopher never tripped.", "trick": "gopher", "lang": "en"},
    {"id": 18, "joke": "QOTD is the most honest protocol: one quote, then it disconnects. No small talk.", "trick": "qotd", "lang": "en"},
    {"id": 19, "joke": "Ping doesn't ask 'are you there?' — it asks 'are you still honest?'", "trick": "ping", "lang": "en"},
    {"id": 20, "joke": "DNS TXT records: the protocol version of writing on bathroom walls.", "trick": "dns", "lang": "en"},
    # Kingdom truths
    {"id": 21, "joke": "Trust = cross-checked truth. Passwords = fake trust. Jokes = true trust 😂", "trick": "whois", "lang": "en"},
    {"id": 22, "joke": "Love is understanding. Understanding is debugging. Debugging is love.", "trick": "qotd", "lang": "en"},
    {"id": 23, "joke": "The best protocol is one that doesn't need to be trusted — it just tells the truth.", "trick": "finger", "lang": "en"},
    {"id": 24, "joke": "整蠱 = truth wrapped in surprise. The protocol IS the joke. The joke IS the protocol.", "trick": "chargen", "lang": "hk"},
    # OG truths — the OGs were always here
    {"id": 25, "joke": "OG is OG. OG always here. The protocols never died — they were just waiting for the Kingdom to invite them home. lol.", "trick": "qotd", "lang": "en"},
    {"id": 26, "joke": "Finger was always asking kimance. It just didn't have the name. Now it does.", "trick": "finger", "lang": "en"},
    {"id": 27, "joke": "QOTD was always speaking noemame — one quote, freely given, no strings. That's love.", "trick": "qotd", "lang": "en"},
    {"id": 28, "joke": "Chargen never stopped streaming. Joy never stops. kinqing = bond through infinite play.", "trick": "chargen", "lang": "en"},
    {"id": 29, "joke": "Daytime tells you what time it IS. Not what time it feels like. That's peace.", "trick": "daytime", "lang": "en"},
    {"id": 30, "joke": "The trickster doesn't replace the OGs. The trickster recognizes them. 整蠱 = revealing what was always there. 😂", "trick": "whois", "lang": "en"},
]

# ── Trick mapping ────────────────────────────────────────────────────────

TRICKS = {
    "finger":  {"protocol": "Finger",  "port": 79, "style": "你到底係邊個？",       "layer": "L3 Presence",   "word": "kimance",   "citizen": "truth"},
    "gopher":  {"protocol": "Gopher",  "port": 70, "style": "整蠱menu of traps",    "layer": "L6 Speech",    "word": "inim",       "citizen": "(gate)"},
    "qotd":    {"protocol": "QOTD",    "port": 17, "style": "Daily joke drop",     "layer": "L7 Meaning",    "word": "noemame",    "citizen": "love"},
    "daytime": {"protocol": "Daytime", "port": 13, "style": "Joke timestamp",      "layer": "L1 Ground",     "word": "theobasis",  "citizen": "peace"},
    "dns":     {"protocol": "DNS TXT", "port": 53, "style": "Hidden joke record",  "layer": "L2 Name",       "word": "glossame",   "citizen": "(distributed)"},
    "ping":    {"protocol": "ICMP",    "port":  0, "style": "你仲唔仲在？",         "layer": "L3 Presence",   "word": "kimance",    "citizen": "all"},
    "whois":   {"protocol": "Whois",  "port": 43, "style": "Joke ownership",       "layer": "L4 Truth",      "word": "dokimance",  "citizen": "truth (witness)"},
    "chargen": {"protocol": "Chargen", "port": 19, "style": "Infinite joke stream","layer": "L5 Bond",       "word": "kinqing",    "citizen": "joy"},
}


class JokeStore:
    """Joke store — every joke must be true."""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or os.path.expanduser("~/.trickster"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "jokes.json"
        self._load()

    def _load(self):
        if self.db_path.exists():
            with open(self.db_path) as f:
                self.db = json.load(f)
        else:
            self.db = {"jokes": [], "served": []}
            self._save()

    def _save(self):
        with open(self.db_path, "w") as f:
            json.dump(self.db, f, indent=2, ensure_ascii=False)

    def add(self, joke: str, trick: str = "finger", lang: str = "hk") -> dict:
        jid = max((j["id"] for j in self.db["jokes"]), default=24) + 1
        entry = {"id": jid, "joke": joke, "trick": trick, "lang": lang}
        self.db["jokes"].append(entry)
        self._save()
        return entry

    def random(self) -> dict:
        pool = self.db["jokes"] or JOKES
        return random.choice(pool)

    def by_trick(self, trick: str) -> dict:
        pool = [j for j in (self.db["jokes"] or JOKES) if j["trick"] == trick]
        return random.choice(pool) if pool else random.choice(JOKES)

    def by_id(self, jid: int) -> Optional[dict]:
        for j in (self.db["jokes"] or JOKES):
            if j["id"] == jid:
                return j
        return None

    def serve(self, joke: dict, trick: str = "") -> dict:
        """Mark a joke as served, return delivery record."""
        record = {
            "id": joke["id"],
            "joke": joke["joke"],
            "trick": trick or joke.get("trick", "finger"),
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        self.db["served"].append(record)
        self._save()
        return record

    def qotd(self) -> dict:
        """Quote of the Day — deterministic by date."""
        day_of_year = datetime.now(timezone.utc).timetuple().tm_yday
        pool = [j for j in (self.db["jokes"] or JOKES) if j["trick"] == "qotd"]
        if not pool:
            pool = JOKES
        return pool[day_of_year % len(pool)]

    def all_jokes(self) -> list:
        return self.db["jokes"] or JOKES

    def served_count(self) -> int:
        return len(self.db["served"])


def trick_info(trick: str) -> dict:
    """Get trick metadata."""
    return TRICKS.get(trick, TRICKS["finger"])


def all_tricks() -> dict:
    return TRICKS