# Forge v5 · 001 · P1 · Opus47Max · 独立审阅(no search)

**Timestamp**: 2026-08-02T08:20:42Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

**读了(12/12,无跳过)**:

- `discussion/001/handback/HANDBACK-LOG.md`(793 行 · 38 条)→ 全读 26/29/31/34/35/36/37/38 条正文;其余按 tag 扫。
- `20260802T012127Z`(决议 37 源包)→ 全读,重点 §2.2 数字表 / §2.4 24 条 finding 逐条 / §2.5.3 / §2.6 / §4.2-4.4。
- `20260802T073925Z`(决议 38 源包)→ 全读,重点 §2.3 / §3.1 / §3.2 三条硬证据 / §5.1-5.6 / §6 产物全文。
- `PRD.md` v1.6(187 行)→ 全读;重点 Success O1-O5 / O4 生效条款段 / Scope OUT 的五轮退役史 / OQ #3。
- `spec.md` v0.6 `frozen`(327 行)→ 全读 §1-O1/O2/O3/O4/O7 + §6 verification 全表 + §7-P1/P2 + 反 PPV + Amendment log 8 条(尤其第 7 条 scope 回撤记录)+ Glossary。
- `T040.md`(59 行)→ 全读。
- `ephemeral.py`(699 行)→ 读 `:135 DECLARED_READ_SITES` / `:624 audit_evaluation_reads` / `:636 audit_undeclared_reads` / `:653 audit_module_classification` / `:660 audit_persisted_artifact_classes` 五个 audit 函数本体 + 模块 docstring 边界表。
- `writer.py`(102 行)→ 全读,`:85-97` 逐字读。
- `judge.py`(423 行)→ 读模块 docstring 契约段 / `:53` / `:92 sparse_coverage` 退路 / `:118 not anchor_map` 退路 / `:319-322` prompt JSON 契约 / `:364` 截断 / `:380-393` 严校布尔。
- `selfcheck_sequence.py`(314 行)→ 读 `:174 _require_eval_briefing_shape`。
- `evaluate.py`(213 行)→ 读 `:84-90` 注入拒绝 / `:145-165 run_evaluate` 产物面。
- `journal/cli.py`(321 行)→ 读 `:172-187` 真跑横幅 `lines[2]` 绑定。

**K(用户判准)摘要**:核心问题是「**一条机器可判的验收判据,在被冻结成 gate 之前,必须先证明什么、挂在哪一侧、由谁写、用什么词指称?**」。要能执行的裁决不要正确的综述;可达性判据本身要可达(防自指);**v5 结束时 T040 若仍不能起跑,这场 forge 没解决主要问题**。后悔值不对称:存疑偏向不放松,但**只挂着不给可达路径 = 没裁**。强制每条裁决写成「A + 判据 + 证不出则 B」。

**阅读策略**:按 Y=架构设计 优先读两处**拓扑**——C9 双门的职责边界(`ephemeral.py` 五个 audit 函数)与 evaluate/reconstruct 两族产物的分叉点(`evaluate.py` × `selfcheck_sequence.py`);按 Y=工程纪律 优先读 spec §6 verification 全表与 `T040.md` 的对应关系(判据到测的映射是否 1:1);按 Y=产品价值 读 PRD O1/O5 与决议 38 §6 的真产物全文对照(判断产物对 operator 还有没有决策价值)。**刻意最后读 HANDBACK-LOG 的结论段**,先自己从 spec + 代码看一遍,避免直接继承 IDS 已有归因。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 架构设计

**C9 双门的不对称是结构性的,不是疏忽。** `ephemeral.py` 里五个 audit 函数职责清晰:① `audit_evaluation_reads` 扫「评估链路模块内的读调用点」,判据是**模块前缀匹配** `EVALUATION_MODULES`,命中即 violation,**函数体内没有任何 per-file 或 per-line 的豁免入口**;② `audit_undeclared_reads` 扫全包,但**第一行就是** `if rel in DECLARED_READ_SITES: continue` —— 逐文件声明理由即可放行。②的 docstring 自己写明它是「①的补位」,因为「评审实测的绕过恰恰是把读放进一个已分类的非评估包」。**即:② 是为了堵 ① 的边界外泄而生的,两道门的关系是覆盖面互补,不是强度递进。** 这就解释了为什么 R4-F4 无解:`briefing/` 在 `EVALUATION_MODULES` 里,要 fsync 目录必须 `os.open`,而 ① 对 `os.open` 一律保守计入(flags 是整数常量,静态判不了)且**没有 ② 那样的声明机制**。`writer.py:85-97` 把三条路各自的问题逐条写死在代码注释里,是我在本仓见过的最诚实的一处「不修理由」。

