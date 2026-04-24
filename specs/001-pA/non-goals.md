# Non-Goals · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**原则**：**每条都是"有意识 descope，不是遗忘"**。一份没有 non-goals 的 spec 会让 agent 默认扩 scope；本清单的每条都是未来 spec-writer / builder / reviewer 可以引用的"它被删掉了，不要再加"的硬证据。

本文件分三类：(A) **直接继承自 PRD Scope OUT**（OUT-1..OUT-11）；(B) **工程层 non-goals**（PRD 没说但明显会被 agent 添加回来的）；(C) **未来路径上的 non-goals**（v0.2+ 才可能讨论的 feature，本 v0.1 绝不提前做）。

---

## A. 直接继承自 PRD Scope OUT

### NG-A1 · 完整 Taste Agent 闭环
**PRD**: OUT-1
**本 v0.1 具体边界**：v0.1 收集 operator 对 skip / breadcrumb 的 "why I disagree" 文本（≤ 280 字符），**仅存入 `actions.why` 字段，不反向影响 briefing ranking / state-shift judgment / summary 生成**。
**为什么看起来诱人**：只要把 `why` 字段喂回 LLM prompt，就是一个 closed-loop taste agent，感觉差 50 行代码。
**为什么 v0.1 不做**：
1. Hybrid taste agent 的 cold-start 期（前 4 周）如果 operator 写 disagree 频率太低（DOGFOOD-3），closed loop 没数据可学，学 wrong thing 反而污染 briefing
2. L2 §6 condition 3 明确要 hybrid，但 v0.1 5 周预算无法 afford 设计 + 验证 + 调参
3. 这是 Candidate A → B 升级的 40–60% 可复用部分中的一部分，**刻意留给 B**
**何时可能重启**：60 天验证成功后 fork 001-pB 时。

### NG-A2 · Topology Graph / Topic 关系图（主视图）
**PRD**: OUT-2
**本 v0.1 具体边界**：UI 中**不渲染** graph；后端**不预计算** paper-to-paper 共引 / 共被引关系；schema 中**不含** topic 关系表；不引入 graph visualization 库（d3 / cytoscape / sigma）。
**为什么诱人**：L2 场景 D（90 秒 topology 查询）确实有吸引力；看起来 "加一个页面就行"。
**为什么 v0.1 不做**：
1. digest-first 是 L2 §6 condition 2 明确承诺；topology 做成主视图会稀释首页价值
2. R2 搜索（emergency physicians 调查 + r/ML）支持 digest-first、topology 降为 second-order
3. graph view 单独有用户但**赢家未定**（ResearchRabbit / Connected Papers / Litmaps 都没占稳），v0.1 不下注
**何时可能重启**：B 候选的"topology explainer（二级 view）"—— 不是首页入口。

### NG-A3 · Lab Shared Belief Ledger / Stance History
**PRD**: OUT-3
**本 v0.1 具体边界**：**无 `stances` / `beliefs` / `positions` 表**；UI **无任何** "lab 立场" "stance update" 相关视图；operator 和 PI 的判断完全通过 4-action 体现，不写立场文本。
**为什么诱人**：B 候选的核心叙事；让 lab 的 "研究品味沉淀" 具象化。
**为什么 v0.1 不做**：
1. 属 Candidate B 范畴，不是 A 范畴
2. 立场 ledger 的维护成本（operator 每周 > 20 分钟）是 B 假设的前提，A 明确不假设
3. 引入后 briefing 的 "state shift" 语义会被"stance 变化" 争抢主舞台，破坏 A 的单一焦点
**何时可能重启**：fork 001-pB。

### NG-A4 · Paper 二次分析 / Novelty 自动评分 / 跨 Paper 对比
**PRD**: OUT-4
**本 v0.1 具体边界**：LLM **不做跨 paper 对比**（state-shift 判定除外，因那是 anchor-中心 relation 判定，不是通用对比）；**不生成** novelty 分数 / impact 预测 / ranking 列表；**不引入** embedding / vector similarity。
**为什么诱人**：Elicit / alphaXiv / ResearchRabbit 都在做，看起来是"进步"。
**为什么 v0.1 不做**：
1. 守红线 2："委托 triage ≠ 替代阅读"；novelty 自动评分是典型的 "把品味外包给 LLM"，是产品死亡路径
2. Elicit 88 feature / 125 周的迭代节奏 solo 20h/周 跟不上（L3 stage doc candidate C biggest risk）
3. 破坏差异化：一旦做这一项，产品立刻变成 "Elicit 但更差"
**何时可能重启**：不重启；即便 v0.2 也只做 per-topic scoring，不做 per-paper novelty。

