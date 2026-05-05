---
name: 表计数 / 数字 narrative 必须以 enumerated list 为权威
description: 写 spec narrative 里的 "N 张表" / "M 个 endpoint" 等数字时容易 off-by-one · 改动后容易忘记同步 · enumerated list 才是真 ground truth
type: feedback
---

在 fork 001-pA 的 R1 adversarial fix（新增 `paper_summaries` + `export_log` 两张表）时，architecture.md §5.1 narrative 写成 "12 → 14"，但实际枚举列表是 15 张（`llm_calls` 一直就在 · narrative 未算进去 · 产生 off-by-one）。T003.md Verification 也照抄了 "14 个 CREATE TABLE" 断言 · 会让 builder 跑 verification 误报 fail。

**Why**: 数字 narrative 是 derived metadata · 实际 ground truth 永远在 enumerated list（`spec.md §Outcomes` · `architecture §5.1` 表格 · `schema.sql` 实际 CREATE TABLE · `api-contracts.md §2` endpoint 块 · `tasks/T*.md` task 块列表）。narrative 与 list 冲突时 **list 赢**。

**How to apply**:
- 写任何 "N 张表 / M 个 endpoint / K 个 error code" narrative 时 · 同 PR 内必须和 enumerated list 交叉验证一次
- Verification checklist 里的 "内含 N 个 CREATE TABLE" 这种断言 · 必须从枚举列表数 · 不从 narrative 抄
- 改动 enumerated list（加 / 删 / 改表）时 · grep 所有 "N 张表 / X 个 endpoint" narrative · 同步更新
- 发现 drift 时 · 走 OPEN-QUESTIONS-FOR-OPERATOR.md → operator 签字 → spec-writer patch（遵守 spec-protection.md）· **不**自行改 spec
