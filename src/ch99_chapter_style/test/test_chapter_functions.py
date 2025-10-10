from importlib import import_module as importlib_import_module
from inspect import getsource as inspect_getsource
from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import (
    create_path,
    get_dir_file_strs,
    get_dir_filenames,
    open_file,
)
from src.ch98_docs_builder.doc_builder import (
    get_chapter_desc_prefix,
    get_chapter_desc_str_number,
    get_chapter_descs,
    get_chapter_num_descs,
    get_chXX_keyword_classes,
    get_cumlative_ch_keywords_dict,
    get_keywords_by_chapter,
    get_keywords_src_config,
)
from src.ch99_chapter_style.style import (
    check_all_test_functions_are_formatted,
    check_all_test_functions_have_proper_naming_format,
    check_if_test_HasDocString_pytests_exist,
    check_if_test_ReturnsObj_pytests_exist,
    find_incorrect_imports,
    get_all_semantic_types_from_ref_files,
    get_chapters_func_class_metrics,
    get_docstring,
    get_json_files,
    get_max_chapter_import_str,
    get_python_files_with_flag,
    get_semantic_types_filename,
    get_top_level_functions,
)


def expected_semantic_types() -> set:
    return {
        "BeliefName",
        "RespectGrain",
        "CRUD_command",
        "FirstLabel",
        "NexusLabel",
        "EventInt",
        "FaceName",
        "FundGrain",
        "FundNum",
        "GrainNum",
        "GroupTitle",
        "HealerName",
        "KnotTerm",
        "LabelTerm",
        "LobbyID",
        "MomentLabel",
        "MoneyNum",
        "NameTerm",
        "MoneyGrain",
        "PoolNum",
        "RespectNum",
        "RopeTerm",
        "TimeLineLabel",
        "TimeLinePoint",
        "TitleTerm",
        "VoiceName",
        "WorldName",
    }


def test_Chapters_CheckStringMetricsFromEveryFile():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH
    excluded_functions = {
        "_get_inx_label",
        "_get_inx_value",
        "_get_rid_of_translate_core_keys",
        "_is_inx_knot_inclusion_correct",
        "_is_otx_knot_inclusion_correct",
        "_unknown_str_in_otx2inx",
        "add_fund_give_take",
        "del_label",
        "del_otx2inx",
        "env_dir_setup_cleanup",
        "find_replace_rope",
        "get_json",
        "get_chapter_temp_dir",
        "get_obj_key",
        "is_empty",
        "is_valid",
        "label_exists",
        "otx_exists",
        "otx2inx_exists",
        "reveal_inx",
        "set_all_otx2inx",
        "set_knot",
        "set_label",
        "set_otx2inx",
        "to_dict",
    }

    # WHEN
    chapters_func_class_metrics = get_chapters_func_class_metrics(excluded_functions)
    duplicated_functions = chapters_func_class_metrics.get("duplicated_functions")
    unnecessarily_excluded_funcs = chapters_func_class_metrics.get(
        "unnecessarily_excluded_funcs"
    )
    semantic_types = chapters_func_class_metrics.get("semantic_types")
    all_functions = chapters_func_class_metrics.get("all_functions")

    # THEN
    for function_name in sorted(all_functions.keys()):
        func_metrics = all_functions.get(function_name)
        if func_metrics > 1:
            print(f"{function_name} {func_metrics=}")
    assertion_fail_str = f"Duplicated functions found: {duplicated_functions}"
    assert not duplicated_functions, assertion_fail_str
    # print(f"{sorted(unnecessarily_excluded_funcs.keys())=}")
    assert not unnecessarily_excluded_funcs, sorted(unnecessarily_excluded_funcs.keys())
    assert semantic_types == expected_semantic_types()
    print(f"{len(all_functions)=}")
    for semantic_type in sorted(list(semantic_types)):
        expected_semantic_type_exists_test_str = f"test_{semantic_type}_Exists"
        # print(expected_semantic_type_exists_test_str)
        assert expected_semantic_type_exists_test_str in all_functions


