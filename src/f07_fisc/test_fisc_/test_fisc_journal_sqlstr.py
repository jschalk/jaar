# from src.f04_gift.atom import atom_hx_table_name
# from src.f00_instrument.sqlite import check_table_column_existence
# from src.f07_fisc.journal_sqlstr import get_atom_hx_table_insert_sqlstr
# from src.f07_fisc.fisc import fiscunit_shop
# from src.f07_fisc.examples.fisc_env import (
#     get_test_fisc_title,
#     get_test_fiscs_dir,
#     env_dir_setup_cleanup,
# )
# from src.f00_instrument.sqlite import get_row_count
# from os.path import exists as os_path_exists
# from pytest import raises as pytest_raises


# def test_FiscUnit_get_atom_hx_table_insert_sqlstr_CorrectlyInsertsIntoDatabase(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     accord45_str = "accord45"
#     accord_fisc = fiscunit_shop(accord45_str, get_test_fiscs_dir())
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
