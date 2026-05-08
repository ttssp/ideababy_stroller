# PRD · 007a-pA · "证词契约日志 — agent-emit friction archive (v0.1 substrate + day-14 trust prompt)"

**Version**: 1.0  (human-approved via fork)
**Created**: 2026-05-08T12:09:30Z
**Source**: discussion/007/007a-agent-emit/L3/stage-L3-scope-007a-agent-emit.md · Candidate A + GPT R2 §4 hybrid recommendation
**Approved by**: human moderator (via /fork command,synthesizer 强推 hybrid 路径)
**PRD-form**: simple
**Forked-from**: 007a-agent-emit (L3) → 007 (L1 Direction 1) → root proposal 007 "friction-tap"

---

## Problem / Context

forge 006 路径 2 playbook 在 W2 step 4 明确要求"每次 V4 retrospective skill 跑得不顺畅就 jot 一笔到 friction-log"。但当前 operator 必须经 5 步动作(切目录 / 找文件 / 算 ISO 时间戳 / append / 保存)才能记一条,且 90 秒打断了"我正在调试这个具体 task"的心流。结果:90% 的真实 friction 在当下被跳过,4 周后 retrospective 没有素材可复盘。

L1 Inspire 给出 6 个方向,operator 选 Direction 1"主语反转":把 friction-log 的写入者从 operator 反转为 Claude session 自身。L2 Explore 经两轮 cross + value-validation search(quantified-self 弃用研究 / electronic monitoring meta-analysis / error-reporting psych safety 综述 / trust calibration 研究)确认:**核心价值脊柱不是"自动记日志",而是"agent-generated review evidence with human adjudication"** —— agent 提名摩擦时刻,operator 审阅 / 反驳 / 补充 / 拥有最终叙事权。L3 Scope 在 R2 cross + 19 次 scope-reality search 后,**两侧 debater 独立收敛**到 "Candidate A 是 substrate / 脊柱;B 和 C 是 wrapper" 的同一组织原则。

本 PRD 选 **Candidate A + 1 day-14 自访谈问题 hybrid 路径**(GPT R2 §4 strong recommendation):pure substrate scope + 几乎零工程成本的 industry-aligned hedge,与 BugBug + ClawStaff 验证的 2026 dev tool 2 周 pilot baseline 对齐。

**核心 bet**:当 friction-log 的写入者是 agent 自身、entry 是可审阅证词卡、operator 用 markdown tag 保留最终叙事权,且第 14 天 trust mini-summary 强制 operator 直面 "我感觉是 relieved / watched / both" 这个问题——operator 4 周后回看 retrospective 时不再是"从零回忆哪里烦",而是"审一份现场笔录"。

## Users

**主用户(唯一用户)· Yashu Liu**:IDS 单 operator,正在跑 V4 dogfood,同时还要推进 forge 006 路径 2 的 4 周 playbook + 其他 forge 事务。每周 5-10 小时是 friction-tap 这条 fork 的所有可用时间。背景非软件开发,但是 IDS 这工具链的最高频用户。三种角色由同一个人在不同时间扮演:
- **当下角色**(每个 dogfood task 期间):"做事的人" —— 不希望任何记录动作打断 task 心流
- **每日角色**(working session 末):"审阅者" —— 在 entry 后追加 markdown tag 标 [acked]/[disputed]/[needs-context],对部分 entry 补一句人的体感
- **第 14 天角色**:"adoption-decision 者" —— 看 trust mini-summary,直面"hook 是否还该开着"

**非用户**(明确排除):
- 团队成员 / reviewer(C2 single-operator 锁,multi-reader 留 §4 extension)
- 外部 dogfood 客户 / customer(C3 free OSS / self-hosted,无 SaaS 假设)
- ADP 那边的 operator(C8 IDS first;ADP 跨仓 v0.1 不支持,4 周等待期不动 ADP)

## Core user stories

