# SLA — 004-pB · 决策账本

**Version**: 0.1
**Created**: 2026-04-25T15:15:00+08:00
**Companion**: `spec.md` §6 verification / O5-O8 / O10

> 这是**单用户 localhost 自用工具**, 没有正式商业 SLA 概念。本文档定义的是
> **可度量的工程目标 (Service Level Objectives, SLO)**, 用于工程团队 (= human +
> AI agents) 设计决策与回归监控。

---

## 1. v0.1 (MVP / 单用户自用)

### 1.1 可用性

| 指标 | 目标 | 说明 |
|------|------|------|
| 系统启动成功率 | 100% | `./scripts/start.sh` 必须 5 秒内完成启动并打印 `[OK] http://localhost:8000` |
| Web UI 可达 | best-effort | localhost 单进程, 进程崩 = 不可达; 无正式 incident SLA |
| Telegram bot 在线 | best-effort | 长轮询断线自动重连 ≤ 1min |

无外部用户, 无 9-9-9 / 99.9% / on-call。

### 1.2 性能 (latency / throughput)

| 流程 | 目标 | 测量方式 |
|------|------|---------|
| **Web UI 第一屏** | **< 2 秒** (PRD §UX 4 "5 秒看完", 给 2 秒上限留余量) | 浏览器 DevTools Performance + E2E test 断言 |
| **决策录入提交 (POST /decisions)** | p50 < 200ms, **p95 < 500ms** | FastAPI middleware log + pytest-benchmark |
| **决策录入端到端 (打开页 → 提交确认)** | **< 30 秒 (硬门槛, C11 / O5)** | E2E playwright timing test + 5 次手动压测 |
| **首次 onboarding 完成** | **≤ 15 分钟 (C12 / O6)** | onboarding flow 内置计时, 写 `release_log.jsonl` |
| **PDF 解析 (单份咨询师周报)** | < 30 秒 (后台不阻塞) | parser job log + integration test |
| **LLM 调用 (conflict_resolve 一次)** | < 30 秒 (后台异步可接受) | LLM 调用 log; **此目标允许慢, 但不允许阻塞录入** |
| **三路冲突报告生成 (含 LLM)** | 后台 < 60 秒 | 录入提交后 60s 内 conflict_report_ref 应已 populate |
| **周报 cron 完整跑通** | < 5 分钟 | apscheduler job log |

### 1.3 错误率

| 指标 | 目标 |
|------|------|
| 决策录入失败率 | **< 1%** (失败 = 提交后未入库) |
| LLM 调用失败率 (含 retry 后) | < 5% |
| PDF 解析失败率 | < 30% (PDF 多样性强, 失败可入 parse_failures 由 human 手动结构化) |
| Telegram push 失败率 | < 5% |

### 1.4 UX 硬约束

