# from src.f04_gift.atom import atom_hx_table_name
# from src.f00_instrument.sqlite import check_table_column_existence
# from src.f07_deal.journal_sqlstr import get_atom_hx_table_insert_sqlstr
# from src.f07_deal.deal import dealunit_shop
# from src.f07_deal.examples.deal_env import (
#     get_test_deal_id,
#     get_test_deals_dir,
#     env_dir_setup_cleanup,
# )
# from src.f00_instrument.sqlite import get_row_count
# from os.path import exists as os_path_exists
# from pytest import raises as pytest_raises


# def test_DealUnit_get_atom_hx_table_insert_sqlstr_CorrectlyInsertsIntoDatabase(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     accord_str = "accord"
#     accord_deal = dealunit_shop(accord_str, get_test_deals_dir())
#     # with accord_deal.get_journal_conn() as journal_conn:
#     #     assert check_table_column_existence({atom_hx_table_name()}, journal_conn)
#     #     assert get_row_count(journal_conn, atom_hx_table_name()) == 0

#     # WHEN
#     x_atom = get_atom_example_factunit_knee()
#     # with accord_deal.get_journal_conn() as treasury_conn:
#     #     treasury_conn.execute(get_atom_hx_table_insert_sqlstr(x_atom))

#     # THEN
#     with accord_deal.get_journal_conn() as journal_conn:
#         assert get_row_count(journal_conn, atom_hx_table_name()) == 1

#     assert 1 == 2
