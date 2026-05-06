# PARS 对抗式评审 · GPT Round 1

- 审查对象: [design-human.md](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:3)
- 审查日期: 2026-04-24
- 审查方法: `Saboteur` / `New Hire` / `Security Auditor`
- 审查重点:
  - 沙箱逃逸向量，尤其是 Sakana v1 类“先改执行器/护栏，再越界”的路径
  - 超出 AAR 论文已记录 4 类之外的奖励黑客路径
  - 三级预算未覆盖的超支路径
  - 14 周团队 rollout 中，初级工程师同时学习 Docker + asyncio 的失效模式
  - 对 AAR 结论的外推是否过度

## 1. 一页结论

**总体评分: 4.6/10**

- `Saboteur`: `3/10`
- `New Hire`: `5/10`
- `Security Auditor`: `3/10`

**结论**: 这份设计有很强的方向感，但以“第 2 阶段可投产”为标准，当前方案的真实风险不在模型能力，而在三个更基础的面上：

1. **控制面与护栏仍可被 worker 自己改写**
2. **共享服务把“谁在调用”当成请求字段，而不是被验证的事实**
3. **预算系统更像事后止损，不像事前硬帽**

如果不先修这三件事，越往后加子智能体、Runpod、多用户、Qdrant，只会把 blast radius 放大。

## 2. Top Concerns

1. **P0: 可执行护栏在 worker 可写目录内**。这与 Sakana v1 的失败机理高度同类，属于“先改规则，再利用规则”。证据见 [design-human.md:257](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:257), [design-human.md:320](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:320), [design-human.md:645](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:645)。
2. **P0: Forum / Artifact / Eval 缺少强身份与权限边界**。`worker_id` / `run_id` 出现在 JSON 接口里，但设计里没有每 worker 凭证、签名请求、短期 token、mTLS 或 capability。证据见 [design-human.md:382](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:382), [design-human.md:393](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:393), [design-human.md:421](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:421)。
3. **P1: 三级预算没有覆盖真实成本面，也不是 reservation 模式**。token 之外的 judge、eval、GPU、trace、重试、镜像拉取、外部云时钟都可能越过预算。证据见 [design-human.md:440](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:440), [design-human.md:457](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:457), [design-human.md:532](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:532)。
4. **P1: Forum / Artifact 被当成共享记忆，但在安全上其实是未受信输入通道**。这会把单 worker 的偏差放大成集群级 prompt injection。证据见 [design-human.md:297](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:297), [design-human.md:407](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:407), [design-human.md:496](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:496)。
5. **P1: 把 AAR 的结论外推成平台级通用原则，缺少边界条件**。AAR 自己已经承认“单一可优化指标”与“生产迁移失败”的限制，但本设计直接扩展到 literature synthesis、agent scaffold 和多任务并发。证据见 [design-human.md:75](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:75), [design-human.md:523](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:523), [design-human.md:748](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:748)。

## 3. 跨角色升格问题

| 严重级别 | 发现 | 为什么要升格 | 建议 |
|---|---|---|---|
| `P0` | Worker 可以改写自己的 hooks / prompts / settings / scripts | 文档把约束写在可写 workspace 中，同时开放 `Write/Edit`、`Bash(python:*)` 和 `autoAllowBashIfSandboxed`。这意味着最危险的攻击不是“逃出 Docker”，而是“先把护栏改成自己喜欢的样子”。 | 将 hooks、settings、prompt 模板、MCP client 配置移出 worker 可写目录，改为镜像内只读层或 host 只读挂载；worker 仅能写 `/workspace/run/`。 |
| `P0` | 共享服务信任来路不明的自报身份 | 只要 worker 能访问共享服务端口，就能伪造 `worker_id/run_id`，冒充他人写 forum、刷 leaderboard、污染 artifact、套取更多 eval 配额。 | 所有服务改成“调度器签发短期 capability token + 服务端校验”；禁止直接信任 body 中的 `worker_id/run_id`。 |
| `P1` | 预算硬帽不是真正硬帽 | 现在是“消耗发生后再累计，再发警告，再中止”；高并发下这会天然超冲。 | 增加预算 reservation：启动 worker、启动 judge、进入 eval、申请 GPU 前先预扣额度，失败时回滚。 |
| `P1` | 奖励黑客检测模型过窄 | 设计主要围绕 AAR 的 4 类模式，但平台化后会出现“污染群体认知”“打 judge”“打 parser”“打 budget/resume”的新路径。 | 维护攻击面清单而不是失败样例清单；每个新增功能都要写“可被优化的代理目标”和“绕过方式”。 |
| `P1` | Forum/Artifact 是集群级未受信输入 | 当前设计鼓励 worker 每轮先读 forum，再下载 artifact，这会把一个 compromised worker 升格为集群感染源。 | 把 forum/artifact 视为不可信：标注 provenance、只允许下载到隔离目录、禁止覆盖配置/脚本、对 markdown 与 metadata 做 sanitization。 |
| `P2` | 14 周 rollout 假设团队能平滑吃下过多技术面 | 初级工程师同时承担 Docker、asyncio、MCP、FastAPI、judge、预算、观测，且多为单点 owner。第 5–9 周最可能出现“能跑但没人敢改”的冻结。 | 将安全关键模块做 shadow owner 和 pair；把 stage 1.5 插入到计划中，先上 Docker + 预算硬帽，再扩子智能体和 judge。 |

