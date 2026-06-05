---
forge_version: v1
created: 2026-06-04T12:09:28Z
convergence_mode: strong-converge
x_hash: 544bd175721e166e0caec2e75a4a325f
prefill_source: proposals.md§008
---

# Forge Config · 008 · v1

## X · 审阅标的

本轮 forge 由 `/handback-review 008` 决议触发:008-pB Phase 0 探针判定 FAIL(回放「合规下不可达」)被 operator 证伪。operator 澄清两条事实:(1) 图文采集原内容与回放一样都需抓包,探针「图文合规可达」是把「浏览/截屏」误当「采集」;(2) C5 红线判定错误 —— 实际采集手段 = 付费订阅用户 · 有效登录态抓自己合法流量 · 自用不传播,**非**复用过期 token 规避访问控制。详见 handback 包 + HANDBACK-LOG.md。

审阅标的(供双专家定位 C5 措辞的来龙去脉):

- `discussion/008/008-pB/PRD.md` —— 现行 PRD,C5 在 §"Real-world constraints" line 116,scope/outcomes/gate 上下文
- `discussion/008/L3/L3R2-Opus47Max.md` —— C5 措辞的 source(§2 SOTA 检索 + §"合规红线收紧措辞",line 22-28 是 C5 over-broadening 的发生点:把「自动化我自己的眼睛」从法律安全隐喻收成了字面「只采视觉可见」)
- `discussion/008/handback/20260604T095517Z-008-pB-20260604T095517Z.md` —— XenoDev 探针 hand-back 包(被证伪的 FAIL 论证 + reachability 判定)
- `proposals/proposals.md` §008 —— operator 原始意图(痛点 = token 过期要重登录;意图 = 个人留存付费订阅内容)

### 解析后的标的清单

- discussion/008/008-pB/PRD.md(类型:本仓库文件 · ✅ 可达)
- discussion/008/L3/L3R2-Opus47Max.md(类型:stage 文档 · ✅ 可达)
- discussion/008/handback/20260604T095517Z-008-pB-20260604T095517Z.md(类型:本仓库文件 · ✅ 可达)
- proposals/proposals.md §008(类型:本仓库文件 · 只读 §008 段 line 250-275 · ✅ 可达)

## Y · 审阅视角

✅ 产品价值 —— 唯一视角

> ⚠ **operator 显式姿态(binding · 见 K)**:合规/法律定性**不是本轮 forge 的审议对象**。operator 已对采集手段的合规性拍板并承担责任。双专家**不得**跑去论证 DMCA§1201/CFAA、不得劝阻、不得把「这可能违法」当审阅结论。把合规当**已决前提**输入,只从产品价值审。

## Z · 参照系

mode: 不对标

> Phase 2 **不跑法律检索**(合规由 operator 负责,非 forge 审议对象)。双专家若在产品价值层需要对标个人内容采集/知识库沉淀类产品(如 Readwise / 笔记类),可在 Phase 2 自行轻量判断,但**不强制**、**不得跑法律判例检索**。

## W · 产出形态

✅ verdict-only —— verdict + 简短 rationale
✅ decision-list —— 4 列矩阵(保留/调整/删除/新增),聚焦 C5 措辞 + 受 C5 影响的 scope 项
✅ next-PRD —— C5 重定后的 PRD 修订草案(可进 /scope-inject 或新 PRD 版本)

## K · 用户判准

**核心问题**:在「C5 不再卡死抓包」这个**已由 operator 拍板的新前提**下,008 的产品形态 / scope / 自动化挑战该怎么定?

**binding 前提(双专家必须接受,不得审议)**:
- **合规边界由 operator 负责**。新 C5 = operator 作为付费订阅用户,用有效登录态抓自己合法请求返回的内容(图文/回放原文件)直接留存,自用不传播。这**不是**复用过期 token 规避访问控制。operator 已就此合规性拍板并承担法律责任。
- 因此原 C5「只采正常登录、正常能看到的内容,绝不破解/绕过访问控制」中,**「正常能看到」不等于「视觉可见/截屏」** —— 它的本意是「operator 有权访问的内容」。抓包拿自己有权访问的原文件**在 C5 内**。
- 探针原 FAIL 结论(回放不可达)**作废**:回放与图文在新 C5 下**均可达**(技术上都靠有效登录态抓包)。

**operator 最在乎的(产品价值层,这才是双专家该审的)**:
1. **自动化程度** —— proposals.md §008 的真痛点:token 会失效 → 每次要重新登录,很麻烦。operator 想要「最小化我的操作」。新 C5 解锁了「抓包可达」,但「token 失效后怎么少操作 / 趋近无感」仍是 008 的核心产品挑战。这条独立于合规,是纯产品/工程价值问题。
2. **回放是 008 的最高价值内容**(含重要消息 + 周度复盘 + 下周策略),必须获取。原「图文先走、回放移 v0.2」的退路因 C5 证伪而**不成立** —— 不该再把回放当 v0.2 backlog。
3. **三形态不漏**(图文 + 回放 + 预警)是终态;v0.1 价值优先含回放。
4. 原文可追溯、不产投资建议、单源、个人自用 —— 这些 PRD 既有约束(C4/C6/C8/C9)**不变**。

**不关心 / 不要双专家做的**:
- 不要论证法律(operator 负责)。
- 不要劝阻 operator 改 C5。
- 不要重新质疑 008 的 candidate 选择(B 已定)或 phase 排序(价值优先已定)。

**贯穿 context**:本轮 forge 的产出会回流改 PRD C5 措辞 + 解锁探针 gate(回放放行)+ 可能让 XenoDev 按正确 C5 理解重跑探针。verdict 应直接给「C5 该怎么重写 + 受影响的 scope 项怎么调」。

## 收敛强度

✅ strong-converge

---

## Summary for reviewers

**审阅标的总数**: 4(PRD / L3R2-Opus C5 source / handback 包 / proposals §008)
**视角维度**: 仅产品价值(合规由 operator 负责,binding 前提,非审议对象)
**参照系**: 不对标 — Phase 2 不跑法律检索;产品价值层可轻量对标个人采集/知识库类产品(非强制)
**预期产出**: verdict-only + decision-list(聚焦 C5 措辞 + 受影响 scope)+ next-PRD(C5 重定草案)
**用户最在乎**: 新 C5(抓包可达,operator 负责合规)前提下,008 产品形态/scope 怎么定 —— 尤其「token 失效后如何最小化 operator 操作」这个核心自动化挑战,以及「回放是最高价值、不可移 v0.2」。不要论证法律、不要劝阻、不要重审 candidate/phase。
**收敛模式**: strong-converge — 必须给单一 verdict(C5 该怎么重写 + scope 怎么调);残余分歧降级 v0.2 note
