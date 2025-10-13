from src.ch01_py.file_toolbox import create_path


def get_keywords_filename(chapter_desc_prefix: str) -> str:
    return f"{chapter_desc_prefix}_keywords.py"


def create_keywords_class_file_path(chapter_dir: str, chapter_prefix: str) -> str:
    """Returns path: src\\ref\\chXX_keywords.py"""

    # ref_dir = create_path(chapter_dir, "_ref")
    keywords_filename = get_keywords_filename(chapter_prefix)
    return create_path(chapter_dir, keywords_filename)


def create_keywords_classes_file_path() -> str:
    """Returns path: src\\ref\\keywords.py"""

    # ref_dir = create_path(chapter_dir, "_ref")
    return create_path("src\\ref", "keywords.py")
