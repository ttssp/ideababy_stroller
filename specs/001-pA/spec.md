# Spec · 001-pA · PI Briefing Console

**版本**: 0.3.1
**创建**: 2026-04-23
**上次修订**: 2026-04-24（R_final2 G6 patch · D15 clarification · LLM 合同 split-brain 闭合 · 见变更日志）
**Source PRD**: `discussion/001/001-pA/PRD.md`（version 1.0 · 人工通过 `/fork 001 from-L3 candidate-A as 001-pA` 批准）
**Lineage**: `proposals/001` → `discussion/001/L1` → `discussion/001/L2` → `discussion/001/L3` candidate A → `001-pA`
**L4 intake date**: 2026-04-23（Q1–Q6 在 operator 与 spec-writer 之间解决）

> 本 spec 是下游 task-decomposer / parallel-builder / adversarial reviewer 的**工程合同**。PRD.md 是产品决策源头，本文件不得覆写产品决策；若发现产品层缺陷请写到 `OPEN-QUESTIONS-FOR-OPERATOR.md`，不得私自 revise。

---

## 1. Outcomes（来自 PRD · 可观察 · 可验证）

每一条结果都可以被"是 / 否 / 具体数字"判定，不使用"可扩展 / 体验好"等副词。

| # | Outcome（来自 PRD §Success）| 观察窗口 | 可验证信号 |
|---|---|---|---|
| O1 | **PI 日活 ≥ 25/30**（briefing 成为每日 ritual，不是 newsletter） | 连续 30 天 | Postgres `sessions` 表中 PI seat `user_id` 的 distinct `login_date` ≥ 25 |
| O2 | **PI 每月 ≥ 5 次 breadcrumb resurface 被实际点开** | 按自然月统计 | `resurface_events.clicked_at IS NOT NULL` 行数 ≥ 5 |
| O3 | **Operator 每周 ≥ 2 次独立登入 briefing**（独立 seat 不会死） | 从第 4 周起 | `sessions` 表中 operator seat 周内 distinct `login_date` ≥ 2 |
| O4 | **PI 可说出 ≥ 2 个"没这工具会漏看"的真实案例**（Q6 下调：外部访谈 → 周度自陈 + 截图证据） | 30 天 + 60 天 | `briefings/self-report/YYYY-WW.md` 文件存在且附 ≥ 1 张带时间戳的"原本会漏看"截图 |
| O5 | **Day-45–60 breadcrumb resurface 出现 aha（A→B 升级 gate）** | 45–60 天 | 周度自陈中出现"因 breadcrumb 重新点开 X 并改变本周方向"的具体案例 ≥ 1 例 |

**PRD §Biggest product risk 的 Kill-window = 60 天** 明确写入 spec.md：日程上 v0.1 ship 后 day-60 做全量复盘，任一 O1/O2/O5 未达成即回 L2。

**O4 的 Q6 下调理由**（L4 intake 2026-04-23）：v0.1 的 dogfood 收缩为 operator 自用 + ≤ 2 名 lab-internal operator，原 PRD "30 天外部访谈"无法闭合；改为 **"周度 1 次自陈（self-report）+ 每次附一张带时间戳的截图（证明当下若没有本工具会漏看）"**。若 O4 60 天累计 < 2 例，视同 O4 失败。

---

## 2. Scope Boundaries

### 2.1 v0.1 Scope IN（直接继承 PRD · 新增 IN-8）

| # | Item | PRD 引用 |
|---|---|---|
| IN-1 | **Topic 管理** · 8–15 topic · admin 手动 CRUD · 每 topic = {keyword pool, arXiv category, optional seed author} | PRD §Scope IN IN-1 |
| IN-2 | **每日 briefing（Web page）**：digest-first · 按 **state shift** 组织（不是论文堆叠）· 每 topic 一行 state 摘要 + 至多 3 篇触发论文 | PRD IN-2 |
| IN-3 | **4-action 标注**：`read_now` / `read_later` / `skip` / `breadcrumb` · 每次可附一句自由文本 why | PRD IN-3 |
| IN-4 | **Breadcrumb resurface**：6 周 / 3 个月 / 6 个月分别 resurface · 带 "为什么现在又回来" 上下文 · **并叠加 citation trigger**（L4 intake Q4）：新论文在同 topic 引用了用户之前 breadcrumb 过的论文 → 立即 resurface | PRD IN-4 + L4 Q4 |
| IN-5 | **双 seat auth**：PI + operator 各自独立 login · email token invite · ≤ 15 用户 · 全员 read+write · admin 管理 topic 池 | PRD IN-5 |
| IN-6 | **Data portability**：JSON export 全量（涵盖 topic / paper / action / breadcrumb / resurface event） | PRD IN-6 |
| IN-7 | **LLM 解读**：仅基于 abstract + metadata · summary ≤ 3 句 · **summary 持久化在 `paper_summaries` 表 per (paper_id, topic_id, prompt_version)**（R1 adversarial fix · D15）· 守红线 2（委托 triage ≠ 替代阅读） | PRD IN-7 · R1 2026-04-23 |
| **IN-8** | **自持 Postgres 16 作为唯一主存储 + JSON export endpoint**（L4 intake Q1）：SQLite 路径推迟到 v0.2 · Postgres 16 由 operator 自行部署 · 数据不离开 operator 掌控的机器 | L4 intake Q1（2026-04-23） |

