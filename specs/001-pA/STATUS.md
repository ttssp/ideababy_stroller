# Status · 001-pA L4 交付包

**Last updated**: 2026-04-24T02:20:00Z
**Spec version**: 0.3.0
**Phase**: L4 Plan · R_final BLOCK 已修（G1–G4）· 等 R_final2 narrow re-verify 后进 Phase 0 build

---

## 一句话总结

001-pA（PI Briefing Console）的 v0.1 **spec 包已修完 R_final BLOCK 的 3 blocker + 5 high-severity drift（G1/G2/G3/G4）**。当前 115h（5 周 × 20h = 100h + 15h slack，已到硬线）/ 关键路径 ~59h。**R_final2 narrow kickoff 就位**（`.codex-inbox/latest.md`→ `20260424T021718-001-pA-L4-adversarial-r_final2.md`），由 operator 在 Codex 终端跑 `cdx-run` 触发。R_final2 scope 是**只复核 G1/G2/G3/G4**，不重开未在 BLOCK 范围内的 R_final 项。

---

## 关键数字

| 指标 | 值 |
|---|---|
| Task 数 | 25 |
| 总工时 | 115h（@ 20h/周 × 5 周 = 100h；slack 0h / 硬线 115h · G2 已用尽 slack） |
| 关键路径 | ~59h（T002→T003→T005→T011→T012→T014→T015→T020→T022→T024→T032→T034） |
| Schema 表 | 15（13 既有 + R1 新增 paper_summaries + export_log） |
| API 端点 | 18 文档化（16 v0.1 实现 + 2 v0.2 deferred） |
| 错误码 | 31 HTTP + 20 worker/DB/infra（G4 H4 新增 `CSRF_ORIGIN_MISMATCH`） |
| 术语 | 70+ glossary entries |
| R1 adversarial verdict | BLOCK（3 blocker 已修） |
| R2 verdict | BLOCK（3 blocker 已修） |
| R_final verdict | **BLOCK**（B1 中文句界 + B2 LLM 合同 + B3 export envelope + 5 high-severity）— 全部 G1/G2/G3/G4 修完 |
| R_final2 verdict | **等 Codex 跑**（narrow re-verify · `.codex-inbox/latest.md`） |
| 开放问题 | Q1–Q4 + Q5 全部 ✅ resolved · Q3 deferred to T033 kickoff |

---

## 交付清单（14,932 行总）

### 主 spec 层 · `specs/001-pA/`
```
README.md                    222   navigation landing（三角色阅读路径）
spec.md                      271   v0.2.2 · 6-element contract · O1-O5 · C1-C13 · D1-D16
architecture.md              ~440  v0.2 · C4 L1/L2 + ADR-1..7 + 15 表 ER + 部署拓扑
tech-stack.md                ~240  Next 15 / TS 5.6 / Drizzle / Postgres 16 · LLM 双 adapter
SLA.md                       142   v0.1 self-dogfood + v1.0 aspirational · RPO≤24h RTO≤2h
risks.md                     ~280  TECH×9 / OPS×5 / SEC×10 / COM×4 / LEG×3 / DOGFOOD×3 / BUS×3
non-goals.md                 236   25 条 A/B/C 三类显式 non-goal
compliance.md                ~180  PIPL 轻度 + 数据主权 + 保留策略
dependency-graph.mmd         86    25 task DAG · 4 phases · mermaid
DECISIONS-LOG.md             339   所有第一性论证的犹豫点（16+ 条目）
OPEN-QUESTIONS-FOR-OPERATOR  178   Q1–Q5 含 resolution markers
STATUS.md                    <this file>
tasks/T001..T034.md          25 个 · 每个 ~3-5k 字 · 总 ~4800 行
```

### 参考层 · `specs/001-pA/reference/`
```
schema.sql                   624   完整可执行 DDL · 15 表 · CHECK / UNIQUE / FK / INDEX
directory-layout.md          794   monorepo 树 + package.json + tsconfig + biome + CI
api-contracts.md             1119  18 端点 · 输入/输出 schema · 30 HTTP 错误码 · curl 示例
llm-adapter-skeleton.md      1354  TS interface + Anthropic/OpenAI 两 adapter 完整代码 + prompts + T001 spike harness
ops-runbook.md               1556  部署 13 节 · systemd/Caddy/pg_dump/restic · 8 类 incident SOP
testing-strategy.md          733   unit/E2E/redline test catalog · fixture 协议
error-codes-and-glossary.md  713   50+ error codes · 70+ glossary
```

