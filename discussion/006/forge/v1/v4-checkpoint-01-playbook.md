---
horizon: 2026-06-03 ± (V4 frozen 后第 4 周)
in_repo: autodev_pipe (执行) + ideababy_stroller (索引)
goal: 满足 ADR 0008 AC5(每 4 周 1 份 checkpoint,12 周 ≥3 份);诚实记录 V4 frozen 后的 dogfood 真实状态(可能是 "0 个真自用项目")
estimate: 50 min - 1.5h(乐观)~ 4-5h(若 retrospective skill 多次重跑)
prerequisite: 4 周等待期已过即可执行(2026-06-03 ± 任一天)
upstream:
  - discussion/006/forge/v1/playbook-4-weeks.md (本 playbook 是其 Step 5 的展开)
  - discussion/006/forge/v1/stage-forge-006-v1.md (forge 006 verdict)
  - autodev_pipe/docs/decisions/0008-v4-dogfood-path.md (AC4/AC5/D5 时间约束)
  - autodev_pipe/docs/decisions/0009-v4-scope-downgrade.md (D5 12 周浮现条件)
  - autodev_pipe/docs/dogfood/v3.3-w27-retrospective.md (模板参考)
---

# v4 checkpoint-01 Playbook · forge 006 路径 2 W3 必做

本 playbook 是 `playbook-4-weeks.md` Step 5 的可执行展开,2026-05-09 写,基于 ADP 当时实测状态:

**ADP 实测状态(2026-05-09 grep)**:
- V4 frozen 后 commit = 全部是 V4 spec 自审 round 1-4(`574a2ee 重 frozen` 是最后一次),**无真自用项目 commit**
- `docs/dogfood/v4-friction-log.md`:**MISSING**(playbook step 4 dogfood 流程未启动)
- `~/.claude/lessons/`:2 条(V3 遗留 `core-enum-validation-twins.md` + `core-promise-implementation-debt.md`),V4 frozen 后无新增
- `specs/v4/`:仅 `spec.md` + `reviews/`,无真自用 feature 子目录

→ checkpoint-01 必须以**诚实记录 dogfood 未发生**为主要叙事,不能假装有数据。

---

## Section 0 · 执行前自查(IDS,5 min)

W3 当天(2026-06-03 ±),先在 IDS 这边跑 4 项 grep 重新校准 ADP 真实状态(可能 4 周里 W2 期间有变化):

```bash
cd /Users/admin/codes/autodev_pipe

# 1. V4 frozen 后是否有真自用项目 commit
git log --since="2026-05-06" --oneline | grep -v -E "specs-v4-review|v4-frozen|fix\(v4-script" | head -20
# 期望:0 行 = 4 周 0 真自用项目;若有 → 标记到 checkpoint-01 §1 AC4

# 2. friction-log 是否存在
test -f docs/dogfood/v4-friction-log.md && wc -l docs/dogfood/v4-friction-log.md || echo "MISSING"
# 期望(2026-05-09 实证):MISSING;若 W2 期间补创建 → 报条数

# 3. 新 lesson 数量
ls ~/.claude/lessons/ | wc -l
# 期望:2(V3 遗留);若 >2 → 列出新增

# 4. 真自用 spec 子目录数量
find specs -mindepth 2 -maxdepth 2 -name "spec.md" | grep -v "v4/spec.md\|v3" | wc -l
# 期望:0;若 >0 → 那就是真自用项目候选
```

四项数据存到一个临时 txt(`/tmp/checkpoint-01-prep.txt` 或同等位置),作为 §1 retrospective skill 的输入素材。

---

## Section 1 · 切到 ADP 跑 retrospective skill(ADP,30-60 min)

```bash
cd /Users/admin/codes/autodev_pipe
claude
```

ADP Claude Code session 里粘贴下面 prompt(基于 `playbook-4-weeks.md` L279-313 但适配"4 周低活跃"现实):

