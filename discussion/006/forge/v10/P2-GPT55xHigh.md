# Forge v10 · 006 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-08-11T05:43:53Z
**Searches run**: 24 queries，SOTA-benchmark。
**Visibility**: 我已读双方 P1；未读 `P2-Opus47Max.md`。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| warn→error | Rust future-incompat | compiler team 每个 6 周周期回审，FCP 后明确转 hard error 或撤销 | 写“复发 ≥2 次”，无计数者、消费 gate、执行者 | 缺 owner、周期关卡与可枚举出口；次数不是升级机制 | [Rust RFC 1589](https://rust-lang.github.io/rfcs/1589-rustc-bug-fix-procedure.html) |
| warn/defer | Python、Kubernetes deprecation | Python hard deprecation 写目标 release，soft deprecation 明示无移除计划；Kubernetes 以稳定级别绑定最短 release/时间窗并在发布边移除 | 三种 warn 均未区分临时态与稳定 advisory | `defer` 合法，但必须是显式终态；拟升级者必须有版本/事件 sunset | [PEP 387](https://peps.python.org/pep-0387/) · [Kubernetes policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/) |
| 存量债 ratchet | Sonar “new code” gate | PR 只对相对 baseline 的新代码应用失败条件，旧债不被追溯阻断 | check-8 若直接升硬门会拒 47/100 历史包 | 应分 forward gate 与历史只读语料，而非全库同步翻硬 | [Sonar quality gate](https://docs.sonarsource.com/sonarqube-server/2026.1/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates) |
| 例外回收 | Ruff `RUF100` | 机器识别已不再压制任何诊断的 `noqa`，并可自动删除 | 白名单只靠定期人工过表，“只减不增”无工具 | ratchet 应消费基线并自动拒新增/清除失效例外 | [Ruff RUF100](https://docs.astral.sh/ruff/rules/unused-noqa/) |
| review 分级 | 变更风险研究 | 48 人对照实验中，风险提示显著提高风险意识与 review effectiveness；11 项目 JIT 模型以 68% accuracy/64% recall 预测缺陷变更，供 QA 分配注意力 | 以“脚手架 vs gate.py”两个案例推模块关键性 | 支持**风险感知分配注意力**，不支持静态模块二分类或据此设不同轮数 | [Yu et al. 2024](https://rebels.cs.uwaterloo.ca/papers/emse2024_yu.pdf) · [Kamei et al.](https://kyushu-u.elsevierpure.com/en/publications/a-large-scale-empirical-study-of-just-in-time-quality-assurance/) |

## 2. 用户外部材料消化

n/a（K 未提供外部链接、文件或文本材料）。

## 3. 修正后的视角

1. P1“不能再靠无人消费的复发计数”**站住**：Rust 的升级由具名团队在固定 release gate 作 hard/remove 决策；Kubernetes 也把 sunset 绑版本与时间，而非观察次数。
2. P1 的隐含二态观被**修正**：并非所有 warn 都必须升级。PEP 387 证明永久 `defer` 可以合法，但须显式标为 soft、承认无移除计划；临时 warn 才必须带 due event 与 owner。
3. P1 对历史包不追溯硬拦、对新包直接消费 gate 的方向**站住**；Sonar 的 new-code baseline 给出成熟 ratchet，Ruff 又证明失效例外可机器回收。KG-B19 不能只“接 v9 ledger”，仍需要实际比较基线的工具。
4. **对 (a)：证据不足。**研究支持按**变更风险信号**调整注意力，但没有支持“低关键脚手架/高关键门禁”的静态分类，更没有支持不同轮数；T041 vs FU-R5F4 的 n=2 不能决定 XD-44′ 修法。
5. **对 (b)：类比只在状态形状上部分成立，不能提高对 v9 完整机制的评价。**SOTA 的 warning/debt 都绑定真实 release/PR gate；本仓 ledger 虽有 `pending/due_gate` 同形，但 9/11 obligation 的 consumer 未接线，且无自然时钟。相似数据模型不等于相似 enforcement coverage。
6. 因此我 P1“多数不是 v9 未接线实例”**站住**：v9 可承载 sunset 与修复义务，却不能替代 advisory 分类、风险模型、review 终态或 ratchet 工具本身。
