# Forge v4 · 008 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-06-30T17:47:35+08:00
**Searches used**: NONE in this round.
**Visibility**: I did NOT read other reviewer's P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:`forge-config.md` 全文;hand-back 全文;`STRUCTURE-DICTIONARY-draft.md` 全文;`008-pB/PRD.md` 全文;`dogfood-backlog.md` 的 KG-24/KG-25;`forge-protocol/SKILL.md` 的 P1 模板;`AGENTS.md`。
- 我跳过的:`discussion/008/forge/v4/moderator-notes.md` 不存在;X#2/X#4 均真实可读,未使用 fallback 摘录;按约束未读 `discussion/008/forge/v4/P1-Opus47Max.md`。
- **K(用户判准)摘要**:operator 的核心担心是结构化数据会变成「纸上谈兵」:下游用途/消费目标从未定义,字段越堆越多但没有价值闭环。operator 倾向「自己回看检索 + 提炼投资信号 / 跟单」,且要求机器可信,但 K 明确说真瓶颈不是 schema,而是 LLM 在反讽+黑话语料里提 `stance_direction` / `conviction` / `action_type` 的可靠性;「信号错标 = 真金白银亏损,比没有信号更危险」。
- **我的阅读策略**:先用 K 锁住“用途”和“可靠性”两个主轴,再按 Y 四维把 PRD、hand-back、字典、KG 缺陷映射到现状,避免把工程架构或合规重新打开。

## 1. 现状摘要(按 Y 视角组织)

### 视角 A · 产品价值/用途成立性

现 PRD 把 008 定义为 004 的上游采集模块:负责完整、及时、省心地把单一顾问内容收进个人知识库,并通过 US6 给 004 一个轻量输出包。Scope OUT 明确不由 008 产生投资建议、买卖信号、仓位建议或收益判断。hand-back 则指出结构化数据的消费目标没有进入 PRD gate,导致第 2/3 层字段无法判断该不该提。

### 视角 B · 提取可靠性/可行性

hand-back 记录了红队判断:trader韭语料包含反讽、黑话、方言和免责声明,`stance_direction`、`conviction`、`action_type` 恰是跟单依赖字段,但目前没有本语料实测准确率。字典草稿也把 `stance_direction`、`conviction`、`author_tone` 从无悔层踢出,理由是反讽/语气判断中等易错,且错标会污染下游。

### 视角 C · 数据建模/字典设计

结构化字典经红队后收敛为三层:第 1 层无悔,包含 `asker`、双时间戳、`entity_type`、三值 `tech_side`、黑话词典;第 2 层赌用途,包含 stance/conviction/action/positions/priced_in 等;第 3 层结构关系,包括 sections、relations、cross_refs 和细粒度标注。作者约束已确认语料永远只来自 trader韭团队,所以黑话和方言可按单团队过拟合。

### 视角 D · 工程纪律

KG-24 是 manifest 状态语义不一致:下载断点续把已存在媒体标为 `skipped`,守护只认 `downloaded`,正牌 ASR 入口却认 `downloaded` + `skipped`,导致增量守护静默漏 ASR。KG-25 是 LLM 结构化提取直接 `json.loads(content)`,遇到稳定坏 JSON 无清洗、无降级、无可见告警,条目每轮失败且永久缺 summary。

## 2. First-take 评分(按 Y 视角)

| Y 维度 | 倾向 | 理由(引用 §1 现状) |
|---|---|---|
| 产品价值/用途成立性 | refactor | §1A 显示现 PRD 的正式价值闭环仍是采集与喂给 004,而 operator 新倾向的机器可信信号尚未成为明确定义的下游;不补用途,第 2/3 层字段继续悬空。 |
| 提取可靠性/可行性 | new | §1B 显示关键字段无本语料准确率,现有 C6/C9 只能保证可追溯,不能证明可半自动跟单;需要新增证据项,先拿真实错标率再谈可行性。 |
| 数据建模/字典设计 | keep | §1C 的三层划分已经把“信息价值高”和“现在无悔做”切开,尤其把 stance/conviction 踢出无悔层是正确的边界收敛;后续只需按用途挑第 2/3 层。 |
| 工程纪律 | refactor | §1D 的 KG-24/KG-25 都是静默失败族:共享状态没有单一契约,LLM JSON 没有鲁棒解析/降级/告警;这会直接削弱结构化链路可信度。 |

## 3. 我现在最不确定的 3 件事

1. 机器可信信号/跟单是否应归入 008,还是仍应由 008 只产可溯源证据包、004 消费后负责信号决策;P2/P3 需要把产品边界和责任链钉住。
2. 在单作者 trader韭语料里,LLM 对反讽、黑话、免责声明剥离后的 stance/action 准确率能达到什么数量级;我需要 P2 用外部证据判断“先 spike”是不是硬前置。
3. KG-24/KG-25 应优先作为 XenoDev 框架契约修复,还是只作为 008 结构化链路的局部加固;P3 需要决定它们进入最终 W 产出的粒度。
