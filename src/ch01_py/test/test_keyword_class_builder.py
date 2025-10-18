from src.ch01_py.file_toolbox import open_file, save_file
from src.ch01_py.keyword_class_builder import (
    create_all_enum_keyword_classes_str,
    create_keywords_enum_class_file_str,
    get_keywords_src_config,
)
from src.ch01_py._ref.ch01_path import create_keywords_classes_file_path


def test_get_keywords_src_config_ReturnsObj():
    # ESTABLISH / WHEN
    keywords_config = get_keywords_src_config()

    # THEN
    assert keywords_config
    for keyword, ref_dict in keywords_config.items():
        assert set(ref_dict.keys()) == {"init_chapter"}
        print(f"{keyword=} {ref_dict=}")


def test_create_keywords_enum_class_file_str_ReturnsObj_Scenario0_Empty_keyword_set():
    # ESTABLISH
    ch04_str = "ch04"
    ch04_keywords = {}

    # WHEN
    file_str = create_keywords_enum_class_file_str(ch04_str, ch04_keywords)

    # THEN
    assert file_str
    key_str = "Key"
    expected_file_str = f"""

class Ch04{key_str}words(str, Enum):
    pass

    def __str__(self):
        return self.value
"""
    print(file_str)
    print(expected_file_str)
    assert file_str == expected_file_str


def test_create_keywords_enum_class_file_str_ReturnsObj_Scenario1_NonEmpty_keyword_set():
    # ESTABLISH
    ch04_str = "ch04"
    keywordF = f"Funny"
    keywordI = f"INSET"
    keywordf = f"funny"
    keywordG = f"Guppies"
    keywordH = f"Heath"
    keywordR = f"Ristore"
    ch04_keywords = {keywordF, keywordI, keywordf, keywordG, keywordH, keywordR}

    # WHEN
    file_str = create_keywords_enum_class_file_str(ch04_str, ch04_keywords)

    # THEN
    assert file_str
    key_str = "Key"
    expected_file_str = f"""

class Ch04{key_str}words(str, Enum):
    {keywordF} = "{keywordF}"
    {keywordG} = "{keywordG}"
    {keywordH} = "{keywordH}"
    {keywordI} = "{keywordI}"
    {keywordR} = "{keywordR}"
    {keywordf} = "{keywordf}"

    def __str__(self):
        return self.value
"""
    print(file_str)
    print(expected_file_str)
    assert file_str == expected_file_str


def test_SpecialTestThatBuildsKeywordEnumClasses():
    # ESTABLISH
    # save file for all Enum class references
    keywords_classes_file_path = create_keywords_classes_file_path("src")
    enum_classes_str = create_all_enum_keyword_classes_str()
    current_classes_file_str = open_file(keywords_classes_file_path)
    print(enum_classes_str[:100])
    save_file(keywords_classes_file_path, None, enum_classes_str)
    assertion_failure_str = (
        "Special case: keywords.py file was rebuilt, run test again."
    )

    # WHEN / THEN
    assert enum_classes_str == current_classes_file_str, assertion_failure_str
