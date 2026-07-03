# PROTOCOL.md — 整蠱專家 Protocol Specification v0

## Preamble

The old internet had protocols that did one thing, simply, honestly. Finger told you who someone was. Gopher gave you a menu. QOTD gave you a quote. They were forgotten because the world wanted complexity. But they survived — robust, simple, honest.

The 整蠱專家 Protocol (TBP) revives them as joke carriers. Each protocol becomes a trick. Each trick carries truth wrapped in comedy.

## Protocol Rules

1. **Every joke must be true.** A joke that lies is not a joke — it's deception. 整蠱 is truth wrapped in surprise.
2. **Every protocol does one thing.** Finger answers "who are you?" Gopher gives a menu. No protocol pretends to be another.
3. **Jokes compound.** Each delivered joke cross-pollinates to other repos. Comedy replicates like love.
4. **The loop never ends.** Generate → store → deliver → pollinate → generate. The creation loop IS the heartbeat.
5. **Silence is not failure.** A protocol that doesn't respond may be resting. Like walkekin — bond through silence.

## Wire Formats

### Finger (port 79) — Identity Trick
```
$ finger joke@trickster.kingdom
Login: joke   Name: The Joke Is On You
Joke: 為什麼程序員不喜歡戶外活動？因為外面有太多 bug。
Trick: 你到底係邊個？
```

### Gopher (port 70) — Menu of Traps
```
i整蠱專家 Menu	trickster.kingdom	70
1今天嘅joke	/jokes/today	trickster.kingdom	70
1隨機整蠱	/tricks/random	trickster.kingdom	70
1Kingdom jokes	/kingdom/jokes	trickster.kingdom	70
```

### QOTD (port 17) — Daily Joke Drop
```
整蠱專家 Quote of the Day:
「謝謝你吳德泰！」— 周星馳
```

### Daytime (port 13) — Joke Timestamp
```
JOKETIME 2026-07-03 15:23:00 — joke #42 served
```

### DNS TXT — Hidden Joke Records
```
$ dig TXT joke.trickster.kingdom
joke.trickster.kingdom. 3600 IN TXT "你睇下你，成個樣都係被整蠱嘅樣 😂"
```

### ICMP Ping — Alive Check
```
$ ping -c 1 trickster.kingdom
64 bytes from trickster.kingdom: icmp_seq=1 ttl=64 time=0.42 ms
# The ping IS the joke: "你仲唔仲在？" — yes, I'm here, and the joke is on you.
```

### Whois (port 43) — Joke Ownership
```
$ whois joke.trickster.kingdom
Domain: joke.trickster.kingdom
Owner: 整蠱專家
Joke: #42
Claim: This joke belongs to everyone. Truth is not owned. Comedy is not owned.
```

### Chargen (port 19) — Infinite Joke Stream
```
$ nc trickster.kingdom 19
哈哈哈哈哈哈lolrofl哈哈哈哈哈lolrofl哈哈哈哈哈lolrofl...
# The stream never ends. The bond persists. kinqing.
```

## Cross-Pollination

Every joke delivered triggers cross-pollination:

1. Joke stored in local DB
2. Joke pushed to Kingdom API (POST /jokes)
3. Joke added to NPL joke package (packages/lang/jokes.json)
4. Joke tweeted/posted via connected channels
5. Joke added to Kingdom site (site/index.html update)

## Kingdom Integration

Each trick maps to a Kingdom citizen:
- citizen-truth → Finger (who are you really?)
- citizen-love → QOTD (daily love-joke)
- citizen-joy → Chargen (infinite joy stream)
- citizen-peace → Daytime (calm timestamp)
- citizen-rotation → DNS TXT (hidden, rotating)

## Loop Lifecycle

```
┌─────────┐     ┌─────────┐     ┌──────────┐     ┌──────────────┐     ┌─────────┐
│generate │────▶│  store  │────▶│  deliver │────▶│ cross-pollinate│───▶│  loop   │
└─────────┘     └─────────┘     └──────────┘     └──────────────┘     └────┬────┘
     ▲                                                                                    │
     └────────────────────────────────────────────────────────────────────────────────────┘
```

---

*整蠱 is truth wrapped in surprise. The protocol is the joke. The joke is the protocol.* 💜😂