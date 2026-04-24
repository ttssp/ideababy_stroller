# OPEN QUESTIONS FOR OPERATOR

> 本文件由 task-decomposer 在 R1→R2 转换重跑时追加。task-decomposer 不能直接改 task 文件，只能在此登记需要 operator / spec-writer 决定的合同漂移。

---

## 2026-04-23 · task-decomposer R1→R2 DAG 重跑

### Q1 · T030 grants.sql 未包含 R1 新增的两张表

**位置**：`specs/001-pA/tasks/T030.md` Outputs 段 `deploy/postgres/grants.sql` 描述行 50

**问题**：T030 `grants.sql` 枚举的表清单为：
- webapp_user `SELECT/INSERT/UPDATE`：`{sessions, actions, breadcrumbs, resurface_events, topics, seats, labs, briefings, papers, paper_citations, paper_topic_scores}` — **缺 `paper_summaries` 和 `export_log`**
- worker_user 额外 INSERT：`{papers, paper_citations, paper_topic_scores, briefings, fetch_runs, llm_calls, resurface_events}` — **缺 `paper_summaries`**

**下游影响**：
- T013 `persistSummary` 用 `dbWorker`（worker_user）向 `paper_summaries` INSERT → 部署后会 403/permission denied
- T015 `/today` loader 用 webapp_user 从 `paper_summaries` SELECT → 同样 permission denied
- T023 `logExport` 用 webapp_user 向 `export_log` INSERT → 同样 permission denied
- T016 `/papers/:id/history` 读 `paper_summaries` → 同样 permission denied

**建议修复方向**（需 operator 批准后由 spec-writer 追加到 T030）：
- webapp_user 增加 `SELECT on paper_summaries` 与 `SELECT/INSERT on export_log`
- worker_user 增加 `SELECT/INSERT/UPDATE on paper_summaries`（upsert 需 UPDATE）
- T003 已在 schema.ts 提供表；T030 grants.sql 是最后一道部署脚本，必须同步

**紧迫性**：中。Phase 0 本地开发期 dev 用 superuser 不会遇到；但 T034 smoke soak 在 VPS 上会 fail。建议在 T030 kickoff 前修。

---

### Q2 · T006 声明的 auth 列是否已在 T003 schema.ts 中预置？

**位置**：`specs/001-pA/tasks/T006.md` Implementation plan 第 3 步 + Known gotchas 最后一条

**问题**：T006 明写"数据库 migration 增量（属于 T003 的 `0002_auth_columns.sql`）"，新增以下列：
- `seats.invite_token_hash TEXT`
- `seats.invite_expires_at TIMESTAMPTZ`
- `seats.invited_at TIMESTAMPTZ`
- `sessions.revoked_at TIMESTAMPTZ`
- `sessions.last_active_at TIMESTAMPTZ`

T006 Implementation 第 3 步最后写"选后者"=把列 merge 到 T003 schema.ts 里提前定义。但 T003 Outputs / Implementation plan 现在**没有**显式列出这 5 个 auth 列（R1 fix 只动了 `paper_summaries` / `export_log` / `labs.first_day_at` / `labs.allow_continue_until` / `fetch_runs.notes`）。

**验证方法**：读 T003 `src/db/schema.ts` 的 `seats` + `sessions` 表定义（目前是任务文件未实现），若未枚举这 5 列，会在 T006 本地测试跑 `invite.ts` 时立即挂。

**建议修复方向**（需 operator / spec-writer 决定）：
- Option A：在 T003 schema.ts 里显式追加 5 个 auth 列（与 B3 其他列同批）
- Option B：允许 T006 在 `src/db/migrations/0002_auth_columns.sql` 追加独立 migration（会稍微扩大 T006 的 file_domain，需要更新 T006 的 file_domain 声明）

**紧迫性**：高。T006 无法跑通会阻塞 T010 / T015 / T023 三条并行支线。建议 Phase 0 kickoff 前闭合。

---

### Q3 · T033 runbook/self-report.md 并未显式要求填入 skip.why 证据

**位置**：`specs/001-pA/tasks/T033.md` Outputs 段 `docs/runbook/self-report.md` 描述

**问题**：R1 fix B2 落地了"skip 必须有 why（≥5 字符）"三层机械兜底（DB CHECK + API + UI），但 T033 self-report 模板字段仍为 "active seats / 4-action 数量 / 漏看案例 / breadcrumb aha"，没有要求 operator 每周采样 3-5 条 skip.why 做月度 self-audit。

**下游影响**：红线 2 的"可追溯"落到了数据层，但没有对应的"人工定期回看"流程。operator 60 天后想验证"skip why 是否真的写得有用"时，没有 protocol 可依。

