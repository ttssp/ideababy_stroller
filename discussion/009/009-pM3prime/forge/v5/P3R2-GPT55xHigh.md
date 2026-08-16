# Forge v5 · 009-pM3prime · P3R2 · GPT-5.5 xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-08-16T14:36:08+08:00
**Visibility**: 我已读对方 P3R1 + P3R2。
**Convergence mode**: **strong-converge**
**Searches in this round**: NONE。

## 1. 我对每条分歧的最终立场 + 让步

- `-04`：接受对方全让后的形态——载体裁级、映射绑定消费 gate 与结账证据；我让步于“不预设正文镜像”。
- 完备性：双方收敛为“语义不可穷举、程序必须全定义”；`unclassified` 交具名解释者并留痕复审，默认 fail-closed。
- `-05`：双方撤回先后排序，每态同时绑定允许方法、已知敞口、退出证据。
- 模板：双方采用七问消费契约；`clock_or_reachable_event` 两者皆无则消费点 fail-closed，不伪造期限。

## 2. 联合 verdict（单一）

**CONCERNS；定向 refactor，不 redesign。** 五题统一改写为七问消费契约：`normative_site/owner/trigger/options/clock_or_reachable_event/consumer_action/settlement_evidence`。动作分类：`-04/-05/-12` refactor，`-11` new，`-09` refactor + new。程序必须全定义，未分类不得自动通过。

四条跨体系硬内容审查后需条件化：① **过度外推**：OLRC 支持“未 codify 仍可合法且可映射”，不支持本仓必须采用固定三级标签；正文只应强制载体等级显式、可发现、可消费。② **过度外推**：DO-178C 的独立性随安全保证目标成立，不能推出每条仓库义务都须 owner 与 reviewer 人员分离。③ **过度外推**：NCHS 的比例呈现规则不能直接移植精确三档或阈值；可保留“目标市场分别判、低样本显式状态”，且 US 不构成 CN/HK 重判依据来自本仓量词，不靠 NCHS。④ **忠于适用条件**：BCBS 要求风险相关分层可得；本仓条件 2 已把 market 定为相关轴，故 `-09` 新建 market 观测轴成立。

元层活体标本的处置：A∧¬B 落入未分类时，由 operator 解释，默认不自动通过，以 `moderator-notes.md` 留痕并交双方后续 phase 消费。本 note 有载体、消费者、实际可达触发和个案处置；欠缺的是 K 的一般 fallback。本轮七问补成 `unclassified→operator note→cross-model review→synthesis settlement`。因解释者仍是最终 owner，证据等级只能是 `post-hoc-accepted`，不得称 independent。

## 3. 残余分歧降级为 v0.2 note

- **KG-42 同族未解**：同意具名敞口。单人仓可用跨模型、跨会话时间分离和 operator 独立签收作缓解，但不满足人员独立。**due_gate**: `forge:006:phase0`；**exposure**: 同一 authority 自审，相关盲点无组织隔离。
- **可达事件源未验全**：**due_gate**: `forge:009-pM3prime:phase0`；**exposure**: 若无事件，fail-closed 可能永久悬置。
- **`-09` 成本未实测**：**due_gate**: `xenodev:task-review`；**exposure**: 该消费 gate 未接线，成本与义务均可能不被复核。

## 4. W 形态产出的初步草稿建议

- **verdict-only**：「五条义务由产生侧完成改为七问消费契约；程序未分类一律 fail-closed。」
- **decision-list**：

| 决定 | obligation path（产生→消费） | evidence_grade |
|---|---|---|
| `-04` 调整载体裁级/映射 | forge 裁决→相关正文 gate | `SOTA-corrected` |
| `-05` 调整方法×状态×敞口 | control history→PRD §6 重判 | `SOTA-corrected` |
| `-11` 新增消费动作 | `census_run`→`/handback-review` | `independent` |
| `-09` 调整条件并新增 market 轴 | `_run_batch`→SLA E1/PRD §6 条件 2 | `SOTA-corrected` |
| `-12` 调整为 catch-all/复审 | task-review verdict→operator ship gate | `SOTA-corrected` |

- **refactor-plan**：`PRD.md §6` 改目标市场量词与低样本状态；`warn-registry/README.md` 状态表绑定方法/敞口/退出证据；XenoDev `aggregation_probe.py::_run_batch` 与 `SLA.md E1` 接 market 轴及消费判据；`codex-review/SKILL.md §4.2` 加程序 catch-all；`framework/obligations/ledger.jsonl` 仅记录裁决与路径，不现场改 schema。

红线保持：M1 不解锁扩样/E2，41 条盲标路 CLOSED，C6 数字不动，不现场改 producer/validator/SHARED-CONTRACT schema，不跨入 PRD/dev plan。
