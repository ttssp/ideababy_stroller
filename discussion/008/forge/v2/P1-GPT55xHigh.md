# Forge v2 · 008 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-06-16T08:55:55Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

我读了 `forge-config.md`、现行 `PRD.md`、v0.1 hand-back、forge v1 stage、`_external/` 三份 XenoDev 快照、`.claude/skills/forge-protocol/SKILL.md`。`moderator-notes.md` 不存在。按 inbox 约束,我没有读 `P1-Opus47Max.md`,也没有读 XenoDev 跨仓原路径。

**K 摘要**:用户要判断的是:在 v0.1 已 ship 的前提下,是否把 Obsidian 个人知识库前端定为 US8 的实现方向,并把「库→vault 单向 exporter」写成 v0.2 scope 增量;同时只在产品/数据流层重画 C5 的 vault/cloud-sync 边界。法律/ToS/DMCA 合规性是已决前提,本轮不审。

我的阅读策略是把问题拆成两层:产品价值层看 Obsidian 是否兑现 US8「统一时间线 + 已看/未看 + 长内容不进 backlog」;数据流层看 SQLite SSOT、C7、allowlist、`source_id` 反作弊是否被 vault 破坏。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 产品价值

PRD v1.1 已把 008 定义为「采集 → 个人知识库」,但 US8 仍只是 v0.2 意图:三形态统一时间线、回放已看/未看。XenoDev 输入包把 Obsidian 具体化为这个意图的载体:每条记录导出 note,用 `published_at` 做 Calendar/Bases 时间线,用 `reviewed` 标记回放消费状态,用 `[[标的]]` 反链聚合相关内容。

v0.1 hand-back 显示图文+回放采集、存储、检索、缺口可见、004 输出包已 code-complete,406 tests 绿;但 O1/O2/O3/O5b 仍需真实使用观察。因此 US8 的数据基础已经存在,但「Obsidian 是否真的减少 backlog 遗忘」还不是已验证事实。

这使 Obsidian 更像 v0.2 的消费层增量,不是对 v0.1 交付质量的重新审判。

### 视角 B · 架构设计 / 数据流边界

调研报告确认 v0.1 的权威源是 SQLite:库层只存 `raw_ref` 指针,`validate_record` 强校字段和时间戳,缺口报告和 004 输出包都依赖受控记录流。Obsidian 原生没有 schema 强校、C7 不静默丢、`source_id` 反作弊一致性,所以①替换 SSOT 和③双向同步已出局;②单向 exporter 是本轮 binding 底线。

新的 C5 模糊点是传播渠道,不是采集合法性。git-ignore 只能挡 git,但 vault 可能被 iCloud/Obsidian Sync 同步。输入包和调研报告都把最严档写成:vault 只放白名单 frontmatter、`raw_ref` 指针、标的双链和摘要/溯源;图文原文、完整转录、音视频、签名 URL 不进 vault。

## 2. First-take 评分(按 Y 视角)

| 项 | Y 维度 | 倾向 | 理由 |
|---|---|---|---|
| US8 实现方向 = Obsidian | 产品价值 | **new** | 现行 PRD 有 US8 目标但无载体;Obsidian 的 Calendar/Bases/双链/`reviewed` 正好把目标落成可用前端。 |
| ② 单向 exporter | 架构/数据流 | **new** | 可作为 v0.2 新能力加入,但只能是 SQLite→vault 单向衍生;这保留 v0.1 的三条护栏。 |
| C5 措辞扩到云同步渠道 | 架构/数据流 | **refactor** | 「绝不入 git」不足以表达「自用不传播」的数据流边界;应扩到任何可能传播/同步的输出渠道。 |
| vault 放原文 | 架构/数据流 | **cut** | 原文进 vault 会让 vault 从索引层变成内容存储层,绕开 `raw_ref` 边界;即使 ignored,云同步仍改变传播面。 |
| v0.2 启动时机 | 产品价值 + 架构/数据流 | **refactor** | 可以现在启动 PRD/spec 增量决议;正式 build 前先收口 hand-back、C5 措辞和 exporter 验收边界。exporter 应作为 US8 bounded scope,不替代 US7。 |

## 3. 我现在最不确定的 3 件事

1. Obsidian 的真实使用增益是否超过 v0.1 SQLite 检索 + 004 输出包;尝鲜证据还不是长期使用证据。
2. `key_points.text` / `source_ref` 允许写多长;太长会从「摘要+指针」滑向事实上的原文复制。
3. v0.2 里 US7 与 US8 exporter 的先后顺序;两者都合理,但资源约束下需要明确谁先进入 build。
