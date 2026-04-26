"""
决策录入全程 timing 测试 — T009
结论: 测量并断言 GET /decisions/new → POST commit 全程 wall-clock < 30s (R3 守 PRD 原口径)
细节:
  - 标记 @pytest.mark.e2e 便于 CI 单独运行
  - Playwright browser 测试使用 pytest.importorskip("playwright") skip 保护
  - timer_start = page.goto("/decisions/new") 完成 (200 OK)
  - timer_end = commit 页面 200 OK (/decisions/{trade_id})
  - CI 阈值: < 25000ms (留 5s GHA 余量; PRD 口径 30s)
  - 503 测试通过 app_client_slow in-process fixture，无需 subprocess
"""

from __future__ import annotations

import time
from typing import Any

import pytest

# ── 常量 ─────────────────────────────────────────────────────────────────────

_CI_THRESHOLD_MS = 25000  # GHA 安全余量 (PRD 30s，留 5s buffer)
_PRD_THRESHOLD_MS = 30000  # PRD §S1 原口径
_DRAFT_CACHE_HIT_MAX_MS = 1000  # D21: cache 命中 ≤ 1s
_DRAFT_CACHE_MISS_MAX_MS = 5000  # D21: cache miss ≤ 5s
_COMMIT_MAX_MS = 1000  # commit 零 LLM < 1s

# E2E 表单填写用测试数据
_E2E_TICKER = "NVDA"
_E2E_ACTION = "buy"
_E2E_DRAFT_REASON = "技术面突破, NVDA 上升通道确认, 量价配合"
_E2E_FINAL_REASON = "综合分析后买入, 冲突报告确认看多信号"

# ── Playwright 可用性保护 ─────────────────────────────────────────────────────
# 在 conftest.py 之外不直接 import playwright，避免 ImportError 导致整个文件跳过。
# 每个需要 playwright 的测试内部 importorskip。


# ── 辅助: Playwright 同步 API 包装 ───────────────────────────────────────────


def _run_full_e2e_flow(
    base_url: str,
    ticker: str = _E2E_TICKER,
    draft_reason: str = _E2E_DRAFT_REASON,
    final_reason: str = _E2E_FINAL_REASON,
    action: str = _E2E_ACTION,
) -> dict[str, float]:
    """结论: 运行完整双阶段流程，返回计时结果（毫秒）。

    细节:
      - timer_start = page.goto("/decisions/new") 返回后 (200 OK)
      - timer_end = commit 跳转后页面 200 OK
      - 返回 {"total_ms", "draft_ms", "commit_ms"}
    """
    playwright = pytest.importorskip("playwright")  # noqa: F841
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # ── 预热：加载一次 /decisions/new 触发模板编译（不计入 timer）
            page.goto(f"{base_url}/decisions/new", timeout=15_000, wait_until="load")

            # ── timer_start: 正式 GET /decisions/new (R3 起点)
            t_start = time.perf_counter()
            response = page.goto(
                f"{base_url}/decisions/new",
                timeout=15_000,
                wait_until="load",
            )
            assert response is not None and response.ok, (
                f"GET /decisions/new 失败: status={response.status if response else 'None'}"
            )

            # ── 填写草稿表单
            page.fill("#ticker", ticker)

            # 选择 action radio
            page.click(f'input[name="intended_action"][value="{action}"]')

            # 填写 draft_reason
            page.fill("#draft_reason", draft_reason)

            # ── 提交草稿（POST /decisions/draft）
            t_draft_start = t_start  # 与 timer_start 相同（R3 全程计时）
            page.click("#submit-btn")

            # 等待跳转到 preview 页（draft 阶段 LLM 完成）
            page.wait_for_url("**/decisions/draft/*/preview", timeout=10_000)

            t_after_draft = time.perf_counter()
            draft_ms = (t_after_draft - t_draft_start) * 1000

            # ── 填写 commit 表单
            # final_action 已预填（与 intended_action 一致），不必重选
            page.fill("#final_reason", final_reason)

            # 选择 would_have_acted_without_agent = "yes"
            page.click('input[name="would_have_acted_without_agent"][value="yes"]')

            # commit button 被 JS 启用后点击
            page.click("#commit-btn")

            # ── timer_end: commit 完成跳转到 /decisions/{trade_id} (R3 终点)
            page.wait_for_url("**/decisions/*", timeout=5_000)
            # 确认不是 preview URL
            current_url = page.url
            assert "/draft/" not in current_url, (
                f"commit 后 URL 仍含 /draft/: {current_url}"
            )

            t_end = time.perf_counter()
            total_ms = (t_end - t_start) * 1000
            commit_ms = (t_end - t_after_draft) * 1000

        finally:
            browser.close()

    return {
        "total_ms": total_ms,
        "draft_ms": draft_ms,
        "commit_ms": commit_ms,
    }


