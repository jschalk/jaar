from src.ch01_py.file_toolbox import create_path, get_level1_dirs


def get_chapter_descs() -> dict[str, str]:
    """Returns chapter_desc, chapter_dir for all Chapters"""
    src_dir = "src"
    chapter_descs = get_level1_dirs(src_dir)
    """linter is not evaluated"""
    chapter_descs.remove("linter")
    chapter_descs.remove("ref")
    return {
        chapter_desc: create_path(src_dir, chapter_desc)
        for chapter_desc in chapter_descs
    }


def get_chapter_desc_prefix(chapter_desc: str) -> str:
    # sourcery skip: str-prefix-suffix
    """Returns chapter number in 2 character string."""
    if chapter_desc[:2] == "ch":
        return chapter_desc[:4]
