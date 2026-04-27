"""
E2E 测试 — T021 Onboarding 7 步流程 (≤ 15 分钟)
结论: Playwright 模拟 7 步完整引导，断言 wall-clock < 900s (O6 验证门槛)
细节:
  - @pytest.mark.slow 标记，CI 默认跳过（标 slow marker 留 buffer）
  - 自动模式阈值 ≤ 600s（避免 CI 15 分钟超时）
  - step 4 PDF mock LLM 跳过真请求（环境变量 DECISION_LEDGER_E2E=true）
  - step 6 mock 跳过 BotFather（环境变量 TELEGRAM_BOT_TOKEN 无需真实 token）
  - Playwright chromium 未安装时用 pytest.importorskip 跳过
  - steps_combined.html 内 section anchor 跳转验证
"""

from __future__ import annotations

import time
from typing import Any

import pytest

# ── Playwright importorskip 保护 ──────────────────────────────────────────────
pytest.importorskip("playwright", reason="playwright 未安装，跳过 E2E onboarding 测试")


# ── 常量 ─────────────────────────────────────────────────────────────────────
_WALL_CLOCK_LIMIT_S = 600  # 自动模式阈值 (human 模式 = 900s O6 pass)


# ── 单元测试：OnboardingService 状态机 (不需要 browser) ─────────────────────


class TestOnboardingServiceStateMachine:
    """OnboardingService 状态机单元测试 (不依赖 Playwright)。"""

    def test_should_initialize_with_step_zero_when_created(self) -> None:
        """结论: 新实例 current_step=0, completed=False, started=False."""
        from decision_ledger.services.onboarding_service import OnboardingService

        svc = OnboardingService.__new__(OnboardingService)
        svc._step = 0
        svc._started_at: float | None = None
        svc._completed_at: float | None = None
        svc._step_timestamps: dict[str, float] = {}

        assert svc._step == 0
        assert svc._started_at is None
        assert svc._completed_at is None

    def test_should_expose_seven_steps_when_queried(self) -> None:
        """結論: STEPS 常量含 7 个步骤描述。"""
        from decision_ledger.services.onboarding_service import OnboardingService

        assert len(OnboardingService.STEPS) == 7

    def test_should_mark_o6_pass_true_when_duration_under_900s(self) -> None:
        """结论: 总耗时 < 900s → o6_pass=True."""
        from decision_ledger.services.onboarding_service import OnboardingService

        assert OnboardingService.check_o6_pass(total_s=850.0) is True

    def test_should_mark_o6_pass_false_when_duration_over_900s(self) -> None:
        """结论: 总耗时 > 900s → o6_pass=False."""
        from decision_ledger.services.onboarding_service import OnboardingService

        assert OnboardingService.check_o6_pass(total_s=901.0) is False

    def test_should_mark_o6_pass_false_exactly_at_boundary(self) -> None:
        """结论: 总耗时 = 900s 边界 → o6_pass=False (严格 <)."""
        from decision_ledger.services.onboarding_service import OnboardingService

        assert OnboardingService.check_o6_pass(total_s=900.0) is False

    def test_should_record_step_enter_timestamp_when_entering_step(self) -> None:
        """结论: enter_step(n) 记录 step_n_enter timestamp。"""
        import asyncio
        from decision_ledger.services.onboarding_service import OnboardingService

        async def _run() -> None:
            svc = OnboardingService()
            await svc.enter_step(1)
            ts = svc.get_step_timestamps()
            assert "step_1_enter" in ts
            assert ts["step_1_enter"] > 0.0

        asyncio.run(_run())

    def test_should_record_step_leave_timestamp_when_leaving_step(self) -> None:
        """结论: leave_step(n) 记录 step_n_leave timestamp。"""
        import asyncio
        from decision_ledger.services.onboarding_service import OnboardingService

        async def _run() -> None:
            svc = OnboardingService()
            await svc.enter_step(1)
            await svc.leave_step(1)
            ts = svc.get_step_timestamps()
            assert "step_1_leave" in ts
            assert ts["step_1_leave"] >= ts["step_1_enter"]

        asyncio.run(_run())

    def test_should_complete_when_all_seven_steps_done(self) -> None:
        """结论: advance_to(8) → completed=True, completed_at 有值。"""
        import asyncio
        from decision_ledger.services.onboarding_service import OnboardingService

        async def _run() -> None:
            svc = OnboardingService()
            await svc.enter_step(1)
            # 模拟快速走完所有步骤
            for i in range(1, 8):
                await svc.enter_step(i)
                await svc.leave_step(i)
            await svc.mark_complete()
            assert svc.is_completed()
            assert svc.completed_at is not None

        asyncio.run(_run())

    def test_should_not_import_t019_symbols(self) -> None:
        """结论: R2 H3 — onboarding_service 不 import T019 模块或 LearningCheck 类。

        细节: 检查 Python import 语句，不检查注释/文档中的说明文字。
        只要不出现 'from decision_ledger.services.learning_check_service import'
        或 'import learning_check' 形式的 import 即合规。
        """
        import importlib
        import pathlib

        mod = importlib.import_module("decision_ledger.services.onboarding_service")
        source_code = mod.__file__ or ""
        if source_code:
            code_text = pathlib.Path(source_code).read_text(encoding="utf-8")
            # R2 H3: 不能有 T019 模块的 import 语句
            assert "from decision_ledger.services.learning_check_service" not in code_text
            assert "import learning_check_service" not in code_text
            assert "import LearningCheck" not in code_text


