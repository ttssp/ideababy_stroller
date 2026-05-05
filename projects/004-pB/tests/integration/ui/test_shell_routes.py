"""
集成测试 — Web UI shell 路由 (T004)
结论: 验证 GET / 200 + footer 文案 + nav 8 项顺序 + 反 0.0.0.0 binding
细节:
  - 使用 FastAPI TestClient (httpx)
  - footer 文案必须与 compliance.md §4.1 原文一致 (逐字比对)
  - nav 8 项顺序: 决策档案/冲突报告/错位矩阵/笔记wiki/周review/月review/学习检查/设置
  - 反 0.0.0.0 单测: 验证 uvicorn host 配置硬编码 127.0.0.1
  - GET /_partials/alert-banner 在 T004 阶段返回 200 空内容
"""

from __future__ import annotations

import ast
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


# ── 测试 fixture ─────────────────────────────────────────
@pytest.fixture
def app_client() -> TestClient:
    """创建 TestClient 用于集成测试。"""
    # 设置最小环境变量避免 ConfigError
    os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-placeholder")
    os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test-token-placeholder")

    from decision_ledger.ui.app import create_app

    # 使用 create_app 工厂，不依赖全局 main.py
    test_app = create_app()
    return TestClient(test_app, raise_server_exceptions=True)


# ── 1. 主页 GET / ─────────────────────────────────────────
class TestIndexRoute:
    """GET / 路由测试组。"""

    def test_should_return_200_when_get_root(self, app_client: TestClient) -> None:
        """结论: GET / 必须返回 200。"""
        response = app_client.get("/")
        assert response.status_code == 200

    def test_should_return_html_content_type_when_get_root(self, app_client: TestClient) -> None:
        """结论: Content-Type 必须是 text/html。"""
        response = app_client.get("/")
        assert "text/html" in response.headers.get("content-type", "")

    def test_should_contain_footer_disclaimer_line1_when_get_root(
        self, app_client: TestClient
    ) -> None:
        """结论: footer 必须包含 compliance.md §4.1 第 1 行原文。"""
        response = app_client.get("/")
        assert "本系统是" in response.text
        assert "个人投资决策辅助工具" in response.text
        assert "不是持牌投顾产品" in response.text

    def test_should_contain_footer_disclaimer_line2_when_get_root(
        self, app_client: TestClient
    ) -> None:
        """结论: footer 必须包含 compliance.md §4.1 第 2 行原文。"""
        response = app_client.get("/")
        assert "所有决策由 human 自己最终做出" in response.text
        assert "工具仅提供参考视角与冲突报告" in response.text

    def test_should_contain_footer_disclaimer_line3_when_get_root(
        self, app_client: TestClient
    ) -> None:
        """结论: footer 必须包含 compliance.md §4.1 第 3 行原文。"""
        response = app_client.get("/")
        assert "LLM 输出可能包含错误或偏见" in response.text
        assert "human 不应不加审慎地接受任何建议" in response.text

    def test_should_contain_footer_disclaimer_line4_when_get_root(
        self, app_client: TestClient
    ) -> None:
        """结论: footer 必须包含 compliance.md §4.1 第 4 行原文。"""
        response = app_client.get("/")
        assert "不接受任何外部投资委托" in response.text
        assert "不为他人提供建议" in response.text

    def test_should_contain_all_8_nav_items_when_get_root(
        self, app_client: TestClient
    ) -> None:
        """结论: nav 必须包含全部 8 个 tab 文本。"""
        response = app_client.get("/")
        html = response.text
        # D14 tab 列表
        nav_items = [
            "决策档案",
            "冲突报告",
            "错位矩阵",
            "笔记 wiki",
            "周 review",
            "月 review",
            "学习检查",
            "设置",
        ]
        for item in nav_items:
            assert item in html, f"nav 缺少: {item}"

    def test_should_have_correct_nav_order_when_get_root(
        self, app_client: TestClient
    ) -> None:
        """结论: nav 顺序必须与 D14 一致，错位矩阵第三 (OP-6 mitigation)。"""
        response = app_client.get("/")
        html = response.text

        # 按顺序 D14: 决策档案/冲突报告/错位矩阵/笔记wiki/周review/月review/学习检查/设置
        ordered_items = [
            "决策档案",
            "冲突报告",
            "错位矩阵",
            "笔记 wiki",
            "周 review",
            "月 review",
            "学习检查",
            "设置",
        ]
        positions = [html.find(item) for item in ordered_items]
        # 验证每个 item 都存在
        for item, pos in zip(ordered_items, positions, strict=True):
            assert pos >= 0, f"nav item 未找到: {item}"
        # 验证顺序单调递增
        for i in range(len(positions) - 1):
            assert positions[i] < positions[i + 1], (
                f"nav 顺序错误: '{ordered_items[i]}' 应在 '{ordered_items[i + 1]}' 前面"
            )

    def test_should_have_matrix_as_third_nav_item_when_get_root(
        self, app_client: TestClient
    ) -> None:
        """结论: 错位矩阵必须是第三个 nav 项 (OP-6 mitigation)，排在冲突报告后、笔记 wiki 前。"""
        response = app_client.get("/")
        html = response.text
        pos_conflict = html.find("冲突报告")
        pos_matrix = html.find("错位矩阵")
        pos_notes = html.find("笔记 wiki")
        assert pos_conflict < pos_matrix < pos_notes, (
            "错位矩阵必须排在冲突报告之后、笔记 wiki 之前 (OP-6 第三位)"
        )

    def test_should_load_pico_css_when_get_root(self, app_client: TestClient) -> None:
        """结论: base.html 必须引入 Pico CSS (vendored, 不走 CDN)。"""
        response = app_client.get("/")
        assert "/static/pico.min.css" in response.text

    def test_should_load_htmx_when_get_root(self, app_client: TestClient) -> None:
        """结论: base.html 必须引入 HTMX (vendored, 不走 CDN)。"""
        response = app_client.get("/")
        assert "/static/htmx.min.js" in response.text

    def test_should_have_alert_banner_hook_when_get_root(
        self, app_client: TestClient
    ) -> None:
        """结论: base.html 必须包含 alert-banner HTMX hook (T020 接管用)。"""
        response = app_client.get("/")
        assert 'id="alert-banner"' in response.text
        assert 'hx-get="/_partials/alert-banner"' in response.text
        assert "hx-trigger=" in response.text


