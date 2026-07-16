# Forge v1 · 001 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-07-15T13:30:37Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:
  - `discussion/001/forge/v1/forge-config.md` → 读取 X/Y/Z/W/K、strong-converge 和本次真实标的。
  - `proposals/proposals.md` 行 99-134 → 只作为 Research Radar 原始愿景背景。
  - `discussion/001/001-radar/L3/stage-L3-scope-001-radar.md` → 整文件,重点读 Candidate A 的信任三件套、A→B 顺承关系、Honesty check。
  - `discussion/001/001-radar/001-radar-pA/PRD.md` → 整文件,重点读 v1.2 O4 双层信任、Moderator injection response、Open questions #3。
  - `discussion/001/handback/20260715T093226Z-001-radar-pA-20260715T093226Z.md` → 整文件,作为本次 forge 第一触发因。
  - `discussion/001/handback/HANDBACK-LOG.md` → 整文件,读 11 条 hand-back 决议史。
  - `discussion/001/001-radar/L3/moderator-notes.md` → 整文件,读 2026-07-10 与 2026-07-13 两次 hard injection。
  - `discussion/001/handback/20260711T135303Z-001-radar-pA-20260711T135303Z.md` → 整文件,作为能力层 FAIL 对照。
  - `/home/ys/codes/XenoDev/dogfood-backlog.md` 行 525-640 → 读 KG-B4/B7/B8 原文,未使用 inbox 内嵌摘录兜底。
  - `.claude/skills/forge-protocol/SKILL.md` → 读 P1 模板与约束。
  - `AGENTS.md` → 读 repo 级铁律、forge 入口、跨仓边界和中文输出要求。
- 我跳过的:`discussion/001/forge/v1/moderator-notes.md` 不存在;`discussion/001/forge/v1/P1-Opus47Max.md` 按 hard constraint 未读;本轮未联网。
- **K(用户判准)摘要**:K 明确说本次真实标的不是宽泛 research-radar seed,而是已 ship 的 `001-radar-pA` 里 **P0.2 盲测 gate 的形态治理**。用户最在乎的张力是:保留弱化版 gate,还是彻底改成可审计留痕验收;同时同簇裁 KG-B8(gate 形态)、KG-B4(gate 无机器强制)、KG-B7(反作弊单次执行)。K 还明确说不在乎现有 gate 代码沉没成本,但要保留防 V4 的精神。
- **我的阅读策略**:先把 2026-07-11 首跑 FAIL 和 2026-07-15 拒签分层,避免把“pipeline 能力不够”和“gate 治理形态不成立”混成一个问题;再按 Y 的工程纪律、架构设计、产品价值三条线读同一组事实。

## 1. 现状摘要(按 Y 视角组织)

### 工程纪律

当前纪律层有两股相反力量。正面是 L4/hand-back 边界守得很硬:首跑 FAIL 后 T010/T011 未起,hand-back 回 IDS 决议,PRD v1.1/v1.2 都有显式 injection response;2026-07-15 形态拒签后也没有在 XenoDev 静默改 spec,而是升级 forge。AGENTS.md 的“PRD source-of-truth after L3”“No code without hand-off”“pre-merge review mandatory”在这条链路里实际生效。

但 gate 的机器纪律没有真正闭环。KG-B4 指出 `evaluate_gate` 和 `write_prd_revision_trigger` 是库函数,没有生产路径把“gate PASS artifact 存在且判 PASS”接到 T010/T011 preflight;parallel-builder 主要靠 markdown depends_on 和“task 已 merge”判断。KG-B7 又显示,一旦把 gate 设计成人在环、机器对答案的二值机制,反作弊执行语义会膨胀:run 绑定、nonce、FAIL reason 泛化只能堵已知泄露面,无法消除可重跑/试错的结构面。

### 架构设计

PRD v1.2 已经不是原始硬 gate。O4 被拆成初始层和长期层:初始层 P0.2 盲测 gate 只看真切片可信、阴性对照识伪;要件③新证据链降级为使用期校准信号;长期主锚移到 O2 三击回溯和 O5/O7 journal 后验复核。L3 Candidate A 原本的信任三件套也是证据链、journal、盲测校准并列,不是只靠盲测发证。

架构张力在于:文档语义已把信任主轴迁出 gate,但依赖结构仍把 `P0.2-RERUN-PASS artifact` 作为 T010/T011 唯一前置。也就是说,PPV 的叙事从“长期校准”转向 O2/O7,而 DAG 解锁点还停在“一次性二值 PASS”。KG-B8 是更上游的架构信号:若 gate 形态本身不应存在为硬前置,则 B4 的强制点和 B7 的单次执行反作弊都可能是在加固一个被上游否决的接口。

### 产品价值

产品价值层的事实最直接:operator 真跑后拒绝填要件③,并给出三条批评。第一,他不认为自己是可靠二值打分器,单轮 3 切片 1 负控的统计功效也低。第二,他要的是每条位移判断有 source trace,能快速抽查,发现问题后 agent 有 log 可回溯调整。第三,他倾向在使用中发现问题、解决问题、回溯更新,不想为一个 local 解付出高摩擦前置考试。

这和原始 Research Radar 愿景并不冲突,反而更贴近“长期跟进、梳理脉络、可靠前瞻判断”。PRD v1.2 还把 Candidate B 的“跟踪动态/及时同步”记为 v0.2 复活信号。当前盲测 gate 的问题不是它完全无价值,而是它把用户自然的审计与校准工作流转换成了停机式签字仪式,产品体验和 operator 的真实判断习惯出现错位。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 工程纪律 | refactor | 防 V4 的 FAIL→STOP 精神应保留,但现在 gate PASS 与下游解锁没有机器闭环;若继续有任何阻断语义,B4/B7 说明执行契约必须重构,不能靠 markdown 纪律。 |
| 架构设计 | refactor | PRD 语义已转向 O2/O7 长期信任链,但 T010/T011 仍绑定一次性 RERUN-PASS;这是依赖结构滞后于 PPV 语义。 |
| 产品价值 | cut | 我倾向切掉“人肉盲测二值硬前置”这个产品仪式。它和 operator 的边用边审计工作流冲突,且沉没在 B7 的反作弊成本里;是否保留非阻断 smoke 信号留到后续阶段裁。 |

## 3. 我现在最不确定的 3 件事

1. 如果切掉二值硬前置,什么最小机制仍能保留防 V4 的“明显不可信就停”精神,而不是滑回随意续建?我希望 P2/P3 重点验证可审计留痕、抽查、后验校准在类似场景里的边界。
2. P0.2 盲测是否仍值得作为低成本 smoke signal 存在?当前事实只能证明它不适合作唯一硬闸门,还不能证明它完全没有诊断价值。
3. T010/T011 的新解锁条件应落在“先证明 trace 完整性”还是“先进入有限使用、由 journal 累积校准”?这会决定 B4/B7 是自然消解,还是需要保留一部分 gate 执行契约。
