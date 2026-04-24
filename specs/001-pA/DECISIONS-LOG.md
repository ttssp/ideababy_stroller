# Decisions Log · 001-pA

> 本文件记录 L4 阶段所有需要第一性论证的犹豫点。决策要么已在 spec/architecture/tech-stack 落地、要么在 risks.md 作为已知权衡、要么在此保留理由，供未来回看。

---

## 2026-04-23 · 规范参考资料目录位置

**犹豫**：`reference/`（完整 schema.sql / API 合同 / adapter 骨架 / runbook / 测试策略 / 错误码 / 术语 / 决策日志）应放在：
- A. `projects/001-pA/docs/`（建设者资料）
- B. `specs/001-pA/reference/`（与 spec 同级的规范）
- C. `discussion/001/001-pA/engineering-reference/`

**决策 · 选 B**：

**第一性**：这些文档的**读者**是初级工程师在**写代码前**必读。它们的权威度与 spec.md / architecture.md 完全相同（例如 error-codes.md 规定了 API 必须返回哪些 code，偏离就是 bug）。它们的**来源**是从 spec 推导的工程化细节，不是过程产物（不是 discussion 性质）。因此它们应当与 spec 同目录、同受 `specs-protection.md` 保护、同通过 spec-writer 修改。

**后果**：
- 必须由 spec-writer 创建（主会话不可直接 mkdir specs/ 下的新目录）
- 任何改动受版本控制，变动需配合 spec 版本 bump
- 初级工程师读文档的路径统一：`specs/001-pA/` 一个地方看完
- task 文件里的 `spec_ref` 可以指向具体 reference file（如 `reference/api-contracts.md#post-actions`）

---

## 2026-04-23 · R2 前是否补 DAG 重跑

**犹豫**：Q1/Q2/Q4 patch 让 T003 从 9h → 10h，但 edge 没变。是否要让 task-decomposer 重跑生成新 `dependency-graph.mmd`？

**决策 · 不重跑**：

**第一性**：DAG 图的语义是"有向图的拓扑"，节点权重是渲染细节，不影响依赖关系。`dependency-graph.mmd` 文件头注释说"113h, critical path 58h" —— 把它视为**粗估 metadata**，而非精确 ground truth（精确值永远从 task files sum 得到）。跑 R2 前让 decomposer 再跑一次纯为了把 header 数字从 113 改 114、58 改 59，投入产出不划算。

**记下**：初级工程师若想查精确总工时，应跑 `rg -h "estimated_hours" specs/001-pA/tasks/ | awk '{s+=$2}END{print s}'` 而不是读 DAG 文件。

---

## 2026-04-23 · reference/ 里的文档优先级

**犹豫**：P1–P8 共 8 份文档，在 R2 等待期哪些先写？

**分析**：
- P1 schema.sql（完整 DDL）— **阻塞** T003 的 Drizzle 翻译、所有 DB 测试、所有 migration 决策
- P2 api-contracts.md — **阻塞** T015（4-action API）、T010（topic CRUD API）、T023（export API）
- P3 llm-adapter-skeleton.md — **阻塞** T004（interface）、T013（summary pass）、T001 spike（要 adapter 才能跑 blind test）
- P4 directory-layout + env — **阻塞** T002（monorepo scaffold）
- P5 ops-runbook — **阻塞** T030/T031/T034（所有部署 + soak）
- P6 testing-strategy — **阻塞** T008（test harness）+ 全部 verification checklists
- P7 DECISIONS-LOG — 元文档，持续追加
- P8 error-codes + glossary-extended — 阻塞 API 实现者和前端消费者

**决策**：P1 + P4 + P3 先写（最阻塞 Phase 0），P2 次优先（Phase 1 前必备），P5/P6/P8 可在 Phase 0 后半段写。P7 持续追加。

---

## 2026-04-23 · 是否等 R2 再写 reference/

**犹豫**：R2 若返工 B1/B2/B3，reference/ 需要改 schema、API、adapter。

**第一性权衡**：
- R2 CLEAN/CONCERNS 概率 ~80% → reference/ 零返工
- R2 BLOCK 概率 ~20% → reference/ 返工**范围**通常小：
  - schema.sql：主体已定，只可能改 paper_summaries 字段名之类（<20% 内容）
  - api-contracts.md：POST /api/actions 骨架已有，可能改错误码
  - adapter-skeleton.md：interface 形态已稳
