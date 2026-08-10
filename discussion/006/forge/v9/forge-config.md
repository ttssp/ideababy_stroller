---
forge_version: v9
created: 2026-08-04T00:29:49Z
convergence_mode: strong-converge
x_hash: 7ad1bb97a7760addddb7cd371eca3b71
prefill_source: manual(caller v9 批次 = XenoDev dogfood-backlog 证据完整性家族 4 条 + IDS HANDBACK-LOG 第 40/42 条实测证据 · 非 proposals.md prefill)
---

# Forge Config · 006 · v9

## X · 审阅标的

discussion/006/forge/v9/_x-batch-snapshot.md
/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/dogfood-backlog.md
discussion/001/handback/HANDBACK-LOG.md
framework/SHARED-CONTRACT.md
.claude/commands/handback-review.md
discussion/006/forge/v8/stage-forge-006-v8.md
CLAUDE.md

### 解析后的标的清单

- `discussion/006/forge/v9/_x-batch-snapshot.md`(类型:本仓库文件 · **权威快照 · 首选阅读源 ·
  自足** · ✅ 可达。六部分:Part 0 四条缺口的共同结构;Part 1 IDS 侧两次独立真核的实测证据
  (含 **1.3 一项比 KG-B11 更坏的精确化**,请重点核);Part 2 四条 backlog 原文;
  Part 3 现行机制**带行号的现场原文**(XenoDev SKILL ×3 + IDS SHARED-CONTRACT + handback-review 命令);
  Part 4 四个待判问题;Part 5 本快照自身的诚实边界。**外部路径 BLOCK 时以本文件为准。**)
- `/home/ys/codes/XenoDev/.claude/worktrees/001-radar-pA/dogfood-backlog.md`(类型:外部 repo 文件 ·
  ⚠ Codex 沙箱可能 BLOCK · 仅作能读时的原文核对源。**1768 行,勿整读** —— 用 Grep 定位
  `KG-B11`(:721)/ `XD-41`(:1486)/ `XD-43`(:1568)/ `XD-44`(:1722)四段。
  ⚠ 注意这是 **worktree 分支**的那份,XenoDev main checkout 的 dogfood-backlog.md **没有 XD-41..44**)
- `discussion/001/handback/HANDBACK-LOG.md`(类型:本仓库文件 · ✅ 可达 · **173k,严禁整读** ——
  只读三段:**第 40 条**(`:891` 起 · 首次发现 R-Q7 未调用)· **第 41 条**(`:1070` 起 · chair 条款
  第一次执行 · 逐条 addressed 裁决)· **第 42 条**(`:1155` 起 · **本轮升级依据 · 复发计数 +1**))
- `framework/SHARED-CONTRACT.md`(类型:本仓库文件 · ✅ · **协议 SSOT** · 只读 **§6 B-4-IDS**
  `:911-1030` —— verdict-evidence consumer contract + `:993` known-gap 注记
  「consumer 校验深度 < producer」。🔴 重点:`:949` 协议写「任一字段缺 = consumer REJECT」,
  与实装「父键不存在 ⇒ 整步跳过不 warn」有落差)
- `.claude/commands/handback-review.md`(类型:本仓库文件 · ✅ · **「缺席即豁免」的实装现场** ·
  读 Step 2(§6.2.1 六约束)+ Step 4.2/4.3(validator 调用 + verdict-evidence syntax-precheck
  的 `if grep -q '^ids_verdict_evidence:'` 条件))
- `discussion/006/forge/v8/stage-forge-006-v8.md`(类型:stage 文档 · ✅ · 最近 verdict 承接 ·
  只读 Verdict / decision matrix / underweights / v0.2 note 四节。**注意:v8 的四簇
  (B2+worktree / B3+B6 / B4+B7 / B5)不含本批次任何一条**;v8 自列的 v9 触发器 (a)(b)(c)(d)
  **全是观察位且一条都未触发** —— 本轮驱动力完全来自新证据,不是 v8 的预留口)
- `CLAUDE.md`(类型:本仓库文件 · ✅ · IDS 宪法 —— 「框架级变更只走 forge / XenoDev 不当场改」
  铁律的定义处,是 XD-43/XD-44「不当场改」行为的规约来源)

## Y · 审阅视角

✅ **工程纪律**(主视角:review gate 的执行强制 / 证据入仓 / 收敛判据 / 替代路径的可信边界 ——
  四条缺口全部落在「评审这件事本身怎么被保证」上)
