# SLA · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**原则**: v0.1 SLA **必须**与 v1.0 SLA 显式分开，避免 v0.1 过度工程化。v0.1 的服务对象是 operator 自己 + ≤ 2 名 lab 成员，任何"商业级 SLA"的开销都不合理。

---

## 1. v0.1 · self-dogfood · ≤ 3 seat · 5 周 ship

面向：operator + ≤ 2 名 lab-internal operator（总共 ≤ 3 个 active seat · C10）。
目标：让 PI 8:00 能稳定读到 briefing · 让 operator 能稳定完成 triage · **不追求** commercial 可靠性。

### 1.1 可用性（availability）

| 指标 | 目标 | 理由 |
|---|---|---|
| 整体服务 | **best-effort · 无正式承诺** | 单 VPS + solo operator，不引入冗余也不买多节点 |
| `/today` briefing 页可用 | **6/7 天** at 08:00 local | PI 的 8:00 10 分钟 ritual 是 O1 的命脉；丢一天可接受，连丢两天要排查 |
| Daily briefing 生成完成 | **07:30 local · 6/7 天** | 06:00 cron 启动，留 1.5h buffer 容忍 arXiv API 抖动 + LLM 重试；T3 周起纳入 self-report 指标 |

### 1.2 延迟（latency）· 单用户 local Postgres

| 路径 | p95 目标 | 测量方法 |
|---|---|---|
| `/today` 首屏 SSR | **< 1.0s** | Playwright `performance.timing` 连跑 20 次取 p95 |
| `/topics`, `/breadcrumbs` 列表页 | **< 1.2s** | 同上 |
| 4-action POST（Server Action） | **< 500ms** | `X-Response-Time` header 采集 |
| JSON export（admin-only · 全量） | **< 10s**（15 seat × 1 年数据规模） | 手动 `time curl -o /tmp/export.json /api/export/full` |

**为什么 < 1.0s**：PRD UX principle 1（"Speed > Polish"）+ O1（PI 每日 ritual 不容忍"卡一下"）。这个数字基于 Postgres 本地 socket query < 50ms × SSR render < 300ms × 网络 + browser parse < 300ms 的 ball-park 叠加。

### 1.3 数据完整性（更重要 · 替代高可用）

| 指标 | 目标 | 理由 |
|---|---|---|
| 任一天 briefing 生成失败 | **24h 内 catchup** | worker on-boot 检查 `fetch_runs.last_success` 决定是否回补 |
| arXiv API 抖动容忍 | **3 次 exponential-backoff retry** · 单次调用最多 60s | arXiv 夜间维护窗口偶发 500 |
| LLM provider 抖动容忍 | **5 次 retry**（每次 10s、20s、40s、80s、120s） | 单篇 LLM 调用，抖动 recover |
| DB 备份 | 每日 `pg_dump` 到 `/var/backups/pg/` · 保留 7 份 | `crontab -e` 由 operator 维护 |
| 数据丢失最大窗口（RPO） | **≤ 24h**（昨天 `pg_dump` 之后到故障点） | 符合 solo operator 5 周预算 |
| 恢复时间（RTO） | **≤ 2h**（operator 手动 `pg_restore + systemctl restart`） | 有 runbook 即可 |

### 1.4 错误率

| 指标 | 目标 |
|---|---|
| 请求 5xx 错误率 | < **2%** / 天 |
| Worker 失败率 | 任一周不超 2 天失败 |
| LLM 调用失败率（经 retry 后） | < **1%** |

### 1.5 支持 / incident response

- **无正式 SLA**，operator 自己发现自己修
- Uptime 监控：`cron` + `curl` + `mailx` 脚本每 30 分钟 ping `/today`；连续 2 次失败 → 给 operator 发邮件
- LLM 成本监控：每次 worker 跑完写 `llm_calls` 行；月累计 $40 时发邮件（C11 $50 envelope 预警）

### 1.6 可观测性（solo operator 最小集）

