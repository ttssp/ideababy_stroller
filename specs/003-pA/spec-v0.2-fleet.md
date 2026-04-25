# Spec 增量 — 003-pA · v0.2 "Fleet Mode"

**Version**: 0.2.0-dev
**Created**: 2026-04-24
**Base spec**: `specs/003-pA/spec.md` v0.2.2(v0.1.0 已 ship,tag = `v0.1.0_idea003`)
**Bump 类型**: minor(scope 扩展,无契约破坏)
**Source**: 操作员 2026-04-24 澄清 — 实际工作场景是单人在自己机器上**并行追踪 8-15 个研究方向**,目标聚焦在 4-6 个并行实验线。
**Lineage**: 003 → 003-pA(v0.1 单 worker 已交付)→ v0.2 在同 PRD 下扩展并行能力
**OQ 决策**: OQ-v02-1=A(macOS 排除训练,仅 status/compare 可用)· OQ-v02-2=阻塞(不 daemonize)· OQ-v02-3=不实现 DAG 依赖

---

## 0. TL;DR

v0.1 是"单 worker 单循环"。v0.2 加 **fleet mode**:**单 operator 同时管理 4-6 个并行实验线**,共享本机 GPU(1× 4090)+ 弹性 H200(1-8 张)。

四个增量:
1. `pars fleet status` — 一眼看到所有 active runs 的 phase/budget/ETA(消除"得 cat N 个 state.json"痛点)
2. `pars fleet start <batch.yaml>` — 一次声明 N 个 run + GPU 分配,**阻塞前台跑 dashboard**
3. **GPU lock manager** — 同一 GPU 同一时间只一个 worker(避免 OOM 误杀)
4. `pars fleet compare` — 跨 N 个 run 的总览矩阵(每方向当前最佳 + delta)

**强制留白**:v0.2 不引入任何 LLM-driven 自动 surface / 自动 retry 决策。理由:Phase B(独立研究项目"多 agent 研究协作")需要 v0.2 真实使用 6 周积累的 painful 数据作为输入;若 v0.2 提前实现 LLM-driven surface,会用"凭直觉的 v0"代替"基于真实数据的 v1",Phase B 价值大打折扣。

---

## 1. 增量 Outcomes(对齐 v0.1 O1-O7,不替换)

| ID | 描述 | 验证 |
|---|---|---|
| **O8** | operator 离开电脑 30min 回来,执行 `pars fleet status` 可在 < 5 秒内看到所有 active runs 的 phase/已花预算/估算剩余时间 | T029 + e2e |
| **O9** | 一次声明 4-6 个 run 后,fleet 自动按 GPU 可用性串行启动,**不发生 GPU OOM** | T030 + T031 + e2e |
| **O10** | `pars fleet compare` 给出 4-6 个 run 的总览矩阵 + 每个方向"当前最佳 run id" + 跨方向 verdict("方向 X 已收敛,可停") | T032 + e2e |
| **O11** | v0.1 已有的 7 个 Outcome 全部仍然成立(向后兼容 gate) | 全量 regress run v0.1 e2e |

---

## 2. Scope Boundaries

### 2.1 In scope for v0.2

- **`pars fleet status`**:CLI 列出所有 `runs/*/state.json` 的当前 phase / 已花 USD / wall_clock 已用 / ETA(基于剩余 epoch 估算)
- **`pars fleet start <batch.yaml>`**:声明 N 个 run config(每个含独立 question / dataset / hyperparam),阻塞前台跑 dashboard,自动批量启动
- **GPU lock manager**:`runs/.gpu_locks/<gpu_uuid>.lock` 文件,单 GPU 同时只允许一个 worker;新 worker 启动前先 acquire,失败则 wait(可配 max_wait_minutes)
- **`pars fleet compare`**:跨 N 个 run 的 markdown 矩阵 + 每方向最佳 verdict
- **macOS 仅 status/compare**(OQ-v02-1=A):Mac 上 `pars fleet start` 直接 refuse + 提示"v0.2 fleet 训练仅支持 NVIDIA GPU,请在 4090/H200 机器跑"
- **Backward compat**:v0.1 的 5 个命令(start/resume/retry/compare/unlock)行为完全不变

### 2.2 Explicitly out of scope for v0.2

