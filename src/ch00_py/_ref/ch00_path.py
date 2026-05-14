from ch00_py.file_toolbox import create_path


def create_src_example_strs_path(src_dir: str) -> str:
    """Returns path: src\\ch99_ref\\example_strs.json"""

    ref_dir = create_path(src_dir, "ch99_ref")
    return create_path(ref_dir, "example_strs.json")


def create_src_keywords_main_path(src_dir: str) -> str:
    """Returns path: src\\ch99_ref\\keywords_main.json"""

    ref_dir = create_path(src_dir, "ch99_ref")
    return create_path(ref_dir, "keywords_main.json")


def create_keywords_classes_file_path(src_dir: str) -> str:
    """Returns path: src\\ch99_ref\\keywords.py"""

    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "ch99_ref")
    return create_path(ref_dir, "keywords.py")
