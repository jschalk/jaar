from src.ch01_py.chapter_desc_tools import get_chapter_desc_prefix


def test_get_chapter_desc_prefix_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_chapter_desc_prefix("ch04_") == "ch04"
    assert get_chapter_desc_prefix("ch99") == "ch99"
    assert get_chapter_desc_prefix("ch04") == "ch04"
    assert get_chapter_desc_prefix("ch99") == "ch99"
    assert get_chapter_desc_prefix("chXX") == "chXX"
    assert get_chapter_desc_prefix("cha01") != "ch02"
