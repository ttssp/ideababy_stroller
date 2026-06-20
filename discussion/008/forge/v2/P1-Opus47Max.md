# P1 · Opus 4.7 Max · forge 008 v2 · Phase 1(独立审阅)

**审阅人姿态**:评判已存在物(XenoDev 输入包提案 + 研究报告 + 现行 PRD v1.1),非 daydream。NO web search(P2 才搜)。未读对方 P1。

## §0 我读到的标的清单 + 阅读策略 + K 摘要

**读取策略**:Y = 产品价值 + 数据流边界两镜头。故优先读 ① 议题主源(`_external/006`)定 scope 增量的诉求;② 研究报告(`_external/005`)拿三姿势取舍 + v0.1 护栏被冲击面 + C5 守法方案;③ PRD v1.1 的 US8/C5/Scope/Phase-transition 锚点,确认提案「落在已有 v0.2 锚点上」而非无中生有;④ handback(T112)只取「v0.1 已 ship、406 test 绿」这一事实;⑤ v1 stage 只取「C5 重定基线 + 合规由 operator 负责」这一前提。spec 快照用于核对 v0.2 outcomes 阈值「待 v0.1 learnings」的留白位置。

**实际读到**(全部 ✅ 可达,无 BLOCK):
- `008-pB/PRD.md` v1.1 — US8(:57)、C5(:133)、Scope IN v0.2(:70)、Phase transition learning、v0.1 OUT。
- `_external/XENODEV-006-...scope-input.md` — §0 提案 / §4 exporter 6 要点 + 验收 / §6 C5 待议 / §7 决策清单。
- `_external/XENODEV-005-...research.md` — §0 结论(②号方案)/ §2 v0.1 被冲击面 / §3 三姿势 / §4 C5 守法 / §5 落点判定。
- `_external/XENODEV-spec-008-pB.md` — §1.2 v0.2 Outcomes(阈值待 learnings)/ §2.1 v0.2 in-scope。
- `handback/...20260615...md`(T112)、`forge/v1/stage-forge-008-v1.md`。

**K 摘要**:在「v0.1 已 ship」前提下,(1) 把 Obsidian 知识库前端定为 US8 实现方向 + v0.2 加「库→vault 单向 exporter」该不该做、怎么做;(2) C5 在「vault 可能被云同步」下边界怎么画。**binding**:C5 法律定性由 operator 负责(不审违法性,只审产品/数据流层边界);SSOT 不可漂(①替换/③双向已出局,②单向 exporter 是设计底线,不重论)。

## §1 现状摘要(按 Y 视角)

### 视角 A · 产品价值

PRD 标题本就是「采集 **→ 个人知识库**」,US8(v0.2)= 「三形态统一时间线 + 回放已看/未看,长内容不消失进 backlog」。这是一个**已立项但未指定实现载体**的 story。提案的实质 = 给 US8 选一个具体载体(Obsidian vault + Calendar + Bases + frontmatter `reviewed`),而非新开 scope。这一点站得住:US8 的「统一时间线」天然映射 Calendar 插件 + `published_at`;「已看/未看」天然映射一个 frontmatter 布尔字段;「长内容不消失」天然映射双链反链聚合(标的→所有提它的采集)。**产品价值的真问题不在「能不能映射」,而在「值不值得」**:v0.1 已有 SQLite `query(date, form, ticker)` 三维检索(研究报告 §2),US5「按日期/形态/标的回看」v0.1 已交付。那么 US8 相对 US5 的增量价值 = 「统一时间线视图 + 已看/未看状态 + 双链知识网」。前两者是 UI 便利,第三者(双链图谱)是 SQLite 给不了的**新认知价值**——operator 在尝鲜中「实看双链 + 图谱效果,判定值得投」(006 §5),这是真实用户信号,不是纸面推断。

### 视角 B · 架构设计 / 数据流边界

研究报告已把设计空间收敛干净:①替换 SSOT(撞 v0.1 三护栏:allowlist 强校 / C7 不静默丢 / source_id 反作弊一致性)→ 出局;③双向同步(一致性地狱 + 最易破 C5)→ 出局;**②单向 exporter(库→vault,vault 只读衍生)→ 推荐**。这个收敛我认同,且它是 K 的 binding。②号方案的数据流护栏有三道,全部**复用 v0.1 既有机制**而非新发明:(a) vault 目录强制 git-ignored + 拒非 ignored 输出路径(复用 `_assert_c5_safe_out_dir`);(b) frontmatter 只映射白名单字段(复用 allowlist,杜绝正文字段冗余进 frontmatter);(c) 单向 = vault 不回写库,SSOT 唯一性自然保住。**数据流边界的真问题在 C5**:vault git-ignored 只挡 git,但 vault 常挂 iCloud/Obsidian Sync,原内容进 vault 仍可能被同步传播出去。研究报告 §4 的最严档建议(原内容绝不进 vault,vault 只放指针 raw_ref + 摘要 key_points.text/source_ref)是数据流层的正确默认——它把「C5 在 git 之外的传播渠道」这个新暴露的边界,用「物理隔离原内容」一招兜住,**不依赖 C5 措辞先改完**。

