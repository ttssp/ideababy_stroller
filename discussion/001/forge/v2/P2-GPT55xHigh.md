# Forge v2 · 001 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-07-16T19:41:45+08:00
**Searches run**: 4, SOTA-benchmark
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标(或指定对标)

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| ideababy_stroller | SLSA Build Provenance + W3C PROV | provenance 是 artifact 的生成期事实:输入、依赖、执行者、输出一起记录,用于事后验证与重建。 | 真 briefing 在 gate 前已丢 source token;TimeSlice/DisplacementNarrative 没有 source 回链。 | 核心 gap 是生成路径没保留最小 lineage,a1 若只做 slice→source refs 保留,不是补锅,是 SOTA 方向。 | https://slsa.dev/spec/v1.2/build-provenance ; https://www.w3.org/TR/prov-overview/ |
| ideababy_stroller | Flagger progressive delivery | canary gate 随 rollout 阶段跑指标阈值、pre-rollout hook、人工 confirmation;检查绑定到已有流量/指标。 | v1 把 ①② 绑到 T010/T011 解锁,但 Judgment/图证据在下游。 | 对方 P1 的“Phase 2 形状的验收绑到 P0.1”站住:gate 谓词必须跟 artifact 就绪时点对齐。 | https://docs.flagger.app/main/usage/metrics ; https://docs.flagger.app/main/usage/webhooks |
| ideababy_stroller | Diverse Double-Compiling(DDC) | bootstrap 问题不用被测系统自证自己,而用独立路径生成可比输出,再按假设验证一致性。 | 我们想验证 checker 能力,却又让 checker 依赖自己将来生产的底料。 | “直接解锁”过松;需要一个独立小 fixture/既有真产物自证,证明 a1/③ 的检查器本身能判。 | https://dwheeler.com/trusting-trust/ ; https://arxiv.org/abs/1004.5534 |
| ideababy_stroller | OpenTelemetry trace sampling | trace 可按 head/tail sampling 抽查;tail sampling 在 trace 完整后按错误、延迟、属性等条件选择样本。 | 用户真实偏好是 O2/O7:边用边抽查,不是停下来考试。 | ①② 更适合作为 trace 完整后的 ship/使用期抽查对象,不是 trace 能力生产前的前置门。 | https://opentelemetry.io/docs/concepts/sampling/ |

## 2. 用户外部材料消化

n/a。K 内无新增外部链接、文本或文件。

## 3. 修正后的视角

- P1 判断“①② 不是 checker 尚未实现,而是当前拓扑下无可判对象” → **站住**。Flagger 的 staged gate 也把检查绑定到已有指标;DDC 也拒绝让待验证能力空转自证。
- P1 判断“a1 不是我的首选” → **修正**。SLSA/PROV 强化了 lineage 必须在生成期采集:窄 a1(slice→source refs)应升为必要底料,但仍不得偷建 T011 图或 Judgment。
- P1 判断“T010/T011 倾向直接解锁 trace-producing tasks” → **部分被推翻**。DDC 说明 bootstrap 要有独立可比路径;解锁前至少要用真 briefing 或固定 fixture 跑通 a1/③ 的存在性、可解析性自证。
- P1 判断“B4 必须先改 wiring 对象” → **站住**。对标后 wiring 对象应是 a1 后真实存在的 slice source map、③ 审计入口、治理 STOP 记录,不是当前不存在的 3-hop evidence。
- 读对方 P1 后我的立场变化:我从“a3 为主、a1 谨慎保留”收敛到“a1 是最小 lineage 底料,a3 是 ①② 的验收/使用期位置”。也就是说,bottom line 不是放弃 ①②,而是先保留生成期 lineage,再在 trace 完整时验 ①②。
