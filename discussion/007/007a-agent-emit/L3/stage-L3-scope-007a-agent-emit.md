# L3 Scope Menu · 007a-agent-emit · "Agent 自录摩擦 — agent 当 witness, operator 当审阅者"

**Generated**: 2026-05-08T11:00:00Z
**Source**: L2 explore report + L3R0 intake + 2 rounds of debate (Opus 4.7 Max + GPT-5.5 xhigh)
**Rounds completed**: L3R1 (both, no search) · L3R2 (both, with search)
**Searches run**: 19 scope-reality queries total (Opus 3 / GPT 16 query strings, 7 sources cited)
**Moderator injections honored**: none(本 fork 全程无 moderator notes)

## How to read this menu

这是 L3 对 `007a-agent-emit` 的输出:针对 v0.1 的候选 PRD 菜单。每条都是 **peer**——在 operator stated constraints 下的不同合法切法。你 fork 一条(或多条)进 PRD branch 作为 L4 输入:

    /fork 007a-agent-emit from-L3 candidate-X as 007a-agent-emit-<prd-id>

Fork 后跑 `/plan-start 007a-agent-emit-<prd-id>` 启动 L4 (spec + build)。

**这次 menu 的特点**:两位 debater 在 L3R2 **独立收敛到同一个组织原则** ——
> "Candidate A 是 substrate (脊柱);B 和 C 是 A 之上的 wrapper,不是 A 的 substitute。"

这个收敛在 menu 里是组织主轴,不是被压缩成"都 recommend A"的注脚。下面三条候选保持 peer 形态,但它们的 product spine 关系不是平行,而是**substrate vs wrapper**——这点直接影响 fork 决策。

---

## Intake recap — what we honored

### Hard constraints (✅) — respected in all candidates
- **C1 · Time**: 1-2 周 ship v0.1,5-10 hr/week,**总预算 10-20 小时**(含 L4 spec / build / test / commit)
- **C2 · Audience**: Single operator dogfood 自用(Yashu),无 multi-reader 假设
- **C3 · Business**: Free OSS / self-hosted,无 SaaS / 付费 tier
- **C4 · Platform**: Claude Code `PostToolUseFailure` hook + Python CLI fallback (macOS)
- **C5 · 红线 4 条** (全 hard,见下文 Red lines 节)
- **C6 · v0.1 必含 4 条 condition**:
  - cond-1: 人类审阅入口(simplified — markdown tag,不做 state machine)
  - cond-2: entry tone 暴露 uncertainty + reason
  - cond-3: week-2 trust monitoring metric (条数 / 同意 / 不同意 / hook 是否还开)
  - cond-4: default single operator + default private
- **C7 · Event scope**: 仅 `PostToolUseFailure`(其他 lifecycle hook 留 v0.2+)
- **C8 · Ship target**: IDS first(跳过 ADP V4 4 周等待期)
- **C9 · Time budget cap**: friction-tap 不能拼动 operator 太多时间(catch-all 反向压力)

### Soft preferences (🤔) — operator priority order
1. **Trust calibration** (cond-2) — 最高优先级
2. **Differentiation** (cond-4) — 不与 enterprise observability 正面比
3. **Trust monitoring** (cond-3) — week-2 反馈信号必须可见
4. **Speed to ship** — 1-2 周必须 ship,但前 3 项不让步

### Red lines — never violated
- **RL-1 · 不接全知监控**:agent 是 witness,不是管理者 / 裁判;不解释情绪
- **RL-2 · 不接追责文化**:log 不能被当问责材料;v0.1 不做"自动开 issue / PR / fix"
- **RL-3 · 不接合作上传**:log default private to operator;不能 default-shared;不上传云
- **RL-4 · 不与 enterprise observability 竞争**:不跟 Langfuse / Helicone / Phoenix / Pydantic Logfire / Datadog LLM 正面比;无 SaaS 特性

### ❓ items resolved by this menu (how each candidate decided)

| ❓ item | Candidate A 决议 | Candidate B 决议 | Candidate C 决议 |
|---|---|---|---|
| **OQ-2** friction signal 判定规则 | **静态规则** (基于 hook payload + 白/黑名单) | 同 A | 同 A |
| **OQ-4** log 路径硬编码 vs 可配 | **硬编码** `docs/dogfood/v4-friction-log.md` (privacy promise 工具) | 同 A | 同 A |
| **OQ-10** 误报 5 条如何处理 | **mark, don't delete** ([disputed] tag + 计数到 trust report) | 同 A,且作为 self-interview 输入 | 同 A,且作为 weekly review 评估材料 |

> 三条 ❓ 在三条 candidate 中**决议一致** —— 这反映了 substrate vs wrapper 的关系:
> A 决定的是 substrate 设计,B/C 在 A 之上加封装,不重新决定 substrate 决策。

### ❓ items STILL OPEN for you (fork 时回答)

- **OQ-A · 选 pure A 还是 A + week-2 自访谈问题混合体?** synthesizer 最强推荐是后者(GPT R2 §4 specific recommendation:"choose A as v0.1, but include one B-compatible week-2 question")。**这是这次 menu 唯一悬而未决的关键决策**。
- **OQ-B · 如果 fork C, ritual prompt 的具体措辞**(weekly pattern sentence 怎么提问? top-3 怎么选?)— 仅在 fork C 时相关。
- **OQ-C · 如何观测 "hook 是否仍 enabled"** — observational metric (脚本检查) vs operator self-report (周末自填一行)。这关系到 cond-3 trust monitoring 的可信度,A/B/C 都受影响。

---

## The key tradeoff axis

**两位 debater 在 R2 独立收敛到同一个轴的两种 framing,合成一句**:

