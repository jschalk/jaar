from os.path import basename as os_path_basename
from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path
from src.a99_module_logic.module_eval import (
    check_if_module_str_funcs_is_sorted,
    check_import_objs_are_ordered,
    check_module_imports_are_ordered,
    check_str_func_test_file_has_needed_asserts,
    check_str_funcs_are_not_duplicated,
    get_all_str_functions,
    get_function_names_from_file,
    get_imports_from_file,
    get_json_files,
    get_module_descs,
    get_module_str_functions,
    get_python_files_with_flag,
)


def test_ModuleStrFunctionsTestFileFormat():
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH

    # WHEN / THEN
    # previous_module_number = -1
    for module_desc, module_dir in get_module_descs().items():
        module_number = int(module_desc[1:3])
        # assert module_number == previous_module_number + 1
        print(f"{module_desc=} {module_number=}")
        utils_dir = create_path(module_dir, "_test_util")
        assert os_path_exists(utils_dir)
        str_func_path = create_path(utils_dir, f"a{module_desc[1:3]}_str.py")
        assert os_path_exists(str_func_path)
        env_files = get_python_files_with_flag(utils_dir, "env")
        if len(env_files) > 0:
            print(f"{env_files=}")
            assert len(env_files) == 1
            env_filename = str(list(env_files.keys())[0])
            print(f"{env_filename=}")
            assert env_filename.endswith(f"a{module_desc[1:3]}_env.py")

        # previous_module_number = module_number


def test_PythonFileImportsFormat():
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN / THEN
    for module_desc, module_dir in get_module_descs().items():
        python_files = get_python_files_with_flag(module_dir)
        desc_number = int(module_desc[1:3])
        # print(f"{desc_number} {module_desc=} {len(python_files)=}")
        for file_path, file_imports in python_files.items():
            # check_module_imports_are_ordered(file_imports, file_path, desc_number)
            # TODO uncomment and correct all file imports
            # check_import_objs_are_ordered(file_imports, file_path)

            filename = str(os_path_basename(file_path))
            file_path = str(file_path)
            if not filename.startswith("test") and "_test_util" not in file_path:
                for file_import in file_imports:
                    if str(file_import[0]).endswith("_str"):
                        print(f"{module_desc} {filename} {file_import[0]=}")
                    assert not str(file_import[0]).endswith("_str")


def test_StrFunctionsAreAssertTested():
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH

    # WHEN / THEN
    running_str_functions = set()
    for module_desc, module_dir in get_module_descs().items():
        desc_number_str = module_desc[1:3]
        util_dir = create_path(module_dir, "_test_util")
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


def test_StrFunctionsAppearWhereTheyShould():
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH
    all_str_functions = get_all_str_functions()
    str_first_ref = {str_function: None for str_function in all_str_functions}
    # TODO change excluded_strs to empty set by editing codebase
    excluded_strs = {"close", "time", "day", "days"}

    # WHEN / THEN
    for module_desc, module_dir in get_module_descs().items():
        desc_number_str = module_desc[1:3]
        module_files = list(get_python_files_with_flag(module_dir).keys())
        module_files.extend(list(get_json_files(module_dir)))
        module_files = sorted(module_files)
        str_funcs_set = set(get_module_str_functions(module_dir, desc_number_str))
        for file_path in module_files:
            if file_path.find("_test_util") == -1:
                first_ref_missing_strs = {
                    str_function[:-4]
                    for str_function in str_first_ref
                    if str_first_ref.get(str_function) is None
                }
                file_str = open(file_path).read()
                for x_str in first_ref_missing_strs:
                    if file_str.find(x_str) > -1 and x_str not in excluded_strs:
                        x_str_func_name = f"{x_str}_str"
                        str_first_ref[x_str_func_name] = file_path
                        if x_str_func_name not in str_funcs_set:
                            print(f"missing {x_str=} {file_path=}")
                        assert x_str_func_name in str_funcs_set
