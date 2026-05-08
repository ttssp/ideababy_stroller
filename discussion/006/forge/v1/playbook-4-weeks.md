---
doc_type: operator-playbook
generated: 2026-05-08
horizon: 2026-05-08 → 2026-06-03 (4 weeks)
goal: 完成 V4 dogfood checkpoint-01 + 浮现 1 个真自用候选(满足 ADR 0009 D5 12 周硬条件)+ 实测 SHARED-CONTRACT v1.1.0 跨仓 hand-off
status: ready-to-execute
---

# 4 周 Playbook · forge 006 路径 2 启动前的 V4 dogfood + 跨仓压测

> **怎么用这份 playbook**:每个 ▶ Step 是一段**可粘贴进 Claude Code 的指令**;每个 ✅ 是验收命令(终端粘贴)。按时间表顺序走,中途遇到阻塞回到本文档对应 step。

---

## 时间表(锚定)

```
W0 · 2026-05-08(今天)        → Step 0 准备 + Step 1 选 idea 候选
W0 · 2026-05-08 → 2026-05-15  → Step 2 IDS L1→L4 跑通(挑一个 small idea)
W1 · 2026-05-15 → 2026-05-22  → Step 3 切 ADP 做跨仓 hand-off + 起新 feature
W2 · 2026-05-22 → 2026-05-29  → Step 4 ADP build + observe(retrospective 自然触发)
W3 · 2026-05-29 → 2026-06-03  → Step 5 写 V4 checkpoint-01(必做)+ 决策 gap A/B/C
W4 · 2026-06-03 后             → Step 6 路径 2 真启动(切 ADP 补 gap-1)
```

**最低标准**:只跑 Step 0 + Step 5(checkpoint-01)
**建议路径**:全跑(产 D5 候选 + 实测 SHARED-CONTRACT + 给 V4 dogfood 真数据)

---

## 🟢 Step 0 · 准备(IDS,~10 min)

**何时**:今天(2026-05-08)
**在哪**:IDS Claude Code session(`/Users/admin/codes/ideababy_stroller`)
**目的**:确认前序 commit 落地 + 看池子里有哪些 idea 可挑

### ▶ 粘贴进 Claude

```
检查 forge 006 路径 2 启动前的状态:

1. 读 framework/ADP-AUDIT-2026-05-08.md §8(grep 校验结果),确认 14 项全通过
2. 读 framework/SHARED-CONTRACT.md frontmatter,确认 contract_version: 1.1.0
3. 跑 /status 看全局 idea 池子,告诉我哪些 ideas 处于以下状态之一:
   - L3 已完成有 candidate PRD 待 fork
   - L4 已 fork 有 PRD 但还没跑 /plan-start
   - L4 已跑过 /plan-start 但没 build
4. 给我一份 5 行内的 W0 起点报告:今天可以挑哪个 idea 做 first end-to-end pilot
```

### ✅ 验收

```bash
cd /Users/admin/codes/ideababy_stroller
git log --oneline -1  # 应是 0808984 路径 2 启动前 4 件事
grep "^contract_version:" framework/SHARED-CONTRACT.md  # 应 1.1.0
ls discussion/  # 看有哪些 idea
```

---

## 🟢 Step 1 · 选 idea(IDS,~30 min · operator + Claude 对话)

**何时**:Step 0 之后,W0 内
**在哪**:IDS Claude Code session
**目的**:挑一个**小到能 1 周走完 L1→L4** 的 idea 作为 first pilot

### 选择标准(必须全满足)

- ✅ scope 小(目标:能在 1 周内走完 L1→L4 出 PRD + spec + tasks)
- ✅ 有真实自用价值(不是为了 dogfood 而 dogfood)
- ✅ 不涉及生产凭据 / 不可逆操作(避免触发还没补的 gap-1 风险)
- ✅ 涉及代码产出(不能只是文档项目,否则 ADP 跨仓没意义)

### ▶ 粘贴进 Claude

```
我要在 4 周内完成 forge 006 路径 2 启动前的 V4 dogfood pilot。需要挑一个
small idea,从 IDS L1 走到 L4(产 PRD + spec + tasks + HANDOFF.md),再切到
ADP 跑 build。

候选必须满足:
1. scope 小(能 1 周内 L1→L4 出全套产物)
2. 有真实自用价值
3. 不涉及生产凭据 / 不可逆操作
4. 涉及代码产出(不只是文档)

请:
1. 看 proposals/proposals.md 里所有 proposal,以及 discussion/ 里所有未完成的 idea
2. 按上面 4 条筛掉不符合的
3. 给我前 3 个最适合的候选,每个 1 段(50 字内)说明,以及它当前在 L 几
4. 推荐 1 个 + 理由
5. 不要直接动手,等我确认后再启动 L1 / L2 / L3 / L4 的某个 phase
```

