# v0.2 scope 增量提案 · Obsidian 个人知识库前端 — 回 IDS 的输入包

> **性质**:这是给 **operator 拿回 IDS 治理仓**用的「v0.2 scope 增量输入」,**不是 XenoDev 实装**,也**不是**已写进 IDS 的决议。
> XenoDev 只读 IDS;本包等 operator 在 IDS 决议后,才可能回流成 v0.2 task。
> **日期**:2026-06-16 · **依据**:`005-obsidian-knowledge-store-research.md`(调研)+ 零成本尝鲜实跑(已挂 .db + 导出 vault 看到双链效果,operator 判定「值得投」)。
> **结论先**:见 §0。

---

## §0 一句话提案

把 **Obsidian 个人知识库前端**定为 PRD **US8「三形态统一时间线 + 回放已看/未看」的具体实现方向**,并在 v0.2 scope 增量一条新能力:**v0.1 库(SSOT)→ Obsidian vault 单向 exporter**。SQLite 仍是唯一 SSOT,Obsidian 当人读前端(双链/图谱/Bases),**不替换库**。

---

## §1 为什么这是 IDS 的事(不是 XenoDev 当场改)

per CLAUDE.md 决策矩阵 + SHARED-CONTRACT:

- 「采集→知识库前端」= **v0.2 新能力(B)**,且可能触及 **PRD v0.2 章节 + 完整 004 契约(C)** 与 **C5 措辞(D)** → **SSOT 在 IDS,不在 XenoDev 当场实装**。
- v0.1 已 ship(T101-T112 已 merge + hand-back 在 IDS 待 review),这**不是** v0.1 的 bug 修复。
- 故本包是「输入」,回 IDS 决议后才回流 XenoDev 拆 task。

## §2 走哪个 IDS 入口(operator 选)

⚠️ **`/scope-inject` 不对口**:它是 **L3 阶段**(scope 还在辩论期)的 moderator note 注入器,会触发 debaters 重跑。**008-pB 早过 L3**(PRD 已 frozen,phase 已 v0.1 ship)。用它等于把已定稿的 scope 打回辩论,错。

正确入口二选一:

| 入口 | 适用 | 怎么用本包 |
|---|---|---|
| **`/handback-review 008`**(推荐先走) | 之前的 v0.1 hand-back 已在 IDS 待 review;Obsidian 决策是 v0.1 反馈的一部分 | review v0.1 时**连带决议**:① 启动 v0.2;② 把 Obsidian 定为 US8 实现方向;③ 接受本包的 exporter scope 增量 |
| **`/expert-forge 008`** | 若要正式论证「知识库前端形态」写进 PRD v0.2 章节(动 PRD) | 把 §4 的 scope 增量 + §6 的 C5 待议点作为 forge 议题 |

**建议**:先 `/handback-review 008` 把 v0.1 收口 + 决议启动 v0.2 方向;若决议要正式改 PRD v0.2 措辞,再 `/expert-forge 008`。

## §3 与现有 PRD/spec 的挂接(不是凭空加 scope)

本提案**落在已有的 v0.2 锚点上**,非新开 scope:

- **PRD 标题已是**「投资顾问内容自动采集 **→ 个人知识库**」(discussion/008/008-pB/PRD.md:1)—— 知识库本就是终态。
- **US8(v0.2)**=「三形态在**统一时间线**回看,标记回放已看/未看」(PRD:57)。**Obsidian vault + Calendar/Bases 正是 US8 的实现载体**(按天时间线 = Calendar 插件;已看/未看 = frontmatter 一个 `reviewed` 字段)。
- **PRD:89**「完整 004 输出契约(v0.1 仅粗约定)」—— exporter 的 frontmatter 字段映射与这条对齐(白名单字段→frontmatter)。
- **spec §1.2 v0.2 Outcomes（阈值待 v0.1 learnings）**(spec.md:180)—— 本提案是 v0.1 learning 的一部分,正是「待补」要补的内容。

→ 即:**这是给已存在的 v0.2 US8 补具体实现方向 + 明确「知识库前端」作为一种交付形态**,不是无中生有。

## §4 提议的 v0.2 scope 增量(给 IDS 决议用)

**新增能力**:`库 → Obsidian vault` 单向 exporter(②号方案)。

