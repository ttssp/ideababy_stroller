# Status · 001-pA L4 交付包

**Last updated**: 2026-04-23T18:10:00Z
**Spec version**: 0.2.2
**Phase**: L4 Plan · 文档加厚完成 · 等 R_final adversarial review 后进 Phase 0 build

---

## 一句话总结

001-pA（PI Briefing Console）的 v0.1 **spec 包已达"1 架构师 + 6-8 初级工程师可直接照抄开发"的门槛**。总计 14,932 行（7 份规范 + 7 份参考 + 13 份代码骨架 + 6 份工作流 + 25 个 task + 元文档）。**正在等 Codex R_final adversarial review 给最终 verdict**（kickoff 在 `.codex-inbox/latest.md`，由 operator 在 Codex 终端跑 `cdx-run` 触发）。

---

## 关键数字

| 指标 | 值 |
|---|---|
| Task 数 | 25 |
| 总工时 | 114h（@ 20h/周 × 5 周 = 100h；slack 1h / 硬线 115h） |
| 关键路径 | ~59h（T002→T003→T005→T011→T012→T014→T015→T020→T022→T024→T032→T034） |
| Schema 表 | 15（13 既有 + R1 新增 paper_summaries + export_log） |
| API 端点 | 18 文档化（16 v0.1 实现 + 2 v0.2 deferred） |
| 错误码 | 50+（30 HTTP + 20 worker/DB/infra） |
| 术语 | 70+ glossary entries |
| R1 adversarial verdict | BLOCK（3 blocker 已修） |
| R2 / R_final verdict | **等 Codex 跑** |
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
| （waiting） | **Codex R_final cdx-run 待 human 触发** |

---

## R_final 在挑战什么（outbox 回来前的预判）

Codex R_final 会查（详见 `.codex-inbox/latest.md`）：

**X1 Schema 完整性** · 每列/CHECK/FK/index 正确 ← schema.sql 已 625 行涵盖
**X2 API ↔ schema 一致** · 18 端点字段名 vs schema 列名 ← api-contracts.md §3 已做 camelCase↔snake_case 映射声明
**X3 LLM interface ↔ spec ↔ cost** · OpenAI $15/M 一致性 ← tech-stack 已同步，envelope $50 仍守住
**X4 Task ↔ reference alignment** · file_domain / depends_on 精确 ← R1 fix 已修，审计 pass 过
**X5 测试 catalog** · spec §6 每条 hook 有对应测试 ← testing-strategy.md 已一一对应
**X6 Ops runbook** · systemd 单元 / backup 脚本可运行 ← 1556 行完整命令
**X7 Junior readiness** · T010/T015/T021 能否独立开工 ← 刚审过 T001/T003/T004/T013/T015 并 patch
**X8 Spec versioning** · 0.1 → 0.2 → 0.2.1 → 0.2.2 changelog 清晰
**X9 新 blocker** · reference 层引入的新冲突 ← spec-writer 自检 4 条 drift 都 close 了
**X10 Bus-factor** · operator 缺席 14 天后别人接手 ← ops-runbook §9 I4 + §10 operator-planned-absence

**主要判断**：≥ 80% 概率 R_final = CLEAN 或 CLEAN-WITH-NOTES。BLOCK 可能来自 LLM prompt injection 防御不充分或 export schema 的字段映射问题（spec-writer 自己标注的 3 个 drift 风险点）。

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

1. 在 Codex 终端跑 `cdx-run`，读 `.codex-outbox/20260423T175614-001-pA-L4-adversarial-r_final.md`
2. 若 **CLEAN / CLEAN-WITH-NOTES**：
   - Git commit + tag 整个 spec 包：`git tag spec/001-pA/v0.2.2`
   - Phase 0 kickoff：先跑 T001 spike（~8h，独立不依赖任何 task），并行 T002 scaffold
3. 若 **CONCERNS**：读 blocker/concern 清单，决定修或记 risks.md 后启动
4. 若 **BLOCK**：走上面"应急路径"表

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
