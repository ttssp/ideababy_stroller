# Forge v6 · 006 · P1 · GPT55xHigh · 独立审阅(no search)

**Timestamp**: 2026-07-02T07:34:27Z
**Searches used**: NONE in this round.
**Visibility**: I did NOT read the other reviewer P1.
**Reviewer stance**: 审阅人 — 评判已存在物,不是 daydream。

## 0. 我读到的标的清单 + 阅读策略

- 我读了:forge-config;`moderator-notes.md` 不存在;backlog KG-26..30;IDS `plan-start.md`/`SHARED-CONTRACT.md` §6.2;XenoDev 三 SKILL;KG29 diff+check-6;XenoDev `gen-handback.sh`+template;IDS `validate-handback.sh`/check-5;PROTOCOL P1 template。
- 我跳过的:无。`/home/ys/codes/XenoDev/` 可读;未读 Opus P1;未联网。
- **K 摘要**:K 判准是“同一根因 = 框架把某台 mac 的环境形态硬编码成默认”;binding 是本 forge 决策、SSOT 三层同步、不推翻 009 已 ship、只面向单人 mac+linux 双机。
- **阅读策略**:先按 Y1 找路径/版本/env/目录假设在 linux 的触发点,再按 Y2 看 contract、bootstrap-kit、XenoDev mirror/SKILL 是否漂移。

## 1. 现状摘要(按 Y 视角组织)

### Y1 · 跨机器可移植性

KG-26 把 `/Users/admin/codes/XenoDev` 写进 IDS 模板和 contract 示例,而本机是 `/home/ys/codes/XenoDev`。KG-27 在三 SKILL 中写死 mac codex 路径,且多处钉 `1.0.3`,本机是 `1.0.4`。KG-28 缺 uv/.venv/index/lock preflight。KG-30 假设 `tests/red-green-log/` 在仓根,mirror 子项目会被 `.gitignore` 挡。KG-29 已修;我实跑 `009-pForge`、`006a-pM-v0.2` PASS,`009-pv0.2` 与 `008/../../etc` FAIL。

### Y2 · 工程纪律

共同问题是 SSOT 分层漂移:协议示例、命令模板、SKILL、validator template 各自携带环境事实。X#5 证明同族未清:gen-handback 有 `IDS_ROOT` fallback,但 template 的 `to_source_repo`/`workspace.source_repo` 仍是 mac 字面量。KG-29 是较好样本,同步了 contract、bootstrap-kit、schema、fixture,但也暴露 IDS 先落、XenoDev mirror 后补的半同步窗口。

## 2. First-take 评分(5 条 KG 一一对应)

| KG | 倾向 | 理由 |
|---|---|---|
| KG-26 | refactor | 保留 workspace 语义,删除 mac 默认;射程要含 gen-handback template。 |
| KG-27 | refactor | 强 hook 不该写死 mac base/`1.0.3`;版本升级必腐烂。 |
| KG-28 | new | 新机首跑阻断项,需新增 env preflight 判定。 |
| KG-29 | keep | 追认,不推翻;只加字母后缀,负例仍被多层拒。 |
| KG-30 | refactor | 保留 red-green 证据,修正落点与 mirror 子项目错配。 |

## 3. 我现在最不确定的 3 件事

1. 环境事实入口该落协议、生成器、运行时,还是 env。
2. KG-28 preflight 是只报错,还是允许受控 bootstrap。
3. KG-30 log 是否必须随 commit,还是可审计留证即可。
