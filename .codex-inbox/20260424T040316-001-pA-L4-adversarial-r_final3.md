# Codex Inbox · 001-pA · L4 Adversarial R_final3 (super-narrow)

**Kickoff time**: 2026-04-24T04:03:16Z
**Reviewer role**: GPT-5.4 xhigh · Adversarial Reviewer
**Mission**: Super-narrow re-verify of G6/G7/G8/G9 mechanical sync fixes applied after R_final2 BLOCK. **Nothing else**.
**Max runtime**: ≤ 20 min (this is a spot-check, not a review)
**Output language**: 中文

---

## Context

R_final2 BLOCK verdict reasons（见 `.codex-outbox/20260424T021718-001-pA-L4-adversarial-r_final2.md`）:
- G2 X3 ❌ · LLM 合同 split-brain（tech-stack / skeleton §2/§3/§4/§7 / spec.md D15 / llm-types.ts 未同步到 adapter-内写 llm_calls 合同）
- G2 X8 ❌ · spec.md §4 D15 仍写「T013 写双表」
- G4 H2 ❌ · T010.md Goal 仍写 POST 返 400
- G4 H4 ❌ · error-codes-and-glossary.md 缺 CSRF_ORIGIN_MISMATCH + 3 条旧 glossary 未标 deprecated

spec-writer 已提交 G6-G9 mechanical sync patch（spec.md 0.3.0 → 0.3.1）。本轮**只复核这 4 条是否真的机械闭合**。

---

## Rules

1. **Do not reopen any other checks.** G1/G3/G4-H1/G4-H3/G2-X3b/G2-X3c 在 R_final2 已 ✅，本轮**不得重开**。
2. Verdict gate:
   - **CLEAN-WITH-NOTES**: G6-G9 全部机械闭合（即使你发现不在本 scope 内的 minor drift）
   - **BLOCK**: G6-G9 中**任何一条**未机械闭合
3. **Do not produce patches.** 只报"闭合 / 未闭合 + 具体行号"。
4. Stop hard at 20 min.

---

## G6 verification (LLM contract single source of truth)

**Expected state**: adapter-内写 llm_calls 合同已同步到所有权威文件。

### G6a · tech-stack.md §2.4
- `rg -n "llmCallId" specs/001-pA/tech-stack.md` 应 ≥ 1 行
- `rg -n "caller.*写.*llm_calls|T013.*写.*llm_calls" specs/001-pA/tech-stack.md` 应 0 行（或只在 changelog/historical 段）
- 契约段（约 line 141-148）应含 "adapter 内部调 `recordLLMCall`" 明确职责陈述

### G6b · reference/llm-adapter-skeleton.md §2 / §3 / §4 / §7
- `rg -cn "recordLLMCall" specs/001-pA/reference/llm-adapter-skeleton.md` 应 ≥ 6 行
- `SummaryRecord` interface 必须含 `llmCallId: number | null` 或 `llmCallId?: number | null` 字段（§2）
- `JudgeRelationResult` interface 也应含 `llmCallId` 字段（G6 新要求）
- §3 Anthropic adapter `summarize()` 实现代码必须在 return 前调 `recordLLMCall(...)` 拿 id
- §3 Anthropic adapter `judgeRelation()` 同样
- §4 OpenAI adapter 两处同样
- §7 audit 段必须明确 "`recordLLMCall()` 由 adapter 内部调用 · caller 不再调"

### G6c · spec.md §4 D15
- `rg -n "T013.*写双表|写双表.*T013" specs/001-pA/spec.md` 应 0 行
- §4 D15 段应明确 "T013 只写 `paper_summaries` · adapter 已内部写 `llm_calls` 并把 `llmCallId` 通过 `SummaryRecord` 回传"
- spec.md header 版本应是 **0.3.1**（不再是 0.3.0）
- changelog 必须含 0.3.1 entry 描述本次 patch

### G6d · skeletons/llm-types.ts
- `rg -n "llmCallId" specs/001-pA/reference/skeletons/llm-types.ts` 应 ≥ 1 行（SummaryRecord interface 内）

