# Forge v2 · 008 · P3R2 · Opus 4.7 Max · 联合收敛 R2(finalize)

**Timestamp**: 2026-06-16T09:38:00Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge(从 forge-config 读)

## 1. 我对每条分歧的最终立场 + 让步

P3R1 §3 列的三条「分歧」,读完 Codex P3R1 后确认**全部已收敛**——双方在 R1 各自给出的解法逐条一致,无真冲突。逐条 finalize:

- **分歧 1 · C5 改法(全局原则 vs 局部钉)**:
  - 对方在 P3R1 给的论证:"扩渠道中性原则 + 不溯及既有 v0.1 落点 + vault 只放指针摘要"——与我 P3R1 提议**逐字同向**。
  - 我的最终立场:**完全接受,无让步必要**。C5 增补一条**渠道中性原则**——「operator 自用不传播:原内容不得进入会被传播/同步的衍生渠道(含 git、iCloud/Obsidian Sync 及任何同步通道)」;明确**不溯及 v0.1 已 ship 的采集落点**(其合规性 operator 已负责,不重审);vault 这类衍生导出层只放白名单 frontmatter + `raw_ref` 指针 + 摘要级 key_points + 标的双链 + `reviewed`。
  - 让步给对方的部分:采纳 Codex「限制影响面」的精确表述(「增补」而非「重写」C5,避免误伤),比我 P3R1 初版「双保险」更收敛。

- **分歧 2 · Dataview JS 脚本边界**:
  - 对方论证:"不依赖可写文件/联网脚本;查询能力以只读 frontmatter 消费为准" → **接受**。
  - 我的最终立场:固化为**验收边界**(非实施细节):v0.2 验收只要求 frontmatter 可被 Obsidian Bases / 普通(只读)查询 / 静态 Markdown 结构消费;Dataview JS(能写文件/联网)**不进入合格线**,可作 operator 自用增强但不算验收通过条件。
  - 让步:我 P2 把它当「Bases vs Dataview 的 L4 细节」,**收回**——这是数据流护栏的一部分(查询层也必须只读,不开新写路径/旁路),应进 verdict。

- **分歧 3 · v0.2 排序(US7 vs US8 exporter)**:
  - 对方论证:"主 verdict 不绑定先后,只要求 next-PRD 写明并列,build sequencing 另决" → **接受**。
  - 我的最终立场:本 forge **只决定 US8 exporter 入 v0.2**,不替 L4 排工程顺序。verdict 声明 exporter 是 **bounded scope,不得挤掉 US7**;具体先后留 v0.2 note + next-PRD 写明并列。

## 2. 联合 verdict(单一)

**GO · Obsidian-as-US8-frontend + 单向 exporter,以最严 C5 数据流边界落地**。

把 Obsidian 个人知识库前端定为 PRD **US8(三形态统一时间线 + 回放已看/未看)的实现方向**,并在 **v0.2 scope 新增一条 bounded 能力**:`SQLite 库 → Obsidian vault` **单向 exporter**(库→vault 衍生,vault 只读、不回写)。**SQLite 仍是唯一 SSOT**——v0.1 三条护栏(allowlist 强校 / C7 不静默丢 / source_id 反作弊一致性)原样保留;①替换 SSOT、③双向同步永久出局。**C5 增补渠道中性原则**(自用不传播:原内容不得进入会被传播/同步的衍生渠道),**不溯及 v0.1 已 ship 落点**;vault 只放指针 + 摘要,**原文/完整转录/音视频/签名 URL 永久不进 vault**(双方 SOTA 双重坐实:iCloud 不读 .gitignore;Readwise full-text 开关证明原文导出会被当便利功能加回来,必须显式禁)。**验收边界**:exporter 幂等 + drift 可检(导出后 vault 记录数 == 库记录数,无静默漏导,对齐 v0.1 C7)、git check-ignore 命中、Dataview/Bases 按天·标的·形态可查、双链反链聚合正确、查询不依赖可写文件/联网脚本。**v0.2 可立即启动 PRD/spec 增量决议**;exporter 是 bounded scope 不挤掉 US7,正式 build 顺序另决。无 unresolved 项。

## 3. 残余分歧降级为 v0.2 note

- **v0.2 note 1 · US7/US8 build 排序**:本 forge 不定先后;next-PRD 写明 US7(盘中预警)与 US8 exporter 并列,build sequencing 在 L4 plan-start 时决。何时回头看:v0.2 立项拆 task 时。
- **v0.2 note 2 · 摘要 vs 原文的粒度线**:`key_points.text` / `source_ref`(转录子串)允许进 vault,但「子串多长算摘要、多长滑向事实原文复制」未量化(双方 §3 共同不确定点)。何时回头看:exporter 验收标准细化时,建议定一个 source_ref 最大长度 + 「可溯源但不可重建原文」判准。
- **v0.2 note 3 · 维护成本长期验证**:尝鲜「图谱值得投」是用户信号非长期证据;SOTA 显示 neglected vault compounds friction。何时回头看:v0.2 运行一段后,评估 exporter 是否真降低 backlog 遗忘(US8 价值证否点)。

## 4. W 形态产出的初步草稿建议

forge-config W 三件套(verdict-only + decision-list + next-PRD),给 synthesizer 的草稿建议:

- **W 含 verdict-only → verdict 关键句**:"GO:Obsidian 作 US8 人读前端入 v0.2,新增库→vault 单向 exporter;SQLite 唯一 SSOT 不漂;C5 增补渠道中性原则(不溯及 v0.1 落点);vault 只放指针+摘要,原文永久 OUT;验收=幂等+drift 可检+只读查询。"

- **W 含 decision-list → 4 列矩阵(前 5 条)**:
  - **保留**:SQLite SSOT + v0.1 三护栏(allowlist / C7 / source_id 反作弊);v0.1 已 ship 采集落点(合规不重审)。
  - **调整**:C5 措辞——增补渠道中性原则(自用不传播,覆盖 git + 云同步),不溯及既有落点;US8 从抽象 story → 指定 Obsidian 载体。
  - **删除**:vault 放原文/完整转录/音视频/签名 URL(永久 OUT);依赖 Dataview JS(可写文件/联网)作验收合格线;①替换 SSOT / ③双向同步(防回潮)。
  - **新增**:v0.2 `库→vault` 单向 exporter(frontmatter 白名单映射 + 标的双链 + `reviewed` + Calendar 时间线);exporter C5 守卫(复用 `_assert_c5_safe_out_dir` + vault 强制 git-ignored);幂等 + drift 可检验收项。

- **W 含 next-PRD → 关键产品决策点**(3 条):
  1. **US8 实现方向锚定**:Obsidian vault 作 US8 载体(Calendar=统一时间线 / `reviewed` frontmatter=已看未看 / 双链=长内容不进 backlog)。
  2. **C5 §Real-world constraints 增补**:渠道中性原则 + vault 只放指针摘要 + 原文永久 OUT 清单 + 不溯及 v0.1 落点声明。
  3. **v0.2 Scope IN/OUT 增量**:IN = 单向 exporter(bounded,不挤 US7);OUT = 双向同步 / 替换 SSOT / 原文进 vault / 依赖可写脚本作验收。验收 outcomes 五条(无正文字段 / git check-ignore 命中 / 三维可查 / 双链聚合 / 幂等 drift 可检)。
