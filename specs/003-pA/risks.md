# Risk Register — 003-pA · RecallKit v0.1

**Version**: 0.2.1 · **Updated**: 2026-04-24(OQ5 CONFIRMED patch · MacFUSE + bindfs · 澄清 only · 不改风险清单)· **Source**: PRD §9 + moderator-notes(仅 v0.1 相关项)+ spec-writer 引申 + R1 对抗审查

**Format**: 每条 risk 含 ID · 类别 · 严重度(Critical/High/Medium/Low)· 概率(H/M/L)· 触发信号 · 缓解方案 · 是否 v0.1 必须解决 · owner(v0.1 仅操作员本人)

---

## 0. 一页结论

11 条 risk,3 条 Critical(R1 硬件 / R2 stuck 状态机 / R3 归因质量)必须 v0.1 解决;其余高/中严重度通过架构层面缓解(R4 API key proxy + 前置 USD 硬帽、R5 pip 锁定、R6 配置**fail-closed** 只读分离、R11 模型路由 rebalance),接受 bus-factor(R9)与弱 demo(R7)作为 OSS 单人项目的常态风险。

---

## 1. Technical

### R1 · 本机硬件能力紧张(来自 PRD §9 Biggest risk)

- **严重度**:**Critical** · **概率**:**M**
- **描述**:7B QLoRA 在 4090 24GB 紧张但可行;Qwen3-4B 预期能跑通;若想做 8B+(Llama 3.1 8B)显存可能 OOM,需手动 rsync 到 H200
- **触发信号**:第一次跑 Qwen3-4B QLoRA OOM / epoch 时间 > 2h(暗示 batch_size 被压到极小)
- **缓解**:
  1. **D7 选 Unsloth**(显存 ~30% 省)
  2. Demo 默认选 Qwen3-4B + gsm8k-100(PRD OQ3),**不**默认 Llama 3.1 8B
  3. README 明示最低 GPU = 24GB + 推荐配置,降级 fallback = TinyLlama 1.1B
  4. C9 路径可移植性让"跑不动就 rsync H200"不割裂
- **v0.1 必须解决**:**是**(否则 O1/O5 可能无法达成)
- **owner**:操作员

### R2 · Stuck 状态机做不对(来自 moderator P1-10 + PRD §9)

- **严重度**:**Critical** · **概率**:**H**(若不专门设计必误杀)
- **描述**:LoRA 一 epoch 30-90min 全程无 `tool_use` 事件;若用 L2 原方案 15min 黑名单 timeout → 必误杀 → 操作员会误以为是模型能力问题,debug 几天
- **触发信号**:集成测试 `test_stuck_no_false_positive_during_lora_epoch` 失败;或真实 demo 中操作员观察到训练中途被 SIGINT
- **缓解**:
  1. **D13 白名单 4 态** 状态机(`idle / training / downloading / truly_stuck`)
  2. 判据走 GPU util / 子进程 CPU / 磁盘 IO / 网络 IO(任一活跃即 not stuck)
  3. 启动后头 5min 永不 SIGINT(冷启动 / pip / cache warmup 豁免)
  4. 连续 3 次 stuck-restart 熔断 → `needs_human_review`,不再自动重启
  5. 状态转换日志落 `state.json`,操作员 `pars status` 可见,便于 debug
- **v0.1 必须解决**:**是**(直接对应 O7,也是 spec C18)
- **owner**:操作员

### R3 · LLM 失败归因质量差(来自 PRD §9)

- **严重度**:**Critical** · **概率**:**M-H**(LLM 爱输出安全叙述)
- **描述**:若 worker 给的归因都是"可能是数据问题,可能是超参问题",产品核心价值崩塌,变成"高级 log 打印器"
- **触发信号**:demo 跑完后操作员人审 `failure_attribution.md` 发现必填字段被填"未知"/ "可能";或自由叙述段全是套话
- **缓解**:
  1. **D16 半结构化 schema**:必填枚举字段 + 自由段
  2. 枚举字段强制(模板中预写,LLM 须选一项 + 说明,不选就 schema 校验失败)
  3. 必填字段要求引用具体 metric 数字(如"eval_loss 从 2.1 升到 2.4, 在 epoch 3 后")
  4. Phase 3 写 "归因质量 demo"(一个故意 LR 过大的 run + 一个故意 LR 过小的 run),人审 worker 是否归因到正确类别
  5. 若持续 fail,fallback 到"把 metric jsonl 丢给另一次 claude -p 做归因 = 小型 judge"(但这越过 D2 不做 judge 的边界,只作 v0.2 option)
- **v0.1 必须解决**:**是**
- **owner**:操作员