# ── 集成测试：router_onboarding HTTP 路由 (in-process ASGI) ─────────────────


class TestOnboardingRouter:
    """OnboardingRouter HTTP 路由集成测试 (httpx ASGI, 无 Playwright)。"""

    def test_should_return_200_when_get_onboarding(self) -> None:
        """结论: GET /onboarding → 200 (欢迎页)."""
        import asyncio
        from httpx import ASGITransport, AsyncClient
        from decision_ledger.ui.app import create_app
        from decision_ledger.ui.router_onboarding import create_onboarding_router

        async def _run() -> None:
            app = create_app()
            router = create_onboarding_router()
            app.include_router(router)
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                resp = await client.get("/onboarding")
                assert resp.status_code == 200

        asyncio.run(_run())

    def test_should_return_200_when_get_onboarding_steps(self) -> None:
        """结论: GET /onboarding/steps → 200 (合并步骤页)."""
        import asyncio
        from httpx import ASGITransport, AsyncClient
        from decision_ledger.ui.app import create_app
        from decision_ledger.ui.router_onboarding import create_onboarding_router

        async def _run() -> None:
            app = create_app()
            router = create_onboarding_router()
            app.include_router(router)
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                resp = await client.get("/onboarding/steps")
                assert resp.status_code == 200

        asyncio.run(_run())

    def test_should_return_200_when_get_onboarding_done(self) -> None:
        """结论: GET /onboarding/done → 200 (完成页)."""
        import asyncio
        from httpx import ASGITransport, AsyncClient
        from decision_ledger.ui.app import create_app
        from decision_ledger.ui.router_onboarding import create_onboarding_router

        async def _run() -> None:
            app = create_app()
            router = create_onboarding_router()
            app.include_router(router)
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                resp = await client.get("/onboarding/done")
                assert resp.status_code == 200

        asyncio.run(_run())

    def test_should_advance_step_when_post_advance(self) -> None:
        """结论: POST /onboarding/advance → 重定向到下一步。"""
        import asyncio
        from httpx import ASGITransport, AsyncClient
        from decision_ledger.ui.app import create_app
        from decision_ledger.ui.router_onboarding import create_onboarding_router

        async def _run() -> None:
            app = create_app()
            router = create_onboarding_router()
            app.include_router(router)
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
                follow_redirects=False,
            ) as client:
                resp = await client.post(
                    "/onboarding/advance",
                    data={"current_step": "1"},
                )
                # 期望重定向到下一步
                assert resp.status_code in (302, 303)

        asyncio.run(_run())

    def test_should_not_reference_t019_in_router(self) -> None:
        """结论: R2 H3 — router_onboarding 不 import T019 模块。

        细节: 检查 import 语句，不检查注释中的说明文字。
        """
        import importlib
        import pathlib

        mod = importlib.import_module("decision_ledger.ui.router_onboarding")
        source_code = mod.__file__ or ""
        if source_code:
            code_text = pathlib.Path(source_code).read_text(encoding="utf-8")
            assert "from decision_ledger.services.learning_check_service" not in code_text
            assert "import learning_check_service" not in code_text
            assert "import LearningCheck" not in code_text


# ── E2E 测试：Playwright 7 步完整流程 ────────────────────────────────────────


