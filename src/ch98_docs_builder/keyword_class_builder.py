from src.ch01_py.file_toolbox import save_file
from src.ch98_docs_builder._ref.ch98_path import create_keywords_class_file_path


def create_keywords_enum_class_file_str(chapter_prefix: str, keywords_set: set) -> str:
    keywords_str = ""
    if not keywords_set:
        keywords_str += "\n    pass"
    else:
        for keyword_str in sorted(keywords_set):
            keywords_str += f'\n    {keyword_str} = "{keyword_str}"'

    chXX_str = f"{chapter_prefix.upper()[:1]}{chapter_prefix.lower()[1:]}"
    key_str = "Key"
    dunder_str_func_str = """
    def __str__(self):
        return self.value
"""
    return f"""from enum import Enum


class {chXX_str}{key_str}words(str, Enum):{keywords_str}
{dunder_str_func_str}"""


def save_keywords_enum_class_file(
    chapter_dir: str, chapter_prefix: int, keywords_set: set
):
    file_path = create_keywords_class_file_path(chapter_dir, chapter_prefix)
    file_str = create_keywords_enum_class_file_str(chapter_prefix, keywords_set)
    save_file(file_path, None, file_str)
