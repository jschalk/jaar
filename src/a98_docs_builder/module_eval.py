from ast import FunctionDef as ast_FunctionDef, parse as ast_parse, walk as ast_walk
from src.a00_data_toolbox.file_toolbox import create_path, get_level1_dirs, save_file


def get_module_descs() -> dict[str, str]:
    src_dir = "src"
    module_descs = get_level1_dirs(src_dir)
    module_descs.remove("a99_module_linter")
    return {
        module_desc: create_path(src_dir, module_desc) for module_desc in module_descs
    }


def get_function_names_from_file(file_path: str, suffix: str = None) -> list:
    """
    Parses a Python file and returns a list of all top-level function names.

    :param file_path: Path to the .py file
    :return: List of function names
    """

    with open(file_path, "r", encoding="utf-8") as file:
        node = ast_parse(file.read(), filename=file_path)
    return [n.name for n in ast_walk(node) if isinstance(n, ast_FunctionDef)]


def get_module_str_functions(module_dir, desc_number_str) -> list[str]:
    test_dir = create_path(module_dir, "test")
    util_dir = create_path(test_dir, "_util")
    str_util_path = create_path(util_dir, f"a{desc_number_str}_str.py")
    return get_function_names_from_file(str_util_path)


def get_str_funcs_md() -> str:
    func_lines = ["## Str Functions by Module"]
    for module_desc, module_dir in get_module_descs().items():
        desc_number_str = module_desc[1:3]
        module_str_funcs = get_module_str_functions(module_dir, desc_number_str)
        x_list = [str_func[:-4] for str_func in module_str_funcs]
        _line = f"- {module_desc}: " + ", ".join(x_list)
        func_lines.append(_line)
    return "# String Functions by Module\n\n" + "\n".join(func_lines)


def save_str_funcs_md(x_dir: str):
    str_funcs_md_path = create_path(x_dir, "str_funcs.md")
    save_file(str_funcs_md_path, None, get_str_funcs_md())
