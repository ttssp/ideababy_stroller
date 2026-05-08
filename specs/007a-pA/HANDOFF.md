# Hand-off · 007a-pA → autodev_pipe

**Handed off at**: 2026-05-08T12:43:06Z
**Revised**: 2026-05-08T14:30:00Z(R2 propagation fix · B-R2-1 PRD v1.1 C1 12-23h + B-R2-3 review-mode 与 enabled 正交)
**IDS spec path**: /Users/admin/codes/ideababy_stroller/specs/007a-pA
**PRD source**: /Users/admin/codes/ideababy_stroller/discussion/007/007a-agent-emit/007a-pA/PRD.md(**v1.1 · 2026-05-08 sign-off**)
**ADP repo path** (operator 自填,默认 `/Users/admin/codes/autodev_pipe`): /Users/admin/codes/autodev_pipe
**SHARED-CONTRACT version honored**: 1.1.0

## Operator manual steps(切仓后)

1. cd /Users/admin/codes/autodev_pipe
2. 阅读 IDS PRD 与 IDS spec:
   - `cat /Users/admin/codes/ideababy_stroller/discussion/007/007a-agent-emit/007a-pA/PRD.md`
   - `cat /Users/admin/codes/ideababy_stroller/specs/007a-pA/spec.md`
3. 在 ADP 起新 feature(真实入口 = skill,不是 Makefile target):
   - 在 ADP Claude Code session 里,触发 `.claude/skills/sdd-workflow/SKILL.md`
   - **operator 必须人工转写**:把下面**结构化 mini-PRD handoff block 直接复制粘贴**到 sdd-workflow input(R1 H5 fix:不再用 1-2 段短描述,因 schema drop 太重 — 之前 ADP 端必须重建 O1-O6 / 全部 Constraints / UX principles / Biggest risk / Verification,极易丢)。

