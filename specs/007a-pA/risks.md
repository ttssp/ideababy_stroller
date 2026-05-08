# Risk Register — 007a-pA

**Version**: 0.3
**Created**: 2026-05-08T13:30:00Z
**Revised**: 2026-05-08T14:30:00Z(R2 fix:COMM-2 dual-metric 残留清理 / TECH-1+TECH-3 health_check 替换为已实装 CLI 入口 / SEC-2 D19 false-positive ack / BUS-1 review-mode 与 O3 正交描述对齐 R2 B-R2-3;**R3/R4 narrow drift fix**:PROD-3 health_check → CLI 入口 · Partial-1 / SCH-1 22.5h/20h → 22.75h within PRD v1.1 23h cap · M-R3-1)
**PRD-form**: simple → 单 v0.1 column,无 phased multi-phase
**Source**: PRD §"Biggest product risk" + L2 §6 failure cases + L2 §5 limits + R1/R2/R3/R4 review fix

格式:每行 ID · Category · Risk · L(Likelihood) · I(Impact) · Trigger · Mitigation · Owner · Phase

L/I 取值:`L=Low / M=Medium / H=High`

## Technical

| ID | Risk | L | I | Trigger | Mitigation | Owner | Phase |
|----|------|---|---|---------|------------|-------|-------|
| TECH-1 | hook 漏 fire(false negative)— Claude Code 在某些 tool 失败下未触发 PostToolUseFailure,operator 觉得"明明卡过 5 次没记一条" | M | M | day 3 / day 7 中段 review 发现 entry 数 < 估算 | (a)`friction <msg>` CLI 兜底 subjective(IN-6);(b)README 教学 mid-pilot day-3 跑 `python -m friction_tap.grep --count-agent-emit --since=72h` + `--check-enabled`(R2 M-R2-3 fix:替换不存在的 `health_check` 引用为已实装的 R1 B2 双 CLI 入口);(c)v0.2 候选扩展 hook 范围(C7 暂不) | operator | v0.1 |
| TECH-2 | 静态规则误报洪水(false positive)— 白名单 tool × `exit_code != 0` 命中过宽,合法测试失败也 emit | H | H | `[disputed]` 比例 > 20%(O2 secondary fail);entry 数远超 8 / 14 天上限 | **R1 B1 fix · 重写**:(a)**confidence 分类与 threshold 解耦(D16)** — confidence 由 event features(stderr 强信号 / tool kind / Claude Code block)决定;无强信号的 generic Bash 失败 → L bucket(b)`friction --threshold high` **真过滤**:仅 emit confidence=H,M/L 全 skip(架构 §5.2 Stage C + spec §6 Tech 单元测试 `test_judge_threshold_actually_filters` 强制断言)(c)`friction --off` 一行止血(D10 mark don't delete)(d)`task_description` 含 `[debugging-friction-detection]` 黑名单 skip(e)**Read tool 移出白名单(R1 H4)** 减少 noisy 入口 | operator | v0.1 |
| TECH-3 | operator 忘 `friction --on` → 整 dogfood 周期无 entry(C13 / D15 副作用) | M | H | day 3 `python -m friction_tap.grep --count-agent-emit --since=72h` 返回 0 且 `--check-enabled` 显示 enabled=false(R2 M-R2-3 fix:替换 health_check 引用)| (a)README 安装步骤把 `friction --on` 列为 dogfood 起点仪式;(b)mid-pilot day-3 推荐流程是跑 `--count-agent-emit --since=72h` + `--check-enabled`(R2 M-R2-3:已实装的 R1 B2 双 CLI 入口);(c)installation 后 launchd 安装脚本提示 "执行 friction --on 启动 dogfood" | operator | v0.1 |
| TECH-4 | hook 内部异常未 silently swallow,污染 Claude Code session(`set -e` 传播)| M | H | Claude Code session 异常退出可关联 hook 调用 | hook.py 顶层 try/except 兜所有 Exception;exit 0;细节 log 到 `~/.config/friction-tap/last_run.log` | spec-writer / parallel-builder | v0.1 |
| TECH-5 | `O_APPEND` 在 NFS / 外挂卷上不保证原子 — 若 operator 把 repo 移到 iCloud Drive / SMB | L | M | log 出现错位 / 部分截断;集成测试在 NFS mount 失败 | README 明示"必须在本地 APFS 卷工作";v0.1 不支持 iCloud Drive / SMB(scope OUT) | operator | v0.1 |
| TECH-6 | launchd plist 安装失败(权限 / SIP)致 day-14 trust-summary 不 fire — O3/O6 全断 | M | H | day-14 当天 docs/dogfood/v4-trust-w2.md 不存在 | (a)install_launchd.sh 安装后 `launchctl print` 验证;(b)README 提供 manual fallback `python -m friction_tap.trust_summary` 一行命令;(c)trust_summary 写到 last_run.log 留痕 | operator | v0.1 |
| TECH-7 | git 仓库探测在 git submodule / worktree 边界返回错误 root,致 log 写错路径 | L | M | log 出现在意外路径(eg parent repo)| (a)`git rev-parse --show-toplevel` 是 git 标准 API,边界已被 git 处理好;(b)集成测试在 worktree 场景验证 OQ-D 行为 | spec-writer / parallel-builder | v0.1 |
| TECH-8 | hook 与 CLI 并发 append 同一文件 — `O_APPEND` 单 write 在本地 APFS / ext4 atomic;**不依赖 PIPE_BUF 语义**(R1 medium fix · architecture §5.3 措辞修订);跨平台保证仅在本地 POSIX regular file | L | M | 罕见的 entry 错位 | (a)entry 单行 ≤ 4 KiB conservative engineering bound(非 PIPE_BUF);(b)集成测试模拟 50 次并发 append 验证(spec.md §6);(c)NFS / iCloud Drive / SMB 不支持(README + TECH-5 警告) | spec-writer / parallel-builder | v0.1 |
| TECH-9 | **(R1 H3 新增)Claude Code payload schema drift 静默 noop** — 若 Claude Code 升级修改 hook payload 字段名(如 `tool_name` 改 `toolName`),hook 内部 silently swallow 后**capture 直接归零**,operator 在 day-14 才发现 `total_agent_emit < 8` | M | H | dogfood 第 1-2 周后某天 friction-log 突然不再写入;day-14 trust-summary 显示 `schema_error_count > 0` 累计 | (a)**D18 schema_error_count 计数器**:每次 schema 异常 +1,trust-summary `## Schema health` 段可见(R1 H3);(b)install.sh **post-install real-payload smoke test**(T033):用 fixture JSON pipe hook,断言 entry 写入 → 失败 install 阶段已警告;(c)`~/.config/friction-tap/last_run.log` traceback 留排错入口;(d)hook 仍 silently exit 0(TECH-4 不破) | operator | v0.1 |

## Operational

| ID | Risk | L | I | Trigger | Mitigation | Owner | Phase |
|----|------|---|---|---------|------------|-------|-------|
| OPS-1 | install / uninstall 留下脏 state(plist 残留 / state.json 不清)— 若 v0.2 升级 schema 兼容性破裂 | M | M | v0.2 install 后 state 字段缺失致脚本崩溃 | (a)v0.1 state.json 含 `version: "0.1"` 字段;v0.2 升级时检查 + 迁移;(b)README 提供 `uninstall_launchd.sh` 一键清 | operator | v0.1 |
| OPS-2 | day-14 trigger 时间窗与 forge 006 路径 2 W3 V4 checkpoint-01 节奏不咬合 — operator 太忙跳过看 trust 报告 | M | H | day-14 trust-w2.md 存在但 self-interview prompt 未填(O6 fail) | (a)launchd 触发 09:00 选 operator 历史晨间 review 时段;(b)README 强调 self-interview 1 题仅需结构化答案(D14 hybrid + R1 H1 label + reason ≥ 20 CJK chars);(c)mid-pilot day-3 health check 也提醒 day-14 即将到来;(d)**R1 B3 修订:O3 现严格 binary,operator 暂离不导致 false adoption fail;O6 仍要求 operator 主动写答(forcing function 保留)** | operator | v0.1 |
| OPS-3 | docs/dogfood/v4-friction-log.md 被 operator 误手 git rm / clean → archive 丢失 | L | H | log 文件突然消失;无 entry | (a)README 强调"v0.1 是 archive,不要 git clean / rm";(b)operator 可选定期 cp 到 ~/Documents 备份(README 注明,非脚本强制) | operator | v0.1 |
| OPS-4 | 多个 dogfood 周期(V4 → V5)log 路径冲突 — `v4-friction-log.md` 名字写死 | M | M | V5 dogfood 时 entry 仍 append 到 v4 log 文件(语义错配) | (a)v0.2 加 `--scope=v4|v5` flag 是计划内升级路径;(b)v0.1 README 提示 V4 dogfood 结束时 git rename 文件 | operator | v0.1 |

## Security

| ID | Risk | L | I | Trigger | Mitigation | Owner | Phase |
|----|------|---|---|---------|------------|-------|-------|
| SEC-1 | privacy promise 破裂 — friction-log 误 commit + push 共享 → 违反 C5 RL-3 + C10 | M | H | git diff 显示 `docs/dogfood/v4-friction-log.md` staged + push 到 remote | (a)README 强烈推荐 `.gitignore` 加 `docs/dogfood/v4-friction-log.md` + `docs/dogfood/v4-trust-w2.md`(operator 决定);(b)CLI 安装步骤可选执行 `echo "..." >> .gitignore`;(c)entry 含 `[private-to-operator]` 字段是 visible 提醒不是隐藏假设(C10) | operator | v0.1 |
| SEC-2 | hook payload `stderr` 含 secret(API key / token)被持久化到明文 log | L | M(降级,因 v0.1 已加 minimal redact) | dogfood 期间某 tool 输出 secret 到 stderr,被截断 200 chars 后落地 | **R1 medium fix · v0.1 加 minimal redact**:(a)D19 `format.py` 写入前对 stderr regex 替换 `(sk\|pk\|ghp\|github_pat\|aws\|AKIA)_[A-Za-z0-9]{16,}` / `Bearer [A-Za-z0-9_-]{20,}` 等常见 token shape → `[redacted]`;(b)README 仍警告"redact 是 best-effort,non-standard token shape 可能漏";(c)operator 发现仍可手工编辑文件删该 entry(D5 markdown 直接编辑);(d)v0.2 候选 expand pattern set 与 entropy 检测;**(e)D19 false-positive 显式 acknowledgment(R2 medium fix)**:7 类 token shape regex 可能误杀正常长 identifier(如 GitHub username 或 Base64-like UUID);**trust loss(信号被误 redact)与 privacy gain(secret 不落地)是双向 tradeoff** — v0.1 接受 false positive redaction 作为 privacy 优先的代价,operator 若发现 entry 含意外 `[redacted]` 可手编辑还原(D5 markdown 直接编辑) | operator | v0.1 |
| SEC-3 | state.json 权限过宽(world-readable)— 单 user 系统下风险低,但若多 user 共享机器异常 | L | L | `~/.config/friction-tap/state.json` mode 0644 而非 0600 | install 时 `os.umask` 或显式 `chmod 600`;state.py 写入时主动设置 mode | spec-writer / parallel-builder | v0.1 |
| SEC-4 | hook 注册路径 `.claude/hooks/post_tool_use_failure.sh` 被恶意修改后 sudo 执行 | L | M | 攻击者已能写仓内文件;但 hook 只在 Claude Code session 内 fire,scope 受限 | hook 入口仅 `python -m friction_tap.hook` 一行;主逻辑在 Python module(operator-readable);git diff 可见 | operator | v0.1 |

## Commercial

| ID | Risk | L | I | Trigger | Mitigation | Owner | Phase |
|----|------|---|---|---------|------------|-------|-------|
| COMM-1 | 与 enterprise observability 工具(Langfuse / Helicone / Phoenix / Pydantic Logfire / Datadog LLM)正面冲突 — 违反 C5 RL-4 | L | M | external feedback "你这是迷你 Datadog?"或 v0.2 加 dashboard 倾向 | (a)C5 RL-4 hard;(b)scope OUT 显式列 frontend/dashboard;(c)README §"What this is NOT" 节明示;(d)v0.1 substrate 形态 stdlib only 与 enterprise SaaS 工具的 architecture 完全 orthogonal | operator | v0.1 |
| COMM-2 | quantified-self 弃用 pattern — operator 自己 dogfood 第 2 周关 hook,产品死亡 | M | H | day 14 之前 `friction --off`(O3 fail · binary-only)| (a)**O3 严格 binary 监控(D7 R1 B3 修订)**:仅 state.json `enabled: true` 是 adoption verdict,**移除 R1 之前的双指标设计**(R2 M-R2-2 / B-R2-2 fix);activity freshness 单列 informational 段不进 verdict(D20);(b)precision > recall(C11)+ `[disputed]` mark not delete(D10)+ `--threshold high` 安全网;(c)hybrid self-interview(D14)强制 operator 直面"relieved/watched/both"问题 | operator | v0.1 |

## Compliance / legal

| ID | Risk | L | I | Trigger | Mitigation | Owner | Phase |
|----|------|---|---|---------|------------|-------|-------|
| LEGAL-1 | GDPR / CCPA / PDPA 适用性 — log 含 operator 行为数据 | L | L | external audit 询问 | single-operator self-hosted offline = data subject 与 controller 是同一人;不适用(详见 compliance.md);若 v0.2 ship 给 ADP / 其他 user 需重新评估 | operator | v0.1 |
| LEGAL-2 | OSS license — v0.1 ship 形态(IDS 内部还是 公开 repo) | L | L | operator 决定是否公开 | v0.1 IDS 内部使用,license 由仓库整体决定;若 v0.2 公开 → README 顶部加 license 声明 | operator | v0.1 |

## Personnel — bus-factor

| ID | Risk | L | I | Trigger | Mitigation | Owner | Phase |
|----|------|---|---|---------|------------|-------|-------|
| BUS-1 | Solo operator(Yashu)unavailable > 7 days → friction-tap dogfood 中断;若中断在 day 7 之后,trust mini-summary 仍会 fire(launchd day-14)但无 entry 新增 — verdict 失真 | M | H | operator 长期不在(病假 / 度假 / 紧急事务) | (a)`friction --off` 是 1 行命令,出门前可关(也可用 `--review-mode` · D17 修订;两者都可让 hook 暂停,**但 `--off` 让 enabled=false 才会改变 O3,`--review-mode` 不改 O3** · D20 R2 B-R2-3);(b)若忘关,trust mini-summary `## Activity health` 段(informational,不进 O3)显示"近 24h 无 entry"作为客观证据;**(c)R1 B3 + R2 B-R2-3 fix · O3 现严格 binary**(`enabled=true` 即 pass,`review_mode` 与 O3 正交)— operator 暂离不导致 O3 false fail;activity freshness 是 informational metric,不影响 adoption verdict;(d)operator 回来后 self-interview 答结构化答案即可(R1 H1 label + reason);(e)v0.1 是 substrate,不依赖 operator 持续在场 — log 文件本身保留;**accepted**:这种 risk 在 single-operator 设计下不可消除 | operator | v0.1 |

## Product-level (PRD-derived)

| ID | Risk | L | I | Trigger | Mitigation | Owner | Phase |
|----|------|---|---|---------|------------|-------|-------|
| PROD-1 | **biggest product risk · "file too trustworthy, weakly opened"**(PRD §"Biggest product risk")— substrate-only scope 把 weekly opening cadence 赌给 operator 自律 | M | H | 4 周后回看 retrospective 时 operator 仍未主动打开 friction-log;day-14 verdict 无说服力 | (a)day-14 trust mini-summary 写到 `docs/dogfood/v4-trust-w2.md` IDS 工作流自然路径;(b)hybrid self-interview prompt(D14)强制 operator 在 day 14 至少打开一次文件答 1 句话;(c)v0.2 候选加 day-28 / day-42 trust report cadence(暂不) | operator | v0.1 |
| PROD-2 | "format readable but rarely reviewed" 风险(L2 §6 failure case + PRD secondary)— 即使 hook 工作 + 格式对,operator 实际不打开 friction-log → entry 死在文件里 | M | H | day-14 trust-w2 self-interview 答案空(O6 fail) | 与 PROD-1 共享 mitigation;trust-w2 是 forcing function;若 self-interview 仍空 → 直接触发 v0.2 candidate C(weekly ritual)的考虑 | operator | v0.1 |
| PROD-3 | trust monitoring metric 设计未经 user research 验证(L3 §"Honesty check" #4)— O1 ≥8 / O2 acked ≥50% / O2 disputed ≤20% 的数字是 Opus R1 提的,真实 dogfood 第 1 周可能 disputed 显著高于 20% | M | M | day 7 mid-pilot 发现 disputed 率已 > 20%(尚未 day 14)| (a)README 推荐 day-3 / day-7 mid-pilot 跑 `python -m friction_tap.grep --count-agent-emit --since=72h` + `python -m friction_tap.trust_summary --check-enabled` 双 CLI 入口(R3/R4 Partial-1 fix · 替换原 health_check 引用为已实装 CLI 入口,与 TECH-1 / TECH-3 对齐);(b)`friction --threshold high` 一行收紧;(c)第 14 天若超阈值 → trust-w2 §"Outcome check" 显示 fail,但 self-interview 仍可答 → verdict 不丢 | operator | v0.1 |
| PROD-4 | hybrid 增量(D14 self-interview 1 题)被 operator 当 chore 跳过 — 留 1 行空答 | L | M | day-14 trust-w2 grep 后 prompt 下行为空 | (a)D14 prompt 文案"1 句话"明示极简;(b)若仍空 → O6 fail 在 trust-w2 显示,但 README 提示"操作员可后补",非永久失败 | operator | v0.1 |

## Schedule(R1 H6 fix · 新增分类)

| ID | Risk | L | I | Trigger | Mitigation | Owner | Phase |
|----|------|---|---|---------|------------|-------|-------|
| SCH-1 | **(R1 H6 + R2 B-R2-3 + R3/R4 narrow drift fix)Task hours sum 22.75h 在 PRD v1.1 C1 上限 23h 内** | M | M | spec.md §5 Schedule risk 段已显式记录;PRD v1.1 C1 = 12-23h(operator 2026-05-08 sign-off) | (a)**当前路径**:R2 sum 22.75h / 23h = 0.989 在 PRD v1.1 C1 预算内(余量 0.25h),无需 cut scope;R3/R4 narrow drift fix 不增工时(都是 thin wrapper / state field / template segment 在原 task 内可吸收);(b)备选 cut path(若未来 review 引入额外 hours 把 sum 推到 > 23h):T031 smoke test 合并 T033(-0.5h)+ T030 D19 redact 测试 cut 至 3 case(-0.25h),回到 ~22.0h;(c)R3/R4 是 hard cap 最后一轮,后续无 R5 风险 | operator | v0.1 |

## Summary stats(R1 fix 后)

- 共 **24** 条 risk 条目(9 TECH 含新 TECH-9 + 4 OPS + 4 SEC + 2 COMM + 2 LEGAL + 1 BUS + 4 PROD + 1 SCH 新增)
- 高 likelihood × 高 impact:**1 条 TECH-2 误报洪水(主 mitigation 已 R1 B1 重写为真过滤)** + **1 条 SCH-1 schedule(operator 接受 12.5% overshoot)**
- 中 likelihood × 高 impact:9 条(含新 TECH-9 schema drift)→ mitigation 全部就位
- BUS-1 entry 必含,**already present + R1 B3 调整 O3 binary 后不再产生 false fail**
- **R1 medium follow-up(已修)**:SEC-2(v0.1 redact)/ TECH-8(PIPE_BUF 措辞)/ SCH-1(显式记录 schedule overshoot)
- **R2 修订(已修)**:COMM-2 dual-metric 残留清 / TECH-1+TECH-3 health_check 引用替换为已实装 CLI 入口 / SEC-2 D19 false-positive 双向 trade ack / BUS-1 review-mode 与 O3 正交描述 / SLA.md PIPE_BUF 措辞替换 / spec.md/architecture.md 移除 Read 残留 + 加 D20 review_mode 与 O3 orthogonal 决策
- **R3/R4 narrow drift fix(已修)**:spec.md C14 重写不再"`--review-mode` alias `--off`"(B-R3-1)/ spec.md task summary + Schedule risk 措辞 alias → 独立 state field / 加 D21 `--on` 完整恢复语义(H-R3-1) / spec §6 加 trust_summary 显示 review_mode visibility verification(H-R3-2)/ T012 `--on` 实装 set_review_mode(False)+ stdout `review_mode cleared` / T020 模板加 `## Hook Operational Status` 段 + stuck-true WARNING / T031 加 TestOnClearsReviewMode + TestTrustSummaryShowsReviewMode / T032 README 加 `--on` 完整恢复教学 / architecture §5.4 加 review_mode_set_at field + §5.5 模板更新 / SLA.md review session 流程加 `--on` 完整恢复 vs `--review-mode-off` 部分恢复区分 / risks.md PROD-3 health_check → CLI 入口 + SCH-1 22.5h/20h → 22.75h within 23h
- **R1 medium follow-up(显式 v0.2)**:`-f` path persistence / state corruption recovery / TECH-2 entry-volume math(architecture §7 已加)

## Open risk-level questions for operator

- **R1 H6 schedule** :operator 已选方案 (a)接受 22.5h 超 C1 12.5%。**若 R2 还加 finding 引入额外 hours**,必须二选:cut R2 提案中较低优先级项 OR 把该项推 v0.2。
