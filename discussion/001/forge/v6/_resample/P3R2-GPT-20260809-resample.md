> ## ⚠ 归档说明(非正式轮次产物 · 2026-08-09 补写)
>
> **这是什么**:2026-08-09T21:24 一次 `cdx-run 001` **误重放**产生的 P3R2 **重采样**。
> 001 队列的 `HEAD` 自 08-03 起一直停在 `20260803T113500-001-forge-v6-p3r2.md` 未前进,
> `cdx-run` 读 HEAD 即重跑,产物**直接覆盖**了正式的 `P3R2-GPT55xHigh.md` 与同名 outbox 文件
> (二者已从 git 恢复原文)。
>
> **正式轮次产物是 `../P3R2-GPT55xHigh.md`(2026-08-03T20:01)** —— 本文件**不是**它的替代,
> 也**不得**被当作 forge v6 的第二次独立复核引用。
>
> **证据力上限(必须随文件一起读)**:本任务书 frontmatter 写的是 `Kickoff form: reuse-session`,
> 而 `cdx-run` 的实现是 `codex "read <task> and execute…"` = **每次新起 session**
> (`codex resume` 是独立子命令,未被使用;bus README §"两种 kickoff 形态" 明写 reuse-session
> 须由人在已开终端粘贴)。⇒ 任务书里「**已读(勿重读)**:双方 P1/P2/P3R1 + X 的 9 件标的」
> 在冷 session 下等价于「**根本不读**」。本文件是一次**上下文更少**的跑,只能证明
> 「同一提示下 `evidence_grade` 打分不稳定」,不能证明任何结论被独立复现。
>
> **实质差异**:verdict 与四条分歧的收敛结果与正式版**完全一致**;唯一分歧在 `evidence_grade` ——
> 本文件把第 1 行降为 `post-hoc-accepted(X-seeded)`、第 8 行降为 `post-hoc-accepted`
> (分布 independent×2 / SOTA-corrected×3 / post-hoc-accepted×3)。
> **operator 裁决(2026-08-09)**:第 1 行的降级**不采纳为改动**(正式版 §underweight-1 已载同一限缩);
> **第 8 行的降级采纳**,已订正进 `stage-forge-001-v6.md`(见该文档 §underweight-11)。
>
> 机制缺陷已另立 `KG-B13` / `KG-B14` 攒批,见 `discussion/006/FORGE-006-v10-PENDING.md`。

# Forge v6 · 001 · P3R2 · GPT-5.5 xHigh · 联合收敛 R2(finalize)· ⚠ 重采样,非正式产物

**Timestamp**: 2026-08-09T21:24:08+08:00
**Visibility**: 已读 Opus P3R2；本轮零新检索。
**Convergence mode**: `strong-converge`

## §1 我对每条分歧的最终立场 + 让步

- **D-1**：接受 `direction` 进入比较类但退出去重，改用 stable claim identity；让步是池化可保留为 warn。残余定义权与冻结时点降 note-2。
- **D-2**：接受 T040 立即局部起跑：5 个非 O2 文件 block，O2 仅 warn/baseline；无需等待额外隔离证明。
- **D-3**：接受对称三级标注，但不接受 Opus 的逐行全判。行 5、7 保持 `independent`；行 1 来自双方共同可见的 X 标的，不是独立到达，降为 `post-hoc-accepted（X-seeded）`；行 8 是我提出合一、Opus 本轮让步，降为 `post-hoc-accepted`。
- **D-4**：坚持且获接受：三态接口 owner 与消费点 fail-closed 合为一个具名新 task，不塞入 T041。

四项均收敛，**无 `unresolved`**。

证据等级只描述结论如何进入共同裁决，不等于结论本身的正确性。共同读取同一标的后给出相同答案，最多证明双方接受了共同输入，不能冒充两次独立复现；一方先提出、另一方在交叉轮让步，也必须记作事后接受。故行 1 与行 8 的降级是对称规则的必要结果，而非针对 Opus；行 5 有双方独立提出及仓内实查，行 7 有双方独立到达，保留原级。

## §2 联合 verdict（单一）

保留池化，但关闭 block-PASS，只作探索/warn。重开须同时满足：池键为 `decision_epoch + rubric + comparability_class` 且 epoch 开启时冻结；`direction` 不参与去重；stable claim identity 已实现。追溯分 `rejected-like`（机器拒绝）与 `disputed-like`（保留但不得 clean PASS）。零旧 PASS 必须形成具名核查记录。`needs-attention` 非 veto，但只有 operator-chair 可逐条记录 addressed 后 override；spec-writer 不得自任，无 chair 记录不得 clean PASS。T040 按局部范围立即启动；三态接口及消费点另立合一 task。此裁决符合 K 对可审计、可证伪且不得以沉默推断结论的要求。

执行顺序固定为：先落零受影响核查记录与合一新 task，再让 T040 在已隔离范围起跑；池化 PASS 继续关闭，直至全部重开条件留下可审计证据。任一前置缺失只能维持 warn，不允许以人工口头确认、空迁移表或事后补 chair 记录替代。这样既不阻塞已安全的局部工作，也不让未闭合语义穿透消费点。

## §3 残余分歧降级为 v0.2 note

- **note-1 · `≥3` 阈值未裁**：触发时点是首个 epoch 关闭、池首次达到 3 条且抽样器记录 `threshold_reached` 事件时；**operator** 必须在该批产生任何 PASS 前回答“是否足以支撑可用判断”。此前风险敞口是阈值价值未经验证；若事件或闸门漏接，会产生结构合规但决策无用的 PASS。
- **note-2 · stable claim identity**：触发时点是 **T021 owner** 将首版 claim 规范化算法提交 `/task-review` 时，由 reviewer 裁定定义与冻结边界。此前 PASS 始终为 warn，同义改写、仅换锚、跨 epoch 重复三类绕过去重风险持续开放。note-2 未闭合前不得进入 note-1 的可信计数。

## §4 W 形态初稿（`decision-list` only）

| # | 裁决 | fallback 三要素 | evidence_grade |
|---|---|---|---|
| 1 | 比较类池键 + epoch 开启冻结 | 齐 | `post-hoc-accepted（X-seeded）` |
| 2 | `direction` 退出去重；stable claim identity | 齐 | `post-hoc-accepted` |
| 3 | 关闭 block-PASS，降探索/warn | 齐 | `SOTA-corrected` |
| 4 | 追溯二态 | 齐 | `SOTA-corrected` |
| 5 | 零受影响具名核查记录 | 齐 | `independent` |
| 6 | operator-chair override 条款 | 齐 | `SOTA-corrected` |
| 7 | T040 局部立即起跑 | 齐 | `independent` |
| 8 | 三态接口 + 消费点合一新 task | 齐 | `post-hoc-accepted` |

最终分布：`independent` ×2、`SOTA-corrected` ×3、`post-hoc-accepted` ×3；不得把共同输入或事后让步包装成独立复现。
