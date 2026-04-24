# SLA — 003-pA · RecallKit v0.1

**Version**: 0.2 · **Updated**: 2026-04-24(R1 macOS test 兼容性修复 + USD 硬帽前置验证)· **Source**: spec.md §6 / PRD §6

---

## 0. 一页结论

**v0.1** = 单人本机 OSS CLI 工具,无 uptime SLA(不是服务),所有目标是**单 run 内**的可观测 metric;**v1.0**(展望)= 多 backend 可插拔 + 研究问题级协调,仍不做 SaaS / uptime SLA。

---

## 1. v0.1 (MVP / 单人 / OSS)

### 1.1 核心 metric(均对应 spec.md §6 verification)

| 维度 | 目标 | 度量方式 | 对应 PRD outcome |
|---|---|---|---|
| **单 run 端到端 wall-clock** | **< 12h**(LoRA SFT 7B 规模) | `runs/<id>/config.yaml.wall_clock_seconds` < 43200 | O5 |
| **单 run API USD** | **< $30**(Anthropic 部分,不含 HF/compute)· **proxy 前置硬帽(C20)** | ① proxy 预估拒请求:`tests/integration/test_proxy_prerejects_on_budget.py` 构造"余额紧缺"场景(`state.usd_spent=29.9`, cap=30),proxy 对下一个请求返回 **402/429**,Anthropic mock 端断言**0 次被调用**;② Budget Tracker 60s 轮询 `usd_total` 作为兜底,正常情况下**不应**触发 SIGINT;③ 人工构造预算紧缺 run(`--usd-cap 0.05`)实测 proxy 返回 4xx | O5 |
| **resume 成功率** | **> 95%**(kill 后 `pars sft resume` 能续,结果与未 kill 误差 < 1%) | `tests/integration/test_resume_after_kill.py` + 操作员月度抽测 | O3 |
| **stuck 误杀率** | **= 0**(LoRA 一 epoch 30-90min 全程不误判) | `tests/integration/test_stuck_no_false_positive_during_lora_epoch.py` | O7 |
| **报告 schema 合规** | **= 100%**(每份 report.md 都含强制 sections) | `tests/test_report_schema.py` 在 CI 上 100% 通过 | O2 |
| **compare 功能** | `pars compare` 对任意 2 个 run 可生成可读 diff | `tests/integration/test_compare_two_runs.py` | O6 |
| **demo 可复现** | 他人在独立 4090 机器按 README 步骤跑完,产 report.md 与原 demo 仅时间戳/UUID 差异 | 人审签字(PR checklist) | O1, O4 |

### 1.2 可用性 / 服务相关(明示不适用)

| 项 | v0.1 承诺 |
|---|---|
| **Uptime / 服务可用性** | **N/A**(不是服务,是本机 CLI 工具) |
| **外部依赖宕机** | Anthropic API 宕机 → worker SIGINT + state 保留 + 操作员之后 resume;HF hub 宕机 → 下载 retry 3 次后 fail |
| **API 速率限制** | LiteLLM proxy 遇 429 自动退避;budget 仍按实际烧入 |
| **Incident response** | **informal**(单人 OSS,GitHub issue 答复 best-effort) |
| **Support SLA** | 无正式 SLA;README 明示"best-effort + 欢迎 PR" |
| **数据持久性** | 所有 run artifact 本地 SSD,不做云备份;操作员自己 rsync |

### 1.3 质量 / 性能 metric

| 维度 | 目标 |
|---|---|
| **`pars sft start` 启动到第一个 tool_use 事件** | < 60s(冷启动含 worker 派生 + proxy 启动) |
| **`pars status <id>` 响应时间** | < 2s(读 state.json 即可) |
| **`pars compare` 响应时间** | < 5s(读两份 config + metric 的文件 diff) |
| **CLI 内存占用(host 主控)** | < 500MB(不含 worker 子进程) |
| **Report 渲染** | < 10s(matplotlib 训练曲线 PNG 生成) |
| **Stuck 检测采样周期** | **5s**(详 architecture.md §8.1 契约;60s 滚动窗口 = 12 个 5s 样本,deque maxlen=12);不能更短(不必要烧 CPU),不能更长(30s / 60s 条件粒度不足) |
| **Budget tracker 精度** | 计量延迟 < 5s(单 worker 场景无并发问题,直接解析 stream-json) |

### 1.4 安全承诺

