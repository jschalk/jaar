from importlib import import_module as importlib_import_module
from inspect import getmembers as inspect_getmembers, isfunction as inspect_isfunction
from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, get_dir_filenames
from src.a98_docs_builder.module_eval import get_module_descs, get_module_str_functions
from src.a99_module_linter.linter import (
    check_all_test_functions_are_formatted,
    check_all_test_functions_have_proper_naming_format,
    check_if_test_HasDocString_pytests_exist,
    check_if_test_ReturnsObj_pytests_exist,
    get_all_str_functions,
    get_docstring,
    get_duplicated_functions,
    get_json_files,
    get_max_module_import_str,
    get_python_files_with_flag,
    get_top_level_functions,
)


def test_Modules_StrFunctionsAppearWhereTheyShould():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH
    all_str_functions = get_all_str_functions()
    str_first_ref = {str_function: None for str_function in all_str_functions}
    # "close" is excluded because it is used to close sqlite database connections
    excluded_strs = {"close"}

    # WHEN / THEN
    # all_file_count = 0
    for module_desc, module_dir in get_module_descs().items():
        desc_number_str = module_desc[1:3]
        module_files = list(get_python_files_with_flag(module_dir).keys())
        module_files.extend(list(get_json_files(module_dir)))
        module_files = sorted(module_files)
        str_funcs_set = set(get_module_str_functions(module_dir, desc_number_str))
        # print(f"{desc_number_str} {len(str_funcs_set)=}")
        # module_file_count = 0
        for file_path in module_files:
            if file_path.find("_util") == -1:
                # module_file_count += 1
                # all_file_count += 1
                # print(f"{all_file_count} Module: {module_file_count} {file_path}")
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


# def test_Modules_AllImportsAreFromLibrariesInLessThanEqual_aXX():
#     # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
#     # ESTABLISH
#     module_descs = get_module_descs()


#     # WHEN / THEN
#     all_file_count = 0
#     for module_desc, module_dir in get_module_descs().items():
#         desc_number_str = module_desc[1:3]
#         module_files = list(get_python_files_with_flag(module_dir).keys())
#         module_files.extend(list(get_json_files(module_dir)))
#         module_files = sorted(module_files)
#         str_funcs_set = set(get_module_str_functions(module_dir, desc_number_str))
#         print(f"{desc_number_str} {len(str_funcs_set)=}")
#         module_file_count = 0
#         for file_path in module_files:
#             if file_path.find("_util") == -1:
#                 module_file_count += 1
#                 all_file_count += 1
#                 print(f"{all_file_count} Module: {module_file_count} {file_path}")
#                 first_ref_missing_strs = {
#                     str_function[:-4]
#                     for str_function in str_first_ref
#                     if str_first_ref.get(str_function) is None
#                 }
#                 file_str = open(file_path).read()
#                 for x_str in first_ref_missing_strs:
#                     if file_str.find(x_str) > -1 and x_str not in excluded_strs:
#                         x_str_func_name = f"{x_str}_str"
#                         str_first_ref[x_str_func_name] = file_path
#                         if x_str_func_name not in str_funcs_set:
#                             print(f"missing {x_str=} {file_path=}")
#                         assert x_str_func_name in str_funcs_set
#     assert 1 == 2


def test_Modules_StrFunctionsAreAllImported():
    # ESTABLISH / WHEN
    all_str_functions = get_all_str_functions()

    # THEN confirm all str functions are imported to max module
    max_module_import_str = get_max_module_import_str()
    print(f"{max_module_import_str=}")
    max_mod_obj = importlib_import_module(max_module_import_str)
    mod_all_funcs = inspect_getmembers(max_mod_obj, inspect_isfunction)
    mod_str_funcs = {name for name, obj in mod_all_funcs if not name.startswith("__")}

    print(f"{len(mod_all_funcs)=}")
    assert len(all_str_functions) == len(mod_str_funcs)
    all_str_func_set = set(all_str_functions)
    assert all_str_func_set == mod_str_funcs


def test_Modules_MostFunctionsAreUniquelyNamed():
    # ESTABLISH
    excluded_functions = {
        "_example_empty_bob_beliefunit",
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
        "add_beliefatom",
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
        "get_bob_mop_with_reason_beliefunit_example",
        "get_budunit_55_example",
        "get_budunit_66_example",
        "get_budunit_88_example",
        "get_budunit_invalid_example",
        "get_class_type",
        "get_dict",
        "get_edited_belief",
        "get_factunits_dict",
        "get_from_dict",
        "get_from_json",
        "get_json",
        "get_membership",
        "get_module_temp_dir",
        "get_obj_key",
        "get_beliefdelta_example1",
        "get_beliefdelta_sue_example",
        "get_beliefunit_irrational_example",
        "get_beliefunit_with_4_levels",
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
        "beliefatom_exists",
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
        "sue_1beliefatoms_packunit",
        "sue_2beliefatoms_packunit",
        "sue_3beliefatoms_packunit",
        "sue_4beliefatoms_packunit",
        "sue_str",
        "taxs1_dict",
        "test_str_functions_ReturnsObj",
        "to_dict",
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
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    x_count = 0
    path_functions = {}
    all_test_functions = {}
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
        for filepath_set in filenames_set:
            file_dir = create_path(module_dir, filepath_set[0])
            file_path = create_path(file_dir, filepath_set[1])
            file_functions = get_top_level_functions(file_path)
            for function_name in file_functions.keys():
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
                if str(function_name).startswith("test_"):
                    function_str = file_functions.get(function_name)
                    all_test_functions[function_name] = function_str

    print(f"Total path functions found: {len(path_functions)}")
    for function_name, file_path in path_functions.items():
        func_docstring = get_docstring(file_path, function_name)
        # if not func_docstring:
        #     print(f"docstring for {function_name} is None")
        # else:
        #     print(
        #         f"docstring for {function_name}: \t{func_docstring.replace("\n", "")}"
        #     )
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
            test_path_func_names = set(
                get_top_level_functions(pytest_path_func_path).keys()
            )
            # print(f"{module_desc} {test_path_func_names=}")
            check_if_test_ReturnsObj_pytests_exist(
                path_funcs, module_desc, test_path_func_names
            )
            check_if_test_HasDocString_pytests_exist(
                path_funcs, module_desc, test_path_func_names
            )

    all_test_function_names = all_test_functions.keys()
    check_all_test_functions_have_proper_naming_format(all_test_function_names)
    check_all_test_functions_are_formatted(all_test_functions)
