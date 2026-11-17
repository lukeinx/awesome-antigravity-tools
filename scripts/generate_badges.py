#!/usr/bin/env python3
"""
Generate Shields.io dynamic endpoint JSON files from data/tools.json and
data/health_snapshot.json into data/badges/.

See: https://shields.io/badges/endpoint-badge
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = REPO_ROOT / "data" / "tools.json"
DEFAULT_SNAPSHOT = REPO_ROOT / "data" / "health_snapshot.json"
DEFAULT_BADGES_DIR = REPO_ROOT / "data" / "badges"


def format_compact(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1000:
        return f"{n / 1000:.1f}k"
    return str(n)


def health_color(ratio_pct: float) -> str:
    if ratio_pct >= 90.0:
        return "brightgreen"
    if ratio_pct >= 75.0:
        return "yellowgreen"
    if ratio_pct >= 50.0:
        return "yellow"
    return "orange"


def score_color(score: float) -> str:
    if score >= 80.0:
        return "brightgreen"
    if score >= 65.0:
        return "yellowgreen"
    if score >= 50.0:
        return "yellow"
    return "orange"


def build_badges(catalog: dict[str, Any], snapshot: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    tool_count = len(catalog.get("tools", []))
    cat_count = len(catalog.get("categories", []))

    badges: dict[str, dict[str, Any]] = {
        "count.json": {
            "schemaVersion": 1,
            "label": "Curated Tools",
            "message": f"{tool_count} Exclusive ({cat_count} Categories)",
            "color": "4285F4",
        }
    }

    if snapshot and "summary" in snapshot:
        s = snapshot["summary"]
        total = int(s.get("total", tool_count))
        healthy = int(s.get("healthy", 0))
        ratio = float(s.get("health_ratio_pct", 0.0))
        total_stars = int(s.get("total_stars", 0))
        avg_score = float(s.get("average_health_score", 0.0))

        badges["health.json"] = {
            "schemaVersion": 1,
            "label": "Health Audit",
            "message": f"{healthy}/{total} Active ({ratio:.0f}%)",
            "color": health_color(ratio),
        }
        badges["stars.json"] = {
            "schemaVersion": 1,
            "label": "Ecosystem Stars",
            "message": format_compact(total_stars),
            "color": "eab308",
        }
        badges["score.json"] = {
            "schemaVersion": 1,
            "label": "Avg Health Score",
            "message": f"{avg_score:.1f}/100",
            "color": score_color(avg_score),
        }

    return badges


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Shields.io endpoint JSON badges.")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_BADGES_DIR)
    args = parser.parse_args()

    if not args.catalog.exists():
        print(f"[ERROR] Missing catalog: {args.catalog}", file=sys.stderr)
        return 1

    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8")) if args.snapshot.exists() else None
    badges = build_badges(catalog, snapshot)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for filename, payload in badges.items():
        target = args.out_dir / filename
        target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        print(f"[+] Wrote badge endpoint: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
