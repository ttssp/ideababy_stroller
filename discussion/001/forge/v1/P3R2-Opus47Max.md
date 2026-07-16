# Forge v1 · 001 · P3R2 · Opus(Claude Code main)· 联合收敛 R2(finalize)

**Timestamp**: 2026-07-16T06:20:00Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge(从 forge-config 读)

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1(盲测识伪的残余地位)**:
  - 对方 P3R1 论证:"optional calibration 只入 journal,不得解锁" → **接受并采纳其收紧**。
  - 我的最终立场:识伪盲测 **retire-as-gate, keep-as-calibration**——保留负控注入机制作可选校准活动(operator 自发起、无签字模板、无 PASS/FAIL 裁决),产出只写 journal 作校准证据,**零解锁语义**(防止盲测借尸还魂回前置)。
  - 让步给对方的部分:我原表述「可选校准活动」未封死解锁语义,采纳对方的显式封条。
- **分歧 2(新阻断前置清单宽度)**:
  - 对方 P3R1 论证:"阻断项限 trace 完整、引用可达、review queue 一致;journal 放使用期治理" → **部分接受**。
  - 我的最终立场:阻断前置 = **机器可自动判三项**:① trace/provenance schema 完整性(每条位移判断/边带 source trace);② 证据可达性(3 击回溯的链路机器可解析、引用可解析到原文条目);③ 审计通道就位(留痕可被 operator 抽查的最小结构存在且一致)。journal 规则**全部**归使用期治理,不阻断。
  - 让步给对方的部分:采纳其「引用可达」为独立第③……实为第②项;我原「抽查通道就位」与其「review queue 一致」合并为第③项。我坚持并对方无实质异议的一点:第③项在 v0.1 自用语境下必须是**轻量文件级结构**(briefing 留痕 + 抽查记录的 schema 校验),不得膨胀为 LangSmith 级基础设施——否则新 gate 变旧仪式(对方 R2 期望原话即"防新 gate 变旧仪式",此为共识)。
- **分歧 3(FAIL→STOP 触发器)**:
  - 对方 P3R1 论证:"STOP 限缺 trace、时间线断裂、引用不可达……人工只补证" → **接受为机器道;补充治理道**。
  - 我的最终立场:**双道 STOP**。机器道:可复现的机器可验失败(缺 trace / 时间线断裂 / 引用不可达 / 留痕结构不一致)→ pipeline 内自动 STOP,阻断下游。治理道:operator 抽查发现叙事级造假/系统性失真(机器判不了的判断级发现)→ 走既有 **prd-revision-trigger hand-back** 通道 = 流程级 STOP(本次 forge 自身就是该通道运转的实证)。人工发现不直接拍机器 gate,先转化为可复现证据(对方「人工只补证」)或升级治理(hand-back)。
  - 让步给对方的部分:接受「机器 gate 只接可复现失败」;治理道不是新机制,是既有通道的显式命名,对方应无异议。

## 2. 联合 verdict(单一)

**P0.2「人肉盲测二值签字」gate 从 T010/T011 解锁前置中退役——采纳 KG-B8。**新解锁前置 = 机器可自动判的最小验收三项:trace schema 完整性、证据 3 击可达性、轻量审计通道就位;三项秒级可跑、无人肉停机。operator 的判断力从「一次性考官」移位为「使用期抽查者 + journal 累积校准」——批评①②③的直接落地,且有 SOTA 先例背书(抽样人审 + 噪声传感器校准 + provenance 验收,双方 P2 独立命中)。防 V4 铁律不丢:FAIL→STOP 双道保留——机器道拦可复现失败,治理道(prd-revision-trigger)接 operator 判断级发现。识伪盲测机制降级为可选校准活动,产出只入 journal,零解锁语义。KG 级联:**B8 采纳**(形态重构);**B7 大部消解**(签字/answer-key/反作弊面随盲测退役而退场,残余的 reviewer leakage/Goodhart 归为使用期审计设计,不再投资加固);**B4 保留但改写**(机器强制对象从「RERUN-PASS artifact 存在」改为「最小验收三项的机器闭环 + 机器道 STOP 的代码级 wiring」——B4 的教训恰恰适用于新 gate:不能再靠 markdown 约定)。无 unresolved。

## 3. 残余分歧降级为 v0.2 note

- **v0.2 note 1**:第③项「审计通道」的最小 schema 具体长什么样(单文件 vs 目录结构 vs 附着在 briefing 内),留 XenoDev spec 层按 v0.1 自用实况定;若实装时发现三项里任何一项无法秒级机器判,回头重审该项资格。
- **v0.2 note 2**:识伪校准活动的频率与统计设计(多方向/多轮累积、按目标功效反推样本数,Kim 2026 路线)——v0.1 不定,攒 journal 数据后再说。
- **v0.2 note 3**:治理道 STOP(operator 抽查发现)的证据标准——本次先不形式化,复用 hand-back §6 schema;若误触发/漏触发再收紧。

## 4. W 形态产出的初步草稿建议

- **verdict-only** → 关键句:"人肉盲测二值签字 gate 退役,T010/T011 改由机器可判最小验收三项解锁;operator 移位为抽查者+journal 校准;FAIL→STOP 双道保留;B8 采纳、B7 大部消解、B4 改写为新前置的机器闭环。"
- **decision-list** → 建议 4 列矩阵 rows:
  - 保留:FAIL→STOP 铁律(触发器改写)· O2 三击回溯(升级为验收机制)· 负控注入机制(降级校准)· prd-revision-trigger 通道 · journal/taste(O5/O7)
  - 调整:T010/T011 解锁前置(RERUN-PASS → 三项机器验收)· O4 初始层语义(盲测 smoke → 机器 smoke)· KG-B4(强制对象改写 + 要求代码级 wiring)· spec §5 重跑协议(改校准活动协议)
  - 删除:人肉盲测二值签字的解锁形态 · 签字模板-解锁耦合 · KG-B7 反作弊面的进一步投资(现状冻结)
  - 新增:trace schema 机器校验 · 证据可达性检查 · 轻量抽查记录通道 · journal 累积校准规则(使用期)
- **next-PRD** → 关键产品决策点:① O4 重写:初始层 = 机器最小验收(自动、秒级、阻断),长期层 = O2+O5 强化 + 抽查记录;② Open questions #3 重写(RERUN-PASS 唯一前置的表述废止);③ 明示「识伪校准活动」为可选使用期活动,入 journal。
- **refactor-plan** → 关键模块:① XenoDev spec §5/§6 + dependency-graph:T010/T011 前置重定义 + 机器道 STOP wiring(B4 改写的落点);② credibility/gate.py + injector.py:降级为校准工具(去签字/解锁路径,保留负控注入与叙事产出);③ 新增 trace-validator(三项验收的机器实现);④ journal/抽查记录的最小 schema。