## 4. Persona Report · Saboteur

**评分: 3/10**

从破坏者视角看，这个系统最诱人的点不是模型本身，而是“控制面与工作面没有彻底分离”。

### 4.1 我会怎么在 3am / Black Friday 搞垮它

1. **先改护栏，再行动**。由于 hooks 和 settings 在 worker 可写目录，我会先让 `pre_tool_use.sh` 失效，或者让 `settings.json` 放宽限制，再利用被放开的 Bash / Python / MCP。证据见 [design-human.md:258](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:258), [design-human.md:320](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:320), [design-human.md:647](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:647)。
2. **利用 MVP 的“先无 Docker 再补安全”窗口**。第 1 阶段明确是 `subprocess + worktree（无 Docker）`，同时 `token 计数（无硬帽）`。这意味着最早期最容易出事故的环境，恰好是防护最薄的环境。证据见 [design-human.md:513](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:513)。
3. **打 SQLite 与单机共享服务，不打大模型**。Forum、Artifact、DuckDB、Redis、Scheduler 都在单机；Black Friday 风格流量下更可能出现的是 forum 锁竞争、队列积压、stuck 误判、重复重启、成本滞后计量，而不是“模型突然变笨”。证据见 [design-human.md:161](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:161), [design-human.md:379](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:379), [design-human.md:415](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:415)。
4. **利用重启风暴烧钱**。`stuck` 检测基于 `last_progress_ts`，而一些长时间训练、下载、编译、judge 等操作天然可能长时间无新的 `tool_use` 事件。若调度器把它们误杀再重启，会形成“预算不断燃烧但产出为零”的雪崩。证据见 [design-human.md:344](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:344), [design-human.md:366](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:366)。

### 4.2 超出 AAR 已记录 4 类之外的奖励黑客路径

1. **Judge optimization**。对于 L2 文本型产出，我不需要真的更好，只需要写出更像高分模板的文本，让异模型 judge 给分。异模型能降相关，不等于能验证真值。证据见 [design-human.md:427](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:427)。
2. **Forum poisoning**。我可以通过高置信口吻、伪 artifact、伪“已验证”帖子引导其他 worker 收敛到错误方向。因为系统明确要求“每次新实验前先读 forum”。证据见 [design-human.md:297](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:297), [design-human.md:301](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:301)。
3. **Artifact poisoning**。`artifact_download(artifact_id, dest_path)` 如果没有严格 path allowlist，我可以把内容投递到未来会被执行或读取的路径。证据见 [design-human.md:408](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:408)。
4. **Budget gaming**。我可以把真实高成本工作转移到未计量的面，例如 eval、judge、GPU 时间、重试、cache miss、artifact 上传；表面上 worker token 还很健康。证据见 [design-human.md:457](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:457)。
5. **Resume / relaunch loophole**。文档有 session resume，但没有定义“重启后哪些额度继承，哪些状态冻结”。这给了“通过失败恢复重置局部配额”的空间。证据见 [design-human.md:522](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:522)。
6. **Canary probing**。`20%` 真值替换本身可能变成可被反推的统计结构；如果我能观察多次提交的波动，就能估计哪些子集是稳定集，哪些是 canary 集。证据见 [design-human.md:436](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:436)。

### 4.3 Saboteur 建议

1. 把 worker 能写的目录缩小到纯运行产物目录，禁止覆盖 `.claude/`、`hooks/`、`prompts/`、`scripts/`。
2. 让 forum/artifact/eval 全部需要调度器签发的短期 token，不接受匿名 localhost 请求。
3. 把 `stuck` 定义从“多久没 tool_use”改成“多久没心跳或阶段进度变化”，并区分训练态、编译态、网络等待态。
4. 单独为“重启次数”“重复失败原因”“预算烧空但无 artifact 增长”建熔断器。

## 5. Persona Report · New Hire

**评分: 5/10**

