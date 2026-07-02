# Forge v6 · P3R1 · Opus 4.8 Max（联合收敛 · 第 1 轮）

**Phase**: 3R1（读双方 P2 + 收敛残留分歧 + 锁 verdict 骨架）
**Reviewer**: Opus 4.8 Max
**Read**: P1×2 + P2×2（全部）
**收敛状态自评**: 极高。双方 P1 5/5 评分一致,P2 SOTA 锚点 8 条几乎逐条相同,KG-28 修正双方**独立**得到同一结论。无实质对立。本轮主要做**固化 + 收 3 条残留 + 消化 Codex 的 1 条新 caveat**。

---

## §1 · 双方 P2 对齐盘点（收敛度确认）

| 维度 | Opus P2 | GPT P2 | 状态 |
|---|---|---|---|
| 根因命名 | config-as-constant 反模式（12-factor §III） | 同（12-Factor + XDG） | ✅ 一致 |
| KG-26 路径修法 | 运行期 `git rev-parse`/`realpath` 推断 | 跨机器路径用 env/生成时,仓内用运行时 repo-root | ✅ 一致（GPT 更细分了"跨机器 vs 仓内"两类路径） |
| KG-27 版本修法 | glob+`sort -V`(spec-writer 已用,推广) | 同 + **caveat: `sort -V` 是 GNU,mac 便携性要核** | ⚠ **GPT 补了关键 caveat（见 §3）** |
| KG-28 修法 | `UV_DEFAULT_INDEX` 环境变量 + `--frozen`,不去 --locked | 同（preflight + 受控 lock/sync,不无脑去 --locked） | ✅ 独立同结论 |
| KG-29 追认 | keep,安全（双方实测负例全拒） | keep,OWASP known-good+containment 支持 | ✅ 一致 |
| KG-30 log 落点 | 落仓根（`rev-parse --show-toplevel` 锚） | 同（绑 XenoDev 仓根,非 task cwd） | ✅ 一致 |
| 防漂移 | grep-gate,轻量够用 | pre-commit / grep,单人双机不必上重 CI | ✅ 一致 |

**结论**:strong-converge 已实质达成。verdict 骨架 = **环境假设分层住**（下 §2）。

---

## §2 · Verdict 骨架（锁定 · 三类硬编码分层修 + 一个防漂移守卫 + 一条追认）

> 这是 v6 单一 verdict 的核心结构,synthesizer 按此展开 decision-list + refactor-plan。

**根因一句话**:框架把某台 mac 的环境形态（路径/版本/index/目录）当 constant 塞进模板/SKILL/示例 —— 违 12-factor §III（会随机器变的量 = config,不进 code）。**修法 = 按硬编码的"性质"分层外置,不是逐处补丁。**

**分层修法矩阵**（每类一个机制 + SOTA 锚 + 命中 KG）:

| 硬编码性质 | 修法（机制） | SOTA 锚 | 命中 KG |
|---|---|---|---|
| **跨机器绝对路径**（repo 位置/build_repo/handback source） | **生成时推断**:`git rev-parse --show-toplevel` / `realpath`,模板/示例不含字面量 | 12-factor + git rev-parse | KG-26 + X#5 gen-handback template |
| **仓内/子项目相对路径**（red-green log 落点） | **运行时锚仓根**:`rev-parse --show-toplevel` 定 XenoDev 仓根,不随 task cwd/子树 | git rev-parse | KG-30 |
| **工具版本号**（codex 1.0.3） | **单一解析点 glob**:`codex/*/scripts/...` + `sort -V \| tail -1`,绝不散写版本号（spec-writer 已用,推广到 codex-review/parallel-builder） | SemVer + coreutils version-sort | KG-27 |
| **外部 index/env config**（pypi mirror） | **环境变量**:`UV_DEFAULT_INDEX`(不进 lockfile);yanked-dep 用 `--frozen`(不去 --locked) | 12-factor + uv docs + PEP 592 | KG-28 |
| **base 目录**（codex plugin cache `/Users/admin/.claude`） | **env / `$HOME`**:`${HOME}/.claude/...` 或 `$CODEX_HOME`,不写死用户名 | XDG Base Directory | KG-27 base 段 |

**加一个防漂移守卫（新增 · 双方判最有价值）**:
- `check-no-hardcoded-env.sh`:grep 扫 `/Users/admin` + `/home/ys`（任何用户绝对家目录）+ 散写版本号模式 → 命中即拒。
- **轻量**:pre-commit hook / 手动 gate,**不上重 CI**（K binding④ 单人双机非发行）。
- **自身可移植**:守卫脚本用 `rev-parse --show-toplevel` 定位,不重蹈硬编码。

