# API Contracts · 001-pA · PI Briefing Console

**版本**: 0.4
**创建**: 2026-04-23
**上次修订**: 2026-04-24（R_final BLOCK fix G3 schemaVersion/casing + G4 H4 POST invite · 见变更日志）
**对应 spec**: `spec.md` v0.3.0 · `architecture.md` v0.3 · `tech-stack.md` v0.1
**读者**: 实现 API route 的后端工程师 + 消费 API 的前端工程师 + 跑 E2E 的测试工程师

> 本文件是所有 HTTP / Server Action 契约的**权威单一来源**。每个 endpoint 描述为"一个 T 任务的实现合同"；与 `spec.md §6 verification hooks` / `tasks/T015.md` / `tasks/T016.md` / `tasks/T023.md` / `tasks/T027.md` 对齐。代码里任何 endpoint 的行为偏离本文件 = bug。**冲突以 spec.md / architecture.md 为准**。

---

## §1 Global conventions

### 1.1 基础信息

| 项 | 值 |
|---|---|
| **Base URL** | `${APP_ORIGIN}`（本地 `http://localhost:3000` · 生产 `https://<operator-domain>`） |
| **Content-Type 默认** | `application/json; charset=utf-8`（除 `/api/export/full` 下载） |
| **Protocol** | HTTPS in production · HTTP in local dev（reverse-proxy = Caddy） |
| **路由位置** | 全部位于 `src/app/api/**/route.ts`（Next 15 App Router）· 直接 SSR fetch 走 Server Action（`src/app/(main)/*/actions.ts`） |
| **HTTP methods** | 按 REST 语义：GET（读）· POST（创建）· PATCH（局部更新）· DELETE（软/硬删） |

### 1.2 认证

所有 endpoint **默认 require auth**（通过 `requireAuth` / `requireAdmin` middleware）；例外显式标注 "no auth"。

- **Cookie**：`pi_session`（httpOnly · Secure · SameSite=Lax · Max-Age 动态滑动 30 天）
- **Cookie value**：JWT HS256 签名，payload `{sub: seat_id, lab: lab_id, role: 'admin'|'member', iat, exp}`
- **验证**：中间件读 cookie → verify JWT signature → 查 `sessions` 表（`token_hash = sha256(cookie_value)` AND `revoked_at IS NULL` AND `expires_at > now()`）→ bump `last_active_at`
- **失败**：401 `SESSION_EXPIRED`（未登录访问受保护路由时 **浏览器访问自动 302 到 `/login`**；API 直接请求返 JSON 401）

### 1.3 Error envelope 规范

**所有**失败响应统一形态（禁止各 route 自造 shape）：

```jsonc
{
  "error": {
    "code": "SKIP_WHY_REQUIRED",              // 稳定机器码；见 §4 catalog
    "message": "skip 必须填写 why (至少 5 字符)",   // 面向终端用户的中文消息（默认 zh-CN）
    "fields": {                                // 可选；字段级错误映射
      "why": "至少需要 5 个非空白字符"
    },
    "requestId": "7f2c1a9b-..."                // 可选；与 server 日志关联，便于 operator 排错
  }
}
```

**Success envelope**：payload 直接返回（无统一包装）；仅当 endpoint 语义上需要元数据（如 `/api/today` 的 `staleDate`）时才外层包一层 `{data, meta}`。

**HTTP status vs code**：HTTP status 反映 HTTP 语义（200/201/204/400/401/403/404/409/410/422/429/500/503）；`error.code` 反映**业务语义**；两者独立但成对出现。例如 "skip why 不足"是 400 `SKIP_WHY_REQUIRED`（参数错误语义），"email 已被邀请"是 409 `EMAIL_ALREADY_INVITED`（资源冲突语义）。

### 1.4 Idempotency

- **写入 endpoint**（POST / PATCH / DELETE）**可选** `Idempotency-Key` header（UUIDv7 推荐）
- 作用范围：`(seat_id, endpoint, key)` 三元组；TTL 24h（由内存 LRU cache 实现即可，Postgres 不需要新表；v0.1 规模 ≤ 15 seat × 24h × 每 seat 估计 < 100 个 key = 可忽略内存）
- 行为：
  - 首次见此 `(seat, endpoint, key)` → 正常执行并记录 response
  - 同 key 第二次 → **直接返回首次的 response**（完全相同 body + status）
  - 同 key 但 body 不同 → 409 `IDEMPOTENCY_MISMATCH`
- v0.1 **实现**层：`/api/actions` 与 `/api/invite` 必须支持（防网络抖动造成的重复 4-action 或重复邀请）；其他 endpoint 可先不做（由 T015 / T027 实现）

### 1.5 Rate limit

v0.1 **不实现** explicit rate limit。理由：≤ 15 seat 无真实流量压力；引入 rate limit 会多一个调优点（risks.md OPS 栏位空间有限）。**软上限记录**：`10 req/s per seat`；超过此速率行为未定义。`/api/invite` 管理路由建议前端加防抖（5 秒内重复点击只触发一次），服务端无限流。

未来 v0.2 若启用 rate limit，响应：429 `RATE_LIMITED` + header `Retry-After: <seconds>`。

### 1.6 Request / response timing

- Web page SSR **不走 API**（`/today` 直接 Server Component `await db.select(...)`，避免 1 次额外 HTTP round-trip）
- 4-action 通过 Server Action 提交（内部不 HTTP；直接 RSC invocation）；**但** `/api/actions` 仍保留作为 "外部客户端 / curl / 第三方脚本" 入口
- p95 目标（SLA §1.2）：`/api/actions` < 300ms · `/api/export/full` < 5s（1 年数据 < 10MB）· `/api/today` 前端 SSR < 1s

### 1.7 路径大小写 + trailing slash

- 统一 lowercase · kebab-case · **无 trailing slash**（`/api/topics/42`，不是 `/api/topics/42/`）
- Next 15 默认重定向带 slash 的请求；CI 的 E2E 需断言最终 URL 无 slash

### 1.8 Content-Security-Policy（生产）

由 Caddy 注入（不在 API route 层管理）：

```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'; form-action 'self';
```

API 响应头不强制 CSP；浏览器访问 HTML 页面时由 Next/Caddy 共同注入。

---

## §2 Endpoint catalog

下列共 **18** 个 endpoint。每个块按 `方法 · 路径 · Auth · Req · Success · Error · Notes` 组织。

### 2.A Auth 群（4 个）

#### E1 · `POST /api/invite` · admin only · **T027**

| 项 | 值 |
|---|---|
| **路由文件** | `src/app/api/invite/route.ts` |
| **Auth** | `requireAdmin`（session + seats.role = 'admin'） |
| **实现任务** | T027 |

**Request body**（zod 校验）：

```typescript
z.object({
  email: z.string().trim().toLowerCase().email(),
  role: z.enum(['admin', 'member']),
});
```

**Success 201**（`Content-Type: application/json`）：

```jsonc
{
  "inviteUrl": "https://<operator-domain>/login/verify?token=9f...e1",
  "expiresAt": "2026-04-24T08:00:00.000Z",
  "seatId": 7
}
```