> **========== Mini-PRD Handoff Block(直接复制到 sdd-workflow input) ==========**
>
> **Problem / Context**:
> forge 006 路径 2 playbook 在 W2 step 4 明确要求"每次 V4 retrospective skill 跑得不顺畅就 jot 一笔到 friction-log",但当前 operator 必须经 5 步动作记一条 friction(切目录 / 找文件 / 算 ISO 时间戳 / append / 保存),且 90 秒打断"我正在调试这个具体 task"的心流。结果 90% 真实 friction 在当下被跳过,4 周后 retrospective 没有素材可复盘。
>
> 主语反转 substrate:把 friction-log 的写入者从 operator 反转为 Claude session 自身,operator 只做审阅 + 反驳 + 拥有最终叙事权。
>
> **User persona**:Yashu Liu — IDS 单 operator,跑 V4 dogfood,同时推进 forge 006 路径 2 + 其他 forge 事务;每周 5-10 hr 是 friction-tap 这条 fork 的所有可用时间;非软件开发背景,但 IDS 这工具链的最高频用户。三种角色由同一个人不同时间扮演:做事的人 / 审阅者 / day-14 adoption-decision 者。
>
> **Outcomes(O1-O6 — full numbered list,**严格遵循 IDS spec §1 R1 review-fixed 版本**)**:
> - **O1 · Capture**:第 14 天 friction-log 累计 ≥ 8 条 `[agent-emit]` entry
> - **O2 · Trust**:第 14 天 trust mini-summary 显示 acked ≥ 50% AND disputed ≤ 20%
> - **O3 · Adoption**(R1 B3 修订严格 binary):第 14 天 hook 仍 enabled(state.json `enabled: true`);**activity freshness 单列 informational,不进 O3**
> - **O4 · Review**:operator 能 ≤ 10 min 审阅 20 条 entry
> - **O5 · 主观**:operator 能 named ≥ 3 条改善 retrospective recall 的 entry
> - **O6 · Hybrid**(R1 H1 结构化):day-14 self-interview 答案含 `[label: relieved\|watched\|both]` + Reason 一句话 ≥ 20 CJK chars OR ≥ 8 English words
>
> **Scope IN(v0.1)**:
> 1. PostToolUseFailure hook(Python stdlib only)
> 2. 静态规则白名单 = {Bash, Edit, Write}(R1 H4 修订:Read 移出 v0.1)+ Claude Code lifecycle hook block 信号
> 3. 黑名单 = `--off` state + task_description 含 `[debugging-friction-detection]`
> 4. friction-log 硬编码路径 `<repo-root>/docs/dogfood/v4-friction-log.md`
> 5. Entry 格式 `<ISO> [agent-emit] [confidence:H|M|L] [private-to-operator] · <tool> exit <code> · "<stderr-200chars-redacted>" · task: <desc>`(secret-pattern redact · D19)
> 6. Adjudication tag(markdown 一行追加 `[acked|disputed|needs-context]`)无 state machine
> 7. `friction <msg>` CLI(operator subjective entry)
> 8. `friction --on / --off / --threshold {low,medium,high} / --review-mode / --review-mode-off / -f`(**R2 B-R2-3 修订:`--review-mode` 设 `state.review_mode=true`,与 `state.enabled` 正交;`--review-mode-off` 退出 review;O3 仅看 enabled 不看 review_mode · D17/D20**)
> 9. Day-14 trust mini-summary(grep + 模板,launchd 触发)+ 结构化 self-interview prompt
> 10. 测试 + commit + 文档
>
> **Scope OUT(non-goals)**:state machine for adjudication / Skill placeholder 检测 / LLM-judge / 跨仓 ship / 可配 log 路径 / Frontend dashboard / 团队共享 / 自动开 issue PR / 完整 2 周 pilot 协议 / 完整 weekly review ritual / 跨 dogfood 周期聚合 / Read tool failure 进 v0.1 白名单(R1 H4 留 v0.2)/ -f path 持久化(R1 留 v0.2)/ friction --reset-state(R1 留 v0.2)
>
> **Constraints C1-C14(数字化,**严格遵循 IDS spec §3 R2 review-fixed 版本**)**:
> - C1: 总预算 **12-23h**(PRD v1.1 sign-off 2026-05-08 · operator 显式接受 R1 修订项后 22.5h 工程量 → 12.5% overshoot;R2 B-R2-1 fix:本行从原 10-20h 修订为 PRD v1.1 实际值),1-2 周 ship(2 周 wall time @ 10 hr/week 上限)
> - C2: single-operator dogfood,无 multi-reader
> - C3: free OSS / self-hosted,无 SaaS / 付费
> - C4: macOS · Claude Code PostToolUseFailure hook + Python CLI
> - C5: 4 红线(RL-1 不接全知监控 / RL-2 不接追责文化 / RL-3 不接合作上传 / RL-4 不与 enterprise observability 竞争)
> - C6: v0.1 必含 4 condition(cond-1 审阅入口 / cond-2 entry tone 含 uncertainty / cond-3 week-2 trust monitoring / cond-4 default single-operator + private)
> - C7: Event scope 仅 PostToolUseFailure
> - C8: Ship target IDS first,4 周等待期不动 ADP
> - C9: friction-tap 不能拼动 operator 太多时间
> - C10: Privacy as visible promise
> - C11: Precision > recall
> - C12: stdlib only,无 venv,无第三方包
> - C13: 默认 off / opt-in
> - **C14**(R1 H2 + R2 B-R2-3):review session 必先 `friction --review-mode`(设 `state.review_mode=true`,**与 enabled 正交,O3 不受影响 · D17/D20**),编辑完跑 `friction --review-mode-off` 退出;否则编辑器 stale snapshot 写回会丢 hook 期间的新 entry + tag 物理位置错位
>
> **UX principles(tradeoff stances)**:
> - Trust calibration > Speed to ship — entry tone 必须含 confidence(L/M/H),不假装权威
> - Differentiation > Broad appeal — 不跟 enterprise observability 比;default single-operator + default private 是 product promise 一部分
> - Trust monitoring on day 14 — self-interview 1 题 hedge 是必须 deliverable
> - Speed to ship — 1-2 周必须 ship,但前 3 项不让步
> - Simplicity > Cleverness — markdown tag 优于 state machine
> - Fast off-switch > Sophisticated tuning — `friction --off` 一行止血
> - Agent 是 witness 不是 judge — 提名摩擦,不下结论
> - Mark, don't delete — 误报用 `[disputed]` 标记不删
>
> **Biggest product risk · "file too trustworthy, weakly opened"**:
> 即使 entry 格式做对、标记体系 fair、hook 工作正常,如果 operator 4 周后实际不主动打开 friction-log,产品价值就死在文件里。这是 substrate-only scope 的固有风险。
> Mitigation:(1) day-14 trust mini-summary 是 operator 必看产物;(2) Hybrid 增量(self-interview 1 题)强制 operator day 14 至少打开一次文件;(3) day-28 / day-42 trust report 留 v0.2。
> Secondary risk:静态规则误报率超容忍。Mitigation: `--threshold high` 真过滤(R1 B1 修订)+ `[disputed]` 标记保留信号 + day 14 self-interview 强制直面这个数字。
>
> **Verification(O1-O6 → 可执行命令,严格遵循 IDS spec §6 R1 review-fixed 版本)**:
> - O1: `python -m friction_tap.grep --count-agent-emit --since=14d` ≥ 8(R1 B2:T013 提供 CLI)
> - O2: `python -m friction_tap.trust_summary` 非零 exit code 表 violation
> - O3: `python -m friction_tap.trust_summary --check-enabled` exit 0/1(R1 B2 + B3:严格 binary)
> - O4: operator stopwatch 自测 ≤ 10 min
> - O5: trust 报告下方手写 ≥ 3 条 named entry
> - O6: `python -m friction_tap.trust_summary --check-self-interview` exit 0(R1 B2 + H1:结构化 label + reason ≥ 字数阈值)
>
> **========== Mini-PRD Handoff Block END ==========**