### 2.2 v0.1 Scope OUT（直接继承 PRD · 工程语境下"这是有意识 descope，不是遗漏"）

| # | Item | PRD 引用 | 工程语境补注 |
|---|---|---|---|
| OUT-1 | 完整 Taste agent 闭环（hybrid agent 反向影响 briefing） | PRD OUT-1 | 只 collect explicit disagree，disagree 文本落库但不喂回 ranking |
| OUT-2 | Topology graph / topic 关系图主视图 | PRD OUT-2 | 前端不渲染 graph，数据层不预计算 co-cite 关系 |
| OUT-3 | Lab shared belief ledger / stance history | PRD OUT-3 | 无 `stances` 表，无 stance UI |
| OUT-4 | Paper 二次分析 / novelty 自动评分 / 跨 paper 对比 | PRD OUT-4 | LLM 只处理单篇 abstract，不做 cross-paper |
| OUT-5 | Mobile native / CLI / PWA | PRD OUT-5 | 仅 desktop Web（≥ 1024px viewport） |
| OUT-6 | PDF 全文解析 | PRD OUT-6 | 仅从 arXiv API 取 metadata + abstract，不下载 PDF |
| OUT-7 | Onboarding-focused view / Carol 场景 | PRD OUT-7 | 无 guided tour、无"第一次使用"特殊视图 |
| OUT-8 | 公开打分 / 社区 review / 排行榜 | PRD OUT-8（硬红线 3） | 任何 endpoint 都需 auth，无匿名读 |
| OUT-9 | Billing / payment | PRD OUT-9 | auth 预留但不实现 billing，不引入 Stripe SDK |
| OUT-10 | Per-topic 可见性分层 / 细粒度权限 | PRD OUT-10 | schema 不为 per-topic ACL 预留列，v0.2 加即可（Q5 记入本 spec Open Questions） |
| OUT-11 | 跨 lab federation / 公开 radar | PRD OUT-11 | 无 external sharing endpoint，所有 endpoint 均 lab-internal auth |

详见 `non-goals.md`。

---

## 3. Constraints（数字 + 来源，不使用形容词）

| # | Constraint | Source | Rigidity |
|---|---|---|---|
| C1 | **时间预算 ~20h/周，目标 v0.1 ~5 周（总 ~100h）** | PRD C1 · L3R0 intake Block 1 | Hard |
| C2 | **Platform = desktop Web only**（无 mobile native、PWA、CLI） | PRD C2 | Hard |
| C3 | **v0.1 先免费，预留 auth 不做 billing** | PRD C3 · L3R0 intake Block 3 | Hard |
| C4 | **双 persona 必须被 serve，PI 优先** | PRD C4 · L3R0 intake Block 2 | Hard |
| C5 | **Red line 1: 不扩成通用论文发现器**，守 8–15 topic | PRD C5 | Hard · 违反 = block |
| C6 | **Red line 2: 不替代第一手阅读** · (a) summary_text 受 DB CHECK `summary_sentence_cap` 限制为 ≤ 3 句（`paper_summaries` 表）· (b) skip 决策**必须**可追溯：skip 的 `why` ≥ 5 chars 由 **DB CHECK `skip_requires_why` + API validation（`recordAction.ts`）+ UI required（`skip-why-input.tsx` inline expand）三层机械兜底**（R1 adversarial fix · D16） | PRD C6 · R1 2026-04-23 | Hard · 违反 = block |
| C7 | **Red line 3: v0.1 不做公开打分 / 社区 review** | PRD C7 | Hard · 违反 = block |
| C8 | **Data portability 是 v0.1 承诺** | PRD C8 · L2 §6 condition 1 | Hard |
| C9 | **≤ 15 用户**（lab 边界） | PRD C9 | Hard |
| **C10** | **Dogfood = operator + ≤ 2 名 lab-internal operator**（v0.1 不招募外部 lab） | L4 intake Q6（2026-04-23） | Hard |
| **C11** | **LLM 月度 token 成本 envelope ≤ $50 USD**（15 topic × 20 candidate papers/day × 300-token abstract × 30 day ≈ 3M token/month） | L4 intake Q2（2026-04-23） | Hard |
| **C12** | **所有用户数据仅存 operator 自持的 Postgres，不经第三方分析/日志** | L4 intake Q1 · C8 延伸 | Hard |
| **C13** | **Solo operator 可持续性**：任何依赖持续人工 oncall 的设计不可接受（需支持 operator 不在 7 天时自动继续 briefing） | PRD §Biggest risk · bus-factor | Hard |

C11 的数字来源：Claude Sonnet 4.6 input $3/M·output $15/M、GPT-5.4 input $2.5/M·output $15/M（2026-04 官方 pricing · R1 Codex review refreshed）。3M input + 0.3M output → Claude ≈ $13.5/月，GPT ≈ $12/月，留 ≥ 3× buffer 给重试/spike → $50 envelope 合理。（数字权威来源：`reference/llm-adapter-skeleton.md §4 calcCostOpenAI` 按 $15/M 实现。）

---

## 4. Prior Decisions（来自 PRD / L3 / L4 intake，不得 re-litigate）