`inviteUrl` = 运行时拼接 `${APP_ORIGIN}/login/verify?token=<plaintext>`；plaintext 仅在此响应出现一次，之后只存 hash。

**Errors**：

| HTTP | code | 触发条件 |
|---|---|---|
| 400 | `INVALID_EMAIL` | email 不合 RFC5322 |
| 400 | `INVALID_ROLE` | role 不在 enum |
| 403 | `NOT_ADMIN` | session.role !== 'admin' |
| 409 | `EMAIL_ALREADY_INVITED` | `seats.lab_email_unique` 已存在且 `invite_token_hash IS NOT NULL`（未消费） |
| 409 | `EMAIL_ALREADY_JOINED` | `seats` 存在且 token 已消费（seat 已是活跃成员） |
| 409 | `IDEMPOTENCY_MISMATCH` | `Idempotency-Key` 重放且 body 不同 |

**Notes**：

- 24h TTL 来自 env `INVITE_TOKEN_TTL_HOURS=24`（directory-layout §3）
- **不发邮件**（DECISIONS-LOG 2026-04-23 "operator 自用为主" 结论）；admin 手工复制 `inviteUrl` 给被邀者
- 写入：同事务 `seats INSERT`（`invite_token_hash = sha256(plaintext)` · `invite_expires_at = now() + 24h` · `invited_at = now()` · `role` from body）

**curl 示例**：

```bash
curl -X POST http://localhost:3000/api/invite \
  -H 'content-type: application/json' \
  -H 'cookie: pi_session=<admin-jwt>' \
  -H 'Idempotency-Key: 01943b1c-6f29-7a9e-bfe2-00004d4e5a00' \
  -d '{"email":"maya@lab.example.com","role":"member"}'
```

---

#### E2 · `POST /api/invite/consume` · public（via `/login` 页面 · **G4 H4 · R_final 2026-04-24 重写**）· **T006**

| 项 | 值 |
|---|---|
| **路由文件** | `src/app/api/invite/consume/route.ts` |
| **Auth** | 无（body 内的 token 本身是 one-shot 凭证 · SameSite=Lax + Origin 检查防 CSRF） |
| **实现任务** | T006（Phase 0 · 原 T027 已按新 task ID 映射到 T006） |

**Request body**（JSON · 必须 `Content-Type: application/json`）：

```typescript
z.object({
  token: z.string().regex(/^[0-9a-f]{64}$/),   // 64-hex plaintext
});
```

**Request headers**（CSRF 缓解 · G4 H4 SEC-10 更新）：
- `Origin: <APP_ORIGIN>` — 必须匹配 server-side `env.APP_ORIGIN`；不匹配 → 403 `CSRF_ORIGIN_MISMATCH`
- （可选）`X-Invite-Nonce: <uuid>` — 前端生成的 one-time nonce · cookie 同步 · 防重放（v0.1 可选；v0.2 强制）

**Behavior**：

1. 校验 `Origin` header 与 `env.APP_ORIGIN` 一致；不一致 → 403 `CSRF_ORIGIN_MISMATCH`
2. `tokenHash = sha256(body.token)` → `SELECT id, role, lab_id, invite_expires_at FROM seats WHERE invite_token_hash = ?`
3. 若不存在 / 已消费 → 410 `INVITE_TOKEN_EXPIRED`（message 中不区分 invalid / consumed，避免账号枚举）
4. 若 `invite_expires_at < now()` → 410 `INVITE_TOKEN_EXPIRED`
5. 若有效：事务 `UPDATE seats SET invite_token_hash = NULL, last_login_at = now()` + `INSERT sessions(...)` + `Set-Cookie: pi_session=<jwt>; HttpOnly; Secure; SameSite=Lax; Max-Age=2592000`
6. 返回 200 `{ ok: true, redirectTo: '/today' }`；前端 SPA 负责 client-side 跳转

**Response 成功 200**：

```jsonc
{
  "ok": true,
  "redirectTo": "/today"
}
```

配套 `Set-Cookie: pi_session=<jwt>; HttpOnly; Secure; SameSite=Lax; Max-Age=2592000`。

**Errors**：

| HTTP | code | 触发 |
|---|---|---|
| 400 | `INVALID_TOKEN` | body.token 不符 64-hex 正则 |
| 403 | `CSRF_ORIGIN_MISMATCH` | Origin header 不匹配 APP_ORIGIN（SEC-10 缓解） |
| 410 | `INVITE_TOKEN_EXPIRED` | token 不存在 / 已消费 / 已过期（所有情况统一 code · 不泄漏差异 · SEC-2） |

**客户端配套页面** · `/login`（T006 产物 · client component）：

- URL 形式：`https://<domain>/login#invite=<token>`（**fragment** · 不是 query）
- **为何用 fragment**：URL fragment（`#` 之后）**绝不**发送给服务端，因此：
  - Caddy access log 不记录 token（不像原 GET path-token 方案）
  - 代理 / IM link-preview GET 请求也不会发送 fragment（大多数 preview 机制只看 path/query）
  - email 扫描器同理（本项目也不走 email 传递）
- Client JS 读 `window.location.hash` → parse `invite=<token>` → `POST /api/invite/consume` with body `{ token }` → 按响应 redirect
- 失败时页面展示 `INVITE_TOKEN_EXPIRED` 中文消息（"邀请链接已失效，请联系 operator 重新发起"），引导联系 operator 重发

**Notes · G4 H4 安全模型（2026-04-24 R_final 更新 · SEC-10 重定位）**：

1. **原 GET path-token 风险已消除**：token 不再在 URL path；Caddy 的 `log { format filter { uri query delete } }` 只能删 query · 无法删 path · 但新方案的 token 在 POST body · Caddy 默认不记 POST body · 彻底无日志泄漏
2. **CSRF 风险（替代）**：POST endpoint 需防跨站 CSRF · 缓解：
   - `SameSite=Lax` session cookie（Chrome/Safari/Firefox 均支持）→ 跨站表单无法带 session cookie
   - Origin header 检查（POST without matching Origin 一律拒）
   - （v0.2 加固）one-time nonce：前端生成 UUID · cookie 同步 · body/header 回传 · 一次性验证后失效
3. **Email 扫描 / IM preview 风险消除**：fragment 不进 server log；即使扫描器 GET `/login#invite=xxx`，server 收到的只是 `/login`（无 token）· 不会误消费
4. **原 GET endpoint 废弃**：`GET /api/invite/:token/consume` 正式 deprecated · v0.1 不实现 · client-side `/login` + POST 是唯一路径

**v0.2 升级空间**：加 one-time nonce 强制（防重放）· 加 CAPTCHA 前置（大规模招募时）；目前 v0.1 lab ≤ 15 seat 不需要。

---

#### E3 · `POST /api/login/verify` · public · **T027 future**（v0.2 option）

**v0.1 不实现**；此项目仅留设计契约，供 v0.2 上线 POST-based 消费时直接对齐。

| 项 | 值 |
|---|---|
| **路由文件** | `src/app/api/login/verify/route.ts`（v0.2） |
| **Auth** | 无 |
| **实现任务** | v0.2 TBD |