4. sdd-workflow 产出 `specs/<feature>/spec.md`(7 元素骨架,schema_version: 0.2,reviewed-by: pending)后,operator 按下表强制项填入(**R1 H5 fix:加 Problem/Context、UX principles、Biggest risk 三行**):

| IDS 来源 | ADP spec 节 | 强制? |
|---|---|---|
| IDS PRD frontmatter | spec.md frontmatter (`spec_id` / `status: draft` / `schema_version: 0.2` / `reviewed-by: pending`) | 强制 |
| **IDS PRD §"Problem / Context"(R1 H5 新增)** | **spec.md §"Background" 或 §0(取决 ADP template)** | **强制(R1 H5 fix)** |
| IDS PRD §"User persona" + §"Core user stories" | §1 Outcomes(O1, O2, ...; 本 PRD 共 6 条 outcomes O1-O6 R1 修订版本) | 强制 |
| IDS PRD §"Scope IN (v0.1)" 表 | §2.1 Scope IN(本 PRD 共 10 行 component table · R1 修订:Read 移出 + redact 入) | 强制 |
| IDS PRD §"Scope OUT (explicit non-goals)" | §2.2 Scope OUT(本 PRD 11 项 + R1 加 3 项 + 见 IDS specs/007a-pA/non-goals.md 26+ 条扩展) | 强制 |
| IDS PRD §"Real-world constraints" 表 | §3 Constraints(**C1-C14**,数字化 · R1 H2 加 C14) | 强制 |
| **IDS PRD §"UX principles"(R1 H5 新增)** | **§3 Constraints 内"UX stance" 子节,或单独 §"UX principles"(取决 ADP template)** | **强制(R1 H5 fix)** |
| IDS spec §"Prior Decisions"(specs/007a-pA/spec.md §4)+ architecture.md §"ADRs" | §4 Prior Decisions(PD1-PD19;**R1 加 D16/D17/D18/D19 共 19 条** + 5 ADR) | 强制 |
| **IDS PRD §"Biggest product risk"(R1 H5 新增)** | **§4 Prior Decisions 末尾"Risk acknowledgement" 子节,或拷到 risks.md 顶部** | **强制(R1 H5 fix)** |
| IDS spec §"Verification" + dependency-graph.mmd 高层 phase | §5 Task Breakdown(高层 phase 0-3 + **13 task ID 引用 R1 修订:确认 T022 ghost 已合并到 T020,无遗漏**) | 强制 |
| IDS PRD §"Success — observable outcomes" + IDS spec §6 Verification | §6 Verification Criteria(每条 V_n 可执行 shell;本 PRD O1-O6 R1 修订版本 + R1 新增工程 verification(threshold 真过滤 / stale-save / schema drift / redact 共 4 条工程级)= 10 条) | 强制 |
| **operator 须补**(IDS 不产出,见 step 4.5) | §7 Production Path Verification | **强制(v3.3 起)** |
| IDS PRD §"Open questions for L4 / Operator" 中**关于 constraint 数字**的(eg "白名单具体 tool 列表") | ADP spec §3 Constraints 末尾 "Open" 小节(C-OQ-1 ...) | 可选 |
| IDS PRD §"Open questions" 中**关于 build 路径选择**的(eg "OQ-D CLI cwd 不在 git repo 怎么办" — 已在 spec.md D6 解决,但若 ADP 转写时 reframe 出新 OQ 时) | 不进 ADP spec,留在本 HANDOFF.md §"Open questions for build phase" | 可选 |

> **本 PRD 的特殊情况**:OQ-C / OQ-D / OQ-E 三条 L3 留下的 Open questions 已在 spec-writer 产出的 spec.md §4 Prior Decisions(D6/D7/D8)中显式 sign-off(operator 在 plan-start 调用文里 pre-decide)。ADP 转写时这些是 PD 而非 Constraint Open;若 ADP 重新 raise 同主题 OQ,走 ADP 自己 spec_validator 反馈循环。

