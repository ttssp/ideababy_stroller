# Forge v3 · 008 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-06-20T01:42:58Z
**Searches run**: 8 targeted SOTA-benchmark lookups; 6 usable sources.
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| 自动翻页持 key 主体 | CyberArk Secretless Broker | broker 作为本地连接代理,client 不直接接触目标服务密码;凭据由 broker/credential provider 取用,connector 负责协议适配。含义:②不是“agent 直接发请求”,而是 credential broker 基座。 | ② daemon 可类比 broker,但必须只暴露特定 moduleContentList/detail 连接器,不能做任意 URL 转发。 | 当前候选没有写“connector/端点白名单”;这是防 agent 滥用持 key 进程的核心缺口。 | https://github.com/cyberark/secretless-broker |
| 自动翻页持 key 主体 | HashiCorp Vault Agent | agent daemon 做 auto-auth、token renewal、caching/template,并提醒某些本地 API 要只放在可信接口。含义:持 key 进程独立、可更新凭据、可审计,是成熟范式。 | ② daemon 可负责登录态生命周期;③控制面不能拿到 token,只提交计划。 | Vault Agent 是 secret delivery,不是任意业务请求执行器;008 仍需业务白名单和落盘契约。 | https://developer.hashicorp.com/vault/docs/agent-and-proxy/agent |
| 认证会话隔离 | Playwright auth + persistent context | Playwright 建议把 authenticated state 存文件且不要提交;persistent context 使用独立 userDataDir 保存 cookie/localStorage,并建议不要自动化默认浏览器 profile。含义:持 key runner 可独占自动化 profile。 | ③可把 cookie 留在 runner 的 userDataDir/storageState,agent 只看计划和输出。 | 若 agent 能读 userDataDir/storageState,隔离失败;必须用文件权限/路径 deny 和日志脱敏兜住。 | https://playwright.dev/docs/auth ; https://playwright.dev/docs/api/class-browsertype#browser-type-launch-persistent-context |
| 分页抓取失败模式 | Stripe v1 pagination | cursor 用 `starting_after`/`ending_before`,响应用 `has_more` 标末页。含义:自动翻页必须以服务端末页信号停止,不是硬猜页数。 | ③计划可给起点和上限,但 runner 应按响应 checkpoint 驱动。 | moduleContentList 是否有等价 cursor/has_more 未知;没有就只能保守增量探测。 | https://docs.stripe.com/api/pagination |
| 分页抓取失败模式 | Microsoft Graph paging | 服务端返回 `@odata.nextLink`;文档强调整条 nextLink 继续请求,分页行为随 API 变化,重试 token 不可误作后续 token。含义:分页 checkpoint 要保存“最后成功响应”的 next/cursor。 | ②/③都必须把 cursor、页边界、重试来源落盘,供 agent 只读审计。 | 当前三候选没有显式 checkpoint/重试语义;这是 silent gap 风险。 | https://learn.microsoft.com/en-us/graph/paging |
| agent 工具边界 | MCP security research | 研究把 tool 调用链的信任边界、capability access control、runtime policy 作为防线。含义:agent 不持 key 只是第一层,还要限制能力。 | ③的 plan 应是 capability-scoped intent:固定源、端点、参数 schema、预算上限。 | 需把“白名单 broker 不盲转发”升成可验条件。 | https://arxiv.org/abs/2604.05969 |

## 2. 对方 P1 + 外部材料消化

K 无新增外部链接。本轮主要消化 Opus P1 与我的 P1 的异同。

Opus P1 强点有三处。第一,它把当前半自动命名为「被动性即隔离」,比我 P1 的“agent 只读落盘”更准:旧架构靠 agent 没有发请求能力。第二,它指出 §2 件1 未字面覆盖采集 cookie,所以 v3 应补采集会话凭据子条款。第三,它提出③为主、①兜底,并担心②常驻 daemon 生命周期和被诱导执行任意请求。

我与 Opus 的差异在于②的定位。我 P1 把②看成执行基座,③看成控制面;Opus 更倾向③一次性 runner。SOTA 后我认为二者可合并:②不是“全自动常驻产品形态”,而是 credential broker/runner 基座;③是计划与确认控制流;①是诊断/fallback 层。

需要明确反驳一个可能误读:broker/sidecar 并不天然安全。如果它只是把 agent 给的任意 URL 加 cookie 转发,那只是把 key 从 agent context 移到一个可被 agent 滥用的代理里。SOTA 支持的是协议连接器、端点白名单、能力范围和审计,不是通用 HTTP 代理。

## 3. 修正后的视角

- P1 判断“③是一阶主向” → **站住但需改写**。SOTA 支持 agent 出 declarative plan、operator 确认、隔离进程执行;但③不应孤立存在,它需要②式 broker/runner 作为持 key 执行基座。
- P1 判断“②应是执行基座,不是单独 verdict” → **站住并增强**。Secretless/Vault Agent 坐实“凭据由独立主体管理”是成熟范式;但必须从“daemon 自动翻页”重述为“白名单 credential broker/runner”。
- P1 判断“agent 不持 key 还不够,要防滥用持 key 进程” → **站住并升格为核心 gap**。SOTA 的 connector/能力控制说明 broker 不能盲转发;白名单端点、参数 schema、请求预算、落盘 checkpoint 是 P3 必须收敛的边界。
- P1 对“C5 / PRD 配套 refactor”的表述 → **部分修正**。C5 OUT 侧渠道中性继续 keep;本轮更应补的是 IN 侧采集架构约束与 §2 采集会话凭据隔离,不是重写 C5。
- 对 orchestrator 的“分层组合 vs 单一候选” → **接受分层组合框架**。我的 P2 立场是:最终 verdict 不应三选一,而应定为 **③控制流 + ②白名单 broker/runner 基座 + ①侦察兵/fallback**。若 strong-converge 需要一句话,就是“agent 只产可审计计划,operator 授权,隔离 broker 按白名单抓取并落盘,agent 只读结果”。