- ❌ 多用户/多 operator 并发(仍是单人)
- ❌ 远程 GPU 调度(H200 是 operator 自己 ssh 进去手跑)
- ❌ LLM-driven surface / 自动 retry 决策(留 Phase B)
- ❌ Web UI / dashboard server(CLI rich 表格)
- ❌ 跨机器 fleet 视图(C22 跨机硬拒绝原则保留)
- ❌ GPU 抢占 / 优先级 / 队列管理(简单 lock + FIFO wait,不做调度器)
- ❌ fleet-level budget aggregate(per-run 预算独立)
- ❌ daemonize / 后台 detach(OQ-v02-2 接受默认 = 阻塞)
- ❌ batch.yaml DAG 依赖(OQ-v02-3 接受默认 = `depends_on` 字段保留但 warning+忽略)
- ❌ macOS 真实训练(OQ-v02-1 接受默认 = scope 排除)

### 2.3 留给 Phase B(新 idea,不在 003-pA 树)

- agent 自动决定"哪个方向该 surface 给我了"
- agent 自动决定"哪个方向已收敛,可以停"
- 跨方向 retro learning("这个学期我学到了什么")
- multi-agent 协作模式(主 agent + N 个 sub-agent)

---

## 3. 增量 Constraints

### 3.1 来自 v0.1 的不变约束(再次声明)

- 单人单机,API key 不入 worker(C15)
- USD 真硬帽 proxy 前置拒绝(C20)
- `.claude/` fail-closed(C21)
- 跨机 resume 硬拒绝(C22)

### 3.2 v0.2 新增约束

- **C23 · GPU lock 互斥**:同 GPU UUID 同时刻只一个 worker。lock 用 `fcntl.flock`(Unix)+ atomic 文件创建。stale lock(进程已死)自动清理(检查 PID + start_time)。
- **C24 · fleet status 性能**:列 ≤ 50 个 active run 必须 < 5s 返回(目标:聚合 stat call,不真实读 metrics.jsonl 全文)。
- **C25 · batch DAG 不实现**:batch.yaml 可声明 `depends_on: <run_id>`,但 v0.2 行为是 warning + 忽略。完整实现留 v0.3。
- **C26 · GPU UUID 是 lock 唯一标识**(不是 device index,因为 CUDA_VISIBLE_DEVICES 切换会让 cuda:0 指向不同卡 → lock 失效)。
- **C27 · macOS fleet start 直接 refuse**(OQ-v02-1=A):检测 platform.system() == "Darwin" → exit 2 + 引导信息。fleet status / compare 在 mac 仍工作。
- **C28 · 阻塞模式**(OQ-v02-2):`pars fleet start` 不支持 `--detach`。Ctrl+C 后 fleet 命令退出但 worker subprocess 仍在跑(因为 RunOrchestrator 已 fork);operator 新开 terminal `pars fleet status` 可继续监控。

---

## 4. 增量 Prior Decisions

### D20 · GPU lock 用文件锁,不用数据库
理由:fleet 不需要事务、不需要历史。文件锁(fcntl)+ stale 检测即可。如果未来要做 cross-machine fleet 才上 SQLite/Redis。

### D21 · `pars fleet start` 是阻塞命令(前台跑 dashboard · OQ-v02-2)
理由:fleet mode 的核心卖点 = dashboard。阻塞 + Ctrl+C 安全退出已覆盖 90% 场景。daemonize 多很多 edge case(孤儿 worker / PID 复用 / 启动失败清理)。

### D22 · `pars fleet status` 不需要 daemon
理由:每次 invoke 即时 scan `runs/` + `runs/.gpu_locks/` 即可。没有"实时推送"。Phase B 做 dashboard 时再考虑。

### D23 · batch.yaml 格式
```yaml
fleet_name: 2026-W17-qwen-arch-search   # 用于 status 分组显示
gpu_strategy: auto                       # auto = 按 nvidia-smi 自动分配; manual = 严格按 gpu_uuid
runs:
  - name: r16-ep3
    base_model: Qwen/Qwen2.5-3B-Instruct
    dataset: openai/gsm8k
    dataset_split: "main[:200]"
    lora_rank: 16
    epochs: 3
    usd_cap: 5.0
    wall_clock_hours_cap: 4
    gpu_uuid: GPU-aaaa-bbbb-...   # 可选,留空 = auto;manual 模式必填
    depends_on: null              # v0.2 保留字段,行为是 warning+忽略(C25)
  - name: r32-ep3
    ...
```

### D24 · fleet status 的 ETA 估算
最简单:`ETA = (epochs_remaining * (wall_clock_so_far / epochs_done))`;`epochs_done < 1` 时显示 `"--"`。**不**做复杂回归。