设计要点(已在尝鲜中验证可行):
1. **SQLite 仍是唯一 SSOT**,exporter **单向**(库→vault),vault 只读衍生,不回写库 —— 保住 v0.1 所有护栏(allowlist 强校 / C7 不静默丢 / source_id 反作弊一致性 / C5-pointer)。
2. **每条采集记录 → 一个 `<source_id>.md`**:frontmatter = **白名单字段**(source_id/published_at/form/capture_status/raw_ref/source_url_canonical/tickers);body 写 `[[标的]]` 双链。
3. **标的 → 双链节点**:Obsidian 图谱/反链天然聚合「某标的出现在哪些采集」——这是 SQLite 给不了的知识网价值(尝鲜已实证)。
4. **US8 已看/未看**:frontmatter 加 `reviewed: true|false`(回放长内容不消失进 backlog)。
5. **US8 统一时间线**:Calendar 插件 + `published_at` 的 pub_date = 按天时间线视图。
6. **Bases/Dataview**:frontmatter 标准 YAML,原生 Bases 即可做 form/状态/标的的表视图(无需写 SQL）。

**验收(草案,供 task-decomposer 细化)**:
- exporter 跑后 vault md 过「无正文字段」检查(只白名单字段 + raw_ref 指针）；
- `git check-ignore` vault 命中（C5）；
- Dataview/Bases 能按天/标的/形态查出（对齐 O1「那天发了什么」）；
- 标的双链反链聚合正确（一个标的 → 所有提它的采集）。

## §5 尝鲜证据（本提案不是纸上谈兵）

已在 XenoDev 用 git-ignored 的 `out/` 跑通（**非实装,产物不入 git**）：
- `out/db/collection.db` — 6 条样本（4 图文 + 2 回放，跨 2 天，多标的，含 uncertain/failed），走真 `validate_record` 门入库；
- `out/export-to-obsidian-probe.py` — 一次性导出脚本，把库导成 `out/004-feed/vault/`（6 篇笔记 + 标的总览页）；
- C5 三检全过：vault 被 git 忽略 / 笔记零正文（只指针）/ git status 无新受控文件；
- operator 在 Obsidian 实看双链 + 图谱效果，判定「值得投」。

→ 临时脚本若 v0.2 立项，将升级为带 C5 守卫的正式 exporter（走 plan mode + TDD + 红队）。

## §6 必须连带决议的 C5 边界问题（forge 候选 · 重要）

> 这是尝鲜暴露的**新 C5 模糊点,必须回 IDS 厘清,不在 XenoDev 自决**。

现行 **C5 = 原内容「绝不入 git」**，但**没说「绝不进会被云同步的目录」**。Obsidian vault 常挂 **iCloud / Obsidian Sync**——

- 即便 vault git-ignored，原内容若进 vault 仍可能被云同步**传播出去**，**走出「本地自用」边界**。
- **本提案的最严档处置**（建议默认）：**原内容（图文原文/回放视频/音频/完整转录/含签名 URL）绝不进 vault**，vault 只放**指针（raw_ref）+ 摘要（key_points.text/source_ref）**。原内容留在 `raw_ref` 指的本地原文区。
- **待 IDS 决议**：C5 措辞是否要从「绝不入 git」扩展为「绝不进任何会被传播/云同步的渠道」？这影响 vault 到底能放什么。

## §7 待 operator 决策清单（回 IDS 时一并定）

1. 启动 v0.2 build？（phase 转换由 operator 显式决定 · PRD:105）
2. 把 Obsidian 知识库前端定为 US8 实现方向？（接受 §4 scope 增量）
3. C5 措辞是否扩展到「云同步渠道」？（§6）——决定 vault 放什么
4. 入口走 `/handback-review 008`（连带决议）还是 `/expert-forge 008`（正式改 PRD）？

---

## 来源 / 关联

- 调研报告：`projects/008-pB/probe/005-obsidian-knowledge-store-research.md`
- v0.1 hand-back（IDS 待 review）：`ideababy_stroller/discussion/008/handback/20260615T234706Z-008-pB-20260615T234706Z.md`
- PRD：`ideababy_stroller/discussion/008/008-pB/PRD.md`（US8:57 / Scope IN v0.2:70 / v0.1 OUT:86 / v0.1 假设:93）
- spec：`specs/008-pB/spec.md`（§1.2 v0.2 Outcomes:180 / §2.1 v0.2 in-scope:207）