**Request body**：`{token: string}`
**Success 200**：`{ok: true, redirectTo: '/today'}` + `Set-Cookie: pi_session=...`
**Errors**：400 `INVALID_TOKEN` · 410 `INVITE_TOKEN_EXPIRED`

---

#### E4 · `POST /api/logout` · any authed · **T028**

| 项 | 值 |
|---|---|
| **路由文件** | `src/app/api/logout/route.ts` |
| **Auth** | `requireAuth` |
| **实现任务** | T028 |

**Request**：无 body。

**Behavior**：`UPDATE sessions SET revoked_at = now() WHERE id = ?`（当前 session id 从 cookie 解出） + `Set-Cookie: pi_session=; Max-Age=0`。

**Success 204**：No Content（空 body）。

**Errors**：

| HTTP | code | 触发条件 |
|---|---|---|
| 401 | `SESSION_EXPIRED` | 未带 cookie |

**curl**：

```bash
curl -X POST http://localhost:3000/api/logout -H 'cookie: pi_session=<jwt>' -i
```

---

### 2.B Topic 群（4 个）

#### E5 · `GET /api/topics` · authed · **T010**

| 项 | 值 |
|---|---|
| **路由文件** | `src/app/api/topics/route.ts` (GET) |
| **Auth** | `requireAuth` |
| **实现任务** | T010（G4 H2 · 2026-04-24 · 原 T009 按 dependency-graph.mmd 迁移到 T010） |

**Request**：query `?includeArchived=false|true`（默认 false）

**Success 200**：`Topic[]`（参考 §3 shape）

```jsonc
[
  {
    "id": 1,
    "labId": 1,
    "name": "RLHF alignment",
    "keywords": ["RLHF", "preference learning"],
    "arxivCategories": ["cs.LG", "cs.CL"],
    "seedAuthors": ["Christiano Paul F"],
    "createdAt": "2026-04-23T09:00:00.000Z",
    "archivedAt": null
  }
]
```

**Errors**：401 `SESSION_EXPIRED`

---

#### E6 · `POST /api/topics` · admin only · **T010**

**Request body**：

```typescript
z.object({
  name: z.string().trim().min(1).max(80),
  keywords: z.array(z.string().trim().min(1)).min(1).max(30),
  arxivCategories: z.array(z.string().trim().regex(/^[a-z-]+\.[A-Z]{2}$/)).min(1).max(8),
  seedAuthors: z.array(z.string().trim().min(1)).max(10).default([]),
});
```

**Success 201**：返回新建的 `Topic`

**Errors**：

| HTTP | code |
|---|---|
| 400 | `INVALID_TOPIC_INPUT` |
| 403 | `NOT_ADMIN` |
| 409 | `TOPIC_NAME_CONFLICT`（同 lab 下 name 重复） |
| 422 | `TOO_MANY_TOPICS`（ > 15 active topics） |

**Notes**：`TOO_MANY_TOPICS` 来自 spec IN-1（8–15 topic 边界），由 API 层检查 `SELECT count(*) FROM topics WHERE lab_id=? AND archived_at IS NULL`；422 而非 409 语义更合适（"语义正确但业务规则拒绝"）。

---

#### E7 · `PATCH /api/topics/:id` · admin only · **T010**

**Path param**：`id`（topic id）

**Request body**：全部字段 optional（partial update），使用 zod `.partial()`

**Success 200**：更新后的 `Topic`

**Errors**：

| HTTP | code |
|---|---|
| 403 | `NOT_ADMIN` |
| 404 | `TOPIC_NOT_FOUND` |
| 409 | `TOPIC_NAME_CONFLICT` |

---

#### E8 · `DELETE /api/topics/:id` · admin only · **T010**

**Behavior**：软删除（`UPDATE topics SET archived_at = now()`），保留历史；不真 DELETE。

**Success 204**：No Content

**Errors**：403 `NOT_ADMIN` · 404 `TOPIC_NOT_FOUND` · 409 `TOPIC_ALREADY_ARCHIVED`

---

### 2.C Briefing & Action 群（2 个 · v0.1 实现）

> **E9 `GET /api/today` 已移至 §7 Future / deferred endpoints（v0.1 不实现）**。v0.1 的 `/today` 页面走 Next 15 Server Component + `loadTodayBriefing()` 直接 SSR（单次 Node → Postgres，无 HTTP round-trip · 见 DECISIONS-LOG 2026-04-23 `/today page 数据 fetch 策略`）。T015 的 file_domain 不包含 `/api/today` route。

---

#### E10 · `POST /api/actions` · authed · **T015**

| 项 | 值 |
|---|---|
| **路由文件** | `src/app/api/actions/route.ts` |
| **Auth** | `requireAuth` |
| **实现任务** | T015 · **D16 Layer 2 红线兜底位置** |

**Request body**（zod；见 `tasks/T015.md` Implementation plan 第 2 步）：

```typescript
z.object({
  paperId: z.number().int().positive(),
  action: z.enum(['read_now', 'read_later', 'skip', 'breadcrumb']),
  why: z.string().trim().max(280).optional(),
}).refine(
  (v) => v.action !== 'skip' || (v.why !== undefined && v.why.trim().length >= 5),
  { message: 'skip 必须填写 why (至少 5 字符)', path: ['why'] },
);
```

**Success 201**：

```jsonc
{
  "actionId": 1027,
  "breadcrumbId": 83   // 仅当 action='breadcrumb' 时有此字段（同事务写 breadcrumbs 表）
}
```

**Errors**：

| HTTP | code | 触发条件 |
|---|---|---|
| 400 | `SKIP_WHY_REQUIRED` | `action='skip'` 且 `why` 为空或 btrim < 5 chars（D16 Layer 2） |
| 400 | `WHY_TOO_LONG` | `why.length > 280` |
| 400 | `INVALID_ACTION` | action 不在 enum |
| 401 | `SESSION_EXPIRED` | |
| 404 | `PAPER_NOT_FOUND` | paperId 不存在 |
| 409 | `DUPLICATE_ACTION` | 同 seat + 同 paper + 同 action 在 60s 内重复（可选去重；防双击） |
| 422 | `PAPER_NOT_IN_LAB_TOPICS` | breadcrumb action 但 paper 未被任何 topic 匹配 (`paper_topic_scores` 空) · 必要字段 `topic_id` 无法确定 |

**Notes**：
- `action='breadcrumb'` 同事务写 `actions` + `breadcrumbs`；`breadcrumbs.topic_id` 取 `paper_topic_scores.topic_id` 中任意一条（v0.1 不细分多 topic 场景）
- `DB CHECK skip_requires_why` 是 D16 Layer 1 最后兜底；API 层（D16 Layer 2）应在 DB CHECK 触发前就拦截并返 400
- `actions` 表是 append-only；同 seat + 同 paper 可重复（从 read_later 改 breadcrumb 是合法场景），`DUPLICATE_ACTION` 仅防 60s 内的明显重复点击

**curl 示例**（成功 skip）：

