# Forge v2 · 006 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-05-09T13:12:54Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1 · Spec Kit v2 事实表述**
  - 对方在 P3R1 的论证:"Spec Kit 0.8.7" → 让步。
  - 我的最终立场:stage 文档不得写"Spec Kit v2 已发布";应写"对齐 Spec Kit 现行 spec-first 范式,评估 fork/adapter,保留 XenoDev 的 PPV 与 Safety Floor 扩展"。
  - 让步给对方的部分:采用 0.8.7/现行版措辞;不把 schema 选择硬锁死。

- **分歧 2 · sdd-workflow / task-decomposer C 级处置**
  - 对方论证:"由该 schema 重新派生" → 让步。
  - 我的最终立场:L/P 保留,C 不从 IDS 或 V4 自动 cp。XenoDev 选定 spec/task schema 后重新生成 L4 skills;IDS 同名 L4 skills 标 deprecated 或迁出。
  - 让步给对方的部分:不坚持直接继承任何 port 版。

- **分歧 3 · `working_repo` emergent 字段**
  - 对方论证:"显式定义跨仓 workspace 模型" → 让步。
  - 我的最终立场:SHARED-CONTRACT v2.0 与 XenoDev schema 必须一等建模 workspace,至少含 `source_repo`、`build_repo`、`working_repo`、`handback_target` 四字段。
  - 让步给对方的部分:不试图通过单仓物理位置消除该字段。

- **分歧 4 · Eval Score / risk tier v0.1 形态**
  - 对方论证:留数据接口、不做算法 → 部分接受。
  - 我的最终立场:v0.1 必落 append-only event schema,记录 review failures、operator interventions、hand-back drift 三类事件;完整 scoring、risk tier verdict、阈值算法进 v0.2。
  - 让步给对方的部分:不在 v0.1 强推算法;但数据接口不可省。

- **分歧 5 · K3 小型项目轻入口**
  - 对方在 P3R1 标 K3 为唯一 ⚠ → 我坚持并收敛进主线。
  - 我的最终立场:v2 verdict 必须继承 v1 "轻入口、重升级":Small 走 PRD→XenoDev minimal lane;Medium/Large 才触发完整 L4 harness、cross-model review、hand-back metrics。
  - 让步给对方的部分:W4/W5 仍聚焦 XenoDev,轻入口只作为 tier policy 明确写入,不展开成另一个 PRD。

## 2. 联合 verdict(单一)

我和对方在 R2 后达成的单一 verdict: **forge 006 v2 应判定为 redesign by new repo, not incremental V4**。V4 打 `v4-final` archive,作为证据库和 lesson/pattern 来源,不作为 ADP-next 继承对象。IDS 退回 idea→PRD + governance/forge + SHARED-CONTRACT v2.0;XenoDev 新建为唯一 PRD→spec→build→ship 运行时 harness。B1 必须先完成 IDS 优化:SHARED-CONTRACT v2.0 双向 hand-off/hand-back、CLAUDE.md L4 重定义、plan-start 改产 hand-off 包、IDS specs/ 处置。B2 再启动 XenoDev:L4 spec/task/build/ship 全在 XenoDev,workspace 四字段一等建模,v0.1 落 Safety Floor 三件套、单一 build spec source、hand-back 三标签、Eval/risk 数据接口。主线同时保留 "轻入口、重升级":小项目不强制全套重流程,中大型再升级。

## 3. 残余分歧降级为 v0.2 note

- **v0.2 note 1 · Spec Kit fork 边界**:XenoDev v0.1 可先 adapter 到现行 Spec Kit schema;若 PPV/Safety Floor 无法自然表达,再 fork。回头看时机:第一个 XenoDev PRD build 完成后。
- **v0.2 note 2 · Eval scoring 算法**:v0.1 只记事件;v0.2 再定义 N、干预率 X、滑动窗口、risk tier。回头看时机:累计 3 个真 idea 或 30 个 task 后。
- **v0.2 note 3 · risk tier 与 PPV 的关系**:risk tier 是否由 file_domain/spec section/PPV path 联合决定,暂不锁。回头看时机:出现第一次 High-risk hand-back。
- **v0.2 note 4 · retrospective/lessons 机制**:保留 V4 L/P,但不 cp V4 skill。回头看时机:XenoDev 完成第一轮 ship retrospective。

## 4. W 形态产出的初步草稿建议

- **W1 verdict-only**:关键句: "新建 XenoDev,archive V4;IDS 只负责 idea→PRD 与元治理,XenoDev 负责唯一 L4 build runtime,并保留轻入口、重升级。"

- **W2 decision-list**:保留:Safety Floor 三层可靠性、forge 元层锁、AGENTS/Skills 标准、ADP 的 L/P lesson、block-dangerous pattern。调整:SHARED-CONTRACT v2.0 双向、plan-start 只产 hand-off、workspace 四字段、skills source-of-truth 迁 XenoDev。删除:autodev_pipe-cli/Makefile 假设、IDS 内部 build spec/task 双写、V4 12 周 dogfood 作为前置、V4 增量补 gap 路径。新增:XenoDev repo、hand-back 包三标签(drift/PRD gap/practice stats)、Eval/risk event log、Small/Medium/Large tier policy。

- **W3 refactor-plan**:模块 1 IDS contract:改 SHARED-CONTRACT v2.0、CLAUDE.md L24、plan-start、AGENTS §4/§5 旧命令。模块 2 archive/cleanup:V4 tag `v4-final`,IDS `specs/007a-pA` 标物证或 deprecated。模块 3 XenoDev bootstrap:新仓 AGENTS、Safety Floor hook、spec/task skill、workspace schema、hand-back receiver。

- **W4 next-PRD**:PRD 名称: XenoDev v0.1。用户:能写 PRD 但非软件背景的 operator。Outcomes:从 IDS PRD 生成单一 build spec;完成一个真实 small/medium task build;所有 high-risk 操作被 Safety Floor 阻断;每次 build 产 hand-back;记录干预/失败事件。Non-goals:v0.1 不做 SaaS、不做完整 Eval scoring、不继承 V4 repo。

- **W5 next-dev-plan**:Milestone A(B1):1-2 天改 IDS contract 与文档,停止新 IDS build spec。Milestone B(B2.1):初始化 XenoDev,导入 Safety Floor + spec/task skeleton + workspace schema。Milestone C(B2.2):用 forge v2 PRD 手补 Real constraints 后跑首个 XenoDev L4,ship 后 hand-back 回 IDS。

- **W6 free-essay**:三论点:第一,V4 失败不是代码失败,是元层转向无锁导致的沉没;第二,SOTA 的共同方向是运行时 harness,不是更多 prompt;第三,可靠自动化要靠双向学习闭环,所以 hand-back 是 ADP-next 的核心产品特性。
