# Awesome Antigravity Tools (Antigravity 专有工程工具精选榜) [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![每日健康巡检](https://github.com/wllzhang/awesome-antigravity-tools/actions/workflows/health-check.yml/badge.svg)](https://github.com/wllzhang/awesome-antigravity-tools/actions/workflows/health-check.yml)
[![巡检状态](https://img.shields.io/badge/巡检状态-100%25%20验证-brightgreen)](health_report.md)
[![Antigravity](https://img.shields.io/badge/Google-Antigravity-4285F4.svg?logo=google)](https://antigravity.google)

> 纯粹且极致：只收录 **100% 专为 Google Antigravity 设计研发** 的原生 IDE 扩展、底层系统补丁、运行时热修补与专用工程网关。

[English Documentation](README.md) · [贡献指南](CONTRIBUTING.md) · [每日健康与清退报告](health_report.md) · [提交新工具](https://github.com/wllzhang/awesome-antigravity-tools/issues/new/choose)

---

## 🎯 我们的纯粹性原则：严拒泛用充数，只收专有原生

当前 AI 编程领域的绝大多数 Awesome 列表充斥着两大臃肿噪音：
1. **纯 Markdown 提示词堆砌**（`SKILL.md`）：在 Claude Code、Cursor、Codex 间无差别通用，毫无工程壁垒；
2. **跨平台泛用工具贴牌**：原本为 Claude Code 或通用 LLM 开发，仅在 README 里贴一个“Antigravity”关键词引流。

**本项目坚决拒绝一切泛用充数。** 列表中收录的每一个项目，**其核心使命 100% 专为 Google Antigravity 而生**：
- 专为 Antigravity IDE、官方 CLI (`agy`) 或 `agy acp` 底层协议深度研发；
- 正面攻克 Antigravity 运行时的特定缺陷、系统级死锁或配额盲区。

---

## 目录

- [🖥️ IDE 扩展与专属控制台](#️-ide-扩展与专属控制台)
- [🔧 平台补丁与底层运行时修复](#-平台补丁与底层运行时修复)
- [🔌 专用网关与工程迁移工具](#-专用网关与工程迁移工具)
- [🏷️ 项目徽章 (Badge)](#️-项目徽章-badge)

---

## 🖥️ IDE 扩展与专属控制台

专为 Antigravity 模型配额监控、状态栏倒计时与账号管理打造的桌面应用与扩展。

- [Antigravity-Manager](https://github.com/lbjlaq/Antigravity-Manager) - 基于 Rust (Tauri v2) + React 构建的专业桌面级 Antigravity 账号管理与一键切换工具。 `Desktop` `Rust` `Tauri`
- [antigravity-link-extension](https://github.com/cafeTechne/antigravity-link-extension) - 专为 Antigravity IDE 打造的手机伴侣扩展，实时镜像会话进度，支持手机端紧急终止并提供 9 种 MCP 工具操作。 `Mobile` `Antigravity-IDE`
- [AntigravityQuotaWatcher](https://github.com/wusimpl/AntigravityQuotaWatcher) - 长期维护的高星 Antigravity AI 模型配额观察与状态栏提示插件。 `VS Code` `IDE`
- [vscode-antigravity-cockpit](https://github.com/jlcodes99/vscode-antigravity-cockpit) - Antigravity 标杆级 VS Code 扩展，支持多模型配额实时监控、状态栏倒计时提示、多模型置顶及模型能力 HUD。 `VS Code` `TypeScript`

---

## 🔧 平台补丁与底层运行时修复

正面攻克 Antigravity 官方客户端特定缺陷、操作系统级符号链接失效与进程死锁的热修复工具。

- [antigravity_bypass](https://github.com/Futureppo/antigravity_bypass) - 底层限制解除补丁，将 Antigravity IDE 本地 MCP 工具数量上限安全提升至 8192，带自动备份与一键还原。 `Windows` `Patch`
- [antigravity-conversation-fix](https://github.com/FutureisinPast/antigravity-conversation-fix) - 修复 Antigravity 会话数据损坏、历史乱序与线程丢失的专用修复工具。 `IDE` `Fix`
- [antigravity-junction-skill-fix](https://github.com/wllzhang/antigravity-junction-skill-fix) - 零磁盘占用 NTFS 硬链接目录桥接工具，彻底解决 Antigravity Go Language Server 无法加载 Windows 目录联接 (`mklink /J`) 与符号链接 (`mklink /D`) 的硬伤问题。 `Windows` `PowerShell` `NTFS`
- [vscode-antigravity-backend-fix](https://github.com/HeshamNoaman/vscode-antigravity-backend-fix) - 官方 VS Code 插件热修补工具，彻底解决 Windows Defender 超时引发的每次启动重复下载 ~202MB `agy.exe` 的网络拥堵与进程锁死问题。 `Windows` `Node.js` `PowerShell`

---

## 🔌 专用网关与工程迁移工具

严格围绕 Antigravity 核心协议（`agy acp`）与原生插件规范（`plugin.json`）打造的高性能工程工具。

- [antigravity-skill-porter](https://github.com/Pranav-Nexus/antigravity-skill-porter) - 专门用于将外部技能代码适配并打包为规范 Antigravity 原生插件（自动补全 `plugin.json` 与生命周期配置）的转换脚手架。 `CLI` `Converter`
- [liftgate](https://github.com/acking-you/liftgate) - 专为 Antigravity 官方 `agy acp`（Agent Client Protocol）通道构建的原生 API 网关与 GPUI 桌面控制中心，免除任何账号池与封号风险。 `Rust` `GPUI` `Gateway`

---

## 🏷️ 项目徽章 (Badge)

如果您的工具已被收录到本榜单，欢迎在您的 README 中展示收录徽章：

[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/wllzhang/awesome-antigravity-tools)

```markdown
[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/wllzhang/awesome-antigravity-tools)
```

---

## 🤝 参与贡献

欢迎提交您的专有工具！在提交前请阅读我们的 [贡献指南](CONTRIBUTING.md) 与 [行为准则](CODE_OF_CONDUCT.md)。
