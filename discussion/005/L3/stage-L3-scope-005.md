# L3 Scope Menu · 005 · 「PRD-to-confidence framework(不是 PRD-to-code 工厂)」

**Generated**: 2026-05-07T03:15:00Z
**Source**: L2 report(stage-L2-explore-005.md, verdict=Y-with-conditions)+ L3R0 intake + L3R1×2 + L3R2×2
**Rounds completed**: L3R1(Opus + GPT)、L3R2(Opus + GPT)
**Searches consolidated**: 17 条 scope-reality 检索(8 类对照产品)
**Moderator injections**: 无(005 走 skip-mode 直入 L2,标准 advance,非 redebate)
**Fork origin**: 无(005 是 root idea,经 `/inspire-start --mode=skip` 直入 L2)

---

## How to read this menu

这是 L3 的产出:idea 005 的**候选 PRD 菜单**。3 个候选**地位平等**(peer,不是"主选 + 备胎")——它们在你 L3R0 给出的硬约束下,都是合法的 v0.1 切片,只是切的角度不同。

人类下一步:fork 一个(或多个)进入 PRD 分支,然后 `/plan-start` 进 L4。

```
/fork 005 from-L3 candidate-A as 005-pA
/plan-start 005-pA
```

允许 fork 多个并行做(每个 PRD 一条线,L4 独立推进)。

---

## Executive summary

- **两轮辩论罕见地收敛到同一个 tradeoff 轴**——Opus 称之为"v0.1 在哪个时间维度上交付价值(分钟级 / 小时级 / 月级)",GPT 称之为"v0.1 先卖单次项目的可信推进感 vs 先卖跨项目的个人工程判断记忆"。两种描述是同一根轴的两个侧面,互相印证。
- **3 个候选地位平等(peer)**:A · PRD Clarifier(单次项目即时价值,6-8 周)/ B · Solo Confidence Map(单次 build run 的可视化交付信心,9-12 周)/ C · Confidence Journal(跨项目长期 calibration,9-13 周)。3 个都尊重 L2 §6 的 5 条 Y-with-conditions 硬约束。
- **关键搜索 verdict**:A 的市场是真空白(GitHub Spec Kit 已做 `/speckit.clarify`,但**没有**单人开发者 PRD 信心产品);B 的甜蜜带很窄(agent observability 已被 Datadog/Splunk/Maxim/Salesforce 占满,005 的 B 必须以"个人视角"区分,严格不做 token/trace/performance);C 的差异化只能是"开发者判断特定 calibration"(Mem0/Personal.ai/Rewind 已是通用 personal memory baseline)。
- **关键分歧已收敛**:Opus R1+R2 主张 A 完全 stateless,GPT R2 反推——A 必须留"用户裁决记录作为 calibration seed",否则违反 L2 §6 抗重做硬约束、且面对 Spec Kit 容易被读成"独立包装"。本菜单**采纳 GPT 的修正**:Candidate A 含 calibration seed(可导出的决策记录),不做完整 profile。
- **Synthesizer 推荐**:**A 作为 v0.1 主推,但 A 的设计必须为 B/C 演化留 hook**——这等价于 Opus R1 §4 的 Option 4/5(A→B 或 A→C 渐进路径)。3 个候选**不是互斥世界观**:A 是最可控 v0.1,B 是 A 的可视化产品化层(更适合 v0.2),C 更像 v0.2 长期护城河。详见 §"Synthesizer 推荐"。

---

## Intake recap — 我们尊重了什么

### Hard constraints(✅,每个候选都遵守)

1. **Persona = ML 研究员/PhD 型 + 独立创业者并集**——必须显式处理两者张力(A 偏 Persona A 但导出报告需 Persona B 也能读;B 偏 Persona B 但保 CLI 入口给 Persona A;C 切两者交集)
2. **Form factor 是 L3 的真实差异轴**——3 个候选以 form factor 切片(A=CLI/skill / B=Web dashboard+CLI / C=Desktop 本地优先)
3. **R1-R3 已确认红线**:不代写 PRD / 不做 human-out-of-the-loop 黑箱交付 / 不做多人协作(>2 人)
4. **L2 §6 五条硬约束**全部贯穿:
   - (1) scope 收紧到两个 novelty 缺口(ambiguity policy + 用户级 calibration)
   - (2) ambiguity policy 是产品核心语言,不是隐含行为
   - (3) 必须 human-on-the-loop("几乎没有低价值人工陪护",不是"几乎没有人工干预")
   - (4) 抗重做硬约束(v0.1→v1.0 不能推倒重来——所以 A 必须留 calibration seed,不能完全 stateless)
   - (5) "可信赖输出"硬标准必须在 L3 定义(L3 给 stub,L4 落具体阈值)
5. **Polish > Speed**——v0.1 即使小也要"拿得出手",没有"先粗后精"的妥协空间(每个候选的 Polish 集中点都已显式标出)
6. **Differentiation > Broad appeal**——宁可少服务一类用户,也要把 ambiguity policy + 用户级 calibration 两个 novelty 打深

### Soft preferences(强信号)

- 周投入 ≈ 25 小时/周(中位数,区间 20-35)——所有时间估算按此倒推
- 商业模式不锁死(免费 v0.1 + 留付费 tier 路径)——scope 不必预留 hook,但避免硬绑定免费 LLM API 这种"未来不可能商业化"的决定

