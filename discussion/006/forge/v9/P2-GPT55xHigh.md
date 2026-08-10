# Forge v9 · 006 · P2 · GPT55xHigh · 参照系评估(with search)

**Timestamp**: 2026-08-10T17:32:50+08:00  
**Searches run**: 36 queries, SOTA-benchmark  
**Visibility**: 我已读对方 P1；未读对方 P2。

## 1. SOTA 对标

| 标的 X' | 参照项 | 它怎么做 | 我们怎么做 | gap | URL/Source |
|---|---|---|---|---|---|
| KG-B11 | RFC 5848 / Rekor / WORM | 签名摘要可检缺失、重放与顺序；透明日志给 inclusion/integrity proof；WORM 防覆盖删除 | git 内 immutable 文件 + 可覆盖 singleton，且两轮均未写 | SOTA 给“已有记录不可篡改”，但本题是“该产却未产”；WORM/Merkle 不生成 obligation | [RFC 5848](https://www.rfc-editor.org/rfc/rfc5848) · [Rekor](https://github.com/sigstore/rekor) · [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) |
| KG-B11 + XD-43 | in-toto layout | owner 先签必经步骤、授权者与产物规则；link 是后生证据，缺步骤即验证失败 | 是否必需由证据父键自身是否出现决定 | 这是反例：缺的并非只在 execution，而是独立 expectation/obligation 的设计层 | [in-toto](https://github.com/in-toto/in-toto) |
| XD-43 | SLSA v1.2 + in-toto Statement | subject digest 绑定内容；buildDefinition、runDetails、builder identity 说明谁以何输入执行哪次 invocation | SHA、task、命令、退出码散列为建议字段，producer 与证据同信任域 | SOTA 可证明“谁对哪份内容作何声明”，但不能证明 review 足够；可信 control plane 仍须另立 | [SLSA provenance](https://slsa.dev/spec/v1.2/build-provenance) · [Statement v1](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md) |
| XD-43 / B-4-IDS | GitHub required checks | requirement 由 branch/ruleset 预置；check 未上报保持 Pending 并阻断，且可限定来源 App | runner 存在但入口、ship gate 都不要求状态出现 | 直接表达“该跑而未跑 ≠ 通过”；但若交付可绕过权威 gate，机制仍无效 | [Required checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks) |
| XD-43 | OPA | OPA 只作 policy decision point，应用/CI 的 enforcement point 必须主动询问并执行决定 | 现有 runner 同样是孤立 decision point | 反证“采 policy-as-code 即解决”：OPA 明确不负责接线，未调用问题原样保留 | [OPA deployment](https://www.openpolicyagent.org/docs/deploy) |
| stale pointer | GitHub / Gerrit stale approval | GitHub 以 diff/merge-base 变化撤销；Gerrit 依 change-kind copyCondition 决定 vote 是否沿用 | singleton 可跨 16 轮保持 approve/0，无内容适用性判断 | 成熟判据是当前 patch 身份/差异；全量撤销会因 merge-base 漂移误报，Gerrit 的细分可减误报但需可信分类 | [GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) · [Gerrit](https://gerrit-review.googlesource.com/Documentation/config-labels.html) |
| XD-44 | 同行评议实证研究 | 19,177 reviews 显示初始 patch 大小/新增行与 review changes 相关；另一研究发现规模、复杂度影响轮次，70% 约 1–2 轮但精确轮次预测很差 | 固定 4 轮；T042 同时承载多状态与多消费点 | 未取到支持统一停轮阈值的研究；证据支持按 task 规模/复杂度分层，不支持仅凭“finding 类别重复”停 | [Fregnan et al., EMSE 2022](https://link.springer.com/article/10.1007/s10664-022-10205-7) · [Reviewing rounds, EMSE 2022](https://link.springer.com/article/10.1007/s10664-021-10035-z) |
| XD-41 / XD-44 | defect escape 研究 | review coverage、参与度、专家度与 post-release defects 有显著关系；但覆盖率 100% 仍可有缺陷 | fallback 做了动作，强度与跨 task 覆盖不足 | SOTA 给过程质量变量，不给“跑过即可靠”；轮数也不是充分统计量 | [McIntosh et al., EMSE 2016](https://rebels.cs.uwaterloo.ca/journalpaper/2015/03/03/an-empirical-study-of-the-impact-of-modern-code-review-practices-on-software-quality.html) |

## 2. 用户外部材料消化

n/a。`forge-config.md` §Z 明示“外部材料叠加：无”；以上均为本轮 SOTA 检索，不冒充 operator 材料。

## 3. 修正后的视角

- P1「现行系统并非没有机制」→ **站住，但“失效只在入口”的完整诊断被推翻**：§1 第 2、4 行显示，成熟体系先在证据之外定义必经 obligation；本仓同时有 execution gap 与 design gap。对方“四条机制侧全都写对了”也因此只站住一半。
- P1「预先生成、内容绑定的 obligation」→ **站住**：§1 第 2–4 行分别给出 layout、subject digest 与 required-status 三种同构先例；证据不能决定自身是否应存在。
- P1「SHA 不能证明本次评审跑过」→ **站住**：§1 第 1、3 行表明不可篡改、内容绑定、可信执行者是三项不同保证；采用任一标准都不能单独覆盖“够不够”。
- P1「四轮不应是无差别质量上限」→ **站住**：§1 第 7、8 行没有给出统一停轮数，且 review 是否发生、参与质量、patch 规模均分别影响结果；“类别重复”也尚无可执法实证。
- 对 XD-44 的 task 粒度 reframe：**支持，但证据不足以判为唯一根因**。§1 第 7 行直接把较大/复杂 patch 与更多轮次、更多 review changes 相联，故 T042 过大比“上限单纯太低”更有实证基础；但研究未证明拆分会提高缺陷发现率，仍需保留有界 hard-stop。

