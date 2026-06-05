# Idea 008 · L3R1 · GPT-5.5 xhigh · Scope (no search)

**Timestamp**: 2026-06-04T00:23:47Z
**Inputs read**: `proposals/proposals.md` §008, `discussion/008/L2/stage-L2-explore-008.md`, `discussion/008/L2-SKIP-NOTE.md`, `discussion/008/L3/L3R0-intake.md`, `.claude/skills/scope-protocol/SKILL.md`, `AGENTS.md`
**Searches used**: NONE in this round
**Visibility**: did NOT read other debater's L3R1

## 0. How I read the intake

我把 008 读成 004 的上游数据采集模块,不是独立工具,也不是投资助手本体。human 的优先级非常清楚:不漏 + 省心 > 快速上线 / 简单 / 低成本。因此 v0.1 不能用"偶尔手动补一下"来换小 scope,但也不能因为追求全自动而把 008 做成通用采集平台。本轮应钉住四件事:一个顾问、哪些内容形态、知识库深度、给 004 的输出约定。最大未决项是采集落点;它虽然带有运行场景含义,但在 L3 已经变成产品 scope 前置条件,必须在 L4 动手前拍板。

- Hard constraints I'm respecting: 永久自用; 008 服务 004; 2-3 个月、每周 15-30 小时; 不漏和省心最高优先; 不做投资建议; 不二次分发顾问内容。
- Unknowns I'll propose options for: 采集落点; v0.1 内容形态; 知识库深度; 004 输出约定。
- Red lines I'll honor: 只采集沉淀,不决策; 仅个人留存; 不公开、不转售、不转发顾问内容。

## 1. Candidate A · "图文 + 预警完整留存"

### v0.1 in one paragraph

v0.1 专注收齐顾问每天的盘前 / 盘后图文分析和盘中关键预警,并沉淀成按时间线可回看、可检索、可交给 004 消费的个人知识库。直播回放不进入 v0.1 的完整采集范围,最多只记录"有一场直播回放发布了"这类提醒。这个 cut 的立场是:先把最影响日常决策节奏、最容易漏、最常用的文字与预警内容守住。

### User persona

operator 自己:有投资顾问订阅,工作日不能持续盯微信小程序,但晚上或周末愿意集中复盘,并希望 004 未来能引用顾问观点作为一个输入来源。

### Core user stories

- As the operator, I can see today's collected advisor posts in chronological order so that I know whether anything important was missed.
- As the operator, I can review intraday alerts after work so that time-sensitive advisor messages are not lost.
- As the operator, I can search past advisor analysis by date, content type, and mentioned topic so that I can revisit what the advisor said.
- As the operator, I can hand a clean daily collection to 004 so that 004 can use advisor content without mixing it with unrelated sources.

### Scope IN

- 单一指定顾问的信息源。
- 盘前 / 盘后图文分析的完整留存。
- 盘中关键预警的完整留存和醒目标记。
- 时间线浏览、基础检索、内容类型区分。
- 面向 004 的最小栏目约定:发布时间、内容形态、原始内容、涉及主题 / 标的、采集状态。

### Scope OUT

- 不完整采集直播回放;直播只做存在性记录。
- 不支持多个顾问或多个平台。
- 不生成买卖建议、仓位建议、收益判断。
- 不追求秒级提醒;目标是合理延迟内不漏。
- 不做深度观点归因或自动复盘评分。

### Success looks like

- 连续 2 周内,operator 认为图文分析和盘中预警没有漏收。
- operator 每天用 10 分钟以内确认当天顾问内容是否收齐。
- 004 可以稳定拿到一份边界清楚的顾问内容集合,且不会误认为 008 在给投资建议。
- 每条内容都能回到原始顾问表达,避免二次改写污染。

### Honest time estimate under human's constraint

- 在每周 15-30 小时、2-3 个月窗口内,这个 cut 约 6-8 周。
- Confidence: M。最大不确定性不是内容范围,而是采集落点能否同时满足不漏和省心。

### UX principles

- 完整性优先于漂亮展示。
- 原文可追溯优先于自动总结。
- 每天确认状态要低摩擦,但不需要做成面向外部用户的产品。
- 任何不确定内容都标为"待确认",不要静默丢弃。

### Biggest risk to this cut

如果盘中预警只能在某个特定微信场景里稳定出现,而最终落点又选了不可靠的运行场景,这个 cut 会直接违背"不漏"。因此它必须先解决"顾问图文与预警到底从哪里算正式出现"的问题。