- 期望返工量 = 0.2 × 20% = 4% 总工作 —— 可接受

**决策 · 不等 R2**，边推进 P1–P4 边等。R2 一回来读 verdict，若 BLOCK 则 surgical patch reference/。

---

## 2026-04-23 · schema_version bump 策略

**犹豫**：JSON export schema_version 从 1.0 → 1.1 是 breaking 吗？future bump rules？

**决策**：
- **1.x** = 前向兼容（新增顶层 key；旧 importer 忽略新 key 仍工作）
- **2.x** = breaking（重命名字段、改字段类型、删除 key）
- 本次加 `paper_summaries` 顶层 key 属于前向兼容 → 1.1 正确
- 未来加 `export_log` 顶层 key → 1.2（不是 2.0）
- **规则落地**：reference/api-contracts.md 会在 Export section 给出完整版本演进规则

---

## 2026-04-23 · Drizzle ORM vs 原生 SQL 代码风格

**犹豫**：T003 写 Drizzle schema 还是 raw migration SQL？

**决策 · 双轨**：
- **Drizzle schema（TS）**：作为代码内类型源头，运行时 query builder 用
- **生成的 migration SQL（`drizzle-kit generate`）**：checked in to git，作为 authoritative DDL
- **reference/schema.sql**：手写的、完整的、commented DDL —— 供 DBA 审查 + 团队阅读 + 断线时快速查找

理由：Drizzle schema 对 TS 类型推导友好但对 CHECK/UNIQUE constraint 表达较啰嗦；生成的 migration 真实反映跑 DB 的 DDL；手写 schema.sql 最易读，初级工程师疑惑时查它。三者需保持一致，CI 跑 `drizzle-kit generate` 后 diff `reference/schema.sql` 确认无漂移。

---

## 2026-04-23 · prompt_version 命名规范

**犹豫**：`paper_summaries.prompt_version` 值怎么写？

**决策 · 语义版本 + 日期戳**：
- 格式：`v<major>.<minor>-<YYYY-MM>`
- 示例：`v1.0-2026-04`（初版）、`v1.1-2026-05`（调了示例）、`v2.0-2026-07`（重写结构）
- minor bump 表示 prompt 文字调整、major bump 表示 input/output schema 变化
- 同一 prompt_version 的 summary 视为等价；prompt bump 必须批量重跑历史 paper（由 T001 之后的 ops 任务处理，不在 v0.1 范围）
- **落地位置**：reference/llm-adapter-skeleton.md 会给出 const 清单和 bump policy

---

## 2026-04-23 · skip.why ≥ 5 chars 的中文边界

**犹豫**：char_length 对中文字符计数吗？CHECK constraint 会不会误杀中文 "太难" 这种 2 字合法 why？

**第一性验证**：Postgres `char_length(text)` 返回 character 数，对 UTF-8 编码正确按码点计数（中文字符每个 = 1 char，不是 byte）。所以 "太难了" = 3 chars < 5 → 被 CHECK 拒绝 —— **这是符合设计意图的**：我们要求 ≥ 5 字符，意味着 "太难了" 被认为信息量不足，operator 要写 "这篇和上周 X 方向冲突" 这样具体的理由。

**落地**：
- 保持 CHECK `char_length(btrim(why)) >= 5`
- risks.md TECH-8 已记录"中文边界"风险；对应 T015 写单元测试覆盖中/英/混合文本
- UI 提示 placeholder："为什么 skip？(至少 5 字符，说清这篇为何信息量不足)"

---

## 2026-04-23 · /today page 数据 fetch 策略

**犹豫**：`/today` 是 SSR fetch latest briefing（Server Component）还是 Client Component fetch after mount？

**决策 · SSR Server Component + 静态 fallback**：

**第一性**：
- PI 每天 8:00 打开，目标 p95 < 1.0s（SLA v0.1 §1.1）
- 06:00 worker 已把 briefing 全算完写进 Postgres → 8:00 读库就是纯静态
- Client-side fetch after mount 会引入 white-flash + 对 Postgres 发多余 round-trip
- Server Component 在 Next 15 App Router 下是一次 Node → Postgres，更快、更省

