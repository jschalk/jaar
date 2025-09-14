# your_module.py
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
from src.a00_data_toolbox.file_toolbox import create_path, get_dir_filenames
from src.a98_docs_builder.doc_builder import (
    get_function_names_from_file,
    get_module_descs,
)
from textwrap import dedent as textwrap_dedent
from typing import List


def get_imports_from_file(file_path):
    """
    Parses a Python file and returns a list of lists.
    Each inner list contains:
    - The source module from a 'from ... import ...' statement
    - Followed by all imported objects from that module

    Example:
    [['math', 'sqrt', 'pi'], ['os.path', 'join']]

    :param file_path: Path to the Python (.py) file
    :return: List of lists: [module, imported_obj1, imported_obj2, ...]
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


def check_module_imports_are_ordered(imports: list[list], file_path: str, desc_number):
    previous_module_number = -1
    previous_module_str = "a"
    module_section_passed = False
    for x_import in imports:
        module_location = str(x_import[0])
        if module_location.startswith("src"):
            module_number = int(module_location[5:7])
            if desc_number < module_number:
                print(f"{desc_number} {file_path} {module_number=} {module_location=}")
            assert desc_number >= module_number
            assert module_section_passed is False
            if module_number < previous_module_number:
                print(
                    f"{file_path} {module_number=} {previous_module_number=} {x_import=}"
                )
            assert module_number >= previous_module_number
            previous_module_number = module_number
        else:
            module_section_passed = True
            if module_location <= previous_module_str:
                print(f"{file_path} switch {module_location} and {previous_module_str}")
            assert module_location > previous_module_str
            previous_module_str = module_location

        if module_location.endswith("env"):
            env_number = int(module_location[-6:-4])
            if desc_number != env_number:
                print(f"{desc_number} {file_path} {env_number=} {module_location=}")
            assert desc_number == env_number


def get_all_str_functions() -> list:
    all_str_functions = []
    for module_desc, module_dir in get_module_descs().items():
        desc_number_str = module_desc[1:3]
        ref_dir = create_path(module_dir, "_ref")
        str_util_path = create_path(ref_dir, f"a{desc_number_str}_terms.py")
        str_functions = get_function_names_from_file(str_util_path)
        if len(str_functions) > 0:
            str_functions = get_function_names_from_file(str_util_path)
            all_str_functions.extend(iter(str_functions))
    return all_str_functions


def get_duplicated_functions(excluded_functions) -> set[str]:
    x_count = 0
    duplicate_functions = set()
    all_functions = set()
    for module_desc, module_dir in get_module_descs().items():
        filenames_set = get_dir_filenames(module_dir, include_extensions={"py"})
        for filenames in filenames_set:
            file_dir = create_path(module_dir, filenames[0])
            file_path = create_path(file_dir, filenames[1])
            file_functions = get_function_names_from_file(file_path)
            for function_name in file_functions:
                x_count += 1
                if function_name in all_functions:
                    print(
                        f"Function #{x_count}: Duplicate function {function_name} in {file_path}"
                    )
                    duplicate_functions.add(function_name)
                if function_name not in excluded_functions:
                    all_functions.add(function_name)
    print(f"{duplicate_functions=}")
    print(f"{len(all_functions)=}")
    return duplicate_functions


def check_if_module_str_funcs_is_sorted(module_str_funcs: list[str]):
    if module_str_funcs != sorted(module_str_funcs):
        for module_str_func in sorted(module_str_funcs):
            module_str_func = module_str_func.replace("'", "")
            module_str_func = module_str_func.replace("_str", "")
    sorted_module_str_funcs = sorted(module_str_funcs)
    if module_str_funcs != sorted_module_str_funcs:
        first_wrong_index = None
        for x in range(len(module_str_funcs)):
            # print(f"{module_str_funcs[x]}")
            if (
                not first_wrong_index
                and module_str_funcs[x] != sorted_module_str_funcs[x]
            ):
                first_wrong_index = (
                    f"{module_str_funcs[x]} should be {sorted_module_str_funcs[x]}"
                )

        # print(f"{first_wrong_index=}")
        # print(f"Bad Order     {module_str_funcs}")
        # print(f"Correct order {sorted(module_str_funcs)}")
    assert module_str_funcs == sorted(module_str_funcs)


def check_str_funcs_are_not_duplicated(
    module_str_funcs: list[str], running_str_functions_set: set[str]
):
    if set(module_str_funcs).intersection(set(running_str_functions_set)):
        print(
            f"Duplicate functions: {set(module_str_funcs).intersection(set(running_str_functions_set))}"
        )
    assert not set(module_str_funcs).intersection(set(running_str_functions_set))


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
    module_str_funcs, test_file_path, util_dir, desc_number_str
):
    for str_function in module_str_funcs:
        # print(f"{str_util_path} {str_function=}")
        assert str(str_function).endswith("_str")
        str_func_assert_str = f"""assert {str_function}() == "{str_function[:-4]}"""
        test_file_str = open(test_file_path).read()
        if test_file_str.find(str_func_assert_str) <= 0:
            str_util_path = create_path(util_dir, f"a{desc_number_str}_terms.py")
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
        # print(f"{module_desc} {path_func}")
        expected_test_func = f"test_{path_func}_HasDocString"
        for test_path_func_name in test_path_func_names:
            if test_path_func_name.startswith(expected_test_func):
                pytest_for_func_exists = True
            # print(
            #     f"{pytest_for_func_exists} {module_desc} {path_func} {test_path_func_name}"
            # )
        assert pytest_for_func_exists, f"missing {expected_test_func=}"
        # print(f"{module_desc} {test_func_exists} {path_func}")


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


