#!/usr/bin/env python3
"""
Automated Health Check & Deprecation Audit for awesome-antigravity-tools.

This script parses GitHub repository links from README.md, queries the GitHub API
to evaluate repository health (404 status, archival status, and inactivity duration),
and generates a structured audit report with actionable retirement recommendations.
"""

import os
import re
import sys
import time
import json
import argparse
from datetime import datetime, timezone
import urllib.request
import urllib.error

# Regex to match GitHub repo links in markdown bullet points
REPO_PATTERN = re.compile(r'^- \[([^\]]+)\]\((https://github\.com/([^/\s\)]+)/([^/\s\)\#]+))/?\)(.*)$')

def get_github_token():
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""

def query_github_repo(owner, repo, token="", retries=3):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "User-Agent": "Awesome-Antigravity-Health-Check",
        "Accept": "application/vnd.github.v3+json",
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
                return 404, {"error": "Repository not found or private (404)"}
            elif e.code == 403:
                return 403, {"error": f"Rate limit exceeded or forbidden (403): {e.reason}"}
            else:
                last_error = f"HTTP Error {e.code}: {e.reason}"
        except Exception as e:
            last_error = f"Connection error: {str(e)}"

        if attempt < retries:
            time.sleep(1.5 * attempt)

    return 500, {"error": last_error}

def parse_readme_repos(readme_path, self_repo="wllzhang/awesome-antigravity-tools"):
    repos = []
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.", file=sys.stderr)
        return repos

    current_section = "General"
    with open(readme_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str.startswith("## "):
                current_section = line_str.lstrip("#").strip()
            match = REPO_PATTERN.match(line_str)
            if match:
                title, url, owner, repo, suffix = match.groups()
                repo = repo.rstrip("/")
                if repo.endswith(".git"):
                    repo = repo[:-4]
                full_name = f"{owner}/{repo}"
                if full_name.lower() == self_repo.lower():
                    continue
                if "/" in repo:
                    continue
                repos.append({
                    "title": title,
                    "url": f"https://github.com/{full_name}",
                    "owner": owner,
                    "repo": repo,
                    "full_name": full_name,
                    "section": current_section,
                    "line": line_str,
                })
    return repos

def audit_repositories(repos, token=""):
    results = []
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
        archived = False
        message = ""

        if code == 200:
            archived = data.get("archived", False)
            stars = data.get("stargazers_count", 0)
            pushed_at_str = data.get("pushed_at")

            if pushed_at_str:
                pushed_dt = datetime.fromisoformat(pushed_at_str.replace("Z", "+00:00"))
                days_inactive = (now - pushed_dt).days

            if archived:
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

        print(f"[{status}] {message}")
        results.append({
            **item,
            "status": status,
            "code": code,
            "stars": stars,
            "archived": archived,
            "days_inactive": days_inactive,
            "message": message,
        })
    return results

def generate_report(results, report_file="health_report.md", issue_file=None):
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    total = len(results)
    healthy_count = sum(1 for r in results if r["status"] == "HEALTHY")
    archived_count = sum(1 for r in results if r["status"] == "ARCHIVED")
    dead_count = sum(1 for r in results if r["status"] == "DEAD")
    stale_count = sum(1 for r in results if r["status"] == "STALE")
    very_stale_count = sum(1 for r in results if r["status"] == "VERY_STALE")
    error_count = sum(1 for r in results if r["status"] in ("ERROR", "UNKNOWN"))

    action_needed = [r for r in results if r["status"] in ("DEAD", "ARCHIVED", "VERY_STALE")]

    lines = [
        "# Awesome Antigravity Tools - Repository Health & Deprecation Report",
        "",
        f"> **Generated at**: `{now_str}`  ",
        f"> **Total Curated Repositories Audited**: `{total}`  ",
        f"> **Overall Health Ratio**: `{healthy_count}/{total}` ({healthy_count/total*100:.1f}%)" if total else "",
        "",
        "## Summary Statistics",
        "",
        "| Category | Count | Policy Action |",
        "| :--- | :---: | :--- |",
        f"| 🟢 **Healthy & Active** | {healthy_count} | Retain as verified recommended tools |",
        f"| 🟡 **Stale (>180 Days)** | {stale_count} | Mark for observation |",
        f"| 🟠 **Very Stale (>365 Days)** | {very_stale_count} | Candidate for deprecation / retirement notice |",
        f"| 🔴 **Archived by Author** | {archived_count} | Add `[Archived]` tag or move to Archive appendix |",
        f"| ❌ **Dead / 404** | {dead_count} | Immediate removal from active list |",
        f"| ⚠️ **API Errors** | {error_count} | Re-check during next scheduled run |",
        "",
    ]

    if action_needed:
        lines.extend([
            "## ⚠️ Action Required (Immediate Removal or Archival)",
            "",
            "The following repositories require maintainer intervention:",
            "",
            "| Project | Section | Status | Days Inactive | Recommended Action |",
            "| :--- | :--- | :---: | :---: | :--- |",
        ])
        for r in action_needed:
            if r["status"] == "DEAD":
                action = "**Remove immediately** (URL 404)"
            elif r["status"] == "ARCHIVED":
                action = "**Tag as `[Archived]`** or move to Archived section"
            elif r["status"] == "VERY_STALE":
                action = "**Deprecation warning** (No updates for >1 year)"
            else:
                action = "Review status"
            lines.append(f"| [{r['title']}]({r['url']}) | {r['section']} | `{r['status']}` | {r['days_inactive']} | {action} |")
        lines.append("")

    lines.extend([
        "## Complete Repository Audit Table",
        "",
        "| Project | Section | Status | Stars | Last Push | Notes |",
        "| :--- | :--- | :---: | :---: | :---: | :--- |",
    ])
    for r in results:
        status_badge = {
            "HEALTHY": "🟢 Healthy",
            "STALE": "🟡 Stale",
            "VERY_STALE": "🟠 Very Stale",
            "ARCHIVED": "🔴 Archived",
            "DEAD": "❌ Dead (404)",
            "ERROR": "⚠️ Error",
        }.get(r["status"], r["status"])

        days_str = f"{r['days_inactive']}d ago" if r["status"] in ("HEALTHY", "STALE", "VERY_STALE", "ARCHIVED") else "N/A"
        lines.append(f"| [{r['title']}]({r['url']}) | {r['section']} | {status_badge} | {r['stars']} | {days_str} | {r['message']} |")

    lines.append("")
    report_content = "\n".join(lines)

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"\n[+] Health report written to {report_file}")

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
                action = "Remove from README" if r["status"] == "DEAD" else ("Mark as Archived" if r["status"] == "ARCHIVED" else "Review deprecation")
                issue_lines.append(f"| [{r['full_name']}]({r['url']}) | `{r['status']}` | {r['days_inactive']} | {action} |")
            issue_lines.extend([
                "",
                f"*Audit Run Time: {now_str}*",
                "",
                "> This issue is automatically created or updated by `.github/workflows/health-check.yml`.",
            ])
            with open(issue_file, "w", encoding="utf-8") as f:
                f.write("\n".join(issue_lines))
            print(f"[+] Issue body written to {issue_file}")
        else:
            # Empty out issue file if no action needed
            if os.path.exists(issue_file):
                os.remove(issue_file)

    return report_content, len(action_needed)