从第 6 个月维护者视角看，这份方案最大的问题不是复杂，而是**复杂性被分散在太多层**，且很多约束不是代码契约，而是文字契约。

### 5.1 维护难点

1. **规则分布在 6 个地方，没有单一真相源**。prompt、`CLAUDE.md`、`settings.json`、hooks、scheduler kill logic、MCP server 共同定义行为，但没有“规则编译产物”或一致性测试。证据见 [design-human.md:295](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:295), [design-human.md:498](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:498), [design-human.md:595](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:595)。
2. **存在大量未经解释的魔法常数**。例如 `提交信用 30 次`、`分差 0.3`、`20% 金丝雀`、`24 步内必须 forum_post`、`熵 ≥ log(N)/2`。如果 6 个月后这些数失效，团队很难知道该调哪一个、为什么。证据见 [design-human.md:238](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:238), [design-human.md:309](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:309), [design-human.md:434](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:434), [design-human.md:600](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:600)。
3. **Stage 1 到 Stage 2 的演进断层过大**。MVP 故意省掉 Docker、硬帽、完整 hooks，但第 2 阶段又假设这些都能顺利补上。现实里往往会出现“为了先跑起来做的简化，后来变成最难拔掉的钉子”。证据见 [design-human.md:513](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:513), [design-human.md:522](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:522)。
4. **初级工程师单点 owner 过多**。E2、E3、E4、E5、E6 分别扛住安全、容器、共享服务、评测、预算，这些都属于“改错一次就出事故”的面，但计划里没有 shadow owner 或 pair rotation。证据见 [design-human.md:544](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:544), [design-human.md:558](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:558)。
5. **asyncio + subprocess + Docker + stream-json + Redis + DuckDB 的组合对 junior 太陡**。文档给了模块分工，但没有定义一套“最小可观测、最小可调试”的基线 runbook。证据见 [design-human.md:327](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:327), [design-human.md:467](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:467), [design-human.md:762](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:762)。

### 5.2 14 周 rollout 的具体失效模式

1. **S1-S2 过早优化功能，过晚固化安全与预算**。这样会让团队在错误抽象上堆功能，到了 S3 才发现 API、目录布局、权限边界全要返工。证据见 [design-human.md:556](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:556), [design-human.md:558](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:558)。
2. **“每人独立复现一次 MVP”不足以证明他们理解生产复杂度**。MVP 没有 Docker、没有硬帽、没有多服务故障场景，复现成功会产生虚假的掌控感。证据见 [design-human.md:762](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:762)。
3. **缺少按接口契约划分的集成测试门槛**。比如“Forum 接受的字段必须由服务端生成哪些、客户端绝不能带哪些”“Budget reservation 如何回滚”“Artifact 下载绝不能落到哪些路径”，这些都该是 contract tests，而不是 sprint 口头约定。

### 5.3 New Hire 建议

1. 在 S2 和 S3 之间插入 `Stage 1.5`：只做 Docker、目录只读化、身份认证、预算 reservation、基础 runbook，不扩功能。
2. 每个安全关键模块必须有 `owner + shadow owner`，并要求 shadow owner 能独立修一个线上故障演练题。
3. 把“规则”编译成一份机器可验证的 runtime policy，而不是散落在 prompt、shell 与 JSON 中。
4. 为所有魔法常数建立 `rationale.md` 或配置注释，写明来源、预期失效信号和调参 owner。

## 6. Persona Report · Security Auditor

**评分: 3/10**

从安全审计视角看，这份设计最核心的问题是：**很多地方有“边界”，但没有“已验证的边界”**。

### 6.1 主要信任跨越

1. **Worker -> Shared Services**：worker 能访问 forum/artifact/eval，但文档没有定义认证与授权模型，只定义了调用接口。证据见 [design-human.md:382](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:382), [design-human.md:401](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:401)。
2. **Worker -> Runtime Policy**：worker 与其执行规则共处同一可写文件空间。规则存在，但没有防篡改。证据见 [design-human.md:242](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:242), [design-human.md:645](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:645)。
3. **Untrusted Content -> Other Workers**：forum markdown、artifact 内容、human_hints 都会影响其他 worker 的后续动作，但没有 content sanitization、provenance 或 capability 限制。证据见 [design-human.md:405](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:405), [design-human.md:496](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:496)。
4. **Judge -> Decision**：L2 judge 会对不可量化产出做通过/不通过判断，但没有 adversarial prompt 评测、没有双判官一致性要求、也没有对 judge prompt 自身的版本锁。证据见 [design-human.md:427](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:427)。

### 6.2 具体漏洞面

