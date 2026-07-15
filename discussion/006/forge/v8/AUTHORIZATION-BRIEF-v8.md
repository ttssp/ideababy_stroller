# Forge v8 · 授权条目 brief(下发 XenoDev 改源)

**Generated**: 2026-07-13
**Source**: forge 006 v8 verdict(`stage-forge-006-v8.md`)+ operator 决策 [A] 全量落地
**Landing decision**: 选项 [A] 四簇 P0/P1 一并落地 · 守铁律(契约/规约先行 · 框架级变更只走 forge 决议后落地 · 不在 XenoDev 当场另改)
**IDS 侧本轮已落**(4 commit · 见落地记录):
- 簇① SHARED-CONTRACT **§8 gate 执行语义 SSOT**(四不变量)+ bump 2.4 · commit `7fe29c7`
- 簇② IDS CLAUDE.md **session-per-idea worktree 规约** + main 生命周期 · commit `67a41a3`
- 簇④ B3 bootstrap-kit **gitignore red-green-log 路径无关豁免** · commit `fb72e77`
- 簇④ B6 **hook 白名单治理规则**(`framework/hook-allowlist-governance.md`)· commit `1ce272d`
- 簇③ SHARED-CONTRACT **§5 Interface 5 LlmClient messages-style v2 契约** · commit `d37e1f1`

**本文件性质**: 授权条目——列出 mirror 件 / XenoDev runtime 侧需改动项。**这些不在本 forge 当场落地**(SSOT 在 XenoDev · per K5 硬约束);XenoDev session 消费本 brief 改源,改完 mirror 件的 cp -p 回 IDS mirror + 更新 MANIFEST SHA + 跑 mirror-sha 测试。

---

## 为什么是授权条目而非当场改

XenoDev runtime 实装(preflight / LlmClient / credential hook / parallel-builder)+ bootstrap-kit mirror 件的 **SSOT 在 XenoDev**(`MANIFEST-v0.2.md`:`maintained_by: XenoDev → IDS bootstrap-kit mirror sync`)。forge 治理仓(IDS)只定契约/规约,不当场改 mirror 源或 XenoDev runtime。

**注意方向**:SHARED-CONTRACT 的 SSOT 在 **IDS**(`ssot_owner: ideababy_stroller`)——§8/§5 契约 IDS 本轮**已直接落**,XenoDev 侧的 SHARED-CONTRACT mirror 由 XenoDev 侧 pull 同步(见 D0)。bootstrap-kit 内文件(scan-credentials / check-* / skills)方向相反,SSOT 在 XenoDev,IDS 是 mirror。

三层同步链(**仅 bootstrap-kit mirror 件适用**):
```
XenoDev SSOT(改在这) → framework/xenodev-bootstrap-kit/(IDS mirror · cp -p) → MANIFEST-v0.2.md(登记双侧 SHA · mirror-sha 测试守护)
```

operator [A]=全量落地但守铁律 → IDS 只落契约/规约,XenoDev 侧实装等本 brief 消费。

---

## 授权条目清单(XenoDev 侧改源)

### 簇① · gate 执行语义执行侧(P0)

#### A1 · preflight 登记表 + `evaluate_gate` 接进下游 preflight
- **文件**: XenoDev runtime 侧 preflight(消费 SHARED-CONTRACT §8.2 四不变量)
- **实装四不变量(§8.2)最轻实现**:
  1. **(a) gate task 语义**:task frontmatter 加 `gate: true`;task-decomposer 对 gate task 产 PASS 前置检查(下游 `depends_on` 消费 PASS artifact,非「已 merge」git 事实)。
  2. **(b) PASS artifact 存在性机器查验**:下游放行前机器查 gate PASS artifact 存在且格式合法;不存在 = 视同 FAIL(fail-closed)。**把 `evaluate_gate` 返回值真正接进下游 preflight**——现状 code-reviewer 佐证 *nothing gates action on evaluate_gate return*,这是核心止血。
  3. **(c) 已判 run 登记一次性消费**:机器可读登记表(文件级即可,≈ ACME nonce list)记每次 gate 判定的唯一 run 标识;同一标识只能被下游消费一次,重放 reject(治 KG-B7 replay)。
  4. **(d) 新 run 作废 stale 签字**:gate 输入变化产新 run,新 run 出现即作废旧 PASS 签字(≈ GitHub stale approvals)。
- **最轻实现原则**:登记表 = 文件级,无重型基建(forge v8 「强制点实现可轻,语义不降级」)。
- **动因**:防 V4 失控的 STOP 从 markdown 约定升为机器强制(KG-B4)+ 堵 codex R12-14 三轮同族假 PASS(KG-B7)。
- **同步**: preflight 实装若落 bootstrap-kit mirror 件 → cp -p 回 IDS mirror + MANIFEST SHA + mirror-sha 测试;纯 XenoDev runtime 侧则属 C 类(非 mirror)。
- **⚠ v0.2 note**: 登记表并发语义(多 session 判同一 gate 竞态)v0.1 单 operator 不触发 · 真冲突后再加原子写/锁。