> v0.1 的工程脊柱(spine)只有一条—— Candidate A 的"私有 IDS friction-log + agent 提名 + adjudication tag + week-2 mini-summary"是 substrate。**真正的决策不是"A 还是 B 还是 C",而是"v0.1 在 A 之上加多少 wrapper"**:不加 = pure A(H confidence,1-1.5 周),加一个 day-14 自访谈问题 = A+B-lite(M-H confidence,1.5 周),加完整 2 周 pilot 协议 = full B(M confidence,1.5-2 周),加完整 weekly ritual = full C(M-L confidence,1.5-2 周,且面临 ritual prompt 调优的不可压成本)。

**Opus R2 §3 的原话(意译)**:三条 candidate 都合法,但应按 "trust surface placement" 维度重组——A 把 trust 放在 entry 格式 + adjudication;B 把 trust 放在 2 周 adoption decision;C 把 trust 放在 weekly opening cadence。**operator 不能选"都做"**,因为工程量爆炸 (A+B+C ≈ 25-30h,显著超 timeline)。

**GPT R2 §2 的原话(意译)**:scope-reality search 显示 "A is closest to real v0.1 practice. **B is validated as an adoption wrapper around A, not a substitute. C has precedent, but likely needs too much scaffolding**." 这是 search verdict,不是直觉。

**两侧独立同口径** —— 这种收敛在 L3 是稀有信号。

---

## Candidate PRDs

### Candidate A · "证词契约日志"

**Suggested fork id**: `007a-agent-emit-pA-substrate`
**Sources**: Opus R1 Candidate A (refined R2) + GPT R1 Candidate A (refined R2) — **两侧 R1 各自独立提出且 R2 完全收敛**

**v0.1 in one paragraph**:
私有 IDS friction-log 作为 v0.1 中心。每条 agent entry = 可审阅证词卡(timestamp / tool / exit code / agent reason / confidence L|M|H / 200-char stderr 截断 / task description)。`PostToolUseFailure` hook 通过**静态规则**(基于 hook payload 的 tool 名 + exit code + 白/黑名单)判断是不是 friction,是 → append 一行进 `docs/dogfood/v4-friction-log.md`(**硬编码路径**,以路径本身作为 privacy promise 工具)。Operator 在 entry 后手工敲 `[acked]` / `[disputed]` / `[needs-context]` 一行 tag(无 state machine,记事本就能编辑)。`friction <msg>` Python CLI fallback 用于 subjective 体感。`friction --off` / `--on` / `--threshold` 一行止血开关。第 14 天自动跑一次 trust mini-summary(grep 统计三种 tag 比例 + hook 是否仍开),写入 `docs/dogfood/v4-trust-w2.md`。

**User persona** (specific):
Yashu Liu — IDS 单 operator,正在跑 V4 dogfood,同时还要推进 forge 006 路径 2 的 4 周 playbook + 其他 forge 事务。每周 5-10 小时是 friction-tap 这条 fork 的所有可用时间。背景非软件开发,但是 IDS 这工具链的最高频用户。需要 v0.1 在他被 tool 卡住的当下不打扰他,只默默把摩擦点留给 4 周后回看的同一个自己。

**Core user stories** (5):
- 作为 operator,我可以**完全不动手**(0 操作)就让 agent 把"刚才 tool 失败"这件事记到 friction-log,所以我不会因为"切上下文太麻烦"漏记真正卡过的事
- 作为 operator,我可以在任何 entry 后追加 `[acked]` / `[disputed]` / `[needs-context]` 一行,所以我能保留对 entry 准确性的最终叙事权
- 作为 operator,我可以敲 `friction <msg>` 命令补一条 subjective 体感 entry,所以 agent 看不到的层面也能进 archive
- 作为 operator,我可以一行命令(`friction --off`)关掉 hook 或调阈值,所以误报失控时我有快速止血
- 作为 operator,我可以在第 14 天读一份自动产出的 trust mini-summary,所以我知道这个 hook 真的在帮我还是只在制造噪声

**Scope IN (v0.1)**:
- `PostToolUseFailure` hook(JSON 解析 + 静态规则 + append,~50 行)
- 静态规则 = 白名单(`Bash` / `Edit` 失败 + 自定义) + 黑名单(operator `--off` / 含 `[debugging-friction-detection]` 关键字)
- friction-log 硬编码路径 `docs/dogfood/v4-friction-log.md`(脚本启动时若无目录则创建)
- entry 格式: `<ISO> [agent-emit] [confidence:H|M|L] · <tool> exit <code> · "<stderr-200chars>" · task: <desc>` ——**privacy 字段 visible 在 entry 里**(显式标 `[private-to-operator]` 或类似)
- markdown tag (operator 直接编辑文件):`[acked]` / `[disputed]` / `[needs-context]` 一行,grep 即可统计
- `friction <msg>` CLI(~30 行,subjective 体感 fallback)
- `friction --off` / `--on` / `--threshold low|medium|high`(~20 行)
- 第 14 天 trust mini-summary 脚本(grep 统计 + 输出到 `docs/dogfood/v4-trust-w2.md`,~50 行 cron / launchd 触发)

