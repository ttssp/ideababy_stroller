---
doc_type: forge-config
forge_id: 006
forge_version: v6
created: 2026-07-02T06:45:04Z
prefill_source: manual(009-pForge M1 linux 新机首跑暴露的 5 条同根 backlog · operator 攒批回 forge)
convergence_mode: strong-converge
x_count: 5
x_hash: 6b39d6badc8fa245ccc6a47735518e54
y_count: 2
w_count: 2
z_mode: 对标 SOTA(跨平台工具链可移植性 · Phase 2 跑搜索)
k_provenance: verbatim 本 session operator 决策(KG-29 追认 · KG-26/27 系统性修法 · 双机非发行)
v6_mission: 跨机器可移植性加固 —— 框架把某台 mac 的环境形态(路径/版本/env/目录)硬编码成默认,linux 新机首跑全暴露
inheritance: v5 verdict(并发安全 · CONCERNS)不重审;本轮只审 KG-26/27/28/29/30 五条同根缺陷
---

# Forge config · idea 006 · v6

## 背景:为什么起 v6

009-pForge M1(投资闭环第一期 PIT 价格层)第一次在 **linux 新机**(`/home/ys/`)上跑完整条
IDS→XenoDev build 链(spec → task → parallel-builder → ship → hand-back)。此前所有 006 forge
(v1-v5)+ 所有 dogfood 都在 **mac**(`/Users/admin/`)上。**一换机器,一天暴露 5 条同根框架缺陷**:

> **同一根因**:框架在多处**把某台 mac 的环境形态硬编码成默认值** —— 绝对路径、codex 版本号、
> env 工具链假设、目录结构假设。单机(mac)永远触发不了;跨机器(linux)首跑全部 reachable。

这不是 5 个孤立 bug,是**一个系统性可移植性缺陷的 5 个切面**。v6 要给出**系统性修法**(环境假设
该住哪层 + 一次清扫全实例 + 防再漂移机制),不是逐处补丁。