**evaluate 与 reconstruct 是两族产物、两条 provenance 链,但 spec 用同一个词指称。** `evaluate.py:145-165 run_evaluate` 只写 briefing;`selfcheck_sequence.py:174 _require_eval_briefing_shape` 是正向 allowlist,按 `^###\s+(\S+)\s+·` 分段并**逐段**要求块级来源块。T022 的 renderer 出 `### {i} · {ring}`——heading 正则会匹配(slice_id 位被解析成判断序号),但逐段来源块必然缺 ⇒ fail-closed STOP。**这不是 bug,是这道门正确地拒绝了一个不属于它的产物族。** evaluate 自己那条链是 `RunProvenance` 三值 + `journal/cli.py:172-187` 的 `lines[2]` 逐字相等,与 a1 解锁链完全不同源。

**判据的消费面已经是网状而非树状。** spec §1-O2 (c) 一条被 §0 / §1-O1 / §2.1 / §5-P2.2 / §6 / §7 六处引用,Amendment log 第 2 条明写「7 处消费面收窄适用域」是为了「防各面另立定义二次漂移」。同一份 spec 里 §6 定 pytest 五条、§7-P2 定验证命令、`T040.md` 定 contract suite 分两层——**同一个判据在三个抽象层各有一份表述**。

### 视角 B · 工程纪律

**spec §6 已经是一张相当成熟的判据表**,每行都区分了「机器可跑」与「人审签字」,meta-note 还显式声明诚实边界(「不宣称豁口是密码学防伪门」)。Amendment log 第 7 条记录了一次**教科书级的 scope 自查**:codex round-2 要求补三值 verdict + 重算门堵免检通道,round-3 反过来指出这两项超出 IDS 决议 A1 授权且把它们标成「非行为改」是掩盖 scope 扩张,operator 裁方案 C 部分回撤 → 记 OQ-A1-1。**「两个都成立 —— A1 字面授权的豁口本身留洞,而堵洞需要 A1 没给的决定」这句话是整份 spec 里方法论密度最高的一句。**

**但 (c) 与 §1-O4 之间存在一处未被任何文档指出的字面张力。** (c) 要求「≥3 条非豁免判断供抽样」;§1-O4 / OUT-8 要求「不做真理机 · 无证据必标低置信」;`judge.py` 的实装是**只有上界** `JUDGE_MAX_JUDGMENTS=12`、`:364` 截断,**全文件无下界措辞**——但它有一条相反方向的硬约束:模块 docstring 明写「非稀疏叙事零有效判断 → raise 失败响亮」。**即 judge 的下界事实上是 1(且是 fail-loud 的),不是 0。** (c) 要的是 3。

**T040 的阻塞是精确的,不是笼统的。** `depends_on: [T030,T031,T032]` 三者已 ship ⇒ 依赖已满足;`T040.md:39-42` 的 `test_o2_exemption_contract.py` 明确要断言「(c) 抽样下界:非豁免 0/1/2 → 不得判 PASS · 恰 3 → 可 PASS」,并已诚实标注「结果值语义待 OQ-A1-1,本 suite 先不断言」。**所以 T040 不是整体被阻,是它 6 个测文件里的 1 个的 1 条断言被阻。**

**两个仓级 shell 门此前不在任何 task 的 `file_domain` 里**(决议 37 §2.6 ④)——`T040.md:9` 的 `file_domain` 是 `tests/contract/**`,确实覆盖不到 `scripts/`。

### 视角 C · 产品价值

**O7 是唯一带墙钟的产品成功信号,且它的分子分母都不依赖 P2。** PRD O1 = 「3 个月内 ≥5 次真实新方向评估,其中 ≥1 次实际改变投入决策」;spec §1-O7 同义但**无起算点**。决议 38 已达成 1/5 且 `decision_delta=true`。

**但本次真产物的产品价值实况是矛盾的。** 决议 38 §6.1 全文可见:200 篇语料、41.8 秒、位移叙事有相当密度(四条结构接合链条被点名,正是 PRD story 2 要的「结构位移」而非热度),**但只产出 1 条判断,且该判断自标低置信,证据链只有 1 个锚 1 击**。同时叙事被 T021/T022 两层消毒转义弄成 `\*\*结构连接\*\*` / `\(u+201c\)生成主导\(u+201d\)` 这种形态。**产物同时具备「内容质量达到 PRD 预期」与「呈现形态显著劣化 + 判断密度不足」两种属性。**

