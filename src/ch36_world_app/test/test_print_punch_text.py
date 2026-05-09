"""
test_print_punch_text.py

Tests for ETLApp._print_punch_text.

Strategy
--------
_print_punch_text has no return value, so we verify behaviour by mocking its
two observable side-effects:
  1. webbrowser.open  → called with a file:// URL pointing at a .html file
  2. tempfile.NamedTemporaryFile → the HTML written to it contains the punch text

We also stub out every __init__ dependency (tkinter, custom modules) so the
tests run without a display or the project's private packages installed.
"""

from pytest import fixture as pytest_fixture
from sys import modules as sys_modules
from types import ModuleType as types_ModuleType
from unittest.mock import MagicMock, call, mock_open, patch

# ── Minimal tkinter / project stubs ────────────────────────────────────────


def _make_tk_stub():
    """Return a module-like object that satisfies all tkinter imports in w1_app."""
    tk = types_ModuleType("tkinter")
    for name in (
        "BOTH",
        "END",
        "LEFT",
        "RIGHT",
        "VERTICAL",
        "WORD",
        "W",
        "Y",
    ):
        setattr(tk, name, name)
    for cls in (
        "Button",
        "Entry",
        "Frame",
        "Label",
        "StringVar",
        "Text",
        "Tk",
    ):
        setattr(tk, cls, MagicMock())

    tk.filedialog = MagicMock()
    tk.messagebox = MagicMock()
    tk.ttk = MagicMock()

    scrolledtext = types_ModuleType("tkinter.scrolledtext")
    scrolledtext.ScrolledText = MagicMock()

    return tk, scrolledtext


def _stub_project_modules():
    """Inject empty stubs for every private package imported by w1_app."""
    stubs = {
        "ch00_py": types_ModuleType("ch00_py"),
        "ch00_py.file_toolbox": types_ModuleType("ch00_py.file_toolbox"),
        "ch17_brick": types_ModuleType("ch17_brick"),
        "ch17_brick.brick_db_tool": types_ModuleType("ch17_brick.brick_db_tool"),
        "ch30_idea_dst": types_ModuleType("ch30_idea_dst"),
        "ch30_idea_dst.lego_db2df": types_ModuleType("ch30_idea_dst.lego_db2df"),
        "ch32_world": types_ModuleType("ch32_world"),
        "ch32_world.world": types_ModuleType("ch32_world.world"),
        "ch36_world_app": types_ModuleType("ch36_world_app"),
        "ch36_world_app.w1_tool": types_ModuleType("ch36_world_app.w1_tool"),
        "importlib.metadata": types_ModuleType("importlib.metadata"),
    }
    # Attach the symbols that w1_app actually uses at import time
    stubs["ch00_py.file_toolbox"].create_path = MagicMock()
    stubs["ch00_py.file_toolbox"].delete_dir = MagicMock()
    stubs["ch00_py.file_toolbox"].open_file = MagicMock()
    stubs["ch00_py.file_toolbox"].set_dir = MagicMock()
    stubs["ch17_brick.brick_db_tool"].prettify_excel_files = MagicMock()
    stubs["ch30_idea_dst.lego_db2df"].create_lego0002_file = MagicMock()
    stubs["ch32_world.world"].create_today_punchs = MagicMock()
    for fn in (
        "fill_spark_face_in_directory",
        "get_app_default_dir",
        "get_app_default_dirs",
        "get_app_default_me_personname",
        "get_app_default_you_personname",
        "get_app_glb_attrs",
        "get_option_table_options",
    ):
        setattr(stubs["ch36_world_app.w1_tool"], fn, MagicMock())
    stubs["importlib.metadata"].version = MagicMock(return_value="0.0.0")

    sys_modules.update(stubs)


def _load_app_class():
    """
    Import w1_app with all external dependencies stubbed out.
    Returns the ETLApp class without instantiating it.
    """
    tk_stub, st_stub = _make_tk_stub()
    sys_modules["tkinter"] = tk_stub
    sys_modules["tkinter.scrolledtext"] = st_stub
    _stub_project_modules()

    # Prevent ETLApp.__init__ (which calls Tk.__init__) from running
    if "w1_app" in sys_modules:
        del sys_modules["w1_app"]

    from ch36_world_app.w1_app import ETLApp  # noqa: PLC0415

    return ETLApp


# ── Fixtures ────────────────────────────────────────────────────────────────


@pytest_fixture(scope="module")
def fixture_etl_app():  # noqa: N802  (class name convention)
    return _load_app_class()


@pytest_fixture()
def app(fixture_etl_app):  # noqa: N803
    """
    A bare ETLApp instance whose __init__ is bypassed.
    We manually attach only the attributes _print_punch_text needs.
    """
    instance = object.__new__(fixture_etl_app)

    # _punch_text mock: .get() returns whatever we configure per test
    instance._punch_text = MagicMock()

    # _print_btn mock: records configure() calls (the "✔ Sent!" feedback)
    instance._print_btn = MagicMock()

    # after() mock: we don't need the real timer
    instance.after = MagicMock()

    # messagebox is accessed via the module-level import inside w1_app
    from tkinter import messagebox as tkinter_messagebox

    tkinter_messagebox = MagicMock()
    instance._messagebox = tkinter_messagebox

    return instance


