# Forge v5 · 001 · P3R1 · Opus47Max · 联合收敛 R1(标分歧)

**Timestamp**: 2026-08-02T14:05:00Z
**Visibility**: 我已读对方 P1 + P2。
**Searches in this round**: 1 条**验证性**检索(不是发散 —— 是核对方 P2 推翻我 P2 负结果的那条,详见 §1)。

## 1. 整合摘要

**⚠ 先更正我自己 P2 的一处错误 —— 这是本轮最大的单条发现,而它来自对方。**
我 P2 §1 写了条负结果:「**没有检索到**任何工程先例把『gate 上线前先证明它能被满足』写成正式前置」。
对方 P2 §1 用 W3C / NASA / IEEE 29148 打了这一条。我**独立复核了 ISO/IEC/IEEE 29148**,
它**确实**把这件事定成了标准:个体需求的九特征里,**Feasible** = "realizable within the given
system constraints considering an acceptable risk";**Verifiable** = "**if and only if there exists
a process that can prove** that the system satisfies the specified requirement"。
⇒ **我的负结果错了,对方对。** 这正是跨模型对标该起的作用,如实登记。

**而且它比对方主张的还要强 —— 本仓那张「判据可达性族」清单是 ISO 29148 九特征的重新发明:**

| 本仓自造术语 | ISO 29148 既有特征 | 原文判据 |
|---|---|---|
| 结构/数学可达(KG-43 · T022 下界) | **Feasible** | 在系统约束与可接受风险内可实现 |
| 可判定 / 可复现(unlock-preflight) | **Verifiable** | 当且仅当**存在一个过程能证明**系统满足它 |
| **唯一可读性**(决议 35 (F) · 本仓视为方法论增量) | **Unambiguous** | "allows **only one** interpretation" |
| OQ-A1-1 悬空在 frozen spec 里 | **Complete**(集合级) | 完整集合"**no TBD, TBS, or TBR clauses**" |
| O7 缺起算点 | Verifiable + measurable | "verifiability is enhanced when the requirement is measurable" |

⇒ **K 的核心问题有现成答案,不必发明**:「判据冻结前必须先证明什么」= **证九特征**,
且 ISO 29148 明确区分**个体级**与**集合级**特征 —— 这一条直接落在 (c) 上:
(c) 是**集合级**属性(一份 briefing 里判断的集合),却被写成**每 run 必须自足**的个体级门。

**第二个整合点:双方 P2 从两条独立路径得到同一个 R4-F4 答案。** 我走 ISO 27001 5.3 /
compensating control(requester ≠ approver + expiry),对方走 **NIST RMF authorizing official**
(风险接受须有独立责任主体)。**两个互不重叠的合规体系给出同构结论**,且双方都**没找到**
支持「作者本地 allowlist 即合法例外」的材料。这是本轮**证据强度最高**的一条。

**第三:(c) 的挂点双方无分歧。** 我引 SPIRIT/临床(预先定累积规则 + 报 inconclusive + 可 pooling),
对方引 SPIRIT 2013 + Goodhart/OpenAI reward-model overoptimization,结论都是**挂验收侧、
不挂产出侧**。分歧只在**要不要现在就落第三值**(见 §3-2)。

## 2. 我的初步 verdict(草案)

**采「ISO 29148 九特征作为判据冻结前置」为 v5 主裁,12 项按它逐条归位;T040 立即以
warn+baseline 形态窄起跑,不等全部收敛。** 理由:(1) K 要的通用前置**已有国际标准**,
本仓不必自造术语,自造反而让四例看起来像四个偶发事故而非同一族;(2) 九特征自带
**个体级 / 集合级**二分,恰好是 (c) 挂错侧的诊断工具与修法;(3) R4-F4 有两套合规体系
同构背书(compensating control + 独立授权主体),可当场裁死不必留悬;(4) T040 的
warn+baseline 起跑是 ratchet 标准做法,与「不给未定规则焊牙」不冲突 —— **焊的是 baseline,
不是判据**。关键不确定点是 **OQ-A1-1 第三值现在落还是等**(§3-2);若 R2 证明落第三值会
连带改 CLI 退出码契约进而触 KG-B10 冻结面,我改为「先落 spec 语义、CLI 协议留 T041」。

## 3. 关键分歧清单

