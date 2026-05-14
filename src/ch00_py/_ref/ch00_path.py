from ch00_py.file_toolbox import create_path


def create_src_example_strs_path(src_dir: str) -> str:
    """Returns path: src\\ch99_glossary\\example_strs.json"""

    ref_dir = create_path(src_dir, "ch99_glossary")
    return create_path(ref_dir, "example_strs.json")


def create_src_keywords_src_path(src_dir: str) -> str:
    """Returns path: src\\ch99_glossary\\keywords_src.json"""

    ref_dir = create_path(src_dir, "ch99_glossary")
    return create_path(ref_dir, "keywords_src.json")


def create_keywords_classes_file_path(src_dir: str) -> str:
    """Returns path: src\\ch99_glossary\\keywords.py"""

    # ref_dir = create_path(chapter_dir, "_ref")
    ref_dir = create_path(src_dir, "ch99_glossary")
    return create_path(ref_dir, "keywords.py")
