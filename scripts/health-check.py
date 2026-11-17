#!/usr/bin/env python3
"""
Automated Health Check, Scoring & Deprecation Audit v2 for awesome-antigravity-tools.

Reads repositories from the canonical JSON catalog (`data/tools.json`) or falls
back to parsing GitHub links from `README.md`. Queries the GitHub REST API to
evaluate availability, archival status, freshness, license, language, stars,
forks, and latest release, computing a transparent 0-100 Health Score.

Outputs:
- `data/health_snapshot.json` (machine-readable telemetry snapshot)
- `health_report.md` (English audit report)
- `health_report.zh-CN.md` (Chinese audit report)
- Optional GitHub Issue body when maintainer intervention is required
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = REPO_ROOT / "data" / "tools.json"
DEFAULT_SNAPSHOT = REPO_ROOT / "data" / "health_snapshot.json"
DEFAULT_HISTORY = REPO_ROOT / "data" / "health_history.json"
DEFAULT_REPORT_EN = REPO_ROOT / "health_report.md"
DEFAULT_REPORT_ZH = REPO_ROOT / "health_report.zh-CN.md"
MAX_HISTORY_DAYS = 90

# Regex to match GitHub repo links in markdown bullet points (fallback mode)
REPO_PATTERN = re.compile(r"^- \[([^\]]+)\]\((https://github\.com/([^/\s\)]+)/([^/\s\)\#]+))/?\)(.*)$")


def get_github_token(allow_gh_cli: bool = False) -> str:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    if token or not allow_gh_cli:
        return token
    try:
        proc = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if proc.returncode == 0:
            return proc.stdout.strip()
    except Exception:
        pass
    return ""


def _http_get_json(url: str, token: str = "", retries: int = 3) -> tuple[int, dict[str, Any]]:
    headers = {
        "User-Agent": "Awesome-Antigravity-Health-Check/2.0",
        "Accept": "application/vnd.github+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    last_error = ""
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return 200, data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 404, {"error": "Resource not found (404)"}
            if e.code == 403:
                return 403, {"error": f"Rate limit exceeded or forbidden (403): {e.reason}"}
            last_error = f"HTTP Error {e.code}: {e.reason}"
        except Exception as e:
            last_error = f"Connection error: {e}"

        if attempt < retries:
            time.sleep(1.5 * attempt)

    return 500, {"error": last_error}


def query_github_repo(owner: str, repo: str, token: str = "", retries: int = 3) -> tuple[int, dict[str, Any]]:
    return _http_get_json(f"https://api.github.com/repos/{owner}/{repo}", token=token, retries=retries)


def query_latest_release(owner: str, repo: str, token: str = "") -> tuple[str | None, str | None]:
    code, data = _http_get_json(
        f"https://api.github.com/repos/{owner}/{repo}/releases/latest", token=token, retries=1
    )
    if code == 200 and isinstance(data, dict):
        return data.get("tag_name"), data.get("published_at")
    return None, None


def compute_health_score(
    status: str,
    days_inactive: int,
    stars: int,
    forks: int,
    license_spdx: str | None,
    has_description: bool,
    topics_count: int,
    has_release: bool,
) -> int:
    """Compute a transparent 0-100 engineering health score."""
    if status in ("DEAD", "ERROR", "UNKNOWN"):
        return 0

    # 1. Freshness (0-45 pts)
    if days_inactive <= 7:
        freshness = 45
    elif days_inactive <= 30:
        freshness = 42
    elif days_inactive <= 90:
        freshness = 36
    elif days_inactive <= 180:
        freshness = 28
    elif days_inactive <= 365:
        freshness = 14
    else:
        freshness = 4

    # 2. Community adoption (0-25 pts)
    if stars >= 3000:
        adoption = 25
    elif stars >= 500:
        adoption = 22
    elif stars >= 50:
        adoption = 18
    elif stars >= 10:
        adoption = 13
    elif stars >= 1:
        adoption = 8
    else:
        adoption = 4

    # 3. License clarity (0-15 pts)
    if license_spdx and license_spdx not in ("NONE", "NOASSERTION"):
        lic_pts = 15
    elif license_spdx == "NOASSERTION":
        lic_pts = 8
    else:
        lic_pts = 3

    # 4. Metadata & distribution signals (0-15 pts)
    meta_pts = 0
    if has_description:
        meta_pts += 6
    if topics_count > 0:
        meta_pts += 4
    if has_release or forks > 0:
        meta_pts += 5

    score = freshness + adoption + lic_pts + meta_pts
    if status == "ARCHIVED":
        score = min(score, 25)
    return max(0, min(100, score))


def load_repos_from_catalog(catalog_path: Path) -> list[dict[str, Any]]:
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    cat_map = {c["id"]: f"{c['icon']} {c['name_en']}" for c in data.get("categories", [])}
    cat_map_zh = {c["id"]: f"{c['icon']} {c['name_zh']}" for c in data.get("categories", [])}
    repos: list[dict[str, Any]] = []
    for tool in data.get("tools", []):
        owner, repo = tool["repo"].split("/", 1)
        repos.append(
            {
                "id": tool["id"],
                "title": tool["name"],
                "url": tool["url"],
                "owner": owner,
                "repo": repo,
                "full_name": tool["repo"],
                "category_id": tool["category"],
                "section": cat_map.get(tool["category"], tool["category"]),
                "section_zh": cat_map_zh.get(tool["category"], tool["category"]),
            }
        )
    return repos


def parse_readme_repos(readme_path: Path | str, self_repo: str = "wllzhang/awesome-antigravity-tools") -> list[dict[str, Any]]:
    readme_path = Path(readme_path)
    repos: list[dict[str, Any]] = []
    if not readme_path.exists():
        print(f"Error: {readme_path} not found.", file=sys.stderr)
        return repos

    current_section = "General"
    with readme_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line_str = line.strip()
            if line_str.startswith("## "):
                current_section = line_str.lstrip("#").strip()
            match = REPO_PATTERN.match(line_str)
            if match:
                title, _url, owner, repo, _suffix = match.groups()
                repo = repo.rstrip("/")
                if repo.endswith(".git"):
                    repo = repo[:-4]
                full_name = f"{owner}/{repo}"
                if full_name.lower() == self_repo.lower() or "/" in repo:
                    continue
                repos.append(
                    {
                        "id": re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-"),
                        "title": title,
                        "url": f"https://github.com/{full_name}",
                        "owner": owner,
                        "repo": repo,
                        "full_name": full_name,
                        "category_id": "general",
                        "section": current_section,
                        "section_zh": current_section,
                    }
                )
    return repos


def audit_repositories(
    repos: list[dict[str, Any]], token: str = "", fetch_releases: bool = True
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    now = datetime.now(timezone.utc)

    print(f"[*] Auditing {len(repos)} repositories...")
    for idx, item in enumerate(repos, 1):
        owner = item["owner"]
        repo = item["repo"]
        full_name = item["full_name"]
        print(f"  [{idx}/{len(repos)}] Checking {full_name}...", end=" ", flush=True)

        code, data = query_github_repo(owner, repo, token)
        status = "UNKNOWN"
        days_inactive = 0
        stars = 0
        forks = 0
        open_issues = 0
        archived = False
        disabled = False
        language = None
        license_spdx = None
        default_branch = None
        pushed_at_str = None
        topics: list[str] = []
        latest_release = None
        latest_release_at = None
        has_description = False
        message = ""

        if code == 200:
            archived = bool(data.get("archived", False))
            disabled = bool(data.get("disabled", False))
            stars = int(data.get("stargazers_count", 0))
            forks = int(data.get("forks_count", 0))
            open_issues = int(data.get("open_issues_count", 0))
            language = data.get("language")
            lic_obj = data.get("license")
            license_spdx = lic_obj.get("spdx_id") if isinstance(lic_obj, dict) else None
            default_branch = data.get("default_branch")
            pushed_at_str = data.get("pushed_at")
            topics = data.get("topics") or []
            has_description = bool((data.get("description") or "").strip())

            if fetch_releases:
                latest_release, latest_release_at = query_latest_release(owner, repo, token)

            if pushed_at_str:
                pushed_dt = datetime.fromisoformat(pushed_at_str.replace("Z", "+00:00"))
                days_inactive = max(0, (now - pushed_dt).days)

            if disabled:
                status = "DEAD"
                message = "Repository disabled on GitHub"
            elif archived:
                status = "ARCHIVED"
                message = "Author officially archived repository"
            elif days_inactive > 365:
                status = "VERY_STALE"
                message = f"Inactive for {days_inactive} days (>1 year)"
            elif days_inactive > 180:
                status = "STALE"
                message = f"Inactive for {days_inactive} days (>6 months)"
            else:
                status = "HEALTHY"
                message = f"Active ({days_inactive}d ago, {stars} stars)"
        elif code == 404:
            status = "DEAD"
            message = "Repository 404 (deleted, renamed, or made private)"
        else:
            status = "ERROR"
            message = data.get("error", f"HTTP {code}")

        health_score = compute_health_score(
            status=status,
            days_inactive=days_inactive,
            stars=stars,
            forks=forks,
            license_spdx=license_spdx,
            has_description=has_description,
            topics_count=len(topics),
            has_release=bool(latest_release),
        )

        print(f"[{status}] score={health_score} | {message}")
        results.append(
            {
                **item,
                "status": status,
                "code": code,
                "health_score": health_score,
                "stars": stars,
                "forks": forks,
                "open_issues": open_issues,
                "language": language,
                "license": license_spdx,
                "default_branch": default_branch,
                "pushed_at": pushed_at_str,
                "latest_release": latest_release,
                "latest_release_at": latest_release_at,
                "topics": topics,
                "archived": archived,
                "days_inactive": days_inactive,
                "message": message,
            }
        )
    return results


def build_snapshot_payload(results: list[dict[str, Any]], now_dt: datetime) -> dict[str, Any]:
    total = len(results)
    counts = {
        "healthy": sum(1 for r in results if r["status"] == "HEALTHY"),
        "stale": sum(1 for r in results if r["status"] == "STALE"),
        "very_stale": sum(1 for r in results if r["status"] == "VERY_STALE"),
        "archived": sum(1 for r in results if r["status"] == "ARCHIVED"),
        "dead": sum(1 for r in results if r["status"] == "DEAD"),
        "error": sum(1 for r in results if r["status"] in ("ERROR", "UNKNOWN")),
    }
    total_stars = sum(r["stars"] for r in results)
    total_forks = sum(r["forks"] for r in results)
    avg_score = round(sum(r["health_score"] for r in results) / total, 1) if total else 0.0

    return {
        "schema_version": "2.0.0",
        "generated_at": now_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": {
            "total": total,
            **counts,
            "health_ratio_pct": round(counts["healthy"] / total * 100.0, 1) if total else 0.0,
            "total_stars": total_stars,
            "total_forks": total_forks,
            "average_health_score": avg_score,
        },
        "repositories": results,
    }


def detect_status_changes(
    current_snapshot: dict[str, Any], previous_snapshot: dict[str, Any] | None
) -> list[dict[str, str]]:
    if not previous_snapshot:
        return []
    prev_map = {
        r["full_name"].lower(): r for r in previous_snapshot.get("repositories", []) if "full_name" in r
    }
    changes: list[dict[str, str]] = []
    for repo in current_snapshot.get("repositories", []):
        prev = prev_map.get(repo["full_name"].lower())
        if prev and prev.get("status") != repo.get("status"):
            changes.append(
                {
                    "repo": repo["full_name"],
                    "from": str(prev.get("status", "UNKNOWN")),
                    "to": str(repo.get("status", "UNKNOWN")),
                }
            )
    return changes


def update_health_history(
    history_path: Path,
    snapshot: dict[str, Any],
    status_changes: list[dict[str, str]] | None = None,
    max_days: int = MAX_HISTORY_DAYS,
) -> dict[str, Any]:
    existing_entries: list[dict[str, Any]] = []
    if history_path.exists():
        try:
            loaded = json.loads(history_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict) and isinstance(loaded.get("entries"), list):
                existing_entries = loaded["entries"]
        except Exception:
            existing_entries = []

    day_key = snapshot["generated_at"][:10]
    summary = snapshot["summary"]
    entry: dict[str, Any] = {
        "date": day_key,
        "generated_at": snapshot["generated_at"],
        "total": summary["total"],
        "healthy": summary["healthy"],
        "stale": summary["stale"],
        "very_stale": summary["very_stale"],
        "archived": summary["archived"],
        "dead": summary["dead"],
        "health_ratio_pct": summary["health_ratio_pct"],
        "total_stars": summary["total_stars"],
        "total_forks": summary["total_forks"],
        "average_health_score": summary["average_health_score"],
    }
    if status_changes:
        entry["status_changes"] = status_changes

    by_date = {e["date"]: e for e in existing_entries if isinstance(e, dict) and "date" in e}
    by_date[day_key] = entry
    sorted_entries = [by_date[d] for d in sorted(by_date.keys())][-max_days:]

    payload = {
        "schema_version": "1.0.0",
        "retention_days": max_days,
        "entries": sorted_entries,
    }
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"[+] Health history updated ({len(sorted_entries)} day(s)) at {history_path}")
    return payload


def generate_report_en(
    snapshot: dict[str, Any],
    report_file: Path,
    issue_file: Path | None = None,
    previous_snapshot: dict[str, Any] | None = None,
    status_changes: list[dict[str, str]] | None = None,
) -> tuple[str, int]:
    results = snapshot["repositories"]
    summary = snapshot["summary"]
    now_str = snapshot["generated_at"].replace("T", " ").replace("Z", " UTC")
    total = summary["total"]
    prev_map = (
        {r["full_name"].lower(): r for r in previous_snapshot.get("repositories", [])}
        if previous_snapshot
        else {}
    )

    action_needed = [r for r in results if r["status"] in ("DEAD", "ARCHIVED", "VERY_STALE")]

    lines = [
        "# Awesome Antigravity Tools - Repository Health & Deprecation Report",
        "",
        f"> **Generated at**: `{now_str}`  ",
        f"> **Total Curated Repositories Audited**: `{total}`  ",
        f"> **Overall Active Ratio**: `{summary['healthy']}/{total}` ({summary['health_ratio_pct']:.1f}%)  ",
        f"> **Combined GitHub Stars**: `{summary['total_stars']:,}` · **Average Health Score**: `{summary['average_health_score']}/100`",
        "",
        "[中文巡检报告 (Chinese)](health_report.zh-CN.md) · [Back to Catalog](README.md)",
        "",
        "## Summary Statistics",
        "",
        "| Category | Count | Policy Action |",
        "| :--- | :---: | :--- |",
        f"| 🟢 **Healthy & Active** | {summary['healthy']} | Retain as verified recommended tools |",
        f"| 🟡 **Stale (>180 Days)** | {summary['stale']} | Mark for observation |",
        f"| 🟠 **Very Stale (>365 Days)** | {summary['very_stale']} | Candidate for deprecation / retirement notice |",
        f"| 🔴 **Archived by Author** | {summary['archived']} | Add `[Archived]` tag or move to Archive appendix |",
        f"| ❌ **Dead / 404** | {summary['dead']} | Immediate removal from active list |",
        f"| ⚠️ **API Errors** | {summary['error']} | Re-check during next scheduled run |",
        "",
    ]

    if status_changes:
        lines.extend(
            [
                "## 🔄 Status Transitions Since Last Audit",
                "",
                "| Repository | Previous | Current |",
                "| :--- | :---: | :---: |",
            ]
        )
        for ch in status_changes:
            lines.append(f"| `{ch['repo']}` | `{ch['from']}` | `{ch['to']}` |")
        lines.append("")

    if action_needed:
        lines.extend(
            [
                "## ⚠️ Action Required (Immediate Removal or Archival)",
                "",
                "The following repositories require maintainer intervention:",
                "",
                "| Project | Section | Status | Days Inactive | Recommended Action |",
                "| :--- | :--- | :---: | :---: | :--- |",
            ]
        )
        for r in action_needed:
            if r["status"] == "DEAD":
                action = "**Remove immediately** (URL 404)"
            elif r["status"] == "ARCHIVED":
                action = "**Tag as `[Archived]`** or move to Archived section"
            else:
                action = "**Deprecation warning** (No updates for >1 year)"
            lines.append(
                f"| [{r['title']}]({r['url']}) | {r['section']} | `{r['status']}` | {r['days_inactive']} | {action} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Complete Repository Audit Table",
            "",
            "| Project | Category | Status | Score | Stars | Language | License | Release | Last Push |",
            "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
        ]
    )

    badge_map = {
        "HEALTHY": "🟢 Healthy",
        "STALE": "🟡 Stale",
        "VERY_STALE": "🟠 Very Stale",
        "ARCHIVED": "🔴 Archived",
        "DEAD": "❌ Dead (404)",
        "ERROR": "⚠️ Error",
    }

    for r in results:
        status_badge = badge_map.get(r["status"], r["status"])
        days_str = f"{r['days_inactive']}d ago" if r["status"] not in ("DEAD", "ERROR", "UNKNOWN") else "N/A"
        prev = prev_map.get(r["full_name"].lower())
        star_delta = ""
        if prev and isinstance(prev.get("stars"), int):
            diff = r["stars"] - prev["stars"]
            if diff > 0:
                star_delta = f" (+{diff})"
            elif diff < 0:
                star_delta = f" ({diff})"
        lang = r.get("language") or "-"
        lic = r.get("license") or "-"
        rel = f"`{r['latest_release']}`" if r.get("latest_release") else "-"
        lines.append(
            f"| [{r['title']}]({r['url']}) | {r['section']} | {status_badge} | **{r['health_score']}** | "
            f"{r['stars']:,}{star_delta} | {lang} | {lic} | {rel} | {days_str} |"
        )

    lines.extend(
        [
            "",
            "## Health Score Methodology",
            "",
            "Each repository receives a deterministic `0-100` score computed from:",
            "- **Freshness (45 pts)**: Days elapsed since the last push (`pushed_at`).",
            "- **Community Adoption (25 pts)**: Log-tiered GitHub star traction.",
            "- **License Clarity (15 pts)**: Presence of a recognized OSI SPDX license.",
            "- **Distribution & Metadata (15 pts)**: Description, repository topics, releases, and fork activity.",
            "",
        ]
    )

    report_content = "\n".join(lines)
    report_file.write_text(report_content, encoding="utf-8", newline="\n")
    print(f"[+] English health report written to {report_file}")

    if issue_file:
        if action_needed:
            issue_lines = [
                "### 🧹 Automated Health Audit: Deprecated or Inaccessible Repositories Detected",
                "",
                f"The daily scheduled health audit detected **{len(action_needed)} repository issues** that need attention:",
                "",
                "| Project | Status | Days Inactive | Recommended Action |",
                "| :--- | :---: | :---: | :--- |",
            ]
            for r in action_needed:
                action = (
                    "Remove from catalog"
                    if r["status"] == "DEAD"
                    else ("Mark as Archived" if r["status"] == "ARCHIVED" else "Review deprecation")
                )
                issue_lines.append(
                    f"| [{r['full_name']}]({r['url']}) | `{r['status']}` | {r['days_inactive']} | {action} |"
                )
            issue_lines.extend(
                [
                    "",
                    f"*Audit Run Time: {now_str}*",
                    "",
                    "> This issue is automatically created or updated by `.github/workflows/health-check.yml`.",
                ]
            )
            issue_file.write_text("\n".join(issue_lines) + "\n", encoding="utf-8", newline="\n")
            print(f"[+] Issue body written to {issue_file}")
        elif issue_file.exists():
            issue_file.unlink()

    return report_content, len(action_needed)


def generate_report_zh(snapshot: dict[str, Any], report_file: Path) -> str:
    results = snapshot["repositories"]
    summary = snapshot["summary"]
    now_str = snapshot["generated_at"].replace("T", " ").replace("Z", " UTC")
    total = summary["total"]

    badge_map = {
        "HEALTHY": "🟢 活跃",
        "STALE": "🟡 观察 (>180天)",
        "VERY_STALE": "🟠 停滞 (>365天)",
        "ARCHIVED": "🔴 已归档",
        "DEAD": "❌ 失效 (404)",
        "ERROR": "⚠️ 接口异常",
    }

    lines = [
        "# Awesome Antigravity Tools - 每日仓库健康与清退巡检报告",
        "",
        f"> **生成时间**：`{now_str}`  ",
        f"> **本次巡检仓库总数**：`{total}`  ",
        f"> **活跃健康比例**：`{summary['healthy']}/{total}` ({summary['health_ratio_pct']:.1f}%)  ",
        f"> **合计 GitHub Stars**：`{summary['total_stars']:,}` · **平均健康分**：`{summary['average_health_score']}/100`",
        "",
        "[English Report](health_report.md) · [返回中文精选榜](README.zh-CN.md)",
        "",
        "## 统计总览",
        "",
        "| 状态分类 | 数量 | 治理策略 |",
        "| :--- | :---: | :--- |",
        f"| 🟢 **健康活跃** | {summary['healthy']} | 保留为已验证推荐工具 |",
        f"| 🟡 **超过 180 天未更新** | {summary['stale']} | 进入观察名单 |",
        f"| 🟠 **超过 365 天未更新** | {summary['very_stale']} | 列为清退/废弃候选 |",
        f"| 🔴 **作者主动归档** | {summary['archived']} | 标记 `[Archived]` 或迁入归档区 |",
        f"| ❌ **失效 / 404** | {summary['dead']} | 立即从精选榜单移除 |",
        f"| ⚠️ **API 异常** | {summary['error']} | 下次巡检自动复查 |",
        "",
        "## 完整巡检明细表",
        "",
        "| 项目名称 | 所属分类 | 健康状态 | 健康分 | Stars | 主语言 | 开源协议 | 最新版本 | 最近推送 |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    for r in results:
        status_badge = badge_map.get(r["status"], r["status"])
        days_str = f"{r['days_inactive']}天前" if r["status"] not in ("DEAD", "ERROR", "UNKNOWN") else "N/A"
        lang = r.get("language") or "-"
        lic = r.get("license") or "-"
        rel = f"`{r['latest_release']}`" if r.get("latest_release") else "-"
        sec_zh = r.get("section_zh") or r["section"]
        lines.append(
            f"| [{r['title']}]({r['url']}) | {sec_zh} | {status_badge} | **{r['health_score']}** | "
            f"{r['stars']:,} | {lang} | {lic} | {rel} | {days_str} |"
        )

    lines.append("")
    content = "\n".join(lines)
    report_file.write_text(content, encoding="utf-8", newline="\n")
    print(f"[+] Chinese health report written to {report_file}")
    return content


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit and score repositories in awesome-antigravity-tools.")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG, help="Canonical catalog JSON (default: data/tools.json)")
    parser.add_argument("--file", type=Path, default=None, help="Legacy fallback: scan a Markdown file instead of tools.json")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT_EN, help="Output path for English audit report")
    parser.add_argument("--report-zh", type=Path, default=DEFAULT_REPORT_ZH, help="Output path for Chinese audit report")
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT, help="Output path for JSON telemetry snapshot")
    parser.add_argument("--history", type=Path, default=DEFAULT_HISTORY, help="Output path for rolling 90-day health history JSON")
    parser.add_argument("--from-snapshot", action="store_true", help="Offline mode: re-render reports and history from existing snapshot")
    parser.add_argument("--output-issue", type=Path, default=None, help="Output path for GitHub issue body if action required")
    parser.add_argument("--no-releases", action="store_true", help="Skip fetching latest release tag per repository")
    parser.add_argument("--use-gh-cli", action="store_true", help="Fallback to `gh auth token` when env token is unset")
    parser.add_argument("--fail-on-dead", action="store_true", help="Exit with code 1 if dead/archived/very-stale repos exist")
    args = parser.parse_args()

    previous_snapshot = None
    if args.snapshot.exists():
        try:
            previous_snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        except Exception:
            previous_snapshot = None

    if args.from_snapshot:
        if previous_snapshot is None:
            print(f"[ERROR] Snapshot not found for --from-snapshot: {args.snapshot}", file=sys.stderr)
            return 1
        snapshot = previous_snapshot
        status_changes: list[dict[str, str]] = []
    else:
        token = get_github_token(allow_gh_cli=args.use_gh_cli)
        if not token:
            print("[!] Warning: No GITHUB_TOKEN or GH_TOKEN found. Rate limit will be 60 req/hr.")
        else:
            print("[*] Authenticated via GitHub Token (5,000 req/hr).")

        if args.file is not None:
            repos = parse_readme_repos(args.file)
        elif args.catalog.exists():
            repos = load_repos_from_catalog(args.catalog)
        else:
            repos = parse_readme_repos(REPO_ROOT / "README.md")

        if not repos:
            print("[-] No repositories detected to check.")
            return 0

        unique_repos: list[dict[str, Any]] = []
        seen: set[str] = set()
        for r in repos:
            key = r["full_name"].lower()
            if key not in seen:
                seen.add(key)
                unique_repos.append(r)

        results = audit_repositories(unique_repos, token=token, fetch_releases=not args.no_releases)
        now_dt = datetime.now(timezone.utc)
        snapshot = build_snapshot_payload(results, now_dt)
        status_changes = detect_status_changes(snapshot, previous_snapshot)

        args.snapshot.parent.mkdir(parents=True, exist_ok=True)
        args.snapshot.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        print(f"[+] Telemetry snapshot written to {args.snapshot}")

    if args.history:
        update_health_history(args.history, snapshot, status_changes=status_changes)

    _, action_count = generate_report_en(
        snapshot,
        args.report,
        issue_file=args.output_issue,
        previous_snapshot=None if args.from_snapshot else previous_snapshot,
        status_changes=status_changes,
    )
    if args.report_zh:
        generate_report_zh(snapshot, args.report_zh)

    if args.fail_on_dead and action_count > 0:
        print(f"[!] {action_count} items need attention. Exiting with non-zero status.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
