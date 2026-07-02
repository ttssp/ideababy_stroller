# Forge Stage · 006 · v6 · "跨机器可移植性加固 · mac 环境形态硬编码根治"

**Generated**: 2026-07-02T13:10:00Z
**Source**: forge run v6 with X = 5 标的（backlog 快照 + IDS 双现场 + XenoDev 三 SKILL + KG-29 追认 + X#5 evidence）, Y = 跨机器可移植性 + 工程纪律, Z = 对标 SOTA（跨平台工具链可移植性）, W = decision-list + refactor-plan
**Convergence mode**: strong-converge
**Rounds completed**: P1 (both), P2 (both), P3R1 (both), P3R2 (both)
**Searches run**: 9 across 8 distinct sources（12-factor / git rev-parse / SemVer+coreutils version-sort / uv indexes+PEP592 / OWASP path-traversal / XDG Base Dir / ast-grep+semgrep / pre-commit）
**Moderator injections honored**: none
**Convergence outcome**: converged（单一 verdict · 双方 P3R2 0 实质分歧签字）

---

## How to read this

本文档是 v6 forge run 的收尾产物。**这是"轻收尾框架修"（K binding⑤），不是大重构** —— 目标是把 009-pForge M1 在 linux 新机首跑暴露的 5 条同根缺陷系统性修掉，可执行优先。

- W 只勾了 **decision-list + refactor-plan**，本文档就只产这两块（无 next-PRD / dev-plan / long-essay）。
- verdict 是**单一收敛**（strong-converge），骨架直接取自 P3R2-Opus §2 的 6 类分层修法矩阵。
- refactor-plan 每条都标清**落哪个仓（IDS / XenoDev）+ 双仓落地顺序 + SHA 复验**，可直接指导落地。
- 读完你应能直接进 §"Decision menu" 选 [A] 全落 / [B] 局部先落 P0 / [C] 跑 v7 / [P] park。

## Verdict

009-pForge M1 在 linux 新机（`/home/ys/`）首跑 IDS→XenoDev 全链，一天暴露 KG-26/27/28/29/30 五条框架缺陷。**它们不是 5 个孤立 bug，是同一根因的 5 个切面 = 框架把某台 mac（`/Users/admin/`）的环境形态当 constant 塞进模板 / SKILL / 示例字面**（违 12-factor §III：会随机器变的量 = config，不进 code）。

修法 = **按硬编码性质分 6 类外置 + 加一个防漂移守卫 + 追认 KG-29**，不是逐处补丁。硬约束一条：**"修可移植性的手段本身必须先验可移植"** —— mac `sort -V`（GNU vs BSD）是这条原则的元级复现，故版本排序落成 3 级 capability resolver 而非硬选一个工具。

单一 verdict 回应 K 的第一性原理：**会跨机器变的环境事实（路径 / 版本 / index / 目录形态 / 工具能力）该外置到环境或运行期推断，不该硬编码进框架字面**。KG-29 已 operator 直接决策修（IDS `7164381`），追认审计通过、安全、不推翻 009 已 ship 链。

## Evidence map

