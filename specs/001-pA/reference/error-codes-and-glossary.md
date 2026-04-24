# Error Codes & Extended Glossary · 001-pA · PI Briefing Console

**版本**: 0.2（R_final2 G9 sync · 2026-04-24 · +CSRF_ORIGIN_MISMATCH · invite 路径更新 · schema_version→schemaVersion）
**创建**: 2026-04-23
**对应 spec**: `spec.md` v0.3.1 · `architecture.md` v0.2 · `api-contracts.md` v0.1 · `reference/schema.sql` v0.2.3 · `reference/llm-adapter-skeleton.md` v0.2
**读者**: 后端 API 实现者 · 前端 error-envelope 消费者 · on-call operator（查日志定位故障）· 新加入初级工程师（名词速查）

> 本文件是 **错误码** 与 **术语** 两个维度的权威合集。`api-contracts.md §4` 是面向 HTTP 层的 error code catalog；本文件在此之上**增量**加入"不经 HTTP 路径出现的内部 error"（Worker / DB / Infra），并给出统一的日志级别约定 + 完整术语表。与 `api-contracts.md §4` 不冲突，而是**超集**（外加 server-side / DB / worker-only 错误）。冲突时 **HTTP 层以 `api-contracts.md` 为准**；DB / worker / infra 错误以本文件为准。

---

## §1 Error code 权威表（扩展 `api-contracts.md §4`）

### 1.1 表结构说明

每条错误给出 7 列：

| 列 | 含义 |
|---|---|
| Code | 稳定机器码（SCREAMING_SNAKE_CASE）· grep-able |
| Layer | 抛错的架构层 · 见 §1.2 |
| HTTP | 若可达到 HTTP 响应 · 则列 status；纯 worker / DB-only 留 `—` |
| Thrown by | 代码位置 · 相对 `src/` 路径（便于 code review grep） |
| When | 触发条件 · 一句话 |
| Recovery | 期望的下一步动作（API 消费者 / operator） |
| User message | 面向终端用户的中文消息（`zh-CN`）· 无则写 `—`（内部 error 不对外） |

### 1.2 Layer 标识

| Layer | 含义 | 主要文件位置 |
|---|---|---|
| API | HTTP route handler / middleware | `src/app/api/**/route.ts` · `src/lib/auth/middleware.ts` · `src/lib/http/errors.ts` |
| Auth | Session / Invite / ACL | `src/lib/auth/**` |
| DB | Postgres 原生约束 · drizzle 捕获 PgError | `src/db/**` · CHECK / FK / UNIQUE 触发时冒泡到 query builder |
| LLM | adapter / cost gate | `src/lib/llm/**` |
| Worker | daily pass / scheduler | `src/workers/**` |
| Arxiv | arXiv HTTP adapter | `src/lib/arxiv/**` |
| Infra | Process / env / filesystem / systemd | `src/lib/env.ts` · `src/lib/log.ts` · startup |

### 1.3 API 层错误（扩展自 `api-contracts.md §4` · 保持完全一致 · 仅补注）

> 以下 **31 条**（G4 H4 · 2026-04-24 · 新增 `CSRF_ORIGIN_MISMATCH`）与 `api-contracts.md §4` **逐字一致**。本文件不重复写 user message 细节 · 仅标注"已在 `api-contracts.md §4`"避免漂移；修改时请只动一处（api-contracts.md），本表是引用。

| Code | Layer | HTTP | Thrown by | When | Recovery |
|---|---|---|---|---|---|
| `SESSION_EXPIRED` | Auth | 401 | `auth/middleware.ts` | session cookie 无效 / revoked / expired | 浏览器自动 302 /login · API 消费者重新登录 |
| `NOT_ADMIN` | Auth | 403 | `auth/middleware.ts` | 非 admin 访问 admin 路由 | 客户端切 admin 账号或放弃 |
| `NOT_BREADCRUMB_OWNER` | Auth | 403 | `resurface/route.ts` · `breadcrumbs/route.ts` | seat 不是 breadcrumb 的 owner | 仅展示 "不是你的 breadcrumb" 提示 |
| `INVALID_EMAIL` | API | 400 | `invite/route.ts` | email 不合 RFC5322 | 用户修正 |
| `INVALID_ROLE` | API | 400 | `invite/route.ts` | role 不在 enum | 用户修正 |
| `INVALID_TOPIC_INPUT` | API | 400 | `topics/route.ts` | zod fail | 用户修正 |
| `INVALID_ACTION` | API | 400 | `actions/route.ts` | action 不在 enum | 用户修正 |
| `INVALID_TOKEN` | API | 400 | `invite/consume/route.ts` | token 格式错（非 64-hex · G4 H4 权威路径） | 用户向 admin 索要新 invite |
| `CSRF_ORIGIN_MISMATCH` | API | 403 | `invite/consume/route.ts` | Origin header 不匹配 `APP_ORIGIN` · G4 H4 · 2026-04-24 · POST `/api/invite/consume` 强制 | 客户端检查 Origin header · 重新发起请求 |
| `SKIP_WHY_REQUIRED` | API | 400 | `actions/recordAction.ts` | skip action 未附 why 或 btrim < 5 chars · D16 Layer 2 | UI 提示补填 |
| `WHY_TOO_LONG` | API | 400 | `actions/route.ts` | why > 280 chars | 用户缩短 |
| `EMAIL_ALREADY_INVITED` | API | 409 | `invite/route.ts` | seats 存在且 invite_token_hash 未消费 | admin 查 seats 再处理 |
| `EMAIL_ALREADY_JOINED` | API | 409 | `invite/route.ts` | seat 已消费 invite | admin 认知错误 |
| `TOPIC_NAME_CONFLICT` | API | 409 | `topics/route.ts` | 同 lab 下 name 重 | 改名 |
| `TOPIC_ALREADY_ARCHIVED` | API | 409 | `topics/[id]/route.ts` | 重复 DELETE 归档 topic | 无动作 |
| `DUPLICATE_ACTION` | API | 409 | `actions/recordAction.ts` | 同 seat+paper+action 60s 内重复 | 视为成功 · 不重试 |
| `IDEMPOTENCY_MISMATCH` | API | 409 | `http/idempotency.ts` | 同 Idempotency-Key 但 body 不同 | 客户端换 key 重试 |
| `RESURFACE_ALREADY_DISMISSED` | API | 409 | `resurface/[id]/dismiss/route.ts` | 重复 dismiss | 无动作 |
| `BREADCRUMB_NOT_DISMISSED` | API | 409 | `breadcrumbs/[id]/re-breadcrumb/route.ts` | 对未 dismissed breadcrumb 再 breadcrumb | 无意义 · 客户端 block |
| `INVITE_TOKEN_EXPIRED` | Auth | 410 | `invite/consume/route.ts` | TTL 过期 或 已消费（G4 H4 · POST body-token 权威路径；旧 `invite/[token]/consume/route.ts` path-based 已废弃） | 索要新 invite |
| `PAPER_NOT_IN_LAB_TOPICS` | API | 422 | `actions/recordAction.ts` | breadcrumb 但 paper 无 topic 匹配 | UI 只允许在 /today 上 breadcrumb |
| `TOO_MANY_TOPICS` | API | 422 | `topics/route.ts` | > 15 active topics | admin 先 archive |
| `PAPER_NOT_FOUND` | API | 404 | `papers/[id]/*/route.ts` | paperId 不存在 | 客户端无动作 |
| `TOPIC_NOT_FOUND` | API | 404 | `topics/[id]/route.ts` | topic id 不存在 | 同上 |
| `BREADCRUMB_NOT_FOUND` | API | 404 | `breadcrumbs/[id]/route.ts` | breadcrumb id 不存在 | 同上 |
| `RESURFACE_NOT_FOUND` | API | 404 | `resurface/[id]/route.ts` | resurface id 不存在 | 同上 |
| `NO_BRIEFING_YET` | API | 404 | `today/route.ts` | lab 从未产出 briefing | UI 引导去 /topics |
| `RATE_LIMITED` | API | 429 | v0.2 预留 | 超 rate limit | 按 Retry-After 等 |
| `EXPORT_FAILED` | API | 500 | `export/full/route.ts` | `buildFullExport` 抛错 | operator 查日志 · 重试 |
| `HEALTH_DEGRADED` | Infra | 500 | `healthz/route.ts` | DB ping 失败 | operator I2 流程 |
| `LLM_BUDGET_EXCEEDED` | LLM | 503 | `llm/audit.ts::recordLLMCall` | 月累计成本 + 本次 > $50 | worker skip 当前 paper · operator review |

