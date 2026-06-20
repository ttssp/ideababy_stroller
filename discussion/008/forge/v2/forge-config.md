---
forge_version: v2
created: 2026-06-16T08:36:44Z
convergence_mode: strong-converge
x_hash: d987d4d0d726dca3cadbb0b08bcc56b4
prefill_source: manual
---

# Forge Config · 008 · v2

## X · 审阅标的

本轮 forge 由 operator 触发,议题源 = XenoDev 跨仓输入包 `projects/008-pB/probe/006-obsidian-v0.2-scope-input.md`(已快照进本 forge 目录 `_external/`)。

**议题三件套**(供双专家定位 v0.2 scope 增量 + C5 边界):
1. **v0.2 scope 增量**:把「库 → Obsidian vault 单向 exporter」(研究报告②号方案)定为 PRD **US8「三形态统一时间线 + 回放已看/未看」的具体实现方向**,作 v0.2 新增能力。SQLite 仍是唯一 SSOT,Obsidian 当人读前端(双链/图谱/Bases),不替换库。
2. **C5 边界扩展**:现行 C5(PRD:133)只钉「绝不入 git」,但没说「绝不进会被云同步的目录」。Obsidian vault 常挂 iCloud / Obsidian Sync → 原内容若进 vault 可能被同步传播,**走出「本地自用」边界**。是否要把 C5 措辞从「绝不入 git」扩展为「绝不进任何会被传播/云同步的渠道」?这影响 vault 到底能放什么(指针+摘要 vs 原文)。
3. **v0.2 启动 + US8 实现方向锚定**。

> ⚠ **跨仓快照说明**:议题源 + 调研报告 + spec 三个标的物理上在 XenoDev 仓(`/Users/admin/codes/XenoDev/...`),Codex 沙箱大概率不可达。故 operator 决议把三者**快照进 `discussion/008/forge/v2/_external/`**,两位审阅人读同一份本仓内容,避免沙箱 BLOCK。快照保真(`cp` 原文),保留 audit trail。

### 解析后的标的清单

**IDS 本仓(✅ 可达):**
- `discussion/008/008-pB/PRD.md` —— 现行 PRD v1.1(US8:57 / Scope IN v0.2:70 / v0.1 OUT:86 / C5:133 / Phase transition learning)。类型:本仓库文件。
- `discussion/008/handback/20260615T234706Z-008-pB-20260615T234706Z.md` —— v0.1(T101-T112)集成 ship 的 hand-back 包,406 test 全绿,v0.1 已 code-complete 的事实依据。类型:本仓库文件。
- `discussion/008/forge/v1/stage-forge-008-v1.md` —— forge v1 verdict(refactor-and-reset,C5 重定基线),v2 在其结论之上推进。类型:stage 文档。

**XenoDev 快照(✅ 可达 · 已拷进 `_external/`):**
- `_external/XENODEV-006-obsidian-v0.2-scope-input.md` —— **议题主源**。§0 一句话提案 / §4 v0.2 scope 增量(exporter 设计 6 要点 + 验收草案) / §6 C5 边界待议点 / §7 待 operator 决策清单。
- `_external/XENODEV-005-obsidian-knowledge-store-research.md` —— 调研报告。§0 三种集成姿势(①替换②衍生③双向,推荐②) / §2 v0.1 现状被冲击面(C5-pointer 库 schema / validate_record 门 / source_id 反作弊一致性) / §4 C5 红线在 Obsidian 下怎么守 / §5 落点判定 A-E。
- `_external/XENODEV-spec-008-pB.md` —— XenoDev spec(§1.2 v0.2 Outcomes 阈值待 v0.1 learnings:180 / §2.1 v0.2 in-scope:207),exporter frontmatter 字段映射与 004 契约对齐点。

## Y · 审阅视角

✅ **产品价值** —— Obsidian 知识库前端对 operator(真实用户)是不是真有用?US8 的价值能否被 vault 双链/图谱/Bases 兑现?
✅ **架构设计 / 数据流边界**(本轮特设)—— ②号方案「单向 exporter + SSOT 不漂」的数据流是否守得住 v0.1 三条护栏(allowlist 强校 / C7 不静默丢 / source_id 反作弊一致性)?vault 放指针+摘要 vs 放原文的数据流边界怎么画?

> ⚠ **operator 显式姿态(binding · 见 K)**:**C5 的法律/合规定性沿用 v1 binding —— 不是本轮 forge 的审议对象**。本轮审 C5 只审**产品/数据流层**:即「vault 该放指针还是原文 / C5 措辞该不该扩到云同步渠道」这个**边界怎么画**的问题。双专家**不得**论证「云同步是否违法 / 是否踩平台 ToS / DMCA§1201」—— 那些 operator 已拍板并承担责任。把「合规由 operator 负责」当**已决前提**输入。

## Z · 参照系

mode: 不对标(法律层)；产品价值层可轻量对标

> Phase 2 **不跑法律检索**(合规由 operator 负责,非 forge 审议对象)。双专家在产品价值层**可**轻量对标个人知识库 / 双链笔记类产品(Obsidian Bases/Dataview、Readwise、Logseq 等「采集→知识沉淀」形态),判断 ②号方案的产品价值定位,但**不强制**、**不得跑法律判例检索**。研究报告 §1 已含 Obsidian 能力事实表 + 来源,可直接引用,无需重复检索。

