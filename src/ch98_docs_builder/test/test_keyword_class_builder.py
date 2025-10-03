from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import open_file
from src.ch98_docs_builder.ch98_path import create_keywords_class_file_path
from src.ch98_docs_builder.keyword_class_builder import (
    create_keywords_enum_class_file_str,
    save_keywords_enum_class_file,
)
from src.ch98_docs_builder.test._util.ch98_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)


def test_create_keywords_enum_class_file_str_ReturnsObj_Scenario0_Empty_keyword_set():
    # ESTABLISH
    ch04_int = 4
    ch04_keywords = {}

    # WHEN
    file_str = create_keywords_enum_class_file_str(ch04_int, ch04_keywords)

    # THEN
    assert file_str
    key_str = "Key"
    expected_file_str = f"""from enum import Enum


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
    ch04_int = 4
    ch04_keywords = {
        "FundGrain",
        "INSERT",
        "fund_pool",
        "GroupTitle",
        "HealerName",
        "RespectGrain",
    }

    # WHEN
    file_str = create_keywords_enum_class_file_str(ch04_int, ch04_keywords)

    # THEN
    assert file_str
    key_str = "Key"
    expected_file_str = f"""from enum import Enum


class Ch04{key_str}words(str, Enum):
    FundGrain = "FundGrain"
    GroupTitle = "GroupTitle"
    HealerName = "HealerName"
    INSERT = "INSERT"
    RespectGrain = "RespectGrain"
    fund_pool = "fund_pool"

    def __str__(self):
        return self.value
"""
    print(file_str)
    print(expected_file_str)
    assert file_str == expected_file_str


def test_save_keywords_enum_class_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    ch04_int = 4
    ch04_keywords = {"RespectGrain", "FundGrain"}
    ch04_dir = get_chapter_temp_dir()
    expected_file_path = create_keywords_class_file_path(ch04_dir, 4)
    assert not os_path_exists(expected_file_path)

    # WHEN
    save_keywords_enum_class_file(ch04_dir, 4, ch04_keywords)

    # THEN
    assert os_path_exists(expected_file_path)
    file_str = open_file(expected_file_path)
    assert file_str
    expected_file_str = create_keywords_enum_class_file_str(ch04_int, ch04_keywords)
    print(file_str)
    print(expected_file_str)
    assert file_str == expected_file_str
