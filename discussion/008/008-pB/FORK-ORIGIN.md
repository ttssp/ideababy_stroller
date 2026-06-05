# Fork origin · 008-pB

**This fork**: 008-pB
**Forked by**: /fork-phased 008 from-L3 candidate-B as 008-pB @ 2026-06-04T02:14:35Z
**Source**: discussion/008/L3/stage-L3-scope-008.md · Candidate B「全形态 · 原始证据库」
**Selected candidate**: Candidate B
**PRD-form**: phased | Phases: [v0.1, v0.2]
**Approved by**: human moderator

## 为什么选 B(且为什么 phased)

operator 在充分知情下选 B(全形态),理由:**任何一种形态被漏都不可接受**,尤其直播回放里
是"重要消息 + 周度复盘 + 下周策略" = 决策价值最高的内容。双模型 L3R2 都判 B "ambitious and
brittle"(最高风险/最长工期/最低置信度),operator 接受这个代价,但选择 **phased 降风险**:
不在源头可达性未验时一次性下注,而是分阶段、用"能否稳定采"做 phase 门。

## ⚠️ 关键:phase 排序按"价值优先"而非"风险优先"

operator 明确选择 **v0.1 = 图文 + 回放,v0.2 = 加预警**(价值优先),而非原方案的
"v0.1 图文+预警 / v0.2 才加回放"(风险优先)。理由:回放价值最高(operator 亲自确认,
不再是 GPT R2 说的"假设"),最想要的不该最晚拿到。

**代价(operator 已知情)**:v0.1 直接包含整个项目最难的回放,放弃了"v0.1 先拿稳的"这个
phased 好处。补偿:回放的**价值风险已消除**(operator 确认),只剩**可行性风险**。因此那两个
L4 前置 gate(源头可达性 + 回放能否下载/转录)在本 fork 里**加重**——进 v0.1 主开发前必做探针。

## operator 的两条关键补充(2026-06-04,改变了 scope)

1. **直播回放处理意图**:回放是 1-2 小时视频,operator 没时间看完,但内含重要消息/周度复盘/
   下周策略展望。意图 = 下载视频 → 提取音频 → ASR 转文本 → LLM polish & extract key points,
   把 1-2 小时压成几分钟可消费的文字 + 关键点。
   - **product 级翻译写进 PRD**(how=ASR/LLM 留 L4):"系统把回放转成可几分钟消费的文字+关键点
     摘要,operator 不需看完整视频,且每个关键点能溯源原始内容。"
   - ⚠️ **这使 candidate B 原文的"回放存文件不转写"被 operator 意图覆盖** —— v0.1 的回放
     **要做到文字摘要**,不是仅存文件。PRD 按 operator 意图,非照抄 stage doc 原始 B。
   - ⚠️ **新增回放红线**:LLM 提取的关键点必须能溯源到原始转录文本,不让 LLM 发挥成 008 自己
     的观点(呼应"不产建议 + 原文可追溯")。

2. **资讯以文字为主、图片少**:图片是文字的补充(数据)、偶尔搞笑。→ 降低了"图文结构化成本
   爆炸"风险(文字好提取)。**图片 v0.1 只原样留存,不费力解析。**

## 继承自 L3 的硬约束(写进 PRD)

- ⭐ 合规硬红线(C5):~~只采 operator 正常登录、正常能看到的内容,绝不破解/绕过访问控制~~
  → **v1.1 已由 forge v1 重定**(2026-06-05):只采 operator **有权访问**的内容,可用**有效登录态采集原内容**
  (含须抓包),自用不传播,不规避**他人**访问控制。合规由 operator 负责。
  (探针「合规可达性」FAIL 被证伪;见 PRD v1.1 + discussion/008/forge/v1/stage-forge-008-v1.md)
- uncertain capture states 一等公民:采集失败/不确定显式可见,不静默丢失
- 单源 v0.1;原文可追溯(不为结构化牺牲原始留存)
- 008 = 004 的上游采集模块(不产投资建议;不二次分发顾问内容)

## 后续

- 本 fork 只产 PRD(L3→L4 fork 产物)。下一步 `/plan-start 008-pB` 产 HANDOFF.md → 切 XenoDev 真开发。
- 008 此前经 L2-skip 桥接进 L3,见 discussion/008/L2-SKIP-NOTE.md。
