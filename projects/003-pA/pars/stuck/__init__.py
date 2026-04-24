"""
pars.stuck — Stuck Detector 状态机。

职责：5s 周期采样 GPU/CPU/disk/net 指标；实现 architecture §8 的
4 态状态机（idle / training / downloading / truly_stuck）；
冷启动 300s 豁免；连续 3 次 stuck-restart 熔断 + stuck_lock 持久化。
由 T017 实现。
"""
