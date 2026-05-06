# Codex Inbox · 001-pA · L4 Adversarial R_final2 (narrow re-verify)

**Kickoff time**: 2026-04-24T02:17:18Z
**Reviewer role**: GPT-5.4 xhigh · Adversarial Reviewer
**Mission**: Narrow verification of G1/G2/G3/G4 fixes applied after R_final BLOCK. Do **not** reopen R1/R_final checks that were not flagged by R_final. Scope is surgical.
**Max runtime**: ~30 min (this is a targeted follow-up, not a full pass)
**Output language**: 中文

---

## Context: what R_final BLOCKed and what was fixed

R_final (outbox `20260423T175614-001-pA-L4-adversarial-r_final.md`) returned **BLOCK** with 3 blockers + 5 high-severity drifts. Operator authorized a surgical fix pass tagged **G1/G2/G3/G4**. All fixes claim to be landed as of 2026-04-24T02:10Z.

| Fix tag | Original blocker/high | Files claimed changed | Your verify target |
|---|---|---|---|
| **G1** | B1 · D15 中文句界 CHECK 仍用 whitespace lookbehind | `reference/schema.sql §14`, `reference/skeletons/llm-utils.ts`, `risks.md TECH-8`, `DECISIONS-LOG.md drift 6` | X1 + X5 只复核此段 |
| **G2** | B2 · LLM 合同三套并存（T004/T007/T013 vs skeleton/tech-stack） | `tasks/T004.md`, `tasks/T007.md`, `tasks/T013.md`, `spec.md §5`, `spec.md` version bump → 0.3.0 | X3 + X8 只复核此段 |
| **G3** | B3 · Export envelope 三层不一致 | `architecture.md §8`（redirect to api-contracts.md §3.11 as authoritative）, `tasks/T023.md`, `reference/api-contracts.md §3.11/E17`, skeleton | X2 + X5 只复核此段 |
| **G4 H1** | `T021` resurface enum `6w\|3mo\|6mo` vs schema `timed_*` | `tasks/T021.md` | X4 子项 |
| **G4 H2** | `T010` Topics CRUD 路径/code/编号三套 | `tasks/T010.md` | X4 子项 |
| **G4 H3** | `T030` 备份脚本路径 + DB role 误当 OS user | `tasks/T030.md`, `reference/ops-runbook.md` | X4 + X6 子项 |
| **G4 H4** | invite consume 路径 token 落 access log | `reference/api-contracts.md §E2` 改 POST + body token + CSRF_ORIGIN_MISMATCH | X6 子项（H6 原文问题） |

**`spec.md §5` 旧 task 编号** 也已在 G2 一并恢复（T001–T034）。

---

## Rules for this review

1. **Do not reopen** items R_final marked as ✅ / ⚠️ that weren't in G1–G4. Specifically:
   - H5（export-route-scan CI 仍注释）— 不 re-verify（deferred by design）
   - H7（prompt injection defense）— 不 re-verify（addressed, continue-watch 状态）
   - H8（budget gate 归属）— G2 已归属，若你已核到 T004/T013 一致则 OK
   - H9（spike sample size）— 不 re-verify
   - H10（BUS-1）— 不 re-verify
2. **Do reopen** if a G-fix introduced a new contradiction elsewhere you hadn't flagged.
3. Verdict gate: 如果 G1–G4 全部 mechanically close，即使你找到新的 minor drift 也给 `CLEAN-WITH-NOTES`。只有再次出现合同级断裂（junior 会因此卡住）才 `BLOCK`。
4. **Stop after these checks** — don't drift into tone/style/readability.

---

## Scope · X1/X3/X5 deep re-check (G1 Chinese sentence boundary)

### X1 · Schema CHECK 实际行为
**Target**: `specs/001-pA/reference/schema.sql` lines 510–560 (paper_summaries.summary_sentence_cap).

