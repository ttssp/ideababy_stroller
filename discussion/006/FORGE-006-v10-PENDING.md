# Forge 006 · v10 待跑批次(攒批处 · append-only)

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

### KG-B15 · Session-per-idea worktree 规约:warn 已复发 **2** 次,hook block 升级判据达成

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

### XD-44′ · 「撞 4 轮上限 → 轮次外直接修 → 确认轮又出 high → 记 backlog ship」已连续 **3** 次(收敛判据缺失)

> **来源**:HANDBACK-LOG 第 44 条 · 三个 hand-back 的横切观察。**operator 决议**:同 XD-47 并案起 forge 专场。

- **计数(据实 · 均在 001-radar-pA)**:
  1. **T040** round-6 · 3×`[P2]` · operator 判「测试严谨度边际改进」→ 停止迭代 ship。
  2. **FU-R1F1** round-4 · 1×`[high]` · operator 判「架构边界归属分歧而非已验证活漏洞」→ ship,转 IDS 决议。
  3. **T042** round-5(确认轮)· 1×`[high]`(KG-50)+ 1×`[medium]`(KG-51)· operator 判「中等工作量新功能
     超出本轮授权」→ 记 backlog ship。
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

## 与 v9 的关系(起 v10 时必读)

全部条目都与 v9 正在审的**证据完整性家族**同题,**建议并案而不是另起家族**:

| v10 pending | v9 在审 | 共同结构 |
|---|---|---|
| KG-B14(形态声明 vs 执行无校验) | B-4-IDS「缺席即豁免」 | 声明层与执行层之间没有校验点 |
| KG-49(SKILL 要求与 file_domain 结构冲突) | R-Q7(REVIEW-LOG 被整条绕过) | 同上 · 且本条给出**绕过的结构性理由** |
| KG-B13(完成状态从不被写下) | XD-43(preflight 已实装但从未被调用) | 机制存在但**没有强制边**,靠副作用推断状态 |
| **XD-47**(假审与真审解析层同形) | **XD-41**(needs-attention 等价于放行) | gate 输出**不携带 gate 是否真跑过**这一位 |
| **XD-44′**(收敛判据缺失 · 连续 3 次) | XD-41 + XD-44 | 撞上限后 needs-attention 与 approve **同一出口** |
| **KG-B16**(v8 三字段 IDS SSOT 空缺) | v8 落地验收本身 | 「已落地」的判据是什么 · 单侧实装即算数 |
| **KG-B17**(fixture 语料整体不可跑) | XD-43(机制已装从未被调用) | 防线**存在**但从未被执行,状态靠假设 |
| KG-B15(warn 型规约的升级判据 · **已复发 3 次**) | v8 簇② 的 warn 起步设计本身 | warn→block 的升级由谁、在哪触发,至今无 owner |

⚠ **起 v10 前先读 v9 的 verdict** —— 若 v9 已给出「声明/执行两层校验」的一般条款,
这些条目可能变成**该条款的实例**而非独立议题,X 应据此重写。

**⚠ v10 的 X 若只收「证据完整性」会漏掉一条更硬的线**:XD-44′ / KG-B15 / XD-47 三条共同指向的不是
「某个机制缺校验」,而是 **「本框架写下的规则,默认没有执行边;有执行边的,默认是 warn;warn 的升级,
没有 owner」**。KG-B15 在判据达成后仍复发第 3 次,是这条线目前最干净的实证。
起 v10 时建议把它作为**独立的 X 分支**(治理条款的可执行性),而非塞进证据完整性家族。
