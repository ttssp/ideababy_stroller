"""
pars.proxy.prereject_middleware — USD 预算前置拒绝逻辑（C20 硬约束）。

结论：
  `check_budget_prereject` 在请求转发给 upstream 之前执行：
  1. 读取 state.json 中的 usd_spent（fcntl.flock 保护）
  2. 用 budget_estimator 估算本次请求成本（含 SAFETY_COEFFICIENT）
  3. 若 usd_spent + estimated_cost >= cap → BudgetPrerejectResult(should_reject=True)
  4. state.json 不可读 → fail-safe 拒绝（保守策略，严守 C20 硬帽）

设计约束：
  - 此函数是纯判断函数，不调用 upstream API
  - 调用方（server.py / LiteLLM 钩子）负责根据结果返回 HTTP 402/429
  - 通过 upstream 之后，调用方用实际 usage 更新 usd_spent（audit + T018）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pars.ledger.state import read_state
from pars.proxy.budget_estimator import estimate_request_cost


# ---------------------------------------------------------------------------
# 结果数据类
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BudgetPrerejectResult:
    """check_budget_prereject 的返回值，包含拒绝判断和诊断信息。

    字段：
        should_reject:  True = 必须返回 HTTP 4xx，False = 放行
        http_status:    拒绝时的 HTTP 状态码（402 或 429）；放行时 None
        usd_spent:      当前已消费（来自 state.json，或 fail-safe 时为 None）
        estimated_cost: 本次请求的预估 USD 成本
        usd_cap:        调用方传入的预算上限
        error_body:     拒绝时的 JSON 响应体 dict（含 error/usd_spent/estimate/cap）
    """

    should_reject: bool
    http_status: int | None
    usd_spent: float | None
    estimated_cost: float
    usd_cap: float
    error_body: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# 主检查函数
# ---------------------------------------------------------------------------


def check_budget_prereject(
    *,
    request_body: dict[str, Any],
    run_id: str,
    usd_cap: float,
) -> BudgetPrerejectResult:
    """在转发请求前检查预算是否充足（C20 硬约束）。

    逻辑：
        1. 估算本次请求成本（budget_estimator）
        2. 读 state.json.usd_spent（fcntl.flock 保护，T007 read_state）
        3. 若 usd_spent + estimated >= cap → 拒绝
        4. state.json 不可读 → fail-safe 拒绝（绝不放行未知状态的请求）

    Args:
        request_body: Anthropic Messages API 请求 body dict（含 model/max_tokens/messages）
        run_id:       run 唯一标识，用于定位 state.json
        usd_cap:      USD 硬帽上限（来自 ProxyConfig 或 CLI 参数）

    Returns:
        BudgetPrerejectResult（frozen，包含完整诊断信息）

    注意：
        此函数不调用 upstream API，纯判断。
    """
    # 1. 估算本次请求成本（含 SAFETY_COEFFICIENT 缓冲）
    estimated_cost = estimate_request_cost(request_body)

    # 2. 读取当前已消费（state 不可读时 fail-safe 拒绝）
    try:
        state = read_state(run_id)
        usd_spent = state.usd_spent
    except FileNotFoundError:
        # fail-safe：state.json 不存在 → 无法确认预算状态 → 保守拒绝
        return BudgetPrerejectResult(
            should_reject=True,
            http_status=503,
            usd_spent=None,
            estimated_cost=estimated_cost,
            usd_cap=usd_cap,
            error_body={
                "error": "budget_prereject",
                "reason": "state.json not found — cannot confirm budget status",
                "estimate": estimated_cost,
                "cap": usd_cap,
            },
        )
    except Exception as exc:
        # 其他读取错误 → 同样保守拒绝
        return BudgetPrerejectResult(
            should_reject=True,
            http_status=503,
            usd_spent=None,
            estimated_cost=estimated_cost,
            usd_cap=usd_cap,
            error_body={
                "error": "budget_prereject",
                "reason": f"state read error: {exc}",
                "estimate": estimated_cost,
                "cap": usd_cap,
            },
        )

    # 3. 预算检查：usd_spent + estimated >= cap → 拒绝
    if usd_spent + estimated_cost >= usd_cap:
        return BudgetPrerejectResult(
            should_reject=True,
            http_status=402,
            usd_spent=usd_spent,
            estimated_cost=estimated_cost,
            usd_cap=usd_cap,
            error_body={
                "error": "budget_prereject",
                "usd_spent": usd_spent,
                "estimate": estimated_cost,
                "cap": usd_cap,
                "message": (
                    f"预算已耗尽：已消费 ${usd_spent:.4f}，本次预估 ${estimated_cost:.4f}，"
                    f"超出上限 ${usd_cap:.2f}"
                ),
            },
        )

    # 4. 预算充足 → 放行
    return BudgetPrerejectResult(
        should_reject=False,
        http_status=None,
        usd_spent=usd_spent,
        estimated_cost=estimated_cost,
        usd_cap=usd_cap,
        error_body={},
    )