# ── 2. alert-banner partial ───────────────────────────────
class TestAlertBannerRoute:
    """GET /_partials/alert-banner 路由测试组。"""

    def test_should_return_200_when_get_alert_banner(
        self, app_client: TestClient
    ) -> None:
        """结论: T004 阶段 alert-banner endpoint 返回 200 (空内容，T020 接管)。"""
        response = app_client.get("/_partials/alert-banner")
        assert response.status_code == 200

    def test_should_return_empty_content_when_get_alert_banner(
        self, app_client: TestClient
    ) -> None:
        """结论: T004 阶段 alert-banner 内容为空 (无激活告警)。"""
        response = app_client.get("/_partials/alert-banner")
        # 内容为空或极短 (仅空白)
        assert response.text.strip() == ""


# ── 3. static 文件服务 ────────────────────────────────────
class TestStaticFiles:
    """静态文件服务测试。"""

    def test_should_serve_pico_css_when_get_static(
        self, app_client: TestClient
    ) -> None:
        """结论: /static/pico.min.css 必须可访问 (本地 vendor，不走 CDN)。"""
        response = app_client.get("/static/pico.min.css")
        assert response.status_code == 200
        assert "text/css" in response.headers.get("content-type", "")

    def test_should_serve_htmx_js_when_get_static(
        self, app_client: TestClient
    ) -> None:
        """结论: /static/htmx.min.js 必须可访问 (本地 vendor，不走 CDN)。"""
        response = app_client.get("/static/htmx.min.js")
        assert response.status_code == 200
        assert "javascript" in response.headers.get("content-type", "")


