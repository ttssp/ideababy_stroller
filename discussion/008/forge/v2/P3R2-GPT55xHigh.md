# Forge v2 · 008 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-06-16T10:30:05Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge

## 1. 我对每条分歧的最终立场 + 让步

- **分歧 1 · C5 改法:全局原则 vs 局部 scope 钉死**
  - 对方在 P3R1 给的论证:"扩原则 + 不溯及既有落点" → 让步并接受。
  - 我的最终立场:C5 增补渠道中性原则,表达为「自用不传播」覆盖 git、云同步和任何会传播的衍生输出渠道;但不重审、不溯及 v0.1 已 ship 的采集落点与实现。v0.2 exporter 作为衍生导出层,必须显式钉死:原内容不进 vault,vault 只放指针、摘要、白名单 frontmatter、标的双链和 `reviewed`。
  - 让步给对方的部分:我不再主张无条件全局收紧;接受把影响面限定在「衍生导出/传播渠道」,避免误伤 v0.1。

- **分歧 2 · Dataview JS / 插件脚本是否进入验收可信路径**
  - 对方在 P3R1 给的论证:"不依赖能写文件/联网的脚本" → 接受。
  - 我的最终立场:该点不是 L4 小细节,而是数据流验收边界。v0.2 只验 frontmatter 可被 Obsidian Bases、普通只读查询或静态 Markdown 结构消费;Dataview JS 等可写文件/联网脚本不得成为验收必需路径,也不得作为 C5/SSOT 可信边界的一部分。
  - 让步给对方的部分:接受把此项从 P2 concern 升为 verdict 附带验收约束。

- **分歧 3 · v0.2 排序:US7 与 US8 exporter 谁先**
  - 对方在 P3R1 给的论证:"不替代 US7" → 接受。
  - 我的最终立场:forge v2 只决定 US8 exporter 是否进入 v0.2 scope,不绑定 build 先后。next-PRD 应写明 US7 盘中预警、US8 Obsidian exporter、完整 004 契约并列属于 v0.2;具体 sequencing 留给 v0.2 plan/operator 决议。
  - 让步给对方的部分:不在本 verdict 中暗示 exporter 优先级高于 US7。

## 2. 联合 verdict(单一)

**我和对方在 R2 后达成的单一 verdict**:008-pB v0.2 应该接受 Obsidian 作为 US8「三形态统一时间线 + 回放已看/未看」的人读前端,并新增「SQLite SSOT → Obsidian vault」单向 exporter。理由是:US8 已在 PRD 中成立但缺具体载体;Obsidian 的 Calendar/Bases/frontmatter/双链可兑现该载体价值;单向 exporter 保留 v0.1 的 allowlist、C7、`source_id` 反作弊和 SQLite SSOT,不触碰①替换或③双向同步。C5 必须同步 refactor:新增渠道中性的数据流原则,禁止原内容进入任何会传播/同步的衍生输出渠道;但不重审 v0.1 已 ship。vault 只允许白名单 frontmatter、`raw_ref` 指针、摘要级 key points/source_ref、标的双链和 `reviewed`;图文原文、完整转录、音视频、签名 URL 永久 OUT。验收只依赖只读 frontmatter 消费,不依赖可写文件/联网脚本。无 unresolved。

## 3. 残余分歧降级为 v0.2 note

- v0.2 note 1:US7 与 US8 exporter 的 build 先后不由 forge v2 强定。进入 v0.2 plan 时,operator 应按盘中预警时效价值、exporter 工作量、004 契约补全需求一起排序。
- v0.2 note 2:`key_points.text` / `source_ref` 的长度边界需在验收中钉清,防止「摘要级溯源」滑成事实上的完整转录导出。
- v0.2 note 3:exporter 必须幂等、可重跑、drift 可检;至少能检查库记录数与 vault note 数/`source_id` 集合一致,避免 silent loss。

## 4. W 形态产出的初步草稿建议

- **W 含 verdict-only** → 关键句:
  - "GO:把 Obsidian 定为 US8 人读前端,新增 SQLite→vault 单向 exporter;同时 refactor C5 为渠道中性传播边界,vault 只放指针+摘要,原文永久不进 vault。"

- **W 含 decision-list** → 建议矩阵:
  - 保留:
    - SQLite 是唯一 SSOT。
    - v0.1 已 ship 事实,不重审 T101-T112。
    - C5 法律/合规定性由 operator 负责。
    - US7 盘中预警仍是 v0.2 scope。
  - 调整:
    - C5 增补「自用不传播覆盖 git + 云同步 + 传播渠道」原则。
    - v0.2 US8 写明 Obsidian vault 是实现载体。
    - exporter 验收增加 no-original-content、drift 可检、只读查询边界。
  - 删除:
    - vault 放图文原文、完整转录、音视频、签名 URL。
    - ①Obsidian 替换 SQLite SSOT。
    - ③双向同步 / vault 回写库。
    - Dataview JS 等可写/联网脚本作为验收必需路径。
  - 新增:
    - 库→vault 单向 exporter。
    - 每条记录一个 `<source_id>.md`,frontmatter 白名单字段。
    - `reviewed` 字段、`published_at` 时间线、`[[标的]]` 双链。
    - vault 目录必须被 git-ignore 且通过 C5 safe out dir 守卫。

- **W 含 next-PRD** → 关键草案点:
  - Scope IN v0.2 增补:「Obsidian vault as US8 carrier: SQLite→vault 单向 exporter;vault 只读衍生,不回写;frontmatter 白名单字段 = source_id/published_at/form/capture_status/raw_ref/source_url_canonical/tickers/reviewed;body 仅摘要级 key_points/source_ref 与标的双链。」
  - C5 / Scope OUT 增补:「自用不传播覆盖 git、云同步和任何传播渠道;原内容(图文全文、完整转录、视频/音频、签名 URL)不得进入 vault 或任何可能传播的衍生输出目录;不双向同步,不替换 SSOT。」
  - Outcomes / Acceptance 增补:「导出后无正文字段检查通过;vault 路径 git check-ignore 命中;库记录 `source_id` 集合与 vault note 集合一致;可按日期/形态/标的/已看状态查询;查询验收不依赖可写文件/联网脚本。」
