# Tech Stack · 001-pA · PI Briefing Console

**版本**: 0.1.1（R_final2 G6 sync · 2026-04-24 · §2.4 LLM 合同与 spec.md D15 / llm-adapter-skeleton §2 同步 adapter-内写 llm_calls）
**创建**: 2026-04-23
**原则**: **Boring over clever**。100h 的工程预算（5 周 × 20h/周）里没有任何多余时间用于配置复杂工具 —— 每个技术决策以 "最少 ramp time × 最少 on-call × 最少依赖" 为第一目标。

---

## 1. Primary stack（v0.1 默认 · 已 commit）

| Layer | 选择 | 版本 | Rationale |
|---|---|---|---|
| 语言 | **TypeScript strict** | 5.6+ | CLAUDE.md 项目偏好；全栈同语言避免 context switching；strict 模式在编译期抓住大多数 v0.1 bug |
| 运行时 | **Node.js LTS** | 22.x LTS | CLAUDE.md 指定；LTS 确保 5 周开发窗口内不踩 breaking change |
| Package manager | **pnpm** | 9.x+ | CLAUDE.md 指定；比 npm 快、硬链接更省空间、workspace 友好（即便 v0.1 单 package 也用上） |
| Web framework | **Next.js 15 · App Router** | 15.x | SSR + Server Actions 覆盖 v0.1 所有交互；无需 tRPC；`/today` 页 SSR 直连 Postgres 满足 p95 < 1s |
| ORM | **Drizzle ORM** | 0.36+ | TypeScript-first；migration 即 SQL 文件，易审；比 Prisma 轻量 40%+ 二进制体积；无 schema generator 工艺折腾 |
| 数据库 | **PostgreSQL** | 16.x | 项目约定的唯一主存储；15 seat × 1 年规模远在单实例能力内；pgvector 可 v0.2 按需装 |
| DB driver | **`postgres` (porsager)** | 3.4+ | Drizzle 官方推荐；支持 prepared statements；无 connection pool 地狱 |
| Auth | 自写 email token 流程 · JWT 存 httpOnly cookie | — | 无需 OAuth；发 token 用 `crypto.randomBytes`；session 表 + middleware 足够（≤ 15 seat） |
| 测试 runner | **Vitest** | 3.x | CLAUDE.md 没指定但 vitest 是 TS 项目事实标准；Node test runner 目前生态仍不完整 |
| E2E 测试 | **Playwright** | 1.48+ | 浏览器端验证 Phase 1/2/3 Exit；T001 spike 不需要 |
| Lint / Format | **Biome** | 1.9+ | CLAUDE.md 指定；一个二进制替掉 ESLint + Prettier，ramp time 最小 |
| CI | **GitHub Actions** | — | 免费额度够；跑 `pnpm lint + test + playwright` |
| 部署 | **单 VPS** + systemd + Caddy | — | 见 architecture.md §9；无 Docker、无 k8s；5 周预算不允许任何 infra 折腾 |
| Reverse proxy / TLS | **Caddy** | 2.8+ | 自动 Let's Encrypt；配置文件比 nginx 短 10 倍 |
| Cron 机制 | **systemd timer**（非 node-cron / BullMQ） | — | OS 级可靠；不进 Node 进程；重启机器自动恢复 |

### 1.1 辅助库（都是 well-maintained · 不写 framework）

| 用途 | 库 | 版本 | 备注 |
|---|---|---|---|
| HTTP client（arXiv + LLM） | **`undici`**（Node 内置 fetch 底层） | node 22 自带 | 不引入 axios/got |
| XML 解析（arXiv OAI-PMH response） | **`fast-xml-parser`** | 4.5+ | 10kb；arXiv 的 Atom feed 解析够用 |
| Date/time | **`date-fns`** | 4.1+ | 只 import 需要的函数（tree-shake 友好）；不用 moment |
| Email 发送（invite） | **`nodemailer`** | 6.x | 走 operator 的 SMTP（Gmail app password 即可）；无第三方 SDK |
| Env 变量校验 | **`zod`** | 3.23+ | schema-in-one-file 校验所有 `process.env.*`，启动期 fail-fast |

