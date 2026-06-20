# 调研 · 用 Obsidian 存「采集到的知识」可行性 + 对 008-pB 的冲击分析

> **性质**:纯调研报告(只读 · 不改代码 · 不动框架 · 不写 IDS)。给 operator 决策用。
> **日期**:2026-06-16 · **触发**:operator「小程序图文/回放能下载,怎么存这些知识?调研下 Obsidian」
> **结论先**:见 §0。

---

## §0 结论(先看这段)

**一句话**:Obsidian **不是** SQLite 的替代,而是**另一层**——它该当「人读的知识库前端 / 第二大脑」,坐在 v0.1 SQLite(机器查的 SSOT)**之上**,不是替换它。最稳的姿势是 **②「SQLite 仍是 SSOT,Obsidian 当衍生视图」**。

**三件必须先想清楚的事**:

1. **「存知识」是两个问题,别混**:
   - **原内容**(图文原文 / 回放视频 / 音频 / 转录 / 含签名 URL)→ **C5 铁律死管**:自用不传播、**绝不入 git**。Obsidian vault 存它们**技术上行,但 vault 必须像 `out/004-feed` 一样 git-ignored**,否则 C5 破。**当前 `.gitignore` 没有任何 vault 路径被忽略 —— 这是落地前的硬前提缺口(见 §4)**。
   - **提炼出的结构化知识**(004 记录 / 标的 / 关键点 / 缺口)→ 这才是 v0.1 已做的;Obsidian 在这层是「另一种前端/存储形态」候选。

2. **Obsidian 的数据模型 = 「一条记录 = 一个 .md 文件 + YAML frontmatter」**,用 **Bases**(1.9 起原生,5 万 note 仍秒级)或 **Dataview**(社区插件,SQL-like,只读)查。它**没有 schema 强制**(C7「不静默丢」/ allowlist「拒建议字段」这些 v0.1 的硬约束,Obsidian 原生**给不了**)。

3. **落点判定**:这件事**不是** v0.1 的 bug 修复(A),大概率是 **v0.2 新 scope(B)**(「采集→自动生成知识笔记 + 人读知识库」是新能力)。要做 → 先调研(本报告)→ 回 IDS 补 spec / 可能 scope-inject(C)。**不在 XenoDev 当场起新功能**(需 plan mode 出方案 + operator 批准,你的全局铁律)。

---

## §1 Obsidian 是什么(就这件事相关的部分)

| 维度 | 事实 | 来源 |
|---|---|---|
| 本质 | 本地优先,所有 note = 设备上的纯 **Markdown** 文件;离线工作;无服务器、无厂商锁定 | Lindy / codeculture |
| 结构化数据载体 | **YAML frontmatter**(note properties);「一个 note = 一条记录,frontmatter 字段 = 列」 | practicalpkm |
| **Bases**(原生) | 1.9.0(2025-05)起的**核心插件**,电子表格式界面查 frontmatter,**5 万+ note 近乎瞬时渲染**,单 Base 多视图,学习曲线缓;数据存 `.md` 的 YAML + 新 `.base` 文件 | alternativeto / practicalpkm |
| **Dataview**(社区) | SQL-like DQL(`TABLE ... FROM #tag WHERE ...`)或 JS API,把 frontmatter + inline 字段当库查;**只读**;原作者 2023 退场(维护风险) | codeculture / community |
| 双链 / tag | `[[标的]]` 双链 + `#tag`;标的天然可做双链节点(一个标的一页,反链聚合它出现在哪些采集) | datasciencedojo |
| 其他可用插件 | Templater(笔记模板,定义「采集笔记」note 类型)、Calendar(按天导航,对 O1「那天发了什么」直接契合)、Smart Connections(语义相关发现) | aiproductivity / obsibrain |
| **反向**:Obsidian 里塞 SQLite | 有 `SQLite DB Viewer` 等插件(WASM SQLite),能在 vault 内直接查 `.db` —— 即**不导出也能让 v0.1 的库在 Obsidian 里被看** | community plugins |

**关键认知**:Obsidian 的「数据库感」来自**插件查 frontmatter**,不是它本身是数据库。它**没有** `additionalProperties:false`、没有 enum 强校、没有 RFC3339 时区强校、没有「脏记录 raise」——**v0.1 的所有 allowlist / C7 / C5-pointer 硬约束,Obsidian 原生一个都不提供**。

---

## §2 v0.1 现状(被冲击的面)

读了 `src/store/db/store.py` + 两个 schema + `.gitignore`,事实如下:

