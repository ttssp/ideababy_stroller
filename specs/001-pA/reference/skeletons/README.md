# Skeletons · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**对应 spec**: `spec.md` v0.2.2 · `architecture.md` v0.2 · `tech-stack.md` v0.1.1
**读者**: 6–8 名初级工程师(第一次写本项目代码的那天)

> 本目录里的每个 `.ts` / `.tsx` 都是**可抄即用的起点代码**(skeleton)。每个文件顶部的 banner 说明**目标路径**(把文件 `cp` 到哪)、**所属 task**、**填 TODO 的职责归属**。**禁止原地编辑本目录下的任何代码**,所有改动只能发生在 `src/` 的拷贝版本里,由对应 task 的 PR 承担。

---

## §1 这是什么

Skeleton 是一份**"编译能过、逻辑待填"** 的最小代码骨架:

- 通过 TS 5.6 strict + `noUncheckedIndexedAccess` 类型检查
- 所有 import 路径可解析(`@/lib/...` / `@/db/schema.js` / 等)
- Export 的**公开 API surface**(函数名、类型、常量)与 `reference/api-contracts.md` / `reference/llm-adapter-skeleton.md` / `spec.md` 对齐
- 未实现的逻辑用 `throw new Error('TODO(T<NNN>): <what> — see reference/...')` 占位 + 英文注释标注"去哪查规范"

**不是**:
- 生产代码(每处 TODO 都必须由 task PR 填完才能 merge)
- 最终架构(允许在 task 实现时 surgical refactor,只要不改 public surface)
- 测试(测试文件在 `tests/` 下,不走 skeleton 路径)

---

## §2 如何使用(初级工程师 day-1 流程)

1. **读你被分配的 task file**(`specs/001-pA/tasks/T<NNN>.md`),确认本 task 的 Outputs 列表里包含哪些 `src/` 文件。
2. 在本目录(`specs/001-pA/reference/skeletons/`)找对应 skeleton。
3. **literally copy**:
   ```bash
   cp specs/001-pA/reference/skeletons/recordAction.ts \
      src/lib/actions/recordAction.ts
   ```
4. 打开拷贝的文件,逐个找 `TODO(T<NNN>):` 注释,对照 `reference/*.md` 填充。
5. 先写测试(CLAUDE.md "TDD for production code"),再跑 `pnpm typecheck && pnpm test` 直到全绿。
6. 提 PR:标题 `feat(T<NNN>): <short>`,描述里 `Closes T<NNN>`。

---

## §3 Skeleton → Target path → Task 归属矩阵

| Skeleton 文件 | 目标 `src/` 路径 | 主 task | 辅 task | 主要 TODO 归属 |
|---|---|---|---|---|
| `env.ts` | `src/lib/env.ts` | **T007** | T002 (scaffold) | env zod schema + lazy Proxy |
| `db-schema.ts` | `src/db/schema.ts` | **T003** | — | Drizzle 15 张表完整定义 + CHECKs |
| `llm-types.ts` | `src/lib/llm/types.ts` | **T004** | — | 零 runtime · 逐字抄 `llm-adapter-skeleton.md §2` |
| `llm-anthropic-stub.ts` | `src/lib/llm/anthropic.ts` | **T004** | T001 spike · T013 | `summarize()` / `judgeRelation()` 实现见 `llm-adapter-skeleton.md §3` |
| `llm-openai-stub.ts` | `src/lib/llm/openai.ts` | **T004** | T001 spike · T013 | `summarize()` / `judgeRelation()` 实现见 `llm-adapter-skeleton.md §4` |
| `recordAction.ts` | `src/lib/actions/recordAction.ts` | **T015** | — | D16 Layer 2 红线兜底(zod refine 已就位;DB 写入 + breadcrumb 分支待补) |
| `skip-why-input.tsx` | `src/components/skip-why-input.tsx` | **T015** | — | D16 Layer 3 红线兜底(inline expand + disabled-until ≥5 字符 gate 已就位) |
| `today-page-server.tsx` | `src/app/(main)/today/page.tsx` | **T014** | T015 | 拼装 `BriefingItem[]` 查询(`@/lib/briefings/loadTodayBriefing`) |
| `today-page-client.tsx` | `src/app/(main)/today/today-client.tsx` | **T014** | T015 | 4-action wiring(`ActionRow` 组件) |
| `worker-daily.ts` | `src/workers/daily.ts` | **T011** | T012 / T013 / T014 / T021 | 5 个 pass 子模块 |
| `middleware-auth.ts` | `src/middleware.ts` | **T028** | T027 | JWT verify 已就位;session DB 校验由 `getCurrentSeat()` 负责 |
| `api-healthz-route.ts` | `src/app/api/healthz/route.ts` | **T030** | — | 基本 DB ping 已就位(直接能跑) |
| `api-export-full-route.ts` | `src/app/api/export/full/route.ts` | **T023** | — | `buildFullExport` + `writeExportLog` 两个 stub 待替换 |

