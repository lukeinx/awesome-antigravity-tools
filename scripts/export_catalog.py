#!/usr/bin/env python3
"""
Export awesome-antigravity-tools catalog into developer & machine-readable formats:
- `COMPARISON.md`: Side-by-side Markdown comparison matrix
- `data/exports/tools.csv`: Flat tabular CSV for spreadsheet/data analysis
- `data/exports/catalog.jsonld`: Schema.org ItemList JSON-LD for semantic discovery
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = REPO_ROOT / "data" / "tools.json"
DEFAULT_SNAPSHOT = REPO_ROOT / "data" / "health_snapshot.json"


def load_enriched(catalog_path: Path, snapshot_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    health_map: dict[str, dict[str, Any]] = {}
    if snapshot_path.exists():
        snap = json.loads(snapshot_path.read_text(encoding="utf-8"))
        for r in snap.get("repositories", []):
            if "full_name" in r:
                health_map[r["full_name"].lower()] = r

    cat_map = {c["id"]: c for c in catalog.get("categories", [])}
    rows: list[dict[str, Any]] = []
    for tool in catalog.get("tools", []):
        h = health_map.get(tool["repo"].lower(), {})
        cat = cat_map.get(tool["category"], {})
        rows.append(
            {
                **tool,
                "category_en": cat.get("name_en", tool["category"]),
                "category_icon": cat.get("icon", ""),
                "status": h.get("status", "UNAUDITED"),
                "health_score": h.get("health_score"),
                "stars": int(h.get("stars", 0)),
                "forks": int(h.get("forks", 0)),
                "language": h.get("language") or "-",
                "license": h.get("license") or "-",
                "latest_release": h.get("latest_release") or "-",
                "days_inactive": h.get("days_inactive"),
            }
        )
    return catalog, rows


def render_comparison_md(catalog: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        "<!-- AUTO-GENERATED FROM data/tools.json BY scripts/export_catalog.py — DO NOT EDIT DIRECTLY -->",
        "",
        "# Awesome Antigravity Tools — Comparison Matrix",
        "",
        "[Back to README](README.md) · [中文文档](README.zh-CN.md) · [Health Audit Report](health_report.md) · [CSV Export](data/exports/tools.csv)",
        "",
        "> Side-by-side comparison of all strictly Antigravity-exclusive tools sorted by category and GitHub stars.",
        "",
    ]

    for cat in catalog["categories"]:
        cat_rows = [r for r in rows if r["category"] == cat["id"]]
        cat_rows.sort(key=lambda r: (r["stars"], r["name"].lower()), reverse=True)
        if not cat_rows:
            continue
        lines.extend(
            [
                f"## {cat['icon']} {cat['name_en']}",
                "",
                "| Tool | Status | Score | Stars | Language | License | Release | Platforms |",
                "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |",
            ]
        )
        for r in cat_rows:
            score_s = f"**{r['health_score']}**" if r["health_score"] is not None else "-"
            rel_s = f"`{r['latest_release']}`" if r["latest_release"] != "-" else "-"
            plats = ", ".join(r["platforms"])
            lines.append(
                f"| [{r['name']}]({r['url']}) | `{r['status']}` | {score_s} | {r['stars']:,} | "
                f"{r['language']} | {r['license']} | {rel_s} | {plats} |"
            )
        lines.append("")

    return "\n".join(lines)


def render_csv(rows: list[dict[str, Any]]) -> str:
    buf = io.StringIO()
    fields = [
        "id",
        "name",
        "repo",
        "url",
        "category",
        "category_en",
        "status",
        "health_score",
        "stars",
        "forks",
        "language",
        "license",
        "latest_release",
        "days_inactive",
        "platforms",
        "tags",
        "added_at",
        "description_en",
    ]
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for r in rows:
        writer.writerow(
            {
                **{k: r.get(k, "") for k in fields},
                "platforms": "; ".join(r.get("platforms", [])),
                "tags": "; ".join(r.get("tags", [])),
            }
        )
    return buf.getvalue()


def render_jsonld(catalog: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Awesome Antigravity Tools",
        "description": "Strictly curated directory of 100% Google Antigravity-exclusive engineering tools, IDE extensions, runtime hotfixes, and ACP gateways.",
        "url": f"https://github.com/{catalog['repository']}",
        "numberOfItems": len(rows),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx,
                "item": {
                    "@type": "SoftwareApplication",
                    "name": r["name"],
                    "url": r["url"],
                    "applicationCategory": r["category_en"],
                    "operatingSystem": ", ".join(r["platforms"]),
                    "description": r["description_en"],
                    "keywords": ", ".join(r["tags"]),
                },
            }
            for idx, r in enumerate(rows, 1)
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def write_or_check(path: Path, content: str, check_only: bool) -> bool:
    if check_only:
        if not path.exists():
            print(f"[FAIL] Missing export file: {path}", file=sys.stderr)
            return False
        current = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        if current != content:
            print(f"[FAIL] Out of sync export: {path} (run `python scripts/export_catalog.py`)", file=sys.stderr)
            return False
        print(f"[OK] Export in sync: {path}")
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"[+] Wrote export: {path}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Export catalog to Markdown matrix, CSV, and JSON-LD.")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    catalog, rows = load_enriched(args.catalog, args.snapshot)
    targets = {
        REPO_ROOT / "COMPARISON.md": render_comparison_md(catalog, rows),
        REPO_ROOT / "data" / "exports" / "tools.csv": render_csv(rows),
        REPO_ROOT / "data" / "exports" / "catalog.jsonld": render_jsonld(catalog, rows),
    }
    ok = all(write_or_check(p, content, args.check) for p, content in targets.items())
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