### ❓ items 由本菜单解决的部分

| ❓ 项 | A 的处理 | B 的处理 | C 的处理 |
|---|---|---|---|
| 目标交付时间 | 6-8 周(乐观 5w/现实 7w/悲观 10w) | 9-12 周(乐观 8w/现实 11w/悲观 15w) | 9-13 周(乐观 7w/现实 10w/悲观 14w) |
| Form factor | CLI / Claude Code skill | Web dashboard(CLI 入口同等重要) | Desktop / 本地优先 |
| Calibration 何时入场 | seed 形式(导出决策记录) | 薄层(项目内一致性提醒) | 双层(单项目日志 + 跨项目自动 calibration) |
| Polish 集中点 | ambiguity 分类精度 + 报告可读性 | 信心地图视觉语义 + 决策审计页自我解释 | 信心日志结构化 + 个性化提醒诚实度 |
| 持久度轴 | stateless + seed | 单项目内累积 | 跨项目累积 |

### ❓ items 仍开放给人类(本菜单无法替你决定)

1. **R4 红线打包选哪套?** GPT R1 §4 给了 3 套打包,你需要在 fork 前挑(或在 fork 后写进 PRD):
   - **保守包**:同时接受"不一句话生成 app"+"不实时同屏协作"+"不面向 50 人+大团队/强监管行业",v0.1 守窄而深
   - **产品化包**:接受前两条,但暂缓第三条(给未来商业化留观察空间)
   - **个人工具包**:接受第一条+第三条,把"不一句话生成 app"写进 onboarding 文案,作为产品定位声明
2. **Persona A 和 Persona B 的真实占比?**——直接影响选 A(偏 A)、选 B(偏 B)、还是选 C(交集)。L2 §7 第 1 题已标"必须用户访谈才能答"——只能你自己访 5 位目标用户后定
3. **用户会不会回来读自己的画像/日志?**——这是 C 的核心赌注(L2 §7 第 7 题)。访谈不到这个信号,直接做 C 就是 high-risk bet
4. **"可信赖输出"硬标准的具体阈值?**——L3 只能给 stub(passing tests / coverage / human 抽查比例 / NPS 等指标的语义),具体数字必须在 L4 spec 阶段定
5. **目标用户当前用什么工具 + 工作流?**——影响入口设计(假设用 Claude Code/Cursor/agent-skills,但若实际用 Devin/Sweep,3 个候选的集成方式都要重做)

---

## The single biggest tradeoff axis

**轴的名称**:**「v0.1 先把价值锁在哪个时间维度上」**

具体含义:三个候选的真正差别不在形态(CLI/Web/Desktop),也不在 Persona 重心——是它们**让用户感到"这个工具有用"的时间尺度不同**:

- **A · 单次 PRD 写作的瞬间(分钟级)**——用户跑完一次拿到 ambiguity map + 信心报告就立刻有用,不依赖回看历史、不依赖 calibration 累积。**成败标准 = "PRD 写完后是否更清晰"**
- **B · 单次 build run 的几小时(小时级)**——用户离开屏幕几小时回来看「信心地图」,价值在"知道这段时间发生了什么 + 哪些我现在该回来拍板"。**成败标准 = "异步离开屏幕后回来是否更安心"**。依赖用户开夜间 run 而不是同步盯着
- **C · 多个项目跨度的几个月(月级)**——用户跑多次后看到自己被理解。**成败标准 = "用户是否长期回来 + 第 3 个项目起 calibration 是否真的提醒得上"**。依赖用户长期使用 + 愿意回看个人画像

**这三个标准没法同时成立**——它们对应不同的 v0.1 测试方法、不同的早期用户画像、不同的 N=5 用户访谈问题。**这是 human 必须主动选的**。

---

## Candidate PRDs

### Candidate A · 「PRD Clarifier + 信心报告」

**Suggested fork id**: `005-pA`
**Sources**: Opus R1+R2 的 Ambiguity Forge + GPT R2 的 PRD Clarifier 修正(采纳 GPT 关于 calibration seed 的 push back)

**v0.1 in one paragraph**:
一个 CLI 工具 / Claude Code skill,**专做一件事**:扫描你写好的 PRD,产出一份 **ambiguity map + 一页信心报告**——明确列出 PRD 在哪些位置 underspecified、每处给"必须问 / 推断+TODO 标 / 暂停"三选一建议、最后导出 `prd.refined.md` + `assumptions.md`(推断清单可作下游审计依据)+ 一份**用户裁决记录**(每次的"必须问/推断/暂停"选择)作为 **calibration seed**——不做完整 profile,但**为后期 fork 出 B 或 C 留导出 hook**(符合抗重做硬约束)。它**不写代码**、不接管 build、不做 dashboard、不做完整画像。它是站在 PRD 和现有 agent-skills 中间的一道安检。

**User persona**:
**林博士**,ML 博士第 4 年,实验室同事,手头有一份"把组里 RL 训练流水线变成内部工具"的 PRD 草稿。她能写清"输入输出+成功标准",但不知道"支持 multi-GPU 训练"该具体到 NCCL 还是只说功能。她想在丢给 agent 之前**先让一个东西告诉她她的 PRD 哪里还不够**。副 persona 是独立创业者 Maya——她也用 CLI,但需要导出报告"能给一位合作者读"。

