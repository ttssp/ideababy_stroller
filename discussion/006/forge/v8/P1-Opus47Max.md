# Forge 006 v8 · Phase 1 · Opus 4.7 Max 独立审阅

**Written**: 2026-07-13T11:35:00Z
**Constraints honored**: no web search · no SOTA 对比 · no 详细方案 · 基于 X 具体内容

## §0 · 我读到的标的 + 阅读策略 + K 摘要

**已读**(6/6 全可达):① `_x-batch-snapshot.md`(权威快照:operator worktree 诉求原话 + KG-B2..B7 全文 @ XenoDev cc4edeb + XenoDev CLAUDE.md 工作流摘录);② dogfood-backlog 原文(Grep 定位 508-600 行核对,未整读);③ v7 stage doc(verdict/decision matrix/underweights 三节);④ IDS CLAUDE.md;⑤ XenoDev CLAUDE.md(经快照 Part 3);⑥ proposal §006 文本(经 K)。

**K 摘要**:本轮不重开 006 大方向,审七项批次(六条 KG-B + worktree 隔离诉求),收敛 verdict + 簇化改造方案 → 双仓落地 brief。operator 在乎:可靠 > 全面、止血核心优先防过度工程(v7 D1 先例)、gate 强制性不靠程序纪律、mirror 件三层同步(本周刚实证 mirror 漂移)、动冻结契约须给迁移路径、尊重证据权重(B5 九轮/B7 三轮 = 硬证据)。

## §1 · 现状摘要(按 Y 三视角)

**架构设计**:七项批次不是七个孤立 bug,我读出**三个结构性缺口**。(a) **gate 只有判定逻辑,没有执行语义**——B4(PASS artifact 无机器查验,depends_on 只证「代码 merge 了」不证「operator 签字 PASS 了」)与 B7(答案可试错/重放,gate 代码逐个封泄露面被 codex 三轮连破)是同一缺口的静态面和动态面:框架层没有「gate 是特殊 task」这个一等概念。v7 已预判 B4 与 B2 同簇留本批,证据现在齐了。(b) **并行多线的分支拓扑无规约**——B2(parallel-builder 硬编码 main 基线,blocked-handback fork 立刻炸出 import fail + depends_on 误报)与 operator worktree 诉求(IDS 本周 001/006/009 三 idea 20+ commits 混在 forge/009-blueprint 一根分支)是同一缺口在 build 侧和治理侧的两个症状。值得注意:codex inbox v2 已做过完全同构的改造(单 latest.md → queue-per-idea),证明这个方向在本框架内有成功先例。(c) **信任边界缺陷**——B5 的根因 codex R2 一句话点破:「边界只靠 prompt 文本让模型理解,没有真实 parser 强制隔离」。`complete(prompt: str)` 单字符串入口结构上无法表达「这是数据不是指令」。

**工程纪律**:B3 最扎眼的不是 gitignore pattern 写错,而是**它静默失效了两个 task 才被发现**(T001 ship 时 §4.4 只靠 worktree 文件系统过关,证据从未入 git)——「证据存在」的检查本身没有机器牙齿,与 B4 是同族病(约定代替验证)。B6 则是反向问题:hook 有牙但咬错人,与 parallel-builder §6.1 明写范式直接冲突,说明 Safety Floor 件1 与 SKILL 层缺一致性测试——铁律与范式打架时,输的是 operator 的时间。

**用户体验**:worktree 诉求的本质是**单人多线操作的心智负担**:operator 要自己记住「现在这个 session 在哪根分支、动的是哪个 idea」,框架没有替他记。B6 高频误报(每个 ship 都可能撞)+ 每次要临场找绕法,是同一类摩擦。K 的原始愿景是「几乎没有人工干预的可靠自动化」——这两项恰是「人工干预被迫增加」的实证。

## §2 · First-take 评分(keep/refactor/cut/new)

| 项 | 评分 | 理由(基于标的具体内容) |
|---|---|---|
| B2 build 基线 | **refactor** | 基线从硬编码 main 改显式声明(参数/规约二选一留 P2 后裁);v7 判「KG-B1 解阻后自然消解」只对了一半——blocked 窗口仍会重现,且 worktree 规约(下行)落地后基线声明是其自然组成 | 
| B3 TDD 证据 | **refactor** | bootstrap-kit 模板豁免改路径无关 `!**/red-green-log/*.log`(项目内已验证可行);另需给「证据已入 git」加机器检查,否则修完 pattern 仍是约定 |
| B4 gate 静态强制 | **new** | gate 类 task 加 `gate: true` 语义 + 下游 preflight 查 PASS artifact;这是防 V4 的机器化,X 内三处独立证据(backlog 原文/红队原话/code-reviewer 佐证)同指 |
| B5 role 分离 | **new(契约变更)** | 九轮不收敛 = 证据链完整;messages-style(system=指令/user=数据)是唯一结构性解,DeepSeek/Anthropic provider 都支持;必须给 T001 冻结接口的迁移路径,不可原地爆改 |
| B6 hook 误报 | **refactor** | 三类误报模式(heredoc/变量拼路径/$())各裁白名单或标准绕法文档化;件1 non-overridable 地位不动,动的是误报面;需与 parallel-builder §6.1 协调(SKILL 与 hook 二者必改其一) |
| B7 gate 执行语义 | **new** | 单次执行/answer-key 一次性/签字不可变三要素进 gate 契约;与 B4 合为一个「gate 执行语义」模块设计,不拆两个半吊子机制 |
| worktree 隔离诉求 | **new** | session-per-idea worktree 规约,IDS+XenoDev 双仓;main 只留 proposal 期;与 B2 基线声明合簇设计。**但实现层级(纯规约 vs 命令支持 vs hook 强制)是本轮最大的过度工程风险点,见 §3** |

**Cut 候选**:无——七项全部有真实复现证据,无一是推演出来的(对齐 forge-verdict-vs-empirical-ship 教训,这批料的证据质量显著好于 v5)。

## §3 · 我现在最不确定的 3 件事

1. **worktree 隔离的强制层级**。纯 CLAUDE.md 规约(零成本但靠自觉——而本周混线恰恰发生在有规约意识的 operator 身上)、命令支持(如 idea 级 start 命令自动建/切 worktree,中成本)、hook 强制(检测「所改 discussion/NNN 与当前分支名匹配」,高成本高摩擦)——三档取哪档?v7 underweight 明言「企业级模式套单人工具链可能过度工程」,这里是同一陷阱的入口。
2. **B5 迁移的爆炸半径**。T001 冻结接口的消费面在 001 项目内有多少(reconstructor/gate/CLI/fake 至少四处)?bootstrap-kit 模板是否也内嵌了 `complete(prompt)` 形状?若模板已扩散,迁移 = 契约版本化(v1/v2 并存过渡)而非一次性替换——代价差一个量级。
3. **B4+B7 强制点的层次归属**。PASS artifact 查验放 parallel-builder preflight(SKILL 层,XenoDev 自派生可当场改)还是进 SHARED-CONTRACT gate 契约章(契约层,IDS SSOT + mirror 同步)?B7 的单次执行强制天然偏契约层(威胁模型要形式化),但 v7 D0/D1 先例提示「契约先行」与「止血核心」可以分层落——哪部分是 P0 止血、哪部分是契约章,期待 P2/P3 收敛。
