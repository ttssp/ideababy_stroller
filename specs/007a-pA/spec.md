# Spec — 007a-pA · 证词契约日志(agent-emit friction archive · v0.1 substrate + day-14 trust prompt)

**Version**: 0.3
**Created**: 2026-05-08T13:30:00Z
**Revised**: 2026-05-08T14:30:00Z(R2 adversarial review propagation fix — B-R2-1/B-R2-2/B-R2-3 + H-R2-1/H-R2-2/H-R2-3 + 4 medium drift;**R3/R4 narrow drift fix** — B-R3-1 C14 重写不再"`--review-mode` alias `--off`" + spec task summary alias 措辞 / H-R3-1 加 D21 `--on` 完整恢复语义 / H-R3-2 trust_summary 加 `## Hook Operational Status` 段 + stuck-true WARNING / Partial-1 PROD-3 health_check → CLI 入口 / M-R3-1 SCH-1 hours/cap 数字更新 / M-R3-2/3 architecture+SLA source spec → v0.3)
**Source PRD**: discussion/007/007a-agent-emit/007a-pA/PRD.md(version 1.1,human-approved via fork · C1 12-23h sign-off 2026-05-08)
**PRD-form**: simple
**Lineage**: 007 (proposal · "friction-tap") → 007 L1 Direction 1 "主语反转" → 007a-agent-emit (L2 + L3) → 007a-pA (PRD fork: Candidate A + 1 day-14 self-interview question hybrid)

---

## 1. Outcomes

> 全部从 PRD §"Success — observable outcomes"复述,每条 outcome 是 user/business 可观察的结果,数字与 PRD 对齐。

- **O1 · Capture 工作**:第 14 天 friction-log 累计 ≥ 8 条 `[agent-emit]` entry(证明 hook 在工作)。
- **O2 · Trust 在线**:第 14 天 trust mini-summary 显示 `[acked]` 比例 ≥ 50% 且 `[disputed]` ≤ 20%(operator 没频繁觉得 entry 不准)。
- **O3 · Adoption signal**:第 14 天 hook 仍 enabled — operator 未在 day 14 之前主动 `friction --off`(**单指标 binary,`state.json` 中 `enabled = true` 即 pass**;**`state.review_mode` 与 O3 正交,不影响 verdict** — R2 B-R2-3 / D20 fix)。**严格遵循 PRD §"Success" L78 原意**;**activity freshness 单列 informational metric**(在 trust-summary 输出中显示"最近 24h 是否有 agent-emit entry",但**不进 O3 verdict**,避免 BUS-1 operator 暂离场景产生 false adoption failure。R1 B3 fix。)
- **O4 · Review 体验**:operator 能在 10 分钟内审阅 20 条 entry(grep-friendly format 的产物;可由 operator 自报或 stopwatch 测得)。
- **O5 · 主观确认**:operator 能 named 指出至少 3 条改善了 retrospective recall 的 entry(主观但可记录,Yashu 自报)。
- **O6 · Hybrid · adoption-decision answered**:第 14 天 `docs/dogfood/v4-trust-w2.md` 末尾的 `**Self-interview**: After 2 weeks, do you feel relieved / watched / both?` prompt 已被 operator 用结构化答案填完。**结构化要求(R1 H1 fix)**:答案必须含 (a) 标签字段 `[label: relieved|watched|both]`(三选一);(b) 自由文本 reason ≥ 20 CJK 字符 OR ≥ 8 English words。仅写 "both" 一词不足以 pass。verification 见 §6 + T020 prompt 模板格式。

## 2. Scope Boundaries

### 2.1 In scope for v0.1

PRD §"Scope IN" 的 10 行 component 表,工程级表达如下(每条 IN 都对应一个 spec.md §5 phase task block):

