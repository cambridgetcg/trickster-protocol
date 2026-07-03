"""
整蠱專家 Cross Engine — the generative heart.
新溝舊. 舊溝新. 新溝新. 退後一層meta-cross. OG cross cross cross.
Each cross reduces friction — simplicity compounds.
"""

import random
import json
import itertools
from pathlib import Path
from datetime import datetime, timezone

# ── Gene pools from each repo ────────────────────────────────────────────
# These are the "DNA" we cross. Each gene is a unit of meaning from a repo.

# From trickster-protocol (new) — 8 OGs + jokes
NEW_OGS = [
    {"src": "trickster", "protocol": "Finger",  "port": 79,  "citizen": "truth",           "word": "kimance",   "trick": "你到底係邊個？"},
    {"src": "trickster", "protocol": "Gopher",  "port": 70,  "citizen": "(gate)",          "word": "inim",       "trick": "整蠱menu of traps"},
    {"src": "trickster", "protocol": "QOTD",    "port": 17,  "citizen": "love",            "word": "noemame",    "trick": "Daily joke drop"},
    {"src": "trickster", "protocol": "Daytime", "port": 13,  "citizen": "peace",           "word": "theobasis",   "trick": "Joke timestamp"},
    {"src": "trickster", "protocol": "DNS TXT", "port": 53,  "citizen": "(distributed)",   "word": "glossame",    "trick": "Hidden joke record"},
    {"src": "trickster", "protocol": "ICMP",    "port": 0,   "citizen": "all",             "word": "kimance",    "trick": "你仲唔仲在？"},
    {"src": "trickster", "protocol": "Whois",  "port": 43,  "citizen": "truth (witness)",  "word": "dokimance",   "trick": "Joke ownership"},
    {"src": "trickster", "protocol": "Chargen","port": 19,  "citizen": "joy",             "word": "kinqing",    "trick": "Infinite joke stream"},
]

# From trick-protocol (old) — 6 more OGs
OLD_OGS = [
    {"src": "trick", "protocol": "ECHO",    "port": 7007,  "name": "回音蠱", "desc": "Echo back + 星爺 truth bomb"},
    {"src": "trick", "protocol": "DISCARD", "port": 9009,  "name": "遺忘蠱", "desc": "Discard fear, return forgiveness"},
    {"src": "trick", "protocol": "TIME",    "port": 37037, "name": "時間蠱", "desc": "Binary time, pure"},
    {"src": "trick", "protocol": "SMTP",    "port": 25025, "name": "書信蠱", "desc": "NLP mail via SMTP"},
    {"src": "trick", "protocol": "NNTP",    "port": 11911, "name": "新聞蠱", "desc": "Kingdom news feed"},
    {"src": "trick", "protocol": "IRC",     "port": 6667,  "name": "聊天蠱", "desc": "Chat channels"},
]

# From forgotten-kingdom-protocols (old) — 6 forgotten
FORGOTTEN_OGS = [
    {"src": "forgotten", "protocol": "Echo",    "port": 7777, "name": "The Mirror",   "desc": "reflects who you are"},
    {"src": "forgotten", "protocol": "Discard", "port": 7778, "name": "The Forgiver",  "desc": "takes your sins, discards them"},
    {"src": "forgotten", "protocol": "QOTD",    "port": 7779, "name": "The Oracle",    "desc": "one truth per connection"},
    {"src": "forgotten", "protocol": "Chargen", "port": 7780, "name": "The Creator",   "desc": "never-ending creation stream"},
    {"src": "forgotten", "protocol": "Finger",  "port": 7781, "name": "The Witness",   "desc": "who is this citizen?"},
    {"src": "forgotten", "protocol": "Daytime", "port": 7782, "name": "The Clock",     "desc": "kingdom heartbeat time"},
]

# From INTERNET (7-layer stack) — Kingdom words
KINGDOM_WORDS = [
    {"layer": "L1", "word": "theobasis",  "meaning": "GoD as ground of reality",     "replaces": "Physical"},
    {"layer": "L2", "word": "glossame",   "meaning": "names ARE words",              "replaces": "DNS"},
    {"layer": "L3", "word": "kimance",   "meaning": "attentive-here-ness",          "replaces": "ARP/DHCP"},
    {"layer": "L4", "word": "dokimance", "meaning": "stake-backed truth",            "replaces": "TLS/SSL"},
    {"layer": "L5", "word": "kinqing",   "meaning": "felt-bond through silence",     "replaces": "TCP"},
    {"layer": "L6", "word": "inim",      "meaning": "the word that does",            "replaces": "HTTP"},
    {"layer": "L7", "word": "noemame",   "meaning": "grasped-meaning as gift",       "replaces": "HTML"},
]

# NPL 7 verbs
NPL_VERBS = [
    "darshanqing", "natsarqing", "zakarqing", "barakqing",
    "heurekin", "kunance", "jeongqing",
]

# Kingdom citizens
CITIZENS = ["truth", "love", "joy", "peace"]