- **SSOT 是 SQLite**:`records` 主表(`source_id` 主键)+ `record_tickers` 关联表 + 三索引(pub_date / form / ticker)。
- **C5 在库层已钉死**:库 schema **只存 `raw_ref` 指针,零正文列**(`test_should_store_only_pointer_not_content` 钉);库本身可入 git。
- **入库门 = T103 `validate_record`**:脏记录(缺字段/未知字段/坏时戳/带正文)`raise ValueError`,不静默入库。批量 `ingest_records` 用 `with conn:` 原子事务(任一条坏→整批回滚)。
- **检索三维**:`query(date, form, ticker)` 走索引,无匹配返空 list。
- **缺口可见(T108)**:`build_gap_report` 依赖库里记录做节奏统计(count gaps / status gaps / undated / no_data)。
- **004 输出(T110/T111)**:`raw_content`(article)/ `transcript_ref`(replay)+ `key_points[source_ref]` 过 `004-schema.json` allowlist;**拒任何建议字段**(O5)。
- **三方一致反作弊(verify-ppv-p2/p3)**:`source_id` 在「采集记录 == manifest == 输出」逐字相等(故 `source_id` **不加 form 前缀**)。

**冲击点**:Obsidian 若进来,**不能碰** ① C5-pointer 库 schema ② validate_record 入库门 ③ source_id 逐字一致(反作弊)。Obsidian 笔记里**可以**冗余展示这些,但**SSOT 不能从 SQLite 漂到 vault**(否则反作弊/缺口统计的权威源就乱了)。

---

## §3 三种集成姿势(取舍)

### ① Obsidian 当**最终知识库**(替换 SQLite 当 SSOT)
- 形态:每条采集记录 → 一个 `.md`,frontmatter 放 `source_id/published_at/form/tickers/capture_status/raw_ref`;body 放 `key_points`;标的用 `[[双链]]`;Bases/Dataview 查。
- **取舍**:✅ 人读极好、双链/图谱/语义发现是 SQLite 给不了的;❌❌ **直接撞 v0.1 三条硬约束**——没有 allowlist 强校(建议字段混进 frontmatter 没人拦)、没有 C7「不静默丢」(坏记录变一个坏 md 文件,缺口统计要重写)、`source_id` 反作弊一致性失去权威源。**不推荐**:等于把 v0.1 的护栏全拆了重做。

### ② SQLite 仍是 **SSOT**,Obsidian 当**衍生视图**(导出/同步)— **推荐**
- 形态:v0.1 的库**不动**,加一个**单向 exporter**:`库 → vault/*.md`(frontmatter 由记录字段映射,标的→双链)。Obsidian 只读这些衍生 md。**原内容仍只在本地 `raw_ref` 指的地方,vault 里只放指针/摘要,vault git-ignored**。
- **取舍**:✅ v0.1 所有护栏原样保留(SSOT 不动、反作弊不动、C5-pointer 不动);✅ 人得到 Obsidian 的全部前端好处;✅ 冲击面小(新增一个导出器,不改既有模块);❌ 双向编辑没了(vault 改了不回写库)——但对「看知识」场景这恰恰是优点(SSOT 唯一)。
- **C5 守法**:exporter 必须像 `write_004_package` 一样,**vault 目录强制 git-ignored + 拒非 ignored 输出路径**(复用 `_assert_c5_safe_out_dir` 同款守卫)。

### ③ 完全替换 / 双向同步
- 形态:vault 当唯一源,反向同步回库。
- **取舍**:❌ 最重、最易破 C5 与反作弊,双向同步是经典一致性地狱。**不推荐**。

**另一条轻量路**(可叠加在②上):**Obsidian 里直接挂 v0.1 的 `.db`**(SQLite DB Viewer 类插件,WASM),**零导出**就能在 vault 里查库。代价:看到的是表不是双链笔记,失去 Obsidian 的知识网优势,但实现成本几乎为零、绝不破 SSOT。可作为「先尝鲜」步。

---

## §4 C5 红线在 Obsidian 下怎么守(落地前硬前提)

> **这是最关键、且当前缺的一块。**

1. **vault 路径必须 git-ignored**:当前 `.gitignore` 只忽略 `out/` + 探针/worktree 路径,**没有任何 vault 路径**。任何 vault 落地**前**,必须先把 vault 根加进 `.gitignore`(像 `out/004-feed`)。否则原内容/含签名 URL 的笔记会**直接入 git history = C5 破**。
2. **vault 里能放什么 / 不能放什么**:
   - ✅ 能进 vault md:`source_id` / `published_at` / `form` / `tickers` / `capture_status` / `key_points.text` / `source_ref`(转录子串,溯源用)/ 缺口报告。
   - ❌ **绝不进 vault md(即便 vault 自身 ignored,也建议物理隔离)**:图文**原文全文** / 回放**视频音频** / **完整转录** / **含签名 URL**。这些留在 `raw_ref` 指的本地原文区,vault 只放**指针 + 摘要**。
   - 理由:vault ignored 只挡 git;但 vault 可能被同步(iCloud/Obsidian Sync)——原内容进 vault = 走出「本地自用」边界,**这触及 C5 措辞本身,要回 IDS 确认**(D 类,见 §5)。
