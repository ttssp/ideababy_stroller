# Adversarial Review · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**读者**: 架构师 + operator
**规则**: Spec 变动时再跑一轮 Codex 对抗性审查;4 轮封顶

> 本文档回答:"Spec 改了,要不要再过一次 Codex adversarial review?" + "怎么触发 + 在哪看结果 + BLOCK 了怎么办"。流程已在 R1 / R2 两轮落地(见 `.codex-outbox/20260423T142034-001-pA-L4-adversarial-r1.md` 等),本文档是权威总结。

---

## §1 何时触发

**必须触发**(operator 不可豁免):
- 修改 `specs/001-pA/spec.md` 的**任一**非"变更日志"章节
- 修改 `architecture.md` 的 ADR 列表或 data model
- `reference/` 新增文档 OR 修改已有契约(api-contracts / schema.sql / llm-adapter-skeleton / error-codes)

**建议触发**(架构师判断):
- 某个 PR 影响 ≥ 3 个下游 task 的 file_domain / Outputs
- 某个 constraint(C1–C13)被突破
- 某个 risk(TECH/SEC/OPS)的 likelihood 或 impact 有实质变化

**不必触发**:
- 纯 typo 修复 / 格式调整(patch bump)
- 只改 `workflows/*.md` / `skeletons/*` 内代码注释措辞
- 只改 `DECISIONS-LOG.md`(本身就是记录决策的过程文档)

---

## §2 4 轮封顶规则

spec 的一个版本号内(如 v0.2.x 内)最多跑 4 轮 adversarial review:

- **R1**:首版审查(通常覆盖最大,BLOCK 最多)
- **R2**:R1 修复后验收;此时聚焦回归与新引入的 regression
- **R3**:若 R2 仍 BLOCK,operator 判断是否继续
- **R4**:最后一轮;仍有 BLOCK → **operator 决策**(不是自动进入 R5)

**为什么 4 轮封顶**:adversarial review 的边际发现率在 R3 之后急剧衰减;继续跑 ≈ 不信任 spec-writer + 自己也没备选方案。到 R4 仍 BLOCK 一般意味着 spec 设计本身有根本问题,需要回 L3(退化出 kill-window)。

**历史**:到 2026-04-23 spec v0.2.2,001-pA 只用了 R1 + R2(R1 BLOCK + R2 CONCERNS);R3 / R4 未动用。

---

## §3 触发流程(操作细节)

### Step 1 · 写 inbox 文件
路径:`.codex-inbox/<TS>-001-pA-L4-adversarial-r<N>.md`
`<TS>` = `YYYYMMDDTHHMMSS`(机器排序友好),例 `20260423T142034`。

**模板**(复制 R1 文件结构):

