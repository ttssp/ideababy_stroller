"""
pars.ledger — Run Ledger 读写层。

职责：维护 runs/<ULID>/ 下的 config.yaml、metrics.jsonl、state.json 的
append-only 读写；ULID 生成；checkpoint 路径登记。
由 T009 实现。
"""

# T006: RunConfig schema + config.yaml IO
from pars.ledger.config_schema import (
    BudgetConfig,
    DatasetConfig,
    EnvSnapshot,
    EvalConfig,
    RunConfig,
    TrainingConfig,
)
from pars.ledger.config_io import (
    get_run_config_path,
    load_config,
    save_config,
    update_config_field,
)

# T007: ULID 生成
from pars.ledger.run_id import (
    generate_ulid,
    parse_ulid_timestamp,
    validate_ulid,
)

# T007: state.json 读写 + lifecycle 状态机
from pars.ledger.state import (
    VALID_TRANSITIONS,
    RunPhase,
    RunState,
    new_run_state,
    read_state,
    update_state,
    write_state,
)

# T009: 高层 facade API
from pars.ledger.ledger import (
    create_run,
    get_run_summary,
    list_runs,
    run_exists,
)

# T008: metrics.jsonl append + 读取工具
from pars.ledger.metrics import (
    MetricKind,
    MetricPhase,
    MetricRecord,
    append_metric,
    count_metrics,
    get_metrics_path,
    last_metric,
    read_metrics,
)

__all__ = [  # noqa: RUF022
    # T009: ledger high-level API
    "create_run",
    "get_run_summary",
    "list_runs",
    "run_exists",
    # T006: schema models
    "BudgetConfig",
    "DatasetConfig",
    "EnvSnapshot",
    "EvalConfig",
    "RunConfig",
    "TrainingConfig",
    # T006: IO functions
    "get_run_config_path",
    "load_config",
    "save_config",
    "update_config_field",
    # T007: ULID
    "generate_ulid",
    "parse_ulid_timestamp",
    "validate_ulid",
    # T007: state
    "VALID_TRANSITIONS",
    "RunPhase",
    "RunState",
    "new_run_state",
    "read_state",
    "update_state",
    "write_state",
    # T008: metrics
    "MetricRecord",
    "MetricPhase",
    "MetricKind",
    "append_metric",
    "read_metrics",
    "count_metrics",
    "last_metric",
    "get_metrics_path",
]
