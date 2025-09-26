# your_chapter.py
from ast import (
    FunctionDef as ast_FunctionDef,
    Import as ast_Import,
    ImportFrom as ast_ImportFrom,
    NodeVisitor as ast_NodeVisitor,
    get_docstring as ast_get_docstring,
    get_source_segment as ast_get_source_segment,
    parse as ast_parse,
    walk as ast_walk,
)
from os import walk as os_walk
from os.path import join as os_path_join
from pathlib import Path as pathlib_Path
from re import compile as re_compile
from src.ch01_data_toolbox.file_toolbox import create_path, get_dir_filenames
from src.ch98_docs_builder.doc_builder import (
    get_chapter_desc_prefix,
    get_chapter_desc_str_number,
    get_chapter_descs,
    get_function_names_from_file,
)
from textwrap import dedent as textwrap_dedent
from typing import List


def get_imports_from_file(file_path):
    """
    Parses a Python file and returns a list of lists.
    Each inner list contains:
    - The source chapter from a 'from ... import ...' statement
    - Followed by all imported objects from that chapter

    Example:
    [['math', 'sqrt', 'pi'], ['os.path', 'join']]

    :param file_path: Path to the Python (.py) file
    :return: List of lists: [chapter, imported_obj1, imported_obj2, ...]
    """
    imports = []

    with open(file_path, "r", encoding="utf-8") as file:
        node = ast_parse(file.read(), filename=file_path)

    for n in ast_walk(node):
        if isinstance(n, ast_ImportFrom) and n.module:
            import_entry = [n.module, [alias.name for alias in n.names]]
            imports.append(import_entry)

    return imports


def get_python_files_with_flag(directory, x_str=None) -> dict[str, list]:
    """
    Recursively finds .py files in a directory.
    If x_str is provided, only files with x_str in the filename are included.

    Returns a dictionary: {file_path: 1, ...}

    :param directory: Root directory to search
    :param x_str: Optional substring to filter filenames
    :return: Dictionary of matching file paths and the number 1
    """
    py_files = {}

    for root, _, files in os_walk(directory):
        for file in files:
            if file.endswith(".py") and (x_str is None or x_str in file):
                full_path = os_path_join(root, file)
                py_files[full_path] = get_imports_from_file(full_path)

    return py_files


def get_json_files(directory) -> set[str]:
    json_files = set()

    for root, _, files in os_walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.add(os_path_join(root, file))

    return json_files


def get_top_level_functions(file_path) -> dict[str, str]:
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = ast_parse(source_code)
    functions = {}

    for node in tree.body:
        if isinstance(node, ast_FunctionDef):
            # Get the function name
            func_name = node.name

            # Extract the exact source text of the function
            # (ast.get_source_segment is available in Python 3.8+)
            func_source = ast_get_source_segment(source_code, node)

            # Optional: dedent to remove extra indentation
            if func_source:
                func_source = textwrap_dedent(func_source)

            functions[func_name] = func_source

    return functions

    # with open(file_path, "r") as f:
    #     tree = ast_parse(f.read(), filename=file_path)

    # functions = []
    # functions.extend(
    #     node.name for node in tree.body if isinstance(node, ast_FunctionDef)
    # )
    # return functions


def check_chapter_imports_are_ordered(imports: list[list], file_path: str, desc_number):
    previous_chapter_number = -1
    previous_chapter_str = "a"
    chapter_section_passed = False
    for x_import in imports:
        chapter_location = str(x_import[0])
        if chapter_location.startswith("src"):
            chapter_number = int(chapter_location[5:7])
            if desc_number < chapter_number:
                print(
                    f"{desc_number} {file_path} {chapter_number=} {chapter_location=}"
                )
            assert desc_number >= chapter_number
            assert chapter_section_passed is False
            if chapter_number < previous_chapter_number:
                print(
                    f"{file_path} {chapter_number=} {previous_chapter_number=} {x_import=}"
                )
            assert chapter_number >= previous_chapter_number
            previous_chapter_number = chapter_number
        else:
            chapter_section_passed = True
            if chapter_location <= previous_chapter_str:
                print(
                    f"{file_path} switch {chapter_location} and {previous_chapter_str}"
                )
            assert chapter_location > previous_chapter_str
            previous_chapter_str = chapter_location

        if chapter_location.endswith("env"):
            env_number = int(chapter_location[-6:-4])
            if desc_number != env_number:
                print(f"{desc_number} {file_path} {env_number=} {chapter_location=}")
            assert desc_number == env_number


def get_semantic_types_filename(chapter_desc_prefix: str) -> str:
    return f"{chapter_desc_prefix}_semantic_types.py"