| # | Decision | Source |
|---|---|---|
| D1 | **三红线绝对硬宪法**（不扩通用发现器 / 不替代阅读 / 不做公开打分） | PRD C5–C7 · L3 stage doc candidate A · 3 红线 |
| D2 | **digest-first homepage，topology 不做主视图** | PRD UX principle 4 · L2 §6 condition 2 · L2 §5 自限 |
| D3 | **双 persona，PI 优先**；operator 独立 login（R2 修正，不允许共用 login） | PRD §User persona · L3R0 intake Block 2 |
| D4 | **4-action = `read_now` / `read_later` / `skip` / `breadcrumb`**（不可增减） | PRD IN-3 · L2 §1 |
| D5 | **Breadcrumb resurface schedule = {6w, 3mo, 6mo} + citation-triggered 即时触发** | PRD IN-4 · L4 intake Q4（2026-04-23） |
| D6 | **State shift 定义 v0.1 启发式**（下一小节 §4.1 formalize），标记 `provisional`，T001 spike 后 refine | PRD Open Q3 · L4 intake Q3（2026-04-23） |
| D7 | **LLM provider 推迟到 T001 spike 决定**；v0.1 tech stack 给出统一 adapter interface（Claude Sonnet 4.6 long-context 与 GPT-5.4 两个候选并列，spike 后 operator 拍板） | L4 intake Q2（2026-04-23） |
| D8 | **Dogfood = 自用 + lab-internal ≤ 2 seat**；O4 下调为周度自陈 + 截图证据；day-30 < 3 seat active 时触发 escalate | L4 intake Q6（2026-04-23） |
| D9 | **主存储 = self-host Postgres 16** · JSON export 覆盖全部 user-authored 数据 · SQLite fallback 推到 v0.2 | L4 intake Q1（2026-04-23） |
| D10 | **Summary ≤ 3 句**（守红线 2）· LLM 不做 cross-paper 对比 · 不解析 PDF 全文 | PRD IN-7 · OUT-4 · OUT-6 |
| D11 | **L2 §6 6 条 conditions 全数继承**：data portability 承诺、digest-first 首页、hybrid taste（v0.1 仅 explicit disagree 文本，不闭环）、可剪枝低价值留痕、buyer+operator 双层、delegation 假设待 60 天真实验证 | L2 §6 · L3R0 intake Block "硬约束" |
| D12 | **Kill-window = 60 天**（不是 30；breadcrumb aha 窗口需要 45–60 天真实陪跑） | PRD §Biggest risk · L3 stage doc candidate A |
| D13 | **Backend 语言 = TypeScript strict**（pnpm + Node 22 LTS + Biome） | CLAUDE.md 项目偏好 + tech-stack.md §Primary stack |
| D14 | **UI 粗糙可接受**（Speed > Polish；表格 + 纯文本 briefing 即可） | PRD UX principle 1 · L3 stage doc candidate A |
| **D15** | **Per-paper summary 持久化在独立 `paper_summaries` 表** per `(paper_id, topic_id, prompt_version)` · `llm_calls` 仅作审计表（不存 response body）· **T013 只写 `paper_summaries` · adapter 已内部写 `llm_calls` 并把 `llmCallId` 通过 `SummaryRecord` 回传**（G6 权威 · R_final2 · 2026-04-24）· T014/T015/T016/T023 读 `paper_summaries` | 2026-04-23 R1 adversarial fix（Codex B1）· 解决 IN-7 原设计 summary 无权威落点的结构合同空洞；2026-04-24 R_final2 G6 fix · adapter-内写消除 cost-cap 绕过风险（详见 `reference/llm-adapter-skeleton.md §2/§3/§4/§7`） |
| **D16** | **Skip `why` 强制 ≥ 5 chars** 三层机械兜底：(1) DB `actions.skip_requires_why` CHECK `action != 'skip' OR char_length(btrim(why)) >= 5`；(2) API `src/lib/actions/recordAction.ts` 预验证返 400 `SKIP_WHY_REQUIRED`；(3) UI `skip-why-input.tsx` inline expand + `Submit` 按钮 disabled until trim ≥ 5 | 2026-04-23 R1 adversarial fix（Codex B2）· 将 C6 从"可选习惯"升级为硬约束 |

### 4.1 State-shift heuristic · v0.1 formal 定义（provisional，T001 后可改）

**输入**：某 topic T 在过去 7 天内被匹配进入的新 paper 集合 `P_new(T)`（匹配规则：arXiv category 交集 OR keyword pool 命中 ≥ 1 OR seed author 命中）。

**规则**（纯 Postgres query，无 LLM）：
```
shift(T) := TRUE iff
  ∃ earlier_paper e ∈ Papers
  where e 被 ≥ 2 个 p_i ∈ P_new(T) 引用
  AND LLM_judge(p_1, p_2, e) 在 {supports, contradicts, supersedes} 中返回
      至少一对 conflicting labels （即一个 supports + 另一个 contradicts/supersedes）
```

**输出**：对每个 shift，系统记录 `{topic_id, trigger_papers: [p_1, p_2, ...], anchor_paper: e, label_conflict: {p_1: supports, p_2: contradicts}}`，briefing 用它生成 "state 摘要一行 + 至多 3 篇触发论文"。

