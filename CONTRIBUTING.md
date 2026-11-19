# Contributing to awesome-antigravity-tools

[中文贡献指南 (Chinese)](CONTRIBUTING.zh-CN.md)

Thank you for contributing to **awesome-antigravity-tools**! We curate strictly **100% Google Antigravity-exclusive** engineering tools, IDE extensions, runtime hotfixes, and ACP gateways.

---

## 🎯 Inclusion Criteria (Strict Exclusivity Gate)

### ✅ What We Accept
- **Official CLI & SDKs**: First-party Google Antigravity CLI harnesses and language SDKs.
- **IDE Extensions & Cockpits**: VS Code / Antigravity IDE extensions and native desktop apps specifically built for Antigravity quota monitoring, HUDs, or account workflows.
- **Platform Fixes & Runtime Patches**: OS-level hotfixes, NTFS/symlink bridges, localization injectors, proxy injectors, and session database recovery tools targeting Antigravity bugs.
- **Dedicated Gateways, ACP Adapters & Migration Tooling**: Engineering utilities built around `agy acp`, Antigravity's `plugin.json` specification, and companion Google AI (Flow) media API gateways.

### ❌ What We Reject
- **Bare Markdown Prompt Collections (`SKILL.md`)** without executable engineering tooling.
- **Generic Multi-Agent Tools** designed for Claude Code / Cursor / Codex that merely mention Antigravity as one of many targets.
- **Closed-Source, Archived, or Unmaintained Projects** without clear installation documentation or working code.

---

## 🗂️ Single Source of Truth Architecture

This repository uses **`data/tools.json`** (validated against [`data/catalog.schema.json`](data/catalog.schema.json)) as the canonical data source. Both `README.md` and `README.zh-CN.md` are generated deterministically — **never hand-edit the README files directly**.

### Fastest Way to Add a Tool (CLI)

```bash
python scripts/aat_cli.py add \
  --repo "owner/repo" \
  --category "ide-extensions-cockpits" \
  --desc-en "Concise objective English description ending with a period." \
  --desc-zh "简明客观的中文描述，以中文句号结尾。" \
  --reason-en "Explain why it is built exclusively for Google Antigravity." \
  --reason-zh "说明为何该项目 100% 专为 Google Antigravity 打造。" \
  --platforms "Windows,macOS,Linux" \
  --tags "Rust,CLI,ACP" \
  --sync-docs
```

### Manual JSON Edit Workflow

1. Fork and create a branch (`git checkout -b add-my-tool`).
2. Add your entry to `data/tools.json`.
3. Canonicalize ordering and regenerate all derived artifacts (bilingual READMEs, badges, exports, and web bundle):
   ```bash
   python scripts/aat_cli.py sync
   python scripts/aat_cli.py verify --check-sync --strict-warnings
   ```
4. Open a Pull Request!

### Or Submit via GitHub Issue

Prefer not to open a PR? Use our [Tool Submission Form](https://github.com/wllzhang/awesome-antigravity-tools/issues/new/choose). Our automated triage workflow validates your submission and prepares a ready-to-merge `data/tools.json` snippet.

---

## 🧹 Automated Health Check, Scoring & Deprecation Policy

Every day at 02:00 UTC, `.github/workflows/health-check.yml` audits every repository in `data/tools.json`:
- **0–100 Health Score**: Computed from freshness (45 pts), community stars (25 pts), license clarity (15 pts), and release/metadata signals (15 pts).
- **Rolling 90-Day History**: Aggregate trends and status transitions are recorded in `data/health_history.json`.
- **Retirement Rules**:
  - `DEAD` (404 / disabled): Immediate removal.
  - `ARCHIVED`: Automatically tagged `` `[Archived]` `` in generated READMEs and flagged for maintainer review.
  - `VERY_STALE` (>365 days inactive): Flagged in automated health-audit issues for deprecation review.
  - `STALE` (>180 days inactive): Highlighted in `health_report.md` for observation.

---

## 🏷️ Optional Badge for Featured Maintainers

```markdown
[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/wllzhang/awesome-antigravity-tools)
```