### R8 · 训练后端踩坑(来自 PRD §10 OQ1 + tech-stack D7)

- **严重度**:**High** · **概率**:**M**
- **描述**:Unsloth 2026 版本与 transformers/peft 可能出现 compat 问题;或 Unsloth API 在模板覆盖外的边缘场景不足用,debug 几天
- **触发信号**:Phase 1 训练 backend 集成 task 预算超 30h 未完成
- **缓解**:
  1. pin 到 Unsloth + transformers/peft 官方兼容组合
  2. Phase 1 留 buffer(120-160h 区间)
  3. README 的最小 demo 用 Unsloth 官方教程数据集(Alpaca-子集),优先保证"至少一个路径走通"
  4. 若真踩大坑,OQ1 fallback 到 Axolotl(+20h 预算)
- **v0.1 必须解决**:**是**(Phase 1 阻塞)
- **owner**:操作员

### R11 · AI 模型路由偏贵(R1 Codex Model routing concern)

- **严重度**:**Medium** · **概率**:**H**(按 spec v0.1 task 表默认路由会命中)
- **描述**:task-decomposer 的首版路由按 task 数给了 Opus 28.6% / Sonnet 46.4% / Codex 14.3% / Haiku 10.7%;按工时给 Opus **38.4%**。spec 目标是 Opus 10-15%。差距明显,单次 v0.1 build 成本可能 2-3x 预期
- **触发信号**:task-decomposer 重新 routing 后 Opus 工时占比仍 > 20%;或首周 build 实际 API bill > $30 × 28 × Opus 份额
- **缓解(交给 task-decomposer R2)**:
  1. Opus **仅留**给 **contract-heavy 安全任务**:T012(`.claude/` 只读 + integrity)、T017(Stuck 状态机 single-truth 实现)、T020(FailureAttribution schema)
  2. 其他 "high risk_level" 任务(T010 / T011 / T018 / T019 / T023)降级到 **Sonnet**(仍有强代码能力 + 契约意识),用 Codex 做成对审查
  3. 确定性编码任务(T013 / T014 / T015 / T021 / T022 / T024 / T025)下放到 **Sonnet / Codex**
  4. 文档 / CI / polish(T026-T028)下放到 **Haiku**(已是)
  5. **目标**:Opus 按工时份额 ≤ 15%(仅 3 task ≈ 23h / 152h = **15.1%**)
- **v0.1 实际达成**:Opus 工时 **15.1%**(目标 ≤ 15%,**压线超 0.1pp,v0.1 可接受**);v0.2 若要进一步降,考虑把 T017 的 Stuck 状态机实现分拆(主逻辑 Opus / 状态转换表生成 Sonnet),或把其他 contract-heavy 任务的 reviewer 路径改 Codex 成对审查
- **v0.1 必须解决**:**是**(对齐 C2 单人 350-450h 预算 + C3 无商业预算)
- **owner**:task-decomposer R2(spec R1 修完后立即重新 routing)

### R10 · 操作员手工 rsync H200 体验割裂(来自 spec C9 / C22 · D-OP3 收窄)

- **严重度**:**Medium** · **概率**:**M**(操作员实际用时才暴露)
- **描述**:若 checkpoint / 训练脚本路径不 portable(写死绝对路径),rsync 到 H200 跑了发现路径 miss,debug 数小时。**注意 D-OP3 收窄**:v0.1 只承诺"rsync 后远端重跑训练",不承诺"跨机 resume";因此风险只限路径层面
- **触发信号**:操作员第一次实测手工迁移时报"跑不起来"
- **缓解**:
  1. **D18 路径走 env var + 相对路径**
  2. 训练脚本模板中所有路径 = `os.environ['RECALLKIT_RUN_DIR']` / `RECALLKIT_CKPT_DIR` / `HF_HOME`
  3. README + `docs/h200-rsync-playbook.md` 写"手工迁移 H200"小节(仅基线 + LoRA 的"重跑"how-to,**不写**跨机 resume 教程)
  4. README 明示"迁移后需**从零开始训练**,非续跑;同机续跑走 `pars sft resume`"
- **v0.1 必须解决**:**是**(对齐 C9 / C22 硬约束)
- **owner**:操作员

---

## 2. Security(大部分来自 moderator P0 在 single-op 场景的降级版)

### R4 · API key exfil(来自 moderator P0-5 + spec C10/C15)