```markdown
---
round: <N>
fork: 001-pA
layer: L4
mode: adversarial-review
target: specs/001-pA
version_under_review: <spec.md 的 Version 字段,如 0.2.2>
issued_at: <ISO>
---

# Adversarial Review R<N> · 001-pA

## 任务
Codex 请对下述 spec 包做**对抗性审查**:
- `specs/001-pA/spec.md` (v<X>)
- `specs/001-pA/architecture.md`
- `specs/001-pA/tech-stack.md`
- `specs/001-pA/reference/*.md`
- `specs/001-pA/tasks/T*.md`

## 本轮关注点(operator 指定)
- <focus area 1>
- <focus area 2>
- <focus area 3>

## 输出要求
1. **BLOCK / CONCERNS / CLEAN** 每条 finding 带严重度
2. 每条 finding 对齐具体行号 / 文件
3. 给出**可执行 patch 建议**(不是"建议重构",而是"把 §4 D15 第 3 句改成 X")
4. R<N-1> 留的 deferred 项是否仍相关?

## 变更自上一轮(如 R≥2)
<简述 R<N-1> 后 spec 有哪些改动>

## 输出目标
`.codex-outbox/<TS>-001-pA-L4-adversarial-r<N>.md`
```

### Step 2 · 更新 latest 指针
```bash
ln -sf <TS>-001-pA-L4-adversarial-r<N>.md .codex-inbox/latest.md
```

### Step 3 · 在 Codex terminal 跑
operator 在另一个 terminal 跑:
```bash
cdx-run
```
`cdx-run` 读 `latest.md` → 喂给 Codex → 写结果到 `.codex-outbox/<同 TS>-....md`。

### Step 4 · 查结果
```bash
less .codex-outbox/$(ls -t .codex-outbox/*L4-adversarial*.md | head -1)
```

---

## §4 结果处理

### 4.1 CLEAN
- 操作:无;spec 已可以进入 task-decomposer 下一步 / 继续实现
- 记录:`spec.md` 变更日志加一行 "R<N> · CLEAN · no blocking issues"

### 4.2 CONCERNS
- 定义:非 BLOCK,但指出风险或优化点
- 操作:
  - 每条 concern 判定:(a) 立即修 · (b) 登记到 `risks.md` 作已知权衡 · (c) 驳回(附理由到 `DECISIONS-LOG.md`)
  - 若 (a) 的条数 ≥ 3 → 修完后跑 R<N+1>
  - 若 (a) 的条数 < 3 且全是 patch 级 → 可跳 R<N+1>,直接在 spec 变更日志记 "R<N> · CONCERNS N 条,全修复"

### 4.3 BLOCK
- 定义:contract 层缺陷,继续实现会导致可预见的 bug
- 操作:
  - **停止** 下游 task-decomposer / parallel-builder 工作
  - spec-writer 按 Codex 的 patch 建议修 spec.md / reference/
  - `spec.md` minor bump(e.g. 0.2 → 0.3)
  - 跑 R<N+1> 验收
  - 若 R<N+1> 又 BLOCK → 评估是否 spec 设计有根本问题
- **BLOCK 不可绕过**;operator 也不能签字"同意保留 BLOCK"

---

## §5 作为 spec-writer 修 BLOCK 的 checklist

R<N> 返回 BLOCK 后,spec-writer 要做的事:

1. 逐条读 BLOCK finding,在 `DECISIONS-LOG.md` 开一节 `## <日期> · R<N> 反馈修复`
2. 每条 BLOCK 对应一个 patch 点;patch 要**surgical**(不趁机重写其他章节)
3. 改动涉及 `reference/*.md` 时同步更新 skeletons(如 `db-schema.ts` 里对应 CHECK)
4. bump `spec.md` Version(通常 minor)
5. 在 `spec.md` 变更日志里详细记录 R<N> 引发的改动
6. 如有下游 task file_domain 变化,update `tasks/T<NNN>.md`(task-decomposer 重跑)
7. 开 PR,描述里贴 `.codex-outbox/<TS>-...-r<N>.md` 的 URL,操作人 = spec-writer
8. PR merge → `cdx-run` R<N+1>

---

## §6 R<N> 结果在哪些地方留痕

| 痕迹位置 | 内容 |
|---|---|
| `.codex-inbox/<TS>-001-pA-L4-adversarial-r<N>.md` | 本次触发的输入(operator 写) |
| `.codex-outbox/<TS>-001-pA-L4-adversarial-r<N>.md` | Codex 的 finding 原文 |
| `spec.md` §变更日志 | 该版本的 R<N> 结果摘要("R1 BLOCK · 修 B1/B2/B3") |
| `DECISIONS-LOG.md` | R<N> 修复背后每条第一性论证 |
| `risks.md` | CONCERNS 中被转为已知权衡的条目 |
| PR 描述 | 附 outbox 文件 URL;reviewer 可快速验证 |

---

## §7 Operator 对抗性审查的角色

operator 在本流程里的责任:

- **不决定 contract**:操作流程,不要在 .codex-outbox/ 基础上二次解读 BLOCK 条款 —— spec-writer 读原文处理
- **批准跳轮**:如果架构师判断 "这次 spec 改动不够大,不必触发 R<N+1>",需要 operator 书面批准(PR comment);默认触发
- **裁决 R4 仍 BLOCK**:最后那一步只有 operator 能拍板

---

## §8 本项目已有的审查历史

| 轮次 | 日期 | 审查对象版本 | 结论 | 主要修复 |
|---|---|---|---|---|
| R1 | 2026-04-23 | spec v0.2 · reference/ v0.1 | BLOCK(3 条) + CONCERNS(10 条) | D15 新增 paper_summaries 表 + D16 红线 2 三层兜底 + T003 schema 前置 |
| R2 | 2026-04-23 | spec v0.2.1 · reference/ v0.1.1 | CONCERNS(4 条) | Q1–Q4 闭合 · grants.sql 补齐 · schema_version 前向兼容断言 |

(R3 / R4 尚未触发。)

---

## §9 未来若要改此流程

- 流程本身的修改也走 adversarial review(meta!);但需要 operator 书面批准绕过
- 若引入更多 agent(例如 Sonnet adversarial 与 Codex adversarial 并列),需要修订 §3 多路触发流程

---

## §10 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · 4 轮封顶规则 · inbox/outbox 契约 · 已有 R1/R2 历史 |
