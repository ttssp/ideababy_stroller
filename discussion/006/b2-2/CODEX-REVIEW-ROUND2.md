---
doc_type: codex-review-decision-log
review_round: 2
reviewer: codex (HEAD~20 base, B2.2 Block D 完成时点)
review_date: 2026-05-10
operator: Yashu Liu
review_verdict: needs-attention (4 finding)
operator_decision: 3 accept (fix in B2.2 Block A.5) + 1 partial-accept (Park to v0.2)
related_plan: ~/.claude/plans/plan-rosy-naur.md v11 Block A.5
---

# Codex review round 2 决策日志(B2.2 Block A.5)

## Codex 给出的 4 个 finding(verdict: needs-attention)

| # | severity (codex) | 文件:行 | 摘要 |
|---|---|---|---|
| 1 | critical | `framework/xenodev-bootstrap-kit/safety-floor-2/block-dangerous.sh:40-64` | dangerous patterns 不全(declared AGENTS.md §1 vs enforced gap) |
| 2 | high | `framework/xenodev-bootstrap-kit/safety-floor-1/pre-commit-credential.sh:23-57` | 扫 working tree 不扫 staged blob → staged-but-cleaned 攻击绕过 |
| 3 | high | `framework/xenodev-bootstrap-kit/handback-validator/check-3-repo-identity.sh:39-52` | normalize 删 host → 同 owner/repo 跨 host 冒充 |
| 4 | medium | `framework/SHARED-CONTRACT.md:699-719` | §6.3 schema 漏 source_repo_identity 块,与 validator + valid fixture 漂移 |

## 我的第一性原理评级 + 处置

| # | 我的评级 | 处置 | commit |
|---|---|---|---|
| 1 | medium(降级,见理由) | **Park v0.2**(OQ-codex-2-1)| (无 fix commit;OQ 入 plan) |
| 2 | high(确认)| **B2.2 Block A.5 fix** | `10774b4` |
| 3 | high(确认)| **B2.2 Block A.5 fix** | `14a1d5c` |
| 4 | high(升级,见理由)| **B2.2 Block A.5 fix** | `b34686e` |

## Finding 1 降级 + Park 理由(Park 决策核心)

Codex 评 critical · 我评 medium · Park 到 v0.2:

**事实依据**:
- `block-dangerous.sh` 顶部 L16-21 标注:"Mirror provenance: from autodev_pipe / **byte-for-byte 一致** / 未来 XenoDev 定制 patterns 在 XenoDev 仓内 fork 后修改,**不要改本 mirror**"
- stage-forge-006-v2.md M5 step 2 verbatim:"cp block-dangerous.sh from V4(纯工业共识,无定制)"
- AGENTS.md §1 是 "**declared spec**";block-dangerous.sh 是 "**enforcement layer**";AGENTS.md §2 reliability 三层(Safety Floor + Deterministic Feedback + Learning Loop)允许 enforcement 是 declared subset

**为什么 Park 到 v0.2 而不是 B2.2 内 fix**:
- (a) 改 IDS mirror 违 stage doc M5 step 2 约束(byte-for-byte);
- (b) v0.1 scope 是"工业共识 mirror",非"XenoDev 定制完备性";
- (c) 真正 fix 路径是 **XenoDev 仓内 fork mirror 加 patterns**,不动 IDS。

**v0.2 trigger**:
- XenoDev 跑 ≥1 真 task 后(Block D-G 完成)回看 enforcement gap 实战暴露程度
- 决定是否在 XenoDev 内 fork mirror(若决定 fork → 在 XenoDev `.claude/hooks/` 加 patterns + 文档化"v0.2 起 XenoDev 不再 byte-for-byte mirror")
- 若 v0.1 实跑期间 enforcement gap 真触发漏洞 → 提前到 v0.1 patch

## Finding 2/3/4 fix 摘要

### Fix #2(commit `10774b4`)
- `pre-commit-credential.sh`:`grep -q 'prod://' "$file"`(working tree)→ `git show ":$file" | grep -I -q 'prod://'`(staged blob)
- 加 `test-pre-commit-staged-blob.sh`,3 case 全 PASS:
  - case 1 staged-but-cleaned 攻击场景 → BLOCK ✅
  - case 2 working tree 含但未 stage → PASS ✅
  - case 3 两端都含 → BLOCK ✅(回归)

### Fix #3(commit `14a1d5c`)
- `check-3-repo-identity.sh` normalize 函数:统一 scp + URL 形式为 `host[:port]/path`,**保留 host**
- 加 `test-check-3-host-binding.sh`,9 case 全 PASS:
  - 5 正向(scp ↔ url 跨形式等价 + trailing .git + 大小写)
  - 4 负向含 finding #3 攻击场景(`https://evil.example/owner/repo` ≠ `git@github.com:owner/repo`)

### Fix #4(commit `b34686e`)
- `framework/SHARED-CONTRACT.md` §6.3 schema 加 `source_repo_identity:` 三字段块 + producer 来源说明
- Changelog 加 v2.0 patch entry
- 非 BREAKING(producer 实装 + valid fixture 本就携带,本 patch 只把已实装写进 schema)

## 整体判断:不接受 codex 的 "no-ship" 总判决

- 4 个 finding 中 3 个真 + 1 个范围误判(critical 评级不当)
- 3 个真 finding 全 B2.2 Block A.5 内 fix · 0 commit 进 production 前 ship
- finding #1 Park 到 v0.2,XenoDev 实跑后回看 — 这是 v0.1 scope 决定,不是漏洞

**B2.2 Block A.5 commit 总数:3**
- `10774b4` fix #2
- `14a1d5c` fix #3
- `b34686e` fix #4

## 后续

- B2.2 进 Block D 跨仓实跑(operator 在 XenoDev session 自跑)
- Block G 评分时,这 3 个 fix 计入维度 #2 (validator 错误信息) + #4 (false positive/negative)
- v0.2 plan 起跑时,OQ-codex-2-1 进 v0.2 trigger 列表
