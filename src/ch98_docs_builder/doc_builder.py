from ast import FunctionDef as ast_FunctionDef, parse as ast_parse, walk as ast_walk
from pathlib import Path
from src.ch01_data_toolbox.file_toolbox import (
    create_path,
    get_level1_dirs,
    open_json,
    save_file,
)
from src.ch02_rope_logic._ref.ch02_doc_builder import get_ropeterm_explanation_md
from src.ch17_idea_logic._ref.ch17_doc_builder import (
    get_brick_formats_md,
    get_idea_brick_mds,
)


def get_chapter_descs() -> dict[str, str]:
    src_dir = "src"
    chapter_descs = get_level1_dirs(src_dir)
    chapter_descs.remove("ch99_chapter_linter")
    return {
        chapter_desc: create_path(src_dir, chapter_desc)
        for chapter_desc in chapter_descs
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


def get_chapter_str_functions(chapter_dir: str, chapter_desc_prefix: str) -> list[str]:
    ref_dir = create_path(chapter_dir, "_ref")
    str_util_path = create_path(ref_dir, f"{chapter_desc_prefix}_keywords.py")
    return get_function_names_from_file(str_util_path)


def get_chapter_desc_str_number(chapter_desc: str) -> str:
    """Returns chapter number in 2 character string."""
    if chapter_desc.startswith("a"):
        return chapter_desc[1:3]
    elif chapter_desc.startswith("ch"):
        return chapter_desc[2:4]


def get_chapter_desc_prefix(chapter_desc: str) -> str:
    """Returns chapter number in 2 character string."""
    if chapter_desc.startswith("a"):
        return chapter_desc[:3]
    elif chapter_desc.startswith("ch"):
        return chapter_desc[:4]


def get_str_funcs_md() -> str:
    func_lines = ["## Str Functions by Chapter"]
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        chapter_str_funcs = get_chapter_str_functions(chapter_dir, chapter_prefix)
        x_list = [str_func[:-4] for str_func in chapter_str_funcs]
        _line = f"- {chapter_desc}: " + ", ".join(x_list)
        func_lines.append(_line)
    return "# String Functions by Chapterr\n\n" + "\n".join(func_lines)


def save_str_funcs_md(x_dir: str):
    str_funcs_md_path = create_path(x_dir, "str_funcs.md")
    save_file(str_funcs_md_path, None, get_str_funcs_md())


def get_chapter_blurbs_md() -> str:
    lines = ["# Chapterr Overview\n", "What does each one do?\n", ""]
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        docs_dir = create_path(chapter_dir, "_ref")
        chapter_ref_path = create_path(docs_dir, f"{chapter_prefix}_ref.json")
        chapter_ref_dict = open_json(chapter_ref_path)
        chapter_description_str = "chapter_description"
        chapter_blurb_str = "chapter_blurb"
        mod_blurb = chapter_ref_dict.get(chapter_blurb_str)
        ref_chapter_desc = chapter_ref_dict.get(chapter_description_str)

        lines.append(f"- **{ref_chapter_desc}**: {mod_blurb}")

    return "\n".join(lines)


def save_chapter_blurbs_md(x_dir: str):
    save_file(x_dir, "chapter_blurbs.md", get_chapter_blurbs_md())


def save_ropeterm_explanation_md(x_dir: str):
    save_file(x_dir, "ropeterm_explanation.md", get_ropeterm_explanation_md())


def save_idea_brick_mds(dest_dir: str):
    idea_brick_mds = get_idea_brick_mds()
    dest_dir = create_path(dest_dir, "ch17_idea_brick_formats")

    for idea_number, idea_brick_md in idea_brick_mds.items():
        save_file(dest_dir, f"{idea_number}.md", idea_brick_md)


def save_brick_formats_md(dest_dir: str):
    brick_formats_md = get_brick_formats_md()
    save_file(dest_dir, "idea_brick_formats.md", brick_formats_md)
