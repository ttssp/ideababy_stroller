> ⚠ **DEPRECATED — 2026-05-10 起不再维护**
>
> forge 006 v2 verdict(`discussion/006/forge/v2/stage-forge-006-v2.md`)决议 IDS 退回 idea→PRD + 治理,
> 不再产 `specs/`;build runtime 由新建的 XenoDev 仓承担(per `framework/SHARED-CONTRACT.md` §6 v2.0 草稿)。
>
> 本 spec 保留作 forge v2 evidence(stage doc §"Evidence map" row 13);
> 不再加新 task,不再做 review。新 PRD 走 `discussion/<id>/<fork>/L4/HANDOFF.md` → XenoDev 消费。

# Spec — 003-pA · "RecallKit" 单人后训练决策循环

**v0.2 增量**: 见 `specs/003-pA/spec-v0.2-fleet.md`(fleet mode · 4 个 T029-T032 task · v0.1 完全向后兼容)

**Version**: 0.3.0-dev (主版号 bump:v0.1.0 已 ship + v0.2 fleet mode 规划中)
**Previous**: 0.2.2
**Created**: 2026-04-24 · **Updated**: 2026-04-24 (v0.2.2 · 操作员 OQ1/OQ2/OQ5 决策 lock-in · 不改 scope)
**Source PRD**: `discussion/003/003-pA/PRD.md` (v1.0, human-approved)
**Lineage**: 003 (PARS 14 周方案 L2 → L3 候选 A → 003-pA PRD)
**关联**: `discussion/003/L3/L3R0-intake.md`、`discussion/003/L3/moderator-notes.md` (47/100, 仅消化 v0.1 相关项)
**R1 对抗审查**: `.codex-outbox/20260424T071844-003-pA-L4-adversarial-r1.md` (BLOCK · 3 blocker + 5 high + 4 med-low,v0.2 解决 3 blocker + 5 high)
**R2 对抗审查**: `.codex-outbox/20260424T081730-003-pA-L4-adversarial-r2.md` (BLOCK · B1/H1/H2 STILL_OPEN + 1 new high + 2 regression,本 v0.2.1 文档 patch 精准修复)

---

## 0. 一页结论 (TL;DR)

**RecallKit v0.1**:CLI 驱动的"单人 × 单 worker × 单后训练循环"工具,让 1 个 `claude -p` headless worker 在 git worktree 里**严格顺序**跑 baseline → LoRA SFT → eval → markdown 决策报告(强制含失败归因)。10-12 周交付,本机 1× RTX 4090 24GB 假设,API key 不入 worker,pip 锁定,stuck 状态机白名单训练态,**USD 硬帽 proxy 前置拒绝(C20)**,**`.claude/` fail-closed 只读分离(C21)**,**跨机器 resume 不承诺(C22,仅手工 rsync 后远端重跑)**。**不做** Docker / 多 worker / 调度器 / Runpod / Web UI / forum / judge LLM。

**OQ1 CONFIRMED**:训练后端 = **Unsloth**(操作员于 2026-04-24 确认 · 理由见 §4 D7)
**OQ2 CONFIRMED**:评测后端 = **LM Eval Harness**(操作员于 2026-04-24 确认 · 理由见 §4 D8)
**OQ5 CONFIRMED**:`.claude/` 只读分离 = **MacFUSE + bindfs**(操作员于 2026-04-24 确认 · refuse-to-start 逻辑保留作防御)

---

## 1. Outcomes(对齐 PRD §6 O1-O7)

每条 outcome 都来自 PRD 原文,在此仅细化"如何观测"。

