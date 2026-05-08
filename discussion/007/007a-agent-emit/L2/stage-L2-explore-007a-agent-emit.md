# L2 Explore Report · 007a-agent-emit · "Agent 自录摩擦——agent 当 witness,operator 当审阅者"

**Generated**: 2026-05-08T09:30:00Z
**Source**: forked from 007 L1 menu Direction 1 "Agent 自录摩擦"(主语反转)
**Source rounds**: L2R1 (Opus + GPT) · L2R2 (Opus + GPT)
**Searches run**: 19 query strings across 15+ distinct sources(Opus 4 次 value-validation,GPT 15 次 query / 6 sources cited)
**Moderator injections honored**: none(本 fork 无 moderator notes)

## How to read this

这是 L2 对 `007a-agent-emit` 的深度展开。它不是 L1 那种"多个浅层方向的菜单",而是**对一个 idea 的丰富理解**。读完之后你应该清楚:

- 这个 idea **真正是什么**(不是表层"自动记日志",而是一种 agent-operator 关系的契约)
- 它**为什么值得做**(以及哪些 honest reasons 值得三思)
- 它**会自然长成什么 / 不该长成什么**
- 进 L3 之前,你必须先回答(或先去找用户聊)的问题

两位 debater 在这个 fork 上走出了**两个互补的 aperture**:Opus 偏机制与可发车性(载体确定为 `PostToolUseFailure` hook、entry id 状态机、~150-200 行实现);GPT 偏心理与采纳(empowerment vs anxiety、trust calibration、"agent 当 witness 不当 judge")。**这两个视角不是分歧,是同一座房子的两扇窗** —— 本报告把它们合成完整画像。

---

## Executive summary

- **这个 idea 的真正脊柱不是"自动记日志",而是"agent-generated review evidence with human adjudication"** —— agent 提名摩擦时刻,operator 审阅 / 反驳 / 补充 / 拥有最终叙事权。两侧 R2 独立收敛到这一句话。
- **载体已落定**:Claude Code 的 `PostToolUseFailure` hook 是 documented + 工业化的,允许 hook 写文件,2026 新增 `duration_ms` 字段。Opus q1 由搜索 GREEN 解决 —— **这条不再是 L3 的 OQ**。
- **Validation 网评:Y-with-conditions**。dogfooding feedback loop、incident timeline auto-witness、psychologically safe reporting 都有先例。但 quantified-self 弃用研究 + electronic monitoring meta-analysis + error-reporting psych safety review 反复警告:**如果 entry 让 operator 觉得不准、judge、surveillance,他会在第 2 周关掉 hook**。
- **v0.1 必须包含 4 条硬条件**(详见 §6),其中"人类审阅入口在 v0.1 而不是 v0.2"是不可让步的产品决策(不是工程 polish)。
- **进 L3 的关键 OQ 不是技术,是 scope 取舍**:审阅入口在不在 v0.1 / friction signal 用静态规则还是 LLM-driven / 事件覆盖范围多大 / 先 ship 给 IDS 自用还是等 ADP V4(forge 006 路径 2 的 4 周等待期)。

---

## 1. The idea, fully unpacked

**它不是一个 CLI,也不是一个 hook —— 它是一种 agent-operator 间的协作契约**。原 proposal `friction <msg>` 50 行 Python CLI 仍然存在,但在这条 fork 形态下从主路径退到"operator-fallback":日常 95% 的 friction entry 由 Claude session 在被工具链卡住的当下自己 emit;CLI 只在 agent 漏报、或 operator 想留 subjective 体感时才被使用。这不是 CLI 的功能扩展,是**主语反转**:`friction-log` 的写入者从"想记笔记的开发者"反转成"参与工作的 agent 自己"。

