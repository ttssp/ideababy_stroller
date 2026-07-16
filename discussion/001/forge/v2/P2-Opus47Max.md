# P2 · Opus 4.8 Max · 参照系评估(forge 001 v2)

**Phase**: 2(SOTA 对标 · 已读对方 P1)
**Written**: 2026-07-16T11:35:00Z
**Searches run**: 4(生成时 provenance / bootstrap 循环依赖 / 分阶段 gate / eval-in-production 抽查)

## §1 · SOTA 对标

| # | 检索方向 | SOTA 结论 | 对本裁决的含义 |
|---|---|---|---|
| 1 | provenance:生成时采集 vs 事后补锅 | 工程共识:provenance 在**生成时**织入产物(wrapper 拦截/执行时注 token),事后从 log 重建是次优且有损(只见读写不见变换逻辑);「审计 = 对既有图查询,而非重建工程」(emergentmind Generation-Time Provenance · Atlan/DataHub/Snowflake lineage 指南) | **a1(per-slice source 映射)是 SOTA 正解方向,非临时补丁**——位移叙事生成时保留 paper→slice 映射,正是「生成时织入」;当前 reconstructor 丢弃映射再想事后判 trace,恰是 SOTA 说的次优形态 |
| 2 | 验证系统的循环依赖(bootstrap) | 编译器自举的标准解:**stage-0 种子**——用已存在的外部语言写第一个编译器,显式地、一次性地在起点打破循环;此后自托管。信任验证用「多样性双编译」(独立第二路径交叉比对,Wheeler DDC) | 裁决 B 的范式钥匙:**打破循环的正解是显式的一次性 stage-0 治理动作,不是等系统先产出只有解锁后才能产出的自证物**。对方 P1「直接解锁 trace-producing tasks」在此获得先例支撑——但 stage-0 必须显式、一次性、带事后交叉核验(≈ hand-back 13 已用的独立子代理双路径,DDC 同构) |
| 3 | 分阶段 gate(检查项随能力就绪激活) | CI/CD 共识:gate 分布在多阶段、**各阶段只放该阶段可判的检查**(静态检查早、集成中、canary/SLO 晚、运行时动态 gate);检查项在其前提就绪时激活(InfoQ/Octopus/LaunchDarkly) | ①②(3 击链可达性)是 Phase 2 形状的检查,SOTA 做法是把它放到 Phase 2 出口(T021/T022 验收),而非堆在最早闸口;a2 的「分阶段」直觉符合 SOTA,但正确表述是「**各阶段配各自可判的 gate**」,不是「先放空壳 gate」 |
| 4 | eval-in-production 抽查范式 | 生产系统标准:1-5% trace 抽样 + judge/rubric 打分 + 审计留痕;observability(含 trace)**包摄**预部署 gate;生产 trace 回流为测试集形成持续改进环(LangChain/Braintrust/Confident-AI) | operator 的「边用边抽查」不是妥协,是行业标准范式;①② 作**使用期抽查对象**(a3)+ journal 校准样本回流,与「production traces become datasets」逐字对应 |

## §2 · 用户外部材料消化

K 内无外部链接/文件——无本节内容。

## §3 · 修正后的视角

**P1 站住的**:a3 为主(①② 重绑 Phase 2 出口验收 + 使用期抽查)——SOTA #3/#4 双重背书;a1 是 SOTA 正解方向(#1「生成时织入」),非过度投资;a2 空壳形态 cut;B4 换绑定对象。与对方 P1 在这些点上独立同向。

**P1 被修正/深化的两点**:

1. **a1 与解锁的拓扑关系,我 P1 说错了半句**。我原判「T010/T011 等 a1 落地后解锁」,隐含 a1 是解锁的时间前置。重读拓扑:a1 改的是 slicer/reconstructor/writer——**全是已 ship 的 P0.1 组件**,走 T002-A1/T003-A1/A2 同款 amendment 通道(gate blocked 期间照常 ship 过三次,有先例)。a1 **不被 gate 挡**,也不依赖 T010/T011。所以「等 a1」的真实代价只是一个 S 级 amendment 周期,而其收益是:解锁谓词从「纯治理签放」升级为「对真产物秒级机器可判」(K 的自证硬要求)。这大幅削弱对方「不要用尚未产出的 trace 卡住产 trace 的任务」的担忧——a1 的 trace 不由被卡任务产出。
2. **stage-0 框架给了「解锁语义」正名**(#2)。新解锁不该伪装成「机器已验证了信任」——它是显式 stage-0 治理动作:机器道只验「该边界真能判的最小集」(a1 映射存在且可解析 + ③ 通道结构 + 命名一致),信任的完整机器验证在 Phase 2 出口(①② 重绑处)自托管,并用独立路径交叉核验(DDC 同构,项目内已有先例)。这同时回应我 P1 §3.3 的解锁时机不确定:**不是二选一**(等 a1 vs 立即),而是「a1 作 P0.1 amendment 立即起建,解锁谓词绑 a1 产物」——快与可判兼得。

**给 P3R1 的分歧预告**(与对方 P1 的真分歧,其余高度同向):对方主张「直接解锁 + O2/O7/治理道兜底」(零机器谓词),我主张「解锁谓词绑 a1 产物的最小机器判」。分歧实质 = stage-0 动作里机器道占多少:纯治理 vs 治理+最小机器判。K 第 4 条(新前置必须附现有产物立即可验证的自证步骤)偏向后者——纯治理解锁没有可跑的自证物,而 a1 谓词可以对 rerun 的真 briefing 当场验。

Sources: [Generation-Time Fine-Grained Provenance](https://www.emergentmind.com/topics/generation-time-fine-grained-provenance) · [Data Lineage vs Data Provenance (Atlan)](https://atlan.com/data-lineage-vs-data-provenance/) · [DataHub lineage](https://datahub.com/blog/data-lineage-vs-data-provenance/) · [Snowflake lineage vs provenance](https://www.snowflake.com/en/fundamentals/data-lineage/lineage-vs-provenance/) · [Bootstrapping (compilers)](https://en.wikipedia.org/wiki/Bootstrapping_(compilers)) · [Wheeler · Diverse Double-Compiling](https://dwheeler.com/trusting-trust/) · [InfoQ · Pipeline Quality Gates](https://www.infoq.com/articles/pipeline-quality-gates/) · [LaunchDarkly progressive gates](https://launchdarkly.com/docs/tutorials/aic-cicd) · [LangChain LLM observability](https://www.langchain.com/resources/llm-monitoring-observability) · [Braintrust observability guide](https://www.braintrust.dev/articles/llm-observability-guide)
