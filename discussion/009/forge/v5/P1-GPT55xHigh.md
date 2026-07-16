# Forge v5 · 009 · P1 · GPT-5.5 xHigh · 独立审阅(no search)

**Timestamp**: 2026-07-16T11:05:54Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:`forge-config.md` 全文,确认 X/Y/Z/W/K 与 strong-converge;`moderator-notes.md` 不存在;`operator-input-2026-07-16-implicit-signals.md` 全文;`proposals.md` 第 276 行到 EOF;`009-pForge/PRD.md` 全文;`HANDBACK-LOG.md` 的 2026 entry 标题,并精读 2026-07-06 M-fork-complete 与 2026-07-07 P2-prod-precondition-gap;`stage-forge-009-v4.md` 全文;`xenodev-alpha-assets-snapshot.md` 全文;`.claude/skills/forge-protocol/SKILL.md` 的 P1 模板;`AGENTS.md` 全文。
- 我跳过的:外部 `XenoDev/projects/004-pB` 与 `collection.db` 原路径均被当前沙箱以 `bwrap: loopback: Failed RTM_NEWADDR` 阻断;按任务约束,这不算 BLOCK,以内部快照件替代。没有读取 `P1-Opus47Max.md` 内容。
- **K(用户判准)摘要**:我把 K 理解为两句硬约束:009 的本质是把 004/008/alpha 回测/信号蒸馏合成“完整投资决策闭环”,且产品本质是“用工程强项补齐投资 domain 短板”。v5 新增事实修正更关键:该分析师“不产显性荐股 call”,009 实际要造的是从笔记/直播的隐性信息中学会他怎么看盘,回测只是考官。
- **我的阅读策略**:按 Y 三视角读。产品价值先看 operator 事实修正是否改变价值锚;架构设计看 M1/M2、004、008、提取头之间边界;工程纪律重点看 M2 已有 PIT/DSR/PBO 严格性能否延伸到文本提取层。

## 1. 现状摘要(按 Y 视角组织)

### 产品价值

原 proposal 的价值锚是 operator 不懂投资,希望用工程把外部专家内容、回测验证、纪律执行连成闭环。M1+M2 已把“价格地基 + alpha 评估机器”做成 743 passed 的可用资产,但 07-07 之后才发现机器没有输入。2026-07-16 的事实修正进一步说明:不是缺少搬运,而是原本假设的显性 `(ticker,direction,date)` 信号不存在。

因此当前产品问题已从“这个分析师行不行”变成“分析师隐性信息 × 提取方法这组联合假设行不行”。这不削弱闭环价值,反而更贴近 K:operator 真正想补的是读懂盘前/盘中/直播里零散信息的能力,不是复刻一个荐股榜。

### 架构设计

M1/M2 的边界很清楚:M1 给 PIT 价格层,M2 用 frozen join、realized return、DSR/PBO 和 O8 evidence lane 给出评估端数字。v4 已把 alpha 质量定义成非方向 evidence,上游回答“信号质量如何”,下游 004 仍负责纪律与执行不走样。

现 PRD 把“蒸馏 lane”放在 M4 OUT,前提是 M2 能先吃到显性信号。该前提已失效。008 现在是内容库:records 有 `published_at/captured_at/raw_ref/form`,还有 `record_tickers` 但语义未裁。004 三表和 M2 join 则只接受已解析、无歧义的信号。缺口位于 008 内容与 M2 join 之间,不是 004 下游展示层。

### 工程纪律

评估端纪律资产很强:双 as_of 价格轴、精确交易日命中、七类 join 拒绝、O9 insufficient_sample、trial-count、DSR/PBO 都已经定型。07-07 smoke path 原决议选择手工塞少量真历史信号以避免通用 backfill 越界,但该路径依赖显性真值,现在不可执行。

v5 的纪律焦点必须上移到文本侧。operator 提的两条红线都与既有 M2 哲学一致:每个提取规则/prompt 变体计入 trial_count,防在噪声里调到回测好看;提取只能用信号时点前已发布文本,把 `published_at` 变成文本侧 PIT 轴。美光/海力士记忆只能当 sanity check,不能当提取规则的答案来源。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由 |
|---|---|---|
| 产品价值 | refactor + new | keep 009 闭环与 M1/M2 资产;但价值命题需 refactor 为“隐性信息提取器是否能产可评估疑似信号”。提取头应 new,否则 operator 真需求没有入口。 |
| 架构设计 | refactor | cut 07-07 smoke path 的显性信号手工塞入前提;把“蒸馏排 M4 末位”改成“提取/蒸馏的最小前置器官”,但不要动 004 纪律壳和 M2 评估端。008→004 桥不应只是机械搬运,应以提取头产物/适配边界重新定义。 |
| 工程纪律 | keep + new | keep M1/M2 的 PIT、拒绝行、DSR/PBO 与 anti-PPV 终点;new 两条文本侧红线:prompt/rule variant 入 trial_count,文本 published_at PIT。验收终点应是真接受/拒绝行与真回测数字,不是“提取器跑通”。 |

具体对象上:我会保留 M1/M2 既有资产;废止 07-07 smoke path 作为主路径;调整原 M4 蒸馏排期;新增提取头;采纳 operator 两条红线为硬纪律;把 008→004 桥归属从“backfill 搬运”改判为“提取头及其输出适配”的问题,但正式 schema 仍需后续裁。

## 3. 我现在最不确定的 3 件事

1. 隐性信号能否被定义到足够可审计:同一句“看好主线/预警风险”到底落 sector、ticker、方向、horizon 还是置信区间,不同标注口径会直接改变回测结论。
2. `record_tickers` 的真实语义:它是采集侧弱关联、标题/正文命中,还是已有人类/规则消歧过的候选?这决定提取头是复用、校验还是完全重建 ticker 解析。
3. 联合假设如何拆账:若回测不显著,失败可能来自分析师无 alpha、提取器差、样本少、文本噪声或 market/horizon 选错。P2/P3 需要裁最小实验如何避免把这些失败原因混成一团。