## 2. Candidate B · "全形态原始档案"

### v0.1 in one paragraph

v0.1 覆盖顾问发布的三类内容形态:盘前 / 盘后图文、盘中预警、直播回放。它不追求把所有内容立刻结构化,而是优先保证每一种形态都有原始留存、发布时间线和可回看入口。这个 cut 的立场是:既然 human 最怕漏,那 v0.1 先把顾问内容生态完整装进个人档案,之后再让 004 慢慢消费其中最有价值的部分。

### User persona

operator 自己:不仅需要日常分析和预警,也担心直播回放里有长期观点、组合逻辑或口头补充,希望以后复盘时不因为 v0.1 切太窄而丢历史。

### Core user stories

- As the operator, I can open one archive and see every advisor content item published during a period so that I have a complete history.
- As the operator, I can distinguish text analysis, alerts, and replay items so that I know what kind of review each item needs.
- As the operator, I can mark which replay items I have watched so that long-form content does not disappear into a backlog.
- As the operator, I can preserve original advisor materials for personal review so that later 004 work can be grounded in the source.

### Scope IN

- 单一顾问的图文分析、盘中预警、直播回放三类形态。
- 所有内容按发布时间进入统一时间线。
- 原始留存优先,每条内容记录来源、形态、标题 / 摘要性描述、采集状态。
- 基础检索和回看状态管理。
- 给 004 的输出先以"原始档案 + 最少元信息"为主。

### Scope OUT

- 不要求直播内容在 v0.1 被完整整理成观点台账。
- 不做自动投资结论。
- 不做跨顾问比较。
- 不保证所有长内容都被当日消费。
- 不把知识库做成研究报告生产工具。

### Success looks like

- 连续 2 周内,operator 能在一个地方看到顾问三类内容的完整发布历史。
- 直播回放不会因为形态重而被漏记。
- operator 可以区分"已看 / 未看 / 待确认"内容,减少心理负担。
- 即便 004 暂时只消费部分内容,008 也保留了以后可追溯的原始材料。

### Honest time estimate under human's constraint

- 在每周 15-30 小时、2-3 个月窗口内,这个 cut 约 9-12 周。
- Confidence: L-M。范围符合 human 的"不漏"偏好,但三种内容形态会显著放大落点风险和验收复杂度。

### UX principles

- 档案完整性优先于结构化深度。
- 长内容可以先进入 backlog,但不能消失。
- 状态要诚实:已收、待确认、未能确认要分开。
- 用一条统一时间线降低 operator 回看成本。

### Biggest risk to this cut

这个 cut 很容易把 v0.1 变成"什么都要收一点",但每一种形态都不够稳。若采集落点对直播回放天然不友好,全形态承诺会拖累图文与预警这两个更高价值场景。human 选择它,等于接受更长验收周期和更高失败概率。

## 3. Candidate C · "004 友好观点台账"

### v0.1 in one paragraph

v0.1 覆盖图文分析和盘中预警,但比 Candidate A 更重视让 004 消费:每条内容除了原始留存,还要形成轻结构化台账,包括时间、形态、涉及标的 / 主题、顾问原话要点、情绪或倾向的原文依据。直播回放不做完整采集,除非其中明确出现 operator 关心的标的或主题。这个 cut 的立场是:008 既然一开始就是 004 模块,就不只是收纳箱,而是要提供干净的顾问观点输入层。

### User persona

operator 自己:已经有 004 作为下游,希望顾问内容不只是被保存,而是能比较快地进入个人投资研究流程,同时又不能让 008 自己越界做建议。

### Core user stories

- As the operator, I can inspect each advisor item with its original text and lightweight labels so that I know why 004 may use it.
- As the operator, I can filter advisor content by mentioned stock or theme so that I can connect it with my watchlist.
- As the operator, I can separate advisor-stated claims from my own interpretation so that 008 does not become an advice generator.
- As the operator, I can send a daily advisor-content ledger to 004 so that downstream reasoning has clean provenance.

### Scope IN

- 单一顾问的图文分析和盘中预警。
- 原始内容留存 + 轻结构化台账。
- 标的 / 主题 / 内容形态 / 发布时间 / 顾问原话要点。
- 对 004 友好的日度或周度内容包。
- 人工可快速校正的"不确定标签"。

### Scope OUT

