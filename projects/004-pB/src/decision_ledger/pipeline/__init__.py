"""
决策账本 pipeline 包 — T006
结论: 咨询师 PDF pipeline 的三个核心模块
细节:
  - watcher: watchdog 监听 inbox 目录，触发 enqueue 回调
  - pdf_extractor: pdfplumber 提取 PDF 文本
  - parser: LLM 结构化解析 + ConflictCacheWarmer 预热
"""