**Expected**（G1 新策略）:
```sql
constraint summary_sentence_cap check (
  coalesce(
    array_length(regexp_matches(summary_text, '[.!?。！？]', 'g'), 1),
    0
  ) between 1 and 3
)
```
计数**终结符数量**（不是 split），对纯中文无空格「第一句。第二句。第三句。」返回 3（pass），对 5 句纯中文返回 5（reject），对「第一句」无终结符返回 0（reject）。

**Verify**:
1. Read schema.sql 的 paper_summaries §14。确认 CHECK 不再含 `\s+`、`split_part`、`regexp_split_to_array`。
2. Mentally execute 以下 3 个 payload 得到期待结果：
   - `中文一。中文二。中文三。` → 3 terminators → pass
   - `中文一。中文二。中文三。中文四。中文五。` → 5 → reject
   - `中文无终结符` → 0 → reject
   - `A. B. C.`（英文带空格 · 3 句）→ 3 → pass
3. **Fail condition**: CHECK 仍含 whitespace lookbehind 或 split-based；或计数不走 `regexp_matches(..., 'g')`。

### X5 · Application-layer truncate 与 DB CHECK 一致
**Target**: `specs/001-pA/reference/skeletons/llm-utils.ts` 的 `truncateTo3Sentences`。

**Expected**: 输入 4 句中文无空格 → 输出仅前 3 句，`truncated: true`；输入 2 句 → 原样，`truncated: false`；输入无终结符 → 追加 `。` 或截断策略之一（任何合理选择），但**不得**抛错。

**Verify**:
1. Read skeletons/llm-utils.ts lines 1–60。
2. 核对 implementation 是否使用 `match(/[^.!?。！？]+[.!?。！？]+/g)` 或等价「capture chunks」策略（不是 `split`）。
3. 核对 `reference/testing-strategy.md §3.2` 的测例清单已更新，覆盖纯中文/中英混合/无尾标点三种 corner case（至少 9 行 DB + 10 行 app = 19 断言）。
4. **Fail condition**: 仍用 whitespace split；或测例未覆盖纯中文无空格。

### X5b · risks.md TECH-8 同步
**Target**: `specs/001-pA/risks.md` TECH-8 段落。
**Expected**: 已改写为「G1 · 2026-04-24 · 通过 terminator-count CHECK + application-layer truncateTo3Sentences 闭合；原 lookbehind 策略作废」或等价。
**Fail condition**: TECH-8 仍说 D15 风险未缓解或仍引用旧 lookbehind。

---

## Scope · X3/X8 deep re-check (G2 LLM contract)

### X3 · `T004.md` vs `llm-adapter-skeleton.md §2/§7` vs `tech-stack.md §2.4`
**Target**:
- `specs/001-pA/tasks/T004.md` 全文
- `specs/001-pA/reference/llm-adapter-skeleton.md §2`（interface）and §7（audit）
- `specs/001-pA/tech-stack.md §2.4` LLM 段

**Verify 合同点（7 条）**:
1. ✅ `SummaryRecord` camelCase：`{ summaryText, promptVersion, modelName, llmCallId?, inputTokens, outputTokens, latencyMs, truncated, requestHash }`。
2. ✅ `judgeRelation` per-pair 签名：`({candidatePaper, earlierAnchor, topic}) → JudgeRelationResult`（不是 batch `Paper[] → ...`）。
3. ✅ Provider enum = `'anthropic' | 'openai'`（不是 `claude | gpt`）。
4. ✅ Adapter 内部调 `recordLLMCall()` 写 `llm_calls`，把 `id` 填进返回的 `SummaryRecord.llmCallId`。
5. ✅ Caller（T013）**不**再写 `llm_calls`，只写 `paper_summaries`。
6. ✅ GPT 输出单价 = `$15/M tokens`（不是 `$10/M`）。
7. ✅ `llm_calls` 字段使用 `purpose`（enum `'summarize'|'judge_relation'`）+ `called_at`，而非不存在的 `kind` 或 `created_at`。

