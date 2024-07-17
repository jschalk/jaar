# from src.gift.atom import atom_hx_table_name
# from src._instrument.sqlite import check_table_column_existence
# from src.real.journal_sqlstr import get_atom_hx_table_insert_sqlstr
# from src.real.real import realunit_shop
# from src.real.examples.real_env import (
#     get_test_real_id,
#     get_test_reals_dir,
#     env_dir_setup_cleanup,
# )
# from src._instrument.sqlite import get_row_count
# from os.path import exists as os_path_exists
# from pytest import raises as pytest_raises


# def test_RealUnit_get_atom_hx_table_insert_sqlstr_CorrectlyInsertsIntoDatabase(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     music_text = "music"
#     music_real = realunit_shop(music_text, get_test_reals_dir())
#     # with music_real.get_journal_conn() as journal_conn:
#     #     assert check_table_column_existence({atom_hx_table_name()}, journal_conn)
#     #     assert get_row_count(journal_conn, atom_hx_table_name()) == 0

#     # WHEN
#     x_atom = get_atom_example_factunit_knee()
#     # with music_real.get_journal_conn() as treasury_conn:
#     #     treasury_conn.execute(get_atom_hx_table_insert_sqlstr(x_atom))

#     # THEN
#     with music_real.get_journal_conn() as journal_conn:
#         assert get_row_count(journal_conn, atom_hx_table_name()) == 1

#     assert 1 == 2
