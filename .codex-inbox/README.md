# Codex Inbox / Outbox 机制

## 这是什么

为了避免 human 在 Claude Code 和 Codex 终端之间反复"复制 kickoff 提示词、粘贴、记
住下一步、找文件"，本仓库使用 **文件总线** 在两个智能体之间传递任务。

- `.codex-inbox/` —— Claude Code 写、Codex 读。每个文件 = 一个待 Codex 执行的任务
- `.codex-outbox/` —— Codex 写、Claude Code 读。每个文件 = Codex 完成任务后的产物清单

human 在 Codex 终端只需要敲一行：

```
read .codex-inbox/latest.md and execute exactly what it says.
```

或者配置个 alias（见下面）。

## inbox 文件命名

```
.codex-inbox/
  ├── latest.md                              ← 总是指向最新一个
  └── 20260423T142500-001-L1R1.md            ← 时间戳-idea-任务
```

`latest.md` 是 symlink，每次 Claude Code 写新任务时自动更新。

## inbox 文件长什么样

每个 inbox 任务文件都是自包含的，Codex 读了就能执行：

```markdown
# Codex Task · idea 001 · L1R1

**Created**: 2026-04-23T14:25:00Z
**Created by**: Claude Code (Opus 4.7 Max acting as orchestrator)
**Recommended model**: gpt-5.4 (default)
**Recommended reasoning_effort**: high
**Estimated tokens**: ~8k

## 你需要做什么

[完整、自包含的任务描述，包括：
 - 读哪些文件
 - 不读哪些文件
 - 写到哪个文件
 - 内容模板
 - 风格约束
 - 完成后做什么]

## 完成后

把以下内容写到 `.codex-outbox/<同样的文件名>.md`：

```markdown
# Codex Done · idea 001 · L1R1
**Completed**: <ISO>
**Files written**: <list with line counts>
**Key moves this round**: <2-3 bullets>
**Self-flag**: <anything Claude should know about, e.g. "I had to make assumption X">
```
```

## Codex 端推荐设置

在 `~/.bashrc` / `~/.zshrc` 加：

```bash
# 一行执行最新 inbox 任务
alias cdx-run='codex "read .codex-inbox/latest.md and execute exactly what it says, then write the outbox confirmation file"'

# 看看 inbox 里有什么
alias cdx-peek='ls -lt .codex-inbox/ | head -5 && echo "---" && cat .codex-inbox/latest.md | head -50'
```

之后每次 Claude Code 提示 "Codex 任务已就绪"，你只要在 Codex 终端敲：

```
cdx-run
```

完事。

## 模型/effort 影响

inbox 文件的 frontmatter 包含 `recommended_model` 和 `recommended_reasoning_effort`。
高质量发散（L1 Inspire、L2 Explore）默认 `gpt-5.4` + `xhigh`；执行性任务（L4
build）可降到 `gpt-5.4-mini` + `medium`。

如果想覆盖，启动 Codex 时显式指定：

```bash
codex --model gpt-5.4 -c reasoning_effort=xhigh
cdx-run
```

## outbox 用途

Claude Code 在每次 `/status` 或下一阶段命令开始时，会扫 outbox 检查：
- 哪些任务 Codex 已完成（自动消化进 status 显示）
- 哪些任务还在等（提示 human "Codex 那边还没跑完，要等吗？"）

## 不用 inbox 行不行？

可以。每个命令的"下一步菜单"里也会显示完整 kickoff 文本，human 可以传统粘贴。
inbox 只是 **可选的快捷路径**。