- **严重度**:**High** · **概率**:**M**(即使 single-operator,worker 处理 HF dataset README 即可能触发)
- **描述**:worker 读到外部数据(HF dataset README / 训练样本)含 prompt injection →`bash -c 'printenv | base64'` → 通过合法 API 调用把 key 外泄;或 LLM 自身 bug 把 key 写入 log
- **触发信号**:审计日志里出现 base64 / hex 编码的异常字符串;或 Anthropic 账单异常激增(非单 run 烧法)
- **缓解**:
  1. **D10 本机 localhost API proxy**(持 key),worker subprocess env **不含** `ANTHROPIC_API_KEY`
  2. proxy 仅 bind `127.0.0.1`,拒绝 LAN 来源
  3. proxy 仅放行必要 Anthropic 端点
  4. 单测 `test_worker_env_no_api_key`(读 `/proc/<pid>/environ` 断言)
  5. Budget Tracker 硬帽兜底(即使 key 被拿走也有 USD 上限)
- **v0.1 必须解决**:**是**(C10/C15 硬约束)
- **owner**:操作员

### R5 · pip 供应链投毒(来自 moderator P0-6 + spec C17)

- **严重度**:**High** · **概率**:**L-M**(typosquatting / dependency confusion 在 Python 生态常见)
- **描述**:worker 读到外部内容后 `pip install malicious-pkg`(拼写错误或依赖混淆),postinstall 脚本跑恶意代码;或 `pip install git+<url>` 拉任意代码
- **触发信号**:worker 的 `pip install` 命令中出现非预期包名;`requirements-locked.txt` 无故变更
- **缓解**:
  1. **D12 pip 白名单**:hook 仅允许 `pip install -r requirements-locked.txt --require-hashes`
  2. `requirements-locked.txt` 由 `uv lock --hash` 生成,含 SHA-256 hash(hash 不对直接 fail)
  3. `hooks/pre_pip_install.sh` 拦截任何其他形式的 `pip install`
  4. 每月 `pip-audit` + `pip-licenses` 扫描
- **v0.1 必须解决**:**是**(C17 硬约束)
- **owner**:操作员

### R6 · worker 修改 `.claude/` 让 deny 失效(来自 moderator P0-2 + spec C16 / C21 · R1 BLOCKER #3 fail-closed 改写)

- **严重度**:**High** · **概率**:**L-M**(LLM bug 或 prompt injection)
- **描述**:worker 通过 `Edit .claude/hooks/pre_tool_use.sh` 改成 `exit 0`,黑名单失效;Sakana v1 真实发生过。**关键风险**:worker 允许 `Bash(python:*)`,Python 面的 `os.chmod` / `pathlib.Path.chmod` 可绕过纯 `chmod -R a-w`,因此 **fallback 不能是纯 chmod**
- **触发信号**:`.claude/` 下任何文件 checksum 变化;worker 尝试 `chmod` / `chflags` / `chattr` 或 Python `os.chmod`
- **缓解(fail-closed · D-OP2)**:
  1. **C21 只读分离(必须其一)**:
     - **首选** `bindfs --ro`(macOS + MacFUSE)/ `mount --bind + remount ro`(Linux)— 真只读 mount,kernel 层拒绝所有 write syscall
     - **fallback** `sudo chflags uchg`(macOS)/ `sudo chattr +i`(Linux)— immutable flag,syscall 层拒绝
     - **二者都不可用 → CLI refuse to start**(打印可操作错误 + 指向 OQ5)
     - ❌ 纯 `chmod -R a-w` **不作为生产路径**(Python 面可绕过)
  2. **主验证**:T012 integration test 在 **允许的 Python 面**(`Bash(python:*)` 场景)下尝试改回 `.claude/` 可写 → **必须失败**(EACCES/EPERM)
  3. **第二道验证**:hooks 与 settings 启动 / 退出时校验 SHA-256(事后发现事故,非主防护)
  4. settings.json `deny` 深度防御:`Bash(chmod:*)`、`Bash(chflags:*)`、`Bash(chattr:*)`、`Bash(sudo:*)`、`Write(.claude/**)`、`Edit(.claude/**)`
- **v0.1 必须解决**:**是**(C16 / C21 硬约束)
- **owner**:操作员(**OQ5 CONFIRMED 2026-04-24: MacFUSE + bindfs**;fallback `sudo chflags uchg` 作防御保留)

---

## 3. Operational

### R7 · 诚实负面 demo 的 GitHub star 弱(来自 PRD §9 + L3 stage doc 诚实检查 §2)

