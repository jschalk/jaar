# from src.a08_bud_atom_logic.atom import atom_hx_table_name
# from src.a00_data_toolboxs.sqlite import check_table_column_existence
# from src.a15_fisc_logic.journal_sqlstr import get_atom_hx_table_insert_sqlstr
# from src.a15_fisc_logic.fisc import fiscunit_shop
# from src.a15_fisc_logic.examples.fisc_env import (
#     env_dir_setup_cleanup,
# )
# from src.a00_data_toolboxs.sqlite import get_row_count
# from os.path import exists as os_path_exists
# from pytest import raises as pytest_raises


# def test_FiscUnit_get_atom_hx_table_insert_sqlstr_CorrectlyInsertsIntoDatabase(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     accord45_str = "accord45"
#     accord_fisc = fiscunit_shop(accord45_str, get_test_fisc_mstr_dir())
#     # with accord_fisc.get_journal_conn() as journal_conn:
#     #     assert check_table_column_existence({atom_hx_table_name()}, journal_conn)
#     #     assert get_row_count(journal_conn, atom_hx_table_name()) == 0

#     # WHEN
#     x_atom = get_atom_example_factunit_knee()
#     # with accord_fisc.get_journal_conn() as treasury_conn:
#     #     treasury_conn.execute(get_atom_hx_table_insert_sqlstr(x_atom))

#     # THEN
#     with accord_fisc.get_journal_conn() as journal_conn:
#         assert get_row_count(journal_conn, atom_hx_table_name()) == 1

#     assert 1 == 2
