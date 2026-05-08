---
doc_type: framework-cross-repo-reference
status: v2 (rewritten 2026-05-08 after sanity-check-v2 finding)
target_repo: autodev_pipe
generated: 2026-05-08
upstream: ideababy_stroller framework/SHARED-CONTRACT.md (v1, contract_version 1.0.0)
purpose: 描述 ideababy_stroller framework 文档如何参考 autodev_pipe 已落地实践;**不要求 ADP 做任何同步动作**
---

# autodev_pipe 关系参考(v2,2026-05-08)

## v2 重写说明(必读)

本文件 **2026-05-08 v2 sanity check 发现 v1 整体方向错误,全文重写**。

### v1 错误(已撤回)

v1 错误地把 IDS framework 文档当成 autodev_pipe 的"上游 binding contract",要求 ADP 做 3 节同步动作:
- 节 1:ADP README 加"消费 IDS PRD,honor IDS Safety Floor" 段
- 节 2:ADP AGENTS.md 加 "binding from ideababy_stroller framework/SHARED-CONTRACT.md §2"
- 节 3:ADP 持有 SHARED-CONTRACT.md byte-level mirror + 同步检查脚本

### v2 修正(本文件)

经核查 autodev_pipe 真实状态(2026-05-08):
- **autodev_pipe 早于本 framework 文档存在**(v3.1 设计稿 2025-Q4 / v3.2 frozen 2026-04-29 / v3.3 frozen 2026-04-29 / v4 frozen 代码层 2026-05-06 / 12 周 dogfood 进行中)
- **autodev_pipe 不消费 IDS PRD**(它 self-parasitic,用自己的 spec 跑)
- **autodev_pipe Safety Floor 已多层实装**(`block-dangerous.sh` + parallel-builder 5 hard rule + spec-validator + reviewed-by hook),不需要 IDS 给它 SSOT
- **要求 ADP "binding from IDS" 是 retroactive 倒置因果** — 一个早于 framework 文档存在 6 个月的成熟系统不需要新文档说"它必须遵守"

**本文件 v2 方向**:**framework 文档参考 ADP 实践**(单向引用),**ADP 不需要做任何同步动作**。

---

## §1 · ADP 真实状态参考(IDS framework 文档单向引用)

### autodev_pipe 版本演进时间线(2026-05-08 核查)

| 版本 | 状态 | 主旨 | 对 IDS framework 的参考价值 |
|---|---|---|---|
| v3.1 | 设计稿 | 11 阶段流水线 + 三层成本控制 | 提供失败案例(gap-audit 11 项 ×)的反面教材 |
| v3.1-gap-audit | 完成 | 11 × / 5 △ / 13 √ 真实落地盘点 | 揭示"设计稿 ≠ 已运行系统"的范式;影响 IDS NG-1 论证 |
| v3.2 | frozen 2026-04-29 | port stroller 五件套(sdd / decompose / quality-gate / parallel-builder / check-disjoint) | IDS framework SHARED-CONTRACT §3 hand-off 流程**实际终点**;IDS PRD → ADP `make sdd-init` 流程的 ADP 半边 |
| v3.3 | frozen 2026-04-29 / 真审 2026-05-06 | spec-validator + reviewed-by hook + Constraint Index + 7 元素 + Production Path Verification | IDS framework 文档应**参考**而非重新发明:Constraint Index / cross-LLM review / 第 7 元素 |
| v4 | frozen 代码层 2026-05-06 / 12 周 dogfood 进行中 | retrospective L1+L2 + lesson 反哺 + append_lesson + ~/.claude/lessons/ | IDS framework Learning Loop 立场已被 ADP v4 实装,不需要 IDS 重做 |
| ADR 0008 → 0009 | 2026-05-06 | dogfood 路径 B 真外部 → C Hybrid | 影响 IDS framework 对"跨仓 dogfood 节奏"的预期(不是 IDS 单方面驱动) |
| next_draft §3 | reference | 三方共同盲区:Production Path / Constraint Index / cross-LLM review / lesson 反哺 | IDS framework SHARED-CONTRACT 应在 §1 PRD schema 加 Production Path 字段 |

### 核心事实(IDS framework 文档必须采纳)

1. **ADP 实际入口 ≠ `autodev_pipe-cli build`** — 实际是 `make sdd-init` / `make decompose` / `parallel-builder` agent
2. **ADP spec ≠ IDS PRD** — ADP 用 7 元素 schema(Outcomes / Scope / Constraints / Prior Decisions / Tasks / Verification / Production Path Verification);IDS 用 8 字段 PRD schema;两者不是同一文件
3. **ADP self-parasitic** — v4 第一个 dogfood 客户是 ADP 自己的 v3.3 W2.7 retrospective,不是 IDS 的 PRD
4. **ADP 不读 IDS framework 文档** — IDS 这边的 NON-GOALS / SHARED-CONTRACT / AGENTS.md 是 IDS 内部 SSOT,ADP 不需要消费

---

## §2 · IDS framework 文档应参考 ADP 实践的具体点

按 sanity-check-v2 的 5 个真发现逐条:

### 参考 1 · spec 第 7 元素 Production Path Verification

- **ADP 实践**:`autodev_pipe/templates/spec.template.md` §7(2026-05-06 加)+ `autodev_pipe/specs/v3.3/spec.md` §7(自我寄生 dogfood)
- **失败案例**:`autodev_pipe/docs/case-studies/stroller-idea004-12-routes-404.md`
- **核心**:所有 mock-pass-prod-fail 都因为 mock 满足 spec,真路径不满足 → spec 必须强制描述真路径上 X 起点 Y 终点的可达性证据
- **IDS framework 已采纳**(v2 修订):SHARED-CONTRACT §3 HANDOFF.md schema 中"Schema 转换"表已包含"§7 Production Path Verification(operator 必须补)"行

### 参考 2 · Constraint Index 跨多 agent 引用范式

- **ADP 实践**:`autodev_pipe/docs/constraints/<id>.md` + `autodev_pipe/scripts/check_constraint_references.py`(v3.3 W2.5)
- **失败案例**:`autodev_pipe/docs/case-studies/gamma2-w18-cp-drift.md`(idea_gamma2 同字段约束在 4 文件 cp 漂移)
- **核心**:跨多 agent 引用的业务约束抽到单一 `docs/constraints/` 目录,agent 文件**只引用不 cp**
- **IDS framework follow-up**(v2 sanity check 暴露的 gap):IDS 这边的 forge stage v1 §2 Decision matrix 28 项里**有跨多 agent 引用的约束**(eg "Safety Floor 不可被覆写"出现多处);可参考 ADP 实践把它们抽到 `framework/constraints/` 目录。**v2 不强制现在做**,留作 follow-up

### 参考 3 · cross-LLM review 实装机制

- **ADP 实践**:v3.3 reviewed-by hook(`scripts/check_spec_review.py`)+ pre-commit reject + `/codex:adversarial-review` plugin 路径
- **核心**:spec frontmatter 必须含 `reviewed-by: <peer-llm>` 字段;status: review/frozen 时不允许 pending
- **IDS framework 同构**:forge protocol 横切层(`/expert-forge`)是同一范式的另一尺度 — Opus + GPT-5.5 双专家审 = ADP 的 reviewed-by hook 在 idea 阶段的等价物
- **建议**:IDS framework 文档明确"forge 横切层 = idea 阶段的 cross-LLM review 实装",指向 ADP v3.3 hook 作为 build 阶段的对应实装

### 参考 4 · ADP v4 已实装 retrospective + lesson 反哺

- **ADP 实践**:`.claude/skills/retrospective/SKILL.md`(L1+L2 触发)+ `scripts/append_lesson.py`(状态机 APPENDED/SKIPPED/MATERIALIZED/REPAIRED/MISSING)+ `~/.claude/lessons/<category>-<slug>.md`(user scope 跨项目复用)
- **自寄生证据**:`docs/dogfood/v3.3-w27-retrospective.md`(v4 用自己的 retrospective skill 处理 v3.3 W2.7 phase)
- **核心**:retrospective 多触发器(phase / 上下文阈值 / 失败事件 / 周期);lesson 跨项目复用通过 user scope `~/.claude/lessons/`(不进项目 git)
- **对 IDS framework 的影响**:**stage-forge-006-v1.md §3 模块 4 "Learning Loop 层" 描述 90% 已被 ADP v4 实装**;IDS 这边不需要重做 Learning Loop 模块。IDS 自己范畴 = 在 idea→PRD 阶段使用 lesson(eg `/scope-start` 时读 `~/.claude/lessons/anti-pattern-*.md`),而不是实现 lesson 反哺机制本身

### 参考 5 · ADR 0008 → 0009 路径修正(B → C Hybrid)

- **ADP 决策**:V4 dogfood 从"≥ 2 真自用业务项目"降级为"1 真自用 + 1 ADP 自身 retrospective 周期";真跨项目反哺主张推 V4.2
- **影响**:IDS 不能假设"ADP 在等 IDS 的 PRD 作为 dogfood 输入" — ADP 已自己跑自己的 dogfood
- **IDS framework 立场修正**:跨仓 hand-off 是**未来某天**真实跑 IDS L1→L4 + 切仓走 ADP 流程的事;不是 ADP 现在就在等 IDS 输入。本文件 v2 修订采纳此事实

---

## §3 · 真 gap(IDS 和 ADP 各自的真实工作)

sanity-check-v2 §3 模块 1-4 对照表已揭示 3 个真 gap。本节明确各 gap 应在哪一仓做:

### Gap 1 · Production credential 物理隔离 + 备份破坏检测

- **应在 ADP 做**(运行时阻断必须有运行时,只有 ADP 有)
- **不在 IDS 做**(IDS 阶段没运行时,只能"声明 PRD 不允许提出违反 Safety Floor 的需求")
- **优先级**:P0(Cursor 9 秒删库案例直接对应)
- **估时**:1-2 周(ADP 那边)

### Gap 2 · Risk tier 分类器(file_domain / spec section / 危险命令 → tier 1/2/3)