| # | Outcome | 来源 | 验证方式(见 §6) |
|---|---|---|---|
| **O1** | 一周内能跑完 1 个 baseline + 1-2 个 LoRA 变体 + 决策记录 | PRD §6 O1 | demo 跑通 + 计时 |
| **O2** | markdown 报告**必有**训练曲线 PNG + 分数对比表 + 失败归因文字 | PRD §6 O2 | 报告 schema 校验脚本 |
| **O3** | 重启电脑后 `pars sft resume` 能续上中断训练 | PRD §6 O3 | 集成测试 `test_resume_after_kill` |
| **O4** | README 给 1 个真实可复现 demo(即使是诚实负面 demo 也算 ship 成功) | PRD §6 O4 | 他人本机重现验收 |
| **O5** | 端到端单 run < 12h、< $30 API 费 | PRD §6 O5 | run ledger 自带计时 + budget tracker 累计 |
| **O6** | `pars compare runA runB` 输出可读差异表(config / metric / 结论) | PRD §6 O6 | 集成测试 `test_compare_two_runs` |
| **O7** | Stuck 检测在 LoRA 一 epoch 30-90min 全程不误杀 | PRD §6 O7 | 集成测试 `test_stuck_no_false_positive_during_lora_epoch` |

---

## 2. Scope Boundaries

### 2.1 In scope for v0.1(PRD §4)

**用户接口**
- CLI 命令套:`pars sft start / status / retry / report / compare / resume`
- 单一 markdown 决策报告作为最终产出物(强制含失败归因)

**执行模型**
- 1 worker **严格顺序**(无并行,无 forum,无 leaderboard,无 sidecar)
- worker = `claude -p` headless 进程,跑在 git worktree 里
- 全程可重启 / 可 resume(checkpoint 写盘到 worktree 外)

**训练后端**
- **CONFIRMED: Unsloth**(见 §4 D7 rationale · 操作员 2026-04-24 确认)
- 仅 LoRA SFT(不做 RLHF / DPO / RLOO 等其他后训练算法)

**评测后端**
- **CONFIRMED: LM Eval Harness**(见 §4 D8 rationale · 操作员 2026-04-24 确认)
- eval 进程**外置**(与 worker 进程分离),避免 worker 自评作弊

**Stuck 检测(关键)**
- 状态机区分:`idle / training / downloading / truly_stuck`
- 仅 `truly_stuck > 15min` 才 SIGINT
- 判据:GPU util / 子进程 CPU / 磁盘 IO / 网络 IO 任一活跃即 not stuck
- **唯一真相源 = `architecture.md §8` 的契约表**(采样周期、窗口语义、转移条件、disk/net 阈值、冷启动豁免策略、false negative 判定、`needs_human_review` 持久化);spec/task 所有引用点统一回指 §8

**Budget 控制(USD 硬帽前置拒绝,D-OP1)**
- **proxy 前置预估**:worker 每次 API 请求到达 proxy 时,proxy 按 (input_token_count × input_price + max_tokens × output_price + 20% 保守系数) 估算成本;**余额不足即返回 402/429,**不发出**上游请求**
- 失败 / 重试 / cache miss / artifact 生成等都同步入账(v0.1 不做 judge LLM,故 judge 成本 N/A)
- 60s 轮询 + SIGINT 降级为**第二道保险**(兜底,非主控制路径;`architecture.md §5` 明示)
- wall-clock / GPU hours 上限保留 60s 轮询 SIGINT 路径(非硬帽)
- 简单实现(proxy middleware + 文件 lock,**无** Redis、**无**复杂调度)

**本地 Run Ledger + Compare**
- 每 run 落 `runs/<id>/{config.yaml, metrics.jsonl, artifacts/, report.md, failure_attribution.md}`
- `pars compare runA runB`:跨 run 对比 config / 指标 / 结论
- 跨 run 引用允许(`pars sft retry --from <run-id>`)