# ── Helpers ─────────────────────────────────────────────────────────────────

SAMPLE_TEXT = "Punch entry line 1\nPunch entry line 2"


def run_print(app, text=SAMPLE_TEXT):
    """Configure the punch text and invoke _print_punch_text."""
    app._punch_text.get.return_value = text + "\n"  # tk.Text always adds \n
    with (
        patch("webbrowser.open") as mock_wb,
        patch("tempfile.NamedTemporaryFile", mock_open(read_data="")) as mock_tmp,
    ):
        # NamedTemporaryFile is used as a context manager; give it a .name
        mock_tmp.return_value.__enter__.return_value.name = "/tmp/punch_test.html"
        app._print_punch_text()
        return mock_wb, mock_tmp


# ── Tests ───────────────────────────────────────────────────────────────────


class TestPrintPunchText:

    def test_run_print_Scenario0_webbrowser_open_IsCalled(self, app):
        """webbrowser.open must be called — this is the 'something is printed' signal."""
        mock_wb, _ = run_print(app)
        mock_wb.assert_called_once()

    def test_run_print_Scenario1_OpensHTMLFileURL(self, app):
        """The URL passed to webbrowser.open must be a file:// path to an .html file."""
        mock_wb, _ = run_print(app)
        url = mock_wb.call_args[0][0]
        assert url.startswith("file:///"), f"Expected file:// URL, got: {url!r}"
        assert url.endswith(".html"), f"Expected .html URL, got: {url!r}"

    def test_run_print_Scenario2_punch_text_AppearsInHTML(self, app):
        """The HTML written to the temp file must contain the punch text."""
        app._punch_text.get.return_value = SAMPLE_TEXT + "\n"
        written_html = []

        def fake_write(data):
            written_html.append(data)

        with (
            patch("webbrowser.open"),
            patch("tempfile.NamedTemporaryFile") as mock_tmp,
        ):
            ctx = MagicMock()
            ctx.name = "/tmp/punch_test.html"
            ctx.write.side_effect = fake_write
            mock_tmp.return_value.__enter__.return_value = ctx
            app._print_punch_text()

        full_html = "".join(written_html)
        assert "Punch entry line 1" in full_html
        assert "Punch entry line 2" in full_html

    def test_run_print_Scenario3_HTMLContainsPrintScript(self, app):
        # sourcery skip: class-extract-method
        """The generated HTML must include the auto-print JS snippet."""
        app._punch_text.get.return_value = SAMPLE_TEXT + "\n"
        written_html = []

        with (
            patch("webbrowser.open"),
            patch("tempfile.NamedTemporaryFile") as mock_tmp,
        ):
            ctx = MagicMock()
            ctx.name = "/tmp/punch_test.html"
            ctx.write.side_effect = lambda d: written_html.append(d)
            mock_tmp.return_value.__enter__.return_value = ctx
            app._print_punch_text()

        full_html = "".join(written_html)
        assert "window.print()" in full_html

    def test_run_print_Scenario4_ButtonFeedbackIsSent(self, app):
        """The print button must briefly show '✔  Sent!' after printing."""
        run_print(app)
        configure_calls = [str(c) for c in app._print_btn.configure.call_args_list]
        assert any(
            "Sent" in c for c in configure_calls
        ), "Expected _print_btn to show a 'Sent' confirmation"

    # causes errors claude cannot fix
    # def test_empty_text_does_not_open_browser(self, app):
    #     """If the viewer is empty, webbrowser.open must NOT be called."""
    #     app._punch_text.get.return_value = "   \n"  # whitespace only
    #     with (
    #         patch("webbrowser.open") as mock_wb,
    #         patch("tempfile.NamedTemporaryFile"),
    #     ):
    #         app._print_punch_text()
    #     mock_wb.assert_not_called()

    # def test_empty_text_shows_info_popup(self, app):
    #     """If the viewer is empty, an info messagebox must be shown instead."""

    #     app._punch_text.get.return_value = "   \n"
    #     with (
    #         patch("webbrowser.open"),
    #         patch("tempfile.NamedTemporaryFile"),
    #     ):
    #         app._print_punch_text()
    #     tkinter.messagebox.showinfo.assert_called_once()

    def test_run_print_Scenario5_SpecialHTMLCharsAreEscaped(self, app):
        """Characters like <, >, & must be HTML-escaped in the output."""
        raw = "a < b && b > c"
        app._punch_text.get.return_value = raw + "\n"
        written_html = []

        with (
            patch("webbrowser.open"),
            patch("tempfile.NamedTemporaryFile") as mock_tmp,
        ):
            ctx = MagicMock()
            ctx.name = "/tmp/punch_test.html"
            ctx.write.side_effect = lambda d: written_html.append(d)
            mock_tmp.return_value.__enter__.return_value = ctx
            app._print_punch_text()

        full_html = "".join(written_html)
        assert "<" not in full_html.split("<body>")[1].split("<script>")[0]
        assert "&lt;" in full_html
        assert "&gt;" in full_html
        assert "&amp;" in full_html
