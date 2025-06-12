from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_row_count
from src.a02_finance_logic.deal import tranbook_shop
from src.a18_etl_toolbox._test_util.a18_str import (
    owner_net_amount_str,
    vow_acct_nets_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import CREATE_VOW_ACCT_NETS_SQLSTR
from src.a18_etl_toolbox.transformers import insert_tranunit_accts_net


def test_insert_tranunit_accts_net_PopulatesDatabase():
    # ESTABLISH
    a23_str = "accord23"
    a23_tranbook = tranbook_shop(a23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    a23_tranbook.add_tranunit(sue_str, yao_str, t55_tran_time, t55_yao_amount)
    a23_tranbook.add_tranunit(sue_str, yao_str, t66_tran_time, t66_yao_amount)
    a23_tranbook.add_tranunit(sue_str, bob_str, t55_tran_time, t55_bob_amount)
    a23_tranbook.add_tranunit(yao_str, yao_str, t77_tran_time, t77_yao_amount)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        dst_tablename = vow_acct_nets_str()
        cursor.execute(CREATE_VOW_ACCT_NETS_SQLSTR)
        assert get_row_count(cursor, dst_tablename) == 0

        # WHEN
        insert_tranunit_accts_net(cursor, a23_tranbook)

        # THEN
        assert get_row_count(cursor, dst_tablename) == 2
        cursor.execute(
            f"SELECT vow_label, owner_name, {owner_net_amount_str()} FROM {dst_tablename}"
        )
        rows = cursor.fetchall()
        assert rows == [
            (a23_str, bob_str, t55_bob_amount),
            (a23_str, yao_str, t55_yao_amount + t66_yao_amount + t77_yao_amount),
        ]