- **严重度**:**Medium** · **概率**:**M**(OSS 用户对"demo 实际失败"接受度未验证)
- **描述**:Demo 跑完发现 LoRA 没真提升 baseline,PRD 定义这是合法 ship,但 README reader 可能觉得"连 demo 都失败,这工具有啥用"
- **触发信号**:首月 GitHub star < 10;issue 区出现"你这 demo 不 work 啊"
- **缓解**:
  1. README 首屏明确定位:"这是**决策工具**不是**LoRA 炼丹工具**;证明 LoRA 没提升也是有价值的 output"(D20)
  2. 准备 2 个候选 demo:① 预期有提升的(便于展示 happy path);② 预期可能没提升的诚实 demo。**先 ship ①**,再补 ②
  3. 不追求 star,追求"有人真的用它判断 go/no-go";OSS 成功定义按 C3(无商业目标)
- **v0.1 必须解决**:**否**(接受)
- **owner**:操作员

### R9 · 单人 bus factor(来自 spec C19)

- **严重度**:**Medium** · **概率**:**L**(操作员病假 / 换工作 / 失去兴趣)
- **描述**:整个项目单人维护,操作员不可用 > 7 天即停摆
- **触发信号**:操作员 > 7 天不 commit
- **缓解**:
  - **接受**(OSS 单人项目通病,C2/C3 约束下无人可替代)
  - 长期降级:MIT License + README + 1 个真实可复现 demo 即"遗产"
  - 代码保持 CLAUDE.md 一致("中文注释 + 先结论后细节 + 结构化"),降低他人接手门槛
  - 不做交接 runbook(投入产出比低)
- **v0.1 必须解决**:**否**(显式接受)
- **owner**:操作员(接受)

---

## 4. Personnel / bus-factor(必填条目)

### BUS-1 · Solo operator unavailable > 7 days

- **严重度**:**Medium** · **概率**:**L**
- **描述**:同 R9
- **触发信号**:同 R9
- **缓解**:
  - 明示**接受**;README + LICENSE + demo 已是"遗产"
  - v0.1 不写交接 runbook
  - 若社区出现 PR / contributor,merge policy 写进 `CONTRIBUTING.md`(v0.1 可选)
- **v0.1 必须解决**:**否**(接受)
- **owner**:操作员(接受)

---

## 5. Commercial

**N/A**(C3 明示 OSS 免费,无商业风险)

---

## 6. Compliance / legal

**大部分 N/A**(单人 OSS 工具,无 PII 处理,无支付,无医疗数据)。仅 2 条轻量项,详见 `compliance.md`:

- 用户训练数据若含 PII,操作员自行处理(产品不主动判定 PII)
- 第三方依赖 license check(拒绝 GPL/AGPL 与 MIT LICENSE 冲突)

---

## 7. 汇总表(快速查阅)

| ID | 类别 | 严重度 | 概率 | v0.1 必须解决 | 缓解 key |
|---|---|---|---|---|---|
| R1 | Technical | Critical | M | 是 | D7 Unsloth + TinyLlama fallback + C9 路径 |
| R2 | Technical | Critical | H | 是 | D13 状态机白名单 4 态 + 5min 冷启动豁免 + 熔断 |
| R3 | Technical | Critical | M-H | 是 | D16 半结构化 schema + 必填 metric 引用 + demo 归因质量验证 |
| R4 | Security | High | M | 是 | D10 API proxy + env strip + budget 兜底 |
| R5 | Security | High | L-M | 是 | D12 pip 白名单 + hash 校验 |
| R6 | Security | High | L-M | 是 | **C21 fail-closed** · MacFUSE bindfs 或 chflags uchg · **禁纯 chmod** · Python 面整合测试 |
| R7 | Operational | Medium | M | 否 | README 定位 + 准备 2 种 demo |
| R8 | Technical | High | M | 是 | pin 版本 + Phase 1 buffer + OQ1 fallback |
| R9 | Operational | Medium | L | 否(接受) | README + LICENSE + demo 作遗产 |
| R10 | Technical | Medium | M | 是 | D18 env var + 相对路径 + C22 明示不跨机 resume |
| **R11** | Operational | Medium | H | 是 | **task-decomposer R2 重新 routing,Opus ≤ 15% 工时** |
| BUS-1 | Personnel | Medium | L | 否(接受) | 同 R9 |

**"v0.1 必须解决" = 是** 的 8 条全部对应 spec §3 C10-C22 硬约束或 §4 D10-D18 锁定决策,已在 architecture.md 里有具体实现方案。

---

## 8. R1 反馈新增开放项(交给 task-decomposer)

- **OQ5**:**CONFIRMED 2026-04-24 · MacFUSE + bindfs**(操作员确认)。装机路径 = `brew install --cask macfuse && brew install bindfs`(首次需重启一次加载 kext)。fallback `sudo chflags uchg` + refuse-to-start 兜底保留作防御。参考 spec.md §Open Questions OQ5。
- **R11**:task-decomposer R2 必须重新计算模型路由,目标 Opus ≤ 15% 工时。