| 工具 | 用途 |
|---|---|
| Postgres `fetch_runs` 表 | 每日 worker 审计 |
| Postgres `llm_calls` 表 | LLM 成本审计 |
| `journalctl -u pi-briefing-*` | systemd 服务日志 |
| 邮件告警 | 失败 / 成本超线 |
| **不装**：Grafana、Prometheus、DataDog、Sentry | 无需；每增加一个服务 = 一个 on-call 点 |

---

## 2. v1.0 · aspirational · 仅在 60 天 dogfood 后 operator 决定商业化时适用

**此节为 aspirational**，v0.1 ship 时**不实现**；作为未来路径的锚点，避免 v0.1 做出让 v1.0 不可能的早期决策（C3）。

### 2.1 可用性

| 指标 | 目标 |
|---|---|
| 整体 uptime | **99.5%** monthly（≤ 3.6h 下线/月） |
| `/today` briefing 可用 | **99.9%** at 08:00 local · 任一 lab |
| Daily briefing 生成完成 | **07:00** · 6/7 天 · 任一 lab |

### 2.2 延迟（≤ 15 concurrent seats · per lab）

| 路径 | p95 目标 |
|---|---|
| `/today` SSR | < **500ms** |
| `/topics`, `/breadcrumbs` | < **700ms** |
| 4-action POST | < **300ms** |
| JSON export | < **5s**（同样数据规模） |

### 2.3 支持 SLA

| 等级 | 响应 | 解决 |
|---|---|---|
| P1（briefing 不出、auth 全挂） | 1h | 4h |
| P2（单 topic 断 / resurface 不触发） | 8h（工作时间） | 48h |
| P3（UI bug / 显示问题） | 3 工作日 | 下一 release |

### 2.4 Error budget policy

- Monthly error budget = 99.5% 对应 3.6h downtime
- 若某月 error budget 耗尽，**冻结新 feature 1 个 sprint**（2 周），只允 reliability 工作

### 2.5 扩展性上限

v1.0 不是水平扩展目标；若单 lab > 15 seat 或同时有 > 5 个 lab 在一个实例，则 re-architecture，不在 SLA 范围。

---

## 3. 测量方法（v0.1 可执行）

| SLA 项 | 工具 | 命令 |
|---|---|---|
| `/today` 可用 | cron + curl | `* * * * * curl -fsS https://.../today > /dev/null \|\| mail -s 'down' operator@` |
| p95 latency | Playwright smoke | `pnpm test:perf --runs=20 --p95` |
| Worker 6/7 成功 | Postgres | `SELECT date_trunc('day', started_at), bool_or(status='ok') FROM fetch_runs WHERE started_at > now() - 7 days GROUP BY 1` |
| LLM 成本 | Postgres | `SELECT sum(cost_cents)/100.0 FROM llm_calls WHERE created_at > date_trunc('month', now())` |
| DB backup 完整 | filesystem | `find /var/backups/pg -mtime -2 -name '*.dump'` |

**Self-report 指标**：O1–O5 的验收（见 `spec.md` §6）不在本 SLA；本 SLA 仅关心服务层 SLO，不关心用户行为。

---

## 4. 对红线的自守 · v0.1

以下 SLA 项不是纯 SLO，**而是守 PRD 三红线的机械兜底**，违反即视为 P1 事故：

| 机械兜底 | 守的红线 | 触发条件 |
|---|---|---|
| LLM summary > 3 句时 adapter 外层截断 | R2 · 不替代阅读 | `summary.split(/[.!?]\s+/).length > 3` |
| 任何 endpoint 无 auth middleware | R3 · 不做公开 view | CI 扫描：每个 route file 必须 import auth middleware |
| Topic 数 > 15 时 topic CRUD 返回 400 | R1 · 不扩通用发现器 | admin POST /topics 时检查 `count(topics) < 15` |

这三条若被绕过 → P1 事故 → 立即 rollback + root cause。

---

## 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · v0.1 + v1.0 分层 SLA · 自守红线机械兜底 |
