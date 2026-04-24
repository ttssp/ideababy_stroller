"""
pars.workflow — Workflow 模板渲染层。

职责：读取 templates/ 下的 Jinja2 模板（baseline / lora / eval），
根据 RunConfig 渲染成实际 Python 脚本并写入 .worktrees/<id>/artifacts/。
由 T015 实现。
"""
