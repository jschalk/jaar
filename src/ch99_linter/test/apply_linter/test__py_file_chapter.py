from ast import (
    Import as ast_Import,
    ImportFrom as ast_ImportFrom,
    Module as ast_Module,
    parse as ast_parse,
    walk as ast_walk,
)
from ch99_linter.style import (
    BANNED_IMPORTS,
    find_incorrect_imports,
    get_file_ast_tree,
    no_banned_imports_exist,
)
from pathlib import Path as pathlib_Path
from pytest import fixture as pytest_fixture, raises as pytest_raises


def _create_temp_py_file(py_file_text: str) -> str:
    import tempfile
    from pathlib import Path

    temp_dir = tempfile.mkdtemp()
    file_path = Path(temp_dir) / "test_file.py"
    file_path.write_text(py_file_text, encoding="utf-8")

    return str(file_path)


def test_get_file_ast_tree_ReturnsObj_Scenario0_AstTreeIsModuleNode():
    # ESTABLISH
    py_file_text = """
import os
from pathlib import Path
"""
    # WHEN
    ast_tree = get_file_ast_tree(_create_temp_py_file(py_file_text))
    # THEN
    assert isinstance(ast_tree, ast_Module)
    assert hasattr(ast_tree, "body")
    assert len(ast_tree.body) == 2


def test_get_file_ast_tree_ReturnsObj_Scenario1_CanDetectImportPresence():
    # ESTABLISH
    py_file_text = """
import os
import json
"""
    # WHEN
    ast_tree = get_file_ast_tree(_create_temp_py_file(py_file_text))
    # THEN
    imported_modules = {
        node.names[0].name
        for node in ast_walk(ast_tree)
        if isinstance(node, ast_Import)
    }

    assert "os" in imported_modules
    assert "json" in imported_modules
    assert "requests" not in imported_modules


def test_get_file_ast_tree_ReturnsObj_Scenario2_CanDetectFromImports():
    # ESTABLISH
    py_file_text = """
from pathlib import Path
from collections import defaultdict
"""
    # WHEN
    ast_tree = get_file_ast_tree(_create_temp_py_file(py_file_text))
    # THEN
    from_imports = {
        node.module for node in ast_walk(ast_tree) if isinstance(node, ast_ImportFrom)
    }
    assert "pathlib" in from_imports
    assert "collections" in from_imports
    assert "subprocess" not in from_imports


def test_get_file_ast_tree_ReturnsObj_Scenario3_CanAssertForbiddenImportAbsent():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH
    py_file_text = """
import os
from pathlib import Path
"""
    # WHEN
    ast_tree = get_file_ast_tree(_create_temp_py_file(py_file_text))
    # THEN
    forbidden_imports = {"subprocess", "requests"}

    discovered_imports = set()

    for node in ast_walk(ast_tree):
        if isinstance(node, ast_Import):
            discovered_imports.update(alias.name for alias in node.names)

        if isinstance(node, ast_ImportFrom):
            discovered_imports.add(node.module)

    assert forbidden_imports.isdisjoint(discovered_imports)


@pytest_fixture
def sample_file(tmp_path: pathlib_Path):
    content = """\
import os
import ch51_old_chapter
from ch54_helpers import func
import ch53_calendar_viewer
from ch55_utils import helper
from ch55_utils import helper as h
from ch53.tools import alpha, beta as b
def inside_func():
    import ch60_bikehouse
    from ch61_more import thing
# relative import that should NOT match:
from .ch62_local import nope
"""
    fp = tmp_path / "sample.py"
    fp.write_text(content, encoding="utf-8")
    return fp


def test_find_incorrect_imports_ReturnsObj_Scenario0_threshold_52(sample_file):
    # ESTABLISH
    file_ast_tree = get_file_ast_tree(sample_file)
    # WHEN
    result = find_incorrect_imports(file_ast_tree, 52)
    # THEN
    print(f"{result=}")
    assert "import ch53_calendar_viewer" in result
    assert "from ch55_utils import helper" in result
    assert "from ch55_utils import helper as h" in result
    assert "from ch53.tools import alpha, beta as b" in result
    assert "import ch60_bikehouse" in result
    assert "from ch61_more import thing" in result
    # ensure lower/equal series are excluded
    assert all("ch51" not in r and "ch57" not in r for r in result)


def test_find_incorrect_imports_ReturnsObj_Scenario1_high_threshold_only_top_matches(
    sample_file,
):
    # ESTABLISH
    file_ast_tree = get_file_ast_tree(sample_file)
    # WHEN
    result = find_incorrect_imports(file_ast_tree, 59)
    # THEN
    assert "import ch60_bikehouse" in result
    assert "from ch61_more import thing" in result
    assert all("ch53" not in r and "ch55" not in r for r in result)


def test_find_incorrect_imports_ReturnsObj_Scenario2_no_matches(sample_file):
    # ESTABLISH
    file_ast_tree = get_file_ast_tree(sample_file)
    # WHEN
    result = find_incorrect_imports(file_ast_tree, 99)
    # THEN
    assert result == []


def test_BANNED_IMPORTS_Exists():
    # ESTABLISH / WHEN / THEN
    assert BANNED_IMPORTS == {"replace_me_when_new_element_added"}


def test_no_banned_imports_exist_ReturnsObj_Scenario0_WhenBannedImportExists():
    # ESTABLISH
    ast_tree = ast_parse("""
import os
import replace_me_when_new_element_added
""")
    # WHEN
    result = no_banned_imports_exist(ast_tree)
    # THEN
    assert result is False


def test_no_banned_imports_exist_ReturnsObj_Scenario1_WhenBannedImportExists():
    # ESTABLISH
    ast_tree = ast_parse("""
import os
from pandas import replace_me_when_new_element_added
""")
    # WHEN
    result = no_banned_imports_exist(ast_tree)
    # THEN
    assert result is False


def test_no_banned_imports_exist_ReturnsObj_Scenario2_WhenBannedImportExists():
    # ESTABLISH
    ast_tree = ast_parse("""
import os
from pandas import replace_me_when_new_element_added as pandas_replace_me_when_new_element_added
""")
    # WHEN
    result = no_banned_imports_exist(ast_tree)
    # THEN
    assert result is False


def test_no_banned_imports_exist_ReturnsObj_Scenario3_WhenBannedImportExists():
    # ESTABLISH
    ast_tree = ast_parse("""
import os
from pandas import read_csv, replace_me_when_new_element_added as pandas_replace_me_when_new_element_added
""")
    # WHEN
    result = no_banned_imports_exist(ast_tree)
    # THEN
    assert result is False


def test_no_banned_imports_exist_ReturnsTrue_WhenNoBannedImportsExist():
    # ESTABLISH
    ast_tree = ast_parse("""
import os
from pathlib import Path
""")
    # WHEN
    result = no_banned_imports_exist(ast_tree)
    # THEN
    assert result is True
