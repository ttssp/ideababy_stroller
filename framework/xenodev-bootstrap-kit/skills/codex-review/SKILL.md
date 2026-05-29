---
name: codex-review
description: |
  XenoDev codex review 标准 SKILL · 单点真相决策"跑 review 还是 adversarial-review"
  + 真路径(node companion.mjs · 不是 codex exec hack)+ verdict 解析 fail closed
  + review log 留档。**覆盖 ship 流程内 cross-model gate + 独立 review(老 commit / PR / 别人代码)
  双场景**。

  **Load 触发条件**(任一满足必激活):
    1. parallel-builder SKILL §3 跑 cross-model review 时(ship 流程内 · 内部调用)
    2. operator 说"起 codex review" / "review T<NNN>" / "review commit <SHA>" / "压测 T<NNN>"
    3. operator 说"review 一下 <文件/PR/branch>"(独立 review · 非 ship 流程)
    4. operator 说"跑 adversarial-review" / "跑 codex review"(显式命令)

  **强约束**(违 = review 流程错误):
    - 真路径 = `node "/Users/admin/.claude/plugins/cache/openai-codex/codex/1.0.3/scripts/codex-companion.mjs" {review|adversarial-review} --wait --base <ref> --scope branch`
    - 不准走 `codex exec --json ... <手写 prompt>` hack 路径(companion 自动 collect git context · 不需手写 review framing)
    - 命令选择按 §2 决策表(adv 不是默认 · 普通改动用 review)
    - **commit message 是 codex 的 focus 真路径**:Conventional Commits + body 写清楚改了什么 / 为什么 / 重点验什么 · 让 codex 看 commit 自己定 focus(无需 CLI focus text)
    - `review` 命令真不接 focus text(companion 1.0.3 字面 · per commands/review.md L39)· 想加 focus → 写进 commit body / 升 `adversarial-review`(80/20 例外)
    - verdict enum 严格 `{approve, needs-attention}` · 任何其它值 fail closed
    - §3.2 解析必走 grep -E "^Verdict: " anchored full-line
    - review log 必留 worktree 内 `review-log/<TID>-round<N>.md`(ship 场景)或
      `review-log/<scope>-<date>-round<N>.md`(独立 review 场景)

inspired_by: 实际 ship 过程(T010-T020 复盘)发现默认全走 adversarial 浪费 round + over-engineer finding;operator 2026-05-17 决议分流
schema_version: 0.3
schema_version_history:
  - 0.1(2026-05-17 operator decision):从 parallel-builder §3.0/§3.1/§3.2/§3.3 抽出
    独立 SKILL · cover ship + 非 ship 双场景
  - 0.2(2026-05-18 operator decision · FU-T022-followup-3):
    T022 6 round 实证 `review` 命令真不接 focus text(companion 1.0.3 字面)·
    简化方案(operator D):commit message + `--base` 是 codex 真 focus 路径 · 不再绕走 adversarial · 不加 decision tree。
    改 §3.1/§3.2 真路径示例 + §6 加 anti-pattern(focus text 替代不了 commit message)
    驱动:IDS hand-back-id 004-pB-20260518T013000Z §4 + §7 #7
  - 0.3(2026-05-18 operator decision · FU-codex-review-skill-1):
    T002 2 round 实证 `review` 命令真不出 `Verdict: ` 行(companion 1.0.3 真路径输出格式 · 跟 adversarial-review structured schema 不同)。
    0 finding 时只出 codex Assistant 总结句 · 有 finding 时只出 `^- [P[0-9]]` finding 列表。
    分流方案:§4.1.1 adversarial-review 严走 Verdict: 行 · §4.1.2/§4.1B review 命令走 P-prefix 推断
    (0 P-prefix + 总结句 = approve 等价 / ≥1 P-prefix = needs-attention / 0+0 = fail closed)。
    §6 加 anti-pattern #9 防 adv 0 Verdict 行误套 review 推断规则 · §7 表 update · §8 加 0.3 升级 entry。
    驱动:T002 hand-back 004-pB-20260518T102817Z §4
tools: Read, Write, Edit, Glob, Grep, Bash
model: opus
isolation: inline
disable-model-invocation: false
---

# codex-review · XenoDev cross-model review 单点真相