def get_all_semantic_types_from_ref_files() -> set[str]:
    all_ref_files_semantic_types = set()
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        ref_dir = create_path(chapter_dir, "_ref")
        semantic_types_filename = get_semantic_types_filename(chapter_prefix)
        str_util_path = create_path(ref_dir, semantic_types_filename)
        functions, class_bases = get_function_names_from_file(str_util_path)
        print(f"{chapter_desc} {class_bases=}")
        all_ref_files_semantic_types.update(class_bases)
    print(all_ref_files_semantic_types)
    return all_ref_files_semantic_types


def get_all_str_functions() -> list:
    all_str_functions = []
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        ref_dir = create_path(chapter_dir, "_ref")
        str_util_path = create_path(ref_dir, f"{chapter_prefix}_keywords.py")
        str_functions, class_bases = get_function_names_from_file(str_util_path)
        if len(str_functions) > 0:
            all_str_functions.extend(iter(str_functions))
    return all_str_functions


def add_or_count_function_name_occurance(all_functions: dict, function_name: str):
    if all_functions.get(function_name):
        all_functions[function_name] += 1
    else:
        all_functions[function_name] = 1


def get_duplicated_functions(excluded_functions) -> set[str]:
    x_count = 0
    duplicate_functions = set()
    non_excluded_functions = set()
    all_functions = {}
    all_classes = {}
    semantic_type_candidates = {}
    for chapter_dir in get_chapter_descs().values():
        filenames_set = get_dir_filenames(chapter_dir, include_extensions={"py"})
        for filenames in filenames_set:
            file_dir = create_path(chapter_dir, filenames[0])
            file_path = create_path(file_dir, filenames[1])
            file_functions, class_bases = get_function_names_from_file(file_path)
            for x_class, x_bases in class_bases.items():
                if len(x_bases) > 1:
                    all_classes[x_class] = (
                        f"A class with more than one inheritance. {filenames[1]} {x_bases}"
                    )
                elif len(x_bases) == 0:
                    no_bases_str = f"A class with no inheritance. {filenames[1]}"
                    all_classes[x_class] = no_bases_str
                elif x_bases == ["Exception"]:
                    exception_base_str = f"An Exception inheritance. {filenames[1]}"
                    all_classes[x_class] = exception_base_str
                elif len(x_bases) == 1:
                    one_base_str = f"A single inheritance {filenames[1]} {x_bases}"
                    all_classes[x_class] = one_base_str
                    semantic_type_candidates[x_class] = x_bases
            for function_name in file_functions:
                add_or_count_function_name_occurance(all_functions, function_name)
                x_count += 1
                if function_name in non_excluded_functions:
                    print(
                        f"Function #{x_count}: Duplicate function {function_name} in {file_path}"
                    )
                    duplicate_functions.add(function_name)
                if function_name not in excluded_functions:
                    non_excluded_functions.add(function_name)
    # print(f"{duplicate_functions=}")
    # print(f"{len(non_excluded_functions)=}")
    # print(f"{len(all_functions)=}")
    unnecessarily_excluded_funcs = {
        function_name: f"{func_count=}. '{function_name}' does not need to be in excluded_functions set"
        for function_name, func_count in all_functions.items()
        if func_count == 1 and function_name in excluded_functions
    }
    for excluded_function in excluded_functions:
        if excluded_function not in all_functions:
            does_not_exist_str = f"'{excluded_function}' is not used in codebase"
            unnecessarily_excluded_funcs[excluded_function] = does_not_exist_str
    for func_name in sorted(list(all_functions.keys()), reverse=False):
        func_count = all_functions.get(func_name)
        # if func_count > 1:
        #     print(f"{func_name} {func_count=}")
    print(f"{len(excluded_functions)=}")

    # figure out which classes are semantic types
    semantic_types = get_semantic_types(semantic_type_candidates)
    return duplicate_functions, unnecessarily_excluded_funcs, semantic_types


def get_semantic_types(semantic_type_candidates) -> set:
    semantic_type_confirmed = set()
    base_types = (int, float, bool, str, list, tuple, range, dict, set)
    # Check if any base is in base_types by name
    candidates_list = list(semantic_type_candidates.keys())

    while candidates_list != []:
        x_class = candidates_list.pop()
        bases = semantic_type_candidates.get(x_class)
        is_subclass = any(base in [t.__name__ for t in base_types] for base in bases)
        if is_subclass:
            semantic_type_confirmed.add(x_class)
        else:
            x_base = bases[0]
            new_bases = semantic_type_candidates.get(x_base)
            if new_bases:
                # if x_base exists in semantic_type_candidates change classes bases reference to parent class
                semantic_type_candidates[x_class] = new_bases
                candidates_list.append(x_class)
                # print(f"{x_class} popped {x_base=} {new_bases=}")

    print(f"{sorted(list(semantic_type_confirmed))=}")
    return semantic_type_confirmed


