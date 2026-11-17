# Awesome Antigravity Tools [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Daily Health Audit](https://github.com/wllzhang/awesome-antigravity-tools/actions/workflows/health-check.yml/badge.svg)](https://github.com/wllzhang/awesome-antigravity-tools/actions/workflows/health-check.yml)
[![Repository Health](https://img.shields.io/badge/Health%20Audit-100%25%20Verified-brightgreen)](health_report.md)
[![Antigravity](https://img.shields.io/badge/Google-Antigravity-4285F4.svg?logo=google)](https://antigravity.google)

> A strictly curated directory of **100% native, dedicated tools, IDE extensions, runtime hotfixes, and engineering gateways** built exclusively for Google Antigravity.

[中文文档 (Chinese)](README.zh-CN.md) · [Contributing Guidelines](CONTRIBUTING.md) · [Daily Health Report](health_report.md) · [Submit a Tool](https://github.com/wllzhang/awesome-antigravity-tools/issues/new/choose)

---

## 🎯 Our Manifesto: Strictly Antigravity-Exclusive

Most "awesome" lists in the AI agent space are flooded with two types of noise:
1. **Generic Markdown prompt dumps** (`SKILL.md`) that work identically across Claude Code, Cursor, and Codex.
2. **Generic multi-agent tools** that were designed for other platforms and merely slapped "Antigravity" onto their tags.

**This repository rejects all generic padding.** Every single project curated here is **100% dedicated to Google Antigravity**:
- Built specifically for the Antigravity IDE, CLI (`agy`), or `agy acp` protocol.
- Directly fixes critical Antigravity bugs, OS runtime limitations, or telemetry blind spots.

---

## Contents

- [IDE Extensions & Cockpits](#-ide-extensions--cockpits)
- [Platform Fixes & Runtime Patches](#-platform-fixes--runtime-patches)
- [Dedicated Gateways & Migration Tooling](#-dedicated-gateways--migration-tooling)
- [Badge](#-badge)

---

## 🖥️ IDE Extensions & Cockpits

Extensions and desktop applications designed exclusively to monitor Antigravity model quotas, manage accounts, and provide HUD telemetry.

- [Antigravity-Manager](https://github.com/lbjlaq/Antigravity-Manager) - Professional native desktop account manager and one-click switcher for Antigravity built with Tauri v2 (Rust) and React. `Desktop` `Rust` `Tauri`
- [antigravity-link-extension](https://github.com/cafeTechne/antigravity-link-extension) - Mobile companion extension specifically mirroring Antigravity IDE sessions to phone with emergency stop triggers and 9 MCP tools. `Mobile` `Antigravity-IDE`
- [AntigravityQuotaWatcher](https://github.com/wusimpl/AntigravityQuotaWatcher) - Popular VS Code extension for continuous monitoring and status bar alerts of Antigravity AI model quotas. `VS Code` `IDE`
- [vscode-antigravity-cockpit](https://github.com/jlcodes99/vscode-antigravity-cockpit) - Flagship VS Code extension for real-time Antigravity model quota tracking, status bar countdowns, multi-model pinning, and capability HUDs. `VS Code` `TypeScript`

---

## 🔧 Platform Fixes & Runtime Patches

System-level hotfixes and patches solving core Antigravity bugs, file system failures, and runtime limitations.

- [antigravity_bypass](https://github.com/Futureppo/antigravity_bypass) - Runtime patch raising local MCP tool limits to 8192 in Antigravity IDE and Windows desktop client with automated backup and restore. `Windows` `Patch`
- [antigravity-conversation-fix](https://github.com/FutureisinPast/antigravity-conversation-fix) - Repairs corrupted Antigravity session databases, missing threads, and out-of-order conversation history. `IDE` `Fix`
- [antigravity-junction-skill-fix](https://github.com/wllzhang/antigravity-junction-skill-fix) - Zero-copy NTFS hardlink directory bridge that resolves Go language server discovery failures for Windows directory junctions (`mklink /J`) and symlinks (`mklink /D`). `Windows` `PowerShell` `NTFS`
- [vscode-antigravity-backend-fix](https://github.com/HeshamNoaman/vscode-antigravity-backend-fix) - Hotfix for the official VS Code Antigravity extension resolving the repeated ~202 MB `agy.exe` background download loop caused by Windows Defender timeouts. `Windows` `Node.js` `PowerShell`

---

## 🔌 Dedicated Gateways & Migration Tooling

Engineering utilities specifically built around the Antigravity Agent Client Protocol (`agy acp`) and native plugin specifications (`plugin.json`).

- [antigravity-skill-porter](https://github.com/Pranav-Nexus/antigravity-skill-porter) - CLI tool specifically adapting, wrapping, and validating external skills into native Antigravity plugins with `plugin.json` and tool name mapping. `CLI` `Converter`
- [liftgate](https://github.com/acking-you/liftgate) - Legitimately run Antigravity as a local OpenAI Responses and Anthropic Messages gateway via official `agy acp` over stdio with native GPUI desktop and TUI controls. `Rust` `GPUI` `Gateway`

---

## 🏷️ Badge

If your tool is featured in this list, add this badge to your README:

[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/wllzhang/awesome-antigravity-tools)

```markdown
[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/wllzhang/awesome-antigravity-tools)
```

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting a pull request or issue.