**v6 审的 5 条 backlog**(全文见 X#1 快照 `discussion/006/dogfood-backlog-20260702.md`):

| KG | 一句话 | 状态 |
|---|---|---|
| **KG-26** | IDS `/plan-start` HANDOFF 模板 + SHARED-CONTRACT §6.2 硬编码 mac 路径 `/Users/admin/codes/XenoDev` | 未修 |
| **KG-27** | XenoDev 三 SKILL(spec-writer/parallel-builder/codex-review)硬编码 mac codex-companion.mjs 路径 + 钉死已不存在的 1.0.3 版本 | 未修 |
| **KG-28** | parallel-builder/task 假设 uv+可复现 env 就位;linux 新机无 uv/无 .venv/pypi 被墙/uv.lock 有 yanked dep | 未修 |
| **KG-29** | `/plan-start` 铸的 fork id `009-pForge` 过不了 hand-back validator id 正则(`-p[A-Z]` 只收单字符) | **已 operator 直接决策修复(IDS `7164381`)· 本轮追认审计** |
| **KG-30** | parallel-builder §4.4 red-green log 落点假设仓根 tests/,build mirror 子项目时被子树 .gitignore 挡 | 未修 |

## X · 审阅标的(5 槽 · 跨机器可移植性现场)

### 槽位 1 · backlog 快照(核心 X · 5 条缺陷全文)
- `discussion/006/dogfood-backlog-20260702.md`(cp 自 XenoDev `dogfood-backlog.md` · **本轮只审 KG-26/27/28/29/30 段**;
  KG-1..25 为历史背景不重审 · 整文件可读但聚焦这 5 条)

### 槽位 2 · KG-26 现场(IDS 侧硬编码 mac 路径)
- `.claude/commands/plan-start.md`(HANDOFF 模板 §workspace.build_repo + §1 `cd` 指令 · 均写死 `/Users/admin/codes/XenoDev`)
- `framework/SHARED-CONTRACT.md` §6.2 workspace schema(4 字段示例表 + YAML 块 · 全 mac 路径 · line ~635-651)

### 槽位 3 · KG-27/28/30 现场(XenoDev 三 SKILL · 最重点)
- `/home/ys/codes/XenoDev/.claude/skills/spec-writer/SKILL.md` §3.1 L94-96(base 目录 `/Users/admin/.claude/...` mac · find `*/` glob 逻辑对)
- `/home/ys/codes/XenoDev/.claude/skills/codex-review/SKILL.md`(L16/58/122/138/152/156/357 等 8+ 处 · mac 路径 **+ 钉死 `1.0.3`**,本机是 1.0.4)
- `/home/ys/codes/XenoDev/.claude/skills/parallel-builder/SKILL.md`(L17+L58 mac+1.0.3;§0/§2 无 env preflight = KG-28;§2.1 L135-151 red-green log `tee tests/red-green-log/<TID>.log` 相对路径 = KG-30;§4.4 verifier 期望 log 随 commit)

### 槽位 4 · KG-29 已落地修复(追认审计标的 · 不推翻)
- `discussion/006/forge/v6/KG29-fix-commit-7164381.txt`(IDS commit `7164381` diff · charset 正则 `-p[A-Z]`→`-p[A-Z][a-zA-Z]*` + 对齐 `-v` 段 · 5 处统一)
- 实证:009 两个 hand-back 包(`161131Z`/`005910Z`)6 约束全 PASS(consumer mode) · path-traversal 负例仍 FAIL(4 道防线全触发)

### 槽位 5 · KG-26 同族未入册实例(evidence · 修法射程要覆盖)
- `/home/ys/codes/XenoDev/lib/handback-validator/gen-handback.sh`(产包 `to_source_repo` / `workspace.source_repo` 仍填 mac 路径 · 009 两包 frontmatter 可证 · KG-26 同根但 backlog 未单列)
- validator 相对路径 papercut:`validate-handback.sh` 约束5 路径提取要求 leading `/`,传相对路径误报 FAIL(本 session `/handback-review 009` 实测)

## Y · 审阅视角(2)
- **跨机器可移植性(核心)** — 环境假设怎么从硬编码变推断(路径/版本/index/目录形态),mac↔linux 两机都能跑;修法有外部锚不自创
- **工程纪律** — SSOT 三层同步纪律(条款 SHARED-CONTRACT / 实装 bootstrap-kit / XenoDev mirror);修法可测性;防再漂移机制(否则修完又漂)

## Z · 参照系
- mode: 对标 SOTA(聚焦跨平台工具链可移植性)
- 候选对标:12-factor config(config 从环境注入)/ XDG Base Directory + 环境变量惯例 / monorepo 相对路径推断(兄弟目录定位)/ uv·lockfile 可复现 env + index 配置 / CI 跨平台矩阵实践
- 不重刷 v1-v5 的并发安全 SOTA

## W · 产出形态(2)
- **decision-list** ✅ → 逐 KG 的 4 列决议矩阵(保留/调整/删除/新增 · 每条修法选型 + 理由 + 优先级 · 含 KG-29 追认审计结论)
- **refactor-plan** ✅ → 按模块分组的改造方案(哪些文件怎么改 · 双仓同步顺序 · 可测验收 · 直接指导落地)
- (verdict-only / next-PRD / next-dev-plan / free-essay 未勾)

## K · 用户判准

> 本批 5 条 backlog 是 009-pForge M1 在 **linux 新机首跑** IDS→XenoDev 全链一天暴露的,**同一根因 =
> 框架把某台 mac 的环境形态硬编码成默认**(绝对路径 `/Users/admin/...`、codex 版本号钉死 `1.0.3`、
> env 工具链假设 uv 就位、目录结构假设仓根 tests/)。这些坑单机(mac)永远触发不了,跨机器一上全暴露。
>
> **要你们盯死的**:
> 1. **KG-26/27 系统性修法**:环境假设该住哪一层 —— 模板字面?生成时推断(`realpath`/`git config`)?
>    运行时探测?环境变量(`$XENODEV_REPO`)?要一个**能一次清扫所有硬编码实例 + 防再漂移**的方案,
>    不是逐处补丁。KG-27 的 codex 版本尤其:钉死 `1.0.3` 每次 codex 升版本(1.0.3→1.0.4→…)都腐烂,
>    必须 `codex/*/scripts/...` glob + `sort -V | tail -1`,**绝不写死版本号**。
> 2. **KG-29 追认审计**:这条我已当场直接决策修了(charset 正则 `-p[A-Z]`→`-p[A-Z][a-zA-Z]*` + 对齐 `-v`
>    段,IDS commit `7164381`,009 两包已 6 约束全 PASS)。请审:**放宽 charset 有没有引入 path-traversal
>    等安全隐患**?有则给增量修正,**但不推翻已跑通的解阻**(009 T001/T002 已 ship 依赖它)。
> 3. **KG-28 env bootstrap**:parallel-builder 假设 env 就位,新机四连坑(无 uv / 无 .venv / pypi 被墙 /
>    uv.lock yanked dep)。要不要 §0 加 env preflight + 文档化新机首次 build 前的 env 建设?
> 4. **KG-30 red-green log 落点**:mirror 子项目 build 时 log 落子树被 .gitignore 挡,§4.4 verifier 恒不满足。
> 5. **修法射程要覆盖 evidence**:X#5 的 gen-handback mac 硬编码 + validator 相对路径 papercut 是同族,
>    别只修 backlog 单列的、漏了同根实例。
>
> **binding**:
> ① 框架级变更**只走本 forge**(不在 XenoDev / 不在别处当场改);
> ② 守 **SSOT 三层同步纪律**(SHARED-CONTRACT 条款 / bootstrap-kit 实装 / XenoDev mirror)——
>    修法两仓一次落地,不留半同步态(KG-29 现在就是半同步:IDS 修了 XenoDev mirror 靠 operator 手动补);
> ③ **别推翻 009 已 ship 链**(T001/T002 已 codex approve + hand-back 回流);
> ④ **自用单人双机(mac + linux),非通用多平台发行** —— 修法按"两台已知机器都能跑"设计,不做 Windows/
>    容器/CI 矩阵的过度工程(那是 V4);
> ⑤ **轻收尾**:可执行优先,decision-list + refactor-plan 要能直接指导落地,不要长 essay。

## 收敛模式
strong-converge → 单一 verdict + 残余分歧降级 v0.2 note