### Decision point(operator)

读完 Claude 给的 3 候选 + 推荐,选 1 个。如果都不合适(比如都太大),可以:
- (a) **降级 minimum 路径**:跳过 Step 1-4,直接做 Step 5 写 checkpoint-01
- (b) **新写一个 micro-proposal**:30 字以内,做个最小自用工具(比如"扫 ~/.claude/lessons/ 输出一份 markdown 索引")

---

## 🟢 Step 2 · IDS L1→L4 跑通(IDS,~5-7 天)

**何时**:Step 1 选定后,W0-W1
**在哪**:IDS Claude Code session
**目的**:产出 specs/<id>/HANDOFF.md(本次 commit 新加的 Step 5.5 自动产出)

### 2.1 起 inspire(L1)

```
/inspire-start <idea-id>
```

跑完后 operator 看 L1 stage doc,如果觉得够用直接 advance:

```
/inspire-advance <idea-id>
```

### 2.2 选一个方向 fork 进 L2

```
/fork <idea-id> from-L1 <chosen-direction> as <fork-id>
/explore-start <fork-id>
```

### 2.3 跑完 L2 → L3 → L4

```
/explore-advance <fork-id>
/scope-start <fork-id>
/scope-advance <fork-id>

# 选一个 candidate fork 进 PRD
/fork <fork-id> from-L3 candidate-<X> as <prd-fork-id>

# 跑 L4 plan(本次 commit 新加 Step 5.5,会产 HANDOFF.md)
/plan-start <prd-fork-id>
```

### ✅ 验收(每跑完一个 phase 就跑)

```bash
cd /Users/admin/codes/ideababy_stroller
ls discussion/<idea-id>/  # 看 L1/L2/L3/<fork>/<prd-fork>/PRD.md 是否齐
ls specs/<prd-fork-id>/   # 看 spec.md / tasks/ / HANDOFF.md 是否产出
cat specs/<prd-fork-id>/HANDOFF.md | head -30  # 确认 HANDOFF.md schema 对
```

### ▶ 如果 HANDOFF.md 没产出(/plan-start 没自动写)

```
/plan-start 应该在 Step 5.5 写 HANDOFF.md 但没产出。
请按 framework/SHARED-CONTRACT.md §3 的 HANDOFF.md schema 模板,
手工生成 specs/<prd-fork-id>/HANDOFF.md。timestamp 用 date -u 命令实时算。
```

---

## 🟢 Step 3 · 跨仓 hand-off(切 ADP,~30 min)

**何时**:Step 2 完成,W1 内
**在哪**:**新开一个 ADP Claude Code session**(`/Users/admin/codes/autodev_pipe`)
**目的**:实测 SHARED-CONTRACT v1.1.0 hand-off 协议;让 V4 dogfood 多一个真自用客户

### 3.1 切仓 + 读 hand-off

```bash
# 在 ADP 仓库根目录起 Claude Code
cd /Users/admin/codes/autodev_pipe
claude  # 或你常用的启动方式
```

### ▶ 粘贴进 ADP Claude

```
我刚在 ideababy_stroller 仓库跑完一个 idea 的 L1→L4,产出了 HANDOFF.md。
现在要把这个 idea 作为 ADP V4 dogfood 的"真自用业务项目候选"接入 ADP。

请:
1. 读 /Users/admin/codes/ideababy_stroller/specs/<prd-fork-id>/HANDOFF.md
2. 严格按 HANDOFF.md "Operator manual steps" 的 step 1-8 走,不要跳步
3. step 4 把 IDS PRD 转写为 ADP spec.md 7 元素时,告诉我每节填了什么、
   哪节缺源数据需要我补
4. step 4.5 写 §7 Production Path Verification 时,先读
   specs/v3.3/spec.md §7 + templates/spec.template.md §7 作为样本,然后
   给我列你打算怎么写 §7,等我确认再下笔
5. 所有 Open questions 中"关于 build 路径选择的"留给我,不进 ADP spec

这是 ADR 0009 D5 12 周硬条件下的第一个真自用候选,所以严格度跟实跑业务
项目一致 — 不要为了快牺牲质量。
```

### ✅ 验收

```bash
# 在 ADP 跑
cat specs/<feature>/spec.md | head -50  # 7 元素 frontmatter + §1 Outcomes 要齐
grep -E "^## [1-7]\." specs/<feature>/spec.md  # 应 7 行
grep "schema_version: 0.2" specs/<feature>/spec.md  # 1
grep "reviewed-by" specs/<feature>/spec.md  # 应有
```

### 3.2 跑 reviewed-by

按 HANDOFF.md step 5 的引导跑 ADP `/codex:adversarial-review`(或 plugin 路径)。
review 通过后 status: draft → review → frozen。