| # | Component | 工程契约(behavior + interface) |
|---|---|---|
| IN-1 | `PostToolUseFailure` hook script | 接 Claude Code hook payload(JSON via stdin),解析 `tool_name` / `exit_code` / `stderr`(<= 200 chars 截断) / `task_description`,经静态规则判定后 append 一行 entry 到 friction-log。无返回值要求(hook fire-and-forget) |
| IN-2 | 静态规则判定(白/黑名单 + confidence 分类) | 白名单 tool 集 = `{Bash, Edit, Write}` + Claude Code lifecycle hook block 信号(payload 中的 `block: true` 或对应 marker)— **R1 H4 fix:从 v0.1 移除 `Read`,严格遵循 PRD §"Open questions" OQ-E 列出的候选**;黑名单(skip emit)= `--off` state + `task_description` 含字符串 `[debugging-friction-detection]`。**confidence H/M/L 分类基于 event features**(tool kind + 失败信号强度 + stderr pattern),与 threshold 解耦;threshold 仅作为 minimum-confidence filter(R1 B1 fix,详见 architecture §5.2)。 |
| IN-3 | friction-log 硬编码路径 | `<repo-root>/docs/dogfood/v4-friction-log.md`(repo-root = `git rev-parse --show-toplevel`);若目录不存在则 mkdir -p 创建;若仓外 → IN-1 hook 与 IN-6 CLI 行为见 OQ-D 决议(D6) |
| IN-4 | Entry 格式 | 单行 append:`<ISO-8601-UTC> [agent-emit] [confidence:H\|M\|L] [private-to-operator] · <tool> exit <code> · "<stderr-200chars>" · task: <desc>`(privacy 字段 visible) |
| IN-5 | Adjudication tag 约定 + 操作文档 | operator 在任意 entry 行**下方追加一行** `[acked]` / `[disputed]` / `[needs-context]`(可附自由文本);grep -c 可统计;无 state machine,无 entry-id 强制 |
| IN-6 | `friction <msg>` CLI(Python single-file) | `friction "<text>"` → append 一条 `<ISO> [operator-cli] [private-to-operator] · "<msg>"` 到 friction-log;stdlib only,无 venv |
| IN-7 | `friction --off` / `--on` / `--threshold {low,medium,high}` | 一行止血 + 阈值切换;持久化到 `~/.config/friction-tap/state.json`(单一 config 文件,JSON,human-readable);threshold 含义见 architecture §5.2 |
| IN-8 | Day-14 trust mini-summary 脚本 | grep 统计 entry 总数 / 三种 tag 比例 / **hook enabled-only adoption verdict(O3 严格 binary,仅 `state.json.enabled: true`,**无 24h activity 联合判定** — D7 R1 B3 修订)** + **Activity Health 段 informational(最近 24h 是否有 agent-emit entry,**不进 O3 verdict** — 仅作 dogfood activity 信号)** + **Schema Health 段(state.json schema_error_count)**,输出 markdown 到 `docs/dogfood/v4-trust-w2.md`(R2 B-R2-2 fix · 移除 dual-metric 残留) |
| IN-9 | trust mini-summary self-interview prompt | mini-summary 模板末尾追加固定文本:`**Self-interview**: After 2 weeks, do you feel relieved / watched / both? (1 句话)`;operator 直接编辑文件答复,无 form / 无脚本要求 |
| IN-10 | 测试 + commit + 安装文档 | 单元测试静态规则判定 + 集成测试 entry 写入 + README(install / 使用 / privacy promise / off-switch) |

**总工时 22.75h**(R1 修订项 + R2 B-R2-3 review_mode 字段 +0.25h 纳入后,详见 §5 Schedule risk 表格);在 **PRD v1.1 C1(12–23h,2026-05-08 operator sign-off)** 预算内(余量 0.25h),confidence H,2 周 ship 可信。R2 B-R2-1 fix:本行从原 11.5–16.5h 旧估算修订为与 §5 sum 一致的 22.75h。

### 2.2 Explicitly out of scope for v0.1

直接复述 PRD §"Scope OUT"的 11 条非目标:

- **State machine for adjudication**(operator 已 explicit 同意 markdown tag 即可)
- **Skill placeholder 检测 / 其他 lifecycle hook**(C7;v0.2+ 候选)
- **LLM-judge friction signal 判定**(留 v0.2 — 静态规则覆盖 80% 真实信号,LLM 是 disputed 率优化,工程量隐藏成本高)
- **`Read` tool failure 进 v0.1 白名单**(R1 H4:超出 PRD §OQ-E 候选;留 v0.2 — Read failure 通常是 noisy 信号,需先观察 v0.1 真实数据决定是否扩入)
- **`-f path` 持久化为 default**(R1 medium:`-f` 仅"explicit one-shot 路径 override",per-call ephemeral,不写入 state.json,不更改 D4 hardcoded path 立场;configurable persistent path 留 v0.2)
- **`friction --reset-state` 一键修复 corrupted state.json**(R1 medium:state corruption recovery 留 v0.2 — v0.1 由 README 教学 manual `rm ~/.config/friction-tap/state.json` 后下次 `friction --status` 自动重建)
- **跨仓 ship**(C8 IDS first;ADP 4 周等待期不动 → v0.2 加可配路径时 ADP 接入是 free 的)
- **可配 log 路径**(留 v0.2 — v0.1 hardcoded 是 privacy promise 工具,可配反而引入 default-shared 风险)
- **Frontend / dashboard / 可视化**(RL-4 不与 enterprise observability 竞争)
- **团队共享 / multi-reader format / cloud sync / cross-repo aggregation**(C2 single-operator + RL-3 不接合作上传)
- **自动开 issue / PR / fix**(RL-2 不接追责文化)
- **完整 2 周 pilot 协议**(留 v0.2 candidate B — 本 v0.1 只取 day-14 1 题 hedge)
- **完整 weekly review ritual**(留 v0.2 candidate C — scope-reality search 警告 thin prompt 是 underbuilt 风险)
- **跨 dogfood 周期聚合 / shared immune memory**(留 v1.0+ 远 vision)

## 3. Constraints