### X3b · `T007.md` env 枚举
**Target**: `specs/001-pA/tasks/T007.md` 中 `LLM_PROVIDER` / `LLM_FALLBACK_PROVIDER` 值。
**Expected**: `anthropic | openai`（**不是** `claude | gpt`）。
**Fail condition**: 仍写 `claude | gpt`。

### X3c · `T013.md` persistSummary 契约
**Target**: `specs/001-pA/tasks/T013.md` 的 `persistSummary` 签名与 step 流程。
**Expected**:
- 签名 `persistSummary({ paperId, topicId, record: SummaryRecord }) → Promise<{ paperSummaryId: number }>`
- Step 明确「adapter 已写 `llm_calls`，T013 只读 `record.llmCallId` 作为 FK」
- fallback 路径（provider 全挂）允许 `llmCallId=null`（schema F5 已允许 null）
- 不再双写 `llm_calls`

### X8 · spec.md 版本/任务表同步
**Target**: `specs/001-pA/spec.md`:
- Header 版本字段 = 0.3.0
- §5 Task Breakdown 列出 T001–T034（25 条任务）
- §4 D15/D16 与 G1 新策略一致
- changelog 含 0.3.0 entry
**Fail condition**: 仍是 0.2.2 / 旧 task 编号 / 旧 interface 描述如 `summarize(paper): string`。

---

## Scope · X2/X5 deep re-check (G3 export envelope)

### X2 · Single source of truth
**Target**:
- `specs/001-pA/architecture.md §8`
- `specs/001-pA/tasks/T023.md`
- `specs/001-pA/reference/api-contracts.md §3.11` + `§E17`

**Expected layering**:
- `architecture.md §8` = **redirect** 到 `api-contracts.md §3.11` 作为权威（不含内联 snake_case JSON 样例）
- `T023.md` = **按 api-contracts.md §3.11 完整实现**（无重复/冲突字段定义）
- `api-contracts.md §3.11` = **权威 12 顶层 key**：`schemaVersion`、`exportedAt`、`lab`、`seats`、`topics`、`papers`、`paperSummaries`、`paperTopicScores`、`paperCitations`、`fetchRuns`、`actions`、`breadcrumbs`、`resurfaceEvents`
- 全文 camelCase（`schemaVersion` / `firstDayAt` / `paperSummaries`），**不得**混用 `schema_version`

**Verify**:
1. `rg "schema_version" specs/001-pA/` —— 应该仅在 changelog 或「旧 snake_case 已废弃」上下文出现，不在契约段。
2. `rg "buildFullExport\(env\.LAB_ID\)" specs/001-pA/` —— 应为 0 行。
3. `rg "buildFullExport\(labId" specs/001-pA/` —— 应命中 T023 + architecture + api-contracts。
4. api-contracts.md E17 body 样例使用 `schemaVersion: "1.1"`，不是 `schema_version`。

### X5 · Testing coverage for new export
**Target**: `specs/001-pA/reference/testing-strategy.md §2.5/§4.4`。
**Expected**: 断言更新到 12 top-level keys + `schemaVersion='1.1'` + 排除 `llmCalls`/`exportLog`/`sessions` + 排除 `inviteTokenHash`。
**Fail condition**: 仍断言 9 table 子集，或未覆盖 camelCase。

---

## Scope · X4 deep re-check (G4 H1–H3 task drift)

### X4a · T021 resurface enum
**Target**: `specs/001-pA/tasks/T021.md`。
**Verify**:
1. `grep "'6w'\|'3mo'\|'6mo'" T021.md` → 0 occurrences (except possibly changelog note)
2. `grep "'timed_6wk'\|'timed_3mo'\|'timed_6mo'" T021.md` → ≥ 3 occurrences
3. Verification 段已 enforce `rg "'6w'\|'3mo'\|'6mo'" src/lib/resurface/ = 0` as a gate.

