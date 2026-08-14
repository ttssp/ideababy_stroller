# P2 · Opus · forge 009-pM3prime v4

**Phase 2 · 参照系评估(Z = 对标 SOTA)**

---

## 🔴 §0 检索能力声明(必须先读 · 影响本轮全部结论的可信度)

**本轮我这一侧的 `WebSearch` 在环境层故障**(后端返回
`400 output_config.effort 'xhigh' is not supported when thinking is disabled`,连试三次,与查询内容无关)。
`WebFetch` 正常。⇒ 我的实际检索通道被削减为:**arXiv 结构化 API 查询 + 对已知 URL 的定向抓取**,
**没有开放网关键词发现能力**。

**这对 Z 的实质影响,不得被后续环节忽略**:
1. 定向抓取意味着「我只找到我已经猜到它存在的东西」—— 这**本身就是 K 点名警告的回声室形态**,只是换了个入口;
2. 故本轮**我无法承担「双方零重叠检索」中属于我的那一半保证**。v2 之所以能破回声室,靠的是双方各自
   **发现**了对方没想到的文献。本轮该机制在我侧只剩一半。
3. ⇒ **正交面的保证本轮主要落在 Codex 侧 P2**;若 Codex 侧 P2 的检索面与我高度重叠,
   **本轮的 SOTA 对标应被降级看待**,不得当作已完成的外证据检验。

已跑 **6 条**检索(4 条 arXiv API + 2 条工业文档定向抓取),**其中 3 条是否定性结果**。

---

## §1 SOTA 对标

| # | 检索面 | 关键发现 | 对哪一题 |
|---|---|---|---|
| 1 | 标注不一致是否为信号 | **5 篇一致主张 disagreement 是 signal 不是 noise**。NUTMEG(2025-07)「variation should be treated as **signal** rather than noise」,保留系统性分歧的聚合法训出的模型**显著优于**传统聚合;Hate-speech(2026-06)「**filtering non-consensus samples results in over-optimistic results**」;CrowdTruth 2.0 主张分歧揭示的是**歧义**而非错误;Perspectivist(2026-01)记录了从 consensus learning 转向显式建模分歧的整体转向 | **①④(重)** |
| 2 | 多数票聚合与信度 | 多数票确能抬一致率(CODA-19 crowd-vs-expert κ=0.741 逼近专家间 0.788),但 ACORN(2024-05)发现 LLM 与**多数票人类评分**的相关性**不稳定**,不足以替代;CrowdTruth 实证「以分歧度量优于多数票聚合」 | ①④ |
| 3 | 校准节奏:定期 vs 触发 | **drift-triggered 明显占优**(5/8 篇)。但 **LEAF(2023-02)反向警告**:「frequent model retraining with newly available data is **not sufficient** to mitigate concept drift, and **can even degrade** model accuracy further」;**#7(2026-07)**:最优策略「depend critically on the **aging properties** of concept durations」,且「**intuitive heuristics are provably suboptimal**」 | **③(推翻我 P1 的确定度)** |
| 4 | ML pipeline provenance 最小充分集 | **否定性结果** —— 5 篇 provenance/reproducibility 文献**无一**定义「哪些记账必须挺过事务回滚或进程崩溃」。**SOTA 不提供这个答案** | **②(重要)** |
| 5 | OPA Gatekeeper `dryrun`→`warn`→`deny` | **否定性结果** —— 三档强制形态齐备,但文档**不给任何晋级判据**:只说 dryrun「allows constraints to be tested without enforcing」,**stops short of prescribing what data or conditions should trigger promotion to deny** | **④** |
| 6 | Chrome/Blink 弃用→移除 | **否定性结果且更强** —— 官方原文:「Use counter data: Try to estimate how many users would be inconvenienced. **There is no threshold for which removal is necessarily safe.**」改为规定**过程量**:最少 1 个 milestone 观察期、Deprecation Trial 典型 6 个 milestone、跨引擎协调、与历史移除案例对照 | **④(决定性)** |