1. **As an operator, I can be 0-action while agent emits friction entries** during a dogfood session, so that capture happens without breaking my task flow. (核心机制 — 主语反转的载体表现)
2. **As an operator, I can mark any entry with `[acked]` / `[disputed]` / `[needs-context]`** by editing the markdown file directly (no state machine required), so that I retain final narrative rights over what counts as friction. (Adjudication 入口 — L2 §6 condition 1 + RL-1 不接全知监控的工具)
3. **As an operator, I can run `friction <msg>` from CLI** to append a subjective entry, so that subjective frictions agent can't see (eg "心里这流程不对劲") still enter the archive. (CLI fallback — right of reply)
4. **As an operator, I can `friction --off` / `--threshold high`** to instantly stop or tighten emit when false-positive load gets uncomfortable, so that a noisy hook doesn't force me to abandon the whole tool. (止血开关 — OQ-10 mark-don't-delete 的兜底)
5. **As an operator, on day 14, I read a trust mini-summary** showing entry counts / acked-vs-disputed ratio / hook-still-enabled state **and answer 1 self-interview question** ("After 2 weeks, do I feel relieved / watched / both?") in the same file, so that adoption evidence is captured before habit takes over.
   *(Hybrid increment vs pure Candidate A — synthesizer 强推 + GPT R2 §4 specific recommendation。industry-aligned 2 周 pilot decision baseline。工程量增 < 1h:trust report 模板多一行 prompt + operator 直接编辑文件答 1 句话。)*

## Scope IN (v0.1)

| # | Component | Scope | Rough engineering hours |
|---|---|---|---|
| 1 | `PostToolUseFailure` hook (Python) | JSON parse hook payload + 静态规则判定 + append entry 到 friction-log | 3-4h |
| 2 | 静态规则集 | 白名单(`Bash` / `Edit` / 自定义 hook block 失败)+ 黑名单(`--off` 标志 + task description 含 `[debugging-friction-detection]` 关键字 skip) | 含上 |
| 3 | friction-log 硬编码路径 | `docs/dogfood/v4-friction-log.md`,启动时若无目录则创建 | 0.5h |
| 4 | Entry 格式 | `<ISO> [agent-emit] [confidence:H\|M\|L] [private-to-operator] · <tool> exit <code> · "<stderr-200chars>" · task: <desc>` —— privacy 标记 visible 在 entry 字段(不是隐藏假设) | 含上 |
| 5 | Adjudication tag 约定 + 文档 | `[acked]` / `[disputed]` / `[needs-context]` 一行追加(operator 用记事本即可),grep 统计;无 state machine | 1h |
| 6 | `friction <msg>` CLI(Python single-file) | append 一条 subjective entry,无依赖,stdlib only | 1-2h |
| 7 | `friction --off` / `--on` / `--threshold low\|medium\|high` | 一行止血 + 阈值切换,持久化到 `~/.config/friction-tap/state.json`(只此一个 config 文件) | 1-2h |
| 8 | Day-14 trust mini-summary 脚本 | grep 统计 entry 数 / 三种 tag 比例 / hook 是否仍 enabled,输出 markdown 到 `docs/dogfood/v4-trust-w2.md` | 2-3h |
| 9 | **Hybrid · trust mini-summary 多 1 行 prompt** | 模板末尾追加 "**Self-interview**: After 2 weeks, do you feel relieved / watched / both? (1 句话)" + operator 在文件直接补答 plain text | 0.5-1h |
| 10 | 测试 + commit + 文档(README + 安装说明) | 单元测试 hook 静态规则 + 集成测试 entry 写入 + 文档 | 3-4h |

**总计 ≈ 11.5-16.5h**(在 10-20h 总预算内,Confidence H,1-1.5 周 ship 可信)

## Scope OUT (explicit non-goals)

