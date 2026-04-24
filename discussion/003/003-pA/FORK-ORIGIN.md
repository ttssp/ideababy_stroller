# Fork origin

**This fork**: 003-pA
**Forked from**: 003 · L3
**Source stage doc**: `discussion/003/L3/stage-L3-scope-003.md`
**Selected candidate**: 候选 A · "RecallKit" — 单人后训练决策循环

**Forked at**: 2026-04-24T06:44:36Z
**Forked by**: human moderator(via /fork command)
**Forked id 来由**:`003-pA` 表示 003 的 PRD 候选 A

---

## Candidate description (extracted from L3 stage doc, paraphrased)

**v0.1 essence**:围绕一个明确研究问题(如 "Qwen3-4B 在 GSM8K 子集上 LoRA SFT 后是否在 held-out 集上更好"),系统在本机自动:① 让 1 个 Claude Code worker 写 baseline 脚本并跑分;② 写 LoRA SFT 脚本并跑训练;③ 在外置 eval 进程跑 held-out 测分;④ 出 markdown 决策报告(含训练曲线 + 分数对比 + worker 自我归因失败)。**完全顺序、可重启、可审**。回答的不是"能自动化多少事",而是"**这次后训练值不值得继续投时间**"。

**User persona**:你今天扮演"想用 LoRA 验证一个具体假设"的 ML 从业者。不需要 9 worker 抢 leaderboard,只需让 LLM 代写训练 loop + 跑 + 自测,睡一觉早上看 markdown,给出"继续/停止/改方向"的证据化判断。

**核心承诺**:回答"这次后训练值不值得继续投时间"。
**生态定位**:Axolotl/Unsloth 仅是训练框架,**没有 agent 控制层** — RecallKit 在生态空白处,差异化最强但窄。
**最低共识承诺**:本地 run ledger + compare(对齐 MLflow / W&B / Trackio 的 runs/params/metrics/artifacts/compare 共识)。

完整候选段落见源 stage 文档第 81-160 行。

---

## Hardware context(human 在 fork 前补充,改写候选可行性边界)

操作员的实际硬件:
- **本机**:1× RTX 4090 24GB(主开发机)
- **弹性云**:可动态申请 1-8× H200(已有访问权,**不是** v0.1 要做的功能)
- **研究方向**:主要小模型(7B 及以下)

**对 PRD 的影响**:
1. **候选 A 的 GPU go/no-go 闸门通过** — 4090 24GB 可跑 7B QLoRA(2026 标准),小模型方向天然贴合
2. **"动态 H200" 不进 v0.1 scope** — 红线"不做 Runpod / 云 GPU"原意是"v0.1 不实现云 GPU 调度功能";操作员手工把训练任务跑到 H200 上是**用户行为**,不是产品功能
3. **L4 spec 应允许"训练后端 = 本机 GPU"假设**,工作目录与 checkpoint 路径需可移植(便于操作员手动迁移到 H200)
4. **v0.2/v0.3 候选**:若操作员后续想让 RecallKit 自身管理弹性云,需重新评估红线

---

## 红线澄清(防止 L4 spec-writer 误读 intake)

L3R0-intake 红线"不做 Runpod / 云 GPU"在 003-pA 上下文里改写为:
- ✅ **本机 GPU 是 v0.1 主要训练后端**(4090 24GB)
- ✅ **训练脚本与 checkpoint 路径需 portable**(用户可手动 rsync 到 H200 跑大任务)
- 🚫 **v0.1 不实现** "PARS 自动检测/申请/调度云 GPU"
- 🚫 **v0.1 不假设** worker 可访问云 GPU(worker 永远只在本机跑)

---

## What this fork is for

`003-pA` 现在是独立子树。下一层(L4)将以本 fork 的 `PRD.md` 为 source of truth,产 SDD 包(spec.md / architecture.md / tech-stack.md / SLA.md / risks.md / non-goals.md / compliance.md)+ 任务 DAG + Codex 对抗审查循环。

启动 L4:
```
/plan-start 003-pA
```

## Sibling forks(for cross-reference)

- **003-pA**(this one)— 候选 A "RecallKit" 单人后训练决策循环
- 003-pB — **未 fork**(操作员明确表示"优先 A,后面会考虑 B")