| 结论 | 来源 | 引用 | 反对证据 |
|---|---|---|---|
| 5 条同根 = config-as-constant 反模式 | P1-Opus §1 + P1-GPT §1 + P2-Opus §1 row1（12factor.net/config） | "把'我这台机器现在长这样'固化进了框架" | - 双方 P1 + SOTA 三方同判 |
| KG-26 同仓路径 → 运行期 `rev-parse`/`realpath` | P3R2-Opus §2 row1 + P2-Opus §1 row2（git-tower） | "source_repo 该运行期 rev-parse 推断" | - |
| KG-26 跨仓 build_repo → `$XENODEV_REPO`→sibling→fail-closed（**不 rev-parse**） | P3R1-GPT §1 挑战 + P3R2-Opus §1 精修1 | "build_repo 是另一个仓，不能靠 IDS rev-parse 推出" | ⚠ P3R1-Opus 原骨架把 build_repo 误归 rev-parse，被 GPT 挑对（见 §underweight） |
| KG-27 版本号 → 单点 glob + resolver，绝不散写 1.0.3 | P3R2-Opus §2 row4 + P2-Opus §1 row3 | "spec-writer 已用 glob+sort -V，推广不发明" | - |
| KG-27 命令方言 → capability probe + 3 级 resolver（拒 gsort） | P3R1-GPT §1 补类别 + P3R2-Opus §1 精修2 | "sort -V 是 GNU 能力，修 KG-27 会种下新 KG-27" | ⚠ mac `sort -V` 实测未跑（见 §underweight v0.2 note 1） |
| KG-28 → `UV_DEFAULT_INDEX`（不进 lock）+ `--frozen`（不去 --locked） | P2-Opus §1 row4 + P2-GPT §1 row5（uv#9053/PEP592） | "去 --locked 是次优，index 走环境变量更干净" | ⚠ backlog KG-28 原处置"去 --locked"被 SOTA 修正 |
| KG-29 charset 放宽 → keep（追认 · 安全） | P3R2-Opus §2 追认段 + P2-GPT §1 row6（OWASP） | "四层 containment 未动，负例全拒" | - 双方独立实测 `009-pv0.2`/`008/../../etc` 全 FAIL |
| KG-30 → verifier 降级"磁盘可读+red/green 序列即 PASS" | P3R2-Opus §3 + P3R1-GPT §3 | "随 commit 是手段非目的，mirror 子项目下逼出 .gitignore 冲突" | - |
| 防漂移守卫（新增） `check-no-hardcoded-env.sh` | P1-Opus §2 + P2-Opus §1 row5（ast-grep/semgrep） | "5 条同时存在 = 没守卫拦硬编码进来" | - 双方判最有价值新增 |

（表以最 load-bearing 的 9 条结论为限；X#5 的 KG-31 gen-handback template 字面量归入第 1 类"同仓路径"射程，见 refactor-plan 组 A）

## Intake recap

### X · 审阅标的（5 槽）
- **槽1 · backlog 快照**（核心）：`discussion/006/dogfood-backlog-20260702.md` KG-26..30 五条全文 + KG-31（X#5 同族实例）
- **槽2 · KG-26 现场（IDS 侧）**：`.claude/commands/plan-start.md` HANDOFF 模板 + `framework/SHARED-CONTRACT.md` §6.2（均写死 `/Users/admin/codes/XenoDev`）
- **槽3 · KG-27/28/30 现场（XenoDev 三 SKILL · 最重点）**：spec-writer / codex-review / parallel-builder SKILL（mac base 路径 + 钉死 `1.0.3` + 无 env preflight + red-green log 相对路径）
- **槽4 · KG-29 已落地修复（追认审计标的）**：IDS commit `7164381` diff + 009 两包 6 约束全 PASS
- **槽5 · KG-26 同族未入册实例（evidence）**：`gen-handback.sh` template 的 `to_source_repo`/`workspace.source_repo` mac 字面量（= KG-31）+ validator 相对路径 papercut

### Y · 审阅视角（2）
- **跨机器可移植性（核心）** — 环境假设怎么从硬编码变推断，mac↔linux 两机都能跑；修法有外部锚不自创
- **工程纪律** — SSOT 三层同步纪律（条款 / bootstrap-kit / XenoDev mirror）；修法可测性；防再漂移机制

### Z · 参照系
- mode: 对标 SOTA（聚焦跨平台工具链可移植性）
- 用户外部材料: 无（X 的 5 槽 = 全部一手材料）

### W · 产出形态（2）
- **decision-list** ✅ → §"Decision matrix"
- **refactor-plan** ✅ → §"Refactor plan"
- （verdict-only / next-PRD / next-dev-plan / free-essay 未勾 → 本文档不产）

### K · 用户判准（binding 5 条）
> 5 条 backlog 同一根因 = 框架把某台 mac 环境形态硬编码成默认（绝对路径 / codex 版本号钉死 1.0.3 / env 工具链假设 uv 就位 / 目录结构假设仓根 tests/）。盯死：① KG-26/27 系统性修法（环境假设住哪层 · 一次清扫 + 防再漂移 · 版本绝不写死）② KG-29 追认审计（放宽 charset 有无安全隐患 · 不推翻已跑通的解阻）③ KG-28 env bootstrap ④ KG-30 red-green log 落点 ⑤ 修法射程覆盖 evidence（KG-31 同族别漏）。
>
> **binding**：① 框架级变更只走本 forge；② 守 SSOT 三层同步纪律，不留半同步态；③ 别推翻 009 已 ship 链；④ 自用单人双机（mac+linux）非通用多平台发行，不做 Windows/容器/CI 矩阵过度工程；⑤ 轻收尾，可执行优先，decision-list + refactor-plan 直接指导落地，不要长 essay。