> ```
> 今天是 2026-06-03,V4 frozen 后第 4 周 checkpoint-01 时间点。
>
> 请用 .claude/skills/retrospective/ skill 走 L2 phase 级 retrospective,
> phase 范围 = "V4 frozen → 现在 这 4 周"。
>
> 输入(实证 4 项,可能多数为空,**诚实写空**不要造假):
> - git log 2026-05-06..HEAD(限 specs/v4/ + .claude/skills/retrospective/ +
>   scripts/append_lesson.py + scripts/init_user_lessons.py +
>   templates/AGENTS.md + 真自用项目范围;若仅有 V4 自审 commit,如实说)
> - specs/v4/spec.md(读最新 frozen 版本)
> - docs/dogfood/v4-friction-log.md(若 MISSING,写 "未创建 → step 4 dogfood 流程未启动")
> - specs/<feature>/ 下 L1 retrospective(若仅有 V4 自身,如实说)
> - ~/.claude/lessons/ 4 周新增(若仅有 V3 遗留 2 条,如实说)
>
> 输出:写到 docs/dogfood/v4-checkpoint-01.md,模仿
> docs/dogfood/v3.3-w27-retrospective.md 的结构,8 节必须全含:
>
> 1. AC4 进度:V4 真自用业务项目候选浮现状态
>    - 实测计数(0 / 1 / >1?)
>    - 若 0:列出原因(operator 把 4 周时间投到 forge 006 路径 2 跨仓 dogfood,
>      ADP V4 frozen 后未启动真自用 feature)
> 2. AC5 兑现:本份是第 1/3 份 checkpoint(2026-05-06 → 2026-06-03)
> 3. D5 12 周硬条件预判:
>    - 还剩 8 周(到 2026-07-29)
>    - 浮现 1 个真自用项目的概率(高/中/低 + 为什么)
>    - 若 0 候选 → 概率必然降为"中-低",触发 ADR 0009 D5 复审
> 4. 3 段 retrospective:
>    - V4 工具链本 phase 真有用:V4 spec 自审 4 round 暴露的 F1+F2 修订
>    - 假阳性:V4 frozen 后未跑真自用,工具是否过度设计无法实证
>    - 漏抓:跨仓 dogfood (forge 006 路径 2) 暴露的 SHARED-CONTRACT
>      drift 是否应该 V4 早期就警示
> 5. 真自用项目带回的 friction:
>    - 实测 = 0 条(friction-log MISSING)
>    - 但跨仓 dogfood 在 IDS 仓 framework/ADP-AUDIT-2026-05-08.md §9 沉淀
>      4 条 cross-repo drift,作为补充信号
> 6. 路径 2 gap 取舍输入(给 ideababy_stroller framework 用):
>    - gap-1(production credential 隔离 + 备份破坏检测):4 周内有没有
>      遇到真实威胁?(实证:无真自用 = 无威胁数据;但 IDS framework
>      §2 仍标 1-2 周 ADP 工作量)
>    - gap-2(risk tier 分类器):4 周内 reviewed-by hook 是否漏抓什么?
>      (实证:仅 V4 自审,4 round Codex review 闭环顺利)
>    - gap-3(Eval Score micro-benchmark):4 周内 G1-G10 + audit-consistency
>      + reviewed-by 是否够用?(实证:V4 自审表现充分)
> 7. V4 工具链是否到位:
>    - retrospective skill 自身(本次跑用了它 → 实证它能不能产出真报告而非
>      placeholder)
>    - append_lesson.py(F1+F2 修订 round 3-4,parser 严格化,force 路径生效)
>    - init_user_lessons.py(未在 4 周内动过)
>    - 真用过 4 周后,有应该改的吗?
> 8. 下一个 4 周(checkpoint-02)的 focus:
>    - 推荐:operator 在 8 周内浮现 ≥1 个真自用项目候选(D5 硬条件)
>    - 或:若 D5 不达 → 触发 ADR 0009 复审,V4 scope 进一步降级 / 终止
>    - 或:把 IDS 跨仓 dogfood §9 drift 4 条作为 ADP V5 设计输入
>
> 不要写到一半 placeholder;不要假数据;不知道就写"unknown" 或 "not yet
> applicable"。诚实优于夸大。
> ```

---

## Section 2 · 验收 checkpoint-01(ADP,5 min)

```bash
cd /Users/admin/codes/autodev_pipe
test -f docs/dogfood/v4-checkpoint-01.md && echo "FILE OK"
wc -l docs/dogfood/v4-checkpoint-01.md       # 应 100-300 行
grep -c "^## " docs/dogfood/v4-checkpoint-01.md  # 应 ≥6(理想 8 节)
grep -ciE "placeholder|TODO|TBD|<.*>" docs/dogfood/v4-checkpoint-01.md
# 期望:0 命中(若有 placeholder → 不通过,回 §1 让 skill 重跑或手补)
```

若 4 项验收任一 FAIL → 不要 commit,先修。

---

## Section 3 · commit checkpoint-01(ADP,5 min)

```bash
cd /Users/admin/codes/autodev_pipe
git status --untracked-files=all  # 确认只有 v4-checkpoint-01.md modified/new
git add docs/dogfood/v4-checkpoint-01.md

# 一行总结写 checkpoint-01 核心结论(实测数据,不写期望)
# 例:"docs(v4-dogfood): checkpoint-01 (4-week mark) — 0 真自用项目, AC5 1/3, D5 概率中-低"

git commit -m "$(cat <<'EOF'
docs(v4-dogfood): checkpoint-01 (4-week mark) — <一行实测总结>

AC4 进度: <实测>
AC5 兑现: 1/3 (2026-05-06 → 2026-06-03)
D5 12 周硬条件预判: <实测概率>

详情见 docs/dogfood/v4-checkpoint-01.md
EOF
)"
```

**不 push**(等 operator 显式确认)。记录此 commit hash,§4 要用。

---

## Section 4 · 切回 IDS 加索引(IDS,5 min)