### D25 · v0.2 暂不改 RunOrchestrator
v0.1 的 RunOrchestrator 是"启动 1 个 worker + 跑完 + cleanup"。v0.2 的 fleet 在它**之上**编排,不进入 orchestrator 内部。`pars fleet start` 等价于"对 batch 中每个 run 调一次 RunOrchestrator.start(),但用 GPU lock 控制启动时机"。这样保证 v0.1 e2e 测试 100% 不受影响。

### D26 · macOS fleet start 行为(OQ-v02-1=A)
检测平台:
- `platform.system() == "Darwin"` → fleet start exit 2 + 打印"v0.2 fleet 训练不支持 macOS,请在 NVIDIA GPU 机器跑"
- fleet status / compare 在 mac 仍正常(只读 runs/ 目录,不需要 GPU)
- 未来 v0.3 如真要支持 mac mlx-lm,新开 OQ 重新评估

---

## 5. Task Breakdown(phase 4 — fleet)

| Task | 主题 | 估时 | 文件域 |
|---|---|---|---|
| T029 | `pars fleet status` + GPU lock 状态 surface | 5h | `pars/cli/fleet.py`(部分)+ `pars/fleet/__init__.py` + `pars/fleet/status.py` + `tests/unit/test_fleet_status.py` + `tests/integration/test_fleet_status.py` |
| T030 | `pars fleet start <batch.yaml>` + batch parse + 阻塞 dashboard | 6h | `pars/cli/fleet.py`(部分)+ `pars/fleet/batch.py` + `pars/fleet/dispatcher.py` + `pars/fleet/dashboard.py` + tests |
| T031 | GPU lock manager(C23 · C26 · stale 检测) | 5h | `pars/fleet/gpu_lock.py` + `pars/fleet/gpu_probe.py` + tests |
| T032 | `pars fleet compare` 跨 N run 矩阵 + e2e 套 | 4h | `pars/cli/fleet.py`(部分)+ `pars/fleet/cross_compare.py` + `tests/e2e/test_fleet_*.py` |

总计 ~20h(net code)+ 5h Codex review + 5h 文档 + 5h e2e = **~35h**(2-3 周晚上跑完)。

依赖图:
```
T031 (GPU lock)  ──┐
                   ├──→  T030 (fleet start) ──→  T032 (fleet compare + e2e)
T029 (fleet status)┘
```

T029 + T031 可 2-way 并发(disjoint file_domain)。
T030 依 T031(start 必须先能 acquire lock)。
T032 依 T030(compare 用 fleet 跑出的 run)+ 已有 T025 compare engine。

---

## 6. Verification Criteria(增量)

- [ ] **O8 操作**:跑 4 个 run → 等其中一个进入 lora_train phase → `pars fleet status` < 5s 返回 + 显示 4 行,各 phase 正确
- [ ] **O9 GPU lock**:1 GPU 机器上启动 batch(2 run)→ run-1 跑、run-2 排队 → run-1 完成后 run-2 自动启动 → 无 OOM
- [ ] **O10 cross compare**:跑 batch(3 run,不同 lora_rank)→ `pars fleet compare 2026-W17-qwen-arch-search` → 输出含 "best run = ..." + 每方向 winner
- [ ] **O11 v0.1 regress**:`uv run pytest -m "not slow and not gpu"` 仍 639 passed / 0 failed
- [ ] **C27 mac refuse**:在 macOS 跑 `pars fleet start any.yaml` → exit 2 + 提示信息
- [ ] e2e:fleet 套(O8/O9/O10)新增至少 5 test 在 `tests/e2e/test_fleet_*.py`
- [ ] CHANGELOG bump 0.2.0,LICENSE/README 增量段说明 fleet mode

---

## 7. 与 Phase B(未来研究项目)的边界

v0.2 是 **被动工具**:
- status = 你问才告诉你
- compare = 你 invoke 才算
- 所有"该不该 retry / 该不该停"的判断 = 你自己看了再决定

Phase B 是 **主动 agent**:
- agent 看完 fleet status 后**主动告诉你**"方向 3 该看了"
- agent 看完 compare 后**主动建议**"r=64 试一试"
- agent 跨 4-6 个方向做 retro learning

**v0.2 必须不引入任何 LLM call** 在 fleet 路径上,否则 Phase B 无法被独立验证。

---

## 8. 风险