> **结论先**:codex 是 XenoDev cross-model review 的强 hook(per AGENTS.md C11)· 两条 path(`review` 标准 / `adversarial-review` 对抗)· 按 §2 决策表选 · 不默认全走 adv · 真路径走 node companion.mjs · 不走 codex exec hack · verdict 严格 enum + fail closed。

## §0 输入硬约束(失败立停 · fail closed)

### §0.1 codex CLI 可用性

```bash
test -f "/Users/admin/.claude/plugins/cache/openai-codex/codex/1.0.3/scripts/codex-companion.mjs" \
  || { echo "ERR: codex companion.mjs 缺;先装 codex plugin" >&2; exit 1; }
which node >/dev/null || { echo "ERR: node 不可用" >&2; exit 1; }
```

### §0.2 review scope 必明

| scope 模式 | 触发 | 说明 |
|---|---|---|
| **ship 流程内**(working-tree)| parallel-builder SKILL §3 调 | worktree 内未 commit 改动 + 已 commit 但未 merge 改动 |
| **独立 review · branch**(commit SHA / branch)| operator 显式"review commit X" / "review branch Y" | 已 merge 的老代码 / 别人的 PR |
| **独立 review · working-tree** | operator 在 main 上想 review 自己改动 | 跟 ship 流程 path 相同 |

scope 不明 → 必问 operator · 不猜。

## §2 决策表(adv 不是默认 · 按 task 风险面选)

两个命令是**并列**关系 · 不是 adv 替代 review · 选哪个看风险面:

| 命令 | 用途 | 强度 | 适用场景 |
|---|---|---|---|
| `/codex:review`(标准)| bug / 质量 / 一致性扫描 | 标准 1-2 round | 普通改动 · 风险面小 |
| `/codex:adversarial-review`(对抗)| 挑战架构 / edge / 风险 / 安全 + 完整 review | 严苛 2-4 round | 高风险 · spine 重构 · 安全敏感 |

### §2.1 走 adversarial-review(任一命中)

| 触发条件 | 例子 |
|---|---|
| task `risk_level: high` | T013 / T040-A / T020 |
| phase 2-3 spine 重构(parser / orchestrator / ledger core / decision pipeline 核心)| T020 parser 三层 |
| 改 alembic migration 文件(`alembic/versions/*.py` 新增) | T010 / T020 alembic 0010 |
| 改 raw SQL / ORM SQL 模板(SEC-4 SQL injection 面) | upsert_weekly SQL 扩字段 |
| 改 auth / 凭据相关代码(credential / token / session) | secrets/ 相关 |
| 新增 API endpoint / 路由(FastAPI router add) | T040 SLA 4 endpoint chain |
| operator 显式说"起 adversarial review" / "压测 review" | 手动覆写 |

### §2.2 走 review(默认 fallback)

| 触发条件 | 例子 |
|---|---|
| task `risk_level: low` / `medium` 单层改动 | T011 recall_score · T012 agent prompt |
| FU-* hotfix / FU-followup(纯 bug fix · 无设计决策) | FU-notes-fix · FU-weekly-fix |
| docs-only commit(specs/ / *.md 改 · 0 src 改动) | retroactive amendment 类 |
| domain field 加 / repo method 加 / 普通 CRUD 扩 | 单文件级改动 |
| 独立 review 老代码 / 别人 PR(operator 显式 review 命令)| operator 主动 review |

### §2.3 跳过 review(只此一种)

| 触发条件 | 例子 |
|---|---|
| retroactive spec amendment commit · 纯 task frontmatter 改 · 0 src/tests 改 | T013 / T040-A / T020 spec amend |

### §2.4 选错时 fallback

| 错误 | 处置 |
|---|---|
| 本该 review 但跑了 adversarial | 不破事 · review 通过即可 · 下次按表 |
| 本该 adversarial 但跑了 review | review 通过 → operator 再跑一次 adversarial · 不接受只 review 就 ship 高风险 task |
| operator 觉得规则误判 | operator 显式 override · skill 不强制 enum 化(留人判断空间) |

## §3 跑 codex(两条 path)

### §3.0 真路径决定:commit message 是 codex 的 focus(0.2 起)