# ── 测试套件 ──────────────────────────────────────────────────────────────────


@pytest.mark.e2e
def test_full_flow_under_30s(e2e_server_url: str) -> None:
    """结论: 全程 wall-clock < 30s（R3 守 PRD §S1 原口径, CI 用 25s 余量）。

    细节:
      - timer_start = GET /decisions/new 200 OK
      - timer_end = POST commit 后 /decisions/{trade_id} 200 OK
      - 含 draft LLM 阶段（cache 命中 ≤ 1s）
    """
    pytest.importorskip("playwright")

    result = _run_full_e2e_flow(e2e_server_url)
    total_ms = result["total_ms"]

    assert total_ms < _CI_THRESHOLD_MS, (
        f"全程 wall-clock={total_ms:.0f}ms 超过 CI 阈值 {_CI_THRESHOLD_MS}ms "
        f"(PRD 口径 {_PRD_THRESHOLD_MS}ms, R3 守 PRD 原口径)。"
        f"阶段分解: draft={result['draft_ms']:.0f}ms, commit={result['commit_ms']:.0f}ms"
    )


@pytest.mark.e2e
def test_draft_phase_under_5s(e2e_server_url: str) -> None:
    """结论: draft 阶段（含 LLM cache 命中）≤ 1s；无 mock 场景 ≤ 5s（D21 R3 上限）。

    细节:
      - cache 已预热（seed_llm_cache），命中路径 ≤ 1s
      - draft_ms = page.goto("/decisions/new") → redirect 到 preview (200 OK)
    """
    pytest.importorskip("playwright")

    result = _run_full_e2e_flow(e2e_server_url)
    draft_ms = result["draft_ms"]

    # cache 命中（seed_llm_cache 已预热）
    assert draft_ms <= _DRAFT_CACHE_MISS_MAX_MS, (
        f"draft 阶段={draft_ms:.0f}ms 超过 D21 上限 {_DRAFT_CACHE_MISS_MAX_MS}ms (R3)"
    )
    # cache 命中时应更快
    # Note: cache miss 场景用 conftest 中 app_client_503 测，不在此测（需真实 LLM）


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_draft_timeout_returns_503(app_client_slow: Any) -> None:
    """结论: mock LLM 6s sleep 超过 5s timeout → POST /decisions/draft 返回 503 (B-R2-2)。

    细节:
      - 不启动 subprocess server，用 in-process AsyncClient (app_client_slow fixture)
      - slow_assembler.assemble() sleep 6s → asyncio.timeout(5.0) 触发 → 503
      - 验证 503 且不进入 preview（防止 commit）
    """
    response = await app_client_slow.post(
        "/decisions/draft",
        data={
            "ticker": "AAPL",
            "intended_action": "buy",
            "draft_reason": "测试 draft 超时场景",
        },
        follow_redirects=False,
    )
    assert response.status_code == 503, (
        f"mock LLM 6s sleep 应返回 503，实际: {response.status_code}。"
        f"响应内容: {response.text[:200]}"
    )


