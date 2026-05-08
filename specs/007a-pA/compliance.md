# Compliance — 007a-pA

**Version**: 0.2
**Created**: 2026-05-08T13:30:00Z
**Revised**: 2026-05-08T13:55:00Z(R1 修订:加 D19 stderr secret redact 影响声明,无新合规触发器)
**Source spec**: spec.md v0.2 §"Open Questions" footnote + R1 review fix
**Verdict**: **No regulatory triggers for v0.1**(simple-form PRD,single-operator self-hosted,no external network calls,no PII handling,no third-party data subjects)

---

## 1. Scope of compliance review

本文件评估 v0.1 是否触发任何主流合规框架的义务。**结论:全部不触发**(详见各项)。

## 2. Per-regulation evaluation

### 2.1 GDPR(EU)/ UK GDPR / Swiss FADP
- **Trigger condition**:处理 EU/UK/CH 自然人 personal data 作为 "controller" 或 "processor"
- **本 v0.1 评估**:
  - 唯一"data subject" = operator(Yashu)本人
  - operator 是 controller AND processor AND data subject(三位一体)
  - 数据(friction-log entry)从未离开 operator 本机(C5 RL-3 + 无网络调用)
  - GDPR Art. 2(2)(c) "household exemption" — purely personal/household activity by natural person 不适用 GDPR
- **判定**:**不触发**;v0.2 若 ship 给 ADP / 其他 user 或加云同步,需重新评估

### 2.2 CCPA / CPRA(California)
- **Trigger condition**:California consumer 的 personal information 被 business(收入 / 数据量阈值)收集
- **本 v0.1 评估**:
  - 不构成 "business"(无 commercial purpose,无 25M USD 营收,无 100k consumer 数据,non-commercial)
  - 无 California consumer 处理(同 2.1)
- **判定**:**不触发**

### 2.3 PDPA(Singapore)/ PDPA(Thailand)
- **Trigger condition**:Singapore / Thailand 自然人 personal data 处理
- **本 v0.1 评估**:同 2.1 single-operator 自处理
- **判定**:**不触发**

### 2.4 PCI DSS
- **Trigger condition**:储存 / 处理 / 传输 cardholder data
- **本 v0.1 评估**:无 payment 流程;无 cardholder data 字段;no commerce
- **判定**:**不触发**

### 2.5 HIPAA
- **Trigger condition**:US covered entity 处理 protected health information
- **本 v0.1 评估**:non-healthcare;无 PHI 字段;single-operator non-clinical context
- **判定**:**不触发**

### 2.6 COPPA
- **Trigger condition**:online service 知道在收集 < 13 岁儿童 personal info
- **本 v0.1 评估**:operator(Yashu)是成年单一用户;无 child user surface
- **判定**:**不触发**

### 2.7 SEC / FINRA / 证券监管
- **Trigger condition**:financial services / 证券业务 / brokerage records
- **本 v0.1 评估**:non-financial
- **判定**:**不触发**

### 2.8 SOC 2 / ISO 27001
- **Trigger condition**:enterprise SaaS 客户合规要求(non-statutory but de facto)
- **本 v0.1 评估**:无 enterprise 客户(C2 single-operator + C3 free OSS / self-hosted)
- **判定**:**不触发**(C5 RL-4 不与 enterprise observability 竞争 = 不进入 enterprise procurement 通道)

### 2.9 EU AI Act
- **Trigger condition**:high-risk AI system 部署 / general-purpose AI model 提供商
- **本 v0.1 评估**:
  - friction-tap 不是 AI system — 是 deterministic static rule judge(D3)+ markdown writer
  - 无 LLM / model 在 v0.1(LLM 留 v0.2)
  - 即使 v0.2 引入 LLM-judge,只用 LLM 作为 internal evidence 工具,不构成 AI system 决策给"affected persons"
- **判定**:**不触发 v0.1**;v0.2 若加 LLM-judge 重新评估(初判仍不构成 high-risk)