T022 6 round 实证 + companion 1.0.3 commands/review.md L39 字面:
- **`review` 命令真不接 focus text**(只接 `--base` / `--scope` / `--wait`)
- **`adversarial-review` 真接末尾位置参数** `[focus text]`(80/20 例外用)
- **真路径**:commit message body(Conventional Commits + 详细说明)= codex 真 focus · 让 codex 看 commit 自己定 focus

agent 跑 review 前必先确保 commit message body 写清:
- **改了什么**(file 列表 + 关键改动点)
- **为什么**(spec 行 / decision 引用 / operator Q&A 决议)
- **重点验什么**(round 1 review 关注点)
- **scope 守边界**(无 Out of scope 文件改动 / 依赖声明)

不写好 commit message 想用 CLI focus text 凑 = 治标不治本(只在挑某个具体设计假设 / commit body 没明说的点时 · 才升 `adversarial-review` + focus 80/20 例外路径)。

### §3.1 path A · `adversarial-review`(高风险)

```bash
node "/Users/admin/.claude/plugins/cache/openai-codex/codex/1.0.3/scripts/codex-companion.mjs" \
  adversarial-review --wait --base main --scope branch
```

可选末尾 focus text(只在 commit body 不够说清某个具体假设时加 · 80/20 例外):

```bash
node companion.mjs adversarial-review --wait --base main --scope branch \
  "重点 challenge: <spec 某行假设是否兜底 / 某个 edge case>"
```

### §3.2 path B · `review`(普通)

```bash
node "/Users/admin/.claude/plugins/cache/openai-codex/codex/1.0.3/scripts/codex-companion.mjs" \
  review --wait --base main --scope branch
```

**真不接 focus text**(companion 1.0.3 字面)· focus 全来自 commit message 真路径:codex 看 `git log main..HEAD` + 每 commit 的 diff 自己定 review focus。

### §3.3 命令参数说明

| 参数 | 必加 | 说明 |
|---|---|---|
| `--wait` | ✅ | 前台跑 · review < 60s · adversarial < 90s · 不加会异步返不可用 |
| `--base <ref>` | ✅ ship 流程 | branch 模式必给 base(通常 `main`)· codex 自动算 `<base>...HEAD` 真 diff 包 commit + 文件改动 |
| `--scope branch` | ✅ ship 流程 | ship 流程内 commits 已落 worktree branch · 走 branch 模式让 codex 看完整 commit 序列 + body(commit message 是 focus 真路径) |
| `--scope working-tree` | 备用 | 改动还在未 commit 状态时用(operator 临时 review 草稿) |
| `[focus text]` 末尾位置参数 | ❌ `review` 不接 · ✅ `adversarial-review` 80/20 例外 | review framing **必写进 commit body**(focus 真路径)· 只在 commit 没法说清具体假设时升 adversarial + focus |

ship 流程内必跑 `--wait --base main --scope branch`;独立 review 显式指定 base + scope。

### §3.4 ship 流程内调用(parallel-builder SKILL §3 内部)

parallel-builder §3 调本 SKILL 时:

1. 读 task frontmatter `risk_level` + `phase` + `file_domain`
2. 按 §2.1/§2.2 决策表自动选 path A 或 B
3. **commit message 真路径 contract**(关键):
   - 每个 commit body 写清 task / scope / 改动点 / 重点验点 / 依赖声明 / 边界守
   - red commit:写清"why red / TDD red phase / 14 fail 1 pass 期望"
   - green commit:写清"impl + verify 项 + 0 回归证据 + Conventional `feat(<scope>):` / `fix(<scope>):`"
   - fix commit(round N · 修 codex finding):写清"round N codex finding 摘要 + fix 真路径 + 新增 test"
4. 跑 §3.1/§3.2 命令(`--base main --scope branch` 真路径 · review 命令**不传 focus text**)
5. §4 verdict 解析(共用)
6. §5 log 留 worktree 内 `review-log/<TID>-round<N>.md`

### §3.5 独立 review 调用(非 ship 流程)

operator 说"review commit X" / "review PR Y" 时:

1. 必问 scope:working-tree / branch / 具体 SHA
2. 按 §2 决策表问"高风险吗?"(默认 path B · operator 可覆写 path A)
3. 跑 §3.1/§3.2 命令(`--base <ref> --scope branch` · review 不传 focus · adversarial 可选 focus)
4. §4 verdict 解析
5. §5 log 留 `review-log/<scope-slug>-<date>-round<N>.md`(不是 TID · 因为不在 task 流程内)