### 1.2 UI（刻意粗糙）

PRD UX principle 1 · "UI 粗糙可接受（表格 + 纯文本 briefing）"。v0.1 **不引入** UI 组件库：

| 用途 | 方案 | 备注 |
|---|---|---|
| 样式 | **Tailwind CSS** 3.4+ | 配 Next 15 官方 preset；原子类 + utility-first；无 design system |
| 组件 | **原生 HTML + Server Actions** | 无 shadcn / Radix / MUI；表格、表单、按钮手写 |
| Icon | 无（可选 emoji） | 不装 icon library |

---

## 2. LLM provider · **T001 spike 后决定**（两家候选并列 · 待 operator 拍板）

**本 v0.1 不预 commit 到单一 provider**。`LLMProvider` interface（见 `architecture.md` ADR-4）抽象了所有 LLM 调用；T001 spike 跑完后，operator 选定某家，换 env 即可。

### 2.1 候选 A · Anthropic Claude Sonnet 4.6（long-context）

| 维度 | 数值 / 说明 |
|---|---|
| Model ID | `claude-sonnet-4-6-20250701`（或 spike 当日最新 4.6 变体） |
| Context window | 200K tokens（long-context 变体 1M） |
| Pricing（2026-01） | input $3 / M token · output $15 / M token |
| 每月预估成本 · 本项目 | 3M input + ~0.3M output ≈ $9 + $4.5 = **$13.5/月** |
| Latency（ballpark · 300-token abstract summarize） | p50 ~1.8s · p95 ~4s |
| 对 AI research novelty 判断质量 | Anthropic 在 research-text 任务上的公开评测普遍强；文献 agent 场景是强项 |
| 适配负担（T007） | SDK `@anthropic-ai/sdk`；adapter 一天完成 |
| 特殊优势 | long-context 支持 full briefing prompt（把一个 topic 的 anchor + candidates 全喂进一个 prompt）；适合做 §4.1 state-shift judgment |

### 2.2 候选 B · OpenAI GPT-5.4

| 维度 | 数值 / 说明 |
|---|---|
| Model ID | `gpt-5.4-turbo`（或 spike 当日最新 5.4 变体） |
| Context window | 128K tokens |
| Pricing（2026-04 · R1 Codex refreshed） | input $2.5 / M token · output $15 / M token |
| 每月预估成本 · 本项目 | 3M input × $2.50/M = $7.50 + 0.3M output × $15/M = $4.50 ≈ **$12/月** |
| Latency | p50 ~1.5s · p95 ~3.5s |
| 对 AI research novelty 判断质量 | GPT-5.4 在 benchmark 上与 Claude 4.6 近似；判断风格偏"保守偏 consensus" |
| 适配负担（T007） | SDK `openai`；adapter 一天完成 |
| 特殊优势 | 成本略低；latency 略低；工具链 mature |

### 2.3 开放第三路径 · 本地开源模型（secondary · 不在 T001 默认候选里）

operator 明确表示本地 open model（Llama 4 / Qwen 3 等）可作为后续考虑。**v0.1 不投入** T001 spike 资源跑本地模型，因为：
- 需要 GPU 资源 → 超出 $10–15 VPS 预算
- 自托管 LLM 运维成本远超 $50 envelope 之外
- T001 退出条件必须在 5 天内完成，无时间评估本地模型

**何时重新考虑**：v0.2 若 operator 愿意投入 GPU 或 API 成本突破 envelope 时，再加一个 `LocalLLMAdapter`（interface 已兼容）。

### 2.4 **两家共用的 LLMProvider interface**（T004 必须先落到 `src/lib/llm/types.ts` + `provider.ts`）

> **接口层 camelCase / DB 列 snake_case**：以下 TS 接口字段遵循 TS 惯例使用 camelCase；DB 列使用 snake_case；`src/lib/summary/persist.ts` 负责两层之间的显式映射（见 `reference/llm-adapter-skeleton.md §2` 的权威实现）。**本节契约与 `reference/llm-adapter-skeleton.md §2` 必须逐字一致**；冲突时以 `reference/llm-adapter-skeleton.md` 为准（该文档是 LLM adapter 的权威实现指南）。