### NG-A5 · Mobile Native / CLI / PWA
**PRD**: OUT-5
**本 v0.1 具体边界**：仅支持 desktop Web · 最小 viewport 1024×768 · **不做** responsive design for mobile · **不做** PWA manifest · **不做** CLI / REST API 给第三方消费。
**为什么诱人**：PI 在机场 / 通勤看手机时想扫 briefing；PWA 只需加个 manifest。
**为什么 v0.1 不做**：
1. PRD 场景（PI 8:00 ritual 在办公室 / 家里 desktop）不需要 mobile
2. responsive 设计会多吃 10–15h（5 周预算的 15%）
3. PWA 拆出去是 Candidate C 的差异化维度，保留给 C；A 选 desktop-only 是刻意的
**何时可能重启**：用户实际反馈 mobile 需求 > 3 次/月后。

### NG-A6 · PDF 全文解析
**PRD**: OUT-6
**本 v0.1 具体边界**：**仅使用** arXiv API 返回的 title + abstract + authors + categories + 可取到的 reference list；**不下载** PDF；**不跑** OCR / PDF parser（pdfjs / pdfminer）；LLM prompt 只包含 title + abstract。
**为什么诱人**：abstract 有时候信息不足，拿到全文 LLM summary 更准确。
**为什么 v0.1 不做**：
1. PDF parse 的 engineering cost（下载 / OCR / chunk / 对齐 metadata）占 10+h
2. 全文喂 LLM 的 token 成本爆炸（300 token abstract → 10000 token full paper → C11 月度 $50 envelope 3 倍超）
3. 红线 2 的精神：v0.1 是委托 triage，用 abstract 判 shift 够用
**何时可能重启**：v0.2 若 operator 愿意加 GPU + 本地模型（避免 token 成本）。

### NG-A7 · Onboarding-Focused View / Carol 场景
**PRD**: OUT-7
**本 v0.1 具体边界**：**不做** guided tour · 不做 "新 seat 第一次登录" 特殊视图 · 不做 topic 介绍页（新人点 topic 看到的就是 briefing 历史）。
**为什么诱人**：L2 场景 C 生动；3 天 onboarding 是很诱人的 demo。
**为什么 v0.1 不做**：
1. v0.1 ≤ 3 seat，新人少；PRD 明确 Carol 场景降级 v0.2
2. onboarding 假设产品已成熟稳定，A 还在 60 天验证期，给新人用会 confuse
**何时可能重启**：v0.2 或单独拆成 Lab-brain-for-onboarding 独立产品。

### NG-A8 · 公开打分 / 社区 Review / 排行榜
**PRD**: OUT-8（红线 3）
**本 v0.1 具体边界**：**零公开 endpoint**；所有 route 必经 auth middleware；**无** 公开 paper rating / 社区评论 / 最热 paper 榜 / lab 对比页；任何页面都要求 lab seat 登入。
**为什么诱人**：社区化带流量 —— 但这是 Paperstars 失败模式。
**为什么 v0.1 不做**：
1. 硬红线 3
2. 一旦公开，lab 的 "honest 4-action" 变成 "performative rating"，产品内核崩
3. 技术上 CI 有守门人：`rg "public" src/app/api/` 出现即 fail
**何时可能重启**：从不（这是永久红线，不是 v0.2 可解锁）。

### NG-A9 · Billing / Payment
**PRD**: OUT-9
**本 v0.1 具体边界**：**不集成** Stripe / Lemon Squeezy / PayPal 任何 billing SDK；**无** 付费 tier / plan 差异 / 账单页；auth 保留 seat 角色（admin / member），但不记录付费状态。
**为什么诱人**：现在加 "pay once" 比未来重构 schema 简单。
**为什么 v0.1 不做**：
1. v0.1 先免费（C3）
2. 付费 SDK 合规成本（PCI / 税务 / 发票）不值 5 周预算
3. 数据 portability（C8）保证用户随时退出，v0.2 引入付费 tier 只需加 `plans` 表，不 break 现有 schema
**何时可能重启**：v1.0 正式商业化。