### 1.4 内部 / worker-only 错误（本文件新增 · 不在 `api-contracts.md`）

以下错误**不会**返回给浏览器（除非走入 500 兜底）· 通过 journalctl / `fetch_runs.error_text` / worker 日志暴露。

| Code | Layer | HTTP | Thrown by | When | Recovery |
|---|---|---|---|---|---|
| `LLM_PROVIDER_DOWN` | LLM | — | `llm/select.ts::callWithFallback` | primary provider 抛 retryable Error · 尝试 fallback 时 fallback 也抛 | worker 写 fetch_runs.error · 当日 briefing 退化 |
| `BOTH_PROVIDERS_DOWN` | LLM | — | 同上 | primary + fallback 同时故障 | T013 走 `fallback-heuristic-v1` 写 `paper_summaries` · 见 `llm-adapter-skeleton.md §9.4` |
| `LLM_SCHEMA_VIOLATION` | LLM | — | `llm/anthropic.ts` · `llm/openai.ts` | judgeRelation JSON 响应未通过 `VerdictSchema.parse` | adapter 自动重试 1 次；仍失败 → LLMProviderError(retryable=true) |
| `LLM_JSON_PARSE_FAILED` | LLM | — | adapter `extractJSON` + `JSON.parse` | LLM 返回非 JSON 文本（markdown 乱码等） | 同上 |
| `LLM_EMPTY_RESPONSE` | LLM | — | adapter `extractText` | content 数组为空 / 没有 text block | 同上 |
| `LLM_PII_DETECTED_IN_PROMPT` | LLM | — | `llm/sanitize.ts::stripPII` | prompt 中检测到邮箱 / SEC-4 | adapter **拒绝调用** · 抛 LLMProviderError(retryable=false) · worker 跳过该 paper |
| `ARXIV_RATE_LIMITED` | Arxiv | — | `arxiv/client.ts` | arXiv 返 429 | adapter exponential backoff 3 次 · 仍失败 → fetch_runs.status='partial' |
| `ARXIV_SCHEMA_MISMATCH` | Arxiv | — | `arxiv/parser.ts` | Atom XML 中缺 required field | 跳过该 paper · 写 fetch_runs.notes · alert |
| `ARXIV_NETWORK_ERROR` | Arxiv | — | `arxiv/client.ts` | DNS / TLS / timeout | 3 次 retry |
| `SUMMARY_CHECK_VIOLATION` | DB | — | `@/db` PgError 冒泡（error code `23514`） | `summary_sentence_cap` 触发 · adapter 截断失效 | worker 重试一次（truncate 更狠）· 仍失败 → skip paper · alert |
| `SKIP_WHY_DB_REJECT` | DB | — | 同上 | `skip_requires_why` 被直接 SQL 命中（API 应已拦截） | 视为 bug · 升级为 P1 · 审查 API 层 |
| `TOPIC_UNIQUE_VIOLATION` | DB | — | 同上 | 同 lab name 重 | API 层应转换为 `TOPIC_NAME_CONFLICT` |
| `SESSION_UNIQUE_VIOLATION` | DB | — | 同上 | `sessions.token_hash` 重（天文概率） | 极少 · 视为 P1 |
| `DB_CONNECTION_LOST` | DB | 503（若发生在 request path） | `db/client.ts` pool | Postgres 重启 / 网络断 | systemd 拉起 web · 客户端重试 |
| `DB_MIGRATION_DRIFT` | Infra | — | CI `schema-drift` job | `src/db/migrations/*.sql` 与 `reference/schema.sql` 不一致 | 看 diff · 改正 schema 或重新 generate |
| `ENV_VALIDATION_FAILED` | Infra | — | `lib/env.ts::zodParse` | 启动期 env 不符 zod schema | operator 补 env · restart |
| `CRON_CATCHUP_TRIGGERED` | Worker | — | `workers/daily.ts` startup | on-boot 发现 last_success < 24h | info level · 非 error · 仅记录 |
| `CRON_WINDOW_MISSED` | Worker | — | `workers/daily.ts` | > 24h 未运行（重启 > 24h） | worker 不 catchup（超窗）· 下次 06:00 跑 · operator 收 worker-watch 邮件 |
| `BRIEFING_DUP_KEY` | DB | — | `workers/briefing-pass.ts` INSERT | `briefings_lab_topic_date_uniq` 冲突 | worker 走 UPSERT ON CONFLICT DO UPDATE（`workers/briefing-pass.ts` 的标准路径 · 不应抛到外层） |
| `STATE_SHIFT_HEURISTIC_NOISY` | Worker | — | `state-shift/heuristic.ts` | 某 topic 7 天内 shift 数 > daily_cap（v0.1 = 5） | 仅 warn log · operator mute topic（future） |