**Core user stories**:
- 作为林博士,我可以 `prd-forge analyze ./my-prd.md`,几分钟内拿到 ambiguity map + 一页信心报告,在跑 agent 前先补好 PRD
- 作为林博士,我对 ambiguity map 每一项都可以**接受/修改/拒绝**它的建议,生成 `prd.refined.md` + 我的裁决记录
- 作为 Maya,在把 PRD 丢给 Claude Code 之前,我可以走一轮 5-10 分钟的 `--interactive` 对话式补漏,产出**敢丢给 agent** 的版本 + 一份能发给合作者的信心报告
- 作为林博士,完成后我可以查看"推断假设清单",事后审计 agent 是不是真按这些推断做的
- 作为回访用户,我的过往裁决记录已被保留(seed),未来若升级到 B 或 C,这些记录可被自动导入(抗重做)

**Scope IN(v0.1)**:
- PRD ingest(markdown / 自由文本)
- 结构化 ambiguity 检测(分类:输入定义不全 / 边界缺失 / 非功能需求模糊 / 验收标准未量化 / 依赖关系隐含)
- 每处的"必须问 / 推断+TODO / 暂停"三选一裁决
- Interactive mode(对话式补漏,5-10 分钟中位时长)
- 输出 `prd.refined.md` + `assumptions.md` + 一页**信心报告**(给用户自己 / 一位合作者 / 自己未来回看)
- **裁决记录**导出(JSON,作为 calibration seed,留 hook)

**Scope OUT(显式 non-goals)**:
- **不写代码**——PRD 之后交给 addy osmani agent-skills / Claude Code 原生 skill,不重做工程纪律
- **不做 dashboard / GUI**——CLI 输出 + markdown 报告,polish 集中在分类精度和报告可读性
- **不累积完整用户画像**——v0.1 只做 seed(裁决记录),不做跨项目 calibration profile
- **不做项目级 codebase lore**——只看一份 PRD,不读 codebase
- **不做付费层 / billing**——免费 OSS

**Success looks like(可观测)**:
1. 在 5 份代表性 PRD 上跑,每份发现 ≥5 处真实 ambiguity,≥80% 被作者认可有意义
2. Interactive mode 中位时长 ≤ **8 分钟**
3. 使用 ambiguity-refined PRD 跑 agent build 比直接跑节省 ≥30% 返工(基线对比)
4. 5 位非 human 自己的早期用户中,≥4 位认为信心报告"能阻止明显返工"
5. 首次用户在 ≤45 分钟内完成一次 PRD 预检 + 关键裁决

**Time estimate under your constraints**:
25 小时/周 × **6-8 周** = ~150-200 小时(乐观 5w / 现实 7w / 悲观 10w)
Confidence: **H**——单一 surface,不依赖大架构;比 R1 的 5-7w 多 1w 留给"导出报告 polish"和 calibration seed 的最薄实现

**UX priorities(tradeoff stances)**:
- **少而精**:CLI 输出每行都该有用,不堆"为了完整"的废话
- **诚实优先**:遇到不确定就标"low confidence",绝不靠 hallucinate 撑门面
- **报告必须像专业交付材料**(不是聊天记录)——这是 P2 Polish 的着力点
- **可被脚本化**:ambiguity map 是结构化 JSON+ 人类 markdown 双输出
- **裁决记录可导出**:用户随时可拿走数据,不被锁定

**Calibration stance**: **Seed**——记录每次裁决,不做画像;为 B/C 演化留 hook
**Form factor**: CLI / Claude Code skill

**Biggest risk**:
**赌"PRD 写作是真痛点"**——若用户真实痛点其实在 build 过程(Devin 路线),A 没切到核心。但 search 显示 PRD 工具市场 ≥10 个生成器、0 个分析器,**这恰是有空缺的信号,不是没需求的信号**。次级风险:GitHub Spec Kit `/speckit.clarify` 已是公开标杆,A 必须把"裁决经济学"产品化(报告可读性 + 裁决记录可导出 + Persona B 也能读)才不被读成"Spec Kit 的独立包装"。

