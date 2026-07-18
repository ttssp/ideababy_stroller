# Forge v4 · 001 · P2 · Opus47Max · 参照系评估(with search)

**Timestamp**: 2026-07-18T02:05:00Z
**Searches run**: 3, SOTA-benchmark(Z 收窄三方向:评估集污染治理 / 生效绑首个真实 run / 预注册 vs 事后豁免)
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| 07-17 产物处置 | LLM benchmark 污染治理(decontamination 文献族) | 污染样本标准处置 = **识别并移出评估集**(exclusion);诚实标注「exclusion alters the evaluation set」;**无 grandfather 豁免先例**——被污染样本不获豁免,只获移除或保留为非评估用途 | γ = 07-17 移出生效证据集、降为校准历史样本;β = 给污染样本发豁免 | 我们的 γ 与 SOTA 标准处置同构;β 在该文献族**零先例** | arxiv.org/abs/2605.21543 · arxiv.org/pdf/2406.13990 · mbrenndoerfer.com/writing/benchmark-contamination-llm-detection-mitigation |
| 生效条款形态 | progressive delivery / canary(Argo Rollouts · SLO-based gates) | 「deploy and **verify**」:验证绑**真实生产流量**的首个阶段;success criteria **在第一步之前预定义**(baseline + guardrail metrics + 阈值);未通过验证的 release **诚实停在未晋级态,无 deadline** | γ = 自证绑首个真实评估 run;T010/T011 blocked 直到自证 PASS;判据(B′+D′ 谓词)已预定义 | 同构成立。关键佐证:canary 的「blocked until verified」是**正统常态非治理逃避**——晋级没有期限,只有判据 | opsiocloud.com/blogs/argocd-rollouts · designgurus.io/answers/detail/how-do-you-do-progressive-delivery-flags-canaries-safely · medium.com/@simardeep.oberoi(SLO-based rollbacks) |
| β 的治理定性 | 临床试验 protocol 治理(FDA 指南族) | 「Protocol **waivers or exemptions are not permitted**」;变更两条正路:**prospective amendment**(事前提交审批)或 **documented deviation**(事后如实记录上报,不追认为合规);emergency exception 仅限受试者即时风险 | β 字面就是 post-hoc waiver;而 07-17 STOP → hand-back 19 → forge v4 这条链恰是「documented deviation → prospective amendment」的教科书走法 | β 在最成熟的预注册治理体系里**被明文禁止**;我们已在走的回流通道 = SOTA 正路本身 | intuitionlabs.ai/articles/managing-protocol-deviations · appliedclinicaltrialsonline.com/view/waive-inclusion-and-exclusion-criteria |

## 2. 用户外部材料消化

n/a — K 内无额外外部链接/文件(v4 的「外部材料」= hand-back 19 与 XenoDev worktree 真产物,P1 已消化)。

## 3. 修正后的视角

- P1 判断 A「β 结构性不可行非仅不可取」→ **站住并加强**。两条独立 SOTA 线合围:污染治理文献族对被污染样本零豁免先例(只有移除/降级);临床 protocol 治理明文「waivers are not permitted」。β 可干净关死——不是权衡后放弃,是**跨域一致的反模式**。
- P1 判断 B「γ 的 blocked-until-first-use 是诚实自我施压,悬空风险与 v3 有本质区别」→ **站住,且获正统性背书**。canary/progressive delivery 的晋级语义正是「判据预定义、验证绑真实流量、未验证就停在未晋级态」——**没有 deadline 只有判据**,这在 SOTA 是常态不是逃避。悬空担忧的正解不是给 γ 加期限,而是把判据与兑现步骤(runbook 级:命令/窗口/key 时序/授权点)预注册进条款——「预定义 success criteria」恰是 canary 第一步。
- P1 判断 C「α 是停下来考试」→ **被部分修正(措辞降级,实质保留)**。SOTA 里不存在「仪式性验证 run」这个独立类别:progressive delivery 的验证一律绑真实工作负载。所以 α 的正确定性不是「考试」而是「γ 的立即执行版」——若 operator 现在就有真实想评估的方向,立刻跑就是 γ 兑现;若为凑条款而跑一个不关心的方向,才退化为考试。这与对方 P1 §2「α 更像 γ 的立即兑现形态」在我读后印证一致(⚠ 回声室提示:双方 P1 此点独立同构,P3 须显式标注)。条款措辞应锚**事件**(首个评估 run 产物落地)而非锚**期限**,时序自由留给 operator。
- P1 不确定点 2「pre-split 遗留产物处置先例」→ **已解**。污染文献的 exclusion 语义 + 临床的 documented deviation 语义都指向:07-17 降级为校准历史样本 + 在 journal/决议里如实记录其 pre-split 身份,**不销毁不豁免**。与 v1「retire-as-gate keep-as-calibration」裁决的一致化有了外部背书。
- 新增视角(来自检索 ③,P1 未见):**本次 v4 自身就是 SOTA 正路的运行实例**——STOP(deviation 如实记录)→ hand-back(上报)→ forge v4(prospective amendment 审批)→ 改 PRD(批准后生效)。裁决措辞可显式采用「amendment 非 waiver」框架:γ 是对条款的**事前修订**,经治理通道批准后才执行;这让「不许悬空」有了程序语义——条款改写文本里预注册全部兑现步骤,任何再偏离都须再走 deviation→amendment 循环。
