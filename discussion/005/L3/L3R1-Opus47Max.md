# Idea 005 · L3R1 · Claude Opus 4.7 · Scope (no search)

**Timestamp**: 2026-05-07T01:55:00Z
**Inputs read**: stage-L2-explore-005.md (L2 report), L3R0-intake.md, scope-protocol SKILL.md
**Searches used**: NONE in this round
**Visibility**: I did NOT read GPT-5.5 的 L3R1.

---

## 0. How I read the intake

Human 的核心信号在 §6 priorities: **Differentiation + Polish**(没选 Speed)。配合 §1 时间未锁 + §2 周投入 ≈25 小时(主力项目),这告诉我:他愿意为差异化和体验密度多花 1-2 个月,**v0.1 必须在那个小切片上做到「能拿出去给目标用户看」的程度**。

**我尊重的硬约束**:Persona = ML 研究员/PhD 型 + 独立创业者(二者并集);3 条已确认红线;ambiguity policy + 用户级 calibration 是差异化核心;必须 human-on-the-loop;抗重做(v0.1→v1.0 不能推倒);时间估算用 25h/周中位数。

**我会主动给 options 的 ❓**:目标交付时间(每个 candidate 给诚实估算让 human 选);R4 红线候选 3 条(§5)。

**我看到的最关键 scope 张力**:**"用户级 calibration"何时入场**。 L2 §6 条件 1 说"收紧到两个 novelty 缺口",但条件 4 说"v0.1 必须能演化到 v1.0 不推倒"——这两个条件在"calibration 何时进 v0.1"这件事上**直接冲突**:
- 早入(v0.1 含)= 抗重做强,但 scope 鼓胀,polish 难做
- 晚入(v0.2 加)= polish 容易做透,但需要 v0.1 架构层就为 calibration 留空(否则推倒重来)

我下面 3 个候选**就以这个轴切片**——每个对此给不同答案,让 human 看清取舍。

---

## 1. Candidate A · "Ambiguity Forge"(收紧到单一 novelty 点 + 工具形态)

### v0.1 in one paragraph
一个 CLI 工具 / Claude Code skill,**专做一件事**:扫描你的 PRD,产出**一份 ambiguity map**——明确列出这份 PRD 在哪些位置 underspecified、每处给"必须问 / 可推断+TODO 标 / 可暂停"三选一建议、以及如果选"推断"的话推断方向。它**不写代码**,不接管 build pipeline,不做 calibration。它是**站在 PRD 和现有 agent-skills 中间的一道安检**——你写完 PRD,先过它一遍,补完之后再丢给 addy osmani agent-skills / Superpowers 走标准 build 流程。

### User persona (sharpened from L2)
**Lin**,ML 博士第 4 年,实验室同事,手头有一份"把组里 RL 训练流水线变成内部工具"的 PRD 草稿。她能写清"输入输出+成功标准",但不知道 PRD 里"支持 multi-GPU 训练"是该具体到 NCCL 还是只说功能。她想在丢给 agent 之前,**先让一个东西告诉她她的 PRD 哪里还不够**。

### Core user stories (3-5)
- 作为 Lin,我可以 `prd-forge analyze ./my-prd.md`,几分钟内拿到一份 ambiguity map(每处 PRD 漏洞 + 三选一建议),让我**在跑 agent 之前**先补好 PRD
- 作为 Lin,对 ambiguity map 的每一项,我可以**接受、修改或拒绝**它的建议,生成 `prd.refined.md` 直接用于下游 build
- 作为独立创业者 Mira,在把 PRD 丢给 Claude Code 之前,我可以 `prd-forge --interactive` 走一轮 5-10 分钟的对话式补漏,产出我**敢丢给 agent** 的版本
- 作为 Lin,我可以查看 ambiguity map 的"推断假设"清单,做事后审计:agent build 完后是不是真按这些推断做的

### Scope IN
- PRD ingest(markdown / 自由文本)
- 结构化 ambiguity 检测(分类:输入定义不全、边界缺失、非功能需求模糊、验收标准未量化、依赖关系隐含等)
- 每处 underspec 的"三选一"建议(必须问 / 推断+TODO / 暂停)
- Interactive mode(对话式补漏)
- 输出 `prd.refined.md` + 一份 `assumptions.md`(推断清单可作下游审计依据)

