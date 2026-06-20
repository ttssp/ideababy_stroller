# Forge v2 · 008 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-06-16T09:22:10Z
**Searches run**: 13 queries, 产品价值层 SOTA-benchmark; no legal / ToS / DMCA search.
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标(产品价值层)

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| 008-pB US8 | Obsidian Sync | vault 可连接 remote vault,并有 selective sync;官方还提醒第三方同步文件夹需谨慎。 | 现行 C5 只钉 git;P1 倾向 vault 只放指针/摘要。 | P1 的 C5 云同步边界站住:git-ignore 不等于不传播。 | https://obsidian.md/help/sync/setup |
| 008-pB exporter | Readwise → Obsidian | 新 highlight 可自动同步;新文档建页,旧文档 append;不会覆盖用户改动;另有 full-text export 开关。 | 一条采集记录一个 `<source_id>.md`;vault 只读衍生。 | 单向/append-only 是成熟形态;但 full-text 开关证明必须显式禁止原文导出。 | https://docs.readwise.io/readwise/docs/exporting-highlights/obsidian |
| 008-pB vault 查询 | Obsidian Dataview | 把 vault 当可查询的 markdown 数据集;读取 frontmatter/inline fields;JS 查询有文件/网络能力风险。 | 拟用白名单 frontmatter + Bases/Dataview 查日期/形态/标的。 | 查询价值站住;但验收应偏只读/受限查询,别把插件脚本变成新写路径。 | https://github.com/blacksmithgu/obsidian-dataview |
| 008-pB 知识图谱 | Logseq | local-first / privacy-first 知识管理,支持 Markdown/Org,强调 user control;DB 版本仍提示备份和测试图。 | SQLite 为 SSOT,vault 为人读衍生。 | PKM SOTA 支持本地文件+图谱价值;也支持不把 PKM 工具当权威库。 | https://github.com/logseq/logseq |
| 008-pB 采集→笔记链 | Omnivore | read-it-later 产品支持 Obsidian/Logseq 插件;云服务 2024-11 后退成 self-hosted。 | v0.1 本地 SQLite 已 ship;Obsidian 只是导出层。 | P1 的“本地 SSOT + 可重导出”更强:外部采集/阅读服务生命周期不应卡住知识库。 | https://github.com/omnivore-app/omnivore |

## 2. 用户外部材料消化

> 基于上一轮已读内容消化;本轮按 reuse-session 约束未重读 `_external/` 文件。

- **`_external/XENODEV-006-obsidian-v0.2-scope-input.md`**
  - 可吸收:把 Obsidian 定为 US8 载体、`reviewed` 字段、`published_at` 时间线、`[[标的]]` 反链、vault 只放白名单字段。
  - 会改方向:搜索后更支持把 exporter 设计成 append/regenerate 明确的单向导出,并把 full-text 禁止写进边界。
  - 噪音:尝鲜「图谱效果值得投」只能算用户信号,不能替代长期使用证据。
- **`_external/XENODEV-005-obsidian-knowledge-store-research.md`**
  - 可吸收:②单向 exporter、SQLite SSOT 不漂、原内容留在 `raw_ref` 本地原文区。
  - 会改方向:Dataview JS 能写文件/联网,所以“vault 可查询”不应默认等于“任意插件脚本可跑”。
  - 噪音:①替换 SSOT / ③双向同步已被 K binding 排除,本轮只作防回潮记录。

## 3. 修正后的视角

- P1 判断「Obsidian 作为 US8 载体 = new」→ **站住**。Readwise 和 Logseq 证明采集/高亮进入本地知识图谱是成熟产品形态;不是 008 独创负担。
- P1 判断「vault 原文 cut」→ **更强**。Readwise 的 full-text export 是成熟产品里的显式开关,反证 008 必须把这类能力列为禁止,否则后续很容易被当作便利功能加回来。
- P1 判断「C5 扩到云同步渠道 = refactor」→ **站住但需收窄表述**。Obsidian Sync 证明 vault 本身就是同步对象;但对方 P1 的提醒也成立:全局改 C5 可能波及 v0.1 落点。P3 应收敛为“PRD C5 增补传播渠道原则 + v0.2 exporter 明确原文不进 vault”,避免过宽误伤。
- P1 判断「②单向 exporter 保住 SSOT」→ **站住**。Omnivore 云端退场和 Logseq DB beta 警告共同支持:可重建的人读导出层比把权威源交给 PKM/阅读服务更稳。
- P1 未充分覆盖的点 → **新增 concern**。Dataview JS 查询有写文件/联网能力;若 v0.2 验收依赖 Dataview,应只要求 frontmatter 可被 Bases/普通查询消费,不要把任意脚本能力纳入可信路径。
