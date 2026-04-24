"""
pars.safety — 安全 deny 清单与 hook 管理。

职责：管理 worker_claude_dir/ 下的 settings.json deny 规则和 hooks 脚本；
提供 is_command_allowed() 供 proxy 层使用；fail-closed 只读挂载逻辑。
由 T012 实现。
"""
