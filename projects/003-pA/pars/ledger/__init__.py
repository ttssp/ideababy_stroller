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

__all__ = [
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
]
