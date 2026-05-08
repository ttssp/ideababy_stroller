# L3R0 Intake · 007a-agent-emit · Scope phase human-input

**Captured at**: 2026-05-08T09:50:00Z
**Method**: AskUserQuestion (4 batches, 7 questions total — 浓缩自标准 6 block,因 L2 stage doc 已默认了 audience / business / platform 维度)
**Operator**: Yashu Liu

> **设计原则**(scope-protocol):每条问题允许 "not sure"。"Not sure" 是 first-class 答案,
> 标注 ❓ 后,L3R1 必须主动给 ❓ 项提选项,不替 operator 决定。

---

## Block 1 · Time + hours

### ✅ Q1 · v0.1 多快拿到手
**1-2 周 (匹配 playbook timeline)**

operator 同时在跑 forge 006 路径 2 的 4 周 playbook,W0-W2 期间需要 friction-tap 落地以便 W2 step 4 用得上(playbook L211 "每次 V4 retrospective skill 跑得不顺畅就 jot 一笔到 friction-log")。超过 2 周则违反 playbook timeline。

### ✅ Q2 · hours/week
**5-10 小时(部分时间 · 与 dogfood 并行)**

operator 同时还要跑 V4 dogfood + 其他 forge 事务,friction-tap 是辅助项,不能成为主线。

**计算**:1-2 周 × 5-10 小时 = **10-20 小时总预算**(含 L4 spec / L4 build / 测试 / commit)。

---

## Block 2 · Audience(从 L2 §3 默认)

### ✅(默认,无需 question)
**Single operator 跑 V4 dogfood 自用** —— L2 stage doc §1 / §3 / §6 condition 4 已强 lock。
multi-reader / 团队扩展 / 跨 dogfood 实例聚合全部留 §4 extension,**v0.1 不接受任何 multi-user 假设**。

---

## Block 3 · Business model(从 L2 §5 默认)

### ✅(默认,无需 question)
**Free OSS / 自用脚本** —— 红线之一 = "不与 enterprise observability 竞争",所以无 SaaS / 付费 tier。

---

## Block 4 · Platform(从 L2 §6 / `PostToolUseFailure` hook 验证默认)

### ✅(默认,无需 question)
**Claude Code hook + CLI(macOS)** —— 载体已锁:`PostToolUseFailure` hook 写文件 + `friction <msg>` Python CLI fallback。operator 工作环境是 macOS。

---

## Block 5 · Red lines

### ✅ Q5 · v0.1 红线(operator 选了 4 条,全 hard)
- ✅ **Hard red line 1 · 不接全知监控**:agent 是 witness,不是管理者 / 裁判;不试图解释情绪
- ✅ **Hard red line 2 · 不接追责文化**:log 不能被当问责材料;v0.1 不做任何"自动开 issue"自动化
- ✅ **Hard red line 3 · 不接合作上传**:log 默认 private to operator;不能 default-shared;不上传云
- ✅ **Hard red line 4 · 不与 enterprise observability 竞争**:不跟 Langfuse / Helicone / Phoenix 正面比;不加 SaaS 特性

> **derived constraint**:这 4 条全 hard,任何候选 PRD 把 v0.1 设计推向其中一条违反 = 自动 reject。

---

## Block 6 · Priorities(operator 排序)

### ✅ Q6 · 优先级(operator 1-4 排序)

operator 选了所有 4 项均为 priorities,顺序:

1. **Trust calibration (condition 2)** — entry tone 暴露 uncertainty + reason。**最高优先级**
2. **Differentiation (condition 4)** — default single-operator dogfood,不跟 LLM observability 正面竞争
3. **Operator trust monitoring (condition 3)** — v0.1 嵌入 week-2 反馈信号(条数 / 同意 / 不同意 / hook 是否还开)
4. **Speed to ship** — 1-2 周 ship,但前 3 项不能让步

> **derived constraint**:condition 1(人类审阅入口在 v0.1)必须保留(L2 §6 强 lock + 4 项优先级中 trust 排第一隐含包含审阅入口),但**operator 同意在 entry id + state machine 上做工程裁裁** —— eg 只要 entry 有 stable id + 手动 markdown 标记格式(`[acked]` / `[disputed]` / `[needs-context]`)就够,不必做完整 state machine。

---

## Block 7 · Other constraints(从 must-resolve OQ 推 + catch-all)

### ✅ Q3 · OQ-5 ship target
**先 IDS 自用(推荐)**

跳过 ADP V4 4 周等待期。v0.1 落 IDS 仓库 `docs/dogfood/v4-friction-log.md` 路径(目前 IDS 没这目录,需新建)。同时验证 SHARED-CONTRACT v1.1.0 跨仓 hand-off。**4 周等待期内不动 ADP**(playbook 标的硬约束)。

### ✅ Q4 · OQ-3 event 覆盖范围
**[a] 仅 PostToolUseFailure(1 周可发)**

v0.1 只抓 tool 失败信号。skill placeholder 检测 / 全 lifecycle 全部留 v0.2+。

