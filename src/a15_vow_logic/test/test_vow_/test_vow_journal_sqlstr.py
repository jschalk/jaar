# from src.a08_plan_atom_logic.atom import atom_hx_str
# from src.a00_data_toolbox.sqlite import check_table_column_existence
# from src.a15_vow_logic.journal_sqlstr import get_atom_hx_table_insert_sqlstr
# from src.a15_vow_logic.vow import vowunit_shop
# from src.a15_vow_logic.test._util.vow_env import (
#     env_dir_setup_cleanup,
# )
# from src.a00_data_toolbox.sqlite import get_row_count
# from os.path import exists as os_path_exists
# from pytest import raises as pytest_raises


# def test_VowUnit_get_atom_hx_table_insert_sqlstr_CorrectlyInsertsIntoDatabase(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     accord45_str = "accord45"
#     accord_vow = vowunit_shop(accord45_str, get_module_temp_dir())
#     # with accord_vow.get_journal_conn() as journal_conn:
#     #     assert check_table_column_existence({atom_hx_str()}, journal_conn)
#     #     assert get_row_count(journal_conn, atom_hx_str()) == 0

#     # WHEN
#     x_atom = get_atom_example_factunit_knee()
#     # with accord_vow.get_journal_conn() as treasury_conn:
#     #     treasury_conn.execute(get_atom_hx_table_insert_sqlstr(x_atom))

#     # THEN
#     with accord_vow.get_journal_conn() as journal_conn:
#         assert get_row_count(journal_conn, atom_hx_str()) == 1
