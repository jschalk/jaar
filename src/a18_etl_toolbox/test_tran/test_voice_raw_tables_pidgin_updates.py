from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_table_columns
from src.a06_bud_logic._test_util.a06_str import bud_concept_awardlink_str
from src.a09_pack_logic._test_util.a09_str import event_int_str, face_name_str
from src.a16_pidgin_logic._test_util.a16_str import (
    inx_name_str,
    otx_name_str,
    pidgin_name_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_voice_tables,
    create_update_voice_raw_empty_inx_col_sqlstr,
    create_update_voice_raw_existing_inx_col_sqlstr,
)
from src.a18_etl_toolbox.transformers import set_all_voice_raw_inx_columns

# TODO create test for mapped_names sqlstr (link otx_)


def test_create_update_voice_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario0_FullPidginTables():
    # ESTABLISH
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    yao_otx = "Yao"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budawar_dimen = bud_concept_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        # print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename} 
        ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
        VALUES
          ({event1}, '{sue_otx}', NULL)
        , ({event2}, '{yao_otx}', NULL)
        , ({event5}, '{sue_otx}', NULL)
        , ({event7}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)

        pidname_dimen = pidgin_name_str()
        pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
        print(f"{pidname_s_vld_tablename=}")
        insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename} 
        ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
        VALUES
          ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_pidname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        update_sqlstr = create_update_voice_raw_existing_inx_col_sqlstr(
            "name", budawar_v_raw_put_tablename, face_name_str()
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 3
        select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_otx, sue_inx),
            (2, yao_otx, None),
            (5, sue_otx, sue_inx),
            (7, bob_otx, bob_inx),
        ]


def test_create_update_voice_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario1_PartialPidginTables():
    # ESTABLISH
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    yao_otx = "Yao"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budawar_dimen = bud_concept_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename}
        ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
        VALUES
          ({event1}, '{sue_otx}', NULL)
        , ({event2}, '{yao_otx}', NULL)
        , ({event5}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)
        pidname_dimen = pidgin_name_str()
        pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
        print(f"{pidname_s_vld_tablename=}")
        insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
        VALUES
          ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_pidname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        update_sqlstr = create_update_voice_raw_existing_inx_col_sqlstr(
            "name", budawar_v_raw_put_tablename, face_name_str()
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 pidgin record's
        assert rows == [
            (event1, sue_otx, sue_inx),
            (event2, yao_otx, None),
            (event5, bob_otx, None),
        ]


def test_create_update_voice_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario2_Different_event_int_PidginMappings():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_sue_inx = "BobSuzInx"
    bob_otx = "Bob"
    bob_inx0 = "Bobby"
    bob_inx7 = "Robert"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    event0 = 0
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event8 = 8
    event9 = 9

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budawar_dimen = bud_concept_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename}
        ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
        VALUES
          ({event0}, '{bob_otx}', NULL)
        , ({event1}, '{bob_otx}', NULL)
        , ({event2}, '{yao_otx}', NULL)
        , ({event5}, '{bob_otx}', NULL)
        , ({event7}, '{bob_otx}', NULL)
        , ({event9}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)

        pidname_dimen = pidgin_name_str()
        pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
        print(f"{pidname_s_vld_tablename=}")
        insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
        VALUES
          ({event1}, '{bob_otx}', '{bob_otx}', '{bob_inx0}')
        , ({event2}, '{yao_otx}', '{yao_otx}', '{yao_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx7}')
        , ({event7}, '{bob_otx}', '{sue_otx}', '{bob_sue_inx}')
        , ({event8}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        ;
        """
        cursor.execute(insert_pidname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        update_sqlstr = create_update_voice_raw_existing_inx_col_sqlstr(
            "name", budawar_v_raw_put_tablename, face_name_str()
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 pidgin record's
        assert rows == [
            (0, bob_otx, None),
            (1, bob_otx, bob_inx0),
            (2, yao_otx, yao_inx),
            (5, bob_otx, bob_inx0),
            (7, bob_otx, bob_inx7),
            (9, bob_otx, bob_inx7),
        ]


def test_create_update_voice_raw_empty_inx_col_sqlstr_UpdatesTable_Scenario0_EmptyPidginTables():
    # ESTABLISH
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    yao_otx = "Yao"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        pidname_s_vld_tablename = prime_tbl(pidgin_name_str(), "s", "vld")
        print(f"{pidname_s_vld_tablename=}")
        print(f"{get_table_columns(cursor, pidname_s_vld_tablename)=}")

        budawar_dimen = bud_concept_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename} ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
VALUES
  ({event1}, '{sue_otx}', '{sue_inx}')
, ({event2}, '{yao_otx}', NULL)
, ({event5}, '{sue_otx}', NULL)
, ({event7}, '{bob_otx}', '{bob_inx}')
;
"""
        cursor.execute(insert_face_name_only_sqlstr)
        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 2

        # WHEN
        update_sqlstr = create_update_voice_raw_empty_inx_col_sqlstr(
            budawar_v_raw_put_tablename, face_name_str()
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 4
        select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_otx, sue_inx),
            (2, yao_otx, yao_otx),
            (5, sue_otx, sue_otx),
            (7, bob_otx, bob_inx),
        ]


def test_set_all_voice_raw_inx_columns_Scenario0_empty_tables():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_sue_inx = "BobSuzInx"
    bob_otx = "Bob"
    bob_inx0 = "Bobby"
    bob_inx7 = "Robert"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    event0 = 0
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event8 = 8
    event9 = 9

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budawar_dimen = bud_concept_awardlink_str()
        budawar_v_raw_put_tablename = prime_tbl(budawar_dimen, "v", "raw", "put")
        print(f"{get_table_columns(cursor, budawar_v_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {budawar_v_raw_put_tablename}
        ({event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx)
        VALUES
          ({event0}, '{bob_otx}', NULL)
        , ({event1}, '{bob_otx}', NULL)
        , ({event2}, '{yao_otx}', NULL)
        , ({event5}, '{bob_otx}', NULL)
        , ({event7}, '{bob_otx}', NULL)
        , ({event9}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)

        pidname_dimen = pidgin_name_str()
        pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
        print(f"{pidname_s_vld_tablename=}")
        insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
        VALUES
          ({event1}, '{bob_otx}', '{bob_otx}', '{bob_inx0}')
        , ({event2}, '{yao_otx}', '{yao_otx}', '{yao_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx7}')
        , ({event7}, '{bob_otx}', '{sue_otx}', '{bob_sue_inx}')
        , ({event8}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        ;
        """
        cursor.execute(insert_pidname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {budawar_v_raw_put_tablename} WHERE {face_name_str()}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        set_all_voice_raw_inx_columns(cursor)

        # THEN
        select_face_name_only_sqlstr = f"""SELECT {event_int_str()}, {face_name_str()}_otx, {face_name_str()}_inx FROM {budawar_v_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 pidgin record's
        assert rows == [
            (0, bob_otx, bob_otx),
            (1, bob_otx, bob_inx0),
            (2, yao_otx, yao_inx),
            (5, bob_otx, bob_inx0),
            (7, bob_otx, bob_inx7),
            (9, bob_otx, bob_inx7),
        ]