**最小 Safety**
- API key 走环境变量(`ANTHROPIC_API_KEY`),**不**注入 worker 子进程环境
- **`HF_TOKEN` 例外条款(与 `architecture.md §1 / §5` 和 `tasks/T011.md` 对齐)**:默认公开 demo(Qwen3-4B / gsm8k)**无 `HF_TOKEN` 也能跑**;**仅在 gated 模型下载场景**允许由 orchestrator(**非 worker**)临时注入 **read-only scope** `HF_TOKEN` 到 worker env,下载完成后立即从 env 移除;`HF_TOKEN` 严禁含 write / private-mirror / write-repo 权限
- worker 走 API proxy(本机 localhost),proxy 持有 key + **预算预估前置拒绝**
- 最小 deny 清单:`rm -rf /` / `curl 外部` / `cat .env`
- `pip install` **仅允许**从锁定依赖文件(`pip install -r requirements-locked.txt --require-hashes` 或等价的 `uv pip install -r requirements-locked.txt --require-hashes` / `uv sync --frozen`);uv 路径由 uv 自身保证 lockfile + hash 一致性,与 pip `--require-hashes` 等价
- worker 工作目录与 host `.claude/` 配置**只读分离(fail-closed)**:
  - **CONFIRMED: MacFUSE + bindfs**(操作员 2026-04-24 确认)真只读 mount
  - **fallback 保留作防御**:`sudo chflags uchg`(macOS)/ `sudo chattr +i`(Linux)一次性装机步骤
  - **纯 `chmod -R a-w` 不被接受为生产路径**(可被 Python `os.chmod` 面绕过,见 C16 收紧版)
  - refuse-to-start 逻辑保留作防御:MacFUSE/fallback 都不可用时 v0.1 **refuse to start** 打印明确错误
- HF_TOKEN 最小 scope:默认场景(Qwen3-4B / gsm8k 公开 demo)**无 HF_TOKEN 也能跑**;需要 token 仅限 gated 模型,README 明示"最小 read-only scope、禁止 write / private mirror / write-repo 权限"

**决策报告**
- markdown 强制含:训练曲线 PNG + 分数对比表 + worker 自我归因(loss 上升明说,eval 退步明说)
- 不允许 LLM 美化("模型自己声称的提升"必须有 eval 数字 backing)

**文档**
- README + 1 个真实可复现 demo

### 2.2 Explicitly out of scope for v0.1(PRD §5 + spec 引申)

详见 `non-goals.md`。提纲:

- 多 worker 并行 / forum / leaderboard / sidecar
- prompt 优化 / agent scaffold 工作流(候选 B 剧本)
- workflow 插件契约 / 通用扩展接口
- 多研究问题并发
- RLHF / DPO / RLOO / 全参微调
- Multi-modal / vision 后训练
- 自研训练框架
- Docker / 容器化
- 复杂调度器(asyncio scheduler / GPU 分配信号量)
- Runpod / 云 GPU 自动调度(操作员手工 rsync 是用户行为,不是产品功能)
- Web UI / Streamlit dashboard / 任何 HTTP 服务器(仅本机 localhost API proxy 例外)
- 多用户 / 账号 / 权限系统
- LLM-as-judge / 自动种子扩展 / 文献挖矿 / Meta-review / 向量库 / 红队仿真
- 跨 run 知识迁移 / AgentRxiv 风格

---

## 3. Constraints

### 3.1 来自 PRD §7 的硬约束

| # | Constraint | Source | Rigidity |
|---|---|---|---|
| **C1** | v0.1 在 ~10-12 周内交付(2026-04-24 → ~2026-07 中) | PRD §7 C1 / L3R0 Block 1 | Hard |
| **C2** | 单人 × 30+ h/周 → 总预算 350-450h | PRD §7 C2 / L3R0 Block 2 | Hard |
| **C3** | OSS 免费,GitHub 即分发渠道(无 landing / 定价 / 注册) | PRD §7 C3 / L3R0 Block 3 | Hard |
| **C4** | 平台:CLI 优先,本地极简 web 可有可无(本 spec D6:不做 web) | PRD §7 C4 | Hard |
| **C5** | 训练后端假设 = 本机 GPU(1× 4090 24GB);**不实现**云 GPU 自动调度 | PRD §7 C5 + FORK-ORIGIN.md | Hard |
| **C6** | 不做 Docker / 多用户 / 复杂调度 / Runpod 集成 | PRD §7 C6 / L3R0 Block 5 | Hard |
| **C7** | 必须支持 LoRA SFT(单 GPU 单任务) | PRD §7 C7 / L3R0 Block 5 | Hard |
| **C8** | 优先级:速度 + 低成本 + 技术简单(三选三,互相强化) | PRD §7 C8 / L3R0 Block 6 | Hard |
| **C9** | 训练脚本与 checkpoint 路径**需可移植**(相对路径 + 环境变量),**允许**操作员手工 `rsync` 整个 `runs/<id>/` + `checkpoints/<id>/` 到远程 GPU 机器后**在远端重跑**训练;**不保证** 4090 ↔ H200 跨机器 resume 一致性(optimizer state / RNG seed 跨机器不一致),**不实现**自动同步(D-OP3 收窄) | PRD §7 C9 / FORK-ORIGIN.md / D-OP3 | Hard |
| **C10** | API key 不进 worker 容器 / worktree(env-only 或 proxy) | PRD §7 C10 / moderator P0-5 | Hard |