### NG-A10 · Per-Topic 可见性分层 / 细粒度权限
**PRD**: OUT-10
**本 v0.1 具体边界**：所有 seat 对所有 topic 一视同仁（admin 多 CRUD topic 权限，member 仅读+标注）；schema **不预留** per-topic ACL 列；URL 不根据 seat 过滤 topic 列表。
**为什么诱人**：某些 lab 内 PI 不想让特定 operator 看到 "确信感低" 的新 topic。
**为什么 v0.1 不做**：
1. PRD Open Q5 明确 v0.1 不做，v0.2 只有真实摩擦发生时才升级
2. 复杂化 schema 会 ripple 到所有 query
3. ≤ 15 seat 的小 lab 默认"全员可见"是 L2 §6 的 lab-unit 假设
**何时可能重启**：60 天 dogfood 中出现 ≥ 2 次真实权限摩擦报告。

### NG-A11 · 跨 Lab Federation / 公开 Radar
**PRD**: OUT-11
**本 v0.1 具体边界**：**单 lab 部署单 Postgres**；**无** cross-lab 数据交换 endpoint；**无** "公开 radar / 半公开 frontier" 概念；任何跨 lab 分享需走 JSON export 人工传递。
**为什么诱人**：L2 §4 "Fed-Lab brain" 叙事诱人；network effect 快速获得。
**为什么 v0.1 不做**：
1. 彻底破坏 lab-private 假设（红线 3 精神延伸）
2. federation 需要中心 registry + 信任模型 + 合规审计，solo 20h/周 × 100h 预算万不可能
**何时可能重启**：2028 年 academia infra 成熟后独立产品。

---

## B. 工程层 non-goals（PRD 没明说但 agent 会默认加回）

### NG-B1 · 高可用 / 多实例 / 负载均衡
**本 v0.1 具体边界**：单 VPS · 单 Next 进程 · 单 Postgres · 无 replica · 无 auto-scaling · 无 load balancer。
**为什么诱人**："可扩展" 听起来专业；agent 会默认加 Docker Compose / k8s。
**为什么 v0.1 不做**：
1. ≤ 15 seat 不需要
2. 多实例把 cron 唯一性问题暴露（两个实例同时跑 06:00 worker → 成本 × 2）
3. C13（solo operator 可持续性）：每多一个 moving part 多一个 on-call 点
**何时可能重启**：V1.0 且同时 lab > 3 个时。

### NG-B2 · 实时 / WebSocket / SSE 推送
**本 v0.1 具体边界**：所有交互 request-response · 无长连接 · 无 push notification · 无 realtime paper alert。
**为什么诱人**："新 paper 立刻提醒" 是产品经理直觉；加个 SSE route 感觉不贵。
**为什么 v0.1 不做**：
1. PRD 场景是 08:00 ritual，不是"刷新等新 paper"
2. 实时会打破 "precompute briefing" 的成本优势（ADR-2）
3. 长连接让部署拓扑变复杂（Caddy / Next / Postgres 都要配置 keepalive）
**何时可能重启**：不重启；即便 v1.0 也不做 realtime，仅做"定时 hourly summary"。

### NG-B3 · 完整的 observability 栈（Grafana / Prometheus / Sentry / DataDog）
**本 v0.1 具体边界**：仅用 Postgres 表（`fetch_runs` / `llm_calls`）+ systemd journal + 邮件告警；**不安装** 任何监控服务。
**为什么诱人**："生产级 observability" 看起来必须。
**为什么 v0.1 不做**：
1. SLA §1.5 明确 solo operator 最小集
2. 多一个服务多一个 on-call
3. 当用户 = operator 时，operator 自己就是"监控"
**何时可能重启**：V1.0 商业化时。

### NG-B4 · 完整的用户邀请 / 权限管理 UI
**本 v0.1 具体边界**：admin 通过一个极简页面（表格 + 按钮）发 invite token；**无** 权限矩阵 UI、**无** role 编辑页、**无** seat 暂停 / 禁用 UI（admin 可用 SQL 直接 update）。
**为什么诱人**：Gmail-like admin 面板看起来专业。
**为什么 v0.1 不做**：
1. ≤ 15 seat，lifetime 不超过一次邀请；UI 折腾 ROI 极低
2. 红线 1 精神：不偏离核心价值
**何时可能重启**：≥ 10 seat 时或 v1.0 商业化。

