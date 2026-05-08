# Fork origin

**This fork**: 007a-pA
**Forked from**: 007a-agent-emit · L3
**Source stage doc**: ../L3/stage-L3-scope-007a-agent-emit.md
**Selected candidate**: Candidate A · "证词契约日志" + 1 day-14 self-interview question (synthesizer-recommended hybrid)

**Candidate description (extracted from L3 stage doc, paraphrased)**:

PRD 主体 = stage-L3-scope §"Candidate A"(私有 IDS friction-log + agent 提名 + adjudication tags + week-2 trust mini-summary + CLI fallback + off-switch)。**关键修正**(operator 选定的 OQ-A 决议):**A + 1 个 day-14 自访谈问题** —— pure A 之外,trust mini-summary 多挂一行 prompt 让 operator 自答(GPT R2 §4 strong recommendation),与 industry 2 周 pilot baseline 对齐而几乎零工程成本。

具体 hybrid 增量:
- 第 14 天 trust mini-summary 在标准 4 项 metric (entry 数 / acked 比例 / disputed 比例 / hook 是否仍开)之上,**追加 1 行 prompt**:"After 2 weeks, do you feel **relieved / watched / both**? (1 句话)"
- operator 在 mini-summary 文件直接补一句 plain text 答案,无 form / 无脚本要求
- 工程量增 < 1h(改 trust report 模板加一行 prompt 文本)

**为什么选 hybrid 而非 pure A**:
- 两侧 R2 在 search 后独立确认 industry baseline = 2 周 pilot + decision date(BugBug + ClawStaff source 实证)
- pure A 缺这个 hedge → 4 周后回看时容易后悔"应该当时多加一个问题"
- hybrid 在工程上不影响 H confidence 与 1-1.5 周 timeline(增量 < 1h)
- 不动 A 的 substrate;不引入 B 的 self-interview 完整 6 题 协议负担(operator catch-all 已 explicit 说"friction-tap 不能拼动太多时间")

**为什么不选 pure A / B / C**:
- pure A:无 industry-aligned hedge → 同上
- full B:14-18h + 1-2h interview = 接近 2 周上限,且 self-interview 完整 6 题 触发 catch-all 反向压力
- C:M-L confidence + ritual prompt 调优是不可压成本 + scope-reality search 警告"weekly-review 工具通常需要 prompts/summaries/history,thin prompt 是 underbuilt"

**Forked at**: 2026-05-08T12:09:30Z
**Forked by**: human moderator (via /fork command;synthesizer 强推 hybrid 路径,operator 接受)
**Rationale**:
本 PRD 是 forge 006 路径 2 的 first end-to-end pilot,目标:
1. 1-1.5 周 ship v0.1(playbook W0-W2 timeline)
2. 真测 SHARED-CONTRACT v1.1.0 跨仓 hand-off(spec.md → ADP spec 7 元素转换)
3. 给 V4 dogfood 提供真用 friction archive 工具(playbook W2 step 4 用得上)
4. 用 hybrid 路径不放弃 industry-aligned hedge

---

## What this fork is for

`007a-pA` 是 simple form PRD(单 candidate · scope IN 仅 v0.1)。下一步:

```
/plan-start 007a-pA
```

L4 阶段 spec-writer 读 PRD.md → 产出 spec.md / architecture.md / tech-stack.md / SLA.md / risks.md / non-goals.md / compliance.md。task-decomposer 产出 dependency-graph + tasks/T*.md。Codex adversarial review 跑 4 轮。**Step 5.5 写 HANDOFF.md** —— 跨仓 hand-off 协议产物,contract_version 1.1.0(SHARED-CONTRACT 实测)。

## Sibling forks (for cross-reference)

L3 stage doc 中其他 2 candidate 仍未 fork(parked,可后续 fork):

- `007a-pA` (this one) — Candidate A + 1 自访谈问题 hybrid(synthesizer 强推路径)
- `007a-pB-trust-flight` — Candidate B 完整 2 周 pilot 协议(park,v0.1 ship 后可考虑 fork 为 v0.2 候选)
- `007a-pC-weekly-ritual` — Candidate C 周复盘仪式(park,scope-reality search 警告 underbuilt 风险,优先级低)

L1 menu 其他 5 条 directions 仍可 fork(L1 menu park 状态):
`007b-team-heat-mirror` / `007c-mirror-on-write` / `007d-complaint-license` / `007e-inline-comment` / `007f-future-self-trail`
