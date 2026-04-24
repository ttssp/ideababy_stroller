# Tech Stack — 003-pA · RecallKit v0.1

**Version**: 0.2.1 · **Updated**: 2026-04-24(OQ1/OQ2/OQ5 CONFIRMED patch · 澄清 only · 不改 stack)· **Source**: spec.md §4 D7-D9 + §3 C21 / architecture.md §6, §7

---

## 0. 一页结论

Python 3.12+ × uv 管理 × Typer CLI × **Unsloth 训练**(OQ1 CONFIRMED 2026-04-24) × **LM Eval Harness 评测**(OQ2 CONFIRMED 2026-04-24) × `claude -p` worker × 本机文件系统 ledger。**无** JS/TS,**无** 容器,**无** DB,**无** 云依赖。

---

## 1. Primary stack(pinned)

| Layer | 选型 | 版本(或约束) | Rationale |
|---|---|---|---|
| **主语言** | Python | **3.12.x**(uv 管理) | Axolotl/Unsloth/HF 生态 = Python;3.12 是 2026 主流 LTS 级,3.13 稳定性还不够(PEP 703 GIL 相关未定);**不**上 3.13 |
| **环境管理** | **uv** | ≥ 0.5.0 | 比 pip/poetry 快 10x;`uv lock --hash` 给 C17 pip 锁定直接支持;CLAUDE.md 私人偏好指定 uv |
| **CLI 框架** | **Typer** + **rich** | Typer ≥ 0.12, rich ≥ 13.7 | Typer 是 Click 的类型友好封装,写 `pars sft start/status/retry/report/compare/resume` 每个 20 行以内;rich 给好看的终端表(`pars compare` 输出) |
| **Worker 底座** | **Claude Code CLI**(`claude`) | Claude Code ≥ 2026-04-latest | headless `claude -p ... --output-format stream-json --max-turns N`;原生支持 hooks / settings / MCP / git worktree;不自研 |
| **训练后端**(D7) | **Unsloth** | ≥ 2026.3.x | 见 §2 详细 rationale;**OQ1 CONFIRMED 2026-04-24** |
| **训练依赖** | transformers / peft / trl / accelerate / bitsandbytes | HF 官方 latest stable(Unsloth 自带兼容版本) | Unsloth 依赖这些;pin 到 Unsloth 推荐 |
| **数据集** | datasets | ≥ 2.20 | HF 生态标准 |
| **评测后端**(D8) | **LM Eval Harness** | `lm-eval-harness` ≥ 0.4.5 | 见 §3 详细 rationale;**OQ2 CONFIRMED 2026-04-24** |
| **GPU driver assumption** | NVIDIA CUDA 12.x + cuDNN | — | 4090 本机 CUDA 12.x 是 2026 标准;不覆盖 ROCm / MPS(见 §5 excluded) |
| **进程管理** | Python `subprocess` + `signal` + `psutil` | psutil ≥ 5.9 | **非** asyncio scheduler;单 host 进程派生单 worker,signal 控制,psutil 探测 GPU/CPU/IO |
| **API proxy**(OQ4) | **LiteLLM**(首选) 或自写最简 | litellm ≥ 1.50 | 见 §4 详细 rationale |
| **报告渲染** | Jinja2 + matplotlib | Jinja2 ≥ 3.1, matplotlib ≥ 3.9 | 模板 + 训练曲线 PNG |
| **Diff/Compare** | `deepdiff` | ≥ 7.0 | config / metric 跨 run diff,比手写好 |
| **Linter** | **ruff** | ≥ 0.5 | CLAUDE.md 私人偏好指定 |
| **Formatter** | ruff format | 同上 | 不装 black |
| **Test** | **pytest** + pytest-cov | pytest ≥ 8.2 | CLAUDE.md 私人偏好指定 |
| **Pre-commit** | pre-commit | ≥ 3.7 | ruff / Conventional Commits 检查 |
| **CI** | GitHub Actions | — | OSS 免费,对齐 C3 |
| **License** | MIT | — | D19 / `compliance.md` |

**Pin 策略**(C17,与 architecture.md §7 对齐):
- `requirements-locked.txt` 由 `uv lock --hash` 生成,**每依赖含 SHA-256 hash**
- `uv.lock` 由 `uv lock` 生成,checked into git(两文件并存)
- worker 内**仅允许**以下三种等价命令(task T015 详细规则):
  1. `pip install -r requirements-locked.txt --require-hashes`
  2. `uv pip install -r requirements-locked.txt --require-hashes`
  3. `uv sync --frozen`(等价 — `--frozen` 强制按 `uv.lock` 精确安装,含 hash 校验)
