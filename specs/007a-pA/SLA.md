# SLA — 007a-pA

**Version**: 0.3
**Created**: 2026-05-08T13:30:00Z
**Revised**: 2026-05-08T14:30:00Z(R2 修订:M-R2-1 PIPE_BUF 措辞替换为 POSIX O_APPEND semantics / B-R2-3 review-mode 流程对齐 set_review_mode 与 enabled 正交;**R3/R4 narrow drift fix** — review session 流程加 `--on` 完整恢复语义 vs `--review-mode-off` 部分恢复区分 · H-R3-1)
**PRD-form**: simple → 单一 v0.1 SLA 段
**Source spec**: spec.md v0.3 + architecture.md §7 + R1/R2/R3/R4 review fix

## v0.1(MVP · single-operator dogfood substrate)

### Capture latency(hook fire window)
- **Hook end-to-end p95 ≤ 200 ms**(stdin parse + state.json read + judge classify + judge filter + **D19 redact regex** + format + atomic append)
- **Hook end-to-end p99 ≤ 500 ms**
- **Bound by Claude Code 自身 hook execution timing** — 无独立网络往返;不应阻塞 Claude Code session
- **R1 SEC-2 redact 影响**:`_redact_secrets()` 是 7 条 regex 顺序 sub,在 200 char 截断后跑,实测 < 1 ms 不影响 p95
- **测量**:hook.py 内部 wall-clock 计时,可选追加到 entry trailing(开发期);v0.1 不强制持续监控,operator 主观感觉无卡顿即视为通过

### Capture reliability(precision > recall · C11)
- **False-negative tolerance**:hook 漏 fire 至多 ~10%(L2 §6 cond + PRD UX 原则)
  - 真实场景:agent 漏报 / Claude Code hook payload 字段缺失 / disk full 等边缘
  - **Mitigation**:operator-fallback `friction <msg>` CLI 兜底 subjective 与漏报