- **State machine for adjudication**(simplified — markdown tag 即可,operator 已 explicit 同意)
- **Skill placeholder 检测 / 其他 lifecycle hook**(C7 PostToolUseFailure only;v0.2+ 候选)
- **LLM-judge friction signal 判定**(留 v0.2 — 静态规则覆盖 80% 真实信号,LLM 是 disputed 率优化,且工程量隐藏成本高)
- **跨仓 ship**(C8 IDS first — ADP 4 周等待期不动 → v0.2 加可配路径时 ADP 接入是 free 的)
- **可配 log 路径**(留 v0.2 — v0.1 hardcoded 是 privacy promise 工具,可配反而引入 default-shared 风险)
- **Frontend / dashboard / 可视化**(RL-4 不与 enterprise observability 竞争)
- **团队共享 / multi-reader format / cloud sync / cross-repo aggregation**(C2 single-operator + RL-3 不接合作上传)
- **自动开 issue / PR / fix**(RL-2 不接追责文化)
- **完整 2 周 pilot 协议**(留 v0.2 candidate B —— 本 v0.1 只取 day-14 1 题 hedge)
- **完整 weekly review ritual**(留 v0.2 candidate C —— scope-reality search 警告 thin prompt 是 underbuilt 风险)
- **跨 dogfood 周期聚合 / shared immune memory**(留 v1.0+ 远 vision)

## Success — observable outcomes

- **O1 · Capture 工作**:第 14 天 friction-log 累计 ≥ 8 条 agent-emit entry(证明 hook 在工作)
- **O2 · Trust 在线**:第 14 天 trust mini-summary 显示 `[acked]` 比例 ≥ 50% 且 `[disputed]` ≤ 20%(operator 没频繁觉得 entry 不准)
- **O3 · Adoption signal**:第 14 天 hook 仍 enabled(operator 没在 day 14 前主动 `friction --off`) — quantified-self 弃用研究的反向 metric
- **O4 · Review 体验**:operator 能在 10 分钟内审阅 20 条 entry(GPT 给的可测试目标 + grep-friendly format 的产物)
- **O5 · 主观确认**:operator 能指出至少 3 条改善 retrospective recall 的 entry(主观但可记录;Yashu 自报)
- **O6 · Hybrid · adoption-decision answered**:第 14 天 self-interview 1 题答完,operator 在 mini-summary 文件直接写 1 句话答案("relieved" / "watched" / "both" + 一句 why)

## Real-world constraints

| # | Constraint | Source |
|---|---|---|
| C1 | Time: 1-2 周 ship,5-10 hr/week,**总预算 12-23 小时**(R1 → R2 修订后接受 12.5% overshoot,operator 2026-05-08 显式 sign-off — 见 PRD 末尾 Revision log) | L3R0 intake Block 1 Q1+Q2 + R1 review SCH-1 / R2 sign-off |
| C2 | Audience: single operator dogfood,无 multi-reader 假设 | L3R0 default + L2 §6 condition 4 |
| C3 | Business: free OSS / self-hosted,无 SaaS / 付费 | L3R0 default + RL-4 |
| C4 | Platform: Claude Code `PostToolUseFailure` hook + Python CLI(macOS) | L3R0 default + L2 §6 prior art search GREEN |
| C5 | 红线 4 条全 hard:RL-1 不接全知监控 / RL-2 不接追责文化 / RL-3 不接合作上传 / RL-4 不与 enterprise observability 竞争 | L3R0 intake Q5 |
| C6 | v0.1 必含 4 condition:cond-1 审阅入口 / cond-2 entry tone 含 uncertainty / cond-3 week-2 trust monitoring / cond-4 default single-operator + private | L2 §6 + L3R0 priorities |
| C7 | Event scope: 仅 `PostToolUseFailure`(其他 hook 留 v0.2+) | L3R0 intake Q4 |
| C8 | Ship target: IDS first,4 周等待期不动 ADP | L3R0 intake Q3 |
| C9 | friction-tap 不能拼动 operator 太多时间 | L3R0 catch-all |
| C10 | Privacy as promise(visible commitment, not hidden assumption) | GPT L3R2 §1 push back |
| C11 | Precision > recall(false positive 的成本是 trust loss > miss 的成本) | L2 §6 + Opus L3R2 UX 原则 |