### 收敛模式
strong-converge → 单一 verdict + 残余分歧降级 v0.2 note

---

## Decision matrix（W#1 · 逐 KG 决议）

> 4 列决议。每行可在 §"Evidence map" 溯源。"来源"列指向 backlog 具体 KG + round 具体位置。

| 类别 | KG / 项 | 硬编码性质 | 修法机制（选型） | 来源 | 优先级 |
|---|---|---|---|---|---|
| **调整** | KG-26 · IDS 同仓路径（source_repo/handback_target） | 跨机器绝对路径 | 运行期 `git rev-parse --show-toplevel`/`realpath`，模板不含字面量 | backlog KG-26 L648 + P3R2-Opus §2 row1 | **P0** |
| **调整** | KG-26 · 跨仓 build_repo（XenoDev 位置） | 跨仓绝对路径 | 优先级链 `$XENODEV_REPO`→sibling `../XenoDev`(test -d)→fail-closed（**不 rev-parse**） | P3R1-GPT §1 + P3R2-Opus §1 精修1 | **P0** |
| **调整** | KG-31 · gen-handback template `to_source_repo`/`workspace.source_repo` | 跨机器绝对路径（X#5 evidence） | template L6/L8 改 `{{SOURCE_REPO}}` 占位 + 从 `$IDS_ROOT` 或 HANDOFF SSOT 喂值 | backlog KG-31 L689 + P2-Opus §2 | **P1** |
| **调整** | KG-27 · codex 版本号 `1.0.3`（散写 8+ 处） | 工具版本号（最会腐烂） | 单点 glob `codex/*/scripts` + 版本 resolver，**绝不散写版本号**（spec-writer 已用，推广） | backlog KG-27 L656 + P2-Opus §1 row3 | **P0** |
| **调整** | KG-27 · codex base 目录 `/Users/admin/.claude` | base 目录 | `${HOME}/.claude/...` 或 `$CODEX_HOME`，不写死用户名 | backlog KG-27 L662 + P3R2-Opus §2（base 段） | **P0** |
| **调整** | KG-28 · pypi mirror + yanked dep | index/env config | `UV_DEFAULT_INDEX`（不进 lock）+ yanked-dep 用 `--frozen`（**不去 --locked**） | backlog KG-28 L664 + P2-Opus §1 row4 | **P1** |
| **调整** | KG-30 · red-green log 落点 | 仓内相对路径 | §4.4 verifier 降级"磁盘可读 + red/green 序列即 PASS"；log 锚 XenoDev 仓根 | backlog KG-30 L681 + P3R2-Opus §3 | **P2** |
| **保留（追认 keep）** | KG-29 · charset 正则放宽 `-p[A-Z]`→`-p[A-Z][a-zA-Z]*` | （已修 · 追认审计） | 保留不动。审计结论：安全（OWASP known-good + 四层 containment 未动 · 双方实测负例全拒）· 不推翻 009 已 ship | backlog KG-29 L672 + P3R2-Opus §2 追认段 | **P0**（补 mirror） |
| **新增** | 命令方言/工具能力 probe（`sort -V` 泛化 realpath/sed 等） | 工具行为方言 | capability probe + 3 级 resolver（sort -V→python3→受限 shell，拒 gsort） | P3R1-GPT §1 + P3R2-Opus §1 精修2 | **P0** |
| **新增** | 防漂移守卫 `check-no-hardcoded-env.sh` | （元问题 · 现无守卫） | grep 扫 `/Users/*`+`/home/*` 家目录 + 散写版本号 → 命中拒；IDS+XenoDev 各一份；轻量 pre-commit 不上重 CI | P1-Opus §2 + P2-Opus §1 row5 | **P1** |