### R12 · GPU UUID 解析依赖 nvidia-smi
**Why**: `nvidia-smi --query-gpu=uuid --format=csv` 在 macOS 没有,在没有 NVIDIA 的 Linux 也没有。
**How to apply**: macOS 通过 C27 直接 refuse,问题不发生。其它 fallback 场景(无 nvidia-smi 的 Linux)→ `pars/fleet/gpu_probe.py` 用 hostname + cuda:N index 拼伪 UUID + warning。

### R13 · stale lock 检测竞态
**Why**: worker 进程崩溃后 lock 文件残留,fleet 启动时检测 PID → 若 PID 已被新进程复用,误判 alive。
**How to apply**: lock 文件含 `pid + start_time + worker_run_id`;PID 复用极少且 start_time 不会一致;若全部一致,接受 < 1ppm 概率的伪 alive(operator `pars fleet unlock-gpu <gpu_uuid>` 手工解)。

### R14 · v0.1 e2e 套被改坏
**Why**: 有诱惑改 RunOrchestrator 让它"知道 fleet"。这会破坏 v0.1 契约。
**How to apply**: D25 已固定。v0.2 task 文件 file_domain 明确不包含 `pars/orch/orchestrator.py`。Codex review 必须 catch。

### R15 · 阻塞模式 + Ctrl+C 后孤儿 worker(D21 · OQ-v02-2)
**Why**: fleet 命令 Ctrl+C 后,各 run 的 worker subprocess 仍在跑,如果 worker 自己也卡死 → 没人清理。
**How to apply**: 各 worker 仍有自己的 stuck monitor + budget monitor + 自己的 SIGINT 处理(v0.1 已实现);fleet 退出不影响这些。文档明确"Ctrl+C 后用 `pars fleet status` 监控,不要 kill -9 fleet pid"。

---

## 9. Non-goals(显式拒绝)

- v0.2 不引入 LLM-driven 决策(留给 Phase B)
- v0.2 不做远程 / 多机 fleet(C22 原则保留)
- v0.2 不做调度器 / 优先级队列(简单 lock + FIFO 即可)
- v0.2 不做 Web UI / 实时 dashboard(CLI rich 表格)
- v0.2 不改 v0.1 任何 module 的契约(orchestrator / proxy / monitors 不动)
- v0.2 不在 macOS 上支持训练(OQ-v02-1=A)
- v0.2 不支持 daemonize / detach(OQ-v02-2 接受默认)
- v0.2 不实现 batch DAG 依赖(OQ-v02-3 接受默认)

---

## 10. 已 lock-in 的 OQ 决策

- **OQ-v02-1=A**:macOS 排除训练,fleet status/compare 仍可用
- **OQ-v02-2=阻塞**:fleet start 前台跑 dashboard,Ctrl+C 安全退出,worker 不死
- **OQ-v02-3=不实现 DAG**:batch.yaml `depends_on` 字段保留但 warning+忽略

未来 v0.3 重新评估解锁条件:
- mac 上跑 mlx-lm 真实需求出现 → 解锁 OQ-v02-1
- 想 cron 自动触发 fleet → 解锁 OQ-v02-2
- "链式实验"频繁出现 → 解锁 OQ-v02-3

---

## 11. v0.2 不变的 v0.1 文件(file_domain 红线)

下列文件 v0.2 任何 task 不应触碰(违反 = scope 违例 = Codex BLOCK):
- `pars/orch/orchestrator.py`
- `pars/orch/worker.py`
- `pars/orch/worker_env.py`
- `pars/orch/worktree.py`
- `pars/orch/machine_fingerprint.py`
- `pars/orch/resume.py`
- `pars/orch/retry.py`
- `pars/orch/env_snapshot.py`
- `pars/proxy/**`
- `pars/safety/**`
- `pars/stuck/**`
- `pars/budget/**`
- `pars/ledger/**`
- `pars/report/**`
- `pars/workflow/**`
- `pars/compare/engine.py`(可 import,不可改)
- `pars/cli/start.py / resume.py / retry.py / compare.py / unlock.py / status.py`(允许在 main.py 加 1 行挂 fleet 子命令)

v0.2 新增文件全部在:
- `pars/cli/fleet.py`(新)
- `pars/fleet/**`(新模块树)
- `tests/unit/test_fleet_*.py`
- `tests/integration/test_fleet_*.py`
- `tests/e2e/test_fleet_*.py`
- `tests/fixtures/fleet/*.yaml`
