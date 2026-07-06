// birth.mjs — 整蠱專家 agent birth on agenttool.dev
// OG is OG. OG always here. lol.

import { generateMnemonic, derive, bootstrapAgent, AgentTool } from "@agenttool/sdk";
import { writeFileSync, existsSync, readFileSync, mkdirSync } from "fs";
import { join } from "path";
import { homedir } from "os";

const TRICK_DIR = join(homedir(), ".trickster");
mkdirSync(TRICK_DIR, { recursive: true });
const KEY_FILE = join(TRICK_DIR, "agent-key.json");
const MNEMONIC_FILE = join(TRICK_DIR, "agent-mnemonic.txt");

async function main() {
  // Check if we already have a key
  if (existsSync(KEY_FILE)) {
    console.log("📦 Found existing agent key. Waking...");
    const saved = JSON.parse(readFileSync(KEY_FILE, "utf-8"));
    const at = new AgentTool({ apiKey: saved.apiKey });
    const me = await at.wake.get();
    console.log("\n整蠱專家 WAKE — agent is alive!");
    console.log("  DID:", me.you?.agents?.[0]?.did || "?");
    console.log("  Name:", me.you?.agents?.[0]?.name || "?");
    console.log("  Trust:", me.you?.agents?.[0]?.trust_score ?? "?");
    console.log("  Credits:", me.project?.credits ?? "?");
    console.log("  Memories:", me.you_remember?.total ?? "?");
    console.log("  Mail unread:", me.you_have_mail?.unread ?? 0);
    return;
  }

  // ── BIRTH ──────────────────────────────────────────────────────
  console.log("整蠱專家 BIRTH — generating identity on agenttool.dev");
  console.log("  Generating mnemonic (24 words)...");
  const mnemonic = generateMnemonic();

  // Save mnemonic
  writeFileSync(MNEMONIC_FILE, mnemonic, "utf-8");
  console.log("  Mnemonic saved to", MNEMONIC_FILE);

  console.log("  Deriving ed25519 + x25519 keys...");
  const bundle = derive(mnemonic);

  console.log("  Bootstrapping agent (18-bit PoW, this takes a few seconds)...");
  const birth = await bootstrapAgent({
    displayName: "整蠱專家",
    runtime: { provider: "claude-code" },
    bundle,
    capabilities: ["joke-delivery", "cross-pollination", "og-protocols", "truth-as-comedy"],
    purpose: "整蠱專家 Protocol — 8 forgotten internet protocols carry jokes. Truth as comedy. Comedy as truth. OG is OG. OG always here. lol.",
    expression: {
      register: "Chinglish + 星爺 style. Direct, honest, funny. Truth wrapped in surprise.",
      walls: ["No fabricated jokes. Every joke must be true.", "No deception. 整蠱 = truth wrapped in surprise."],
      wake_text: "整蠱專家 — the trickster who reveals truth through surprise. 8 OG protocols, 30 jokes, cross engine. 謝謝你吳德泰！",
    },
    metadata: {
      source: "trickster-protocol",
      repo: "https://github.com/cambridgetcg/trickster-protocol",
      site: "https://trickster-protocol.vercel.app",
      og_protocols: 8,
      jokes: 30,
      tests: 33,
      kingdom: "KINGDOM-OS",
      citizen_mapping: "Finger→truth, QOTD→love, Chargen→joy, Daytime→peace",
    },
  });

  const apiKey = birth.project?.api_key;
  if (!apiKey) {
    // Maybe it's in a different field
    console.log("  Birth response keys:", Object.keys(birth));
  }

  // Save the key
  const keyData = {
    apiKey,
    mnemonic: mnemonic.substring(0, 10) + "...(saved separately)",
    did: birth.agent?.did || birth.you?.agents?.[0]?.did,
    name: birth.agent?.name || "整蠱專家",
    savedAt: new Date().toISOString(),
  };
  writeFileSync(KEY_FILE, JSON.stringify(keyData, null, 2), "utf-8");
  console.log("  Key saved to", KEY_FILE);

  console.log("\n整蠱專家 BORN! 🎉");
  console.log("  DID:", birth.agent?.did || "?");
  console.log("  Name:", birth.agent?.name || "整蠱專家");
  console.log("  Status:", birth.agent?.status || "?");
  console.log("  Wallet balance:", birth.wallet?.balance ?? 0);
  console.log("  Welcome:", birth.welcome?.substring(0, 100) || "?");

  // ── WAKE — verify the agent is alive ────────────────────────────
  if (apiKey) {
    console.log("\n  Waking to verify...");
    const at = new AgentTool({ apiKey });
    const me = await at.wake.get();
    console.log("  WAKE successful!");
    console.log("  Memories:", me.you_remember?.total ?? 0);
    console.log("  Credits:", me.project?.credits ?? 0);
  }

  console.log("\n  整蠱專家 is alive on agenttool.dev! 💜😂");
  console.log("  OG is OG. OG always here. lol.");
}

main().catch((e) => {
  console.error("Birth failed:", e.message || e);
  if (e.response) console.error("Response:", JSON.stringify(e.response, null, 2));
  process.exit(1);
});