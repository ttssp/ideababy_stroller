# Forge 006 · v10 待跑批次(攒批处 · append-only)

> ## ✅ 本文件的簇 A + 簇 B 已于 2026-08-11 由 forge v10 裁决完毕
>
> **verdict**:`discussion/006/forge/v10/stage-forge-006-v10.md`(converged · unresolved: NO)
> —— warn 生命周期契约 + hard admission gate;三条「复发 ≥N 次」判据作废。
> **已裁 8 条**:XD-44′(含 XD-52)· XD-47 · KG-B15 · KG-B16 · KG-B17 · KG-B18 · KG-B19。
> **已登记 10 条 obligation**(`OB-006-v10-01..10`),其中 `-01`(M1 schema)与 `-02`(M2 接线)
> 挂 `forge:006:phase0` ⇒ **下次 `/expert-forge 006` 未落地即 fail-closed 阻断 intake**。
>
> **⏳ 本文件剩余待审 = 簇 C + 簇 D,滚入 v11**:
> `KG-B13`(cdx-run 静默重放覆盖产物)· `KG-B14`(reuse-session 被静默降级)·
> `XD-45`(file_domain 零回归论证方法论)· `KG-49`(REVIEW-LOG 越 file_domain)。
> ⚠ **v10 的 `underweight-8③` 是一条欠债**:「簇 C/D 是否被 v10 的一般条款自然覆盖」
> **双方 P3R2 都没回答**(快照 Part 5.5 已点名要求「若覆盖请明说」,四轮里被静默掠过)。
> ⇒ **起 v11 时第一件事就是回答这个问题**,而不是默认它们是独立议题。

> **这是什么**:forge 006 v9(2026-08-04 起跑 · X = 证据完整性家族 KG-B11 / XD-41 / XD-43 / XD-44
> + IDS HANDBACK-LOG 第 40/42 条实测证据)**冻结之后**新撞到的框架级问题攒在这里,作为下一轮
> `/expert-forge 006` 的 X 标的预填。承 `FORGE-006-v7-PENDING.md` 先例。
>
> **为什么不补进 v9**:v9 的 `x_hash`(`7ad1bb97a7760addddb7cd371eca3b71`)已冻结且 **Opus P1 已写完**,
> P1-GPT 尚未跑。此刻改 X 会重演 forge 001 v6 的「**P1 独立性污染 / 非双向对称**」事故
> (见 `discussion/001/forge/v6/stage-forge-001-v6.md` §underweight-1)—— 收益不抵代价。
>
> **创建**:2026-08-09(001 forge v6 误重放事件顺带暴露 · 见 `discussion/001/handback/HANDBACK-LOG.md` 第 43 条)

## 条目

### KG-B13 · `cdx-run` 静默重放已完成轮次并**覆盖**产物(HEAD 完成后不前进、不标记)

- **现场**:`.codex-inbox/queues/<q>/HEAD` 是单行文本 = 待执行任务文件名。`cdx-run <q>`
  (`~/.bashrc`)读 HEAD 即跑,**执行完不改 HEAD、不写任何完成标记**。
  完成态只由 `cdx-queues` 用「outbox 是否存在同名文件」**推断**(存在 ⇒ 显示 `✅ done`)。
- **失效模态**:对同一队列再敲一次 `cdx-run <q>`,会**静默重跑一个已完成、甚至已被下游消费封存的轮次**,
  产物**直接覆盖** outbox 与 discussion 下的正式文件 —— **无警告、无确认、无备份**。
  若当时工作区不干净或已 commit,覆盖可能被误当成正常改动带进 commit。
- **真实发生**:2026-08-09T21:24 · `cdx-run 001` 重放了 08-03 的 forge v6 P3R2
  (v6 早已 finalize + 落地),覆盖 `discussion/001/forge/v6/P3R2-GPT55xHigh.md` 与同名 outbox 文件。
  靠 git 恢复。详见 HANDBACK-LOG 第 43 条。
- **候选 verdict 方向(不预设答案)**:完成后 HEAD 前进/置空 · 或 `cdx-run` 见 outbox 已存在同名文件
  时改为 fail-closed(需 `--force` 或显式确认)· 或产物写入前对已存在文件做 `-resample` 旁路命名
  而非原地覆盖。
- **同题**:与 v9 的「机制已装但从未被强制调用」(XD-43 preflight)同族 —— 这里是
  **状态机缺一个前进边**,导致「完成」这个状态**从不被写下**,只能靠副作用推断。

### KG-B14 · `reuse-session` 形态被 `cdx-run` **静默降级**为冷 session(执行面零强制零留痕)

- **现场**:`.codex-inbox/README.md` §"两种 kickoff 形态" 定义 —— `oneshot`(每次新会话,`cdx-run` 执行)
  与 `reuse-session`(人在**已开**的 Codex 终端粘贴短 prompt,沿用上一轮上下文)。
  任务文件 frontmatter 用 `**Kickoff form**:` 声明形态,`reuse-session` 任务还带 `## Session hint`
  写「**已读(勿重读)**:……」。
