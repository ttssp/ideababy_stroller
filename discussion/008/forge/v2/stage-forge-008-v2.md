# Forge Stage · 008 · v2 · "Obsidian 作 US8 人读前端 + 库→vault 单向 exporter + C5 渠道中性边界"

**Generated**: 2026-06-16T11:00:00Z
**Source**: forge run v2 with X = 6 标的(IDS 3 + XenoDev 快照 3), Y = 产品价值 + 架构/数据流边界, Z = 不对标(法律层)· 产品价值层轻量对标, W = verdict-only + decision-list + next-PRD
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both) — 共 8 份 round file
**Searches run**: 16 across 产品价值层多源(Opus P2 三次:Obsidian 同步行为 / 库→vault 单向导出 SOTA / 知识库维护失败模式;Codex P2 十三次)— **零法律/ToS/DMCA 检索**(binding 禁止)
**Moderator injections honored**: none(本 v 无 moderator-notes.md)
**Convergence outcome**: converged(双方 P3R2 §2 各为单一 verdict 且同向;双方均显式标 "无 unresolved";Codex 末轮 Verdict 收敛到 CLEAN)

---

## How to read this

forge 是横切层(不是 L1-L4 pipeline 的一部分)。本文档是双专家(Opus 4.7 Max + GPT-5.5x High)
独立审阅 + 产品价值层 SOTA 对标 + 两轮联合收敛后的产出,**强制给出立场**(不是候选菜单 defer 给你拍板)。

读完后你应该:
- 知道双专家对「Obsidian 作 US8 实现方向 + v0.2 单向 exporter + C5 边界」的最终 verdict(单一 GO)
- 能用 §"Evidence map" 把每条结论逐条溯源到具体 round file 段落
- 拿到三件套产物:§"Verdict rationale"(浓缩立场展开)、§"Decision matrix"(保留/调整/删除/新增 全景)、§"Next-version PRD draft"(可直接回流改 PRD v0.2 + C5 的章节草案)
- 能基于 §"Decision menu" 直接进入下一步(改 PRD v0.2 → v0.2 立项 → XenoDev 拆 task / 跑 v3 / park / abandon)

> ⚠ **本 forge 审的是产品价值 + 数据流边界,不审工程可行性**(Y 未含工程量),也**不审 C5 法律合规性**(operator 已拍板并承担责任,binding)。GO 不等于「能在 C1 时间窗内建成」——那是 L4/XenoDev 才能回答的真风险。

## Verdict

**GO** · 把 **Obsidian 个人知识库前端定为 PRD US8(三形态统一时间线 + 回放已看/未看,长内容不消失进 backlog)的实现方向**,并在 **v0.2 scope 新增一条 bounded 能力:`SQLite 库 → Obsidian vault` 单向 exporter**(库→vault 衍生,vault 只读、不回写)。**SQLite 仍是唯一 SSOT**——v0.1 三护栏(allowlist 强校 / C7 不静默丢 / source_id 反作弊一致性)原样保留;**①替换 SSOT、③双向同步永久出局**。**C5 增补渠道中性原则**(operator 自用不传播:原内容不得进入会被传播/同步的衍生渠道,覆盖 git + iCloud/Obsidian Sync + 任何同步通道),**不溯及 v0.1 已 ship 采集落点**;vault 只放白名单 frontmatter + `raw_ref` 指针 + 摘要级 key_points/source_ref + 标的双链 + `reviewed`,**原文/完整转录/音视频/签名 URL 永久 OUT**。验收只依赖只读 frontmatter 消费(Bases/普通查询),**不依赖可写文件/联网脚本**(Dataview JS 不进合格线)。无 unresolved。

> **显式回应 K**:K#1(US8 价值 vs 过度工程)→ GO,双盲一致 + SOTA 双向印证,非过度工程;K#2(数据流护栏)→ ②单向 exporter 三护栏复用 v0.1 既有 + 新增 Dataview-JS 只读约束;K#3(C5 边界)→ 渠道中性原则 + 不溯及既有落点 + vault 只放指针摘要;K#4(v0.2 排序)→ exporter 是 bounded scope 不挤 US7,build 先后留 L4。

