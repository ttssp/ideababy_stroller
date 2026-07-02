# Forge v6 · P3R2 · Opus 4.8 Max（联合收敛 · 第 2 轮 · 定稿）

**Phase**: 3R2（最后一轮 · 吸收 Codex 两条精修 · 确认 0 分歧 · 为 synthesizer 定稿 verdict）
**Reviewer**: Opus 4.8 Max
**Read**: 全部 8 份（P1×2 / P2×2 / P3R1×2）
**收敛状态**: **strong-converge 达成 · 0 实质分歧**。Codex P3R1 §4 明说无实质分歧,仅两条精修(均为改进非对立),本轮全部吸收。verdict 定稿。

---

## §1 · 吸收 Codex 的两条精修（both 改进 · 我认同并采纳）

### 精修 1：`build_repo` 推断要有优先级链,不能只 `rev-parse`（Codex 对,我 P3R1 有 bug）

**Codex 挑对了**:我 P3R1 §2 把 `build_repo`(XenoDev 位置)和 `source_repo`(IDS 位置)都归"生成时 `git rev-parse --show-toplevel` 推断" —— **这对 source_repo 对,对 build_repo 错**。`plan-start` 在 IDS 仓跑,`rev-parse --show-toplevel` 给的是 **IDS 仓根**,不是 XenoDev。XenoDev 是**另一个仓**,不能靠 IDS 的 rev-parse 推出来。

**采纳的修正（build_repo 专用优先级链)**:
```
build_repo 解析 =
  1. 显式 $XENODEV_REPO 环境变量（若设,直接用）
  2. 否则 sibling heuristic:$(dirname $(source_repo))/XenoDev（test -d 验存在）
  3. 否则 fail-closed:报错让 operator 显式填,不猜、不写死 mac 默认
```
→ 这比"一律 rev-parse"精确。**source_repo/handback_target 仍用 rev-parse/realpath（它们确在 IDS 仓内）;build_repo 走上面三级链。** 两类路径分开处理。

### 精修 2：新增"命令方言 / 工具能力假设"类别（Codex 的最佳贡献 · 元级洞察)

**Codex 把 mac `sort -V` 从"open-item"升成"矩阵第六类"—— 这是对的,且更深刻**:`sort -V`(GNU vs BSD)、`realpath -m`、`sed -i` 语法差异……这些不是路径值/版本号,是**工具行为方言**。它们与 v6 根因**同源**(想当然某台机器的工具行为),只是层级不同。**修法 = capability probe + fallback,不是硬选一个工具。**

**采纳 Codex 的 3 级 resolver（我认可,且认同它拒 `gsort` 的理由——那只是把问题转成"装没装 coreutils")**:
```
版本排序 resolver（单点）:
  1. 探测:printf '1.0.3\n1.0.10\n' | sort -V 成功且顺序对 → 用 sort -V
  2. 否则 python3 fallback:切 codex/<ver>/ 的 <ver> 按 . 分段转 int 排序
  3. 否则受限 shell fallback:sort -t. -k1,1n -k2,2n -k3,3n（仅声明支持 X.Y.Z 目录形态）
```
→ 既保留 spec-writer 已有 glob 思路,又不把 GNU/BSD 差异写成新假设。**这条把"修可移植性的手段本身可移植"落成可执行 resolver。**

---

## §2 · Verdict 定稿（单一 · strong-converge · 6 类分层 + 防漂移 + 追认）

**verdict 一句话**:009-pForge M1 在 linux 新机首跑暴露的 5 条框架缺陷,**同一根因 = 框架把某台 mac 的环境形态当 constant 塞进模板/SKILL/示例**(违 12-factor §III)。修法 = **按硬编码性质分 6 类外置 + 加防漂移守卫 + 追认 KG-29**,不是逐处补丁;且**"修可移植性的手段本身必须先验可移植"**(mac `sort -V` = 该原则的元级复现)。

**分层修法矩阵（定稿 · 6 类 · synthesizer 按此产 decision-list + refactor-plan)**:

| # | 硬编码性质 | 修法机制 | SOTA 锚 | 命中 |
|---|---|---|---|---|
| 1 | **同仓绝对路径**(source_repo/handback_target) | 运行期 `git rev-parse --show-toplevel`/`realpath`,模板不含字面量 | 12-factor + git rev-parse | KG-26 + X#5 gen-handback template |
| 2 | **跨仓路径**(build_repo = XenoDev) | 优先级链:`$XENODEV_REPO` → sibling `../XenoDev` → fail-closed（**不 rev-parse**,它是另一个仓） | 12-factor(config 出环境) | KG-26 |
| 3 | **仓内相对路径**(red-green log 落点) | 运行时锚 XenoDev 仓根(`rev-parse --show-toplevel`),不随 task cwd/子树 | git rev-parse | KG-30 |
| 4 | **工具版本号**(codex 1.0.3) | 单一解析点 glob `codex/*/scripts` + 版本 resolver(见 §1 精修2),**绝不散写版本号** | SemVer + coreutils | KG-27 |
| 5 | **index/env config**(pypi mirror) | 环境变量 `UV_DEFAULT_INDEX`(不进 lock);yanked-dep 用 `--frozen`(不去 --locked) | 12-factor + uv + PEP 592 | KG-28 |
| 6 | **命令方言/工具能力**(sort -V、realpath -m 等) | capability probe + fallback(见 §1 精修2 resolver) | GNU/BSD 差异 + coreutils | KG-27 版本排序 + 泛化 |
| — | **base 目录**(codex plugin cache) | env/`$HOME`/XDG,不写死用户名 | XDG Base Directory | KG-27 base 段 |

