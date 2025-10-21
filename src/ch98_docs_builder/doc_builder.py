from ast import (
    ClassDef as ast_ClassDef,
    FunctionDef as ast_FunctionDef,
    Name as ast_Name,
    parse as ast_parse,
    walk as ast_walk,
)
from src.ch01_py.chapter_desc_tools import get_chapter_desc_prefix, get_chapter_descs
from src.ch01_py.file_toolbox import create_path, open_json, save_file
from src.ch04_rope._ref.ch04_doc_builder import get_ropeterm_explanation_md
from src.ch17_idea._ref.ch17_doc_builder import get_brick_formats_md, get_idea_brick_mds


def get_chapter_num_descs() -> dict[int, str]:
    """Returns dict [Chapter_num as Int, chapter_desc]"""
    chapter_descs = get_chapter_descs()
    chapter_prefix_descs = {}
    for chapter_desc in chapter_descs:
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        chapter_prefix_descs[chapter_prefix] = chapter_desc
    return chapter_prefix_descs


def get_func_names_and_class_bases_from_file(
    file_path: str, suffix: str = None
) -> tuple[list, dict[str, bool]]:
    """
    Parses a Python file and returns a list of all top-level function names.

    :param file_path: Path to the .py file
    :return: List of function names, dict key: Class Name, value: list of class bases
    """

    with open(file_path, "r", encoding="utf-8") as file:
        node = ast_parse(file.read(), filename=file_path)
    file_funcs = []
    class_bases = {}
    for n in ast_walk(node):
        if isinstance(n, ast_FunctionDef):
            file_funcs.append(n.name)
        if isinstance(n, ast_ClassDef):
            bases = [b.id for b in n.bases if isinstance(b, ast_Name)]
            class_bases[n.name] = bases
    return file_funcs, class_bases


def get_chapter_desc_str_number(chapter_desc: str) -> str:
    """Returns chapter number in 2 character string."""
    if chapter_desc.startswith("a"):
        return chapter_desc[1:3]
    elif chapter_desc.startswith("ch"):
        return chapter_desc[2:4]


def get_chapter_blurbs_md() -> str:
    lines = ["# Chapter Overview\n", "What does each one do?\n", ""]
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