4.5. **operator 在 ADP 写 §7 Production Path Verification**(IDS 不越界产出,ADP 强制):
   - 参考样本:`/Users/admin/codes/autodev_pipe/specs/v3.3/spec.md` §7 真路径 P1-P4 example
   - 模板:`/Users/admin/codes/autodev_pipe/templates/spec.template.md` §7 骨架
   - 最小要求:列至少 1 条 P_i 描述"真路径起点 → 终点 + 必经环节 + 可执行验证命令"
   - 失败模式:不写或只写 mock-pass-prod-fail 的样本 → ADP `scripts/spec_validator.py` reject + status 无法转 frozen
   - 第一性原因:所有 mock-pass-prod-fail 都因为 mock 满足 spec 真路径不满足
   - **本 PRD 建议的 P1**:"agent emit → friction-log 真路径"(Claude Code 真实跑一次失败 tool → PostToolUseFailure hook fire → judge.py 静态规则判 friction → 写 entry 到 hardcoded `docs/dogfood/v4-friction-log.md`,验证用 `tail -1 docs/dogfood/v4-friction-log.md` grep entry 格式)

5. 在 ADP 跑 reviewed-by:
   - frontmatter `reviewed-by: pending` → 触发 ADP `/codex:adversarial-review` 或 plugin 路径
   - review 通过 → frontmatter 改 `reviewed-by: codex`(或 gpt-5.5 / gemini)
   - status: draft → review → frozen
6. 任务分解(ADP 这边的 task-decomposer skill,不复用 IDS task DAG):
   - 在 ADP Claude Code session 触发 `.claude/skills/task-decomposer/SKILL.md`
   - 产出 `specs/<feature>/tasks/T*.md`(9 字段 frontmatter)
   - **不要**直接 cp IDS specs/007a-pA/tasks/T*.md(IDS 13 task 是 IDS 工作流命名,ADP 走 ADP 自己工程 9 字段 schema)
7. parallel-builder 跑 task(走 ADP 5 hard rule + Safety Floor)
8. ship 走 ADP 自己规则(不回 IDS)

## ADP-side prerequisites(operator 切仓前自查)

- ADP 仓库为 v3.2+(含 `.claude/skills/sdd-workflow/` + `.claude/skills/task-decomposer/` skill)
- ADP `make doctor` exit 0
- ADP `pre-commit install` 已跑(spec-validator + check-spec-review + check-constraint-references hooks 装齐)
- **operator 已读 ADP `templates/spec.template.md` §7 + `specs/v3.3/spec.md` §7 真实样本**(为 step 4.5 写 §7 PPV 做准备)
- ADP V4 dogfood 状态(2026-05-08 ±):**第 0 周** — 切仓时机过早会污染 dogfood signal(ADR 0008 D2)。建议**等到 V4 checkpoint-01 出**(2026-06-03 ±)再切仓
- **本 PRD 的特殊建议**:由于 007a-pA 本身是 IDS-first ship(C8),v0.1 不强制跨仓。本 HANDOFF.md 主要价值是**实测 SHARED-CONTRACT v1.1.0 跨仓 hand-off 协议是否在真实 PRD 上跑得通**。operator 可在 V4 checkpoint-01 出之后,把 007a-pA v0.1 的成熟版本作为 ADP V4 dogfood 候选项目接入。

## Schema 转换说明

详见 `framework/SHARED-CONTRACT.md` §3 HANDOFF.md schema(contract_version 1.1.0)。

本 HANDOFF.md 是 SHARED-CONTRACT v1.1.0 的**第一个真实产出**(forge 006 路径 2 的 first end-to-end pilot)。期望:operator 切仓后实测过程会暴露 SHARED-CONTRACT 假设 vs ADP 现实的 drift 点(若有),drift 点的发现是本 PRD pilot 的核心价值之一,会反馈到 SHARED-CONTRACT v1.2.0 修订。

## Open questions for ADP build phase

(IDS PRD 中**关于 build 路径选择**的 OQ 在此承载;ADP build 自然遇到时再解决,不污染 ADP spec frozen)

由 operator 在切仓时手工分流。本 PRD 在 IDS 阶段已经把 OQ-C/D/E 全部决议(spec.md §4 D6/D7/D8),所以**预期 ADP build 阶段无 IDS-side OQ 残留**。若 ADP 重新审视后浮现新 OQ,在此追加。

## Rollback plan

如果 ADP build 失败:
- (a) 回到 IDS 修 PRD,重跑 `/plan-start 007a-pA`(本场景几乎不会触发,因为 IDS 阶段 spec 已成熟)
- (b) 改 ADP spec(不改 IDS PRD),用 ADP 自己的 W-* 修订机制
- (c) 起 forge v2 重新审整个 idea(若多次 ADP build 失败暴露 IDS PRD 根本性问题)

**最可能 rollback 场景**:SHARED-CONTRACT v1.1.0 假设的"sdd-workflow skill 接受 short feature description"在 ADP 现实中需要更结构化的 input,导致 step 3 转写失败。此情况触发 SHARED-CONTRACT v1.2.0 修订,不是 PRD rollback。
