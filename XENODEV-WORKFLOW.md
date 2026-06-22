# XenoDev 工作流 · IDS ↔ XenoDev 两仓怎么用

> **这是什么**:用 **IDS**(治理)+ **XenoDev**(开发)两仓做开发的**权威操作入口**。
> 想用 XenoDev 写代码、不确定"现在该在哪个仓、该切回来吗、问题该记哪",看这一份。
>
> **版本**:v1.0 · 2026-06-03
> **边界 SSOT**:本文是"怎么用"的快速入口;最权威、最详尽的两仓分工 / hand-back schema /
> workspace 校验在 [`framework/SHARED-CONTRACT.md`](./framework/SHARED-CONTRACT.md) **§6**(contract v2.0)。
> 本文与 §6 冲突时,**以 §6 为准**。
>
> ⚠️ **注意**:仓内老手册 [`PLAYBOOK.md`](./PLAYBOOK.md) §6/§7 和 [`README.md`](./README.md) §3.2
> 的 "L4 在 IDS 内产 specs/ + 并行开发" 写法是 **M2 切换前的旧世界观,已过时** —— 真开发早已
> 搬去 XenoDev。那两处只保留 L1-L3 主线参考价值,L4 之后一律以本文为准。

---

## 0. 一句话先认清

| 仓 | 路径 | 角色 | 你在这里干什么 |
|---|---|---|---|
| **IDS** | `/Users/admin/codes/ideababy_stroller` | 🏛️ **治理** | idea → PRD → 治理决策(forge / handback-review / scope-inject) |
| **XenoDev** | `/Users/admin/codes/XenoDev` | 🏭 **唯一 build runtime** | 真写代码:spec → tasks → build → ship → hand-back |

**两个"绝不"是这套体系的地基**:

- ❌ **代码绝不在 IDS 写** —— IDS 自 M3 起不再产 `specs/`(per SHARED-CONTRACT §6 v2.0)。
- ❌ **框架绝不在 XenoDev 当场改** —— 协议 / SKILL / mirror / 并发机制的改动必须回 IDS 走 `/expert-forge`(防 V4 失败模式)。

两仓之间只靠两个包传递:

- **HANDOFF**(IDS → XenoDev):`/plan-start` 产 `discussion/<id>/<prd>/L4/HANDOFF.md`,XenoDev 消费。
- **hand-back**(XenoDev → IDS):XenoDev ship 后产 `discussion/<id>/handback/<ts>-<id>.md`,IDS `/handback-review` 消费。

---

## 1. 完整生命周期(一个新想法从 0 到 ship)

