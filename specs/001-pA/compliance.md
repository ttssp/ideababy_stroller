# Compliance · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**判定**：本产品 v0.1 **不属于受监管领域**（无医疗 / 金融 / 儿童 / 支付 / 政府数据）；无需 HIPAA / PCI / COPPA / SEC / FINRA 认证。但会存储 lab 成员身份 + 阅读行为 + "品味信号"文本，属于**个人数据（Personal Data）**范畴，值得一份简明声明以便将来审计 / 成员询问 / 商业化时升级。

---

## 1. 受监管认定 · 逐项清单

| 监管 | 是否适用 | 判定理由 |
|---|---|---|
| **GDPR**（欧盟）/ **UK GDPR** | **v0.1 不直接适用**（operator 在中国，lab 成员均在中国；**若未来有欧盟成员** 加入则需重新评估） | 无欧盟 data subject |
| **中国《个人信息保护法》(PIPL)** | **轻度适用** | lab 成员邮箱 + 阅读行为 = 个人信息；但本产品为 lab 内部工具，operator 同时是 controller，数据不出境，不跨主体分享 |
| **CCPA**（加州） | 不适用 | 无加州 data subject |
| **HIPAA** | 不适用 | 无医疗信息 |
| **PCI-DSS** | 不适用 | 无支付（C3 · v0.1 不集成任何支付 SDK） |
| **COPPA** | 不适用 | 用户均为成年学者，无 < 13 儿童 |
| **SEC / FINRA** | 不适用 | 无金融数据 |
| **学术伦理 / IRB** | **弱适用** | 若 operator 计划把 lab 成员的使用数据用于学术研究（e.g. 发表"PI vs operator 使用模式差异"论文），需走本单位 IRB；v0.1 不发表 |
| **arXiv Terms of Service** | **适用** | 通过 arXiv API 抓取 metadata；必须遵守 rate limit（≤ 1 req/3s）+ 不公开再分发 metadata |
| **LLM Provider ToS**（Anthropic / OpenAI） | **适用** | 调用前需遵守其"不上传个人信息"条款；adapter 已强制 strip email（risks.md SEC-4） |

**结论**：v0.1 无需正式 compliance 证书，但**需要**一份面向 lab 成员的"数据使用声明"（下方 §3）。

---

## 2. 数据资产清单（存了什么）

| 类别 | 具体数据 | 存储位置 | 保留期 | 是否出境 |
|---|---|---|---|---|
| **身份** | `seats.email`（lab 成员邮箱）、`sessions.token_hash`（登录 session） | Postgres（operator 自持 VPS） | 永久保留，除非成员请求删除 | 否（单 VPS 所在地 = 运维所在国） |
| **授权** | `seats.role`、invite token hash | 同上 | 永久保留 | 否 |
| **行为** | `actions`（4-action 历史 + why 文本）、`sessions`（登录历史） | 同上 | 永久保留（breadcrumb 需 ≥ 6 月回溯，见 C.1） | 否 |
| **品味信号** | `actions.why`（"why I disagree" 文本 ≤ 280 字符） | 同上 | 永久保留（OUT-1 不喂回 LLM，但保留供 v0.2 用） | 否 |
| **公共数据副本** | `papers`（arXiv metadata + abstract） | 同上 | 永久保留（非 PII） | 否 |
| **LLM 调用日志** | `llm_calls`（tokens / cost / provider），**不存 prompt 或 response 原文** | 同上 | 永久保留（成本审计需要） | 否 |
| **派生数据** | `briefings`（state 摘要一句话判断 + trigger paper ids）、`resurface_events` | 同上 | 永久保留 | 否 |
| **LLM 生成摘要**（R1 新增） | `paper_summaries`（3 句 LLM 解读 · per paper × topic × prompt_version · 受 DB CHECK ≤ 3 句）· 外键指回 `llm_calls` 追溯调用成本（**F5 · 2026-04-24 v0.2.2**：`llm_call_id` 允许 null · round-trip import 场景下该字段可能为空 · 对应审计链失效但 `model_name` / `prompt_version` 保留 reproducibility） | 同上 | 永久保留直到 paper 删除（CASCADE）或 operator 手动 drop | 否 |
| **导出审计**（R1 新增） | `export_log`（`lab_id, seat_id, export_type, row_counts_jsonb, byte_size, created_at`）；记录每次 `/api/export/full` 成功调用 | 同上 | 永久保留（SEC-1 审计需要） | 否 |