### 代码骨架 · `specs/001-pA/reference/skeletons/` （可 cp 直接跑）
```
README.md                    149   skeleton→task 所有权矩阵 + 使用协议
env.ts                       131   zod-typed env Proxy
db-schema.ts                 458   Drizzle 全 15 表定义 + CHECKs
llm-types.ts                 158   LLMProvider interface + SummaryRecord + StateShiftVerdict union
llm-anthropic-stub.ts        87    最小 compiling stub 指向 llm-adapter-skeleton.md §3
llm-openai-stub.ts           83    同上，指向 §4
recordAction.ts              200   Result-return 模式 · B2 Layer 2 zod refine 完整实现
skip-why-input.tsx           128   B2 Layer 3 UI · 5 字符 gate · Chinese 文案
today-page-server.tsx        104   SSR Server Component loader
today-page-client.tsx        149   Client Component wrapper · TopicCard + ActionRow
worker-daily.ts              102   systemd entry · 5 pass 顺序 · 顶部 banner 禁 next/*
middleware-auth.ts           148   Edge 安全 JWT 验证 · 路由分类 · 头部注入 seat-id/lab-id/role
api-healthz-route.ts         53    /api/healthz 完整（DB ping + uptime + git sha）
api-export-full-route.ts     106   admin gated · export_log 审计 · 无 query-param
```

### 工作流 · `specs/001-pA/reference/workflows/`
```
local-dev-setup.md           287   clone → green 15 步骤 · 故障排除
task-pickup.md               228   10 步骤 · file_domain 速查 · TDD-first 提醒
git-branching.md             211   Conventional Commits · 分支生命周期 · lefthook
pr-review.md                 153   PR 模板 · 6 类 review bar · 合并规则
on-boarding-day-1.md         192   8 小时新手 Day 1 计划 · 含起步 task 推荐
adversarial-review.md        197   何时触发 R(N) · 4 轮上限 · 文件格式
```

---

## L4 时间线

| 时间 (UTC) | 事件 |
|---|---|
| 2026-04-23T13:27 | `/fork 001 from-L3 candidate-A as 001-pA` 执行 |
| 2026-04-23T13:37 | `/plan-start 001-pA` 开始 |
| 2026-04-23T13:37 | Q2 (LLM=E spike) + Q6 (dogfood=self-use) 决定 |
| 2026-04-23T13:46–13:56 | spec-writer R1 产 spec 包（7 份规范 + 6 tasks 模板） |
| 2026-04-23T14:02 | task-decomposer R1 产 25 task + DAG（107h / 51h） |
| 2026-04-23T14:20 | Codex R1 kickoff |
| 2026-04-23T14:28 | **Codex R1 BLOCK** (B1 per-paper summary · B2 skip CHECK · B3 task contracts) |
| 2026-04-23T14:58 | spec-writer 修 B1/B2/B3（spec 0.1 → 0.2） |
| 2026-04-23T15:08 | task-decomposer R1→R2 DAG 重跑（113h / 58h） |
| 2026-04-23T15:08 | task-decomposer 发现 Q1/Q2/Q4/Q5 drift |
| 2026-04-23T15:55 | spec-writer 修 Q1/Q2/Q4 · spec 0.2 → 0.2.1 |
| 2026-04-23T16:00 | spec-writer 写 reference/schema.sql + directory-layout.md |
| 2026-04-23T16:18 | spec-writer 写 reference/llm-adapter-skeleton.md + api-contracts.md |
| 2026-04-23T16:43 | spec-writer 写 reference/ops-runbook.md + testing-strategy.md + error-codes-and-glossary.md |
| 2026-04-23T16:55 | spec-writer 修 Q5 + 5 drift + README · spec 0.2.1 → 0.2.2 |
| 2026-04-23T17:35 | spec-writer 写 skeletons/ 13 份代码 + workflows/ 6 份 SOP |
| 2026-04-23T17:52 | Explore agent 审计 5 spine tasks 初级可读性 |
| 2026-04-23T17:55 | spec-writer 补 5 task 关键 gap |
| 2026-04-23T17:56 | Codex R_final kickoff 就位 |
| 2026-04-24T01:57 | **Codex R_final = BLOCK**（B1 D15 中文句界 whitespace-split 失败 · B2 LLM 合同 T004/T007/T013 vs skeleton 三套 · B3 export envelope architecture/task/API 三层不一 · 5 high-severity drift） |
| 2026-04-24T02:10 | spec-writer 执行 G1–G4 修补包（22 文件改动 · 114h→115h · 仍在硬线内） |
| 2026-04-24T02:17 | R_final2 narrow re-verify kickoff 就位 |
| （waiting） | **Codex R_final2 cdx-run 待 human 触发** |