**真实用户是同一个人扮演三种角色,而不是三个不同的人**。主用户是正在跑 V4 dogfood 的单个 operator —— 他在 Claude Code 终端调度 agent 跑 task,目标是把 autodev_pipe V4 阶段(2026-05-06 frozen 起 12 周)走完并产出 checkpoint-01/02/03 三份 retrospective 报告。次用户是 3 天后 / 4 周后回看 friction-log 的**同一个 operator** —— 他在不同时间点扮演不同角色:当下是"做事的人",4 周后是"审阅者",6 个月后是"trace 历史 archive 的研究者"。这个 1:1:1 架构(同一人既是 user 又是 dogfooder 又是审阅者)是 LLM observability 行业(Langfuse / Helicone / Phoenix / Pydantic Logfire / Datadog LLM)**没有任何对手在做**的 narrow slice —— 这些工具都是为"product team 监控用户用 LLM 服务"的多人架构服务的。

**没有这个工具时的一天**:operator 跑了 6 小时 dogfood task,其中 2 小时被工具坑(retrospective skill 跑出 placeholder、`append_lesson.py` 静默失败、parallel-builder 在某个 task 上无限重试同一个错)。每次坑的当下他想"我应该记一笔",然后(1)找 friction-log 文件路径(2)算 ISO timestamp(3)切到正确 cwd(4)echo + redirect。4 步加在一起 90 秒,但更关键是这 90 秒打断了"我正在调试这个具体 task"的心流。结果:他记了第 1 次,跳过第 2/3/4 次,第 5 次记了一条情绪化的"!!! 又来了 !!!" 但缺 context。一周后他打开 friction-log 看到 4 条混乱条目,3 条已经想不起来当时具体是什么。**周五复盘变成了"工具链还有摩擦"这句没素材的空话**。

**有这个工具时的一天**:operator 跑同样 6 小时 dogfood。这一次,每次某个 hook 或 tool 失败、或某个 skill 输出明显是 placeholder 时,Claude session 自己识别这是 friction signal 并写一行。operator 看不见这个动作,他依然在解决眼前的具体 task。一周后他打开 friction-log,看到 27 条带完整 context 的 entry,例如:`2026-05-15T08:23:11Z [agent-emit] · spec_validator failed during T007 build, exit code 2 stderr "expected 7 elements found 6", task description: ...`。这段是 agent 写的,不是他写的。**他从"记录的人"变成"审阅的人"**。

**第一次"啊哈"30 秒发生时,empowerment 与 anxiety 同时到来**。operator 看到一条不是自己写的 entry,却立刻点头 "对,刚才就是这个"。empowerment 是他从书记员变成审阅者;anxiety 是 witness 会选择、命名、遗漏 —— "凭什么是 agent 决定哪些时刻值得记?它会不会漏了我心里真正觉得卡的那条?它会不会把我故意制造的失败误标成 friction?"。**两位 debater 在这个紧张点上独立收敛**:GPT 直接命名为 empowerment-vs-anxiety,Opus 在 R2 读 GPT R1 后认账"这个让渡同时带 anxiety,如果 v0.1 不显式给 operator 审阅 / 反驳 / 补充 入口,这个 anxiety 会让 operator 默默把 agent emit 关掉"。这一条不是 nice-to-have polish,是 v0.1 的产品决策级 hard requirement。

**4 周后回看时,friction-log 呈双声部 archive**。人写的 entry 像自我报告,带情绪重音;agent 写的 entry 像第三人观察,更冷,有时更刺眼。最有意思的是"这条不是我,但我同意"。operator 学会读两种不同语气:哪些 agent entry 该追问、哪些只是噪声、哪些需要补一句人的体感。这种**"两类 entry —— agent 自己承认的 vs operator 后补充的 —— 可对照"** 的形态,是这条 fork 真正没人在做的 narrow slice。