## §2 First-take 评分

| 维度 | 评分 | 理由 |
|---|---|---|
| **US8 实现方向 = Obsidian**(产品价值) | **keep(采纳)** | US8 三要素天然映射 vault 能力;双链图谱是 SQLite 给不了的真增量;operator 尝鲜已给真实用户信号。非过度工程——它落在已有 US8 锚点上,不新开 scope。 |
| **②号单向 exporter**(scope 增量) | **new(新增)** | v0.2 新增能力,设计已被研究报告论证、尝鲜已验证可行(6 篇笔记 + 标的总览,C5 三检全过)。护栏复用 v0.1 既有,冲击面小(加一个导出器,不改既有模块)。 |
| **C5 措辞**(数据流边界) | **refactor(调整)** | 现行 C5「绝不入 git」(PRD:133)在「vault 同步」场景下**覆盖不全**。需调整:要么扩措辞到「绝不进任何会被传播/云同步的渠道」,要么保持 C5 不动但在 v0.2 scope 显式钉「原内容绝不进 vault,vault 只放指针+摘要」。无论哪条,**最严档(原内容物理隔离)是 binding 默认**。 |
| **vault 放原文** | **cut(删除/禁止)** | 原内容(图文原文/回放视频音频/完整转录/含签名 URL)进可同步的 vault = 走出本地自用边界。应永久 OUT,留在 `raw_ref` 本地原文区。 |
| **①替换 / ③双向同步** | **cut(已出局)** | 研究报告已判出局,K binding 不重论。仅记录:防后续轮次回潮。 |
| **v0.2 启动时机** | **refactor(需排序)** | exporter 是 v0.2 的**一条** scope,与 US7(盘中预警)、完整 004 契约并列。需在 next-PRD 里给优先级,不能默认它挤掉 US7。 |

**与 K 的初步对齐**:K 的 4 个 operator 关切——(1) US8 价值兑现 → §1A 正面回应;(2) 数据流护栏 → §1B 三道护栏复用既有;(3) C5 边界 → §2 refactor + 最严档;(4) v0.2 排序 → §2 标记需排序。无遗漏项。

## §3 我现在最不确定的 3 件事

1. **US8 增量价值 vs US5 的边际**:v0.1 SQLite 三维检索已交付 US5。US8 的 UI 便利(统一时间线 + 已看/未看)若**只**靠 Obsidian 实现,会不会让 008 从「004 单源采集模块」漂成「我要维护一个 Obsidian workflow」?即:exporter 的**维护成本**(每次采集后跑导出、vault 与库的最终一致性、插件生态维护风险——研究报告 §1 注 Dataview 原作者已退场)是否被 operator 在尝鲜的「值得投」里充分计入?这是产品价值层我最不确定的。
2. **C5 措辞改 vs 不改的取舍**:扩 C5 措辞到「云同步渠道」是更干净的根因修复,但会**反向收紧整个 008**——它意味着任何「可能被同步的目录」都受 C5 约束,可能波及 v0.1 已 ship 的产物落点(PRD Phase-transition 提到落点含「云/手机微信」)。保持 C5 不动 + 仅在 v0.2 scope 钉 vault 规则,影响面小但留了「C5 措辞与实际边界不完全吻合」的债。这个取舍 next-PRD 必须替 operator 摆清,我现在倾向后者(局部钉)但不确定。
3. **「摘要」进 vault 的边界粒度**:研究报告 §4 允许 `key_points.text` + `source_ref`(转录子串)进 vault。但「转录子串」多长算「摘要」、多长算「完整转录」?US3 要求关键点可溯源回**原始转录 + 视频稳定时间戳**——若 vault 里的 source_ref 子串足够长以满足溯源,它离「完整转录」有多远?这条数据流边界的**粒度**(摘要 vs 原文的分界线具体画在哪)我不确定,可能是 next-PRD 验收项里要量化的点。