## §4 verdict 解析(对齐 codex companion 真 enum · fail closed)

per parallel-builder round-3 codex F1(实证 codex companion mjs 源代码):codex `/codex:adversarial-review` 真实 verdict enum = **{`approve`, `needs-attention`}**(structured review schema)。`/codex:review` 真路径输出格式不同(per 0.3 升级 实证):有 finding 时只出 `^- [P[0-9]]` finding 列表 · **不**出 `Verdict:` 行;0 finding 时只出 codex Assistant 总结句 · 仍**不**出 `Verdict:` 行。

**对齐后 enum**(adversarial-review 严走 Verdict: 行 · review 命令真路径走 P-prefix finding 推断):

### §4.0 命令分流解析(adversarial-review vs review)

| 命令 | 真路径输出格式 | 解析规则 |
|---|---|---|
| `adversarial-review` | 严走 structured schema:输出顶层 `Verdict: approve` / `Verdict: needs-attention` 行 | §4.1 表 enum 严格匹 · 0 / 多 Verdict 行 = fail closed |
| `review` | **无 `Verdict:` 行**:有 finding 时输出 `^- [P[0-9]]` 列表 · 0 finding 时输出 codex Assistant 总结句 | §4.1B 表 P-prefix 推断 · 0 P-prefix + 总结句 = approve 等价 |

### §4.1 enum 表(adversarial-review 严走)

| 顶层 `Verdict:` 行(anchored full-line)| 处理 |
|---|---|
| `Verdict: approve` | PASS · 进下游(ship 流程 = parallel-builder §4 merge / 独立 review = 报 operator) |
| `Verdict: needs-attention` | **不**进下游 · 按 finding 改 impl(回 ship 流程 §2 / 独立 review 等 operator 决策)→ 重跑(最多 4 轮)|
| 0 个 / 多个 `Verdict:` 行 / 未命中 enum | **fail closed**:不放行 · stderr 真粘 · operator 修 codex / SKILL §4 · **`adversarial-review` 0 Verdict 行仍 fail closed**(adv 必出 verdict · 缺 = bug) |

### §4.1B review 命令 P-prefix 推断表(0.3 升级)

| codex stdout 真路径 | 推断 verdict | 处理 |
|---|---|---|
| 0 个 `^- [P[0-9]]` finding + 含 codex Assistant 总结句(eg "未发现阻断性问题" / "no findings") | **approve 等价** | PASS · 进下游 · log 留档时记"P-prefix 推断 approve" |
| ≥1 个 `^- [P[0-9]]` finding | **needs-attention 等价** | 不进下游 · 按 finding 改 impl · 重跑 |
| 0 个 P-prefix + **0** Assistant 总结句(stdout 完全空 / 只 [codex] command log)| fail closed | stderr 真粘 · operator 修 codex / SKILL |

**关键**:本 §4.1B 仅适用 `review` 命令 · `adversarial-review` 仍走 §4.1 严格 Verdict: 行解析。

### §4.1.1 严格解析命令(adversarial-review · 严走 Verdict: 行)

```bash
bash -c '
set -e
CODEX_MJS="/Users/admin/.claude/plugins/cache/openai-codex/codex/1.0.3/scripts/codex-companion.mjs"
CMD="${1:-adversarial-review}" # 本节专用 adversarial-review
SCOPE="${2:-working-tree}"
FOCUS="${3:?focus 必传}"

CODEX_OUT=$(node "$CODEX_MJS" "$CMD" --wait --scope "$SCOPE" "$FOCUS") || {
  echo "ERR: codex 进程 exit 非 0 · review fail closed" >&2
  exit 1
}
[[ -n "$CODEX_OUT" ]] || { echo "ERR: codex stdout 空 · fail closed" >&2; exit 1; }

# 抽所有 ^Verdict: 开头的行(anchored · full-line)
VERDICT_LINES=$(printf "%s\n" "$CODEX_OUT" | grep -E "^Verdict: " || true)
VERDICT_COUNT=$(printf "%s" "$VERDICT_LINES" | grep -c "." || true)
[[ "$VERDICT_COUNT" -eq 1 ]] || {
  echo "ERR: codex 输出含 $VERDICT_COUNT 个 Verdict: 行 · 期 exactly 1 · fail closed" >&2
  printf "%s\n" "$CODEX_OUT" >&2
  exit 1
}

VERDICT=$(printf "%s" "$VERDICT_LINES" | sed "s/^Verdict: //")
case "$VERDICT" in
  approve)         echo "review PASS"; ;;
  needs-attention) echo "review needs-attention · 回上游修"; exit 2 ;;  # 2 = verdict-block;1 = process-fail
  *)               echo "ERR: Verdict=\"$VERDICT\" 不在 enum {approve, needs-attention} 内 · fail closed" >&2; exit 1 ;;
esac
'
```