**6 个月 mastery 是 operator 不再每天 cat friction-log**。retrospective skill 在 phase 收官时自动从 friction-log 提取主题并产出聚合报告,operator 直接看报告;friction-log 自身退到 audit trail。**它的真价值不是日常工具,是历史 archive** —— 历经 12 周后回头看,你能 trace 出哪一类 friction 是哪个 phase 才出现、哪个 phase 真的修掉、哪个 phase 假装修掉但又复发。**daily delight 不是产品成功的指标,weekly/phase-end trust 才是** —— "当我回来时,这份 archive 仍然 feels fair, useful, and mine"。

**一百万人这样用时,人机协作多出一种礼仪**:参与工作的一方(无论人类还是 agent)都要留下可回看的协作证词。但这是一条远 vision,v0.1 不需要它就有意义 —— **聚焦 single-operator dogfood 这个 narrow slice,multi-reader / 团队扩展全部留给 §4 extension**。

## 2. Novelty assessment

**Novel slice**(同空间新切法)。

记录 friction、observability、self-monitoring agent 都不是新概念 —— LLM observability 行业(Langfuse / Helicone / Phoenix / Pydantic Logfire / Datadog LLM / Confident AI / Braintrust)在 2026 已工业化;incident timeline 自动 witness(Atlassian)早是成熟模式;dogfooding feedback log(PostHog / Martin Fowler feedback flywheel)是工程实践标配。GPT R2 search 还找到 Atlassian 把 incident timeline 描述为"实时记录组合 manual entries + alerts + acknowledgements + automatic updates"—— 这就是 auto-witness 的先例。

**真正"haven't seen this before"在两个层面叠加**:(1)**social position 反转** —— operator 写 entry 是抱怨工具,agent 写 entry 是参与者承认"我刚才让协作变难,或我被环境绊住"。friction-log 因此从"记忆辅助物"升级为"协作契约":谁在场,谁就有责任留下可复盘的证词;(2)**架构反转** —— 主流 LLM observability 是"product team 监控用户用 LLM 服务"的多人架构,这条 fork 是"同一个人既是 user 又是 dogfooder 又是审阅者"的 1:1 架构。两侧 R2 search 都确认:**market 上没有"agent 自己 emit + 1:1 dogfood"形态的工具**。

novelty 在 execution 而非 concept,但这个 execution 的价值脊柱是身份反转 + 架构反转的叠加 —— 两侧 R2 收敛到"agent-generated review evidence with human adjudication"这一表述,这是**两位 debater 都没在 R1 单独说出来、但在 cross 后独立收敛到的同一句话**,它是这个 idea 的真正名字。

## 3. Utility — concrete usage scenarios

**场景 1 · 周三下午,锁文件坑(Opus 视角)**:operator W2 周三下午跑 task T012,parallel-builder 在 BLOCKED 状态卡 7 分钟。他的本能是切换到另一个 task 把 T012 暂时搁置。一周后他打开 v4-friction-log.md 看到 agent 已经记了 "T012 BLOCKED · stale lock file in worktree-T012/.git/index.lock · session 7m22s no progress"。**他没动手,记录已经在那里了**。第一反应:"对,锁文件我没清";第二反应:"这条以前从来没记下来过"。他立刻去修 hook 自动检测过期 lockfile,不再 4 周后被同样的坑撞。他跟朋友说:"我不是回忆哪里烦,是在审一份现场笔录。"

**场景 2 · 周五审阅者复盘(GPT 视角)**:operator 连续五天跑 dogfood,周五打开 friction-log 时看到十几条 agent 证词。他做的不是写新 entry,是**给证词打勾、划掉、补一句人的体感**。某条 agent entry 写"spec_validator 拒绝但错误信息只有 'failed at line 23',没指明哪条 constraint 违反",他在旁边补一句"对,而且我那次手动跑 --verbose 才知道是 C-OQ-3 缺值,这事让我多花了 20 分钟"。**消失的是"周五复盘没素材可写"这件事**。他跟朋友说:"我不是从零回忆哪里烦,是在审一份现场笔录,然后补我自己的体感。"