- 生产依赖全部 exact pin(`==1.2.3`),不用 `^` / `~`
- Dev 依赖(ruff / pytest 等)可用 `>=`,不进 worker 环境

**依赖总数预算**(对齐 C8"技术简单"):
- runtime deps(要跑训练的)≤ 30 个(Unsloth + 其传递依赖 + HF 几个 + CLI 几个,预计 ~25)
- dev deps ≤ 10 个
- 超出预算就砍功能,不砍预算

---

## 2. D7 · 训练后端:Unsloth vs Axolotl(OQ1 CONFIRMED 2026-04-24 · Unsloth)

### 对比

| 维度 | **Unsloth**(CONFIRMED) | Axolotl |
|---|---|---|
| **速度(7B QLoRA, 4090 24GB)** | ~2x Axolotl(官方 benchmark 与社区复现) | baseline |
| **显存(7B QLoRA)** | ~30% 更省(fused kernel + 精细 4-bit) | 紧,24GB 有时 OOM |
| **API 风格** | Python 函数调用,100 行内可跑完整 LoRA SFT | YAML config + CLI,灵活但需写 config |
| **多卡 / FSDP** | 2026 已支持但非强项 | Axolotl 强项 |
| **模型覆盖** | Llama / Qwen / Mistral / Phi / Gemma 全系 + 12× MoE(2026 更新) | 覆盖更广 |
| **社区活跃** | 高,2026 持续更新 | 高 |
| **学习曲线** | 1h 上手 | 半天上手 YAML |
| **符合 D15 "模板修改"路线** | ✅ 模板极简,100 行覆盖 | ⚠️ 模板 = YAML,Python 只少量胶水 |

### 为什么推荐 Unsloth(3 条决定性 · CONFIRMED 2026-04-24)

1. **4090 24GB 紧张场景**:30% 显存优势可能是 7B QLoRA 跑得通 / 跑不通的分水岭。PRD §9 Biggest risk 明示"4090 24GB 紧张但可行",Unsloth 是最直接的应对。
2. **速度 = 成本 = 迭代**:2x 速度意味着单 run < 12h 的 O5 目标更容易达成,且便于操作员在 demo 阶段反复迭代超参。
3. **C8 "技术简单"**:Unsloth 的 Python API 比 Axolotl YAML 更贴 D15"模板修改"(worker 改 Python 变量比改 YAML block 更自然,LLM 生成成功率更高)。

### Unsloth 的风险(接受)

- **多卡 / FSDP 不是 Unsloth 强项**:v0.1 = 单 4090,不需要;若操作员未来想上多卡,需切 Axolotl(v0.2 议题)
- **API 比 YAML 灵活度低**:Axolotl YAML 能支持一些边缘 config 组合;Unsloth 默认覆盖 80% 场景,剩余 20% 可以 hack
- **2026 更新快,pinned 版本要跟**:每 1-2 个月 review 一次

### 如果操作员回复"选 Axolotl"(OQ1 更改)

- D7/D15 模板结构改 YAML + Python 胶水两层
- Phase 1 训练 backend 集成任务预算 +10-20h(Axolotl YAML 学习 + debug)
- 显存紧张时可能做不到 Qwen3-4B full QLoRA,demo 可能降级到 TinyLlama 1.1B

---

## 3. D8 · 评测后端:LM Eval Harness vs 自包装(OQ2 CONFIRMED 2026-04-24 · LM Eval Harness)

### 对比

| 维度 | **LM Eval Harness**(CONFIRMED) | 自包装 |
|---|---|---|
| **数据集覆盖** | GSM8K / HumanEval / MMLU / ARC / TruthfulQA 等 150+ | 从零写每个 |
| **初次 setup 时间** | 0.5-1 天(装 + 跑通一个 task) | 每 task 0.5-1 天 |
| **长期维护** | 社区维护,跟模型升级 | 自维护 |
| **N-shot / 答案抽取 / metric 细节** | 已标准化,对齐 Open LLM Leaderboard | 自实现,易踩坑 |
| **对 demo 可信度** | 用同社区标准 = 可复现 + 可与其他 model 比 | 可信度需自证 |
| **依赖重量** | 中等(torch / datasets + 自带几十个任务) | 轻 |
| **自定义 task** | 支持,但要写 YAML + Python | 完全自由 |

### 为什么推荐 LM Eval Harness(3 条决定性 · CONFIRMED 2026-04-24)

