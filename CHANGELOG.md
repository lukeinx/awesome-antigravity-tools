# Changelog

All notable changes to **awesome-antigravity-tools** are documented in this file.

## [2.0.0] - 2026-11-18

A complete architectural evolution from a hand-edited Markdown list into a schema-validated, self-auditing, bilingual Antigravity-exclusive engineering index platform.

### Added
- **Single Source of Truth (`data/tools.json` + `data/catalog.schema.json`)**: Canonical JSON catalog with strict schema validation, bilingual EN/ZH descriptions, explicit Antigravity exclusivity rationales, platform enums, tags, and install hints.
- **Expanded Curated Catalog (10 → 21 Verified Tools across 4 Categories)**: Added `Official CLI & SDKs` (`antigravity-cli`, `antigravity-sdk-python`), plus live-verified Antigravity-exclusive tools (`AntigravityManager`, `antigravity-panel`, `Antigravity-Chinese-Localization`, `antigravity-fixer`, `antigravity-proxy`, `ACP-Ant`, `agy-acp`, `antigravity-acp`, `refined-antigravity-acp`), representing 59,000+ combined GitHub stars with 0 generic cross-agent padding.
- **Deterministic Bilingual Generator (`scripts/generate_docs.py`)**: Generates `README.md` and `README.zh-CN.md` with guaranteed EN/ZH parity, alphabetical ordering, live Ecosystem Pulse metrics, and `--check` CI sync verification.
- **Strict Zero-Dependency Validator (`scripts/validate_catalog.py`)**: Enforces schema compliance, duplicate/self-reference checks, URL integrity, punctuation & anti-hyperbole rules, canonical sorting (`--fix-order`), and README sync checks.
- **Health Engine v2 (`scripts/health-check.py`)**: Adds deterministic `0–100` Health Score, richer GitHub metadata (stars, forks, language, SPDX license, latest release), machine-readable `data/health_snapshot.json`, bilingual audit reports (`health_report.md` & `health_report.zh-CN.md`), rolling 90-day trend history (`data/health_history.json`), status transition diffing, and offline `--from-snapshot` mode.
- **Shields.io Dynamic Endpoint Badges (`scripts/generate_badges.py`)**: Emits `data/badges/{count,health,stars,score}.json`.
- **Candidate Discovery Radar (`scripts/discover_candidates.py`)**: Automated GitHub search & Antigravity-exclusivity heuristic scorer to surface emerging native tools while filtering out prompt dumps and multi-agent noise.
- **Interactive Catalog CLI (`scripts/aat_cli.py`)**: Zero-dependency CLI supporting `list`, `search`, `info`, `stats`, `add --sync-docs`, and `verify`.
- **Submission Triage Parser (`scripts/parse_submission.py`)**: Converts `.github/ISSUE_TEMPLATE/submit_tool.yml` issues into validated `data/tools.json` snippets with live GitHub verification.
- **Interactive GitHub Pages Web Explorer (`docs/`)**: Zero-framework bilingual directory (`index.html`, `styles.css`, `app.js`, `catalog-logic.js`, `insights.js`) featuring live search, category/platform/status filtering, sorting, native `<dialog closedby="any">` modals with scroll containment, collapsible Ecosystem Insights charts, 3-tool side-by-side comparison drawer, URL deep-linking, keyboard navigation (`/`, `j`/`k`, `l`), print styles, RSS feed (`docs/feed.xml`), sitemap, and JSON bundle (`docs/catalog-bundle.json`).
- **Exports & Developer Ergonomics**: Added `scripts/export_catalog.py` (`COMPARISON.md`, `data/exports/tools.csv`, `data/exports/catalog.jsonld`), `scripts/dev.ps1`, `Makefile`, `pyproject.toml`, and `CONTRIBUTING.zh-CN.md`.
- **Automated Test Suite (`tests/`) & CI/CD Workflows**: Added 17 Python `unittest` tests + 5 Node.js `node:test` frontend tests, upgraded `lint-and-links.yml` and `health-check.yml`, and added `pages.yml` and `submission-triage.yml`.

## [1.0.0] - 2026-11-17

- Initial release with 10 curated Antigravity-exclusive repositories, bilingual READMEs, and initial daily GitHub Actions health check workflow.