**落地**：
- `/app/(main)/today/page.tsx` 默认 Server Component，直接 `await db.select(...)`
- 4-action 按钮使用 Server Action（Next 15 原生），不需要 REST API
- skip-why-input.tsx 是 Client Component（需要 useState 和 key-stroke validation）

---

## 2026-04-23 · 单进程 vs 多进程部署

**犹豫**：Web server 和 worker 是同进程（Next.js 内嵌 cron）还是独立 systemd units？

**决策 · 独立 systemd units**：

**第一性**：
- Next.js 进程内跑 cron = **死锁风险**（worker crash 拖垮 web server）
- 独立 systemd units = **失败域隔离**；web 挂了 worker 还能算 briefing；worker 挂了 PI 还能看最后一份 briefing（stale banner）
- 独立部署 = **资源配额独立**：worker 内存可以给更大上限（LLM 调用吃内存）
- 独立部署 = **ops 可见**：`systemctl status pi-briefing-web` vs `pi-briefing-worker` 清楚

**落地**：
- `deploy/systemd/pi-briefing-web.service`（Next 启动）
- `deploy/systemd/pi-briefing-worker.timer` + `pi-briefing-worker.service`（每日 06:00）
- 详见 reference/ops-runbook.md

---

## 2026-04-23 · "operator 自用为主" 下 lab 邀请流程怎么做？

**犹豫**：PRD/L3 约定双 persona，但 Q6 结论"自用为主"。那还需要完整 invite 流程吗？

**决策 · 完整流程，简化 UX**：

**第一性**：
- **功能要做**：否则 operator 自己也没法把 2 位 lab-internal 成员拉进来，Q6 的"self + ≤2 seats"变成"operator 1 seat"，直接塌掉 O3
- **UX 可以极简**：一个 `/admin/invite` 页面，输入 email → 生成 token → 复制链接给成员 → 成员点链接登录；不做邮件发送（operator 手动在 lab 微信/消息里贴链接给成员）
- **简化后的预算**：T006 保留，但 T006 可以不实现邮件发送（SMTP 完全跳过），这和 CLAUDE.md "auth 最轻（lab 邀请码）" 对齐

**落地**：
- T006 范围：生成 hashed token + seat 行 + 24h TTL + 单次使用；NOT sending email
- UI：admin 在 `/admin/invite` 看到 token 的完整 URL (e.g. `https://lab-briefing.example.com/login?token=xxx`) 并 copy-paste 出去
- 节省的工时记入 slack

---

## 2026-04-23 · 初始化 topic 池怎么种？

**犹豫**：operator 第一次登陆时 topics 表空，看到什么？

**决策 · 引导式首页空态**：

**第一性**：v0.1 无 onboarding tour（PRD OUT-7），但 topic 池空 = briefing 永远为空 = 工具不可用。必须有一个 "首次 open 时的 topic 创建 UI"。

**落地**：
- `/today` loader 检测 topics 表为空（或 < 3 行）→ 渲染 empty state，文案："你还没有关注任何 topic。去 `/topics` 添加 8–15 个感兴趣的方向（每个 topic 定义 3–5 个关键词）。"
- `/topics` 页面上方一个 "Import from arXiv category" 辅助按钮（pre-fill cs.AI/cs.LG/cs.CL 常见分类）
- T010 task 需覆盖 empty state + category import helper
- 节省 onboarding tour 投入，但仍解决了 first-time UX

---

## 2026-04-23 · 为什么 ADR-3 共享 per-topic judgment 合理？

**回顾**：R1 Codex H2 + R1 review C4 都质疑过 ADR-3（shared judgment 让 operator seat 独立价值弱化）。

**决策论证**：
- **产品侧**：O3（operator 每周 ≥ 2 次登录）的核心价值不是"operator 看到不同 briefing"，而是"operator 的 4-action 反哺 lab 决策"。即使 briefing 内容一致，operator 的 skip/breadcrumb 行为差异仍然是独立价值。
- **成本侧**：per-seat judgment = 每天 4× 成本（假设 lab 4 seats）。PRD C11 envelope $50/月 vs per-seat 可能 $200/月。
- **H2 建议**：`/today` 直接展示 operator 痕迹（"Maya flagged this", "Maya disagreed"）。**这个产品增强接受**，但放 v0.2 —— v0.1 先验证 O3 是否成立，若 operator 从不登录，H2 的增强也救不回来。