```typescript
/** State-shift judgement 的三类结果；见 spec.md §4.1 provisional definition. */
export type RelationLabel = 'shift' | 'incremental' | 'unrelated'

/**
 * G2/G6 权威合同（R_final / R_final2 · 2026-04-24）：
 *   adapter 内部**已**调 `recordLLMCall(...)` INSERT `llm_calls` RETURNING id
 *   并把 id 填入返回的 `SummaryRecord.llmCallId`；
 *   caller（T013 `persistSummary`）只写 `paper_summaries`，消费 `record.llmCallId` 作为 FK。
 *   Fallback 路径（两家 provider 都 down）允许 `llmCallId = null`（schema F5 已允许）。
 */
export interface SummaryRecord {
  summaryText: string          // ≤ 3 句（adapter 已 truncate）
  promptVersion: string        // 如 'v1.0-2026-04' · 来自 SUMMARY_PROMPT_VERSION 常量
  modelName: string            // adapter.name；e.g. 'claude-sonnet-4-6-20250701'
  llmCallId: number | null     // G6 · adapter 已写 `llm_calls` · fallback 路径可为 null
  inputTokens: number
  outputTokens: number
  latencyMs: number
  truncated: boolean           // 是否因 > 3 句被截断（审计用）
  requestHash: string          // SHA-256(promptVersion + arxivId + topicId)
}

/** judgeRelation 的返回形态 · 单 candidate-anchor tuple 判定 · discriminated union 利于 TS strict. */
export type StateShiftVerdict =
  | { kind: 'shift'; confidence: number; rationale: string; anchorPaperId: number }
  | { kind: 'incremental'; confidence: number }
  | { kind: 'unrelated'; confidence: number }

export interface LLMProvider {
  readonly name: 'anthropic' | 'openai'

  /** ≤ 3 句话 summary；adapter **已写** `llm_calls` 并将 id 回传在 `SummaryRecord.llmCallId`；caller 只写 `paper_summaries` */
  summarize(input: {
    paper: { arxivId: string; title: string; abstract: string; authors: readonly string[]; categories: readonly string[]; publishedAt: Date }
    topic: { id: number; name: string; keywords: readonly string[] }
  }): Promise<SummaryRecord>

  /** 给定 candidate + earlier anchor + topic · 返回单对 verdict（per-pair）· adapter 已写 `llm_calls(purpose='judge')` */
  judgeRelation(input: {
    candidatePaper: { arxivId: string; title: string; abstract: string; authors: readonly string[]; categories: readonly string[]; publishedAt: Date }
    earlierAnchor: { arxivId: string; title: string; abstract: string; authors: readonly string[]; categories: readonly string[]; publishedAt: Date }
    topic: { id: number; name: string; keywords: readonly string[] }
  }): Promise<{ verdict: StateShiftVerdict; inputTokens: number; outputTokens: number; latencyMs: number; requestHash: string; llmCallId: number | null }>
}
```

**契约**（G2/G6 权威版本 · 2026-04-24）：
- 两家 adapter 返回结构完全一致；**spike 后切换 provider = 改 env + restart worker**，不改业务代码
- **casing 分层**：接口层 camelCase（上述 `summaryText` / `promptVersion` / `modelName` / `llmCallId`）；DB 列 snake_case（`paper_summaries.summary_text` / `.prompt_version` / `.model_name` / `.llm_call_id`）；`src/lib/summary/persist.ts` 是两层之间的唯一映射点
- **judgeRelation 每次判一对**（candidate × anchor）；batch 由 caller（T012 state-shift pass）循环完成；选 per-pair 而非 batch 的理由：discriminated union 让 TS strict 类型推导更稳、错误隔离粒度更小、retry / budget 检查更自然（见 DECISIONS-LOG 2026-04-23 · drift 2）
- `summarize` 返回 `SummaryRecord`；adapter 内部已 `truncateTo3Sentences`，结果句数 ≤ 3（同时 `paper_summaries.summary_sentence_cap` DB CHECK 是最后兜底，见 architecture.md §7 + ADR-6）
- **`llm_calls` 写入职责 · G6 权威**：adapter 内部调 `recordLLMCall({ provider, purpose: 'summarize'|'judge', inputTokens, outputTokens, costCents, latencyMs, paperId, requestHash })` INSERT `llm_calls` RETURNING id，并把 id 填入 `SummaryRecord.llmCallId`（或 JudgeRelationResult.llmCallId）；caller（T013 `persistSummary` / T012 state-shift pass）**不写** `llm_calls`，只读 `record.llmCallId` 作为 `paper_summaries.llm_call_id` 的 FK
- **Fallback 路径**：两家 provider 同时故障时 T013 走 `fallback-heuristic-v1`，此时 `llmCallId = null`（schema F5 `paper_summaries.llm_call_id` 为 nullable FK）
- token / latency 指标必须返回以便 `llm_calls` 表审计