**阈值**：v0.1 要求 trigger_papers 数 ≥ 2；若某 topic 7 天内无 shift，briefing 该 topic 行显示 "frontier stable, no shift"（不强行捏造）。

**status = provisional**：T001 spike（见 §5）将用 20 篇 operator 预先人工标注过的 arXiv paper blind 测；若 LLM judgment 准确率 < 70%，保留 heuristic（可 adjust 阈值），LLM 降级为仅生成 summary；若 ≥ 70%，保留 heuristic + LLM judge 联合判定。任一路径都不会把 state-shift 判定完全交给 LLM 黑箱。

### 4.2 Breadcrumb resurface trigger · formal 定义

**触发条件（timed）**：
- breadcrumb 创建 ≥ 6 周、未 dismissed → surface 一次
- breadcrumb 创建 ≥ 3 个月、此前 timed surface 未 clicked 或 clicked 后未 dismissed → surface 一次
- breadcrumb 创建 ≥ 6 个月、此前两次 timed surface 未 dismissed → 最后一次 surface

**触发条件（event-triggered · citation-driven）**：
- 新 paper p 进入同 topic 流；p 的 reference list 中命中用户任一 breadcrumb paper → 立即 surface（**优先级高于 timed**，且不消耗 timed schedule 次数）

**"为什么现在又回来" 上下文**：每次 resurface 系统必须自动填写以下两种模板之一并写入 `resurface_events.context_text`：
- timed: "于 YYYY-MM-DD 被 breadcrumb；距今已 {n_weeks} 周"
- citation: "于 YYYY-MM-DD 被 breadcrumb；今天被新 paper [title](url) 引用"

---

## 5. Task Breakdown（phase 级 · 具体 T-file 已由 task-decomposer 展开在 `tasks/T<NNN>.md`）

下方给出**阶段骨架 + 权威 task ID**（G2 · 2026-04-24 R_final BLOCK fix 迁移到与 `dependency-graph.mmd` 一致的新编号；此前 T005/T007/T009/T029 等旧编号已废弃）。

### Phase 0 · Foundation + LLM spike（T001–T008 · ~22h）
- **T001 · LLM provider blind-test spike**（2–3 天，入口关卡）
  - **退出条件**：至少一个 provider 在 20 篇 blind test 上 `state-shift` 判定准确率 ≥ **70%**（≥ 14/20 正确）；两家都 ≥ 70% 按成本裁决；两家都 < 70% 降级为纯启发式，LLM 仅用于 summary
  - **产出**：`projects/001-pA/spikes/T001-llm-provider-report.md` + operator `approved-provider: <name>` sign-off
- **T002 · 项目脚手架**：Next.js 15 App Router + TS strict + pnpm + Biome + Vitest/Playwright 基础
- **T003 · Postgres schema + Drizzle migrations**：**15 张表**（labs / seats / sessions / topics / papers / paper_citations / paper_topic_scores / actions / breadcrumbs / resurface_events / briefings / fetch_runs / llm_calls / paper_summaries / export_log）· R1 CHECK（`skip_requires_why` · `summary_sentence_cap` · G1 count-terminator 语义）· F5 nullable `llm_call_id`
- **T004 · LLMProvider interface + Anthropic/OpenAI adapters**：`src/lib/llm/` 完整落地（types camelCase · adapter 内部写 `llm_calls` · select + fallback · prompt-version · audit · truncateTo3Sentences · stripPII）。**权威契约见 `reference/llm-adapter-skeleton.md §1–§7`**，本 spec 不再内联接口代码样例
- **T005 · arXiv API adapter**（daily batch 拉取 + category/keyword 过滤；catchup ≤ 24h；rate limit 遵守 arXiv ToS · LEG-2）
- **T006 · Auth skeleton**：email token invite（**G4 H4 · POST `/api/invite/consume` + body token · 不再用 GET path token**）· session middleware · 双 seat 独立 login
- **T007 · Env / secrets / systemd units baseline**：zod env schema（**provider enum = `anthropic|openai`**，不是 `claude|gpt`）· systemd unit 文件 · `.env.example` · `LoadCredential=`
- **T008 · Test harness**：vitest / playwright 全局 setup · truncate-between-tests · meta test（red-line 3 no-public-endpoint scan）

**Phase 0 Exit**：T001 blind-test 出结果并 operator 批准；schema 可执行；adapter contract test 全绿；能在 CLI 里跑 `pnpm dev:fetch arxiv --topic <id>` 拿到 paper 落库。

### Phase 1 · Core briefing（T010–T016 · ~33h）
- **T010 · Topic CRUD**（admin-only write · all seat read · cap 15 · **G4 H2 · 422 `TOO_MANY_TOPICS`**；路径 `src/app/(main)/topics/page.tsx` + `[id]/edit/page.tsx` + API `src/app/api/topics/route.ts` + `[id]/route.ts`）
- **T011 · Daily fetch worker**（systemd timer 06:00 · on-boot catchup · fetch → match → briefing hook slot · resurface hook slot）
- **T012 · State-shift pass**（§4.1 heuristic + LLM judge per-pair · T001 spike 结果驱动）
- **T013 · LLM summary pass + `persistSummary`**：T004 adapter 返回 `SummaryRecord`（camelCase · `llmCallId` 已由 adapter 写 `llm_calls` 时填好）→ `persistSummary` 写 `paper_summaries`（**T013 不写 `llm_calls`** · ADR-6）· OpenAI 输出 $15/M
- **T014 · Briefing 预计算**（写 `briefings` 表 · topic-level `state_summary` + `trigger_paper_ids` ≤ 3 · 读 `paper_summaries` 的 summary 片段 JOIN 展示）
- **T015 · /today page + 4-action API**（SSR Server Component 直连 DB · **v0.1 无 `/api/today`** · POST `/api/actions` 含 **D16 三层红线兜底**：DB CHECK + API 验证 + UI Submit disabled）
- **T016 · Paper history page** `/papers/:id/history`（多 topic summary 分节展示 · skip why 可见）

