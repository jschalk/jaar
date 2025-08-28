from pathlib import Path as pathlib_Path
from src.a98_docs_builder.module_eval import get_str_funcs_md


def test_get_str_funcs_md_SetsFile_CheckMarkdownHasAllStrFunctions():
    # ESTABLISH / WHEN
    str_funcs_md = get_str_funcs_md()

    # THEN
    assert str_funcs_md.find("String Functions by Module") > 0
    a09_pack_logic_index = str_funcs_md.find("a09_pack_logic")
    assert a09_pack_logic_index > 0
    event_int_index = str_funcs_md.find("event_int")
    assert event_int_index > 0
    assert a09_pack_logic_index < event_int_index

    # # write to production
    # doc_main_dir = pathlib_Path("docs")
    # doc_main_dir.mkdir(parents=True, exist_ok=True)
    # doc_main_dir.write_text(str_funcs_md)