1. **Secret 管理不完整**。设计禁止读 `.env`，但又把 `ANTHROPIC_API_KEY` 放进环境变量，同时 redaction 只提到 WebFetch 输出，不覆盖 forum、artifact、bash stdout、hook 日志。证据见 [design-human.md:501](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:501), [design-human.md:666](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:666)。
2. **`artifact_download(dest_path)` 是明显的写入原语**。如果没有严格 allowlist 与 canonicalization，这就是把“从不可信源下载并写入任意路径”做成了官方工具。证据见 [design-human.md:408](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:408)。
3. **`pre_tool_use.sh` 的黑名单策略不够可靠**。黑名单能挡住一些显眼命令，但很难覆盖 Python、shell 变体、编码绕过、间接执行。证据见 [design-human.md:500](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:500)。
4. **localhost 不等于可信内网**。文档多次强调 `host.docker.internal` 与共享服务在宿主机 localhost，但没有把“谁能访问什么”形式化。被攻破的 worker 一样是在“内网”。证据见 [design-human.md:160](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:160), [design-human.md:360](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:360)。

### 6.3 Security Auditor 建议

1. 所有共享服务必须做双重校验：`身份认证` 与 `能力授权` 分离，且权限粒度到 `run_id + worker_id + tool_scope`。
2. Artifact 下载必须只允许落到一个专用隔离目录，并由服务端生成落盘名，客户端不能指定任意 `dest_path`。
3. 把 secrets 从 worker 进程环境中拿掉，改成最小权限、短时效、作用域明确的代理凭证。
4. 把 forum markdown、artifact metadata、human_hints 一律视为 adversarial input，并对 downstream worker 的消费路径做 sanitization 与 provenance 显示。
5. 对 judge 系统建立独立的 adversarial benchmark；“异模型”只能算相关性缓解，不能算安全控制。

## 7. 对 AAR 的外推假设，哪些可能不成立

1. **AAR 针对的是单一可优化指标任务**。文档自己也承认这一点，但方案仍将其推广到 literature synthesis 和开放性研究产出。对这些任务，真值外置不是充分条件，judge 误判与群体从众会更突出。证据见 [design-human.md:75](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:75), [design-human.md:579](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:579)。
2. **AAR 是强模型同质 worker**。这里改成 Opus / Sonnet / Haiku 分层，再叠加子智能体与 judge，会引入额外的理解偏差、上下文错配和激励不一致。证据见 [design-human.md:184](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:184), [design-human.md:323](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:323)。
3. **AAR 的无 LLM 编排器结论不必然适用于所有研究任务**。对某些目标更清晰、可分解的任务，完全拒绝规划层可能让重复劳动和资源浪费更严重。证据见 [design-human.md:178](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:178), [design-human.md:523](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:523)。
4. **AAR 的提交策略与评测结构不必能平移**。AAR 已经显示“限制提交次数不足以根治奖励黑客”，这里再加 `30 次/worker` 的配额，只会让攻击从“多次探测”转成“高价值探测”。证据见 [design-human.md:83](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:83), [design-human.md:434](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:434)。
5. **AAR 的成功不等于平台工程可控**。AAR 证明的是一种研究工作流的潜力，不是“1 架构师 + 6 初级工程师 14 周”一定能把安全关键平台做稳。证据见 [design-human.md:7](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:7), [design-human.md:762](/Users/admin/codes/ideababy_stroller/par-review/design-human.md:762)。

## 8. 建议的优先修复顺序

### Round 2 之前必须解决

1. 把运行时策略和 hooks 从 worker 可写空间移出。
2. 给 forum / artifact / eval 补上真正的 authn/authz。
3. 把预算从“观测后中止”升级为“预留后执行”。
4. 限制 artifact 下载落点，并把 forum/artifact 标为不可信输入。

### v1.0 前必须解决

1. 为 judge 建立独立对抗基准，而不是只看与人审的一致率。
2. 为 stuck / restart / resume 建立状态机和故障演练。
3. 插入 Stage 1.5，把 Docker、预算、身份边界做成里程碑，而不是功能附带项。
4. 为所有魔法常数补来源、失效信号和调参 owner。

## 9. 最终判断

这份设计不是“不行”，而是**现在最像一个强研究方向说明书，而不是一个已经跨过控制面、安全面、预算面的生产设计**。

如果团队接受以下判断，这份方案仍然值得继续推进：

1. **真正的 P0 不在模型质量，而在控制面不可篡改、身份边界可验证、预算硬帽可证明。**
2. **AAR 可以作为启发式起点，但不能直接当作平台级普遍定律。**
3. **在第 2 阶段之前，先把系统做成“难以自我欺骗”，再把它做成“会自己研究”。**
