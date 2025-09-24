from os import listdir as os_listdir, walk as os_walk
from os.path import basename as os_path_basename, exists as os_path_exists
from pathlib import Path as pathlib_Path
from src.ch01_data_toolbox.file_toolbox import (
    create_path,
    get_dir_file_strs,
    get_level1_dirs,
    open_json,
)
from src.ch98_docs_builder.doc_builder import (
    get_chapter_desc_prefix,
    get_chapter_desc_str_number,
    get_chapter_str_functions,
)
from src.ch99_chapter_style.style import (
    check_if_chapter_str_funcs_is_sorted,
    check_import_objs_are_ordered,
    check_str_func_test_file_has_needed_asserts,
    check_str_funcs_are_not_duplicated,
    get_chapter_descs,
    get_function_names_from_file,
    get_imports_from_file,
    get_python_files_with_flag,
)


def test_Chapter_ref_util_FilesExist():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH

    # WHEN / THEN
    # previous_chapter_number = -1
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        print(f"Evaluating {chapter_desc=} {chapter_dir=}")
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        # assert chapter_number == previous_chapter_number + 1
        # print(f"{chapter_desc=} {chapter_number=}")
        ref_dir = create_path(chapter_dir, "_ref")
        keywords_filename = f"{chapter_prefix}_keywords.py"
        str_func_path = create_path(ref_dir, keywords_filename)
        assert os_path_exists(str_func_path)
        test_dir = create_path(chapter_dir, "test")
        util_dir = create_path(test_dir, "_util")
        assert os_path_exists(util_dir)
        # str_func_test_path = create_path(utils_dir, f"test_{chapter_prefix}_keywords.py")
        # assert os_path_exists(str_func_test_path)
        env_files = get_python_files_with_flag(util_dir, "env")
        if len(env_files) > 0:
            assert len(env_files) == 1
            env_filename = str(list(env_files.keys())[0])
            chapter_desc_str_number = get_chapter_desc_str_number(chapter_desc)
            ch_num = int(chapter_desc_str_number)
            check_env_file_has_necessary_elements(env_filename, chapter_prefix, ch_num)
        util_files = get_dir_file_strs(util_dir, include_dirs=False)
        for util_file in util_files.keys():
            is_test_file = util_file[:4] == "test"
            is_json_file = util_file.endswith("json")
            is_env_file = util_file == f"{chapter_prefix}_env.py"
            is_example_file = util_file == f"{chapter_prefix}_examples.py"
            is_keywords_file = util_file == keywords_filename
            assert_fail_str = f"{util_file} should not be in {util_dir=}"
            # print(f"{util_file=}")
            # print(f"{is_json_file=} {util_file.endswith("json")=}")
            # print(f"{is_test_file=} {util_file[:4]=}")
            # print(f"{is_example_file=}")
            # print(f"{is_keywords_file=}")
            acceptable_filename = (
                is_test_file
                or is_example_file
                or is_env_file
                or is_keywords_file
                or is_json_file
            )
            assert acceptable_filename, assert_fail_str


def check_env_file_has_necessary_elements(
    env_filename: str, chapter_prefix: str, chapter_number: int
):
    # print(f"{env_files=}")
    # print(f"{env_filename=}")
    assert env_filename.endswith(f"{chapter_prefix}_env.py")
    assertion_fail_str = (
        f"{chapter_number=} {get_function_names_from_file(env_filename)}"
    )
    env_functions = set(get_function_names_from_file(env_filename))
    assert "env_dir_setup_cleanup" in env_functions, assertion_fail_str
    assert "get_chapter_temp_dir" in env_functions, assertion_fail_str


def path_contains_subpath(full_path: str, sub_path: str):
    full = pathlib_Path(full_path).resolve()
    sub = pathlib_Path(sub_path).resolve()
    try:
        full.relative_to(sub)
        return True
    except ValueError:
        return False


def test_Chapters_util_AssertsExistForEverytermFunction():
    """
    Test that all string-related functions in each chapter directory are asserted and tested.
    This test performs the following checks for each chapter:
    - Retrieves all string functions and ensures they are sorted and not duplicated.
    - Verifies that if string functions exist, a corresponding test file exists in the chapter's utility directory.
    - Checks that the test file imports exactly one object and that imports are ordered.
    - Ensures the test file contains a single test function named 'test_str_functions_ReturnsObj'.
    - Validates that the test file includes the necessary assertions for all string functions.
    Raises:
        AssertionError: If any of the above conditions are not met.
    """

    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    running_str_functions = set()
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_desc_prefix = get_chapter_desc_prefix(chapter_desc)
        chapter_desc_str_number = get_chapter_desc_str_number(chapter_desc)
        ref_dir = create_path(chapter_dir, "ref")
        test_dir = create_path(chapter_dir, "test")
        util_dir = create_path(test_dir, "_util")
        print(f"{util_dir}")
        chapter_str_funcs = get_chapter_str_functions(chapter_dir, chapter_desc_prefix)
        check_if_chapter_str_funcs_is_sorted(chapter_str_funcs)
        check_str_funcs_are_not_duplicated(chapter_str_funcs, running_str_functions)
        running_str_functions.update(set(chapter_str_funcs))

        if len(chapter_str_funcs) > 0:
            test_file_path = create_path(
                util_dir, f"test_{chapter_desc_prefix}_keywords.py"
            )
            assert os_path_exists(test_file_path)
            test_file_imports = get_imports_from_file(test_file_path)
            assert len(test_file_imports) == 1
            check_import_objs_are_ordered(test_file_imports, test_file_path)
            test_functions = get_function_names_from_file(test_file_path)
            assert test_functions == ["test_str_functions_ReturnsObj"]
            check_str_func_test_file_has_needed_asserts(
                chapter_str_funcs, test_file_path, util_dir, chapter_desc_str_number
            )