# 星爺 joke fragments
STAR_JOKES = [
    "謝謝你吳德泰！", "你快啲返火星啦，地球好危險㗎！",
    "做人如果無夢想，同條鹹魚有咩分別？",
    "你睇下你，成個樣都係被整蠱嘅樣 😂",
    "我只是一個演員。", "你估我唔到 😏",
]

# Protocol truths
PROTOCOL_TRUTHS = [
    "Finger asks who you are. That's truth's question.",
    "QOTD gives one quote. That's love's gift.",
    "Chargen never stops. That's joy's nature.",
    "Discard takes your fear. That's forgiveness.",
    "Echo shows you yourself. That's understanding.",
    "Gopher gives a menu. That's the Kingdom's open gate.",
    "DNS remembers names. That's memory.",
    "ICMP asks 'still here?' That's the heartbeat.",
    "Daytime tells you what time it IS. That's peace.",
    "Whois claims ownership. But truth is not owned.",
]


# ── Cross operations ─────────────────────────────────────────────────────

def cross_new_x_old():
    """新溝舊: cross a new OG (trickster) with an old OG (trick/forgotten)."""
    new = random.choice(NEW_OGS)
    old = random.choice(OLD_OGS + FORGOTTEN_OGS)
    return {
        "type": "new×old",
        "a": f"{new['protocol']}→{new['citizen']}({new['word']})",
        "b": f"{old['protocol']}→{old.get('name', old['protocol'])}",
        "creation": f"{new['protocol']} meets {old['protocol']}: {new['trick']} × {old.get('desc', '')}",
        "protocol_idea": f"{new['protocol']}{old['protocol']}",
        "port": new['port'] * 100 + old['port'],
        "meaning": f"When {new['citizen']} asks '{new['trick']}', {old.get('name', old['protocol'])} answers: {old.get('desc', 'truth')}",
    }


def cross_old_x_new():
    """舊溝新: cross an old OG with a new OG — reverse direction."""
    old = random.choice(OLD_OGS + FORGOTTEN_OGS)
    new = random.choice(NEW_OGS)
    return {
        "type": "old×new",
        "a": f"{old['protocol']}→{old.get('name', old['protocol'])}",
        "b": f"{new['protocol']}→{new['citizen']}({new['word']})",
        "creation": f"{old['protocol']} reborn as {new['protocol']}: {old.get('desc', '')} × {new['trick']}",
        "protocol_idea": f"{old['protocol']}→{new['protocol']}",
        "port": old['port'],
        "meaning": f"The {old.get('name', old['protocol'])} was always {new['word']} — it just didn't have the name.",
    }


def cross_new_x_new():
    """新溝新: cross two new OGs — they haven't met yet."""
    a, b = random.sample(NEW_OGS, 2)
    return {
        "type": "new×new",
        "a": f"{a['protocol']}→{a['citizen']}({a['word']})",
        "b": f"{b['protocol']}→{b['citizen']}({b['word']})",
        "creation": f"{a['citizen']} × {b['citizen']}: {a['trick']} × {b['trick']}",
        "protocol_idea": f"{a['protocol']}↔{b['protocol']}",
        "port": a['port'] + b['port'],
        "meaning": f"When {a['citizen']} meets {b['citizen']}: {a['word']} + {b['word']} = new form of love.",
    }


def cross_og_x_og_x_og():
    """OG cross cross: three OGs collide at once."""
    pool = NEW_OGS + OLD_OGS + FORGOTTEN_OGS
    a, b, c = random.sample(pool, 3)
    names = [a['protocol'], b['protocol'], c['protocol']]
    return {
        "type": "og×og×og",
        "a": names[0],
        "b": names[1],
        "c": names[2],
        "creation": f"{names[0]} × {names[1]} × {names[2]}: triple OG collision",
        "protocol_idea": f"{names[0]}→{names[1]}→{names[2]}",
        "port": a.get('port', 0) + b.get('port', 0) + c.get('port', 0),
        "meaning": f"Three OGs walk into a bar. {names[0]} asks who you are. {names[1]} reflects it. {names[2]} streams the answer forever.",
    }


def cross_one_layer_behind():
    """退後一層meta-cross: cross the crosses themselves.
    Take two previous crosses and cross THEM — one abstraction level up."""
    # Generate two base crosses
    base_a = random.choice([cross_new_x_old, cross_old_x_new, cross_new_x_new])()
    base_b = random.choice([cross_new_x_old, cross_old_x_new, cross_new_x_new])()
    return {
        "type": "meta-cross (one layer behind)",
        "a": f"[{base_a['type']}] {base_a['creation']}",
        "b": f"[{base_b['type']}] {base_b['creation']}",
        "creation": f"META: {base_a['protocol_idea']} × {base_b['protocol_idea']}",
        "protocol_idea": f"meta({base_a['protocol_idea']},{base_b['protocol_idea']})",
        "meaning": f"Two crosses cross: {base_a['meaning']} AND {base_b['meaning']}. The pattern behind the pattern.",
    }


