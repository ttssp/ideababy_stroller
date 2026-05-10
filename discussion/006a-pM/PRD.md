# PRD · XenoDev v0.1

**PRD-form**: simple
**Status**: approved
**Sources**: discussion/006/forge/v2/stage-forge-006-v2.md §"Next-version PRD draft (W4)" + moderator-notes §一/§三/§五
**Forked-from**: forge 006 v2 stage-forge-006-v2.md (B2.2 Block B operator manual L3 — 不走 IDS 完整 L1-L3 流程,per stage doc M4)

---

## User persona

能写 PRD 但**非软件背景**的 operator(Yashu Liu)。痛点:对各规模(大中小型)开发的方案、流程、规范没有把握(K2+K3)。

不熟悉:spec/task 拆解、parallel build 编排、跨仓 hand-off 协议细节。

熟悉:idea 描述、PRD 写作、读 stage 文档、做拍板决策。

## Core user stories

- **US-1**:operator 在 IDS 完成 PRD 后,触发 hand-off 进 XenoDev,**几乎不需要手工转写**(K1)
- **US-2**:XenoDev 自动拆 spec → tasks → parallel build → ship,operator 仅在 hand-back / 重大决策时介入
- **US-3**:Small 项目可绕过 XenoDev 完整 L4(直驱 Claude Code + AGENTS.md + Safety Floor 轻入口),Medium/Large 才走全链(K3)
- **US-4**:每次 build 完产 hand-back 包,operator 在 IDS 看到反馈(drift / PRD gap / 统计)
- **US-5**:任何高风险破坏性操作被 Safety Floor 阻断,留人审

## Scope IN

v0.1 必落 5 件(per forge 006 v2 verdict):

- **IN-1**:Safety Floor 三件套(凭据隔离 + 不可逆命令 block-dangerous.sh + 备份破坏检测)
- **IN-2**:单一 build spec source(在 XenoDev,对齐评估 fork Spec Kit 0.8.7 现行 schema + 自带 PPV 扩展;per `framework/spec-kit-evaluation.md` 推荐 adapter 模式)
- **IN-3**:workspace schema 4 字段一等建模(`source_repo` / `build_repo` / `working_repo` / `handback_target`;per `framework/SHARED-CONTRACT.md` §6.2)
- **IN-4**:hand-back 包结构化(drift / PRD-revision-trigger / 实践统计三类标签;per §6.3)
- **IN-5**:Eval/risk 数据接口(append-only event log,记 review failures / operator interventions / hand-back drift;**v0.1 不实装 scoring 算法**)

## Scope OUT(显式 non-goals)

- **NOT** SaaS / 多用户(operator 单人;evidence: `discussion/006/forge/v2/stage-forge-006-v2.md` §"P3R2-GPT §4 W4")
- **NOT** 完整 Eval scoring 算法 / risk tier verdict / 阈值数字(evidence: stage doc §"v0.2 note 2")
- **NOT** 继承 V4 repo 任何 code(L+P 作为 lesson,C 仅 cp `block-dangerous.sh`;evidence: stage doc §"模块 B" step 2)
- **NOT** 复制 forge 机制(forge 在 IDS 治理仓集中管;evidence: stage doc §"moderator-notes §四")
- **NOT** 支持 Small 项目走完整 L4 全链(Small 走轻入口;evidence: stage doc §"K3 + W2 tier policy")

## Success looks like

可证伪标准:

- 跑通 ≥1 真实 PRD 的 small/medium task `build → ship → hand-back` 完整 round-trip(目前 = 本 PRD 自身;`framework/b2.1-dry-run-validation.md` 已验 dry-run mock 路径)
- 所有高风险破坏性操作被 Safety Floor 阻断 = **0 漏**(以 `framework/xenodev-bootstrap-kit/safety-floor-2/block-dangerous.sh` 24 类 dangerous patterns 为基线)
- operator 干预率 < X%(具体 X 由 v0.2 note 2 定;**v0.1 仅记录原始 event,不算阈值**)
- hand-back 包格式 operator 可读可消费(主观评分 ≥ 7/10;评分维度见 `plan-rosy-naur` v11 Block G)

## Real constraints

- **时间**:operator §6.7 不设上限,但 v0.1 ship 节奏参考 = 2-4 周(B2 全部 milestone)
- **预算**:operator 单人 + Claude Code subscription(无云成本预算)
- **平台**:macOS / git / Claude Code CLI
- **合规**:无外部用户 → 隐私合规 N/A;但凭据隔离仍是 Safety Floor 必备

## UX principles

- operator 主动介入越少越好(K1)
- 失败时 hand-back 必显式说明 root cause + 建议(不让 operator 猜)
- 高风险时显式拒绝(hard block)而非提示(防 9 秒删库 — Cursor + Claude tomshardware 2025 案例)

## Open questions(forge / scope 阶段未解决的)

- **OQ-1**:成功指标 N(连续 idea 数)和干预率 X 的具体阈值 — 需 XenoDev 跑 ≥3 真 idea / 30 task 后回看(v0.2 note 2)
- **OQ-2**:Spec Kit 0.8.7 schema 与 PPV 第 7 元素兼容度 — XenoDev 第一个真 PRD 起 sdd-workflow 时回看(v0.2 note 1;`framework/spec-kit-evaluation.md` 已预答 adapter 模式)
- **OQ-3**:Small → Medium 升级触发器精确判准(代码行 / 工时 / 跨仓需求 / 等) — XenoDev 跑过 ≥1 Medium 项目后回看(v0.2 note 5)