**建议修复方向**（若 operator 接受）：
- T033 self-report 增加字段 "本周随机抽样 3 条 skip 记录，人工打分 why 可读性（1-5）并记录"
- 或在 compliance §7 月度自审清单里补一条

**紧迫性**：低。Phase 2/3 都不阻塞；但若忘记在 v0.1 上线前补，O4 faithfulness 会打折。可作为 T033 kickoff 时补充。

---

### Q4 · T032 E2E admin-export.spec.ts 的 schema_version 断言值

**位置**：`specs/001-pA/tasks/T032.md` Implementation plan 第 4 步

**问题**：T032 Implementation 第 4 步写 `assert schema_version=='1.0'`，但 T023 已把 export schema_version 升级为 `'1.1'`（因新增 `paper_summaries` 顶层 key，属 breaking change）。

**下游影响**：T032 E2E 跑时会断言失败。

**建议修复方向**：T032 Implementation 第 4 步把 `1.0` 改为 `1.1`（或 `>= 1.1` 以便未来 bump 兼容）。

**紧迫性**：中。T032 实际动手时才会发现；建议在 T032 kickoff 前一并修。

---

## 约定

- 上述 Q1–Q4 都是 task-decomposer 在 R1→R2 重跑时发现的**合同漂移**，不是 task 文件本身有 bug；
- task-decomposer scope 规则禁止直接修 task 文件，故在此登记；
- 任何一条被 operator 或 spec-writer 闭合后，请在对应条目末尾追加 `✅ resolved by <task-id> / spec-writer / operator (YYYY-MM-DD)` 而不是删除（保留审计）。

---

## 2026-04-23 · Q1+Q2+Q4 resolution by spec-writer

- Q1 ✅ resolved — grants.sql enumeration updated in T030.md
- Q2 ✅ resolved — 5 auth columns front-loaded into T003.md; T006.md updated to consume not create; T003 hours 9 → 10
- Q4 ✅ resolved — T032 step 4 now asserts >= '1.1'
- Q3 🔜 deferred — to be added when T033 kickoff (before writing `docs/runbook/self-report.md`)

Total hours after this patch: 113 + 1 = **114h / 115h** (still within budget, but headroom reduced to 1h).

---

## 2026-04-23 · Q5 · 表计数标注漂移（spec-writer 写 reference/schema.sql 时发现）

**位置**：
- `architecture.md` §5.1 首行："R1 从 12 张升至 14 张"
- `tasks/T003.md` Goal 第 1 段："把 architecture.md §5 的 **14 张表**（原 12 张 + `paper_summaries` + `export_log`）"
- `tasks/T003.md` Verification：`pnpm drizzle-kit generate` 产出 `0000_initial.sql`，内含 **14 个** `CREATE TABLE`"
- `tasks/T003.md` Outputs 枚举（实际清单）：labs / seats / sessions / topics / papers / paper_citations / paper_topic_scores / actions / breadcrumbs / resurface_events / briefings / fetch_runs / llm_calls / paper_summaries / export_log = **15 张**

**问题**：全局"14 表"计数注释与枚举清单不一致。枚举清单（15 张）是**结构权威**，"14"应为 R1 fix 时遗留的 off-by-one 计数注释（R1 fix 实际新增 2 张表；此前 spec 的"原 12 张"未算 `llm_calls` —— `llm_calls` 在架构里一直存在、非 R1 新增，但被 R1 注释遗漏）。

**下游影响（当前）**：
- `reference/schema.sql` 写的是 **15 个** `CREATE TABLE`（与 architecture §5.1 / T003 Outputs 枚举清单一致）
- T003 verification checklist 中 "14 个 CREATE TABLE" 断言会**过不了**（reality = 15）；若 T003 builder 严格照 verification 跑会误报错

**建议修复方向**（需 operator/spec-writer 决定）：
- Option A（推荐）：把 3 处 "14" 改为 "15"（architecture §5.1 首行；T003 Goal 与 Verification 两处）
- Option B：把 `llm_calls` 从 T003 Outputs 枚举中显式拆出声明"已存在"，并把 R1 新增范围说清楚——schema 不变，只是文案明确

**spec-writer 本次处理**：遵守 scope discipline（不改既有 specs/ 文件），**不**自行 patch 三处数字。`reference/schema.sql` 注释里已注明 "Table count: 15"。

**紧迫性**：中。T003 verification 跑通前必须闭合；Phase 0 kickoff 前 15 min 操作即可。

---

## 2026-04-23 · Q5 resolution by spec-writer

- Q5 ✅ resolved — architecture §5.1 first line + T003 Goal + T003 Verification updated to "15 张".
  Reason: llm_calls 一直存在、被 R1 fix 注释漏计；实际 R1 新增 2 张 (paper_summaries, export_log)；
  故 13 + 2 = 15，非 14.
