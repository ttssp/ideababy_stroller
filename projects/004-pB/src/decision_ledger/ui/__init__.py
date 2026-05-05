"""
Web UI 包 — T004
结论: 导入此包时自动通过 plugin registry 注册 shell router
细节: import 副作用模式，main.py 不需修改
"""

from decision_ledger.ui import app as _app_module  # noqa: F401 — 触发 router 注册副作用

__all__: list[str] = []
