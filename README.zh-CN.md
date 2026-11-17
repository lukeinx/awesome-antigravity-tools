# Awesome Antigravity Tools (精选工程工具榜) [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![每日健康巡检](https://github.com/wllzhang/awesome-antigravity-tools/actions/workflows/health-check.yml/badge.svg)](https://github.com/wllzhang/awesome-antigravity-tools/actions/workflows/health-check.yml)
[![仓库健康状态](https://img.shields.io/badge/巡检状态-每日验证-blue)](health_report.md)
[![Antigravity](https://img.shields.io/badge/Google-Antigravity-4285F4.svg?logo=google)](https://antigravity.google)

> 汇集 Google Antigravity 生态中高含金量的 **IDE 控制台、底层系统补丁、上下文优化引擎、生命周期守卫、集群编排与专用 MCP 桥接器**。

[English Documentation](README.md) · [贡献指南](CONTRIBUTING.md) · [每日健康与清退报告](health_report.md) · [提交新工具](https://github.com/wllzhang/awesome-antigravity-tools/issues/new/choose)

---

## 💡 为什么要建立这个精选集？

社区中已有一些收集通用 `SKILL.md` 提示词的列表，但随着多 Agent 生态发展，纯文本 Skill 规范在 Claude Code、Cursor、Codex 与 Antigravity 之间已高度互通。

**真正的开发者与重度用户迫切需要的是具备独立执行能力的软件工具与工程补丁：**

* 🚀 **IDE 控制台与监控 HUD**：实时追踪模型配额、重置倒计时与模型能力 HUD。
* 🔧 **底层系统补丁与环境修复**：攻克 Windows NTFS 目录链接丢失、202MB 二进制反复下载等系统级缺陷。
* 🔌 **上下文、知识图谱与记忆引擎**：利用本地 AST 解析与 SQLite FTS5 全文索引，直接砍掉 90%+ 的 Token 消耗。
* 🪝 **生命周期守卫与安全拦截**：前置拦截高危删除命令与敏感凭证泄露。
* 🛠️ **CLI 脚手架与智能体编排中枢**：合规调度多智能体集群协同，告别不可靠的灰产账号池。

本项目**明确拒绝单纯堆砌纯文本 Prompt/Skill，拒绝违规灰产**，专注于收录**真实、可运行、可复用的软件工具与工程扩展**。

---

## 目录

- [🖥️ IDE 扩展与控制台](#️-ide-扩展与控制台)
- [🔧 平台补丁与底层系统工具](#-平台补丁与底层系统工具)
- [🔌 上下文、记忆与优化引擎](#-上下文记忆与优化引擎)
- [🪝 生命周期钩子与安全守卫](#-生命周期钩子与安全守卫)
- [🛠️ CLI 工具与多智能体编排](#️-cli-工具与多智能体编排)
- [⚡ MCP 桥接器与移动扩展](#-mcp-桥接器与移动扩展)
- [🏷️ 项目徽章 (Badge)](#️-项目徽章-badge)

---

## 🖥️ IDE 扩展与控制台

为 VS Code、Antigravity IDE 增强实时遥测、配额监控和模型交互界面的桌面软件与插件。

- [Antigravity-Manager](https://github.com/lbjlaq/Antigravity-Manager) - 基于 Rust (Tauri v2) + React 构建的专业桌面级 Antigravity 账号管理与一键切换工具。 `Desktop` `Rust` `Tauri`
- [AntigravityQuotaWatcher](https://github.com/wusimpl/AntigravityQuotaWatcher) - 长期维护的高星 Antigravity AI 模型配额观察与状态栏提示插件。 `VS Code` `IDE`
- [pilothouse](https://github.com/aemresrbyk/pilothouse) - 现代化多终端控制台，支持 Antigravity CLI、Claude Code 与 Codex 的多标签协同，带端到端加密的手机端通知与审批。 `Desktop` `React 19` `Electron`
- [token-monitor](https://github.com/Javis603/token-monitor) - 本地优先的桌面端悬浮小组件，实时监控包括 Antigravity 在内的 50+ 编程智能体的 Token 与费用限额。 `Desktop` `Widget`
- [vscode-antigravity-cockpit](https://github.com/jlcodes99/vscode-antigravity-cockpit) - VS Code 扩展，支持多模型配额实时监控、状态栏倒计时提示、多模型置顶及模型能力 HUD。 `VS Code` `TypeScript`

---

## 🔧 平台补丁与底层系统工具

针对操作系统或底层运行时的热修复脚本与环境桥接器。

- [antigravity_bypass](https://github.com/Futureppo/antigravity_bypass) - 底层限制解除补丁，将 Antigravity IDE 本地 MCP 工具数量上限安全提升至 8192，带自动备份与一键还原。 `Windows` `Patch`
- [antigravity-conversation-fix](https://github.com/FutureisinPast/antigravity-conversation-fix) - 修复 Antigravity 会话数据损坏、历史乱序与线程丢失的专用修复工具。 `IDE` `Fix`
- [antigravity-junction-skill-fix](https://github.com/wllzhang/antigravity-junction-skill-fix) - 零磁盘占用 NTFS 硬链接目录桥接工具，彻底解决 Antigravity Go Language Server 无法加载 Windows 目录联接 (`mklink /J`) 与符号链接 (`mklink /D`) 的硬伤问题。 `Windows` `PowerShell` `NTFS`
- [vscode-antigravity-backend-fix](https://github.com/HeshamNoaman/vscode-antigravity-backend-fix) - 官方 VS Code 插件热修补工具，彻底解决 Windows Defender 超时引发的每次启动重复下载 ~202MB `agy.exe` 的网络拥堵与进程锁死问题。 `Windows` `Node.js` `PowerShell`

---

## 🔌 上下文、记忆与优化引擎

高性能本地引擎，压缩上下文、构建代码知识图谱并实现跨会话持久化记忆。

- [codegraph](https://github.com/colbymchenry/codegraph) - 100% 离线运行的预索引代码知识图谱，代码变动自动热同步，成倍削减 Antigravity 的重复探索性工具调用。 `Code-Intelligence` `Graph`
- [context-mode](https://github.com/mksglu/context-mode) - 基于 SQLite FTS5 的本地高性能插件，将超大工具输出拦截在上下文窗口之外，节省高达 99% 的 Token 消耗。 `Plugin` `Performance`
- [LongMemory](https://github.com/CaviraOSS/LongMemory) - 专为编程智能体设计的本地持久化无向量记忆引擎，跨会话保留重要项目背景。 `Memory` `Plugin`
- [memorix](https://github.com/AVIDS2/memorix) - 基于 Model Context Protocol 的轻量级跨 Agent 共享记忆层。 `MCP` `Memory`

---

## 🪝 生命周期钩子与安全守卫

通过 `hooks.json` 配置的会话前、工具调用前后的自动化处理脚本与安全拦截器。

- [antigravity-session-bridge-hook](https://github.com/wllzhang/awesome-antigravity-tools) - 会话启动前自动同步目录桥接与刷新环境变量的 Hook 模板。 `Hooks` `Automation`
- [cc-safety-net](https://github.com/kenryu42/cc-safety-net) - 专为 Coding Agent 打造的执行安全拦截器，在工具调用前实时阻断高危 Git 覆盖、敏感凭据文件读取与毁灭性删除。 `Hooks` `Security`

---

## 🛠️ CLI 工具与多智能体编排

脚手架、网关转换器与本地智能体集群守护进程。

- [agents-manager](https://github.com/Eden-Sun/agents-manager) - Rust 守护进程 + Web 前端，支持在本地或远程 SSH 主机上集中管理与协作调度 Antigravity (`agy`)、Claude Code 与 Codex 智能体。 `Rust` `React` `Orchestration`
- [antigravity-skill-porter](https://github.com/Pranav-Nexus/antigravity-skill-porter) - CLI 自动化工具，将 Claude Code 与 Cursor 技能一键迁移并打包为符合规范的 Antigravity 原生插件（自动补全 `plugin.json`）。 `CLI` `Converter`
- [ctx](https://github.com/ctxrs/ctx) - 高性能本地会话时光机，提供类似 Git blame 的智能体对话历史极速检索与回溯。 `CLI` `Rust`
- [liftgate](https://github.com/acking-you/liftgate) - 基于官方 `agy acp`（Agent Client Protocol）通道构建的本地合法 API 网关与原生 GPUI 桌面控制中心，免除任何封号与灰产风险。 `Rust` `GPUI` `Gateway`
- [skills-manager-cli](https://github.com/wllzhang/awesome-antigravity-tools) - 跨 Coding Agent (Antigravity, Claude Code, Cursor, Codex) 的技能统一管理与软链接分发 CLI。 `CLI` `Cross-Agent`

---

## ⚡ MCP 桥接器与移动扩展

连接桌面无障碍系统、移动端与外部协议客户端的专用 MCP 适配器。

- [antigravity-link-extension](https://github.com/cafeTechne/antigravity-link-extension) - Antigravity IDE 手机伴侣扩展，手机端实时镜像会话进度，支持一键紧急终止并提供 9 种 MCP 工具操作。 `Mobile` `MCP`
- [chrome-devtools-mcp](https://github.com/wllzhang/awesome-antigravity-tools) - 为 Antigravity 智能体提供深度 Chrome 浏览器控制与 DevTools 协议调试的 MCP 服务。 `Browser` `DevTools`
- [claude-antigravity-mcp-bridge](https://github.com/im-mahdi-74/claude-antigravity-mcp-bridge) - 专用的 MCP 协议网关，支持外部客户端通过标准协议调度 Antigravity CLI (`agy`) 执行开发任务。 `MCP` `Bridge`
- [windows-mcp](https://github.com/wllzhang/awesome-antigravity-tools) - 深度集成 Windows 系统无障碍树、UI 自动化、PowerShell 执行与通知推送的专用 MCP 服务。 `Windows` `Automation`

---

## 🏷️ 项目徽章 (Badge)

如果您的工具已被收录到本榜单，欢迎在您的 README 中展示收录徽章：

[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/wllzhang/awesome-antigravity-tools)

```markdown
[![Awesome Antigravity Tools](https://img.shields.io/badge/Awesome-Antigravity--Tools-brightgreen?logo=google&logoColor=white)](https://github.com/wllzhang/awesome-antigravity-tools)
```

---

## 🤝 参与贡献

欢迎提交您的工具！在提交前请阅读我们的 [贡献指南](CONTRIBUTING.md) 与 [行为准则](CODE_OF_CONDUCT.md)。