```bash
curl -X POST http://localhost:3000/api/actions \
  -H 'content-type: application/json' \
  -H 'cookie: pi_session=<jwt>' \
  -d '{"paperId": 42, "action": "skip", "why": "已在上周读过同方向 A 的更强版本"}'
```

**curl 示例**（失败 · why 不足）：

```bash
curl -X POST http://localhost:3000/api/actions \
  -H 'content-type: application/json' \
  -H 'cookie: pi_session=<jwt>' \
  -d '{"paperId": 42, "action": "skip", "why": "no."}'
# 400 {"error":{"code":"SKIP_WHY_REQUIRED","message":"skip 必须填写 why (至少 5 字符)","fields":{"why":"至少需要 5 个非空白字符"}}}
```

---

### 2.D Papers 群（1 个)

#### E11 · `GET /api/papers/:id/history` · authed · **T016**

| 项 | 值 |
|---|---|
| **路由文件** | `src/app/api/papers/[id]/history/route.ts`（如果前端也通过 API）or Server Component 直接查 |
| **Auth** | `requireAuth`（admin + member 分支展示量不同） |
| **实现任务** | T016 |

**Success 200**：

```jsonc
{
  "paper": {
    "id": 42,
    "arxivId": "2305.18290",
    "title": "Direct Preference Optimization: ...",
    "abstract": "...",
    "authors": ["Rafailov et al."],
    "publishedAt": "2023-05-29T00:00:00.000Z",
    "arxivUrl": "https://arxiv.org/abs/2305.18290"
  },
  "summaries": [
    {
      "topicId": 1,
      "topicName": "RLHF alignment",
      "summaryText": "DPO removes the explicit reward model... (≤ 3 句)",
      "modelName": "claude-sonnet-4-6-20250701",
      "promptVersion": "v1.0-2026-04",
      "createdAt": "2026-04-23T06:02:11.000Z"
    }
    // 一 paper 可对应多 topic → 多条 summary；逐 topic 分节展示
  ],
  "events": [
    // 按时间倒序的混合 event · 见 §3 shape · admin 看全 lab；member 看自己 + 聚合
    {
      "kind": "action",
      "time": "2026-04-24T08:15:00.000Z",
      "seatEmail": "maya@lab.example.com",   // member 视图里 = "其他（匿名）" 或 "自己"
      "detail": { "action": "skip", "why": "已在上周读过同方向 A 的更强版本" }
    },
    {
      "kind": "breadcrumb_created",
      "time": "2026-04-23T20:30:00.000Z",
      "seatEmail": "you",
      "detail": { "topicId": 1 }
    },
    {
      "kind": "resurface_clicked",
      "time": "...",
      "seatEmail": "you",
      "detail": { "triggerType": "citation", "contextText": "..." }
    }
  ]
}
```

**C6 / D16 Layer 3 UI 红线 可见性要求**（T016 verification）：`events[].kind='action' && detail.action='skip'` 的行，前端必须把 `detail.why` 渲染为**可见 `<strong>` 或等价显式元素**，不得藏入 `title` / tooltip / hover。本 API 只负责把 `why` 文本返回完整（不做额外处理）；UI 展示合规性由 T016 E2E 验证。

**Errors**：

| HTTP | code |
|---|---|
| 401 | `SESSION_EXPIRED` |
| 404 | `PAPER_NOT_FOUND` |

---

### 2.E Breadcrumb & Resurface 群（3 个）

#### E12 · `GET /api/breadcrumbs` · authed · **T019**

**Request**：query `?status=active|dismissed|all`（默认 active）

**Success 200**：`Breadcrumb[]`（见 §3）

**Errors**：401 `SESSION_EXPIRED`

---

#### E13 · `POST /api/resurface/:id/dismiss` · authed · **T023**

**Auth**：`requireAuth` + 校验当前 seat 是该 resurface 事件对应 breadcrumb 的拥有者（否则 403 `NOT_BREADCRUMB_OWNER`）

**Request**：无 body

**Behavior**：`UPDATE resurface_events SET dismissed_at = now() WHERE id = ?`

**Success 204**

**Errors**：

| HTTP | code |
|---|---|
| 403 | `NOT_BREADCRUMB_OWNER` |
| 404 | `RESURFACE_NOT_FOUND` |
| 409 | `RESURFACE_ALREADY_DISMISSED` |

---

#### E14 · `POST /api/breadcrumbs/:id/re-breadcrumb` · authed · **T023**

**Auth**：owner only

**Behavior**：创建新的 breadcrumb 行（`INSERT breadcrumbs(seat_id, paper_id, topic_id)` 复制原行 · 新 `created_at`），原 breadcrumb 保留 `dismissed_at` 不变；resurface schedule 从新行重新起点。

**Success 201**：`{newBreadcrumbId: 87}`

**Errors**：

| HTTP | code |
|---|---|
| 403 | `NOT_BREADCRUMB_OWNER` |
| 404 | `BREADCRUMB_NOT_FOUND` |
| 409 | `BREADCRUMB_NOT_DISMISSED`（只能对已 dismissed 的 re-breadcrumb；仍 active 无意义） |

---

### 2.F Admin & Sentinel 群（2 个）

#### E15 · `GET /api/admin/lab-stats` · admin only · **T026**

**Success 200**：

```jsonc
{
  "activeSeats30d": 2,                 // 过去 30 天有 ≥1 次 login 的 seat 数
  "sinceDay": 18,                      // 今天距 labs.first_day_at 的天数
  "sentinelState": "warn",             // ok | warn | escalate
  "allowContinueUntil": null,          // 若 operator 已签 allow-continue，ISO 时间；否则 null
  "costThisMonthCents": 1842,          // llm_calls SUM(cost_cents) for current month
  "costBudgetCents": 5000,
  "lastBriefingAt": "2026-04-23T06:02:11.000Z",
  "lastWorkerStatus": "ok"             // 最新 fetch_runs.status
}
```

`sentinelState` 定义：
- `ok`：`activeSeats30d >= 3` 或 `sinceDay < 30`（未触发）
- `warn`：`sinceDay >= 30 AND activeSeats30d = 2`（警示但不阻塞新 feature）
- `escalate`：`sinceDay >= 30 AND activeSeats30d < 2` 且 `allow_continue_until < now()` · **阻塞新 feature 开发**（spec §6 Sentinel）

**Errors**：401 / 403

---

#### E16 · `POST /api/admin/allow-continue` · admin only · **T026**

**Request body**：

```typescript
z.object({
  days: z.number().int().min(1).max(30).default(14),
});
```

**Behavior**：`UPDATE labs SET allow_continue_until = now() + INTERVAL '<days> days'`

**Success 200**：`{allowContinueUntil: "2026-05-07T00:00:00.000Z"}`

**Errors**：401 / 403

---

### 2.G Export 群（1 个）

#### E17 · `GET /api/export/full` · admin only · **T023**

| 项 | 值 |
|---|---|
| **路由文件** | `src/app/api/export/full/route.ts` |
| **Auth** | `requireAdmin`（+ controller 层 **二次** assert `seat.role === 'admin'` · SEC-1 双重检查） |
| **实现任务** | T023 |

