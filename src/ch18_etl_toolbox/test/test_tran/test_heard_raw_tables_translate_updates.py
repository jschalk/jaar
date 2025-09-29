from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import get_table_columns
from src.ch18_etl_toolbox._ref.ch18_keywords import (
    Ch07Keywords as wx,
    Ch10Keywords as wx,
    Ch16Keywords as wx,
)
from src.ch18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    create_update_heard_raw_empty_inx_col_sqlstr,
    create_update_heard_raw_existing_inx_col_sqlstr,
)
from src.ch18_etl_toolbox.transformers import set_all_heard_raw_inx_columns


def test_create_update_heard_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario0_FullTranslateTables():
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
        create_sound_and_heard_tables(cursor)
        blrawar_dimen = wx.belief_plan_awardunit
        blrawar_h_raw_put_tablename = prime_tbl(blrawar_dimen, "h", "raw", "put")
        # print(f"{get_table_columns(cursor, blrawar_h_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {blrawar_h_raw_put_tablename} 
        ({wx.event_int}, {wx.face_name}_otx, {wx.face_name}_inx)
        VALUES
          ({event1}, '{sue_otx}', NULL)
        , ({event2}, '{yao_otx}', NULL)
        , ({event5}, '{sue_otx}', NULL)
        , ({event7}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)

        trlname_dimen = wx.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s", "vld")
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename} 
        ({wx.event_int}, {wx.face_name}, {wx.otx_name}, {wx.inx_name})
        VALUES
          ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {blrawar_h_raw_put_tablename} WHERE {wx.face_name}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        update_sqlstr = create_update_heard_raw_existing_inx_col_sqlstr(
            "name", blrawar_h_raw_put_tablename, wx.face_name
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 3
        select_face_name_only_sqlstr = f"""SELECT {wx.event_int}, {wx.face_name}_otx, {wx.face_name}_inx FROM {blrawar_h_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_otx, sue_inx),
            (2, yao_otx, None),
            (5, sue_otx, sue_inx),
            (7, bob_otx, bob_inx),
        ]


def test_create_update_heard_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario1_PartialTranslateTables():
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
        create_sound_and_heard_tables(cursor)
        blrawar_dimen = wx.belief_plan_awardunit
        blrawar_h_raw_put_tablename = prime_tbl(blrawar_dimen, "h", "raw", "put")
        insert_face_name_only_sqlstr = f"""INSERT INTO {blrawar_h_raw_put_tablename}
        ({wx.event_int}, {wx.face_name}_otx, {wx.face_name}_inx)
        VALUES
          ({event1}, '{sue_otx}', NULL)
        , ({event2}, '{yao_otx}', NULL)
        , ({event5}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)
        trlname_dimen = wx.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s", "vld")
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
        ({wx.event_int}, {wx.face_name}, {wx.otx_name}, {wx.inx_name})
        VALUES
          ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {blrawar_h_raw_put_tablename} WHERE {wx.face_name}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        update_sqlstr = create_update_heard_raw_existing_inx_col_sqlstr(
            "name", blrawar_h_raw_put_tablename, wx.face_name
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        select_face_name_only_sqlstr = f"""SELECT {wx.event_int}, {wx.face_name}_otx, {wx.face_name}_inx FROM {blrawar_h_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 translate record's
        assert rows == [
            (event1, sue_otx, sue_inx),
            (event2, yao_otx, None),
            (event5, bob_otx, None),
        ]


def test_create_update_heard_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario2_Different_event_int_TranslateMappings():
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
        create_sound_and_heard_tables(cursor)
        blrawar_dimen = wx.belief_plan_awardunit
        blrawar_h_raw_put_tablename = prime_tbl(blrawar_dimen, "h", "raw", "put")
        print(f"{get_table_columns(cursor, blrawar_h_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {blrawar_h_raw_put_tablename}
        ({wx.event_int}, {wx.face_name}_otx, {wx.face_name}_inx)
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

        trlname_dimen = wx.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s", "vld")
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
        ({wx.event_int}, {wx.face_name}, {wx.otx_name}, {wx.inx_name})
        VALUES
          ({event1}, '{bob_otx}', '{bob_otx}', '{bob_inx0}')
        , ({event2}, '{yao_otx}', '{yao_otx}', '{yao_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx7}')
        , ({event7}, '{bob_otx}', '{sue_otx}', '{bob_sue_inx}')
        , ({event8}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {blrawar_h_raw_put_tablename} WHERE {wx.face_name}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        update_sqlstr = create_update_heard_raw_existing_inx_col_sqlstr(
            "name", blrawar_h_raw_put_tablename, wx.face_name
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        select_face_name_only_sqlstr = f"""SELECT {wx.event_int}, {wx.face_name}_otx, {wx.face_name}_inx FROM {blrawar_h_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 translate record's
        assert rows == [
            (0, bob_otx, None),
            (1, bob_otx, bob_inx0),
            (2, yao_otx, yao_inx),
            (5, bob_otx, bob_inx0),
            (7, bob_otx, bob_inx7),
            (9, bob_otx, bob_inx7),
        ]


def test_create_update_heard_raw_empty_inx_col_sqlstr_UpdatesTable_Scenario0_EmptyTranslateTables():
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
        create_sound_and_heard_tables(cursor)
        trlname_s_vld_tablename = prime_tbl(wx.translate_name, "s", "vld")
        print(f"{trlname_s_vld_tablename=}")
        print(f"{get_table_columns(cursor, trlname_s_vld_tablename)=}")

        blrawar_dimen = wx.belief_plan_awardunit
        blrawar_h_raw_put_tablename = prime_tbl(blrawar_dimen, "h", "raw", "put")
        print(f"{get_table_columns(cursor, blrawar_h_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {blrawar_h_raw_put_tablename} ({wx.event_int}, {wx.face_name}_otx, {wx.face_name}_inx)
VALUES
  ({event1}, '{sue_otx}', '{sue_inx}')
, ({event2}, '{yao_otx}', NULL)
, ({event5}, '{sue_otx}', NULL)
, ({event7}, '{bob_otx}', '{bob_inx}')
;
"""
        cursor.execute(insert_face_name_only_sqlstr)
        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {blrawar_h_raw_put_tablename} WHERE {wx.face_name}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 2

        # WHEN
        update_sqlstr = create_update_heard_raw_empty_inx_col_sqlstr(
            blrawar_h_raw_put_tablename, wx.face_name
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 4
        select_face_name_only_sqlstr = f"""SELECT {wx.event_int}, {wx.face_name}_otx, {wx.face_name}_inx FROM {blrawar_h_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_otx, sue_inx),
            (2, yao_otx, yao_otx),
            (5, sue_otx, sue_otx),
            (7, bob_otx, bob_inx),
        ]


def test_set_all_heard_raw_inx_columns_Scenario0_empty_tables():
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
        create_sound_and_heard_tables(cursor)
        blrawar_dimen = wx.belief_plan_awardunit
        blrawar_h_raw_put_tablename = prime_tbl(blrawar_dimen, "h", "raw", "put")
        print(f"{get_table_columns(cursor, blrawar_h_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {blrawar_h_raw_put_tablename}
        ({wx.event_int}, {wx.face_name}_otx, {wx.face_name}_inx)
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

        trlname_dimen = wx.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s", "vld")
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
        ({wx.event_int}, {wx.face_name}, {wx.otx_name}, {wx.inx_name})
        VALUES
          ({event1}, '{bob_otx}', '{bob_otx}', '{bob_inx0}')
        , ({event2}, '{yao_otx}', '{yao_otx}', '{yao_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx7}')
        , ({event7}, '{bob_otx}', '{sue_otx}', '{bob_sue_inx}')
        , ({event8}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {blrawar_h_raw_put_tablename} WHERE {wx.face_name}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        set_all_heard_raw_inx_columns(cursor)

        # THEN
        select_face_name_only_sqlstr = f"""SELECT {wx.event_int}, {wx.face_name}_otx, {wx.face_name}_inx FROM {blrawar_h_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # event5 does not link to event7 translate record's
        assert rows == [
            (0, bob_otx, bob_otx),
            (1, bob_otx, bob_inx0),
            (2, yao_otx, yao_inx),
            (5, bob_otx, bob_inx0),
            (7, bob_otx, bob_inx7),
            (9, bob_otx, bob_inx7),
        ]