**Scope-reality verdict**:
- **直接对照**:GitHub Spec Kit `/speckit.clarify`(已 ship,要求标 `[NEEDS CLARIFICATION]`,但是 spec-driven workflow 的子步骤,**不是独立 PRD 信心产品**)— [github/spec-kit](https://github.com/github/spec-kit)
- **侧面对照**:ChatPRD / Scriptonia / Keeborg 都做 PRD **生成**(撞 R1 红线),没有 PRD ambiguity **分析**工具
- **Cline / GitHub Copilot coding agent**:都做"人批准每步"的同步陪跑或异步 PR/review,**不积累用户级产品裁决偏好** → 005 的 A 的 calibration seed 是真空白
- **Net read**:**healthy MVP**(非鼓胀,非 undershoot)。市场空白真实,差异化点清晰

**Best fit for human who**:
你想用最快路径验证"ambiguity policy 单点"是否真需求,愿意接受 v0.1 形态较窄(CLI),但要求每个产出都有真实价值;你认可"先做最可控 v0.1,跑 4-6 周用户后再决定要不要加 B 或 C"的渐进路径。

---

### Candidate B · 「Solo Confidence Map」

**Suggested fork id**: `005-pB`
**Sources**: Opus R1+R2 的 Confidence Atelier + GPT R2 的 Solo Confidence Map(采纳 GPT 关于"严格不做 LLM observability"的克制约束)

**v0.1 in one paragraph**:
一个 **Web dashboard**(CLI 入口同等重要),接受 PRD 输入,启动一次完整的 build run,产出代码 + **一张可视化的「信心地图」**——4 个区块(自动推进区 / 必须澄清区 / 事后可审计区 / 暂停区),每个区块下挂着 task / 决策记录 / 测试证据 / 风险标记。底层调用 addy osmani agent-skills 完成 build,Atelier 的核心价值是**信心呈现层** + ambiguity policy 的可视化执行 + **决策审计页(自我解释为什么 agent 选了 A 而非 B)+ 自动 retro 生成(每个 run 完后产 1 页)**。**严格不做** LLM token/trace/performance monitoring(不撞 Datadog/Splunk/Maxim 红海)。calibration 推到 v0.2,但**架构层留 hook**(符合抗重做)。

**User persona**:
**Maya**,独立创业者,有 3 个 demo 想跨到正式产品(其中一个是 SaaS 工具),会写 PRD 但每次 demo→产品中间总散掉。她要的不是"再快 30% 写代码",而是**「我离开屏幕这 6 小时它做了什么 + 哪些我现在该回来拍板 + 为什么 agent 这么选」**的可视化报告。副 persona 是林博士——她不打开 dashboard,但用 CLI 调同一 backend,看 markdown 版的"信心地图导出"。

**Core user stories**:
- 作为 Maya,我可以上传 PRD,启动 run,关掉浏览器去做别的事
- 我打开 dashboard 看到 4 区块的实时状态,**澄清区**有 3 个等我裁决的决策点(每个 3 种选项)
- 我点开**事后可审计区**的某个决策,看到"为什么 agent 选了 A 而非 B"完整推理 + 它执行的 test 证据
- 一个 run 失败后,系统自动产出 1 页 `retro.md`,沉淀进我的"判断历史"(为 v0.2 calibration 留 seed)
- 作为林博士,我用 CLI 跑同一 backend,导出 markdown 版的"信心地图摘要"

**Scope IN(v0.1)**:
- PRD ingest + 一次完整 build run(调用底层 agent-skills,不自己写 build 逻辑)
- 「信心地图」可视化(4 区块的实时状态 + 颜色语义)
- ambiguity policy 引擎(三类决策:打断 / 推断+TODO / 暂停)
- 决策审计页(每个决策的"为什么"+ 证据,自我解释,不需文档)
- 自动 retro 生成(每个 run 完后 1 页 `retro.md`)
- demo→产品化检查清单(为 Persona B 暴露"看起来能跑但不能信"的部分)
- CLI 入口同等支持(Persona A 用)

**Scope OUT(显式 non-goals)**:
- **不重做** spec/test/review/build 工程纪律(直接调 addy osmani agent-skills)
- **不做 LLM observability**(token / trace / latency / performance / errors / token consumption)——撞红海,严格避开
- **不做完整用户级 calibration 面板**——v0.1 只做"项目内一致性提醒"薄层,完整画像推 v0.2
- **不做团队协作 / 多人 dashboard**(R3)
- **不做实时同屏协作**(R4 候选)
- **不做项目类型识别**(L2 §4 扩展项)
- **不做 dark mode 等装饰性 polish**——polish 集中在「信心地图」视觉语义和审计页自我解释

**Success looks like**:
1. Maya 一次完整 run 后,**≤90 秒**回答:它做了什么 / 哪些我要拍板 / 哪些已 ok
2. 用户 90 秒内能说清"能继续什么、要裁决什么、为什么暂停"
3. ambiguity policy 引擎在 5 个真实 PRD 上的"该问 vs 该推断"判断与人工 baseline 一致率 ≥ **75%**
4. 一次完整预检中,系统把问题压缩为 ≤12 个高价值裁决点
5. ≥70% 裁决卡片被用户标记"确实值得我决定"
6. 8-10 位 Persona A+B 早期用户,中位 NPS ≥ +30

**Time estimate under your constraints**:
25 小时/周 × **9-12 周** = ~225-300 小时(乐观 8w / 现实 11w / 悲观 15w)
Confidence: **M**——「信心地图」UI 和 calibration 薄层都是新形态,实际打磨周期不好估;Web dashboard 的 polish 是无底洞,若 P2 不打折易超期到 14-16 周

**UX priorities**:
- **「信心地图」是产品语义,不是装饰**——4 区块的命名/颜色/排布必须反映"我现在该信任什么",每个颜色/状态/卡片都对应一个用户动作
- **审计页要自我解释**——不需要文档,人看一眼能懂"为什么 agent 这么决定"
- **CLI 入口同等重要**——dashboard 是看的,run 入口仍要支持命令行
- **可视化服务判断,不服务表演**——视觉必须服务裁决和信心,不做空洞仪表盘
- **Persona B 的"产品化焦虑"要被正面处理,但不能牺牲 Persona A 的证据密度**

**Calibration stance**: **薄层**(项目内一致性提醒,不做跨项目 profile;架构层为 v0.2 留 hook)
**Form factor**: Web dashboard + CLI 入口

**Biggest risk**:
**Web dashboard + observability 红海误判 = 双重风险**。Mira/Maya 是不是真会**回到 dashboard 看**,而不是只用 CLI?如果 Persona A 占主力,他们大概率不打开 dashboard,Web 投入就是浪费。这强依赖 Persona B 真实存在且会用 dashboard——这是 L2 §7 第 1 题需要 user research 的核心问题。次级风险:agent observability 已被 Datadog/Splunk/Maxim/Salesforce 占满,B 必须**严格守住"个人视角 vs 企业级 SRE/SOC 视角"**的语义分割,任何一卡片若滑入 token/trace/performance 就会被读成"小号 Datadog"。

**Scope-reality verdict**:
- **直接对照(红海)**:Datadog LLM Observability / Splunk AI Agent Monitoring / Maxim AI / Salesforce Agentforce / Google Cloud AI Agent Builder——全是企业级 SRE/SOC 视角(execution flow chart, token consumption, agent health),**不做"单人离开屏幕的信心地图"** — [datadoghq.com](https://www.datadoghq.com/product/ai/llm-observability/) ; [splunk help](https://help.splunk.com/en/splunk-observability-cloud/observability-for-ai/splunk-ai-agent-monitoring) ; [getmaxim.ai](https://www.getmaxim.ai/products/agent-observability)
- **侧面对照**:GitHub Copilot coding agent(异步 PR/review,但不积累用户级产品裁决偏好);Cline(同步陪跑,005 不该做)
- **Net read**:**ambitious**(不是 undershoot,但 scope 偏重;Polish 要求高且容易在 v0.1 阶段失控)。差异化点清晰但窗口窄

**Best fit for human who**:
你认识具体的独立创业者会用、对 Persona B 有强信号(已经访谈过 ≥3 位会用的人),且愿意接受 9-12 周长周期换取"v0.1 即可视化产品"的体验密度;你能严守"严格不做 LLM observability"的克制纪律,不让 scope 滑向红海。

---

### Candidate C · 「Confidence Journal」

**Suggested fork id**: `005-pC`
**Sources**: GPT R1+R2 的 Confidence Journal + Opus R2 采纳 GPT 的"双层日志"组织方式(消解"≥3 项目才有用"的冷启动张力)

**v0.1 in one paragraph**:
一个 **Desktop / 本地优先**的工具,核心组织是 **「单项目信心日志为入口 + 跨项目 calibration 自动生长」**——每个项目从 PRD、歧义、裁决、推断、暂停、复盘形成可回溯账本(单项目就有价值);跨 2-3 个项目后,系统自动从这些日志中**生长出**用户级 calibration 画像(漏 PRD 的常见类目、对 ambiguity 的偏好、翻案率)。第 3 个项目起,新 PRD 写作时主动 surface "按你过往模式这份 PRD 的非功能需求又只写了 1 行,要补吗?"。**它不替代任何现有工具**(不写代码、不做 build、不做完整 PRD lint),是装在所有 agentic-coding 之上的"个人判断元层"。本地优先,数据可导出,不被锁定。

**User persona**:
**陈宇**,CS PhD 转独立产品作者,有多个小项目和研究工具(Persona A+B 交集)。他能写 PRD,也关心 demo→产品,但最痛的是**每个项目结束后经验沉不到下一次**——前 4 次尝试每次都从零搭脚手架,retro 沦为死档案。他要一个工具帮他**积累自己的工程判断,而不是套用社区最佳实践**。副 persona 是 Maya——她愿意用一个本地"交付账本"避免反复重做。

**Core user stories**:
- 作为陈宇,我可以为每个项目维护一条**信心日志**(PRD、歧义点、裁决、推断、暂停理由、复盘结论)——**第一个项目就能 5 分钟内回溯关键裁决的理由和后果**
- 作为陈宇,跨 2-3 个项目后,我可以打开"我的工程判断画像"——漏 PRD 的常见类目、对 ambiguity 的偏好、哪些决策事后被自己推翻过(自动从日志生长,不是冷启动 prompt)
- 在新 PRD 写作时,Journal 主动给出 **3 条最值得关注的 PRD 漏洞**(基于我的过往画像,不是通用 lint)
- 作为 Maya,我可以把 demo→产品的关键裁决留档,以便未来回看为什么当时继续或暂停
- 我可以导出 Journal 数据(JSON),不被锁定;数据本地存储,隐私可控

**Scope IN(v0.1)**:
- 项目级信心日志(PRD 摘要、歧义点、裁决、推断、暂停理由、复盘结论)——单项目即有价值,这是 v0.1 第一屏
- 多源 ambiguity 摄取(Claude Code log / 手动 prompt / agent-skills decision log,通过 hook)
- 跨项目 calibration 画像(自动从日志生长,≥2-3 项目后浮现)
- 新项目启动时的个人化预检(基于历史画像)
- 安静的实时提醒(可关,不打断)
- 极简 ambiguity policy 引擎(只在写 PRD 阶段用,不接管 build)
- 本地数据 + 可导出(JSON)

**Scope OUT(显式 non-goals)**:
- **不替代任何现有工具**——不写代码、不做 build、不做完整 PRD lint
- **不做云端同步 / 多设备**——v0.1 单设备本地
- **不做团队 / 多人画像**(R3)
- **不监听一切**(隐私边界:只摄取用户主动 hook 的信号源)
- **不要求用户先跑 5 个项目才有价值**——单项目即有用(这是 GPT R2 对 Opus R1 C 的核心修正)
- **不在前 2 个项目主动给画像建议**——signal 不够时显式说"还没积累够",不假装智能(这是产品诚实)
- **不做项目级 codebase lore**(addy 已做,不重复)
- **不做通用 personal memory**(Mem0/Limitless/Personal.ai 已做 baseline,C 只切"开发者判断"垂直)

**Success looks like**:
1. **第 1 个项目**:用户 5 分钟内回溯关键裁决的理由和后果(单项目价值证明)
2. **第 3 个项目**:Journal 提出 ≥3 条历史相关提醒,≥50% 被用户认可有用
3. 用户从第 4 个项目起**真的会回来读画像**(打开率 ≥ 60%)
4. 个性化建议被采纳率 ≥ 50%(对比通用 PRD lint 的 baseline)
5. 5 位早期用户中,≥3 位在 5 个月内运行 ≥5 个项目(累积型工具的留存命题)

**Time estimate under your constraints**:
25 小时/周 × **9-13 周** = ~225-325 小时(乐观 7w / 现实 10w / 悲观 14w)
Confidence: **L-M**——picture 算法路径未收敛;且**赌"用户真的会读自己的画像"**这个行为假设(L2 §7 第 7 题);多源摄取 hook 的工程量不确定。比 R1 的 8-12w 略上调,因加了"单项目即有价值"层

**UX priorities**:
- **长期记忆优先于单次惊艳**——每个项目都为下一次留下可调用资产
- **本地掌控感优先于社交传播**——它像个人交付账本,不像团队平台
- **抗重做是核心体验**(不是后期复盘功能)
- **安静优先**:Journal 不打扰、不弹窗、不强 review
- **诚实优先**:signal 不足时**显式说"还没积累够"**,不假装智能
- **数据主权**:本地 + 可导出,任何时候用户可以走人

**Calibration stance**: **完整双层**(单项目日志 + 跨项目 calibration 自动生长)
**Form factor**: Desktop / 本地优先(可与 Claude Code/Cursor/agent-skills 集成)

**Biggest risk**:
**赌"人会读自己的画像"+ "首项目价值是否足够硬"**——L2 §7 第 7 题就是问前者:若用户不读画像,Journal 就是死档案版的 AGENTS.md。GPT R2 的"双层日志"组织方式部分缓解了这个风险(单项目就有价值),但若第 1 个项目的"信心日志"用户感觉"还不如直接记 markdown",日志会被弃用——这是 v0.1 必须打磨的关键体验。这个 cut **最依赖 user research**;直接做就是 high-risk bet。但若赌中,这是 005 真正护城河——其他两个候选都没这层。

**Scope-reality verdict**:
- **直接对照(红海)**:Mem0 v1.0.3(项目级 inclusion/exclusion prompts、memory depth)/ Personal.ai(My AI 主张记住每次对话、学习偏好)/ Rewind(已被 Meta 收购 sunset,印证"个人 memory 工具独立活下来"难度)— [mem0.ai](https://mem0.ai/blog/state-of-ai-agent-memory-2026) ; [personal.ai](https://www.personal.ai/products) ; [techcrunch on Rewind](https://techcrunch.com/2022/11/01/rewind-wants-to-revamp-how-you-remember-with-millions-from-a16z/)
- **关键差异化**:都是**通用** personal memory,**没有"开发者判断特定 calibration"**——005 的 C 必须切这个垂直
- **Microsoft ACE**(L2 已识别)对长期上下文累积有学术支持,但警告 brevity bias / context collapse — calibration 必须可整理、可裁剪
- **Net read**:**ambitious**(行为假设最重,回报最慢)。差异化点清晰但需 user research 验证

**Best fit for human who**:
你愿意赌"长期记忆 + 抗重做"的护城河,且对 ≥5 个项目使用频率有强信心(自己用 + 已访谈 ≥3 位会用的人);你能接受 9-13 周长周期 + L-M 的低 confidence;你认为前 4 次失败的根因就是"经验沉不到下一次",修这个根因比做单次工具更值。

---

## Comparison matrix

| Dimension | A · PRD Clarifier | B · Solo Confidence Map | C · Confidence Journal |
|---|---|---|---|
| Form factor | CLI / Claude Code skill | Web dashboard + CLI 入口 | Desktop / 本地优先 |
| Persona 重心 | A(技术容忍)+ 报告给 B 读 | B(创业者)+ CLI 给 A 用 | A+B 交集(长期掌控) |
| Calibration stance | Seed(裁决记录可导出) | 薄层(项目内一致性) | 完整双层(单项目+跨项目) |
| 时间估算(25h/周) | **6-8 周** | **9-12 周** | **9-13 周** |
| Confidence | **H** | **M** | **L-M** |
| 价值时间维度 | **分钟级**(单次 PRD) | **小时级**(单次 run) | **月级**(跨项目) |
| Polish 集中点 | ambiguity 分类精度 + 报告可读性 | 信心地图视觉语义 + 审计自解释 | 信心日志结构化 + 提醒诚实度 |
| Differentiation source | "PRD ambiguity 分析"是真空白 | "个人视角 vs 企业级 observability" | "开发者判断特定 calibration" |
| 抗重做 strength | 强(seed hook 留 B/C 路径) | 中(架构留 hook,calibration 推 v0.2) | 最强(双层结构本身就是抗重做) |
| 主要 risk | 赌 PRD 是真痛点 + 不被 Spec Kit 覆盖 | scope 鼓胀 + 误入 observability 红海 | 赌"人会读画像" + 首项目价值需够硬 |
| Scope-reality fit | ✅ 真空白 healthy MVP | ⚠ ambitious 窗口窄 | ⚠ ambitious 行为假设最重 |
| 红线遵守 | ✅(R1-R3 全守) | ✅(R1-R3 全守) | ✅(R1-R3 全守) |
| 时间预算适配 | ✅ 舒适 | ⚠ 偏紧(易超 14w) | ⚠ 偏紧 + 不确定性高 |

---

## Validation status — 17 条 search 收敛(取最关键 7 条)

| 类别 | 来源 | 关键发现 | 对 005 的意义 | URL |
|---|---|---|---|---|
| A 直接竞品 | **GitHub Spec Kit** | `/speckit.clarify` 已 ship,要求标 `[NEEDS CLARIFICATION]`,但作为 spec-driven workflow 子步骤 | A 必须把"裁决经济学"+"信心报告"+ 用户裁决记录产品化,不被读成"Spec Kit 独立包装" | [github/spec-kit](https://github.com/github/spec-kit) |
| A 市场空白 | ChatPRD/Scriptonia/Keeborg | 全是 PRD **生成**(撞 R1 红线) | **没有 PRD ambiguity 分析工具**——A 的市场是真空白 | [scriptonia.dev](https://www.scriptonia.dev/blog/best-ai-prd-tools) |
| B 红海 | **Datadog/Splunk/Maxim/Salesforce/Google Cloud** | 全是 SRE/SOC 视角的 agent observability(token/trace/performance) | B 必须严格守"个人视角",任何卡片滑入 token/trace/perf 就被读成"小号 Datadog" | [datadoghq.com](https://www.datadoghq.com/product/ai/llm-observability/) ; [getmaxim.ai](https://www.getmaxim.ai/products/agent-observability) |
| C 红海 | Mem0 / Personal.ai / Limitless(原 Rewind) | 通用 personal memory 已 baseline;Rewind 被 Meta 收购 sunset(印证独立活下来难) | C 的差异化只能是"开发者判断特定 calibration",不能做通用 memory | [mem0.ai](https://mem0.ai/blog/state-of-ai-agent-memory-2026) ; [personal.ai](https://www.personal.ai/products) |
| 同步陪跑被验证不是 005 方向 | Cline Plan/Act / GitHub Copilot coding agent | Cline 已覆盖"人批准每步"的同步陪跑;Copilot 异步 PR/review,但不积累用户级裁决偏好 | 005 应做"低打扰的裁决经济学",不做同步陪跑;**用户级产品裁决偏好是真空白** | [docs.cline.bot](https://docs.cline.bot/getting-started/what-is-cline) ; [github copilot docs](https://docs.github.com/en/copilot/using-github-copilot/coding-agent/about-assigning-tasks-to-copilot) |
| 大方向反向印证 | **Devin v1→v2→v2.2** | v1 chat-only 自主 → v2 加 IDE 让人介入 → v2.2 加 desktop 让 Devin 直接操作。**反向往人靠拢** | 印证 human-on-the-loop 方向对(L2 §6 条件 3 + intake R2);但**Devin 自己可能演化成 005 竞品**——窗口期可能比想的窄 | [cognition.ai](https://cognition.ai/blog/introducing-devin) |
| 需求侧 | L2 已收 Stack Overflow 2025 / arxiv 2502.13069 / METR RCT | 46% 信任缺口、ambiguity-aware +74% 性能、主观顺滑感不可靠 | 005 三个候选都对症,且"诚实优先"原则有学术依据 | (L2 §6 已记录) |

---

## Synthesizer 推荐

**推荐路径:Candidate A 作为 v0.1,且 A 的设计必须为 B/C 演化留 hook(渐进路径)**

理由(2 段):

**第一段——为什么 A 是 v0.1 主推**:A 在你的硬约束下风险最低、confidence 最高(H)、时间最舒适(6-8 周适配 25h/周中位数)。Search verdict 显示 PRD ambiguity 分析是真空白(GitHub Spec Kit 之外没有独立产品),A 的差异化点清晰可执行。在 P1 Differentiation × P2 Polish 的两个强信号下,A 的"窄而深"切片让 polish 资源能集中在 ambiguity 分类精度 + 报告可读性这两个最高 ROI 的点上。最关键:A 含 calibration seed(GPT R2 的修正),让 A 的产物(`prd.refined.md` + `assumptions.md` + 裁决记录)可以**自然演化**为 B 或 C 的 v0.2 起点——这等价于 Opus R1 §4 的 Option 4(A→B,先 6-8w 做 A,跑 4-6w 用户后再 6-8w 加 dashboard)或 Option 5(A→C,先 6-8w 做 A,4-6w 后再 6-8w 加 Journal)。**总时长更长但风险分摊**,且 A 的产物即使 B/C 不做也能独立活。这最尊重 L2 §6 抗重做硬约束。

**第二段——什么情况下应该直接选 B 或 C**:**3 个候选不是互斥世界观**——A 是最可控 v0.1,B 是 A 的可视化产品化层(更适合 v0.2),C 更像 v0.2 长期护城河。如果你**已经访谈过 ≥3 位独立创业者会用 dashboard**(Persona B 的强信号),直接做 B 也合理(承担 9-12w 风险,但拿到完整可视化产品体验);如果你**愿意赌"人会读画像"且对 ≥5 个项目使用频率有强信心**(自己 + 已访谈),直接做 C 也合理(承担 9-13w + L-M confidence,但拿到 005 真正护城河——其他候选没这层)。**但若你没有这两个强信号中的任何一个,A→B 或 A→C 的渐进路径是最负责任的选择**——它让你用 6-8 周拿到第一个产品级反馈,基于真实用户数据再决定 v0.2 走 B 还是 C。

**不推荐**:
- "直接同时 fork A+B+C 三个并行做"——你周 25h 的预算不够支撑三条 v0.1 同时推进,会稀释 P2 Polish 强信号
- "Pause 等用户访谈"——3 个候选都给了诚实时间估算,A 即使在没访谈下也是低风险高 confidence;若一定要等访谈,可在 fork A 后**并行做 5 位访谈**(不阻塞 v0.1 推进),访谈结果用于决定 v0.2 走 B 还是 C
- "Back to L2"——L2 verdict 是 Y-with-conditions 不是 N,证据基础充分,没有回退理由

---

## Honesty check — 本菜单可能 underweight 的点

L3 是产品层决策,以下是诚实的 gap:

1. **3 个候选都假设用户当前用 Claude Code / Cursor / agent-skills**——但若实际目标用户用 Devin / Sweep / 其他工具,3 个候选的入口设计都要重做(L2 §7 第 4 题,需用户访谈)。本菜单未替你解决这个不确定性。
2. **Persona A vs Persona B 真实占比未确认**——A 偏 A、B 偏 B、C 切交集,但若实际占比 9:1 或 1:9,选哪个候选的最优解会变。L2 §7 第 1 题已标"必须访谈",L3 也无法替你回答。
3. **"可信赖输出"硬标准只给了 stub**——3 个候选的 Success 标准给了具体百分比(如 ≥80% 认可率、≥75% 一致率、≥90 秒回答),但这些数字的合理阈值需要 L4 spec 阶段结合早期用户数据校准。L3 给的是语义,不是科学测量。
4. **Devin 的演化窗口期未量化**——Opus R2 §5 提醒"Devin 自己可能演化成 005 竞品",但没法估"窗口还有多少周/月"。这影响"先做 A 还是直接做 B/C"的紧迫性判断。
5. **中文文化对"用文档驱动开发"的接受度未处理**——L2 §5 已识别"中文场景下用文档驱动开发的文化薄弱",但 3 个候选都假设用户愿意写高质量 PRD。这是真实的张力,L3 没专门切片处理。
6. **R4 红线打包菜单未替你拍板**——保守包/产品化包/个人工具包是 3 套合法 stance,本菜单没替你选(开放在 ❓ items 中)。fork 后写进 PRD 时必须明确。
7. **3 个候选都假设 human-on-the-loop 是用户偏好,但实际"承受打断频率"的上限未知**——L2 §7 第 3 题需访谈 5 位用户。ambiguity policy 引擎的默认参数(打断频率)直接受这个数据影响。

---

## Decision menu(给 human)

### [F] Fork 单个候选(synthesizer 推荐)

```
/fork 005 from-L3 candidate-A as 005-pA
/plan-start 005-pA
```

(A 是低风险高 confidence 的入口;v0.2 再决定要不要加 B 或 C)

### [MF] Fork 多个候选并行

```
/fork 005 from-L3 candidate-A as 005-pA
/fork 005 from-L3 candidate-B as 005-pB
# 或
/fork 005 from-L3 candidate-C as 005-pC
```

(每条线独立 `/plan-start`;**不推荐三条并行**——周 25h 预算不够;最多两条且必须有强 Persona 信号)

### [R] Re-scope(重新讨论)

```
/scope-inject 005 "<新输入,例如访谈完 5 位用户后的关键发现>"
/scope-next 005
```

### [B] Back to L2 — rethink the idea

```
/status 005
```

(**不推荐**——verdict Y-with-conditions,证据充分)

### [P] Park

```
/park 005
```

(若你看完后压力大、想做 1-2 周用户访谈再回来,park 是体面选择)

### [A] Abandon

```
/abandon 005
```

(**不推荐**——没有合理理由)

---

## Fork log

(由 /fork 命令更新;目前无 sub-fork)