def test_Chapters_Semantic_Types_HasCorrectFormating():
    # ESTABLISH / WHEN
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_desc_prefix = get_chapter_desc_prefix(chapter_desc)
        docs_dir = create_path(chapter_dir, "_ref")
        semantic_types_filename = get_semantic_types_filename(chapter_desc_prefix)
        semantics_path = create_path(docs_dir, semantic_types_filename)
        print(f"{chapter_desc=}")
        # THEN
        # semantic_types_file never has import *
        assert open_file(semantics_path).find("import *") == -1


def test_Chapters_Semantic_Types_AreAllIn_chXX_semantic_types_ref_files():
    # ESTABLISH / WHEN
    ref_files_semantic_types = get_all_semantic_types_from_ref_files()

    # THEN
    print(f"{len(ref_files_semantic_types)=}")
    expected_types = expected_semantic_types()
    print(f"{len(expected_types)=}")
    print(f"missing {expected_types.difference(ref_files_semantic_types)}")

    assert ref_files_semantic_types == expected_types


def test_Chapters_KeywordsAppearWhereTheyShould():
    """Test that checks no str function is created before it is needed or after the term is used."""

    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH
    # "close" is excluded because it is used to close sqlite database connections
    excluded_strs = {"close"}
    # new method references from keywords config file
    keywords_dict = get_keywords_src_config()
    keywords_by_chapter = get_keywords_by_chapter(keywords_dict)
    all_keywords_set = set(keywords_dict.keys())
    keywords_in_ch_count = {}
    for keyword in keywords_dict.keys():
        keywords_in_ch_count[keyword] = {}
    cumlative_ch_keywords_dict = get_cumlative_ch_keywords_dict(keywords_by_chapter)

    # WHEN / THEN
    # all_file_count = 0
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        allowed_chapter_keywords = cumlative_ch_keywords_dict.get(chapter_prefix)
        not_allowed_keywords = all_keywords_set.difference(allowed_chapter_keywords)
        not_allowed_keywords = not_allowed_keywords.difference(excluded_strs)
        # print(f"{chapter_prefix} {len(not_allowed_keywords)=}")

        chapter_files = list(get_python_files_with_flag(chapter_dir).keys())
        chapter_files.extend(list(get_json_files(chapter_dir)))
        chapter_files = sorted(chapter_files)
        # chapter_file_count = 0
        for file_path in chapter_files:
            # chapter_file_count += 1
            # all_file_count += 1
            # print(f"{all_file_count} Chapter: {chapter_file_count} {file_path}")
            file_str = open(file_path).read()
            for keyword in not_allowed_keywords:
                notallowed_keyword_failure_str = f"keyword {keyword} is not allowed in chapter {chapter_prefix}. It is in {file_path=}"
                assert keyword not in file_str, notallowed_keyword_failure_str
            # print(f"{file_path=}")
            excessive_imports_str = f"{file_path} has too many Keywords class imports"
            ch_class_name = f"C{chapter_prefix[1:]}Keywords"
            is_doc_builder_file = "doc_builder.py" in file_path
            if file_path.find(f"test_{chapter_prefix}_keywords.py") == -1:
                assert file_str.count("Keywords") <= 1, excessive_imports_str
            elif not is_doc_builder_file:
                assert file_str.count(ch_class_name) in {0, 4}, ""
            enum_x = f"{file_path} Keywords Class Import is wrong, it should be {ch_class_name}"
            if "Keywords" in file_str and not is_doc_builder_file:
                assert ch_class_name in file_str, enum_x

            is_ref_keywords_file = f"\\{chapter_prefix}_keywords.py" in file_path
            if is_ref_keywords_file:
                # print(f"{file_path=}")
                assert file_str.count("keywords import") == 0, "No imports"
                assert file_str.count("from enum import Enum") == 1, "import Enum"

            for keyword in allowed_chapter_keywords:
                if keyword in file_str:
                    add_ch_keyword_count(keywords_in_ch_count, keyword, chapter_prefix)

    # Check that keyword is not introduced before it is used.
    for keyword, chapters_dict in keywords_in_ch_count.items():
        # for chapter_prefix in sorted(chapters_dict.keys()):
        #     chapter_count = chapters_dict.get(chapter_prefix)
        #     # print(f"{keyword=} {chapter_prefix} {chapter_count=}")
        min_chapter_prefix = min(chapters_dict.keys())
        min_chapter_count = chapters_dict.get(min_chapter_prefix)
        if min_chapter_count <= 2:
            print(f"{keyword=} {min_chapter_prefix} {min_chapter_count=}")
        assert min_chapter_count != 1