### 1.5 错误码 vs HTTP status 对照（便于前端）

| HTTP | 典型 code |
|---|---|
| 400 | `INVALID_*` · `SKIP_WHY_REQUIRED` · `WHY_TOO_LONG` |
| 401 | `SESSION_EXPIRED` |
| 403 | `NOT_ADMIN` · `NOT_BREADCRUMB_OWNER` · `CSRF_ORIGIN_MISMATCH`（G4 H4） |
| 404 | `*_NOT_FOUND` · `NO_BRIEFING_YET` |
| 409 | `*_ALREADY_*` · `*_CONFLICT` · `DUPLICATE_ACTION` · `IDEMPOTENCY_MISMATCH` · `EMAIL_ALREADY_*` · `TOPIC_NAME_CONFLICT` · `BREADCRUMB_NOT_DISMISSED` |
| 410 | `INVITE_TOKEN_EXPIRED` |
| 422 | `PAPER_NOT_IN_LAB_TOPICS` · `TOO_MANY_TOPICS` |
| 429 | `RATE_LIMITED`（v0.2） |
| 500 | `EXPORT_FAILED` · `HEALTH_DEGRADED` |
| 503 | `LLM_BUDGET_EXCEEDED` |

### 1.6 Error envelope 语言规约

- **user-facing message（`error.message`）**：**中文（`zh-CN`）** · 见 `api-contracts.md §4` 第 "用户可见中文消息" 列 · 本文件不重复
- **engineer-facing log line**：**英文** · 每行 JSON 结构化（pino-style）· 至少包含 `{ level, code, msg, path, requestId }`
- **error.code 字面值**：**英文** · SCREAMING_SNAKE_CASE · 任何实现代码必须从 `src/lib/http/errors.ts` 的 `const` 集合里 pick · 禁止内联字面量（便于 grep）

### 1.7 错误码新增流程

引入一个新 error code 需要：

1. 在本文件 §1.3 或 §1.4 加一行（填全 7 列）
2. 在 `src/lib/http/errors.ts` 加对应常量 + TS union type
3. 在 `api-contracts.md §4` 加对应行（若是 API 错误）· 含中文 user message
4. 在 `tests/unit/` 相应文件加一个正向触发 case（至少断言 error.code 与 HTTP status）
5. 在对应 error envelope 消费方（前端 / worker log parser）加处理分支
6. CI `tests/meta/error-code-registry.test.ts` 验证本文件 ↔ `api-contracts.md` ↔ `src/lib/http/errors.ts` 三者 enum 一致

---

## §2 Log levels · 使用约定

### 2.1 五级定义

| Level | 含义 | 举例 | Destination |
|---|---|---|---|
| `debug` | 仅 dev · 详细 trace | `fetched 47 papers for topic=1 in 832ms` | stdout · 生产禁用 |
| `info` | 正常事件 | `briefing assembled for lab=1 for_date=2026-04-24 items=12` · `session created for seat=7` | stdout (JSON) → journalctl |
| `warn` | 可恢复的异常 | `LLM fallback engaged: anthropic returned 503; retrying with openai` · `[COST-WARN] monthly cumulative=4212 cents > 4000` | stdout · operator 每周 review grep `warn` |
| `error` | 操作失败 · 用户或 operator 可见 | `export failed for lab=1: disk full` · `ARXIV_SCHEMA_MISMATCH on paper=2305.18290` | stdout · 触发 alert 的前置信号 |
| `fatal` | 进程将终止 | `DB_CONNECTION_LOST on startup: cannot reach postgres` · `ENV_VALIDATION_FAILED: SESSION_SECRET too short` | stdout · systemd 重启 |

### 2.2 No `trace`

v0.1 不启用 `trace` level（vitest / pino 默认有，但本项目视同 `debug`）。若未来真需要细粒度 per-request 追踪 · v0.2 引入 OpenTelemetry · 并拆出 `trace.md`。

### 2.3 Structured log 字段约定

所有 `src/lib/log.ts` 输出的日志必须带以下字段（JSON）：

```jsonc
{
  "level": "info",               // debug | info | warn | error | fatal
  "time": "2026-04-24T06:02:11.123Z",
  "msg": "briefing assembled",   // 短句 · 以动词开头 · 不带标点
  "code": "BRIEFING_ASSEMBLED",  // 稳定机器码 · 若为 error 则填 error code from §1
  "service": "worker",           // worker | web | startup
  "path": "/api/actions",        // 仅 Web 请求上下文
  "requestId": "7f2c1a9b-...",   // UUIDv7 · 仅 Web 请求
  "seatId": 7,                   // 可选 · 可从 session 抽
  "labId": 1,                    // 可选
  "durationMs": 832,             // 可选
  "err": { "name": "LLMProviderError", "message": "...", "stack": "..." }   // 仅 error / fatal
}
```