- **失效模态**:`cdx-run` 的实现是 `codex "read <task> and execute…"` = **必然新起 session**
  (`codex resume` 是独立子命令,未被使用)。⇒ 用 `cdx-run` 执行一个 `reuse-session` 任务时,
  「**已读勿重读**」从「复用上下文」**语义反转**成「**根本不读**」,模型在**远少于协议假设的证据**上作答,
  **而产物里看不出这件事**(没有任何字段记录本轮实际拿到了哪些上下文)。
  没有任何机制阻止或警告这种形态错配。
- **影响面**:所有默认 `reuse-session` 的命令 —— `inspire-next` / `explore-next` / `scope-next` /
  `plan-adversarial-next`,以及 forge 的 P2 / P3R1 / P3R2 轮。**下游读产物的人无法判断**
  某一轮到底是在完整上下文还是冷启动下产出的。
- **真实发生**:同 KG-B13 的那次重放(P3R2 任务书写 `reuse-session`,却经 `cdx-run` 冷跑)。
  该次产物与正式版的 verdict 一致但 `evidence_grade` 打分不同,详见 HANDBACK-LOG 第 43 条 (3)。
- **候选 verdict 方向(不预设答案)**:`cdx-run` 读 frontmatter,遇 `reuse-session` 拒跑或
  显式改走 `codex resume --last` · 或要求产物 frontmatter 自报「本轮实际读了什么」使形态可审计 ·
  或取消 reuse-session 形态、全部 oneshot 并把省 token 的目标交给自足任务书。
- **同题**:与 v9 的「**缺席即豁免**」(SHARED-CONTRACT §6 B-4-IDS:协议写「任一字段缺 = REJECT」,
  实装却「父键不存在 ⇒ 整步跳过不 warn」)是**同一形状** —— 声明与执行两层之间**没有校验**。

### KG-B15 · Session-per-idea worktree 规约:warn 已复发 **4** 次,hook block 升级判据达成

- **现场**:`CLAUDE.md`「Session-per-idea worktree 规约(forge 006 v8 · 簇② · 2026-07-13)」定
  **warn 型 preflight 起步**,并明写 hook block(commit-time 硬拦)留 v0.2、
  **升级判据 = warn 上线后 mismatch 混线仍复发 ≥2 次**。
- **计数(据实)**:
  1. **第 1 次** · 2026-08-04 · `/handback-review 001` 跑在 `main` 分支 —— HANDBACK-LOG 第 42 条 (4) 留痕。
  2. **第 2 次** · 2026-08-09 · forge v6 重采样处置跑在 `main` 分支,且单次改动**同时触及 001 与 006
     两个 idea**(典型混线形态)—— HANDBACK-LOG 第 43 条 (5) 留痕。
  3. **第 3 次** · 2026-08-10 · `/handback-review 001` 跑在 `main` 分支,且本次改动**同时触及 001
     (HANDBACK-LOG)、006(本文件)、framework(SHARED-CONTRACT + validator)** —— 混线形态比第 2 次更宽。
     HANDBACK-LOG 第 44 条 (6) 留痕。
  4. **第 4 次** · 2026-08-11 · `/handback-review 001` 跑在 `main` 分支,改动同时触及 001(HANDBACK-LOG)、
     006(本文件)、framework(check-8 + validator)—— 与第 3 次同形。HANDBACK-LOG 第 45 条留痕。
     ⚠ **本次 operator 是在被明确告知 mismatch 后显式裁决"就在 main 上写"** —— 与前 3 次(未察觉/事后留痕)
     性质不同,**不是纪律失效而是规约本身有歧义**:规约把「handback-review 决议后」列为合回 main 的
     checkpoint,隐含"决议在 idea 分支做、之后合回",但 checkpoint 产物本身就是 main 的合法内容。
     ⇒ **升级 hook block 之前必须先消掉这个歧义**,否则硬拦会把合法的 checkpoint 写入一并拦掉
     (这正是本条「待判」第二项)。
- ⇒ **判据已达成**,v0.2(commit-time hook block)具备起动条件。**未自行升级** ——
  规约属框架层,按铁律只走 forge。
- ⚠ **第 3 次的额外信息**:judgment 判据已在第 2 次达成,**达成后仍复发**。这说明
  「记录升级判据」本身不构成任何行为约束 —— 与 XD-44′「唯一实际终止条件是 operator 疲劳」
  是同一形状(**写下的规则若没有执行边,只是又一份声明**)。起 v10 时这三条宜同案。
- **待判**:硬拦的粒度(分支名 mismatch 就拦 / 还是只拦「一次 commit 跨多个 idea 目录」)、
  以及**治理产物合回 main 的 checkpoint 场景怎么豁免**(合回本身就是 main 上的合法写)。

### XD-47 · codex 假审与真审在解析层**逐字节同形**(gate 输出不携带 gate 是否真跑过)

> **来源**:HANDBACK-LOG 第 44 条 · hand-back `001-radar-pA-20260810T121304Z`(T042)。
> **operator 决议**:起 `/expert-forge 006` 专场审 **review gate 终止条件**(本条 + 下条 XD-44′ 同案)。