- **False-positive tolerance**:`[disputed]` 比例 ≤ 20%(O2 数值)
  - 超过 20% → secondary risk 触发(risks.md TECH-2)
  - **Mitigation**:`friction --threshold high` 一行收紧;`friction --off` 一行止血(D10 mark, don't delete)

### Storage availability
- **本地 markdown 文件**;无远程依赖
- **Disk 满 / 权限错** → 抛 `IOError`,hook 路径 silently swallow,CLI 路径 fail loud
- **可用性目标**:与 macOS filesystem 同等(operator 能用 macOS = 工具能用)
- **数据持久性**:friction-log 写入是 `O_APPEND` 单 write 在本地 POSIX regular file 上原子(macOS APFS / Linux ext4 实测;**非 PIPE_BUF 语义** — PIPE_BUF 仅适用于 pipe/FIFO,不适用于 regular file;实际原子保证来自 POSIX `O_APPEND` semantics for regular file appends;4 KiB 是 conservative engineering bound 而非 PIPE_BUF cap — R2 M-R2-1 fix · architecture §5.3 措辞修订);不会因为部分写产生 partial entry

### Review ergonomics(O4)
- **Operator 能在 ≤ 10 min 内审阅 20 条 entry + 在每条下方追加 tag**(O4 verification)
- **测量**:operator stopwatch 自测;grep-friendly 单行格式 + markdown plain text 编辑保证
- **R1 H2 + R2 B-R2-3 + R3/R4 H-R3-1 / C14 / D17 / D20 / D21:Review session 流程**:
  1. 进 review session 前必跑 `friction --review-mode`(设 `state.review_mode=true`,**不动 `state.enabled`** — hook gate 短路防 stale-save tag 误绑)
  2. 编辑 friction-log
  3. 完成后**两种退出路径**(R3/R4 H-R3-1 / D21):
     - 若 review session 前 enabled 一直为 true(典型场景)→ 用 `friction --review-mode-off`(部分恢复 — 只清 review_mode,enabled 保 true)
     - 若 review session 前已 `--off` 又进 review session(混合场景)→ 用 `friction --on`(完整恢复 — set_enabled=true AND set_review_mode=false;stdout 显式打印 `review_mode cleared`)
     - **保守建议**:不确定时用 `--on`(完整恢复永远 safe,不会让 review_mode 卡 true)
  4. **关键变更(R2 B-R2-3)**:review_mode 与 enabled 正交 — review session 期间 day-14 trust_summary 跑 `--check-enabled` 仍 PASS(O3 不受 review_mode 影响 · D20),修复了 R1 H2 原方案"review session 让 enabled=false 触发 false adoption fail"的设计冲突
  5. **R3/R4 H-R3-2 stuck-true 防护**:trust_summary 输出 `## Hook Operational Status` 段显示 `state.review_mode` 当前值;若 review_mode 持续 > 24h → 段内含 WARNING(operator 在 day-14 review 能看到 review_mode 卡死,而不是只看到 O3 PASS 的 false adoption signal)
  6. 不遵循此流程 → 编辑器 stale snapshot 写回会丢 hook 期间的新 entry + tag 物理位置错位

### Day-14 trust mini-summary timing
- **launchd 触发误差 ≤ ±5 min**(macOS launchd 文档);对 day-14 单次足够
- **trust-summary 渲染时间 ≤ 5 s**(grep 14 天 markdown 文件,典型 < 100 行)
- **Self-interview prompt 必有**(D14 / O6 / R1 H1 结构化):脚本固定追加 `[label:` 与 `Reason:` 两行模板,不依赖 operator action
- **R1 B2 health 等价 metric**:`python -m friction_tap.trust_summary --check-enabled` < 100ms;`--check-self-interview` < 200ms

### Schema health metric(R1 H3 新增)
- **`schema_error_count` 是 monotone counter**,每次 hook payload schema drift +1;day-14 trust-summary `## Schema health` 段可见
- **Target**:14 天内 `schema_error_count == 0` 是健康;> 0 表 Claude Code 升级 / hook 注册问题
- **告警**:R1 v0.1 不实现 active alerting(C2 single-operator 无 on-call)— operator 在 day-14 review 自见

### Error response
- **Informal**:operator 自己排错;无 on-call;无 alerts
- **Operator 发现 hook 异常**(eg dogfood 第 3 天没 entry 但记忆中至少卡过 5 次):
  1. **R1 B2 修订**:`python -m friction_tap.trust_summary --check-enabled` → 看 state.enabled
  2. **R1 B2 修订**:`python -m friction_tap.grep --count-agent-emit --since=24h` → 看最近 24h capture 数
  3. `tail docs/dogfood/v4-friction-log.md` → 验证最近 entry
  4. **R1 H3 修订**:`friction --status` 看 `schema_error_count`,> 0 → 见 last_run.log traceback
  5. 必要时 `friction --off && friction --on` 重置 state(v0.1 不提供 `--reset-state` flag,留 v0.2)
- **No formal incident SLA**(C2 single-operator)

### Support SLA
- **None**(C2 single-operator;C9 不拼时间);operator 即维护者
- 若日后 ship 给 ADP(C8 v0.2)→ 重新评估 support 模型

### Privacy & data retention
- **default private**(C2 + C5 RL-3 + C10):log 文件在 repo 内,operator 决定是否 .gitignore;README 提供 .gitignore 建议(详见 risks.md SEC-1)
- **No external network call**:hook / CLI / trust_summary 全部 offline
- **No telemetry**:不向任何第三方上报;不收集 operator behavior

## How we measure

| Metric | 测量方法 |
|---|---|
| Hook latency | hook.py 内部 wall-clock(可选 print to stderr / 写到 last_run.log);v0.1 不强制 dashboard |
| Capture reliability | day-14 trust mini-summary 输出 entry 总数 + 三种 tag 比例(脚本) |
| Review ergonomics | operator stopwatch 自测;trust mini-summary §"Outcome check" §O4 字段 |
| Day-14 trigger 准确度 | `~/.config/friction-tap/last_run.log` 实际 fire 时间 - install_at + 14d |
| Storage availability | macOS filesystem 自身可用性;无独立监控 |

## What this v0.1 does NOT promise

- 不承诺 100% recall(C11 precision > recall;仅 ~10% 漏报容忍)
- 不承诺 LLM-quality friction signal 判定(D3 静态规则)
- 不承诺多 operator / 团队 SLA(C2 single-operator)
- 不承诺跨仓 / ADP availability(C8 IDS first)
- 不承诺 data sync / cloud backup(C5 RL-3 offline only)
- 不承诺 24/7 support(C2 + C9)

## v0.2+ 候选 SLA 演化(留存,未承诺)

(以下是 v0.2 候选 — 不在本 v0.1 SLA 内,仅备忘)

- 跨仓 ship 后:per-repo capture latency 一致性 ≤ 50 ms 偏差
- LLM-judge 引入后:disputed_ratio 目标 ≤ 10%(优化目标)
- weekly review ritual(Candidate C)引入后:weekly review 完成率 ≥ 50%

> 这些不是承诺,是 v0.2 设计参考,具体由 day-14 verdict 决定。