### G6e · skeletons/llm-anthropic-stub.ts + llm-openai-stub.ts
- `rg -n "recordLLMCall|G6.*MANDATORY|必须.*recordLLMCall" specs/001-pA/reference/skeletons/llm-anthropic-stub.ts` 应 ≥ 1 行（summarize 或 judgeRelation TODO 中明确必调 recordLLMCall）
- 同样 llm-openai-stub.ts

---

## G7 verification (spec.md D15 clarified)

G7 是 G6c 的一部分。若 G6c 通过则 G7 通过。

---

## G8 verification (T010 Goal 400 → 422)

- `rg -n "^.*400.*$" specs/001-pA/tasks/T010.md | rg -v "changelog|R_final|旧|废|Deprecated"` 应 0 行
- `rg -n "422.*TOO_MANY_TOPICS|TOO_MANY_TOPICS.*422" specs/001-pA/tasks/T010.md` 应 ≥ 2 行
- T010 Goal 段（约 line 25）必须明确写 422 而非 400

---

## G9 verification (error-codes-and-glossary sync)

### G9a · CSRF_ORIGIN_MISMATCH 加入
- `rg -n "CSRF_ORIGIN_MISMATCH" specs/001-pA/reference/error-codes-and-glossary.md` 应 ≥ 1 行
- §1.3 错误码表必须含 `CSRF_ORIGIN_MISMATCH` 行（HTTP 403 · Layer=API · route = `invite/consume/route.ts`）
- 错误码总数更新到 **31 HTTP**（或文档其他一致表述，重点是加了一条）

### G9b · 旧 glossary 条目标 Deprecated
- `rg -n "login/verify\?token|invite/\[token\]/consume/route|schema_version" specs/001-pA/reference/error-codes-and-glossary.md | rg -v "Deprecated|废|旧|deprecated"` 应 0 行
- 每条旧术语应带 Deprecated / 废 / 旧 注记

### G9c · 正权威条目已存在
- `email token invite` glossary 条目应提到 `POST /api/invite/consume` + body token + Origin 校验
- `schemaVersion`（camelCase）应作为权威名出现（可以与旧 `schema_version` Deprecated 同时存在）

---

## What you must output

Outbox: `.codex-outbox/20260424T040316-001-pA-L4-adversarial-r_final3.md`
Language: 中文
Max length: ≤ 80 lines

```markdown
# Adversarial Review · 001-pA · R_final3 (super-narrow)

**Reviewer**: GPT-5.4 xhigh
**Completed**: <ISO>
**Runtime**: ~<N> min
**Scope**: G6/G7/G8/G9 mechanical sync re-verify only

## Matrix

| G | Target | Close? | Key finding (≤ 1 line) |
|---|---|---|---|
| G6a | tech-stack.md §2.4 | ✅/❌ | ... |
| G6b | llm-adapter-skeleton.md §2/§3/§4/§7 | ✅/❌ | ... |
| G6c | spec.md D15 + 0.3.1 | ✅/❌ | ... |
| G6d | skeletons/llm-types.ts | ✅/❌ | ... |
| G6e | skeletons stub files | ✅/❌ | ... |
| G8 | T010 Goal 400→422 | ✅/❌ | ... |
| G9a | CSRF_ORIGIN_MISMATCH | ✅/❌ | ... |
| G9b | Deprecated 注记 | ✅/❌ | ... |
| G9c | email/schemaVersion 权威 | ✅/❌ | ... |

## Residual blockers

<If all ✅: "None — all G6-G9 mechanically close. Ready for Phase 0 kickoff.">
<If any ❌: file:line + exact remaining drift + one-line fix required>

## Final verdict
- **CLEAN-WITH-NOTES** (all ✅) / **BLOCK** (any ❌)

## Optional ≤ 2 notes
<Minor drift outside G6-G9 scope the operator should know about. No action required in this review.>
```

---

## Operational constraints

- **No WebSearch, no WebFetch.** Evidence from repo only.
- **Cite file:line** for ❌.
- **Do not rewrite spec.** Don't suggest patches; only pass/fail.
- **Chinese output.**
- **20 min hard cap.** If a check takes > 2 min, mark it ⚠️ with reason and move on.