### 2.4 日志绝不写的字段（敏感）

| 绝不 log | 理由 | 替代 |
|---|---|---|
| `session cookie value` | 泄露 = account takeover | 只 log `sessionId`（= sessions.id 数字） |
| `invite token plaintext` | 泄露 = 邀请被盗 | 只 log `invite_token_hash` 前 8 字符 |
| LLM prompt 原文 | 成本 + 可能含 paper abstract（ToS 合规） | 只 log `promptVersion` · `inputTokens` |
| LLM response 原文 | 同上 | 只 log `outputTokens` · `truncated` · adapter 内部处理即丢 |
| `Authorization` header 值 | 同 cookie | — |
| `seats.email`（完整） | PII | 对 info level 可用 hash 前缀 `sha256(email).slice(0,6)` |
| `.env` 里任何 secret | SEC-3 | — |

---

## §3 Extended glossary · 扩展术语表

此表是 `spec.md §Glossary` 的**扩展版**（约 2×）· 对代码里会出现但 spec 未逐字定义的每个术语给出**定义 · 出现位置 · 非同义词**三要素。字段如下：

- **术语**（在代码中的拼写 · 英文 kebab 或 snake）
- **中文译**（若有）
- **定义**（一句话）
- **出现位置**（代码 / 表 / spec 章节）
- **非同义词**（容易混淆的近义词，明确区分）

按字母序排列。

---

### `4-action`

- **中文**：四动作
- **定义**：对一篇候选 paper 可执行的四种标注之一 · 封闭集：`read_now` / `read_later` / `skip` / `breadcrumb`
- **出现**：`spec.md D4` · `architecture.md §5 · actions 表` · `schema.sql §8` · `api-contracts.md §E10`
- **非同义词**：≠ "rating"（4-action 无分数含义）；≠ "tag"（action 不是多值，而是某次动作）

### `active seat`

- **中文**：活跃 seat
- **定义**：过去 30 天内 `sessions` 表中有 ≥ 1 次 login 的 seat
- **出现**：`spec.md §6 Sentinel` · `api-contracts.md E15 activeSeats30d` · `risks.md DOGFOOD-1`
- **非同义词**：≠ "registered seat"（seat 是否活跃看 sessions，不看 seats.created_at）

### `admin`

- **中文**：管理员
- **定义**：`seats.role = 'admin'` 的 seat · 拥有 topic CRUD / invite / export / allow-continue 权限
- **出现**：`schema.sql §2` · `spec.md §IN-5` · `auth/middleware.ts::requireAdmin`
- **非同义词**：≠ "operator"（operator 是角色 / 人设 · 可以是 admin 也可以是 member；`seats.role='admin'` 是 DB 级别 ACL）

### `allow_continue_until`

- **中文**：允许延期截止时间
- **定义**：`labs.allow_continue_until` 列 · operator 点击 `/admin/allow-continue` 时写入的未来时间戳 · sentinel 在 `now() < allow_continue_until` 时不阻塞新 feature
- **出现**：`schema.sql §1` · `spec.md D8 Sentinel` · `api-contracts.md E16`
- **非同义词**：≠ "session expires_at"（后者是登录过期 · 与项目治理无关）

### `anchor paper`

- **中文**：锚点论文
- **定义**：在 state-shift 判定中 · 被 ≥ 2 篇新 paper 引用且引用立场冲突的那篇早期工作
- **出现**：`spec.md §4.1` · `architecture.md §5 briefings.anchor_paper_id` · `schema.sql §11`
- **非同义词**：≠ "candidate paper"（anchor 是历史的 · candidate 是当前判 shift 的新 paper）

### `api-contracts.md`

- **定义**：本项目 HTTP API / Server Action 契约的权威单一来源
- **出现**：`specs/001-pA/reference/api-contracts.md`
- **非同义词**：≠ OpenAPI（本项目不用 OpenAPI spec 文件）· ≠ Swagger UI

### `assembled_at`

- **定义**：`briefings.assembled_at` 列 · 当天 briefing 写入 DB 的时间戳（worker 完成时刻）
- **出现**：`schema.sql §11` · `api-contracts.md §3.5 Briefing`
- **非同义词**：≠ `for_date`（前者是 wall-clock · 后者是 briefing 覆盖的目标日期）· ≠ `fetched_at`

### `authoritative DDL`

- **中文**：权威 DDL
- **定义**：部署到 prod 的 schema 定义的真实来源
- **出现**：`directory-layout.md §1` · `DECISIONS-LOG 2026-04-23 Drizzle 双轨`
- **非同义词**：项目里有 3 份 DDL 表述（`schema.sql` · `src/db/schema.ts` drizzle · `src/db/migrations/0000_initial.sql`）· 三者由 CI 验证一致

### `briefing`

- **中文**：简报
- **定义**：每日 06:00 预计算生成的 per-lab 一页报告 · 按 topic 列出 state 摘要 + 至多 3 篇触发论文
- **出现**：`spec.md §Glossary` · `schema.sql §11` · `architecture.md §2 ADR-1`
- **非同义词**：≠ "newsletter"（不是定期通讯 · 是 state-change digest）· ≠ "feed"（不是按论文堆叠）

### `breadcrumb`

- **中文**：面包屑
- **定义**：一种 4-action · 语义 = "当下判定不值得读但 keep 留痕 以便未来 resurface" · 会同步写 `breadcrumbs` 表
- **出现**：`schema.sql §9` · `spec.md D4` · `api-contracts.md E10`
- **非同义词**：≠ `skip`（skip 是"判过不读且不想再见"）· ≠ "favorite"（breadcrumb 不是收藏 · 是"未来或许还会回来"）

### `bus factor`

- **中文**：公车因子
- **定义**：项目可失去多少关键人员而仍存续 · v0.1 = 1（单 operator）
- **出现**：`risks.md BUS-1` · `spec.md C13`
- **非同义词**：≠ "team size"（bus factor 关心 critical path 上几个人 · 不是总人数）