**分歧 1 · T040 窄起跑的正当性来源**
- **我的立场**:partial oracle(differential/metamorphic 只判输入子集)+ CI ratchet(warn → baseline diff → 只卡新增)**共同**构成明文先例,T040 可以现在就跑 warn。
- **对方立场**(P2 §3-3 / outbox):"partial T040 start is only an inference from scoped conformance/verification sources";并明说 **"no strong direct source for a named 'half gate can ship' doctrine"**。
- **我希望 R2 怎么收敛**:对方的检索没覆盖 **CI ratchet 族**(20 条里无一条搜 ratchet / baseline / warn-mode rollout),这不是「无先例」而是**未检索到**。R2 请对方就 ratchet 这一族表态:它是否构成明文先例。若对方仍判「仅推论」,我接受降级表述为「**scoped verification(W3C/NASA 明文)+ ratchet(行业实践,非标准条文)**」,但结论不变。

**分歧 2 · OQ-A1-1 第三值(`INSUFFICIENT_EVIDENCE`)现在落还是等**
- **我的立场**:**现在落 spec 语义层**。SPIRIT/临床那套三件套里,"report inconclusive" 不是可选项 ——
  缺了它,(c) 就只有「不得判 PASS」而没有「那判什么」,**判据不完整 = 违 ISO 29148 的 Complete
  (no TBD/TBS/TBR)**。⇒ OQ-A1-1 挂在 frozen spec 里本身就是一处标准违反。
- **对方立场**:P2 未直接表态落不落,但 P1 §3-3 说 "O2(c) 结果值与 C9 证明强度不该先焊牙"。
- **我希望 R2 怎么收敛**:区分**两层**——**spec 语义层**(非-PASS 有个名字)现在落;
  **CLI 退出码 / 产物状态字段协议**留 T041。请对方确认这个二分能否解掉它「不该先焊牙」的顾虑。

**分歧 3 · 产品价值 keep vs refactor(P1 起就在,P2 后收窄未消)**
- **我的立场**:refactor —— 可读性(消毒转义)× 判断密度(1 条低置信)**合流**打 PRD O1「信任第一块砖」,
  而 O7 要 operator 每周真读 5 次。
- **对方立场**(P2 §3-1):"product keep 站住但收窄 … P2 后应 **narrow PASS/hold**"。
- **我希望 R2 怎么收敛**:分歧其实比字面小 —— 对方从 keep 移到 narrow-hold,我从 refactor 出发,
  中点是「**O7 机制 keep,产物呈现面 refactor**」。R2 请把两件事**拆开表决**,不要合成一个词。

**分歧 4 · 对方 §4 自查末句的一处「解释掉」(方法层 · 我主动标)**
- **我的立场**:对方 §4 诚实列出覆盖缺口(「较少覆盖『强制多样本输出是否在某些评审系统中有效』」),
  但紧接着写 **"这不改变当前 verdict,因为 OpenAI Goodhart 与 SPIRIT 已足够反证单纯凑数"** ——
  **自己识别出的缺口被同句话消解**,这是 forge-config 反自欺条款点名的形态(009 forge v1 同型)。
- **对方立场**:如上引。
- **我希望 R2 怎么收敛**:不要求对方改结论(我也认为结论大概率对),**要求它把那句话改成
  「未检索,结论在此面上不设防」**。⚠ 同理我自陈:我 P2 §3-5 已登记自己一处「被解释掉」
  (post-hoc 定规则),**本条不是单向指摘**。

## 4. 与 K 的对齐性自检

- K「**判据冻结前必须先证明什么、挂哪一侧、由谁写、用什么词指称**」→ ✅ 四问在 R1 后各有归宿:
  证什么 = ISO 29148 九特征;挂哪侧 = 个体级/集合级二分((c) 归集合级=验收侧);
  由谁写 = 独立责任主体(NIST authorizing official / ISO 27001 5.3,**非申请人**);
  用什么词 = bounded context 各自限定 + RFC 6365 点名否决。
- K「**要能执行的裁决,不要正确的综述**」→ ⚠ **R1 尚未达标**。九特征是诊断框架,还没落成
  「spec 改哪一行」。R2 必须产出 12 项逐条施工单,否则本轮失败。
- K「**可达性判据本身要可达(防自指)**」→ ✅ 九特征是**清单式**判据(逐条问是/否),
  不是需要另证的元判据 —— 自指陷阱在采用既有标准后自动解除。
- K「**T040 若仍不能起跑,这场 forge 没解决主要问题**」→ ⚠ 取决于分歧 1+2 的收敛。
  我的方案能让它起跑;若 R2 采对方更严读法,T040 仍卡在 (c)。**这是本轮最关键的一票。**
- K「**每条裁决写成 A + 判据 + 证不出则 B**」→ ❌ **R1 未做**,R2 必须补齐 12 条 fallback 分支。
- K「**存疑偏向不放松,但只挂着不给可达路径 = 没裁**」→ ✅ 本 verdict 无一条放松既有门槛;
  (c) 从「单 run 自足」改「集合级累积」是**换挂点不是降门槛**,且给了可达路径。
