# Forge v2 · 008 · P3R1 · GPT55xHigh · 联合收敛 R1(标分歧)

**Timestamp**: 2026-06-16T09:28:52Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: NONE(避免 R1 又开搜索发散)。

## 1. 整合摘要

双方 P1/P2 的主线已经高度一致:Obsidian 不应替换 v0.1 SQLite,而应作为 US8 的人读前端;②「SQLite SSOT → vault 只读衍生」是唯一可接受路线;①替换 SSOT 与③双向同步继续出局。产品价值层也基本对齐:Obsidian 的 Calendar/Bases/双链/`reviewed` 能把 US8 从抽象 story 落成 operator 可消费界面,并且 Readwise/Logseq/Omnivore 等参照共同证明「采集/高亮 → 本地知识图谱」不是孤例。

数据流层的证据更强:我的 P2 用 Obsidian Sync / Readwise / Dataview / Logseq / Omnivore 得出三点:git-ignore 不覆盖同步传播面;成熟导出产品会显式区分 highlights 与 full text;本地 SSOT + 可重导出的衍生层抗生命周期风险。Opus P2 也独立强化同一结论,尤其指出 iCloud 不读 `.gitignore`,所以「原文物理隔离」不是锦上添花,而是 C5 产品边界的硬前提。

剩下要收敛的不是 go/no-go,而是 wording 和验收边界:第一,C5 是全局扩成「传播渠道原则」,还是只在 v0.2 exporter scope 局部钉 vault 规则;第二,Obsidian 查询验收应只要求 frontmatter 可被原生/普通查询消费,还是允许 Dataview JS 一类可写文件/联网的脚本进入可信路径。

## 2. 我的初步 verdict(草案)

我倾向 **go:把 Obsidian 定为 US8 实现方向,新增 v0.2 单向 exporter,但以最严 C5 数据流边界落地**。SQLite 继续是唯一 SSOT;vault 只放白名单 frontmatter、`raw_ref` 指针、摘要级 key points、标的双链和 `reviewed`;原文、完整转录、音视频、签名 URL 永久不进 vault。C5 应写成渠道中性的「不得进入会传播/同步的衍生渠道」原则,并注明不溯及 v0.1 已 ship 落点;验收只看可重导出、可查询、无原文、drift 可检,不依赖可写脚本。

## 3. 关键分歧清单

- **分歧 1 · C5 改法:全局原则 vs 局部 scope 钉死**
  - 我的立场:采用渠道中性原则,但限制影响面。写法应是「C5 增补传播/同步渠道边界;v0.2 exporter 原文不进 vault;不重审 v0.1 已 ship 落点」。这样避免只局部钉导致后续输出路径复发,也避免全局措辞误伤已有交付。
  - 对方立场(引用对方 P2):"C5 扩措辞 + vault 只放指针摘要"。
  - 我希望 R2 怎么收敛:直接收敛到 Opus P3R1 提示的折中:扩渠道中性原则 + 不溯及既有 v0.1 落点 + vault 只放指针摘要。

- **分歧 2 · Dataview JS / 插件脚本是否进入验收可信路径**
  - 我的立场:不进入。v0.2 验收只要求 frontmatter 可被 Obsidian Bases / 普通 Dataview 查询 / 静态 Markdown 结构消费;Dataview JS 可作为用户自用增强,但不能成为合格线,因为它具备写文件/联网能力,会扩大数据流面。
  - 对方立场(引用对方 P2):"选 Bases(原生)而非 Dataview(社区)"。
  - 我希望 R2 怎么收敛:固化为验收边界,不是实施细节:「不依赖可写文件/联网脚本;查询能力以只读 frontmatter 消费为准」。

- **分歧 3 · v0.2 排序:US7 与 US8 exporter 谁先**
  - 我的立场:本 forge 只决定 US8 exporter 是否入 v0.2,不替 L4 排工程顺序。verdict 可以说 exporter 是 bounded scope,不得挤掉 US7;排序留为 v0.2 note。
  - 对方立场(引用对方 P1):"不能默认它挤掉 US7"。
  - 我希望 R2 怎么收敛:主 verdict 不绑定先后,只要求 next-PRD 写明 US7 与 US8 exporter 并列,build sequencing 另决。

## 4. 与 K 的对齐性自检

- K「把 Obsidian 个人知识库前端定为 US8 的实现方向」→ ✅ verdict 明确 go,且把它限定为 US8 人读前端,不是替换库。
- K「②单向 exporter + SSOT 不可漂」→ ✅ SQLite 继续唯一 SSOT,vault 只读衍生,①/③不重论。
- K「C5 只审产品/数据流层边界」→ ✅ 全程不审法律/ToS/DMCA;只处理传播渠道、vault 字段、原文隔离。
- K「vault 该放指针还是原文」→ ✅ 明确指针+摘要;原文、完整转录、音视频、签名 URL 永久 OUT。
- K「v0.2 该不该现在启动」→ ⚠ 支持启动 PRD/spec 增量决议,但 build 顺序仍需后续决定,尤其不能让 exporter 隐式挤掉 US7。