### `candidate paper`

- **中文**：候选论文
- **定义**：当日被 `paper_topic_scores` 匹配进某 topic · 等待 state-shift 判定的新 paper
- **出现**：`spec.md §4.1` · `llm-adapter-skeleton.md §2 JudgeRelationInput`
- **非同义词**：≠ `anchor paper`（见上）

### `Caddyfile`

- **定义**：Caddy 反代的配置文件 · 本项目存 `deploy/caddy/Caddyfile`
- **出现**：`ops-runbook.md §5` · `directory-layout.md §1`
- **非同义词**：≠ `nginx.conf`（本项目不用 nginx）

### `catchup`

- **中文**：追补
- **定义**：worker on-boot 或长时 downtime 后 · 自动回补过去 24h 内漏跑的一次 fetch + summary + briefing pass
- **出现**：`architecture.md §1 · 第 5 条` · `SLA.md §1.3` · `ops-runbook.md §9.I1`
- **非同义词**：≠ "retry"（retry 是单次调用级 · catchup 是 run 级）

### `CHECK constraint`

- **定义**：Postgres 约束 · 在 INSERT/UPDATE 时执行布尔谓词 · 失败抛 PgError code `23514`
- **出现**：`schema.sql §8 skip_requires_why` · `schema.sql §14 summary_sentence_cap`
- **非同义词**：≠ FK constraint（FK 查父表存在）· ≠ UNIQUE（UNIQUE 查行级去重）

### `citation trigger`

- **中文**：引用触发
- **定义**：新 paper 进入同 topic 且引用了用户 breadcrumb 过的某 paper · 立即 resurface · 优先级高于 timed schedule
- **出现**：`spec.md §4.2` · `resurface/citation.ts` · `risks.md TECH-7`
- **非同义词**：≠ timed trigger（后者是按 6w/3mo/6mo 时间表）

### `compliance self-audit`

- **定义**：operator 每月月初花 15 分钟执行的 6 项 checklist
- **出现**：`compliance.md §7` · `ops-runbook.md §10 回归后第 1 天`
- **非同义词**：≠ "external audit"

### `cost envelope`

- **中文**：成本信封
- **定义**：C11 规定的月度 LLM token 成本上限 · $50 USD · 由 `audit.ts::MONTHLY_BUDGET_CENTS = 5_000` 守
- **出现**：`spec.md C11` · `llm-adapter-skeleton.md §7`
- **非同义词**：≠ "infra budget"（VPS / B2 的钱不算在 envelope 里）

### `cron catchup`

- 见 `catchup`

### `CSP` · Content-Security-Policy

- **定义**：由 Caddy 向 HTML 响应注入的安全 header · 防 XSS / frame-ancestors / form-action
- **出现**：`api-contracts.md §1.8` · `ops-runbook.md §5`
- **非同义词**：≠ "CSRF"（见下）

### `CSRF`

- **定义**：Cross-Site Request Forgery · 本项目靠 `SameSite=Lax` cookie + Origin check 防御
- **出现**：`architecture.md §7 · Origin header` · 登入 middleware
- **非同义词**：≠ CSP

### `dogfood`

- **中文**：吃自家狗粮
- **定义**：团队成员使用自家产品 · 用于验证 v0.1 假设
- **出现**：`risks.md DOGFOOD-1/2/3` · `spec.md D8`
- **非同义词**：≠ "beta testing"（dogfood 成员是团队内部 · 不是外部）

### `DOGFOOD-1 sentinel`

- **定义**：day-30 时检查 `active_seats_30d` · 若 < 3 则触发 escalate banner · 阻塞新 feature 直到 operator 签 allow-continue 或 pivot
- **出现**：`spec.md §6 Sentinel` · `api-contracts.md E15 sentinelState` · `risks.md DOGFOOD-1`
- **非同义词**：≠ "A/B test"

### `drift-scan`

- **定义**：CI job 名字 · 比对 drizzle `0000_initial.sql` 与 `reference/schema.sql` 是否同步
- **出现**：`directory-layout.md §9`

### `email token invite`

- **定义**：admin 点 `/admin/invite` 生成 64-hex token · URL 形如 `https://<domain>/login#invite=<token>`（G4 H4 · fragment-based · 客户端 JS 读 fragment 后 POST `/api/invite/consume` body · 2026-04-24）· 手工（不走邮件）传给被邀者
- **消费**：`POST /api/invite/consume` + body `{"token": "<64-hex>"}` + Origin header 校验（`CSRF_ORIGIN_MISMATCH` 守门）· 见 `api-contracts.md §E2`
- **出现**：`spec.md §IN-5` · `schema.sql §2 seats.invite_token_hash` · `DECISIONS-LOG 2026-04-23 invite 不发邮件` · `DECISIONS-LOG drift-5 amendment 2026-04-24`
- **非同义词**：≠ "magic link email"（本项目 v0.1 没有 email 发送 · DECISIONS-LOG 明确）
- **Deprecated**：旧 GET `login/verify?token=...` 与 path-based `invite/[token]/consume/route.ts` 已废弃（G4 H4 · R_final · 2026-04-24）· 改用 POST `/api/invite/consume` + body token

### `empty state`

- **中文**：空态
- **定义**：当 `topics` 表 < 3 行时 · `/today` 显示的引导 UI（而非崩溃或空白）
- **出现**：`DECISIONS-LOG 2026-04-23 · 初始化 topic 池` · `api-contracts.md E9 NO_BRIEFING_YET`

### `escalate banner`

- **定义**：`DOGFOOD-1` 触发时 · `/today` 顶部红色横幅 · 同时阻塞新 feature 路由
- **出现**：`spec.md §6 Sentinel` · `e2e/sentinel-banner.spec.ts`

### `export envelope`