## W · 产出形态

✅ **verdict-only** —— 浓缩 verdict + 简短 rationale(≤500 字):US8 实现方向 = Obsidian 的 go/no-go + ②单向 exporter 该不该做 + C5 措辞决议方向,一段话给立场不 hedge。
✅ **decision-list** —— 4 列矩阵(保留 / 调整 / 删除 / 新增),把本轮所有可决项理清:聚焦 US8 实现方向、②exporter scope 增量、C5 措辞、vault 放原文 vs 指针、v0.2 启动排序等,每项落到 keep/refactor/cut/new 一格。
✅ **next-PRD** —— C5 边界重定 + v0.2 scope 增量(US8 实现方向 = Obsidian exporter)的 **PRD v0.2 章节草案**,可直接回流改 `discussion/008/008-pB/PRD.md` 的 v0.2 部分。

> **W 三件套**(2026-06-16 operator 调整:原单一 next-PRD → verdict-only + decision-list + next-PRD)。三者职责互补:verdict-only 给浓缩立场、decision-list 给可决项全景矩阵、next-PRD 给可直接回流的草案。本轮目标仍是「正式论证写进 PRD v0.2 章节」,next-PRD 是落地产物;verdict-only + decision-list 是它的浓缩与结构化前置,便于 operator 快速决议。
>
> **next-PRD 草案须覆盖**:① US8 实现方向锚定(Obsidian vault as US8 载体);② v0.2 Scope IN 增量(库→vault 单向 exporter + frontmatter 白名单映射 + 标的双链 + reviewed 字段 + Calendar 时间线);③ C5 措辞决议(扩到云同步渠道 / vault 只放指针+摘要的最严档,或保持现状 + 显式标注);④ v0.2 Scope OUT(原内容绝不进 vault / 不双向同步 / 不替换 SSOT);⑤ 验收 outcomes(无正文字段检查 / git check-ignore 命中 / Dataview 按天·标的·形态可查 / 双链反链聚合正确)。

## K · 用户判准

**核心问题**:在「v0.1(图文+回放)已 ship」的前提下,把 **Obsidian 个人知识库前端**定为 PRD **US8 的实现方向**、并在 v0.2 scope 增量「库→vault 单向 exporter」—— 这个产品决策该怎么定?同时,**C5 措辞在「vault 可能被云同步」下的边界怎么画**?

**binding 前提(双专家必须接受,不得审议):**
- **C5 的法律/合规定性由 operator 负责**(沿用 forge v1)。新 C5 = operator 作为付费订阅用户,用有效登录态抓自己合法请求返回的内容(图文/回放原文件)直接留存,自用不传播。这**不是**复用过期 token 规避访问控制。operator 已就此合规性拍板并承担法律责任。
- 因此本轮审 §6 的 C5 扩展问题,**只审产品/数据流层**(vault 放什么 / 措辞要不要扩到云同步渠道),**不审**「云同步是否违法 / 是否踩 ToS」。后者是已决前提。
- **v0.1 已 ship 是事实**(T101-T112 已 merge,406 test 全绿,hand-back 已在 IDS 决议=收悉入库)。本轮**不**重审 v0.1 已交付的实现。
- **SSOT 不可漂**:研究报告 §2 已确认 Obsidian 原生**给不了** v0.1 三条硬约束(allowlist 强校 / C7 不静默丢 / source_id 反作弊一致性)。故任何方案都**不得**把 SSOT 从 SQLite 漂到 vault —— ②号方案(单向 exporter,vault 只读衍生)是 binding 的设计底线,①替换/③双向同步已被研究报告判出局,**不在本轮重新论证**。

**operator 最在乎的(产品价值 + 数据流层,这才是双专家该审的):**
1. **US8 价值能否兑现** —— Obsidian 的双链/图谱/Bases/Calendar 是否真能交付 US8「三形态统一时间线 + 回放已看/未看,长内容不消失进 backlog」的价值?还是过度工程(v0.1 SQLite 检索其实已够)?这是纯产品价值判断。
2. **数据流护栏守得住吗** —— ②号方案「单向 exporter + vault git-ignored + 复用 `_assert_c5_safe_out_dir`」能否在不破 v0.1 三条护栏的前提下,把 v0.1 库导成人读 vault?frontmatter 白名单映射 + 标的双链的具体边界。
3. **C5 边界怎么画** —— vault 只放「指针(raw_ref)+ 摘要(key_points.text/source_ref)」、原内容(图文原文/回放视频音频/完整转录/含签名 URL)**绝不进 vault**(研究报告 §4 最严档建议)—— 这个边界够不够?C5 措辞要不要从「绝不入 git」扩展为「绝不进任何会被传播/云同步的渠道」?这是 PRD 措辞级决策。
4. **v0.2 该不该现在启动** —— Obsidian exporter 作为 v0.2 的一条 scope,与 v0.2 既有锚点(US7 盘中预警 / 完整 004 契约)的优先级关系。

## 收敛模式

strong-converge —— 必须 finalize 单一 verdict(US8 实现方向 go/no-go + C5 措辞决议 + v0.2 scope 增量草案)。残余分歧降级为 v0.2 note。沿用 v1 收敛强度。
