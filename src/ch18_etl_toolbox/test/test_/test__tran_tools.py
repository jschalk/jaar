from pathlib import Path
from src.ch01_data_toolbox.file_toolbox import get_level1_dirs, set_dir
from src.ch18_etl_toolbox.test._util.ch18_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)


def test_get_level1_dirs_EmptyDirectory(env_dir_setup_cleanup):
    # ESTABLISH
    test_dir = get_chapter_temp_dir()

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
    test_dir = get_chapter_temp_dir()
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