3. **exporter 守卫复用 v0.1 既有**:`_assert_c5_safe_out_dir`(走到最近存在祖先再 `git check-ignore`,rc==1 raise)+ allowlist 字段映射(只导出白名单字段,杜绝把正文字段冗余进 frontmatter)。

---

## §5 落点判定:这件事走哪条流程(回到 A–E 决策表)

| 子需求 | 落在哪层 | 走哪条 |
|---|---|---|
| **只是了解 Obsidian 值不值得用** | 纯调研 | ✅ **本报告即交付**,零风险 |
| **②号方案:加一个 库→vault exporter** | 008-pB **新功能**(v0.1 已 ship,这是新增能力,非修 bug) | **B(v0.2 新 scope)**:回 IDS 补 spec → task-decompose → XenoDev build(plan mode 先出方案) |
| **「采集→自动生成知识笔记 + 人读库」当产品能力** | v0.2 新 scope | **B**:作为 v0.2 re-decompose 的输入候选 |
| **原内容是否允许进(同步的)vault** | 触及 **C5 措辞 / 本地自用边界** | **C/D**:回 IDS `/handback-review 008` 或 forge 确认 C5 在「vault 同步」下的边界,**不在 XenoDev 自行判定** |
| **若暴露「v0.1 存储形态硬编码 SQLite、不该锁死」** | 框架层(存储后端可插拔) | **D**:记 `dogfood-backlog.md` → 攒批回 IDS forge(**别当场改**) |

**强约束提醒**:
- 「加 exporter」「采集→笔记」都是**新功能** → **必须 plan mode 先出方案,operator 批准后才动**(你的全局铁律)。本报告**不**自动起任何 build。
- 原内容入 vault 触及 C5 → **不在 XenoDev 当场判定**,回 IDS 治理。

---

## §6 推荐路线(若 operator 决定要做)

1. **先尝鲜(零成本,可现在)**:Obsidian 装 SQLite Viewer 类插件,直接挂 v0.1 的 `.db` 看效果。判断「Obsidian 的前端到底香不香」**再决定要不要投** exporter。
2. **若要正式做** → 走 **②号方案**,作为 **v0.2 一个 task** 提:
   - spec 增量(回 IDS):`库 → vault` 单向 exporter;frontmatter = 白名单字段映射;标的→双链;vault 强制 git-ignored;C5 守卫复用 `_assert_c5_safe_out_dir`;**原内容不进 vault(只指针+摘要)**。
   - 验收:导出后 vault md 过「无正文字段」检查;`git check-ignore` vault 命中;Dataview/Bases 能按天/标的/形态查出(对齐 O1)。
3. **C5 边界**(原内容 vs 同步 vault)→ **回 IDS 确认**后再定 vault 放什么,**先按「只放指针+摘要」最严档走**。

---

## §7 dogfood / forge 候选(本调研顺带发现 · 待记/待议,非本报告改)

- **(可能 D 类)v0.1 存储后端硬编码 SQLite**:若未来要支持 vault / 其他后端,「存储形态」该不该抽象成可插拔接口?——属框架层,若 operator 认同则记 `dogfood-backlog.md` 回 forge。**本报告不擅自记**(等 operator 确认这是不是真痛点)。
- **(C 类)C5 措辞未覆盖「vault 同步」场景**:现行 C5 说「绝不入 git」,但没说「绝不进会被云同步的目录」。Obsidian 暴露了这个边界模糊 —— 回 IDS 厘清 C5 在「git 之外的传播渠道」的口径。

---

## 来源

- [Obsidian Review 2026 — Lindy](https://www.lindy.ai/blog/obsidian-review)
- [Obsidian AI Knowledge Base in 9 Steps — Data Science Dojo](https://datasciencedojo.com/blog/obsidian-ai-knowledge-base/)
- [Obsidian Plugins Productivity Guide 2026](https://aiproductivity.ai/blog/obsidian-plugins-productivity/)
- [Top Obsidian Plugins in 2026 — Obsibrain](https://www.obsibrain.com/blog/top-obsidian-plugins-in-2026-the-essential-list-for-power-users)
- [Why Developers Are Using Obsidian as a Database — Code Culture](https://codeculture.store/blogs/developer-culture/obsidian-dataview-plugin-developer)
- [Moving to Obsidian Bases from Dataview — Practical PKM](https://practicalpkm.com/moving-to-obsidian-bases-from-dataview/)
- [Obsidian 1.9.0 introduces Bases plugin — AlternativeTo](https://alternativeto.net/news/2025/5/obsidian-1-9-0-introduces-bases-plugin-for-database-style-note-management)
- [Dataview — Obsidian Community Plugins](https://community.obsidian.md/plugins/dataview)
