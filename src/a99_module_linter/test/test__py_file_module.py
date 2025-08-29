from pathlib import Path as pathlib_Path
from pytest import fixture as pytest_fixture, raises as pytest_raises
from src.a99_module_linter.linter import find_incorrect_imports


@pytest_fixture
def sample_file(tmp_path: pathlib_Path):
    content = """\
import os
import src.a21_old_module
from src.a22_helpers import func
import src.a23_calendar_viewer
from src.a25_utils import helper
from src.a25_utils import helper as h
from src.a23.tools import alpha, beta as b
def inside_func():
    import src.a30_internal
    from src.a31_more import thing
# relative import that should NOT match:
from .a32_local import nope
"""
    fp = tmp_path / "sample.py"
    fp.write_text(content, encoding="utf-8")
    return fp


def test_threshold_22(sample_file):
    result = find_incorrect_imports(sample_file, 22)
    assert "import src.a23_calendar_viewer" in result
    assert "from src.a25_utils import helper" in result
    assert "from src.a25_utils import helper as h" in result
    assert "from src.a23.tools import alpha, beta as b" in result
    assert "import src.a30_internal" in result
    assert "from src.a31_more import thing" in result
    # ensure lower/equal series are excluded
    assert all("a21" not in r and "a22" not in r for r in result)


def test_high_threshold_only_top_matches(sample_file):
    result = find_incorrect_imports(sample_file, 29)
    assert "import src.a30_internal" in result
    assert "from src.a31_more import thing" in result
    assert all("a23" not in r and "a25" not in r for r in result)


def test_no_matches(sample_file):
    result = find_incorrect_imports(sample_file, 99)
    assert result == []


def test_missing_file():
    with pytest_raises(FileNotFoundError):
        find_incorrect_imports("nope.py", 10)
