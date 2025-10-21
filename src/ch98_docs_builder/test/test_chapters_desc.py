from src.ch98_docs_builder.doc_builder import get_chapter_desc_str_number


def test_get_chapter_desc_str_number_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_chapter_desc_str_number("ch04") == "04"
    assert get_chapter_desc_str_number("ch99") == "99"
    assert get_chapter_desc_str_number("aXX") == "XX"
    assert get_chapter_desc_str_number("aa01") != "01"
    assert get_chapter_desc_str_number("ch03") == "03"
    assert get_chapter_desc_str_number("ch99") == "99"
    assert get_chapter_desc_str_number("chXX") == "XX"
    assert get_chapter_desc_str_number("cha01") != "01"