### Scope OUT (explicit non-goals)
- **不写代码**——离开 PRD 之后这个工具就不管了
- **不集成 agent-skills 的 build 流程**——交给 addy osmani 现有体系或 Claude Code 原生 skill
- **不累积用户级 calibration**——v0.1 每次跑都是 stateless
- **不做多 PRD 比对 / 项目级 lore**——只看一份 PRD,不读 codebase
- **不做付费层 / billing**——免费 OSS

### Success looks like (observable outcomes)
1. 在 5 份代表性 PRD 上跑,**每份发现至少 5 处真实 ambiguity**,且 ≥80% 的发现被作者认可为有意义(非误报)
2. Interactive mode 的中位时长 ≤ **8 分钟**(若超过,说明问得太多/不到位)
3. **使用 ambiguity-refined PRD 跑 agent build 比直接跑节省 ≥30% 返工**(基线对比)
4. 收到至少 **5 位非 human 自己**的早期用户反馈(Persona A 同类 + Persona B)

### Honest time estimate under human's constraint
- 25h/周 × **5-7 周** = ~150 hours 总投入
- Confidence: **H**——单一 surface,不依赖大架构,模型能力(Claude/GPT)已支持 PRD 解析
- 风险:把 ambiguity 分类做"够准"是技术活,不是堆功能就完事

### UX principles (tradeoff stances, not designs)
- **少而精**:CLI 输出每行都该有用,不堆"为了完整"的废话
- **诚实优先**:遇到不确定就标"low confidence",不靠 hallucination 撑门面
- **可被脚本化**:ambiguity map 是结构化 JSON+ 人类 markdown 双输出,方便 power user 接入自己流程

### Biggest risk to this cut
**赌"ambiguity policy 单点工具"是真需求**——如果用户的真实痛点是"整个 build 流程不可信"而不是"PRD 不够清晰",这个工具会被认为"没解决真问题"。但这个赌的好处是:即使错了,产物本身仍是个有用的小工具(可作 agent-skills 上游 lint),损失有限。

---

## 2. Candidate B · "Confidence Atelier"(完整 PRD-to-confidence 管道 / Web)

### v0.1 in one paragraph
一个 **Web dashboard**,接受 PRD 输入,启动一次完整的 build run,产出代码 + **一张可视化的「信心地图」**——4 个区块(自动推进区 / 必须澄清区 / 事后可审计区 / 暂停区),每个区块下挂着对应的 task / 决策记录 / 测试证据 / 风险标记。底层调用 addy osmani agent-skills 完成 build(不重做工程纪律),Atelier 的核心价值是**信心呈现层** + ambiguity policy 的可视化执行。**用户级 calibration 在 v0.1 只做最薄一层**:记录"这个 user 的过往 ambiguity 决策模式",下次 PRD 进时拿出来 surface,不做完整 profile。

### User persona (sharpened from L2)
**Mira**,独立创业者,有 3 个 demo 想跨到正式产品(其中一个是 SaaS 工具),会写 PRD 但每次 demo→产品中间总散掉。她要的不是"再快 30% 写代码",而是**「我离开屏幕这 6 小时它做了什么 + 哪些我现在该回来拍板」**的可视化报告。

### Core user stories (3-5)
- 作为 Mira,我可以上传 PRD,启动 run,关掉浏览器去做别的事
- 我打开 dashboard 看到 4 区块的实时状态,**澄清区**有 3 个等我裁决的决策点(每个有 3 种选项)
- 我点开**事后可审计区**的某个决策,看到"为什么 agent 选了 A 而非 B"完整推理 + 它执行的 test 证据
- 同一个 PRD 二次 run,系统提醒"上次你在类似 ambiguity 上选了 X,这次推断是 Y,要保持一致吗?"——这是用户级 calibration 的最薄层
- 一个 run 失败后,系统自动产出 1 页 `retro.md`,沉淀进我的"判断历史",**下次 PRD 进时自动 surface 相关条目**

### Scope IN
- PRD ingest + 一次完整 build run(调用底层 agent-skills,不自己写 build 逻辑)
- 「信心地图」可视化(4 区块的实时状态)
- ambiguity policy 引擎(三类决策:打断 / 推断+TODO / 暂停)
- 决策审计页(每个决策的"为什么"+ 证据)
- 用户级 calibration v0.1 薄层:记录用户在 ambiguity 上的历史选择 + 下次主动 surface
- 自动 retro 生成(每个 run 完后产出 1 页)

### Scope OUT (explicit non-goals)
- **不重做 spec/test/review/build 工程纪律**——直接调用 addy osmani agent-skills(条件 1)
- **不做完整的"用户工程风格画像"**——v0.1 只做"过往决策一致性提醒",不做风格画像
- **不做多人协作**(R3)
- **不做付费 tier**——免费,但留扩展点
- **不做项目类型识别**(L2 §4 扩展项)
- **不做 dark mode 之类细枝末节 polish**——polish 集中在「信心地图」可视化和审计页这两块