### §4.1.2 严格解析命令(review · 走 P-prefix finding 推断)

```bash
bash -c '
set -e
CODEX_MJS="/Users/admin/.claude/plugins/cache/openai-codex/codex/1.0.3/scripts/codex-companion.mjs"
SCOPE="${1:-working-tree}"
BASE="${2:-main}"

CODEX_OUT=$(node "$CODEX_MJS" review --wait --base "$BASE" --scope "$SCOPE") || {
  echo "ERR: codex 进程 exit 非 0 · review fail closed" >&2
  exit 1
}
[[ -n "$CODEX_OUT" ]] || { echo "ERR: codex stdout 空 · fail closed" >&2; exit 1; }

# review 命令真路径不出 Verdict: 行 · 走 P-prefix finding 推断
P_PREFIX_COUNT=$(printf "%s\n" "$CODEX_OUT" | grep -cE "^- \[P[0-9]\]" || true)
ASSISTANT_LINE=$(printf "%s\n" "$CODEX_OUT" | grep -E "\[codex\] Assistant message captured" | head -1 || true)

if [[ "$P_PREFIX_COUNT" -eq 0 ]]; then
  if [[ -n "$ASSISTANT_LINE" ]]; then
    echo "review PASS · 0 finding · approve 等价(P-prefix 推断)"
    exit 0
  else
    echo "ERR: 0 P-prefix finding 且无 Assistant 总结句 · stdout 异常 · fail closed" >&2
    printf "%s\n" "$CODEX_OUT" >&2
    exit 1
  fi
else
  echo "review needs-attention · $P_PREFIX_COUNT P-prefix finding · 回上游修"
  exit 2
fi
'
```

### §4.2 4 轮上限(同 spec-writer SKILL §3.2)

| 轮次 | verdict | 处置 |
|---|---|---|
| Round 1-3 | needs-attention | 按 finding 改 impl · 重跑 |
| Round 4 | needs-attention | **hard-stop** · operator 决:接受 finding ship / 升级 forge / 退 task |
| 任意轮 | approve | PASS · 进下游 |
| 任意轮 | fail closed(verdict 不在 enum) | hard-stop · operator 修 codex / SKILL |

**注**:codex companion 升级若改 enum → 本 §4 拒收 · operator 必更新此节;`fail closed` 设计意图就是不悄漂。可改用 codex `--json` 输出 + `jq -r '.result.verdict'` 更鲁棒(future enhancement)。

## §5 review log 留档

### §5.1 ship 流程内(worktree)

```
.claude/worktrees/<TID-slug>/review-log/<TID>-round<N>.md
```

例:`.claude/worktrees/t020-parser-refactor/review-log/T020-round2.md`

内容:codex stdout 完整 dump · 不脱敏(worktree 不进 main · merge squash 时丢)。

### §5.2 独立 review(主仓 review-log/)

```
review-log/<scope-slug>-<YYYY-MM-DD>-round<N>.md
```

例:`review-log/commit-7eb8626-2026-05-17-round1.md`(review FU-notes-fix ship 后老 commit)

内容:codex stdout 完整 dump · operator 自行决定要不要 commit 这个 log。

### §5.3 log 必含

- codex 命令真实参数(可 reproduce)
- codex stdout 完整(verdict + findings + 推理过程)
- 处理结论(approve → ship / needs-attention → 修哪 finding / fail closed → operator 决策)

## §6 Anti-patterns(直接拒)