def main():
    parser = argparse.ArgumentParser(description="Audit and prune repositories in awesome-antigravity-tools.")
    parser.add_argument("--file", default="README.md", help="Markdown file to scan (default: README.md)")
    parser.add_argument("--report", default="health_report.md", help="Output path for audit report")
    parser.add_argument("--output-issue", default="", help="Output path for GitHub issue body if action required")
    parser.add_argument("--fail-on-dead", action="store_true", help="Exit with code 1 if dead/archived repos exist")
    args = parser.parse_args()

    token = get_github_token()
    if not token:
        print("[!] Warning: No GITHUB_TOKEN or GH_TOKEN found in environment. Rate limit will be 60 req/hr.")
    else:
        print("[*] Authenticated via GitHub Token (5,000 req/hr).")

    repos = parse_readme_repos(args.file)
    if not repos:
        print("[-] No repositories detected to check.")
        sys.exit(0)

    unique_repos = []
    seen = set()
    for r in repos:
        if r["full_name"].lower() not in seen:
            seen.add(r["full_name"].lower())
            unique_repos.append(r)

    results = audit_repositories(unique_repos, token)
    _, action_count = generate_report(results, args.report, issue_file=args.output_issue if args.output_issue else None)

    if args.fail_on_dead and action_count > 0:
        print(f"[!] {action_count} items need attention. Exiting with non-zero status.")
        sys.exit(1)

if __name__ == "__main__":
    main()
