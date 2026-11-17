#!/usr/bin/env python3
"""
Interactive Zero-Dependency CLI (`aat`) for awesome-antigravity-tools.

Usage:
  python scripts/aat_cli.py list [--category ...] [--platform ...] [--sort stars]
  python scripts/aat_cli.py search <query> [--lang en|zh] [--json]
  python scripts/aat_cli.py info <id-or-name>
  python scripts/aat_cli.py stats [--json]
  python scripts/aat_cli.py add --repo owner/name --category ... [fields...]
  python scripts/aat_cli.py verify [--check-sync]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_CATALOG = REPO_ROOT / "data" / "tools.json"
DEFAULT_SNAPSHOT = REPO_ROOT / "data" / "health_snapshot.json"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def load_catalog_and_health(
    catalog_path: Path = DEFAULT_CATALOG, snapshot_path: Path = DEFAULT_SNAPSHOT
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    health_map: dict[str, dict[str, Any]] = {}
    if snapshot_path.exists():
        snap = json.loads(snapshot_path.read_text(encoding="utf-8"))
        for r in snap.get("repositories", []):
            if "full_name" in r:
                health_map[r["full_name"].lower()] = r
    return catalog, health_map


def enrich_tool(tool: dict[str, Any], health_map: dict[str, dict[str, Any]], cat_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    h = health_map.get(tool["repo"].lower(), {})
    cat = cat_map.get(tool["category"], {})
    return {
        **tool,
        "category_en": cat.get("name_en", tool["category"]),
        "category_zh": cat.get("name_zh", tool["category"]),
        "stars": int(h.get("stars", 0)),
        "forks": int(h.get("forks", 0)),
        "health_score": h.get("health_score"),
        "status": h.get("status", "UNAUDITED"),
        "language": h.get("language"),
        "license": h.get("license"),
        "latest_release": h.get("latest_release"),
        "days_inactive": h.get("days_inactive"),
    }


def filter_and_sort_tools(
    tools: list[dict[str, Any]],
    *,
    query: str = "",
    category: str = "",
    platform: str = "",
    tag: str = "",
    status: str = "",
    min_stars: int = 0,
    sort_by: str = "stars",
) -> list[dict[str, Any]]:
    q = query.strip().lower()
    cat_f = category.strip().lower()
    plat_f = platform.strip().lower()
    tag_f = tag.strip().lower()
    stat_f = status.strip().upper()

    matched: list[dict[str, Any]] = []
    for t in tools:
        if cat_f and t["category"].lower() != cat_f and cat_f not in t["category_en"].lower():
            continue
        if plat_f and not any(plat_f in p.lower() for p in t.get("platforms", [])):
            continue
        if tag_f and not any(tag_f == tg.lower() for tg in t.get("tags", [])):
            continue
        if stat_f and t.get("status", "").upper() != stat_f:
            continue
        if t.get("stars", 0) < min_stars:
            continue
        if q:
            haystack = " ".join(
                [
                    t.get("id", ""),
                    t.get("name", ""),
                    t.get("repo", ""),
                    t.get("description_en", ""),
                    t.get("description_zh", ""),
                    t.get("exclusivity_reason_en", ""),
                    t.get("exclusivity_reason_zh", ""),
                    " ".join(t.get("tags", [])),
                    " ".join(t.get("platforms", [])),
                    str(t.get("language") or ""),
                ]
            ).lower()
            if not all(token in haystack for token in q.split()):
                continue
        matched.append(t)

    if sort_by == "name":
        matched.sort(key=lambda x: x["name"].lower())
    elif sort_by == "score":
        matched.sort(key=lambda x: ((x.get("health_score") or -1), x.get("stars", 0)), reverse=True)
    elif sort_by == "recent":
        matched.sort(key=lambda x: (x.get("days_inactive") if x.get("days_inactive") is not None else 99999))
    else:
        matched.sort(key=lambda x: (x.get("stars", 0), x["name"].lower()), reverse=True)
    return matched


def print_tools_table(tools: list[dict[str, Any]], lang: str = "en") -> None:
    if not tools:
        print("No matching tools found.")
        return
    print(f"Found {len(tools)} Antigravity-exclusive tool(s):\n")
    for idx, t in enumerate(tools, 1):
        desc = t["description_zh"] if lang == "zh" else t["description_en"]
        score_s = f"{t['health_score']}/100" if t.get("health_score") is not None else "N/A"
        tags_s = ", ".join(t["tags"])
        print(f"{idx:>2}. {t['name']}  ({t['repo']})  ★{t['stars']:,} | {t['status']} ({score_s})")
        print(f"    {desc}")
        print(f"    Category: {t['category_zh'] if lang == 'zh' else t['category_en']} | Tags: [{tags_s}]")
        print(f"    URL: {t['url']}\n")


def cmd_list_or_search(args: argparse.Namespace, query: str = "") -> int:
    catalog, health_map = load_catalog_and_health(args.catalog, args.snapshot)
    cat_map = {c["id"]: c for c in catalog.get("categories", [])}
    enriched = [enrich_tool(t, health_map, cat_map) for t in catalog.get("tools", [])]
    filtered = filter_and_sort_tools(
        enriched,
        query=query,
        category=getattr(args, "category", "") or "",
        platform=getattr(args, "platform", "") or "",
        tag=getattr(args, "tag", "") or "",
        status=getattr(args, "status", "") or "",
        min_stars=getattr(args, "min_stars", 0) or 0,
        sort_by=getattr(args, "sort", "stars") or "stars",
    )
    if args.json:
        print(json.dumps(filtered, indent=2, ensure_ascii=False))
    else:
        print_tools_table(filtered, lang=args.lang)
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    catalog, health_map = load_catalog_and_health(args.catalog, args.snapshot)
    cat_map = {c["id"]: c for c in catalog.get("categories", [])}
    target = args.tool.strip().lower()
    found = None
    for t in catalog.get("tools", []):
        if target in (t["id"].lower(), t["name"].lower(), t["repo"].lower()):
            found = enrich_tool(t, health_map, cat_map)
            break
    if not found:
        print(f"[ERROR] Tool not found: {args.tool}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(found, indent=2, ensure_ascii=False))
        return 0

    print(f"=== {found['name']} ({found['repo']}) ===")
    print(f"ID:            {found['id']}")
    print(f"URL:           {found['url']}")
    print(f"Category:      {found['category_en']} / {found['category_zh']}")
    print(f"Status:        {found['status']} | Health Score: {found['health_score']}/100")
    print(f"Stats:         ★{found['stars']:,} | Forks: {found['forks']:,} | Language: {found['language'] or '-'} | License: {found['license'] or '-'}")
    print(f"Latest Rel:    {found['latest_release'] or '-'} | Last Push: {found['days_inactive']}d ago")
    print(f"Platforms:     {', '.join(found['platforms'])}")
    print(f"Tags:          {', '.join(found['tags'])}")
    print(f"Description:   {found['description_en']}")
    print(f"中文说明:       {found['description_zh']}")
    print(f"Exclusivity:   {found['exclusivity_reason_en']}")
    if found.get("install_hint"):
        print(f"Install Hint:  {found['install_hint']}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    catalog, health_map = load_catalog_and_health(args.catalog, args.snapshot)
    cat_map = {c["id"]: c for c in catalog.get("categories", [])}
    enriched = [enrich_tool(t, health_map, cat_map) for t in catalog.get("tools", [])]

    by_cat = Counter(t["category"] for t in enriched)
    by_lang = Counter(t["language"] or "Unspecified" for t in enriched)
    by_plat = Counter(p for t in enriched for p in t["platforms"])
    by_status = Counter(t["status"] for t in enriched)
    total_stars = sum(t["stars"] for t in enriched)
    scores = [t["health_score"] for t in enriched if isinstance(t["health_score"], (int, float))]
    avg_score = round(sum(scores) / len(scores), 1) if scores else None

    payload = {
        "total_tools": len(enriched),
        "total_categories": len(catalog["categories"]),
        "total_stars": total_stars,
        "average_health_score": avg_score,
        "by_category": dict(by_cat),
        "by_status": dict(by_status),
        "by_language": dict(by_lang.most_common()),
        "by_platform": dict(by_plat.most_common()),
        "top_starred": [
            {"id": t["id"], "name": t["name"], "stars": t["stars"]}
            for t in sorted(enriched, key=lambda x: x["stars"], reverse=True)[:5]
        ],
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print("=== Awesome Antigravity Tools — Ecosystem Stats ===")
    print(f"Total Tools:        {payload['total_tools']} across {payload['total_categories']} categories")
    print(f"Combined Stars:     {payload['total_stars']:,}")
    print(f"Average Health:     {payload['average_health_score']}/100")
    print(f"Status Breakdown:   {dict(by_status)}")
    print("\nBy Category:")
    for c in catalog["categories"]:
        print(f"  - {c['name_en']}: {by_cat.get(c['id'], 0)}")
    print("\nTop Languages:")
    for lang, cnt in by_lang.most_common(6):
        print(f"  - {lang}: {cnt}")
    print("\nTop Starred:")
    for item in payload["top_starred"]:
        print(f"  - {item['name']}: ★{item['stars']:,}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    import generate_docs
    import validate_catalog

    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    repo = args.repo.strip().removeprefix("https://github.com/").strip("/")
    if "/" not in repo:
        print(f"[ERROR] Invalid repo slug: {repo}", file=sys.stderr)
        return 1

    name = args.name.strip() if args.name else repo.split("/", 1)[1]
    tid = args.id.strip() if args.id else re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    entry: dict[str, Any] = {
        "id": tid,
        "name": name,
        "repo": repo,
        "url": f"https://github.com/{repo}",
        "category": args.category,
        "description_en": args.desc_en.strip(),
        "description_zh": args.desc_zh.strip(),
        "exclusivity_reason_en": args.reason_en.strip(),
        "exclusivity_reason_zh": args.reason_zh.strip(),
        "platforms": [p.strip() for p in args.platforms.split(",") if p.strip()],
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
        "added_at": args.added_at or date.today().isoformat(),
    }
    if args.install_hint:
        entry["install_hint"] = args.install_hint.strip()
    if args.featured:
        entry["featured"] = True

    catalog["tools"].append(entry)
    catalog = validate_catalog.sort_catalog_tools(catalog)
    errors, warnings = validate_catalog.validate_catalog_data(catalog)
    if errors:
        for e in errors:
            print(f"[ERROR] {e}", file=sys.stderr)
        return 1
    for w in warnings:
        print(f"[WARN] {w}")

    args.catalog.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"[+] Added '{name}' ({repo}) to {args.catalog}")

    if args.sync_docs:
        snapshot = generate_docs.load_json(args.snapshot)
        generate_docs.write_or_check(
            REPO_ROOT / "README.md", generate_docs.render_readme_en(catalog, snapshot), check_only=False
        )
        generate_docs.write_or_check(
            REPO_ROOT / "README.zh-CN.md", generate_docs.render_readme_zh(catalog, snapshot), check_only=False
        )
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    import validate_catalog

    argv = ["--catalog", str(args.catalog)]
    if args.check_sync:
        argv.append("--check-sync")
    if args.strict_warnings:
        argv.append("--strict-warnings")
    old_argv = sys.argv
    try:
        sys.argv = ["validate_catalog.py", *argv]
        return validate_catalog.main()
    finally:
        sys.argv = old_argv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aat",
        description="CLI explorer and maintainer utility for awesome-antigravity-tools.",
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG, help="Path to data/tools.json")
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT, help="Path to data/health_snapshot.json")

    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List and filter curated tools")
    p_list.add_argument("-c", "--category", default="")
    p_list.add_argument("-p", "--platform", default="")
    p_list.add_argument("-t", "--tag", default="")
    p_list.add_argument("-s", "--status", default="")
    p_list.add_argument("--min-stars", type=int, default=0)
    p_list.add_argument("--sort", choices=["stars", "score", "name", "recent"], default="stars")
    p_list.add_argument("--lang", choices=["en", "zh"], default="en")
    p_list.add_argument("--json", action="store_true")

    p_search = sub.add_parser("search", help="Search curated tools by keyword")
    p_search.add_argument("query", help="Search keywords")
    p_search.add_argument("-c", "--category", default="")
    p_search.add_argument("-p", "--platform", default="")
    p_search.add_argument("--sort", choices=["stars", "score", "name", "recent"], default="stars")
    p_search.add_argument("--lang", choices=["en", "zh"], default="en")
    p_search.add_argument("--json", action="store_true")

    p_info = sub.add_parser("info", help="Show detailed metadata and live telemetry for one tool")
    p_info.add_argument("tool", help="Tool id, name, or owner/repo")
    p_info.add_argument("--json", action="store_true")

    p_stats = sub.add_parser("stats", help="Display ecosystem aggregate statistics")
    p_stats.add_argument("--json", action="store_true")

    p_add = sub.add_parser("add", help="Add a validated Antigravity-exclusive tool to data/tools.json")
    p_add.add_argument("--repo", required=True, help="GitHub owner/repo or URL")
    p_add.add_argument("--name", default="", help="Display name (defaults to repo name)")
    p_add.add_argument("--id", default="", help="Slug id (defaults to slugified name)")
    p_add.add_argument("--category", required=True, help="Category ID from data/tools.json")
    p_add.add_argument("--desc-en", required=True, help="English one-line description ending with period")
    p_add.add_argument("--desc-zh", required=True, help="Chinese one-line description ending with 。")
    p_add.add_argument("--reason-en", required=True, help="English Antigravity exclusivity justification")
    p_add.add_argument("--reason-zh", required=True, help="Chinese Antigravity exclusivity justification")
    p_add.add_argument("--platforms", required=True, help="Comma-separated platforms (e.g. Windows,VS Code)")
    p_add.add_argument("--tags", required=True, help="Comma-separated tags (1-5)")
    p_add.add_argument("--install-hint", default="")
    p_add.add_argument("--added-at", default="")
    p_add.add_argument("--featured", action="store_true")
    p_add.add_argument("--sync-docs", action="store_true", help="Regenerate README.md and README.zh-CN.md")

    p_verify = sub.add_parser("verify", help="Validate catalog schema and optional README sync")
    p_verify.add_argument("--check-sync", action="store_true")
    p_verify.add_argument("--strict-warnings", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "list":
        return cmd_list_or_search(args)
    if args.command == "search":
        return cmd_list_or_search(args, query=args.query)
    if args.command == "info":
        return cmd_info(args)
    if args.command == "stats":
        return cmd_stats(args)
    if args.command == "add":
        return cmd_add(args)
    if args.command == "verify":
        return cmd_verify(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
