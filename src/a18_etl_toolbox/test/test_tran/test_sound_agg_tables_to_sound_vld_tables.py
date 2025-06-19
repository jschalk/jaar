from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_row_count, get_table_columns
from src.a02_finance_logic.test._util.a02_str import owner_name_str, vow_label_str
from src.a06_plan_logic.test._util.a06_str import (
    acct_name_str,
    credit_score_str,
    debt_score_str,
    plan_acctunit_str,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
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
    x22_debt = 22
    x66_debt = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        planaacct_s_agg_put_tablename = prime_tbl(
            plan_acctunit_str(), "s", "agg", "put"
        )
        print(f"{get_table_columns(cursor, planaacct_s_agg_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {planaacct_s_agg_put_tablename} (
  {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_score_str()}
, {debt_score_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao}', {x44_credit}, {x22_debt})
, ({event2}, '{yao_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event5}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debt})
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, planaacct_s_agg_put_tablename) == 4
        plnawar_v_vld_put_tablename = prime_tbl(plan_acctunit_str(), "s", "vld", "put")
        assert get_row_count(cursor, plnawar_v_vld_put_tablename) == 0

        # WHEN
        sqlstr = get_insert_into_sound_vld_sqlstrs().get(plnawar_v_vld_put_tablename)
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert get_row_count(cursor, plnawar_v_vld_put_tablename) == 4
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_score_str()}
, {debt_score_str()}
FROM {plnawar_v_vld_put_tablename}
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
    x22_debt = 22
    x66_debt = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        plnacct_s_agg_put_tablename = prime_tbl(plan_acctunit_str(), "s", "agg", "put")
        print(f"{get_table_columns(cursor, plnacct_s_agg_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {plnacct_s_agg_put_tablename} (
  {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_score_str()}
, {debt_score_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao}', {x44_credit}, {x22_debt})
, ({event2}, '{yao_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event5}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debt})
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, plnacct_s_agg_put_tablename) == 4
        plnacct_v_vld_put_tablename = prime_tbl(plan_acctunit_str(), "s", "vld", "put")
        assert get_row_count(cursor, plnacct_v_vld_put_tablename) == 0

        # WHEN
        etl_sound_agg_tables_to_sound_vld_tables(cursor)

        # THEN
        assert get_row_count(cursor, plnacct_v_vld_put_tablename) == 4
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_score_str()}
, {debt_score_str()}
FROM {plnacct_v_vld_put_tablename}
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
    x22_debt = 22
    x66_debt = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        plnacct_s_agg_put_tablename = prime_tbl(plan_acctunit_str(), "s", "agg", "put")
        print(f"{get_table_columns(cursor, plnacct_s_agg_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {plnacct_s_agg_put_tablename} (
  {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_score_str()}
, {debt_score_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao_str}', {x44_credit}, {x22_debt})
, ({event2}, '{yao_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event5}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debt})
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, plnacct_s_agg_put_tablename) == 4
        plnacct_v_vld_put_tablename = prime_tbl(plan_acctunit_str(), "s", "vld", "put")
        assert get_row_count(cursor, plnacct_v_vld_put_tablename) == 0

        # WHEN
        etl_sound_agg_tables_to_sound_vld_tables(cursor)

        # THEN
        assert get_row_count(cursor, plnacct_v_vld_put_tablename) == 4
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_score_str()}
, {debt_score_str()}
FROM {plnacct_v_vld_put_tablename}
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
    x22_debt = 22
    x66_debt = 66

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        plnacct_s_agg_put_tablename = prime_tbl(plan_acctunit_str(), "s", "agg", "put")
        print(f"{get_table_columns(cursor, plnacct_s_agg_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {plnacct_s_agg_put_tablename} (
  {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_score_str()}
, {debt_score_str()}
, error_message
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao_str}', {x44_credit}, {x22_debt}, NULL)
, ({event2}, '{yao_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt}, 'Data is not correct')
, ({event5}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt}, NULL)
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debt}, NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, plnacct_s_agg_put_tablename) == 4
        plnacct_v_vld_put_tablename = prime_tbl(plan_acctunit_str(), "s", "vld", "put")
        assert get_row_count(cursor, plnacct_v_vld_put_tablename) == 0

        # WHEN
        etl_sound_agg_tables_to_sound_vld_tables(cursor)

        # THEN
        assert get_row_count(cursor, plnacct_v_vld_put_tablename) == 3
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}
, {vow_label_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_score_str()}
, {debt_score_str()}
FROM {plnacct_v_vld_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, a23_str, yao_str, yao_str, 44.0, 22.0),
            (5, sue_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (7, bob_str, a23_str, bob_str, bob_str, 55.0, 66.0),
        ]
