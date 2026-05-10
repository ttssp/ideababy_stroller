---
doc_type: codex-review-decision-log
review_round: 3
reviewer: codex (HEAD~24 base, B2.2 Block A.5 完成时点)
review_date: 2026-05-10
operator: Yashu Liu
review_verdict: needs-attention (3 finding)
operator_decision: 3 accept (fix in B2.2 Block A.6)
related_plan: ~/.claude/plans/plan-rosy-naur.md v11 Block A.6
prior_round: discussion/006/b2-2/CODEX-REVIEW-ROUND2.md
---

# Codex review round 3 决策日志(B2.2 Block A.6)

## Codex 给出的 3 个 finding(verdict: needs-attention)

| # | severity (codex) | 文件:行 | 摘要 |
|---|---|---|---|
| 1 | high | `framework/xenodev-bootstrap-kit/safety-floor-2/block-dangerous.sh:40-65` | force-push 参数顺序 + 大小写 SQL bypass(具体 payload:`git push origin main --force` / `drop table users;`) |
| 2 | high | `framework/xenodev-bootstrap-kit/handback-validator/check-3-repo-identity.sh:40-87` | 三模式 OR 关系 → expected_remote 非空 + remote mismatch 时仍能 fall through 到 marker 通过(同 marker 攻击) |
| 3 | medium | `framework/xenodev-bootstrap-kit/bootstrap.sh:61-104` | bootstrap 装 hook 在 git commit 之前没装,首 commit 不受 Safety Floor 件 1 保护 |

## 我的第一性原理评级 + 处置

| # | 我的评级 | 处置 | commit |
|---|---|---|---|
| 1 | high(确认 + 重新论证 round 2 Park) | **B2.2 Block A.6 fix**(反向 fork mirror) | `be5bafd` |
| 2 | high(确认,Round 2 fix 不完整) | **B2.2 Block A.6 fix**(fail-closed 优先级链) | `c3027a5` |
| 3 | medium(确认) | **B2.2 Block A.6 fix**(装 hook + scan before commit) | `0937f36` |

## Finding 1 重新论证 round 2 Park 决策(关键)

Round 2 我把同一文件的 declared-vs-enforced gap Park 到 v0.2,理由是"byte-for-byte mirror"。
Round 3 codex 给出**具体 bypass payload**:`git push origin main --force`(参数顺序)+ `drop table users;`(小写)。

**Round 2 我的 Park 论证哪里错了**:
- 当时混淆了"patterns 缺"(可 Park 到 v0.2)与"patterns 实现 bypass"(必须 fix)
- "byte-for-byte mirror"约束适用于"不擅自 fork";但 mirror 源本身 bypassable = 协议层假设
  (三件硬约束第 2 条 hard block)从来没真正实施 — 这是协议失效,不是定制需求

**新决策(反向 fork mirror)**:
- fix in IDS mirror,作为反向 mirror 修复
- 在 mirror 文件顶部加 audit trail 注:operator 后续可决定是否同步回 autodev_pipe 上游
- 不违反 stage doc M5 step 2 的本意("纯工业共识,无定制")— 修复 bypass bug 不是定制,是
  让 mirror 真正实现 declared 的工业共识
- 前置约束:任何 patterns **新增** 仍走 stage doc 路径(不在本 fix 内做);本 fix 只修
  bypass bug 让既有 patterns 真生效

**Round 2 OQ-codex-2-1 状态**:Park 决策仍有效(declared vs enforced 完备性差距继续 Park 到
v0.2),但本 finding(force-push 参数顺序 + 大小写 SQL)从 Park 列表移除,因为它是 bug 不是
完备性差距。OQ-codex-2-1 描述需更新(本 commit 暂不动 plan,Block A.6 完成后整体回 plan)。

## Finding 2 重新论证 Round 2 fix #3 不完整(关键)

Round 2 我 fix 了 normalize 函数(保留 host),9 测试场景全过。
Round 3 codex 指出:fix 只动了 normalize,没动**模式优先级**。

**事实查证**:旧 check-3 三模式是 OR 关系,任一 PASS 即满足。fix #3 后:
- remote 模式 normalize 保留 host → 正向场景对
- 但若 remote mismatch,仍 fall through 到 no-remote 模式
- 攻击者只要保留前 30 字 CLAUDE.md header → no-remote 模式 PASS → 整体 PASS

