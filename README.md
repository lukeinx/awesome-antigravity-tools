# Awesome Antigravity Tools [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Antigravity](https://img.shields.io/badge/Google-Antigravity-4285F4.svg?logo=google)](https://antigravity.google)

> A curated directory of **engineering tools, IDE cockpits, platform hotfixes, MCP bridges, lifecycle hooks, and performance engines** for Google Antigravity.

[中文文档 (Chinese)](README.zh-CN.md) · [Contributing Guidelines](CONTRIBUTING.md) · [Submit a Tool](https://github.com/wllzhang/awesome-antigravity-tools/issues/new/choose)

---

## 💡 Why This List?

While there are many lists compiling generic `SKILL.md` prompt files, AI agent prompt skills are largely portable across Claude Code, Cursor, and Codex. **What power users and engineers truly need are executable software tools:**

* 🚀 **IDE Cockpits & HUDs** to monitor quota, reset countdowns, and track model metrics.
* 🔧 **Platform Fixes & System Utilities** resolving OS-level quirks (e.g. Windows NTFS junction traversal, 202MB backend download loops).
* 🔌 **Context, Memory & Optimization Engines** saving 90%+ tokens via AST graphs and local full-text search.
* 🪝 **Lifecycle Safety Hooks** intercepting dangerous operations and managing runtime environments.
* 🛠️ **CLI Utilities & Orchestrators** coordinating multi-agent clusters across hosts legitimately without proxy pools.

This directory is dedicated exclusively to **executable software, extensions, and engineering utilities** that elevate your Antigravity experience.

---

## Contents

- [IDE Extensions & Cockpits](#-ide-extensions--cockpits)
- [Platform Fixes & System Utilities](#-platform-fixes--system-utilities)
- [Context, Memory & Optimization Engines](#-context-memory--optimization-engines)
- [Lifecycle Hooks & Safety Guards](#-lifecycle-hooks--safety-guards)
- [CLI Utilities & Multi-Agent Orchestration](#-cli-utilities--multi-agent-orchestration)
- [MCP Bridges & Extensions](#-mcp-bridges--extensions)
- [Badge](#-badge)

---

## 🖥️ IDE Extensions & Cockpits

Tools and extensions that enhance IDEs (VS Code, Antigravity IDE) with real-time telemetry, model switching, and dashboard interfaces.

- [Antigravity-Manager](https://github.com/lbjlaq/Antigravity-Manager) - Professional native desktop account manager and one-click switcher for Antigravity built with Tauri v2 and React. `Desktop` `Rust` `Tauri`
- [AntigravityQuotaWatcher](https://github.com/wusimpl/AntigravityQuotaWatcher) - Popular VS Code extension for continuous monitoring and status bar alerts of Antigravity AI model quotas. `VS Code` `IDE`
- [pilothouse](https://github.com/aemresrbyk/pilothouse) - Unified desktop cockpit with tabbed embedded terminals for Antigravity CLI, Claude Code, and Codex with mobile push notifications and encrypted approvals. `Desktop` `React 19` `Electron`
- [token-monitor](https://github.com/Javis603/token-monitor) - Local-first desktop widget tracking real-time token usage, costs, and limits across Antigravity and coding tools. `Desktop` `Widget`
- [vscode-antigravity-cockpit](https://github.com/jlcodes99/vscode-antigravity-cockpit) - VS Code extension for real-time model quota tracking, status bar countdowns, multi-model pinning, and capability HUDs. `VS Code` `TypeScript`

---

## 🔧 Platform Fixes & System Utilities

Low-level patches, file system bridges, and OS-specific hotfixes resolving core Antigravity runtime limitations.

- [antigravity_bypass](https://github.com/Futureppo/antigravity_bypass) - Hotfix patch raising local MCP tool limits to 8192 in Antigravity IDE and Windows desktop client with automated backup and restore. `Windows` `Patch`
- [antigravity-conversation-fix](https://github.com/FutureisinPast/antigravity-conversation-fix) - Repairs corrupted session databases, missing threads, and out-of-order conversation history. `IDE` `Fix`
- [antigravity-junction-skill-fix](https://github.com/wllzhang/antigravity-junction-skill-fix) - Zero-copy NTFS hardlink directory bridge that resolves Go language server discovery failures for Windows directory junctions (`mklink /J`) and symlinks (`mklink /D`). `Windows` `PowerShell` `NTFS`
- [vscode-antigravity-backend-fix](https://github.com/HeshamNoaman/vscode-antigravity-backend-fix) - Hotfix for the official VS Code Antigravity extension resolving the repeated ~202 MB `agy.exe` background download loop caused by Windows Defender timeouts. `Windows` `Node.js` `PowerShell`

---

## 🔌 Context, Memory & Optimization Engines

High-performance local engines that compress context, build codebase knowledge graphs, and preserve long-term session memory.

- [codegraph](https://github.com/colbymchenry/codegraph) - Pre-indexed 100% offline code knowledge graph auto-syncing on changes for Antigravity to slash token use and redundant tool calls. `Code-Intelligence` `Graph`
- [context-mode](https://github.com/mksglu/context-mode) - Local plugin using SQLite FTS5 to keep bulky tool outputs out of your agent's context window, cutting token consumption by up to 99%. `Plugin` `Performance`
- [LongMemory](https://github.com/CaviraOSS/LongMemory) - Local persistent memory store and vectorless recall engine across agent sessions. `Memory` `Plugin`
- [memorix](https://github.com/AVIDS2/memorix) - Lightweight cross-agent shared memory layer operating seamlessly over Model Context Protocol. `MCP` `Memory`

---

## 🪝 Lifecycle Hooks & Safety Guards

Shell, Python, and PowerShell hooks configured via `hooks.json` to enforce security, manage sessions, and automate workflows.

- [antigravity-session-bridge-hook](https://github.com/wllzhang/awesome-antigravity-tools) - Pre-session hook template ensuring dynamic directory bridges and environment variables are refreshed before the agent starts. `Hooks` `Automation`
- [cc-safety-net](https://github.com/kenryu42/cc-safety-net) - Pre-execution guard hook blocking destructive Git commands, sensitive credential file reads, and dangerous file deletions before tool calls run. `Hooks` `Security`

---

## 🛠️ CLI Utilities & Multi-Agent Orchestration

Scaffolding tools, gateways, and daemon coordinators for terminal agents and multi-agent fleets.

- [agents-manager](https://github.com/Eden-Sun/agents-manager) - Rust daemon and web UI to coordinate Antigravity (`agy`), Claude Code, and Codex CLI agents across local and SSH hosts with cluster dispatch and mobile push. `Rust` `React` `Orchestration`
- [antigravity-skill-porter](https://github.com/Pranav-Nexus/antigravity-skill-porter) - CLI tool to adapt, wrap, and validate Claude Code and Cursor skills into native Antigravity plugins with `plugin.json`. `CLI` `Converter`
- [ctx](https://github.com/ctxrs/ctx) - High-speed local session recall tool providing Git blame-style chronological history search across machine agent sessions. `CLI` `Rust`
- [liftgate](https://github.com/acking-you/liftgate) - Legitimately run Antigravity as a local OpenAI Responses and Anthropic Messages gateway via official `agy acp` with native GPUI desktop and TUI controls. `Rust` `GPUI` `Gateway`
- [skills-manager-cli](https://github.com/wllzhang/awesome-antigravity-tools) - CLI utility to manage, deploy, symlink, and adopt skills across multiple coding agents (Antigravity, Claude Code, Cursor, Codex). `CLI` `Cross-Agent`

---

## ⚡ MCP Bridges & Extensions

Model Context Protocol (MCP) servers and bridges extending Antigravity to local desktop environments and mobile companions.

- [antigravity-link-extension](https://github.com/cafeTechne/antigravity-link-extension) - Mobile companion mirroring Antigravity IDE sessions to your phone with emergency stop triggers and 9 MCP tools. `Mobile` `MCP`
- [chrome-devtools-mcp](https://github.com/wllzhang/awesome-antigravity-tools) - Deep Chrome browser automation and DevTools protocol inspection for Antigravity agents. `Browser` `DevTools`
- [claude-antigravity-mcp-bridge](https://github.com/im-mahdi-74/claude-antigravity-mcp-bridge) - Dedicated MCP bridge enabling external AI clients to delegate and execute tasks via Antigravity CLI (`agy`). `MCP` `Bridge`
- [windows-mcp](https://github.com/wllzhang/awesome-antigravity-tools) - Native Windows system integration server providing control over accessibility trees, UI automation, PowerShell execution, and notifications. `Windows` `Automation`

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