**Phase 1 Exit**：operator 06:30 看到当天 briefing；p95 /today < 1s（local Postgres）；4-action 全部可追溯。

### Phase 2 · Breadcrumb + resurface + export + sentinel（T020–T024 · ~24h）
- **T020 · Breadcrumb 列表页** `/breadcrumbs`（展示 user 历史 breadcrumb）
- **T021 · Resurface scheduler**（timed `timed_6wk | timed_3mo | timed_6mo` + citation-triggered · TECH-7 topic-overlap 去噪 · worker hook slot · citation 优先于 timed）
- **T022 · Resurface UI**（/today 顶部 banner · dismiss / re-breadcrumb API）
- **T023 · JSON export endpoint** `/api/export/full`（admin-only · `schemaVersion='1.1'` · **G3 · 12 顶层 keys** camelCase · `buildFullExport(labId)` · 审计写 `export_log`）
- **T024 · day-30 sentinel**（read `labs.first_day_at` + `labs.allow_continue_until` · `/today` 顶部 banner · admin sign-off `/admin/allow-continue`）

**Phase 2 Exit**：breadcrumb 两条 resurface 路径可触发并展示 context；export round-trip 通过；sentinel 按 `active_seats_30d` 触发。

### Phase 3 · 部署 + E2E + soak（T030–T034 · ~18h）
- **T030 · Deployment**（`deploy/scripts/provision.sh` + `deploy/scripts/deploy.sh` + Caddy reverse_proxy + auto-TLS + Postgres 16 provision + **G4 H3 · systemd unit 仅安装不创建**（unit 文件来自 T007）+ **`deploy/scripts/pg-dump.sh` + `deploy/scripts/restic-backup.sh`** · 权限验证用 `PGUSER=webapp_user PGPASSWORD=... psql`，不用 `sudo -u webapp_user`）
- **T031 · Backup drill**（restic 云盘副本 · 季度 restore drill · RTO ≤ 2h）
- **T032 · Phase 3 Playwright e2e**（双 seat login · export 下载 · round-trip · sentinel banner · skip-requires-why）
- **T033 · Ops runbook**（`reference/ops-runbook.md` 主体已写 · T033 只补生产验证段 + 冷备 / 换 VPS）
- **T034 · 48h soak test**（真实 arXiv 日 fetch × 2 天连跑 · LLM 成本跟踪）

**Phase 3 Exit**：operator 可部署到一台 VPS · ≥ 7 天连跑无人工干预 · export round-trip · sentinel 响应正常。

> **LLMProvider interface 权威**：不再在本 spec 内联代码样例（旧 `summarize(paper): string` 签名已废弃）；**以 `reference/llm-adapter-skeleton.md §2`（`src/lib/llm/types.ts`）为单一真源**，含 camelCase `SummaryRecord` + per-pair `judgeRelation(input: JudgeRelationInput) => Promise<JudgeRelationResult>` + discriminated union `StateShiftVerdict`。任何 task 的代码样例/签名与此文件冲突 = PR 打回。

---

## 6. Verification Criteria（每条 Outcome → 具体可执行的判定）

| Outcome | Verification 方法 |
|---|---|
| O1 · PI 日活 ≥ 25/30 | `pnpm ops:metric daily-active --user-id <pi-seat> --window 30d` 返回 ≥ 25 |
| O2 · 每月 ≥ 5 次 resurface click | `SELECT count(*) FROM resurface_events WHERE clicked_at IS NOT NULL AND seat_id = <pi> AND clicked_at >= now() - interval '30 days'` ≥ 5 |
| O3 · Operator 每周 ≥ 2 次独立登入 | 从 week-4 起，每周 Monday 跑 `pnpm ops:metric weekly-operator-login --week <n>`，连续 4 周 ≥ 2 视为 sustain |
| O4 · ≥ 2 个漏看真实案例（下调版） | `ls briefings/self-report/*.md \| wc -l` ≥ 4（每周 1 个）AND 其中 ≥ 2 篇包含 "若无本工具 → 会漏" 并附带截图文件 |
| O5 · day-45–60 aha | week 6–9 的 self-report 中必须出现 ≥ 1 条 "因 breadcrumb 重新点开 X 并改变本周方向" 具体案例；由 operator 人工 sign-off（标记在 self-report 中） |

**R1 adversarial fix 新增红线验收**（2026-04-23）：