**根因**:Round 2 我没思考"三模式之间的关系是什么"— 只是机械地修了 normalize。Round 3 强制
我重新思考:既然 producer 已经 declared 用 remote 模式(填 expected_remote_url 非空),
consumer 必须强制走 remote 比对;marker / hash 仅作 producer declared 的 fallback,不作
"任一通过即可"的逃生口。

**改 fail-closed 优先级链**(语义 BREAKING)+ §3.1 + §6.2.1 normative spec 同步更新 +
4 invalid fixtures expected_remote_url 改填实际 IDS remote(否则被新 check-3 短路掉真正
失败原因)+ Changelog v2.0 patch entry 标"语义 BREAKING 但 producer 实装无 break"。

## Finding 3 论证(链式风险)

bootstrap.sh 旧顺序:cp 件 1 → git add . → git commit → 让 operator 手装 hook(README 说明)。
首 commit 不受保护,任意 prod:// 字面串(若 stage doc PRD 含)可直接进 git 历史。

**论证**:
- 修复成本低(在 bootstrap.sh 加 Step 8.5 装 hook + 跑 scan)
- 现实风险低但非零:operator 在 bootstrap 前 cp PRD 进 XenoDev/PRD.md(per workflow),若 PRD
  含 prod:// 示例(eg "我们的 prod://db 出过事故…")就泄
- 防御深度原则:Safety Floor 件 1 应在 first commit 前激活,不能依赖文档化的手装步骤

**修复**:
- 加 Step 8.5:ln -s pre-commit hook + 跑 scan-credentials.sh
- 顺带 fix 一个旧 bug:pre-commit-credential.sh 的 SCAN_SCRIPT 引用是死代码且通过 symlink
  调起会报错(BASH_SOURCE 在 .git/hooks/),删除
- 顺带 fix 一个新 bug:scan-credentials.sh 和 pre-commit-credential.sh 的 SKIP_BASENAMES 不一致
  (SSOT 文档 AGENTS.md / CLAUDE.md / SHARED-CONTRACT.md 含 prod:// 字面串作模式定义,
   两边必须同步 skip)
- 验证:mock bootstrap 完整跑通,initial commit 落地

## 整体判断:不接受 codex 的 "no-ship" 总判决,但接受 3 全 fix

- 3 个 finding 全真,无误判
- finding #1 直接挑战我 Round 2 Park 决策 — 重新论证后接受 fix(反向 fork mirror,前所未有的边界处理)
- finding #2 直接打 Round 2 fix #3 — 接受为不完整的 fix 必须补全
- finding #3 是 Round 1 没爆出的新 finding,接受 fix(链式风险)

**B2.2 Block A.6 commit 总数:4**
- `c3027a5` fix #2 fail-closed 优先级链 + 4 fixtures + Changelog
- `be5bafd` fix #1 反向 fork mirror block-dangerous.sh + 24 case test
- `0937f36` fix #3 bootstrap.sh 装 hook + scan before commit
- (本 commit) decision log

## 后续

- B2.2 进 Block D 跨仓实跑(operator 在 XenoDev session 自跑)
- Block G 评分时,这 3 个 fix(尤其 finding #1 反向 fork)进 retrospective evidence
- v0.2 plan 起跑时:
  - OQ-codex-2-1(Park decl vs enforced 完备性差距)继续 v0.2 trigger
  - 新 OQ:autodev_pipe 是否同步回灌本 mirror fix(operator 决定)

## 与 Round 2 决策的对比(防再失误)

Round 2 4 finding:3 fix + 1 Park。
Round 3 3 finding:0 Park + 3 fix(其中 1 fix 直接修 Round 2 fix #3 incomplete)。

教训:
- Round 2 fix #3(normalize 保留 host)我以为闭环了,因为 9 测试 PASS — 但忘了"三模式优先级"
  这个上层语义。**fix code 时必须重新审整体设计**,不只补丁式修 regex。
- Round 2 finding #1 Park 是错误的 — 我用"mirror 边界"挡住了对 implementation bug 的修复。
  **mirror 边界**应该是"不擅自加新规则",**不是**"已有规则可以 bypass 也不修"。

这两个失误都被 Round 3 强制纠正,体现 codex 多轮 review 的价值。