def test_Chapters_test_TestsAreInCorrectFolderStructure():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_desc_str_number = get_chapter_desc_str_number(chapter_desc)
        desc_number = int(chapter_desc_str_number)
        level1_dirs = get_level1_dirs(chapter_dir)
        print(f"{desc_number} {level1_dirs=}")
        test_str = "test"
        for level1_dir in level1_dirs:
            if level1_dir.find(test_str) > -1:
                if level1_dir != test_str:
                    print(f"{desc_number=} {level1_dir=}")
                assert level1_dir == test_str


def test_Chapters_NonTestFilesDoNotHavePrintStatments():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH
    print_str = "print"

    # WHEN / THEN
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        py_files = [f for f in os_listdir(chapter_dir) if f.endswith(".py")]
        for py_file in py_files:
            py_file_path = create_path(chapter_dir, py_file)
            py_file_str = open(py_file_path).read()
            if py_file_str.find(print_str) > -1:
                print(f"Chapter {chapter_desc} file {py_file_path} has print statement")
            assert py_file_str.find(print_str) == -1


def test_Chapters_NonTestFilesDoNotHaveStringFunctionsImports():
    """Check all non-test python files do not import str functions"""

    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        for file_path, file_imports in get_python_files_with_flag(chapter_dir).items():
            filename = str(os_path_basename(file_path))
            file_path = str(file_path)
            print(f"{file_path=}")
            if not filename.startswith("test") and "_util" not in file_path:
                for file_import in file_imports:
                    if str(file_import[0]).endswith("_str"):
                        print(f"{chapter_desc} {filename} {file_import[0]=}")
                    assert not str(file_import[0]).endswith("_str")


def test_Chapters_ChapterReferenceFolder_ref_ExistsForEveryChapter():
    """
    Test that all string-related functions in each chapter directory are asserted and tested.
    This test performs the following checks for each chapter:
    Raises:
        AssertionError: If any of the above conditions are not met.
    """

    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_desc_prefix = get_chapter_desc_prefix(chapter_desc)
        docs_dir = create_path(chapter_dir, "_ref")
        assert os_path_exists(docs_dir)
        chapter_ref_path = create_path(docs_dir, f"{chapter_desc_prefix}_ref.json")
        assert os_path_exists(chapter_ref_path)
        chapter_ref_dict = open_json(chapter_ref_path)
        print(f"{chapter_desc=}")
        # print(f"{chapter_ref_path} \t Items: {len(chapter_ref_dict)}")
        ref_keys = set(chapter_ref_dict.keys())
        chapter_description_str = "chapter_description"
        chapter_blurb_str = "chapter_blurb"
        chapter_number_str = "chapter_number"
        chapter_content_str = "chapter_content"
        keys_assertion_fail_str = f"ref json for {chapter_desc} missing required key(s)"
        expected_ref_keys = {
            chapter_blurb_str,
            chapter_description_str,
            chapter_number_str,
            chapter_content_str,
        }
        assert ref_keys == expected_ref_keys, keys_assertion_fail_str
        assert chapter_ref_dict.get(chapter_description_str) == chapter_desc
        ref_chapter_blurb = chapter_ref_dict.get(chapter_blurb_str)
        MAX_CHAPTER_BLURB_LENGTH = 88  # arbitrarily choosen

        assert len(ref_chapter_blurb) > 0
        assert len(ref_chapter_blurb) <= MAX_CHAPTER_BLURB_LENGTH
        ref_chapter_content = chapter_ref_dict.get(chapter_content_str)
        content_assertion_fail_str = f"{chapter_desc} {chapter_content_str} is invalid"
        assert len(ref_chapter_content) > 0, content_assertion_fail_str
        chapter_desc_ch_int = int(get_chapter_desc_str_number(chapter_desc))
        chapter_ref_ch_int = chapter_ref_dict.get(chapter_number_str)
        assertion_fail_str = f"{chapter_desc} expecting key {chapter_number_str} with value {chapter_desc_ch_int}"
        assert chapter_ref_ch_int == chapter_desc_ch_int, assertion_fail_str


def test_Chapters_DoNotHaveEmptyDirectories():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH
    exclude_dir = "src/ch20_world_logic/test/test_world_examples/worlds"

    # WHEN / THEN
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        for dirpath, dirnames, filenames in os_walk(chapter_dir):
            if not path_contains_subpath(dirpath, exclude_dir):
                assert_fail_str = f"{chapter_desc} Empty directory found: {dirpath}"
                if dirnames == ["__pycache__"] and filenames == []:
                    print(f"{dirnames} {dirpath}")
                    dirnames = []
                # print(f"{dirnames=}")
                # print(f"{filenames=}")
                assert dirnames or filenames, assert_fail_str