| 验收 hook | 验证命令 / 步骤 | 属于 |
|---|---|---|
| **O-verify-red-line-2** | `INSERT INTO paper_summaries (summary_text = 's1. s2. s3. s4.')` → CHECK 约束 `summary_sentence_cap` 拒绝（`pnpm vitest run tests/db/constraints.test.ts`） | C6 红线 2 机械兜底 |
| **O-verify-c6-db** | `INSERT INTO actions (action='skip', why=NULL)` → CHECK `skip_requires_why` 拒绝；`(action='skip', why='  ')` 同样拒绝（btrim 后 < 5）；`(action='read_now', why=NULL)` 通过 | C6 / D16 Layer 1 |
| **O-verify-c6-api** | `POST /api/actions {action:'skip', why:''}` → 400 `SKIP_WHY_REQUIRED`；`{action:'skip', why:'no.'}` → 400；`{action:'skip', why:'I have read this before'}` → 200 | C6 / D16 Layer 2 |
| **O-verify-c6-ui** | Playwright：点击 skip 按钮 → textarea 展开（不立即 POST）；输入 < 5 字符 → Submit 按钮 disabled；输入 ≥ 5 字符 → Submit 可点 + 提交成功 | C6 / D16 Layer 3 |

**T001 spike 额外验收**（这是 Phase 0 准入条件而非 Outcome）：blind test 结果报告必须由 operator 签字（即 operator commit 一个 `approved-provider: <name>` 行到 `projects/001-pA/spikes/T001-llm-provider-report.md`）后 Phase 1 才能开始。

**Sentinel 验收**：`day-30` 时自动计算 `active_seats_30d` = 过去 30 天有 ≥ 1 次 login 的 seat 数；若 < 3，`/today` 顶部显示 escalate banner 并阻塞新 feature 开发，直到 operator 签字 `allow-continue` 或 pivot。Sentinel 状态由 T024 读 `labs.first_day_at` + `labs.allow_continue_until` 两列（T003 R1 已前置）。

---

## 术语表（Glossary）

| 术语 | v0.1 项目内权威含义 |
|---|---|
| **Topic** | PI 手动维护的一个关注主题，包含 {keyword pool, arXiv category, optional seed author}；一个 lab 有 8–15 个 topic。 |
| **State shift** | 某 topic 过去 7 天内，出现 ≥ 2 篇引用同一早期工作且结论/立场有冲突的新 paper；v0.1 的正式定义见 §4.1。**不等于**"今天出了新 paper"。 |
| **Briefing** | 每日 06:00 预计算的 per-lab 一页报告，按 topic 列出 state 摘要 + 至多 3 篇触发论文。**不是**按论文堆叠的 digest。 |
| **4-action** | 对 briefing 中每篇候选 paper 可执行的四种标注之一：`read_now` / `read_later` / `skip` / `breadcrumb`（不可增减）。 |
| **Breadcrumb** | 一种 4-action，语义 = "当下判定不值得读但 keep 留痕 以便未来 resurface"；**不等于** skip（skip 是"判过不读且不想未来回看"）。 |
| **Resurface** | 系统把某个 breadcrumb 在 {6w, 3mo, 6mo} 或 citation 触发时重新推到用户面前的事件；每次 resurface 必须附带"为什么现在又回来"上下文文本（见 §4.2）。 |
| **Seat** | 一个独立的登录账号，挂在单个 lab 实例下；v0.1 所有 seat 在同一 lab 内 read+write，admin seat 额外可 CRUD topic。 |
| **Lab** | v0.1 部署单位，一个 Postgres 实例对应一个 lab；≤ 15 seat。 |
| **Summary** | LLM 对单篇 abstract 产出的 ≤ 3 句解读；**永不超过 3 句**（红线 2 机械兜底）；持久化在 `paper_summaries` 表 per (paper_id, topic_id, prompt_version)。 |
| **paper_summaries** | R1 R2 新增表 · per-paper × per-topic × per-prompt_version 一条 summary_text · 外键指回 `llm_calls`（审计链）· IN-7 summary 的唯一权威落点 · D15 · 不与 `llm_calls` 合并（后者仅记 tokens/cost/provider 审计）。 |
| **prompt_version** | summarize / judge prompt 的版本号字符串（如 `v1.0-2026-04`）· prompt 文案改动时 bump · 用于 `paper_summaries.unique(paper_id, topic_id, prompt_version)` 唯一键，支持 reproducibility 与 export。 |
| **Skip why** | 当 action='skip' 时**必填**的一句话解释（btrim 后 ≥ 5 字符）· 三层机械兜底 DB CHECK + API validation + UI required · 红线 2 追溯承诺的代码兑现（D16）· **不**做语义质量检查（避免误杀）。 |
| **Explicit disagree** | operator 对某次 skip / breadcrumb 附加的一句 "why I disagree" 文本；**v0.1 只存不喂回**（OUT-1）。 |

---

## 开放问题（Open Questions for Operator）

以下问题未在本 spec 阶段 resolve，但明确记录等待 operator 拍板；**不得** 在不通知 operator 的情况下由下游 agent 自行决定。