def add_ch_keyword_count(keywords_ch_counts: dict, keyword: str, chapter_prefix: str):
    keyword_ch_counts = keywords_ch_counts.get(keyword)
    if keyword_ch_counts.get(chapter_prefix) is None:
        keyword_ch_counts[chapter_prefix] = 0
    keyword_ch_counts[chapter_prefix] += 1


def test_Chapters_FirstLevelFilesDoNotImportKeywords():
    """Test that checks no str function is created before it is needed or after the term is used."""
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests

    # ESTABLISH

    # WHEN / THEN
    # all_file_count = 0
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)

        chapter_files = list(get_dir_file_strs(chapter_dir, include_dirs=False).keys())
        chapter_files = sorted(chapter_files)
        print(f"{chapter_files=}")
        # chapter_file_count = 0
        for filename in chapter_files:
            file_path = create_path(chapter_dir, filename)
            file_str = open_file(file_path)
            print(f"{file_path=}")
            assert "Keywords" not in file_str, f"Keywords reference in {file_path}"


def test_Chapters_KeywordEnumClassesAreCorrectlyTested():
    """"""
    keywords_dict = get_keywords_src_config()
    keywords_by_chapter = get_keywords_by_chapter(keywords_dict)
    cumlative_ch_keywords_dict = get_cumlative_ch_keywords_dict(keywords_by_chapter)

    chXX_keyword_classes = get_chXX_keyword_classes(cumlative_ch_keywords_dict)
    chapter_num_descs = get_chapter_num_descs()

    for chapter_prefix, ExpectedEnumClass in chXX_keyword_classes.items():
        chapter_ref_keywords_path = f"src.ref.{chapter_prefix}_keywords"
        print(f"{chapter_ref_keywords_path=}")

        # dynamically import the module
        mod = importlib_import_module(chapter_ref_keywords_path)
        enum_class_name = f"C{chapter_prefix[1:]}Keywords"
        # try:
        #     getattr(mod, enum_class_name)
        # except Exception:
        #     print(f"class {enum_class_name}(str, Enum):")
        #     for keyword in sorted(list(cumlative_ch_keywords_dict.get(chapter_num))):
        #         print(f"    {keyword} = '{keyword}'")
        #     print("def __str__(self): return self.value")

        # print(f"{len(mod.__dict__)=}")
        ChKeywordsClass = getattr(mod, enum_class_name)
        assert ChKeywordsClass
        expected_enum_keys = set(ExpectedEnumClass.__dict__.keys())
        current_enum_keys = set(ChKeywordsClass.__dict__.keys())
        # print(expected_enum_keys.difference(current_enum_keys))
        assert not expected_enum_keys.difference(current_enum_keys)
        expected_dunder_str_func = """    def __str__(self):
        return self.value
"""
        assert inspect_getsource(ChKeywordsClass.__str__) == expected_dunder_str_func
        # assert ChKeywordsClass == ExpectedEnumClass