---

## R_final BLOCK 的 3 blocker（已全部修完 · G1/G2/G3）

### B1 · D15 中文句界 CHECK 失效（G1 修）
**原因**: `paper_summaries.summary_sentence_cap` 用 `(?<=[.!?。！？])\s+` whitespace lookbehind，纯中文无空格「第一句。第二句。第三句。」被视为 1 段，误放行。`truncateTo3Sentences` 骨架也依赖 split-on-whitespace。
**修法（G1）**: CHECK 改为计数终结符 `coalesce(array_length(regexp_matches(summary_text, '[.!?。！？]', 'g'), 1), 0) between 1 and 3`；`llm-utils.ts` 改用 `match(/[^.!?。！？]+[.!?。！？]+/g)` capture chunks；`testing-strategy.md §3.2` 增 9 DB + 10 app 测例覆盖纯中文/中英混合/无尾标点；`risks.md TECH-8` 改写。

### B2 · LLM 合同三套并存（G2 修）
**原因**: `tech-stack.md §2.4` + `llm-adapter-skeleton.md §2/§7` 已是权威 camelCase/per-pair/`anthropic|openai`，但 `T004.md` 仍写 snake_case `SummaryRecord` + batch `judgeRelation` + 自相矛盾的 llm_calls 归属；`T007.md` env 写 `claude|gpt`；`T013.md` 引用不存在的 `llm_calls.kind/created_at` 字段且双写 llm_calls，`spec.md §5` 仍列旧 task id（T005=schema）。
**修法（G2）**: `T004.md`（117→130 行 · 5h→6h · 7 条合同点一致化）；`T007.md` env 改 `anthropic|openai`；`T013.md`（127→140 行 · persistSummary 新签名 · 明确 adapter 已写 llm_calls · fallback 允许 null）；`spec.md` 0.2.2→0.3.0 + §5 task id 恢复到 T001–T034 + interface 描述对齐。

### B3 · Export envelope 三层不一（G3 修）
**原因**: `architecture.md §8` snake_case 9 张表 · `T023.md` 调 `buildFullExport(env.LAB_ID)`（.env 无此变量） · `api-contracts.md §3.11` 是 camelCase 12 张表 · testing-strategy.md 只测子集。
**修法（G3）**: `api-contracts.md §3.11` 定为权威单一真源（camelCase 12 顶层 key · `schemaVersion='1.1'`）；`architecture.md §8` 改为 redirect + 摘要；`T023.md` 完整重写（`buildFullExport(labId: number)` 参数签名 · labId 来自 session · 14 条 Verification 断言）；`testing-strategy.md §2.5/§4.4` 扩 12 keys 断言 + audit-consistency + SEC-5 path traversal。

## R_final BLOCK 的 5 high-severity drift（G4 修）

| Tag | Drift | 修法 |
|---|---|---|
| **H1** | `T021` resurface enum `6w\|3mo\|6mo` vs schema `timed_6wk\|timed_3mo\|timed_6mo` | T021 改枚举 + Verification 加 grep gate |
| **H2** | `T010` 路径 `topics/new+[id]/page` vs directory-layout `[id]/edit` + error code `TopicCapExceeded`/400 vs api-contracts `TOO_MANY_TOPICS`/422 | T010 全改权威 |
| **H3** | `T030` 备份脚本 `deploy/backup/*` 与 directory-layout `deploy/scripts/*` · 权限验证 `sudo -u webapp_user` 把 DB role 当 OS user | T030 改 `deploy/scripts/*` + `PGUSER=webapp_user psql` |
| **H4** | invite consume path token 被 Caddy access log 捕获（Caddy 只删 query，不删 path） | `api-contracts.md §E2` 改 `POST /api/invite/consume` + body token + 新 error code `CSRF_ORIGIN_MISMATCH`（403） · URL fragment 传 token |
| **spec.md §5** | 旧 task id T005=schema / T007=LLM / T029=export + 旧 interface `summarize(paper): string` | §5 恢复 T001–T034 + 移除旧描述 |