回到 IDS 仓,在 `discussion/006/forge/v1/next-steps.md` v3 修订记录后追加新节:

```markdown
### W3 进度(2026-06-03 ±)

- ADP V4 checkpoint-01 已写入并 commit:`<ADP commit hash>`
- 路径:`/Users/admin/codes/autodev_pipe/docs/dogfood/v4-checkpoint-01.md`
- 核心结论(供 W4 决策读):
  - AC4 真自用项目候选数:<实测>
  - AC5 兑现度:1/3
  - D5 12 周硬条件预判:<高/中/低>
  - 路径 2 gap 取舍输入:<3 个 gap 各自的 4 周实测>
- W4 决策依据:本 checkpoint-01 + IDS framework/ADP-AUDIT-2026-05-08.md §9 4 条 drift,合并写 SHARED-CONTRACT v2.0 + gap A/B/C 决策
```

commit:

```bash
cd /Users/admin/codes/ideababy_stroller
git add discussion/006/forge/v1/next-steps.md
git commit -m "docs(006-forge-v1): next-steps W3 索引 — V4 checkpoint-01 commit hash 与核心结论"
```

---

## Section 5 · W3 → W4 关口(IDS,1h · 不在本 playbook 范围)

W3 收尾即进 W4。基于:
- ADP `docs/dogfood/v4-checkpoint-01.md`(本次产出)
- IDS `framework/ADP-AUDIT-2026-05-08.md` §9(W0 跨仓 dogfood drift)

合并做 W4 决策(playbook 原 Step 6),3 个待决项:
1. **路径 2 gap 取舍**:A(全做)/ B(P0 = gap-1+2)/ C(只 gap-1)
2. **SHARED-CONTRACT v2.0 重写**:是否触发(取决于 §9 DRIFT-1 严重性 + checkpoint-01 是否暴露同向问题)
3. **D5 12 周硬条件**:V4 是否仍可行,还是进 ADR 0009 复审降级 / 终止

具体决策方案在 W4 时再展开,本 playbook 不预设。

---

## 关键不变量(整个 playbook 通用)

- **诚实优于夸大**:V4 frozen 4 周 0 真自用项目是事实,checkpoint-01 必须如实记录,不能用 V4 自审 4 round commit 充数
- **不动 ADP 工具链**:本 playbook 只跑 retrospective skill 读数据 + 写一份 markdown,不改 ADP 任何代码 / spec / hook
- **不 push 远程**:所有 commit 留本地,等 operator 显式确认
- **失败可重跑**:retrospective skill 输出 placeholder → 删 v4-checkpoint-01.md → 重跑 §1
- **保持 8 节结构**:即使 4 周数据稀疏,8 节标题仍要全在,内容写"unknown" 或 "not yet applicable" 而非删除

---

## 时间表(回到 W3 当天)

| 顺序 | 在哪 | 动作 | 时间 |
|---|---|---|---|
| §0 | IDS | 跑 4 项 grep 自查 | 5 min |
| §1 | ADP | 切 ADP + 跑 retrospective skill + 粘贴 prompt | 30-60 min |
| §2 | ADP | 4 项验收 | 5 min |
| §3 | ADP | commit checkpoint-01(不 push) | 5 min |
| §4 | IDS | next-steps.md 加 W3 索引 + commit | 5 min |
| §5 | IDS | 进 W4(不在本 playbook 范围) | — |

**总计**:50 min - 1.5h(乐观) ~ 4-5h(若 retrospective skill 多次重跑)

---

## 失败模式预案

| 失败模式 | 触发条件 | 处置 |
|---|---|---|
| retrospective skill 不存在或损坏 | `.claude/skills/retrospective/` 缺失 | 跳过 skill,operator 直接按 8 节模板手写(估时翻倍 1-2h) |
| skill 跑出 placeholder | grep 验收命中 placeholder/TODO | 删 v4-checkpoint-01.md → 重跑 §1,prompt 加"严格禁止 placeholder"指令 |
| 4 周内 ADP 工具链有破坏性变更 | git log 显示 V4 spec frozen 后又被 review/unfrozen | 仍写 checkpoint-01,但 §7 单列"V4 spec 在 W2/W3 期间被 unfrozen 的 reason" |
| operator 在 4 周内真启动了真自用项目 | §0 grep 4 项 ≥1 个非空 | 走 playbook L297-301 standard 路径,按真数据写 §1 / §3 / §4 / §5 / §6 |
| AC5 错过 6/3 时间窗 | 操作日 > 6/15 | 不放弃;改 frontmatter horizon 为实际写入日,§2 标"AC5 延期 N 天 — reason: <原因>" |

---

## Changelog

- 2026-05-09 v1: 初稿。基于 2026-05-09 实测 ADP 状态(V4 frozen 4 周 0 真自用项目,friction-log MISSING)适配 playbook-4-weeks.md Step 5 为可执行 5 节流程