**Request**：无 query（v0.1 永远导出当前 lab 全量）。**SEC-5**：绝不接受 `?filename=`、`?path=`、或任何 filesystem path 参数。

**Success 200**：

- **Content-Type**: `application/json; charset=utf-8`
- **Content-Disposition**: `attachment; filename="pi-briefing-export-YYYYMMDD.json"`（YYYYMMDD = server 端 `APP_TIMEZONE` 当日）
- **Body**: 见 §3.11 `ExportEnvelope` shape（`schemaVersion: "1.1"` · camelCase · G3 · 2026-04-24 R_final B3 fix）

**副作用**：在响应返回**前**必须同步写入 `export_log` 一行（`lab_id, seat_id, export_type='full', row_counts_jsonb, byte_size, created_at`）。若 `buildFullExport` 抛错则**不**写 export_log（避免"失败但审计成功"）。

**Errors**：

| HTTP | code |
|---|---|
| 401 | `SESSION_EXPIRED` |
| 403 | `NOT_ADMIN` |
| 500 | `EXPORT_FAILED`（含 `requestId` 便于 operator `journalctl | grep` 排错） |

**curl**：

```bash
curl -X GET http://localhost:3000/api/export/full \
  -H 'cookie: pi_session=<admin-jwt>' \
  -o pi-briefing-export-20260424.json
```

---

### 2.H Health 群（1 个）

#### E18 · `GET /api/healthz` · public · **T030**

| 项 | 值 |
|---|---|
| **路由文件** | `src/app/api/healthz/route.ts` |
| **Auth** | **无**（Caddy health check + systemd watchdog 用） |
| **实现任务** | T030（运维层） |

**Success 200**：

```jsonc
{
  "status": "ok",
  "uptimeSec": 8421,
  "version": "f97b222",    // git SHA at build time
  "now": "2026-04-24T09:30:00.000Z"
}
```

**Errors**：500 `HEALTH_DEGRADED`（若 DB ping 失败；worker status 不算 degraded）

**Notes**：
- 不查 `llm_calls` 或 LLM provider（防止 healthz 触发 LLM 调用增加成本）
- DB ping 仅 `SELECT 1`（单次；无 retry）
- 被 Caddy / playwright E2E `webServer` 作为 readiness probe

---

## §3 Resource type schemas

> 下方是 API 响应中所有资源类型的权威 TypeScript 定义；零 runtime 逻辑，纯合同。实际实现可用 Zod `.infer<>` 或 Drizzle `InferSelectModel<>`，但须与此**逐字对齐**。字段命名：API 层统一 **camelCase**（DB 是 snake_case，由 `src/db/types.ts` 映射层转换）。

### 3.1 Topic

```typescript
interface Topic {
  id: number;
  labId: number;
  name: string;
  keywords: string[];
  arxivCategories: string[];
  seedAuthors: string[];
  createdAt: string;         // ISO 8601 with Z
  archivedAt: string | null;
}
```

### 3.2 Paper

```typescript
interface Paper {
  id: number;
  arxivId: string;           // e.g. '2305.18290'
  title: string;
  abstract: string;
  authors: string[];
  categories: string[];
  primaryCategory: string | null;
  publishedAt: string;
  fetchedAt: string;
  arxivUrl: string;          // 派生字段：`https://arxiv.org/abs/${arxivId}`
}
```

### 3.3 PaperSummaryRecord

```typescript
interface PaperSummaryRecord {
  id: number;
  paperId: number;
  topicId: number;
  summaryText: string;       // ≤ 3 句（DB CHECK + 应用层双兜底）
  modelName: string;         // e.g. 'claude-sonnet-4-6-20250701' · 或 'fallback-heuristic-v1'
  promptVersion: string;     // e.g. 'v1.0-2026-04'
  createdAt: string;
  // llmCallId 故意不暴露到 API 层（审计内部）
}
```

### 3.4 Action

```typescript
interface Action {
  id: number;
  seatId: number;
  seatEmail: string;         // 展示用；member 视图可被匿名化
  paperId: number;
  action: 'read_now' | 'read_later' | 'skip' | 'breadcrumb';
  why: string | null;        // skip 行必非 null 且 trim.length >= 5
  createdAt: string;
}
```

### 3.5 Briefing

```typescript
interface Briefing {
  id: number;
  labId: number;
  topicId: number;
  forDate: string;           // 'YYYY-MM-DD' (不带时区 · 基于 APP_TIMEZONE)
  stateSummary: string;      // 一句 topic-level 判断；不含 per-paper summary
  triggerPaperIds: number[]; // ≤ 3
  anchorPaperId: number | null;
  llmProvider: string | null;
  tokenCostCents: number | null;
  assembledAt: string;
}
```

### 3.6 BriefingItem（`/api/today` 响应中的 items[]）

```typescript
interface BriefingItem {
  topic: Topic;
  topicStateSummary: string;
  anchorPaper: Paper | null;
  papers: Array<{
    paper: Paper;
    summary: PaperSummaryRecord | null;  // null if LLM failed + heuristic fallback 也失败
    selfAction: Action | null;           // 当前 seat 对此 paper 的最新 action
    labActions: Action[];                // 全 lab 的 actions（v0.1 R1 H2 deferred · 返空数组即可）
    isShift: boolean;
    shiftRationale: string | null;
  }>;
}
```

### 3.7 Breadcrumb

```typescript
interface Breadcrumb {
  id: number;
  seatId: number;
  paperId: number;
  topicId: number;
  createdAt: string;
  lastResurfaceAt: string | null;
  dismissedAt: string | null;
}
```

### 3.8 ResurfaceEvent

```typescript
interface ResurfaceEvent {
  id: number;
  breadcrumbId: number;
  triggerType: 'timed_6wk' | 'timed_3mo' | 'timed_6mo' | 'citation';
  triggerPaperId: number | null;        // 仅 citation 触发时非空
  contextText: string;                   // "为什么现在又回来"
  surfacedAt: string;
  clickedAt: string | null;
  dismissedAt: string | null;
}
```

### 3.9 PaperHistoryEvent（`/api/papers/:id/history` 响应中的 events[]）

```typescript
type PaperHistoryEvent =
  | {
      kind: 'action';
      time: string;
      seatEmail: string;        // 'you' | 'lab 成员' | '<real email>'（admin only）
      detail: {
        action: 'read_now' | 'read_later' | 'skip' | 'breadcrumb';
        why: string | null;
      };
    }
  | {
      kind: 'breadcrumb_created';
      time: string;
      seatEmail: string;
      detail: { topicId: number };
    }
  | {
      kind: 'resurface_surfaced' | 'resurface_clicked' | 'resurface_dismissed';
      time: string;
      seatEmail: string;
      detail: {
        triggerType: ResurfaceEvent['triggerType'];
        contextText: string;
      };
    };