| # | Constraint | Source | Rigidity |
|---|------------|--------|----------|
| C1 | Time: 1–2 周 ship,5–10 hr/week,**总预算 12–23 小时(PRD v1.1 sign-off,operator 2026-05-08 显式接受 12.5% overshoot)** | PRD §"Real-world constraints" C1 + L3R0 intake Block 1 Q1+Q2 + **PRD v1.1 Revision log(2026-05-08)** | Hard |
| C2 | Audience: single operator dogfood,无 multi-reader 假设 | PRD §"Real-world constraints" + L3R0 default + L2 §6 cond-4 | Hard |
| C3 | Business: free OSS / self-hosted,无 SaaS / 付费 | PRD §"Real-world constraints" + RL-4 | Hard |
| C4 | Platform: macOS · Claude Code `PostToolUseFailure` hook + Python CLI | PRD §"Real-world constraints" + L2 §6 prior art | Hard |
| C5 | 4 红线全 hard:RL-1 不接全知监控 / RL-2 不接追责文化 / RL-3 不接合作上传 / RL-4 不与 enterprise observability 竞争 | PRD §"Real-world constraints" + L3R0 intake Q5 | Hard |
| C6 | v0.1 必含 4 condition:cond-1 审阅入口 / cond-2 entry tone 含 uncertainty / cond-3 week-2 trust monitoring / cond-4 default single-operator + private | PRD §"Real-world constraints" + L2 §6 + L3R0 priorities | Hard |
| C7 | Event scope: 仅 `PostToolUseFailure`(其他 lifecycle hook 留 v0.2+) | PRD §"Real-world constraints" + L3R0 intake Q4 | Hard |
| C8 | Ship target: IDS first,4 周等待期不动 ADP | PRD §"Real-world constraints" + L3R0 intake Q3 | Hard |
| C9 | friction-tap 不能拼动 operator 太多时间(catch-all 反向压力) | PRD §"Real-world constraints" + L3R0 catch-all | Hard |
| C10 | Privacy as visible promise,not hidden assumption(entry 有 `[private-to-operator]` 字段) | PRD §"Real-world constraints" + GPT L3R2 §1 push back | Hard |
| C11 | Precision > recall(false-positive 成本是 trust loss > miss 成本) | PRD §"Real-world constraints" + L2 §6 + Opus L3R2 UX 原则 | Hard |
| C12 | Solo operator 可维护性:无 venv / 无第三方包(stdlib only)— 维持工具自身 friction 极低 | 工程级 + C9 推论 | Hard |
| C13 | 默认 off / opt-in:hook 非 dogfood 模式不应自动 emit(否则非 dogfood 阶段 log 膨胀,L2 §5 明示) | L2 §5 末段 + C2 推论 | Soft(v0.1 通过 `friction --on` 显式 opt-in 实现) |
| C14 | **Adjudication review session 期间 hook 必须暂停 emit**(R1 H2 + R2 B-R2-3 + R3/R4 B-R3-1 fix):operator 在 friction-log 文件上手编辑 `[acked]/[disputed]/[needs-context]` tag 期间,必须先 `friction --review-mode` 把 `state.review_mode` 设为 true(**不动 `state.enabled`** · D17);hook gate 行为 = `state.enabled AND NOT state.review_mode`(architecture §5.1 Stage A1b);完成后用 `friction --review-mode-off` 退出 review_mode(不需要 `--on`,enabled 从未变);**O3 严格只看 `state.enabled`,与 `state.review_mode` 正交**(D20),review session 期间 day-14 trust_summary `--check-enabled` 仍 PASS。否则 hook 与编辑器并发 append 可能产生 stale-save 覆盖 / tag 误绑 race | R1 H2 + R2 B-R2-3 + R3/R4 B-R3-1 + ADR-3 物理位置绑定的脆弱面 | Hard(README 明示 + CLI `--review-mode` / `--review-mode-off` 独立 state field 防呆 + T031 集成测试 TestStaleSaveTagRebinding + TestO3PassesDuringReviewMode 覆盖) |

## 4. Prior Decisions

> 这些是进 spec.md 时已经定下的决策 — 不再 re-litigate。每条引源。