1. **走 `codex exec --json` hack 路径**(手写 prompt · 自己解析 verdict)→ 拒;companion 自动 collect git context + structured schema · 手写必漂
2. **默认全走 adversarial**(不看 risk_level)→ 拒;按 §2 决策表 · adv 浪费 round + over-engineer finding(实证 T010-T020 期间)
3. **跳过 review 直接 merge**(高风险 task)→ 拒 · 违反 C11
4. **verdict 字符串模糊匹配**(`grep -i approv` 类)→ 拒 · §4.1 必 anchored full-line + enum exact match
5. **review needs-attention 后强 ship**(不修 finding)→ 拒 · 必回上游改 · 4 轮上限触顶才 hard-stop
6. **log 不留档**(只看 stdout 不存文件)→ 拒 · §5 必留(后续 audit / handback 引用)
7. **scope 不明就跑**(scope 默认猜)→ 拒 · §0.2 必问 operator
8. **focus text 替代不了 commit message**(T022 FU-T022-followup-3 实证)→ 拒
   - **真路径**:codex 看 `--base...HEAD` 的 commit message + diff 自己定 focus · commit body 写清楚就够
   - **失败模式 A**:commit body 写一行"feat: T022 ship" + 想用 CLI focus text 700 字凑 review framing → focus text 真冗余 + commit history 不可追溯
   - **失败模式 B**:`review` 命令真不接 focus → agent 默认升 `adversarial-review` 走 focus path → 杀伤过大(adversarial 强度 + 多轮 round)→ 滚 finding(T022 6 round 实证)
   - **真做法**:Conventional Commits + 详细 body(改了什么 / 为什么 / 重点验什么 / scope 守)· review 命令直接 `--base main --scope branch` 不传 focus
9. **`adversarial-review` 0 Verdict 行套用 review P-prefix 推断规则**(T002 0.3 升级实证)→ 拒
   - **真路径**:adversarial-review 严走 structured schema · 必出 `Verdict: approve` 或 `Verdict: needs-attention` 行 · 0 Verdict 行 = codex bug · 必 fail closed
   - **失败模式**:adv 真路径 0 Verdict 行 + agent 误套 §4.1B P-prefix 推断("0 P-prefix + Assistant 总结句 = approve")→ 漏掉 adv 真正的 fail closed 语义 · 让 codex bug 漂过 ship gate
   - **真做法**:本节 §4.1B 推断规则**仅适用 `review` 命令** · adv 0 Verdict 行 = §4.1.1 fail closed + operator 修

## §7 Failure mode + escalation

| 症状 | 处置 |
|---|---|
| codex CLI 不可用(node 报错)| stderr 真粘报错;**不**静默 mark reviewed;operator 修 codex 安装 |
| codex `--wait` 超时(> 120s) | stderr 真粘;operator 决:重试 / 缩 scope / 升 forge |
| `adversarial-review` 输出 0 / 多个 Verdict: 行 | fail closed · operator 修 codex / SKILL §4.1.1(adv 必出 verdict · 缺 = bug)|
| `review` 输出 0 Verdict: 行(0.3 起真路径默认 · 不再 fail closed)| 走 §4.1B P-prefix 推断:0 P-prefix + 总结句 = approve 等价 / ≥1 P-prefix = needs-attention / 0 P-prefix + 0 总结句 = fail closed |
| codex verdict ∉ {approve, needs-attention} | fail closed · operator 修 SKILL §4 enum 接 codex 新版本 |
| 4 轮 needs-attention | hard-stop · operator 决(同 spec-writer §3.2)|
| operator 想 override 决策表(adv→review 或反向)| 显式说"用 review/adv"覆写 · SKILL 不强 enum |

## §8 review_history(本 SKILL 自身经历的 review)

本 SKILL 派生自 parallel-builder §3.0/§3.1/§3.2/§3.3 · 内容字节级 cp · 决策表是 2026-05-17 operator 加新增。后续若 codex companion enum 变化 / review 命令路径迁移 / decision rule 演化 → 单点真相在本 SKILL · parallel-builder §3 引用即可。

### §8.1 0.2 升级(2026-05-18 · FU-T022-followup-3)

T022 ship 6 round 实跑实证:

| 维度 | 0.1 错路径 | 0.2 真路径 |
|---|---|---|
| `review` 命令是否接 focus text | 0.1 假设接 · 命令报错"does not support custom focus text" | 真不接(commands/review.md L39 字面)|
| 替代方案 | 0.1 默认升 `adversarial-review` 走 focus path · T022 全 6 round 走 adv | 写 commit body · `--base main --scope branch` 让 codex 自动 focus |
| adversarial vs review 工具定位 | 0.1 默认全 adv(0.2 起按 §2 决策表已分流)| 两工具目标不同 · adv 是榔头 · review 是起子 · 误升级 = 杀伤过大 + 滚 round |
| 真后果 | T022 round 2-6 滚 5 finding(round 1-3 真有用 / round 4-6 是 partial-failure recovery 同类 pattern · 工具误用放大噪声) | commit body 写好就够 · 不滚 round |

驱动:IDS hand-back-id `004-pB-20260518T013000Z` §4 + §7 #7 · FU-T022-followup-3

### §8.2 0.3 升级(2026-05-18 · FU-codex-review-skill-1)

T002 ship 2 round 实跑实证:

| 维度 | 0.2 错路径 | 0.3 真路径 |
|---|---|---|
| `review` 命令是否出 `Verdict: ` 行 | 0.2 假设出(跟 adversarial-review 共享 enum)| **真不出**(0 finding 时只出 codex Assistant 总结句 · 有 finding 时只出 `^- [P[0-9]]` finding 列表 · 全程无 `Verdict: ` 行)|
| 0 Verdict 行处理 | 0.2 一律 fail closed(SKILL §4.1)· T002 round 2 真路径误拦 approve 等价 | **分流**:review 命令 0 Verdict 行 = §4.1B P-prefix 推断 / adversarial-review 0 Verdict 行 = §4.1.1 fail closed(adv 必出 verdict)|
| 推断规则 | 0.2 无 | §4.1B:0 P-prefix finding + Assistant 总结句 = approve 等价 / ≥1 P-prefix = needs-attention 等价 / 0 P-prefix + 0 总结句 = fail closed |
| 真后果 | T002 round 2 codex 跑完 0 finding · agent 严走 §4.1 fail closed 拦 ship · operator 介入决"语义 approve" 续 ship | review 命令 0 finding case 真路径自动 PASS · 不需要 operator 决议 · 跟 adv path 解耦 |

驱动:T002 hand-back `004-pB-20260518T102817Z` §4 · FU-codex-review-skill-1
跟 0.2 同性质 — SKILL 字面落后于 codex companion 真路径输出格式 · 0.3 修 review 命令 P-prefix 推断 · 跟 0.2 修 commit message focus 路径同 pattern

## §9 与上下游的关系

- **上游**:parallel-builder SKILL §3(ship 流程内调本 SKILL)/ operator 直接调(非 ship 流程)
- **下游**:
  - ship 流程:verdict=approve → parallel-builder §4 merge / verdict=needs-attention → parallel-builder §2 改 impl
  - 非 ship:verdict 报 operator 决策
- **跨 SKILL**:
  - parallel-builder §3 决策规则**完全引用本 SKILL §2**(单一真相)
  - spec-writer §3 cross-model review 也走本 SKILL(自 v0.2 起 · 当前 spec-writer 还独立 · backlog 合并)

## §10 完成 checklist(每次 review 前 operator 自审)

- [ ] §0.1 codex CLI 真可用(companion.mjs 存在 + node 可调)
- [ ] §0.2 scope 明确(working-tree / branch / SHA)
- [ ] §2 按决策表选 path(A=adversarial / B=review / 跳过 = retroactive 纯文档)
- [ ] §3 跑 codex 真路径(node companion.mjs · 不走 codex exec hack)
- [ ] §4.1 verdict 严格 anchored 解析 · enum 命中 · fail closed 兜底
- [ ] §5 log 留档(worktree 内 ship / 主仓 review-log/ 独立)
- [ ] verdict=approve → 报上游 PASS;needs-attention → 回上游改 · 重跑

---

**Provenance**:
- 决策表(§2)2026-05-17 operator 决议(实证 T010-T020 ship 复盘 · 默认全走 adv 浪费)
- 真路径 + verdict 解析(§3.1/§3.2/§4)字节级 cp 自 parallel-builder §3.0/§3.1/§3.2/§3.3(v0.2 → 0.3 之前)
- 4 轮上限 + fail closed 派生自 spec-writer SKILL §3.2 + parallel-builder round-3 codex F1
- codex companion 路径 = `/Users/admin/.claude/plugins/cache/openai-codex/codex/1.0.3/scripts/codex-companion.mjs`(operator 2026-05-17 提供的官方路径)