## R_final2 narrow scope（just landed）

`.codex-inbox/latest.md` → `20260424T021718-001-pA-L4-adversarial-r_final2.md`

只复核 G1/G2/G3/G4 12 行 verification matrix，不重开 H5/H7/H8/H9/H10 等已 accepted 的项。verdict gate: G-fix 全部 mechanically close 则 CLEAN-WITH-NOTES；再次出现合同级断裂才 BLOCK。

---

## Deferred（按 operator 前次决定保留，**不在本轮 scope**）

### R1 H-list（10 条 high-severity 关切）
- **H1** O4 "missed-paper 案例" 降级为自陈文件 — faithfulness 打折，接受作为 dogfood self-use 的代价
- **H2** operator 可见性 shared judgment 下不显性化 — v0.1 先看 O3 是否成立
- **H3** stale briefing fallback 未强制 — 运行中会自然暴露，可在 Week 1 dogfood 补
- **H4** state-shift 假阳性无产品级逃生阀 — 已记 risks.md TECH-5 + week-7/14/21 review
- **H5** export CI grep 未前置 — 见 directory-layout.md §9 注释，可 Week 1 启用
- **H6** invite GET 保留 — 已记 risks.md SEC-10（accepted，因不发邮件仅 lab-private IM 传递）
- **H7** prompt injection 防线 — 已在 llm-adapter-skeleton.md §6/§10 加 XML wrap + system 指令 + adversarial fixture 测试；**可能被 R_final 重评**
- **H8** judge + retry cost — 已在 llm-adapter-skeleton.md §7 `recordLLMCall` 对 `summarize` 和 `judge` 都走 budget check
- **H9** T001 20 篇样本偏弱 — 已在 task + llm-adapter-skeleton §8 建议升到 40 篇（**实际收敛**：operator 在 T001 kickoff 时可选）
- **H10** BUS-1 "接受暂停" — 已在 ops-runbook.md §9 I4 加 operator-absent 流程（安全模式、锁 admin 路由、sentinel、lab 成员能看但不能写）；实质修了

### OPEN-QUESTIONS
- **Q3** T033 self-report 采样 skip.why — 推到 T033 kickoff 时补

---

## 如果 R_final = BLOCK（应急路径）

最可能的 BLOCK 场景 + 应对：

| 可能 blocker | 应对 |
|---|---|
| B1' Prompt injection 加固不够 | spec-writer 写更严的 adversarial fixture 组（目前 5 条 → 升 15 条）+ 加 output JSON schema strict mode |
| B2' Export 字段映射 breaking | spec-writer 明确 `for_date` vs `date` + `timed_6wk` vs `6wk` 的 export builder mapper，schema_version 保持 1.1 |
| B3' 某个 task file_domain 新撞 | task-decomposer 补文件 domain 声明（小工作） |
| B4' 骨架代码 TS strict 下不编译 | spec-writer 修具体 import / type 错误 |

任何一类 blocker 应在 ≤ 1h 修完 · 再跑 R_final+1（第 3 轮）。

---

## 建议 operator 的下一步

1. 在 Codex 终端跑 `cdx-run`（`.codex-inbox/latest.md` 已指向 R_final2 narrow kickoff）
2. 读 `.codex-outbox/20260424T021718-001-pA-L4-adversarial-r_final2.md`
3. 若 R_final2 = **CLEAN / CLEAN-WITH-NOTES**：
   - Git commit + tag 整个 spec 包：`git tag spec/001-pA/v0.3.0`
   - 读 `specs/001-pA/PHASE-0-KICKOFF-CHECKLIST.md`，按 10 节自检
   - Phase 0 kickoff：先跑 T001 spike（~8h，独立不依赖任何 task），并行 T002 scaffold
