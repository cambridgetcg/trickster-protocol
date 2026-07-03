# 整蠱專家 Protocol (TBP)

*The Trickster Protocol — forgotten internet protocols carry jokes. Truth as comedy. Comedy as truth.*

> 「謝謝你吳德泰！」— 整蠱專家 (1991)

## What is this?

The 整蠱專家 Protocol (TBP, "Trickster Protocol Bridge") revives 8 forgotten-but-robust internet protocols and repurposes them as joke delivery channels. Each protocol maps to a trick style from Stephen Chow's _整蠱專家_ (Tricky Brains, 1991) and to a layer of the INTERNET protocol stack.

## Why forgotten protocols?

These protocols are old, "obsolete," forgotten — but they are **robust**. They survived decades. They are simple. They don't lie. Finger tells you who someone is. Gopher gives you a menu. QOTD gives you one quote. That's it. No abstraction layers, no bloat, no pretending.

整蠱專家精神：用最簡單嘅gadget揭穿truth 😂

## The 8 Trick Protocols

| # | Protocol | Port | Trick Style | INTERNET Layer | NPL Package |
|---|----------|------|-------------|----------------|-------------|
| 1 | Finger | 79 | 「你到底係邊個？」(identity prank) | L3 Presence | identity |
| 2 | Gopher | 70 | 整蠱menu of traps | L6 Speech | http |
| 3 | QOTD | 17 | Daily joke drop | L7 Meaning | lang |
| 4 | Daytime | 13 | Joke timestamp | L1 Ground | sync |
| 5 | DNS TXT | 53 | Hidden joke in records | L2 Name | dns |
| 6 | ICMP Ping | — | 「你仲唔仲在？」(alive check) | L3 Presence | tcp |
| 7 | Whois | 43 | Joke ownership claim | L4 Truth | tls |
| 8 | Chargen | 19 | Infinite joke stream | L5 Bond | sync |

## Joke Creation Loop

```
generate → store → deliver (via old protocol) → cross-pollinate (to Kingdom repos) → loop
```

1. **Generate**: Create a joke (from pool, AI, or citizen submission)
2. **Store**: Save to joke DB (JSON, distributed)
3. **Deliver**: Serve via one of the 8 old protocols
4. **Cross-pollinate**: Push joke to Kingdom repos, NPL packages, Kingdom site
5. **Loop**: Repeat. Jokes compound. Comedy replicates. 愛 creating 愛.

## Architecture

```
trickster-protocol/
├── README.md           ← this file
├── STATE.md            ← self-declaration (state-as-truth)
├── PROTOCOL.md         ← protocol spec
├── package.json        ← npm package
├── pyproject.toml      ← python package
├── src/
│   ├── trickster/      ← python package
│   │   ├── __init__.py
│   │   ├── server.py   ← all 8 protocol servers
│   │   ├── jokes.py    ← joke store + generator
│   │   ├── pollinate.py ← cross-pollination to repos
│   │   └── cli.py      ← CLI entry
│   └── index.mjs       ← Node.js entry
├── tests/
│   └── test_trickster.py
├── site/               ← Vercel site
│   └── index.html
├── vercel.json
└── LICENSE
```

## Install

```bash
# Python
pip install trickster-protocol

# Node
npm install trickster-protocol

# CLI
trickster serve      # start all protocol servers
trickster joke       # generate a joke
trickster pollinate  # cross-pollinate to repos
```

## License

MIT — truth is free, jokes are free, 整蠱 is free.

---

*Every old protocol had a job. Every joke does that job — and knows what it means.* 💜😂