**未存储的**：
- LLM API key（仅存 systemd credentials，绝不入 Postgres）
- 未加密的 session token（仅哈希）
- Seat 的 IP 地理位置、User-Agent 指纹、设备信息（超出需要）
- Lab 外部数据 / 学生论文草稿 / 未公开 paper
- **任何 email → LLM 传输**（adapter 强制 strip，risks.md SEC-4）

---

## 3. 面向 Lab 成员的数据使用声明（v0.1 版本）

> 以下文本可直接复制到 `/public/privacy.md` 并在首页 footer 链接。语言：中文；若 lab 有英文成员，operator 应同时提供英文译本。

```markdown
# 数据使用声明 · PI Briefing Console（lab 内部工具）

## 我们会记录什么
- 您的邮箱（仅用于登录 / 接收邀请 token）
- 您的登录时间（用于统计 seat 是否活跃，满足产品验收 O1/O3）
- 您对每篇 paper 的 4-action 标注（`read_now` / `read_later` / `skip` / `breadcrumb`）
- 您可选填写的 "why I disagree" 自由文本（≤ 280 字符，仅存不分享，不喂回 LLM）
- 您 breadcrumb 的 paper 及其 resurface 历史

## 我们不会记录什么
- 您的 IP 精确位置、设备指纹、浏览器历史
- 任何您未在本系统内主动输入的内容
- 您的任何 paper 草稿、实验数据、实验室机密

## 数据存放在哪
- 全部存储在 PI 自持的一台服务器上（由 PI 管理）
- 不经任何第三方云分析 / 行为追踪服务
- LLM 调用（用于生成 briefing 摘要和 state-shift 判定）只发送 arXiv paper 的 title + abstract，不发送您的邮箱、action 历史或 disagree 文本

## 您的权利
- **数据可携**：您可以随时请求导出您的全部数据（JSON 格式）
- **数据删除**：您可以请求 PI 从 Postgres 中删除您的 seat 及其所有 action 历史（v0.1 无自助删除 UI，需联系 PI 手动执行）
- **数据保留期**：默认永久保留，因为 breadcrumb resurface 需要 ≥ 6 个月回溯；如您退出 lab 可请求整体删除

## 如何联系
- 问题 / 删除请求 → 联系 lab PI（admin seat 持有者）
```

**O4 的 "self-report + 截图" 相关**：若 operator 把自己的使用截图用于周度自陈（spec.md §6 O4），**不涉及他人数据**则无合规问题；若截图包含 lab 其他成员的 action / why，operator 应在自陈前脱敏或获得成员同意。

---

## 4. 数据主权 · 不变式（Invariants）

以下是产品代码层必须保证的 invariant（违反 = P1 事故，见 SLA.md §4）：

| Invariant | 守在哪里 | 如何验证 |
|---|---|---|
| 所有业务数据仅存 operator 自持 Postgres | `architecture.md` ADR-5 + C12 | 生产环境 env 扫描：无 Supabase / 外部 DB URL |
| LLM adapter 不传 email / seat id / action history | `risks.md` SEC-4 | adapter 单元测试断言 payload 无邮箱正则 |
| LLM provider 不打开训练数据共享 | tech-stack.md §2 | adapter 设置 provider-specific `opt_out_training=true` 标志 |
| 未授权请求禁止访问任何 user data | SLA.md §4 · architecture.md §7 | CI 扫描每个 route 必须过 auth middleware |
| JSON export 只提供给 admin | spec.md §IN-6 + architecture.md §8 | admin-middleware 双重检查 |
| 数据库不暴露公网 | architecture.md §7 | `pg_hba.conf` 限 localhost · 部署 runbook 验证 |