1. **demo 可复现 > 代码简短**:PRD §6 O4 要求"他人本机重现"。用社区标准意味着他人可以用同一 eval 配置验证,不需要信任我们的自包装脚本。
2. **GSM8K / HumanEval 原生支持**:PRD OQ3 候选数据集都在 harness 覆盖内,零成本。
3. **C8 "技术简单" 的误读防御**:"简单"不等于"重新实现";LM Eval Harness 已封装 N-shot prompting / 答案抽取 / metric 计算,自包装等于重写轮子。

### LM Eval Harness 的风险(接受)

- **首次 setup 半天到 1 天**:Phase 1 eval 集成预算已留 buffer
- **重**:增加 ~5 个传递依赖,但在 30 个总预算内
- **自定义 task 稍麻烦**:v0.1 不用自定义 task(PRD demo 用现成的 GSM8K 即可)

### 如果操作员回复"选自包装"(OQ2 更改)

- D8 变更,`templates/eval_script.py.j2` 改为手写简单 eval(按模板读 jsonl → model forward → metric)
- Phase 1 eval 集成任务 -10h(短期省事)
- Demo 可信度需另写 README 解释"为什么你该信我们的 eval 数字"
- Phase 3 增加"eval 数字与 LM Eval Harness 等效性"抽测

---

## 4. OQ4 · API Proxy:LiteLLM vs 自写

| 维度 | **LiteLLM**(默认推荐) | 自写 |
|---|---|---|
| **代码量** | 0(用现成) | ~150 行 Python + httpx |
| **功能** | 多 provider / 路由 / 重试 / 日志 已有 | 仅转发 |
| **依赖** | +1 中型包 | httpx 一个 |
| **Bind localhost** | 支持,需 config | 默认 |
| **审计日志** | 自带 | 自写 |
| **v0.1 只需 Anthropic 一家** | 稍 overkill,但能用 | 刚刚好 |

**默认**:LiteLLM。**fallback**:若 LiteLLM 启动慢 / 依赖冲突,自写(`aiohttp` 或 `httpx` + 200 行内)。

**强制配置**:
- `bind = 127.0.0.1:<port>`(禁止 0.0.0.0)
- 仅放行 `/v1/messages` 等 Anthropic 必要端点
- 请求日志脱 key 后写 `runs/<id>/artifacts/api_log.jsonl`

---

## 5. Excluded alternatives(考虑过,显式拒绝)

| 被拒 | 拒绝理由 |
|---|---|
| **TypeScript / Node.js** | 训练生态 = Python;MCP server 不做(架构 §14) |
| **Docker / Containerd** | L3R0 红线(Block 5) |
| **asyncio scheduler / Celery / RQ** | L3R0 红线(Block 5)+ 单 worker 顺序不需要 |
| **Redis / Postgres / SQLite / DuckDB** | 单 run 单文件系统已够(architecture §11 A5);C8 简单优先 |
| **FastAPI / Streamlit / Flask** | D6 不做 Web UI;localhost API proxy 是唯一例外 |
| **Prometheus / Grafana** | L2 原方案的重度可观测性过度;单 run 本地 `cat metrics.jsonl` 已够 |
| **Axolotl**(默认) | OQ1 默认选 Unsloth,理由 §2 |
| **自包装 eval**(默认) | OQ2 默认选 LM Eval Harness,理由 §3 |
| **Jupyter / Colab** | CLI 优先(C4);用户可以自己在 Jupyter 里 `!pars sft start ...`,但产品不依赖 |
| **MLflow / W&B / Trackio** | v0.1 不做 experiment tracker 集成;Trackio 是"对齐共识"但不是"依赖"(L3 stage doc 已明示本地 ledger 就是最低共识)。v0.2 可加 |
| **MPS (Apple Silicon)** | L3 stage doc 诚实检查 §1 明示未实测;操作员明确有 NVIDIA 4090,v0.1 只保证 CUDA 12.x 路径 |
| **ROCm (AMD)** | 同上,生态成熟度 unclear,不在 v0.1 覆盖 |
| **Weaviate / Qdrant / Chroma(向量库)** | PRD §5.5 明示不做 |
| **Click**(CLI) | Typer 是 Click 的类型超集,无损代替 |
| **Poetry**(环境) | uv 更快 + CLAUDE.md 偏好 |
| **Docker compose local**(用于 API proxy) | 不必,LiteLLM 可 `uv run` 直接起;不做 Docker = 不做 Docker |

---

## 6. 依赖策略与审计