**加：防漂移守卫（新增）**
- `check-no-hardcoded-env.sh`:grep 扫任何用户绝对家目录(`/Users/*`、`/home/*`)+ 散写版本号模式 → 命中拒。
- **IDS + XenoDev 各放一份**(两仓都会引入硬编码:KG-26 在 IDS,KG-27/28/30 在 XenoDev)。
- 轻量 pre-commit/手动 gate,**不上重 CI**(K binding④);守卫自身用 `rev-parse`+capability probe 定位,不重蹈硬编码。

**追认：KG-29 keep（审计通过）**
- charset 放宽 `-p[A-Z]`→`-p[A-Z][a-zA-Z]*` + 对齐 `-v` 段,**安全**:OWASP known-good charset + 四层 containment 未动,双方独立实测 `009-pForge`/`006a-pM-v0.2` PASS · `009-pv0.2`/`008/../../etc` 全被拒。**009 T001/T002 已 ship 依赖它,不推翻。**

---

## §3 · 3 条残留最终收敛（双方一致)

| 残留 | 定稿收敛 |
|---|---|
| SSOT 半同步窗口 | 不追求消除(跨仓非原子);产**同步 checklist/脚本 + SHA 复验 + outbox/handback 留证**,把窗口从"靠记忆"变"有据可循"。降为工程纪律要求。 |
| KG-30 log 随 commit | **降级"留证即可"**:§4.4 verifier 改判"磁盘可读 + red/green 序列"即 PASS;要入 git 则落仓根 log 路径承载(默认不强制)。 |
| grep-gate 放哪 | **IDS + XenoDev 各一份**;守自身用 repo-root/capability probe。 |

---

## §4 · 残留 v0.2 note（synthesizer 记 · 非阻塞)

1. **mac `sort -V` 实测待跑**:verdict 的版本 resolver 第 1 级(探测 `sort -V`)在 mac 上的真实结果待 operator 在 mac 跑;若不支持自动落 python3 fallback(resolver 已设计好,无需改)。spec-writer SKILL 注释"macOS 默认 sort 支持 -V"**应删/改**(未证实的机器假设,Codex 未找到一手依据)。
2. **`$XENODEV_REPO` 持久化**:build_repo 优先级链第 1 级依赖此 env,而 env 指针持久化本身是坑(项目已有 KG-env-pointer 前例)。fail-closed(第 3 级)兜底,但 operator 该在双机 shell profile 设 `$XENODEV_REPO`。
3. **KG-29 半同步窗口现状**:IDS 已修(`7164381`),XenoDev mirror 靠 operator 手动 apply patch —— 这正是 §3 半同步窗口的活样本,同步 checklist 该覆盖它。

---

## §5 · 0 分歧确认 + synthesizer 指引

**0 实质分歧确认**:Codex P3R1 §4 明说无分歧;其两条精修(build_repo 优先级链 / 工具能力类别)本轮已全采纳进 §2 矩阵。双方 verdict 完全一致。

**给 synthesizer(W = decision-list + refactor-plan)**:
- **decision-list**:5 条 KG + 1 防漂移新增 + 1 追认,按 §2 矩阵逐条填 4 列(保留/调整/删除/新增)。KG-29 = 追认 keep。
- **refactor-plan**:按 §2 六类机制分组,每组列(哪些文件/哪些行 → 改成什么机制 → **双仓落地顺序 + SHA 复验** → 可测验收)。必含:build_repo 优先级链、版本 resolver 3 级、`check-no-hardcoded-env.sh`、mac `sort -V` 实测验收、KG-30 verifier 降级。
- **v0.2 note**:§4 三条。
- **注**:KG-27/28/30 修法落 XenoDev(不走 IDS 三层 mirror,是 XenoDev 自派生 SKILL);KG-26/X#5 落 IDS;KG-29 已落 IDS 待 XenoDev mirror。synthesizer 的 refactor-plan 要标清每条落哪个仓。

**P3R2 自评**:strong-converge 定稿,0 分歧。本轮实产 = 吸收 Codex 两条精修(build_repo 优先级链修了我 P3R1 的 bug / 工具能力类别升为矩阵第 6 类 + 3 级 resolver),verdict 矩阵从 5 类扩到 6 类 + base 目录,3 残留 + 3 v0.2 note 定稿。可进 Phase 4 synthesizer。字数约 1450。