---

## 5. 数据保留与删除策略

### 5.1 Default 保留期（v0.1）
**永久保留**。理由：
- **breadcrumb resurface 需要 ≥ 6 月回溯**（IN-4 + §4.2 of spec）
- **O5 验收窗 = day-45–60**，删历史会破坏验收
- **JSON export 是 portability 承诺**（C8），不自动删才能完整导出

### 5.2 个案删除（v0.1 手动）
当 seat 请求删除：
1. `SELECT` 该 seat 的 `seats.id`
2. `DELETE FROM sessions WHERE seat_id = ?`
3. `DELETE FROM actions WHERE seat_id = ?`
4. `DELETE FROM breadcrumbs WHERE seat_id = ?` → cascade 删 `resurface_events`
5. `DELETE FROM seats WHERE id = ?`
6. 发邮件确认给请求者

v0.1 无自助 UI（NG-B4）；operator 手工 SQL 执行。

### 5.3 整体删除（lab 解散 / 停用产品）
流程：
1. `/api/export/full` 下载 JSON（C8 portability 履约）
2. 给所有 seat 发邮件附 JSON
3. `pg_dump` 备份到 operator 云盘（保留 90 天后再彻底 drop）
4. `DROP DATABASE` + systemd stop service
5. 云盘 90 天过后 purge 备份

### 5.4 LLM provider 侧的数据
- Anthropic / OpenAI 按其 ToS 保留 API call payload 30 天用于 abuse detection
- 因为 adapter 不传 PII，即便 provider 保留也不涉及 lab 成员身份
- adapter 层设置 `opt_out_training=true` 防止用于模型训练

---

## 6. 对未来路径的 flag（v0.2+ 合规）

当 operator 启动以下路径时，**需重新走 compliance review**：

| 路径 | 需要重审因 |
|---|---|
| v0.2 引入 hybrid taste agent（NG-A1 重启） | disagree 文本喂回 LLM → 涉及 PII 跨境传输（如果 LLM provider 在境外） |
| v0.2 引入 federation / cross-lab sharing（NG-A11） | 数据出 operator 主权 → 需 DPA + 合规评估 |
| v1.0 商业化 / 开放注册 | 正式 controller-processor 关系 → 需 PIPL / GDPR 评估 + 完整 privacy policy + DPO 指定 |
| 引入第三方 analytics（Posthog / Plausible / GA） | v0.1 明确拒绝；若重启需成员 opt-in |
| 若未来有欧盟 lab 成员加入 | GDPR 生效 → 需 lawful basis + right-to-erasure UI |

每条一旦触发，compliance.md 必须先升版再动代码。

---

## 7. Operator 自审清单（每月一次）

Operator 每月月初花 15 分钟执行：

- [ ] 检查 `seats` 表是否有当前 lab 已离开但未清理的成员
- [ ] 检查 `llm_calls` 累计成本是否接近 $40（C11 envelope 预警）
- [ ] 检查 Postgres `pg_dump` 备份是否按计划生成
- [ ] 检查 GitHub repo `.env*` 是否意外提交（`gitleaks` scan）
- [ ] Review `journalctl -u pi-briefing-web` 过去 30 天是否有异常访问
- [ ] 若 lab 有新成员加入，发一遍 §3 数据声明

将本清单并入 `runbook.md`（T031 预留）。

---

## 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · 非受监管判定 · PIPL 轻度适用 · 声明模板 · 数据主权 invariants · 未来路径 flag |
| 2026-04-23 | 0.2 | R1 adversarial fix：§2 新增 `paper_summaries`（LLM 3 句解读）+ `export_log`（SEC-1 审计）数据资产条目；其余判定不变 |
| 2026-04-24 | 0.2.1 | F5 pre-R_final hardening：§2 `paper_summaries` 行补注 `llm_call_id` F5 nullable 语义 · round-trip import 场景可能产出 null FK · 对应审计链失效但 `model_name`/`prompt_version` reproducibility 保留 |