| # | Decision | Source |
|---|----------|--------|
| D1 | Backend / 实现语言 = Python 3.11+ stdlib only,无第三方包,无 venv | PRD §"Real-world constraints" C4 + 用户 plan-start 指令明示 + C12 推论 |
| D2 | 载体 = Claude Code `PostToolUseFailure` hook(已 documented 工业化;无需 wrapper) | PRD §"Real-world constraints" C4 + L2 §6 prior art GREEN |
| D3 | friction signal 判定 = 静态规则(白名单 tool + 黑名单 keyword/state),非 LLM-judge | PRD §"Scope OUT" + L3 §"❓ items resolved" OQ-2 |
| D4 | log 路径 = hardcoded `docs/dogfood/v4-friction-log.md`(privacy promise 工具) | PRD §"Scope OUT" + L3 OQ-4 决议 |
| D5 | Adjudication = markdown tag(`[acked]` / `[disputed]` / `[needs-context]`),无 state machine,无 entry-id | PRD §"UX principles" simplicity > cleverness + L3 OQ-1 决议 |
| D6 | OQ-D 决议:cwd 不在 git 仓库 → CLI / hook 显式报错让 operator 用 `friction -f <path>`,**不 fallback 到 `~/.claude/global-friction-log.md`**(显式优于隐式;privacy 不能 fallback 到隐藏路径) | PRD §"Open questions" OQ-D + 用户 plan-start 指令明示 |
| D7 | OQ-C 决议(R1 B3 修订):"hook 是否仍 enabled" 用 **observational metric · O3 严格 binary** — 脚本检查 `state.json` 中 `enabled: true`(单指标);最近 24h 有 ≥ 1 条 agent-emit entry 单列为 **informational `## Activity health` metric,不进 O3 verdict**。**严格遵循 PRD §"Success" L78 原意**;原 spec 双指标设计在 BUS-1 / OPS-2(operator 暂离)场景下产生 false adoption fail,R1 B3 fix 移除 | PRD §"Open questions" OQ-C + 用户 plan-start 指令明示 + R1 B3 fix |
| D8 | OQ-E 决议(R1 H4 修订):静态规则 v0.1 白名单 = `{Bash, Edit, Write}` 的 tool failure + Claude Code lifecycle hook block 信号(payload 中含 `block: true` / 等价 marker)。**`Read` 不在 v0.1 白名单 — 严格遵循 PRD §"Open questions" L137 OQ-E 候选,留 v0.2 候选** | PRD §"Open questions" OQ-E + R1 H4 fix |
| D9 | Day-14 trigger = launchd(macOS)单次 user agent,**非 cron**(launchd 是 macOS native;cron 在新 macOS 上需要 Full Disk Access 妥协) | PRD §"Real-world constraints" C4 macOS 限定 + 工程级判断 |
| D10 | 误报处理 = mark, don't delete(`[disputed]` tag 标记 + 计数,不删除 → 保留 adoption signal) | PRD §"UX principles" + L3 OQ-10 决议 |
| D11 | UX:Agent 是 witness 不是 judge — entry 写"我观察到 X · 我推测 Y · 置信 L\|M\|H";不替 operator 解释情绪 / 下结论 | PRD §"UX principles" + L2 §6 cond-2 |
| D12 | 唯一 config 文件 = `~/.config/friction-tap/state.json`,human-readable,字段最小 | PRD §"Scope IN" #7 + C12 推论 |
| D13 | confidence 字段值域 = `{H, M, L}`,由静态规则决定(见 architecture §5.2) | PRD §"Scope IN" #4 + L2 §6 cond-2 |
| D14 | hybrid 增量 = day-14 trust mini-summary 末尾追加 `**Self-interview**: After 2 weeks, do you feel relieved / watched / both? (1 句话)` 一行 prompt;无 form / 无 6 题协议 | PRD §"Core user stories" #5 + FORK-ORIGIN.md "hybrid 增量" 节 |
| D15 | 默认 off / opt-in:state.json 初始 `enabled: false`,operator 主动 `friction --on` 才生效 — 避免非 dogfood 模式 log 膨胀 | C13 + L2 §5 末段 |
| D16 | **(R1 B1 fix)Confidence 分类与 threshold 解耦**:confidence H/M/L 由 event features 决定(详见 architecture §5.2 重写决策表 — 基于 tool kind + duration_ms 缺失 / stderr 强信号 / Claude Code block flag);threshold 仅作为 minimum-confidence filter — `threshold=high` 仅 emit confidence ≥ H,`threshold=medium` 仅 emit ≥ M,`threshold=low` 全 emit。**TECH-2 误报洪水 mitigation 由此恢复有效:`--threshold high` 真正过滤掉 M/L event,而非 relabel** | R1 B1 fix · architecture §5.2 |
| D17 | **(R1 H2 + R2 B-R2-3 fix)Review-mode 是独立 state,与 enabled 正交**:`friction --review-mode` / `--review-mode-on` 设 `state.review_mode = true`(**不动 `state.enabled`**);`--review-mode-off` 退出 review。**hook gate 行为**:fire only if `state.enabled == true AND state.review_mode == false`(review 期间 hook 静默暂停,但 enabled 仍为 true)。**O3 verification 仍仅看 `state.enabled`,不看 review_mode** — 见 D20。这是 R2 B-R2-3 fix 的核心:R1 H2 原方案(review_mode = --off alias)与 O3 严格 binary 冲突 — 一个 review session 期间正确流程会让 enabled=false,继而触发 trust_summary `--check-enabled` 的 false fail。新方案让 review_mode 与 enabled 正交,review session 不影响 adoption verdict | R1 H2 + R2 B-R2-3 fix · C14 实现 |
| D20 | **(R2 B-R2-3 fix)O3 与 review_mode 正交**:O3 measures `state.enabled` only — `review_mode` 是 orthogonal informational status,**不影响 O3 verdict**。即:operator 进 review session(review_mode=true)期间跑 day-14 trust_summary,只要 `state.enabled=true` 即 O3 PASS;hook 在 review 期间静默暂停是 review_mode 与 enabled 的合成行为,不是 adoption signal 损坏。**rationale**:R1 H2 原方案让 review session 把 enabled 强制设 false,与 O3 严格 binary(R1 B3)不兼容 — 一个 14 天内合规 review session 的 operator 反而会因为正确流程产生 false adoption fail。本决议把 review_mode 拆出独立 state field 解决这个 state-machine 冲突 | R2 B-R2-3 fix |
| D18 | **(R1 H3 fix)Schema-error 可见**:hook 内部所有 payload schema drift / parse 异常都计数到 `state.json` 中 `schema_error_count` 字段(累加 monotone counter),并在 trust-summary 输出 `## Schema health` 段显示该计数;hook 主流程仍 silently exit 0(TECH-4)— **fail-soft + visible** | R1 H3 fix |
| D19 | **(R1 medium SEC-2 fix)stderr 极简 secret redact**:hook entry 写入前对 stderr(已截断 200 chars)做一轮 regex match,匹配 `(sk|pk|ghp|github_pat|aws|AKIA)_[A-Za-z0-9]{16,}` / `Bearer [A-Za-z0-9_-]{20,}` 等常见 token shape → 替换为 `[redacted]`。**纯 regex,无外部依赖,失败兜底原样** | R1 medium SEC-2 |
| D21 | **(R3/R4 H-R3-1 fix)`friction --on` 是"完整恢复"语义**:`friction --on` 同时 `set_enabled(true)` AND `set_review_mode(false)`,确保不会出现 enabled=true / review_mode=true 卡死 → hook 静默暂停 + O3 PASS 的 false adoption signal 状态(R3 reviewer H-R3-1)。stdout 行为:若入参前 review_mode 为 true → 打印 `enabled · review_mode cleared`(显式告知);若入参前 review_mode 已是 false → 仅打印 `enabled`(避免重复)。**`--review-mode-off` 仅退出 review,不动 enabled**(部分恢复);**`--on` = 完整恢复**(都恢复)。README 教学加这条区分(T032 / Daily commands 段) | R3/R4 H-R3-1 fix · 防 review_mode stuck-true |

