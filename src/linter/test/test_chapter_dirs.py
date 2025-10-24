from os import listdir as os_listdir, walk as os_walk
from os.path import basename as os_path_basename, exists as os_path_exists
from pathlib import Path as pathlib_Path
from src.ch01_py.file_toolbox import (
    create_path,
    get_dir_file_strs,
    get_level1_dirs,
    open_json,
)
from src.ch98_docs_builder.doc_builder import (
    get_chapter_desc_prefix,
    get_chapter_desc_str_number,
)
from src.linter.style import (
    check_if_chapter_keywords_by_chapter_is_sorted,
    check_keywords_by_chapter_are_not_duplicated,
    get_chapter_descs,
    get_func_names_and_class_bases_from_file,
    get_imports_from_file,
    get_python_files_with_flag,
    get_semantic_types_filename,
)


def check_env_file_has_necessary_elements(
    env_filename: str, chapter_prefix: str, chapter_number: int
):
    # print(f"{env_files=}")
    # print(f"{env_filename=}")
    assert env_filename.endswith(f"{chapter_prefix}_env.py")
    file_funcs, class_bases = get_func_names_and_class_bases_from_file(env_filename)
    assertion_fail_str = f"{chapter_number=} {file_funcs}"
    env_functions = set(file_funcs)
    assert "temp_dir_setup" in env_functions, assertion_fail_str
    assert "get_temp_dir" in env_functions, assertion_fail_str


def path_contains_subpath(full_path: str, sub_path: str):
    full = pathlib_Path(full_path).resolve()
    sub = pathlib_Path(sub_path).resolve()
    try:
        full.relative_to(sub)
        return True
    except ValueError:
        return False


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
            print_str_in_py_file_bool = print_str in py_file_str
            if print_str_in_py_file_bool:
                print(f"Chapter {chapter_desc} file {py_file_path} has print statement")
            assert not print_str_in_py_file_bool


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
        chapter_ref_path = create_path(docs_dir, f"{chapter_desc_prefix}_ref.json")
        semantic_types_filename = get_semantic_types_filename(chapter_desc_prefix)
        semantics_path = create_path(docs_dir, semantic_types_filename)
        assert os_path_exists(docs_dir)
        assert os_path_exists(chapter_ref_path)
        assert os_path_exists(semantics_path)
        chapter_ref_dict = open_json(chapter_ref_path)
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