- **应在 ADP 做**(routing 在 build 阶段)
- **不在 IDS 做**
- **优先级**:P0(stage v1 §3 模块 3 剩余 25%)
- **估时**:4-5 天(ADP 那边)

### Gap 3 · Eval Score micro-benchmark(SWE-bench Pro 任务集 + recall/precision)

- **应在 ADP 做**(eval 跑代码,只有 ADP 有运行时)
- **不在 IDS 做**(IDS 阶段无代码可 eval)
- **优先级**:P1(framework v1.0 release 前必做,v0.1 可推)
- **估时**:1 周(ADP 那边)

### IDS 自己的 follow-up(独立于上述 3 gap)

- IDS framework `framework/constraints/` 目录(参考 ADP v3.3 Constraint Index)— P2,留作 follow-up
- IDS `/plan-start` 加 HANDOFF.md 产出步骤(SHARED-CONTRACT §3 v2 修订后改为 operator-readable 格式)— P1,真实跑过 1 个 idea 后再做
- IDS `/scope-start` 读 `~/.claude/lessons/anti-pattern-*.md`(消费 ADP v4 已 ship 的 lesson)— P2

---

## §4 · 推荐 operator 行动路径(v2)

### 短期(1 周内)

- **不切到 ADP 仓库做任何同步动作** — ADP 不需要,framework 文档单向引用即可
- **接受 sanity-check-v2 修订后的 5 件事产物** — SHARED-CONTRACT 已修 §1/§2/§3,本文件 v2 重写,stage v1 §2 加 v2 增补
- **最早机会跑一个真实 idea 的完整 L1→L4** — 暴露 SHARED-CONTRACT §3 HANDOFF.md schema 的真实 gap

### 中期(1-3 月内)

- 在跑过的真实 idea 暴露的 gap 基础上,改造 `/plan-start` 加 HANDOFF.md 产出步骤(估时 ~2h)
- 视 ADP v4 dogfood 12 周进度,决定是否启动 IDS framework 的 follow-up(constraints / lesson 消费)

### 长期(3-12 月)

- ADP v4 dogfood 完成 + ship checkpoint 03 后,起 forge v2 重审 framework v0.2(把 v3.2/v3.3/v4 + ADR + dogfood 实测 + 新 SOTA 全部纳入 X)
- 视 forge v2 verdict,决定 framework v1.0 是否需要新增模块

---

## §5 · 客观依据

- **Linux kernel + glibc 30 年 ABI 协调范式** — 两者独立 release,只共享 syscall ABI 契约;**不要求一方"binding from"另一方**;本文件 v2 方向参考此范式
- **Pact framework / Newman *Building Microservices* ch.7 Consumer-Driven Contracts** — Consumer-Driven 不是"Producer 强加 contract 给 Consumer";是"Consumer 主动声明它需要 Producer 满足什么"。ADP 没声明它需要 IDS 提供 SHARED-CONTRACT,**所以 IDS 不应单方面写 binding 给它**
- **autodev_pipe v3.2 PD1**(spec/task 工具链 = stroller schema)— ADP 用 stroller schema 是 ADP 自己的决策,不是 IDS 强加
- **autodev_pipe AGENTS.md L48**(危险命令唯一防线 = block-dangerous.sh)— ADP 已有 Safety Floor SSOT;不需要 IDS 提供
- **autodev_pipe ADR 0009 D5**(真自用候选 12 周内浮现硬条件)— ADP self-parasitic + 真自用候选 TBD,**不在等 IDS 的 PRD 作为 dogfood 候选**

---

## §6 · v1 → v2 修订对照

| 维度 | v1 立场 | v2 修订 | 修订理由 |
|---|---|---|---|
| 文档性质 | 同步提案(action plan) | 关系参考(reference doc) | ADP 不需要做同步动作,文档只是单向引用 |
| 方向 | IDS → ADP(IDS 给 ADP 加 binding) | ADP → IDS(IDS 参考 ADP 实践) | ADP 早于 framework 文档,retroactive binding 不合理 |
| operator 切仓动作 | 3 节强制同步(README + AGENTS + mirror) | 0 节强制 + 真实跑 idea 时按 SHARED-CONTRACT §3 HANDOFF.md schema 操作 | 不污染 ADP self-parasitic 状态 |
| 同步检查脚本 | byte-level mirror diff | 删除(无 mirror 了) | 没有 mirror 文件,无需检查 |
| autodev_pipe 命令假设 | `autodev_pipe-cli build` | `make sdd-init` / `make decompose`(v3.2 V1+V2) | 真实命令 |
| Safety Floor SSOT 归属 | IDS 拥有 | 双层独立(IDS = 上游约束声明 / ADP = 实装) | 实装必须有运行时 |

---

## Changelog

- 2026-05-08 v1: 初稿,3 节同步动作 + 同步检查脚本(后被 v2 重写撤回)
- 2026-05-08 v2: **全文重写**。撤回 v1 的"binding contract"方向;改为单向引用 ADP 实践。基于 sanity-check-v2-2026-05-08.md 发现