---

## 🟢 Step 4 · ADP build + observe(切 ADP,~5-7 天)

**何时**:Step 3 之后,W1-W2
**在哪**:ADP Claude Code session
**目的**:跑 task-decomposer + parallel-builder;**留意 V4 retrospective skill 何时自然触发**

### 4.1 跑 task-decomposer

按 HANDOFF.md step 6 在 ADP 触发:

```
触发 .claude/skills/task-decomposer/SKILL.md,从 specs/<feature>/spec.md
产出 tasks/T*.md 和 dependency-graph.mmd
```

### 4.2 跑 parallel-builder(按 ADP 自己规则)

每完成一个 task 或 phase,**主动触发 V4 L1/L2 retrospective**:

```
我刚跑完 task T<NNN>(BLOCKED / DONE 报告见 ...),触发
.claude/skills/retrospective/ skill 走 L1 任务级 retrospective:
- 读 task 文件
- 读 git log 范围
- 在 task 文件追加 ## L1 Retrospective 段(三段:本任务真有用 / 假阳性 / 漏抓)
```

phase 完成时:

```
phase <X> 已完成,触发 .claude/skills/retrospective/ 的 L2 phase 级:
- 读 phase 范围内所有 task 的 L1 retrospective
- 读 git log <phase-start>..HEAD 范围
- 产出 docs/dogfood/<phase>-retrospective.md
- 把 reusable lesson append 到 ~/.claude/lessons/<category>-<slug>.md
```

### ▶ 重要:**记录 V4 工具链摩擦点**

每次 V4 retrospective skill 跑得**不顺畅**(失败 / 出 placeholder / lesson 没 append 成功),立刻 jot 一笔到:

```bash
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) - <现象描述>" >> docs/dogfood/v4-friction-log.md
```

这些 friction 是 Step 5 写 checkpoint-01 的核心素材。

### ✅ 验收(每天结束跑一次)

```bash
cd /Users/admin/codes/autodev_pipe
ls docs/dogfood/  # 看 retrospective 文件累积
grep -l "L1 Retrospective" specs/<feature>/tasks/T*.md  # 看 L1 段覆盖率
ls ~/.claude/lessons/  # 看新 lesson 是否真 append 进去
```

---

## 🟢 Step 5 · V4 checkpoint-01 报告(切 ADP,~半天 · 必做)

**何时**:**2026-06-03 ± 这一天**(V4 frozen 后第 4 周)
**在哪**:ADP Claude Code session
**目的**:满足 ADR 0008 AC5(每 4 周 1 份 checkpoint,12 周 ≥3 份);沉淀 4 周 dogfood 真数据

### ▶ 粘贴进 ADP Claude

```
今天是 2026-06-03,V4 frozen 后第 4 周 checkpoint-01 时间点。

请用 .claude/skills/retrospective/ skill 走 L2 phase 级 retrospective,
phase 范围 = "V4 frozen → 现在 这 4 周":

输入:
- git log 2026-05-06..HEAD(限 specs/v4/ + .claude/skills/retrospective/ +
  scripts/append_lesson.py + scripts/init_user_lessons.py +
  templates/AGENTS.md + 我们这 4 周跑的 dogfood feature 范围)
- specs/v4/spec.md
- docs/dogfood/v4-friction-log.md(我手记的 friction)
- specs/<feature>/ 下所有 L1 retrospective(从 step 4 累积的真自用项目数据)
- 任何 ~/.claude/lessons/ 在这 4 周新增的 lesson

输出 docs/dogfood/v4-checkpoint-01.md,模仿
docs/dogfood/v3.3-w27-retrospective.md 的结构,但必须包含:

1. **AC4 进度**:V4 真自用业务项目候选浮现状态(0 / 1 / >1?哪个?)
2. **AC5 兑现**:本份是第 1/3 份 checkpoint
3. **D5 12 周硬条件预判**:还剩 8 周(到 2026-07-29);浮现 1 个真自用
   项目的概率高 / 中 / 低?为什么?
4. **3 段 retrospective**(本 phase 真有用 / 假阳性 / 漏抓)
5. **真自用项目带回的 friction**(step 4 friction-log 沉淀)
6. **路径 2 gap 取舍输入**(给 ideababy_stroller framework 用):
   - gap-1(production credential 隔离 + 备份破坏检测):4 周内有没有
     遇到真实威胁?
   - gap-2(risk tier 分类器):4 周内 reviewed-by hook 是否漏抓什么?
   - gap-3(Eval Score micro-benchmark):4 周内 G1-G10 + audit-consistency
     + reviewed-by 是否够用?
7. **V4 工具链是否到位**(retrospective skill 自身,append_lesson.py,
   init_user_lessons.py)— 真用过 4 周后,有没有应该改的?
8. **下一个 4 周(checkpoint-02)的 focus**

不要写到一半 placeholder;不要假数据;不知道就写"unknown"。
```