4. 若 R_final2 = **BLOCK**：读残余 blocker 清单，大概率是某个 G-fix 没有真正机械闭合（可能是 changelog 叙述与实际代码不一致）；重新 spec-writer 修 → R_final3。R_final 已达 3 轮上限的一半，不应再超过 2 轮额外 re-verify。

---

## 建议 operator 在 Phase 0 kickoff 前亲自验证的 3 件事

1. **T001 spike 的 20 篇人工标注 fixture** — 能不能真的收集 10 shift + 6 incremental + 4 unrelated？若收集困难，提前在 T001 spike 里加 "fixture 收集耗时 2-3h" 到工时估算。
2. **本地 Postgres 16 已安装** — 跑 `psql pi_briefing < specs/001-pA/reference/schema.sql` 看能否顺利建所有 15 表 + CHECK 生效。这是最小可开工条件。
3. **LLM API keys 已备妥** — Anthropic + OpenAI 两家的 key 都要有（spike 需要跑两个 provider 对比）；若无，提前申请。

---

## 文档质量自评（相对"初级工程师能开工"门槛）

| 维度 | 分数 | 说明 |
|---|---|---|
| 可阅读路径清晰 | 9/10 | README.md 按角色 × 目的拆三条路径；有时长预估 |
| 抽象到具体的跨度 | 9/10 | spec → architecture → reference → skeletons 四层逐步落地 |
| 可执行代码起点 | 9/10 | 13 份 skeletons + 7 份 reference；junior cp + 填 TODO 即可 |
| 验证 runnable | 9/10 | 每个 task Verification 都是具体 pnpm/psql/curl/playwright 命令 |
| 错误处理规范 | 9/10 | 50+ 错误码 + i18n · 三层红线防御 |
| 决策可追溯 | 9/10 | DECISIONS-LOG 16+ 条 · 每条含"第一性"论证 |
| 运维就绪度 | 8/10 | ops-runbook 1556 行 · 8 类 incident SOP；但没经过真实 incident 磨炼 |
| 适应意外变化 | 7/10 | BUS-1 mitigation 存在但未经真测；operator 缺席 14 天流程是纸面的 |
| **整体** | **8.6/10** | **够初级照抄开工；运维和极端场景只能靠真跑暴露** |

---

## 文件清单（给后续接手者一页看清）

```
specs/001-pA/
├── README.md                  ← 新人从这里开始
├── STATUS.md                  ← 你在读这个
├── spec.md                    v0.2.2 · 合同
├── architecture.md            v0.2 · ADRs
├── tech-stack.md              pinned
├── SLA.md
├── risks.md                   TECH/OPS/SEC/COM/LEG/DOGFOOD/BUS
├── non-goals.md
├── compliance.md
├── dependency-graph.mmd       mermaid DAG
├── DECISIONS-LOG.md           所有"犹豫点"
├── OPEN-QUESTIONS-FOR-OPERATOR.md
├── tasks/                     T001..T034 (25 个)
│   ├── T001.md                LLM spike gate
│   ├── T003.md                schema spine (10h)
│   ├── T004.md                LLM interface
│   ├── T013.md                summary persist
│   └── T015.md                /today + 4-action + skip-why
└── reference/
    ├── schema.sql             15 表 executable DDL
    ├── directory-layout.md    monorepo 完整树
    ├── api-contracts.md       18 端点 + 30 HTTP errors
    ├── llm-adapter-skeleton.md
    ├── ops-runbook.md
    ├── testing-strategy.md
    ├── error-codes-and-glossary.md
    ├── skeletons/             13 份 cp-able 代码
    │   ├── README.md          → task 所有权矩阵
    │   ├── env.ts
    │   ├── db-schema.ts
    │   ├── llm-*.ts           (3)
    │   ├── recordAction.ts
    │   ├── skip-why-input.tsx
    │   ├── today-page-*.tsx   (2)
    │   ├── worker-daily.ts
    │   ├── middleware-auth.ts
    │   └── api-*.ts           (2)
    └── workflows/             6 份团队 SOP
        ├── local-dev-setup.md
        ├── task-pickup.md
        ├── git-branching.md
        ├── pr-review.md
        ├── on-boarding-day-1.md
        └── adversarial-review.md
```

---

**下次 operator 回来**：读这份 `STATUS.md` 第一节（1 分钟），看 R_final 是否已跑（`.codex-outbox/`），按"建议 operator 的下一步"3 条走。