def test_Chapters_AllImportsAreFromLibrariesInLessThanEqual_aXX():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH
    chapter_descs = get_chapter_descs()
    mod_descs_sorted = sorted(list(chapter_descs.keys()))

    # WHEN / THEN
    all_file_count = 0
    for chapter_desc in mod_descs_sorted:
        chapter_dir = chapter_descs.get(chapter_desc)
        chapter_desc_str_number = get_chapter_desc_str_number(chapter_desc)
        desc_number_int = int(chapter_desc_str_number)
        chapter_files = sorted(list(get_python_files_with_flag(chapter_dir).keys()))
        # print(f"{desc_number_str} src.{chapter_desc}")
        for chapter_file_count, file_path in enumerate(chapter_files, start=1):
            all_file_count += 1
            incorrect_imports = find_incorrect_imports(file_path, desc_number_int)
            if len(incorrect_imports) == 1 and file_path.find("_keywords.py") > 0:
                incorrect_imports = []

            assertion_fail_str = f"File #{all_file_count} a{chapter_desc_str_number} file #{chapter_file_count} Imports: {len(incorrect_imports)} {file_path}"
            assert not incorrect_imports, assertion_fail_str


def test_Chapters_All_semantic_types_NamesAreKeywords():
    # ESTABLISH / WHEN
    all_keywords = set(get_keywords_src_config().keys())

    # THEN
    # make semantic_type names required keyword str functions
    semantic_types = expected_semantic_types()
    semantic_keywords_by_chapter = set(semantic_types)
    print(
        f"semantic_types without str function: {sorted(list(semantic_keywords_by_chapter.difference(all_keywords)))}"
    )
    assert semantic_keywords_by_chapter.issubset(all_keywords)


def test_Chapters_path_FunctionStructureAndFormat():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    x_count = 0
    path_functions = {}
    all_test_functions = {}
    chapters_path_funcs = {}
    filtered_chapters_path_funcs = {}
    filterout_path_funcs = {
        "create_path",
        "create_directory_path",
        "rope_is_valid_dir_path",
    }
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        filenames_set = get_dir_filenames(chapter_dir, include_extensions={"py"})
        filtered_path_funcs = set()
        path_func_set = set()
        chapters_path_funcs[chapter_desc] = path_func_set
        filtered_chapters_path_funcs[chapter_desc] = filtered_path_funcs
        for filepath_set in filenames_set:
            file_dir = create_path(chapter_dir, filepath_set[0])
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
    # for chapter_desc, path_funcs in chapters_path_funcs.items():
    #     print(f"{chapter_desc=} {path_funcs=}")

    for chapter_desc, chapter_dir in get_chapter_descs().items():
        if len(filtered_chapters_path_funcs.get(chapter_desc)) > 0:
            chapter_desc_prefix = get_chapter_desc_prefix(chapter_desc)
            path_func_filename = f"{chapter_desc_prefix}_path.py"
            _ref_dir = create_path(chapter_dir, "_ref")
            path_func_library = create_path(_ref_dir, path_func_filename)
            path_funcs = filtered_chapters_path_funcs.get(chapter_desc)
            assert os_path_exists(path_func_library)

            test_dir = create_path(chapter_dir, "test")
            util_dir = create_path(test_dir, "_util")
            pytest_path_func_filename = f"test_{path_func_filename}"
            pytest_path_func_path = create_path(util_dir, pytest_path_func_filename)
            assert os_path_exists(pytest_path_func_path)
            test_path_func_names = set(
                get_top_level_functions(pytest_path_func_path).keys()
            )
            # print(f"{chapter_desc} {test_path_func_names=}")
            check_if_test_ReturnsObj_pytests_exist(
                path_funcs, chapter_desc, test_path_func_names
            )
            check_if_test_HasDocString_pytests_exist(
                path_funcs, chapter_desc, test_path_func_names
            )

    all_test_function_names = all_test_functions.keys()
    check_all_test_functions_have_proper_naming_format(all_test_function_names)
    check_all_test_functions_are_formatted(all_test_functions)