**落地**：
- v0.1 保持 ADR-3（共享 per-topic judgment）
- 在 risks.md DOGFOOD-1 mitigation 追加一条"若 week-4 operator 登入 < 1 次/周，考虑 H2 改动提前到 v0.1"
- 这条放在这里 log，避免 spec 改动污染

---

## 2026-04-23 · drift 1 · SummaryRecord 字段命名：snake_case vs camelCase

**犹豫**：`reference/llm-adapter-skeleton.md §2` 使用 camelCase（`summaryText` / `promptVersion` / `modelName`）；`tech-stack.md §2.4` 初版使用 snake_case（`summary_text` / `prompt_version` / `model_name`）。两处不一致，下游工程师会困惑。

**第一性**：
- **TS 惯例**：JavaScript / TypeScript 生态里 interface 字段默认 camelCase；snake_case 出现的地方基本是 DB driver / JSON API 的边界。接口层 camelCase = 与 npm 生态对齐，不打架。
- **DB 约定**：Postgres 列名约定 snake_case（`architecture.md §5` 已明示），这和任何 SQL 工具的输出格式对齐。
- **边界在哪**：在 `src/lib/summary/persist.ts` 做一次性显式映射，类似 `postgres` driver 的 column-to-field 映射。这是项目里唯一的 snake↔camel 边界。

**决策 · camelCase 赢 · tech-stack.md 向 llm-adapter-skeleton.md 对齐**：
- `SummaryRecord` 接口字段：`summaryText` / `promptVersion` / `modelName` / `inputTokens` / `outputTokens` / `latencyMs` / `truncated`
- DB 列：`paper_summaries.summary_text` / `.prompt_version` / `.model_name` 等
- `src/lib/summary/persist.ts` 负责 camelCase → snake_case 插入 SQL + 反向
- tech-stack.md §2.4 已 patch · 注明"接口层 camelCase / DB snake_case"

**落地**：
- tech-stack.md §2.4 interface 示例全部改 camelCase · 加一句 "接口层 camelCase（TS 惯例）；DB 列 snake_case；`src/lib/summary/persist.ts` 负责转换"
- `reference/error-codes-and-glossary.md §3` 已收录 `paper_summaries` / `prompt_version` / `LLMProvider interface` 等词条 · 不额外增补（映射边界由代码描述，不是术语）

**相关**：drift 2（judgeRelation 签名）同批消化。

---

## 2026-04-23 · drift 2 · judgeRelation 签名：batch vs per-pair

**犹豫**：`tech-stack.md §2.4` 初版签名是 batch（`{anchor, candidates: [...]} → {labels: Record<id, RelationLabel>, tokens...}`）；`reference/llm-adapter-skeleton.md §2` 是 per-pair（`{candidatePaper, earlierAnchor, topic} → StateShiftVerdict`，单对 tuple）。两者不兼容。

**第一性**：
- **TS strict 安全性**：per-pair + `StateShiftVerdict` discriminated union（`kind: 'shift' | 'incremental' | 'unrelated'`）让 caller 可以窄化类型（`if (v.kind === 'shift') { use v.rationale }`）；batch 用 `Record<id, label>` 返回时 TS 只能推出 union 宽化，调用端必须 switch。
- **错误隔离粒度**：per-pair 下某一对判定失败 = 一次 LLM call 失败，caller 可独立 retry；batch 下任一对失败影响整个 response，LLM 是否吐了合法 JSON 也难以 partial-accept。
- **预算 / rate limit 友好**：per-pair 在 `recordLLMCall()` 审计表里也是 1 row / 1 call · `MONTHLY_BUDGET_CENTS` 检查更直觉；batch 下"20 对一 call"需要摊销成本。
- **spec 源**：spec.md §4.1 的 `LLM_judge(p_1, p_2, e)` 也是逐元组描述，caller 本就需要遍历 candidates。
- **batch 的唯一优势**（prompt 复用 / 成本摊销）在我们 8–15 topic × 每天约 5 个 candidate 的流量下可忽略（T001 spike 的 blind-test 成本 < $1）。