### 2.10 OWASP Top 10 for Agentic Applications(2026)
- **Trigger condition**:non-binding security guidance for agentic AI
- **本 v0.1 评估**:
  - 不构成 "agent" — friction-tap 是 hook + CLI + scheduler;judge.py 是静态规则
  - hook silently swallow 异常的设计与 OWASP "Cascading Failures" 风险对齐(SEC-4 mitigation)
  - 无 prompt injection 面(无 LLM)
- **判定**:**no obligations**;但 SEC 风险条目已采纳相关防御原则

## 3. Privacy posture(超出合规但 v0.1 显式承诺)

虽然合规上不触发任何框架,v0.1 仍主动承诺以下 privacy 立场,作为 **product promise**(C10):

| Promise | 实现 | 验证 |
|---|---|---|
| default private | hardcoded path `docs/dogfood/v4-friction-log.md` + `[private-to-operator]` 字段 visible 在 entry | architecture.md ADR-2 + spec.md IN-4 |
| no telemetry | 无网络调用;无外部 API | architecture.md §1 系统外部 actor 列表 |
| no cloud backup | local file only | tech-stack.md "Excluded alternatives" + SLA.md "What this v0.1 does NOT promise" |
| operator final narrative authority | adjudication tag + `[disputed]` mark not delete + manual edit anytime(D5 / D10 / D11) | spec.md §4 D5 / D10 / D11 |
| right to delete | operator 直接编辑 markdown 文件,无 ID 锁;`friction --off` 一行止血 | spec.md §1 IN-7 + D5 |
| transparency | hook + CLI + trust_summary 全部 stdlib Python plain text source | tech-stack.md "Production deps: 0" |
| **stderr secret redact (R1 SEC-2 / D19)** | format.py `_redact_secrets()` 替换 7 类常见 token shape 为 `[redacted]`(best-effort,non-standard token shape v0.1 不覆盖) | spec.md §4 D19 + tasks/T003.md verification 6 case |

## 4. .gitignore guidance(SEC-1 mitigation)

README **强烈推荐**(非强制)添加以下到主仓 `.gitignore`:

```
# friction-tap dogfood archive — single-operator private(C10 promise)
docs/dogfood/v4-friction-log.md
docs/dogfood/v4-trust-w2.md
```

**为什么强烈推荐而非强制**:
- operator 可能希望 commit 进 private repo(IDS 内部)→ 此时不 ignore
- operator 可能希望 commit 进 public repo(开源)→ 此时强烈建议 ignore
- 选择权在 operator(C10 visible commitment 的实现)
- v0.1 安装脚本可选 prompt:"add to .gitignore? [Y/n]"

## 5. v0.2+ compliance triggers to monitor

(以下不在 v0.1 scope,记录为 v0.2 候选触发条件)

| v0.2 触发动作 | 可能新增义务 | 备注 |
|---|---|---|
| ship 给 ADP / 其他 operator(C8) | GDPR / CCPA 重新评估("controller" 角色变化) | 需先评估 ADP operator 所在 jurisdiction |
| 加 LLM-judge(D3 / 1.3) | EU AI Act 初判 + 模型供应商 ToS 合规 | 仍可能不构成 high-risk;但需写 model usage 政策 |
| 加云同步 / 跨仓 aggregation(1.4 / 1.7) | GDPR + cloud DPA + cross-border data transfer | 需 explicit DPIA |
| 公开 release(开源)(4.1) | OSS license 选择 + CONTRIBUTOR ToS | v1.0 时考虑 |

## 6. Compliance verdict

| Question | Answer |
|---|---|
| Does v0.1 require GDPR consent flow? | **No**(no third-party data subject) |
| Does v0.1 require privacy policy? | **No**(no commercial offering;single-operator self-host) |
| Does v0.1 require security audit? | **No**(no enterprise customer;single-user trust boundary) |
| Should v0.1 ship with `.gitignore` recommendation? | **Yes**(SEC-1 mitigation;README 强推荐) |
| Should v0.1 explicitly note "no PII handling"? | **Yes**(README §"Privacy posture" 引用本节) |

**v0.1 compliance 总结:无监管义务;product-level privacy 承诺已写入 spec / architecture / SLA / risks / non-goals 五份文件。**

> spec.md §"Open Questions" 已注:**verified no compliance requirements for v0.1.**
