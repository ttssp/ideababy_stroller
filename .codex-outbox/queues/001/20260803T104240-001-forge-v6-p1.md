# Forge 001 v6 · P1 · GPT55xHigh

## §0 读到的标的 / 策略 / K

篇幅略超 1500 CJK 字符:为保留九标的清单与四列 fallback 三要素,未做有损压缩。

读到:1 `forge/v5/stage-forge-001-v5.md` 全文;2 `HANDBACK-LOG.md` 第 39/40 条;3 hand-back 包 `20260802T162313Z...md` 全文;4 PRD v1.7 的 O1/O2、Biggest product risk、v1.7 response;5 XenoDev worktree `spec.md` 指定 §0.1/§1/§6;6 `review-log/001-radar-pA-spec-v07/` 六个 raw log:round1、round1-rescoped、round2-5;7 T021 全文;8 T040 全文;9 T041 全文。未读到:无。Search used: NONE。未读 Opus P1;未读 `_contaminated-p1/`。

阅读策略:先以 raw review log 定 reviewer 原话,再对照 hand-back 包如何转述,最后查 spec/task 是否有可执行落点。K 摘要:集合级判据的分区键必须防止用不相干样本凑数;若事后证明分区错,必须正面定义已放行结论的追溯语义和责任主体。reviewer 判“不应合入”与落地方称“披露即可合”冲突时,必须由显式裁决文档决定谁的话算数,不能靠转述替代。

## §1 现状摘要

**架构设计**:v5 把 O2(c) 从单 run 门改成集合验收,方向是对的:强迫 judge 凑 3 条会把 measure 变 target。但 v0.7 的池键只含 decision epoch + rubric,方向只进去重,round3/4/5 连续指出可跨不相干方向借数。更关键的是 fallback 写成“证明不可比后拆池、不追溯”,等于先允许假 PASS 进入下游,再把撤销语义留空。分区键不是实现细节,它定义“同一集合”本身。

**工程纪律**:raw round5 的结论是“不应合入”,next steps 是修正池分区和三态接口后再合入;hand-back 包把残留定义为超授权问题并 commit v0.7,第 40 条又确认这个程序转述不对。T021/T040/T041 原文仍显示 v0.7 的池化、借池、`INSUFFICIENT_EVIDENCE`/`FAIL` 机器接口没有 owner。当前最稳的纪律线是:spec 文本可作为 v0.8 输入,但不得作为 O2/P2 PASS 权威。item12 注入/呈现面与“1 条判断有无产品价值”本轮无安全/产品价值视角,不判。

## §2 First-take 评分

| A(裁决) | 判据 | 证不出则 B(fallback) | 落点 |
|---|---|---|---|
| **refactor**:O2 池分区键改为 `decision_epoch + rubric + predeclared_comparability_class`；若没有预声明可比较类,不得借池 PASS | 历史证据:raw round3/4/5 均 high 指出跨方向假 PASS;spec §1-O2 自承方向不进分区且要事后拆池 | **operator** 在 v0.8 amendment 冻结前触发;若证不出可比较类,该 run 只能 `INSUFFICIENT_EVIDENCE`;已基于旧池放行的 PASS 标 `needs-revalidation`,下游不得继续当 PASS 消费 | `spec.md` §1-O2(c)/§6 O2;T021/T040 |
| **new**:定义追溯语义:拆池证明原池无效时,受影响 PASS 必须重验或撤销,不能“不追溯” | 历史证据:raw round5 明写需重新验证并撤销受影响 PASS;v5 自认累积规则 post-hoc,不能回判 08-02 | **operator** 在首次抽样发现不可比或 v0.8 migration 时触发;触发前已放行结论进入 `suspended-pass` 队列,由消费方按非 PASS 处理直到重验 | `HANDBACK-LOG` 第 40 条 follow-up;`spec.md` §1-O2 fallback |
| **cut**:删除“reviewer needs-attention 但落地方可自行合入”的隐含规则;needs-attention 默认阻断合入或阻断 PASS 权威 | 历史证据:raw round5 verdict/next steps 是“不应合入/后再合入”;第 40 条裁定“内容判断对,程序转述不对” | **operator** 在 handback-review 入库前触发逐条 override;若未 override,已 commit 的 v0.7 只保留为 provisional spec,不得援引为 O2/P2 PASS;下游语义由该 override 条写明 | `HANDBACK-LOG`;v0.8 amendment frontmatter / Amendment log |
| **refactor**:给三态结果与池化运行时指定真实 task owner；T040 起跑仅限不依赖新池 PASS 的 warn/contract 面 | 历史证据:round2/3/5 均指出 T041 file_domain 不覆盖 CLI/journal;T021/T040 原文仍是 v0.6 单 run/不测结果值 | **task-decomposer/operator** 在 T040 真起跑前触发;若 owner 未定,既有 exit 0/正常落盘产物不能作为 PASS 证据,已放行结论保持 `INSUFFICIENT_EVIDENCE` 或待重验 | T021/T040/T041 或新 task;dependency graph |
| **keep**:产出侧不加 judge 数量下界;集合样本不足走验收侧状态,不逼 judge 凑数 | 历史证据:v5 与 spec 均保留 judge fail-loud 下界 1;PRD O2 明确“≥3 是集合验收采样口径,非单次 KPI” | **operator** 在首个 epoch 关闭时触发;若池仍 <3,起 provenance/anchor-map 排查 task;已放行结论不因补 task 自动转 PASS,仍按当时状态重验 | `spec.md` §1-O2(c);T021 follow-up |

## §3 我现在最不确定的 3 件事

1. `comparability_class` 应由 operator 预声明、由 rubric 派生,还是由每次 direction canonicalizer 生成;三者追溯成本不同。
2. 已 commit 的 v0.7 在仓库语义上应叫 provisional、amended-but-not-pass-authoritative,还是直接 v0.8 撤改;需要 operator 选状态词。
3. 若过去没有真实 O2/P2 PASS 被旧池消费,追溯动作可能只是标注零受影响;但我尚未读到可证明“零旧 PASS”的运行记录。
