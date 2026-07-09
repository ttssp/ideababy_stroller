# Forge v7 · 授权条目 brief(下发 XenoDev 改源)

**Generated**: 2026-07-08
**Source**: forge 006 v7 verdict(`stage-forge-006-v7.md`)+ operator 决策 D0/D1/D2
**Landing decision**: 选项 [B] 局部先落 P0 + KG-35 提级 · D0=严格守铁律(契约先行)· D1=只落止血核心 · D2=两者都写
**IDS 侧本轮已落**: SHARED-CONTRACT §7 fork-id SSOT + §6.2.1 约束 6 引用改造(commit 见落地记录)
**本文件性质**: 授权条目——列出 mirror 件 / XenoDev runtime 侧需改动项。**这些不在本 forge 当场落地**(SSOT 在 XenoDev,per K5 硬约束);XenoDev session 消费本 brief 改源,改完 cp -p 回 IDS mirror + 更新 MANIFEST SHA。

---

## 为什么是授权条目而非当场改

`codex-review SKILL` + `handback-validator/check-*.sh` 是 bootstrap-kit mirror 件,
**SSOT 在 XenoDev**(`MANIFEST-v0.2.md` line 30:`maintained_by: XenoDev → IDS bootstrap-kit mirror sync`)。
forge 治理仓(IDS)只定契约,不当场改 mirror 源。三层同步链:

```
XenoDev SSOT(改在这) → framework/xenodev-bootstrap-kit/(IDS mirror · cp -p) → MANIFEST-v0.2.md(登记双侧 SHA · mirror-sha 测试守护)
```

operator D0=严格守铁律 → 本轮 IDS 不碰 mirror 源,`001-radar-pA` 解阻等 A1 那一跳完成。

---

## 授权条目清单(XenoDev 侧改源)

### A1 · check-6.sh regex 改为 §7.2 SSOT 值(P0 · 解阻 001-radar-pA)

- **文件**: `handback-validator/check-6-id-charset-and-final-path.sh` §1.2(现 line 45-46)
- **改**: `prd_fork_id` 正则
  - 旧(v0.3):`^[0-9]{3}[a-z]?(-p[A-Z][a-zA-Z]*)?(-v[0-9]+\.[0-9]+)?$`
  - 新(v7 · SHARED-CONTRACT §7.2):`^[0-9]{3}[a-z]?(-[a-z0-9]+)*(-p[A-Z][a-zA-Z0-9]*)?(-v[0-9]+\.[0-9]+)?$`
  - 唯一变化:新增中段 `(-[a-z0-9]+)*`
- **验证**: 用 SHARED-CONTRACT §7.4 列的全量 23 真实已铸 id 语料全绿 + traversal 异常全拒(见 A3 fixture)
- **注释更新**: line 37-44 的演化史注释补 v7 entry,指向 SHARED-CONTRACT §7 为 SSOT
- **同步**: 改完 cp -p 回 `framework/xenodev-bootstrap-kit/handback-validator/check-6-id-charset-and-final-path.sh` + 更新 MANIFEST SHA + 跑 mirror-sha 测试

### A2 · codex-review SKILL 状态机止血核心(P0 · D1=只落止血核心)

- **文件**: `.claude/skills/codex-review/SKILL.md`(XenoDev SSOT)/ IDS mirror `framework/xenodev-bootstrap-kit/skills/codex-review/SKILL.md`
- **改 4 处**(只落止血核心,watchdog 阈值 / 完整 breaker 态机 / half-open 时机标 v0.2 靠真跑校准,**本轮不做**):
  1. **§0/§2 失效判据三分类**:现 §0.1 只 check companion.mjs 存在,无失效分支。加三分类决策:
     - 起不来(KG-32 额度/插件不可用)/ 起得来跑不动(KG-37 沙箱 bwrap loopback)/ 跑得动挂死(KG-38 会话流静默 7min+)
     - 三类均触发 breaker 开路走 fallback reviewer(subagent),不靠临场外推
  2. **§0.2 scope 语义 + 空 diff 拦截**(KG-23 · 报告点名最危险假绿):
     - scope 文档-实现改一致;ship 流程 branch-scope 默认;沙箱失效由状态机降级 working-tree
     - **空 diff → verdict 无效不产生 approve**(现 §4.1.2 只在 stdout 完全空时 fail closed,空 diff 不拦 → 每轮 commit 后可能 vacuous approve)
  3. **§2/§3 降级链 = 交叉矩阵**:失败模态决定开路,task risk × 领域决定 fallback reviewer 分流
     (write-boundary → red-team+code-reviewer 双跑;medium test-only → code-reviewer 单跑;与 T016/T017 实践吻合)
  4. **§5 审计标注**:fallback verdict 带 `reviewed-by: subagent-fallback@date` 不冒充 codex(REVIEW-LOG 已有惯例 · 升格进 SKILL normative)

