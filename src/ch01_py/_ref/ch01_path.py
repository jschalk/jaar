from src.ch01_py.file_toolbox import create_path


def create_src_keywords_path(src_dir: str) -> str:
    """Returns path: src\\ref\\keywords.json"""

    ref_dir = create_path(src_dir, "ref")
    return create_path(ref_dir, "keywords.json")


def create_keywords_classes_file_path(src_dir: str) -> str:
    """Returns path: src\\ref\\keywords.py"""

    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "ref")
    return create_path(ref_dir, "keywords.py")