### 2.5 T001 spike 退出条件（正式 commit）

| 条件 | 阈值 |
|---|---|
| State-shift judgment 准确率（20 篇人工标注 blind test） | 至少一家 ≥ **70%**（≥ 14/20）|
| 月度成本（按 §2.1/2.2 预估） | ≤ $50 USD（C11）|
| p95 latency（summarize 300-token abstract） | ≤ **5s**（worker 跑在 06:00 非交互路径，宽松） |
| API 可用性（spike 期间成功率） | ≥ 99%（连跑 50 次调用，失败 ≤ 1）|

**如果两家都 < 70%**：
- Fallback 路径 = 保留 §4.1 启发式规则（shift = "≥ 2 篇引用同一 anchor"），不再让 LLM 判 relation；LLM 仅用于 summary
- 同时触发 spec.md `OP-Q1` 回到 operator

**如果两家都 ≥ 70%**：按成本取低者；差距 < 10% 则由 operator 主观拍板

---

## 3. 刻意排除的候选（Excluded alternatives · 附明确 why not）

| 候选 | 为什么不选 |
|---|---|
| **Supabase / Firebase** | over-featured · 把 data 绑到第三方，违反 C12（数据主权）；self-host 版本运维比裸 Postgres 还重 |
| **Vercel / Next on Vercel** | cron 限制（Vercel Hobby 只有 limited cron + 10s timeout）；06:00 worker 跑 30–60s 放不下；同时把数据推给 Vercel 违反 C12 |
| **Vercel AI SDK**（`ai` 包） | 设计上 tight-couple 到几个 provider 的特定行为；我们要可 swap interface，自己写 200 行 adapter 更干净 |
| **tRPC** | Next 15 Server Actions 已经提供 type-safe RPC；引入 tRPC 多一层抽象，5 周预算不值得 |
| **Prisma** | 比 Drizzle 重；migration workflow 不如 Drizzle 直观；pnpm + Node 22 有偶发 binary 下载慢的问题 |
| **Elasticsearch / Meilisearch** | 无搜索需求（OUT-4 禁止跨 paper 分析）；Postgres FTS 足够；装 ES 会引入新服务 × on-call 成本 |
| **Redis** | 无缓存需求 —— briefing 已预计算入 Postgres；session 存 Postgres 行；用 Redis 只是增加一个 moving part |
| **BullMQ / Temporal / Inngest** | queue 对单日 cron 纯属过度工程；systemd timer + 单函数就完成任务 |
| **Docker / Kubernetes** | 单 VM × 单进程 × 无水平扩展需求时 Docker 只增加 image build 与网络复杂度；部署用 systemd service 更直接 |
| **shadcn / Radix / MUI** | PRD UX principle 1 明确 UI 粗糙可接受；组件库 ramp time 可以耗掉 5h+ |
| **pgvector / 向量搜索** | v0.1 无 embedding 需求（OUT-4）；pgvector 作为 Postgres extension 未来可随时加，不装新服务 |
| **GraphQL（Apollo 等）** | REST + Server Actions 已够；GraphQL schema 维护 × 5 周时间不值 |
| **monorepo tooling（Turbo / Nx）** | 单 package，不需要 |

