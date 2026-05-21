"""
test_init_files.py � Linter that confirms every non-test directory
inside a given set of root directories contains an __init__.py file.

Usage:
    pytest test_init_files.py -v

Configure ROOT_DIRS below to match your project layout.
"""

from ch00_py.chapter_desc_main import get_chapter_descs
from ch00_py.file_toolbox import get_dir_filenames
from os.path import join as os_path_join
from pathlib import Path


def test_CheckAllNonTestDirectoriesHave__init__py():
    """Every non-test package directory must contain an __init__.py."""
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        dir_filenames = get_dir_filenames(chapter_dir)
        init_file_dirs = {x_dir for x_dir, fn in dir_filenames if fn == "__init__.py"}
        for init_file_dir in init_file_dirs:
            full_dir = os_path_join(chapter_dir, init_file_dir)
            should_not_exist_str = (
                f"test directory '{full_dir}' should not have __init__.py file"
            )
            assert "test" not in full_dir, should_not_exist_str

        json_file_dirs = {
            x_dir
            for x_dir, fn in dir_filenames
            if fn.endswith(".json") and "test" not in x_dir
        }
        json_file_fail_str = f"All {chapter_dir} directories with json files should have __init__.py files. Difference {init_file_dirs.difference(json_file_dirs)}"
        # print(f"{init_file_dirs=}")
        # print(f"{json_file_dirs=}")
        assert init_file_dirs == json_file_dirs, json_file_fail_str

        # if file is .json confirm __init__.py file exists
        for x_dir, x_filename in dir_filenames:
            if x_filename.endswith(".json") and "test" not in x_dir:
                full_dir = os_path_join(chapter_dir, x_dir)
                assertion_fail_str = f"missing __init__.py file in {full_dir}"
                assert x_dir in init_file_dirs, assertion_fail_str
                print(f"{x_dir:20} {x_filename=}")

            # print(f"{chapter_desc=}")
            # print(f"{dir_filenames=}")
    # assert (directory / "__init__.py").exists(), (
    #     f"Missing __init__.py in '{directory}'\n"
    #     f"  Fix: touch {directory / '__init__.py'}"
    # )
