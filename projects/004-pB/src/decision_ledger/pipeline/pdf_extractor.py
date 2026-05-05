"""
PDF 文本提取器 — T006
结论: 用 pdfplumber 提取多页 PDF 文本，支持中文，大 PDF (>50页) 自动切片
细节:
  - extract_text(path) → str，所有页用换行连接
  - 空文本 (提取结果为空或仅空白) 返回空字符串 ""，调用方检查
  - 大 PDF (> MAX_PAGES_SINGLE 页) 按 MAX_PAGES_CHUNK 切片，返回头部切片文本
  - pdfplumber 异常 → 记录日志并 re-raise（调用方负责 parse_failures 记录）
  - 中文 CJK 排版: 接受乱序，让 LLM 处理 (known gotchas)
"""

from __future__ import annotations

import logging
from pathlib import Path

import pdfplumber

logger = logging.getLogger(__name__)

# 单次 LLM token 上限约束：> 50 页切片（每页约 2000 tokens）
MAX_PAGES_SINGLE = 50
MAX_PAGES_CHUNK = 50


def extract_text(path: Path) -> str:
    """
    从 PDF 文件提取全部文本。

    结论:
      - 多页合并（换页符 \f 分隔后再 join）
      - 大 PDF (>50 页) 只取前 MAX_PAGES_CHUNK 页（避免超 LLM token 限制）
      - 提取失败 re-raise，调用方写 parse_failures

    参数:
        path: PDF 文件路径（必须存在）

    返回:
        提取的文本字符串，可能为空字符串（调用方需检查）

    异常:
        Exception: pdfplumber 打开/解析失败时 re-raise
    """
    logger.debug("开始提取 PDF 文本: %s", path)
    try:
        with pdfplumber.open(str(path)) as pdf:
            pages = pdf.pages
            total = len(pages)
            if total == 0:
                logger.warning("PDF 无页面: %s", path)
                return ""

            if total > MAX_PAGES_SINGLE:
                logger.info(
                    "大 PDF (%d 页) 截取前 %d 页: %s",
                    total,
                    MAX_PAGES_CHUNK,
                    path,
                )
                pages_to_extract = pages[:MAX_PAGES_CHUNK]
            else:
                pages_to_extract = pages

            texts: list[str] = []
            for i, page in enumerate(pages_to_extract):
                page_text = page.extract_text()
                if page_text:
                    texts.append(page_text)
                else:
                    logger.debug("第 %d 页无文本: %s", i + 1, path)

            result = "\n".join(texts)
            logger.info(
                "PDF 提取完成: %s，共 %d 页，文本长度 %d",
                path,
                len(pages_to_extract),
                len(result),
            )
            return result
    except Exception:
        logger.exception("PDF 提取失败: %s", path)
        raise
