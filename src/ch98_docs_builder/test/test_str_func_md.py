from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_file
from src.ch98_docs_builder.doc_builder import get_str_funcs_md, save_str_funcs_md
from src.ch98_docs_builder.test._util.ch98_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


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


def test_save_str_funcs_md_SavesFile_get_str_funcs_md_ToGivenDirectory(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    str_funcs_md_path = create_path(temp_dir, "str_funcs.md")
    assert not os_path_exists(str_funcs_md_path)

    # WHEN
    str_funcs_md = save_str_funcs_md(temp_dir)

    # THEN
    assert os_path_exists(str_funcs_md_path)
    str_funcs_md = get_str_funcs_md()
    assert open_file(str_funcs_md_path) == str_funcs_md