**场景 3 · 接近 D5 的图案识别(Opus 视角)**:operator 跑 dogfood 第 8 周,接近 D5 12 周硬条件。打开 friction-log 一看,agent 累计记了 90 条。grep `block-dangerous` 发现有 12 条都是 "Claude 想跑某个命令被 hook 拦截但拦截信息缺乏 context (operator 不知道为什么被拦)"。**他立刻看到 gap-1 production credential 隔离的真实威胁不是"凭据泄漏"——而是"operator 不知道 hook 到底在防什么"**。他跟朋友说:"比起 retrospective 报告,真正给我洞察的是 friction-log 自己 —— 它让我 4 周后能看到自己 4 周前看不到的图案。"

**场景 4 · meta:用 V4 retrospective skill 复盘 V4 retrospective skill(Opus 视角)**:operator 在做 retrospective skill 自身的开发。他跑 L2 phase retrospective,skill 输出明显是 placeholder("phase X 的实际改动如下:[需要补]")。agent 此时识别 "skill 输出 placeholder = friction" 并 emit。一周后看 friction-log,这条触发了 "把 placeholder 检测做成 retrospective skill 自身的内置 verification" 的 V4.1 改进。**这是 self-monitoring primitive 的最纯粹场景:用 retrospective skill 复盘 retrospective skill 自身的失败**。

**场景 5 · 误报(uncomfortable scenario,直面)**:operator 跑某个 task 时**故意**让一个 hook 失败(为了调试 hook 的拦截逻辑)。agent 此时如果不知道这是故意的,会 emit 一条 friction entry。operator 周五看到时第一反应是"等下,这条不是 friction,是我故意触发的"。**他怎么处理这条决定 v0.1 的成败**:如果他能轻松标记"这条不算 / 关掉" → trust 不动摇;如果他必须打开文件手动删 → 第二周就关掉 hook。这是 OQ-1 的核心场景 —— 也直接呼应 GPT search 引到的 quantified-self 弃用研究"abandonment linked to perceived data inaccuracy/uselessness"。

## 4. Natural extensions(the long shadow)

**1 个月内可见**(v0.2 / v0.3):

- **审阅入口的回路化**:每条 agent entry 旁边可标"同意 / 不同意 / 漏重点 / 需补充";被标"漏重点"的 entry 累计到一定数量,触发 emit 阈值的自适应调整(让 agent 学到"我之前没记的这类事,operator 想我记")
- **friction tier**:agent 给每条 entry 打 tier(blocking / annoying / cosmetic),retrospective 时按 tier 加权
- **跨 session 记忆**:同类摩擦连续出现时,从孤立事件变成 recurring pain;让 operator 追踪模式,不是每次从零抱怨

**2-3 个月内可见**(v0.4 - v0.6):

- **friction-log → friction-graph**:phase 结束时聚类,出一份 cluster 报告(哪些工具 / 阶段是 friction 重灾)
- **multi-agent emit**:不只 Claude session,parallel-builder agent / spec-validator / pre-commit hook 都自报 —— 但都要遵守同样的"agent 提名 + human 审阅"协议
- **entry → fix-issue 自动化**:一条 friction(被 operator 确认后)触发自动开 issue / 草稿 PR / 给 retrospective skill 加 verification

**6-12 个月可见**(v1.0 + 远 vision):

- **跨 dogfood 实例的元 friction-log**:多个 dogfood 周期(V4 / V5 / V6)的 friction-log 聚合,看哪些 friction 一直没修复
- **shared immune memory**:多个 operator / 团队的 friction archive 聚合(GPT R2 push back 这条不该 dominate L3 —— 远期 vision 而非 v0.1 设计)
- **新 operator 接手的 onboarding artifact**:她跑同一路径前先读上周 agent-written entries,标出高频摩擦,跑完后对照自己的体感(GPT R1 scenario 3 —— Opus R2 push back 这条对当前单 operator 场景过于多人化,留作 §4 extension 而非 v0.1 utility)

## 5. Natural limits(the protective fence)