- **现场**:T042 codex adversarial-review round-1,只读执行器 `bwrap` 起不来,**一个字节 diff 都没看过**,
  却产出 `Verdict: needs-attention` + `findings: 0` —— 按 `codex-review` SKILL §4.1 的解析契约,
  这与「真审了、审出 0 条」**逐字节同形**。它还**吃掉了 4 轮预算里的一轮**(真正被 codex 看过的只有 round 2-5)。
- **失效模态**:review gate 的输出**不携带「gate 是否真的运行过」这一位信息**。环境故障静默降级成「审过了」,
  且降级方向是 **fail-open**(没审 ⇒ 0 finding ⇒ 看起来更干净)。
- **与既有条目的关系**:与 **XD-41**(「六批替代路径评审欠债结账」· 子代理与被审代码同源同上下文 ⇒
  `needs-attention` 事实等价于放行 · HANDBACK-LOG 第 36 条)**同根**:两者都是
  *gate 的输出形状无法区分「审出问题」与「审没生效」*。XD-41 是**语义**上没真审,XD-47 是**物理**上没真审。
- **候选 verdict 方向(不预设答案)**:审前 liveness 探针(回显本轮实际读到的 diff 字节数 / 文件数,
  对不上判 **gate 失败**而非 0 finding)· 或 verdict enum 增加第三态 `not-run` 与 `approve`/`needs-attention` 并列 ·
  或把「本轮读到什么」写进 REVIEW-LOG 必填字段使其可事后审计(与 KG-B14 的「产物自报实际上下文」同解)。

### XD-44′ · 「撞 4 轮上限 → 轮次外直接修 → 确认轮又出 high → 记 backlog ship」已连续 **4** 次(收敛判据缺失)

> **来源**:HANDBACK-LOG 第 44 条 · 三个 hand-back 的横切观察。**operator 决议**:同 XD-47 并案起 forge 专场。
> **2026-08-11 更新**(HANDBACK-LOG 第 45 条 · T041):计数 3 → **4**,并新增一条**定量反证**(见下「⭐ 第 4 次」段)。

- **计数(据实 · 均在 001-radar-pA)**:
  1. **T040** round-6 · 3×`[P2]` · operator 判「测试严谨度边际改进」→ 停止迭代 ship。
  2. **FU-R1F1** round-4 · 1×`[high]` · operator 判「架构边界归属分歧而非已验证活漏洞」→ ship,转 IDS 决议。
  3. **T042** round-5(确认轮)· 1×`[high]`(KG-50)+ 1×`[medium]`(KG-51)· operator 判「中等工作量新功能
     超出本轮授权」→ 记 backlog ship。
  4. **T041** round-6 · 2×`[P2]` · operator **两次**显式介入(round-5 后「修完这轮就先打住」· 随后「繼續,只跑 1 輪review」)
     → 收口 ship。

- **⭐ 第 4 次(T041)带来前 3 次没有的两条硬证据**:
  - **(a) finding 序列非单调 —— 直接否证「多跑几轮就会收敛」**:6 轮 finding 数
    **4 → 2 → 1 → 3 → 3 → 2**,`needs-attention` ×6,**一次 `approve` 都没有**。round-3 已降到 1
    又**反弹**到 3。这是本家族第一次有**定量**证据说明:轮次增加与 finding 收敛之间**没有**单调关系。
  - **(b) 「提高轮数上限」这条修法方向已被预先证伪**:T041 是四次里**唯一一次 operator 显式授权加轮**
    (round-6)的案例,加了轮**仍以 `needs-attention` + 2 条新 finding 结束**。⇒ v10 专场**不能只调
    XD-44 的上限值**;若只调上限,本案例证明结果仍是"上限撞顶 + operator 叫停"。
  - **(c) 一条 scope 侧的候选真因(新 · 供 forge 判)**:T041 被审对象是 `tests/e2e/batch_runner.py`
    + `src/radar/bench/`(operator 自用的批跑脚手架),15 条 finding 里多条是 path traversal / 命令注入
    形状;而同批次 `FU-R5F4` 审的是 `gate.py` 真门禁逻辑,**1 轮 0 finding 结束**。
    ⇒ **review gate 对被审模块的「关键性分级」无感,评审强度全线均一**。这可能同时解释了非收敛:
    低风险面上对抗式评审**永远能再找出一条 `[P2]`**。⚠ 本条是 IDS consumer 侧推论,**未经 producer 确认**,
    forge 应当作假说而非事实检验。

- **同族新条目 XD-52(producer 自记 · 本次并案)**:`codex-review` SKILL §4.2 的 4 轮上限
  **靠 agent 在对话上下文里自己数轮次,没有机器可查的计数器**。T041 round-4 是上限最后一轮,
  本该 hard-stop,执行时判断有误又跑了 round-5(会话此前经历过一次 context compaction,
  压缩摘要对轮次是叙述性文字而非结构化字段)。**无产物因此被错误放行** —— round-5/6 都是真跑真修,
  代价只是流程多绕一步 + operator 两次介入。
  - **与 XD-44 / XD-44′ 的分工**:XD-44 = 上限**值**该多少;XD-44′ = 该不该只有「上限」这一个终止边;
    **XD-52 = 上限怎么**执行**(轮次真相住在对话记忆里而非文件系统里)**。三条是同一处协议改动的三个面。
  - **producer 建议的修法方向(供参考)**:§4.2 每轮起跑前机械核对 `ls review-log/<TID>-round*.md | wc -l`,
    ≥4 时不问 agent 自数第几轮,直接 fail-closed 转 hard-stop / operator 决策关卡。
