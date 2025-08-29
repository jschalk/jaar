from pathlib import Path as pathlib_Path
from pytest import fixture as pytest_fixture, raises as pytest_raises
from src.a99_module_linter.linter import find_later_imports
import tempfile


@pytest_fixture
def sample_file(tmp_path: pathlib_Path):
    """Create a temporary Python file for testing."""
    content = """\
import os
import src.a21_old_module
from src.a22_helpers import func
import src.a23_calendar_viewer
from src.a25_utils import helper
def inside_func():
    import src.a30_internal
"""
    file_path = tmp_path / "test_file.py"
    file_path.write_text(content, encoding="utf-8")
    return file_path


def test_find_later_imports_threshold_22(sample_file):
    # ESTABLISH / WHEN
    result = find_later_imports(sample_file, 22)

    # THEN
    assert "import src.a23_calendar_viewer" in result
    assert "from src.a25_utils import helper" in result
    assert "import src.a30_internal" in result
    assert all("a21" not in line and "a22" not in line for line in result)


def test_find_later_imports_high_threshold(sample_file):
    # ESTABLISH / WHEN
    result = find_later_imports(sample_file, 29)

    # THEN
    assert result == ["import src.a30_internal"]


def test_find_later_imports_no_matches(sample_file):
    # ESTABLISH / WHEN
    result = find_later_imports(sample_file, 40)

    # THEN
    assert result == []


def test_file_not_found():
    # ESTABLISH / WHEN / THEN
    with pytest_raises(FileNotFoundError):
        find_later_imports("nonexistent.py", 10)