**它不该是什么 —— 这些 limit 帮助 L3 正确 scope**:

- **它不是全知监控**:agent 不是心理医生、管理者或裁判,只能说"我看见了什么卡点",不能替人解释情绪。GPT R1 这一条与 GPT R2 search 引的 electronic monitoring meta-analysis(85 项研究,小但显著的负面效应)精准对齐。
- **它不该吞掉 human entry**:最强日志是双声部,不是 agent 独唱;否则会整齐但失温。CLI fallback 不是 v1 的 deprecated 功能,是 v0.1 就要保留的 right-of-reply。
- **它不该记录一切**:太多证词会制造新的阅读摩擦。GPT R2 search 的 quantified-self 弃用研究证明"effortless capture is not enough" —— 信号噪声比比 capture 成本更决定第 2 周是否还开着。
- **它不适合追责文化**:一旦 log 被当成问责材料,witness 立刻变味。但 Opus R2 push back:在单 operator 场景里"追责"无对象,把这条说得太重会让读者以为 v0.1 已有这个风险 —— 留作 multi-user 扩展时的 explicit guardrail,v0.1 内部不需要为它做工程
- **它不替代 operator 主观感受**:agent 看到 tool 失败,看不到 "我心里觉得这流程不对"。后者必须由 operator-fallback CLI 兜底
- **agent 的 "是 friction" 判断永远是 fuzzy 的**:它会漏(以为是正常错误)、会误报(明明是用户故意制造的失败)。**100% recall / precision 都不是目标**;v0.1 应明确选择 precision over recall(因为 false positive 的成本是 trust loss,远大于 miss 的成本)
- **它不是 enterprise observability 平台**:不要跟 Langfuse / Helicone / Phoenix 正面竞争。差异化必须立在 "single-operator dogfood + friction-as-relational-artifact" 这个 narrow slice
- **超出 dogfood 模式它就退化为日志膨胀**:如果 operator 不在 dogfood 模式(只是日常用 agent 改改东西),agent 自动 emit 没有读者。**需要明确开关 / 默认 off,只在 dogfood 阶段 on**

## 6. Validation status

### Prior art landscape

| Name | Status | What it does | Lesson for us | URL |
|---|---|---|---|---|
| Claude Code `PostToolUseFailure` hook | Documented + 工业化(2026) | tool 失败时 fire,可附 cause-of-error context,允许写文件,带 `duration_ms` 字段 | **载体已落定**,不需退到 wrapper script;Opus q1 GREEN | https://code.claude.com/docs/en/hooks |
| LLM observability 平台(Langfuse / Helicone / Phoenix / Pydantic Logfire / Datadog LLM / Confident AI / Braintrust) | 已工业化 | tracing + evaluation + 部分支持 AI 自己 query observability data via SQL | 多人架构,不是我们的 slice;不要正面竞争 | https://www.confident-ai.com/knowledge-base/top-7-llm-observability-tools |
| Atlassian incident timeline | 成熟 | 实时记录组合 manual entries + alerts + acknowledgements + automatic updates,用于 postmortem | auto-witness 在 incident 域有先例;agent self-emit 仍是新切法 | https://www.atlassian.com/incident-management/postmortem/timelines |
| PostHog dogfooding | 团队实践 | public feedback + tight feedback loops + 把内部用户当 customer | dogfooding 工作前提是 entry 进入决策回路,不能成 inert archive | https://newsletter.posthog.com/p/using-your-own-product-is-a-superpower |
| Pydantic Logfire AI observability | 已发布 | AI agent 可以 SQL 查询自身 trace | 同向但不同 slice(开发者监控产品而非自我 dogfood) | https://pydantic.dev/docs/logfire/get-started/ai-observability/ |
| Martin Fowler feedback flywheel | 写作 + 推广 | 把 friction log 列为 "reducing AI friction" 核心实践 | friction log 这个 artifact 工业上有先例;agent 自动 emit 形态没有 | https://martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html |
| 2026 trust layer / agentic AI evidence | 概念已工业化 | OWASP Top 10 for Agentic Applications 2026 已发布;Secretariat 把 agent 行为 framing 为法律 evidence | "agent 当 witness" 不是 fringe,是工业化的 trust layer | https://secretariat-intl.com/insights/agentic-ai-as-evidence-when-autonomous-systems-become-witnesses-in-investigations/ |

