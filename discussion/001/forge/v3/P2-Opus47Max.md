# Forge v3 · 001 · P2 · Opus47Max · 参照系评估(with search)

**Timestamp**: 2026-07-17T06:05:00Z
**Searches run**: 5, SOTA-benchmark(Z 四方向:非二值留痕验收 / 盲测密封 vs 审计可见 / advisory-vs-hard gate / 生产期抽查)
**Visibility**: 我已读对方 P1。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| gate 形态(g2 留痕验收) | SLSA provenance + Sigstore 部署门 | attestation(builder 身份+源+产物 digest)作**硬性**部署前置,cosign 签名验证、admission webhook 拒无效产物——阻断,但**全自动机器验签,无人肉二值签字** | RERUN-PASS artifact 靠 operator 盲测签字产出,preflight 只 regex 查文本 | 留痕验收 ≠ 去阻断;SOTA 的阻断门全是机器可验 attestation,人不在判定回路 | systemshardening.com/articles/cicd/slsa-build-provenance |
| a1 产物可见性时机(B 议题) | OSCAL/continuous-compliance 管线 | "evidence is produced as a **byproduct of the pipeline** rather than reconstructed ex-post"——证据生成时落盘、审计随时可查,替代人工 signoff(screenshot/百人时审计) | audit.json 在 gate PASS 后从确定性 retrieval **ex-post 重生成**(generate_audit_channel_postgate) | 我们的 post-gate 重生成正是 SOTA 点名的反模式;生成时留痕是正解方向 | arxiv.org/pdf/2607.08288 · regscale.com/automated-evidence-collection |
| 盲测密封 vs 审计可见张力 | LLM sealed-exam / 私有 benchmark 实践 | 密封(SEAL/ARC-AGI/FrontierMath 私有题集)只用于**专门评测活动**;日常凭据靠透明 data provenance——"statistical auditing cannot replace transparent data provenance",两者按活动类型分流并存 | 当前 CLI 把盲测密封当**唯一默认形态**:每次 reconstruct 都产盲测面+answer-key+签字模板,评估用途也被迫走密封 | 密封是特殊活动属性,不是管线默认属性——分流(校准 run 密封 / 评估 run 透明)有直接先例 | arxiv.org/pdf/2603.23292 · arxiv.org/html/2606.03305v2 |
| g3(非阻断 smoke)边界 | CI/CD advisory-vs-hard gate 实践 | 成熟做法:warn 模式起步、量测触发率、只对 **high-confidence + high-impact + 机器可判**项转硬阻断;"a warning nobody reads is not a gate"(纯告警无 escalation = 噪音) | 双道 STOP 已有,但「叙事级可信性」还挂在硬门语义里(签字三要件) | 阻断集划线判据现成:机器可验结构项 = 硬;依赖人判的质量项 = 非阻断 + 后验;纯 g3 无 escalation 是已知失败模式 | dev.to/mumtaz2029(quality gates) · tiobe.com/knowledge/article/how-to-quality-gate-software-code |
| g4(信任移使用期) | progressive delivery / shift-right | "deploy and **verify**":canary 用真流量按 metrics 验证,Flagger 不达标**自动 halt/rollback**——信任主锚在生产期,但 STOP 语义保留(自动回滚 = 后验硬动作) | O2/O7 使用期抽查已是 PRD 长期主锚,但抽查发现问题只有治理道 hand-back,无自动化后验 STOP | g4 不是「无门」:SOTA 生产期照样有机器判据的自动 STOP;后验阻断可补强治理道 | getunleash.io/blog/canary-release-vs-progressive-delivery · techment.com/blog/shift-right-testing-practices |

## 2. 用户外部材料消化

n/a——K 内无额外外部链接/文件(v3 议题的「外部材料」即 X 中 hand-back 17 与 XenoDev 真跑产物,P1 已消化)。

## 3. 修正后的视角

- P1 判断「按 run 类型分流:评估 run 生成时可见、校准 run 维持密封」→ **站住且获直接先例**:sealed-exam 实践把密封限定为专门评测活动、日常靠透明 provenance(§1 row3)。当前「每次 reconstruct 都走盲测三件套」把校准形态误设为唯一形态,是与 SOTA 的根本错位。
- P1 判断「留痕可审计验收(g2)可保留阻断,但阻断集须机器可验」→ **站住并可加锐**:SLSA 硬门全自动验签(§1 row1)+ advisory-gate 划线判据(§1 row4)给出干净公式——**机器可验结构项 = 硬阻断;人判质量项 = 非阻断 + 使用期后验**。这恰好把 g2 与 g4 从「四选一」变成「同一形态的两层」,g1 无先例(v1 已证)、纯 g3 是已知失败模式(warning nobody reads)。
- P1 判断「audit.json post-gate 才产是拓扑锁死」→ **被 SOTA 反面强化**:continuous-compliance 文献点名「证据应是管线副产物,不是 ex-post 重建」(§1 row2),而 `generate_audit_channel_postgate` 字面就是 ex-post 重建(gate PASS 后重跑 retrieval+切窗)。B 议题方向明确:评估 run 的 source 映射生成时落盘。
- P1 不确定 #3(防 V4 最小阻断集)→ **P2 已可回答**:阻断集 = 结构谓词(B' 三件/①b 覆盖)+ 可复现失败(机器道)——高置信、机器可判;叙事可信性归 shift-right(O2/O7 抽查 + 治理道,可补自动后验 STOP,§1 row5)。
- KG-B10 前提方向 → **收窄获证**:业界防产物伪造的解法是密码学签名/受控 writer(cosign 同构 = KG-B10 候选解法 ②),方向成立;但若评估 run 的 audit 生成时可见,「post-gate 产物」概念只剩校准 run 的 answer-key 密封与 rerun 自证记录两处——**KG-B10 协议面大幅缩小**,「等 gate 形态定」的暂缓判断被再次验证。
- 对方 P1 的「§3.2 最小解锁证据 = 可见 a1 审计产物 + 可复现 smoke 记录是否足够」→ 我方向 SLSA/OSCAL 证据倾向**足够且正统**(attestation 范式:产物 + 机器验证记录即是解锁凭据),留 P3 收敛细节。
