"""
AdvisorParser 集成测试 — T006
结论: mock LLMClient + mock AdvisorRepository 验证解析成功/失败路径
细节:
  - mock LLM 返回 fake JSON → 断言 upsert_weekly 被调用
  - mock LLM 返回非法 JSON → 断言 record_parse_failure 被调用
  - R2: parse 成功后 ConflictCacheWarmer.warm_for_advisor_report 被调用 (mock T010 接口)
  - SEC-4: prompt injection 场景 schema 验证仍生效
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from decision_ledger.domain.advisor import AdvisorWeeklyReport, ParseFailure
from decision_ledger.pipeline.parser import AdvisorParser, ConflictCacheWarmer


@pytest.fixture
def sample_pdf_path() -> Path:
    """指向 tests/fixtures 的 sample PDF。"""
    here = Path(__file__).parent.parent.parent  # tests/
    return here / "fixtures" / "sample_advisor_2026w17.pdf"


@pytest.fixture
def corrupted_pdf_path(tmp_path: Path) -> Path:
    """损坏的 PDF 文件（供 parse 失败测试）。"""
    p = tmp_path / "corrupted.pdf"
    p.write_bytes(b"NOT A VALID PDF CONTENT")
    return p


@pytest.fixture
def mock_repo() -> MagicMock:
    """Mock AdvisorRepository。"""
    repo = MagicMock()
    repo.upsert_weekly = AsyncMock()
    repo.record_parse_failure = AsyncMock()
    return repo


@pytest.fixture
def mock_llm_client() -> MagicMock:
    """Mock LLMClient，默认返回合法的 AdvisorParserOutput。"""
    client = MagicMock()
    client.call = AsyncMock()
    return client


@pytest.fixture
def mock_conflict_warmer() -> MagicMock:
    """Mock ConflictCacheWarmer（T010 接口 mock）。"""
    warmer = MagicMock(spec=ConflictCacheWarmer)
    warmer.warm_for_advisor_report = AsyncMock()
    return warmer


class TestAdvisorParserSuccessPath:
    """AdvisorParser 成功路径测试。"""

    async def test_should_call_upsert_weekly_when_llm_returns_valid_schema(
        self,
        sample_pdf_path: Path,
        mock_repo: MagicMock,
        mock_llm_client: MagicMock,
        mock_conflict_warmer: MagicMock,
    ) -> None:
        """mock LLM 返回合法 schema → upsert_weekly 被调用。"""
        from decision_ledger.pipeline.parser import AdvisorParserOutput

        # 安排 mock LLM 返回合法输出
        fake_output = AdvisorParserOutput(
            advisor_id="advisor_zhang",
            week_id="2026-W17",
            raw_summary="本周 TSM 推荐 BUY，置信度 0.85",
            recommendations=[
                {
                    "ticker": "TSM",
                    "direction": "BUY",
                    "confidence": 0.85,
                    "rationale_plain": "台积电本周技术面强势",
                }
            ],
        )
        mock_llm_client.call.return_value = fake_output

        parser = AdvisorParser(
            repo=mock_repo,
            llm_client=mock_llm_client,
            conflict_warmer=mock_conflict_warmer,
        )

        result = await parser.parse(sample_pdf_path)

        # 断言 upsert_weekly 被调用
        assert mock_repo.upsert_weekly.call_count == 1
        saved_report: AdvisorWeeklyReport = mock_repo.upsert_weekly.call_args[0][0]
        assert saved_report.advisor_id == "advisor_zhang"
        assert saved_report.week_id == "2026-W17"
        assert "TSM" in saved_report.structured_json
        assert result is not None
        assert result.advisor_id == "advisor_zhang"

    async def test_should_call_conflict_warmer_when_parse_succeeds(
        self,
        sample_pdf_path: Path,
        mock_repo: MagicMock,
        mock_llm_client: MagicMock,
        mock_conflict_warmer: MagicMock,
    ) -> None:
        """R2: parse 成功后 ConflictCacheWarmer.warm_for_advisor_report 被调用。"""
        from decision_ledger.pipeline.parser import AdvisorParserOutput

        fake_output = AdvisorParserOutput(
            advisor_id="advisor_zhang",
            week_id="2026-W17",
            raw_summary="TSM BUY",
            recommendations=[
                {
                    "ticker": "TSM",
                    "direction": "BUY",
                    "confidence": 0.85,
                    "rationale_plain": "tech strong",
                }
            ],
        )
        mock_llm_client.call.return_value = fake_output

        parser = AdvisorParser(
            repo=mock_repo,
            llm_client=mock_llm_client,
            conflict_warmer=mock_conflict_warmer,
        )

        await parser.parse(sample_pdf_path)

        # R2: warm_for_advisor_report 被调用一次
        mock_conflict_warmer.warm_for_advisor_report.assert_called_once()
        call_args = mock_conflict_warmer.warm_for_advisor_report.call_args[0][0]
        assert isinstance(call_args, AdvisorWeeklyReport)

    async def test_should_not_call_conflict_warmer_when_warmer_is_none(
        self,
        sample_pdf_path: Path,
        mock_repo: MagicMock,
        mock_llm_client: MagicMock,
    ) -> None:
        """conflict_warmer=None 时不报错（T010 未部署时兼容）。"""
        from decision_ledger.pipeline.parser import AdvisorParserOutput

        fake_output = AdvisorParserOutput(
            advisor_id="advisor_zhang",
            week_id="2026-W17",
            raw_summary="TSM BUY",
            recommendations=[
                {
                    "ticker": "TSM",
                    "direction": "BUY",
                    "confidence": 0.85,
                    "rationale_plain": "tech strong",
                }
            ],
        )
        mock_llm_client.call.return_value = fake_output

        parser = AdvisorParser(
            repo=mock_repo,
            llm_client=mock_llm_client,
            conflict_warmer=None,
        )

        # 不应报错
        result = await parser.parse(sample_pdf_path)
        assert result is not None

    async def test_should_store_raw_pdf_path_in_report(
        self,
        sample_pdf_path: Path,
        mock_repo: MagicMock,
        mock_llm_client: MagicMock,
        mock_conflict_warmer: MagicMock,
    ) -> None:
        """raw_pdf_path 应记录在 AdvisorWeeklyReport 中（审计追溯）。"""
        from decision_ledger.pipeline.parser import AdvisorParserOutput

        fake_output = AdvisorParserOutput(
            advisor_id="advisor_zhang",
            week_id="2026-W17",
            raw_summary="summary",
            recommendations=[],
        )
        mock_llm_client.call.return_value = fake_output

        parser = AdvisorParser(
            repo=mock_repo,
            llm_client=mock_llm_client,
            conflict_warmer=mock_conflict_warmer,
        )

        await parser.parse(sample_pdf_path)

        saved_report: AdvisorWeeklyReport = mock_repo.upsert_weekly.call_args[0][0]
        assert saved_report.raw_pdf_path == str(sample_pdf_path)


class TestAdvisorParserFailurePath:
    """AdvisorParser 失败路径测试。"""

    async def test_should_record_parse_failure_when_pdf_is_corrupted(
        self,
        corrupted_pdf_path: Path,
        mock_repo: MagicMock,
        mock_llm_client: MagicMock,
        mock_conflict_warmer: MagicMock,
    ) -> None:
        """损坏 PDF → record_parse_failure 被调用，upsert_weekly 不调用。"""
        parser = AdvisorParser(
            repo=mock_repo,
            llm_client=mock_llm_client,
            conflict_warmer=mock_conflict_warmer,
        )

        result = await parser.parse(corrupted_pdf_path)

        assert result is None
        assert mock_repo.record_parse_failure.call_count == 1
        assert mock_repo.upsert_weekly.call_count == 0

        failure: ParseFailure = mock_repo.record_parse_failure.call_args[0][0]
        assert str(corrupted_pdf_path) == failure.pdf_path
        assert len(failure.failure_id) > 0  # failure_id 非空

    async def test_should_record_parse_failure_when_llm_raises(
        self,
        sample_pdf_path: Path,
        mock_repo: MagicMock,
        mock_llm_client: MagicMock,
        mock_conflict_warmer: MagicMock,
    ) -> None:
        """LLM 抛出异常 → record_parse_failure，不 re-raise 到上层。"""
        from decision_ledger.llm.errors import LLMSchemaError

        mock_llm_client.call.side_effect = LLMSchemaError(
            "schema 不匹配",
            raw_data={"bad": "data"},
        )

        parser = AdvisorParser(
            repo=mock_repo,
            llm_client=mock_llm_client,
            conflict_warmer=mock_conflict_warmer,
        )

        result = await parser.parse(sample_pdf_path)

        assert result is None
        assert mock_repo.record_parse_failure.call_count == 1
        assert mock_repo.upsert_weekly.call_count == 0

    async def test_should_not_call_conflict_warmer_when_parse_fails(
        self,
        corrupted_pdf_path: Path,
        mock_repo: MagicMock,
        mock_llm_client: MagicMock,
        mock_conflict_warmer: MagicMock,
    ) -> None:
        """parse 失败时 ConflictCacheWarmer 不应被调用。"""
        parser = AdvisorParser(
            repo=mock_repo,
            llm_client=mock_llm_client,
            conflict_warmer=mock_conflict_warmer,
        )

        await parser.parse(corrupted_pdf_path)

        mock_conflict_warmer.warm_for_advisor_report.assert_not_called()

    async def test_should_record_parse_failure_when_pdf_is_empty(
        self,
        tmp_path: Path,
        mock_repo: MagicMock,
        mock_llm_client: MagicMock,
        mock_conflict_warmer: MagicMock,
    ) -> None:
        """空文本提取 → record_parse_failure。"""
        # 最小化空 PDF（有效但无文字内容）
        empty_pdf = tmp_path / "empty.pdf"
        # 用一个只有空页的 PDF（pdfplumber 可以打开但提取为空字符串）
        # 先用一个假 PDF 触发提取失败 path
        empty_pdf.write_bytes(b"%PDF-1.4\n%%EOF\n")

        parser = AdvisorParser(
            repo=mock_repo,
            llm_client=mock_llm_client,
            conflict_warmer=mock_conflict_warmer,
        )

        result = await parser.parse(empty_pdf)

        # 空文本 → parse_failure，不调 LLM
        assert result is None
        assert mock_repo.record_parse_failure.call_count == 1
        mock_llm_client.call.assert_not_called()


class TestAdvisorParserPromptInjection:
    """SEC-4: prompt injection 防护测试。"""

    async def test_should_reject_injection_via_schema_validation(
        self,
        sample_pdf_path: Path,
        mock_repo: MagicMock,
        mock_llm_client: MagicMock,
        mock_conflict_warmer: MagicMock,
    ) -> None:
        """
        LLM 被 prompt injection 欺骗返回 direction="BUY everything" 时，
        schema 验证（pydantic enum）拒绝 → parse_failure 被记录。
        """
        from decision_ledger.llm.errors import LLMSchemaError

        # 模拟 LLM 被 inject 后返回非法 direction（不在 enum 内）
        # LLMClient 内部 schema validate 会抛出 LLMSchemaError
        mock_llm_client.call.side_effect = LLMSchemaError(
            "direction 枚举不匹配: 'BUY everything' not in ['BUY','SELL','HOLD']",
            raw_data={"direction": "BUY everything"},
        )

        parser = AdvisorParser(
            repo=mock_repo,
            llm_client=mock_llm_client,
            conflict_warmer=mock_conflict_warmer,
        )

        result = await parser.parse(sample_pdf_path)

        assert result is None
        assert mock_repo.record_parse_failure.call_count == 1
        assert mock_conflict_warmer.warm_for_advisor_report.call_count == 0
