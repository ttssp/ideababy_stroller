# Tech Stack — 007a-pA

**Version**: 0.2
**Created**: 2026-05-08T13:30:00Z
**Revised**: 2026-05-08T13:55:00Z(R1 修订:仅 footnote;tech stack 主体不变)
**Source spec**: spec.md v0.2 §4 D1 / D2 / D9 / D12 + R1 review fix
**Tier**: 1(权威 — 修改版本号也要 bump minor)

## Primary stack

| Layer | Choice | Version | Rationale |
|-------|--------|---------|-----------|
| Language | Python | **3.11+**(macOS Sequoia 内置 3.13;3.11 是 spec 兼容下限) | D1:operator priority + C12 stdlib only;3.11 起 `tomllib` 内置 + `Self` type 支持 |
| Runtime | CPython 系统自带 | macOS 默认 `/usr/bin/python3` | D1:无 venv,无 pyenv;直接 shebang `#!/usr/bin/env python3` |
| Standard library only | stdlib | — | C12:维持工具自身 friction 极低;无 `pip install` 步骤 → operator 安装更轻 |
| Hook integration | Claude Code `PostToolUseFailure` hook | hooks system as documented at https://code.claude.com/docs/en/hooks(2026 含 `duration_ms`) | D2:载体 documented + 工业化(L2 §6 GREEN);project-local `.claude/hooks/post_tool_use_failure.sh` |
| File format | plain markdown(UTF-8) | — | grep-friendly;记事本可编辑(D5);O4 review 体验 |
| Config | JSON | RFC 8259 stdlib `json` | D12:human-readable;single file `~/.config/friction-tap/state.json` |
| Day-14 scheduler | launchd(macOS user agent) | macOS native(`~/Library/LaunchAgents/*.plist`) | D9:macOS native;cron 在新 macOS 需 Full Disk Access 妥协 |
| Test framework | `unittest`(stdlib) | Python 3.11+ | C12:无第三方 test 包;`unittest` 足以覆盖 spec.md §6 verification |
| Lint/format | 无强制(仓内已有 `ruff` 可选) | ruff latest(若 operator 已装) | C9 / C12:不强制安装;CI 阶段 v0.1 单 operator 不需 |
| CI | 无(本地手测 / commit hook 跑 `python -m unittest`) | — | C2 single-operator + C9;v0.2 ship 给 ADP 时再加 |
| Shell wrapper | `bash` minimal | macOS bash 3.2 / zsh 5.9 兼容 | install_launchd.sh 是 ≤30 行 bash;不引入 fish/zsh-only 语法 |
| 时间戳 | ISO-8601 UTC + `Z` suffix | stdlib `datetime.now(timezone.utc).isoformat()` | grep-sortable;tz-aware;无歧义 |

## Excluded alternatives

| Alternative | Rejected because |
|-------------|------------------|
| Node.js / TypeScript | C12 stdlib only;Node 需 npm + node_modules 安装 → 与 C9 拼 operator 时间相悖 |
| Go(单二进制可分发) | 编译步骤增加 install friction;macOS 下 Python stdlib 已够;ADR-1 静态规则 + ADR-3 markdown 不需 Go 性能 |
| Rust | 同 Go;且 stdlib `chrono`-equivalent 需第三方包 |
| `pip install requests` / `httpx` | 无网络调用(C5 RL-3 + ADR offline-only);stdlib 不需 |
| `pyyaml` | C12:state 用 JSON 而非 YAML — JSON 在 stdlib 中,human-readable 够用 |
| `pytest` | 同上 stdlib only;`unittest` 足以覆盖 |
| SQLite / 任何 DB | 14 天 < 30 KiB 数据;markdown 单文件足够,grep 比 SQL 更适合 single-operator review |
| HTTP server / FastAPI | C5 RL-4;无 dashboard;day-14 trust 报告是 markdown 文件不是 web 页 |
| LLM API(OpenAI / Anthropic Claude API) | D3 静态规则;LLM-judge 留 v0.2 |
| systemd / cron / `at` | D9 launchd is macOS native |
| `xattr` / macOS Keychain | 无 secret 需保管;state.json 字段非敏感(只 enabled / threshold / install_at) |
| `entry-id state machine`(SQLite + status) | D5 markdown tag + grep 已够;state machine 是 PRD scope OUT |
| Docker / 任何容器 | C12 + C2:单 operator macOS;容器化反向增 install friction |
| `psutil` / 任何进程监控 | 无 process 需观察(hook 是 fire-and-forget) |

## Dependency policy

> 本 v0.1 stdlib only,无 production dep,无 dev dep,无 transitive risk。

- **Production deps**: **0**(stdlib only)
- **Dev deps**: **0**(`unittest` 是 stdlib)
- **Audit**: 不需(无第三方依赖 = 无 supply-chain attack 面)
- **Max total deps**: **0**(若 v0.2 引入第三方包,必须重新过 dependency policy + bump minor)

**为什么这是 deliberate choice 不是简化**:
1. C12 工具自身 friction 必须极低 — operator 不能花 30 min 调 venv
2. C5 RL-3 无云依赖 — 任何第三方包都是潜在 phone-home 面
3. C1 时间预算紧 — 无 dep 等于无 dep 升级 / 无锁文件 / 无 supply chain incident 处理
4. PRD §"UX principles" simplicity > cleverness — 0 deps 是这个原则的极致表现
5. **R1 SEC-2 fix · D19 secret redact 用 stdlib `re`** — 不引第三方 secret-detection lib(如 `detect-secrets`),保 0 dep policy;v0.2 候选扩 entropy 检测仍打算手写

## Tooling versions(for reference / pinning)

| Tool | Version baseline | 来源 |
|---|---|---|
| macOS | 14 Sequoia / 15+(开发机当前 25.4) | 当前 env(`Darwin 25.4.0`) |
| Python | 3.11+ → 实际 macOS 自带 3.13 | 当前 `/usr/bin/python3 --version` |
| Claude Code CLI | latest documented(`PostToolUseFailure` 含 `duration_ms` 字段 = 2026 build) | L2 §6 prior art |
| launchd | macOS 系统自带 | C4 |
| git | 2.40+(`rev-parse --show-toplevel`) | macOS 自带 |

## Repo layout 预设(work for task-decomposer 参考)

```
specs/007a-pA/                    # 本 spec 包
projects/007-007a-pA/             # parallel-builder 实现路径
  tools/friction_tap/             # Python package
    __init__.py
    paths.py
    state.py
    format.py
    judge.py
    grep.py
    cli.py
    hook.py
    trust_summary.py
  bin/
    friction                      # CLI entry shebang script
  hooks/
    post_tool_use_failure.sh      # Claude Code hook entry
  scripts/
    install.sh
    install_launchd.sh
    uninstall_launchd.sh
  templates/
    trust_w2_template.md
  tests/
    test_judge.py
    test_state.py
    test_format.py
    test_paths.py
    test_integration.py
  README.md
docs/dogfood/                     # 主仓真实存放路径(D4)
  v4-friction-log.md              # 由 hook + CLI 写
  v4-trust-w2.md                  # 由 trust_summary 写(day 14)
~/.config/friction-tap/state.json # 唯一 config(D12)
~/Library/LaunchAgents/dev.idsmaintainer.friction-tap.trust-w2.plist
```

> task-decomposer 拥有完整决定权;以上是参考,非硬约束。
