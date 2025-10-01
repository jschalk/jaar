from src.ch01_data_toolbox.file_toolbox import create_path


def get_keywords_filename(chapter_desc_prefix: str) -> str:
    return f"{chapter_desc_prefix}_keywords.py"


def create_keywords_class_file_path(chapter_dir: str, ch_num: int) -> str:
    """Returns path: chapter_dir\\_ref\\chXX_keywords.py"""

    ref_dir = create_path(chapter_dir, "_ref")
    keywords_filename = get_keywords_filename(f"ch{ch_num:02}")
    return create_path(ref_dir, keywords_filename)
