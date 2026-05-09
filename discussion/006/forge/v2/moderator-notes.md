---
doc_type: forge-moderator-notes
forge_id: 006
forge_target_version: v2
generated: 2026-05-09
binding: true
read_by: [P1-Opus47Max, P1-GPT55xHigh, P2-Opus47Max, P2-GPT55xHigh, P3R1-*, P3R2-*]
purpose: 把 v1 verdict 之后 9 个月内的事实变更 + operator 真实 grounding 显式告诉两个 expert
---

# Moderator Notes · forge 006 v2

**两个 expert 注意**:本文件由 operator (Yashu Liu) 通过 /forge-inject 注入,**binding**。任何与本文件冲突的 v1 verdict / X 标的解读,以本文件为准。

完整上下文见同目录 `_x-input-draft-by-operator.md`(437 行,operator 已通读认可)。本 notes 是其精炼版,聚焦"v2 跑前 expert 必须先吸收的 5 件事"。

---

## 一、ADP-next 角色重定义(operator 2026-05-09 verbatim)

> "**当前 ADP V4 只是作为一个参考,不做任何强要求强关联,一切从第一性原理出发,搭建一个可靠的 AI 自动开发 pipeline。我还是希望 IDS 负责 idea 到 PRD 的部分,ADP-next 只保障稳定、可靠、高质量、产品级的开发**。"

**对 v1 verdict 的颠覆性影响**:

| v1 假设(隐性) | v2 真实 grounding |
|---|---|
| ADP V4 是 framework "下半边活产物",将持续维护 | V4 是 operator 半年前停掉的"半成品",**不再维护** |
| v1 §3 模块 1-4 + §5 dev plan + sanity-v2 路径 2 假设"在 ADP 补 gap" | 不补 V4,**新建 XenoDev 仓重做**(V4 git tag `v4-final` archive)|
| K5"吸收四个项目尝试"中 ADP 项目 = framework 下半边活产物 | ADP 在 K 中实际指 ADP-next 的设计意图;V4 = 物证(与 idea_gamma2 / vibe-workflow 同级,只是参考)|

**应然分工(operator 决议)**:
- **IDS** = idea → PRD(L1 Inspire / L2 Explore / L3 Scope)
- **XenoDev**(ADP-next 仓名)= PRD → spec → build → ship(独立 L4)
- 跨仓接口 = SHARED-CONTRACT v2.0(双向 hand-off,详 §三)

---

## 二、§9 4 实证 drift(架构级证据,优先于 v1 任何 verdict)

来源:`framework/ADP-AUDIT-2026-05-08.md` §9 L281-543。**v1 verdict 未涵盖 § 9 任何一条**(v1 跑于 2026-05-07,§9 产于 2026-05-08)。expert 必须把这 4 条作为 v2 verdict 的核心证据:

| ID | 严重 | 本质 | v2 verdict 必须回应 |
|---|---|---|---|
| **DRIFT-1** | **架构级** | IDS CLAUDE.md L24 "L4 = spec + tasks + parallel build + ship" 错;实证 IDS 仓**无** Python infra / pyproject / pytest / spec_validator | IDS 是否仍声明自身有 L4?若否,IDS pipeline = L1-L3,L4 完全归 XenoDev |
| **DRIFT-2** | 立即阻塞 | IDS 缺 Python infra(DRIFT-1 症状)| 解决 DRIFT-1 即消失 |
| **DRIFT-3** | 中 | 双 source of truth(IDS specs/007a-pA/ + ADP 也有 13 task)| v2 决定 spec 物理位置后,IDS 的 specs/ 是 DEPRECATED 还是删 |
| **DRIFT-4** | 低/信号 | task-decomposer subagent 行为领先 schema(working_repo emergent)| ADP-next schema 是追认还是显式纳入 |

**关键提示给 expert**:DRIFT-1 修复路径不是"在 ADP 补 gap",**是 IDS framework 自身的重写**(SHARED-CONTRACT v2.0 + IDS CLAUDE.md L24 + plan-start.md)。v1 sanity-v2 推荐的"路径 2 在 ADP 补 3 真 gap" **完全失效**。

---

## 三、SHARED-CONTRACT v2.0 双向 hand-off(operator Q12 决议)

**v2 verdict 中 SHARED-CONTRACT 必须从 v1.1.0 → v2.0(major bump,breaking change)**,内容:

- **正向**(IDS → XenoDev):IDS 产 PRD + 元数据(等价当前 v1.1.0 §3 hand-off 包,可继承)
- **反向**(XenoDev → IDS):**hand-back 包**,内容包括:
  - drift 反馈(类似今天 §9 4 drift,XenoDev L4 build 撞墙时反馈到 IDS L3)
  - PRD 不够细的问题(触发 IDS L3 PRD revision)
  - 实践价值评估(N 个 idea ship 完后的成功率/干预率统计,反哺 IDS L1 选题)
- IDS 仓预留接收路径(eg `discussion/<idea>/handback/<timestamp>.md`)

**v2 不接受单向 hand-off 方案**(operator Q9 已否决:单向没闭环,4 项目 dogfood lesson 收敛断链)。

---