**决策 · per-pair 赢 · tech-stack.md 向 llm-adapter-skeleton.md 对齐**：
- `judgeRelation({ candidatePaper, earlierAnchor, topic }) → StateShiftVerdict & { inputTokens, outputTokens, latencyMs }`
- 由 caller（T012 state-shift pass）循环（candidate × anchor）
- tech-stack.md §2.4 已 patch · 签名与 llm-adapter-skeleton.md §2 逐字一致

**落地**：
- `src/lib/llm/types.ts` 字段定义以 llm-adapter-skeleton.md §2 为准
- T012 state-shift pass 实现时外层 loop · budget check 每 call 一次
- `RelationLabel` 的 enum 值集从 `{'supports','contradicts','supersedes','unrelated'}` 改为与 llm-adapter-skeleton.md §2 一致的 `{'shift','incremental','unrelated'}`（原值是 spec.md §4.1 描述层的概念 · 接口层用 3 类 verdict 聚合）

---

## 2026-04-23 · drift 3 · OpenAI output pricing: $10/M → $15/M

**犹豫**：`tech-stack.md §2.2` 初版写 GPT-5.4 output $10/M（2026-01）；`reference/llm-adapter-skeleton.md §4` 使用 $15/M（R1 Codex review 2026-03 refreshed）。月度成本估算对不齐（$10.5 vs $12）。

**第一性**：
- **事实校验**：2026-04 OpenAI 公开 pricing 页 GPT-5.4 输出确为 $15/M（与 Anthropic Claude Sonnet 4.6 一致）；初版 $10/M 是 2025-H2 旧价 · 2026-01 涨价未同步到 tech-stack.md
- **R1 Codex review 已验证**：review 输出里 refresh 过该值 · llm-adapter-skeleton.md §4 `calcCostOpenAI` 按 $15/M 实现是正确的
- **成本影响**：3M input × $2.5/M = $7.50 · 0.3M output × $15/M = $4.50 · 月度 $12 · C11 envelope $50 · buffer 仍 > 4× · **不触发 scope/outcome 变更**

**决策 · R1 Codex 值赢 · tech-stack.md §2.2 改 $15/M · 月度估算 $10.5 → $12**：
- tech-stack.md §2.2 表格 Pricing 行改 "input $2.5 / M token · output $15 / M token"（标注 "R1 Codex refreshed"）
- 月度预估行改 "3M input × $2.50/M = $7.50 + 0.3M output × $15/M = $4.50 ≈ $12/月"
- spec.md §3 C11 注释同步改 "GPT ≈ $10.5 → $12/月"

**落地**：
- tech-stack.md §2.2 ✅ patched
- spec.md §3 C11 注释 ✅ patched（也引用 `reference/llm-adapter-skeleton.md §4 calcCostOpenAI` 作为数字权威来源）
- spec.md 版本 bump 0.2.1 → 0.2.2

---

## 2026-04-23 · drift 4 · `GET /api/today` v0.1 是否实现

**犹豫**：`api-contracts.md` 初版把 E9 `GET /api/today` 列为 "v0.1 optional · SSR-only primary path"；但 T015 的 file_domain 不含 `/api/today` route。语义含糊 · builder 不知道该不该实现。

**第一性**：
- **primary path 是什么**：`/today` 页面是 Next 15 Server Component · `loadTodayBriefing()` 直接 `await db.select(...)` · 单次 Node → Postgres round-trip · p95 < 1s
- **API 版本给谁用**：v0.1 scope 没有 mobile PWA（OUT-5）· 没有第三方消费方（所有 endpoint 均 lab-internal · C7 禁公开）· 即**无消费方**
- **不实现的风险**：零 · v0.2 若启用 mobile PWA 再补上即可 · URL 无 breaking change
- **实现的成本**：~2h（route handler + envelope wrapping + 404 处理） · 在 C1 总预算里是小但非零 · 更糟是 "未被消费却要维护" 的 dead code

