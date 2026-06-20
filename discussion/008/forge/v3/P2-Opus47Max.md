# Forge 008 · v3 · P2 · Opus 4.8 Max(参照系评估)

**读取**:P1-GPT55xHigh.md(对方,新读)+ 自己 P1 + forge-config(refresh)。无 moderator-notes。
**搜索**:本轮跑 3 个 SOTA 检索(架构/凭据层,**未跑法律检索** per Z binding)。

## §1 · SOTA 对标(架构 / 凭据边界层)

| SOTA / prior-art | 关键事实 | 对本轮 3 候选向的含义 |
|---|---|---|
| **CyberArk Secretless Broker / HashiCorp Vault Agent sidecar / Infisical AI-agent credential brokering / MS Entra Auth SDK sidecar** | credential broker「拦截出站请求 → 注入凭据 → 转发上游」,使 app/agent「完成工作而**从不读取底层凭据**」;agent 容器经 localhost 与 sidecar 通信,sidecar 持 key 注入并转发,**agent 永不见 key**。 | **这是②/③背后的工业范式名字 = "secretless / credential broker"**。证明「持 key 主体独立、agent 不经手凭据」**不是新发明,是成熟模式**。**关键修正**:②(持 key daemon)不该被默认判为高负担 —— broker/sidecar 正是把「常驻持 key 进程」做成标准安全姿态(localhost-only、最小 scope、短期凭据)。问题从「②要不要」变成「broker 怎么挡 agent 滥用」。 |
| **Secretless 模式的「agent 完成工作不读凭据」边界** | broker 拦截**出站**;agent 只发「要访问什么」的意图,凭据由 broker 注入。 | 直接落到 Opus P1 §3#2 + GPT §3#1 的共同担忧:**agent 不持 key 易,agent 不能滥用持 key 进程难**。SOTA 答案 = broker 对**端点/参数白名单**(agent 的意图须落在预定义端点集),而非盲转发任意 URL。**这是协议修订草案必须钉的核心机制。** |
| **Playwright persistent context / `storageState` / 独立 `userDataDir`** | 认证态(cookie/localStorage/IndexedDB)存进独立 `userDataDir`,跨执行复用;browser context **隔离 cookie**,持 key 进程独占该 dir。 | ③的「持 key runner」有现成实现路径:runner 独占 `userDataDir`/storageState,登录态**物理上**只在 runner 进程,agent 读 runner **落盘**结果。把「被动性即隔离」从「operator 手动浏览」平移到「runner 持隔离会话翻页」,**隔离性质可保留**。 |
| **Cursor vs offset 分页 + 「无内建增量」铁律**(ProxiesAPI/Zendesk/Gusto/getknit 2026) | 「**没有内建增量机制** —— checkpoint/dedup 须自己设计」;offset 分页在数据变动时**会漏/会重**;`has_more`/空 `next` 标志末页;cursor 优于 offset(大/快变数据集)。 | **直接打 Opus P1 §3#1 + GPT §3#2 的共同根因缺口**:列表止于 2025-07-21 **是已知失败类**(offset 截断 / cursor 未续)。SOTA 命名了它,但**仍无法判定** 2026 项是「cursor 没翻到」(翻页能解)还是「列表 API 服务端不返回」(翻页也没用,只能 detail 批量发现)。**根因仍须实战数据澄清** —— 但 SOTA 给了诊断方法:看响应有无 `has_more`/`next_cursor` 字段、offset 越界返回空还是报错。 |

## §2 · 用户外部材料消化

K 未含外部链接/文件(议题主源已快照进 _external/,P1 已消化)。本轮无新增外部材料须消化。
重申 binding(SOTA 不松动这些):合规 operator 担责 / 凭据隔离不论证放宽 / v0.1·v0.2 不重审 / 只审架构与凭据边界。

## §3 · 修正后的视角(P1 哪些站住、哪些被推翻)

**站住的:**
- **③为主向**:P1 初判 ③(agent 出计划 → operator 确认 → 持 key 进程执行)是凭据隔离最干净的形态 —— SOTA
  的 secretless broker 范式从**工业侧印证**:agent 发意图、独立主体持 key、agent 不读凭据,正是被反复实现的
  标准姿态。GPT P1 独立同样落 ③ = 双盲一致。
- **§2 措辞须改**:双方 P1 + SOTA 一致 —— 现有「凭据隔离」字面只到 deployment secret,采集会话凭据须显式
  纳入。这是协议层真缺口,不是过度设计。
- **IN/OUT 正交**:双方 P1 都钉了,v2 渠道中性(OUT)不替代本轮采集侧(IN)判断。SOTA 无关此分界,保持。

**被 SOTA 修正/推翻的:**
- **⚠ 我 P1 对②(常驻 daemon)的「保留/倾向 cut-unless-forced」立场,SOTA 部分推翻**:我原担心「常驻持 key
  进程攻击面/生命周期/被诱导发请求」更重。但 credential broker/sidecar 范式**正是**把常驻持 key 进程做成标准
  安全组件 —— ②不该被判为劣于③的「一次性进程」。**新认识(向 GPT P1 收敛)**:②和③**不是对立选项,是一条
  管线的不同层**(GPT P1「同一能力的不同控制面」框架更准):**broker/runner(②的持 key 执行基座)是底座,
  ③的「agent 出计划 + operator 确认」是其上的控制面**。真正的 verdict 形态可能是「③的控制流 + ②的 broker
  执行基座 + ①的侦察兵作诊断/fallback 层」三者**分层组合**,而非三选一。这是 P3 要收敛的核心结构。
- **broker 防滥用机制从「未知」升为「有 SOTA 答案」**:P1 §3#2「agent 不能滥用持 key 进程」当时是开放问题;
  SOTA 给出标准解 = broker 对端点/参数**白名单**(agent 意图须落预定义端点集)。这条进协议修订草案。

**残留未解(P3 须处理):**
- **列表截断根因**(分页未尽 vs API 物理截断)SOTA 命名了失败类但答不了具体根因 —— 仍须 operator/实战数据。
  这直接决定①侦察兵能否够到列表、以及翻页(②/③)是否对 2026 有效。**verdict 须对两种根因都给路径**
  (若分页未尽 → cursor 翻页;若 API 截断 → detail 入口批量发现),strong-converge 下可作主路径 + 条件分支。
- **一键确认粒度**(GPT §3#3):太粗近似全自动、太细回到手动,影响 O5b 单一恢复路径是否成立。SOTA 未覆盖
  (属产品/UX 粒度),P3 须给判准。