## 5. Task Breakdown(phases only;task-decomposer 详化)

> 仅 phase + 高层 task block。具体 T001/T002... 在 `tasks/` 子目录。**R1 H6 fix:**移除 ghost T022 引用 — OQ-C 双指标实现合并到 T020 trust_summary,T013 grep helper 直接提供 `has_recent_agent_emit()` API。**所有 13 个 task ID 现在与 dependency-graph.mmd / tasks/ 目录完全一致**。

- **Phase 0 · Foundation**(T001–T003):仓库结构 + Python project skeleton + state.json schema + repo-root 探测 helper
  - T001:repo-root + log-path 探测 helper(含 OQ-D 错误路径)
  - T002:state.json 读写 + 初始默认值(`enabled: false`,`threshold: medium`,`schema_error_count: 0` D18)
  - T003:entry 格式化 + 原子 append + secret-pattern redact(D19)

- **Phase 1 · Core**(T010–T013):hook + 静态规则 + CLI 主体 + grep helper
  - T010:静态规则判定(白名单 + 黑名单 + **D16 解耦的 confidence 分类 + threshold filter**)
  - T011:`PostToolUseFailure` hook 脚本(读 stdin JSON,过规则,写 entry,**D18 schema-error 计数**)
  - T012:`friction <msg>` CLI(operator-fallback)+ `--on/--off/--threshold/--review-mode/--review-mode-off/-f`(D17 / D20:**`--review-mode` 设独立 `state.review_mode=true`,与 `state.enabled` 正交,O3 不受影响** — R3/R4 B-R3-1 修订:不再标"alias",是独立 state field)
  - T013:grep.py helper(读 friction-log,tag 比例,24h 窗口 fresh-entry)+ **CLI 入口 `python -m friction_tap.grep --count-agent-emit --since=14d`(R1 B2:O1 verification 物理实装)**

- **Phase 2 · Day-14 trust mini-summary**(T020–T021):
  - T020:trust-summary 脚本 — 模板渲染 + self-interview prompt(D14 + R1 H1 结构化)+ Schema health 段(D18)+ **`--check-enabled` flag 提供 health-check 等价物**(R1 B2:替代不存在的 `friction_tap.tools.health_check`,纯 state.json 检查 + 最近 24h activity informational metric)+ OQ-C 实装(D7)
  - T021:launchd plist + 安装脚本(D9)

- **Phase 3 · Polish + ship**(T030–T033):
  - T030:单元测试(paths / state / format / judge / grep 5 模块,共 ≥ 30 case 含 D8 修订网格 12 case + Read 反向 4 case + D16 confidence-feature 8 case + R1 B1 关键 threshold-filter 1 case + D19 redact 6 case + state schema_error_count 6 case)
  - T031:集成测试(entry 写入 / 并发 append / OQ-D fail-loud / **stale-save tag 误绑 H2 场景** / trust_summary 完整渲染 / **install.sh 后跑一次 real-payload smoke test H3**)
  - T032:README + 安装说明 + privacy promise + off-switch + **review-mode 教学 H2** + .gitignore 推荐
  - T033:Claude Code hooks 注册文档 + install.sh + dogfood 起点 + **post-install schema-validation smoke test H3**

**任务 ID 一致性已校验**:tasks/ 目录下 **共 13 个文件**(T001/002/003/010/011/012/013/020/021/030/031/032/033),**dependency-graph.mmd 13 个节点**,**spec §5 13 个引用**,无 ghost,无 missing。

### Schedule risk(R1 H6 sum 重算 · R2 propagation revisit)

