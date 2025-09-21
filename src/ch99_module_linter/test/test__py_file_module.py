from pathlib import Path as pathlib_Path
from pytest import fixture as pytest_fixture, raises as pytest_raises
from src.ch99_module_linter.linter import find_incorrect_imports


@pytest_fixture
def sample_file(tmp_path: pathlib_Path):
    content = """\
import os
import src.ch21_old_module
from src.ch22_helpers import func
import src.ch23_calendar_viewer
from src.ch25_utils import helper
from src.ch25_utils import helper as h
from src.ch23.tools import alpha, beta as b
def inside_func():
    import src.ch30_internal
    from src.ch31_more import thing
# relative import that should NOT match:
from .ch32_local import nope
"""
    fp = tmp_path / "sample.py"
    fp.write_text(content, encoding="utf-8")
    return fp


def test_threshold_22(sample_file):
    result = find_incorrect_imports(sample_file, 22)
    assert "import src.ch23_calendar_viewer" in result
    assert "from src.ch25_utils import helper" in result
    assert "from src.ch25_utils import helper as h" in result
    assert "from src.ch23.tools import alpha, beta as b" in result
    assert "import src.ch30_internal" in result
    assert "from src.ch31_more import thing" in result
    # ensure lower/equal series are excluded
    assert all("ch21" not in r and "ch22" not in r for r in result)


def test_high_threshold_only_top_matches(sample_file):
    result = find_incorrect_imports(sample_file, 29)
    assert "import src.ch30_internal" in result
    assert "from src.ch31_more import thing" in result
    assert all("ch23" not in r and "ch25" not in r for r in result)


def test_no_matches(sample_file):
    result = find_incorrect_imports(sample_file, 99)
    assert result == []


def test_missing_file():
    with pytest_raises(FileNotFoundError):
        find_incorrect_imports("nope.py", 10)