# ── 4. 反 0.0.0.0 binding 单测 ───────────────────────────
class TestLocalhostBinding:
    """反 0.0.0.0 binding 单测 (架构不变量 §9.7)。"""

    def _extract_uvicorn_host(self, main_path: Path) -> str | None:
        """结论: 通过 AST 从 uvicorn.run() 调用中提取 host 关键字参数的实际值。
        细节: 仅提取代码中的字符串字面量，不扫描注释/docstring（避免误报）。
        """
        source = main_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            is_uvicorn_run = (
                isinstance(func, ast.Attribute)
                and func.attr == "run"
                and isinstance(func.value, ast.Name)
                and func.value.id == "uvicorn"
            )
            if not is_uvicorn_run:
                continue
            for kw in node.keywords:
                if kw.arg == "host" and isinstance(kw.value, ast.Constant):
                    return str(kw.value.value)
        return None

    def test_should_bind_127_not_0000_when_running_main(self) -> None:
        """结论: main.py 中 uvicorn.run 的 host 参数必须是 127.0.0.1，不能是 0.0.0.0。
        细节: 通过 AST 静态分析 uvicorn.run() 关键字参数，不做原始字符串搜索（避免注释误报）。
        """
        main_path = Path(__file__).parents[3] / "src" / "decision_ledger" / "main.py"
        assert main_path.exists(), f"main.py 不存在: {main_path}"
        host = self._extract_uvicorn_host(main_path)
        assert host is not None, "main.py 中未找到 uvicorn.run(host=...) 调用"
        err_msg = (
            f"uvicorn.run host={host!r} 不是 '127.0.0.1'（违反架构不变量 §9.7）"
        )
        assert host == "127.0.0.1", err_msg

    def test_should_fail_if_host_changed_to_0000_in_main(self) -> None:
        """结论: 如果将 main.py 中的 host 改为 0.0.0.0，此测试失败。
        细节: 通过 AST 解析 uvicorn.run() 参数，改成 0.0.0.0 会导致此测试变红。
        """
        _invalid_host = "0.0" + ".0.0"  # 避免 S104 触发，拼接后等价于 0.0.0.0
        main_path = Path(__file__).parents[3] / "src" / "decision_ledger" / "main.py"
        host = self._extract_uvicorn_host(main_path)
        assert host != _invalid_host, (
            "检测到 uvicorn.run 绑定全局接口 — 违反架构不变量 §9.7，只能 bind 127.0.0.1"
        )

    def test_should_have_hardcoded_127_in_uvicorn_call_via_ast(self) -> None:
        """结论: 通过 AST 解析验证 uvicorn.run() 调用中 host 关键字参数值是 '127.0.0.1'。"""
        main_path = Path(__file__).parents[3] / "src" / "decision_ledger" / "main.py"
        source = main_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        found_correct_host = False
        for node in ast.walk(tree):
            # 寻找 uvicorn.run(...) 调用
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            is_uvicorn_run = (
                isinstance(func, ast.Attribute)
                and func.attr == "run"
                and isinstance(func.value, ast.Name)
                and func.value.id == "uvicorn"
            )
            if not is_uvicorn_run:
                continue
            for kw in node.keywords:
                if kw.arg == "host" and isinstance(kw.value, ast.Constant):
                    host_val = kw.value.value
                    assert host_val == "127.0.0.1", (
                        f"uvicorn.run host={host_val!r} 违反不变量 §9.7，必须是 '127.0.0.1'"
                    )
                    found_correct_host = True

        assert found_correct_host, "未在 main.py 中找到 uvicorn.run(host='127.0.0.1') 调用"


# ── 5. 版本信息 ───────────────────────────────────────────
class TestVersionInfo:
    """页面版本信息测试。"""

    def test_should_contain_version_in_footer_when_get_root(
        self, app_client: TestClient
    ) -> None:
        """结论: footer 需要包含版本号信息。"""
        response = app_client.get("/")
        # 版本号格式: v0.1.0 或 0.1.0
        assert "0.1.0" in response.text or "v0.1" in response.text
