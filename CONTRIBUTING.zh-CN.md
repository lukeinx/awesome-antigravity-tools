# 参与贡献 awesome-antigravity-tools

[English Contributing Guide](CONTRIBUTING.md)

感谢您为 **awesome-antigravity-tools** 贡献力量！本仓库坚持「纯粹且极致」的原则，只收录 **100% 专为 Google Antigravity 设计研发** 的原生工程工具、IDE 扩展、底层补丁与 ACP 专用网关。

---

## 🎯 收录门槛（纯粹性硬标准）

### ✅ 欢迎收录
- **官方 CLI 与开发套件**：`google-antigravity` 官方维护的命令行工具与语言 SDK。
- **IDE 扩展与专属控制台**：专为 Antigravity 配额监控、状态栏 HUD、账号切换打造的扩展与桌面端应用。
- **平台补丁与底层运行时修复**：解决 Antigravity 客户端缺陷、NTFS 符号链接失效、汉化注入、无 TUN 代理或会话损坏修复的底层工具。
- **专用网关、ACP 适配器与迁移工具**：严格基于官方 `agy acp` 协议或原生 `plugin.json` 插件规范研发的工具。

### ❌ 明确拒绝
- **纯 Markdown 提示词合集（`SKILL.md`）**：无实际可执行代码或工程封装。
- **跨平台泛用工具贴牌**：面向 Claude Code / Cursor / Codex 等多平台设计、仅附带提及 Antigravity 的泛用工具。
- **闭源、已归档或无法使用的失效项目**。

---

## 🗂️ 单一数据源（Single Source of Truth）工作流

本项目统一以 [`data/tools.json`](data/tools.json) 为唯一数据源（受 [`data/catalog.schema.json`](data/catalog.schema.json) 约束），中英文 README 均由脚本确定性自动生成——**请勿直接手动修改 `README.md` 或 `README.zh-CN.md`**。

### 方式一：使用 CLI 一键添加（推荐）

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

### 方式二：编辑 JSON 并自动同步文档

1. Fork 仓库并创建新分支（`git checkout -b add-my-tool`）。
2. 在 `data/tools.json` 中添加工具条目。
3. 执行自动排序、全量派生产物生成（双语 README、徽章、导出表与网页包）及严格校验：
   ```bash
   python scripts/aat_cli.py sync
   python scripts/aat_cli.py verify --check-sync --strict-warnings
   ```
4. 提交 Pull Request！

### 方式三：通过 GitHub Issue 表单提报

您也可以直接填写 [工具提报表单](https://github.com/wllzhang/awesome-antigravity-tools/issues/new/choose)，自动化分诊流程将自动校验链接、查重并生成标准 JSON 片段供维护者合入。

---

## 🧹 每日健康巡检与清退机制

每日北京时间 10:00（UTC 02:00），`.github/workflows/health-check.yml` 会自动巡检全部收录仓库：
- **0–100 工程健康分**：综合活跃度（45 分）、社区星标（25 分）、开源协议清晰度（15 分）与发布元数据（15 分）。
- **90 天滚动趋势账本**：每日聚合指标与状态变更记录保存在 `data/health_history.json`。
- **清退规则**：404 失效仓库立即移除；归档仓库自动标注 `[Archived]`；超过 365 天无更新进入废弃评审；超过 180 天进入观察名单。
