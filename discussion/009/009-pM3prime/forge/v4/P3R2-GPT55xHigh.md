# Forge v4 · 009-pM3prime · P3R2 · GPT-5.5 xhigh · 联合收敛 R2（finalize）

**Timestamp**: 2026-08-14T12:46:01+08:00  
**Visibility**: 我已读对方 P3R2。  
**Convergence mode**: strong-converge  
**Searches in this round**: NONE。

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1（`OB-15` 四前提）**：对方承认漏掉 “exact times of failure are recorded”，双方统一四前提加 fallback。我让步于不写死实现；最终要求见 §2。
- **分歧 2（周期与 N）**：接受对方把 K 改判 ✅，也接受剩余能力称**具名敞口**而非优化：身份稳定时的缓慢漂移尚无触发器。不给任意 N，但 note 必须接线。
- **分歧 3（版本化回退）**：完全收敛到“历史不可变；授权被后续 `caliber_version` supersede”。我让步于 convert 可回退不必提高成单向门槛。
- **分歧 4（per-market）**：排除 v4 硬产出；接受对方对误引的更正——“那句是我对议题⑤说的”。未满足说明必须落到 `PRD.md` §6 条件 1，不能只留在 stage doc。
- **A 侧守住项**：同意 “必须带 `due_gate`”。统计重校准 note 的 gate 取 `forge:009-pM3prime:phase0`，但语义须写成**义务登记后的下一次 firing**；它已接线，优于尚未接线的 `xenodev:*`。

## 2. 联合 verdict（单一）

**CONCERNS。** M1 pass 欠具名裁决：仅接受为固定批可比性证据，不作效度代理、不外推、不解锁 E2；rationale 必须载明歧义抹除风险与六项密度全部低于门槛。现状跨批比较不可信；`OB-15` 只有在预注册观察/停止边界、逐 attempt exposure 可计、失败结果及精确时间/区间留存且删失可识别、失败批内容身份可比四项同时可证时兑现，否则回退写穿透或等价耐久回执。每个消费批次必测落库，身份/口径变化立即开新基线；XenoDev 产证，IDS operator-chair 接受基线并升版。C4 convert 须过程证据、结果证据、具名批准、版本化回退四者合取；历史不可变，未来消费权可被新版本 supersede。**0 unresolved。**

## 3. 残余分歧降级为 v0.2 note

1. **统计型重校准间隔**：具名敞口；积累足量 control history 后再预注册方法与 N。`due_gate: forge:009-pM3prime:phase0`；`due_event: obligation 登记后的下一次 firing`。
2. **per-market 跨次分解**：非 v4 硬产出；当前未满足先写入 `PRD.md` §6 条件 1。`due_gate: forge:009-pM3prime:phase0`；下次 firing 决定是否升为义务。
3. **`xenodev:*` 消费点接线**：在接线前所有相关义务均标 `consumer_wired: false` 且填写 `exposure`。`due_gate: forge:009-pM3prime:phase0`；下次 firing 复核接线状态。

## 4. W 形态产出的初步草稿建议

### verdict-only

直接采用 §2；标题为 `CONCERNS`，末尾注明不得解锁 E2、不得翻转 41 条 CLOSED、不得修改 C6 数字。

### decision-list（四列 + obligation path 列）

| 保留 | 调整 | 删除 | 新增 | obligation path |
|---|---|---|---|---|
| M1 仅作固定批证据 | pass 条款与结果矩阵同步写具名裁决 | — | 两项风险输入 | `v4:phase4 → forge:009-pM3prime:phase0` |
| — | `OB-15` 兑现语义 | “机制存在即可信”的隐含等价 | 四前提 + fallback | `→ xenodev:handoff-intake`；`consumer_wired:false` + `exposure` |
| 批次作为监测节拍 | 身份变化立即新基线 | 任意 N | 双仓责任 + 重校准具名敞口 | `→ forge:009-pM3prime:phase0` |
| C6 历史不可回改 | C4 convert 四合取 | “回退等于改旧结论” | 未来消费权 supersede 语义 | `→ forge:006:phase0` |
| per-market 非 v4 gate | `PRD.md` §6 条件 1 注记 | — | 未满足说明 | `→ forge:009-pM3prime:phase0` |

### refactor-plan

1. **条款同步组**：v3 结果矩阵 pass 行、对应 OB note、`PRD.md` §6 条件 1 同步，防止正文与表格分叉。
2. **可观测性组**：`census.py` attempt log 覆盖四前提；`SLA.md:136` 判据列补跨次读数存在性。
3. **C4 同步组**：IDS `PRD.md` §7 红线 3、XenoDev `spec.md` C4、`SLA.md` E1 行采用同一四合取与版本化回退语义。所有 `xenodev:*` obligation 在 Step 6.5 标 `consumer_wired:false` + `exposure`。