def get_max_module_import_str() -> str:
    max_module_int = 0
    for module_desc in get_module_descs():
        max_module_int = max(int(module_desc[1:3]), max_module_int)

    max_module_dir = ""
    for module_desc, module_dir in get_module_descs().items():
        if int(module_desc[1:3]) == max_module_int:
            max_module_dir = module_dir
    max_module_int_str = str(max_module_int)
    max_module_import_str = max_module_dir.replace("\\", ".")
    max_module_import_str = max_module_import_str.replace("""src/""", """src.""")
    max_module_import_str = f"{max_module_import_str}._ref.a{max_module_int_str}_terms"
    return max_module_import_str


_A_PATTERN = re_compile(r"^src\.a(\d+)(?:[._]|$)")
_A_STR_PATTERN = re_compile(r"a(\d{2})_str(?:[._]|$)")


def _extract_series_number(module: str) -> int | None:
    if not module:
        return None
    m = _A_PATTERN.match(module)
    return int(m.group(1)) if m else None


def _extract_aXX_str_number(module: str) -> int | None:
    if not module:
        return None
    m = _A_STR_PATTERN.search(module)
    return int(m.group(1)) if m else None


class _ImportCollector(ast_NodeVisitor):
    def __init__(self, min_number: int):
        self.min_number = min_number
        self.matches: list[str] = []

    def visit_Import(self, node: ast_Import):
        for alias in node.names:
            module = alias.name
            # Check src.aXX
            n = _extract_series_number(module)
            if n is not None and n > self.min_number:
                s = f"import {module}"
                if alias.asname:
                    s += f" as {alias.asname}"
                self.matches.append(s)
            # Check aXX_str
            n2 = _extract_aXX_str_number(module)
            if n2 is not None and n2 != self.min_number:
                s = f"import {module}"
                if alias.asname:
                    s += f" as {alias.asname}"
                self.matches.append(s)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast_ImportFrom):
        module = node.module
        # Check src.aXX
        n = _extract_series_number(module) if module else None
        if n is not None and n > self.min_number:
            parts = [
                f"{a.name} as {a.asname}" if a.asname else a.name for a in node.names
            ]
            self.matches.append(f"from {module} import {', '.join(parts)}")
        # Check aXX_str
        n2 = _extract_aXX_str_number(module) if module else None
        if n2 is not None and n2 != self.min_number:
            parts = [
                f"{a.name} as {a.asname}" if a.asname else a.name for a in node.names
            ]
            self.matches.append(f"from {module} import {', '.join(parts)}")
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
