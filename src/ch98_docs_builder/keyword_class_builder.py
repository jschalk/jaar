from src.ch98_docs_builder.doc_builder import (
    get_chapter_desc_prefix,
    get_chapter_descs,
    get_cumlative_ch_keywords_dict,
    get_keywords_by_chapter,
    get_keywords_src_config,
)


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
    return f"""

class {chXX_str}{key_str}words(str, Enum):{keywords_str}
{dunder_str_func_str}"""


def create_all_enum_keyword_classes_str() -> str:
    keywords_by_chapter = get_keywords_by_chapter(get_keywords_src_config())
    cumlative_keywords = get_cumlative_ch_keywords_dict(keywords_by_chapter)
    classes_str = "from enum import Enum"
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        ch_prefix = get_chapter_desc_prefix(chapter_desc)
        ch_keywords = cumlative_keywords.get(ch_prefix)
        enum_class_str = create_keywords_enum_class_file_str(ch_prefix, ch_keywords)
        classes_str += enum_class_str
    return classes_str