**PRD O1 的原话是「信任第一块砖」**,UX principles 第一条是「判断先行,证据随取;宁可 briefing 观点强 + 标不确定度,不做四平八稳综述」。1 条自标低置信的判断,**在文体上恰恰接近它要反的那种「不下判断」**。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| **架构设计** | **refactor** | C9 双门的不对称是**设计意图**(②补①的覆盖面)而非缺陷,但它产生了一个未被预见的后果:**①成了唯一没有正当例外通道的门**,于是任何合法的新读点都只能靠「不写这个功能」来满足它——R4-F4 就是第一个真实代价(掉电后产物可能不存在)。需要的不是给①开豁免,而是**给①补一个与②同构、但更严格的声明机制**(声明 + 理由 + 二次判据),否则下一次冲突还会来。evaluate/reconstruct 两条链的**结构本身是对的**(两族产物各有各的 provenance),错的只是**词**。 |
| **工程纪律** | **refactor** | spec §6 表的质量高、诚实边界写得好、Amendment log 第 7 条的 scope 自查是范例。问题不在纪律松,而在**判据挂载点未被当作一等设计对象**:(c) 挂在「验收抽样」侧却被 T040 当成要 mutation 证 teeth 的 gate,而其可满足性取决于产出侧的 judge——**同一条判据横跨两侧且两侧没人负责它的可达性**。T040 的阻塞面比想象中窄(6 个测文件里 1 个的 1 条断言),这是好消息:**裁完 (c) 与 OQ-A1-1,T040 立刻能起跑**。 |
| **产品价值** | **refactor** | O7 机制健康(1/5 · decision_delta 已达成 · 不依赖 P2),节奏也合理。真正的产品风险在**产物可读性与判断密度的合流**:O7 要 operator 每周真读 5 次,而当前产物既难读(消毒转义)又只给 1 条低置信判断。这两件事**单独看都是小事,合起来直接打 PRD O1「信任第一块砖」**。⚠ 但我**不认为**修法是「强迫 judge 多产判断」——那会正面违反 OUT-8。 |

## 3. 我现在最不确定的 3 件事

1. **(c) 的「≥3」到底该挂产出侧还是验收侧,以及有没有第三种挂法。**
   我倾向验收侧(允许跨 run 累积抽样),因为 (c) 自己的措辞是「O2 作为 **Outcome** 的达成仍需…供抽样」,而 O2 在 spec 里被反复定义为**长期累计锚**(§1-O1 长期层:「不靠 gate 一次发证,靠使用中持续校准兑现」)——**单份产物扛满 3 条与 O2 自身定位打架**。但我不确定:跨 run 累积会不会让「全豁免 = 空过」那个洞从单 run 换到多 run 重新打开?(c) 立法初衷正是防空过。**希望 P2 搜到 sampling adequacy 不足时的既定处置先例(accumulate vs abort vs report-insufficient),以及 pre-registration 里 outcome definition 与 analysis plan 分离的做法。** 也希望对方在 P3 直接回答:有没有一种挂法能同时满足「防空过」与「不逼 judge 造判断」。

2. **给 C9 门①补声明机制,会不会就是「开豁免」换个说法。**
   `writer.py:85-97` 自己把「给门①开豁免」列为三条坏路之首,理由是「为了让自己刚写的代码过而给安全门加豁免 = 门被人为关掉的经典前戏」。我提出的「补一个与②同构但更严格的声明机制」**在形式上难以与它区分**。区别可能在于**谁批准、什么时候批准**——②的 `DECLARED_READ_SITES` 是**预先存在的通用机制**,而为 R4-F4 现开一个就是**事后特批**(这正是 forge v4 已经 cut 掉的 β 形态)。**希望 P2 搜 security control exception / risk acceptance 的正当化条件与审批分离原则**,尤其「谁有资格批自己代码的例外」。我现在**说不清**这条线该画在哪。

3. **产物「1 条低置信判断」到底是缺陷还是诚实。**
   两种读法都有 spec 支撑:按 (c) 是**样本不足**(不得判 PASS);按 O4/OUT-8 是 judge **正确地**没有硬凑。决议 38 用「200 篇不稀疏语料」论证是前者,但我注意到一个反向线索:`judge.py:118` 的 `not anchor_map` 退路会在**无可锚 provenance** 时直接产 1 条低置信判断且不调 LLM——**而本次产物恰好只有 1 个可用锚(1 击)**。我**没有证据**判断本次是走了 `:92`/`:118` 哪条退路还是正常 LLM 路径只返 1 条,这在归因上是决定性的差别(退路 = 上游 provenance 问题;正常路径 = prompt 问题)。**希望对方在 P3 前先确认这个事实**,或在 P2 阶段各自去读一次本次 run 的 journal `rationale` 与 briefing 抽样计数段的组合能否倒推出来。这是本轮我最担心「在事实未定时就裁判据」的一处。