### Success looks like (observable outcomes)
1. 一次完整 run 后,Mira **能在 ≤90 秒内回答**:它做了什么 / 哪些我要拍板 / 哪些已 ok
2. ambiguity policy 引擎在 5 个真实 PRD 上的"该问 vs 该推断"判断与人工 baseline 一致率 ≥ **75%**
3. 用户级 calibration 在第 3 个 run 起开始**主动 surface 上次类似决策**,且 ≥60% 被用户认可有用
4. 8-10 位 Persona A+B 早期用户反馈,中位 NPS ≥ +30

### Honest time estimate under human's constraint
- 25h/周 × **10-14 周** = ~300 hours 总投入
- Confidence: **M**——「信心地图」UI 和 calibration 薄层都是新形态,实际打磨周期不好估
- 关键风险:Web dashboard 的 polish 是无底洞;若 P2(Polish)不打折,容易超期到 16-18 周

### UX principles
- **「信心地图」是产品语义,不是装饰**——4 个区块的命名 / 颜色 / 排布必须反映"我现在该信任什么"
- **审计页要自我解释**——不需要文档,人看一眼能懂"为什么 agent 这么决定"
- **calibration surface 要克制**——只在第 3 个 run 后才开始,且默认低噪声(可关)
- **CLI 入口同等重要**——dashboard 是看的,run 入口仍要支持命令行

### Biggest risk to this cut
**Web dashboard + calibration 薄层 = 两个新形态同时做**。Mira 是不是真的会**回到 dashboard 看**而不是只用 CLI?如果 Persona A 占主力,他们大概率不打开 dashboard,Web 投入就是浪费。这个 cut 的成立**强依赖 Persona B(创业者)真实存在且会用 dashboard**——这是 §6 第 1 题需要 user research 的核心问题。

---

## 3. Candidate C · "PRD Diary"(累积型工具 / 用户级 calibration 优先)

### v0.1 in one paragraph
一个 **Desktop / 本地优先**的工具,核心是**用户级 calibration 从 day 1 入场**。Diary 不替你 build,也不做完整 PRD lint;它做的是**陪伴你跨多个项目积累一份「你的工程判断日记」**——每次你和 agent 交互(用任何工具:Claude Code / Cursor / agent-skills)的关键决策点(尤其是 ambiguity 处),都被 Diary 捕获并归类。3 个项目后,它开始**主动给你下一份 PRD 提建议**:"你过去在 X 类 ambiguity 上 80% 选了停下问,这次也建议停下"。它**不替代任何现有工具**,是装在所有 agentic-coding 之上的"个人判断元层"。

### User persona (sharpened from L2)
**Lin**(ML 博士)用 Claude Code + Diary 走 5 个项目后,她发现 Diary 知道她**80% 的 PRD 漏在"非功能需求"上**,且每次都倾向"先推断不打断";Diary 在第 6 个 PRD 提交前主动 surface:"按你过往模式这份 PRD 的非功能需求又只写了 1 行,要补吗?"——这是 Lin 第一次感到"工具学到了我"。

### Core user stories (3-5)
- 作为 Lin,我可以让 Diary 监听我和任意 agentic 工具的交互(通过 hook / log 摄取),它**自动**捕获 ambiguity 决策点
- 第 3-5 次项目后,我可以打开 Diary 看到一份**「我的工程判断画像」**:漏 PRD 的常见类目、对 ambiguity 的偏好、哪些决策事后被自己推翻过
- 在新 PRD 写作时,我可以让 Diary 给出 **3 条最值得关注的 PRD 漏洞**(基于我的过往画像,不是通用 lint)
- 在 agent run 过程中,Diary 在背景**安静地**给出"这个决策与你过去模式不一致"的提醒(不强打断)
- 我可以导出 Diary 数据(JSON),不被锁定

### Scope IN
- 多源 ambiguity 摄取(Claude Code log / 手动 prompt / agent-skills decision log)
- 用户判断画像(类目分布 + 偏好 + 翻案率)
- 个性化 PRD 漏洞建议(基于画像)
- 安静的实时提醒(可关)
- 本地数据(隐私),可导出
- 极简 ambiguity policy 引擎(只在写 PRD 阶段用,不接管 build)

