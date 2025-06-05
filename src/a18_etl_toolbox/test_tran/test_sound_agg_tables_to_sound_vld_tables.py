from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_row_count, get_table_columns
from src.a02_finance_logic._test_util.a02_str import owner_name_str, vow_label_str
from src.a06_bud_logic._test_util.a06_str import (
    acct_name_str,
    bud_acctunit_str,
    credit_belief_str,
    debtit_belief_str,
)
from src.a09_pack_logic._test_util.a09_str import event_int_str, face_name_str
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_voice_tables,
    get_insert_into_sound_vld_sqlstrs,
)
from src.a18_etl_toolbox.transformers import etl_sound_agg_tables_to_sound_vld_tables


def test_get_insert_into_sound_vld_sqlstrs_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao = "Yaoito"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debtit = 22
    x66_debtit = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budaacct_s_agg_put_tablename = prime_tbl(bud_acctunit_str(), "s", "agg", "put")
        print(f"{get_table_columns(cursor, budaacct_s_agg_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {budaacct_s_agg_put_tablename} (
  {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_belief_str()}
, {debtit_belief_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao}', {x44_credit}, {x22_debtit})
, ({event2}, '{yao_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debtit})
, ({event5}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debtit})
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debtit})
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, budaacct_s_agg_put_tablename) == 4
        budawar_v_vld_put_tablename = prime_tbl(bud_acctunit_str(), "s", "vld", "put")
        assert get_row_count(cursor, budawar_v_vld_put_tablename) == 0

        # WHEN
        sqlstr = get_insert_into_sound_vld_sqlstrs().get(budawar_v_vld_put_tablename)
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert get_row_count(cursor, budawar_v_vld_put_tablename) == 4
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_belief_str()}
, {debtit_belief_str()}
FROM {budawar_v_vld_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, a23_str, yao_str, yao, 44.0, 22.0),
            (2, yao_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (5, sue_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (7, bob_str, a23_str, bob_str, bob_str, 55.0, 66.0),
        ]


def test_etl_sound_agg_tables_to_sound_vld_tables_Scenario0_AddRowsToTable():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao = "Yaoito"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debtit = 22
    x66_debtit = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budacct_s_agg_put_tablename = prime_tbl(bud_acctunit_str(), "s", "agg", "put")
        print(f"{get_table_columns(cursor, budacct_s_agg_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {budacct_s_agg_put_tablename} (
  {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_belief_str()}
, {debtit_belief_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao}', {x44_credit}, {x22_debtit})
, ({event2}, '{yao_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debtit})
, ({event5}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debtit})
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debtit})
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, budacct_s_agg_put_tablename) == 4
        budacct_v_vld_put_tablename = prime_tbl(bud_acctunit_str(), "s", "vld", "put")
        assert get_row_count(cursor, budacct_v_vld_put_tablename) == 0

        # WHEN
        etl_sound_agg_tables_to_sound_vld_tables(cursor)

        # THEN
        assert get_row_count(cursor, budacct_v_vld_put_tablename) == 4
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_belief_str()}
, {debtit_belief_str()}
FROM {budacct_v_vld_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, a23_str, yao_str, yao, 44.0, 22.0),
            (2, yao_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (5, sue_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (7, bob_str, a23_str, bob_str, bob_str, 55.0, 66.0),
        ]


def test_etl_sound_agg_tables_to_sound_vld_tables_Scenario1_Populates_Columns():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debtit = 22
    x66_debtit = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budacct_s_agg_put_tablename = prime_tbl(bud_acctunit_str(), "s", "agg", "put")
        print(f"{get_table_columns(cursor, budacct_s_agg_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {budacct_s_agg_put_tablename} (
  {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_belief_str()}
, {debtit_belief_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao_str}', {x44_credit}, {x22_debtit})
, ({event2}, '{yao_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debtit})
, ({event5}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debtit})
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debtit})
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, budacct_s_agg_put_tablename) == 4
        budacct_v_vld_put_tablename = prime_tbl(bud_acctunit_str(), "s", "vld", "put")
        assert get_row_count(cursor, budacct_v_vld_put_tablename) == 0

        # WHEN
        etl_sound_agg_tables_to_sound_vld_tables(cursor)

        # THEN
        assert get_row_count(cursor, budacct_v_vld_put_tablename) == 4
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_belief_str()}
, {debtit_belief_str()}
FROM {budacct_v_vld_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, a23_str, yao_str, yao_str, 44.0, 22.0),
            (2, yao_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (5, sue_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (7, bob_str, a23_str, bob_str, bob_str, 55.0, 66.0),
        ]


def test_etl_sound_agg_tables_to_sound_vld_tables_Scenario2_DoesNotSelectWhere_error_message_IsNotNull():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    x44_credit = 44
    x55_credit = 55
    x22_debtit = 22
    x66_debtit = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budacct_s_agg_put_tablename = prime_tbl(bud_acctunit_str(), "s", "agg", "put")
        print(f"{get_table_columns(cursor, budacct_s_agg_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {budacct_s_agg_put_tablename} (
  {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_belief_str()}
, {debtit_belief_str()}
, error_message
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao_str}', {x44_credit}, {x22_debtit}, NULL)
, ({event2}, '{yao_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debtit}, 'Data is not correct')
, ({event5}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debtit}, NULL)
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debtit}, NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, budacct_s_agg_put_tablename) == 4
        budacct_v_vld_put_tablename = prime_tbl(bud_acctunit_str(), "s", "vld", "put")
        assert get_row_count(cursor, budacct_v_vld_put_tablename) == 0

        # WHEN
        etl_sound_agg_tables_to_sound_vld_tables(cursor)

        # THEN
        assert get_row_count(cursor, budacct_v_vld_put_tablename) == 3
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_belief_str()}
, {debtit_belief_str()}
FROM {budacct_v_vld_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, a23_str, yao_str, yao_str, 44.0, 22.0),
            (5, sue_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (7, bob_str, a23_str, bob_str, bob_str, 55.0, 66.0),
        ]