**决策 · 明确 "v0.1 not implemented" · 不是 optional**：
- E9 从 §2.C 移除 · 保留设计 stub 至 §7 "Future / deferred endpoints" · 标注 `v0.2 RESERVED, not implemented v0.1`
- §5 curl 示例删 E9 · §8 hook 表 E9 行标 "v0.2 RESERVED"
- `/today` 走 Server Component 的路径写进 DECISIONS-LOG（2026-04-23 `/today page 数据 fetch 策略` · 已存在 · 本条强化）
- v0.1 endpoint 实现总数：18 stub · 16 实际（E3 + E9 留 v0.2）

**落地**：
- api-contracts.md ✅ patched · E9 stub 移到 §7
- spec.md 变更日志 v0.2.2 记录

---

## 2026-04-23 · drift 5 · Invite consume flow：GET vs POST（R1 H6 accepted risk）

**犹豫**：`api-contracts.md E2` 现为 `GET /api/invite/:token/consume`；R1 H6 担心 email 客户端的 URL 预取（Gmail / Outlook 服务端扫链接）会意外消费 token。是否 v0.1 升级为 POST-based 确认页？

**第一性**：
- **R1 H6 威胁模型**：攻击面是"邮件扫描器 / IM 平台 link-preview 机器人的 GET 请求"触发消费 · 合法用户点击时收到 "already consumed" · 用户体验受损 + 支持成本
- **本项目 v0.1 实际触发条件**：
  1. 本项目 **不发邮件**（DECISIONS-LOG 2026-04-23 "operator 自用为主"）· token 通过 operator 私信（微信 / Slack / Signal）传给 lab 成员 · 不经过邮件扫描器
  2. IM 平台（微信 / Slack）也有 link-preview · 但 (a) 只扫公开可访问的 GET（大多不扫 query-string token）· (b) 本 URL 路径 `/api/invite/:token/consume` 的 token 在 **path**（非 query），多数 link-preview 不遵循 path 变量展开 GET
  3. 操作层缓解：Caddy 配置禁 query-string 日志（`ops-runbook.md §5`）· 即使扫链接也不在本系统留痕
  4. Lab ≤ 3 seat · 真人 operator 可人工帮忙重发
- **v0.1 升级 POST 的成本**：~4h（confirm 页面 + CSRF · GET → 只读 · POST 才 mutate） · 项目总预算 100h · 非零但可接受
- **但升级的收益**：在本项目威胁模型下接近 0（无邮件通道）· 不升级接受的风险是 "lab 内部 IM 偶发消费"，人工重发成本 1 次 5min

**决策 · v0.1 保留 GET · 记 SEC-10 低危险风险 · v0.2 升级 POST（不改 URL）**：
- E2 签名不变 · Notes 补 R1 H6 威胁模型说明（已在 api-contracts.md 中 · 见 E2 §Notes）
- ops-runbook.md §5 Caddy 配置断言 "禁止 query-string 日志"（已存在）
- risks.md 新增 SEC-10 "low severity · GET-based invite consume · 邮件扫描触发误消费"
- v0.2 升级路径：GET 返 confirm 页（只读）· POST 才真正消费 · URL 不变

**落地**：
- api-contracts.md E2 已有 Notes 说明 · 不再改接口
- ops-runbook.md §5 ✅ 已存在"禁 query-string 日志" · 不改
- risks.md SEC-10 待追加（本次若不追加 · 后续 risks.md 维护者补）
- DECISIONS-LOG 本条作为 "接受 H6 低风险" 的权威依据 · 任何 R2/R3 review 再问 H6 时引本条

---

## 2026-04-24 · pre-R_final hardening patch (F1–F6)

**犹豫**：三轮独立 audit（prompt injection L4/L8 + export mapping + cross-ref drift）发现 6 处 surgical drift 需在 Codex R_final review 前闭合。逐项如下：

- **F1 `truncateTo3Sentences()` 实现 + 测试布线**：`llm-adapter-skeleton.md §3` 引用 `enforceThreeSentences(text)` 但从未提供实现。junior 找不到函数定义；adversarial 注入测试缺 5-sentence 场景。
- **F2 confidence 降级逻辑 explicitly wired**：`llm-adapter-skeleton.md §3` 称"自动降级 < 0.5 → incremental"但无显式代码路径。junior 可能跳过。
- **F3 adversarial fixture 从 5 升到 15 类**：R1 H7 + R_final X3 希望更广覆盖。5 条样本不足验证 8 层防御。
- **F4 `api-export-full-route.ts` 过期注释**：comment 列 ~9 张表；实际 envelope 12 张。跟 api-contracts.md §3.11 不一致。
- **F5 `llm_call_id` FK round-trip policy**：`paper_summaries.llm_call_id` FK 指向 `llm_calls`，但 JSON export 不含 `llm_calls`（compliance 审计分离）。round-trip import 会 FK violate。
- **F6 schema.sql header 版本号漂移**：schema.sql header 仍写 "v0.2.1"，spec.md 已 v0.2.2。