### 簇② · 分支拓扑执行侧(P0/P1)

#### A2 · warn 型 worktree preflight + XenoDev CLAUDE.md 同构规约章
- **文件**:
  1. XenoDev `CLAUDE.md` — **补「Session-per-idea worktree 规约」章**(与 IDS CLAUDE.md 同构):默认 `claude -w <idea>`、命名约定 worktree/分支名 = idea id、一个 session 只 working on 一个 idea(切 idea = 换 session 非原 session 内切)、**用法要点**(单 idea 实质开发在该 session 内畅所欲言 · 跨 idea 另开 session)。
  2. XenoDev runtime 侧 session 启动 preflight。
- **改**:
  - CLAUDE.md 规约章:文字规约先行(operator 心智锚点 · 即使 preflight 未上线也先有规矩可依)。
  - preflight:session 的 worktree/分支名与 working idea 不匹配时 **warn 提示不阻断**(hook block 留 v0.2)。
- **动因**: XenoDev 侧同构 IDS worktree 规约(IDS CLAUDE.md「Session-per-idea worktree 规约」已写 · 明写「XenoDev 侧同构规约见 XenoDev CLAUDE.md」· 本条兑现)。operator 明确要求用法落 CLAUDE.md(2026-07-15 确认)。
- **⚠ v0.2 note**: warn 上线后 mismatch 混线仍复发 ≥2 次 → 升 commit-time block(判据数据来自真跑)。
- **⚠ 运行时资源提醒**(写进规约章): worktree **不隔离** DB/env/端口/运行时服务,多 session 并行跑测试会撞资源 → 第一次真冲突后规约互斥(v0.2 note 4)。

#### A3 · outbox/handback frontmatter 加拓扑三字段
- **文件**: `handback-validator/gen-handback.sh`(XenoDev SSOT · IDS mirror)+ codex outbox 写入点
- **改**: hand-back / outbox 包 frontmatter 加 `current_idea` / `worktree` / `baseline` 三字段(跨仓通道自带拓扑自证)。
- **同步**: gen-handback.sh 是 mirror 件 → cp -p 回 IDS mirror + MANIFEST SHA + mirror-sha 测试。
- **注**: 若三字段进 SHARED-CONTRACT §6 hand-back schema(§6.3)则那部分是 IDS SSOT,需 IDS 侧补 §6.3 schema 字段(本 brief 消费时评估是否触碰 §6)。

#### A4 · parallel-builder §0.1/§1.2 baseline 改机器可读声明消费(P1)
- **文件**: `skills/parallel-builder/SKILL.md` §0.1/§1.2(XenoDev SSOT · IDS mirror)
- **改**: 现硬编码 `git log main` / `-b task/... main` → 改消费**机器可读 baseline 声明**(带回流截止条件防长驻)。blocked-handback fork 是 stacked 场景,SOTA 有显式 base 对应物。
- **动因**: KG-B2(build 基线隐含 main · blocked-handback fork 立刻炸 import fail + depends_on 误报)。
- **同步**: parallel-builder SKILL 是 mirror 件 → cp -p 回 IDS mirror + MANIFEST SHA + mirror-sha 测试。

### 簇③ · LlmClient role 分离实装(P0 契约已落 / P1 实施)

#### A5 · LlmClient v2 + legacy adapter 实装 + 兼容测试
- **文件**: XenoDev `LlmClient` 实装(消费 SHARED-CONTRACT §5 Interface 5)
- **实装(迁移三步 · 动冻结契约给路径)**:
  1. messages-style v2 为正典入口(`messages: list[{role, content}]` · 指令走 system 数据走 user · 数据永不进指令通道)。
  2. `complete(prompt: str)` 降 **legacy adapter**(内部包 `[{role:"user", content:prompt}]` 调 v2 · 单向依赖 · 新代码 lint 禁用)。
  3. 旧消费面(001 项目内 reconstructor / gate / CLI / fake **至少四处**)在**下一个自然接触点收编**,**不专开迁移 task**(防过度工程)。
- **兼容测试**: v1 adapter 输出 == v2 messages 输出(**同语料双跑**)保证降级等价。
- **allowlist 保留**: 字符 allowlist / 序列化清洗降 **defense-in-depth 保留不删**(role 分离亦非 proof)。
- **⚠ 迁移爆炸半径(实装前必做)**: **grep bootstrap-kit 模板是否内嵌 `complete(prompt)` 形状**(P1-Opus §3.2 未定)——内嵌则迁移 = 契约版本化(v1/v2 并存过渡);grep 结果决定爆炸半径。
- **同步**: LlmClient Protocol 若为 mirror 件走三层同步;否则属 C 类。
- **⚠ v0.2 note**: v1 直接消费面三个月后仍残留 → 裁是否专开收编 task。
- **⚠ 安全补审(underweights)**: messages-style v2 **上线后**应补一轮注入回归(SOTA 明言 role 分离亦非 proof · allowlist 是对冲)。

