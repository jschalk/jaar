from src.ch98_docs_builder.doc_builder import (
    get_chapter_desc_prefix,
    get_chapter_desc_str_number,
)


def test_get_chapter_desc_str_number_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_chapter_desc_str_number("ch04") == "04"
    assert get_chapter_desc_str_number("ch99") == "99"
    assert get_chapter_desc_str_number("aXX") == "XX"
    assert get_chapter_desc_str_number("aa01") != "01"
    assert get_chapter_desc_str_number("ch04") == "04"
    assert get_chapter_desc_str_number("ch99") == "99"
    assert get_chapter_desc_str_number("chXX") == "XX"
    assert get_chapter_desc_str_number("cha01") != "01"


def test_get_chapter_prefix_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_chapter_desc_prefix("ch04_") == "ch04"
    assert get_chapter_desc_prefix("ch99") == "ch99"
    assert get_chapter_desc_prefix("aXX_ZZZZ") == "aXX"
    assert get_chapter_desc_prefix("aa01") != "ch02"
    assert get_chapter_desc_prefix("ch04") == "ch04"
    assert get_chapter_desc_prefix("ch99") == "ch99"
    assert get_chapter_desc_prefix("chXX") == "chXX"
    assert get_chapter_desc_prefix("cha01") != "ch02"