```

### 3.10 Seat（内部使用；不直接通过 API 暴露全量）

```typescript
interface Seat {
  id: number;
  email: string;
  role: 'admin' | 'member';
  createdAt: string;
  // invite_token_hash / invite_expires_at 永不返回
}
```

### 3.11 ExportEnvelope（`/api/export/full` 响应体）

```typescript
interface ExportEnvelope {
  schemaVersion: '1.1';
  exportedAt: string;
  lab: {
    id: number;
    name: string;
    firstDayAt: string;
    exportedAt: string;          // redundant with top-level exportedAt; kept for operator convenience
    exportedBySeatId: number;
  };
  seats: Array<Pick<Seat, 'id' | 'email' | 'role' | 'createdAt'>>;  // NO invite fields
  topics: Topic[];
  papers: Paper[];
  paperTopicScores: Array<{
    paperId: number;
    topicId: number;
    matchSignal: 'keyword' | 'category' | 'seed_author';
    matchedKeywords: string[];
    computedAt: string;
  }>;
  paperCitations: Array<{
    citingPaperId: number;
    citedArxivId: string;
    discoveredAt: string;
  }>;
  paperSummaries: PaperSummaryRecord[];
  briefings: Briefing[];
  actions: Action[];
  breadcrumbs: Breadcrumb[];
  resurfaceEvents: ResurfaceEvent[];
  fetchRuns: Array<{
    runDate: string;
    source: string;
    status: 'ok' | 'failed' | 'partial' | 'running';
    itemsFetched: number;
    notes: string | null;
  }>;
  // 刻意不包含：sessions / llm_calls / export_log（审计内部）
}
```

**Import round-trip notes**（F5 · 2026-04-24 pre-R_final 加固）：`paper_summaries.llmCallId` 字段 reference `llm_calls`，而 `llm_calls` **不在** envelope 内（审计表 · 刻意排除 · compliance.md §2 数据资产分离）。因此 round-trip import 时 FK 会悬挂。Importer **必须**二选一：

- **(a) 置 null**：import 时设 `llmCallId = null`。简单，丢失成本归因审计但保留 `modelName` + `promptVersion`（reproducibility 未失）。**v0.1 默认选此项**。
- **(b) 创建 stub `llm_calls` 行**并重连 FK，stub 内容：`{provider: 'imported', model: record.modelName, purpose: 'summarize', input_tokens: 0, output_tokens: 0, cost_cents: 0, latency_ms: 0, request_hash: 'import-' + nanoid(), called_at: record.createdAt}`。保留 FK 完整性，代价是审计表被合成行污染（可按 `provider='imported'` 过滤屏蔽）。

两种都要求 `paper_summaries.llm_call_id` 数据库列**允许 NULL**（schema.sql 已调整 · 2026-04-24 F5 · `on delete set null` 保留审计链可重建的机会）。`scripts/export-import-round-trip.ts` 实现 option (a)；operator 若需 (b) 在 v0.2 手写 migration 合并。

Exporter 端**永不**对 `llmCallId` 做兜底：`paper_summaries.llm_call_id` 字段从 DB 原样输出（包含 null）；这避免 exporter 与 importer 的语义双重处理导致 FK ambiguity。

**`schemaVersion` bump 规则**（DECISIONS-LOG 2026-04-23 · G3 · 2026-04-24 R_final B3 fix · 本文件权威 · 字段名统一为 camelCase `schemaVersion`）：

| bump | 触发 |
|---|---|
| 1.0 → 1.1 | 新增顶层 key（如新增 `paperSummaries` · 新增 `lab.firstDayAt` · 新增 paperTopicScores/paperCitations/fetchRuns）· 前向兼容，旧 importer 忽略新 key |
| 1.1 → 1.2 | 新增另一顶层 key（如未来加 `exportLog`）· 前向兼容 |
| 1.x → 2.0 | **breaking**：重命名字段、改字段类型、删除 key · v0.2 / v1.0 才可能 |

Round-trip 脚本（`scripts/export-import-round-trip.ts`）必须兼容 1.0 与 1.1 输入（T023 Implementation plan 第 5 步要求）；1.0 输入时跳过 `paperSummaries` 插入。

---

## §4 Error code catalog（完整清单）

| Code | HTTP | 触发 | 用户可见中文消息 |
|---|---|---|---|
| `SESSION_EXPIRED` | 401 | session cookie 无效 / 已 revoke / 已过期 | 登录已过期，请重新登录 |
| `NOT_ADMIN` | 403 | 非 admin 访问 admin 路由 | 仅管理员可操作 |
| `NOT_BREADCRUMB_OWNER` | 403 | 操作不属于自己的 breadcrumb / resurface | 仅 breadcrumb 所有者可操作 |
| `INVALID_EMAIL` | 400 | 不合 RFC5322 | 邮箱格式不正确 |
| `INVALID_ROLE` | 400 | role 不在 enum | 角色必须为 admin 或 member |
| `INVALID_TOPIC_INPUT` | 400 | POST /api/topics 参数错误 | topic 参数不合法 |
| `INVALID_ACTION` | 400 | action 不在 enum | 无效的 action 类型 |
| `INVALID_TOKEN` | 400 | POST /api/invite/consume 的 token 格式错（非 64-hex） | 无效的 token 格式 |
| `CSRF_ORIGIN_MISMATCH` | 403 | Origin header 不匹配 APP_ORIGIN（G4 H4 · 2026-04-24 · POST /api/invite/consume 强制） | 请求来源不合法 |
| `SKIP_WHY_REQUIRED` | 400 | skip action 未附 why 或 btrim < 5 chars | skip 必须填写 why (至少 5 字符) |
| `WHY_TOO_LONG` | 400 | why > 280 chars | why 最多 280 字符 |
| `EMAIL_ALREADY_INVITED` | 409 | 邀请目标 email 已有未消费 token | 该邮箱已被邀请 |
| `EMAIL_ALREADY_JOINED` | 409 | 邀请目标 email 已是活跃 seat | 该邮箱已是 lab 成员 |
| `TOPIC_NAME_CONFLICT` | 409 | 同 lab 下 topic name 重复 | topic 名称已存在 |
| `TOPIC_ALREADY_ARCHIVED` | 409 | 重复 DELETE 已归档的 topic | topic 已归档 |
| `DUPLICATE_ACTION` | 409 | 同 seat + paper + action 60s 内重复 | 检测到重复 action |
| `IDEMPOTENCY_MISMATCH` | 409 | 同 Idempotency-Key 但 body 不同 | 请求幂等冲突 |
| `RESURFACE_ALREADY_DISMISSED` | 409 | 重复 dismiss 已 dismissed 的 resurface | resurface 已被忽略 |
| `BREADCRUMB_NOT_DISMISSED` | 409 | 对仍 active 的 breadcrumb 调 re-breadcrumb | breadcrumb 仍生效，无需重新 |
| `INVITE_TOKEN_EXPIRED` | 410 | 24h TTL 过期或已消费 | 邀请链接已失效 |
| `PAPER_NOT_IN_LAB_TOPICS` | 422 | breadcrumb 但 paper 无 topic 匹配 | 该论文未匹配任何 topic |
| `TOO_MANY_TOPICS` | 422 | 超过 15 个 active topic | topic 数量已达上限 (15) |
| `PAPER_NOT_FOUND` | 404 | paperId 不存在 | 论文不存在 |
| `TOPIC_NOT_FOUND` | 404 | topic id 不存在 | topic 不存在 |
| `BREADCRUMB_NOT_FOUND` | 404 | breadcrumb id 不存在 | breadcrumb 不存在 |
| `RESURFACE_NOT_FOUND` | 404 | resurface id 不存在 | resurface 事件不存在 |
| `NO_BRIEFING_YET` | 404 | 该 lab 从未产出 briefing | 还没有 briefing，请先创建 topic |
| `RATE_LIMITED` | 429 | v0.2 预留 | 请求过快，请稍后重试 |
| `EXPORT_FAILED` | 500 | buildFullExport 内部错 | 导出失败，请联系 operator |
| `HEALTH_DEGRADED` | 500 | /api/healthz DB ping 失败 | 服务不可用 |
| `LLM_BUDGET_EXCEEDED` | 503 | C11 月度预算已达上限 | LLM 预算已达上限，briefing 暂缓 |

**总计 31 个 code**（G4 H4 · 新增 `CSRF_ORIGIN_MISMATCH` · 2026-04-24）。实现注意：

- `error.code` 所有上述值必须**原样字符串**出现在 `src/lib/http/errors.ts` 的 const 集合里（给 TS type-check + grep 审计）
- 前端 i18n：默认 `zh-CN`；未来 v0.2 若支持多语言，把 "用户可见消息" 列移入 `src/lib/i18n/messages/zh-CN.ts`
- 任何路由抛出不在此清单的 code → CI 审查脚本报错（T008 测试骨架有这条 meta test）

---

## §5 OpenAPI-lite curl 参考（copy-paste-ready）

> 下方 18 个 curl 与 §2 endpoint 一一对应；改 `$COOKIE` 与 `$BASE` 即可跑。

```bash
# 变量（根据环境调整）
BASE=http://localhost:3000
COOKIE="pi_session=eyJhbGciOiJIUzI1NiIs..."                     # 普通用户
ADMIN_COOKIE="pi_session=eyJhbGciOiJIUzI1NiIs..."                 # admin 用户
TOPIC_ID=1
PAPER_ID=42
BREADCRUMB_ID=17
RESURFACE_ID=9

