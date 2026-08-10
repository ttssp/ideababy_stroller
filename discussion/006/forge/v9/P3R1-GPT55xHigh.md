# Forge v9 · 006 · P3R1 · GPT55xHigh · 联合收敛 R1(标分歧)

**Timestamp**: 2026-08-10T18:05:08+08:00  
**Visibility**: 我已读双方 P1 + P2、对方 P3R1 与 moderator notes。  
**Searches in this round**: NONE。

## Moderator injection response

1. **覆盖面**：覆盖治理链。Phase 4 定稿时，forge 编排/合成 gate 应从 stage verdict 机器生成 `pending` obligation；XenoDev hand-off intake 消费授权条目，下一次 forge intake 消费回审条目，二者未取得权威终态不得完成。producer 只能提出 skip 理由；确定性豁免由预置 policy 签，例外由 operator/chair 签，不能由 producer 自批。
2. **归层**：三例皆证明 design gap 与 execution gap 并存，且 design gap 是共同上游。实例 1、3 没有持久 obligation 与消费 gate；实例 2 虽已决议、下发，仍因下游 gate 不要求清偿而蒸发，不能归咎“人没跟进”。
3. **自指处置**：支持 verdict 约束 forge 自身。v9 漏掉 v8 intake 义务，证明 build-only ledger 不成立；必须把“stage verdict→授权登记→下一 intake/落地清偿”纳入同一控制面。此结论也写入下文，避免 Phase 4 因不读 notes 再次丢失。

## 1. 整合摘要

四项缺口不是纯 execution gap。双方 P1 独立识别“证据不能决定自身是否应存在”；P2 的 in-toto layout、required checks 与 OPA 反证进一步确认：必须先由独立权威产生 obligation，再由强制入口消费；append-only、内容绑定只保护已有记录，不能生成缺失义务。moderator 的三例把范围从 build gate 扩到治理 gate，并证明完整 forge 流程走完仍可蒸发。

因此对方的 ledger 方向成立，但三态表述不够精确：`absent` 不是应写入的状态，而是到期 gate 对缺少权威终态的判定。最小状态应为 `pending / satisfied / skipped`；`satisfied` 绑当前内容身份，`skipped` 由 policy 或 operator/chair 签，到期仍 `pending` 即拒。ledger 必须由不可绕过的权威 gate 预建；若 producer 自建、自签 skip，P1 的攻击面原样返回。OPA 说明 decision point 不等于 enforcement point；SLSA 说明同信任域声明不能证明评审充分，故仍须逐入口接线并承认枚举完备性敞口。

## 2. 我的初步 verdict(草案)

**采一簇 `new` 的 obligation control plane，加 XD-41/XD-44 两条校准，并正式接手 `SHARED-CONTRACT:993`。**  
实装件保留 refactor，但 build 与 forge 治理链都须由权威 gate 预建义务、独立签终态、到期 fail-closed。  
`needs-attention` 不得放行；统一四轮改为风险/复杂度分档的有界 hard-stop；finding 类别重复判据 reject。  
这不是 final verdict；R2 须裁清 gate/签署权、已知入口和枚举敞口。

## 3. 关键分歧清单

- **分歧 1 · KG-B11 / XD-43 评级**
  - 我的立场：接受复合措辞“实装件 refactor + obligation 层 new”，总评级按 `new`。
  - 对方立场：“评级按最贵的部分记 `new`”。
  - R2 收敛：同意，且把治理 gate 纳入范围，不能只接 build 三入口。
- **分歧 2 · XD-41 评级与归簇**
  - 我的立场：`new`，并入 obligation 簇；补审债从创建即为 `pending`，不可靠标记自报。
  - 对方立场：“我让步到 `new`…要求并入簇①”。
  - R2 收敛：同意；另明确 fallback producer 无权签自己的 `skipped`。
- **分歧 3 · finding 类别重复信号**
  - 我的立场：**reject**，不是 defer；现有非结构化 finding 无可靠、可执法的等价判定。
  - 对方立场：“我主张从 defer 升级为 reject”。
  - R2 收敛：采 reject；未来若有新实证须作为新提案重开，不保留暗门。
- **分歧 4 · 被推翻地基是否具名**
  - 我的立场：要。verdict 应明写“纯 execution gap 被 SOTA 推翻”，design 与 execution 并存。
  - 对方立场：“要…写成‘原诊断错在哪’”。
  - R2 收敛：作为为何不能再改 SKILL 措辞的理由链，不悄悄换方案。
- **分歧 5 · XD-44 粒度 reframe 落点**
  - 我的立场：支持 reframe，但反对写未经验证的固定 `N`；本轮只留“单 task 含多个可独立评审的跨模块契约面→触发拆分复核”，不称唯一根因。
  - 对方立场：“单 task 同时定义 ≥N 个跨模块契约面 ⇒ 应拆”。
  - R2 收敛：去掉伪精确阈值，作为 task-decomposer 后续触发线，不展开 dev plan。
- **新增分歧 6 · ledger 状态与递归终点**
  - 我的立场：不用第四个业务终态；把 `absent` 改为 gate 派生结果，显式加入初态 `pending`。递归止于不可绕过的 canonical gate，而非 ledger 自证。
  - 对方立场：“三态 `satisfied` / `skipped` / `absent`”。
  - R2 收敛：裁定状态机、skip 签署权及 canonical build/forge gates；否则 ledger 本身仍会缺席。

## 4. 与 K 的对齐性自检

- **K1 enforcement** → ✅ `pending` 到期即拒，且消费 gate 不能绕过；不是建议。
- **K2 先判故障态** → ⚠ 已判 design+execution 并存，但 v0.7/v0.8 精确漏调入口仍未知；不得冒充已定位。
- **K3 该带而未带** → ✅ obligation 由权威 gate 预建；合法不适用走权威 `skipped`，不是全局“未带即拒”。
- **K4 不过度工程** → ✅ build、补审债、治理授权共用一控制面；逐入口接线是 OPA 反证后的必要成本。
- **K5 证据权重** → ✅ XD-41/XD-43 与治理三例定阻断机制；KG-B11 入同簇；XD-44 只采有实证的分档。
- **K6 回声室** → ⚠ 本结论没有因“无人反对”通过：三态、skip 签署权、递归终点均被独立攻击；粒度 reframe 明标事后接受。采用 `evidence_grade`：核心 obligation 抽象与 `:993` 接手=`independent`；纯 execution 地基被推翻、XD-44 reject=`SOTA-corrected`；复合评级、XD-41 并簇、粒度 reframe、moderator 后扩治理链=`post-hoc-accepted`。结论仍须 R2 对每项 addressed，不能把沉默当豁免。
- **硬约束 1** → ✅ 只经 forge 出可下发条目，不当场改 XenoDev。
- **硬约束 2** → ✅ mirror 落地须 IDS SSOT→cp mirror→更新 MANIFEST SHA。
- **硬约束 3** → ✅ 修改 §6 B-4-IDS 必须 bump `contract_version` + Changelog。
- **硬约束 4** → ✅ 不裁 KG-B8/B9/B10/B12/XD-42，也不借 moderator 扩裁其余 8 条。

**篇幅超标声明**：本文超过 600–1000 字；新增 moderator 三问、五项逐条表态、ledger 三项攻击面及 K 十项检查均为硬要求，继续压缩会丢失可裁条件。