**矩阵读法**：无一条要"删除"（没有该砍的功能）；无一条要"新建产品能力"（防漂移守卫 + 工具能力 probe 是新增的**工程守卫机制**，非产品功能）。主体是 8 条"调整"（系统性外置，非逐处补丁）+ 1 条"追认 keep"（KG-29）+ 2 条"新增守卫"。

---

## Refactor plan（W#2 · 按 6 类机制分组）

> 每组：哪些文件/哪些行 → 改成什么机制 → **落哪个仓 + 双仓落地顺序 + SHA 复验** → 可测验收。
> **落仓速查**：KG-26 + KG-31 落 **IDS**（部分含 bootstrap-kit mirror 件）· KG-27/28/30 落 **XenoDev**（自派生 SKILL，不走 IDS 三层 mirror）· KG-29 已落 IDS 待 XenoDev mirror。

### 组 A · 同仓 + 跨仓路径推断（KG-26 + KG-31）· 落 IDS

**改哪里**：
- `.claude/commands/plan-start.md`：HANDOFF 模板 §workspace.build_repo + §1 `cd` 指令（写死 `/Users/admin/codes/XenoDev`）
- `framework/SHARED-CONTRACT.md` §6.2（line ~635-651）：workspace schema 4 字段示例表 + YAML 块（全 mac 路径）
- `lib/handback-validator/templates/handback.template.md` L6/L8：`to_source_repo`/`workspace.source_repo` mac 字面量（KG-31）
- `lib/handback-validator/gen-handback.sh` L424 附近：IDS_ROOT env 化只喂了 handback_target，漏了 template 两字段

**改成什么机制**：
- **同仓路径**（source_repo / handback_target）→ plan-start 实装动作用 `git rev-parse --show-toplevel` / `realpath` 动态填；模板/示例不含字面量（或显式标"示例路径，按本机实际填"）。
- **跨仓 build_repo**（XenoDev 位置）→ **优先级链**（不用 rev-parse，它给的是 IDS 仓根）：
  ```
  build_repo 解析 =
    1. 显式 $XENODEV_REPO 环境变量（若设，直接用）
    2. 否则 sibling heuristic: $(dirname $(source_repo))/XenoDev（test -d 验存在）
    3. 否则 fail-closed: 报错让 operator 显式填，不猜、不写死 mac 默认
  ```
- **KG-31 template** → L6/L8 改 `{{SOURCE_REPO}}` 占位 + gen-handback 从 `$IDS_ROOT`（或更优：从 HANDOFF `workspace.source_repo` SSOT，它本就有正确值）喂值；顺带审 template 有无其他未占位化路径字面量。

**双仓落地顺序 + SHA 复验**：全落 IDS。SHARED-CONTRACT §6.2 是三层 SSOT 的 ①条款层 → 改后须 `check-mirror-drift`（或等价）确认 bootstrap-kit ②实装层不漂；handback.template.md 在 bootstrap-kit 有上游 → 改上游 + XenoDev mirror sync，记双仓 SHA。

**可测验收**：
- 在 linux 机跑 `/plan-start <fork>`，产出 HANDOFF 的 `build_repo` = `/home/ys/codes/XenoDev`（非 mac），`cd` 指令可执行。
- `unset $XENODEV_REPO` + sibling 存在 → 走第 2 级取到正确路径；sibling 不存在 → fail-closed 报错（非静默写 mac）。
- gen-handback 产包 frontmatter `to_source_repo`/`workspace.source_repo` = 真实 IDS 路径（linux 上验，对照 009 两包的错误元数据）。

### 组 B · 工具版本号单点解析（KG-27 版本段）· 落 XenoDev

**改哪里**：
- `spec-writer/SKILL.md` §3.1 L96：`find /Users/admin/.claude/plugins/.../codex/*/scripts/... | sort -V | tail -1`（**find 逻辑对**，只 base 路径 mac）
- `parallel-builder/SKILL.md` L17：mac + 钉死 `1.0.3`
- `codex-review/SKILL.md` L16/58/122/138/152/156/357/391/548 等 8+ 处：mac + 多处钉死 `1.0.3`