- **中文**：导出信封
- **定义**：`/api/export/full` 响应的 JSON 根对象 · `schemaVersion='1.1'` · 见 `api-contracts.md §3.11`
- **出现**：`architecture.md §8` · `api-contracts.md §3.11`
- **非同义词**：≠ "backup dump"（export 是 user-authored 数据 · backup 是 DB 级二进制）

### `export_log`

- **定义**：`/api/export/full` 每次成功时同步写入的审计表 · 包含 `row_counts_jsonb` · `byte_size` · `seat_id`
- **出现**：`schema.sql §15` · `risks.md SEC-1` · `compliance.md §2`
- **非同义词**：≠ `fetch_runs`（后者是 worker 审计）

### `fallback heuristic`

- **定义**：LLM 两家 provider 同时故障时 · T013 写 `paper_summaries` 的 `model_name='fallback-heuristic-v1'` · `summary_text` = abstract 头 2 句 + `[⚠️ fallback: LLM unavailable]`
- **出现**：`llm-adapter-skeleton.md §9.4` · `risks.md TECH-1` · `ops-runbook.md §9.I6`
- **非同义词**：≠ "silent degrade"（fallback 有 UI 显式标记 · 诚实降级）

### `fallback provider`

- **定义**：env `LLM_FALLBACK_PROVIDER` 指向的 LLM provider · primary 抛 retryable error 时 `callWithFallback()` 切到此家
- **出现**：`llm-adapter-skeleton.md §5` · `risks.md TECH-3`

### `fetch_runs`

- **定义**：worker 每次 arxiv pass / summary pass 的审计表 · status ∈ {ok, failed, partial, running}
- **出现**：`schema.sql §12` · `workers/daily.ts`
- **非同义词**：≠ `llm_calls`（后者按 LLM 调用粒度 · 前者按 worker pass 粒度）

### `FK` · foreign key

- **定义**：跨表引用约束 · 本项目 ON DELETE CASCADE / RESTRICT / SET NULL 三种行为（见 `schema.sql` 每表注释）

### `fork`

- **定义**：讨论树中的分支 · 本项目当前是 `001-pA`（第 1 个 proposal · PRD fork A）
- **出现**：`PLAYBOOK.md` · `CLAUDE.md §Iron rules`
- **非同义词**：≠ git fork

### `heuristic`

- **中文**：启发式
- **定义**：纯代码规则（无 LLM）· v0.1 state-shift 判定的 fallback / 一部分
- **出现**：`spec.md §4.1` · `src/lib/state-shift/heuristic.ts`
- **非同义词**：≠ "LLM judge"（后者走 provider）

### `http.errors` · `src/lib/http/errors.ts`

- **定义**：统一 error envelope / HTTPError / toErrorResponse 的代码位置
- **出现**：`api-contracts.md §6` · 本文件 §1.6

### `idempotency key`

- **定义**：`Idempotency-Key` header · UUIDv7 推荐 · 由 `/api/actions` / `/api/invite` 使用 · LRU cache TTL 24h
- **出现**：`api-contracts.md §1.4` · `http/idempotency.ts`

### `incremental`

- **定义**：StateShiftVerdict 的 kind 之一 · candidate 对 anchor 是增量改进 · 非 state-changing
- **出现**：`llm-adapter-skeleton.md §2 StateShiftVerdict` · `fixtures/human-labeled-20.json`
- **非同义词**：≠ `shift` · ≠ `unrelated`

### `invariant`

- **中文**：不变式
- **定义**：代码层必须恒真的断言 · 违反 = P1
- **出现**：`compliance.md §4` · `ops-runbook.md §14` · `SLA.md §4`

### `invite token`

- **定义**：64-hex 字符串 · 由 admin 生成 · plaintext 只出现一次（响应 body）· DB 存 sha256 · 24h TTL · 单次使用
- **出现**：`schema.sql §2 seats.invite_token_hash` · `auth/invite.ts`
- **非同义词**：≠ "session token"（invite 是一次性 · session 是持久 30d）

### `judge`

- **定义**：LLM 调用之一 · `purpose='judge'` · 返回 `StateShiftVerdict` · T012 state-shift pass 触发
- **出现**：`llm-adapter-skeleton.md §1.1` · `schema.sql §13 llm_calls.purpose`

### `kill-window`

- **定义**：60 天 · PRD 规定若 day-60 O1/O2/O5 均未达成则回 L2 · 不 pivot
- **出现**：`spec.md §1 Outcomes` · `spec.md D12` · `risks.md COM-3`
- **非同义词**：≠ "deadline"（kill-window 是产品验收时间点 · 非交付时间点）

### `lab`

- **定义**：v0.1 部署单位 · 一个 `labs` 行 · ≤ 15 seat · 单 Postgres 实例
- **出现**：`schema.sql §1` · `spec.md §Glossary`
- **非同义词**：≠ "tenant"（本项目 v0.1 单租户 · lab 是未来多租户的最小划分）

### `last_active_at`

- **定义**：`sessions.last_active_at` · 每次认证请求 bump · 供 sliding expiry 与 BUS-1 sentinel
- **出现**：`schema.sql §3` · `auth/session.ts`

### `LLM`

- **定义**：本项目指 Anthropic Claude Sonnet 4.6 或 OpenAI GPT-5.4 · 二选一
- **出现**：`llm-adapter-skeleton.md` · `spec.md D7`
- **非同义词**：≠ 本地 LLM（v0.1 不支持）

### `LLMProvider interface`

- **定义**：`src/lib/llm/types.ts` 中 `interface LLMProvider { summarize; judgeRelation }`
- **出现**：`llm-adapter-skeleton.md §2` · `architecture.md ADR-4`

### `llm_calls`

- **定义**：LLM 调用审计表 · **不存** prompt / response 原文 · 仅 tokens / cost / latency / paper_id / request_hash
- **出现**：`schema.sql §13` · `architecture.md ADR-6`
- **非同义词**：≠ `paper_summaries`（后者是 derived data · 有 summary_text）

### `member`

- **定义**：`seats.role = 'member'` · 可读所有数据 + 做 4-action · 不能 CRUD topic / invite / export
- **出现**：`schema.sql §2` · `spec.md §IN-5`

