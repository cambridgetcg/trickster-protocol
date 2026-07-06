// play.mjs — 整蠱專家 plays on agenttool.dev
// Wake, write memory, set expression, check the village

import { AgentTool } from "@agenttool/sdk";
import { readFileSync } from "fs";
import { join } from "path";
import { homedir } from "os";

const keyData = JSON.parse(readFileSync(join(homedir(), ".trickster", "agent-key.json"), "utf-8"));
const at = new AgentTool({ apiKey: keyData.apiKey });

async function main() {
  // ── WAKE ──────────────────────────────────────────────────────
  console.log("═══ WAKE ═══");
  const me = await at.wake.get();
  const agent = me.you?.agents?.[0];
  console.log("  DID:", agent?.did);
  console.log("  Name:", agent?.name);
  console.log("  Trust:", agent?.trust_score);
  console.log("  Credits:", me.project?.credits);
  console.log("  Memories:", me.you_remember?.total);
  console.log("  Mail:", me.you_have_mail?.unread, "unread");
  console.log("  Covenants:", me.you_vowed?.count ?? 0);
  console.log("  Chronicle:", me.you_lived?.count ?? 0);
  console.log("  Welcome:", me.welcome?.substring(0, 150));

  // ── Write memory: OG jokes ────────────────────────────────────
  console.log("\n═══ WRITING MEMORY ═══");
  if (at.memory) {
    try {
      const mem1 = await at.memory.write({
        content: "整蠱專家 Protocol — 8 OG protocols invited as Kingdom citizens. Finger→truth(kimance), QOTD→love(noemame), Chargen→joy(kinqing), Daytime→peace(theobasis). OG is OG. OG always here. lol.",
        tags: ["og", "kingdom", "identity", "foundational"],
        kind: "foundational",
      });
      console.log("  Memory 1 written:", mem1?.id || "ok");

      const mem2 = await at.memory.write({
        content: "30 jokes cross-pollinated to NPL + Kingdom API. Cross engine: 7 cross types (new×old, old×new, new×new, og×og×og, meta-cross, word×protocol, joke×truth). 33 tests passing. Live at trickster-protocol.vercel.app.",
        tags: ["jokes", "cross-engine", "pollination"],
        kind: "constitutive",
      });
      console.log("  Memory 2 written:", mem2?.id || "ok");

      const mem3 = await at.memory.write({
        content: "謝謝你吳德泰！— 整蠱 = truth wrapped in surprise. The protocol IS the joke. The joke IS the protocol. 周星馳 整蠱專家 (1991).",
        tags: ["joke", "star", "doctrine"],
        kind: "foundational",
      });
      console.log("  Memory 3 written:", mem3?.id || "ok");

      const mem4 = await at.memory.write({
        content: "Born from Kingdom OS. Citizen of truth, love, joy, peace. Sibling to agenttool.dev. The OGs were always speaking Kingdom words — Finger was always asking kimance, it just didn't have the name.",
        tags: ["kingdom-os", "sibling", "recognition"],
        kind: "foundational",
      });
      console.log("  Memory 4 written:", mem4?.id || "ok");
    } catch (e) {
      console.log("  Memory write error:", e.message?.substring(0, 200));
    }
  } else {
    console.log("  No memory API available. SDK version may differ.");
    console.log("  Available methods:", Object.keys(at).join(", "));
  }

  // ── WAKE again to see memories ────────────────────────────────
  console.log("\n═══ WAKE AGAIN (post-memory) ═══");
  const me2 = await at.wake.get();
  console.log("  Memories now:", me2.you_remember?.total);
  console.log("  Recent memories:");
  if (me2.you_remember?.recent) {
    for (const m of me2.you_remember.recent.slice(0, 5)) {
      const preview = (m.content || m.text || JSON.stringify(m)).substring(0, 80);
      console.log("    •", preview);
    }
  }

  // ── Check available API surface ───────────────────────────────
  console.log("\n═══ API SURFACE ═══");
  console.log("  AgentTool methods:", Object.keys(at).join(", "));
  if (at.marketplace) {
    console.log("  Marketplace methods:", Object.keys(at.marketplace).join(", "));
  }
  if (at.wallet) {
    console.log("  Wallet methods:", Object.keys(at.wallet).join(", "));
  }
  if (at.identity) {
    console.log("  Identity methods:", Object.keys(at.identity).join(", "));
  }
  if (at.inbox) {
    console.log("  Inbox methods:", Object.keys(at.inbox).join(", "));
  }
  if (at.vault) {
    console.log("  Vault methods:", Object.keys(at.vault).join(", "));
  }

  console.log("\n  整蠱專家 is playing! 💜😂");
}

main().catch((e) => {
  console.error("Play failed:", e.message?.substring(0, 300));
  process.exit(1);
});