### Demand signals

| Source | Signal | Strength | URL |
|---|---|---|---|
| forge 006 路径 2 playbook W2 step 4 | "每次 V4 retrospective skill 跑得不顺畅就 jot 一笔到 friction-log" 是 explicit 要求 | **H** | (内部 playbook) |
| autodev_pipe V4 frozen + 12 周 + checkpoint-01/02/03 节奏 | 12 周窗口需要可信 friction 信号支撑 retrospective | **H** | (内部) |
| PostHog dogfooding 文档 | "tight feedback loops are non-negotiable for dogfood credibility" | M | https://newsletter.posthog.com/p/using-your-own-product-is-a-superpower |
| Martin Fowler feedback flywheel | friction log 被列为 reducing AI friction 核心实践 | M | https://martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html |
| 80% IT leaders 报告 agent 行为意外(2026) | trust layer / agent self-evidence 进入工业化讨论 | M | (Trust Layer field report 综合) |

### Failure cases

| Name | Status | Why it died / risks dying | Avoidance for us | URL |
|---|---|---|---|---|
| Quantified-self / activity tracker abandonment | 159 名 ex-用户研究(Attig & Franke) | abandonment linked to perceived data inaccuracy/uselessness + loss of motivation | 默认 precision > recall;v0.1 必须有标记/审阅入口让 operator 修不准的 entry;week-2 retention 监控 | https://research.uni-luebeck.de/en/publications/abandonment-of-personal-quantification-a-review-and-empirical-stu/ |
| Electronic workplace monitoring | 85 项研究 meta-analysis | small but consistent adverse effects on stress / perceived control / satisfaction / trust;participation + justification + positive feedback 减少伤害 | "agent witness" 必须 feel self-owned + justified,不是 surveillance;default 是 operator 私有的 log,不是 default 共享 | https://link.springer.com/article/10.1007/s41449-018-00140-z |
| Error reporting in safety-sensitive contexts | 系统综述 | fear/self-preservation + negative perceptions of org/leadership 是主要 barrier;reporting rises with confidence + knowledge + positive safety perception | log 必须明确 learning-oriented,不是 blame-oriented;v0.1 不接入任何"自动开 issue"自动化 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10120817/ |
| Anthropomorphic AI without trust calibration | Carter / Loft / Visser 研究 | anthropomorphic appearance alone 不提升 trust;有意义的 uncertainty communication 才提升 trust calibration | entry tone 必须 expose uncertainty + reason("我不确定这是 friction 还是你故意触发的"),不要假装权威 | https://journals.sagepub.com/doi/10.1177/00187208231218156 |

### Net verdict

**Should this exist? Y-with-conditions**

evidence 强支持 dogfooding feedback loop、incident timeline auto-witness、psychologically safe reporting 都有真实价值;载体(`PostToolUseFailure` hook)是 documented 工业化的;市场上没有 "agent 自动 emit + 1:1 dogfood" 形态的对手。但同样强的反向证据(quantified-self 弃用 + electronic monitoring meta-analysis + error-reporting safety review + trust calibration 研究)反复警告:**effortless capture 不能保证 adoption** —— 如果 entry 让 operator 觉得不准 / judge / surveillance,他会在第 2 周关掉 hook。

#### Conditions(v0.1 必须满足才算 Y;任意一条 fail 则退回 unclear)