### 簇④ · 证据与 hook 治理执行侧(P0 已落止血 / P1 实装)

#### A6 · 证据入仓机器检查
- **文件**: `skills/parallel-builder/SKILL.md` §4.4 收口(XenoDev SSOT · IDS mirror)
- **改**: task ship 收口加「证据已入 git」机器检查(`git ls-files` 查 red-green-log 证据在版本控制内)——否则 gitignore pattern 修完仍是约定。
- **动因**: KG-B3——bootstrap-kit gitignore 模板 IDS 侧已修(commit `fb72e77` · `!**/red-green-log/*.log`);XenoDev 项目内 gitignore 若已单独修则随 bootstrap 模板改后统一生效,但**机器检查**才防「以后又被吞」。
- **同步**: parallel-builder SKILL mirror 件 → 三层同步。

#### A7 · credential hook 白名单按模式类实装 + §6.1 冲突协调(P1)
- **文件**: `safety-floor-1/scan-credentials.sh` + `pre-commit-credential.sh`(XenoDev SSOT · IDS mirror)
- **改(按 IDS 治理规则 `framework/hook-allowlist-governance.md` 三不变量)**:
  1. 按**三模式类**实装豁免识别(heredoc-commit-message / mktemp 私有 dir / 变量拼路径·`$()`),**非逐例加白**。
  2. 每条 `SKIP_PATHS` 补**登记理由**(属哪个模式类/谁批准/何时)。
  3. **§6.1 冲突择一实装**:hook 误报 mktemp vs parallel-builder §6.1 mktemp 范式——选 A(固定 scratchpad 路径)或选 B(hook 放行 mktemp),决策登记。
- **动因**: KG-B6——三类误报 fail-closed 与 §6.1 明写 mktemp 范式直接冲突;逐例加白 = KG-B1 同构路径病。
- **地位不动**: 件1 non-overridable + fail-closed 姿态不动,动的只是误报面。
- **同步**: scan/pre-commit 是 Safety Floor 件1 mirror 件 → 三层同步(改误报面走 IDS mirror sync)。

---

## 缓做(本轮 out of scope · 后续批次 / v0.2 note 观察位)

- **worktree hook block**(v0.2 note 1):warn preflight 后 mismatch 混线仍复发 ≥2 次 → 升 commit-time block。
- **B5 收编时限裁决**(v0.2 note 2):v1 直接消费面三个月后仍残留 → 裁是否专开收编 task。
- **gate 登记表并发语义**(v0.2 note 3):多 session 判同一 gate 竞态 → 真冲突后加原子写/锁。
- **worktree 运行时资源互斥**(v0.2 note 4):DB/env/端口不隔离 → 第一次资源冲突后规约互斥声明。
- **簇②③ XenoDev 真跑校准**(underweights 缓解):落地前对簇②③在 XenoDev 真跑一轮,用实证兜 forge 推演盲区(对齐 forge-verdict-vs-empirical-ship 教训)。

---

## 落地顺序(XenoDev session 执行)

1. **A1**(先 · 最高优先)gate 执行语义 preflight 登记表 + `evaluate_gate` 接下游——防 V4 机器化,是本轮最痛点止血。
2. **A2 + A3**(worktree warn preflight + 拓扑三字段)——拓扑显式化止血。
3. **A6**(证据入仓机器检查)——B3 收口(IDS gitignore 模板已改)。
4. **A4**(parallel-builder baseline 声明消费)+ **A7**(hook 白名单模式类 + §6.1 协调)——P1。
5. **A5**(LlmClient v2 + adapter + 兼容测试)——P1 · **实装前先 grep 消费面定爆炸半径**。
6. **每步 mirror 件**:XenoDev 改源 → cp -p 回 IDS mirror → 更新 MANIFEST SHA → 跑 mirror-sha 测试 · 每步记双仓 commit SHA。
7. **簇②③ 真跑校准**:A2/A3/A5 落地后在 XenoDev 真跑一轮,兜回声室盲区(underweights 缓解)。

## 交叉引用

- SSOT 契约: `framework/SHARED-CONTRACT.md` §8(gate 执行语义)+ §5 Interface 5(LlmClient v2)
- IDS 规约/治理: `CLAUDE.md`(worktree 规约)+ `framework/hook-allowlist-governance.md`(hook 白名单)
- gitignore 止血: `framework/xenodev-bootstrap-kit/.gitignore.template`(已改)
- verdict: `discussion/006/forge/v8/stage-forge-006-v8.md`
- XenoDev 侧同 brief 入口: `/home/ys/codes/XenoDev/dogfood-backlog.md`(攒批消费)
- 回声室风险 underweights: `stage-forge-006-v8.md` §"What this menu underweights"