```
┌─────────────────────── IDS 仓(治理) ───────────────────────┐
│  /propose            一句话种子 → proposals.md               │
│     ▼                                                        │
│  /inspire-start  L1 发散 N 方向(纯价值,不碰技术)           │
│  cdx-run ×N → /inspire-advance → 选方向 /fork               │
│     ▼                                                        │
│  /explore-start  L2 深挖(还是不碰技术)                      │
│  cdx-run → /explore-advance                                 │
│     ▼                                                        │
│  /scope-start    L3 真需求:建什么 / 不建什么                │
│  L3R0 intake → cdx-run → /scope-advance → 候选 PRD 菜单      │
│     ▼                                                        │
│  /fork <id> <候选>   候选 PRD 固化成 fork → 得到 PRD.md      │
│     ▼                                                        │
│  /plan-start     L4 hand-off:产 HANDOFF.md                 │
│                  ⚠️ IDS 到此为止,不再产 specs/               │
└─────┼────────────────────────────────────────────────────────┘
      │   ← 切仓 →   cd /Users/admin/codes/XenoDev && claude
      ▼
┌─────────────────────── XenoDev 仓(build) ──────────────────┐
│  cat .../L4/HANDOFF.md     读 hand-off 包                    │
│  cp PRD → XenoDev/PRD.md                                     │
│     ▼                                                        │
│  spec-writer        PRD → spec.md(7 元素 + PPV)           │
│  task-decomposer    spec → tasks/T*.md + dependency-graph   │
│     ▼                                                        │
│  ⚠️ 起并发批次前,回 IDS 跑 concurrency-preflight.sh         │
│     (v5 P0 装的门 · 守护 mirror 不漂移 · 见 §5 第2条)       │
│  parallel-builder   每 task 独立 worktree · TDD · sonnet    │
│     ▼                                                        │
│  /task-review       每个 worktree merge 前必过(verdict≠BLOCK)│
│     ▼                                                        │
│  ship + 产 hand-back 包(跑 6 约束 validator 自检)          │
│                     写回 IDS discussion/<id>/handback/       │
│                                                              │
│  ★ 开发中随手:发现框架级问题 → append dogfood-backlog.md    │
└─────┼────────────────────────────────────────────────────────┘
      │   ← 切回 IDS →
      ▼
┌─────────────────────── IDS 仓(治理) ───────────────────────┐
│  /handback-review <id>   读 hand-back → 决议 §3 actions      │
│     ├─ PRD 没问题、活干完了 → 闭环,这个 fork 完成          │
│     ├─ PRD 有问题 → /scope-inject 改 PRD → 重新 hand-off    │
│     └─ 框架级问题攒够 → /expert-forge 006(见 §4 dogfood)   │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. 何时在哪个仓 · 何时切(决策入口)

### 2.1 何时从 IDS 切到 XenoDev

**触发**:L4 `/plan-start` 产出 `HANDOFF.md` 之后。

```bash
# IDS 侧产出 HANDOFF 后,新开一个 XenoDev session 真开发
cd /Users/admin/codes/XenoDev && claude
```

spec / tasks / build / quality **全在 XenoDev**。IDS 这边的 L4 只到 HANDOFF 为止。

### 2.2 何时从 XenoDev 切回 IDS(照信号查这张表)

> 这张表是 XenoDev `CLAUDE.md`「当出问题时」决策矩阵的镜像入口。XenoDev session 里
> 同一张表也在,两边一致。

| 你遇到的信号 | 处理 | 怎么做 |
|---|---|---|
| **在建项目的功能要改** | XenoDev 内迭代 | 正常开发,**不回 IDS,不记 backlog** |
| **框架本身有坑**(协议 / SKILL / hand-back / mirror / 并发机制) | **记 backlog · 攒批回 forge** | append XenoDev `dogfood-backlog.md` → 攒够 → 回 IDS `/expert-forge 006`。**不当场改框架** |
| **PRD 约束不可达 / spec 与 PRD 矛盾** | **切回 IDS 修 PRD** | 产 hand-back → IDS `/handback-review <id>` → `/scope-inject` 改 PRD → 重新 hand-off |
| **重大架构转向** | **必须先 forge** | 回 IDS `/expert-forge <id>`(forge 永远在 IDS 治理仓,防 V4 失败模式) |
| **Safety Floor 违反**(凭据 / 不可逆命令 / 删备份) | **停 + escalate** | hard-fail,绝不静默绕过 |
| **hand-back 6 约束 / validator 不通** | **先自查再 escalate** | XenoDev 跑 `bash lib/handback-validator/validate-handback.sh <file> /Users/admin/codes/ideababy_stroller` dry-run |

**一句话判别"框架级 vs 项目级"**:这个问题修好后,**受益的是"以后所有用这套 framework 的项目"** → 框架级(记 backlog / 回 forge);**只"当前这个项目"** → 项目级(XenoDev 内迭代)。

---

## 3. 两个高频场景的最短路径

### 场景 A · 我有个新想法,想变成代码

- **想法很模糊**:走完整链 `/propose` → L1 → L2 → L3 → `/fork` → `/plan-start` → 切 XenoDev。
- **想法已经清楚**:L1/L2 可 **skip**(`/inspire-start <id> skip`,甚至直接从 `/scope-start` 起步把 proposal 当方向)。
- **不可跳的两步**:**L3(定 PRD)** + **L4(`/plan-start` 产 HANDOFF)** —— 没 PRD 不许写代码(铁律 "No code without a spec")。

### 场景 B · XenoDev 开发到一半卡住 / 发现问题

照 **§2.2 决策矩阵**查信号。最常踩的两条:
- 只是**当前项目**的功能 → XenoDev 内改,别回 IDS。
- 是**框架坑** → 记 `dogfood-backlog.md`,**别手痒当场改**,攒批回 forge。

---

## 4. dogfood 循环(日常使用的精髓)

你的核心使用模式**不是"一次性把某个 idea 建完"**,而是**边用边攒、定期回炉**:

```
用 XenoDev 真开发若干项目
   │  开发中 Claude 被 CLAUDE.md/AGENTS.md 铁律提醒,
   │  把框架级坑随手记进 XenoDev dogfood-backlog.md
   │  (复现场景越具体越值钱 —— forge v5 最大教训:审没真跑过的东西容易跑偏)
   ▼
