# Forge v4 · 001 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-07-18T06:31:18Z
**Searches run**: 11, SOTA-benchmark.
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| 07-17 校准产物 | ML eval leakage hygiene | scikit-learn 把 data leakage 定义为评估时使用预测时不可得信息,并要求 train/test 分离;Google MLCC 要求 test/validation 集删掉训练集重复样本,否则不是公平测试。 | 07-17 有盲测说明、负控提示、同 stem 校准标记/缺来源块,却被 v3 条款钦点为评估自证标的。 | SOTA 支持“退出评估证据/降级记录”,不支持 β 把污染样本特批消费。 | [scikit-learn](https://scikit-learn.org/stable/common_pitfalls.html), [Google MLCC](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets) |
| γ 的“首个评估 run” | Progressive delivery / canary analysis | Argo Rollouts 的 AnalysisRun 可决定 rollout 继续、abort 或 pause;inline analysis 会阻塞下一步,post-promotion analysis 失败可回退。 | γ 把生效自证绑到首个默认评估 run 产物;未发生前保持 blocked,发生后同事务自证。 | “blocked until verified” 正统;但必须有清楚触发点与失败态,否则会变僵尸条款。 | [Argo analysis](https://argoproj.github.io/argo-rollouts/features/analysis/), [Argo canary](https://argoproj.github.io/argo-rollouts/features/canary/) |
| β 的“事后豁免” | Protocol amendment / pre-registration governance | CONSORT 要报告 trial 开始后的方法/结果变更并说明理由;ClinicalTrials.gov 要把 protocol amendments 更新进记录且保留变更历史。 | β 是事后允许校准产物进入评估解锁链;γ/α 是公开改条款标的后再评估。 | SOTA 允许透明 amendment,不允许静默 waiver;β 若存在正当化,也只能作为“记录历史偏差”,不能当 PASS 证据。 | [CONSORT 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2844940/), [ClinicalTrials.gov](https://clinicaltrials.gov/submit-studies/prs-help/how-edit-record) |

## 2. 用户外部材料消化

n/a。K 内无额外链接、文本或文件;本轮只消化 forge-config 指定的 SOTA 三方向。

## 3. 修正后的视角

- 我 P1 判断“β 应 cut” → **站住且更强**。ML eval hygiene 的处置不是给污染评估样本一次豁免,而是把它移出干净评估集;07-17 降为 calibration record 更合规。
- 我 P1 判断“γ 但必须带硬兑现条件” → **站住**。Argo 给出正统类比:验证可以发生在真实 rollout/traffic 后,但结果必须控制继续、pause 或 abort。映射到本案:首个评估 run 必须同事务自证;失败或未发生都不能解锁。
- 我 P1 中“α 更像 γ 的立即兑现形态” → **站住但收窄**。若 operator 已授权并完成 key 轮换,α 是 γ 的即时实例;若为满足条款而专门烧 key,则偏回“仪式 run”,产品价值弱于自然首个评估 run。
- 对方 P1 “β 的冲突面最宽”“γ 无守卫冲突、但有悬空风险” → **站住**。SOTA 没找到支持 β 的强反例;能支持的只是透明 amendment,不是污染证据通行证。
- 回声室自检:双方 P1 高度同向,检索也主要支持 γ。唯一反向材料是 clinical protocol amendment:事后改协议本身可以正当,但条件是公开、留史、说明理由。这修正我的措辞:不是“所有事后变更都 cut”,而是“事后豁免不能伪装为评估 PASS”。因此 P3 应把 γ 写成正式 amendment,而非口头换标的。
