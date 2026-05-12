---
doc_type: xenodev-skill-derivation-guide
generated: 2026-05-12
upstream: plan-rosy-naur v12 · plan v0.2-global 件 2.6
purpose: task-decomposer SKILL 派生指引(audit checkpoint codification · D-baseline-1 模式落地)
ids_reference_files:
  - framework/SHARED-CONTRACT.md
  - framework/xenodev-spec-writer-derivation-guide.md
  - discussion/004/v0.2-retro.md
  - discussion/004/handback/20260512T040013Z-004-pB-20260512T040013Z.md
---

# task-decomposer SKILL 派生指引(IDS framework feedback · 件 2.6)

## §1 背景(scope · 与 spec-writer derivation guide 关系)

本指引是 plan v0.2-global 件 2.6 落地 · F-new(task-decomposer audit gap) · 触发自 D-baseline-1 真案例。

- **与 `framework/xenodev-spec-writer-derivation-guide.md` 关系**:平级 · 各自覆盖一个 SKILL。spec-writer guide §5 含 task-decomposer 段(范式 / frontmatter)· 本指引补**审查维度**(audit checkpoint codification)。
- **scope IN**:task-decomposer 在拆 spec → tasks/T*.md 时必须跑的 4 条 audit · D-baseline-1 案例引用 · 失败模式 + spec-gap recovery 三选一矩阵。
- **scope OUT**:不替 XenoDev 写 SKILL 内容(XenoDev 自派生) · 不预决 model 选择阈值 · 不锁 DAG 入度上限。

## §2 task-decomposer audit checklist(核心)

task-decomposer 产 tasks/T*.md 前 / commit 前 · operator 跑下面 4 条 audit。每条标格式:**Q**(问题)/ **Pass**(通过判据)/ **Fail action**(失败操作)。

### A1 file_domain 现状 audit(D-baseline-1 primary)

- **Q**: task 的 `file_domain` 路径在 **build runtime**(XenoDev)是否已存在?src 是否在**源仓**(IDS)只读?跨仓 mass cp 前置是否必要?
- **Pass**: file_domain 真实存在于 build runtime · 可字面执行;或 prior baseline-cp task 已 schedule 在本 task 之前(DAG 父节点)。
- **Fail action**: 拆 task(前置加 baseline cp task) · 或 跨仓 mass cp(operator plan-mode 决) · 或 走 `/expert-forge` 起 spec amendment(重路径)。详见 §4 三选一矩阵。
- **触发场景**: phased build form / composite build form / 跨仓 src 持有不同。

### A2 task 依赖图入度 audit(DAG 5 铁律)

- **Q**: 本 task 的 `blockedBy` 是否真在 DAG 中存在?入度 = 0 task 是否 ≥ 1(防 dead-lock)?
- **Pass**: 全部 blockedBy 引用真存在 task id · DAG 至少有 1 个 task 入度 = 0(起点) · 无循环依赖。
- **Fail action**: 修 DAG 或拆 task。常见 bug:写 blockedBy 时手写 typo / 引用不存在 task / 互锁。

### A3 recommended_model audit(opus/sonnet 选择)

- **Q**: high-risk task(LOC ≥ 200 / 跨多 module / 业务逻辑密集 / 跨 schema 改 migration)是否 opus?low-risk task(纯 cp / 标准 refactor / lint fix)是否 sonnet?
- **Pass**: 复杂度 vs model 匹配 · 显式声明 `recommended_model` 字段。
- **Fail action**: 调 recommended_model · 或在 frontmatter 标 "operator override allowed"。
- **注**: 本指引不锁阈值 · operator 按 idea 量级与质量 budget 决。

### A4 phased build 拆 task 特殊审查(D-baseline-1 secondary)

- **Q**: PRD-form = `phased` 时 · phase N 的 task 是否依赖 phase N-1 baseline?baseline cp / migration 等 prior-phase 前置是否真 schedule?phase boundary 跨 task 是否声明?
- **Pass**: phase N task 全部在 phase N-1 baseline task 之后(DAG dep) · 跨 phase task 有 explicit `phase_boundary` flag。
- **Fail action**: 拆 task + 重排 DAG · 把 phase N-1 baseline cp 独立成 task(per D-baseline-1 路线 A)。

## §3 D-baseline-1 案例引用(verbatim · 案例 evidence · 不删)