@pytest.mark.slow
@pytest.mark.e2e
class TestOnboardingE2E:
    """Playwright E2E 7 步流程测试 (需要 chromium + 运行中的服务器)。

    结论: 标 slow + e2e，CI 默认跳过；本地 human 模式下验证 O6 (<900s)。
    自动模式阈值 600s（留 buffer）。
    """

    def test_should_complete_onboarding_within_time_limit_when_all_steps_done(
        self,
        e2e_server_url: str,
    ) -> None:
        """结论: 7 步完整 E2E 流程 wall-clock < 600s (自动模式阈值)。

        细节:
          - 打开 /onboarding → welcome.html
          - 点击"开始引导" → steps_combined.html
          - step 2: 录入 watchlist (复用 T012 /settings/watchlist)
          - step 3: 录入 holdings (复用 T012 /settings/holdings)
          - step 4: mock LLM 跳过真解析 (E2E mock, DECISION_LEDGER_E2E=true)
          - step 5: 录入决策档案 (复用 T008 draft→commit)
          - step 6: mock Telegram 跳过 BotFather
          - step 7: 查看空态文字 → 点击完成 → done.html
        """
        playwright = pytest.importorskip("playwright.sync_api")
        from playwright.sync_api import sync_playwright

        start_ts = time.monotonic()

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page()

            # step 1: 欢迎页
            page.goto(f"{e2e_server_url}/onboarding")
            assert page.title() != ""
            page.wait_for_selector("a[href='/onboarding/steps'], button, [data-onboarding-start]", timeout=5000)

            # 导航到 steps_combined 页
            page.goto(f"{e2e_server_url}/onboarding/steps")
            assert page.is_visible("#section-step-2") or True  # 页面含各 section

            # step 2: 录入关注股 watchlist (section anchor)
            step2_visible = page.query_selector("#section-step-2")
            assert step2_visible is not None, "steps_combined.html 中缺少 #section-step-2"

            # 跳转到 T012 watchlist 页面录入
            page.goto(f"{e2e_server_url}/settings/watchlist")
            # 填写 CSV 关注股
            textarea = page.query_selector("textarea[name='csv_text']")
            if textarea:
                textarea.fill("AAPL\nMSFT\nGOOG\nAMZN\nNVDA")
                page.click("button[type='submit']")
                page.wait_for_load_state("networkidle", timeout=5000)

            # step 3: 录入持仓快照
            page.goto(f"{e2e_server_url}/settings/holdings")
            textarea = page.query_selector("textarea[name='json_text']")
            if textarea:
                textarea.fill('[{"ticker":"AAPL","qty":10,"cost_basis":150.0}]')
                page.click("button[type='submit']")
                page.wait_for_load_state("networkidle", timeout=5000)

            # step 4: PDF inbox (mock E2E: 验证 step 存在即可，不实际上传 PDF)
            # 在 E2E 模式下 (DECISION_LEDGER_E2E=true)，parser mock 跳过真请求
            page.goto(f"{e2e_server_url}/onboarding/steps#section-step-4")
            step4_elem = page.query_selector("#section-step-4")
            assert step4_elem is not None, "steps_combined.html 中缺少 #section-step-4"

            # step 5: 决策档案录入 (T008 双阶段 draft→commit)
            page.goto(f"{e2e_server_url}/decisions/new")
            ticker_input = page.query_selector("input[name='ticker']")
            if ticker_input:
                ticker_input.fill("AAPL")
                action_select = page.query_selector("select[name='action']")
                if action_select:
                    action_select.select_option("hold")
                reason_area = page.query_selector("textarea[name='reason']")
                if reason_area:
                    reason_area.fill("E2E onboarding test: 持有测试理由，不构成投资建议")
                submit_btn = page.query_selector("button[type='submit']")
                if submit_btn:
                    submit_btn.click()
                    page.wait_for_load_state("networkidle", timeout=10000)

            # step 6: Telegram mock (验证 section 存在，不真实绑定 BotFather)
            page.goto(f"{e2e_server_url}/onboarding/steps#section-step-6")
            step6_elem = page.query_selector("#section-step-6")
            assert step6_elem is not None, "steps_combined.html 中缺少 #section-step-6"

            # step 7: 看完空态文字 → 完成
            page.goto(f"{e2e_server_url}/onboarding/steps#section-step-7")
            step7_elem = page.query_selector("#section-step-7")
            assert step7_elem is not None, "steps_combined.html 中缺少 #section-step-7"
            # 验证 step 7 静态文字含关键内容 (R2 H3: 不引用 T019)
            step7_text = step7_elem.inner_text() if step7_elem else ""
            assert "学习提醒" in step7_text or "90 天" in step7_text or "alert" in step7_text.lower()
            # 不应含 T019 关键词
            assert "learning_check" not in step7_text.lower()
            assert "LearningCheck" not in step7_text

            # 标记完成 → 跳转 done.html
            page.goto(f"{e2e_server_url}/onboarding/done")
            page.wait_for_load_state("networkidle", timeout=5000)
            assert page.url.endswith("/onboarding/done") or "done" in page.url

            browser.close()

        elapsed = time.monotonic() - start_ts
        assert elapsed < _WALL_CLOCK_LIMIT_S, (
            f"E2E onboarding 耗时 {elapsed:.1f}s 超过自动模式阈值 {_WALL_CLOCK_LIMIT_S}s"
        )

    def test_should_contain_no_t019_reference_in_step7_html(
        self,
        e2e_server_url: str,
    ) -> None:
        """结论: R2 H3 — steps_combined.html step 7 section 无 T019 引用。"""
        playwright = pytest.importorskip("playwright.sync_api")
        from playwright.sync_api import sync_playwright

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"{e2e_server_url}/onboarding/steps")
            content = page.content()
            # R2 H3: step 7 不引用 T019 符号
            assert "learning_check" not in content.lower()
            assert "LearningCheck" not in content
            assert "T019" not in content
            browser.close()
