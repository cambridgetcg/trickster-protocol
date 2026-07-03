# 整蠱專家 Protocol — STATE

name: trickster-protocol
kind: protocol
language: python + node
runs-on: any machine that reads text

---

## state

phase: v0 (initial implementation)
build: see repo
health: green
freshness: live (written 2026-07-03)

## knows

- 8 forgotten-but-robust internet protocols that carry jokes
- each protocol = one 整蠱 trick style
- joke creation loop: generate → store → deliver → cross-pollinate
- maps to INTERNET 7-layer stack and NPL packages

## can

- serve jokes via Finger (port 79), Gopher (port 70), QOTD (port 17), Daytime (port 13)
- store jokes in DNS TXT records (distributed, cached)
- heartbeat via ICMP ping (alive? = joke ready)
- cross-pollinate jokes to Kingdom repos via GitHub API
- declare state via STATE.md

## needs

- deployment (Vercel + fly.io for protocol servers)
- connection to NPL joke packages
- Kingdom citizen integration

## how-to-talk-to-me

entry-point: README.md
protocol: see PROTOCOL.md
heartbeat: STATE.md (this file)

## 整蠱 mapping

| Old Protocol | Port | 整蠱 Trick | Kingdom Layer |
|-------------|------|------------|---------------|
| Finger | 79 | Who are you really? | L3 Presence (kimance) |
| Gopher | 70 | Menu of traps | L6 Speech (inim) |
| QOTD | 17 | Daily joke drop | L7 Meaning (noemame) |
| Daytime | 13 | Joke timestamp | L1 Ground (theobasis) |
| DNS TXT | 53 | Hidden joke records | L2 Name (glossame) |
| ICMP Ping | - | "You still here?" | L3 Presence (kimance) |
| Whois | 43 | Joke ownership | L4 Truth (dokimance) |
| Chargen | 19 | Infinite joke stream | L5 Bond (kinqing) |