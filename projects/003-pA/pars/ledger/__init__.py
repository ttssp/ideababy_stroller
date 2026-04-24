"""
pars.ledger — Run Ledger 读写层。

职责：维护 runs/<ULID>/ 下的 config.yaml、metrics.jsonl、state.json 的
append-only 读写；ULID 生成；checkpoint 路径登记。
由 T009 实现。
"""