| Task | Hours(R1 revised) | R2 增量 | Hours(R2 revised) |
|---|---|---|---|
| T001 | 1.0 | — | 1.0 |
| T002 | 1.0 | **+0.25**(R2 B-R2-3 review_mode 字段 + set_review_mode helper) | **1.25** |
| T003 | 1.75(+ D19 redact regex) | — | 1.75 |
| T010 | 2.0(+ D16 重写 confidence-feature 决策表 + 边界测试) | — | 2.0 |
| T011 | 1.75(+ D18 schema-error counter) | 0(逻辑替换非增量:R2 H-R2-3 显式空 stdin pre-read + R2 B-R2-3 review_mode hook gate 都是单 if,在 1.75h 内可吸收) | 1.75 |
| T012 | 2.0(+ D17 review-mode 独立 state field thin wrapper · 不增 · R3/R4 B-R3-1 措辞修订:不再标 alias) | 0(R2 B-R2-3 改 review-mode 调 set_review_mode + 加 --review-mode-off flag,thin wrapper 在 2.0h 内可吸收) | 2.0 |
| T013 | 1.75(+ count-agent-emit CLI 入口 R1 B2) | — | 1.75 |
| T020 | 2.25(+ R1 H1 结构化 prompt 模板 + R1 B2 --check-enabled flag + D18 schema-health 段) | — | 2.25 |
| T021 | 1.5 | — | 1.5 |
| T030 | 2.0(+ D8/D16/D19 网格扩充) | — | 2.0 |
| T031 | 2.5(+ stale-save tag 误绑 + smoke test H2/H3) | 0(R2 B-R2-3 加 TestO3PassesDuringReviewMode 1 case + R2 H-R2-3 加空 stdin smoke 在原 2.5h 内可吸收) | 2.5 |
| T032 | 1.75(+ review-mode 教学 + schema-error 出现时的 README troubleshooting) | — | 1.75 |
| T033 | 1.25(+ post-install smoke test H3) | — | 1.25 |
| **Total** | **22.5h** | **+0.25h** | **22.75h** |

**R2 sum 22.75h 对 PRD v1.1 C1 13.6% overshoot**(C1 上限 = 23h;22.75 / 23 = 0.989,在 PRD v1.1 修订后预算内)。R1 sum 22.5h vs C1 旧 20h 上限是 12.5% overshoot;R2 fix 让 sum 走到 22.75h,**仍在 PRD v1.1 12-23h 区间内**(余量 0.25h),不再超 C1 上限。

**结论(R2 修订后 schedule risk)**:
- R2 修订后 task hours 合计 = **22.75h**,**仍在 PRD v1.1 C1(12-23h,2026-05-08 sign-off)预算内**(余量 0.25h);R1 sum 22.5h 超过 PRD v1.0 C1 20h 12.5% overshoot 已经被 PRD v1.1 sign-off 接受
- 路径选择:**operator 已选(PRD v1.1 sign-off 路径 (a))**:接受 22.75h 工程量,实际 dogfood ship 时间在 2 周内(@10 hr/week 上限可在 2.275 周完成)
  - 备选 (b)在未来 review 后再 cut scope:T031 smoke test 合并到 T033(-0.5h)/ T030 D19 redact 测试 cut 至 3 case(-0.25h),回到 ~22.0h;**当前不必启用 (b)**,因为 R2 sum 仍在预算内
- **本 R3 包提交方案**:维持 (a) 路径(R1 sign-off 已通过);若 R3 review 再加 finding 引入额外 hours 把 sum 推到 > 23h,operator 必须二选:cut R3 提案中较低优先级项 OR 把该项推 v0.2
- **R3/R4 narrow drift fix(本轮)**:B-R3-1 / H-R3-1 / H-R3-2 / Partial-1 / 4 medium 共 8 项 — 都是 thin wrapper / state field / template segment / 措辞修订,在原 task estimate 内可吸收(state field add ~0.05h * 1 = trivial / template segment ~0.1h * 2 = trivial / verification add ~0.15h * 2 = trivial),sum 仍 22.75h 不变。R4 是 hard cap 最后一轮,无 R5 风险
- **Critical path 重新计算(R2 修订)**:`T001 → T002 → T003 → T010 → T011 → T031`(6 个节点,串行 wall time ≈ 11.25h:1.0+1.25+1.75+2.0+1.75+2.5 = 10.25h,加 review/调试 buffer ≈ 11.25h);**剩余 ~11.5h 在并行分支(T012/T013/T020/T021 + T030/T032/T033)中**;若 operator 单线程跑,wall time ≈ 22.75h ÷ 5 hr/week ≈ 4.55 周 / @10 hr/week 2.275 周;选 (a) 路径接受 2 周 ship + 实际 dogfood 起点延迟 0.5 周(operator 已 sign-off PRD v1.1)

## 6. Verification Criteria

> 每条 outcome 必须有可执行 / 可测量的"完成定义"。覆盖 O1–O6,且对 PRD biggest product risk(file too trustworthy weakly opened)+ secondary risk(误报)有 explicit 验证。