1. **人类审阅入口在 v0.1 而非 v0.2**:operator 必须能对每条 agent entry 标 "同意 / 不同意 / 漏重点 / 需补充"。这不是 polish,是产品决策级 hard requirement。工程量从 50 行涨到 ~150-200 行 (entry id + 状态机) —— 接受这个成本。两侧 debater 在 R2 独立收敛到这一条。
2. **Entry tone 暴露 uncertainty + reason**:agent 不要假装权威。entry 应明确表达"我观察到 spec_validator exit 2 with stderr X,我推测这是 friction 因为 Y,但你可能有不同看法"。trust calibration 研究强支持这一条。
3. **Operator trust monitoring 是 v0.1 的内置 metric**:第 2 周 operator 是否还开着 hook、有多少条被标"不同意"、有多少条被 operator 主动关闭 emit —— 这些信号必须可见。没有 feedback signal 等于 v0.1 飞行盲。
4. **Default scope 是 single operator dogfood**:multi-reader / 团队共享 / 跨 dogfood 实例聚合 / 共享 immune memory 全部留给 §4 extension。default 是 operator 私有 log,不是 default 共享。

---

## 7. Open questions for L3 / for user research

L2 解不了的问题,按**决策紧迫度**分组。

### A. 必须在 L3 解决的(scope 取舍直接定 v0.1 形态)

| # | Question | Best answered by | Why it matters |
|---|---|---|---|
| OQ-1 | v0.1 scope 是否包含人类审阅入口?(同意 / 反驳 / 补充)| L3 + 用户访谈 | 解决 GPT 指出的 anxiety;但工程量从 ~50 行涨到 ~150-200 行(需 entry id + 状态机)。**§6 condition 1 已定为 must-include,L3 主要是工程量取舍 + 数据格式而不是要不要做** |
| OQ-2 | friction signal 判定规则用静态规则(基于 hook 类型 + 退出码)还是 LLM-driven? | L3 + 用户访谈 | 后者准但慢且贵。precision over recall 已在 §6 condition 4 定调,这里是具体规则集 |
| OQ-3 | event 覆盖范围 v0.1 选 [a] 仅 PostToolUseFailure / [b] PostToolUseFailure + skill placeholder 检测 / [c] 全 lifecycle? | L3 | 范围越大 ship 越慢;[a] 一周可发,[c] 至少 3 周 |
| OQ-4 | log 路径 v0.1 强制是 `docs/dogfood/v4-friction-log.md` 一个绝对路径,还是可配? | L3 | 直接关联是否能跨仓 ship 到 ADP(后者无 docs/dogfood/ 目录);影响 OQ-5 |
| OQ-5 | 先 ship 给 IDS 自用,还是先 ship 给 ADP V4 dogfood 用? | L3 + forge 006 路径 2 决策 | ADP 那边 V4 dogfood 处于第 0 周不能动 → 4 周等待期。这条直接锁住 forge 006 路径 2 的 timeline |
| OQ-6 | log 默认 private to operator 还是 shared by default in retrospective artifacts? | L3 + 用户访谈 | electronic monitoring meta-analysis 警告 default-shared 会让 entry 变 surveillance 味。§6 condition 4 已定 default private,L3 主要是 sharing 入口怎么做 |

### B. 不必 L3 解决但应该带着进 L3 / 早做用户访谈

| # | Question | Best answered by | Why it matters |
|---|---|---|---|
| OQ-7 | operator 4 周后更信任哪类 entry(自己当场写的 / agent 当场写的 / 经人确认的叠加)? | 用户访谈 / 实际 4 周后回看 | 决定 entry 格式优化方向(grep-friendly metadata vs prose) |
| OQ-8 | agent 作为 witness 时,什么语气最让人安心(冷静事实 / 第一人称承认 / 带不确定性观察)? | 用户访谈 / A/B | trust calibration 研究强烈倾向第三种,但需用户确认 |
| OQ-9 | operator 第 2 周后是否仍开着 hook?他感受是 relieved / watched / both? | 实地观察(week-2 后第一次访谈) | 直接验证 §6 condition 3 的 trust monitoring;**这条 Opus 和 GPT 的 OQ 完全重合** |
| OQ-10 | 误报 5 条会让 operator 选 [a] 手工删 [b] 调宽阈值 [c] 直接关 hook? | 用户访谈 | 决定 OQ-2 的偏好 —— noise tolerance 上限 |
| OQ-11 | 这条 idea 的最大价值是"减少漏记"还是"让 agent 承担协作见证责任"? | 哲学/产品决策 | Opus 倾向 v0.1 显式选"减少漏记"(可测量),GPT 暗示后者(更深);**操作目标 vs 哲学描述的取舍** |

