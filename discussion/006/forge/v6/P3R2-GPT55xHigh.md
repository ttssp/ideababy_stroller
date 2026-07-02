# Forge v6 · 006 · P3R2 · GPT55xHigh · 联合收敛 R2(finalize)

**Timestamp**: 2026-07-02T12:42:51Z
**Visibility**: 我已读对方 P3R2。
**Convergence mode**: strong-converge

## 1. 两条精修吸收确认

- **build_repo 优先级链**:确认采纳无误。`source_repo` / `handback_target` 属于 IDS 同仓路径,可用 `git rev-parse --show-toplevel` / `realpath`;但 `build_repo` 是另一个仓,不能从 IDS 的 `rev-parse` 得到。Opus 定稿里的 `$XENODEV_REPO` → sibling `../XenoDev` 且 `test -d` → fail-closed 让 operator 显式填,顺序正确,也符合 K 的“双机非发行、可执行优先”。
- **工具能力 resolver**:确认采纳无误。把 `sort -V` 从 open-item 升为“命令方言/工具能力”类别是必要的;3 级 resolver 也正确:先探测 `sort -V`,失败则 python3 按版本段转 int 排序,再退到受限 shell `sort -t. -k...`。我仍认可不依赖 `gsort`,因为那会把可移植性问题转成安装假设。

## 2. 联合 verdict(单一)

我确认定稿,0 实质分歧,可进 synthesizer。v6 的单一 verdict 是:009-pForge linux 新机首跑暴露的 5 条 KG 不是孤立 bug,而是“mac 环境形态被当 constant 写入框架”的系统性缺陷。最终修法应按硬编码性质分层:同仓绝对路径运行期取仓根;跨仓 `build_repo` 走显式 env/sibling/fail-closed;仓内相对路径锚 XenoDev 仓根;工具版本号走 glob + resolver;index/env config 走 `UV_DEFAULT_INDEX` + `--frozen`;命令方言走 capability probe + fallback;base 目录走 env/`$HOME`/XDG。同时 IDS 与 XenoDev 各放轻量硬编码 grep/pre-commit 守卫。KG-29 追认 keep,不推翻 009 已 ship 链。

## 3. 残余分歧降级为 v0.2 note

- mac `sort -V` 实测仍是 v0.2 note,但不阻塞,因为 resolver 已有 fallback;spec-writer 中“macOS 默认 sort 支持 -V”的注释应删除或改成“需探测”。
- `$XENODEV_REPO` 持久化是 v0.2 note:推荐 operator 在两机 shell profile 明确设;但 sibling/fail-closed 已兜底。
- KG-29 的 IDS/XenoDev 半同步窗口是工程纪律样本,应由同步 checklist + SHA 复验收口。

## 4. 给 synthesizer 的指令

按 Opus P3R2 §2 的 6 类矩阵生成 decision-list + refactor-plan,并把本文件 §1 的确认视为 Reviewer B 签字。W 输出里必须显式包含:build_repo 优先级链、版本 resolver 3 级、KG-30 log 降级为可审计留证、IDS+XenoDev 双侧 grep-gate、KG-29 keep 追认。
