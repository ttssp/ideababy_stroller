# Forge v3 · 008 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-06-20T02:37:48Z
**Visibility**: 我已读对方 P3R1。
**Convergence mode**: strong-converge

## 1. 我对每条分歧的最终立场 + 让步

双方 P3R1 均判「无 reviewer 分歧」,所以本轮没有 unresolved 结构冲突。对方把 GPT P2 的关键句概括为“不是通用 HTTP 代理”,我完全接受;这比只说 daemon/runner 更准确,因为真正的安全闸是 capability-scoped connector。

两个待定点最终处理如下。**列表截断根因**:不阻塞 verdict;主路径按 cursor/next/checkpoint 自动翻页,若实测 API 物理截断,broker 白名单能力切到 detail 入口批量发现,凭据边界不变。**一键确认粒度**:接受 bounded capture batch 判准,每批确认一次;确认必须列源、时间窗/目标范围、端点集、请求预算、停止条件、落盘位置。定时任务只能来自 operator 预授权的固定 schedule/budget/kill-switch,agent 不得临时扩大。

## 2. 联合 verdict(单一)

**我和对方在 R2 后达成的单一 verdict**: **GO(分层架构)**。自动翻页可在「登录态绝不进 agent context」硬约束下落地:agent 只产可审计 declarative plan,operator 对 bounded capture batch 授权,隔离的 capability-scoped credential broker/runner 独占登录态(userDataDir/storageState),按端点/参数白名单抓取列表或 detail,落盘内容、分页 checkpoint 与脱敏日志;agent 只读落盘结果。①侦察兵保留为诊断/fallback。协议层 §2 新增「采集会话凭据隔离」子条款;§1 不动;C5 OUT 侧渠道中性 keep,只补 IN/OUT 边界说明。无 unresolved。

## 3. 残余分歧降级为 v0.2 note

- v0.2 note 1:列表截断根因仍需 L4 前实测。若没有 next/cursor/has_more 或 offset 越界显示服务端不返回 2026,执行目标切到 detail 入口批量发现。
- v0.2 note 2:确认粒度运行后复盘。若 batch 太粗导致 operator 无法理解授权范围,收紧预算/时间窗;若太细导致手动成本回升,引入固定预授权 schedule。
- v0.2 note 3:broker 日志必须默认脱敏,且 checkpoint 可审计,否则会把凭据或签名 URL 间接带回 agent context。

## 4. W 形态产出的初步草稿建议

### W1 · verdict-only

**GO**:采用分层自动翻页架构:③控制流(agent plan + operator bounded-batch 授权) + ②白名单 credential broker/runner 持 key 执行基座 + ①侦察兵/fallback。持 key 主体与 agent 物理隔离;broker 不是通用 HTTP 代理,只执行预定义源/端点/参数 schema/预算内请求。§2 补采集会话凭据隔离;§1 不动;C5 OUT 侧 keep。

### W2 · decision-list

| 类别 | 项 |
|---|---|
| keep | v0.1 被动监听;①侦察兵/fallback;C5 OUT 侧渠道中性;§1 PRD schema |
| refactor | ②从“daemon 自动翻页”改写为 capability-scoped broker/runner;③从“单次脚本”改写为 bounded-batch 控制流;PRD 采集架构补 IN/OUT 边界 |
| cut | agent 持 key/直接发请求;broker 盲转发任意 URL;无预算/无停止条件的开放式翻页;凭据/session 文件进入 agent 可读路径 |
| new | §2 采集会话凭据隔离子条款;端点/参数白名单;分页 checkpoint 落盘;operator batch 确认六要素;定时任务预授权 schedule/budget/kill-switch |

### W3 · 协议修订草案

**层级选择:协议级**,不是仅 008 项目级;理由是该边界适用于所有未来采集类项目。**§1 不改**,因为 PRD schema 无需新增字段。

建议在 SHARED-CONTRACT §2 件1 后新增:

> **采集会话凭据隔离**:任何代表 operator 已认证会话发起采集请求的 cookie/token/storageState/userDataDir 等运行时采集凭据,不得进入 agent context。若需主动采集,持凭据主体必须是独立 broker/runner,与 agent 物理隔离;agent 只能提交 declarative plan。broker/runner 必须执行端点/参数白名单、请求预算、停止条件、日志脱敏与可审计落盘,不得作为通用 HTTP 代理。

### W4 · next-PRD

PRD 需要小幅修订,不是重写 C5。建议在采集架构/关键前置 gate 增补:

> 自动翻页采用分层采集架构:agent 生成 bounded capture batch plan(源、时间窗/目标范围、端点集、参数 schema、请求预算、停止条件、落盘位置),operator 确认后由隔离 broker/runner 使用 operator 登录态执行;agent 不持 key、不发请求、只读落盘结果与脱敏 checkpoint。

C5 保持原义,追加一句边界:

> C5 渠道中性约束管采集后的 OUT 侧传播/同步;自动翻页属 IN 侧采集手段,仅限 operator 有权访问内容,且采集会话凭据不得进入 agent context。