### NG-B5 · i18n / 多语言 UI
**本 v0.1 具体边界**：UI 文案**全部中文 OR 全部英文 二选一，不做 i18n 框架**；arXiv 论文本身自带语言（多为英文），不翻译。
**为什么诱人**：可能有英文 lab 成员。
**为什么 v0.1 不做**：
1. ≤ 3 seat 同一 lab，语言统一
2. i18n 框架 ramp 成本 > 10h
**何时可能重启**：V1.0 时。

### NG-B6 · 文件上传 / 用户自定义 paper 导入
**本 v0.1 具体边界**：论文来源**仅 arXiv API**；不允许用户手动 PDF 上传 / DOI 导入 / URL 粘贴。
**为什么诱人**：看到一篇非 arXiv 好 paper，想加进来。
**为什么 v0.1 不做**：
1. OUT-6（无 PDF 解析）延伸
2. 单一数据源让 pipeline 简单
3. 守红线 1：不扩成通用 paper 管理器
**何时可能重启**：v0.2 加 RSS 源（lab blog）时。

### NG-B7 · Email digest（把 briefing 推送到邮箱）
**本 v0.1 具体边界**：briefing 仅 Web 展示；**不发** daily email digest。
**为什么诱人**：Readwise / newsletter 都这么做；用户不登网站也能看。
**为什么 v0.1 不做**：
1. PRD O1 要求 "日活 ≥ 25/30"（登入行为，不是打开邮件）
2. Email digest 会诱导 user 把本产品当 newsletter 读（biggest product risk）
3. nodemailer + HTML template 维护成本 > 5h
**何时可能重启**：V1.0 商业化时（可选 plan）。

### NG-B8 · 完整的 audit log / 操作历史
**本 v0.1 具体边界**：审计仅限 `fetch_runs` + `llm_calls` + session 记录；**不记录** 每个 UI 操作的 audit trail；`actions` 表本身是用户行为记录，不是 audit log。
**为什么诱人**：合规 ready。
**为什么 v0.1 不做**：
1. LEG-1 已说明 v0.1 不是正式合规对象
2. ≤ 3 seat 且 operator = admin，audit 无意义
**何时可能重启**：V1.0 商业化 & 有外部 lab 成员时。

---

## C. 未来路径上的 non-goals（v0.2+ 才讨论）

### NG-C1 · SQLite fallback 作为主存储选项
**L4 intake Q1**：v0.1 主存储 = Postgres 16。SQLite **推到 v0.2** 考虑。
**为什么诱人**：SQLite 零运维，solo operator 似乎更省事。
**为什么 v0.1 不做**：
1. 并发支持虽然 sufficient (WAL mode)，但 Drizzle 对 SQLite 的 migration 工具链不如 Postgres 成熟
2. 未来 pgvector / FTS 都需要 Postgres
3. 一份 spec 锚定单一 DB 减少 if/else

### NG-C2 · 本地 LLM（Llama 4 / Qwen 3 等）作为 provider
见 `tech-stack.md` §2.3。**不在 T001 spike 中评估**；v0.2 可加 `LocalLLMAdapter`。

### NG-C3 · Per-seat taste agent（即 OUT-1 的 hybrid 版）
**Candidate B 的核心**；60 天验证后 fork 001-pB 启动。

### NG-C4 · Cross-lab 对比 / Field-wide radar
L2 §4 "Fed-Lab brain" 范畴。**2028 年前不讨论**。

### NG-C5 · 自动邮件摘要 / 通知
见 NG-B7；v1.0 可能重启。

### NG-C6 · 移动端（Web + PWA）
**Candidate C 的差异化维度**。如果 A 验证成功后 operator 决定走 C 路径（可能性很低），再单独 fork。

---

## 守门规则（给下游 agent / reviewer）

1. **Adversarial reviewer**（Codex）发现 spec 或 task 中有本清单任一 NG-* 实现代码 → 立即 block
2. **Task-decomposer** 不得产出任何 T-file 目标在本清单内
3. **Parallel-builder** 代码中出现本清单提到的库 / 概念 / endpoint → PR 打回
4. **operator** 若真的想 un-descope 某项，必须先更新 PRD → 再更新 spec → 再更新本文件；不走这条路径直接加 feature = 违反 spec-writer 约束

---

## 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · A 类 11 条全继承 PRD · B 类 8 条工程 non-goals · C 类 6 条未来路径 |
