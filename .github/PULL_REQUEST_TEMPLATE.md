### Summary

<!-- Briefly describe the tool(s) or improvements in this pull request. -->

### Submission Checklist

All catalog entries are maintained in **`data/tools.json`** (single source of truth). Do not manually edit `README.md` or `README.zh-CN.md`.

- [ ] **100% Antigravity-Exclusive**: Built specifically for Google Antigravity IDE, `agy` CLI, or `agy acp` (no generic prompt dumps or cross-agent rebrands).
- [ ] **Edited `data/tools.json`**: Added entry with complete English/Chinese descriptions, exclusivity rationale, platforms, and 1–5 tags.
- [ ] **Canonical Order & Regenerated Docs**: Ran `python scripts/validate_catalog.py --fix-order && python scripts/generate_docs.py`.
- [ ] **Validation Passed**: Ran `python scripts/validate_catalog.py --check-sync --strict-warnings` with 0 errors and 0 warnings.
- [ ] **Tests Passed**: Ran `python -m unittest discover -s tests` (if modifying scripts).