## UX principles (tradeoff stances)

- **Trust calibration > Speed to ship**(L3R0 priority #1)— entry tone 必须含 confidence(L|M|H),不假装权威;不写 "this is critical" / "建议你做"
- **Differentiation > Broad appeal**(L3R0 priority #2)— 不跟 enterprise observability 比;default single-operator + default private 是产品 promise 的一部分
- **Trust monitoring on day 14**(L3R0 priority #3)— self-interview 1 题 hedge 是必须 deliverable,不是 polish
- **Speed to ship**(L3R0 priority #4)— 1-2 周必须 ship,但前 3 项不让步
- **Simplicity > Cleverness**:markdown tag 优于 state machine,记事本就能编辑
- **Fast off-switch > Sophisticated tuning**:`friction --off` 一行止血,胜过精细阈值参数
- **Agent 是 witness 不是 judge**:entry 写"我观察到 X · 我推测 Y · 置信 L|M|H";不替 operator 解释情绪 / 下结论
- **Mark, don't delete**(OQ-10 决议):误报 entry 用 `[disputed]` tag 标记 + 计数,不删除 → 保留 adoption signal

## Biggest product risk

**File too trustworthy, weakly opened**(GPT R1 原话改写)。即使 entry 格式做对、标记体系 fair、hook 工作正常,如果 operator 4 周后实际不主动打开 friction-log,产品价值就死在文件里。这是 substrate-only scope 的固有风险——它把"weekly opening cadence"赌给 operator 自律,而不是产品强制。

**Mitigation**:
1. 第 14 天 trust mini-summary 是 operator 必看的产物(写到 IDS 工作流自然路径 `docs/dogfood/v4-trust-w2.md`,任何 retrospective workflow 经过这个目录)
2. Hybrid 增量(Story 5 的 self-interview 1 题)强制 operator 在 day 14 至少打开一次文件
3. 第 14 天 + day 28 / day 42 trust report 演化(留 v0.2)给 cadence 加更多 forcing function

**Secondary risk**:静态规则误报率超 operator 容忍。Bash tool 失败 ≠ 一定是 friction(operator 故意 `set -e` 测试某条命令时,hook 会把它误判为 friction)。**Mitigation**:`--off` / `--threshold` 一行止血 + `[disputed]` 标记保留信号 + day 14 self-interview 强制直面这个数字。

## Open questions for L4 / Operator

(Any ❓ items from L3 that survived unresolved — block build if critical.)

- **OQ-C(L3 仍开)**:第 14 天 trust mini-summary 怎么观测 "hook 是否仍 enabled"?
  - **Option 1**:observational metric — 脚本检查 `~/.config/friction-tap/state.json` 中 enabled flag + 检查最近 24h 是否有 agent-emit entry(双指标)
  - **Option 2**:operator self-report — trust report 多挂一行 "Is the hook still on? (yes/no)" 让 operator 自答
  - **Recommendation**:Option 1(observational),自动化更可靠,与 cond-3 trust monitoring 自动化对齐。Option 2 留给 v0.2 (与 weekly self-report 一起增强)
  - **L4 决策点**:这条由 spec-writer 在 spec.md §"Verification" 锁定;若 spec-writer 选 Option 2,operator review 时需 push back

- **OQ-D(新)**:`friction <msg>` CLI 在仓库内 vs 仓库外 的行为?
  - **Option 1**:cwd 不在 git 仓库 → 直接报错让 operator 显式 `friction -f <path>`
  - **Option 2**:cwd 不在 git 仓库 → fallback 到 `~/.claude/global-friction-log.md`
  - **Recommendation**:Option 1(显式优于隐式;privacy 不能 fallback 到 home dir 隐藏路径)
  - **来源**:proposal 007 §"还在困扰我的问题" 已提此问题,L1-L3 未决议

- **OQ-E(新)**:静态规则的白名单 v0.1 包含哪些 tool?
  - **候选**:`Bash` / `Edit` / `Write` 失败 + Claude Code lifecycle hook block 信号
  - **L4 决策点**:spec-writer 决定 + Codex review 推 hardening

> **Open questions still relevant from earlier rounds**(L2 § 7 nice-to-have tier · 留作 user research,不阻塞 L4 build):
> - OQ-7 4 周后信任哪类 entry / OQ-8 agent witness 语气 / OQ-11 价值是减少漏记 vs witness 责任 — 这些通过 day-14 self-interview 逐步收集 evidence

---

## PRD Source

This PRD was auto-generated from L3 fork(simple form,via /fork command + synthesizer hybrid recommendation)。Contents derived from approved L3 candidate A + GPT R2 §4 hybrid。For full context (why this cut vs siblings, scope-reality verdict, comparison matrix), see:

- L3 menu: `discussion/007/007a-agent-emit/L3/stage-L3-scope-007a-agent-emit.md`
- L2 unpack: `discussion/007/007a-agent-emit/L2/stage-L2-explore-007a-agent-emit.md`
- L1 menu: `discussion/007/L1/stage-L1-inspire.md`
- FORK-ORIGIN.md (本目录,记 fork rationale)

This PRD is **the source of truth for L4** (spec-writer)。Changes to PRD require explicit human approval — never auto-revised by L4 agents。

---

## Revision log

### 2026-05-08 · v1.0 → v1.1 · C1 budget 接受 12.5% overshoot

**Trigger**: L4 R1 adversarial review verdict = BLOCK,3 blockers + 6 high concerns。spec-writer R2 修订(2026-05-08T13:30 ±)落地全部修复后,task DAG 重新核算 sum = **22.5h**(原 spec.md 内估 11.5-16.5h),超出 PRD v1.0 C1 hard 上限 20h 共 12.5%。

**Operator decision**(2026-05-08,本人 Yashu Liu 显式 sign-off):
**接受 22.5h overshoot,不 cut R1 修订项**。理由:
1. R1 review 命中的是产品脊柱 — B1 threshold filter / B2 verification commands missing / B3 O3 不忠 PRD 都直接打 trust calibration 这条 priority #1。cut 任何一条 = 让 v0.1 在最 critical risk 上 ship-with-bug
2. v0.1 的核心赌注就是"trust"做对,12.5% schedule overshoot 是这个赌注的必要成本
3. wall-clock 上 — 假设 operator 跑 10 hr/week 上限 → 22.5h 在 2.25 周完成,仍在 PRD"1-2 周"语义边界(取上限);如跑 5 hr/week 下限 → 4.5 周,超过 PRD "1-2 周",但 operator 在 catch-all 已表达"varies",上限 10 hr/week 是 operator 真实可投入

**改动**:
- C1 表行 — 从"总预算 10-20 小时"改为"总预算 12-23 小时"(给 R3 / R4 adversarial review 留 0.5h buffer)
- 余下 PRD 内容(用户 / outcome / scope / red lines)**不变**,仅 C1 budget 单维度调整

**Risks 同步**:spec.md §5 + risks.md SCH-1 已显式记录 schedule overshoot;若 R2 review 再次因 schedule risk BLOCK,operator 需考虑 cut scope(把 D19 redact / schema-error counter 推到 v0.2)

**Source for trace**:
- R1 review:`.codex-outbox/queues/007a-pA/20260508T124631-007a-pA-L4-adversarial-r1.md`
- R2 修订报告:本会话 spec-writer(agent-id `a3ab57d009e6bafde`)R2 fix 完整报告