### A3 · KG-35 verdict 提取三级 fallback 链(P0 · operator 提级)

- **文件**: `codex-review SKILL.md` §4.1.2(现只 grep 主 `CODEX_OUT` stdout)
- **改**: verdict 解析加三级 fallback 链,任一级拿到即用,三级全空才 fail closed:
  - Level 1: 主 stdout log(现状)
  - Level 2: `status --all --json` 的 latestFinished.summary
  - Level 3: job 独立 logFile
- **动因**: 只 grep 主 log 会漏 verdict → 误判"无 finding 可 merge"(假绿一种)。与 KG-23 空 diff 同属"守门员表面绿实则没审到"病族,operator 提到 P0 与 KG-23 一起做闭环。

### A4 · 双仓契约 fixture 语料(P0)

- **文件**: `handback-validator/test-fixtures/` 下补 fork-id 语料(现有 `valid-pforge-multichar/` `invalid-6-id-charset/` 作模板)
- **建三类**(Pact 消费者驱动契约测试形状 · 同一语料双仓各跑):
  - **旧 id 全过**: `001-radar-pA` `008-pB` `009-pForge` `006a-pM` `006a-pM-v0.2` `007` `002b-stablecoin-payroll` `007a-agent-emit`
  - **新三段式全过**: 代表性中段 slug
  - **traversal 异常必拒**: `008/../../etc` `001-radar-pA/x` `../008` 含控制字符样本 `006a-pM-v0`(缺 minor)
- **双仓跑**: IDS 铸造侧(plan-start)全过 + XenoDev 接受侧(check-6)全过

### C1-C5 · XenoDev runtime 侧(P1/P2 · 非 mirror · 属 XenoDev)

- **C1**(P1)companion.mjs 内建 watchdog(watchdog 目标态执行层)+ 修 status/result 语义:status 报 running 时 result 该回「job 仍 running · 无结果」而非「No job found」(KG-38 暴露的自相矛盾)
- **C2**(P1)gen-handback fork-id 显式参数化:废「仓根 HANDOFF = 唯一活跃 fork」SSOT 假设(多 fork 008/009/001 并行时静默拿 stale id),消费 SHARED-CONTRACT §7 契约
- **C3**(P1)KG-33:worktree remove 前 stash list 快照 + 删后比对告警(**根因待复现不推演** · v0.2 note 2 · 对齐 forge-verdict-vs-empirical-ship 教训)
- **C4**(P2)KG-34:migration task 必真跑 `alembic upgrade head` 硬 checklist(落 XenoDev 执行面 + parallel-builder §2.4)
- **C5**(P2)长任务 flock 单实例锁 + 心跳查产物/日志不查进程表(未编号长任务条 · 与挂起检测同族)

---

## 缓做(本轮 out of scope · 后续批次)

- **KG-22**(P1)per-phase status 最小 schema + 下游 gate 读取规则(spec-writer SKILL §3.3 · 不重构 phased spec)
- **KG-12 / KG-31**(P2)papercut:validator README valid 示例改 producer mode + fixture / gen-handback mac 字面路径
- **watchdog 阈值 / half-open 触发时机最终值**(v0.2 note 1 · 3-5 次真实 fallback 后校准)
- **通用长任务 liveness 组件**(v0.2 note 3 · 再出第二例多进程互写事故才组件化)

---

## 落地顺序(XenoDev session 执行)

1. **A1**(先 · 解阻)check-6 regex → §7.2 值 + A4 fixture 双仓验证 → **001-radar-pA 解阻**
2. **A2 + A3**(codex-review SKILL 状态机止血核心 + KG-35 三级链)
3. 每步:XenoDev 改源 → cp -p 回 IDS mirror → 更新 MANIFEST SHA → 跑 mirror-sha 测试
4. **C1-C5** 按 P1/P2 分批
5. 半同步窗口用 v6 组 G 同步 checklist 收口 · 每步记双仓 commit SHA

## 交叉引用

- SSOT 契约: `framework/SHARED-CONTRACT.md` §7(fork-id)+ §6.2.1 约束 6
- verdict: `discussion/006/forge/v7/stage-forge-006-v7.md`
- XenoDev 侧同 brief 入口: `/home/ys/codes/XenoDev/dogfood-backlog.md`(D2=两者都写)