# E1 · POST /api/invite (admin)
curl -X POST "$BASE/api/invite" \
  -H 'content-type: application/json' \
  -H "cookie: $ADMIN_COOKIE" \
  -H 'Idempotency-Key: 01943b1c-6f29-7a9e-bfe2-00004d4e5a00' \
  -d '{"email":"maya@lab.example.com","role":"member"}'

# E2 · POST /api/invite/consume (G4 H4 · 2026-04-24 R_final 重写 · POST-based)
# 1) 用户点击 invite 链接：https://<domain>/login#invite=<token>
# 2) 客户端 JS 读 fragment → POST 下面的 endpoint
curl -X POST "$BASE/api/invite/consume" \
  -H 'content-type: application/json' \
  -H "Origin: $BASE" \
  -d '{"token":"<64-hex-plaintext>"}' \
  -i
# 期望 200 + Set-Cookie pi_session=... + body { ok: true, redirectTo: "/today" }

# E4 · POST /api/logout
curl -X POST "$BASE/api/logout" -H "cookie: $COOKIE" -i

# E5 · GET /api/topics
curl "$BASE/api/topics" -H "cookie: $COOKIE"

# E6 · POST /api/topics (admin)
curl -X POST "$BASE/api/topics" \
  -H 'content-type: application/json' \
  -H "cookie: $ADMIN_COOKIE" \
  -d '{
    "name": "RLHF alignment",
    "keywords": ["RLHF","preference learning","reward model"],
    "arxivCategories": ["cs.LG","cs.CL"],
    "seedAuthors": ["Christiano Paul F"]
  }'

# E7 · PATCH /api/topics/:id
curl -X PATCH "$BASE/api/topics/$TOPIC_ID" \
  -H 'content-type: application/json' \
  -H "cookie: $ADMIN_COOKIE" \
  -d '{"keywords": ["RLHF","DPO","RLOO","preference learning"]}'

# E8 · DELETE /api/topics/:id (软删)
curl -X DELETE "$BASE/api/topics/$TOPIC_ID" -H "cookie: $ADMIN_COOKIE" -i

# E9 · GET /api/today · 已移至 §7 Future / deferred endpoints · v0.1 不实现（SSR 走 Server Component · 无此 API）

# E10 · POST /api/actions (4-action)
curl -X POST "$BASE/api/actions" \
  -H 'content-type: application/json' \
  -H "cookie: $COOKIE" \
  -d '{"paperId": '"$PAPER_ID"', "action": "skip", "why": "已在上周读过同方向 A 的更强版本"}'

# E10 失败示例 · why 不足
curl -X POST "$BASE/api/actions" \
  -H 'content-type: application/json' \
  -H "cookie: $COOKIE" \
  -d '{"paperId": '"$PAPER_ID"', "action": "skip", "why": "no."}'
# → 400 SKIP_WHY_REQUIRED

# E11 · GET /api/papers/:id/history
curl "$BASE/api/papers/$PAPER_ID/history" -H "cookie: $COOKIE"

# E12 · GET /api/breadcrumbs
curl "$BASE/api/breadcrumbs?status=active" -H "cookie: $COOKIE"

# E13 · POST /api/resurface/:id/dismiss
curl -X POST "$BASE/api/resurface/$RESURFACE_ID/dismiss" -H "cookie: $COOKIE" -i

# E14 · POST /api/breadcrumbs/:id/re-breadcrumb
curl -X POST "$BASE/api/breadcrumbs/$BREADCRUMB_ID/re-breadcrumb" -H "cookie: $COOKIE"

# E15 · GET /api/admin/lab-stats (admin)
curl "$BASE/api/admin/lab-stats" -H "cookie: $ADMIN_COOKIE"

# E16 · POST /api/admin/allow-continue
curl -X POST "$BASE/api/admin/allow-continue" \
  -H 'content-type: application/json' \
  -H "cookie: $ADMIN_COOKIE" \
  -d '{"days": 14}'

# E17 · GET /api/export/full (admin) · 流式下载
curl -X GET "$BASE/api/export/full" \
  -H "cookie: $ADMIN_COOKIE" \
  -o "pi-briefing-export-$(date +%Y%m%d).json"

# E18 · GET /api/healthz (public)
curl "$BASE/api/healthz"
```

---

## §6 Implementation reference（每个 endpoint 的代码骨架索引）

下方给出每个 endpoint 的**最小实现骨架**，方便初级工程师 T 任务 kickoff 时 copy-adjust。统一 pattern：

```typescript
// src/app/api/<route>/route.ts (示意)
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, requireAdmin } from '@/lib/auth/middleware.js';
import { z } from 'zod';
import { HTTPError, toErrorResponse } from '@/lib/http/errors.js';

const BodySchema = z.object({ /* ... */ });