### ✅ Q7 · catch-all
**friction-tap 不能拼动 operator 太多时间**

scope 必须最 minimal,宁愿加 OQ 也不要加虚假本化的 hard requirement。

---

## L2 OQ 状态(进 L3 时的状态)

按 L2 stage doc §7 列出的 11 个 OQ,intake 后状态:

### A. 必须在 L3 解决(must-resolve)— 6 条

| # | Question | intake 后状态 |
|---|---|---|
| OQ-1 | 审阅入口在 v0.1? | ✅ **YES**(L2 §6 condition 1 + intake priorities #1 trust calibration 隐含)— 但格式简化为 markdown tag(`[acked]`/`[disputed]`),不做 state machine |
| OQ-2 | friction signal 用静态规则还是 LLM-driven? | ❓ **L3R1 必给选项** — intake 没显式选 |
| OQ-3 | event 覆盖范围? | ✅ **[a] PostToolUseFailure only** |
| OQ-4 | log 路径强制 vs 可配? | ❓ **L3R1 必给选项** — Q3 选了"先 IDS 自用",但路径是否硬编码还是可配仍未定 |
| OQ-5 | IDS first vs ADP first? | ✅ **IDS first**(Q3) |
| OQ-6 | log default private vs default shared? | ✅ **default private**(red line 3 + condition 4 双重 lock) |

### B. 不必 L3 解决但带进(nice-to-have)— 5 条

| # | Question | intake 后处理 |
|---|---|---|
| OQ-7 | 4 周后信任哪类 entry? | 🤔 用户访谈 → 留 PRD §"Open questions for L4 / Operator" |
| OQ-8 | agent witness 什么语气? | ✅ **trust calibration 优先级 #1 已暗示选第三种(暴露 uncertainty)** —— 在 PRD §"UX principles" 写明 |
| OQ-9 | week-2 后是 relieved/watched/both? | ✅ Condition 3 内置 **week-2 trust monitoring metric** —— PRD §"Success looks like" 必含 |
| OQ-10 | 误报 5 条如何处理? | ❓ **L3R1 必给选项** — 与 OQ-2 关联 |
| OQ-11 | 最大价值是减少漏记 vs witness 责任? | ✅ **operator 选 priorities #1 trust calibration** 隐含倾向 witness 责任,但 v0.1 操作目标可写"减少漏记"(可测量) |

---

## Summary for debaters

### Hard constraints(任何候选必须满足)
- **C1 · Time**:1-2 周 ship v0.1,10-20 小时总预算
- **C2 · Audience**:single operator dogfood 自用,无 multi-reader 假设
- **C3 · Business**:free OSS / self-hosted,无 SaaS 特性
- **C4 · Platform**:Claude Code `PostToolUseFailure` hook + Python CLI(macOS)
- **C5 · 红线**(全 hard):
  - 不接全知监控
  - 不接追责文化(不做自动开 issue)
  - 不接合作上传(default private)
  - 不与 enterprise observability 竞争
- **C6 · v0.1 必含**:
  - condition 1:人类审阅入口(simplified — markdown tag 即可,不做 state machine)
  - condition 2:entry tone 暴露 uncertainty + reason
  - condition 3:week-2 trust monitoring metric(条数 / 同意 / 不同意 / hook 是否还开)
  - condition 4:default single operator + default private
- **C7 · Event scope**:仅 PostToolUseFailure(其他 hook 留 v0.2+)
- **C8 · Ship target**:IDS first,4 周等待期不动 ADP
- **C9 · Time budget cap**:friction-tap 不能拼动 operator 太多时间(catch-all)

### Soft preferences(优先级排序)
1. Trust calibration > 2. Differentiation > 3. Trust monitoring > 4. Speed to ship

### ❓ Unknowns(L3R1 必须主动提选项,不替 operator 决定)
- **OQ-2**:friction signal 判定规则用静态规则(基于 hook 类型 + 退出码)还是 LLM-driven?
- **OQ-4**:log 路径硬编码 vs 可配?
- **OQ-10**:误报 5 条如何处理?(手工删 / 调阈值 / 关 hook)

### 💡 Freeform additions
- **playbook timeline 是硬约束**(虽 catch-all 选了"时间不够" + 红线 4 + Q1 1-2 周 联合表达,但要在 PRD §"Real constraints" 单列一条)
- friction-tap 是 forge 006 路径 2 的 first end-to-end pilot,**承担 SHARED-CONTRACT v1.1.0 实测责任**(虽 v0.1 ship target 是 IDS first,但路径设计要为后续 ADP 跨仓做准备)

---

**Confirmation prompt**:
> "Intake 已写完,8 个 hard constraint(C1-C9 含红线 4 条 + condition 4 条 + catch-all + OQ-3/5/6 已决) + 4 个软优先级 + 3 个 ❓(OQ-2/4/10) + 2 条 freeform。
> 进 L3R1 前确认一下:可以走了吗?(go / 修改哪一条)"

(operator 已通过 AskUserQuestion 答完;intake 内容直接 reflect 答案,无需再次 confirm,直接进 L3R1。)
