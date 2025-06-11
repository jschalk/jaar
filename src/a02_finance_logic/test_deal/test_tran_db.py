from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import db_table_exists, get_row_count
from src.a02_finance_logic._test_util.a02_str import acct_name_str, vow_label_str
from src.a02_finance_logic.deal import (
    TranBook,
    TranUnit,
    get_tranbook_from_dict,
    tranbook_shop,
    tranunit_shop,
)
from src.a02_finance_logic.deal_db import insert_tranunit_accts_net


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
    accord23_accts_net_array = a23_tranbook._get_accts_net_array()
    assert accord23_accts_net_array == [
        [bob_str, t55_bob_amount],
        [yao_str, t55_yao_amount + t66_yao_amount + t77_yao_amount],
    ]
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        dst_tablename = "tranbook_accts_net"
        assert not db_table_exists(cursor, dst_tablename)

        # WHEN
        insert_tranunit_accts_net(cursor, a23_tranbook, dst_tablename)

        # THEN
        assert db_table_exists(cursor, dst_tablename)
        assert get_row_count(cursor, dst_tablename) == 2
        cursor.execute(f"SELECT owner_name, net_amount FROM {dst_tablename}")
        rows = cursor.fetchall()
        assert rows == [
            (bob_str, t55_bob_amount),
            (yao_str, t55_yao_amount + t66_yao_amount + t77_yao_amount),
        ]
