# Compliance — 003-pA · RecallKit v0.1

**Version**: 0.2 · **Updated**: 2026-04-24(R1 HIGH #4 demo artifact 分发补全)· **Source**: spec.md §4 D19 + risks.md §6

---

## 0. 一页结论

RecallKit v0.1 = **单人本机 OSS CLI 工具**,无法定监管合规义务(无 PII 处理 / 无支付 / 无医疗 / 无儿童数据 / 无金融数据)。本文件仅覆盖**操作员责任声明** + **依赖 license check**,不是法律文件,仅给 task-decomposer / parallel-builder 做"不要把合规想成不存在"的提示。

---

## 1. 适用监管框架检查(全部 N/A,给出理由)

| 框架 | 适用? | 理由 |
|---|---|---|
| **GDPR**(EU 个人数据保护) | **N/A** | 产品不收集 / 处理 / 存储任何用户个人数据;所有数据本地,不传云(C14) |
| **CCPA / CPRA**(加州) | **N/A** | 同上 |
| **PDPA**(新加坡) | **N/A** | 同上 |
| **PIPEDA**(加拿大) | **N/A** | 同上 |
| **HIPAA**(美国医疗) | **N/A** | 产品不设计用于医疗数据;用户若违反自用途自担 |
| **PCI DSS**(支付) | **N/A** | 无支付功能 |
| **COPPA**(美国儿童) | **N/A** | 非面向儿童产品 |
| **SEC / FINRA**(美国金融) | **N/A** | 非金融服务 |
| **EU AI Act**(2026 生效) | **N/A 对工具本身**,操作员应用时自判 | RecallKit 是 ML 训练**工具**,不是部署的 AI 系统;但若操作员训练的模型用于"high-risk" 场景(CV for 招聘、医疗诊断等),操作员需自行评估义务。**README 需声明这一点**。 |
| **中国 生成式人工智能服务管理暂行办法**(2023 生效) | **N/A 对工具本身** | 同上;本产品是个人研究工具,非服务提供者 |
| **开源出口管制(美国 EAR 734.7 / 740.13 TSU)** | 可能适用 | 本产品含加密相关依赖(HTTPS via requests / httpx);主流 OSS 路径 = 用 TSU 豁免,README 声明即可 |

**操作员责任声明(README 必须含)**:

> RecallKit is a research tool. If you use it to train models that will be deployed in regulated contexts (healthcare, finance, hiring, surveillance, etc.), you are responsible for evaluating the applicable regulations (EU AI Act, local ML regulations, etc.) and ensuring your downstream model complies. RecallKit does not evaluate or enforce any such compliance on your behalf.

---

## 2. 用户数据与训练数据处理责任

**操作员使用 RecallKit 时可能投喂**:
- HuggingFace 公开数据集(GSM8K / Alpaca 等)→ 一般为公开,无 PII 问题
- HuggingFace gated 模型(Qwen3-4B / Llama 3.1 等)→ 用户持 `HF_TOKEN` 自行接受 license
- 操作员自有数据集(若含 PII / 敏感内容)→ **RecallKit 不主动识别 PII,不主动过滤**

**产品立场**:
1. RecallKit 视训练数据为"操作员自己的文件",不扫描 / 不上传 / 不修改
2. 所有数据保持本地(C14 架构约束),API proxy 仅转发 claude-p worker 与 Anthropic 的对话,**不会把训练数据集内容转给 Anthropic**(worker 通常不把整个数据集塞进 prompt,只塞 sample 给 LLM 看格式)
3. 若操作员的训练数据含 PII,操作员需自己决定是否投喂给 Claude(通过 worker prompt)— 这是操作员对 Anthropic DPA 的责任,不是 RecallKit 的义务

**README 必须含**:

> RecallKit treats your dataset as opaque bytes — it does not inspect, sanitize, or redact PII. If your training data contains personal data and you instruct the worker to paste samples into prompts, that data will reach Anthropic's API under your Anthropic account's Data Processing Addendum. You are responsible for complying with your own obligations (GDPR data minimization, etc.).

---

## 3. License 选择:MIT(D19)

**为什么 MIT**:
- 对齐 C8 "速度 + 简单" 优先
- 最宽松,对生态扩散友好
- 兼容所有主要 OSS 依赖(Apache 2.0 / BSD / MIT)
- 不引入 copyleft 义务

**拒绝的替代**:
- **Apache 2.0**:技术上 OK,但 v0.1 不需要专利条款;MIT 更简洁
- **AGPL / GPL**:copyleft 传染,对用户 / 潜在 contributor 构成摩擦,反 C8
- **Unlicense / CC0**:放弃版权,法律效力在部分司法辖区(如 EU)不稳

**LICENSE 文件**:标准 MIT 文本,copyright holder = 操作员 real name 或 github handle,year = 2026。

---

## 4. 第三方依赖 license check

### 4.1 策略

- 所有**运行时**依赖 license 必须与 MIT **兼容**
- **拒绝**:GPL / AGPL / LGPL(copyleft 传染或 linking 歧义)
- **接受**:MIT / Apache 2.0 / BSD 3-Clause / BSD 2-Clause / ISC / PSF(Python) / zlib
- 每月 `uv run pip-licenses --format=markdown --output-file=docs/LICENSES.md` 自动生成 + review

### 4.2 主要依赖 license 预检(tech-stack §8)

| 依赖 | License | 兼容? |
|---|---|---|
| Python 3.12 | PSF License | ✅ |
| Unsloth | Apache 2.0 | ✅ |
| transformers | Apache 2.0 | ✅ |
| peft | Apache 2.0 | ✅ |
| trl | Apache 2.0 | ✅ |
| accelerate | Apache 2.0 | ✅ |
| bitsandbytes | MIT | ✅ |
| datasets | Apache 2.0 | ✅ |
| lm-eval-harness | MIT | ✅ |
| matplotlib | PSF License(Python-based) + matplotlib 自 license | ✅ |
| typer | MIT | ✅ |
| rich | MIT | ✅ |
| jinja2 | BSD 3-Clause | ✅ |
| deepdiff | MIT | ✅ |
| psutil | BSD 3-Clause | ✅ |
| litellm | MIT | ✅ |
| ulid-py | MIT | ✅ |
| pyyaml | MIT | ✅ |
| ruff | MIT | ✅ |
| pytest | MIT | ✅ |
| pip-audit | Apache 2.0 | ✅ |
| pip-licenses | MIT | ✅ |

**预判**:所有现选依赖兼容 MIT。若未来某依赖切 GPL 版本,必须找 drop-in 替代或砍功能。

### 4.3 CI 检查

**task 分配(R1 Medium #3 修复)**:`.github/workflows/license-check.yml` 的创建与维护**归属 T028**(release polish 阶段),具体内容:
- 每 PR 跑 `pip-licenses --format=json`,grep `GPL|AGPL|LGPL` → 有即 fail
- 每月 scheduled job 同上,告警操作员
- 同时覆盖 §4.4.3 的 demo artifact 自动化检查(grep 硬路径 / secret 模式 / `.gitignore` 一致性)

---

## 4.4 Demo artifact distribution checklist(R1 HIGH #4 新增)

**场景**:T027 / T028 在 README、`demo/gsm8k-100-qwen3-4b/` 与 `docs/demo-reproduction.md` 中分发**demo 相关 artifact**(训练配置、产出指标、LoRA adapter 权重等)。这些 artifact 不是纯工具代码,部分继承 base model / dataset 的 license 约束,必须显式检查。

### 4.4.1 Base model license 传染(artifact 可公开分发?)

| artifact | 来源 | License | 公开 OSS 分发? | 商业分发? |
|---|---|---|---|---|
| **Qwen3-4B base model weights** | 阿里 Tongyi Qianwen License Agreement | 自定义(含商业限制条款,详见 HF model card) | ✅ 允许(引用原 HF repo,不重分发) | ⚠️ 需单独 review 条款,v0.1 demo 纯个人研究,无商业使用 |
| **Llama 3.1 8B base model weights** | Meta Community License (LLAMA 3.1) | 自定义(月 MAU 7亿用户以上需单独商业许可) | ✅ 允许 | ⚠️ 小团队 OK,大企业商用需 review |
| **gsm8k 数据集** | OpenAI / commoncrawl | MIT | ✅ | ✅ |
| **LoRA adapter 权重(demo 训完产出)** | RecallKit 训练 | **继承** base model license(Tongyi Qianwen / LLAMA 3.1 Community) | ✅(需在 adapter README 附 base model license 声明) | 取决于 base model 条款 |
| **训练曲线 PNG / report.md** | RecallKit 输出 | MIT(RecallKit 自身 license) | ✅ | ✅ |
| **config.yaml / metrics.jsonl** | RecallKit 输出 | MIT | ✅ | ✅(但若含路径 / 账号信息需脱敏) |

### 4.4.2 分发前 checklist(T027 release gate)

- [ ] `demo/gsm8k-100-qwen3-4b/run_config.yaml` 仅引用 **public HF repo id**(如 `Qwen/Qwen3-4B`、`gsm8k`),**不附**任何 base model 权重本体
- [ ] `demo/gsm8k-100-qwen3-4b/expected_metrics.md` 仅含指标数字(baseline accuracy / LoRA accuracy / loss 曲线要点),**不**含任何 PII / 内部路径 / Anthropic account 信息
- [ ] **禁止** commit `runs/<id>/checkpoints/*.safetensors` / `*.bin` / LoRA adapter 权重到本仓库(.gitignore 已含);若未来独立发布 LoRA adapter repo,需单独写 license 声明
- [ ] README 的"demo 重现"小节附 base model license 提示:
  - > This demo uses Qwen3-4B under Tongyi Qianwen License. By running this demo you agree to the base model's terms. RecallKit itself is MIT; base model weights are NOT redistributed by this repo.
- [ ] 若操作员选 OQ3 的 Llama 3.1 8B 变体,README 同步加 LLAMA 3.1 Community License 提示
- [ ] `docs/demo-reproduction.md` 不嵌入任何操作员内部路径(如 `/Users/admin/...`)、私有 checkpoint 链接、内部 run id
- [ ] LoRA adapter 权重若未来要公开(v0.2):独立 HF repo + license 明示继承 base model 条款

### 4.4.3 T028 release gate 硬依赖

- T028 的 `.github/workflows/license-check.yml` 必须跑此 checklist 的自动化部分:
  - grep demo README / config 是否含硬路径(`/Users/`、`/home/`)
  - grep 是否有 secret 模式(`sk-ant-`, `hf_`, AWS keys)
  - 运行时确认 `.gitignore` 含 `*.safetensors` / `*.bin` / `checkpoints/` / `runs/*/artifacts/*.pt`
- 手工部分(checklist 4.4.2 前 3 条)由操作员 PR review 时对照勾选

---

## 5. Claude Code 与 Anthropic API 使用

**合规要点**:
- 操作员用自己的 Anthropic account API key,遵循 Anthropic Usage Policies(acceptable use)
- RecallKit 不代操作员与 Anthropic 签合同
- Anthropic API 用量 / 账单是操作员与 Anthropic 的直接关系
- 若操作员跨境使用(如 EU → US API endpoint),由操作员自行评估数据传输影响

**README 必须含**:

> Using RecallKit requires an Anthropic API key and adherence to Anthropic's Usage Policies. Your API usage is billed to your Anthropic account; RecallKit is a client that calls your configured API.

---

## 6. 安全相关"合规"(非法定,但列出便于审计追溯)

以下 spec 决策**等同于**一个最小安全 baseline(不是法律框架,但 task-decomposer 应理解为"硬义务"):

| 条 | 来源 | 实现 |
|---|---|---|
| API key 不落入 worker env | moderator P0-5 / spec C15 | architecture §5 |
| host `.claude/` 只读分离 | moderator P0-2 / spec C16 | architecture §6 |
| pip 锁定 | moderator P0-6 / spec C17 | architecture §7 |
| deny 危险命令 | spec §4.8 | architecture §6 hooks |
| 所有数据本地 | spec C14 | architecture §13 |
| audit log(run ledger 本地) | spec §4.7 | architecture §4.2 |

**不做**(对合规 baseline 够,但若未来商用要补):
- ❌ 日志签名 / 链式 hash(moderator P2-20)
- ❌ 加密 at-rest(本机用户信任自己磁盘)
- ❌ SOC 2 / ISO 27001 审计(单人 OSS 无意义)
- ❌ 数据保留策略 / 自动删除(操作员自己决定)

---

## 7. 法律免责(README 必须含)

模板文本:

```
RecallKit is provided "as is", without warranty of any kind, express or implied,
including but not limited to the warranties of merchantability, fitness for a
particular purpose and noninfringement. In no event shall the authors or
copyright holders be liable for any claim, damages or other liability, whether
in an action of contract, tort or otherwise, arising from, out of or in
connection with the software or the use or other dealings in the software.

You are responsible for:
1. Compliance with applicable laws and regulations in your use of models
   trained with this tool
2. Your use of the Anthropic API and HuggingFace services under their
   respective Terms of Service
3. Ensuring your training data complies with any applicable data protection
   regulations (GDPR, CCPA, etc.)

This tool does not automatically detect or handle personal data, copyrighted
content, or any other legally regulated content in your training data.
```

---

## 8. 审计追溯(若未来被问"某行为是在哪决定的")

| 决策 | 位置 |
|---|---|
| LICENSE = MIT | spec.md D19 + 本文件 §3 |
| 不做 PII 识别 | 本文件 §2 + PRD §5 无相关要求 |
| 依赖 license 策略 | 本文件 §4 |
| 合规 baseline 等同于安全 spec | 本文件 §6 |
| 操作员责任声明 | 本文件 §2, §5, §7 |

---

## 9. 何时重新评估本文件

触发条件:
- 项目从 OSS 工具转为 SaaS / hosted(立刻,全面重写)
- 任一依赖切 GPL / AGPL(立刻,找替代)
- 操作员发现用户在 high-risk 场景部署本工具训练的模型且抱怨"工具没提醒我"(更新 §1 操作员责任声明)
- EU AI Act / 中国生成式 AI 管理办法 等有新具体条款直接指涉 "ML 训练工具"(重新评估 §1)
- 首次 commercial contribution 或法人实体承接项目(全面法务 review)

---

**底线**:v0.1 在法律层面是"操作员的个人研究脚本",不承担服务提供者 / 数据处理者义务;README 说清楚 + LICENSE 选对 + 依赖 license 合规 = 当前合规工作**完成**。