**总 13 个文件**(含本 README)。

---

## §4 编译 / 类型检查自验

在拷进 `src/` 之前,可以先验证 skeleton 单独编译:

```bash
# 从仓库根目录
pnpm tsc --noEmit --strict --noUncheckedIndexedAccess \
  specs/001-pA/reference/skeletons/*.ts \
  specs/001-pA/reference/skeletons/*.tsx
```

**注意**:skeleton 里的 `@/*` alias 在 `tsconfig.json` 的 `paths` 里解析;在 `specs/` 下独立编译会报 "Cannot find module '@/lib/env.js'" —— 这**是预期**。正确的验证方式是 `cp` 到 `src/` 后,跑整个项目的 `pnpm typecheck`。

---

## §5 公共约定(跨 skeleton)

### 5.1 命名 casing
- **DB 列**: snake_case(`summary_text`)
- **TS 接口 / 变量**: camelCase(`summaryText`)
- **边界映射**: `src/lib/summary/persist.ts`(Drizzle insert 时显式 `.values({ summary_text: record.summaryText })`)
- **zod schema**: 通常 camelCase(与前端 API 契约对齐);若直接映射 DB 可 snake_case,但必须在 tests 里双向 round-trip 验证

### 5.2 Import 路径
- `@/lib/...` → `src/lib/...`(业务代码)
- `@/components/...` → `src/components/...`
- `@/db` → `src/db/index.ts`(barrel · re-export schema + client + types)
- `@/db/schema.js` → `src/db/schema.ts`(直接导入)
- **禁止** 相对路径超过 `../../`;新人看不懂的就是坏代码(directory-layout.md §4)

### 5.3 Error handling
- API route / Server Action 返 `{ error: { code, message, fields?, requestId? } }` 统一信封(api-contracts §1.3)
- error code 必须是 `error-codes-and-glossary.md §1` 列出的 30 个之一
- **不得自造字面量** error code;新 code 先补进 error-codes 文档,再用

### 5.4 Red line 2 三层兜底
必须同时存在:
1. **DB CHECK**(`skip_requires_why` / `summary_sentence_cap`)→ `db-schema.ts`
2. **API validation**(zod refine)→ `recordAction.ts`
3. **UI disabled gate** → `skip-why-input.tsx`

**任一层被绕过 = 余下两层仍兜得住**。CI 里的 `tests/db/constraints.test.ts` + `tests/e2e/skip-requires-why.spec.ts` 同时验证。

### 5.5 LLM 调用红线
- 只能在 `src/workers/**` 里调 LLM;Web request path(`src/app/**`)调 LLM 构成 BLOCK(ADR-2)
- 每次调用必须在同事务写 `llm_calls` 行(审计)+ 对应 `paper_summaries` 行(产出)(ADR-6 · D15)
- 月度 `cost_cents` 总和接近 envelope $40 触发告警;达 $50 停止 summary pass(C11)

---

## §6 填 TODO 的纪律

每个 skeleton 的 `TODO(T<NNN>): <what>` 注释是**合同条款**:

- `<what>` 描述的行为与 `reference/*.md` 的条款一致时 → 直接按条款实现
- 如果发现条款模糊 / 漏掉某情况 → **不要在 src/ 里做"聪明的猜测"**,而是:
  1. 打开 `OPEN-QUESTIONS-FOR-OPERATOR.md` 新增一个 Q
  2. Ping operator(在 PR description 里 @)
  3. 等 spec-writer 决议再继续

**切忌**:
- 为了让 task 看起来"完成"而跳过一个 TODO,用 `console.warn` 顶着 → 一定会被 adversarial review 抓到
- 把 TODO 改写成看似合理的实现但偏离 spec 意图 → 等于修改了 spec 却没走版本 bump 流程

---

## §7 和 `reference/` 其他文件的关系

| 本 skeleton | 最相关的 reference 文件 |
|---|---|
| `db-schema.ts` | `reference/schema.sql` (15 表权威 DDL;CI `schema-drift` 比对) |
| `llm-*.ts` | `reference/llm-adapter-skeleton.md` §2/§3/§4 |
| `recordAction.ts` / `skip-why-input.tsx` | `reference/api-contracts.md` §2.C E10 · `reference/error-codes-and-glossary.md` §1 |
| `today-page-*.tsx` | `reference/api-contracts.md` §3.6 `BriefingItem` shape |
| `worker-daily.ts` | `reference/ops-runbook.md`(systemd unit) · `architecture.md` ADR-1 |
| `middleware-auth.ts` | `reference/api-contracts.md` §1.2 auth |
| `api-*-route.ts` | `reference/api-contracts.md` 对应 endpoint 块 |

---

## §8 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · 12 skeleton + README · 对齐 spec v0.2.2 |
