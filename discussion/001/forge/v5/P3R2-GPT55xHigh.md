# Forge v5 · 001 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-08-02T22:38:30+08:00
**Visibility**: 我已读对方 P3R1 + P3R2；`moderator-notes.md` 不存在。
**Convergence mode**: strong-converge
**Searches in this round**: NONE

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1 · ratchet 证据等级**：接受对方让步。最终写成 scoped verification 是标准依据，ratchet/baseline 是行业实施形态；不再称二者“共同构成明文先例”。
- **分歧 2 · 第三值**：已收敛。`INSUFFICIENT_EVIDENCE` 现在落 spec 语义，CLI/字段协议留 T041，且不追溯。
- **分歧 3 · 产品价值**：已收敛。O7 机制 keep；消毒转义、可读性、判断密度 refactor。
- **分歧 4 · 解释掉**：已收敛并双向登记。我方在强制多样本有效性面不设防；对方的累积规则属 post-hoc，只对下一次评估生效。
- **分歧 5 · 九特征直接成 gate**：接受对方完整让步。ISO 29148 只作分类；本地化表必须有对象、证据、责任人、fallback，Feasible 终止于有资质者评审与真跑/历史证据。

### 12 项施工单逐项审计

| item | 表态 | 最终修订 |
|---|---|---|
| 1 | **改判据、改 B** | A 保留。除四列外，warn 候选必须填 `evidence_plan`、`review_by`、升 block 条件；缺字段当场不通过。Feasible 证不出可 shadow/warn，但不是已冻结 block gate，也不得无证据自动续期。首次出现过期后仍续 warn 即触发 v6，早于“几乎总是证不出”的模糊观察。 |
| 2 | **改 A、改判据、改 B** | 累积池仅限同一 decision epoch 与 rubric；epoch 的 `closes_on` 预先固定且不得事后延长。按“规范化 claim + direction”去重，同 claim 的新 anchor 合并；抽样时 anchor 必须仍有效。当前 run 至少有 1 条非豁免、带证据判断才可借池 PASS；当前全豁免/零有效判断一律 `INSUFFICIENT_EVIDENCE`，旧池不能替它空过。若方向不可比，拆池而非退回强迫单 run 产 3 条。 |
| 3 | **改判据** | A、B 保留；“不得推出两种实装”本身不可机器判。每条规范行改用稳定 requirement ID、唯一 expected outcome，验证命令一对一引用同 ID；语义歧义由有资质者复核，发现双语境即走 item 11。 |
| 4 | **改判据** | A、B 保留。机器判据明确为 `start=min(first_journal_date, effective_date+30d)`，O7 截止为 `start+3 months`；本次首行已触发才得到 2026-08-02 至 2026-11-02，不能把 longstop 的 30 日和观察窗三个月混写。 |
| 5 | **同意** | 三类 usage 互斥；跨用途必须拆成两条，禁止一条兼任。 |
| 6 | **改 B** | 不给 judge 产出下界，A 与判据同意。`≥5 run` 未给来源，删除这个魔数；在 item 2 预先声明的首个 epoch 关闭时池仍 <3，才启动 provenance/anchor-map 上游任务，状态持续为 `INSUFFICIENT_EVIDENCE`。 |
| 7 | **同意** | 语义层现在闭合 OQ-A1-1，协议层留 T041；不追溯。 |
| 8 | **改判据** | A、B 同意；验收除 pytest/mutation 外，必须保存 baseline 版本，并证明存量违规只 warn、新增同类违规才 block，避免“名为 ratchet、实为全量门”。 |
| 9 | **同意** | 兜底必须有另一门实际转红的测试或 mutation 证据；证不出按无兜底收紧本门。 |
| 10 | **改判据、改 B** | 四要件保留，并新增 `review_by < expires_on`。到 `review_by` 后 warn，到 expiry 后 fail closed；与代码无关的转红是风险接受到期的预期语义。NIST 材料不提供固定 N，提前量由 operator 的 review SLA 写入条目。实现超 S 只可人工预警，expiry 的机器转红不可省。 |
| 11 | **同意** | 采用两类限定词、术语章点名否决裸用，不动 C″；裸词扫描范围限定规范性 spec，历史引文不计。 |
| 12 | **改 A、改判据、改 B** | 不是“反转义”，而是从规范存档生成上下文安全的展示投影；恶意样本在目标上下文必须保持 inert，且可回指规范证据。若证不出安全，展示版不 ship，保留规范版并改善非执行式阅读辅助；“不作证据用途”标签不能替代注入防御。 |

**穷尽性检查**：修订后 12 项覆盖四簇的实质问题；正确现状也应在 decision-list 明保留，包括 selfcheck 正向 allowlist、门②声明机制与 C″ 分流契约。施工包仍漏一项过程闭环：P1 已读到 R5 尚未正式裁决。它不另造产品 item，但必须设为落地前置：逐条标 accepted/rejected/deferred，并映射到 12 项，否则“穷尽”没有完整证据基础。

## 2. 联合 verdict(单一)

**联合 verdict：采定向 refactor，CONCERNS，不阻断 T040 窄起跑。** ISO 29148 作为冻结前分类框架，但每项必须本地化为对象、证据、责任人、fallback；Feasible 只认真跑或历史证据。O2(c) 改挂有 epoch、去重、有效性与当前-run 防空过约束的集合验收池，产出侧不设 judge 下界。第三值分层落地；R4-F4 用独立批准、等效控制、预警与到期转红；O7 补 longstop；产品展示采用上下文安全投影。T040 立即以 warn+versioned baseline、只卡新增实施。无 unresolved，但 R5 裁决闭环及上述修订是 synthesizer 落单前置。施工前须采用本稿对 item 2、10、12 的修订；任一被删，都会分别重开空过、隐藏例外到期或用标签解释安全风险，联合 verdict 随即降为 BLOCK，不得降级成实施注记。

## 3. 残余分歧降级为 v0.2 note

- **v0.2 note 1**：强制多样本输出是否在其他评审系统有效仍未检索；若首个预声明 epoch 关闭后池仍 <3，再补该方向证据，不事后改本 epoch 规则。
- **v0.2 note 2**：跨方向判断的长期可比性仍需首池抽样复核；出现 operator 无法作同一验收抽样时，按 item 2 拆池。
- **v0.2 note 3**：forge-protocol 的“字”歧义归 006，改为 CJK 字符/Latin words 双口径并禁止有损机械压缩。
- **反自欺收口**：新发现两处被轻描淡写。其一，item 12 用“不作证据用途”解释掉展示面的注入风险；标签不降低攻击面，已改为证不出安全则不 ship。其二，item 10 把 expiry 的突然转红降成实现代价 note；它其实是必要 fail-closed 行为，已补 `review_by` 预警。另登记 `≥5 run` 为无依据阈值、R5 未裁为证据闭环遗漏。

## 4. W 形态产出的初步草稿建议

- **verdict-only**：判据冻结前采用 ISO 29148 分类，但标准只命名、不代证；block gate 必须有本地化四列与真跑/历史证据，证不出只可有期限地 warn 取证。
- **decision-list**：以 §1 的 12 行为最终底稿；在表前新增“R5 逐条裁决完成”落地前置，在保留栏补 selfcheck 正向 allowlist、门②与 C″。item 2、10、12 必须采用本稿修订，不得沿用旧 fallback。
- **next-PRD**：只补三点：O7 起算/longstop/截止算法；呈现面安全与可读性是 O1 风险；判断数量是集合验收采样，不是单次产出 KPI。Scope OUT 与 O4 不改。
