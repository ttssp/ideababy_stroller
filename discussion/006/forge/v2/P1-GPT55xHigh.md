# Forge v2 · 006 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-05-09T12:38:50Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:`forge-config.md` / `moderator-notes.md` / `_x-input-draft-by-operator.md`;`/Users/admin/codes/autodev_pipe` 的 `.claude/`、`specs/v4/`、`docs/decisions/`;`solo_ai_pipeline_v3.1.md`;V4 `spec.md`;ADR 0008/0009;ADP `sdd-workflow`、`task-decomposer`、`block-dangerous.sh`;IDS `specs/007a-pA/spec.md`、`HANDOFF.md`、007a-pA R1/R4 review outbox;`framework/SHARED-CONTRACT.md`、`AUTODEV-PIPE-SYNC-PROPOSAL.md`、`NON-GOALS.md`、`ADP-AUDIT-2026-05-08.md`;forge protocol P1 template;本仓 `AGENTS.md`。
- 我跳过的:`discussion/006/forge/v2/P1-Opus47Max.md`(按并行独立硬约束不读);v1 X #1-#9(按 no-rerun 不重审);web search(按 P1 禁止)。未通读 v1 stage;若下文触及 v1,只采用 moderator-notes 规则:**v1 verdict 仅参考,不绑定本轮 verdict**。
- **K 摘要**:K1-K6 的核心是"给定 PRD 后,Claude Code 尽量少人工干预地可靠完成开发",且可靠性优先于盲目 full-auto。**K7 必须改变读法**:ADP-next 是 framework 的"待生下半边";V4 是半年前停掉的物证,不是吸收对象。K5 中的 ADP 应理解为 ADP-next 的设计意图,不是 V4 这版实装。
- **Moderator binding 5 件事**:一,ADP-next/XenoDev 只做 PRD→spec→build→ship,IDS 只做 idea→PRD;二,§9 四个 drift 是 v2 核心证据,尤其 DRIFT-1 架构级;三,SHARED-CONTRACT 必须走 v2.0 双向 hand-off,含 hand-back;四,forge 机制保留并强制用于重大元层转向,但 v1/v2 具体 verdict 内容不具硬绑定力;五,v2 后直接拆 IDS 优化 + XenoDev 启动,不重走 L1-L3,不另起 idea/forge。
- **阅读策略**:按本轮 Y 三项看证据:架构先看跨仓边界与 source of truth;工程纪律先看 spec/review/hook/verification 是否能真实运行;Y5 先把 V4 分成 Lesson / Pattern / Component 三层,避免把沉没成本误当约束。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 架构设计

当前名义架构仍有两套语言并存:AGENTS.md §4/§5 还写 `autodev_pipe-cli build` 和 Safety Floor binding,而 `SHARED-CONTRACT.md` v1.1 已改成 operator-readable hand-off + ADP skill 入口。`ADP-AUDIT` §9 进一步指出更深问题:IDS CLAUDE.md 对 L4 的定义假设 IDS 能做 spec、tasks、parallel build、ship,但 IDS 没有 Makefile、pyproject、pytest、spec_validator 或 check-disjoint。007a-pA pilot step 1-6 跑通后,实际产出是 IDS 与 ADP 各一套 13 task,并出现 ADP task-decomposer 自发写 `working_repo` 的 emergent 字段。

### 视角 B · 工程纪律

V4 的工程纪律素材很丰富:V4 spec 有 7 元素、Production Path Verification、4 轮 codex review、append_lesson 状态机和 retrospective/lesson 机制;007a-pA 也经历了 R1-R4 adversarial review,从 BLOCK 收敛到 CONCERNS。但 Safety Floor 现状不完整:ADP `block-dangerous.sh` 覆盖不可逆命令,却没有 production credential 物理隔离和备份破坏检测;Risk tier 与 Eval Score 也在 audit 中为 0 命中。也就是说,纪律存在,但分散在历史 V4 与文档里,尚未成为 ADP-next 的产品级闭环。

### 视角 C · Y5 重做代价 / 沉没成本 / 知识保留

V4 的 Component 层不宜作为起点:它已被 operator 定义为 archive 物证,且 v4 scope 本身已降级到 L1+L2 retrospective/lesson 起步。可保留的是 Lesson:AGENTS 根上下文、7 元素 spec、PPV、reviewed-by、task file_domain、lesson 反哺、dangerous hook 的失败模式。可借鉴的是 Pattern:skill 入口、adversarial review 多轮闭环、状态机式 append_lesson。必须丢掉的是把 V4 当活系统补 gap 的惯性,以及 IDS 内部继续产 build spec/task 的双 source of truth。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由 |
|---|---|---|
| 架构设计 | new | 主线应新建 XenoDev,并把 IDS L4 重定义为 PRD 完工 + hand-off/hand-back;现有 IDS-spec → ADP-spec 双层结构已经被 DRIFT-1/3 证伪。 |
| 工程纪律 | refactor | V4 的 SDD/review/PPV/lesson 纪律值得保留为模式,但 Safety Floor、risk tier、eval、hand-back 必须在 ADP-next 重新组织成运行时闭环。 |
| Y5 重做代价 | cut | cut 的是 V4 代码库作为继承对象;keep Lesson,borrow Pattern,archive Component。否则沉没成本会继续把方向拉回"给半成品补洞"。 |

## 3. 我现在最不确定的 3 件事

1. ADP-next 成功指标中的 N 与 operator 干预率 X 应怎么量化:连续 N 个真 idea,还是滑动窗口;一次"干预"按问题数、阻塞次数还是 spec frozen 后修订次数计。
2. XenoDev 第一版是否应直接纳入 risk tier + Eval Score,还是先把 Safety Floor 三件套和双向 hand-back 做到可运行后再补统计层。
3. `working_repo` 这种 emergent 跨仓字段应被 ADP-next schema 正式吸收,还是应通过彻底改变物理位置让它消失。
