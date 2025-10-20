from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import get_table_columns
from src.ch18_world_etl.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
    create_update_heard_raw_empty_inx_col_sqlstr,
    create_update_heard_raw_existing_inx_col_sqlstr,
)
from src.ch18_world_etl.transformers import set_all_heard_raw_inx_columns
from src.ref.keywords import Ch18Keywords as kw


def test_create_update_heard_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario0_FullTranslateTables():
    # ESTABLISH
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    yao_otx = "Yao"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blrawar_dimen = kw.belief_plan_awardunit
        blrawar_h_raw_put_tablename = prime_tbl(blrawar_dimen, "h", "raw", "put")
        # print(f"{get_table_columns(cursor, blrawar_h_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {blrawar_h_raw_put_tablename} 
        ({kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx)
        VALUES
          ({spark1}, '{sue_otx}', NULL)
        , ({spark2}, '{yao_otx}', NULL)
        , ({spark5}, '{sue_otx}', NULL)
        , ({spark7}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)

        trlname_dimen = kw.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s", "vld")
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename} 
        ({kw.spark_num}, {kw.face_name}, {kw.otx_name}, {kw.inx_name})
        VALUES
          ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {blrawar_h_raw_put_tablename} WHERE {kw.face_name}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        update_sqlstr = create_update_heard_raw_existing_inx_col_sqlstr(
            "name", blrawar_h_raw_put_tablename, kw.face_name
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 3
        select_face_name_only_sqlstr = f"""SELECT {kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx FROM {blrawar_h_raw_put_tablename}"""
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
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blrawar_dimen = kw.belief_plan_awardunit
        blrawar_h_raw_put_tablename = prime_tbl(blrawar_dimen, "h", "raw", "put")
        insert_face_name_only_sqlstr = f"""INSERT INTO {blrawar_h_raw_put_tablename}
        ({kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx)
        VALUES
          ({spark1}, '{sue_otx}', NULL)
        , ({spark2}, '{yao_otx}', NULL)
        , ({spark5}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)
        trlname_dimen = kw.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s", "vld")
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
        ({kw.spark_num}, {kw.face_name}, {kw.otx_name}, {kw.inx_name})
        VALUES
          ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {blrawar_h_raw_put_tablename} WHERE {kw.face_name}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        update_sqlstr = create_update_heard_raw_existing_inx_col_sqlstr(
            "name", blrawar_h_raw_put_tablename, kw.face_name
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        select_face_name_only_sqlstr = f"""SELECT {kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx FROM {blrawar_h_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # spark5 does not link to spark7 translate record's
        assert rows == [
            (spark1, sue_otx, sue_inx),
            (spark2, yao_otx, None),
            (spark5, bob_otx, None),
        ]


def test_create_update_heard_raw_existing_inx_col_sqlstr_UpdatesTable_Scenario2_Different_spark_num_TranslateMappings():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_sue_inx = "BobSuzInx"
    bob_otx = "Bob"
    bob_inx0 = "Bobby"
    bob_inx7 = "Robert"
    yao_otx = "Yao"
    yao_inx = "Yaoito"
    spark0 = 0
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    spark8 = 8
    spark9 = 9

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blrawar_dimen = kw.belief_plan_awardunit
        blrawar_h_raw_put_tablename = prime_tbl(blrawar_dimen, "h", "raw", "put")
        print(f"{get_table_columns(cursor, blrawar_h_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {blrawar_h_raw_put_tablename}
        ({kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx)
        VALUES
          ({spark0}, '{bob_otx}', NULL)
        , ({spark1}, '{bob_otx}', NULL)
        , ({spark2}, '{yao_otx}', NULL)
        , ({spark5}, '{bob_otx}', NULL)
        , ({spark7}, '{bob_otx}', NULL)
        , ({spark9}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)

        trlname_dimen = kw.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s", "vld")
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
        ({kw.spark_num}, {kw.face_name}, {kw.otx_name}, {kw.inx_name})
        VALUES
          ({spark1}, '{bob_otx}', '{bob_otx}', '{bob_inx0}')
        , ({spark2}, '{yao_otx}', '{yao_otx}', '{yao_inx}')
        , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx7}')
        , ({spark7}, '{bob_otx}', '{sue_otx}', '{bob_sue_inx}')
        , ({spark8}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {blrawar_h_raw_put_tablename} WHERE {kw.face_name}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        update_sqlstr = create_update_heard_raw_existing_inx_col_sqlstr(
            "name", blrawar_h_raw_put_tablename, kw.face_name
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        select_face_name_only_sqlstr = f"""SELECT {kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx FROM {blrawar_h_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # spark5 does not link to spark7 translate record's
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
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trlname_s_vld_tablename = prime_tbl(kw.translate_name, "s", "vld")
        print(f"{trlname_s_vld_tablename=}")
        print(f"{get_table_columns(cursor, trlname_s_vld_tablename)=}")

        blrawar_dimen = kw.belief_plan_awardunit
        blrawar_h_raw_put_tablename = prime_tbl(blrawar_dimen, "h", "raw", "put")
        print(f"{get_table_columns(cursor, blrawar_h_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {blrawar_h_raw_put_tablename} ({kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx)
VALUES
  ({spark1}, '{sue_otx}', '{sue_inx}')
, ({spark2}, '{yao_otx}', NULL)
, ({spark5}, '{sue_otx}', NULL)
, ({spark7}, '{bob_otx}', '{bob_inx}')
;
"""
        cursor.execute(insert_face_name_only_sqlstr)
        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {blrawar_h_raw_put_tablename} WHERE {kw.face_name}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 2

        # WHEN
        update_sqlstr = create_update_heard_raw_empty_inx_col_sqlstr(
            blrawar_h_raw_put_tablename, kw.face_name
        )
        print(update_sqlstr)
        cursor.execute(update_sqlstr)

        # THEN
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 4
        select_face_name_only_sqlstr = f"""SELECT {kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx FROM {blrawar_h_raw_put_tablename}"""
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
    spark0 = 0
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    spark8 = 8
    spark9 = 9

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blrawar_dimen = kw.belief_plan_awardunit
        blrawar_h_raw_put_tablename = prime_tbl(blrawar_dimen, "h", "raw", "put")
        print(f"{get_table_columns(cursor, blrawar_h_raw_put_tablename)=}")
        insert_face_name_only_sqlstr = f"""INSERT INTO {blrawar_h_raw_put_tablename}
        ({kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx)
        VALUES
          ({spark0}, '{bob_otx}', NULL)
        , ({spark1}, '{bob_otx}', NULL)
        , ({spark2}, '{yao_otx}', NULL)
        , ({spark5}, '{bob_otx}', NULL)
        , ({spark7}, '{bob_otx}', NULL)
        , ({spark9}, '{bob_otx}', NULL)
        ;
        """
        cursor.execute(insert_face_name_only_sqlstr)

        trlname_dimen = kw.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s", "vld")
        print(f"{trlname_s_vld_tablename=}")
        insert_trlname_sqlstr = f"""INSERT INTO {trlname_s_vld_tablename}
        ({kw.spark_num}, {kw.face_name}, {kw.otx_name}, {kw.inx_name})
        VALUES
          ({spark1}, '{bob_otx}', '{bob_otx}', '{bob_inx0}')
        , ({spark2}, '{yao_otx}', '{yao_otx}', '{yao_inx}')
        , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx7}')
        , ({spark7}, '{bob_otx}', '{sue_otx}', '{bob_sue_inx}')
        , ({spark8}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        ;
        """
        cursor.execute(insert_trlname_sqlstr)

        face_name_inx_count_sql = f"SELECT COUNT(*) FROM {blrawar_h_raw_put_tablename} WHERE {kw.face_name}_inx IS NOT NULL"
        assert cursor.execute(face_name_inx_count_sql).fetchone()[0] == 0

        # WHEN
        set_all_heard_raw_inx_columns(cursor)

        # THEN
        select_face_name_only_sqlstr = f"""SELECT {kw.spark_num}, {kw.face_name}_otx, {kw.face_name}_inx FROM {blrawar_h_raw_put_tablename}"""
        cursor.execute(select_face_name_only_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # spark5 does not link to spark7 translate record's
        assert rows == [
            (0, bob_otx, bob_otx),
            (1, bob_otx, bob_inx0),
            (2, yao_otx, yao_inx),
            (5, bob_otx, bob_inx0),
            (7, bob_otx, bob_inx7),
            (9, bob_otx, bob_inx7),
        ]
