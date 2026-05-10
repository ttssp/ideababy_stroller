---
prd_fork_id: 008a-pA
discussion_id: 008
shared_contract_version_honored: 2.0
# 完全没有 workspace: 块
---

# Invalid fixture — no workspace block

frontmatter 中根本没有 `workspace:` 块。
应 exit 1 + stderr 报 no workspace block found。