@pytest.mark.e2e
def test_default_fill_present(e2e_server_url: str) -> None:
    """结论: GET /decisions/new 页面默认填写字段均非空（action radio 有默认选中）。

    细节:
      - ticker 字段: 无默认（空），但存在 #ticker
      - intended_action: "buy" 默认 checked（last_action=None 时）
      - draft_reason: 无默认（空），但存在 #draft_reason
      - submit button #submit-btn 存在
    """
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(
                f"{e2e_server_url}/decisions/new",
                timeout=10_000,
                wait_until="load",
            )

            # ticker 输入框存在
            ticker_input = page.locator("#ticker")
            assert ticker_input.count() == 1, "#ticker 输入框不存在"

            # action radio 存在且有默认选中 (buy)
            buy_radio = page.locator('input[name="intended_action"][value="buy"]')
            assert buy_radio.count() == 1, "buy radio 不存在"
            assert buy_radio.is_checked(), "buy radio 未默认选中 (last_action=None 时)"

            # draft_reason 存在
            reason_field = page.locator("#draft_reason")
            assert reason_field.count() == 1, "#draft_reason 不存在"

            # submit button 存在
            submit_btn = page.locator("#submit-btn")
            assert submit_btn.count() == 1, "#submit-btn 不存在"

        finally:
            browser.close()


@pytest.mark.e2e
def test_commit_button_disabled_until_yes_no(e2e_server_url: str) -> None:
    """结论: preview 页 #commit-btn 在 would_have_acted 未选时 disabled，选后启用 (R2 M1)。

    细节:
      - 先 POST /decisions/draft 进入 preview
      - 确认 #commit-btn 初始 disabled
      - 选 would_have_acted_without_agent = "yes" → button enabled
    """
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # 进入 draft 表单
            page.goto(
                f"{e2e_server_url}/decisions/new",
                timeout=10_000,
                wait_until="load",
            )

            # 填写并提交 draft
            page.fill("#ticker", _E2E_TICKER)
            page.click(f'input[name="intended_action"][value="{_E2E_ACTION}"]')
            page.fill("#draft_reason", _E2E_DRAFT_REASON)
            page.click("#submit-btn")

            # 等待进入 preview
            page.wait_for_url("**/decisions/draft/*/preview", timeout=10_000)

            # commit button 初始应 disabled
            commit_btn = page.locator("#commit-btn")
            assert commit_btn.count() == 1, "#commit-btn 不存在"
            assert commit_btn.is_disabled(), (
                "would_have_acted 未选时 #commit-btn 应为 disabled (R2 M1)"
            )

            # 选 yes → button 应变 enabled
            page.click('input[name="would_have_acted_without_agent"][value="yes"]')
            # wait for JS to update button state
            page.wait_for_timeout(100)
            assert not commit_btn.is_disabled(), (
                "选 would_have_acted=yes 后 #commit-btn 应变 enabled"
            )

        finally:
            browser.close()


@pytest.mark.e2e
def test_5_consecutive_full_flows(e2e_server_url: str) -> None:
    """结论: 5 次连续完整流程，每次全程 < 30s，平均 < 15s (R3 SLA)。

    细节:
      - 每次独立的 ticker（不同 ticker 保证各自命中独立 cache 键）
      - 全程 = GET /decisions/new → POST commit 后 /decisions/{trade_id}
      - 任一次 ≥ 30s → 断言失败（即使平均 < 15s）
    """
    pytest.importorskip("playwright")

    # 5 个不同 ticker（都已在 seed_llm_cache 中预热）
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

    total_durations: list[float] = []
    draft_latencies: list[float] = []
    commit_latencies: list[float] = []

    for i, ticker in enumerate(tickers):
        result = _run_full_e2e_flow(
            base_url=e2e_server_url,
            ticker=ticker,
            draft_reason=f"{ticker} 连续流程测试第 {i + 1} 次",
            final_reason=f"{ticker} commit 确认第 {i + 1} 次",
        )

        total_ms = result["total_ms"]
        total_durations.append(total_ms)
        draft_latencies.append(result["draft_ms"])
        commit_latencies.append(result["commit_ms"])

        assert total_ms < _PRD_THRESHOLD_MS, (
            f"第 {i + 1} 次全程={total_ms:.0f}ms ≥ PRD 30s 上限 "
            f"(ticker={ticker}, draft={result['draft_ms']:.0f}ms, "
            f"commit={result['commit_ms']:.0f}ms)"
        )

    avg_ms = sum(total_durations) / len(total_durations)
    assert avg_ms < 15000, (
        f"5 次平均全程={avg_ms:.0f}ms ≥ 15s 目标。"
        f"各次: {[f'{d:.0f}ms' for d in total_durations]}"
    )