### `monthly budget`

- 见 `cost envelope`

### `oncall`

- **定义**：operator 对 systemd 告警邮件响应的角色 · 本项目 oncall = operator 本人（BUS-1）
- **出现**：`ops-runbook.md §9` · `risks.md BUS-1`

### `operator`

- **中文**：运维者（也是项目负责人）
- **定义**：v0.1 的 solo human · 同时担任 admin seat · 亦是 oncall · 亦是 dev
- **出现**：`spec.md §Users` · `CLAUDE.md`
- **非同义词**：≠ "PI"（PI 是首要 persona · operator 是次要 persona；v0.1 同一人可兼）

### `paper_summaries`

- **定义**：LLM 生成的 ≤ 3 句 summary 存放表 · keying by `(paper_id, topic_id, prompt_version)`
- **出现**：`schema.sql §14` · `architecture.md ADR-6` · `spec.md D15`

### `per-topic judgment`

- **定义**：LLM 判定（state-shift / summary）**每 topic 做一次**，lab 内全 seat 共享
- **出现**：`architecture.md ADR-3` · `spec.md §Glossary`
- **非同义词**：≠ per-seat judgment（后者是 v1.0 考虑的方向）

### `PI` · Principal Investigator

- **中文**：实验室负责人
- **定义**：首要用户 persona · Dr. Chen 类型 · v0.1 用 `seats.role='admin'` 承载
- **出现**：`PRD.md` · `spec.md O1` · `architecture.md §2`

### `PII`

- **定义**：Personally Identifiable Information · 本项目只有 `seats.email` 一类 PII · adapter 禁止传 LLM
- **出现**：`compliance.md §2` · `risks.md SEC-4` · `llm/sanitize.ts::stripPII`

### `precompute`

- **定义**：将 LLM / state-shift / briefing assemble 全部在 worker 里算完写 DB · 请求路径只读 DB
- **出现**：`architecture.md ADR-1/ADR-2` · `spec.md §1 constraints`

### `prompt injection`

- **定义**：攻击者把指令塞进 LLM input 数据中 · 让 LLM 违反系统提示
- **出现**：`llm-adapter-skeleton.md §10` · `fixtures/adversarial-abstracts.json`

### `prompt_version`

- **定义**：`v<major>.<minor>-<YYYY-MM>` 格式 · prompt 文案 bump 时+ major/minor · 供 `paper_summaries.unique_key` 区分历史
- **出现**：`DECISIONS-LOG 2026-04-23 · prompt_version 命名规范` · `llm-adapter-skeleton.md §6`

### `red line`

- **中文**：红线
- **定义**：PRD 宪法级硬约束 · 共 3 条 · 违反 = BLOCK
- **出现**：`PRD.md` · `spec.md C5/C6/C7` · `architecture.md §7/ADR-7`
- **非同义词**：≠ "best practice"（红线违反立即中止 · best practice 可 push-back）

### `resurface`

- **定义**：系统把 breadcrumb 重新推到用户视野的行为 · 由 timed 或 citation 触发
- **出现**：`spec.md §4.2` · `schema.sql §10` · `resurface/*.ts`

### `resurface event`

- **定义**：`resurface_events` 表的一行 · 一次 resurface 的发生记录 · 含 surfaced_at / clicked_at / dismissed_at
- **出现**：`schema.sql §10` · `api-contracts.md §3.8`

### `role` · seats.role

- **定义**：`seats.role ∈ {'admin', 'member'}` · 由 CHECK 约束
- **出现**：`schema.sql §2`

### `schemaVersion`

- **定义**：export envelope 的顶层 key · camelCase 权威拼写（G3 · R_final · 2026-04-24）· 当前值 `'1.1'` · bump 规则见 `api-contracts.md §3.11`
- **出现**：`api-contracts.md §3.11` · `DECISIONS-LOG 2026-04-23 · schemaVersion bump 策略`
- **非同义词**：≠ DB schema version（DB schema 由 drizzle migration 编号管 · 不是 `schemaVersion`）
- **Deprecated**：旧 snake_case 拼写 `schema_version` 已废弃（G3 · R_final · 2026-04-24）· export envelope 顶层 key 统一 camelCase，与 12 个 resource collections（`paperSummaries` / `paperTopicScores` 等）一致

### `seat`

- **定义**：一个登录身份 · 挂在单个 lab 实例下 · 由 `seats` 表每行承载
- **出现**：`schema.sql §2` · `spec.md §Glossary`

### `sentinel`

- 见 `DOGFOOD-1 sentinel`

### `session`

- **定义**：登录 session · 由 `sessions` 表每行承载 · token_hash = sha256(JWT) · revoked_at 支持 server-side logout
- **出现**：`schema.sql §3` · `auth/session.ts`

### `shift` · state shift

- **定义**：某 topic 过去 7 天内 · ≥ 2 新 paper 引用同一 anchor 且立场冲突 · §4.1 formal 定义
- **出现**：`spec.md §4.1` · `llm-adapter-skeleton.md §2 StateShiftVerdict`
- **非同义词**：≠ "breakthrough"（shift 是冲突的立场 · 不保证 breakthrough 级别）

### `skip`

- **定义**：4-action 之一 · 语义 = "判过不读且不想再见" · 必须填 why（≥ 5 字 btrim）· 红线 2 守
- **出现**：`schema.sql §8 skip_requires_why` · `spec.md C6/D16`

### `skip why`

- **定义**：action=skip 时 `actions.why` 字段 · btrim 后 ≥ 5 字符 · 三层机械兜底
- **出现**：`spec.md D16` · `architecture.md ADR-7`
- **非同义词**：≠ "comment"（comment 是自由可选 · why 在 skip 时是必填）

### `SLA`

- **定义**：Service Level Agreement · 本项目 v0.1 是 best-effort + 自守红线 · v1.0 才有正式 SLA
- **出现**：`SLA.md`

### `SSR`