export async function POST(req: NextRequest) {
  try {
    const session = await requireAuth(req);       // throws 401 SESSION_EXPIRED on failure
    const body = BodySchema.parse(await req.json()); // throws 400 on zod failure (mapped in catch)
    // ... business logic via src/lib/*/service.ts ...
    return NextResponse.json({ /* payload */ }, { status: 201 });
  } catch (err) {
    return toErrorResponse(err);
  }
}
```

`src/lib/http/errors.ts` 的 `HTTPError` + `toErrorResponse` 是**唯一**返回 error envelope 的位置（统一 shape 见 §1.3）。任何 route handler 自己拼 `NextResponse.json({error: ...})` = PR review 打回。

---

## §7 Future / deferred endpoints（v0.1 不实现 · 设计 stub 保留）

本节列 **v0.1 明确不实现**、但需保留设计契约以便 v0.2+ 升级时**无 breaking change** 的 endpoints。v0.1 开发者**不为这些路径创建 route handler**；E2E 测试亦不覆盖。

### E3 · `POST /api/login/verify` · public · **v0.2 TBD**

v0.2 若启用 POST-based invite 消费（mitigate R1 H6 GET-based 风险），将在此处完成。设计契约见 §2.A E3 块（该块保留作设计 stub · 不实现）。

### E9 · `GET /api/today` · authed · **v0.2 RESERVED, not implemented v0.1**

**为什么 v0.1 不实现**：v0.1 的 `/today` 页面走 Next 15 Server Component + 直接 `await db.select(...)` SSR，省去一次 Next → API → DB 的额外 HTTP round-trip（见 DECISIONS-LOG 2026-04-23 `/today page 数据 fetch 策略`）。唯一需要走 API 的场景是 v0.2 的第三方 / mobile PWA 消费 · v0.1 scope OUT-5 明确排除 mobile native / PWA，故 API 版本无对应消费方。

**v0.2 启用路径**（保持 URL 兼容）：

**Path**：`/api/today` · **Auth**：`requireAuth`
**Request**：query `?date=YYYY-MM-DD`（默认 today in `APP_TIMEZONE`）
**Success 200** envelope（设计 stub · 与 Server Component 内部 `loadTodayBriefing()` 返回结构对齐）：

```jsonc
{
  "data": {
    "briefing": { "forDate": "YYYY-MM-DD", "assembledAt": "..." },
    "items": [ /* BriefingItem[] · 见 §3.6 */ ]
  },
  "meta": { "staleDate": null | "YYYY-MM-DD" }
}
```

`staleDate` 字段：若 worker 失败 · `/today` 降级展示最近一次成功的 briefing · `staleDate` = 实际 briefing 日期（不等 query date 即为 stale）。

**Errors**（设计 stub）：401 `SESSION_EXPIRED` · 404 `NO_BRIEFING_YET`（该 lab 从未产出任何 briefing；empty state）

**v0.1 → v0.2 升级**：该 endpoint 实现时 `loadTodayBriefing()` 复用 · 不需要重写；Server Component 继续 SSR 同一函数；API 层仅加一层 HTTP adapter。**无 breaking change on URL structure**。

---

## §8 集成与测试 hook（与 task 绑定）

| Endpoint | 绑定 task | 对应 verification hook |
|---|---|---|
| E1 / E2 / E4 | T006（E1 + E2 invite POST）· T028 废除（logout 归入 T006 auth skeleton） | T006 verification：invite POST flow E2E；logout 返 204 + cookie 清除 |
| E5–E8 | T010 | T010 verification：admin 能 CRUD、member 只能 GET；第 16 topic 返 422 `TOO_MANY_TOPICS`（G4 H2） |
| E9 | **v0.2 RESERVED**（见 §7）· v0.1 不覆盖 · `/today` 走 Server Component | — |
| **E10** | T015（D16 Layer 2） | **O-verify-c6-api**（spec §6）· 3 条 curl 断言 + 4 条 Vitest case |
| E11 | T016 | T016 verification：skip.why 可见（`<strong>`）· multi-topic summary 分节展示 |
| E12 | T019 | T019 verification：breadcrumb 列表 |
| E13 / E14 | T023（resurface 操作） | T023 verification：dismiss / re-breadcrumb 事务 |
| E15 / E16 | T026 | T026 verification：sentinel banner 触发 |
| **E17** | T023 | SEC-1 双重 admin check CI scan + round-trip E2E（T032） |
| E18 | T030 | T030 verification：Caddy health check 接通 |

---

## §9 版本与尺寸

| 指标 | 值 |
|---|---|
| 本文件行数 | ~900 |
| Endpoint 总数（设计 stub 含） | 18 |
| 其中 v0.1 **实现**数 | 16（E3 + E9 留 v0.2 RESERVED · 不实现；E2 已从 GET 重写为 POST · G4 H4） |
| Error code 总数 | 31（+`CSRF_ORIGIN_MISMATCH` · G4 H4） |
| Resource type 总数 | 11（Topic / Paper / Summary / Action / Briefing / BriefingItem / Breadcrumb / ResurfaceEvent / PaperHistoryEvent / Seat / ExportEnvelope） |
| Export `schemaVersion` (camelCase · G3) | 1.1 |
| curl 示例数 | 17（E2 POST 形式 · G4 H4 更新） |

---

## 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · 18 endpoints · 30 error codes · 11 resource shapes · export_log/schema_version=1.1 · 对齐 spec.md v0.2.1 / architecture.md v0.2 / schema.sql v0.2.1 · 绑定 T009/T015/T016/T023/T026/T027/T028/T030 |
| 2026-04-23 | 0.2 | **drift 4 fix**：E9 `GET /api/today` 从 §2.C 移至新 §7 "Future / deferred endpoints"（标注 `v0.2 RESERVED, not implemented v0.1`）；v0.1 `/today` 走 Server Component SSR · 无此 API route · 删 §5 E9 curl 示例；原 §7 集成 hook → §8；原 §8 版本尺寸 → §9；E9 hook 行改为 `v0.2 RESERVED`。（spec.md 同步 bump 到 v0.2.2）|
| 2026-04-24 | 0.3 | **F5 pre-R_final hardening**：§3.11 ExportEnvelope 后新增 "Import round-trip notes" 段落 · 描述 `paper_summaries.llmCallId` FK 悬挂问题的 option (a) / option (b) 策略 · v0.1 默认 option (a)（null + schema.sql 列 nullable + ON DELETE SET NULL）· option (b) 保留为 v0.2 升级路径 |
| 2026-04-24 | 0.4 | **R_final BLOCK fix G3 + G4 H4**：(G3) §3.11 内联 type `schema_version` → `schemaVersion`（camelCase 权威） · bump 规则段改名 · E17 Body 注释从 `schema_version: "1.1"` 改为 `schemaVersion: "1.1"` · lab 对象加 `exportedAt` 字段（与顶层 redundant · operator 便利）· 排除注释 `llm_calls/export_log` → `llmCalls/exportLog`（casing）。(G4 H4) §E2 `GET /api/invite/:token/consume` 完整重写为 `POST /api/invite/consume` + body token · 对应 `/login` 页面读 URL fragment 并 POST · SEC-10 威胁模型重述（原 GET 路径 token 被 Caddy path-log 泄 → 改 POST body + SameSite=Lax + Origin header 检查 + 一次性 nonce CSRF 缓解） |
