from ast import FunctionDef as ast_FunctionDef, parse as ast_parse, walk as ast_walk
from pathlib import Path
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    get_level1_dirs,
    open_json,
    save_file,
)
from src.a01_rope_logic._ref.a01_doc_builder import get_ropepointer_explanation_md
from src.a17_idea_logic._ref.a17_doc_builder import (
    get_brick_formats_md,
    get_idea_brick_mds,
)


def get_module_descs() -> dict[str, str]:
    src_dir = "src"
    module_descs = get_level1_dirs(src_dir)
    module_descs.remove("ch99_module_linter")
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


def get_module_str_functions(module_dir: str, module_desc_prefix: str) -> list[str]:
    ref_dir = create_path(module_dir, "_ref")
    str_util_path = create_path(ref_dir, f"{module_desc_prefix}_terms.py")
    return get_function_names_from_file(str_util_path)


def get_module_desc_str_number(module_desc: str) -> str:
    """Returns module number in 2 character string."""
    if module_desc.startswith("a"):
        return module_desc[1:3]
    elif module_desc.startswith("ch"):
        return module_desc[2:4]


def get_module_desc_prefix(module_desc: str) -> str:
    """Returns module number in 2 character string."""
    if module_desc.startswith("a"):
        return module_desc[:3]
    elif module_desc.startswith("ch"):
        return module_desc[:4]


def get_str_funcs_md() -> str:
    func_lines = ["## Str Functions by Module"]
    for module_desc, module_dir in get_module_descs().items():
        module_prefix = get_module_desc_prefix(module_desc)
        module_str_funcs = get_module_str_functions(module_dir, module_prefix)
        x_list = [str_func[:-4] for str_func in module_str_funcs]
        _line = f"- {module_desc}: " + ", ".join(x_list)
        func_lines.append(_line)
    return "# String Functions by Module\n\n" + "\n".join(func_lines)


def save_str_funcs_md(x_dir: str):
    str_funcs_md_path = create_path(x_dir, "str_funcs.md")
    save_file(str_funcs_md_path, None, get_str_funcs_md())


def get_module_blurbs_md() -> str:
    lines = ["# Module Overview\n", "What does each one do?\n", ""]
    for module_desc, module_dir in get_module_descs().items():
        module_prefix = get_module_desc_prefix(module_desc)
        docs_dir = create_path(module_dir, "_ref")
        module_ref_path = create_path(docs_dir, f"{module_prefix}_ref.json")
        module_ref_dict = open_json(module_ref_path)
        module_description_str = "module_description"
        module_blurb_str = "module_blurb"
        mod_blurb = module_ref_dict.get(module_blurb_str)
        ref_module_desc = module_ref_dict.get(module_description_str)

        lines.append(f"- **{ref_module_desc}**: {mod_blurb}")

    return "\n".join(lines)


def save_module_blurbs_md(x_dir: str):
    save_file(x_dir, "module_blurbs.md", get_module_blurbs_md())


def save_ropepointer_explanation_md(x_dir: str):
    save_file(x_dir, "ropepointer_explanation.md", get_ropepointer_explanation_md())


def save_idea_brick_mds(dest_dir: str):
    idea_brick_mds = get_idea_brick_mds()
    dest_dir = create_path(dest_dir, "a17_idea_brick_formats")

    for idea_number, idea_brick_md in idea_brick_mds.items():
        save_file(dest_dir, f"{idea_number}.md", idea_brick_md)


def save_brick_formats_md(dest_dir: str):
    brick_formats_md = get_brick_formats_md()
    save_file(dest_dir, "idea_brick_formats.md", brick_formats_md)