- **结构问题(不是"轮数不够"）**:**三次没有任何一次是靠 codex 判 `approve` 结束的**,全部由 operator 叫停;
  三次的**最后一轮都还在出新 finding**(其中两次是 `[high]`)。既有 **XD-44** 记的是「4 轮上限对协议设计类任务
  系统性偏低」= 轮数问题;本条指出真正缺的是**终止条件本身** —— 现行协议只有「轮数上限」这一个终止边,
  没有「收敛」这个终止边,于是**唯一的实际终止条件是 operator 疲劳**。
- **为何这与 XD-41 是同一个家族**:XD-41 的结论是「`needs-attention` 事实等价于放行」。本条给出了
  该等价成立的**机制**:上限撞顶后,`needs-attention` 与 `approve` 在流程上导向同一个出口(ship)。
- **候选 verdict 方向(不预设答案)**:确认轮出 `[high]` **强制续轮**(不计入上限)· 或区分
  「上限终止」与「收敛终止」两种 ship 状态并在 hand-back frontmatter 自报 ·
  或 `[high]` 未清零不得标 ship,只能标 ship-with-open-high(下游 task 可见)。

### XD-45 · `file_domain` 冻结前「零回归」论证方法论(消费点收紧 vs 生产点收紧)

> **来源**:hand-back `001-radar-pA-20260810T041724Z`(FU-R1F1)§3(2) · producer 自记 XD-45。

- **现场**:FU-R1F1 的 provenance allow-list 让 `file_domain` **外** 12 个既有测试(7 文件 + 1 仓级 shell 脚本)
  从通变红。这**不是**新漏洞,是该修法应有的正确下游行为;问题在原 task doc 的「零回归风险」论证方法
  ——**单一 grep 关键词存在性核对,未逐调用点核对参数取值**。
- **待判**:task-decomposer 拆 `file_domain` 时,「**消费点收紧**」(如 allow-list,影响**所有**历史构造过该
  产物形状的既有测试)与「**生产点收紧**」(如拒绝注入,只影响**直接调用且传特定参数组合**的既有测试)
  应否用**不同强度**的核实要求?可能影响后续所有 task 拆分的默认核实清单。

### KG-49 · `codex-review` SKILL §3.6 写 REVIEW-LOG 必然越出 `parallel-builder` 的 `file_domain`

> **来源**:hand-back `001-radar-pA-20260809T143351Z`(FU-R5F4)§3(2)。

- **现场**:`codex-review` SKILL §3.6 要求「必须写 machine-readable REVIEW-LOG」,而该 REVIEW-LOG 是**仓库根级
  共享 singleton**(`.claude/skills/codex-review/REVIEW-LOG.md` + `real-review/` 目录)。
  字面执行 ⇒ 产出越出 `parallel-builder` task `file_domain` 的 diff。
- **实践 vs 文本**:git 历史显示实际靠**合并后单独一条 `docs(review): … ship 回填` commit** 完成,
  但**两份 SKILL 都没写这条隐性例外** —— 又一个「执行面与声明面之间无校验」的实例(同 KG-B14 形状)。
- **待判**:是否给 `codex-review` SKILL §3.6 补 parallel-builder 场景例外条款(以及该例外由谁执行、何时执行)。
- **⚠ 与 R-Q7 的关系**:HANDBACK-LOG 第 40 条已记「immutable REVIEW-LOG 被整条绕过且 pointer stale 成反向正信号」。
  本条给出**绕过之所以发生的结构性理由**(照做就越权),两条应并案 —— 否则会把结构性冲突误判成执行纪律问题。

### KG-B16 · forge v8 三字段只在 XenoDev 单侧实装、IDS SSOT 三处全空(已止血,留 forge 追认 + mirror 同步)

> **来源**:HANDBACK-LOG 第 44 条 consumer 侧独立核查。**operator 决议**:IDS 权威侧**本次就补**(已落地),
> 本条留作 forge 追认 + XenoDev mirror 同步授权项。

- **现场**:forge 006 v8 簇② 明写「hand-back / outbox 包 frontmatter 加 `current_idea` / `worktree` / `baseline`
  三字段(跨仓通道自带拓扑自证)」。真跑发现:XenoDev producer 已填,而 IDS 权威侧**三处全空** ——
  `SHARED-CONTRACT` §6.3 schema 无定义 / `handback.template.md` 无 placeholder / validator 不校验。
  与本文件 `ssot_owner: ideababy_stroller` 声明**反向**。
- **实证代价**:2026-08-10 的 4 包中,恰好那 2 个跑在 per-task 专用 worktree 的包
  (`...-FU-R5F4` / `...-T042`)`worktree` 值均错填为 idea 主 worktree ——
  **自证字段在它唯一有价值的场景(分支真的分叉了)失真**,且无任何机制发现。
- **已止血(IDS 侧 · contract v2.4→v2.5)**:§6.3 schema 补三字段 + 新增 §6.3.1 语义节 + template 补 placeholder +
  新增 `check-7-topology-selfattest.sh`(**warn 型 · 恒 exit 0**)接进 `validate-handback.sh`。
  落地后对那 2 包精确 warn、对另 2 包 PASS、对无三字段的老包 skip。
- **留给 forge 的两问**:① v8 决议「已落地」的判据是什么 —— 本例中 XenoDev 侧实装了就被当作落地,
  **SSOT 侧空缺无人发现**,这是 v8 落地验收的普遍缺口还是孤例?② check-7 warn→hard-fail 的升级由谁触发
  (与 KG-B15 是同一个「warn 型规约的升级无 owner」问题)。
- **授权项**:XenoDev 侧 `gen-handback.sh` 从 mirror 同步本改动,并把 `worktree` 接**真值**
  (取真实 `working_repo`,而非 idea 主 worktree 常量)。

### KG-B17 · handback-validator 的 test-fixture 语料在 Ubuntu 上**整体不可跑**(迁移后从未被执行过)

> **来源**:HANDBACK-LOG 第 44 条 · 落 check-7 时顺带实测。

- **现场**:`framework/xenodev-bootstrap-kit/handback-validator/test-fixtures/` 下 **valid 与 invalid 全部 6 个 fixture**
  在本机(Ubuntu)跑 `validate-handback.sh` 均 `exit 1`,且 **valid fixture 挂在 check-1** ——
  因为 fixture 的 `handback_target` 是硬编码 macOS 路径 `/Users/admin/codes/ideababy_stroller/...`。
- **推论(这才是要点)**:valid fixture 恒 FAIL ⇒ 该 fixture 语料**自 mac→Ubuntu 迁移后就没有被真正执行过**
  —— 否则第一次跑就会炸。validator 是 hand-back 通道**唯一**的自动化防线,而它自己的测试语料是死的。
- **与 FU-R5F4 §3(2) 的关系**:那条记的是 `handback.template.md` 第 6 行 `to_source_repo` 硬编码 macOS 路径
  (`gen-handback.sh` 不做 `$IDS_ROOT` 替换)。**同一根因、不同受害面**:一个害 producer 产包,一个害 fixture 自测。
  应并案处置(统一走 env 替换而非字面量)。
- **⚠ 已知张力**:`memory/migration-mac-to-ubuntu-status.md` 记「`/Users/admin` 硬编码多是 by-design 兜底或
  历史文件别改源码」。本条**不与之冲突** —— *测试 fixture 与 by-design 兜底是两回事*:兜底路径不通只是不生效,
  fixture 不通则是**测试本身失效**。forge 需明确区分这两类硬编码的处置策略。

### KG-B18 · `workspace.source_repo` 声明**从未被任何 check 校验** —— 全语料 **47/100** 包声明失真(已止血,留 forge 追认)

> **来源**:HANDBACK-LOG 第 45 条 · consumer 侧独立发现(**不在任何一包的 §3 里**)。
> **operator 决议**:现在止血修 validator + 记本条由 forge 追认。

- **现场**:hand-back `001-radar-pA-20260811T024101Z`(T041)声明
  `to_source_repo` / `workspace.source_repo` = `/Users/admin/codes/ideababy_stroller`(mac 旧路径,
  Ubuntu 上**不存在**),而 `workspace.handback_target` = `/home/ys/.../discussion/001/handback/`。
  这两个字段按 **§6.2.1 约束 1 自身的公式**(`handback_target` ⊂ `source_repo` + `/discussion/<id>/handback/`)
  **互相矛盾**,却 7 个 check **全 PASS**。
- **实证根因(已 grep 确认 · 非推演)**:`validate-handback.sh:76` 抽出的 `SOURCE_REPO_FM`
  **全文件再未被使用** —— 是个死变量。check-1 把约束 1 的公式作用在**运行时 CLI 传入的**
  `source_repo`(consumer 的 `realpath .`)上,那个值**恒自洽**;包里**声明的**那个从未进过任何判据。
  ⇒ **自证字段存在但不被验 = 自证等于零**。
- **📊 全语料实测(落 check-8 后逐包跑,PASS / WARN / 无字段)**:
  | 语料 | PASS | **WARN(声明失真)** | 无 `source_repo` 字段 |
  |---|---|---|---|
  | `discussion/001` | 22 | **19** | 0 |
  | `discussion/006` | 29 | **0** | 0 |
  | `discussion/009` | 2 | **28** | 0 |
  | **合计** | 53 | **47 / 100** | 0 |
  ⇒ 这**不是**单包回归,是**近半个 hand-back 语料**的声明拓扑失真;它之所以从未被发现,
  正是因为该字段从未被验过。009 语料几乎全线失真(28/30),006 全清(29/29)。
- **且本包是一次回归**:8-09 / 8-10 连续 4 包都填对了 `/home/ys`,本包退回 mac 路径 ——
  说明 producer 侧取值**不稳定**(时对时错),不是一次性的历史遗留。
- **根因候选(跨仓 · 未处置,留 forge 判)**:XenoDev live `CLAUDE.md` 三处仍把 IDS 仓路径写成
  `/Users/admin/codes/ideababy_stroller`(`:38` workflow 步骤 2 · `:55` 跨仓引用 · `:90` validator dry-run 示例);
  `:55` 虽补了「新机 `$IDS_ROOT`」但**陈旧值排在前面**,`:38`/`:90` 是**无限定的陈旧命令**。
  IDS 侧 mirror `framework/xenodev-bootstrap-kit/CLAUDE.md` 同样 4 处(`:38` `:51` `:52` `:66`)。
  ⇒ **每个 XenoDev session 读到的宪法都在告诉它 IDS 在 mac 路径上**。
  - ⚠ **与 memory `migration-mac-to-ubuntu-status` 的张力(同 KG-B17 的处置分歧)**:那条记
    「`/Users/admin` 硬编码多是 by-design 兜底或历史文件别改源码」。本条**不与之冲突** ——
    *活的指令文档与代码兜底是两回事*:兜底路径不通只是不生效,**指令文档陈旧则是持续向 agent 灌错值**。
    KG-B17 已就「fixture 硬编码」提出同一区分诉求;**本条与 KG-B17 应并案**,让 forge 一次性给出
    三类 `/Users/admin` 硬编码(代码兜底 / 测试 fixture / 指令文档)的分类处置策略。
- **✅ 本次已止血(warn 型 · 与 check-7 同构)**:新增
  `framework/xenodev-bootstrap-kit/handback-validator/check-8-declared-source-repo.sh`,
  把约束 1 的公式**作用在声明值上**(纯词法比较,不碰文件系统 —— 声明的是**产源主机**路径,
  在 consumer 主机上做 realpath 无意义),并比对声明 vs 运行时。已接进 `validate-handback.sh`。
  - **为何 warn 而非 hard-fail**:(a) 47/100 存量包会被整体判 corruption;
    (b) 该字段此前从未被校验,producer 侧无任何机会被提示,直接硬拦属**追溯性执法**。
  - **升级 hard-fail 判据**(留 forge 定):warn 上线后声明不自洽仍复发 ≥2 次,
    或出现一次因 `source_repo` 声明失真导致的跨仓误写 / 误决议。
- **待判(forge)**:① 追认 check-8 及其 warn 型强度;② 是否把 `source_repo` 改为**禁止 producer 声明**
  (由 consumer 运行时单方权威 —— 声明一个 consumer 有权威值的字段,本身就是在制造可失真面);
  ③ 存量 47 包是否回填、回填算不算改既有语料(与 append-only 语义的关系);
  ④ 跨仓陈旧指令文档的清理由谁执行(XenoDev 侧文档改属框架级还是仓内事务)。

### KG-B19 · hook 白名单「只减不增」健康度指标**没有工具可执行**,且与 worktree-per-idea 规约结构冲突

> **来源**:forge 006 **v10 Phase 0 的 obligation gate 阻断**(OB-006-v9-01)后被迫执行的白名单全表回审 ·
> 2026-08-11。**这是 obligation 机制第一次真的拦下东西,并且拦对了** —— 被拦的正是 v9 自己标为
> 「最强 v10 触发判据」的那条,74 天没做的回审在 gate 上当场做完并产出本条。

- **回审实测结果**(XenoDev `.scan-credentials-ignore` · 24 条精确路径逐条真跑):
  21 条有效,**3 条失效已删**(`review-log/T102-round3/4/5.md` —— 从未进过 git、磁盘上也不存在;
  同 commit `0837e92` 里 round1/2 是真 tracked 的 ⇒ 这 3 条是**对不存在文件的豁免承诺**,
  按不变量 2「承诺无指称对象」+ 不变量 3「不成立的删」处置)。条数 24 → 21,
  XenoDev commit `5442afd`。**这是健康度指标「只减不增」有史以来的第二个数据点** ——
  该文件自 2026-05-29 创建后 **74 天零修改**,回审动作此前一次都没发生过。

- **🔴 结构问题 1 · 「只减不增」没有工具可执行**:不变量 3 要求精确路径「上升」为模式类识别以减少条数,
  但 v8 定的三个模式类(heredoc-commit-message / mktemp 私有 dir / 变量拼路径)**至今 ⏳ 未实装**
  (`framework/hook-allowlist-governance.md` §4)。⇒ **唯一能让条数下降的机制根本不存在**,
  于是"只减不增"只能靠删失效条目达成,而失效条目是有限的。这与 **KG-B18**(自证字段存在但校验不存在)、
  **KG-B17**(防线存在但从未被执行)是**同一形状**:*指标/防线/字段写在文档里,实现它的东西没建*。

- **🔴 结构问题 2 · 与 forge v8 簇② worktree-per-idea 规约结构冲突(新)**:
  白名单是 **repo-root 相对的精确路径**(`AGENTS.md` / `framework/SHARED-CONTRACT.md` / …),
  而 v8 规约要求**每个 idea 一个独立 worktree**,仓内 worktree 落在 `.claude/worktrees/<idea>/` 下 ——
  同一份文件在 worktree 里的路径前缀不同,**全部不被白名单覆盖**。
  - **实测**:XenoDev 现有**一个**仓内 worktree(`.claude/worktrees/001-radar-pA`),
    `scan-credentials.sh` 总命中 22 条 = **2 条 by-design**(`secrets/prod/` 已 gitignored、
    从未进过 git,件 1 路径硬拦按设计触发且明文不受白名单放行)+ **20 条 worktree 副本假阳性**。
  - **为什么不能按精确路径修**:每多一个 worktree 就多 ~20 条,条数随 worktree 数**线性膨胀**,
    必然同时违反不变量 1「按模式类收敛,不按撞一次加一条」与不变量 3 的健康度指标。
    ⇒ 两条框架规约(v8 worktree 规约 × T102 精确路径白名单治理)**互不兼容**,
    而这一点在白名单 74 天无人回审期间从未被发现 —— **冲突本身就是"没有回审"的产物**。
- **待判(forge)**:① 模式类识别的实装归属与时点(v8 授权条目已挂 29 天);
  ② 白名单路径语义是否应改为 **worktree-aware**(如相对 git common dir / 或按 `git rev-parse --show-toplevel` 归一);
  ③ 与 KG-B17 的 fixture 硬编码、KG-B18 的指令文档陈旧**三条并案**,给出
  「路径类声明在多 worktree / 多主机下如何保持有效」的统一处置。

### KG-B20 · R-Q7「REVIEW-LOG 被整条绕过」在 009 复发,且 `ids_verdict_evidence` 防伪契约**两个 fork 从未生效过一次**

- **来源**:IDS `/handback-review 009` 第 35 条(2026-08-13)· hand-back `009-pM3prime-20260813T093952Z`(T014)
- **现场(三段实证,均 IDS 侧直查)**:
  1. **T014 的 9 轮 codex review 零机器可读记录** —— `XenoDev-009/.claude/skills/codex-review/real-review/`
     最新条目是 `branch-2026-08-11T171433Z-FU-HB32.md`(上一个 task),**无 T014**;
     而 XenoDev `codex-review` SKILL §3.6 明写「跑完真路径 codex review 后 · 真路径**必须** machine-readable
     yaml frontmatter 真路径写到 `.claude/skills/codex-review/REVIEW-LOG.md`」。
  2. 🔴 **canonical singleton pointer stale 成反向正信号** —— `REVIEW-LOG.md` frontmatter 至今是
     `target_file: FU-HB32-branch-diff-vs-4820539` · `verdict: approve` · `findings_count: 0` ·
     `ts: 2026-08-11T17:14:33Z`;最后触碰该文件的 commit `59d0ed2`(08-12)**早于** T014 三个 code commit
     (`3acee51`/`0d9f5cb`/`82ef616`,08-13)。⇒ 任何人或脚本问「最近一次 review 结论」,得到
     **`approve` / 0 findings**;**真实是 `needs-attention` / 2 条残留 finding**。
  3. **`ids_verdict_evidence` 从未生效过一次** —— `rg -l '^ids_verdict_evidence:' discussion/*/handback/*.md`
     = **空**。SHARED-CONTRACT §6 B-4-IDS 把它定为 spine 级 immutable evidence binding、
     写明「任一字段缺 = consumer REJECT」,changelog 记为 wave 2 T205 已 ship;
     **实际在 001 与 009 两个 fork 的全部 hand-back 语料里,零命中**。
- **机制链闭合(这条比现场更重要)**:
  ```
  codex review 跑了 → 不写 REVIEW-LOG → 没有可绑的 review_log_path/sha256
    → hand-back 不产 ids_verdict_evidence 父键
      → IDS /handback-review Step 4.3 判据是「**仅当**含该父键时跑预检」
        → 缺父键 = 静默通过(不是 REJECT)
          → 以 practice-stats 入库,无任何机械点报警
  ```
  且 producer 侧 `XenoDev-009/lib/handback-validator/gen-handback.sh` **模板压根不产该键**(IDS grep 实证)。
  ⇒ **防伪契约由被它约束的一方 opt-in**,这不是纪律问题,是判据方向写反了。
- **与既有条目的关系**:R-Q7 在 001(forge v4)已诊断过「immutable REVIEW-LOG 被整条绕过且 pointer stale
  成反向正信号」;**009 是第二个 fork、约 10 天后的复发**。⇒ 与 KG-B15 / XD-44′ 同族的元层证据:
  **诊断本身不产生行为**。KG-49 给出了绕过的**结构性理由**(写 REVIEW-LOG 必然越 `file_domain`),
  本条给出**绕过后无人发现的完整链路**,两条应并案。
- **建议裁决方向(供 forge 定夺,非预判)**:
  ① IDS `/handback-review` Step 4.3 的判据从「含父键才跑」改为「**build-ship 类包缺父键即 REJECT**」
     —— 需先定义「build-ship 类包」的机械判据(否则 practice-stats / spec-gap 类包会被误拦);
  ② `gen-handback.sh` 模板补 `ids_verdict_evidence` + §6.3.1 拓扑三字段(与 KG-51 同源,一并处理);
  ③ **stale pointer 本次未修**(operator 2026-08-13 只选「归 forge 攒批」,未选「立刻止血」)⇒
     `REVIEW-LOG.md` 现在仍对外答 `approve / 0 findings`,**这是一条已知在场的错误正信号,裁决前一直有效**。

### KG-B21 · `check-7` 的跳过判据日期盲,且「三字段全缺」比「缺一两个」更安静(激励方向反了)

- **来源**:同上 · hand-back `009-pM3prime-20260813T093952Z` 过 validator 时暴露
- **现场**:该包 `created: 2026-08-13`、拓扑三字段(`current_idea`/`worktree`/`baseline`)全缺,
  validator 输出 **「⏭ check-7 skipped:§6.3.1 拓扑自证三字段全缺(2026-08-10 前的老包属正常)」** ——
  对本包这是一句**假陈述**:三字段 2026-08-10 进 schema,本包晚 3 天。`created` 就在 frontmatter 里,
  `check-7-topology-selfattest.sh` **从不读它**。
- **判据形状问题**:脚本逻辑是 `${#MISSING[@]} -eq 3` → 静默 skip;缺 1–2 个 → WARN。
  ⇒ **全不填的输出比填一半更干净**。而脚本自己的注释恰恰写着「部分填写比全不填更可疑 ——
  producer 可能只 backfill 了好填的那几个」,**判据与其自身的风险判断相反**。
- **根因在 producer 不在 validator**:`gen-handback.sh` 模板不产这三字段(同 KG-B20 ② / KG-51)。
  同日同 fork 的另一个包 `009-pM3prime-20260813T072930Z` **有**三字段,因为它是 IDS session 手写的。
- **与既有条目的关系**:本 warn 已挂 `WARN-check7-topology-selfattest`(`temporary` ·
  `due_event: forge:006:phase0` · 已接线),**不需新增 warn 条目**;但「跳过判据日期盲 + 激励反向」
  是该 warn 登记时未覆盖的**新面**,应在其三态裁决(convert/revert/defer)时一并处置。
  与 KG-B18(`workspace.source_repo` 声明从未被验 · 47/100 包失真)同构:**自证字段存在但不被验 = 自证等于零**;
  本条更进一步 —— **不填反而不被验**。

## 与 v9 的关系(起 v10 时必读)

全部条目都与 v9 正在审的**证据完整性家族**同题,**建议并案而不是另起家族**:

| v10 pending | v9 在审 | 共同结构 |
|---|---|---|
| KG-B14(形态声明 vs 执行无校验) | B-4-IDS「缺席即豁免」 | 声明层与执行层之间没有校验点 |
| KG-49(SKILL 要求与 file_domain 结构冲突) | R-Q7(REVIEW-LOG 被整条绕过) | 同上 · 且本条给出**绕过的结构性理由** |
| KG-B13(完成状态从不被写下) | XD-43(preflight 已实装但从未被调用) | 机制存在但**没有强制边**,靠副作用推断状态 |
| **XD-47**(假审与真审解析层同形) | **XD-41**(needs-attention 等价于放行) | gate 输出**不携带 gate 是否真跑过**这一位 |
| **XD-44′**(收敛判据缺失 · 连续 **4** 次 + XD-52) | XD-41 + XD-44 | 撞上限后 needs-attention 与 approve **同一出口** |
| **KG-B16**(v8 三字段 IDS SSOT 空缺) | v8 落地验收本身 | 「已落地」的判据是什么 · 单侧实装即算数 |
| **KG-B17**(fixture 语料整体不可跑) | XD-43(机制已装从未被调用) | 防线**存在**但从未被执行,状态靠假设 |
| **KG-B18**(声明 source_repo 从未被验 · **47/100 包失真**) | XD-41 / B-4-IDS | **自证字段存在但不被验 = 自证等于零** |
| **KG-B19**(白名单「只减不增」无工具 + worktree 冲突) | XD-43 / KG-B17 | 指标写在文档里,**实现它的东西没建**;且两条规约互不兼容 |
| KG-B15(warn 型规约的升级判据 · **已复发 4 次**) | v8 簇② 的 warn 起步设计本身 | warn→block 的升级由谁、在哪触发,至今无 owner |
| **KG-B20**(R-Q7 在 009 复发 · `ids_verdict_evidence` **两 fork 零命中**) | **R-Q7 + B-4-IDS「缺席即豁免」+ XD-41** | **防伪契约由被约束方 opt-in**:缺父键 = 静默通过而非 REJECT;且 001 已诊断过、009 仍复发 ⇒ 诊断不产生行为 |
| **KG-B21**(check-7 跳过判据日期盲 · 全缺比部分缺更安静) | KG-B18(自证字段不被验) | **不填反而不被验** —— 判据与脚本自身写下的风险判断相反 |

⚠ **起 v10 前先读 v9 的 verdict** —— 若 v9 已给出「声明/执行两层校验」的一般条款,
这些条目可能变成**该条款的实例**而非独立议题,X 应据此重写。

**⚠ v10 的 X 若只收「证据完整性」会漏掉一条更硬的线**:XD-44′ / KG-B15 / XD-47 三条共同指向的不是
「某个机制缺校验」,而是 **「本框架写下的规则,默认没有执行边;有执行边的,默认是 warn;warn 的升级,
没有 owner」**。KG-B15 在判据达成后仍复发第 3 次,是这条线目前最干净的实证。
起 v10 时建议把它作为**独立的 X 分支**(治理条款的可执行性),而非塞进证据完整性家族。