### X4b · T010 Topics CRUD
**Target**: `specs/001-pA/tasks/T010.md`。
**Verify**:
1. Error code = `TOO_MANY_TOPICS` + HTTP **422**（不是 `TopicCapExceeded` / 400）
2. Files include `src/app/(main)/topics/[id]/edit/page.tsx` + `service.ts`，**不**含 `topics/new/page.tsx` 或独立 `crud.ts`
3. Task id 仍是 T010（api-contracts.md E6 也改为引用 T010，不是 T009）

### X4c · T030 deploy & backup
**Target**: `specs/001-pA/tasks/T030.md` + `specs/001-pA/reference/ops-runbook.md §9/§10`。
**Verify**:
1. `deploy/scripts/pg-dump.sh` + `deploy/scripts/restic-backup.sh`（**不**是 `deploy/backup/*`）
2. 权限验证命令改为 `PGUSER=webapp_user PGPASSWORD=... psql ...`（**不**再用 `sudo -u webapp_user`）
3. systemd unit 归属明确（是 T007 产出 or T030？G4 要求对齐）

### X4d · H4 · invite consume POST redesign
**Target**: `specs/001-pA/reference/api-contracts.md §E2` + `ops-runbook.md §5` Caddy log 段。
**Verify**:
1. §E2 已完整改为 `POST /api/invite/consume` with body `{ token }`（不再是 `GET /api/invite/:token/consume`）
2. 新 error code `CSRF_ORIGIN_MISMATCH` / 403 已列入 §Error codes 表（error-codes-and-glossary.md §1 也同步）
3. SEC-10 威胁模型段已重写，说明 POST body + `SameSite=Lax` + Origin check 如何共同缓解 token 泄漏
4. Caddy log 策略段：原 path token 担心已 moot（POST body 不进 access log path 部分）

---

## What you must output in the outbox

Single markdown file, structure:

```markdown
# Adversarial Review · 001-pA · R_final2 (narrow)

**Reviewer**: GPT-5.4 xhigh
**Completed**: <ISO>
**Runtime**: ~<N> min
**Scope**: G1/G2/G3/G4 re-verification only

## Executive summary (≤ 5 sentences)
<判断 G1-G4 是否 mechanically close；是否可以放 1 architect + 6-8 junior 开工>

## G-fix verification matrix

| Fix | Target X-check | Close? | Key finding |
|---|---|---|---|
| G1 | X1 schema CHECK | ✅/❌ | ... |
| G1 | X5 app truncate + tests | ✅/❌ | ... |
| G2 | X3 T004 7 contract points | ✅/❌ | ... |
| G2 | X3b T007 env enum | ✅/❌ | ... |
| G2 | X3c T013 persistSummary | ✅/❌ | ... |
| G2 | X8 spec.md version + §5 | ✅/❌ | ... |
| G3 | X2 export envelope SSOT | ✅/❌ | ... |
| G3 | X5 export tests | ✅/❌ | ... |
| G4 H1 | X4a T021 enum | ✅/❌ | ... |
| G4 H2 | X4b T010 paths/code | ✅/❌ | ... |
| G4 H3 | X4c T030 backup | ✅/❌ | ... |
| G4 H4 | X4d invite POST | ✅/❌ | ... |

## Residual blockers (if any)
<If found: name, file:line citation, exact fix required. If none: "None — all G-fixes close.">

## Final verdict
- **CLEAN** / **CLEAN-WITH-NOTES** / **BLOCK**

## Optional notes
<Any drift you spotted that is below the BLOCK bar but operator should see — ≤ 3 bullets>
```

---

## Operational constraints

- **No WebSearch, no WebFetch.** All evidence must come from the repo (`specs/001-pA/**`, `discussion/001/001-pA/**`).
- **Cite file:line** for every `❌` finding. `✅` may cite or not.
- **Do not rewrite the spec.** If you find issues, describe the fix; don't produce a patch.
- **Write outbox to** `.codex-outbox/20260424T021718-001-pA-L4-adversarial-r_final2.md` and update `.codex-outbox/latest.md` symlink.
- **Chinese output.**

Time budget is tight (≤ 30 min). Skip long pleasantries.