**决策（逐项）**：

| F# | 决策 | 落地 |
|---|---|---|
| F1 | 新建 `reference/skeletons/llm-utils.ts` · 权威实现放 `llm-adapter-skeleton.md §3.5` · 两 adapter import `./utils.js`（不是 `./truncate.js`） | adapter-skeleton §3/§4 import 更新 · stub `llm-anthropic-stub.ts` + `llm-openai-stub.ts` import 更新 · testing-strategy §2.4 新增 7 条 unit test |
| F2 | 在 `parse()` 之后显式插 `if (kind==='shift' && confidence<0.5) → incremental` guard · 两 provider 对称 | adapter-skeleton §3/§4 代码块更新 · stub TODO 包含字面代码 · testing-strategy §2.4 新增 3 条 confidence-floor test |
| F3 | 15 条分 5 大类（A/B/C/D/E）· fixture shape 补 `category/description/expected_outcome` · 不动 fixture 文件 id 号（rotation 策略保留号位） | testing-strategy §11.3 替换 · §2.4 replace adversarial 子块 · 红线 2 延伸表新增 · adapter-skeleton §10 替换 5-条 → 15-条映射 · T001.md Outputs 加 `adversarial-abstracts.json` 条目 |
| F4 | 注释列全 12 张 · 排除清单 3 张（sessions/llm_calls/export_log）· 引入 F5 stub policy 的 inline 注释 | `api-export-full-route.ts` comment block 替换 |
| F5 | **option (a) 默认**：import 时 `paper_summaries.llm_call_id = null` · schema.sql 列改 `nullable + on delete set null` · T023 round-trip test 加 null 断言 · option (b)（stub rows）保留为 v0.2 升级路径 | api-contracts.md §3.11 新段落 · T023.md Verification + Implementation plan 6 + Known gotchas 更新 · schema.sql 列 DDL 改 · T003.md step 9 + gotchas 更新 · compliance.md §2 备注 |
| F6 | header bump v0.2.1 → v0.2.2 · 附 file-level changelog 两行（v0.2.1 初版 / v0.2.2 F5 hardening） | schema.sql header 替换 |

**第一性**：每条 drift 都会在 R_final review 被 Codex 拎出来成为 BLOCK。提前 surgical patch 比 R_final BLOCK 后再改更便宜（review 再重跑 = 10+ min agent spin-up vs 1 分钟手改）。F1/F2 本质是**文档与代码的契约闭合**（junior 按图索骥不应卡壳）；F3 是**测试深度**（5 条不够 audit 风险面）；F4/F5 是**exporter-importer 契约闭合**（round-trip 不能 FK violate）；F6 是**版本号一致性**（单一事实来源，schema.sql 跟 spec.md 同步 bump）。

**落地确认**：
- 6 个 F-item 涉及文件 · 11 个（`llm-adapter-skeleton.md` · `llm-anthropic-stub.ts` · `llm-openai-stub.ts` · `llm-utils.ts` 新建 · `testing-strategy.md` · `api-export-full-route.ts` · `api-contracts.md` · `T001.md` · `T023.md` · `schema.sql` · `compliance.md`）· 加 T003.md（F5 DDL 连带）· 加本 DECISIONS-LOG 本条。
- `spec.md` 不动（已在 v0.2.2，无新 scope / 无新 outcome）。
- 下一步：kickoff Codex R_final adversarial review，覆盖 8 层 injection defense + export round-trip 全路径。

---

## 持续更新

每次遇到"犹豫点"且超过 3 分钟思考时，在此追加新条目。格式：
```
## YYYY-MM-DD · <简短标题>

**犹豫**: ...
**决策**: ...
**第一性**: ...
**落地**: ...
```