**改成什么机制**：
- 版本号**绝不散写** → 全部改为单点 glob `codex/*/scripts/codex-companion.mjs` + **版本 resolver**（见组 F）取最新。spec-writer 的 `find ... | sort -V | tail -1` 范式是**正确起点**，推广到 codex-review / parallel-builder 所有 `1.0.3` 写死处（本机是 1.0.4，1.0.3 目录已不存在）。

**双仓落地顺序 + SHA 复验**：纯落 XenoDev（三 SKILL 是 XenoDev 自派生，**不走 IDS 三层 mirror**）。forge 在 IDS 决议后，下发 XenoDev 半边 brief 执行；记 XenoDev commit SHA。

**可测验收**：
- 三 SKILL 全仓 `grep -rn '1\.0\.3'` → 0 命中（版本号绝迹）。
- 在 linux 机跑 codex resolver 取到 `1.0.4`（`node /home/ys/.claude/plugins/.../codex/1.0.4/scripts/codex-companion.mjs` 可加载）；codex 下次升 1.0.5 时 resolver 自动跟随，无腐烂行。

### 组 C · base 目录 env 化（KG-27 base 段）· 落 XenoDev

**改哪里**：三 SKILL 里 `/Users/admin/.claude/plugins/...` 的 base 前缀。

**改成什么机制**：`${HOME}/.claude/plugins/...` 或 `$CODEX_HOME`，不写死用户名 `admin`。（XDG Base Directory 锚。）

**双仓落地顺序 + SHA 复验**：随组 B 一起落 XenoDev（同批 codex 路径修法），记同一 commit。

**可测验收**：三 SKILL `grep -rn '/Users/admin'` + `grep -rn '/home/ys'` → 0 命中；`echo ${HOME}/.claude/...` 在 mac 和 linux 各展开到本机真实 base。

### 组 D · index/env config 外置（KG-28）· 落 XenoDev

**改哪里**：
- `parallel-builder/SKILL.md` §0/§2：TDD 命令全 `uv run ...`，无 env preflight
- task `## Verification` 块：全 `uv run alembic/pytest`（假设 env 天然就位）

**改成什么机制**（SOTA 修正 backlog 原"去 --locked"处置）：
- §0 加 **env preflight**：探 `uv` 在否 / `.venv` 在否 / index 可达否 / lock 是否 stale。
- mirror/index → 走 **`UV_DEFAULT_INDEX`** 环境变量（**不污染 lockfile** —— index 是 config，出环境）。
- yanked-dep（如 `anyio==4.6.2` 被撤）→ 用 **`uv sync --frozen`**（装 lock as-is，不校 pyproject），**不用去 --locked**（后者会让 CI 能重写 lock，破可复现）。
- 文档化"新机首次 build 前跑 env 建设"（装 uv + 配可达 index + uv sync）。

**双仓落地顺序 + SHA 复验**：落 XenoDev（parallel-builder SKILL + task Verification 派生规则）。记 XenoDev commit。

**可测验收**：
- linux 新机在无 uv / pypi 被墙场景下：preflight 报出"缺 uv / index 不可达"（非静默卡死 2h19m，对照 009 T001 实况）。
- 设 `UV_DEFAULT_INDEX=https://mirrors.aliyun.com/pypi/simple/` → `uv sync --frozen` 装齐 224 包（对照 009 T001 真值）；`uv.lock` 无 mirror 污染。

### 组 E · 仓内 log 落点 + verifier 降级（KG-30）· 落 XenoDev

**改哪里**：
- `parallel-builder/SKILL.md` §2.1/§2.2/§2.4：`tee -a tests/red-green-log/<TID>.log`（相对路径，mirror 子项目下落子树被 .gitignore 挡）
- §4.4 verifier：期望"red-green log 随 commit / diff 边界含 tests/red-green-log/"

**改成什么机制**（残留收敛：降级"留证即可"，见 P3R2-Opus §3）：
- §4.4 verifier **降级判据**：改判"log 在**磁盘可读** + 含 **red/green 序列**（≥1 [red]rc≠0 + 末尾 [green]rc=0）"即 PASS。**不强制随 commit**。
- log 落点锚 XenoDev **仓根** `rev-parse --show-toplevel`（不随 task cwd / 子树），若 operator 坚持要入 git 则由仓根路径承载。

**双仓落地顺序 + SHA 复验**：落 XenoDev。记 commit。