---

## 4. Dependency policy（解决 "npm 装一装爆 300 个包" 的 solo operator 危机）

1. **生产依赖上限 = 30 个**（目前清单 12 个；留 buffer）；devDeps 不计但不得超 60
2. **所有 `dependencies` 锁定精确版本**（`package.json` 里不用 `^` / `~`）；devDeps 可用 `^`
3. **每次 `pnpm add` 之前**：`pnpm audit --prod`；禁止引入 critical/high 未补丁依赖
4. **每月一次 `pnpm update --interactive`**，批量审视；solo operator 可接受
5. **禁止**：unmaintained >12 个月的包、weekly download < 10k 的包、原作者不再发版的 fork 包
6. **供应链审计**：production build 前运行 `pnpm audit signatures`；CI 失败即阻断 merge

---

## 5. 版本锁定（package.json 样板 · T004 采用）

```json
{
  "engines": { "node": "22.x", "pnpm": "9.x" },
  "dependencies": {
    "next": "15.0.3",
    "react": "19.0.0",
    "react-dom": "19.0.0",
    "typescript": "5.6.3",
    "drizzle-orm": "0.36.0",
    "postgres": "3.4.5",
    "zod": "3.23.8",
    "date-fns": "4.1.0",
    "nodemailer": "6.9.16",
    "fast-xml-parser": "4.5.0",
    "jose": "5.9.6"
  },
  "devDependencies": {
    "@biomejs/biome": "1.9.4",
    "drizzle-kit": "0.27.0",
    "vitest": "^3.0.0",
    "@playwright/test": "^1.48.0",
    "@types/node": "22.10.1",
    "@types/nodemailer": "6.4.16"
  }
}
```

**注**：T001 spike 通过后再按选定 provider 加 `@anthropic-ai/sdk` 或 `openai`，**只加一个**。

---

## 6. 本地开发环境（最少依赖）

| 工具 | 用途 | 安装方式 |
|---|---|---|
| Node 22 LTS | 运行时 | `nvm install 22` 或 mise |
| pnpm 9 | 包管理 | `npm i -g pnpm@9` 或 corepack |
| Postgres 16 | 数据库 | macOS = `brew install postgresql@16`；Linux = `apt install postgresql-16` |
| Biome | lint/format | 从 devDeps 拉，不需要全局 |

**CI**：GitHub Actions 单 workflow，跑 `pnpm install --frozen-lockfile && pnpm biome ci && pnpm vitest run && pnpm playwright test`。

---

## 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · 主栈 commit · LLM 推迟到 T001 spike · 排除清单 |
| 2026-04-23 | 0.1.1 | **Drift consolidation**（随 spec.md v0.2.2）：§2.4 LLMProvider interface 统一 camelCase（`summaryText` / `promptVersion` / `modelName` 等 · drift 1）+ judgeRelation 改 per-pair（单对 StateShiftVerdict · drift 2）· `RelationLabel` 从 `{supports/contradicts/supersedes/unrelated}` 改 `{shift/incremental/unrelated}` 与 `reference/llm-adapter-skeleton.md §2` 对齐；§2.2 OpenAI output pricing $10/M → $15/M（2026-04 公开价 · R1 Codex refreshed · drift 3）· 月度估 $10.5/月 → $12/月（仍 << C11 envelope $50）。Primary stack 未变。 |
| 2026-04-24 | 0.1.1（R_final2 G6 sync） | §2.4 `SummaryRecord` 加 `llmCallId: number \| null` + `requestHash: string` 字段（与 `reference/llm-adapter-skeleton.md §2` 同步 · adapter 内部写 `llm_calls` 并把 id 回传）· LLMProvider `summarize` / `judgeRelation` 方法注释改为 adapter-内写 `llm_calls`（caller 只写 `paper_summaries`）· `StateShiftVerdict` shape 加 `anchorPaperId` 以与 skeleton 一致 · 契约段明确 "fallback 路径允许 `llmCallId=null`（schema F5）" · Primary stack / pricing / 排除清单 / dependency policy 全未变。 |