### 3.2 Spec 引申的工程约束

| # | Constraint | Source | Rigidity |
|---|---|---|---|
| **C11** | 单 run 端到端 < 12h、< $30 API(对齐 O5) | PRD §6 O5 | Hard |
| **C12** | Stuck 状态机误杀率 = 0(LoRA 一 epoch 30-90min 全程不误判,对齐 O7) | PRD §6 O7 / moderator P1-10 | Hard |
| **C13** | resume 成功率 > 95%(checkpoint 写在 worktree 外, **手工 kill** 后 `pars sft resume` 能续上,对齐 O3) | PRD §6 O3 | Hard |
| **C14** | 所有产物本地落盘,无云传输(privacy by design,对齐 PRD UX 原则 5) | PRD §8 UX 原则 5 | Hard |
| **C15** | worker subprocess 不持有 `ANTHROPIC_API_KEY` 环境变量(env-only 在 host,proxy 中转) | moderator P0-5 | Hard |
| **C16** | host `.claude/`(hooks / settings)对 worker 只读;worker 仅在 worktree 与 `runs/<id>/` 可写 | moderator P0-2 | Hard |
| **C17** | `pip install` 在 worker 内仅允许 `pip install -r requirements-locked.txt --require-hashes`,禁止任意 `pip install <pkg>` | moderator P0-6 | Hard |
| **C18** | LoRA stuck 状态机走**白名单**(显式枚举 4 态),不走启发式黑名单 | moderator P1-10 | Hard |
| **C19** | bus-factor 风险接受(单人 OSS 项目),v0.1 不做交接 runbook | spec 决策 | Soft(明示) |
| **C20** | **USD 硬帽前置拒绝**:proxy 必须在 request 前预估成本,余额不足即返回 402/429 不发上游请求;60s 轮询 SIGINT 仅为第二道保险 | D-OP1(R1 BLOCKER #2 修复) | Hard |
| **C21** | **`.claude/` fail-closed 只读分离**:生产运行**必须**走"真只读 mount"(MacFUSE + bindfs)或"immutable flag"(chflags uchg / chattr +i);纯 `chmod -R a-w` 不是可接受的生产路径;若二者都不可用,CLI **必须 refuse to start** 打印可操作错误 | D-OP2(R1 BLOCKER #3 修复) | Hard |
| **C22** | **跨机器 checkpoint 兼容性**:v0.1 **只承诺**"脚本 + checkpoint 手工 rsync 后在远端重跑训练";**不承诺** optimizer / RNG / CUDA 版本跨机器一致性;resume 语义**仅限同机重启** | D-OP3(R1 HIGH #2 + C9 收窄) | Hard |

---

## 4. Prior Decisions

下表记录"L4 接手前已经被锁定"的决策,**不在本 spec 内重新讨论**。每条引用源头。

| # | Decision | Source | 备注 |
|---|---|---|---|
| **D1** | 一次跟一个研究问题,1 worker 严格顺序 | L3 stage doc 候选 A §Scope IN / PRD §4.2 | 反例(多研究问题并发 / 多 worker)被 L3 显式淘汰("被淘汰候选")|
| **D2** | 不做 LLM-as-judge,完全人审 + 客观 metric | L3 stage doc 候选 A §Scope OUT / PRD §5.5 | 反例 moderator P1-11 在本项目 N/A,因为 v0.1 根本不做 judge |
| **D3** | 不做 forum / leaderboard / sidecar | L3 stage doc "❓ 决议表"行 forum / sidecar / 候选淘汰 §"主线 + 摘要搭档"| sidecar 价值不硬,候选 B 也不上 |
| **D4** | 不做 Docker / Runpod / 复杂调度 | L3R0 intake Block 5 红线 / PRD §5.4 | 红线,**不可越线** |
| **D5** | 仅 LoRA SFT,**不**做 RLHF / DPO / RLOO / 全参微调 | L3 stage doc 候选 A §Scope OUT / PRD §5.3 | v0.2 议题 |
| **D6** | 不做 Web UI / Streamlit dashboard / HTTP server(仅本机 localhost API proxy 例外) | PRD §5.4 / L3R0 intake Block 4 + Block 6"技术简单" | CLI 即一切;`pars status` 文本输出 |
| **D7** | 训练后端 = **Unsloth**(**OQ1 CONFIRMED 2026-04-24**) | spec-writer 决策 · 操作员确认 | 见 `tech-stack.md` D7 详细 rationale |
| **D8** | 评测后端 = **LM Eval Harness**(**OQ2 CONFIRMED 2026-04-24**) | spec-writer 决策 · 操作员确认 | 见 `tech-stack.md` D8 详细 rationale |
| **D9** | 主语言 = Python 3.12+(uv 管理) | L2 §4.2 + 训练生态默认 | Axolotl/Unsloth/HF 生态 = Python |
| **D10** | API key 隔离方案 = **本机 localhost API proxy**(LiteLLM 或最简自写),worker 子进程 env 中**无** key;**proxy 同时持有 budget 预估权**(C20):请求进 proxy → 预估 USD → 余额不足拒请求;60s 轮询 SIGINT 仅为兜底 | moderator P0-5 + PRD §7 C10 + D-OP1 | 见 `architecture.md` §5 API Key 隔离 + §5.x 预算预估 |
| **D11** | host `.claude/` 与 worker worktree 走 **fail-closed 只读分离**:首选 MacFUSE+bindfs 真只读 mount;fallback immutable flag(chflags uchg / chattr +i);纯 chmod 不是生产路径;缺上述二者 → refuse to start(C21) | moderator P0-2 + L3R0 红线"不做 Docker" + D-OP2 | 见 `architecture.md` §6 配置只读分离 |
| **D12** | pip 供应链:worker 内仅允许 `pip install -r requirements-locked.txt --require-hashes`,deny `pip install <任意包>` | moderator P0-6 | hook 拦截 |
| **D13** | Stuck 状态机:**白名单 4 态**(`idle / training / downloading / truly_stuck`),仅 `truly_stuck > 15min` 才 SIGINT | moderator P1-10 + PRD §4.5 | 见 `architecture.md` §"Stuck 状态机" |
| **D14** | run id 命名 = **ULID**(时间可排序 + 唯一,操作员可读) | spec-writer 决策(回应 PRD OQ6) | `pars sft start` 自动生成,可被 `--name` 覆盖 |
| **D15** | worker 写训练脚本:**模板修改**(PRD OQ4 选模板路线) | spec-writer 决策(回应 PRD OQ4) | 减少幻觉 + 可控;模板存 `templates/` 下,worker fill blank |
| **D16** | "失败归因"schema = **半结构化**(必填字段 + 自由叙述段) | spec-writer 决策(回应 PRD OQ5) | 见 `architecture.md` §"决策报告 schema" |
| **D17** | 暂**不**引入"研究问题 = 多 run 集合"概念(回应 PRD OQ7,v0.1 一次只跟一个研究问题,跨 run 通过 `pars compare` 与 `pars sft retry --from` 完成) | PRD §5.2 | 简化 v0.1,v0.2 再说 |
| **D18** | Operating mode:**本机为限**,worker 不访问云 GPU;训练脚本与 checkpoint 路径走相对路径 + env var,**仅承诺 "手工 rsync 后远端重跑"**(非 "跨机 resume"),resume 语义严格限同机重启(C22) | PRD §7 C9 + FORK-ORIGIN.md + D-OP3 | 见 `architecture.md` §10 路径可移植(收窄版) |
| **D19** | LICENSE = **MIT**(对齐 C8 速度+简单优先) | spec-writer 决策 | 见 `compliance.md` |
| **D20** | "诚实负面 demo" 是合法 ship 标准(即使 LoRA 没真提升 baseline 也算成功) | PRD §6 O4 / L3 stage doc 诚实检查 §2 | README 明示这一立场 |

### D7 / D8 推荐理由摘要(详见 `tech-stack.md`)

**D7 · Unsloth 优于 Axolotl 的关键点**(在 4090 24GB + 7B QLoRA 场景下):
1. 速度优势 ~2x(用其 fused kernel 与 4-bit 量化优化)
2. 显存优势 ~30%(对 4090 24GB 紧张场景关键,可能决定 7B 跑得通跑不通)
3. API 简洁(单 Python 文件 100 行内可跑完整 LoRA SFT,符合 D15"模板修改"路线)
4. 2026 已支持 12× MoE 等更新,生态健康
**风险**:Unsloth API 比 Axolotl YAML 灵活性低;若操作员未来想做复杂多卡 / FSDP,需切 Axolotl(v0.2 议题)

**D8 · LM Eval Harness 优于自包装的关键点**:
1. 覆盖 GSM8K / HumanEval / MMLU 等所有 PRD demo 候选数据集
2. 已是社区事实标准,与 OpenLLM Leaderboard 对齐(便于 demo 可信度)
3. 自包装短期省事,长期会重新发明 metric 抽样 / N-shot prompting / 答案抽取等轮子
**风险**:LM Eval Harness 比较重,首次 setup 半天到 1 天

操作员已于 2026-04-24 确认 OQ1/OQ2/OQ5 推荐,task-decomposer 无需再 follow up。

---

## 5. Task Breakdown(phases only;task-decomposer 详化)

> 以下仅 phase 级别,具体 T<NNN>.md 由 task-decomposer 接力产生。

**估时口径(2026-04-24 R2 修订,与 `dependency-graph.mmd` 和 `tasks/*.md` metadata 完全对齐)**:task 加总 **152h**(T001-T028 单表实际值,含 R2 后 +6h,详见 `tasks/*.md` 的 `estimated_hours`),乘 **+50% 踩坑 buffer** ≈ **228h**,在 PRD §7 C2 350-450h 内,留充足安全边际。关键路径(按 `depends_on + estimated_hours` 重算):`T001→T004→T005→T007→T010→T013→T017→T019→T023→T024→T027→T028` ≈ **~74h**。Phase 级别按 task metadata 加总 × 1.5:

- **Phase 0 · Foundation(task sum 24h × 1.5 ≈ 36h,Week 1-2)**
  - T001-T008 项目骨架(Python 3.12 + uv + ruff + pytest + Typer)
  - 仓库结构、README 占位、`pars` CLI 入口、最小可调用的 `pars --help`
  - 锁定 `requirements-locked.txt` 流程(uv lock + hash)
  - config/state/metrics/ledger 基础模块

- **Phase 1 · Core 训练循环 + Safety(task sum 41h × 1.5 ≈ 61h,Week 3-6)**
  - T009-T015 worker subprocess 派生(`claude -p` headless,git worktree)
  - API proxy(LiteLLM)+ **预算预估前置拒绝**(C20)
  - worker env strip + pip 白名单 + `.claude/` 只读分离(C21 fail-closed)
  - `.claude/` fail-closed 只读分离的装机前置检测(C21)
  - Run ledger 落地

- **Phase 2 · 决策报告 + Compare + 健壮性(task sum 56h × 1.5 ≈ 84h,Week 7-9)**
  - T016-T025 训练脚本模板(baseline / LoRA SFT / eval),3 套 .py 模板
  - 训练 backend 集成(Unsloth · OQ1 CONFIRMED 2026-04-24)
  - eval backend 集成(LM Eval Harness · OQ2 CONFIRMED 2026-04-24)
  - Stuck 状态机(**`architecture.md §8` 契约表为唯一真相源**,5s 采样 / 12 样本窗口)
  - Budget tracker(前置预估 + 60s 兜底)
  - 失败归因 schema + 报告渲染 + schema 校验
  - `pars compare` / `pars sft retry --from <run-id>` 实现
  - resume 机制(**仅同机重启**,C22;机器指纹 hard reject 仅 OS major / GPU / CUDA,Python / OS patch 降级为 warning)
  - 端到端 `pars sft start` 主编排

- **Phase 3 · Polish + Demo(task sum 31h × 1.5 ≈ 47h,Week 10-12)**
  - T026-T028 e2e 测试套 + demo 剧本 + README + LICENSE + CI
  - 1 个真实可复现 demo(Qwen3-4B + GSM8K-100)
  - rsync playbook(仅手工迁移教程,不写跨机 resume)
  - Conventional Commits 检查(pre-commit)

合计 **228h**(task 加总 **152h** × 1.5 踩坑 buffer);PRD §7 C2 预算 350-450h;剩余 122-222h 作为 R1/R2/R3 Critical risk 的深度修复 + 未预见 scope 调整 buffer。关键路径 **~74h** 意味着并行度拉满理论下限 ~74h,实际加 buffer 仍在预算内。

---

## 6. Verification Criteria

| Outcome | 验证方式(必须可机器跑或人审签字) |
|---|---|
| **O1** 一周内跑完 1 baseline + 1-2 LoRA 变体 + 决策记录 | **T027 7-day operator rehearsal**(`tasks/T027.md:81-85` rehearsal_script.sh):操作员按 `docs/demo-reproduction.md` 实跑 1 个 baseline + 2 个 LoRA 变体(含 1 次 `pars sft retry --hypothesis "调 lr"`)+ `pars compare` 生成对比;**计时**从 `pars sft start` 首次调用到最后一份 `report.md` 落盘,**≤ 7 自然日**(允许分多日执行);T026 e2e 的 `tiny_run_config` 只验证"happy path 机制可跑",**不**充当 O1 验证(归 O2/O5 smoke 用) |
| **O2** 报告含训练曲线 PNG + 分数对比表 + 失败归因 | `tests/test_report_schema.py`:断言每份 `report.md` 含 `## 训练曲线`、`## 分数对比`、`## 失败归因` 三个 section + 引用的 PNG 路径存在;`failure_attribution.md` 经 `validate_quality()` 返回 `(True, [])`(严格,消费端同样严格,消除 T020/T021 contract 漂移) |
| **O3** `pars sft resume` 续上中断训练(**仅同机重启**,C22) | `tests/integration/test_resume_after_kill.py`:启动 LoRA → `kill -9` 训练子进程 → `pars sft resume <id>` → 完成且最终 metric 与未中断版本误差 < 1%;跨机器 resume **不在本 outcome 范围**(README 明示) |
| **O4** README 给真实可复现 demo | 人审签字:操作员在另一台 4090 机器上(或回滚 worktree)跑 README 步骤,产出 `report.md` 与原 demo `report.md` diff 仅时间戳/UUID |
| **O5** 端到端单 run < 12h、**< $30(proxy 前置硬帽,C20)** | run ledger 自带 `wall_clock_seconds` 与 `usd_total`;**关键验证**:`tests/integration/test_proxy_prerejects_on_budget.py` 构造"余额不足"场景(mock `usd_spent=29.9`,cap=30),发 1k input + 1k output 的请求,proxy 预估 > 0.1 后**直接返回 402/429**,上游 Anthropic 从未收到请求(mock 侧断言 0 call);CI 跑一个 5min/$0.5 的 mock-LoRA smoke,确保字段填充正确 |
| **O6** `pars compare runA runB` 可读差异表 | `tests/integration/test_compare_two_runs.py`:跑 2 个 mock run(差 1 个 hyperparam)→ `pars compare runA runB` 输出含 `config diff`、`metric diff`、`conclusion diff` 三栏的 markdown table |
| **O7** Stuck 检测 LoRA epoch 30-90min 不误杀 | 验证对齐 **`architecture.md §8` 契约表**的正负样本矩阵(T022):① LoRA 60min 无 tool_use 但 GPU>20% 不触发、② pip install 网络 slow(net IO active 但 GPU=0)不触发、③ 子进程死锁全无 IO/GPU/CPU 触发(15min 后)、④ 5min 冷启动内真卡死仅记 warning 不 SIGINT、⑤ 60s 窗口边界 off-by-one 正确触发;**false negative(真卡不触发)** 算 O7 失败,操作员月度抽测 |

---

## Glossary

| Term | 在本项目的含义 |
|---|---|
| **run** | 一次完整的 baseline + LoRA + eval 闭环,落地为 `runs/<ULID>/` 目录 |
| **worker** | 一个 `claude -p` headless 子进程,跑在独立 git worktree |
| **stuck** | worker 进入 `truly_stuck` 状态机态(GPU/CPU/IO 全无活跃)且持续 > 15min |
| **失败归因** | worker 输出的半结构化文本,含必填字段(假设 / 观察 / 归因 / 下一步)+ 自由叙述 |
| **API proxy** | 本机 localhost 跑的 HTTP 中转,持有 `ANTHROPIC_API_KEY`,worker 子进程通过 `ANTHROPIC_BASE_URL=http://localhost:<port>` 访问;worker 子进程**不持有** key |
| **诚实负面 demo** | LoRA 训练完发现没真提升 baseline,但报告如实呈现(loss 下降但 eval 不涨)— PRD §6 O4 把这算 ship 成功 |
| **可移植路径** | 训练脚本与 checkpoint 路径走相对路径 + env var(如 `$RECALLKIT_RUN_DIR`),便于 rsync 到 H200(C9) |

---

## Open Questions for Operator

| # | Question | 阻塞什么 | 状态 / 操作员决定 |
|---|---|---|---|
| **OQ1** | 训练后端选 **Unsloth** 还是 **Axolotl**? | Phase 1 训练 backend 集成任务 | **CONFIRMED 2026-04-24**:Unsloth |
| **OQ2** | 评测后端选 **LM Eval Harness** 还是自包装? | Phase 1 eval backend 集成任务 | **CONFIRMED 2026-04-24**:LM Eval Harness |
| **OQ3** | demo 数据集 + 模型组合?(候选:Qwen3-4B + GSM8K-100 / Llama 3.1 8B + Alpaca 子集 / TinyLlama 1.1B + 极小集) | Phase 3 demo 任务 | 默认采用 Qwen3-4B + GSM8K-100(对应 PRD `gsm8k-100-lora-qwen3-4b` · 无异议) |
| **OQ4** | API proxy 选 **LiteLLM** 还是自写极简? | Phase 0 proxy 任务 | 默认采用 LiteLLM(无异议;若启动复杂或依赖太重再换自写) |
| **OQ5** | `.claude/` 只读分离实现路径:① **MacFUSE + bindfs 真只读 mount**;② **sudo chflags uchg**(macOS)/ **sudo chattr +i**(Linux)装机一次性 immutable flag;③ 二者都不装 → v0.1 **refuse to start** | Phase 1 T012 readonly mount 实现路径 | **CONFIRMED 2026-04-24**:MacFUSE + bindfs(fallback / refuse-to-start 保留作防御)|

> **OQ4 ~ OQ7(PRD §10 原编号)** 已在本 spec D14-D17 中给出 spec-writer 默认决策,无需操作员决策。若操作员异议,可在本节追问。

---

## Spec source

This spec was derived from PRD `discussion/003/003-pA/PRD.md` v1.0 by spec-writer at 2026-04-24.
**PRD 是 source of truth,本 spec 不可修改 PRD 决定的产品语义**。若发现 PRD 缺漏或冲突,在 OQ 区追问操作员,不擅自补全。

下一步:`/codex:adversarial-review specs/003-pA/` → task-decomposer。