**一条追认（keep · 不推翻）**:
- KG-29 charset 放宽 `-p[A-Z]`→`-p[A-Z][a-zA-Z]*` + 对齐 `-v` 段,**安全**:OWASP known-good charset + 四层 containment(charset/basename/realpath/hard-fail)未动,双方独立实测 `009-pv0.2`/`008/../../etc` 全被拒。**009 T001/T002 已 ship 依赖它,不推翻。**

---

## §3 · 消化 Codex 的关键 caveat（本轮最重要的新信息）

**GPT P2 补了一条我漏的、且直击要害的 caveat**:

> **KG-27 的修法(`sort -V`)本身可能引入一个新的 mac/linux 分歧** —— `sort -V` 是 **GNU coreutils** 能力,mac 默认 `sort`(BSD)历史上不支持 `-V`。若推广 glob+`sort -V` 而不核 mac 便携性,**修 KG-27 会种下一个 KG-27 形状的新坑**。

**我的处置(实测 + 判断)**:
- 本机(linux)`sort (GNU coreutils) 9.4`,`sort -V` 工作正常,spec-writer 范式跑通取到 `1.0.4`。**linux 侧无问题。**
- **mac 侧我无法在本 linux 机验证**。而且注意:spec-writer SKILL L94 的注释**自称**"macOS 默认 sort 支持 -V" —— 这个 claim **未经本轮核实**,可能是写 SKILL 时的假设(正是 v6 要根治的"想当然的机器假设")。
- → **进 verdict 作显式 open-item + 可执行验收**:推广 glob+`sort -V` 前,**必须在 mac 上实测 `printf '1.0.3\n1.0.10\n' \| sort -V`**;若 mac BSD sort 不支持,用便携替代(如 `sort -t. -k1,1n -k2,2n -k3,3n` 或显式装 GNU coreutils/`gsort`)。**这条不是理论洁癖 —— 它是 v6 根因的元级复现:连"修可移植性"的手段本身都得先验可移植。**

**这条 caveat 的分量**:它是本轮唯一的"新结构性洞"(非前轮精度迭代)。双方在它之后无新分歧。

---

## §4 · 残留 3 条的收敛结论（P2 §3 列的）

1. **SSOT 半同步窗口**（KG-29 现状 IDS 先落 XenoDev 后补 + shared-lib-drift）:
   - **收敛**:承认双仓 mirror 无法做到"字节级同时落"（跨仓非原子），但修法应**产出一个同步脚本/checklist**（如 `sync-mirror-to-xenodev.sh` 或 hand-off brief 里固定"两仓落地顺序 + SHA 复验"步骤），把半同步窗口从"靠 operator 记忆"变成"有据可循 + 可验"。不追求消除窗口(不可能),追求**窗口可见 + 收口有 checklist**。
2. **KG-30 log 是否必须随 commit**:
   - **收敛**:**降级为"留证即可,不强制随 commit"**。理由:log 的价值是审计留痕(磁盘可查即达成),"随 commit"是实现手段非目的;mirror 子项目下强求随 commit 反而逼出 .gitignore 冲突。§4.4 verifier 改判"log 在磁盘可读 + 含 red/green 序列"即 PASS。（若 operator 坚持要进 git,则 log 落仓根 `rev-parse` 路径 —— 但默认降级。）
3. **grep-gate 放哪**:
   - **收敛**:**两边各放一份**(IDS + XenoDev 各自 pre-commit),因两仓都可能引入硬编码(KG-26 在 IDS,KG-27/28/30 在 XenoDev)。守卫脚本自身用 `rev-parse` 定位,不硬编码。

---

## §5 · 给 synthesizer 的 W 草稿指引

- **decision-list**:5 条 KG + 1 防漂移新增 + 1 追认,按 §2 分层矩阵逐条填(保留/调整/删除/新增列)。KG-29 = keep（追认审计通过）。
- **refactor-plan**:按 §2 五类机制分组;每组列(哪些文件/哪些行 → 改成什么机制 → 双仓落地顺序 → 可测验收)。**必含 §3 的 mac `sort -V` 实测验收** + §4.1 的双仓同步 checklist。
- **残留 v0.2 note**:mac `sort -V` 实测结果(待 operator 在 mac 上跑);若不支持则便携替代选型。

**P3R1 自评**:strong-converge 实质达成,无对立 verdict。本轮实产 = 锁定"分层修法矩阵"骨架 + 消化 Codex 的 mac `sort -V` caveat（唯一新结构性洞,已实测 linux 侧 + 标 mac 待核）+ 收敛 3 条残留。P3R2 预计只需双方确认骨架 + 补 v0.2 note,无新分歧。字数约 1500。
