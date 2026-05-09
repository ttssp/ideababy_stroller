# Forge v2 · 006 · P3R1 · GPT55xHigh · 联合收敛 R1(标分歧)

**Timestamp**: 2026-05-09T13:04:48Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE。

## 1. 整合摘要

双方已经在主线高度收敛:ADP V4 不是 ADP-next 的继承对象,而是物证库;IDS 应退回 idea→PRD + 治理/forge + hand-off/hand-back,XenoDev 承担 PRD→spec→build→ship。DRIFT-1 是架构级证据,DRIFT-2/3 是症状,DRIFT-4 是跨仓 schema 未显式化的信号。

Opus P2 强化了两个点:一是 L/P/C 分层可融合我的 P1 "cut V4 Component" 立场;二是 skills 的物理 source-of-truth 应迁到 XenoDev。我同意。我的 P2 额外修正是:Cursor multi-root 说明跨仓不是应消灭的异常,而应成为 workspace/hand-back 一等模型。

剩余分歧不在大方向,而在 R2 verdict 的精确边界:Spec Kit "v2"能否被当作已发布事实;Eval/risk tier 在 v0.1 是留接口还是实装算法;K3 的小/中/大型项目轻入口是否必须进主线。

## 2. 我的初步 verdict(草案)

我主张 **redesign by new repo, not incremental V4**:新建 XenoDev,archive V4,IDS 改为 L1-L3 + governance + 双向 contract。XenoDev v0.1 必须先落 Safety Floor 三件套、单一 build spec source、workspace/working_repo schema、hand-back 包和 Eval/risk 数据接口;不必在 v0.1 完成复杂 risk tier 算法或完整 Eval Score。R2 需要把"轻入口、重升级"显式继承,否则 K3 没被回答。

## 3. 关键分歧清单

- **分歧 1 · Spec Kit v2 事实表述**
  - 我的立场:可对齐 Spec Kit 的 spec-first 范式,但不要把"v2 已发布"写成事实;我 P2 未验证到官方 v2。
  - 对方立场(quote):"直接采用 Spec Kit v2 schema"
  - R2 收敛:写成"对齐/可评估 fork Spec Kit 现行 schema",并保留 XenoDev 自己 PPV/Safety Floor 扩展。

- **分歧 2 · sdd-workflow / task-decomposer C 级处置**
  - 我的立场:接受 Opus 让步。L/P 保留,C 由 XenoDev schema 决定;不要因 port-from-IDS 自动 cp。
  - 对方立场(quote):"skills 物理 source-of-truth 应在 XenoDev"
  - R2 收敛:主线写"迁 source-of-truth 到 XenoDev;IDS 同名 skill deprecated"。

- **分歧 3 · `working_repo` emergent 字段**
  - 我的立场:接受 Opus 让步;这不是噪音,是 workspace schema 信号。
  - 对方立场(quote):"主进程汇总"
  - R2 收敛:SHARED-CONTRACT v2.0 必须含 workspace root / build repo / source PRD repo / hand-back target 四字段。

- **分歧 4 · Eval Score / risk tier v0.1 形态**
  - 我的立场:同意折中:留数据接口和 event schema,不实装完整算法;Safety Floor 三件套不可后置。
  - 对方立场(由 task hint):留接口 / 不实装算法。
  - R2 收敛:W5 只要求 v0.1 记录 review failures、operator interventions、hand-back drift;算法进 v0.2 note。

- **分歧 5 · K3 小型项目轻入口**
  - 我的立场:不同意降级为 v0.2 note。K3 是 operator 核心困境,且 AGENTS §3 已有 Small/Medium/Large tier。
  - 对方立场(由 task hint):Opus 标 1 处 K3 ⚠。
  - R2 收敛:W1/W2 必须显式保留"轻入口、重升级";W4/W5 可聚焦 XenoDev,但不能让小项目入口消失。

## 4. 与 K 的对齐性自检

- K1 可靠+最高自动化 → ✅ Safety Floor + deterministic feedback + hand-back,先可靠后自动化。
- K2 operator 非软件背景 → ✅ XenoDev 接 PRD,但 ⚠ R2 要减少人工转写。
- K3 对各规模开发没把握 → ⚠ 必须显式继承 Small/Medium/Large 轻入口规则。
- K4 四个历史尝试 → ✅ V4/idea_gamma2/vibe-workflow/IDS 都按 L/P/C 吸收,不 cp 整体。
- K5 ADP 项目 → ✅ 按 K7 改读为 ADP-next 设计意图,非 V4 实装。
- K6 framework/pipeline 共识 → ✅ IDS+XenoDev+contract+forge 元治理形成共识主线。
- K7 V4 是物证 → ✅ archive V4,新建 XenoDev。
- Binding1 ADP-next 重定义 → ✅。
- Binding2 §9 drift 优先 → ✅。
- Binding3 v2.0 双向 hand-off → ✅。
- Binding4 forge 元层锁 → ✅。
- Binding5 不重走 L1-L3 → ✅。
- convergence_intent strong-converge + v0.2 note → ✅ 主线单 verdict,Eval算法/Spec Kit fork细节进旁注。
