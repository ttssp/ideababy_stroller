# Fork origin

**This fork**: 007a-agent-emit
**Forked from**: 007 · L1
**Source stage doc**: ../L1/stage-L1-inspire.md
**Selected candidate**: Direction 1 · "Agent 自录摩擦"(主语反转)

**Candidate description (extracted from source, paraphrased)**:

把 friction-tap 的主语从 operator 反转成 Claude session(agent 自身)。原 proposal 假设
"operator 主动跑 `friction <msg>` 命令记录摩擦点",但 dogfood 阶段的真实瓶颈是 operator
注意力稀薄,任何要 operator 主动做的动作都会漏。

这个 fork 把记录的主路径换成 **agent 在被工具链卡住的当下自己写一条 entry**:Claude session
跑 task 时 tool 失败 / hook block / retrospective 出 placeholder — 不需要任何 operator 动作,
session 自己识别"这次失败是工具链摩擦",通过一个 hook 写一行进 friction-log。`friction <msg>`
CLI 仍然存在,但退化成 operator-fallback(用于 agent 没识别但 operator 觉得是 friction 的场景)。
operator 角色从"记录者"变成"看回放者",一周后看 retrospective 时直接看到"agent 自己记了 27 条"。

**为什么选这条**(不是 menu Top 1):
- spark 高 + scope 清晰(post-tool-call hook + emit 函数 + CLI fallback)
- 与 V4 retrospective skill 直接协同(self-monitoring 是 retrospective 的根本预设)
- 1 周内可 ship 可信(适合 playbook L19 时间窗)
- menu Top 1 `007d-complaint-license` 是更彻底的破框,但 scope 是文化产物,1 周内难有可
  ship 代码 — 暂搁;若 007a 跑通后 operator 决定再 fork 一条,Top 1 仍在 L1 menu 等着

**Forked at**: 2026-05-08T07:31:48Z
**Forked by**: human moderator (via /fork command,从 forge 006 路径 2 playbook Step 1
  选定的 first end-to-end pilot)
**Rationale**:

这是 forge 006 路径 2 启动前 4 周 playbook 的 first end-to-end pilot,目标是 1 周内走完
L1→L4 实测 SHARED-CONTRACT v1.1.0 跨仓 hand-off。proposal 007 + L1 menu Direction 1
的组合,既有真实自用价值(让 V4 dogfood 摩擦记录的成本降到零),又能 stress-test 整个
IDS → ADP 流水线。

---

## What this fork is for

Now `007a-agent-emit` is its own independent sub-tree. The next layer (L2 Explore)
will operate on the candidate above as if it were a fresh proposal — deep unpack the
"agent self-emit" idea (who 用 / 体验 / 现成相邻 / spark 持久 / 风险),仍然 NO tech /
feasibility content。

下一步:

```
/explore-start 007a-agent-emit
```

## Sibling forks (for cross-reference)

L1 menu 的其他 5 条 directions 仍未 fork(都在 L1 menu park 状态,可以以后 fork):

- `007a-agent-emit` (this one) — Direction 1 · 主语反转
- `007b-team-heat-mirror` — Direction 2 · 集体觉察(both-endorsed 唯一)
- `007c-mirror-on-write` — Direction 3 · 写时强制读
- `007d-complaint-license` — Direction 4 · 心理许可(menu Top 1 / 最破框 — 暂搁)
- `007e-inline-comment` — Direction 5 · 载体反转
- `007f-future-self-trail` — Direction 6 · 接收者重定义
- 原 proposal baseline — 仍可 `/explore-start 007` 走

仍 fork 兄弟方向?

```
/fork 007 from-L1 direction-<n> as <suggested-id>
```
