<!-- AUTO-GENERATED FROM data/tools.json BY scripts/generate_docs.py — DO NOT EDIT DIRECTLY -->

# Awesome Antigravity Tools [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Curated Tools](https://img.shields.io/badge/Curated-21%20Tools-4285F4.svg)](#contents)
[![Daily Health Audit](https://github.com/wllzhang/awesome-antigravity-tools/actions/workflows/health-check.yml/badge.svg)](https://github.com/wllzhang/awesome-antigravity-tools/actions/workflows/health-check.yml)
[![Repository Health](https://img.shields.io/badge/Health%20Audit-20/21%20Active%20%2895%25%29-brightgreen)](health_report.md)
[![Antigravity](https://img.shields.io/badge/Google-Antigravity-4285F4.svg?logo=google)](https://antigravity.google)

> A strictly curated, schema-validated directory of **100% native, dedicated tools, IDE extensions, runtime hotfixes, and engineering gateways** built exclusively for Google Antigravity.

[🌐 Interactive Web Explorer](https://wllzhang.github.io/awesome-antigravity-tools/) · [📊 Comparison Matrix](COMPARISON.md) · [中文文档 (Chinese)](README.zh-CN.md) · [Contributing Guidelines](CONTRIBUTING.md) · [Daily Health Report](health_report.md) · [Submit a Tool](https://github.com/wllzhang/awesome-antigravity-tools/issues/new/choose)

---

## 🎯 Our Manifesto: Strictly Antigravity-Exclusive

Most "awesome" lists in the AI agent space are flooded with two types of noise:
1. **Generic Markdown prompt dumps** (`SKILL.md`) that work identically across Claude Code, Cursor, and Codex.
2. **Generic multi-agent tools** that were designed for other platforms and merely slapped "Antigravity" onto their tags.

**This repository rejects all generic padding.** Every single project curated here is **100% dedicated to Google Antigravity**:
- Built specifically for the Antigravity IDE, CLI (`agy`), or `agy acp` protocol.
- Directly fixes critical Antigravity bugs, OS runtime limitations, or telemetry blind spots.
- Verified daily by our automated health audit (`scripts/health-check.py`) and backed by a single-source-of-truth JSON catalog (`data/tools.json`).

> **Ecosystem Pulse**: `21` curated tools across `4` categories · `59.2k` combined GitHub stars · `20/21` active (`95.2%`) · Avg Health Score: `85.1/100` ([Full Audit](health_report.md))

---

## Contents

- [Official CLI & SDKs (2)](#-official-cli--sdks)
- [IDE Extensions & Cockpits (6)](#️-ide-extensions--cockpits)
- [Platform Fixes & Runtime Patches (7)](#-platform-fixes--runtime-patches)
- [Dedicated Gateways, ACP Adapters & Migration Tooling (6)](#-dedicated-gateways-acp-adapters--migration-tooling)
- [Badge](#️-badge)
- [Contributing](#-contributing)

---

## 🚀 Official CLI & SDKs

First-party command-line harnesses and SDKs maintained under `google-antigravity` for terminal workflows and programmatic agent orchestration.

- [antigravity-cli](https://github.com/google-antigravity/antigravity-cli) - Official Antigravity CLI (`agy`) bringing the reasoning, execution, and orchestration capabilities of the Antigravity agent harness directly into the terminal. `Official` `CLI` `Terminal`
- [antigravity-sdk-python](https://github.com/google-antigravity/antigravity-sdk-python) - Official Apache-2.0 Python SDK for building programmatic AI agents and workflows powered directly by Google Antigravity. `Official` `Python` `SDK`

---

## 🖥️ IDE Extensions & Cockpits

Extensions and desktop applications designed exclusively to monitor Antigravity model quotas, manage accounts, and provide HUD telemetry.

- [antigravity-link-extension](https://github.com/cafeTechne/antigravity-link-extension) - Mobile companion extension specifically mirroring Antigravity IDE sessions to phone with emergency stop triggers and 9 MCP tools. `Mobile` `Antigravity-IDE` `MCP`
- [Antigravity-Manager](https://github.com/lbjlaq/Antigravity-Manager) - Native desktop account manager and one-click switcher for Antigravity built with Tauri v2 (Rust) and React. `Desktop` `Rust` `Tauri`
- [antigravity-panel](https://github.com/n2ns/antigravity-panel) - Quota monitor and cache manager for Google Antigravity IDE tracking Gemini, Claude, and GPT limits with usage trend analytics. `VS Code` `TypeScript` `Quota`
- [AntigravityManager](https://github.com/Draculabo/AntigravityManager) - Desktop application for managing Google accounts across Antigravity Classic, Antigravity IDE, and `agy` CLI with real-time quota views. `Desktop` `TypeScript` `Quota`
- [AntigravityQuotaWatcher](https://github.com/wusimpl/AntigravityQuotaWatcher) - VS Code extension for continuous monitoring and status bar alerts of Antigravity AI model quotas. `VS Code` `IDE` `Quota`
- [vscode-antigravity-cockpit](https://github.com/jlcodes99/vscode-antigravity-cockpit) - VS Code extension for real-time Antigravity model quota tracking, status bar countdowns, multi-model pinning, and capability HUDs. `VS Code` `TypeScript` `HUD`

---

## 🔧 Platform Fixes & Runtime Patches

System-level hotfixes, localization injectors, network bridges, and patches solving core Antigravity bugs and OS runtime limitations.

- [Antigravity-Chinese-Localization](https://github.com/antigravity-cn-community/Antigravity-Chinese-Localization) - MIT-licensed one-click Chinese localization toolkit and UI translation patch tailored for Google Antigravity IDE. `Localization` `JavaScript` `Patch`
- [antigravity-conversation-fix](https://github.com/FutureisinPast/antigravity-conversation-fix) - Repairs corrupted Antigravity session databases, missing threads, and out-of-order conversation history. `IDE` `Fix` `Recovery`
- [antigravity-fixer](https://github.com/fulldiagnose/antigravity-fixer) - Automated diagnostic and credential-cleanup utility resolving the Google Antigravity 'not eligible' sign-in and account state error. `Python` `Fix` `Diagnostics`
- [antigravity-junction-skill-fix](https://github.com/wllzhang/antigravity-junction-skill-fix) - Zero-copy NTFS hardlink directory bridge that resolves Go language server discovery failures for Windows directory junctions (`mklink /J`) and symlinks (`mklink /D`). `Windows` `PowerShell` `NTFS`
- [antigravity-proxy](https://github.com/yuaotian/antigravity-proxy) - Transparent Windows DLL-injection proxy utility that routes Antigravity process traffic through SOCKS5/HTTP proxies without requiring TUN mode. `Windows` `C++` `Proxy`
- [antigravity_bypass](https://github.com/Futureppo/antigravity_bypass) - Runtime patch raising local MCP tool limits to 8192 in Antigravity IDE and Windows desktop client with automated backup and restore. `Windows` `Patch` `MCP`
- [vscode-antigravity-backend-fix](https://github.com/HeshamNoaman/vscode-antigravity-backend-fix) - Hotfix for the official VS Code Antigravity extension resolving the repeated ~202 MB `agy.exe` background download loop caused by Windows Defender timeouts. `Windows` `Node.js` `PowerShell`

---

## 🔌 Dedicated Gateways, ACP Adapters & Migration Tooling

Engineering utilities specifically built around the official Antigravity Agent Client Protocol (`agy acp`) and native plugin specifications (`plugin.json`).

- [ACP-Ant](https://github.com/czg86389-hub/ACP-Ant) - OpenAI and Anthropic compatible API server bridging Google's official Antigravity CLI over ACP with per-account proxy and tool-calling support. `Python` `ACP` `Gateway`
- [agy-acp](https://github.com/shindgew/agy-acp) - Apache-2.0 Agent Client Protocol adapter wrapping the official Google Antigravity CLI (`agy`) for ACP-compatible editors. `TypeScript` `ACP` `Adapter`
- [antigravity-acp](https://github.com/shubzkothekar/antigravity-acp) - Bun-powered Agent Client Protocol server for Google Antigravity's `agy` CLI featuring live streaming and session history replay. `TypeScript` `Bun` `ACP`
- [antigravity-skill-porter](https://github.com/Pranav-Nexus/antigravity-skill-porter) - CLI tool specifically adapting, wrapping, and validating external skills into native Antigravity plugins with `plugin.json` and tool name mapping. `CLI` `Converter` `Plugin`
- [liftgate](https://github.com/acking-you/liftgate) - Run Antigravity as a local OpenAI Responses and Anthropic Messages gateway via official `agy acp` over stdio with native GPUI desktop and TUI controls. `Rust` `GPUI` `Gateway`
- [refined-antigravity-acp](https://github.com/simonepri/refined-antigravity-acp) - Drop-in refined Google Antigravity ACP binary wrapper resolving protocol compatibility quirks for external ACP clients. `TypeScript` `ACP` `Wrapper`

---

## 🏷️ Badge

If your tool is featured in this list, add this badge to your README:

[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/wllzhang/awesome-antigravity-tools)

```markdown
[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/wllzhang/awesome-antigravity-tools)
```

---

## 🤝 Contributing

Contributions are welcome! All entries are managed in [`data/tools.json`](data/tools.json) and rendered deterministically into both English and Chinese READMEs via `python scripts/generate_docs.py`.

> **Tip**: This repository also ships as a native Antigravity plugin ([`plugin.json`](plugin.json) + `antigravity-tools-advisor` skill) and CLI (`python scripts/aat_cli.py search <query>`).

Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting a pull request or issue.