def check_if_chapter_str_funcs_is_sorted(chapter_str_funcs: list[str]):
    if chapter_str_funcs != sorted(chapter_str_funcs):
        for chapter_str_func in sorted(chapter_str_funcs):
            chapter_str_func = chapter_str_func.replace("'", "")
            chapter_str_func = chapter_str_func.replace("_str", "")
    sorted_chapter_str_funcs = sorted(chapter_str_funcs)
    if chapter_str_funcs != sorted_chapter_str_funcs:
        first_wrong_index = None
        for x in range(len(chapter_str_funcs)):
            # print(f"{chapter_str_funcs[x]}")
            if (
                not first_wrong_index
                and chapter_str_funcs[x] != sorted_chapter_str_funcs[x]
            ):
                first_wrong_index = (
                    f"{chapter_str_funcs[x]} should be {sorted_chapter_str_funcs[x]}"
                )

        # print(f"{first_wrong_index=}")
        # print(f"Bad Order     {chapter_str_funcs}")
        # print(f"Correct order {sorted(chapter_str_funcs)}")
    assert chapter_str_funcs == sorted(chapter_str_funcs)


def check_str_funcs_are_not_duplicated(
    chapter_str_funcs: list[str], running_str_functions_set: set[str]
):
    if set(chapter_str_funcs) & (set(running_str_functions_set)):
        print(
            f"Duplicate functions: {set(chapter_str_funcs) & (set(running_str_functions_set))}"
        )
    assert not set(chapter_str_funcs) & (set(running_str_functions_set))


def check_import_objs_are_ordered(test_file_imports: list[list], file_path: str):
    for file_import in test_file_imports:
        file_import_src = file_import[0]
        file_import_objs = file_import[1]
        if file_import_objs != sorted(file_import_objs):
            print(f"{file_path=}")
            file_import_objs_str = str(sorted(file_import_objs))
            file_import_objs_str = file_import_objs_str.replace("'", "")
            file_import_objs_str = file_import_objs_str.replace("[", "")
            file_import_objs_str = file_import_objs_str.replace("]", "")
            print(f"from {file_import_src} import ({file_import_objs_str})")
        assert file_import_objs == sorted(file_import_objs)


def check_str_func_test_file_has_needed_asserts(
    chapter_str_funcs, test_file_path, util_dir, desc_number_str
):
    for str_function in chapter_str_funcs:
        # print(f"{str_util_path} {str_function=}")
        assert str(str_function).endswith("_str")
        str_func_assert_str = f"""assert {str_function}() == "{str_function[:-4]}"""
        test_file_str = open(test_file_path).read()
        if test_file_str.find(str_func_assert_str) <= 0:
            str_util_path = create_path(util_dir, f"a{desc_number_str}_keywords.py")
            print(f"{str_util_path} {str_func_assert_str=}")
        assert test_file_str.find(str_func_assert_str) > 0


def get_docstring(file_path: str, function_name: str) -> str:
    with open(file_path, "r") as f:
        tree = ast_parse(f.read(), filename=file_path)

    return next(
        (
            ast_get_docstring(node)
            for node in ast_walk(tree)
            if isinstance(node, ast_FunctionDef) and node.name == function_name
        ),
        None,
    )


def check_if_test_ReturnsObj_pytests_exist(
    path_funcs: set, chapter_desc: str, test_path_func_names: set[str]
):
    for path_func in path_funcs:
        pytest_for_func_exists = False
        # print(f"{chapter_desc} {path_func}")
        expected_test_func = f"test_{path_func}_ReturnsObj"
        for test_path_func_name in test_path_func_names:
            if test_path_func_name.startswith(expected_test_func):
                pytest_for_func_exists = True
            # print(
            #     f"{pytest_for_func_exists} {chapter_desc} {path_func} {test_path_func_name}"
            # )
        assert pytest_for_func_exists, f"missing {expected_test_func=}"
        # print(f"{chapter_desc} {test_func_exists} {path_func}")


def check_if_test_HasDocString_pytests_exist(
    path_funcs: set, chapter_desc: str, test_path_func_names: set[str]
):
    for path_func in path_funcs:
        pytest_for_func_exists = False
        # print(f"{chapter_desc} {path_func}")
        expected_test_func = f"test_{path_func}_HasDocString"
        for test_path_func_name in test_path_func_names:
            if test_path_func_name.startswith(expected_test_func):
                pytest_for_func_exists = True
            # print(
            #     f"{pytest_for_func_exists} {chapter_desc} {path_func} {test_path_func_name}"
            # )
        assert pytest_for_func_exists, f"missing {expected_test_func=}"
        # print(f"{chapter_desc} {test_func_exists} {path_func}")