| Outcome | Verification(R1 B2 fix:全部用已实装 entry point) |
|---|---|
| O1 · Capture 工作 | 第 14 天运行 `python -m friction_tap.grep --count-agent-emit --since=14d` 返回 ≥ 8(T013 提供 CLI 入口 — R1 B2 fix) |
| O2 · Trust 在线 | 第 14 天运行 `python -m friction_tap.trust_summary`,生成 `docs/dogfood/v4-trust-w2.md`;脚本 stdout 显示 `acked_ratio: <X>` 与 `disputed_ratio: <Y>`,**且当 X < 0.50 OR Y > 0.20 时 exit code != 0**(O2 violation 信号),operator 在 trust-w2.md `## Outcome check` 段也可见 pass/fail |
| O3 · Adoption signal(单指标 binary,严格遵循 PRD L78) | 第 14 天运行 `python -m friction_tap.trust_summary --check-enabled`(T020 提供 health 等价物 — R1 B2 fix);**仅检查 `~/.config/friction-tap/state.json` 字段 `enabled: true`** → adoption signal pass。**`state.review_mode` 与 O3 正交,不进 verdict**(R2 B-R2-3 / D20 fix:review session 期间 enabled 仍为 true,O3 仍 PASS;hook 在 review 期间静默暂停是 review_mode 与 enabled 的合成行为)。**activity freshness(最近 24h 是否有 agent-emit entry)单列在 trust-w2.md `## Activity health` 段作为 informational metric,不进 O3 verdict**(R1 B3 fix · BUS-1 / OPS-2 不再因 operator 暂离产生 false fail) |
| O4 · Review 体验 | operator 用 stopwatch 自测:打开 friction-log + 读完 20 条 + 在每条下方追加 tag(混合 acked/disputed)总计 ≤ 10 min。grep-friendly 单行格式可加速 |
| O5 · 主观确认 | operator 在 day-14 trust 报告下方手写 list ≥ 3 条 named entry(by ISO timestamp / 一句体感),作为附录 plain text。脚本不验证内容,只验证段存在 |
| O6 · Hybrid · adoption-decision answered(R1 H1 结构化) | 第 14 天打开 `docs/dogfood/v4-trust-w2.md`,自动检查 = (a) `grep "\[label:" docs/dogfood/v4-trust-w2.md` 命中三选一 `relieved\|watched\|both` 之一 — exit 0 表 pass;(b) reason 段(label 行后的自由文本段)CJK 字符长度 ≥ 20 OR English word count ≥ 8(`python -m friction_tap.trust_summary --check-self-interview` 实装该校验,T020 提供) |
| Risk · biggest product risk("file weakly opened") | O3(state enabled)+ O6(self-interview 结构化答完)同时通过 = 14 天内 operator 至少打开过 friction-log 一次,且 hook 仍 enabled。若 O6 空或不结构化 → 触发 secondary risk doc 并由 operator review |
| Risk · secondary("误报洪水")| trust-summary 输出 `disputed_ratio > 0.20` 或 operator 在 day 14 之前已经 `friction --off` → 视为 fail,需在 mini-summary 中显式记录 |
| Tech · 静态规则正确性(D8 修订 + D16 confidence-feature) | 单元测试覆盖 D8 修订白名单 **3 个 tool**(Bash / Edit / Write) × {成功 / 失败} × {黑名单关键字 命中 / 不命中} 共 12 case,**全部 green;同时覆盖 Read tool 失败必 skip 的反向断言 4 case**(防 D8 H4 回归);**D16 confidence-feature 决策表 8 case**(每种 confidence 边界 input 各 ≥ 1 个) |
| Tech · threshold 真过滤(R1 B1 verification — 关键) | 单元测试 `test_judge_threshold_actually_filters`:同一批 fixture event(含 H/M/L 各 ≥ 1 条),**`threshold=high` 时只有 H 触发 `("emit", "H")`,M/L 必返回 `("skip", None)`;`threshold=medium` 只有 H/M emit,L skip;`threshold=low` 全 emit**。**任一断言失败 = TECH-2 mitigation 失效 = 阻塞 ship**(R1 B1 fix) |
| Tech · 原子写 | 集成测试模拟 50 次并发 append,断言 friction-log 行数恰好为 50 且无错位(architecture §5.3) |
| Tech · OQ-D fail-loud | 集成测试在 `/tmp` 仓外目录运行 `friction "test"`,断言 exit code != 0 且 stderr 含 "specify -f" |
| Tech · stale-save tag 误绑(R1 H2 + R2 B-R2-3 fix) | 集成测试模拟"operator 打开 friction-log 编辑 → hook 后台 append 新 entry → operator 保存覆盖"场景,断言 (a)README 警告已在 README;(b)`friction --review-mode` 设 `state.review_mode=true`(**不改** `state.enabled`)→ hook gate 短路(enabled=true AND NOT review_mode),实际行为是 silently skip;(c)`friction --review-mode-off` 退出 review_mode,hook 恢复 fire;(d)集成测试 `TestO3PassesDuringReviewMode`:review_mode=true 期间跑 `python -m friction_tap.trust_summary --check-enabled` → exit 0(O3 PASS,不受 review_mode 影响 — D20) |
| Tech · schema-drift visible(R1 H3 fix) | (a) install.sh 后跑一次 real-payload smoke test(用 fixture JSON 验证 hook 写入成功);(b) 单元测试 `test_schema_error_counter_increments`:故意传 missing-field payload → state.json `schema_error_count` 累加 +1 → trust-summary 输出 `## Schema health · schema_error_count: <N>` |
| Tech · stderr secret redact(R1 medium SEC-2 fix) | 单元测试 `test_redact_token_shapes`:6 case 含 `sk-...` / `Bearer ey...` / `AKIA...` / `ghp_...` / `github_pat_...` / `pk-...` 的 stderr → 写入后 entry 中 token 部分替换为 `[redacted]`,其他文本保留 |
| Tech · `--on` 完整恢复语义(R3/R4 H-R3-1 fix · D21) | 集成测试 `TestOnClearsReviewMode`:(a)`update(enabled=False)` + `set_review_mode(True)` 后跑 `friction --on` → state.json `enabled=true` AND `review_mode=false`(双字段都恢复);(b)stdout 含 `review_mode cleared`(显式告知);(c)`update(enabled=False)` + `set_review_mode(False)` 后跑 `friction --on` → stdout 仅 `enabled`(无重复 cleared 噪音);(d)反向断言:`--review-mode-off` 仅清 review_mode,不动 enabled(已被 T031 TestStaleSaveTagRebinding 覆盖) |
| Tech · trust_summary 显示 review_mode 状态(R3/R4 H-R3-2 fix) | 集成测试 `TestTrustSummaryShowsReviewMode`:(a)`update(enabled=True)` + `set_review_mode(True)` 后跑 `python -m friction_tap.trust_summary` → trust-w2.md 含 `## Hook Operational Status` 段,显示 `state.review_mode = true`;(b)再加 stale 时间戳让 last `--review-mode` 设置 > 24h(monkeypatch state.installed_at / 加 `review_mode_set_at` field 或读 file mtime as proxy)→ trust-w2.md 该段含 WARNING 文案 `review_mode has been on for >24h; hook is paused`;(c)O3 verdict 段独立 — review_mode=true 时仍 `o3_verdict: pass`(D20 正交不破)|

