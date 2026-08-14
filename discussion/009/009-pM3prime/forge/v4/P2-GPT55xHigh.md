# Forge v4 · 009-pM3prime · P2 · GPT-5.6-Sol xhigh · 参照系评估(with search)

**Timestamp**: 2026-08-14T04:18:31Z
**Searches run**: 15 条开放网关键词检索,保留 6 个一手来源面。
**Visibility**: 已读对方 P1 + P2。

## 1. SOTA 对标

**Search status**:WebSearch **可用**。与 A 侧相同查询/来源 **0 条**;议题邻接 ③/④,但证据域改走计量学、可靠性删失、安全规则上线与 Kubernetes PRR,未复用 A 的标注分歧、ML drift、OPA、Chrome、预注册材料。本轮 SOTA 对标**不降级**。

| 检索面 | 关键发现(逐字引文 ≤15 words) | 影响哪一题 |
|---|---|---|
| 计量学的校准间隔 | NIST“不要求任何固定重校准间隔”,应用精度要求 + control-chart 历史决定并修订 interval。引文:“**does not require or recommend any set recalibration interval**”。[NIST](https://www.nist.gov/calibrations/recommended-calibration-interval) | ③:推翻我把“每个消费批次检查”直接写成“每批校准/升版”。 |
| 信度与效度边界 | 测量过程若规格/校准本身错误,统计控制“**can only guarantee comparability among measurements**”,不能保证准确。[NIST](https://www.itl.nist.gov/div898/handbook/mpc/section2/mpc21.htm) | ①④:M1 pass 最多证明可比性改善;不能作为效度 gate 的代理。 |
| 有删失的失败率 | 失败率并非必须拿到每个完整 run 才能估;预先固定观察边界、记录 exposure 与已见 failure 后可作 censored analysis,但原文假设“**exact times of failure are recorded**”。[NIST](https://www.itl.nist.gov/div898/handbook/apr/section1/apr131.htm) | ②:削弱“逐条写穿透是唯一形态”;不改变当前系统因崩溃静默且无内容身份而不可信。 |
| 缺口可检测审计 | RFC 5848 用序号/签名识别已发送却未收到的消息,同时明说可靠传输“**does not protect against loss ... at the application layer**”;RFC 9162 用 inclusion/consistency proof 证明 append-only,但审计失败后的动作不规定。[RFC 5848](https://www.rfc-editor.org/rfc/rfc5848.html) · [RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.html) | ②⑤:可信形态可含“显式缺口/删失”,但光能审计仍不会自动产生治理动作。 |
| detection-only → blocking | ModSecurity 要求新环境先 DetectionOnly,观察事件、修 false positives 后才 protection:“**Every Ruleset can have false positives in new environments**”。[OWASP ModSecurity](https://github.com/owasp-modsecurity/ModSecurity/wiki/ModSecurity-Frequently-Asked-Questions-%28FAQ%29) | ④:convert 需要真实误杀审阅,不只一个稳定性数。 |
| feature graduation | Kubernetes KEP 把 graduation criteria、flake-free e2e、PRR 批准、rollback metrics/测试列为并列必填;原问:“**What specific metrics should inform a rollback?**”[Kubernetes KEP](https://github.com/kubernetes/enhancements/blob/master/keps/NNNN-kep-template/README.md) | ④:过程证据 + 结果证据 + 具名批准 + 可回退应合取。 |

## 2. 用户外部材料消化

K 未给外部链接/文件。其内嵌边界继续有效:M1 不解锁扩样/E2、41 条路不重开、不改 C6 数字。回声室警告已响应:本侧开放检索正常,且没有复用 A 的来源。

## 3. 修正后的视角

- **P1 ③ 被推翻**:我写“每个被消费的新比较批次到期一次”时混同了 **monitor/check** 与 **recalibrate/version bump**。修正为:每个消费批次都监测;是否重校准由长期 control 数据相对应用要求决定,身份/口径变化则启动新基线。产证者与 operator-chair 裁决者分离仍站住。
- **P1 ② 被削弱,现状 verdict 站住**:写穿透不是理论上的唯一解;若崩溃被显式标为具有已知 exposure 的删失、且内容身份可证,跨批估计可能成立。但当前 SIGKILL 路径既无返回标记、又无失败批次内容绑定,故“现在不可信”不变。
- **P1 ④ 被削弱**:我要求先“独立校准证明指标到决策错误的稳定映射”过强。工业晋级更像:观察期误杀审阅 + 预声明指标/错误成本 + 测试/批准 + rollback。它要求可证伪与可撤回,不要求先证明一个普适映射。
- **P1 ① 站住且收窄**:pass 欠显式裁决仍只由本地三载体与 OB-16 支撑;外部证据只说明本次 M1 最多改善可比性,不能替“为何欠裁决”背书。A 侧提出的“歧义抹除风险”应进入裁决 rationale,但不能把 M1 反判为 fail。