verbatim 摘自 `discussion/004/handback/20260512T040013Z-004-pB-20260512T040013Z.md` 行 35-43(FU-hotfix-F1a hand-back §2):

> **触发**:第二阶段 vertical-slice ship 启动时发现 task-decomposer 漏拆 spec gap:
> - FU-hotfix-F1 spec'd file_domain = `projects/004-pB/src/decision_ledger/{main,plugin}.py`
> - 实际 XenoDev 路径仅有 T001 stub `__init__.py`,v0.1 全部 src(90 py / 11k LOC)在 IDS 只读仓
> - 不能 wire 不存在的 main.py;不能 silent expand FU-hotfix-F1 scope 到 16h+
>
> **Operator 决议(D-baseline-1,本次 session 新决策)**:
> - 路线选 A(11k LOC mass cp 进 XenoDev)而非 B(pip install -e IDS)或 C(spec amendment 走 forge 流程)
> - 理由:守 D-spec-3 build vs source 边界 + 后续 T010/T020/T024 都假设本地 src 存在 + 走 forge 流程 4h amendment 太重
> - 拆 FU-hotfix-F1 → F1a(本 task,4h sonnet)+ F1b(原 routes wire scope,6h opus)

RETRO §3.2 收获 3 条(`discussion/004/v0.2-retro.md` 行 143-146):

> - **phased build 时 task-decomposer 必须 audit "build runtime 当前 src 状态 vs file_domain 假设"** · 这是 task-decomposer skill gap · 应入 F-类 framework feedback queue
> - **拆 task 是 framework 真有效的 spec-gap recovery 路径** · 比 spec amendment 轻量 · 比 silent expand task scope 安全
> - **operator plan-mode 决策点**:不是所有 spec-gap 都该走 forge · 拆 task + 跨仓 mass cp 是真可行的中间路径

## §4 失败模式 + spec-gap recovery 路径(三选一矩阵)

A1 / A4 fail 时 · operator 在三条路径中选一:

| 路径 | 量级 | 触发判据 | 决议层 | 优劣 |
|---|---|---|---|---|
| **拆 task**(轻量) | 1-2 task 改 DAG | spec gap 在单 task scope 内 · 加 1 个前置 task 可救 | operator plan-mode | + 轻量 / + 不动 spec frozen · - 拆完 DAG 复杂度升 |
| **跨仓 mass cp**(中等) | 单 task ~4h sonnet | src 在源仓只读 / build 仓空 / 量级 ≤ 20k LOC · phased build 阶段 baseline 起跑 | operator plan-mode | + 一次过 · - 若再次 src drift 需再 cp |
| **forge amendment**(重) | ~4h 流程 · 加 PRD 修订或 spec 重审 | spec gap 在 PRD 级 / 跨多 task / D-spec 红线触动 | `/expert-forge <id>` | + 正本清源 · - 流程长 / 阻 ship 节奏 |

**D-baseline-1 决策点**:本案例 spec gap 在 file_domain 假设(11k LOC src 在源仓只读) · 量级中等 · 选 **跨仓 mass cp** + **拆 task**(F1a baseline cp 4h sonnet + F1b routes wire 6h opus) · 显式不走 forge(理由:4h 流程太重 · 不动 PRD outcome)。

## §5 与 plan-rosy-naur v12 关系

本指引是 plan-rosy-naur v12 B 件 1(2026-05-12 ship)产物 · plan v0.2-global 件 2.6 落地。后续 plan v0.3+(下一 idea batch)若发现新 skill gap(A5 / A6 / ...) · 可 amend 本 checklist · 不需 revert。

- **不动**:spec-writer derivation guide / SHARED-CONTRACT · 本指引是独立 SKILL 派生 guide
- **可 amend**:本 §2 audit checklist(加 A5-AN)/ §4 三选一矩阵(加新路径)
- **下游**:XenoDev session 内 operator 派生 task-decomposer SKILL 时 cp 本 §2 进 SKILL.md §"audit checkpoints" 段

## §6 Changelog

- **2026-05-12 v1.0**: 起新 file · §2 audit checklist A1-A4 落地 · D-baseline-1 verbatim evidence 锚(case + retro 两处) · §4 三选一矩阵成型 · 上游:plan-rosy-naur v12 B 件 1 / plan v0.2-global 件 2.6 / v0.2-retro.md §3.2 + §5 + §6.3
