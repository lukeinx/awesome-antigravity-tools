# Cross-Submission PR Template (向 MichaelZelbel/awesome-antigravity 提交 PR 模板)

> 💡 **使用说明**：
> 当您想将您的底层修复工具 `antigravity-junction-skill-fix` 以及 `vscode-antigravity-cockpit` 推荐收录到已有的 `MichaelZelbel/awesome-antigravity` 时，可以直接 Fork 该仓库并提交 PR，使用本模板作为 PR 描述。

---

### PR Title
`feat: add developer tools and system bridges (junction-fix, cockpit)`

### PR Description

```markdown
### Summary

This PR introduces valuable developer extensions and system-level utilities for Google Antigravity:

1. **[antigravity-junction-skill-fix](https://github.com/wllzhang/antigravity-junction-skill-fix)**: A zero-copy NTFS hardlink bridge resolving the issue where Antigravity's Go Language Server fails to scan skills linked via Windows directory junctions (`mklink /J`) or directory symlinks (`mklink /D`).
2. **[vscode-antigravity-cockpit](https://github.com/jlcodes99/vscode-antigravity-cockpit)**: An essential VS Code extension providing real-time quota tracking, status bar indicators, and model capability HUD for Antigravity.

### Proposed Additions

Under **Developer Tools & Extensions**:
- [antigravity-junction-skill-fix](https://github.com/wllzhang/antigravity-junction-skill-fix) - Zero-copy NTFS hardlink bridge resolving Go language server discovery failures for Windows directory junctions and symlinks. `Windows` `Plugin`
- [vscode-antigravity-cockpit](https://github.com/jlcodes99/vscode-antigravity-cockpit) - VS Code extension for real-time model quota tracking, status bar countdowns, and capability HUDs. `VS Code` `TypeScript`

### Checklist
- [x] Links are verified and working.
- [x] Follows repository markdown formatting standards.
- [x] Both projects are open-source and actively maintained.
```