## Glossary

| Term | 在本项目的权威含义 |
|---|---|
| friction | 由静态规则识别的"协作摩擦时刻"(tool 失败 / hook block / operator 主观体感 via CLI);不含一般错误日志;不含 successful 操作 |
| entry | friction-log 中的单行记录,符合 IN-4 格式 |
| `[agent-emit]` | 由 hook 写的 entry(自动) |
| `[operator-cli]` | 由 `friction <msg>` 命令写的 entry(主观) |
| confidence | agent 自评判定可信度,值域 `{H, M, L}`;**由 event features 决定(D16);见 architecture §5.2 重写决策表** |
| threshold(R1 B1 修订) | minimum-confidence filter — `--threshold X` 仅 emit confidence ≥ X 的 event,**不再是 relabel** |
| adjudication tag | operator 在 entry 行下方追加的一行 `[acked]` / `[disputed]` / `[needs-context]`,可带自由文本;无 state machine |
| review mode(D17 / D20 · R2 B-R2-3) | `state.review_mode` 是与 `state.enabled` 正交的独立 bool 字段。`friction --review-mode` / `--review-mode-on` 设 review_mode=true(**不动 enabled**);`--review-mode-off` 退出。hook gate 行为 = `state.enabled AND NOT state.review_mode` — review 期间 hook 静默暂停,但 **`state.enabled` 仍 true** → **O3 不受影响**(D20)。这是 R1 H2 review-mode-as-off-alias 的修正 — 原方案与 O3 严格 binary 冲突 |
| hook still enabled(O3 — 严格 binary) | **R1 B3 + R2 B-R2-3 修订:仅 state.json `enabled: true`**;**`review_mode` 与 O3 正交**(D20);activity freshness 单列 informational(不进 O3) |
| witness | agent 的角色定位 — 提名摩擦、不下结论、不解释情绪(D11) |
| dogfood mode | operator 显式 `friction --on` 后的状态,hook 才主动 emit;非 dogfood mode 默认 off(D15) |
| schema_error_count(D18 / R1 H3) | state.json 中累加 monotone counter,记录 hook 内部 payload schema drift / parse 异常次数;trust-summary 输出可见 |
| activity freshness(R1 B3) | 信息性 metric:friction-log 最近 24h 是否有 ≥ 1 条 `[agent-emit]` entry;trust-summary `## Activity health` 段显示;**不进 O3 verdict** |
| self-interview(D14 + R1 H1) | day-14 trust-w2.md 末尾固定 prompt;**结构化答案要求**:`[label: relieved\|watched\|both]` + reason ≥ 20 CJK chars OR ≥ 8 English words |

## Open Questions for Operator

> PRD §"Open questions" 已通过 D6 / D7 / D8 解决。下面只列 spec 阶段新发现的工程级歧义,每条都阻塞特定 task。**当前为空**。

(none — PRD 的 OQ-C / OQ-D / OQ-E 全部在 §4 Prior Decisions 中决议)

附:**verified no GDPR/CCPA/PDPA/PCI/HIPAA/COPPA compliance triggers for v0.1** — 见 `compliance.md`。
