from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_row_count, get_table_columns
from src.a06_believer_logic.test._util.a06_str import (
    believer_name_str,
    believer_partnerunit_str,
    coin_label_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_voice_tables,
    get_insert_into_voice_raw_sqlstrs,
)
from src.a18_etl_toolbox.transformers import etl_sound_vld_tables_to_voice_raw_tables


def test_get_insert_into_voice_raw_sqlstrs_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    a23_str = "amy23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
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
        believerapartner_s_vld_put_tablename = prime_tbl(
            believer_partnerunit_str(), "s", "vld", "put"
        )
        print(f"{get_table_columns(cursor, believerapartner_s_vld_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {believerapartner_s_vld_put_tablename} (
  {event_int_str()}
, {face_name_str()}
, {coin_label_str()}
, {believer_name_str()}
, {partner_name_str()}
, {partner_cred_points_str()}
, {partner_debt_points_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao_inx}', {x44_credit}, {x22_debt})
, ({event2}, '{yao_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event5}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debt})
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, believerapartner_s_vld_put_tablename) == 4
        blrawar_v_raw_put_tablename = prime_tbl(
            believer_partnerunit_str(), "v", "raw", "put"
        )
        assert get_row_count(cursor, blrawar_v_raw_put_tablename) == 0

        # WHEN
        sqlstr = get_insert_into_voice_raw_sqlstrs().get(blrawar_v_raw_put_tablename)
        cursor.execute(sqlstr)

        # THEN
        assert get_row_count(cursor, blrawar_v_raw_put_tablename) == 4
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}_otx
, {coin_label_str()}_otx
, {believer_name_str()}_otx
, {partner_name_str()}_otx
, {partner_cred_points_str()}
, {partner_debt_points_str()}
FROM {blrawar_v_raw_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, a23_str, yao_str, yao_inx, 44.0, 22.0),
            (2, yao_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (5, sue_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (7, bob_str, a23_str, bob_str, bob_str, 55.0, 66.0),
        ]


def test_etl_sound_vld_tables_to_voice_raw_tables_Scenario0_AddRowsToTable():
    # ESTABLISH
    a23_str = "amy23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
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
        blrpern_s_vld_put_tablename = prime_tbl(
            believer_partnerunit_str(), "s", "vld", "put"
        )
        print(f"{get_table_columns(cursor, blrpern_s_vld_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {blrpern_s_vld_put_tablename} (
  {event_int_str()}
, {face_name_str()}
, {coin_label_str()}
, {believer_name_str()}
, {partner_name_str()}
, {partner_cred_points_str()}
, {partner_debt_points_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao_inx}', {x44_credit}, {x22_debt})
, ({event2}, '{yao_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event5}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x22_debt})
, ({event7}, '{bob_str}', '{a23_str}','{bob_str}', '{bob_str}', {x55_credit}, {x66_debt})
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        assert get_row_count(cursor, blrpern_s_vld_put_tablename) == 4
        blrpern_v_raw_put_tablename = prime_tbl(
            believer_partnerunit_str(), "v", "raw", "put"
        )
        assert get_row_count(cursor, blrpern_v_raw_put_tablename) == 0

        # WHEN
        etl_sound_vld_tables_to_voice_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, blrpern_v_raw_put_tablename) == 4
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}_otx
, {coin_label_str()}_otx
, {believer_name_str()}_otx
, {partner_name_str()}_otx
, {partner_cred_points_str()}
, {partner_debt_points_str()}
FROM {blrpern_v_raw_put_tablename}
"""
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, a23_str, yao_str, yao_inx, 44.0, 22.0),
            (2, yao_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (5, sue_str, a23_str, bob_str, bob_str, 55.0, 22.0),
            (7, bob_str, a23_str, bob_str, bob_str, 55.0, 66.0),
        ]


def test_etl_sound_vld_tables_to_voice_raw_tables_Scenario1_Populates_inx_Columns():
    # ESTABLISH
    a23_str = "amy23"
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
        blrpern_s_vld_put_tablename = prime_tbl(
            believer_partnerunit_str(), "s", "vld", "put"
        )
        print(f"{get_table_columns(cursor, blrpern_s_vld_put_tablename)=}")
        insert_into_clause = f"""INSERT INTO {blrpern_s_vld_put_tablename} (
  {event_int_str()}
, {face_name_str()}
, {coin_label_str()}
, {believer_name_str()}
, {partner_name_str()}
, {partner_cred_points_str()}
, {partner_debt_points_str()}
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
        assert get_row_count(cursor, blrpern_s_vld_put_tablename) == 4
        blrpern_v_raw_put_tablename = prime_tbl(
            believer_partnerunit_str(), "v", "raw", "put"
        )
        assert get_row_count(cursor, blrpern_v_raw_put_tablename) == 0

        # WHEN
        etl_sound_vld_tables_to_voice_raw_tables(cursor)

        # THEN
        assert get_row_count(cursor, blrpern_v_raw_put_tablename) == 4
        select_sqlstr = f"""SELECT {event_int_str()}
, {face_name_str()}_inx
, {coin_label_str()}_inx
, {believer_name_str()}_inx
, {partner_name_str()}_inx
, {partner_cred_points_str()}
, {partner_debt_points_str()}
FROM {blrpern_v_raw_put_tablename}
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
