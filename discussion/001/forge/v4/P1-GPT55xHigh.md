# Forge v4 · 001 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-07-18T01:45:00Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:`forge-config.md`;`moderator-notes.md` 不存在;IDS 侧 `stage-forge-001-v3.md`、hand-back 19、PRD v1.5、`HANDBACK-LOG.md`;XenoDev 侧 `selfcheck_sequence.py`、`cli/reconstruct.py`、`scripts/selfcheck-07-17.sh`、07-17 briefing、`test_selfcheck_sequence_forge_v3.py`;以及 forge-protocol P1 模板。
- 我跳过的:未读 `P1-Opus47Max.md`;未做 web search;密封 JSON 只指认文件名,不读内容。实际枚举只看到同 stem `diffusion-models-20260717T051551Z.runbinding.json`;`_answer-key-*` 语义来自 hand-back/附录,我未打开。

**K 摘要**:K 写明“本次只裁一件事:生效条款标的重裁”。第五次后的铁律是新条款必须有真跑可执行步骤,不能把“首个评估 run”再次悬空;同时要求“护栏不拆”“不新建机制”,并把烧 key 与 key 轮换时序裁进去。我的阅读策略是先分离四模块机制是否成立,再看 PRD O4 的生效标的是否自洽。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 架构设计

v3 拓扑已变成评估/校准分流:评估 run 默认不注入负控,生成时落 human-readable markdown 与 audit.json;校准 run 用 `--calibration`,保留盲测、负控、answer-key、run-binding,但零解锁语义。D″ 自证序列在评估侧生成 audit,再跑 B′ 结构谓词和 D′ journal 核验。错配只在标的:PRD v1.5 O4 仍写死对 07-17 产物自证,但该 briefing 标题含“位移重建(盲测)”,正文含盲测说明和阴性对照提示,且 slice 无评估面来源块。D″ 三道守卫正是在防止校准产物流入评估解锁链。

### 视角 B · 工程纪律

hand-back 19 记录四模块已落地,354 passed,9 轮 codex review approve;round-2 抓到评估产物标题非 B′ 可解析的真生产 bug,后续把 shape/parser 守卫收紧到 fence-aware 与 B′/D″ regex 单一真相。测试覆盖合成 retriever 恒 fixture、校准 stem STOP、盲测正文 STOP、删 marker 后仍 STOP、fence padding coverage STOP。对 07-17 执行 D″ 的正确结果是 STOP,不是 PASS;这不是代码未完成,而是 v3 条款把 pre-split 校准产物当作 split 后评估 evidence bundle 消费。评估 run 生成 briefing 要走真 LLM,会烧 DEEPSEEK key;自证序列本身不烧 key。

### 视角 C · 产品价值

operator 要的是边用边迭代、留痕可审计的评估流,不是一次考试感 gate。07-17 产物有盲测提示和负控,更像历史校准活动样本,适合保留为识伪/校准证据,不适合当日常评估 run 解锁凭据。贴近工作流的标的应是下一份默认评估 run 产物;但若“下一份”没有授权、时间、key 轮换顺序,它又会变成新的悬空承诺。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由 |
|---|---|---|
| 架构设计 | refactor | 四模块和分流拓扑可 keep,但 O4 的“07-17 真产物”标的必须改;β 会拆掉正好挡住错配的边界。 |
| 工程纪律 | refactor | 护栏与测试应 keep;条款要改成可真跑兑现的对象,并写入 key 轮换/授权时序。 |
| 产品价值 | refactor | 07-17 降为校准历史样本最贴合 retire-as-gate keep-as-calibration;首个评估 run 自证贴近真实使用,但不能悬空。 |

对 α/β/γ 的第一反应:倾向 **γ,但必须带硬兑现条件**。07-17 降为校准活动历史样本;生效条款改绑首个默认评估 run 产物。**β 应 cut**:它是特批旁路,和 9 轮刚建的守卫冲突。**α 更像 γ 的立即兑现形态**:若 operator 要现在解锁,就先完成 key 轮换/授权,烧一次 DEEPSEEK key 生成评估 run 新产物,落地即跑自证;否则条款状态应诚实保持“未生效”,不能口头 PASS。

## 3. 我现在最不确定的 3 件事

1. P2 需要查外部参照:把历史校准样本从生效证据降级为 calibration record,是否有更标准的治理措辞?
2. γ 的“首个评估 run”应写到多硬:下一次默认评估 run 同事务自证,还是 key 轮换后立即执行一次?
3. XenoDev worktree 未 commit 的收编时序是否影响风险:是否应把收编 commit 与首次评估 run 自证绑定为同一验收包?