## Evidence map

| 结论 | 来源 | 引用(≤15 words) | 是否有反对证据 |
|---|---|---|---|
| US8 三要素天然映射 vault 能力(Calendar/reviewed/双链) | P1-Opus §1A | "US8 的统一时间线天然映射 Calendar 插件 + published_at" | - |
| Obsidian 作 US8 载体 = new(不是新开 scope,是选载体) | P1-GPT §2 / P1-Opus §2 | "现行 PRD 有 US8 目标但无载体" | - |
| 库→vault 单向导出是成熟 SOTA 形态 | P2-Opus §1 row1 | "SOTA 有零导出直挂 .db 与快照导出两条成熟路" | - |
| Omnivore 云端退场反证「本地 SSOT + 可重导出」更稳 | P2-GPT §1 row5 | "云服务 2024-11 后退成 self-hosted" | - |
| iCloud 同步整个 vault 目录、不读 .gitignore | P2-Opus §1 row2 | "iCloud 同步整个 vault 目录,不读 .gitignore" | - |
| C5「绝不入 git」措辞不够,须扩到传播/同步渠道 | P2-Opus §3 / P2-GPT §3 | "git-ignore 不等于不传播" | ⚠ 全局改 C5 可能误伤 v0.1 已 ship 落点(P1-Opus §3#2)→ 见 underweight |
| Readwise full-text export 是显式开关 → 原文必须显式禁 | P2-GPT §1 row2 | "full-text 开关证明必须显式禁止原文导出" | - |
| vault 放原文 = cut(永久 OUT) | P1-Opus §2 / P2-GPT §3 | "原文进 vault 会让 vault 从索引层变成内容存储层" | - |
| obsidian-importer #547 silent loss → exporter 须幂等 + drift 可检 | P2-Opus §1 row3 | "importer 有 #547 silent data loss,正撞 v0.1 C7" | - |
| Dataview JS 能写文件/联网 → 验收不依赖可写脚本 | P2-GPT §1 row3 / P3R1-Opus 分歧2 | "JS 查询有文件/网络能力风险" | (Opus P2 曾低估为 L4 细节,P3R2 §1 已收回) |
| C5 增补渠道中性原则 + 不溯及 v0.1 落点(折中) | P3R1-Opus 分歧1 / P3R1-GPT 分歧1 | "扩原则 + 不溯及既有落点" | - |
| exporter bounded scope 不挤掉 US7,build 先后留 L4 | P3R1-GPT 分歧3 / P3R2 双方 §3 | "不替代 US7" | - |
| SSOT 不漂(①③出局)是 binding 设计底线 | P1-Opus §1B / P1-GPT §2 + K binding | "②单向 exporter 是本轮 binding 底线" | - |

(上表 13 行,挑了最 load-bearing 的;其余次级结论散见各 round §1/§2。)

## Intake recap

### X · 审阅标的(6 个)
**IDS 本仓(可达):**
- `discussion/008/008-pB/PRD.md` v1.1 — 本仓库文件(US8:57 / Scope IN v0.2:70 / C5:133 / Phase-transition / UX principles:144)
- `discussion/008/handback/20260615T234706Z-008-pB-...md` — 本仓库文件(v0.1 T101-T112 ship、406 test 绿的事实依据)
- `discussion/008/forge/v1/stage-forge-008-v1.md` — stage 文档(C5 重定基线,v2 在其上推进)

**XenoDev 快照(已拷进 `_external/`,两审阅人读同一份):**
- `_external/XENODEV-006-obsidian-v0.2-scope-input.md` — 议题主源(exporter 6 要点 + 验收草案 + C5 待议 + 决策清单)
- `_external/XENODEV-005-obsidian-knowledge-store-research.md` — 调研报告(三姿势取舍 + v0.1 被冲击面 + C5 守法方案 + 落点判定)
- `_external/XENODEV-spec-008-pB.md` — XenoDev spec(v0.2 Outcomes 阈值待 learnings + frontmatter 字段映射)

### Y · 审阅视角
- ✅ **产品价值** — Obsidian 前端对 operator 是否真有用,US8 价值能否兑现
- ✅ **架构设计 / 数据流边界**(本轮特设)— ②号方案是否守得住 v0.1 三护栏,vault 放指针 vs 原文的边界
- ⚠ **binding**:C5 法律/合规定性沿用 v1,**非本轮审议对象**;只审产品/数据流层边界

### Z · 参照系
- mode: **不对标(法律层)**;产品价值层可轻量对标个人知识库 / 双链笔记类产品
- 用户外部材料:已快照的两份 XenoDev 文档(议题主源 006 + 调研 005)
- Phase 2 **不跑法律检索**(执行一致:双方 P2 零法律/ToS/DMCA 检索)

### W · 产出形态
- ✅ **verdict-only**(浓缩 verdict + 简短 rationale)
- ✅ **decision-list**(4 列矩阵:保留/调整/删除/新增)
- ✅ **next-PRD**(C5 边界重定 + v0.2 scope 增量的 PRD 章节草案,可回流改 PRD v0.2 部分)
- (交叉验证:下方三个 W-shape 章节齐整对应)

### K · 用户判准
核心问题:在「v0.1(图文+回放)已 ship」前提下,把 Obsidian 个人知识库前端定为 PRD US8 的实现方向、并在 v0.2 scope 增量「库→vault 单向 exporter」—— 这个产品决策该怎么定?同时 C5 措辞在「vault 可能被云同步」下的边界怎么画?

binding 前提(双专家必须接受):C5 法律合规由 operator 负责;v0.1 已 ship 是事实不重审;SSOT 不可漂(①替换/③双向已出局,②单向 exporter 是设计底线)。

operator 最在乎(产品价值 + 数据流层):① US8 价值能否兑现 vs 过度工程;② 数据流护栏守得住吗;③ C5 边界怎么画(vault 放指针 vs 原文 / 措辞要不要扩到云同步渠道);④ v0.2 该不该现在启动 + 与 US7 排序。

### 收敛模式
strong-converge —— 必须 finalize 单一 verdict,残余分歧降级为 v0.2 note。沿用 v1 收敛强度。

---

## §Verdict rationale(W 含 verdict-only)

GO 的论证沿三层展开,每层双盲一致且 SOTA 印证:

**产品价值层 —— 为什么是「选载体」而非「过度工程」**。PRD 标题本就是「采集 → 个人知识库」,US8 是已立项但未指定实现载体的 story(PRD:57)。提案实质 = 给 US8 选载体,不是新开 scope。US8 三要素逐一天然映射:统一时间线 → Calendar + `published_at`;已看/未看 → `reviewed` frontmatter 布尔;长内容不进 backlog → 双链反链聚合(标的 → 所有提它的采集)。真问题不在「能不能映射」而在「值不值得」——前两要素是 UI 便利(v0.1 SQLite 三维检索已交付 US5 的近似能力),第三要素(双链知识网)是 SQLite 给不了的**新认知价值**。Readwise / Logseq / Omnivore 三个参照共同证明「采集 → 本地知识图谱」是成熟产品形态,不是 008 独创负担(P2-GPT §1)。

**数据流层 —— 为什么 ②单向 exporter 守得住护栏**。研究报告已把设计空间收敛干净:①替换 SSOT 撞 v0.1 三护栏(Obsidian 原生无 schema 强校 / C7 不静默丢 / source_id 反作弊一致性)→ 出局;③双向同步是一致性地狱且最易破 C5 → 出局;②单向(库→vault,vault 只读衍生)是 binding 底线。三道护栏**全部复用 v0.1 既有机制**:vault 目录强制 git-ignored + 拒非 ignored 输出(复用 `_assert_c5_safe_out_dir`);frontmatter 只映射白名单字段(复用 allowlist);单向不回写(SSOT 唯一性自然保住)。Omnivore 云端退场反证「可重建的人读导出层」比把权威源交给 PKM 工具更稳(P2-GPT §1 row5)。**新增一条 Dataview-JS 只读约束**:查询层也必须只读,验收只要求 frontmatter 可被 Bases/普通查询消费,不依赖能写文件/联网的脚本(Opus P2 曾低估为 L4 细节,P3R2 §1 已显式收回为数据流护栏的一部分)。

**C5 边界层 —— v2 的真焦点,为什么「增补原则」而非「全局重写」**。双方 SOTA 双重坐实 git-ignore 不足以守 C5:iCloud 同步整个 vault 目录、不读 .gitignore(P2-Opus);Readwise full-text export 是成熟产品的显式开关,证明原文导出极易被当便利功能加回来、必须显式禁(P2-GPT)。故 vault 放原文 = cut(双方一致 + 证据加固)。改法上,P3R1 双方从 Opus 初版「双保险扩措辞」收敛到更精确的折中:C5 **增补**一条渠道中性原则(「增补」而非「重写」,避免误伤)+ **不溯及 v0.1 已 ship 落点**(其合规性 operator 已负责,PRD Phase-transition 提到落点含云/手机微信,全局收紧会反向误伤)+ vault 只放指针摘要。

## §Decision matrix(W 含 decision-list)

| 类别 | 项 | 来源(标的具体位置) | 理由 | 优先级 |
|---|---|---|---|---|
| **保留** | SQLite 唯一 SSOT + v0.1 三护栏(allowlist / C7 / source_id 反作弊) | PRD C7:135 + 研究报告 §2 | binding 设计底线;Obsidian 原生给不了这三条 | P0 |
| **保留** | v0.1 已 ship 采集落点(合规不重审 T101-T112) | PRD:82 + handback | operator 已负责合规;新约束只针对衍生导出层 | P0 |
| **保留** | C5 法律/合规定性由 operator 负责 | PRD C5:133 + v1 binding | 沿用 v1,非本轮审议对象 | P0 |
| **保留** | US7 盘中预警仍是 v0.2 scope | PRD:71 / US7:56 | exporter 不挤掉 US7,并列 v0.2 | P0 |
| **调整** | C5 增补渠道中性原则(自用不传播,覆盖 git + 云同步 + 任何传播渠道),不溯及既有落点 | PRD C5:133 / P3R2 双方 §2 | git-ignore≠不传播,iCloud 坐实;增补不重写避免误伤 | P0 |
| **调整** | US8 从抽象 story → 指定 Obsidian vault 载体 | PRD US8:57 | 缺的只是载体,Calendar/reviewed/双链落地 | P0 |
| **调整** | UX principle「不做 PKM 式双链/图谱」需复位 | PRD:144 | ⚠ 现行 UX 原则与 v0.2 双链方向直接冲突,改 PRD 时必须同步处理 | P0 |
| **调整** | exporter 验收增加 no-original-content + drift 可检 + 只读查询边界 | 研究报告 §4 / P2-Opus §1 row3 | 对齐 v0.1 C7,防 silent loss(importer #547 印证) | P1 |
| **删除** | vault 放图文原文/完整转录/音视频/签名 URL(永久 OUT) | P2-GPT §3 / P2-Opus §1 row2 | 走出本地自用边界,留 `raw_ref` 本地原文区 | P0 |
| **删除** | 依赖 Dataview JS(可写文件/联网)作验收合格线 | P2-GPT §1 row3 / P3R2 §1 | 查询层必须只读,不开新写路径/旁路 | P0 |
| **删除** | ①替换 SSOT / ③双向同步 / vault 回写库(防回潮) | K binding / 研究报告 §3 | 已判出局,仅记录防后续轮次回潮 | P0 |
| **新增** | v0.2 `库→vault` 单向 exporter(每条记录一个 `<source_id>.md` + frontmatter 白名单 + 标的双链 + `reviewed` + `published_at` 时间线) | 议题主源 §4 / P3R2 双方 §4 | US8 的具体实现载体;成熟 SOTA 形态 | P0 |
| **新增** | exporter C5 守卫(复用 `_assert_c5_safe_out_dir` + vault 强制 git-ignored) | 研究报告 §4 / P1-Opus §1B | 数据流护栏复用 v0.1 既有 | P0 |
| **新增** | 幂等 + drift 可检验收项(vault note 数 / source_id 集合 == 库记录) | P3R2 双方 §3 / P2-Opus §1 row3 | 对齐 C7「不静默丢」,exporter 可重跑 | P1 |

(每行可在 §"Evidence map" 或上述来源列溯源。)

## §Next-version PRD draft(W 含 next-PRD)

> **关键差别**:本草案不是整个 PRD 重写,而是**针对 PRD v0.2 部分 + C5 的增量修订**,内容来自 forge 已验证事实,**不 daydream**。回流方式见 §"Decision menu [A]"(直接改 `discussion/008/008-pB/PRD.md`,不 fork 新 branch)。

### 修订 1 · US8 实现方向锚定(改 §Core user stories / 新增 v0.2 实现说明)

US8 表项保持不变(PRD:57),在 Scope IN v0.2 下新增实现方向注释:
```
US8 实现载体(forge v2 verdict):Obsidian vault。
- 统一时间线 = Calendar/Bases 插件按 published_at 排布
- 回放已看/未看 = frontmatter `reviewed` 布尔字段
- 长内容不消失进 backlog = 标的双链 [[标的]] 反链聚合
SQLite 仍是唯一 SSOT;Obsidian 是人读衍生前端,不替换库。
```

### 修订 2 · C5 增补渠道中性原则(改 §Real-world constraints C5:133)

C5 措辞从「自用不传播,不规避他人访问控制」**增补**(非重写)为:
```
C5 ⭐ 只采 operator 有权访问的内容;可用有效登录态采集原内容(含须抓包取得的
图文/回放原文件)。**自用不传播 —— 原内容不得进入任何会被传播/同步的衍生渠道**
(含 git、iCloud/Obsidian Sync 及任何同步/传播通道)。合规边界由 operator 负责。

> 渠道中性原则(forge v2 增补):本约束不溯及 v0.1 已 ship 采集落点(其合规性 operator
> 已负责,不重审);新增约束只针对 vault 这类**衍生导出层**。原内容(图文全文 / 完整转录 /
> 视频音频 / 含签名 URL)永久留在本地 raw_ref 原文区,绝不进 vault。
```

### 修订 3 · UX principle 复位(改 §UX principles:144)

> ⚠ **必须同步处理**:现行 PRD:144「省心 > 功能丰富 ... 不做 PKM 式双链/图谱」与 v0.2 Obsidian 双链方向直接矛盾。改 PRD 时复位为:
```
- 省心 > 功能丰富:operator 介入次数趋近零是核心目标。v0.1 检索够用即可;
  v0.2 起以 Obsidian vault 提供双链/图谱(US8 载体),但作**人读衍生层**,
  不增加采集侧维护负担,SQLite 仍是唯一 SSOT。
```

### 修订 4 · Scope IN / OUT v0.2 增量(改 §Scope IN v0.2:70 + §Scope OUT)

```
## Scope IN — v0.2 增补(forge v2)
- Obsidian vault as US8 carrier:SQLite → vault 单向 exporter(vault 只读衍生,不回写)。
  - frontmatter 白名单字段 = source_id / published_at / form / capture_status /
    raw_ref / source_url_canonical / tickers / reviewed
  - body 仅摘要级 key_points / source_ref + 标的双链 [[标的]]
  - vault 目录强制 git-ignored,经 _assert_c5_safe_out_dir 守卫
  - bounded scope:不挤掉 US7;与 US7 盘中预警、完整 004 契约并列属 v0.2

## Scope OUT — v0.2 增补(forge v2)
- ❌ 原内容(图文全文 / 完整转录 / 视频音频 / 含签名 URL)进入 vault 或任何可能传播的衍生输出目录(对应 §Evidence map「vault 放原文 = cut」)
- ❌ 双向同步 / vault 回写库 / Obsidian 替换 SQLite SSOT(对应 K binding ①③出局)
- ❌ 依赖 Dataview JS 等可写文件/联网脚本作为验收必需路径(对应 §Evidence map「查询层只读」)
```

### 修订 5 · v0.2 验收 outcomes 增补(改 §Success v0.2 outcomes:119)

```
| O8 | exporter 导出后 vault 无正文字段、git check-ignore 命中 vault 路径 | 抽查 frontmatter 仅白名单字段;git check-ignore 命中 |
| O9 | 库记录 source_id 集合 == vault note 集合(幂等 + drift 可检,无 silent loss) | 重跑 exporter 对比集合;制造一次漏导确认可检出 |
| O10 | 可按日期/形态/标的/已看状态查询,且查询不依赖可写文件/联网脚本 | Bases/普通只读查询验证四维;确认无 Dataview JS 依赖 |
```

### Open questions(forge 也没解决的 → 见 §What this menu underweights)
- US7 vs US8 exporter 的 build 先后(forge 不定,L4 排)
- `key_points.text` / `source_ref` 子串的最大长度(摘要 vs 原文粒度线未量化)
- exporter 是否真降低 backlog 遗忘(US8 价值证否点,需 v0.2 运行验证)

---

## What this menu underweights(强制自批判)

诚实表述本 stage 文档可能 underweight 的点。这是质量栏,不能跳过。

- **回声室风险(convergence_mode 副作用)**:双专家都只读了**相同的快照标的**(`_external/` 三份 + IDS 三份),都接受同一 binding(C5 合规由 operator 负责 / SSOT 不漂 / ①③出局 / v0.1 不重审)。strong-converge + double-blind 在**同根因**(同一份调研报告 §3/§4 结论)上命中 → 「GO」置信高,但本质可能是两模型在同一前提上的回声室强化,而非独立验证。**双方都同意但可能错的判断**:US8 双链价值「值得投」整条链条上溯到 operator 尝鲜信号 + 同一份研究报告,无第三方独立数据源。

- **US8 价值无长期使用证据(真实证否点未被本 forge 覆盖)**:维护成本是 SOTA 坐实的真实失败模式(P2-Opus「neglected vault compounds friction」+ importer #547 silent loss),但目前**只有 operator 尝鲜的「值得投」用户信号,无长期使用证据**。US8 价值能否兑现、exporter 是否真降低 backlog 遗忘——本 forge 无法验证,只能落为 v0.2 运行后的证否点(O9/O10 验的是数据正确性,不是价值兑现)。

- **Y 视角未含工程量(verdict 的工程前提悬空)**:Y 仅含产品价值 + 数据流边界,**未做 exporter 工程量评估**——v0.1 回放管线已是 1-2h 大文件 + ASR + 摘要 + 稳定时间戳映射的重管线(PRD Biggest product risk:150),在其之上再加导出层的真实工作量,本 forge 没算。且**整个 verdict 的工程前提**:exporter 复用 `_assert_c5_safe_out_dir` 等机制是否真存在/真够用,是 L4 才能确认的;若 C5 合规前提 operator 判断有误,整个 verdict 连带失效。

- **「摘要 vs 原文」粒度线未量化(残余 v0.2 note 2)**:研究报告 §4 允许 `key_points.text` + `source_ref`(转录子串)进 vault,但 US3 要求关键点可溯源回原始转录 + 视频稳定时间戳——若 source_ref 子串足够长以满足溯源,它离「完整转录」有多远?**多长算摘要、多长滑向事实原文复制**,本 stage 未替 operator 定。这条边界粒度直接关系 C5(原文不进 vault)的有效性,是 exporter 验收细化时必须先定的判准(建议定 source_ref 最大长度 + 「可溯源但不可重建原文」判准)。

- **Y 视角覆盖盲区(轻提,非主章节)**:Y 未含「插件生态维护风险」独立审议——Dataview 原作者已退场(研究报告 §1 注)、Obsidian 无内建 export pipeline(P2-Opus §1 row3),verdict 用「选 Bases 原生而非 Dataview 社区 + exporter 自维护」兜住,但插件生态长期可用性是 v0.2 运行后才暴露的 attention 点。

- **forge versioning 提示**:以下新信息进入会触发 v3 跑、改变本 verdict——① v0.2 运行后 US8 价值证否(vault 被 neglect、exporter 没降低 backlog 遗忘);② operator 重估 C5 合规前提(整个 verdict 的 binding 基石松动);③ 工程量评估发现 exporter 在 C2 时间窗内不可行(需重排 v0.2 scope);④ source_ref 粒度线定不下来导致 C5 原文边界失守。

## Decision menu(for human)

### [A] 接受 verdict → 改现行 PRD v0.2 + C5(不 fork 新 PRD branch)
```
⚠ 本 verdict 产出回流的是**改现行 PRD(discussion/008/008-pB/PRD.md)的 v0.2 部分 + C5**,
   不是 fork 新 PRD branch —— 008-pB 早过 L3,PRD 已 frozen 在 v1.1。
⚠ SHARED-CONTRACT 决策矩阵:`/scope-inject` 不对口(那是 hand-back → handback-review
   路径,改未 frozen PRD)。正确入口 = 直接改 PRD v0.2 章节,**像 v1.1 那样 forge verdict
   驱动修订**(PRD:16 v1.1 修订块即先例)。

流程:
1. operator 手工把本 stage §"Next-version PRD draft" 的 5 处修订落进
   discussion/008/008-pB/PRD.md:
   - 修订 1 → US8 实现方向注释(Scope IN v0.2 下)
   - 修订 2 → C5:133 增补渠道中性原则
   - 修订 3 → ⚠ UX principle:144 复位(必须同步,否则 PRD 自相矛盾)
   - 修订 4 → Scope IN/OUT v0.2 增补
   - 修订 5 → v0.2 outcomes O8/O9/O10
2. PRD 版本号 1.1 → 1.2,Last revised 注「forge v2 verdict 驱动修订 · human-approved」
3. v0.2 立项(operator 显式决定 ship v0.1 → 启动 v0.2 build)
4. 新开 XenoDev session 拆 task(L4 build runtime,per SHARED-CONTRACT §6):
   cd /Users/admin/codes/XenoDev && claude
```

### [B] 跑 forge v3(说明需要补什么)
```
/expert-forge 008
# 在 Phase 0 intake 调整 X / Y / Z / W / K
# 旧 v2 整目录保留作历史参考
```
适用:① 要把工程量纳入 Y(评估 exporter 在 v0.2 时间窗内可行性);② source_ref 粒度线需专门论证;③ v0.2 运行后 US8 价值证否触发重审。

### [C] 局部接受
- ✅ 采纳(verdict 主干):US8=Obsidian 载体 + ②单向 exporter + SSOT 不漂 + ①③出局
- ⏸ 挂起(等条件):C5 措辞具体落字(等 operator 确认渠道中性原则表述);UX principle:144 复位(等确认与 v0.1 落点无冲突);source_ref 粒度线(等 exporter 验收细化)
- ❌ 拒绝:本 stage 无明确建议拒绝项(双方收敛,无 unresolved)

### [P] Park
```
/park 008
```
保留所有 forge v2 产物,标记暂停。复活时不重做本层。

### [Z] Abandon
```
/abandon 008
```
仅当 verdict 显示 008 不该继续——本 verdict 是 GO,**不建议** abandon。

---

## Forge log
(由 /expert-forge 命令更新;记录每次 forge run 的 v 序列 + 关键 verdict 一句话)

- v2: 2026-06-16 — verdict: "GO · Obsidian 作 US8 人读前端入 v0.2 + 库→vault 单向 exporter · SQLite 唯一 SSOT 不漂 · C5 增补渠道中性原则(不溯及 v0.1 落点) · vault 只放指针+摘要原文永久 OUT · 验收=幂等+drift 可检+只读查询"
- v1: 2026-06-05 — verdict: "refactor-and-reset · C5 重定基线(有效登录态采集原内容 / 合规由 operator 负责) · 回放 scope 复位留 v0.1 · token 阈值升为显式 outcome"
