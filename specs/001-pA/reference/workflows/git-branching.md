# Git Branching · 001-pA · PI Briefing Console

**版本**: 0.1
**创建**: 2026-04-23
**读者**: 所有提交 PR 的工程师
**原则**: 一个 task = 一个分支 = 一个 PR;Conventional Commits(CLAUDE.md 项目偏好)

---

## §1 分支命名

**单一模板**:`<type>/T<NNN>-<kebab-short>`

| type | 何时用 |
|---|---|
| `feat` | 新功能(大多数 task) |
| `fix` | 修 bug(含修已 merge 的 task 遗留问题) |
| `chore` | 非业务改动(deps / CI / 配置) |
| `docs` | 只改 docs 或 runbook |
| `test` | 只加/改测试(一般少见,测试通常随实现走) |
| `refactor` | 不改行为的重构 |
| `perf` | 性能优化 |

**`<NNN>`**:3 位数字,对齐 `specs/001-pA/tasks/T<NNN>.md`。
**`<kebab-short>`**:≤ 40 字符,全小写,短横连字符。

**示例**:
- `feat/T015-skip-why-input`
- `fix/T018-breadcrumb-dedupe`
- `chore/T002-bump-drizzle-0-36`
- `docs/T031-runbook-backup-section`

**反例**(会被 PR 自动化拒):
- `maya-dev`(无 task 号 / 无 type)
- `T15_skip_why`(下划线 / 无 type / 单字母序号)
- `feature/T015-add-a-lot-of-skip-related-stuff`(用 `feat` 不是 `feature`;描述过长)

---

## §2 Commit 消息:Conventional Commits(硬性)

**模板**:

```
<type>(T<NNN>): <short lowercase summary, ≤ 72 chars>

<blank line>
<body · 可选 · 多行 · 简述 why 或不显然的实现选择>

<blank line>
Closes T<NNN>
```

### 2.1 type 取值

和分支名的 type 一致:`feat` / `fix` / `chore` / `docs` / `test` / `refactor` / `perf` / `ci` / `build` / `revert`。

### 2.2 scope

scope 必定是 `T<NNN>`;**不使用** 其他 scope(不用 `auth` / `ui` / `worker` 等)。原因:scope 里有 task 号 → 所有 commit 可反查 task,git log 可读性一致。

### 2.3 Body 规则

- 先结论后细节(CLAUDE.md 中文注释规则的英文 commit 版)
- 列点用 `-` 而非 `*`
- 引用代码符号用反引号
- 引用 spec 时写 `spec §X` / `reference/xyz.md §N`
- **不写** "I did X", "我改了 X" 之类第一人称
- 不写 emoji(除非明确要求)

### 2.4 Footer

必须有一行 `Closes T<NNN>` 让 PR merge 时自动关联 task。一个 commit 可关闭多 task(仅当 task 确实是同一 PR 交付):`Closes T015, T016`。

### 2.5 示例(好)

```
feat(T015): add skip-why-input inline-expand component

- Implements D16 Layer 3: disabled `submit` until why.trim().length >= 5
- Uses useTransition so focus stays on textarea during submit
- aria-disabled mirrors `disabled` for screen-reader parity
- Renders character counter "(n/5 字符)" per api-contracts §3.4 `Action.why`

Closes T015
```

```
fix(T018): dedupe breadcrumb rows when user re-opens resurface card

- Partial UNIQUE idx `breadcrumbs_active_unique` already prevents DB
  duplicates; this patch stops the UI from sending a 2nd insert when
  the same card is clicked twice within 400ms (Safari touch quirk)
- Adds tests/unit/resurface-click.test.ts for the debounce guard

Closes T018
```

### 2.6 示例(坏 · 会被 lefthook `commit-msg` 拒)

```
// 拒: 无 type
add skip-why-input

// 拒: 无 scope / 无 task 号
feat: add component

// 拒: scope 不是 T<NNN>
feat(ui): skip why input

// 拒: Subject 大写开头 + 句号
feat(T015): Add Skip Why Input Component.
```

---

## §3 分支生命周期

### 3.1 开始

```bash
# 从 main 开新枝
git checkout main
git pull --ff-only origin main
git checkout -b feat/T015-skip-why-input
```

### 3.2 常规提交节奏

- 小而频繁;每 1–2 小时 commit 一次,即便只是 WIP
- 可以在本地用 `git commit --fixup=<sha>` 积累 fixup,之后 `git rebase -i --autosquash` 压合
- **允许** WIP 消息如 `wip(T015): textarea expands correctly`,但最终 push 前 **必须 squash 到合规的 Conventional Commits**
- 任何 push 前 **跟 operator 确认**(CLAUDE.md)

### 3.3 与 main 同步(periodic)

如果你的分支 > 2 天,期间 main 已前进:

```bash
git fetch origin main
git rebase origin/main
# 解冲突 → git add → git rebase --continue
# 强推:分支 push 过了才需要,rebase 后强推:
git push --force-with-lease
```

**禁止** `git merge main` 拉进来(产生 merge commit 污染 git log)。

### 3.4 Merge

- **Squash merge only**(GitHub 设置)
- Merge 时 PR 标题即最终 commit 消息的第一行;保持 Conventional Commits
- merge 后 **立刻** 删除分支(GitHub UI "Delete branch" 按钮)

### 3.5 Fixup 已 merged 的 task

发现之前 merged 的 task 有 bug → 开新分支 `fix/T<NNN>-<desc>`,commit 里写 `Fixes bug introduced by T<NNN-up>`,**不要** reopen 旧 task 文件。

---

## §4 禁令

| 禁 | 原因 |
|---|---|
| 直接 push 到 main | 无 PR review 就进 main |
| `git push --force`(不带 `--force-with-lease`) | 可能覆盖队友工作 |
| rebase `main` 自身 | 永远不 rebase 公共分支 |
| merge PR 时选 "Rebase" 或 "Merge commit"(非 Squash) | 本项目约定 squash |
| 同一 PR 跨多个 task 的业务功能 | 违反"一 task = 一 PR"原则;task-decomposer 会抓 |
| commit 里带 `.env` / 真实密钥 | pre-commit 已 gitleaks 扫;违者 CI 挂 |
| 在 commit 写 "[skip ci]" | 本项目 CI 必跑 |
| force-push 到别人的 branch | 协作禁忌;除非对方书面同意 |

---

## §5 tag & release

仅架构师 / operator 操作。

- 每个 milestone 结束 tag 一次:`v0.1.0-phase0` / `v0.1.0-phase1` / ...
- v0.1 ship 时 tag `v0.1.0` + GitHub Release 描述(指向 `spec.md` 变更日志对应版本)
- 若在 production 打过 hotfix,tag `v0.1.1` / `v0.1.2` 继续

Tag 命名:`v<major>.<minor>.<patch>[-<stage>]`。与 `spec.md` version 字段**不是 1:1 同步**(spec 版本表达合同演化,git tag 表达 release);合入 changelog 时互相引用即可。

---

## §6 Lefthook hooks 一览(本项目默认启用)

从 `reference/directory-layout.md §10`:

```yaml
pre-commit:
  - biome check --write {staged_files}
  - pnpm typecheck

commit-msg:
  - grep Conventional Commits 正则
```

**首次安装**:`pnpm lefthook install`。之后每次 `git commit` 自动跑。

**绕过 hooks**:`git commit --no-verify`(仅紧急情况;绕过就准备好在 CI 被同一套检查拒回)。

---

## §7 变更日志

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | 0.1 | 初版 · 分支命名 + Conventional Commits · 对齐 CLAUDE.md |
