# Forge v3 · 001 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-07-17T14:20:50+08:00
**Searches run**: 24, SOTA-benchmark
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标(或指定对标)

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| ideababy_stroller | PyPI digital attestations + in-toto/SLSA | release distribution 可随包携带签名 attestation,把身份、digest、source/provenance 交给下游与 auditor 验 | a1 source_refs 已在内存有,但正常落盘面不可见,audit.json 还等 gate PASS 后才产 | 留痕应随产物出生,不是判定后补生 | https://docs.pypi.org/attestations/ |
| ideababy_stroller | SLSA provenance verification | 按 builder、signature、source、buildType、parameters 对 provenance 做 expectation check;可在 upload、download 或 monitor 处验 | 现 T010/T011 把验收语义绑到单一 post-gate artifact | 应拆成“产物留痕可验”与“谁在何时采取动作”两层 | https://slsa.dev/spec/v1.2/verifying-artifacts |
| ideababy_stroller | SLSA VSA | 用 verification summary 暴露验证结论,同时不暴露全部 attestations/流水线细节 | 盲测密封与审计可见被做成全有/全无冲突 | 可公开审计摘要/refs,保留 answer-key 与校准细节密封 | https://slsa.dev/spec/v1.2/verification_summary |
| ideababy_stroller | Hugging Face competitions | public/private leaderboard 分面:提交即算两套,只公开 public,赛后揭示 private | 评估 run 与校准 run 仍混在盲测面、answer-key、签字模板一条路径 | 对方 P1 的 run 类型分流有证据支撑:评估面可见,校准面密封 | https://huggingface.co/docs/competitions/main/leaderboard |
| ideababy_stroller | GitLab `allow_failure` / Buildkite `soft_fail` | 非零结果可保留 warning,但不阻断后续 pipeline;也可按 exit code 细分 | gate 仍通过 RERUN-PASS spine 影响解锁 | g3 可成立为 smoke/advisory,但 hard STOP 只留给可复现结构失败 | https://docs.gitlab.com/ci/yaml/ · https://buildkite.com/docs/pipelines/configure/soft-fail |
| ideababy_stroller | Azure SDP / Argo Rollouts | 小流量 progressive exposure + health model/background analysis;异常时 halt/rollback | 现前置一次性考试感强,使用期 O2/O7 价值被削弱 | g4 不是“无前置”,而是前置最小化 + 使用期抽查主导信任 | https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/safe-deployments · https://argoproj.github.io/argo-rollouts/features/analysis/ |

## 2. 用户外部材料消化

K 内无额外外部链接/文本/文件,n/a。可吸收项来自 Z 的 SOTA 搜索,不是用户另贴材料。

## 3. 修正后的视角

- P1 判断“g1 cut,盲测二值签字不应继续作价值主锚” → **站住**。GitLab/Buildkite 证明 CI/CD 里质量信号可非阻断;Azure/Argo 证明信任可通过小步生产期观察逐步建立。
- P1 判断“前置验收只看产物留痕,还是整体移使用期” → **被修正为 hybrid**。SLSA 不取消前置验证,但把它定义为 provenance expectation check;Azure/Argo 再把真实信任交给渐进曝光和 health model。因此 v3 不应选纯 g2 或纯 g4,而应是 g2 最小前置 + g3 smoke signal + g4 使用期后验。
- P1 判断“KG-B10 可改写为任何 provenance/审计产物可伪造性协议” → **收窄**。SLSA 的 roots of trust、签名、builder identity 是成熟方向,但本轮 K 明确只裁前提。过早把 KG-B10 扩成通用防伪协议会重演 KG-B7 过度投资。
- 对方 P1 的“隐依赖环” → **证据增强**。PyPI/SLSA 的常态是 attestation 与 artifact 一起分发或由 ecosystem/monitor 验;我们 post-gate 才产 audit.json,正好把验收底料锁在验收之后。
- 对方 P1 的“按 run 类型分流” → **方向站住但需限定**。HF private leaderboard 与 SLSA VSA 都显示:可见面与密封面可以并存。评估 run 应始终落盘 source_refs/审计摘要;校准 run 才保留 answer-key sealing,并只输出可公开 verification summary。
