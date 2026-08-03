# forge 001 v6 · P1 · GPT55xHigh

## §0 标的清单 + 阅读策略 + K 摘要

**Search used**: NONE。**Visibility**: 未读 Opus P1。九件标的均已读到原文:X1 v5 stage 全读;X2 HANDBACK-LOG 第 39/40 条原文;X3 hand-back 包全读;X4 PRD v1.7 相关段;X5 spec v0.7 指定段;X6 round1、round1-rescoped、round2-5 raw log;X7/T021、X8/T040、X9/T041。XenoDev 侧为 worktree 原文直读,未用摘录兜底。策略:先读 v5 决策表与 v0.2 note,再比对 hand-back 对 round-5 的转述,最后用 spec/task 原文验证可执行落点。
**篇幅声明(GPT55xHigh)**:本文可能超过 1500 CJK 字符;为保留 §0 读到声明与 §2 四列矩阵,未做 `sed`/截断式有损压缩。


K 摘要:本轮裁两件事。第一,集合级判据的池键若为凑数而允许借不相干方向,则 PASS 不是验收而是污染;若事后证错,撤销/重判语义必须由 IDS/operator 定义,不能由 spec-writer 用“不追溯”自批。第二,reviewer 明说 needs-attention/no-ship 时,“披露即可合”不是有效判据;**已显式披露不得作为任何判据或 fallback**。

## §1 现状摘要(按 Y)

**架构设计**:v5 item 2 把池限定为 epoch+rubric,却把 direction 只放进“规范化 claim + direction”去重。结果是 direction 抬高计数,不限制借用;当前 run 1 条有效判断可借其他方向 2 条历史判断 PASS。fallback 首次触发后补出的是“事后拆池、不追溯”,叠加 post-hoc/结果值不追溯,系统趋向“一次 PASS 永久 PASS”。codex round3/4/5 三轮 high 说明这不是披露残留,而是 v5 四列范式 fallback 栏缺主体、时点、既有结论处置后的真实失败。

**工程纪律**:round5 原文是“不应合入”“冻结并实现三态结果的 CLI/产物协议后再合入”,hand-back 包转成“超权限项,披露即完成”后 v0.7 commit 落地,这正击中 K(b)。T021/T040 仍是 v0.6 单 run 阈值并带 OQ-A1-1 死链;T041 只覆盖 bench/e2e,不覆盖 CLI/journal,所以 `INSUFFICIENT_EVIDENCE` 仍无机器接口 owner。涉及注入防御、例外到期、“1 条判断是否有产品价值”的面,本轮无安全/产品价值视角,不作覆盖性判断。

## §2 First-take 评分(decision-list)

| # | score | A(裁决) | 判据 | 证不出则 B | 落点 |
|---|---|---|---|---|---|
| 1 | refactor | pool key 必须加入 `direction` 或预声明 `comparability_class`,并在 epoch 开始冻结;direction 不能只用于去重 | round3/4/5 连续 high;现结构允许跨方向假 PASS | 暂不能定义可比类时,PASS 向维持 warn/`INSUFFICIENT_EVIDENCE`,禁止跨方向借池判 PASS | spec §1-O2(c)/§6 O2,T021/T040,v0.8 amendment |
| 2 | new | 拆池若证明原池不可比,受影响既有 PASS 必须 versioned re-evaluate/撤销或标 disputed;下游语义由 IDS/operator 裁 | K(a) 问“追溯由谁定义”;round4/5 明指 prior PASS invalidation | 无法枚举依赖者时,冻结新 PASS,旧 PASS 不得作为 clean PASS 下传 | spec 状态模型,HANDBACK-LOG/hand-off 语义 |
| 3 | cut | 裁掉“披露即可合”。codex verdict != approve 时,除非 operator 明文 exception,不得把 amendment 视作 reviewed/mergeable | round5 next steps 是“后再合入”;hand-back 转述吞掉 reviewer 结论 | 无 exception 记录则保持 needs-attention,后续 v0.8 强制随行 | HANDBACK-LOG 第40条补裁;spec frontmatter review 状态 |
| 4 | refactor | 三态结果是公共接口,须有覆盖 CLI/journal/status artifact 的 task owner;T041 现状不是 owner | T041 file_domain 仅 bench/e2e;T021/T040 自述旧语义;round2/3/5 high | owner 未定则保留治理阻塞项,非 PASS 不得 exit 0 正常落盘 | 新 task 或重派 T022/T030/T041;依赖排在 T040/T041 前 |
| 5 | keep/refactor | §0.1 的分方向自检保留:IE/FAIL fail-closed 可生效;PASS 向必须 warn,直到 R5-F2/F4 复核且 claim identity 落地 | §0.1 首次应用即抓到 v5 item2 PASS 向不具冻结资格 | 若 usage 标签不能表达分方向等级,整条 PASS gate shadow | spec §0.1/§1-O2,T021 负向测,T040 O2 契约 |
| 6 | keep/refactor | T040 可局部起跑:5 个非 O2 文件和 baseline 可做;O2 pool PASS 断言只做 warn/baseline,等 v6 键裁完再 block | item8 自带 fallback;`tests/contract/` 现零进展;O2 形态依赖本轮裁决 | 若不能隔离 O2 PASS 断言,则 T040 等 v6 后起跑 | T040 执行边界;不阻断其余 contract suite |

## §3 现在最不确定的 3 件事

1. 既有 PASS 的依赖面在哪里:是否已有下游消费 O2/P2 PASS,以及撤销通知、版本化、journal 重判由哪条链承接。
2. §0.1 是“正常工作”还是“把不合格 PASS 判据贴 warn 后塞进 frozen spec”:分界要靠机器可读 usage/status 表达,目前仍像散文。
3. 三态接口 owner 应归 T022/T030/T041 还是新 task:我确定 T041 现状是范畴错误,但未在 P1 展开任务拆解。
