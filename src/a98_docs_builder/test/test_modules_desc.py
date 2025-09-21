from src.a98_docs_builder.doc_builder import (
    get_module_desc_prefix,
    get_module_desc_str_number,
)


def test_get_module_desc_str_number_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_module_desc_str_number("a03") == "03"
    assert get_module_desc_str_number("a99") == "99"
    assert get_module_desc_str_number("aXX") == "XX"
    assert get_module_desc_str_number("aa01") != "01"
    assert get_module_desc_str_number("ch03") == "03"
    assert get_module_desc_str_number("ch99") == "99"
    assert get_module_desc_str_number("chXX") == "XX"
    assert get_module_desc_str_number("cha01") != "01"


def test_get_module_prefix_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_module_desc_prefix("a03_") == "a03"
    assert get_module_desc_prefix("a99") == "a99"
    assert get_module_desc_prefix("aXX_ZZZZ") == "aXX"
    assert get_module_desc_prefix("aa01") != "a01"
    assert get_module_desc_prefix("ch03") == "ch03"
    assert get_module_desc_prefix("ch99") == "ch99"
    assert get_module_desc_prefix("chXX") == "chXX"
    assert get_module_desc_prefix("cha01") != "ch01"
