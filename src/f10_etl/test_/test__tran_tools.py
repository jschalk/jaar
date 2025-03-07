from src.f10_etl.transformers import get_level1_dirs
from pathlib import Path
from os import mkdir as os_mkdir
from pytest import fixture as pytest_fixture, raises as pytest_raises


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


@pytest_fixture
def setup_test_directory(tmp_path):
    # Create a temporary directory structure
    os_mkdir((tmp_path / "dir2"))
    os_mkdir((tmp_path / "dir1"))
    os_mkdir((tmp_path / "dir3"))
    os_mkdir((tmp_path / "dir1" / "subdir1"))
    os_mkdir((tmp_path / "dir2" / "subdir2"))
    return tmp_path


def test_get_level1_dirs_ReturnsObjSorted(setup_test_directory):
    # ESTABLISH
    test_dir = setup_test_directory
    expected_dirs = ["dir1", "dir2", "dir3"]

    # WHEN
    result = get_level1_dirs(test_dir)

    # THEN
    assert result == expected_dirs, f"Expected {expected_dirs}, but got {result}"