**Scope OUT (explicit non-goals — don't build these now)**:
- **state machine**(simplified — markdown tag 即可,operator 同意)
- **skill placeholder 检测 / 其他 lifecycle hook**(C7 PostToolUseFailure only)
- **LLM-judge**(留 v0.2;静态规则覆盖 80% 真实 friction signal,LLM 是 disputed 率优化)
- **跨仓 ship**(C8 IDS first;ADP 4 周等待期不动)
- **可配路径**(留 v0.2;v0.1 hardcoded 是 privacy promise 工具)
- **frontend / dashboard / 可视化**(RL-4 不与 enterprise observability 竞争)
- **团队共享 / multi-reader format**(C2 single-operator)
- **自动开 issue / PR / fix**(RL-2 不接追责)
- **完整 2 周 pilot 协议** (留 v0.2 — Candidate B 的内容)
- **完整 weekly review ritual** (留 v0.2 — Candidate C 的内容)

**Success looks like** (observable outcomes):
- **O1 · capture 工作**: 第 14 天 friction-log 累计 ≥ 8 条 agent-emit entry(证明 hook 在工作)
- **O2 · trust 在线**: 第 14 天 trust mini-summary 显示 `[acked]` 比例 ≥ 50% 且 `[disputed]` ≤ 20%(operator 没频繁觉得不准)
- **O3 · adoption signal**: 第 14 天 hook 仍 enabled(operator 没在第 14 天前关掉)— 这是 GPT R2 search 引的 quantified-self 弃用研究的反向 metric
- **O4 · review 体验**: operator 能在 10 分钟内审阅 20 条 entry(GPT 给的可测试目标)
- **O5 · 主观确认**: operator 能指出至少 3 条改善了 retrospective recall 的 entry(主观但可记录)

**Time estimate under your constraints**:
- 给定 intake (5-10 hr/week × 1-2 周 = 10-20h):
  - hook + 静态规则 + append: 3-4h
  - markdown tag 约定 + 文档: 1h
  - `friction <msg>` CLI: 1-2h
  - 开关 + 阈值: 1-2h
  - 第 14 天 trust report 脚本: 2-3h
  - 测试 + commit + 文档: 3-4h
  - **总计 ≈ 11-15h** → 1-1.5 周 ship 可信
- **Confidence: H**(本 menu 唯一 H confidence cut)

**UX priorities** (tradeoff stances):
- **trust > speed**: entry tone 必须含 confidence 自评(L|M|H),不假装权威
- **simplicity > cleverness**: markdown tag 优于 state machine — 记事本就能编辑
- **fast off-switch > sophisticated tuning**: `friction --off` 一行止血,胜过精细阈值
- **agent 是 witness 不是 judge**: entry 写"我观察到 X · 我推测 Y · 置信 L|M|H",不写"this is critical / 建议你做"
- **precision > recall**: false positive 的成本是 trust loss,远大于 miss 的成本
- **private as user promise**: 不是隐藏假设,是 visible commitment(GPT R2 §1 push back)

**Biggest risk** (non-technical, product-level):
**File too trustworthy, weakly opened**(GPT R1 原话改写)。format 做对了、entry 看起来 fair,但 operator 4 周后实际不去主动打开 log,价值就死在文件里。这是 substrate-only scope 的固有风险——它把"weekly opening cadence"赌给 operator 自律,而不是产品强制。**对应 mitigation** = 第 14 天 trust mini-summary 是 operator 必看的产物 (用脚本输出 markdown 摘要,放在 IDS 工作流自然路径上)。

**Scope-reality verdict**:
- **Similar products usually include**(GPT R2 search 7 sources):journal-cli / tui-journal / Plain-Text-Journal / Rewind / Journalot 等 markdown dev journal CLI v0.1 形态 = entry index + frontmatter + tags
- **This candidate cuts**: dashboard / 团队 sync / 多读者 format / mood tracking
- **This candidate adds vs norm**(genuinely new): agent-emit + adjudication tags + week-2 trust monitoring **三件套** —— **scope-reality search 在 markdown dev journal CLI 域无任何 v0.1 先例**;这是 Yashu fork 真正新的切法
- **Net read**: **healthy MVP**(在工业先例之上做了 narrow 但 substantive 的扩展;substrate scope 与 1-2 周 timeline 高度吻合)
- **Cited comparable**: Journalot dev journal CLI (https://journalot.dev/) — terminal capture + plain markdown + tags/statuses 是 v0.1 normal vocabulary

**Best fit for a human who**:
正在严苛 timeline 下需要 ship 一个 honest substrate,且相信"先把工程脊柱做对、后续 wrapper 由 dogfood 反馈决定"的 operator。如果 you 历史上能自律 weekly review,且能容忍"v0.1 没有 explicit adoption decision protocol"的不确定,A 是你的选择。如果 you 已经知道自己历史上 4 周后不会主动回看 log,A 不够 — 看 C。

---

### Candidate B · "A + Week-2 Trust Flight"

**Suggested fork id**: `007a-agent-emit-pB-pilot`
**Sources**: GPT R1 Candidate B(原创) → Opus R2 接受为 peer + refine

**v0.1 in one paragraph**:
v0.1 不只是 logger,是**一次 2 周 adoption pilot**。包含 Candidate A 的全部 (substrate),但**核心 deliverable 是第 14 天的 30-60 min self-interview**,产物是一份 keep / tighten / pause 决策报告。Self-interview 模板用 L2 §7 GPT R2 列的 3 个问题 + intake OQ-7/8/9/10 衍生的 3 个问题。pilot 结束后产生一份"v0.1 verdict"短报告,直接 feed 进 forge 006 路径 2 的 W3 V4 checkpoint-01 retrospective。

**User persona** (specific):
同 A,但 operator 显式 framed as **pilot participant**——不是"用 v0.1 的人",是"决定 v0.1 是否值得保留的评审人"。Yashu 同时正在跑 forge 006 路径 2 的 4 周 playbook,这条 pilot 与 W2 step 4 / W3 V4 checkpoint-01 节奏天然对齐。

**Core user stories** (4):
- 作为 pilot participant,我可以跑 2 dogfood 周收集足够多的真实 entry,所以 trust 决定基于 evidence 不是 vibes
- 作为 pilot participant,我可以用自己的 entries 完成 30-60 min self-interview,所以 keep / tighten / pause 决定有材料
- 作为 pilot participant,我可以指认哪些 entry **改变了真实决策**、哪些会让我**关掉 witness**,所以 v0.2 设计有方向
- 作为 pilot participant,我可以在 day-14 输出一份 short verdict,所以这条 fork 不会"安静地变 dead code"

**Scope IN (v0.1)**:
- **A 的全部 substrate**(hook + 静态规则 + 硬编码路径 + adjudication tag + CLI fallback + 开关)
- **Self-interview 模板**(`docs/dogfood/v4-pilot-w2-self-interview.md` — 6 个问题:
  - "look at 5 sample entries — which agree, which edit, which feels unfair?"
  - "after 20 entries, which changed an actual decision?"
  - "what exact ratio of disputed entries would make you pause?"
  - "would you keep this enabled if only you read it?"
  - "what false-positive count maps to keep / tighten / pause?"
  - "is the witness empowering or surveilling?")
- **Trust monitoring 章节升级**:在 trust report 加 `keep / tighten / pause` decision section
- **End-of-pilot verdict note**(`docs/dogfood/v4-pilot-w2-verdict.md` — operator 写 1-2 段 verdict)
- **Top false-positive evidence preserved**(mark, don't delete + 选 top-3 进 self-interview 输入)

**Scope OUT (explicit non-goals)**:
- 持续运行的 weekly habit system(留 v0.2 — Candidate C 的领地)
- 多周 trend 引擎 / pattern 累积(C2 single-operator + 1-2 周 timeline)
- team-facing artifact / shared sync(C2 + RL-3)
- 任何 "扩展 event coverage" 在 pilot 中(C7 PostToolUseFailure only)
- 自动转化 verdict 到 v0.2 plan(operator 决定 follow-up 路径,不自动)

**Success looks like**:
- **O1 (B-specific)**: day-14 self-interview 完成(operator 真坐下来花 30-60 min 答完 6 个问题)
- **O2**: operator 能 named 写出 top 2 keep / pause reasons
- **O3**: false-positive tolerance ratio 量化(eg "≤ 3% disputed → keep / 3-15% → tighten / >15% → pause")
- **O4**: L3 / L4 不再 "guess about adoption risk" — 有 evidence base
- **O5**: end-of-pilot verdict note 直接 feed 进 forge 006 路径 2 W3 V4 checkpoint-01

**Time estimate under your constraints**:
- 给定 intake:
  - A 的 substrate: 11-15h
  - self-interview 模板设计 + 文档: 2-3h
  - trust report 升级到 keep/tighten/pause section: 1-2h
  - end-of-pilot verdict 写作: 1-2h(operator 自己写,不是工程量)
  - **总工程时间 ≈ 14-18h** + **operator self-interview 30-60min × 2 = 1-2h**
  - **总计 ≈ 15-20h** → 1.5-2 周 ship + 完整 pilot 跑完 = 与 timeline 边界紧
- **Confidence: M**(scope 仍小,但依赖 operator discipline 真坐下来做 self-interview)

**UX priorities**:
- **adoption evidence > feature completeness**: pilot 决定优先于 v0.2 feature 设计
- **the witness must earn continued permission**: pause is a valid success state
- **archive evaluated as relationship, not file**: v0.1 verdict 是关系评估,不是 product review

**Biggest risk**:
**Self-interview 没做完,scope 塌方**。Self-interview 是 v0.1 的 keystone deliverable —— 如果 operator 在 W3 V4 checkpoint-01 那周太忙跳过 self-interview,加上的 scope (vs A) 就全部白做。这风险与 catch-all "friction-tap 不能拼动 operator 太多时间" 直接拉锯。

**Scope-reality verdict**:
- **Similar products usually include**(GPT R2 search):BugBug pilot testing guide / ClawStaff AI pilot guide / DigitalApplied 2026 AI coding tool adoption survey 等 — 都把 "pilot 含 success/stop criteria + 1-2 周 review window + continue/adjust/stop decision" 列为 baseline
- **This candidate cuts**: 多 workflow 并行 pilot / formal stakeholder review meetings / passive logging without decision date
- **Industry-aligned**: "**Most pilot tests run for 1 to 2 weeks**" + "**After two weeks of pilots with three different AI testing platforms, one team settled on a mid-tier option**" — Candidate B 不是 idiosyncratic 选择,**是 2026 industry baseline 在 Yashu 单 operator 场景的应用**
- **Net read**: **healthy MVP, industry-aligned**;但 timeline 紧
- **Cited comparable**: BugBug pilot testing guide (https://bugbug.io/blog/software-testing/pilot-testing/) + ClawStaff AI pilot guide (https://clawstaff.ai/learn/ai-pilot-program/)

**Best fit for a human who**:
重重看 priority #1 trust calibration(认为"任何不带 explicit adoption 评估的 v0.1 是赌博"),且在 day-14 那周能真坐下来花 1-2h 做 self-interview。如果 you 知道自己历史上"立 flag 容易,执行难"——慎选 B,塌方风险高。如果 you 想要 evidence-based 决策(且不介意为此付 +3-5h 工程量),B 是 industry-standard 选择。

---

### Candidate C · "A + 周复盘提示"

**Suggested fork id**: `007a-agent-emit-pC-ritual`
**Sources**: GPT R1 Candidate C(原创) → Opus R2 接受为 peer(撤回 R1 "C 不必要"判断)+ refine

**v0.1 in one paragraph**:
friction-log 的中心从"capture quality"换成"opening cadence"。Candidate A 的全部 substrate 仍然存在,但**v0.1 加一个轻量 weekly review ritual**:每周末 operator 跑 `friction --review`,脚本输出当周 entry 摘要 + prompt operator 选 top-3 + 写一句 weekly pattern sentence。Top-3 + pattern sentence 直接形成 retrospective 输入。第 14 天 trust mini-summary 升级为"两周累计 + 两次 weekly review 完成度"。

**User persona** (specific):
同 A,但 operator 已经从 self-knowledge 知道:**未打开的 log = 死 log**。Yashu 历史上若有"立 flag 后不主动回看"的模式,C 直接 address 这个 gap,把"future-me 真的会打开"做成产品强制。

**Core user stories** (4):
- 作为 operator,我可以跑 weekly review section(`friction --review`),所以 raw entries 转成"小而可用的记忆"
- 作为 operator,我可以选 top-3 friction entries,所以 retrospective 有 signal,不是一堆
- 作为 operator,我可以标每条 top-3 是 agent-accurate / human-corrected / false-positive,所以 v0.2 设计方向有量化基础
- 作为 operator,我可以写一句 weekly pattern sentence 给未来的自己,所以 archive 有 narrative arc 不是孤立 entry

**Scope IN (v0.1)**:
- **A 的全部 substrate**
- **Weekly review section**(`docs/dogfood/v4-friction-log.md` 末尾追加 weekly section,或独立 `docs/dogfood/v4-friction-weekly-w<n>.md`)
- **`friction --review` 命令**(~40 行 — grep 当周 entry + prompt operator + 写 top-3 + pattern sentence)
- **Top-3 selection ritual**(operator 标 1/2/3 序号 + agent-accurate/human-corrected/false-positive 三选一)
- **Weekly pattern sentence prompt**(以 frame 而非 prompt — eg "若一周下来一句话给 future-me, 最该提醒的 friction 模式是什么?")
- **Trust mini-summary 升级**:第 14 天报告含 "weekly review 完成 X / 2 次" metric

**Scope OUT (explicit non-goals)**:
- daily reminder / push notification(C2 + 不打扰)
- analytics / graphing / dashboard(RL-4)
- 转化 entry 到 task / issue(RL-2)
- mood tracking / 情绪 (RL-1 不接全知监控)
- 多周 history / 历史 archive 浏览(留 v0.2)
- self-interview(B 的领地;C 的 ritual 是 weekly,不是 day-14 一次性)

**Success looks like**:
- **O1 (C-specific)**: operator 在 W1 末和 W2 末各跑一次 `friction --review`(2/2 完成率)
- **O2**: 每次 review 末有 3 selected entries + 1 pattern sentence
- **O3**: weekly review 直接 feed 进 retrospective note,operator 不需要 cat 全部 raw entry
- **O4**: ritual feels lightweight, not chore(主观但可记录:operator 描述 "review 像 reflective practice 还是像 paperwork")
- **O5**: 第 14 天 trust mini-summary 含 weekly review 完成度

**Time estimate under your constraints**:
- 给定 intake:
  - A 的 substrate: 11-15h
  - `friction --review` 命令 + prompt 设计: 2-3h(prompt 文案不可压缩)
  - weekly review section 格式 + 文档: 1-2h
  - **总工程时间 ≈ 14-20h** + **operator weekly review × 2 = 30-60min × 2**
  - **总计 ≈ 15-21h** → 1.5-2 周 ship + 2 次 weekly review 完成 = 与 timeline 边界紧,且面临 prompt 调优风险
- **Confidence: M-L**(GPT R2 §5 新增 caution:"weekly-review products avoid blank-page failure with prompts, summaries, history, and pattern surfacing. **A thin prompt may not be enough**" — Reflct / Mindsera / Reflection / Rosebud 都有 substantial 的 prompt scaffolding,1-2 周 budget 可能不够)

**UX priorities**:
- **cadence > completeness**: 每周开比每条 entry 完美更重要
- **weekly meaning-making > raw accumulation**: top-3 + pattern 比 100 条原始 entry 更有用
- **small prompts > dashboard**: 一行 reflective 提问胜过分析图表
- **private and reflective, not performative**: weekly section 不是给别人看的产物

**Biggest risk**:
**Ritual prompt 调优陷阱 + scaffolding 不足风险**(GPT R2 §5 新 caution)。weekly review 产品(Reflct / Mindsera / Reflection / Rosebud)成熟形态有 prompts + summaries + history + pattern surfacing 四件套;v0.1 1-2 周 budget 只够做 prompts + 单次 weekly section,缺 history 和 pattern surfacing 的 scaffolding —— 操作两次后可能 ritual 感薄弱。第二个风险是 prompt 文案不对(从 personal-growth journaling 域搬来的 adherence/commitment/reward 风格在 engineering friction 域 awkward) — 需要重新设计措辞,这是隐藏成本。

**Scope-reality verdict**:
- **Similar products usually include**(GPT R2 search):Reflct (https://reflct.co/) — prompts + lightweight ratings + weekly summaries + pattern surfacing + private posture;DevDiary (https://devdiary.me/) — automatic developer diary + daily narrative + session context + later review
- **This candidate cuts**: prompts library / mood ratings / pattern surfacing engine / 历史 archive
- **Industry precedent exists, but minimal v0.1 may be underbuilt**: Reflct/Mindsera 类工具典型有 4 件套 scaffolding,Yashu v0.1 budget 只够 1-2 件
- **Net read**: **ambitious for the budget**;real precedent 在 personal journaling 域,engineering friction 域是新切法,但**新切法 + 紧 budget = 双重风险**
- **Cited comparable**: Reflct (https://reflct.co/) - 在功能 fit 上最接近,但其 v0.1 含 prompts + summaries 的 scaffolding 远超 Yashu 1-2 周 budget 能给的

**Best fit for a human who**:
已知自己历史上"立 flag 容易,执行难",且**确信 weekly cadence 是产品命脉**(without it, 任何 capture 都死掉)。如果 you 愿意为 cadence 牺牲 some substrate polish,且能容忍 ritual prompt 文案"先粗后细"的迭代成本,C 是你的选择。如果 you 没有强 self-knowledge 表明"我历史上不主动 review",C 的 +3-5h 工程量与 prompt 调优风险**可能投资回报偏低**。

---

## Comparison matrix

| Dimension | Candidate A · 证词契约日志 | Candidate B · A + Week-2 Trust Flight | Candidate C · A + 周复盘提示 |
|---|---|---|---|
| **Trust surface** (R1 Opus axis) | entry 格式 + adjudication ergonomics | 2 周 adoption decision (evidence-based) | weekly opening cadence (future-me reads it) |
| **v0.1 deliverable** | substrate (private log + tags + week-2 mini-summary) | substrate + self-interview + keep/tighten/pause verdict | substrate + weekly review section + top-3 + pattern sentence |
| **Time estimate** | 11-15h · 1-1.5 周 | 14-18h + 1-2h interview · 1.5-2 周 | 14-20h + weekly × 2 · 1.5-2 周 |
| **Confidence** | **H** | M | M-L |
| **Industry precedent** | journal-cli / tui-journal / Plain-Text-Journal / Journalot — substrate scope 工业化先例 | BugBug / ClawStaff / DigitalApplied — 2 周 pilot 是 **2026 industry baseline** | Reflct / Mindsera / DevDiary — 工具成熟,但 v0.1 形态需 4 件 scaffolding,本预算只够 1-2 件 |
| **Risk if it fails** | file too trustworthy, weakly opened (substrate 赌 operator 自律) | self-interview 没做完, scope 塌方(B 的工程加项白付) | ritual prompt 调优陷阱 + scaffolding 不足风险 |
| **Best for operator profile** | 信"先把脊柱做对、wrapper 由 dogfood 决定" | 重重看 priority #1 trust + 能在 day-14 真坐下来做 self-interview | 已知自己 "立 flag 容易,执行难" + 确信 cadence 是产品命脉 |
| **Fits 1-2 周 timeline** | ✅ | ⚠ tight (1.5-2 周 边界) | ⚠ tight + scaffolding 不足 |
| **Respects all 4 red lines** | ✅ | ✅ | ✅ |
| **Honors all 4 cond** | ✅ | ✅ + 升级 cond-3 | ✅ + 升级 cond-3 |
| **Substrate vs wrapper** | substrate alone | substrate + adoption-protocol wrapper | substrate + ritual wrapper |

---

## Synthesizer recommendation

**Recommended: Candidate A,with one B-compatible week-2 question included**(hybrid — synthesizer's strongest pick)

理由(3 句):
1. Candidate A 是其他两条的 prerequisite —— B 和 C 都依赖私有 log + adjudication 已经在那 (两侧 R2 独立收敛);且 1-2 周 timeline 下,A 是唯一 H confidence cut。
2. **GPT R2 §4 specific recommendation**:"choose A as v0.1, but **include one B-compatible week-2 question**" —— 在 A 的 day-14 trust mini-summary 加一个 self-interview 问题(eg "after 20 entries, which exact ratio of disputed entries would make you pause the witness?")。这是**几乎零工程成本**(<1h)的 hedge:既保 H confidence + 1-1.5 周 ship,又不丢 adoption 评估的 evidence。
3. 与 industry baseline 对齐(2 周 pilot + 决策点是 2026 工业标准),且与 forge 006 路径 2 的 W3 V4 checkpoint-01 节奏天然咬合 —— operator 在 W3 那周复盘 v0.1 verdict 时,已有结构化 evidence 不是凭感觉。

**Defer to v0.2**:
- 完整 B(formal pilot protocol with 6-question interview + verdict report)
- 完整 C(weekly review ritual)
- 两者都可以加在 A's substrate 之上而不需 rework —— substrate 投资保留

**操作建议(给 fork 阶段的 operator)**:
- Fork Candidate A:`/fork 007a-agent-emit from-L3 candidate-A as 007a-agent-emit-pA-substrate`
- 在 PRD §"v0.1 升级" 或 §"Open questions for L4" 显式记一条:"A + 1 个 B-compatible day-14 self-interview question(详见 OQ-A 决议)" — 让 spec-writer 把这一句问题嵌入 day-14 trust mini-summary 模板
- v0.2 触发 trigger 设计:如果 v0.1 day-14 verdict 是 "tighten" → v0.2 候选包含 LLM-judge / 可配路径 / 误报阈值;如果 verdict 是 "keep + 想要 cadence" → v0.2 候选包含 weekly ritual(C 的内容)

**为什么不 recommend "fork both A and B"** :timeline 紧 + B 是 wrapper not peer。fork B 等于在 1-2 周里同时 ship substrate + adoption-protocol,**operator self-interview discipline 是不可工程化的 risk**;一个 day-14 self-interview question hedge 比完整 pilot wrapper 投资回报高得多。

**为什么不 recommend "Pause / Back to L2"**:L2 已经把 conditions 锁得很清楚,intake 已经把 hard constraint 锁得很清楚,3 candidate 形态都合法,**菜单可以决策,无需回上层**。

---

## Honesty check — what the menu might underweight

1. **Candidate A 的 "file too trustworthy, weakly opened" risk 没有被 menu 充分量化**。如果 Yashu 历史上有"立 flag 后不主动回看"模式,A + day-14 self-interview question 这个 hedge 可能不够 —— 那时应该认真考虑 C 而非 A。但 menu 没法替 operator 答这个 self-knowledge 问题。
2. **OQ-C(如何观测 hook is still enabled)在 menu 中没决议** —— observational metric (脚本检查 `~/.claude/settings.json` 是否仍含 hook)与 self-report (operator 自填一行)各有 tradeoff;前者更可信但工程量 +2-3h(且涉及 Claude Code 配置文件 schema 假设),后者轻量但 self-report 偏差。**这是 OQ-A 之外 menu 真正没解决的工程决策**。
3. **三条 candidate 都默认假设 forge 006 路径 2 W2 step 4 时间窗能容纳 v0.1 ship + 第 14 天 trust 报告产物**,但 operator 同时要跑 V4 dogfood + 其他 forge 事务。**如果 W2 实际只剩 4-5h/week(低于 5-10h 区间下沿),所有候选都受影响,A 仍然最 robust 但也面临 timeline 滑出 1.5 周的风险**。
4. **scope-reality search 在 "agent self-emit + adjudication + week-2 trust" 三件套上**找不到任何先例(Yashu fork 真正新),**这意味着 trust monitoring metric 的设计没有工业 baseline 可参考** —— O1 ≥8 entry / O2 acked ≥50% disputed ≤20% / O3 hook still enabled 这些数字是 Opus R1 提的,**未经 user research 验证**;真实 dogfood 第 1 周可能 disputed 率显著高于 20%,需 W1 末做一次 mid-pilot 校准。
5. **Candidate B 的 self-interview 模板有 6 个问题,可能太重**。intake catch-all 明确 "scope 必须最 minimal";B 的 6 个问题在 day-14 那一天压力大,**可能合理压到 3 个**(GPT R2 §6 原本 3 题足够 — 6 题是 B 加进的)。fork B 时 operator 应该回去看 GPT R2 §6 的 3 题原版。
6. **C 的 weekly pattern sentence prompt 措辞 menu 没给**(列在 OQ-B,只在 fork C 时相关)。这是 GPT R2 §5 caution 的核心:bad prompts 会让 ritual 变 chore。fork C 前必须先写好 prompt 草稿,不能边做边想。

---

## Decision menu (for the human)

> **PRD-form 决定用哪个 fork 命令**。简表见 §"Candidate relationships" §3 推荐(下文)。

### [F] Fork one candidate (simple form, single v0.1) — synthesizer 推荐
```
/fork 007a-agent-emit from-L3 candidate-A as 007a-agent-emit-pA-substrate
/plan-start 007a-agent-emit-pA-substrate
```
**推荐操作**:fork A,且在 PRD §"v0.1 升级" 显式记 OQ-A 决议为 "include 1 B-compatible day-14 self-interview question"。

### [MF] Fork multiple in parallel(simple form × N,sibling 子树)
```
/fork 007a-agent-emit from-L3 candidate-A as 007a-agent-emit-pA-substrate
/fork 007a-agent-emit from-L3 candidate-B as 007a-agent-emit-pB-pilot
/fork 007a-agent-emit from-L3 candidate-C as 007a-agent-emit-pC-ritual
```
**不推荐**:timeline 紧 + B/C 是 wrapper not peer,parallel forking 会让 v0.1 工程量爆炸。除非 operator 想做 "A as primary + B/C as park-for-future" 形态。

### [FP] Fork one candidate with phased planning(≥2 phase in same PRD)
```
/fork-phased 007a-agent-emit from-L3 candidate-A as 007a-agent-emit-pA-substrate
```
**可考虑**:phase v0.1 = A substrate + 1 B-compatible question;phase v0.2 = full B 或 full C(由 v0.1 day-14 verdict 决定)。这是 synthesizer 推荐的隐含结构,可以显式化为 phased PRD。

### [FC] Fork composite(multiple candidates → one PRD with modules)
```
/fork-composite 007a-agent-emit from-L3 A,B,C as 007a-agent-emit-pAll
```
**禁止推荐**:§"Candidate relationships" §1 关系矩阵确认 B 和 C 是 A 的 wrapper(顺承 + 替代),不是互补。composite 不适用。

### [F1] Fork v1-direct(skip v0.1, ship v1)
```
/fork-v1 007a-agent-emit from-L3 candidate-A as 007a-agent-emit-pA-substrate
```
**禁止推荐**:§"Candidate relationships" §4 评估 0 条 ✅(C1/C2/C3 全 ❌),v1-direct 无依据。

### [R] Re-scope with new input
```
/scope-inject 007a-agent-emit "<your steering>"
/scope-next 007a-agent-emit
```
**只有在**:(1) operator 新发现 hard constraint(eg "我可用时间从 5-10h 降到 3-5h"),或 (2) 想要探"全 lifecycle 覆盖"或"LLM-judge 路径"等 OQ-2/OQ-3 重大重选时,才用 re-scope。

### [B] Back to L2 — rethink the idea
```
/status 007a-agent-emit
```
**不推荐**:L2 conditions 已锁得很清楚,3 candidate 在 conditions 内合法。除非读完 menu 后觉得整个 idea 需要换框架(eg 想换到 L1 menu 的 `007d-complaint-license` 心理许可方向)。

### [P] Park
```
/park 007a-agent-emit
```
所有 artifacts 保留。**适用场景**:operator 想先去做 30-60 min self-interview(L2 §7 + Opus R1 §6 + GPT R1 §6 共列了 5-6 个问题)再回来 fork。**这是最稳妥的延期选项**——self-interview 输出能让 OQ-A / OQ-B / OQ-C 都有答案。

### [A] Abandon
```
/abandon 007a-agent-emit
```
**不推荐**(L2 verdict 是 Y-with-conditions,4 条 condition 在 L3 已全部内化进 C6 hard constraint,scope 决策清晰)。如果 abandon 应写明 lesson(eg "verdict 是 Y 但我没足够时间")。

---

## Candidate relationships *(强制章节,4 个子节都必须非空)*

> 此章节是 PRD-form 推荐的依据。它分析 3 candidate 之间到底是替代/互补/顺承,从而帮 operator 决定用哪种 fork 命令。

### 1. Pairwise relationship matrix

| 关系维度 | A→B | A→C | B→C |
|---|---|---|---|
| **替代/互补/顺承** | **顺承**(B 是 A 之上的 adoption wrapper;无 A 则 B 无 entry 可 review) | **顺承**(C 是 A 之上的 ritual wrapper;无 A 则 C 无 entry 可 select) | **替代**(B 是 day-14 一次性 evidence-based 决策;C 是 weekly 持续 ritual;两者都消耗 v0.1 budget 顶部 4-6h,做了 B 就不该做 C — 同 timeline 内) |
| **共享产物** | A 的 substrate(hook + tag + log + mini-summary)100% 复用 | A 的 substrate 100% 复用 | A 的 substrate 100% 共享(B/C 都依赖)— 但 B 的 self-interview 模板 vs C 的 weekly review section 是不同产物,不复用 |
| **时间依赖** | A 必须先 / 同时 ship,B 才有 entry 跑 self-interview | A 必须先 / 同时 ship,C 才有 entry 选 top-3 | 无强时间依赖(都依赖 A,互不依赖);但同 timeline 内择一 |

**关系定义复盘**:
- **顺承(A→B / A→C)**:做 B 或 C 必须先做 A;A 是 B 和 C 共同的 substrate
- **替代(B↔C)**:在 1-2 周 timeline 内 B 和 C 不能同时做(A+B = 14-18h, A+C = 14-20h, A+B+C = 25-30h 显著超 budget) —— 是同一资源池上的不同投资

### 2. 如果合体,产品长什么样?

假设 A + B + C 全做掉(忽略 timeline)—— 合体产品形态:
- 私有 IDS friction-log,agent emit + adjudication tag substrate(A 部分)
- 每周末 operator 跑 weekly review 选 top-3 + 写 pattern sentence(C 部分)
- 两周末 operator 做完整 self-interview + 输出 keep/tighten/pause verdict 报告(B 部分)

**形态评估**:**这是合理的一个产品**(weekly ritual 持续 + day-14 explicit decision point),不别扭。**但**:
1. 工程量 25-30h × operator 5-10h/week = 至少 2.5-3 周,**显著违反 1-2 周 timeline**
2. operator self-interview + weekly review × 2 共需 2.5-3.5h operator 时间,**与 catch-all "friction-tap 不能拼动太多时间" 拉锯严重**
3. v0.1 SUDDENLY 同时验证 3 个产品假设(substrate / pilot decision / weekly cadence)—— **科学上 confounded**, 验证不出来哪个 element 真的工作

**结论**:合体在产品形态上 valid,**在 v0.1 timeline 下不 viable**;且科学上不利于 evidence-based 决策。这印证了"必须择一作为 spine"的 Opus R2 §4 判断。

### 3. PRD-form 推荐

**推荐**: **simple**(单 candidate v0.1) 或 **phased**(单 candidate ≥2 phase)

**理由**(2-3 句):
A→B 和 A→C 是顺承,B↔C 是替代 —— 这意味着 v0.1 必有一条单一 spine。最干净的形态是 **simple PRD with Candidate A + 1 B-compatible day-14 self-interview question** (synthesizer 推荐),其次合理形态是 **phased PRD**(phase v0.1 = A + 1 question; phase v0.2 = full B 或 full C, 由 day-14 verdict 决定)。

**不推荐**:
- **composite**(§1 关系矩阵显示 B 和 C 是替代,不是互补,且都是 A 的 wrapper —— composite 不适用)
- **v1-direct**(§4 评估 0 条 ✅)
- **parallel forking 三条**(timeline 紧 + B/C 是 wrapper,parallel 不能让它们独立验证因为它们都依赖 A)

### 4. 跳过 v0.1 的合理性评估

| 条件 | ✅/❌ | 证据 |
|---|---|---|
| **C1** · 核心假设是否已外部验证? | **❌** | scope-reality search(GPT R2 §2)在"agent self-emit + adjudication + week-2 trust 三件套"上**找不到任何先例**(journal-cli / tui-journal / Plain-Text-Journal / Rewind / Journalot 都无 trust monitoring + adjudication);quantified-self 弃用研究 + electronic monitoring meta-analysis 反复警告 adoption 风险。**核心假设(operator 4 周后真的 trust agent witness)未经任何外部验证**。 |
| **C2** · v0.1 是否有独立可发布价值? | **✅** | A 的 substrate(私有 log + adjudication + week-2 mini-summary)对 forge 006 路径 2 W2 step 4 即时可用,且独立产生 retrospective input 价值;v0.1 是 useful artifact 不需 v1.0 才有价值。 |
| **C3** · 多 candidate 是否互补? | **❌** | §1 关系矩阵显示 B↔C 是替代不是互补;A→B / A→C 是顺承(wrapper),A 是 spine,B/C 各自是同一资源池的不同投资。 |

**判断**:**1 条 ✅**(C2)→ **v1-direct 可考虑,但需 operator 在 fork-v1 时填详细 skip-rationale ≥100 字 + 含 C1/C2/C3 之一**

但实际**强烈不推荐 v1-direct**:虽然 C2 ✅,但 C1 ❌ 是关键否决项。在"核心假设未经任何外部验证"情况下跳过 v0.1 = 把 v1.0 设计建立在未证实的 adoption 假设上,与 priority #1 trust calibration 直接冲突。**v0.1 的 day-14 trust mini-summary 是验证 C1 的最便宜手段**。

### 5. composite vs parallel forking 区分(防误用)

**本菜单 §1 关系矩阵的关键发现**:
- A→B / A→C 是**顺承**(wrapper) → composite 不适用(composite 假设 N candidate 是同一产品的不同器官,合体后才完整。这里 B 和 C 各自是 A 的 wrapper,A 已经是完整产品)
- B↔C 是**替代** → 严格根据 menu spec 的 §5 规则:"§1 关系矩阵如果发现关系是'替代',**禁止推荐 composite** — 强制建议 parallel forking。"

**但 parallel forking 在本案也不推荐**,因为:
1. B 和 C 都不是独立 v0.1(都需 A substrate);parallel 跑 A vs B vs C 等于 sibling 都包含 A 工作,3 倍工程量
2. 1-2 周 timeline 下 parallel 跑两条 sibling(A 和 B 或 A 和 C)= 14h × 2 = 28h, 显著超 budget

**结论(本案特例)**:本案的 B↔C 替代关系**不触发 parallel forking 推荐**,因为两条 sibling 都不是独立 v0.1。最终推荐回到 **simple form (Candidate A) + 1 B-compatible question hedge**,或 **phased(A 作 v0.1 + B 或 C 作 v0.2)**。

---

## Fork log

- 2026-05-08T12:09:30Z · Candidate A + 1 day-14 self-interview question hybrid forked as `007a-pA`(simple form, status: just-created, synthesizer-recommended hybrid path, ready for /plan-start)