def check_all_test_functions_have_proper_naming_format(all_test_function_names: set):
    for test_function_name in sorted(list(all_test_function_names)):
        test_function_name = str(test_function_name)
        failed_assertion_str = f"test function {test_function_name} is not named well"
        if test_function_name.lower().endswith("_exists"):
            assert test_function_name.endswith("_Exists"), failed_assertion_str
        if test_function_name.lower().find("returnsobj") > 0:
            assert test_function_name.find("ReturnsObj") > 0, failed_assertion_str
        assert test_function_name.lower().find("correctly") <= 0, failed_assertion_str
        assert test_function_name.lower().find("returnobj") <= 0, failed_assertion_str


def check_all_test_functions_are_formatted(
    all_test_functions: dict[str, str],
):
    for test_function_str in all_test_functions.values():
        establish_str_exists = test_function_str.find("ESTABLISH") > -1
        when_str_exists = test_function_str.find("WHEN") > -1
        then_str_exists = test_function_str.find("THEN") > -1
        assert (
            establish_str_exists and when_str_exists and then_str_exists
        ), f"'ESTABLISH'/'WHEN'/'THEN' missing from {test_function_str[:300]}"


def get_max_chapter_import_str() -> str:
    max_chapter_int = 0
    for chapter_desc in get_chapter_descs():
        chapter_desc_str_number = get_chapter_desc_str_number(chapter_desc)
        max_chapter_int = max(int(chapter_desc_str_number), max_chapter_int)

    max_chapter_dir = ""
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_desc_str_number = get_chapter_desc_str_number(chapter_desc)
        if int(chapter_desc_str_number) == max_chapter_int:
            max_chapter_dir = chapter_dir
    max_chapter_int_str = str(max_chapter_int)
    max_chapter_import_str = max_chapter_dir.replace("\\", ".")
    max_chapter_import_str = max_chapter_import_str.replace("""src/""", """src.""")
    max_chapter_import_str = (
        f"{max_chapter_import_str}._ref.ch{max_chapter_int_str}_keywords"
    )
    return max_chapter_import_str


_CH_PATTERN = re_compile(r"^src\.ch(\d+)(?:[._]|$)")
_CH_STR_PATTERN = re_compile(r"ch(\d{2})_str(?:[._]|$)")


def _extract_series_number(chapter: str) -> int | None:
    if not chapter:
        return None
    m = _CH_PATTERN.match(chapter)
    return int(m.group(1)) if m else None


def _extract_aXX_str_number(chapter: str) -> int | None:
    if not chapter:
        return None
    m = _CH_STR_PATTERN.search(chapter)
    return int(m.group(1)) if m else None


class _ImportCollector(ast_NodeVisitor):
    def __init__(self, min_number: int):
        self.min_number = min_number
        self.matches: list[str] = []

    def visit_Import(self, node: ast_Import):
        for alias in node.names:
            chapter = alias.name
            # Check src.aXX
            n = _extract_series_number(chapter)
            if n is not None and n > self.min_number:
                s = f"import {chapter}"
                if alias.asname:
                    s += f" as {alias.asname}"
                self.matches.append(s)
            # Check aXX_str
            n2 = _extract_aXX_str_number(chapter)
            if n2 is not None and n2 != self.min_number:
                s = f"import {chapter}"
                if alias.asname:
                    s += f" as {alias.asname}"
                self.matches.append(s)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast_ImportFrom):
        chapter = node.module
        # Check src.aXX
        n = _extract_series_number(chapter) if chapter else None
        if n is not None and n > self.min_number:
            parts = [
                f"{a.name} as {a.asname}" if a.asname else a.name for a in node.names
            ]
            self.matches.append(f"from {chapter} import {', '.join(parts)}")
        # Check aXX_str
        n2 = _extract_aXX_str_number(chapter) if chapter else None
        if n2 is not None and n2 != self.min_number:
            parts = [
                f"{a.name} as {a.asname}" if a.asname else a.name for a in node.names
            ]
            self.matches.append(f"from {chapter} import {', '.join(parts)}")
        self.generic_visit(node)


def find_incorrect_imports(
    py_file_path: str | pathlib_Path, min_number: int
) -> list[str]:
    p = pathlib_Path(py_file_path)
    src = p.read_text(encoding="utf-8")
    tree = ast_parse(src, filename=str(p))
    collector = _ImportCollector(min_number)
    collector.visit(tree)
    return collector.matches
