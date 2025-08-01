from os import listdir as os_listdir, walk as os_walk
from os.path import basename as os_path_basename, exists as os_path_exists
from pathlib import Path as pathlib_Path
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    get_dir_file_strs,
    get_dir_filenames,
    get_level1_dirs,
)
from src.a99_module_linter.module_eval import (
    check_if_module_str_funcs_is_sorted,
    check_import_objs_are_ordered,
    check_str_func_test_file_has_needed_asserts,
    check_str_funcs_are_not_duplicated,
    get_all_str_functions,
    get_docstring,
    get_duplicated_functions,
    get_function_names_from_file,
    get_imports_from_file,
    get_json_files,
    get_module_descs,
    get_module_str_functions,
    get_python_files_with_flag,
    get_top_level_functions,
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


def test_Modules_StrFunctionsAppearWhereTheyShould():
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH
    all_str_functions = get_all_str_functions()
    str_first_ref = {str_function: None for str_function in all_str_functions}
    # "close" is excluded because it is used to close sqlite database connections
    excluded_strs = {"close"}

    # WHEN / THEN

    for module_desc, module_dir in get_module_descs().items():
        desc_number_str = module_desc[1:3]
        module_files = list(get_python_files_with_flag(module_dir).keys())
        module_files.extend(list(get_json_files(module_dir)))
        module_files = sorted(module_files)
        str_funcs_set = set(get_module_str_functions(module_dir, desc_number_str))
        print(f"{desc_number_str} {str_funcs_set=}")
        for file_path in module_files:
            if file_path.find("_util") == -1:
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


def test_Modules_CheckMarkdownHasAllStrFunctions():
    # sourcery skip: no-loop-in-tests
    # ESTALBLISH Gather lines here
    doc_main_dir = pathlib_Path("docs")
    doc_main_dir.mkdir(parents=True, exist_ok=True)

    # WHEN
    func_lines = ["## Str Functions by Module"]
    for module_desc, module_dir in get_module_descs().items():
        desc_number_str = module_desc[1:3]
        module_str_funcs = get_module_str_functions(module_dir, desc_number_str)
        x_list = [str_func[:-4] for str_func in module_str_funcs]
        _line = f"- {module_desc}: " + ", ".join(x_list)
        func_lines.append(_line)

    dst_path = pathlib_Path(f"{doc_main_dir}/str_funcs.md")
    str_func_markdown = "# String Functions by Module\n\n" + "\n".join(func_lines)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text(str_func_markdown)

    # THEN
    assert dst_path.exists(), f"Failed to write manifest to {dst_path}"
    # print(str_func_markdown)
    # assert dst_path.exists(), f"{dst_path} does not exist"
    # print(open(dst_path).read())
    assert open(dst_path).read() == str_func_markdown


def test_Modules_MostFunctionsAreUniquelyNamed():
    # ESTABLISH
    excluded_functions = {
        "_example_empty_bob_believerunit",
        "_get_inx_label",
        "_get_inx_value",
        "_get_rid_of_pidgin_core_keys",
        "_is_inx_knot_inclusion_correct",
        "_is_otx_knot_inclusion_correct",
        "_unknown_str_in_otx2inx",
        "add_2_curve",
        "add_column_rect",
        "add_cycle_to_tax_arrows",
        "add_fund_give_take",
        "add_grants_top",
        "add_keep__rect",
        "add_keep_str",
        "add_believeratom",
        "add_rect_arrow",
        "add_rect_str",
        "add_river_col",
        "add_river_rect",
        "add_river_row",
        "add_rivercycle",
        "add_taxs_bottom",
        "add_taxs_column",
        "atom_file_exists",
        "black_str",
        "blue_str",
        "bob_str",
        "buz_str",
        "car_str",
        "casa_rope",
        "casa_str",
        "clean_rope",
        "clean_str",
        "clear_fund_give_take",
        "clear_status",
        "contains_knot",
        "cook_rope",
        "cook_str",
        "create_kpi_csvs",
        "darkred_str",
        "del_label",
        "del_otx2inx",
        "eat_rope",
        "eat_str",
        "ell_str",
        "env_dir_setup_cleanup",
        "example_casa_clean_factunit",
        "example_casa_dirty_factunit",
        "example_casa_grimy_factunit",
        "example_sky_blue_factunit",
        "find_replace_rope",
        "full_rope",
        "full_str",
        "fund_graph0",
        "get_atom_example_planunit_ball",
        "get_atom_example_planunit_knee",
        "get_atom_example_planunit_sports",
        "get_atom_example_factunit_knee",
        "get_bob_mop_with_reason_believerunit_example",
        "get_budunit_55_example",
        "get_budunit_66_example",
        "get_budunit_88_example",
        "get_budunit_invalid_example",
        "get_class_type",
        "get_dict",
        "get_edited_believer",
        "get_factunits_dict",
        "get_from_dict",
        "get_from_json",
        "get_json",
        "get_membership",
        "get_module_temp_dir",
        "get_obj_key",
        "get_believerdelta_example1",
        "get_believerdelta_sue_example",
        "get_believerunit_irrational_example",
        "get_believerunit_with_4_levels",
        "get_slash_namemap",
        "get_slash_ropemap",
        "get_slash_titlemap",
        "get_sue_packunit",
        "get_texas_hubunit",
        "get_texas_rope",
        "grants1_dict",
        "green_str",
        "hungry_rope",
        "hungry_str",
        "is_empty",
        "is_valid",
        "joc_str",
        "label_exists",
        "LightSeaGreen_str",
        "luc_str",
        "membership_exists",
        "otx_exists",
        "otx2inx_exists",
        "pack_file_exists",
        "believeratom_exists",
        "purple_str",
        "red_str",
        "reveal_inx",
        "ric_str",
        "rivercycle1_dict",
        "rivercycle2_dict",
        "rivercycle3_dict",
        "rivercycle4_dict",
        "run_rope",
        "run_str",
        "set_all_otx2inx",
        "set_knot",
        "set_label",
        "set_level",
        "set_membership",
        "set_nameterm",
        "set_otx2inx",
        "set_status",
        "set_sums",
        "sue_1believeratoms_packunit",
        "sue_2believeratoms_packunit",
        "sue_3believeratoms_packunit",
        "sue_4believeratoms_packunit",
        "sue_str",
        "taxs1_dict",
        "test_str_functions_ReturnsObj",
        "xio_str",
        "yao_str",
        "zia_str",
    }

    # WHEN
    duplicated_functions = get_duplicated_functions(excluded_functions)

    # THEN
    assertion_fail_str = f"Duplicated functions found: {duplicated_functions}"
    assert not duplicated_functions, assertion_fail_str


def test_Modules_path_FunctionStructureAndFormat():
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    x_count = 0
    path_functions = {}
    modules_path_funcs = {}
    filtered_modules_path_funcs = {}
    filterout_path_funcs = {
        "create_path",
        "create_directory_path",
        "ropeterm_valid_dir_path",
    }
    for module_desc, module_dir in get_module_descs().items():
        filenames_set = get_dir_filenames(module_dir, include_extensions={"py"})
        filtered_path_funcs = set()
        path_func_set = set()
        modules_path_funcs[module_desc] = path_func_set
        filtered_modules_path_funcs[module_desc] = filtered_path_funcs
        for filenames in filenames_set:
            file_dir = create_path(module_dir, filenames[0])
            file_path = create_path(file_dir, filenames[1])
            file_functions = get_top_level_functions(file_path)
            for function_name in file_functions:
                x_count += 1
                if str(function_name).endswith("_path"):
                    # print(
                    #     f"Function #{x_count}: Path function {function_name} in {file_path}"
                    # )
                    path_functions[function_name] = file_path
                    path_func_set.add(function_name)
                    if (
                        not str(function_name).endswith("config_path")
                        and function_name not in filterout_path_funcs
                    ):
                        filtered_path_funcs.add(function_name)

    print(f"Total path functions found: {len(path_functions)}")
    for function_name, file_path in path_functions.items():
        func_docstring = get_docstring(file_path, function_name)
        if not func_docstring:
            print(f"docstring for {function_name} is None")
        else:
            print(
                f"docstring for {function_name}: \t{func_docstring.replace("\n", "")}"
            )
        assert func_docstring is not None, function_name

    # print(f"Path functions: {path_functions.keys()=}")
    # for module_desc, path_funcs in modules_path_funcs.items():
    #     print(f"{module_desc=} {path_funcs=}")

    for module_desc, module_dir in get_module_descs().items():
        if len(filtered_modules_path_funcs.get(module_desc)) > 0:
            path_func_filename = f"a{module_desc[1:3]}_path.py"
            path_func_library = create_path(module_dir, path_func_filename)
            path_funcs = filtered_modules_path_funcs.get(module_desc)
            assert os_path_exists(path_func_library)

            test_dir = create_path(module_dir, "test")
            util_dir = create_path(test_dir, "_util")
            pytest_path_func_filename = f"test_{path_func_filename}"
            pytest_path_func_path = create_path(util_dir, pytest_path_func_filename)
            assert os_path_exists(pytest_path_func_path)
            test_path_func_names = set(get_top_level_functions(pytest_path_func_path))
            # print(f"{module_desc} {test_path_func_names=}")
            check_if_test_ReturnsObj_pytests_exist(
                path_funcs, module_desc, test_path_func_names
            )
            check_if_test_HasDocString_pytests_exist(
                path_funcs, module_desc, test_path_func_names
            )


def check_if_test_ReturnsObj_pytests_exist(
    path_funcs: set, module_desc: str, test_path_func_names: set[str]
):
    for path_func in path_funcs:
        pytest_for_func_exists = False
        # print(f"{module_desc} {path_func}")
        expected_test_func = f"test_{path_func}_ReturnsObj"
        for test_path_func_name in test_path_func_names:
            if test_path_func_name.startswith(expected_test_func):
                pytest_for_func_exists = True
            # print(
            #     f"{pytest_for_func_exists} {module_desc} {path_func} {test_path_func_name}"
            # )
        assert pytest_for_func_exists, f"missing {expected_test_func=}"
        # print(f"{module_desc} {test_func_exists} {path_func}")


def check_if_test_HasDocString_pytests_exist(
    path_funcs: set, module_desc: str, test_path_func_names: set[str]
):
    for path_func in path_funcs:
        pytest_for_func_exists = False
        print(f"{module_desc} {path_func}")
        expected_test_func = f"test_{path_func}_HasDocString"
        for test_path_func_name in test_path_func_names:
            if test_path_func_name.startswith(expected_test_func):
                pytest_for_func_exists = True
            # print(
            #     f"{pytest_for_func_exists} {module_desc} {path_func} {test_path_func_name}"
            # )
        assert pytest_for_func_exists, f"missing {expected_test_func=}"
        # print(f"{module_desc} {test_func_exists} {path_func}")


def test_check_Modules_filenames_FollowFileNameConventions_NoNamingCollision():
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH
    all_level1_py_files = set()
    for module_desc, module_dir in get_module_descs().items():
        level1_py_files = set(get_dir_file_strs(module_dir, True, False, True).keys())
        all_level1_py_files.update(level1_py_files)
        # print(f"{level1_py_files=}")
        base_map = {}

        for focus_filenamebase in level1_py_files:
            for check_filenamebase in level1_py_files:
                if check_filenamebase.find(focus_filenamebase) > -1:
                    if base_map.get(focus_filenamebase) is None:
                        base_map[focus_filenamebase] = []
                    base_map[focus_filenamebase].append(check_filenamebase)

        collisions = []
        for name_group in base_map.values():
            if len(name_group) > 1:
                collisions.extend(name_group)
        if collisions:
            print(f"{module_desc} {collisions=}")
        assert not collisions

    # CHECK for collisions acress modules
    # all_base_map = {}

    # for focus_filenamebase in all_level1_py_files:
    #     for check_filenamebase in all_level1_py_files:
    #         if check_filenamebase.find(focus_filenamebase) > -1:
    #             if all_base_map.get(focus_filenamebase) is None:
    #                 all_base_map[focus_filenamebase] = []
    #             all_base_map[focus_filenamebase].append(check_filenamebase)

    # all_collisions = []
    # for name_group in all_base_map.values():
    #     if len(name_group) > 1:
    #         all_collisions.extend(name_group)
    # if all_collisions:
    #     print(f"{module_desc} {all_collisions=}")
    # assert not all_collisions