**可测验收**：mirror 进来的 004-pB 子项目 build（file_domain 全在 `projects/004-pB/**`）时，§4.4 verifier PASS（log 在磁盘可读 + red/green 序列全），不再因 `git check-ignore` 命中而恒失败（对照 009 T001/T002 静默吞坑实况）。

### 组 F · 命令方言/工具能力 resolver（新增 · KG-27 版本排序泛化）· 落 XenoDev

**为什么新增**：`sort -V` 是 GNU coreutils 能力，mac 默认 BSD `sort` 历史不支持 `-V`。若组 B 推广 `sort -V` 不核 mac 便携性，**修 KG-27 会种下一个 KG-27 形状的新坑**。这是 v6 根因的元级复现。

**改成什么机制**（3 级 resolver · 单点 · 见 P3R2-Opus §1 精修2）：
```
版本排序 resolver（单点）:
  1. 探测: printf '1.0.3\n1.0.10\n' | sort -V 成功且顺序对 → 用 sort -V
  2. 否则 python3 fallback: 切 codex/<ver>/ 的 <ver> 按 . 分段转 int 排序
  3. 否则受限 shell fallback: sort -t. -k1,1n -k2,2n -k3,3n（仅声明支持 X.Y.Z 目录形态）
```
- **拒 `gsort`**：那只是把可移植性问题转成"装没装 coreutils"的新假设。
- 同源泛化：`realpath -m`、`sed -i` 语法差异同理走 capability probe。
- spec-writer SKILL L94 注释"macOS 默认 sort 支持 -V" **应删/改**（未证实的机器假设，Codex 未找到一手依据）。

**双仓落地顺序 + SHA 复验**：落 XenoDev（resolver 作 SKILL 内的单点函数被组 B 调用）。记 commit。

**可测验收**：
- linux 机：`sort -V` 探测成功 → 第 1 级，取到 1.0.4（本机 `sort (GNU coreutils) 9.4` 实证已通）。
- ⚠ **mac `sort -V` 实测待跑**（v0.2 note 1）：operator 在 mac 跑 `printf '1.0.3\n1.0.10\n' | sort -V`；若 BSD sort 不支持 → resolver 自动落第 2 级 python3（无需改代码）。
- 无 python3 环境 → 第 3 级受限 shell 取到正确顺序（仅 X.Y.Z 形态）。

### 组 G · 防漂移守卫 + KG-29 mirror 补同步（新增 + 追认）

**防漂移守卫 `check-no-hardcoded-env.sh`（新增）**：
- **机制**：grep 扫任何用户绝对家目录（`/Users/*`、`/home/*`）+ 散写版本号模式（如 `1\.0\.[0-9]` 字面）→ 命中即拒。
- **放哪**：**IDS + XenoDev 各一份**（两仓都会引入硬编码：KG-26/31 在 IDS，KG-27/28/30 在 XenoDev）。
- **轻量**：pre-commit hook / 手动 gate，**不上重 CI**（K binding④ 单人双机非发行）。
- **自身可移植**：守卫脚本用 `rev-parse --show-toplevel` 定位 + capability probe，不重蹈硬编码。
- **落仓**：IDS 一份 + XenoDev 一份，各记 commit。
- **验收**：把一个含 `/Users/admin` 的测试文件 stage → pre-commit 拒；守卫脚本自身 `grep '/Users\|/home/ys'` 只命中它的 pattern 定义（不误伤自己的逻辑）。

**KG-29 追认 keep + 补 mirror（P0）**：
- **审计结论**：charset 放宽 `-p[A-Z]`→`-p[A-Z][a-zA-Z]*` + 对齐 `-v` 段（IDS `7164381`），**安全 · 保留不动**。OWASP known-good charset + 四层 containment（charset forbidden-chars / basename / realpath / hard-fail）一字未动；双方独立实测 `009-pForge` PASS · `006a-pM-v0.2` PASS · `009-pv0.2` FAIL · `008/../../etc` 四层全拒。**009 T001/T002 已 ship 依赖它，不推翻。**
- **唯一动作**：补 XenoDev mirror 同步（现半同步态：IDS 已修 commit `ff5b7e1`，XenoDev mirror 靠 operator 手动 apply patch）。这正是下面"半同步窗口"的活样本。
- **验收**：IDS check-6 + SHARED-CONTRACT §6.2.1 + event-schema.json 三处正则一致；XenoDev mirror 的 `check-6-id-charset-and-final-path.sh` 与 IDS 字节一致（记双仓 SHA 复验）。

