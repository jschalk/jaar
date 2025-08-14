from os import listdir as os_listdir, walk as os_walk
from os.path import basename as os_path_basename, exists as os_path_exists
from pathlib import Path as pathlib_Path
from src.a00_data_toolbox.file_toolbox import create_path, get_level1_dirs
from src.a99_module_linter.module_eval import (
    check_if_module_str_funcs_is_sorted,
    check_import_objs_are_ordered,
    check_str_func_test_file_has_needed_asserts,
    check_str_funcs_are_not_duplicated,
    get_function_names_from_file,
    get_imports_from_file,
    get_module_descs,
    get_module_str_functions,
    get_python_files_with_flag,
)


def test_Module_util_FilesExist():
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH

    # WHEN / THEN
    # previous_module_number = -1
    for module_desc, module_dir in get_module_descs().items():
        print(f"Evaluating {module_desc=} {module_dir=}")
        module_number = int(module_desc[1:3])
        # assert module_number == previous_module_number + 1
        # print(f"{module_desc=} {module_number=}")
        test_dir = create_path(module_dir, "test")
        util_dir = create_path(test_dir, "_util")
        assert os_path_exists(util_dir)
        str_func_path = create_path(util_dir, f"a{module_desc[1:3]}_str.py")
        assert os_path_exists(str_func_path)
        # str_func_test_path = create_path(utils_dir, f"test_a{module_desc[1:3]}_str.py")
        # assert os_path_exists(str_func_test_path)
        env_files = get_python_files_with_flag(util_dir, "env")
        if len(env_files) > 0:
            # print(f"{env_files=}")
            assert len(env_files) == 1
            env_filename = str(list(env_files.keys())[0])
            # print(f"{env_filename=}")
            assert env_filename.endswith(f"a{module_desc[1:3]}_env.py")
            assertion_fail_str = (
                f"{module_number=} {get_function_names_from_file(env_filename)}"
            )
            env_functions = set(get_function_names_from_file(env_filename))
            assert "env_dir_setup_cleanup" in env_functions, assertion_fail_str
            assert "get_module_temp_dir" in env_functions, assertion_fail_str
            # print(f"{module_number=} {get_function_names_from_file(env_filename)}")

        # previous_module_number = module_number


def path_contains_subpath(full_path: str, sub_path: str):
    full = pathlib_Path(full_path).resolve()
    sub = pathlib_Path(sub_path).resolve()
    try:
        full.relative_to(sub)
        return True
    except ValueError:
        return False


def test_Modules_DoNotHaveEmptyDirectories():
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH
    exclude_dir = "src/a20_world_logic/test/test_world_examples/worlds"

    # WHEN / THEN
    for module_desc, module_dir in get_module_descs().items():
        for dirpath, dirnames, filenames in os_walk(module_dir):
            if not path_contains_subpath(dirpath, exclude_dir):
                assert_fail_str = f"{module_desc} Empty directory found: {dirpath}"
                if dirnames == ["__pycache__"] and filenames == []:
                    print(f"{dirnames} {dirpath}")
                    dirnames = []
                # print(f"{dirnames=}")
                # print(f"{filenames=}")
                assert dirnames or filenames, assert_fail_str


def test_Modules_NonTestFilesDoNotHavePrintStatments():
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH
    print_str = "print"

    # WHEN / THEN
    for module_desc, module_dir in get_module_descs().items():
        desc_number_str = module_desc[1:3]
        py_files = [f for f in os_listdir(module_dir) if f.endswith(".py")]
        for py_file in py_files:
            py_file_path = create_path(module_dir, py_file)
            py_file_str = open(py_file_path).read()
            if py_file_str.find(print_str) > -1:
                print(f"Module {module_desc} file {py_file_path} has print statement")
            assert py_file_str.find(print_str) == -1


def test_Modules_NonTestFilesDoNotHaveImportStringFunctions():
    """Check all non-test python files do not import str functions"""

    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    for module_desc, module_dir in get_module_descs().items():
        for file_path, file_imports in get_python_files_with_flag(module_dir).items():
            filename = str(os_path_basename(file_path))
            file_path = str(file_path)
            print(f"{file_path=}")
            if not filename.startswith("test") and "_util" not in file_path:
                for file_import in file_imports:
                    if str(file_import[0]).endswith("_str"):
                        print(f"{module_desc} {filename} {file_import[0]=}")
                    assert not str(file_import[0]).endswith("_str")


def test_Modules_util_AssestsExistForEveryStrFunction():
    """
    Test that all string-related functions in each module directory are asserted and tested.
    This test performs the following checks for each module:
    - Retrieves all string functions and ensures they are sorted and not duplicated.
    - Verifies that if string functions exist, a corresponding test file exists in the module's utility directory.
    - Checks that the test file imports exactly one object and that imports are ordered.
    - Ensures the test file contains a single test function named 'test_str_functions_ReturnsObj'.
    - Validates that the test file includes the necessary assertions for all string functions.
    Raises:
        AssertionError: If any of the above conditions are not met.
    """

    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    running_str_functions = set()
    for module_desc, module_dir in get_module_descs().items():
        desc_number_str = module_desc[1:3]
        test_dir = create_path(module_dir, "test")
        util_dir = create_path(test_dir, "_util")
        print(f"{util_dir}")
        module_str_funcs = get_module_str_functions(module_dir, desc_number_str)
        check_if_module_str_funcs_is_sorted(module_str_funcs)
        check_str_funcs_are_not_duplicated(module_str_funcs, running_str_functions)
        running_str_functions.update(set(module_str_funcs))

        if len(module_str_funcs) > 0:
            test_file_path = create_path(util_dir, f"test_a{desc_number_str}_str.py")
            assert os_path_exists(test_file_path)
            test_file_imports = get_imports_from_file(test_file_path)
            assert len(test_file_imports) == 1
            check_import_objs_are_ordered(test_file_imports, test_file_path)
            test_functions = get_function_names_from_file(test_file_path)
            assert test_functions == ["test_str_functions_ReturnsObj"]
            check_str_func_test_file_has_needed_asserts(
                module_str_funcs, test_file_path, util_dir, desc_number_str
            )


def test_Modules_test_TestsAreInCorrectFolderStructure():
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    for module_desc, module_dir in get_module_descs().items():
        desc_number = int(module_desc[1:3])
        level1_dirs = get_level1_dirs(module_dir)
        print(f"{desc_number} {level1_dirs=}")
        test_str = "test"
        for level1_dir in level1_dirs:
            if level1_dir.find(test_str) > -1:
                if level1_dir != test_str:
                    print(f"{desc_number=} {level1_dir=}")
                assert level1_dir == test_str