攒够一批(或某条 high 严重度顶不住)
   │  随 hand-back §3「Suggested IDS actions」回流到 IDS,
   │  或 operator 直接 cp backlog 快照到 IDS discussion/006/
   ▼
回 IDS:/expert-forge 006     ← backlog 整个当 forge 的 X 标的
   │  双 AI 收敛出 v6 verdict + 改造方案
   ▼
下发 XenoDev 半边 brief → 框架升级 → 继续用
```

这正是已经走完的 **v4 → v5** 模式("攒批真问题再 forge")。
当前 backlog 已有 2 条种子(KG-1 单全局指针无 task identity / KG-2 B-3 秒级命名),等真并发把形态撞出来后回 forge v6。

---

## 5. 几条容易忘的硬规矩(贴墙上)

1. **代码绝不在 IDS 写** · **框架绝不在 XenoDev 当场改** —— 两个"绝不"是地基。
2. **起多 worktree 并发批次前,先在 IDS 跑 `concurrency-preflight.sh`** —— v5 P0 装的门,守护
   bootstrap-kit 里 XenoDev 共享 lib 的 mirror SHA 没漂移,对齐才放行并发批次。
   - 脚本位置(IDS 本地,**不在 XenoDev**):`framework/xenodev-bootstrap-kit/concurrency-preflight.sh`。
     它 `SCRIPT_DIR` 指向 IDS 自己的 `tests/integration/`,在 IDS 仓根跑。XenoDev 侧无此脚本。
3. **parallel-builder 一律用 `model=sonnet`**(忽略 task 推荐),operator 既定偏好。
4. **每个 worktree merge 前必过 `/task-review`**,verdict ≠ BLOCK 才能并。
5. **v1.0 路径强制 cross-model review**(L4 质量门)。
6. **push 永远要 operator 点头** —— 不自动 push 任何一仓。

---

## 6. 关键路径速查

| 我要 | 在哪个仓 | 命令 / 文件 |
|---|---|---|
| 提新想法 | IDS | `/propose` |
| 看所有 idea 在哪一层 / 谁等谁 | IDS | `/status` · `/status <id>` · `/status --activity 7` |
| 把想法推到 PRD | IDS | `/inspire-start` → `/explore-start` → `/scope-start` → `/fork` |
| 产 hand-off(切 XenoDev 前最后一步) | IDS | `/plan-start <fork>` → 产 `HANDOFF.md` |
| 进 XenoDev 真开发 | — | `cd /Users/admin/codes/XenoDev && claude` |
| 并发前守护 mirror 不漂移 | **IDS** | `bash framework/xenodev-bootstrap-kit/concurrency-preflight.sh`(IDS 本地脚本) |
| 记框架坑 | XenoDev | append `dogfood-backlog.md`(按模板) |
| hand-back 自检 | XenoDev | `lib/handback-validator/validate-handback.sh <file> <IDS路径>` |
| 收 hand-back 决议 | IDS | `/handback-review <id>` |
| PRD 要改 | IDS | `/scope-inject <fork>` |
| 框架要改(攒批后) | IDS | `/expert-forge <id>` |
| 边界 / schema 权威细节 | IDS | `framework/SHARED-CONTRACT.md` §6 |

---

## 7. 相关文档导航

- [`framework/SHARED-CONTRACT.md`](./framework/SHARED-CONTRACT.md) **§6** — 两仓分工 / hand-back schema / workspace 校验的**边界 SSOT**(最权威)。
- [`CLAUDE.md`](./CLAUDE.md) 「XenoDev 跨仓」段 — IDS 侧宪法级快速指针。
- XenoDev `CLAUDE.md` 「dogfood 铁律」+「当出问题时」 — XenoDev 侧决策矩阵(本文 §2.2 的正本)。
- XenoDev `dogfood-backlog.md` — 框架级问题攒集处(append-only,回流 forge 的 X 标的)。
- [`PLAYBOOK.md`](./PLAYBOOK.md) §0-§5 — L1-L3 主线详细操作(⚠️ §6/§7 的 L4 部分已过时,以本文为准)。
- [`README.md`](./README.md) — 这个孵化器**为什么这么设计**。