| Q | 内容 | 何时需要答复 | 默认假设（在 operator 给出别的决定前生效） |
|---|---|---|---|
| **OP-Q1** | T001 spike 的**额外** exit criteria 细节：若两家 provider 都在 70%–80% 区间，是否进一步按 latency 而非成本裁决？ | T001 kickoff 之前 | 按成本裁决；若成本差 < 10%，按 operator 主观偏好 |
| **OP-Q2** | **Per-topic 权限**（PRD Q5 记录的场景：PI 不想某些 operator 看某些 topic） —— v0.1 确定不做；v0.2 是否进入 radar？ | v0.2 规划前 | v0.2 不入 roadmap，除非 60 天 dogfood 期间出现真实摩擦 |
| **OP-Q3** | **v0.1 免费承诺的时间边界**：是"永久免费"还是"v0.1 期间免费、v1.0 引入 tier"？ | v0.1 ship 时 | v0.1 期间免费 + 不承诺永久（但数据 portability 保证退出成本为零，用户无损） |
| **OP-Q4** | **Compliance 声明 / 隐私政策**：v0.1 数据全在 operator 机器上，是否仍需要一份面向 operator 的"lab 数据使用声明"？ | v0.1 ship 前 | 是，见 `compliance.md` §"Data locality & operator statement"；一页 markdown 够用 |

本 spec **主动不问** 的问题（已在 PRD 或 L4 intake 被 resolve）：LLM provider 选谁（= T001 spike）、用 Postgres 还是 SQLite（= Postgres）、要不要招外部 lab（= 不要，C10）、state shift 怎么定义（= §4.1 provisional）、resurface 规则（= §4.2）。

---