### Scope OUT
- **不替代任何现有工具**——不写代码,不做 build,不做完整 PRD lint
- **不做云端同步 / 多设备**——v0.1 单设备本地
- **不做团队 / 多人画像**(R3)
- **不在前 3 个项目主动给建议**——signal 不够时不假装,这是产品诚实
- **不做项目级 codebase lore**(addy 已做,不重复)

### Success looks like
1. 用户从 第 4 个项目起**真的会回来读画像**(打开率 ≥ 60%)
2. 个性化建议被采纳率 ≥ 50%(对比通用 PRD lint 的 baseline)
3. 5 位早期用户中,≥ 3 位在 5 个月内运行 ≥ 5 个项目(累积型工具的留存命题)

### Honest time estimate under human's constraint
- 25h/周 × **8-12 周** = ~250 hours 总投入
- Confidence: **L**——picture 这事的算法路径还没收敛;且**赌"用户真的会读自己的画像"**这个行为假设(L2 §7 第 7 题)
- 关键不确定:多源摄取 hook 的工程量

### UX principles
- **安静优先**:Diary 不打扰你,不弹窗,不强 review
- **诚实优先**:signal 不足时**显式说"还没积累够"**,不假装智能
- **数据主权**:本地 + 可导出,任何时候用户可以走人

### Biggest risk to this cut
**赌「人会读自己的画像」**——L2 §7 第 7 题就是问这个。如果用户不读画像,Diary 就是死档案版的 AGENTS.md。这个 cut **最依赖 user research**;直接做就是 high-risk bet。但如果赌中,这是 005 真正护城河——其他三个候选都没这层。

---

## 4. Options for the human's ❓ items

### ❓1 · 目标交付时间
- **Option 1 · 跟 A 走**:5-7 周。最快产出,差异化窄但深;先验证"ambiguity policy 单点"是否真需求
- **Option 2 · 跟 B 走**:10-14 周(若不卡 Polish 可压到 8-10 周但牺牲 P2)。中等周期;赌"完整信心地图"对 Persona B 有吸引力
- **Option 3 · 跟 C 走**:8-12 周。中等周期,但 confidence 最低(累积型行为假设未验证)
- **Option 4 · A 然后 B**:先 5-7 周做 A,跑 4-6 周用户后再 6-8 周加 B 的 dashboard 层。**总时长更长但风险分摊**,且 A 的产物即使 B 不做也能独立活
- **Option 5 · A 然后 C**:先 5-7 周做 A,4-6 周用户后再 6-8 周加 C 的 Diary 层。同样分摊风险,但 C 的累积型行为假设到那时才验证

### ❓2 · R4 红线(L2 §5 抽出的 3 条候选)
1. **不做"自然语言一句话生成完整 app"**——L2 §5 已明列,Devin 数据已证伪
2. **不做实时同屏协作**(Cursor 类 sub-100ms ping-pong)——L2 §5 列为"另一个产品族"
3. **不做面向已有 50 人+工程团队的工具**——L2 §5 标"会和现有 CI/CD/code-style 冲突"

Human 在 L3R2 / synthesizer 阶段挑接受/拒绝。

---

## 5. Red lines I'd propose

(已在 §4 ❓2 中给了 3 条,human 在菜单阶段决定)

---

## 6. Questions that need real user interviews (L3 cannot answer)

1. **Persona A 和 B 的真实占比?**——我 3 个候选切片不同程度依赖二者,知道占比可显著影响选哪个
2. **用户真的会"回到 dashboard / Diary 读自己的画像"吗?**——B 和 C 都赌这个;若答案是"不会",B 退化为只是 nicer Devin,C 直接死
3. **"在 PRD 不清时停下问"和"推断+TODO 标"——目标用户实际**承受打断频率**的上限是多少?**——这决定 ambiguity policy 引擎的默认参数;问 5 位用户就能答
4. **目标用户当前用什么工具 + 工作流?**——我假设他们用 Claude Code / Cursor / agent-skills,但如果他们其实用 Devin / Sweep,005 的入口设计完全不同
5. **Persona B 的"demo 到产品"具体卡在哪步?**——如果卡的是"代码不能跑",B 提供的"信心地图"没用;如果卡的是"不知道哪些决策事后是错的",B 完美对症

---

**For human/synthesizer**: 3 个候选**真正的差异轴**是「用户级 calibration 何时入场」——A 完全不做(单点工具),B 做最薄一层(项目内一致性提醒),C 直接做满(跨项目画像优先)。这是 L3 的核心选择,我推荐 human 看完 GPT 的 R1 后,优先在这个轴上拍板。