**7 · 我期待有支撑却没拿到的**:预注册 / 空结果强制申报。arXiv 侧不但没给我要的规范权威,
还给了**反向意见** —— 「Does preregistration improve the credibility of research findings?」(2020-10)
论证预注册的收益被高估、「contemporary transparency」(开放数据/材料/代码)比预注册本身更重要;
另一篇指出「preregistration **may increase** publication bias」。⇒ **我不能用「预注册要求申报空结果」来支撑议题①。**

---

## §2 用户外部材料消化

K 未给外部链接/文件。K 内嵌的两条实质材料已在 P1 消化:
(a) 四题的边界(不解锁 E2 / 41 条 CLOSED / 不改 C6 数字);
(b) 回声室 binding 警告 —— 本轮 §0 已按其判据自评为**部分失效**,并如实上报而非绕过。

---

## §3 修正后的视角

### 站住的

- **③ 事件触发优于日历**:drift 文献 5/8 支持,方向站住。
- **④「给形态,不给数字」**:**三个独立工业先例(OPA / Chrome / 加上仓内已有的 PEP 387、RFC 1589)全部不给数字阈值**。
  Chrome 甚至明写「没有一个阈值使移除必然安全」。⇒ K 这条要求不是本仓的偏好,是成熟弃用流程的**共同形态**。

### 被推翻或必须修正的

**(a) 🔴 最重的一条:M1=pass 的方向性,比 v3 契约说的更不中性。**
v3 说 pass「不证明效度」——对,但**太弱**。检索面 1+2 的一致主张是:**一致率上升本身无法区分
「噪声被去掉」与「歧义被抹掉」**,而后者是**已知的效度危害**(「filtering non-consensus samples
results in over-optimistic results」逐字对应我们的 M2 留存口径)。
⇒ 准确表述应为:**M1=pass 是朝一个已知效度风险方向的弱证据**,不是中性的好消息。
这**直接改写议题①的裁决内容** —— pass 的显式裁决不能只写「不解锁 E2」,必须写明该读数携带的方向性风险,
否则它在语料里会以「聚合更好」的形态留存。⚠ 我 P1 完全没有这一层。

**(b) 我 P1 ③「按事件定」的确定度被打掉一截。**
drift #7 明说「intuitive heuristics are **provably suboptimal**」,而「按事件」正是一个 intuitive heuristic;
最优策略取决于 concept duration 的 aging properties —— **我们没测过那个**。
LEAF 更警告「更频繁地重训**可能反而更差**」。
⇒ 修正:事件触发的**方向**保留,但不能声称最优;且须补一条 Chrome 式的**过程量** ——
观察期以**被消费的批次**为单位计数(本仓无自然时钟,批次是唯一真实节拍),而不是天。
**这与 Codex P1 ③ 提的「每个被消费的新比较批次到期一次」在形态上撞上了**(我们各自独立到达)。

**(c) 我 P1 ④「判据形态在仓里已经存在」只对一半。**
仓里(PRD §6 条件 2)有的是**结果型**判据(噪声量级 < 阈值裕度);三个工业先例给的是**过程型**判据
(观测时长 + 与先例对照 + 协调签署)。⇒ 二者应**合取**而非二选一:
过程型管「够不够格开始谈」,结果型管「谈的时候看什么数」。

**(d) 议题①的支撑被我自己撤掉一条。**
检索 7 表明外部规范权威**不站在我这边**(预注册收益被质疑,甚至可能加剧发表偏倚)。
⇒ ① 的论证必须**只靠本地机制**:3 个广读载体 + 已接线的消费点 + `OB-16` 的存在本身。
**不得援引外部规范权威。** 这削弱了我 P1 §3.3 那条自我怀疑的另一端 —— 窄读的辩护
(「pass 需要的只是被记录并被看见」)现在**更值得认真对待**,因为外部文献没有给「必须走完整裁决仪式」背书。

**(e) ② 的答案不能外借 —— 而这反而抬高了本地证据的地位。**
检索 4 是否定性结果:SOTA 不定义「哪些记账必须挺过回滚/崩溃」。
⇒ 判据只能来自 `RETRY-CONTRACT §2` 自身,而 `census.py:728-731` 的 docstring 恰恰是**本地唯一的判据来源**
(「不做这条,前面全是空话」)。⇒ 我 P1 对 ② 的判定**不但站住,依据还变得更硬**:
它不是我从外部搬来的标准,是这套系统**自己写下的验收条件**。
