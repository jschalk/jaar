from src.f00_instrument.file import get_level1_dirs, set_dir
from src.f11_etl.examples.etl_env import get_test_etl_dir
from pathlib import Path


def test_get_level1_dirs_EmptyDirectory(tmp_path):
    # ESTABLISH
    test_dir = tmp_path

    # WHEN
    result = get_level1_dirs(test_dir)

    # THEN
    expected_dirs = []
    assert_fail_str = f"Expected empty list for empty directory, but got {result}"
    assert result == expected_dirs, assert_fail_str


def test_get_level1_dirs_NonExistentDirectory():
    # ESTABLISH
    test_dir = Path("/non/existent/directory")

    # WHEN
    result = get_level1_dirs(test_dir)

    # WHEN/THEN
    expected_dirs = []
    assert_fail_str = f"Expected empty list for empty directory, but got {result}"
    assert result == expected_dirs, assert_fail_str


def test_get_level1_dirs_ReturnsObjSorted():
    # ESTABLISH
    test_dir = get_test_etl_dir()
    # Create a temporary directory structure
    set_dir((Path(test_dir) / "dir2"))
    set_dir((Path(test_dir) / "dir1"))
    set_dir((Path(test_dir) / "dir3"))
    set_dir((Path(test_dir) / "dir1" / "subdir1"))
    set_dir((Path(test_dir) / "dir2" / "subdir2"))

    # WHEN
    result = get_level1_dirs(test_dir)

    # THEN
    expected_dirs = ["dir1", "dir2", "dir3"]
    assert result == expected_dirs, f"Expected {expected_dirs}, but got {result}"
