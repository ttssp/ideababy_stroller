"""
pars.proxy — API Proxy 层。

职责：在 localhost 启动轻量 HTTP proxy，持有 ANTHROPIC_API_KEY，
对 worker 子进程隐藏真实 key；实现预算前置拒绝（pre-reject）逻辑。

T010 exports:
  - budget_estimator: estimate_request_cost, count_input_tokens, PRICING, SAFETY_COEFFICIENT
  - config:           ProxyConfig, _pick_free_port
  - server:           start_proxy, stop_proxy, ProxyHandle
  - prereject_middleware: check_budget_prereject, BudgetPrerejectResult
  - audit_log:        append_audit_record, get_audit_log_path
"""

from pars.proxy.audit_log import append_audit_record, get_audit_log_path
from pars.proxy.budget_estimator import (
    PRICING,
    SAFETY_COEFFICIENT,
    Pricing,
    count_input_tokens,
    estimate_request_cost,
)
from pars.proxy.config import ProxyConfig, _pick_free_port
from pars.proxy.prereject_middleware import BudgetPrerejectResult, check_budget_prereject
from pars.proxy.server import ProxyHandle, start_proxy, stop_proxy

__all__ = [
    # budget_estimator
    "PRICING",
    "SAFETY_COEFFICIENT",
    "Pricing",
    "count_input_tokens",
    "estimate_request_cost",
    # config
    "ProxyConfig",
    "_pick_free_port",
    # server
    "ProxyHandle",
    "start_proxy",
    "stop_proxy",
    # prereject_middleware
    "BudgetPrerejectResult",
    "check_budget_prereject",
    # audit_log
    "append_audit_record",
    "get_audit_log_path",
]
