"""
pars.ledger.config_schema — Run config 的 Pydantic v2 Schema。

结论：RunConfig 是所有下游模块（orch/report/compare/resume）读写的契约，
      必须先稳定。使用 Pydantic v2 确保 type-safe，并通过 extra="forbid"
      拒绝未知字段（防止 typo 导致的静默错误）。

字段来源：
  - architecture.md §4.2 - 单 run 落地布局（config.yaml 结构）
  - architecture.md §9   - 决策报告 schema 的元数据字段清单
  - spec.md §2.1 IN scope D14 - ULID 命名
  - T006.md Outputs 字段列表

设计原则：
  1. 所有子 model 均 extra="forbid"，避免 typo 静默通过
  2. TrainingConfig 为可选（baseline run 时为 None）
  3. datetime 字段序列化为 ISO8601 字符串（YAML 跨实现不稳）
  4. EnvSnapshot 字段来自 T019（本 task 只定义 schema，不做采集逻辑）
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_serializer


# ---------------------------------------------------------------------------
# 子模型：DatasetConfig
# ---------------------------------------------------------------------------

class DatasetConfig(BaseModel):
    """数据集配置。

    字段来源：T006.md Outputs - dataset: DatasetConfig(hf_id, split, n_samples)
    """

    model_config = ConfigDict(extra="forbid")

    hf_id: str = Field(
        description="HuggingFace 数据集仓库 ID，如 'gsm8k'、'HuggingFaceH4/ultrachat_200k'",
    )
    split: str = Field(
        description="数据集 split 名称，如 'train'、'validation'、'test'",
    )
    n_samples: int = Field(
        ge=1,
        description="使用的样本数量（子集大小）；ge=1 保证至少有 1 条数据",
    )


# ---------------------------------------------------------------------------
# 子模型：TrainingConfig
# ---------------------------------------------------------------------------

class TrainingConfig(BaseModel):
    """LoRA SFT 训练配置。

    字段来源：T006.md Outputs - training: TrainingConfig
              architecture.md §4.2 lora_script.py.j2 模板参数
    backend 默认 unsloth（spec.md §2.1 D7 OQ1 CONFIRMED）
    """

    model_config = ConfigDict(extra="forbid")

    backend: Literal["unsloth"] = Field(
        default="unsloth",
        description="训练后端，固定为 'unsloth'（spec.md §2.1 D7 OQ1 CONFIRMED）",
    )
    lora_rank: int = Field(
        ge=1,
        le=256,
        default=16,
        description="LoRA rank（r）；通常 4-64；ge=1 le=256",
    )
    lora_alpha: int = Field(
        ge=1,
        default=32,
        description="LoRA alpha（缩放系数）；通常 = rank 或 2×rank；ge=1",
    )
    lr: float = Field(
        gt=0,
        lt=1,
        default=2e-4,
        description="学习率（learning rate）；gt=0 lt=1",
    )
    epochs: int = Field(
        ge=1,
        le=100,
        default=3,
        description="训练 epoch 数；ge=1 le=100",
    )
    batch_size: int = Field(
        ge=1,
        default=4,
        description="per-device batch size；ge=1",
    )
    max_seq_len: int = Field(
        ge=64,
        le=32768,
        default=2048,
        description="最大序列长度（tokens）；ge=64 le=32768",
    )


# ---------------------------------------------------------------------------
# 子模型：EvalConfig
# ---------------------------------------------------------------------------

class EvalConfig(BaseModel):
    """评测配置。

    字段来源：T006.md Outputs - eval: EvalConfig(backend, tasks, n_shot, limit)
              backend 默认 lm-eval（spec.md §2.1 D8 OQ2 CONFIRMED）
    """

    model_config = ConfigDict(extra="forbid")

    backend: Literal["lm-eval"] = Field(
        default="lm-eval",
        description="评测后端，固定为 'lm-eval'（spec.md §2.1 D8 OQ2 CONFIRMED）",
    )
    tasks: list[str] = Field(
        min_length=1,
        description="lm-eval task 名称列表，如 ['gsm8k', 'arc_easy']；不得为空",
    )
    n_shot: int = Field(
        ge=0,
        default=0,
        description="few-shot 数量；0 表示 zero-shot；ge=0",
    )
    limit: int | None = Field(
        default=None,
        ge=1,
        description="eval 子集大小；None 表示使用全集；若设置则 ge=1",
    )


# ---------------------------------------------------------------------------
# 子模型：BudgetConfig
# ---------------------------------------------------------------------------

class BudgetConfig(BaseModel):
    """预算配置（architecture.md §5 / §5.1 硬帽前置拒绝）。

    字段来源：T006.md Outputs - budget: BudgetConfig
              spec.md §2.1 O5 - 端到端单 run < 12h、< $30 API 费
    """

    model_config = ConfigDict(extra="forbid")

    usd_cap: float = Field(
        gt=0,
        le=1000,
        description="USD 硬帽（美元）；proxy 前置拒绝超出此限额的请求；gt=0 le=1000",
    )
    wall_clock_hours_cap: float = Field(
        gt=0,
        le=48,
        description="wall-clock 时间上限（小时）；第二道保险（SIGINT 路径）；gt=0 le=48",
    )
    gpu_hours_cap: float = Field(
        gt=0,
        description="GPU 小时上限；第二道保险（SIGINT 路径）；gt=0",
    )


# ---------------------------------------------------------------------------
# 子模型：EnvSnapshot
# ---------------------------------------------------------------------------

class EnvSnapshot(BaseModel):
    """运行环境快照（T019 负责采集，本 task 仅定义 schema）。

    字段来源：T006.md Outputs - env_snapshot: EnvSnapshot
              architecture.md §4.2 artifacts/env_snapshot.txt
    """

    model_config = ConfigDict(extra="forbid")

    python_version: str = Field(
        description="Python 版本字符串，如 '3.12.12'",
    )
    platform: str = Field(
        description="平台字符串，如 'linux-x86_64'、'darwin-arm64'",
    )
    cuda_version: str | None = Field(
        default=None,
        description="CUDA 版本字符串，如 '12.4'；macOS 时为 None",
    )
    gpu_name: str | None = Field(
        default=None,
        description="GPU 型号名称，如 'NVIDIA RTX 4090'；无 GPU 时为 None",
    )
    pip_freeze_sha256: str | None = Field(
        default=None,
        description="pip freeze 输出的 SHA-256 摘要（供复现校验）；T019 填入",
    )


# ---------------------------------------------------------------------------
# 顶层模型：RunConfig
# ---------------------------------------------------------------------------

class RunConfig(BaseModel):
    """单次 run 的完整配置契约。

    结论：所有下游模块（orch/report/compare/resume）均通过 RunConfig 读写
          config.yaml；本 schema 是唯一真相源。

    字段来源：
      - architecture.md §4.2 - config.yaml 文件内容
      - architecture.md §9   - 决策报告 schema 元数据字段
      - spec.md §2.1 D14     - ULID 命名（run_id 正则）
      - T006.md Outputs       - 完整字段列表

    设计约束：
      - extra="forbid"：拒绝未知字段（防 typo 静默通过）
      - run_id 可选（None 在 Orchestrator 创建前），由 ledger 在启动时填入
      - training 可选（baseline run 不做 LoRA SFT）
      - datetime 序列化为 ISO8601 字符串（YAML datetime 跨实现不稳）
    """

    model_config = ConfigDict(extra="forbid")

    # ------ 元信息 ------
    run_id: str | None = Field(
        default=None,
        pattern=r"^[0-9A-HJKMNP-TV-Z]{26}$",
        description="ULID 格式的 run ID（正则 ^[0-9A-HJKMNP-TV-Z]{26}$）；"
                    "由 Orchestrator 在启动时填入，None 表示尚未分配",
    )
    research_question: str = Field(
        min_length=1,
        max_length=500,
        description="研究假设 / 问题（非空，≤500 chars）；与决策报告失败归因关联",
    )
    base_model: str = Field(
        description="HuggingFace 模型仓库 ID，如 'Qwen/Qwen3-4B'",
    )

    # ------ 子配置 ------
    dataset: DatasetConfig = Field(
        description="数据集配置（hf_id, split, n_samples）",
    )
    training: TrainingConfig | None = Field(
        default=None,
        description="LoRA SFT 训练配置；baseline run 时为 None",
    )
    eval: EvalConfig = Field(
        description="评测配置（backend, tasks, n_shot, limit）",
    )
    budget: BudgetConfig = Field(
        description="预算配置（usd_cap, wall_clock_hours_cap, gpu_hours_cap）",
    )
    env_snapshot: EnvSnapshot | None = Field(
        default=None,
        description="运行环境快照；由 T019 在 run 启动时填入；None 表示尚未采集",
    )

    # ------ 时间戳 ------
    created_at: datetime | None = Field(
        default=None,
        description="run 创建时间（ISO8601 UTC）；由 Orchestrator 在创建时填入",
    )
    started_at: datetime | None = Field(
        default=None,
        description="run 实际开始时间（worker 启动后）；None 表示尚未开始",
    )
    completed_at: datetime | None = Field(
        default=None,
        description="run 完成时间；None 表示尚未完成",
    )

    # ------ 计量字段（运行时填入）------
    wall_clock_seconds: float | None = Field(
        default=None,
        ge=0,
        description="实际 wall-clock 耗时（秒）；run 完成后由 Orchestrator 填入",
    )
    usd_total: float | None = Field(
        default=None,
        ge=0,
        description="实际 API USD 消耗；Budget Tracker 累计更新",
    )
    gpu_hours: float | None = Field(
        default=None,
        ge=0,
        description="实际 GPU 小时消耗；run 完成后填入",
    )

    # ------ 可选元数据 ------
    notes: str | None = Field(
        default=None,
        description="人类可读备注；可在 run 进行中追加",
    )
    parent_run_id: str | None = Field(
        default=None,
        pattern=r"^[0-9A-HJKMNP-TV-Z]{26}$",
        description="父 run 的 ULID（retry / variant 链接）；None 表示无父 run",
    )
    retry_hypothesis: str | None = Field(
        default=None,
        max_length=1000,
        description="retry 假设文本（≤1000 chars）；记录本次 retry 的动机；None 表示非 retry run",
    )

    # ------ 序列化：datetime → ISO8601 字符串 ------
    # Pydantic v2 用 field_serializer 替代已废弃的 json_encoders
    # 确保 model_dump(mode="json") 中 datetime 字段输出 ISO8601 字符串
    # 而非 datetime 对象（yaml.safe_dump 对 datetime 对象序列化行为因实现而异）

    @field_serializer("created_at", "started_at", "completed_at", when_used="json")
    def _serialize_datetime(self, value: datetime | None) -> str | None:  # noqa: ANN101
        """将 datetime 字段序列化为 ISO8601 字符串（json mode 下生效）。"""
        return value.isoformat() if value is not None else None
