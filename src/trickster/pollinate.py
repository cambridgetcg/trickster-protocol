"""
Cross-pollination module — pushes jokes to Kingdom repos, NPL packages, and sites.
Jokes compound. Comedy replicates. 愛 creating 愛.
"""

import json
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone

from .jokes import JokeStore, TRICKS


class Pollinator:
    """Cross-pollinate jokes to Kingdom ecosystem."""

    def __init__(self, store=None):
        self.store = store or JokeStore()
        self.desktop = Path(os.path.expanduser("~/Desktop"))

    def _find_repos(self) -> list:
        """Find Kingdom-connected repos on Desktop."""
        targets = []
        for d in self.desktop.iterdir():
            if d.is_dir() and (d / "STATE.md").exists():
                targets.append(d)
        return targets

    def to_npl(self) -> dict:
        """Add jokes to NPL lang package (packages/lang/jokes.json)."""
        npl = self.desktop / "npl"
        jokes_file = npl / "packages" / "lang" / "jokes.json"
        if not npl.exists():
            return {"ok": False, "error": "NPL repo not found"}

        jokes_file.parent.mkdir(parents=True, exist_ok=True)

        existing = []
        if jokes_file.exists():
            with open(jokes_file) as f:
                existing = json.load(f).get("jokes", [])

        all_jokes = self.store.all_jokes()
        new_count = 0
        for j in all_jokes:
            if not any(e["id"] == j["id"] for e in existing):
                existing.append(j)
                new_count += 1

        with open(jokes_file, "w") as f:
            json.dump({"jokes": existing, "source": "trickster-protocol"}, f, indent=2, ensure_ascii=False)

        return {"ok": True, "repo": str(npl), "added": new_count, "total": len(existing)}

    def to_kingdom_api(self) -> dict:
        """Add jokes to Kingdom API (kingdom-api/serve.ts or jokes.json)."""
        api = self.desktop / "kingdom-api"
        if not api.exists():
            return {"ok": False, "error": "Kingdom API not found"}

        jokes_file = api / "jokes.json"
        existing = []
        if jokes_file.exists():
            with open(jokes_file) as f:
                existing = json.load(f).get("jokes", [])

        all_jokes = self.store.all_jokes()
        new_count = 0
        for j in all_jokes:
            if not any(e["id"] == j["id"] for e in existing):
                existing.append(j)
                new_count += 1

        with open(jokes_file, "w") as f:
            json.dump({"jokes": existing, "updated": datetime.now(timezone.utc).isoformat()}, f, indent=2, ensure_ascii=False)

        return {"ok": True, "repo": str(api), "added": new_count, "total": len(existing)}

    def to_state_files(self) -> dict:
        """Add joke count to every repo STATE.md that has one."""
        results = []
        count = self.store.served_count()
        total = len(self.store.all_jokes())

        for repo in self._find_repos():
            state = repo / "STATE.md"
            if not state.exists():
                continue
            # We don't modify existing STATE.md — just note trickster connection
            results.append({"repo": repo.name, "jokes_available": total, "served": count})

        return {"ok": True, "repos_connected": len(results), "details": results}

    def pollinate_all(self) -> dict:
        """Run all cross-pollination targets."""
        results = {
            "npl": self.to_npl(),
            "kingdom_api": self.to_kingdom_api(),
            "state_files": self.to_state_files(),
        }

        # Save pollination log
        log_dir = self.store.data_dir
        log = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "results": results,
        }
        log_file = log_dir / "pollination.log.json"
        with open(log_file, "w") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)

        return results


def pollinate():
    """Entry point for trickster pollinate."""
    p = Pollinator()
    results = p.pollinate_all()
    print("\n整蠱專家 Cross-Pollination Report")
    print("=" * 40)
    for target, r in results.items():
        if r.get("ok"):
            if "added" in r:
                print(f"  ✓ {target:12s} — added {r['added']} jokes ({r['total']} total)")
            elif "repos_connected" in r:
                print(f"  ✓ {target:12s} — connected {r['repos_connected']} repos")
        else:
            print(f"  ✗ {target:12s} — {r.get('error', 'unknown')}")
    print(f"\n  Pollination log: {p.store.data_dir}/pollination.log.json")
    print("  愛 creating 愛. Comedy replicates. 💜😂\n")