✅ **架构设计**(「缺席即豁免」是否存在**通用机制解**,还是必须逐点接线;R-Q7 双写范式的调用点
  归属;门与被门对象的绑定语义 —— XD-43 建议 2 的「内容绑定」是接口设计问题)
✅ **安全**(完整性与防篡改面:stale pointer 构成**错误的正信号**比证据缺失更危险;
  XD-41 的「产物能说谎」族;伪造/stale verdict 流入下游的威胁模型 —— §6 B-4-IDS 的立法本意
  就是「防伪造 verdict」)

## Z · 参照系

mode: **对标 SOTA**

**检索方向**(P2):
- **tamper-evident / append-only 审计日志**(hash chain · WORM · Merkle 化记录)——
  immutable review record 的业界形态与最小可行实现
- **供应链证明 / provenance attestation**(SLSA · in-toto · Sigstore)——
  「这次评审真的跑过、且跑的是这份内容」如何做成可验证声明(直接对应 XD-43 建议 2 的内容绑定)
- **CI 强制执行门**(GitHub required status checks / branch protection / policy-as-code 如 OPA/Conftest)
  —— 「门实装了但没人调用」在业界怎么被结构性排除;**尤其:如何表达「该跑而未跑 ≠ 通过」**
- **stale approval 失效机制**(GitHub `dismiss_stale_reviews` · Gerrit label 重置)——
  pointer/签字 stale 的成熟判据,以及误报边界
- **code review 收敛的经验研究**(review 轮次与缺陷发现率 · defect escape rate ·
  何时该停)—— XD-44 的「轮次上限 vs finding 类别重复」哪个更有实证支撑

**外部材料叠加**:无

## W · 产出形态

✅ **verdict-only**(单一 verdict + 短 rationale)
✅ **decision-list**(四条缺口逐条:保留现状 / 调整 / 新增机制 / defer,4 列矩阵;
  每条须标簇号 + P 级 + **证据源**)
✅ **refactor-plan**(按簇分组的改造方案;mirror 件须标 SSOT 侧改 + cp 回 mirror + MANIFEST SHA 更新的同步顺序)

(❌ 不产 next-dev-plan —— operator 本轮显式不要;落地排期在 verdict 落定后另议)

## K · 用户判准

**[006 大方向背景 · 本轮不重开]**

给定一个 PRD,claude code 可以几乎没有人工干预的情况下自主完成开发任务。我需要一个**可靠的、
自动化程度最高**的解决方案。我是非软件开发背景 —— 我可以把需求描述清楚,也可以尝试构建较可靠的
PRD,但缺少软件开发经验,对各规模开发的方案、流程、规范没有把握。我希望双方凭借最强的 AI 专业
能力与最丰富的软件开发经验,通过调研、论证、思辨、构思、设计、整理归纳,达成一套基于 claude code
实现**可靠**自动化开发的 framework/pipeline 的共识方案。

**[v9 本轮判准 · 真实审议主体]**

本轮**不重开 006 大方向**,专审**证据完整性家族**四条缺口 —— 它们共享一个结构:
**机制存在 → 但它的执行/证据/充分性没有机器落点 → 于是缺席被静默当作通过。**

- **KG-B11**(medium · 但**已被两次实测升级**):R-Q7 评审记录只产 singleton 不产 immutable。
  ⚠ **实测显示的是更坏的第三态:v0.7/v0.8 连 singleton 都没写**(v0.6 双写齐全 ⇒ 步骤曾经工作过)。
  **KG-B11 的诊断可能不足以解释现象。**
- **XD-41**(high):替代路径评审放行的代码,gate 恢复后 4 轮抓 21 条(11 high);
  **needs-attention 事实上等价于放行**;子代理与被审代码同源同上下文、不跨 task 看。
- **XD-43**(high):preflight 门实装了但**没有任何入口调用它**,从未被执行过;与 KG-B4 是同一条链前后两段。
- **XD-44**(medium):4 轮上限对状态机式协议设计系统性偏低(v0.7 五轮 / v0.8 十一轮两独立实例);
  建议改用「finding 类别是否重复」作收敛信号;并请判 5+11 是否合并计为 16。

**operator 在乎**:

1. **要 enforcement,不要又一条建议。** 本轮升级为阻断级的**唯一依据是复发计数**:
   HANDBACK-LOG 第 40 条已把 R-Q7 路由 forge 攒批,**下一个包原样复发**(第 42 条)。
   ⇒ 已经证明**单靠 forge 路由而无机器落点,该缺陷会稳定复发**。**再给一条"建议改 SKILL"等于第三次。**
2. **先判故障态,再定修法。** 见 X 快照 Part 1.3 —— 若按 KG-B11 的「不对称」修而真因是
   「步骤未被调用」,**会修出一个假的完成感**(这恰恰是本家族的病症本身)。
   **请独立验证,不要因该推断来自 IDS 侧就采信。**
3. **「缺席即豁免」需要的是「该带而未带」的判据,不是「未带就拒」。**
   §6 B-4-IDS `:993` 的 known-gap 已实证:字面严格化会对**每个合法老包** REJECT。
   ⇒ 简单收紧是死路,**别给一个会误拒的方案**。
4. **不过度工程**(延续 v7 D1「只落止血核心」+ v8「worktree 复用原生零自建」两个先例)。
   四条里若有可以合并成一个机制的,合;不能合的说清为什么不能。
5. **尊重证据权重**:XD-41(21 条 / 11 high 真跑)与 XD-43(codex 三轮重报)是硬证据;
   KG-B11 现在有两次独立实测;XD-44 有两个独立实例。**证据强度不同,处置档位可以不同。**
6. ⚠ **回声室风险本轮最高**。v8 已自标「echo-chamber 风险高于 v7」,而**本批审的正是
   「评审机制自身失效」** —— 一个由 AI 评审 AI 评审机制的 forge,结构上就在这个家族的射程内。
   **请双方在 P3R1 §4 显式自检:本轮的结论本身有没有落进「缺席即豁免」?**
   (例:因为没人反对就当作共识 = merely noted;RFC 7282 的 addressed vs merely noted 区分
   已在 forge 001 v6 立为本仓条款,本轮适用。)

**硬约束**:
- **框架级变更只走 forge,XenoDev 不当场改**(CLAUDE.md 铁律 · 防 V4 失败模式)。
  XD-43/XD-44 已按此办(只记不改),verdict 须给可下发的落地条目。
- **mirror 件(bootstrap-kit)改动必须 SSOT 侧改 + cp 回 mirror + MANIFEST SHA 更新**
  ——`SHARED-CONTRACT.md` 的 SSOT 在 **IDS** 不在 MANIFEST(与 bootstrap-kit mirror 反向)。
- 改 `§6 B-4-IDS` 属 **spine 协议条目**(协议改错 → XenoDev phase X 4 task 全 rework · risk=high),
  须 bump `contract_version` + Changelog entry。
- **不碰批次外条目**:KG-B8 / B9 / B10 / B12 / XD-42 本轮**显式留在批次外**,不是遗漏,别顺手裁。

## 收敛强度

✅ **strong-converge**(必须 finalize 单一 verdict;残余分歧降级为 v0.2 note。
理由:本批需要的是可执行 enforcement,两条并存路径会让「缺席即豁免」又一次悬置)

---

## Summary for reviewers

**审阅标的总数**: 7(1 权威快照[首选·自足] + 1 外部 backlog 原文[⚠BLOCK 可跳·勿整读·Grep 四段]
+ 1 决议日志[⚠严禁整读·只读第 40/41/42 条] + 1 协议 SSOT[只读 §6 B-4-IDS] + 1 实装现场
+ 1 v8 verdict 承接 + 1 仓宪法)
**视角维度**: 工程纪律(主) · 架构设计 · 安全
**参照系**: 对标 SOTA(tamper-evident 审计日志 · SLSA/in-toto provenance attestation ·
CI required checks / policy-as-code 强制 · stale approval 失效 · review 收敛的经验研究)
**预期产出**: verdict-only + decision-list(4 条逐条 · 标簇/P 级/证据源) + refactor-plan(按簇 · 含 mirror 同步顺序)
**用户最在乎**: **要 enforcement 不要第三条建议**(复发计数已证路由无用) · **先判故障态再定修法**
(KG-B11 诊断可能不足以解释实测) · 「该带而未带」的判据而非「未带就拒」(严格化会误拒合法老包) ·
不过度工程 · 尊重证据权重差异 · **⚠ 显式自检本轮结论有没有落进「缺席即豁免」/ merely noted**
**收敛模式**: strong-converge
