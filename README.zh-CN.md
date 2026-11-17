# Awesome Antigravity Tools (精选工具榜) [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Antigravity](https://img.shields.io/badge/Google-Antigravity-4285F4.svg?logo=google)](https://antigravity.google)

> 汇集 Google Antigravity 生态中优秀的 **IDE 扩展、底层系统补丁、真实插件、MCP 服务器、生命周期钩子与工程开发工具**。

[English Documentation](README.md) · [贡献指南](CONTRIBUTING.md) · [提交新工具](https://github.com/your-username/awesome-antigravity-tools/issues/new/choose)

---

## 💡 为什么要建立这个仓库？

社区中已有一些收集通用 `SKILL.md` 提示词的列表，但随着多 Agent 生态发展，纯文本 Skill 规范在 Claude Code、Cursor、Codex 与 Antigravity 之间已高度通用。

**开发者和深度用户真正迫切需要的是“具有独立执行能力的真实工程工具与扩展”：**

* 🚀 **IDE 监控与状态栏面板**：实时追踪模型配额、重置倒计时与模型能力 HUD。
* 🔧 **底层系统补丁与桥接器**：解决 Windows NTFS 目录链接无法被底层 Go 引擎识别等痛点。
* 🔌 **开箱即用的完整插件与 MCP 服务**：提供代码级外部操作能力。
* 🪝 **生命周期自动化脚本**：在会话启动、工具调用等节点执行自动化流程。

本项目**明确拒绝单纯堆砌纯文本 Prompt/Skill**，专注于收录**真实、可运行、可复用的软件工具与工程扩展**。

---

## 目录

- [🖥️ IDE 扩展与监控面板](#️-ide-扩展与监控面板)
- [🔧 平台补丁与底层系统工具](#-平台补丁与底层系统工具)
- [🔌 打包插件与功能扩展包](#-打包插件与功能扩展包)
- [⚡ MCP 服务器与桥接适配器](#-mcp-服务器与桥接适配器)
- [🪝 生命周期钩子与自动化脚本](#-生命周期钩子与自动化脚本)
- [🛠️ CLI 脚手架与开发者工具](#️-cli-脚手架与开发者工具)
- [🏷️ 项目徽章 (Badge)](#️-项目徽章-badge)

---

## 🖥️ IDE 扩展与监控面板

为 VS Code、Antigravity IDE 增强实时遥测、配额监控和模型交互界面的插件与扩展。

- [vscode-antigravity-cockpit](https://github.com/jlcodes99/vscode-antigravity-cockpit) - VS Code 扩展，支持多模型配额实时监控、状态栏倒计时提示、多模型置顶及模型能力 HUD。 `VS Code` `TypeScript`

---

## 🔧 平台补丁与底层系统工具

针对特定操作系统或底层运行时的桥接工具与修补脚本。

- [antigravity-junction-skill-fix](https://github.com/your-username/antigravity-junction-skill-fix) - 零磁盘占用 NTFS 硬链接目录桥接工具，彻底解决 Antigravity Go Language Server 无法加载 Windows 目录联接 (`mklink /J`) 与符号链接 (`mklink /D`) 的问题。 `Windows` `PowerShell` `NTFS`

---

## 🔌 打包插件与功能扩展包

基于 `plugin.json` 规范打包，内含可执行脚本、MCP 配置与集成能力的综合插件。

- [modern-web-guidance-plugin](https://github.com/your-username/awesome-antigravity-tools) - 针对 Antigravity 的现代前端开发规范、无障碍审查与 DOM 自动化集成插件。 `Web` `Plugin`

---

## ⚡ MCP 服务器与桥接适配器

连接外部服务、桌面系统与专用 API 的模型上下文协议 (MCP) 服务端。

- [windows-mcp](https://github.com/your-username/awesome-antigravity-tools) - 深度集成 Windows 系统无障碍树、UI 自动化、PowerShell 执行与通知推送的专用 MCP 服务。 `Windows` `Automation`
- [chrome-devtools-mcp](https://github.com/your-username/awesome-antigravity-tools) - 为 Antigravity 智能体提供深度 Chrome 浏览器控制与 DevTools 协议调试的 MCP 服务。 `Browser` `DevTools`

---

## 🪝 生命周期钩子与自动化脚本

通过 `hooks.json` 配置的会话前、工具调用前后的自动化处理脚本。

- [antigravity-session-bridge-hook](https://github.com/your-username/awesome-antigravity-tools) - 会话启动前自动同步目录桥接与刷新环境变量的 Hook 模板。 `Hooks` `Automation`

---

## 🛠️ CLI 脚手架与开发者工具

用于构建、测试、迁移和调试 Antigravity 插件的工具套件。

- [skills-manager-cli](https://github.com/your-username/awesome-antigravity-tools) - 跨 Coding Agent (Antigravity, Claude Code, Cursor, Codex) 的技能统一管理与软链接分发 CLI。 `CLI` `Cross-Agent`

---

## 🏷️ 项目徽章 (Badge)

如果您的工具已被收录到本榜单，欢迎在您的 README 中展示收录徽章：

[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/your-username/awesome-antigravity-tools)

```markdown
[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/your-username/awesome-antigravity-tools)
```

---

## 🤝 参与贡献

欢迎提交您的工具！在提交前请阅读我们的 [贡献指南](CONTRIBUTING.md) 与 [行为准则](CODE_OF_CONDUCT.md)。
