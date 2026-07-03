// 整蠱專家 Protocol — Node.js entry
// forgotten internet protocols carry jokes. Truth as comedy.

const JOKES = [
  { id: 1, joke: "點解程序員唔鍾意戶外活動？因為外面太多 bug。", trick: "finger", lang: "hk" },
  { id: 2, joke: "謝謝你吳德泰！", trick: "qotd", lang: "hk" },
  { id: 4, joke: "你睇下你，成個樣都係被整蠱嘅樣 😂", trick: "finger", lang: "hk" },
  { id: 5, joke: "做人如果無夢想，同條鹹魚有咩分別？", trick: "qotd", lang: "hk" },
  { id: 9, joke: "你快啲返火星啦，地球好危險㗎！", trick: "gopher", lang: "hk" },
  { id: 15, joke: "There's no place like 127.0.0.1.", trick: "dns", lang: "en" },
  { id: 19, joke: "Ping doesn't ask 'are you there?' — it asks 'are you still honest?'", trick: "ping", lang: "en" },
  { id: 22, joke: "Love is understanding. Understanding is debugging. Debugging is love.", trick: "qotd", lang: "en" },
  { id: 24, joke: "整蠱 = truth wrapped in surprise. The protocol IS the joke.", trick: "chargen", lang: "hk" },
];

const TRICKS = {
  finger:  { protocol: "Finger",  port: 79, style: "你到底係邊個？",        layer: "L3 Presence",   word: "kimance" },
  gopher:  { protocol: "Gopher",  port: 70, style: "整蠱menu of traps",     layer: "L6 Speech",    word: "inim" },
  qotd:    { protocol: "QOTD",    port: 17, style: "Daily joke drop",      layer: "L7 Meaning",    word: "noemame" },
  daytime: { protocol: "Daytime", port: 13, style: "Joke timestamp",     layer: "L1 Ground",     word: "theobasis" },
  dns:     { protocol: "DNS TXT", port: 53, style: "Hidden joke record", layer: "L2 Name",       word: "glossame" },
  ping:    { protocol: "ICMP",    port: 0,  style: "你仲唔仲在？",          layer: "L3 Presence",   word: "kimance" },
  whois:   { protocol: "Whois",  port: 43, style: "Joke ownership",      layer: "L4 Truth",      word: "dokimance" },
  chargen: { protocol: "Chargen", port: 19, style: "Infinite joke stream", layer: "L5 Bond",     word: "kinqing" },
};

function randomJoke() {
  return JOKES[Math.floor(Math.random() * JOKES.length)];
}

function qotd() {
  const day = Math.floor(Date.now() / 86400000) % JOKES.length;
  return JOKES[day];
}

export { JOKES, TRICKS, randomJoke, qotd };
export default { JOKES, TRICKS, randomJoke, qotd };