### ✅ 验收

```bash
cd /Users/admin/codes/autodev_pipe
test -f docs/dogfood/v4-checkpoint-01.md && echo "checkpoint-01 OK"
wc -l docs/dogfood/v4-checkpoint-01.md  # 应 100-300 行(模仿 w27 retrospective)
grep -c "^## " docs/dogfood/v4-checkpoint-01.md  # 应 ≥6 节
```

### 5.2 commit checkpoint-01

```bash
cd /Users/admin/codes/autodev_pipe
git add docs/dogfood/v4-checkpoint-01.md
git commit -m "docs(v4-dogfood): checkpoint-01 (4-week mark) — <one-line summary>"
# 不 push,等你确认
```

---

## 🟡 Step 6 · 决策 gap 取舍(IDS,~1h · checkpoint-01 之后)

**何时**:Step 5 完成后(2026-06-03 之后)
**在哪**:**回 IDS Claude Code session**
**目的**:基于真 4 周数据决定路径 2 实施什么

### ▶ 粘贴进 IDS Claude

```
V4 checkpoint-01 已出。请:

1. 读 /Users/admin/codes/autodev_pipe/docs/dogfood/v4-checkpoint-01.md
2. 读 /Users/admin/codes/autodev_pipe/docs/dogfood/v4-friction-log.md
3. 对照 framework/ADP-AUDIT-2026-05-08.md §4.3 的 3 个 gap 取舍方案 (A/B/C):
   - A · 全做(gap-1+gap-2+gap-3,~3-4 周)
   - B · 只做 P0(gap-1+gap-2,~1-2 周)
   - C · 只做 gap-1(production credential 隔离,~1-2 周)
4. 基于 checkpoint-01 数据,给我一份决策建议:
   - 哪些 gap 在 4 周里出现真实威胁(应该做)
   - 哪些 gap 4 周里没遇到(可推迟)
   - 推荐 A/B/C 哪个 + 理由
5. 不要直接动手 — 等我看完决策建议再起 plan
```

### Decision point(operator)

- 选定 gap 方案后,起新 plan(plan mode)
- **不要把 4 周等待期的判断推翻**:除非 checkpoint-01 出现真实安全事件,否则保持 4 周等待时初步倾向(C · 只做 gap-1)
- 路径 2 实装 plan 走 SDD 流程:在 ADP 起新 spec(v4.x 或独立 spec)→ codex review → frozen → build

---

## 🟡 Step 7 · 路径 2 真启动(切 ADP,~1-4 周 · 视取舍)

**何时**:Step 6 决策后
**在哪**:ADP Claude Code session
**目的**:落地 framework v1.0 缺的最后 20%

视方案 A/B/C 走对应 PR 周期。**这一步在另一份 plan 里写**,本 playbook 范围到 Step 6 终止。

---

## 风险表 + 触发立即调整 playbook 的条件

| 风险 | 触发条件 | 应对 |
|---|---|---|
| Step 2 走不通 IDS L1→L4(idea 太大) | W0 末没产出 PRD | 降级到 minimum 路径(跳 Step 2-4,只做 Step 5)|
| Step 3 切 ADP 暴露 SHARED-CONTRACT 严重 drift | step 4 转写 ADP spec 时哪节没法填 | jot 到 ADP-AUDIT.md §8 末尾;不阻塞 dogfood,继续走 |
| Step 4 V4 retrospective skill 频繁 fail | 5 次以上 friction-log 同类条目 | 提前(W2 末)起 V4.1 修订,**不等 checkpoint-01** |
| Step 5 没真自用项目数据(D5 12 周条件预警) | checkpoint-01 显示 0 真自用候选 | checkpoint-01 单独标 AMBER;通知 operator 加快找候选 |
| 4 周内出生产凭据真实泄漏 / 备份破坏事件 | 任何安全事件 | 跳过 checkpoint-01,直接起 gap-1 紧急 PR |

---

## 极简版(只跑必做)

如果你 4 周内时间不够,**只跑 Step 0 + Step 5**(~半天总工作量):

- Step 0 今天确认状态
- Step 5 在 2026-06-03 那天回 ADP 跑 V4 self-dogfood retrospective + 写 checkpoint-01

**代价**:不会产生新真自用项目候选(D5 12 周硬条件还得另外满足);不会实测 SHARED-CONTRACT v1.1.0;但能保住 V4 AC5 进度。

---

## Changelog

- 2026-05-08 v1: 初稿。4 周 playbook,Step 0-7 + 风险表 + 极简版
