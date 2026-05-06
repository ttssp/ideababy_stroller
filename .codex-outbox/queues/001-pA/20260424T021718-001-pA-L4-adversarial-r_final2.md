# Adversarial Review · 001-pA · R_final2 (narrow)

**Reviewer**: GPT-5.4 xhigh
**Completed**: 2026-04-24T03:00:53Z
**Runtime**: ~44 min
**Scope**: G1/G2/G3/G4 re-verification only

## Executive summary (≤ 5 sentences)
本次只复核 G1/G2/G3/G4。G1 与 G3 已机械闭合；G4 中 T021、T030 已闭合，但 T010 仍残留 `400`/`422` 自相矛盾，invite 相关 glossary 仍留旧 GET/query/schema_version 术语。最关键的是 G2 仍未闭合：`tech-stack.md`、`reference/llm-adapter-skeleton.md`、`spec.md D15` 仍把 `llm_calls` 写入职责放在 caller/T013，而 T004/T013/changelog 已改成 adapter 内写 `llm_calls` + `llmCallId` 回传。这个 split-brain 会直接卡住 junior 对 T004/T013 的实现归属，因此 verdict = `BLOCK`。在修正该合同裂缝前，不建议放 1 architect + 6-8 junior 全面开工。

## G-fix verification matrix

| Fix | Target X-check | Close? | Key finding |
|---|---|---|---|
| G1 | X1 schema CHECK | ✅ | `schema.sql` 已改为 `regexp_matches(summary_text, '[.!?。！？]', 'g')` 计终结符；不再含 whitespace split / lookbehind，纯中文 3/5 句与 0 终结符三类行为都与预期一致。 |
| G1 | X5 app truncate + tests | ✅ | `truncateTo3Sentences()` 已用 chunk-capture regex（非 split）+ 无终结符 defensive `。` 追加；`testing-strategy.md` 已覆盖纯中文 / 中英混合 / 无终结符 corner cases，`risks.md TECH-8` 也已同步重写。 |
| G2 | X3 T004 7 contract points | ❌ | T004/T013 已改成“adapter 内写 `llm_calls`”，但 `tech-stack.md §2.4` 与 `llm-adapter-skeleton.md §2` 仍写 caller/T013 写 `llm_calls`；skeleton 的 `SummaryRecord` 也没有 `llmCallId`，adapter skeleton 实现本身也未调用 `recordLLMCall()`。 |
| G2 | X3b T007 env enum | ✅ | `T007.md` 中 `LLM_PROVIDER` / `LLM_FALLBACK_PROVIDER` 已统一为 `anthropic | openai`，未见 `claude | gpt` 残留。 |
| G2 | X3c T013 persistSummary | ✅ | `T013.md` 已明确 `persistSummary({ paperId, topicId, record })` 只写 `paper_summaries`，消费 `record.llmCallId` 作为 FK，fallback 允许 `llmCallId=null`，且不再双写 `llm_calls`。 |
| G2 | X8 spec.md version + §5 | ❌ | `spec.md` 版本已是 `0.3.0`，Phase/task 编号也已切到 `T001–T034`，但 `§4 D15` 仍写“`T013 写双表`”，与 `§5`、`T013.md`、`0.3.0` changelog 的“adapter 写 `llm_calls`”相冲突。 |
| G3 | X2 export envelope SSOT | ✅ | `architecture.md §8` 已改为 redirect 到 `api-contracts.md §3.11`；`T023.md` 使用 `buildFullExport(labId: number)`；`rg "buildFullExport\\(env\\.LAB_ID\\)" specs/001-pA/` 为 0 行；`E17` body 也已是 `schemaVersion: "1.1"` camelCase。 |
| G3 | X5 export tests | ✅ | `testing-strategy.md` 已更新为 12 个 resource collections + `schemaVersion='1.1'` + 排除 `llmCalls` / `sessions` / `exportLog` / `inviteTokenHash`，并覆盖 round-trip `paperSummaries.llmCallId -> null`。 |
| G4 H1 | X4a T021 enum | ✅ | `T021.md` 已统一为 `timed_6wk | timed_3mo | timed_6mo | citation`；旧 `6w|3mo|6mo` 只剩 changelog 注记，Verification 也已加 `rg` 守门。 |
| G4 H2 | X4b T010 paths/code | ❌ | 路径、`service.ts`、`TOO_MANY_TOPICS`/422 基本都已对齐，但 `T010.md` Goal 仍写“topic > 15 时 POST 返回 400”，与同文件其余 422 约定自相矛盾。 |
| G4 H3 | X4c T030 backup | ✅ | `T030.md` 与 `ops-runbook.md` 都已切到 `deploy/scripts/pg-dump.sh` / `deploy/scripts/restic-backup.sh`，权限验证改为 `PGUSER=... PGPASSWORD=... psql`，且 T007/T030 的 systemd unit 归属划分已写清。 |
| G4 H4 | X4d invite POST | ❌ | `api-contracts.md §E2` 与 `ops-runbook.md` 已完整切到 `POST /api/invite/consume` + body token + `CSRF_ORIGIN_MISMATCH` + fragment/POST-body 日志模型；但 `error-codes-and-glossary.md` 仍缺 `CSRF_ORIGIN_MISMATCH`，并保留旧 `login/verify?token=...`、`invite/[token]/consume/route.ts`、`schema_version` 条目。 |

## Residual blockers (if any)

- **B1 · G2 LLM 合同仍是 split-brain** — `specs/001-pA/tech-stack.md:98-107,118-138`、`specs/001-pA/reference/llm-adapter-skeleton.md:97-120,164-171,271-302,539-576,1007-1009`、`specs/001-pA/spec.md:107` 与 `specs/001-pA/tasks/T004.md:31,40`、`specs/001-pA/tasks/T013.md:28-31,38-39` 冲突。**Exact fix required**：把所有权威文件统一到同一合同上：adapter 调 `recordLLMCall()` 写 `llm_calls`、`SummaryRecord` 显式含 `llmCallId`、T013 只写 `paper_summaries`、`spec.md D15` 删除“`T013 写双表`”旧说法；并让两家 adapter skeleton `summarize()` / `judgeRelation()` 实现真正调用 `recordLLMCall()` 或删除与实现相反的 caller-persist 文案。
