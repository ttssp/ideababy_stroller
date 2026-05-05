---
name: specs/NNN-pX 四层权威与对齐要求
description: 本项目 specs/ 目录的文档分层（spec/architecture/tech-stack/reference）各自权限、冲突裁决、偏移消化模式
type: project
---

在 `ideababy_stroller` 项目（fork 001-pA 及未来 fork）下，`specs/<fork-id>/` 目录有明确分层：

**Tier 1 · 权威合同**（修改必 bump 版本 + git tag）：
- `spec.md` — 6 要素契约 · 唯一修改方 operator / spec-writer
- `architecture.md` — C4 + ADR · 修改需同步 spec.md 相关字段
- `tech-stack.md` — 版本 pin · 改版本号也要 bump minor

**Tier 2 · 参考（reference/）**：
- `reference/schema.sql` / `reference/api-contracts.md` / `reference/llm-adapter-skeleton.md` / `reference/ops-runbook.md` / `reference/testing-strategy.md` / `reference/error-codes-and-glossary.md` / `reference/directory-layout.md`
- 与 Tier 1 冲突时 **Tier 1 胜**；但工程细节（具体 SQL / 具体 TS 类型 / 具体 curl）以 Tier 2 为最细粒度权威
- reference 文件是 "spec 推导出的工程化细节"，由 spec-writer 写入 · 由版本控制约束

**Tier 3 · 元文档**：
- `DECISIONS-LOG.md` · `OPEN-QUESTIONS-FOR-OPERATOR.md` · `risks.md` · `non-goals.md` · `compliance.md` · `SLA.md` · `README.md` · `dependency-graph.mmd`
- DECISIONS-LOG 持续追加 · 不删
- OPEN-QUESTIONS 条目 resolved 时 **不删 · 追加 "✅ resolved by ... (date)"**（审计保留）

**Tier 4 · 任务**：
- `tasks/T*.md` — 修改方：operator / spec-writer / task-decomposer subagent
- parallel-builder workers 禁止触碰 specs/ 下任何文件 · 发现问题必写 PR blocker

**Why**: 这个分层让 6–8 名初级工程师 + 1 名架构师 + solo operator 协作时不会吵谁改什么 · 合同偏移发现时有明确 "哪层赢 · 哪层消化" 的 protocol。

**How to apply**: 
- 遇 spec 内容与 reference/ 冲突：先读 DECISIONS-LOG 是否已裁决；无则开新 Q 到 OPEN-QUESTIONS · 由 operator 签字；patch 落 Tier 1 并记 DECISIONS-LOG；版本 bump 同步（Patch = 澄清 / Minor = scope / Major = 1.0）
- 写新 reference/*.md 时顶部必写 "对应 spec: spec.md vX.Y / architecture.md vX.Y" 让读者判断版本匹配
- Tier 1 / 2 任一文件 bump 时检查引用方是否需同步