## 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · 基于 PRD v1.0 + L4 intake Q1–Q6 产出 |
| 2026-04-23 | 0.2 | R1 adversarial review（Codex）BLOCK 后修复：B1 新增 D15 + `paper_summaries` 表；B2 新增 D16 + skip_why 三层机械兜底；B3 前置 T003 schema（+2 表 +3 列 +1 CHECK）并修 7 个下游 task file_domain / depends_on 让合同闭合；updated IN-7 / C6；+4 红线 verification hooks；+3 glossary entry。H1–H10 留待 R2。 |
| 2026-04-23 | 0.2.1 | **Patch bump（澄清 only，无 scope/outcome 变更）**。R1→R2 task-decomposer 重跑识别 4 条合同漂移（记于 `OPEN-QUESTIONS-FOR-OPERATOR.md`），operator 批准闭合 Q1 + Q2 + Q4（Q3 deferred）：**Q1** T030 `grants.sql` 补齐 `paper_summaries`（webapp_user SELECT · worker_user SELECT/INSERT/UPDATE upsert）+ `export_log`（webapp_user SELECT/INSERT）；**Q2** T003 前置 5 个 auth 列（`seats.{invite_token_hash, invite_expires_at, invited_at}` + `sessions.{revoked_at, last_active_at}`）进主 schema migration，T003 hours 9→10（+1h），T006 不再写 `0002_auth_columns.sql` 改为 consume only；**Q4** T032 E2E `schema_version` 断言由 `== '1.0'` 改为 `>= '1.1'`（T023 已 bump 到 1.1 · 前向兼容未来 bump）。Prior Decisions / Outcomes / Constraints / Scope 均未变（这 5 个 auth 列原本就是 architecture.md §7 + D16 衍生要求，本次只是从 T006 的 known gotcha 层面升级到 T003 的 Outputs/Verification 明面层）。Total hours 113→114 / 115 budget。 |
| 2026-04-23 | 0.2.2 | **Patch bump（Q5 + 5 interface drift consolidation + reference/ 完整落地 + README 导航）**。(1) Q5 解决：architecture §5.1 首行 + T003 Goal / Verification 由"14 张"订正为"15 张"（llm_calls 原本就在，R1 fix 注释 off-by-one · 实际新增 2 张）。(2) 5 interface drift 闭合：**drift 1** SummaryRecord 字段改 camelCase（接口层 camelCase / DB snake_case / `src/lib/summary/persist.ts` 映射）；**drift 2** judgeRelation 签名改 per-pair（candidate×anchor 单对 verdict + discriminated union · 利 TS strict）；**drift 3** OpenAI output pricing 修正到 $15/M（2026-04 公开价 · 月度估 $10.5 → $12 · envelope $50 仍成立 · C11 注释同步更新）；**drift 4** `GET /api/today` 从 E9 移至 §7 "Future / deferred endpoints"（v0.1 不实现 · SSR Server Component 直连 DB）；**drift 5** `GET /api/invite/:token/consume` 保留（v0.1 不发邮件 · token 通过 operator 私信传递 · Caddy 禁止 query-string 日志 · v0.2 再升级到 POST-based 确认 · SEC-10 风险登记）。(3) reference/ 完整交付（schema.sql · directory-layout · api-contracts · llm-adapter-skeleton · ops-runbook · testing-strategy · error-codes-and-glossary）并写入 README.md 导航。Scope / Outcomes / Constraints 不变。 |
| 2026-04-24 | 0.3.1 | **Patch bump（R_final2 narrow review 残余 G6/G7/G8/G9 mechanical sync · 不改 scope/outcomes）**。R_final2 narrow 复核认定 G2 LLM 合同仍是 split-brain（T004/T013/changelog 已切到 adapter-内写 `llm_calls` + `llmCallId` 回传，但 `tech-stack.md §2.4` / `reference/llm-adapter-skeleton.md §2/§3/§4/§7` / `spec.md §4 D15` 与 `reference/skeletons/llm-types.ts` 仍写旧 caller-写 方案）。本次 patch 完成 4 条机械同步：(G6/G7) **D15 改写**为 "T013 只写 `paper_summaries` · adapter 已内部写 `llm_calls` 并把 `llmCallId` 通过 `SummaryRecord` 回传"；同步更新 `tech-stack.md §2.4`（SummaryRecord 加 `llmCallId: number \| null` + `requestHash` 字段 · 契约段写明 adapter 调 `recordLLMCall` 的职责）、`reference/llm-adapter-skeleton.md §2`（`SummaryRecord` 加 `llmCallId` · `JudgeRelationResult` 加 `llmCallId` · LLMProvider 方法注释改为 adapter-内写）、§3/§4 两家 adapter `summarize()` / `judgeRelation()` 实现真正调 `recordLLMCall()` 并返回 `llmCallId`、§7 audit 段标注 `recordLLMCall()` 由 adapter 调（caller 不再调）、`reference/skeletons/llm-types.ts`（SummaryRecord 加 `llmCallId` 字段）、`reference/skeletons/llm-anthropic-stub.ts` + `llm-openai-stub.ts`（TODO 块明确"必须在 return 前调 `recordLLMCall()` 并把返回 id 填入 `llmCallId`"）。(G8) `tasks/T010.md` Goal 段 "topic > 15 时 POST 返回 400" 改为 "**422 `TOO_MANY_TOPICS`**"，与 Verification + api-contracts §E6 一致。(G9) `reference/error-codes-and-glossary.md` §1.3 加 `CSRF_ORIGIN_MISMATCH` 行（HTTP 403 · `invite/consume/route.ts` · Origin header 不匹配 APP_ORIGIN · G4 H4）· 错误码总数 50 → **51**；§Glossary 段把 `email token invite` URL 模板从 `login/verify?token=...` 改为 `POST /api/invite/consume` body token（旧 GET path 注 Deprecated · G4 H4）· `schema_version` 条目改 `schemaVersion` camelCase（与 G3 export envelope 权威一致 · 旧 snake_case 注 Deprecated）。Scope / Outcomes / Constraints / Phases / Task IDs / 工时（115h）均未变。 |
| 2026-04-24 | 0.3.0 | **Minor bump（R_final BLOCK fix G1/G2/G3/G4 · 结构性变更）**。(1) **G1** `paper_summaries.summary_sentence_cap` CHECK 从 `regexp_split_to_array(…)` 换成 `regexp_matches(..., 'g')` 数终结符语义（纯中文无空格 3 句现在正确判 3、5 句正确拒；无终结符文本拒绝 · adapter `truncateTo3Sentences` defensive 追加 `。`）· TECH-8 risks.md 改写 · T003 CHECK DDL 更新 · schema.sql v0.2.2 → v0.2.3 · 7 条新 DB 约束测试 + 9 条新应用层 test case。(2) **G2** LLM 契约统一：`SummaryRecord` 全 camelCase、provider enum `anthropic|openai`（删 `claude|gpt`）、`judgeRelation` per-pair、adapter 内部写 `llm_calls`（T013 只写 `paper_summaries`）、`llm_calls` 列名权威 = `purpose`/`called_at`（删 `kind`/`created_at`）、OpenAI output $15/M（删 $10/M）· T004/T007/T013 整体重写 · §5 旧 task ID `T005=schema` / `T007=LLM adapter` / `T029=export` 全面迁移到与 `dependency-graph.mmd` 一致的新编号；§5 中的过时 LLM interface 代码样例（`summarize(paper): string`）删除，改为引用 `reference/llm-adapter-skeleton.md §2` 单一真源。(3) **G3** export envelope 单一真源 = `reference/api-contracts.md §3.11` camelCase（12 顶层 key：labs/seats/topics/papers/paperTopicScores/paperCitations/paperSummaries/briefings/actions/breadcrumbs/resurfaceEvents/fetchRuns · 排除 sessions/llmCalls/exportLog）· `schemaVersion='1.1'`（camelCase 字段名）· architecture.md §8 改为引 api-contracts 为权威 · T023 rewrite（`buildFullExport(labId)` 删 `env.LAB_ID`）· skeleton `api-export-full-route.ts` 签名改（labId 参数）· testing-strategy export 断言更新。(4) **G4** H1 T021 `trigger_type` 统一为 `timed_6wk|timed_3mo|timed_6mo|citation`（删 `6w|3mo|6mo`）· H2 T010 路径与 error code 统一（422 `TOO_MANY_TOPICS`，服务层 `src/lib/topics/service.ts`，页面 `[id]/edit/page.tsx`）· H3 T030 backup 脚本路径改 `deploy/scripts/*` + 验证命令改 `PGUSER=... PGPASSWORD=... psql` · H4 invite 消费流程由 GET path-token 改为 POST `/api/invite/consume` + body token（Caddy 不记 POST body · fragment-based link 不进服务端日志 · SEC-10 风险从 "link-preview 误触" 改为 "POST CSRF" 的缓解 SameSite=Lax + Origin 检查 + 一次性 nonce · DECISIONS-LOG drift-5 附 2026-04-24 amendment）· T006 invite 路由改 POST · H5 spec §5 task ID + 过时 interface 已随 G2 同步更新。Scope / Outcomes / Constraints 不变。 |
