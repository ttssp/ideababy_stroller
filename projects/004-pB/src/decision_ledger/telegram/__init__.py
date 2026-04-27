"""
Telegram bot 包 — T017
结论: 提供 Telegram long-polling bot、rate limiter、market session、conflict narrative
细节:
  - bot.py: DecisionLedgerBot 启动 long-polling；send_alert / push_event 接口
  - handlers.py: /start /weekly /ticker /help 只读 handlers
  - rate_limiter.py: 7 天滚动窗口 ≤ 1 weekly + 5 event (R4 红线)
  - market_session.py: US/HK/CN per-market session window (D24 R2)
  - conflict_narrative.py: ConflictReport → 3 行叙事 (顺序按 rendered_order_seed D22 R2)
"""