**SSOT 半同步窗口收口（工程纪律 · 覆盖所有跨仓修法）**：
- 跨仓 mirror 无法字节级同时落（非原子）→ **不追求消除窗口**，追求**窗口可见 + 有 checklist 收口**。
- 产出一个同步 checklist / 脚本（如 hand-off brief 固定"两仓落地顺序 + SHA 复验"步骤，或 `sync-mirror-to-xenodev.sh`），把半同步从"靠 operator 记忆"变"有据可循 + 可验"。KG-29 现状纳入此 checklist 首个用例。

---

## What this menu underweights（强制自批判）

- **双模型回声室（最该警惕）**：双方 P1 5/5 评分一致、P2 SOTA 锚点几乎逐条相同、P3R2 0 分歧签字。收敛度极高**可能掩盖共享盲点**。具体可疑处：**防漂移 grep-gate 自身够不够严** —— 它扫 `/Users/*`/`/home/*` + 版本号字面，但对**别的形态**的机器假设（如 `sed -i ''` 的 BSD 空串参数、硬编码端口、假设某 shell）无覆盖；双方都没质疑 grep pattern 的完备性（backlog KG-4 恰是"grep pattern 与实际输出漂移"的前例，说明 grep-gate 本身可能重蹈）。verdict 采纳它是因"便宜 + 有 SOTA 背书 + 双机非发行不上重 CI"，但它是**下限守卫非完备守卫**。
- **3 条 v0.2 note（非阻塞残留 · 来自 P3R2-Opus §4）**：
  1. **mac `sort -V` 实测待跑** — 版本 resolver 第 1 级在 mac 的真实结果待 operator 在 mac 跑；若不支持自动落 python3 fallback（resolver 已设计好，无需改代码）。这条不跑，"修可移植性的手段本身可移植"就只在 linux 侧证实了一半。
  2. **`$XENODEV_REPO` 持久化坑** — build_repo 优先级链第 1 级依赖此 env，而 env 指针持久化本身是坑（项目已有 KG-env-pointer 前例）。fail-closed（第 3 级）兜底，但 operator 该在双机 shell profile 设 `$XENODEV_REPO`，否则每次 sibling heuristic 兜。
  3. **KG-29 半同步窗口现状** — IDS 已修（`7164381`/`ff5b7e1`），XenoDev mirror 靠手动 apply patch，是半同步窗口活样本，须 §组G 的同步 checklist 覆盖。
- **Y 视角未含"安全"**：Y 只选了可移植性 + 工程纪律。但 KG-29 追认走了 OWASP path-traversal 视角（P2-GPT §1 row6），已覆盖该条的安全面。**其余修法的安全面未系统扫** —— 如组 D 的 `UV_DEFAULT_INDEX` 指向第三方 mirror（aliyun）是否引入供应链信任问题，本轮未评（双机自用场景风险低，但值得后续 attention）。
- **X 标的覆盖局限**：backlog 只审 KG-26..31 段，KG-1..25 明确不重审（forge-config inheritance）。若 KG-1..25 里有与本批同根的可移植性坑（如 KG-13 macOS Bash 3.2 mapfile / KG-6 zsh PATH / KG-14 mitmproxy Homebrew），本 verdict 的防漂移守卫**未把它们纳入 pattern 设计** —— 这些是"工具能力方言"同族，组 F 的 capability probe 思路可延伸覆盖，但本轮射程只锁 KG-26..31。
- **forge versioning 提示**：以下新信息进入会触发 v7 —— (a) mac `sort -V` 实测**不支持且 python3 fallback 也出问题**；(b) 防漂移 grep-gate 上线后**仍漏进新硬编码**（证明 pattern 不完备）；(c) `$XENODEV_REPO` 持久化在双机 shell profile 反复丢失成为高频痛点；(d) 出现 KG-26..31 之外的**新形态**机器假设（非路径/版本/index/目录/工具能力五类）。