| 指标 | 目标 | 违反后果 |
|------|------|---------|
| **单次决策录入耗时** | **< 30 秒** | **系统失败 (Risk #1)** — 触发 O10 告警 → 降级到 B-lite |
| **首次 onboarding** | ≤ 15 分钟 | 74% rule, 必须达成 |
| **稳定期维护时间** | ≤ 3 小时/周 | 红线 R5, 违反触发 scope down |
| **Telegram push 频率** | 每周 ≤ 1 次周报 + event 触发 | 红线 R4, 测试 `test_telegram_cadence.py` |

### 1.5 失败告警 (O10) SLO

| 指标 | 目标 |
|------|------|
| 告警检测延迟 | ≤ 24 小时 (daily cron 09:00 触发) |
| 告警通道 | Telegram + Web banner 双通道, 任一失败仍可触达 |
| 告警 false-positive 率 | < 5% (mock 测试 + 1 次 dry-run 验证) |

### 1.6 数据可靠性

| 指标 | 目标 |
|------|------|
| SQLite 备份频率 | weekly (cron 复制 db 文件) |
| 数据丢失容忍 | ≤ 7 天 (上次备份后) |
| 灾难恢复 | 单文件复制即可 (D5 简化) |

### 1.7 安全 / 隐私

| 指标 | 目标 |
|------|------|
| FastAPI 监听地址 | **永远 127.0.0.1**, 不允许 0.0.0.0 (架构 §9 不变量) |
| API key 存储 | `.env` (gitignored), 启动时检查 |
| 咨询师 PDF / 解析结果 | 仅本地, 不 export, 不 commit |
| 不接 webhook 公网 | Telegram 用 long-polling, 无 ngrok |

### 1.8 不在 v0.1 SLO 内的项目

- 多用户负载 (永远不是单用户外的需求)
- p95 < 100ms (单用户 localhost, p95 < 500ms 已远超需求)
- 99.x% uptime (无外部用户依赖)
- on-call response time
- error budget burn rate
- DR (disaster recovery) RPO/RTO 数字承诺

---

## 2. v1.0 (假设性, 仅用于评估"是否会演化")

> ⚠️ **本节是非约束性参考**, **v0.1 不为 v1.0 做预留**。
> 唯一明确的 v1.0+ 接口预留: `ReviewGenerator.audience: enum {self, partner}` (D18)

### 2.1 如果 v1.0 仍是单用户私用 (likely)
- SLA 概念仍然不适用
- 性能 / 可用性目标延续 v0.1
- 仅 UX 优化 + 真 ML 模型替换占位 + 多模态解析

### 2.2 如果 v1.0 fork 出多用户 / 商业化 (NOT in this fork's scope)
- ⚠️ 这条路径 **不在 004-pB scope 内**, 红线 R1 (永远红线 #6 商业化) 阻断
- 若未来 fork 出 `004-pB-commercial`, **整个 SLA 需重写**:
  - 99.5% monthly uptime
  - p95 < 500ms 顶级流
  - error budget policy
  - on-call SLA
  - 合规重审 (见 compliance.md)

---

## 3. 测量工具与方法

### 3.1 性能监控 (单进程)
- **Latency**: FastAPI middleware 写入 SQLite `request_log` 表 (timestamp + path + duration_ms); Web UI 设置页查最近 24h p50/p95
- **LLM cost / token**: SQLite `llm_usage` 表 (每次调用记录 prompt_tokens / output_tokens / cost_usd / cache_hit)
- **维护时间**: human 自报, weekly review 内置一栏

### 3.2 错误监控
- **应用日志**: structlog → `~/decision_ledger/logs/app.jsonl` (JSON line)
- **未捕获异常**: FastAPI exception handler 写 `errors` 表 + Web UI 红色 banner
- **告警事件**: `alerts` 表 audit trail

### 3.3 SLO 报告
- **每周 review** 自动汇总: 录入次数 / 录入平均耗时 / LLM 成本 / push 次数 / 错误数
- **每月 review** 输出 SLO 达成度 (录入 < 30s 命中率 / push 节制达成率)

### 3.4 自动化 SLO 测试 (CI 跑)

```bash
# 录入 < 30s 的回归测试
uv run pytest tests/e2e/test_decision_input_timing.py

# Telegram cadence 节制
uv run pytest tests/integration/test_telegram_cadence.py

# 失败告警链路
uv run pytest tests/integration/test_failure_alert.py

# Web UI 第一屏 < 2s
uv run pytest tests/e2e/test_first_screen_latency.py
```

---

## 4. SLO 违反处理流程 (单人项目专属)

由于无外部用户, 没有 incident management 流程。简化版:

| 违反 | 严重度 | 处理 |
|------|------|------|
| 录入 > 30s | **Critical** | 立即修复 / 降级 UX / B-lite |
| Telegram push 超频 | High | 修 rate limiter, 单测覆盖 |
| LLM 成本失控 (月超 $50) | Medium | 检查 cache 命中率, 考虑模型降级 (Haiku) |
| Web UI 首屏 > 2s | Low | 下次 sprint 修 |
| PDF 解析失败 > 30% | Medium | 改 prompt / 升级 pdfplumber |

---

## 5. 与 PRD outcomes 的映射

| Outcome | SLO | 测试 |
|---------|-----|------|
| O5 (录入 < 30s) | §1.4 + §1.2 | `test_decision_input_timing.py` + `manual_press_test.py` |
| O6 (onboarding ≤ 15min) | §1.4 | `test_onboarding.py` |
| O7 (维护 ≤ 3h/周) | §1.4 | weekly review 内置 |
| O8 (Telegram 节制) | §1.4 + §1.3 | `test_telegram_cadence.py` |
| O10 (失败告警 24h 内) | §1.5 | `test_failure_alert.py` + dry-run |