**Pin**:
- 生产依赖全部 `==X.Y.Z`(exact)
- `requirements-locked.txt` 含 SHA-256 hash
- `uv lock` 每次更新都 commit

**审计**:
- 每次添加依赖跑 `uv run pip-audit`(或 `safety check`)
- 0 critical / 0 high vulnerability 才 merge
- License 扫描:`uv run pip-licenses --format=json`,**拒绝** GPL / AGPL(避免 MIT LICENSE 冲突,见 `compliance.md`)

**升级**:
- 每月 1 次(operator 定时任务)review `uv lock --upgrade --dry-run`
- Unsloth / transformers / peft / lm-eval-harness 单独 review,因为 API 变化可能破训练
- CI 跑完整 demo smoke 验证升级无回归

**总依赖预算**:
- Runtime ≤ 30
- Dev ≤ 10
- 超出就砍功能或压合并

---

## 7. 最小系统需求(README 必须声明)

| 项 | 最低 | 推荐 |
|---|---|---|
| OS | macOS 14+ / Ubuntu 22.04+ | Ubuntu 22.04 LTS |
| GPU | NVIDIA 16GB+(TinyLlama 1.1B demo) | NVIDIA 24GB(Qwen3-4B QLoRA, 本项目假设) |
| CUDA | 12.1+ | 12.4 |
| RAM | 32GB | 64GB |
| 磁盘 | 100GB 空余(HF cache + checkpoints) | 500GB SSD |
| Python | 3.12.x | 3.12.x |
| Claude Code CLI | 2026-04-latest | 最新 |
| **`.claude/` 只读分离**(C21 fail-closed,**OQ5 CONFIRMED 2026-04-24**) | **MacFUSE + bindfs**(macOS,**OQ5 CONFIRMED**)<br/>fallback 保留防御:`sudo chflags uchg` / `sudo chattr +i`(装机一次性) | MacFUSE + bindfs(最严格,无需重复 sudo) |
| `ANTHROPIC_API_KEY` | 必须 | — |
| `HF_TOKEN` | 仅 gated 模型必须(Llama 3.1 等);**公开 demo(Qwen3-4B + gsm8k)无需** | — |

**OQ5 决策落地(CONFIRMED 2026-04-24 · MacFUSE + bindfs)**:
- 主路径(已确认):MacFUSE + bindfs,安装步骤 `brew install --cask macfuse && brew install bindfs`(首次启动提示 kernel extension 加载,需重启一次)
- fallback 保留作防御:若 MacFUSE 在某次启动不可用(卸载 / kext 未加载),Phase 0 装机脚本提示 `sudo chflags uchg worker_claude_dir/` 一次(每次仓库 clone 后执行一次)
- refuse-to-start 兜底:二者都不可用时 v0.1 **refuse to start**(C21 硬约束)

**HF_TOKEN 最小 scope(R1 HIGH #1 修复)**:
- **默认场景无需 HF_TOKEN**:Qwen3-4B + gsm8k-100 是公开仓库,不需 token
- 仅 gated 模型(Llama 3.1 等)才需 token;
- 要求 **read-only scope**,**禁止 write / private mirror / write-repo 权限**
- README 模板文本:
  > If you use Llama or other gated models, generate an HF token with READ-ONLY scope only. DO NOT grant write, private-mirror, or write-repo permissions. RecallKit only needs to download public or gated models; it never writes to HuggingFace.

---

## 8. 版本表(spec 冻结时的 pin 参考,task-decomposer/parallel-builder 以 `uv lock` 为准)

```
python = "^3.12"
# Runtime
unsloth = "2026.3.*"  # 待 uv lock 后精确
transformers = "4.44.*"
peft = "0.11.*"
trl = "0.9.*"
accelerate = "0.34.*"
bitsandbytes = "0.44.*"
datasets = "2.20.*"
lm-eval-harness = "0.4.5"
matplotlib = "3.9.*"
typer = "0.12.*"
rich = "13.7.*"
jinja2 = "3.1.*"
deepdiff = "7.0.*"
psutil = "5.9.*"
litellm = "1.50.*"
ulid-py = "1.1.*"
pyyaml = "6.0.*"

# Dev
ruff = "^0.5"
pytest = "^8.2"
pytest-cov = "^5.0"
pre-commit = "^3.7"
pip-audit = "^2.7"
pip-licenses = "^4.5"
```

**注意**:上面是 spec 阶段的参考。实际 `requirements-locked.txt` 由 Phase 0 Task 完成时 `uv lock --hash` 生成 + commit,之后除非 security advisory 否则不动。