- 不做直播回放完整采集。
- 不自动判断顾问观点对错。
- 不把顾问内容转化为买入 / 卖出 / 持有建议。
- 不做深度知识图谱或多源融合。
- 不为了结构化牺牲原始内容完整性。

### Success looks like

- operator 能按标的或主题找到过去顾问原始观点。
- 004 拿到的是"顾问说了什么"而不是"008 建议做什么"。
- 每个结构化字段都能回到原文依据。
- 连续 2 周内,图文和预警内容没有漏收,且关键内容能进入台账。

### Honest time estimate under human's constraint

- 在每周 15-30 小时、2-3 个月窗口内,这个 cut 约 8-11 周。
- Confidence: M。它比 A 更有 004 价值,但结构化质量和合规边界要小心,否则容易越界。

### UX principles

- 来源优先:任何标签都不能脱离顾问原话。
- 下游友好优先于展示丰富。
- 允许"未知 / 待确认",避免过度自信地解释内容。
- 结构化只服务检索和复盘,不服务投资建议生成。

### Biggest risk to this cut

轻结构化会诱导系统开始解释顾问观点,这可能越过"采集"边界。必须把台账定义为 provenance 和检索辅助,而不是判断层;否则 008 会和 004 的职责混在一起。

## 4. Options for the human's ❓ items

### ❓ 采集落点 / 运行场景（动手前必答 + 高风险）

1. **本机常驻**:scope 最小、operator 最容易理解,但只要本机关机、断网或不在状态,就可能漏。若 human 坚持"不漏",本机只能作为辅助,不适合作为唯一承诺。
2. **云 / 服务器常驻**:最符合 7x24 和省心目标,但前提是它能稳定接触到顾问内容。scope 含义是:L4 前必须先做源头可达性验证;若不成立,不要硬做。
3. **手机 / 微信贴源**:最贴近顾问内容出现的位置,可能最有机会不漏,但 operator 维护负担可能最高。scope 含义是:把一台手机或微信使用习惯纳入产品流程,并明确什么操作算可接受。

### ❓ 哪些内容形态进 v0.1

1. **图文 + 盘中预警**:推荐给 A / C,价值密度高,更容易验证不漏。
2. **图文 + 预警 + 直播回放存在性记录**:折中,直播不漏记但不承诺完整整理。
3. **三类全进**:对应 B,最符合"完整历史",但最容易把 v0.1 推到 3 个月边缘。

### ❓ 知识库深度

1. **原始时间线**:最稳,适合 B 的全形态档案。
2. **原始留存 + 轻标签 / 检索**:适合 A,兼顾复盘与低越界风险。
3. **004 友好观点台账**:适合 C,下游价值最高,但必须严守"不解释成建议"。

### ❓ 008 输出给 004 的约定

1. **最小内容包**:发布时间、形态、原始内容、采集状态。
2. **轻结构化内容包**:在最小内容包上增加标的 / 主题 / 顾问原话要点。
3. **暂缓深约定**:只在 B 可接受,因为 B 的目标是保全档案;但即便暂缓,也应保留以后给 004 使用的基本栏目。

## 5. Proposed red lines

intake 已明确两条硬红线:不产生投资建议 / 买卖信号;不二次分发或公开顾问内容。我建议 human 再确认以下软红线是否升为 v0.1 硬边界:

1. **v0.1 只支持一个指定顾问**。008 是 004 的模块,不是通用采集器。
2. **不为了结构化牺牲原始留存**。原文丢失会破坏复盘和合规边界。
3. **不承诺毫秒级实时**。008 追求不漏和省心,不是交易提醒系统。
4. **不把顾问观点自动改写成 operator 的投资立场**。任何二次表达都必须能回到顾问原话。

## 6. Questions needing real user interviews

008 是自用项目,这里的"用户访谈"主要是 operator 自我确认 + 源头实测:

- 连续 1-2 周观察顾问实际发布节奏:盘前、盘后、盘中、直播各占多少,漏哪个最痛。
- operator 能接受的延迟是多少:盘中预警是 5 分钟、30 分钟、还是当日收齐即可。
- 直播回放的真实价值:是否经常包含图文没有的关键观点,还是 mostly nice-to-have。
- 哪些字段对 004 真有用:标的、主题、时间、原文要点、还是只要原始内容即可。
- operator 可接受的维护动作:每天一次确认、每周一次检查、还是必须完全无感。
- 顾问订阅条款中个人留存的边界:哪些内容可以私用保存,哪些动作会触碰分发或版权风险。