## 四、防"想法变了 → 静默停"(强制 forge 元层锁决定 / Q5 + Q6)

**operator 决议**(基于 V4 失败模式 = "做了一半,我的想法变了" + "野路子直 spec",半年沉没):

- ADP-next 的所有重大决策(架构 / 重大重构 / 重大想法转向)**强制走 IDS 仓的 `/expert-forge`**
- forge **机制本身**(双 expert + SOTA + Codex review + 收敛)= **保留并强制使用**
- forge v1 / v2 的**具体 verdict 内容**(28 项 L/P/C / §9 4 drift / 决策矩阵 / refactor plan)= **仅参考,不做硬约束**;ADP-next 跑 forge 时 expert 可独立论证,即使结论不同也 OK
- IDS = 治理仓(所有元层决策 + forge 命令);XenoDev = 执行仓(只负 L4,不复制 forge 机制)

**对 expert 的指令**:**不要**因为"v1 verdict 已经收敛过 X" 就规避在 v2 重新评估同一议题。v1 verdict 物证保留,但绑定力 = 0(operator 主动选择放弃绑定)。

---

## 五、启动路径(Q13 第一性结论 — expert 不要再推荐"重走 L1-L3")

**operator 决议**:**forge 006 v2 verdict 出后,直接拆 2 流推进,不重走 L1-L3,不另起 idea 008 / forge 008**

**第一性事实**:

| 阶段 | 干什么 | forge 是否覆盖 |
|---|---|---|
| L1 Inspire | 对 raw idea 发散 | **forge SOTA 对标 + decision-list + free-essay 等价覆盖**(P2 SOTA 检索 = 比 L1 更广) |
| L2 Explore | 选一方向深挖 | **forge P3R1/P3R2 双 expert 收敛 = 比 L2 单一深挖更稳健** |
| L3 Scope | 加 operator 真约束写 PRD | **forge W4 next-PRD 自动产 PRD,但**不带 operator 真约束(forge 不问 operator 时间/失败接受度/最小切片) |
| L4 Plan | spec / task / build | XenoDev 自己的 L4 |

**正确启动路径**(expert 在 W4 next-PRD / W5 next-dev-plan 中应假设这条):

```
Step A · forge 006 v2 跑(IDS 仓)→ stage-forge-006-v2.md
Step B · operator 拆 verdict 为 2 流:
  ├─ B1 · IDS 优化(SHARED-CONTRACT v2.0 + IDS CLAUDE.md L24 + plan-start.md + DRIFT-3 处置)
  └─ B2 · XenoDev 启动:
      ├─ B2.1 · operator 在 IDS 给 v2 §4 next-PRD 加 1 节 "Real constraints" + "Open questions"(1-2h 手补 L3)
      ├─ B2.2 · git init /Users/admin/codes/XenoDev / cp PRD 进 XenoDev/PRD.md
      ├─ B2.3 · 走 XenoDev 自己的 L4
      └─ B2.4 · 第一个 task ship 后 hand-back 反馈回 IDS(SHARED-CONTRACT v2.0 反向通道)
```

**不接受**:
- ❌ "建议 operator 把 v2 verdict 拿去走 idea 008 L1→L4"(冗余,L1-L2 已被 forge 覆盖)
- ❌ "建议另起 forge 008 专门论证 ADP-next"(forge 006 v2 已经是)
- ❌ "建议 operator 延后 XenoDev 启动,先做 ADP V4 dogfood checkpoint 03"(V4 已 archive,checkpoint 03 永不会出)

---

## 六、其他 binding 提示(给 expert 看,prefill 时 operator 已选)

- **convergence_mode** = strong-converge(v1 是 preserve-disagreement;v2 X 厚 + operator 心中已有方向 → 收敛单一 verdict 价值更大)
- **W** = W1-W6 全选,但 W4 next-PRD 应**聚焦 ADP-next/XenoDev 的 PRD**,不是 framework 整体 PRD
- **新增 Y5** = "重做的代价 / 沉没成本 / 知识保留"(L/P/C 分层视角:V4 实装哪些 L 可保留 / P 可借鉴 / C 必须丢)
- **time** = operator 不设上限(§6.7),expert 给的"X 周完成"建议都是节奏参考非硬约束
- **success metric**:质量+数量复合(N 个 idea ship + operator 干预率 < X%);具体 N 与 X、"干预"计量方法、滑动窗口、"真 idea" 边界 = **由 v2 expert 论证决定**(operator 期望 expert 在 P3R2 给具体数字 + 论证)

---

## Changelog

- 2026-05-09 v1: 初稿。从 `_x-input-draft-by-operator.md` §1+§3+§4+§5+§6 + ADP-AUDIT §9 提炼,作为 P1/P2/P3R1/P3R2 binding 上下文。所有 5 个 §对应该草稿的更长论证;expert 若需深读源证据,Read `discussion/006/forge/v2/_x-input-draft-by-operator.md` 全文。
- 2026-05-09 后续操作:`_x-input-draft.md` 重命名为 `_x-input-draft-by-operator.md`(避免被 expert-forge Step 0.5.4 prefill 子代理覆写为同名 `_prefill-draft.md` 兄弟)。