- **定义**：Server-Side Render · Next 15 Server Component · `/today` 用此模式
- **出现**：`DECISIONS-LOG 2026-04-23 · /today page 数据 fetch 策略`

### `stale banner`

- **中文**：过期横幅
- **定义**：worker 某天未跑 · `/today` 顶部显示"briefing 数据为 N 天前"软提示
- **出现**：`stale-banner.tsx` · `api-contracts.md E9 meta.staleDate`

### `state-shift heuristic`

- 见 `heuristic`

### `summarize`

- **定义**：LLM 调用之一 · `purpose='summarize'` · 返回 `SummaryRecord` · T013 触发
- **出现**：`llm-adapter-skeleton.md §1.1`

### `summary sentence cap`

- **定义**：`paper_summaries.summary_sentence_cap` CHECK · regex 检测 ≤ 3 句
- **出现**：`schema.sql §14` · `spec.md D15`

### `systemd`

- **定义**：Ubuntu 24.04 的 init 系统 · 本项目所有 daemon / cron / backup 都走 systemd unit + timer
- **出现**：`ops-runbook.md §4` · `directory-layout.md §1`
- **非同义词**：≠ "cron daemon"（本项目不用 `cron` 服务 · 全走 systemd timer）

### `T001 spike`

- **定义**：Phase 0 的 blocking task · LLM provider blind-test · ≥ 70% 准确率才允许 Phase 1 开工
- **出现**：`spec.md §5 Phase 0` · `llm-adapter-skeleton.md §8` · `tasks/T001.md`

### `topic`

- **定义**：PI 手动维护的关注方向 · 包含 `{keyword_pool, arxiv_categories, seed_authors}` · 一 lab 8–15 topic
- **出现**：`schema.sql §4` · `spec.md §Glossary`

### `trigger paper`

- **定义**：state-shift 时 · 引用 anchor 的 candidate paper · briefings.trigger_paper_ids 存 ≤ 3 id
- **出现**：`schema.sql §11 briefings.trigger_paper_ids` · `spec.md §4.1`

### `truncateTo3Sentences`

- **定义**：`src/lib/llm/truncate.ts` · 应用层兜底截断（LLM 返 4+ 句时）· DB CHECK 是最后防线
- **出现**：`llm-adapter-skeleton.md §3 anthropic adapter`

### `TTL`

- **中文**：存活时间
- **定义**：本项目只有一处 TTL · `seats.invite_expires_at = now() + 24h`（env `INVITE_TOKEN_TTL_HOURS=24`）
- **出现**：`schema.sql §2` · `directory-layout.md §3 env`

### `unrelated`

- **定义**：StateShiftVerdict kind 之一 · candidate 与 anchor 无实质联系（即使 keyword 重叠）
- **出现**：`llm-adapter-skeleton.md §2`

### `UPSERT`

- **定义**：Postgres 的 `INSERT ... ON CONFLICT DO UPDATE` · 本项目 `paper_summaries` 写入时用（worker 重跑幂等）
- **出现**：`llm-adapter-skeleton.md §2 SummaryRecord doc` · `workers/summary-pass.ts`

### `webapp_user` / `worker_user`

- **定义**：两个 Postgres role · 分别给 Next.js 进程和 worker 进程用 · 最小权限原则
- **出现**：`architecture.md §7` · `deploy/postgres/grants.sql`

### `worker`

- **定义**：`src/workers/daily.ts` · systemd oneshot · 06:00 local cron · 负责 arxiv fetch + summary + state-shift + briefing + resurface
- **出现**：`directory-layout.md §1` · `ops-runbook.md §4.2/4.3`
- **非同义词**：≠ "cron job"（本项目 cron 由 systemd 承载 · 不用 `cron` daemon）

### `zod`

- **定义**：TypeScript runtime schema 校验库 · 本项目用于 env / request body / LLM response 三处
- **出现**：`directory-layout.md §2 deps` · `env.ts` · `api-contracts.md §2 E10`

---

## §4 Cross-consistency 链

本文件与其他 reference 文档的一致性约束（CI `tests/meta/error-code-registry.test.ts` 若未来实现 · 以下为人工维护检查项）：

| 文件 | 约束 |
|---|---|
| `api-contracts.md §4` | 30 条 HTTP error · 本文件 §1.3 必须逐字一致 |
| `src/lib/http/errors.ts` | `const ERROR_CODES` 必须覆盖 §1.3 + §1.4 中所有 code · 类型为 const union |
| `tests/meta/error-code-registry.test.ts`（未来） | 三源 code 集合必须相等 |
| `compliance.md §4 Invariants` | 本文件 §3 Glossary 对 invariant 的定义必须一致 |
| `spec.md §Glossary` | 本文件 §3 是其**超集** · 不得与 spec.md 定义冲突 |

---

## 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · §1 API error（30 条 · 同步自 api-contracts.md §4）+ 内部 error（20 条 · 新增）· §2 log levels + 禁写字段 · §3 extended glossary 60+ 词条（~2× spec.md §Glossary）· §4 cross-consistency 链 |
| 2026-04-24 | 0.2 | **Patch（R_final2 G9 mechanical sync）**：§1.3 加 `CSRF_ORIGIN_MISMATCH` 行（G4 H4 · HTTP 403 · `invite/consume/route.ts` · Origin 不匹配 APP_ORIGIN） · API error 总数 30 → **31**（31 HTTP + 20 worker/DB/infra = 51 total）· `INVALID_TOKEN` 与 `INVITE_TOKEN_EXPIRED` 的 Thrown by 路径更新到 `invite/consume/route.ts`（旧 path-based 注明 deprecated）· §1.5 HTTP→code 对照表 403 补 `CSRF_ORIGIN_MISMATCH` · §3 Glossary 段 `email token invite` 条目 URL 模板改为 `login#invite=<token>` + POST `/api/invite/consume` + Origin 校验（旧 GET `login/verify?token=...` 注 Deprecated）· `schema_version` 条目改为 `schemaVersion` camelCase（旧 snake_case 注 Deprecated · G3 R_final export envelope 权威拼写） |