## Decision menu（for human）

### [A] 接受 verdict · 落地全部改动（双仓）
```
落仓顺序（守 SSOT 三层同步 · binding②）：
  IDS 侧（先）：
    1. 组 A — plan-start.md + SHARED-CONTRACT §6.2 + handback.template.md + gen-handback（KG-26/31）
       → 改 §6.2 条款后 check bootstrap-kit 不漂
    2. 组 G — check-no-hardcoded-env.sh（IDS 份）+ KG-29 三处正则复核
  XenoDev 侧（后 · 下发半边 brief）：
    3. 组 B+C+F — 三 SKILL codex 路径 + base 目录 + 版本 resolver（KG-27）· 同批
    4. 组 D — parallel-builder env preflight + UV_DEFAULT_INDEX（KG-28）
    5. 组 E — red-green log verifier 降级（KG-30）
    6. 组 G — check-no-hardcoded-env.sh（XenoDev 份）+ KG-29 mirror sync（补 ff5b7e1 半同步）
  每步记双仓 commit SHA · 半同步窗口用组 G 的同步 checklist 收口
```
⚠ 框架级变更**只走本 forge 决议后落地**，不在 XenoDev 当场另改（binding①）。

### [B] 局部接受 · 先落 P0（**推荐起点**）
可执行优先，先止血最急、最会持续腐烂的：
- ✅ 先落：
  - **组 B+C+F（KG-27）** — 版本号钉死 `1.0.3` 每次 codex 升版本都腐烂，**最急**；且 resolver + base env 化一批落 XenoDev
  - **组 G · KG-29 mirror sync** — 补掉现存半同步窗口（IDS 已修 XenoDev 未 mirror），风险最低收益明确
  - **组 A（KG-26 + KG-31）** — 路径硬编码影响每次 `/plan-start` 产包，落 IDS
- ⏸ 挂起（等条件）：
  - **组 F mac `sort -V` 第 1 级验收** — 等 operator 在 mac 实测（v0.2 note 1）；linux 侧已通，不阻塞落地，只挂"mac 侧确认"
  - **组 D（KG-28）** — env preflight 影响面大，可在下个新机 build 前落
- ❌ 暂不做（本轮不做但非拒绝）：
  - 组 E（KG-30）verifier 降级 — 优先级 P2，不阻断 ship（log 磁盘可审计），可最后落
```
理由：KG-27 版本号是唯一"同机器升版本即腐烂"的一类（比路径更急）；
KG-29 补 mirror 消半同步窗口零风险；KG-26 影响每次产包。三者先落即覆盖 P0。
```

### [C] 跑 forge v7（说明需要补什么）
```
/expert-forge 006
# Phase 0 intake 时调整 X/Y/Z/W/K；旧 v6 整目录保留作历史参考
```
适用触发（见 §underweight forge versioning）：mac `sort -V` 实测失败且 fallback 也崩 / 防漂移 gate 上线仍漏新硬编码 / 出现五类之外的新形态机器假设。

### [P] Park
```
/park 006
```
保留所有 v6 forge 产物，标记暂停。复活时不重做本层收敛。

### [Z] Abandon
不适用 —— 本轮是框架加固收尾（非产品 idea 存废判断），无 abandon 语义。5 条缺陷是已 ship 框架的可移植性债，只有"修 / 缓修"，无"放弃这个 idea"。

---

## Forge log
- v6: 2026-07-02 — verdict: "5 条同根 = mac 环境形态硬编码成 constant；按 6 类性质分层外置（路径推断/版本 resolver/index env 化/log 降级/工具能力 probe/base env）+ 防漂移守卫 + KG-29 追认 keep；修可移植性的手段本身须先验可移植（mac sort -V）"
- v5: 并发安全 · CONCERNS（KG-1 G3 approve-over-approve / KG-2 B-3 同秒碰撞 · 已 ship 留 dogfood 观测）
- v4: hand-back/mirror 机制固化（v4→v5 攒批真问题再 forge 模式）
- v3/v2/v1: XenoDev 跨仓分工 + build runtime 边界确立（forge v2 verdict = IDS 治理 · XenoDev 唯一 L4 build runtime）
