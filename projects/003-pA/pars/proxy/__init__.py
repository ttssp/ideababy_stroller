"""
pars.proxy — API Proxy 层。

职责：在 localhost 启动轻量 HTTP proxy，持有 ANTHROPIC_API_KEY，
对 worker 子进程隐藏真实 key；实现预算前置拒绝（pre-reject）逻辑。
由 T013 实现。
"""
