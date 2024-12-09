from src.f01_road.jaar_config import (
    voice_str,
    final_str,
    get_rootpart_of_keep_dir,
    treasury_file_name,
    max_tree_traverse_default,
    default_river_blocks_count,
    default_unknown_word,
    default_unknown_word_if_none,
)


def test_voice_str():
    assert voice_str() == "voice"


def test_final_str():
    assert final_str() == "final"


def test_get_rootpart_of_keep_dir_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    assert get_rootpart_of_keep_dir() == "itemroot"


def test_treasury_file_name_ReturnsObj() -> str:
    assert treasury_file_name() == "treasury.db"


def test_max_tree_traverse_default_ReturnsObj() -> str:
    assert max_tree_traverse_default() == 20


def test_default_river_blocks_count_ReturnsObj() -> str:
    assert default_river_blocks_count() == 40


def test_default_unknown_word_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert default_unknown_word() == "UNKNOWN"


def test_default_unknown_word_if_none_ReturnsObj():
    # ESTABLISH
    unknown33_str = "unknown33"
    x_nan = float("nan")

    # WHEN / THEN
    assert default_unknown_word_if_none() == default_unknown_word()
    assert default_unknown_word_if_none(None) == default_unknown_word()
    assert default_unknown_word_if_none(unknown33_str) == unknown33_str
    assert default_unknown_word_if_none(x_nan) == default_unknown_word()
