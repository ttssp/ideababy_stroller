# Adversarial Review · 001-pA · R_final3 (super-narrow)

**Reviewer**: GPT-5.4 xhigh
**Completed**: 2026-04-24T05:05:57Z
**Runtime**: ~9 min
**Scope**: G6/G7/G8/G9 mechanical sync re-verify only

## Matrix

| G | Target | Close? | Key finding (≤ 1 line) |
|---|---|---|---|
| G6a | tech-stack.md §2.4 | ✅ | `tech-stack.md:101-146` 已含 `llmCallId`，并明确 adapter 内调 `recordLLMCall`、caller 只消费 FK。 |
| G6b | llm-adapter-skeleton.md §2/§3/§4/§7 | ✅ | `llm-adapter-skeleton.md:96-172,325-406,632-715,1008-1105` 已同步类型、四处 `recordLLMCall()` 与 adapter-内写权责。 |
| G6c | spec.md D15 + 0.3.1 | ✅ | `spec.md:3,107,264` 已是 0.3.1；D15 明写 T013 只写 `paper_summaries`，且 0.3.1 changelog 在列。 |
| G6d | skeletons/llm-types.ts | ✅ | `reference/skeletons/llm-types.ts:87` 的 `SummaryRecord` 已有 `llmCallId: number \| null`。 |
| G6e | skeletons stub files | ✅ | `llm-anthropic-stub.ts:58-70,90-97` 与 `llm-openai-stub.ts:55-64,84-90` 都强制 return 前调 `recordLLMCall()`。 |
| G8 | T010 Goal 400→422 | ✅ | `tasks/T010.md:25,38,44,49,52,61` Goal / Outputs / Verification 全部统一为 **422 `TOO_MANY_TOPICS`**。 |
| G9a | CSRF_ORIGIN_MISMATCH | ✅ | `error-codes-and-glossary.md:42-54,111,718` 已加 `CSRF_ORIGIN_MISMATCH`，31 HTTP / 51 total 同步。 |
| G9b | Deprecated 注记 | ✅ | `error-codes-and-glossary.md:364,576` 旧 `login/verify?token`、`invite/[token]/consume/route`、`schema_version` 正文均已标 Deprecated。 |
| G9c | email/schemaVersion 权威 | ✅ | `error-codes-and-glossary.md:358-364,571-576` 已以 `POST /api/invite/consume` 与 `schemaVersion` 作为权威表述。 |

## Residual blockers

None — all G6-G9 mechanically close. Ready for Phase 0 kickoff.

## Final verdict

- **CLEAN-WITH-NOTES**

## Optional ≤ 2 notes

- `G6a` 的辅助 grep（`caller.*写.*llm_calls|T013.*写.*llm_calls`）会命中 `tech-stack.md:146` 的否定句“caller 不写 `llm_calls`”；这是宽匹配误报，不是 split-brain 残留。
- `G9b` 的辅助 grep 会命中 `error-codes-and-glossary.md:3` 的版本摘要 `schema_version→schemaVersion`；旧术语正文条目本身已在 `:576` 正确标 Deprecated。
