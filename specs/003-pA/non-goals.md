# Non-goals — 003-pA · RecallKit v0.1

**Version**: 0.2 · **Updated**: 2026-04-24(D-OP3 跨机 checkpoint 不兼容 · R1 HIGH #2)· **Source**: PRD §5 Scope OUT + spec-writer 引申

---

## 0. 一页结论

明确**不做**的事,分 5 类。每条都标来源(PRD / L3R0 红线 / spec-writer 引申)与**什么时候可能重新考虑**(v0.2 / v1.0 / 永不)。

**核心 litmus**:若一条 task 的描述让你想做以下任一项,**停下来**,与操作员确认是否越过 non-goal。

---

## 1. 与多 worker / 协作相关(来自 PRD §5.1)

| # | 不做 | 为什么诱人 | 为什么 v0.1 不做 | 何时重新考虑 |
|---|---|---|---|---|
| N1-1 | 多 worker 并行 | AAR 论文 9 worker 很酷;直觉"多 worker = 多 idea = 更快找答案" | L3 stage doc 明示"1 worker 顺序已能解决决策问题";L3R0 Block 5 红线"不做复杂调度" | v0.2+,且仅在 v0.1 完整 demo 跑通后;必须带清晰产品理由(非"好玩") |
| N1-2 | Forum / 共享内存 | 协作感;同类项目如 AAR/PARS L2 方案有 | 单 worker 不需要协作;PRD §5.1 明示 | **永不**(对 v0.1 范式不相容);若未来 N1-1 重开,再单独评估 |
| N1-3 | Leaderboard | "证据化决策"直觉上需要排名 | `pars compare` 已覆盖跨 run 对比需求;leaderboard 引入排序 / 投票等复杂逻辑 | **永不** |
| N1-4 | Sidecar agent(摘要搭档) | Opus R2 提过,GPT R2 淘汰 | L3 stage doc 明示被淘汰,理由"价值不硬" | 若 v0.2 出现真实需求(操作员反馈"每次看 log 太累"),再评估 |
| N1-5 | worker 间互通(消息通道) | 复杂 agent 系统标配 | 1 worker 无对象可通 | **永不**(除非 N1-1 重开) |

**引申**(spec-writer):
- ❌ 不写 asyncio scheduler / event loop(worker 用 blocking subprocess)
- ❌ 不做 capability token / JWT(无共享服务需要鉴权)
- ❌ 不起 FastAPI / Flask / Tornado 的任何 HTTP server(API proxy 除外,只本机 localhost)

---

## 2. 与其他工作流相关(来自 PRD §5.2)

| # | 不做 | 为什么诱人 | 为什么 v0.1 不做 | 何时重新考虑 |
|---|---|---|---|---|
| N2-1 | Prompt 优化 / agent scaffold 工作流 | 候选 B BenchLedger 的剧本;看起来"多一块功能 = 多吸引用户" | 候选 A 明确"押注后训练就是 v0.1 灵魂";两条剧本在 v0.1 会让 10 周预算吃紧 + 产品定位模糊 | v0.2(若操作员未来启动 BenchLedger-lite fork) |
| N2-2 | Workflow 插件契约 / 通用扩展接口 | "可扩展性"总是诱人 | 过度设计 anti-pattern;2 条 workflow 都没有呢,抽象从何来 | v1.0+ 且仅当真有 3+ workflow 需求时 |
| N2-3 | 多研究问题并发 | 操作员手头可能多个 idea 想同时跑 | v0.1 一次一个研究问题(PRD §5.2);手动开多个 `pars sft start` 会 GPU 冲突 | v0.2(若 PRD OQ7 重开"研究问题 = 多 run 集合") |

**引申**:
- ❌ 不写 `pars prompt start` / `pars scaffold start` 等非 sft 命令
- ❌ 不抽象"Workflow interface",所有逻辑在 sft orchestrator 里直写

---

## 3. 与训练算法相关(来自 PRD §5.3)

| # | 不做 | 为什么诱人 | 为什么 v0.1 不做 | 何时重新考虑 |
|---|---|---|---|---|
| N3-1 | RLHF / RLAIF | 2024-2025 前沿 | 硬件 + 复杂度 + 预算都超 v0.1 范围 | v0.2+,且需单独 PRD 评估硬件 / 预算 |
| N3-2 | DPO / RLOO / SimPO / ORPO | Unsloth / trl 已原生支持,诱惑"多加一个 flag 就有了" | 产品定位是"LoRA SFT 决策循环",加一个算法 = 报告 schema / 失败归因 / eval 都要重做 | v0.2 |
| N3-3 | 全参数 fine-tune | 小模型 7B 在 4090 24GB 上做 full fine-tune 在 2026 仍紧张 | 不在 PRD 承诺内 | v1.0+,且需 H200 级硬件集成(即 N4-2 N4-3 重开) |
| N3-4 | Multi-modal / vision 后训练 | diffusion LoRA / LLaVA 训练都成熟 | PRD §5.3 明示 | **永不**(定位偏)或专门 fork |
| N3-5 | 自研训练框架 | "不依赖 Unsloth,自己写 transformer 训练 loop" | 反 C8 "技术简单";反 L2 §4.2 "优先用现成" | **永不** |

**引申**:
- ❌ 不写 RLHF reward model 训练逻辑
- ❌ 不写自定义训练 loop(`torch.nn.functional` 级别)
- ❌ `templates/` 下只有 baseline / lora_sft / eval 三个 .py,不放 dpo_script.py 等

---

## 4. 与基础设施相关(来自 PRD §5.4 + L3R0 红线)

| # | 不做 | 为什么诱人 | 为什么 v0.1 不做 | 何时重新考虑 |
|---|---|---|---|---|
| N4-1 | Docker / 容器化 | 隔离 / 复现性好 | L3R0 Block 5 红线 | **永不**(除非红线解除) |
| N4-2 | Runpod / vast.ai 自动调度 | 4090 24GB 紧张时想自动上云 | L3R0 Block 5 红线 + PRD §5.4;"操作员手工 rsync" 已是用户行为,不需产品介入 | **永不 v0.1**;v1.0 可评估 `pars sft start --remote <alias>` 的轻量集成,但仍不做"自动申请 GPU" |
| N4-3 | 云 GPU 自动申请 / 释放 | Runpod API 做自动化好玩 | 同 N4-2 | **永不 v0.1** |
| N4-4 | 复杂调度器(asyncio scheduler / GPU 分配信号量 / 任务队列) | 看起来"工程感" | L3R0 Block 5 红线 + 单 worker 无需 | **永不**(除非 N1-1 重开) |
| N4-5 | Web UI / Streamlit dashboard | 可视化爽 | PRD §5.4 明示 + C8 "技术简单" | v1.0 可评估,但需证明 CLI + 本地 markdown 不够 |
| N4-6 | HTTP API server(除本机 localhost API proxy) | 未来第三方集成 | 不是服务 → 无需;proxy 是安全手段不是产品 | **永不 v0.1** |
| N4-7 | 多用户 / 账号 / 权限系统 | 协作感 | L3R0 Block 5 红线 | **永不**(本项目单人定位) |
| N4-8 | 数据库(Postgres / SQLite / DuckDB) | 查询方便 | 单 run 单文件系统已够(architecture §11 A5);C8 简单优先 | v1.0 可评估,但需证明 grep/cat 不够用 |
| N4-9 | Redis / 缓存层 | 快 | 单 worker 无并发,不需 | **永不 v0.1** |
| N4-10 | 可观测性栈(Prometheus / Grafana / Sentry / Datadog) | 生产级感 | 单人本机,`cat metrics.jsonl` 即一切 | v1.0 可评估 |
| **N4-11** | **跨机器 checkpoint 兼容性 / 跨机 resume**(v0.1 不承诺 4090 ↔ H200 resume 一致性,D-OP3) | C9 诱惑"既然 rsync 了,那 resume 也支持多好" | optimizer state / CUDA RNG / cudnn 算法版本跨机器不一致;工程成本 > v0.1 预算(需确定性 CUDA + 位宽对齐),且不是 PRD O3 范围 | v0.2 或 fork 新 PRD 单独承诺;v0.1 `docs/h200-rsync-playbook.md` 仅写"远端重跑"how-to,不教跨机 resume |

**引申**:
- ❌ 不写 Dockerfile / docker-compose.yml
- ❌ 不写 systemd unit / launchd plist(不做 daemon)
- ❌ 不起任何 0.0.0.0 端口(只 127.0.0.1 API proxy)
- ❌ 不做 migration 工具(因为没有 DB 可 migrate)

---

## 5. 与"高级 agent 能力"相关(来自 PRD §5.5)

| # | 不做 | 为什么诱人 | 为什么 v0.1 不做 | 何时重新考虑 |
|---|---|---|---|---|
| N5-1 | LLM-as-judge | 2025-2026 热门;"自动评判 worker 输出" | PRD §5.5 + D2;单 worker 自评作弊风险 + 加复杂度 | v0.2+,且须带独立 judge 基准与 F1 验证(不进 v0.1) |
| N5-2 | 自动种子扩展(LLM 生成 N 条种子) | AAR 论文做法 | PRD §5.5;human 写就行,1 worker 也不需要多种子 | **永不**(候选 A 定位"一次一个研究问题",无多种子需求) |
| N5-3 | 文献挖矿 / 自动 arXiv 扫描 | futuristic | PRD §5.5;worker 读 arXiv 是 P0-6 pypi 投毒的隐患源 | **永不 v0.1** |
| N5-4 | Meta-review(自我演化提示重写) | Google AI co-scientist 做法 | PRD §5.5;v0.1 prompt 由操作员手动 tune | v1.0+ |
| N5-5 | 向量库 / 语义检索 | ChromaDB / Qdrant 好装 | PRD §5.5;grep 即可,单 run artifacts 量小 | **永不 v0.1** |
| N5-6 | BenchJack 红队 / 攻击仿真 | 安全研究感 | PRD §5.5;v0.1 安全靠架构隔离(R4-R6)而非红队 | v1.0+ |
| N5-7 | Cross-run 知识迁移 / AgentRxiv 风格 | 每 run 都零起点浪费 | PRD §5.5 明示不做;`pars compare` + `pars retry --from` 是 spec 给的克制替代 | v0.2+(若操作员反馈"每次重头读 ledger 太累") |
| N5-8 | 子智能体(.claude/agents/fact-checker.md 等) | L2 §5.2 有详细方案 | 单 prompt worker 已足;子智能体增复杂度 + token 成本 | v0.2+(若失败归因质量 R3 持续差) |
| N5-9 | CoT monitor / transcript 分析 | 防奖励黑客 | v0.1 无排行榜 = 无奖励黑客激励;过度设计 | **永不 v0.1** |
| N5-10 | 认知科学式评分卡(5 维 LLM judge 评分) | L2 §5.5 提过 | 基于 N5-1 不做 | v1.0+ |

**引申**:
- ❌ 不写 `.claude/agents/*.md`(worker 是单一 prompt,无子智能体)
- ❌ 不做 prompt A/B 框架(操作员手动 tune 即可)
- ❌ 不做"熵坍缩监控"(单 worker 无熵概念)

---

## 6. 质量 / 可观测性方面的 non-goal(spec-writer 引申)

| # | 不做 | 引申自哪条 non-goal | 备注 |
|---|---|---|---|
| N6-1 | 不做正式 error budget / SLO 追踪 | N4-10 | v0.1 非服务 |
| N6-2 | 不做 sentry 崩溃上报(不传云,对齐 C14) | N4-10 + C14 | 用户手动看 traceback |
| N6-3 | 不做 A/B 实验框架 | N5-10 | 操作员手动 compare run |
| N6-4 | 不写"prompt 版本锁 + 回归测试"(moderator P1-11) | N5-1 | 本项目不做 judge = P1-11 N/A |
| N6-5 | 不发布 Docker image / Homebrew formula | N4-1 | `uv tool install` / `pip install .` 自己装 |
| N6-6 | 不维护 v0.x 多版本并行分支 | 单人项目,接受 R9 bus factor | 只维护 main |

---

## 7. 会诱惑下游 agent / 任务的点(task-decomposer / parallel-builder 警惕)

以下表述看起来"合理"但必须**立即停下来**与操作员确认:

- ✋ "我们加个 web dashboard 可视化训练曲线" → **N4-5 不做**,有 matplotlib PNG 嵌入 markdown 即可
- ✋ "我们加一个 sidecar worker 自动摘要长 log" → **N1-4 不做**
- ✋ "我们把 metrics 存到 SQLite 便于查询" → **N4-8 不做**,JSONL + `jq` / pandas 够
- ✋ "我们让 worker 自己写 eval 脚本时从 arXiv 找最新 metric" → **N5-3 不做**
- ✋ "要不我们加个 LLM-as-judge 自动打分" → **N5-1 不做**
- ✋ "我们加个 .claude/agents/fact-checker.md 子智能体提高归因质量" → **N5-8 不做**(R3 缓解用 schema + 必填字段,不用 agent 栈)
- ✋ "我们写个 Dockerfile 让别人容易装" → **N4-1 红线**
- ✋ "我们加 `pars sft start --backend=axolotl` 让用户选训练后端" → v0.1 不做(D7 锁死 Unsloth,除非 OQ1 操作员回复改);v1.0 才考虑
- ✋ "我们集成 Weights & Biases 让用户可追溯" → **N4-10 / N5-10 不做** v0.1
- ✋ "worker 决定 `pip install` 某个额外包以加速训练" → **N4 P0-6 / C17 红线**
- ✋ "我们加 `pars sft resume --remote user@h200` 支持跨机续跑" → **N4-11 不做**(v0.1 仅承诺手工 rsync + 远端重跑训练)
- ✋ "反正 chmod -R a-w 就够了吧" → **C21 红线**(纯 chmod 可被 Python 面 `os.chmod` 绕过,不是生产路径)
- ✋ "要不 budget 超 cap 后 SIGINT 就够了,不用 proxy 预估" → **C20 红线**(单个大请求 / 失败重试 / 59s 内多请求都能在 60s 轮询前破 cap)

---

## 8. 如何使用本文件(task-decomposer / parallel-builder 必读)

1. 写任何 `tasks/T<NNN>.md` 前,扫一遍本文件所有表
2. 如 task 描述命中 §7 任一条,**立即** STOP,回到 operator 确认是否越界
3. Task 的 acceptance criteria 中绝不含 "实现 X non-goal"
4. PR review 时用本文件当 checklist:每条 non-goal "我的 diff 是否引入了它"