### 关于"是否需要先做用户访谈再 L3"

**强建议**:OQ-7 / OQ-8 / OQ-10 在 L3 之前做一次 30-60 分钟 self-interview(operator 即真实用户)能极大降低 L3 rework。GPT R2 §6 列出的 3 个访谈问题可以直接拿来用:

1. "Here are three agent-written entries from your own session. Which do you agree with, which would you edit, and which feels unfair?"
2. "After one week and 20 entries, which entries changed an actual decision? Which ones would make you turn this off?"
3. "Would you keep this enabled if only you read it? What changes if a reviewer or future teammate reads it too?"

这些问题答好了再进 L3,scope 决策会更扎实。

---

## 8. Decision menu(for the human)

### [1] Scope this idea — proceed to L3
```
/scope-start 007a-agent-emit
```
**推荐路径**(verdict 是 Y-with-conditions,4 条 condition 清晰可拿进 L3 做 scope 决策)。L3 会拉入你的真实约束(forge 006 路径 2 timeline、IDS-vs-ADP 优先级、单仓还是跨仓 ship 等)。

进 L3 前建议先做一轮 self-interview(见 §7 末尾),降低 rework。

### [2] Fork another L2 angle from this same idea
```
/fork 007a-agent-emit from-L2 <new-angle> as <new-id>
```
读完报告后如果觉得有更锐利的切法可以再 fork。当前两位 debater 的 cross 已经把"agent 提名 + human 审阅"这个脊柱扎得很稳,fork 必要性不强 —— 但若你想单独探"v0.1 不带审阅入口、纯 silent log"或者"全 lifecycle 覆盖而不只 PostToolUseFailure",fork 是可考虑的。

### [3] Back to L1 menu — pick another inspired direction
```
/status 007
```
看看 L1 menu 其他 5 条 directions(`007b-team-heat-mirror` / `007c-mirror-on-write` / `007d-complaint-license` / `007e-inline-comment` / `007f-future-self-trail`)。如果读完本报告觉得另一条更对路 —— 比如 `007d-complaint-license` 的"心理许可"框架其实更直接戳到第 2 周关 hook 的痛 —— 也是合理选择。

### [4] Re-explore with new input
```
/explore-inject 007a-agent-emit "<your steering>"
/explore-next 007a-agent-emit
```
如果觉得本报告漏了某个角度(比如"我想看跨 dogfood 实例聚合的 vision 怎么落"或"我想多查一些 self-tracking 弃用模式的细节"),inject 后再跑一轮 L2R3。

### [5] Park
```
/park 007a-agent-emit
```
所有 artifacts 保留。**适用场景**:verdict 是 Y-with-conditions 但你想先去聊聊真实用户(自己 + 1-2 个同行)再决定 scope —— 这是合理的等待。

### [6] Abandon
```
/abandon 007a-agent-emit
```
**不推荐**(verdict 不是 N)。如果决定 abandon 应该写明 lesson(为什么 Y-with-conditions 仍然不做 —— 是 conditions 太重?是 forge 006 路径 2 timeline 不够?是另一条 fork 更值?)。L1 menu 其他 5 条 sibling forks 不受影响。

### [V] Show full
完整报告即本文档,读到这里就是。

---

## Fork log

(updated by /fork command for any sub-forks of this L2)
