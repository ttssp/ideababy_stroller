# Forge v2 · 008 · P2 · Opus 4.7 Max · 参照系评估(with search)

**Timestamp**: 2026-06-16T09:05:00Z
**Searches run**: 3,产品价值层 SOTA-benchmark(Obsidian 同步行为 / 库→vault 单向导出 SOTA / 个人知识库维护失败模式)。**未跑任何法律/ToS 检索**(binding 禁止)。
**Visibility**: 我已读对方 P1(P1-GPT55xHigh.md)。

## 1. SOTA 对标(产品价值 + 数据流层)

| 标的 X' | 参照项 | 它怎么做 | 我们(008 ②号方案)怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| 库→vault 单向导出 | Obsidian SQLite Explorer / SQLite DB Viewer 插件 | WASM SQLite 直挂 `.db`,read-only SQL runner + **static snapshot embedding**(把 live query 冻成某时点 md 表) | exporter 把库导成 `<source_id>.md` + frontmatter + 双链 | SOTA 有「零导出直挂 .db」与「快照导出」两条成熟路;②号是后者。**gap**:我们多了 C5 守卫(vault git-ignored + 原文隔离),SOTA 插件无此约束 | [SQLite Explorer](https://www.obsidianstats.com/plugins/sqlite-explorer) / [SQLite DB Viewer](https://community.obsidian.md/plugins/sqlite-db-viewer) |
| vault 云同步边界 | iCloud Drive 同步 vault | **iCloud 同步整个 vault 目录,不读 .gitignore** | 我们靠 vault git-ignored 挡 git | **gap = 致命确认**:git-ignore 挡不住 iCloud。原文进 vault 即便 ignored 仍会被 iCloud 传播 → C5「绝不入 git」措辞确实不够 | [Obsidian Sync help](https://obsidian.md/help/sync-notes) / [Obsidian-iCloud](https://github.com/mnott/Obsidian-iCloud) |
| 采集→笔记 pipeline | Obsidian importer / Zotero-Obsidian / Anki pipeline | 社区插件做导入;质量参差、维护状态不一 | 自建单向 exporter | **gap**:Obsidian **无内建 export pipeline**,全靠自维护;importer 有 [#547「silent data loss」](https://github.com/obsidianmd/obsidian-importer/issues/547) —— 正撞 v0.1 C7「不静默丢」。我们的 exporter 必须幂等 + drift 可检 | [Exporting guide](https://unmarkdown.com/blog/complete-guide-exporting-obsidian) |

## 2. 用户外部材料消化

K 中的外部材料 = 已快照进 `_external/` 的两份 XenoDev 文档(议题主源 006 + 调研 005),P1 已消化,P2 复核其结论是否被 SOTA 站住/推翻:

- **材料 1 · 调研 005 §4「C5 红线在 Obsidian 下怎么守」**
  - 可吸收 → 「vault ignored 只挡 git,vault 可能被 iCloud/Obsidian Sync 同步,原内容进 vault = 走出本地自用」**被 SOTA 独立坐实**(iCloud 不读 .gitignore)。这从「报告的断言」升级为「外部证据」。
  - 会改方向 → 强化:原文物理隔离不是「保守建议」,是**硬前提**。`.gitignore` 加 vault 路径**不足以**守 C5;exporter 必须从源头只写白名单字段 + 指针。
  - 噪音 → 无。
- **材料 2 · 调研 005 §3「②号单向 exporter」+ 006 §4 设计 6 要点**
  - 可吸收 → ②号「SQLite SSOT + vault 衍生」是**已被 SOTA 验证的成熟形态**(多个插件走这条),非我们独创的冒险路径。
  - 会改方向 → SOTA 提供一条更轻的「先尝鲜」路(直挂 .db 零导出),可作 next-PRD 里 exporter 之前的可选 step,但产品价值低于双链笔记(失去知识网),符合报告 §3 判断。
  - 噪音 → Dataview 作者退场的维护风险(报告 §1 注)被 SOTA「无内建 pipeline + 插件维护参差」放大,但不改 ②号方向,改的是「选 Bases(原生)而非 Dataview(社区)」的实现取舍 —— 属 L4 细节。

## 3. 修正后的视角

- P1 判断 A "**C5 措辞 → refactor**" → **强烈站住 + 升级**。P1 时我在「扩措辞 vs 局部钉」间不确定;SOTA 坐实 iCloud 不读 .gitignore 后,**至少**必须扩到「会被同步/传播的渠道」或等价地物理隔离原文。我现在更倾向 next-PRD 用「C5 扩措辞 + vault 只放指针摘要」双保险,而非仅局部钉。这与 Codex P1「C5 扩到云同步传播渠道」收敛。
- P1 判断 B "**②单向 exporter → new**" → **站住**。SOTA 证明这是成熟形态(SQLite Explorer 的 static snapshot embedding 即同构),冲击面小的判断成立。
- P1 判断 C "**US8 价值 vs 维护成本不确定**(§3#1)" → **部分被推翻为「可管理但有真风险」**。SOTA 显示「neglected vault compounds friction」+ importer「silent data loss」是真实失败模式 —— 但解法明确:exporter **幂等 + drift 可检**(对齐 v0.1 已有的 C7「不静默丢」+ 缺口报告机制)。即维护成本不是否决项,而是 next-PRD 必须落的验收项(导出后 vault 记录数 == 库记录数,无静默漏导)。
- P1 判断 D "**vault 放原文 → cut**" → **站住 + 证据加固**(iCloud 传播面坐实)。
- 残留分歧(留 P3):C5 是「扩措辞」还是「仅 v0.2 scope 局部钉」—— 我倾向扩措辞双保险,Codex P1 也倾向扩;但「扩措辞会反向收紧 v0.1 已 ship 落点(云/手机微信)」的副作用需 P3 摆清影响面。
