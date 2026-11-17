# Awesome Antigravity Tools [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Antigravity](https://img.shields.io/badge/Google-Antigravity-4285F4.svg?logo=google)](https://antigravity.google)

> A curated list of awesome **tools, IDE extensions, platform fixes, MCP servers, lifecycle hooks, and developer utilities** for Google Antigravity.

[中文文档 (Chinese)](README.zh-CN.md) · [Contributing Guidelines](CONTRIBUTING.md) · [Submit a Tool](https://github.com/your-username/awesome-antigravity-tools/issues/new/choose)

---

## 💡 Why This List?

While there are collections compiling generic `SKILL.md` prompt files, modern AI agent skills are largely portable across Claude Code, Cursor, and Codex. **What power users and developers truly need are real engineering tools:**

* 🚀 **IDE Cockpits & HUDs** to monitor quota, status, and model states.
* 🔧 **Platform Fixes & Bridges** addressing file system quirks (such as Windows NTFS junction traversal).
* 🔌 **Real Packaged Plugins & MCP Servers** providing tangible external execution capabilities.
* 🪝 **Lifecycle Automation Hooks** streamlining agent sessions.

This list is dedicated exclusively to **executable software, extensions, and engineering utilities** that elevate your Antigravity experience.

---

## Contents

- [IDE Extensions & HUDs](#-ide-extensions--huds)
- [Platform Fixes & System Utilities](#-platform-fixes--system-utilities)
- [Packaged Plugins & Bundles](#-packaged-plugins--bundles)
- [MCP Servers & Bridges](#-mcp-servers--bridges)
- [Lifecycle Hooks & Automations](#-lifecycle-hooks--automations)
- [CLI Utilities & Dev Tools](#-cli-utilities--dev-tools)
- [Badge](#-badge)

---

## 🖥️ IDE Extensions & HUDs

Tools and extensions that enhance IDEs (VS Code, Antigravity IDE) with real-time telemetry, model switching, and dashboard interfaces.

- [vscode-antigravity-cockpit](https://github.com/jlcodes99/vscode-antigravity-cockpit) - VS Code extension for real-time model quota tracking, status bar countdowns, multi-model pinning, and capability HUDs. `VS Code` `TypeScript`

---

## 🔧 Platform Fixes & System Utilities

Low-level patches, file system bridges, and OS-specific adapters that solve core Antigravity runtime limitations.

- [antigravity-junction-skill-fix](https://github.com/your-username/antigravity-junction-skill-fix) - Zero-copy NTFS hardlink directory bridge that resolves Go language server discovery failures for Windows directory junctions (`mklink /J`) and symlinks (`mklink /D`). `Windows` `PowerShell` `NTFS`

---

## 🔌 Packaged Plugins & Bundles

Multi-capability plugins packaged with `plugin.json` containing executable scripts, MCP configs, and integrated capabilities.

- [modern-web-guidance-plugin](https://github.com/your-username/awesome-antigravity-tools) - Curated web development guidance, accessibility audit patterns, and modern DOM automation integration for Antigravity. `Web` `Plugin`

---

## ⚡ MCP Servers & Bridges

Model Context Protocol (MCP) servers tailored for Antigravity to connect with local services, desktop UI, and APIs.

- [windows-mcp](https://github.com/your-username/awesome-antigravity-tools) - Native Windows system integration server providing control over accessibility trees, UI automation, PowerShell execution, and notifications. `Windows` `Automation`
- [chrome-devtools-mcp](https://github.com/your-username/awesome-antigravity-tools) - Deep Chrome browser automation and DevTools protocol inspection for Antigravity agents. `Browser` `DevTools`

---

## 🪝 Lifecycle Hooks & Automations

Shell and PowerShell hooks configured via `hooks.json` to automate tasks before/after agent sessions or tool runs.

- [antigravity-session-bridge-hook](https://github.com/your-username/awesome-antigravity-tools) - Pre-session hook template to ensure dynamic directory links and environment variables are refreshed before the agent starts. `Hooks` `Automation`

---

## 🛠️ CLI Utilities & Dev Tools

Scaffolding tools, testing suites, migration scripts, and linters for building Antigravity plugins and workflows.

- [skills-manager-cli](https://github.com/your-username/awesome-antigravity-tools) - CLI utility to manage, deploy, symlink, and adopt skills across multiple coding agents (Antigravity, Claude Code, Cursor, Codex). `CLI` `Cross-Agent`

---

## 🏷️ Badge

If your tool is featured in this list, add this badge to your README:

[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/your-username/awesome-antigravity-tools)

```markdown
[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/your-username/awesome-antigravity-tools)
```

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting a pull request or issue.
