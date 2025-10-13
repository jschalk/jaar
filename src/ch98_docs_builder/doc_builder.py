from ast import (
    ClassDef as ast_ClassDef,
    FunctionDef as ast_FunctionDef,
    Name as ast_Name,
    parse as ast_parse,
    walk as ast_walk,
)
from copy import copy as copy_copy
from enum import Enum
from src.ch01_py.file_toolbox import create_path, get_level1_dirs, open_json, save_file
from src.ch02_rope._ref.ch02_doc_builder import get_ropeterm_explanation_md
from src.ch17_idea._ref.ch17_doc_builder import get_brick_formats_md, get_idea_brick_mds


def get_keywords_src_config() -> dict[str, dict]:
    return open_json("src/ch98_docs_builder/keywords.json")


def get_keywords_by_chapter(keywords_dict: dict[str, dict[str]]) -> dict:
    chapters_keywords = {
        get_chapter_desc_prefix(chxx): set() for chxx in get_chapter_descs().keys()
    }
    for x_keyword, ref_dict in keywords_dict.items():
        keyworld_init_chapter_num = ref_dict.get("init_chapter")
        chapter_set = chapters_keywords.get(keyworld_init_chapter_num)
        chapter_set.add(x_keyword)
    return chapters_keywords


def get_cumlative_ch_keywords_dict(keywords_by_chapter: dict[int, set[str]]) -> dict:
    allowed_keywords_set = set()
    cumlative_ch_keywords_dict = {}
    for chapter_num in sorted(list(keywords_by_chapter.keys())):
        ch_keywords_set = keywords_by_chapter.get(chapter_num)
        allowed_keywords_set.update(ch_keywords_set)
        cumlative_ch_keywords_dict[chapter_num] = copy_copy(allowed_keywords_set)
    return cumlative_ch_keywords_dict


def get_chXX_keyword_classes(cumlative_ch_keywords_dict: dict) -> dict[int,]:
    chXX_keyword_classes = {}
    word_str = "word"
    for chapter_prefix in sorted(list(cumlative_ch_keywords_dict.keys())):
        ch_keywords = cumlative_ch_keywords_dict.get(chapter_prefix)
        class_name = f"C{chapter_prefix[1:]}Key{word_str}s"
        ExpectedClass = Enum(class_name, {t: t for t in ch_keywords}, type=str)
        chXX_keyword_classes[chapter_prefix] = ExpectedClass
    return chXX_keyword_classes


def get_chapter_descs() -> dict[str, str]:
    """Returns chapter_desc, chapter_dir for all Chapters"""
    src_dir = "src"
    chapter_descs = get_level1_dirs(src_dir)
    """ch99_chapter_style is not evaluated"""
    chapter_descs.remove("ch99_chapter_style")
    chapter_descs.remove("ref")
    return {
        chapter_desc: create_path(src_dir, chapter_desc)
        for chapter_desc in chapter_descs
    }


def get_chapter_num_descs() -> dict[int, str]:
    """Returns dict [Chapter_num as Int, chapter_desc]"""
    chapter_descs = get_chapter_descs()
    chapter_prefix_descs = {}
    for chapter_desc in chapter_descs:
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        chapter_prefix_descs[chapter_prefix] = chapter_desc
    return chapter_prefix_descs


def get_function_names_from_file(
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


def get_chapter_desc_prefix(chapter_desc: str) -> str:
    """Returns chapter number in 2 character string."""
    if chapter_desc.startswith("a"):
        return chapter_desc[:3]
    elif chapter_desc.startswith("ch"):
        return chapter_desc[:4]


def get_keywords_by_chapter_md() -> str:
    words_str = "words"
    keywords_title_str = f"Key{words_str} by Chapter"
    func_lines = [f"## {keywords_title_str}"]
    keywords_src_config = get_keywords_src_config()
    keywords_by_chapter = get_keywords_by_chapter(keywords_src_config)
    for chapter_desc in get_chapter_descs().keys():
        chapter_prefix = get_chapter_desc_prefix(chapter_desc)
        chapter_keywords = keywords_by_chapter.get(chapter_prefix)
        chapter_keywords = sorted(list(chapter_keywords))
        _line = f"- {chapter_desc}: " + ", ".join(chapter_keywords)
        func_lines.append(_line)
    return f"# {keywords_title_str}\n\n" + "\n".join(func_lines)


def save_keywords_by_chapter_md(x_dir: str):
    keywords_by_chapter_md_path = create_path(x_dir, "keywords_by_chapter.md")
    save_file(keywords_by_chapter_md_path, None, get_keywords_by_chapter_md())


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