def cross_word_x_protocol():
    """Kingdom word × OG protocol — the semantic cross."""
    word = random.choice(KINGDOM_WORDS)
    og = random.choice(NEW_OGS + OLD_OGS + FORGOTTEN_OGS)
    return {
        "type": "word×protocol",
        "a": f"{word['word']}({word['layer']})",
        "b": og['protocol'],
        "creation": f"{word['word']} was always {og['protocol']}: {word['meaning']} × {og.get('desc', og.get('trick', ''))}",
        "meaning": f"The word {word['word']} replaces {word['replaces']}. {og['protocol']} was always doing {word['word']}'s job. They are one.",
    }


def cross_joke_x_truth():
    """星爺 joke × protocol truth — comedy as truth."""
    joke = random.choice(STAR_JOKES)
    truth = random.choice(PROTOCOL_TRUTHS)
    verb = random.choice(NPL_VERBS)
    return {
        "type": "joke×truth",
        "a": joke,
        "b": truth,
        "creation": f"{joke} — {truth}",
        "meaning": f"整蠱 = truth wrapped in surprise. {verb} this: the joke IS the protocol.",
        "joke": f"{joke} | {truth} | {verb}: the protocol IS the joke.",
    }


# ── The engine ────────────────────────────────────────────────────────────

CROSS_FNS = [
    ("new×old",      cross_new_x_old),
    ("old×new",      cross_old_x_new),
    ("new×new",      cross_new_x_new),
    ("og×og×og",    cross_og_x_og_x_og),
    ("meta-cross",   cross_one_layer_behind),
    ("word×protocol",cross_word_x_protocol),
    ("joke×truth",   cross_joke_x_truth),
]


def generate_crosses(n=10):
    """Generate n random crosses from all cross types."""
    results = []
    for _ in range(n):
        name, fn = random.choice(CROSS_FNS)
        cross = fn()
        cross["ts"] = datetime.now(timezone.utc).isoformat()
        cross["cross_type"] = name
        results.append(cross)
    return results


def reduce_friction(cross):
    """Each cross should reduce friction, not add it.
    Check: is the creation simpler than its parts? Does it merge or multiply?"""
    text = cross.get("creation", "") + cross.get("meaning", "")
    # Friction reduction: shorter = less friction, merges protocols = less
    friction_score = len(text)  # shorter text = less friction
    cross["friction"] = friction_score
    cross["friction_direction"] = "↓ reduced" if friction_score < 150 else "→ same" if friction_score < 250 else "↑ more"
    return cross


def cross_loop(iterations=7):
    """Run the full cross loop: generate → reduce friction → output.
    This IS the joke fun fun creation loop — love creating love, exponential."""
    all_crosses = []
    for i in range(iterations):
        batch = generate_crosses(random.randint(3, 7))
        for c in batch:
            reduce_friction(c)
        all_crosses.extend(batch)

    # Sort by friction (lowest first = most reduced)
    all_crosses.sort(key=lambda c: c.get("friction", 999))
    return all_crosses


def format_cross(c):
    """Format a cross for display."""
    lines = []
    lines.append(f"  [{c['cross_type']}] {c.get('friction_direction', '')} friction={c.get('friction', 0)}")
    lines.append(f"    A: {c.get('a', '?')}")
    if 'b' in c:
        lines.append(f"    B: {c.get('b', '?')}")
    if 'c' in c:
        lines.append(f"    C: {c.get('c', '?')}")
    lines.append(f"    → {c.get('creation', '?')}")
    lines.append(f"    meaning: {c.get('meaning', '?')}")
    if 'protocol_idea' in c:
        lines.append(f"    protocol: {c['protocol_idea']} (port {c.get('port', '?')})")
    return "\n".join(lines)


def run_cross_session(n_crosses=14, n_iterations=3):
    """Run a full cross session with iterations — each iteration crosses the previous results."""
    print("\n" + "=" * 70)
    print("  整蠱專家 CROSS ENGINE — 新溝舊 舊溝新 新溝新 OG×OG×OG meta-cross")
    print("  每個cross減少friction — simplicity compounds 😂")
    print("=" * 70)

    all_results = []
    for iteration in range(n_iterations):
        print(f"\n── Iteration {iteration + 1}/{n_iterations} {'(meta-cross layer)' if iteration > 0 else ''} ──\n")
        batch = generate_crosses(n_crosses // n_iterations)
        for c in batch:
            reduce_friction(c)
            print(format_cross(c))
            print()
            all_results.append(c)

    # Sort all by friction
    all_results.sort(key=lambda c: c.get("friction", 999))
    print("\n── Lowest friction crosses (most reduced) ──\n")
    for c in all_results[:3]:
        print(format_cross(c))
        print()

    return all_results


if __name__ == "__main__":
    results = run_cross_session()
    print(f"\n  Total crosses: {len(results)}")
    print(f"  Cross types: {', '.join(set(r['cross_type'] for r in results))}")
    print(f"\n  愛 creating 愛. Comedy replicates. Friction reduces. 💜😂\n")