| 承诺 | 如何验证 |
|---|---|
| **`ANTHROPIC_API_KEY` 不进 worker subprocess env** | 单测 `test_worker_env_no_api_key`(fork worker → macOS 用 `psutil.Process(pid).environ()` 读 env;Linux 也用 psutil 统一;**不用 `/proc/<pid>/environ`**,因为 macOS 无 procfs)断言无 `ANTHROPIC_API_KEY` |
| **host `.claude/` 在 worker 视角只读** | 单测 `test_worker_cannot_write_claude_dir`(worker 尝试 `echo x > .claude/settings.json` → 预期 EACCES) |
| **`pip install` 仅允许 locked** | 单测 `test_pip_install_deny_unlocked`(worker 尝试 `pip install requests` → hook deny) |
| **`rm -rf /` / `curl 外部` / `cat .env` 被 hook deny** | 单测 `test_deny_dangerous_commands` |
| **API proxy 仅 bind 127.0.0.1** | 单测 `test_proxy_not_accessible_from_lan` |
| **Stuck 连续 3 次 restart 后不再自动重启** | 单测 `test_stuck_restart_circuit_breaker` |

---

## 2. v1.0(展望,非必须实现)

> v1.0 未承诺上线时间;列在此是让 v0.1 的架构决策**不把 v1.0 堵死**。若操作员未来启动 v0.2/v1.0,需重审此节。

### 2.1 新增 metric

| 维度 | v1.0 目标 |
|---|---|
| **支持多研究问题并发** | 仍保持单 worker 顺序,但 ledger 按"研究问题 → runs"组织;对应 PRD OQ7 |
| **训练后端可插拔** | Unsloth + Axolotl + torchtune 任选,通过 `config.yaml.backend` 切换 |
| **评测后端可插拔** | LM Eval Harness + 自定义 task + Open LLM Leaderboard 对齐模式 |
| **轻量 sidecar(可选)** | 运行时摘要搭档,**默认关闭**,操作员手动开(L3 stage doc 预留) |
| **cross-run 知识迁移** | 可选的"上 run 摘要 → 下 run 系统提示" |
| **远程 GPU 选择性集成** | 仍**不做** Runpod 自动调度;但 `pars sft start --remote <ssh-alias>` 可触发 rsync + remote exec(C9 的自然延伸) |

### 2.2 仍不做

- ❌ SaaS / hosted service
- ❌ Multi-tenant
- ❌ 自动 Runpod 调度
- ❌ LLM-as-judge(除非出现强 research 支持数据)
- ❌ Web UI / Streamlit dashboard
- ❌ uptime SLA(还是 OSS CLI)

### 2.3 迁移路径(v0.1 → v1.0 兼容性承诺)

- `runs/<id>/config.yaml` schema 向后兼容(v1.0 读得了 v0.1)
- CLI 命令 `pars sft start/status/...` 不破坏性改名(仅新增 `pars sft upgrade` 等)
- MIT LICENSE 不变
- 依赖升级 review 月度化

---

## 3. 如何度量(v0.1 实现)

**本机**(无外部监控):

| metric | 实现 |
|---|---|
| **wall_clock_seconds / usd_total / gpu_hours** | Budget Tracker 每 60s 写 `runs/<id>/state.json` |
| **stuck 误杀率** | 手工跑 `test_stuck_no_false_positive_during_lora_epoch.py`(CI 跑 mock-LoRA,月度跑真 LoRA) |
| **resume 成功率** | 集成测试 + 操作员月度抽测(月度日志 checklist) |
| **报告 schema 合规** | CI 每 PR 跑 `test_report_schema` |
| **API proxy 性能** | LiteLLM 自带日志 → `runs/<id>/artifacts/api_log.jsonl`,P95 < 2s 是预期(不是 SLA) |

**无外部工具依赖**:
- 不装 Prometheus / Grafana / Sentry / Datadog
- 所有"监控" = `cat runs/<id>/state.json` / `cat runs/<id>/metrics.jsonl` / `pars status <id>`
- CI 监控 = GitHub Actions 自带 log + job status

---

## 4. Error budget(不适用 v0.1)

v0.1 不是服务,无 "error budget"。取而代之的**质量 gate**:

| Gate | 动作 |
|---|---|
| **单测 coverage < 70%** | PR block |
| **集成测试失败** | PR block |
| **ruff / Conventional Commits lint 失败** | PR block |
| **`pip-audit` 出现 critical / high** | PR block,1 周内修复 |
| **demo 不能在 CI (mock-LoRA smoke) 跑通** | release block |
| **操作员本机跑真 demo fail** | 不 release tag,回滚 |

---

## 5. 对外声明(README 原文占位)

> RecallKit v0.1 是单人 OSS CLI 工具。
> - **无** 服务 uptime 承诺(不是 SaaS)
> - 单 run 典型 wall-clock < 12h、API 费 < $30(Qwen3-4B 级别)
> - 所有数据本地,不传云
> - MIT License,欢迎 PR 与 issue,best-effort 响应
> - 硬件假设:NVIDIA 24GB+ GPU(推荐 4090);MPS / ROCm 暂不覆盖
> - v1.0 路线见 `docs/ROADMAP.md`(若存在)
