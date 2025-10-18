from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import get_row_count
from src.ch16_translate.translate_main import (
    default_knot_if_None,
    default_unknown_str_if_None,
)
from src.ch18_world_etl.tran_sqlstrs import (
    CREATE_TRLCORE_SOUND_AGG_SQLSTR,
    CREATE_TRLCORE_SOUND_RAW_SQLSTR,
    CREATE_TRLCORE_SOUND_VLD_SQLSTR,
    CREATE_TRLLABE_SOUND_AGG_SQLSTR,
    CREATE_TRLNAME_SOUND_AGG_SQLSTR,
    CREATE_TRLROPE_SOUND_AGG_SQLSTR,
    CREATE_TRLTITL_SOUND_AGG_SQLSTR,
    create_insert_into_translate_core_raw_sqlstr,
    create_insert_translate_sound_vld_table_sqlstr,
    create_prime_tablename,
    create_sound_and_heard_tables,
    create_update_translate_sound_agg_inconsist_sqlstr,
    create_update_trllabe_sound_agg_knot_error_sqlstr,
    create_update_trlname_sound_agg_knot_error_sqlstr,
    create_update_trlrope_sound_agg_knot_error_sqlstr,
    create_update_trltitl_sound_agg_knot_error_sqlstr,
)
from src.ch18_world_etl.transformers import (
    etl_translate_sound_agg_tables_to_translate_sound_vld_tables,
    insert_translate_core_agg_to_translate_core_vld_table,
    insert_translate_core_raw_to_translate_core_agg_table,
    insert_translate_sound_agg_into_translate_core_raw_table,
    insert_translate_sound_agg_tables_to_translate_sound_vld_table,
    populate_translate_core_vld_with_missing_face_names,
    update_inconsistency_translate_core_raw_table,
    update_translate_sound_agg_inconsist_errors,
    update_translate_sound_agg_knot_errors,
)
from src.ref.keywords import Ch18Keywords as wx


def test_create_insert_into_translate_core_raw_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    a23_str = "amy23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_TRLROPE_SOUND_AGG_SQLSTR)
        trlrope_dimen = wx.translate_rope
        translate_rope_s_agg_tablename = create_prime_tablename(
            trlrope_dimen, "s", "agg"
        )
        insert_into_clause = f"""INSERT INTO {translate_rope_s_agg_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.otx_rope}
, {wx.inx_rope}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({spark1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ({spark1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
, ({spark2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ({spark5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({spark7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_TRLCORE_SOUND_RAW_SQLSTR)
        translate_core_s_raw_tablename = create_prime_tablename("trlcore", "s", "raw")
        assert get_row_count(cursor, translate_core_s_raw_tablename) == 0

        # WHEN
        sqlstr = create_insert_into_translate_core_raw_sqlstr(trlrope_dimen)
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert get_row_count(cursor, translate_core_s_raw_tablename) == 3
        select_core_raw_sqlstr = f"SELECT * FROM {translate_core_s_raw_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        assert cursor.fetchall() == [
            (translate_rope_s_agg_tablename, "Sue", None, None, None, None),
            (translate_rope_s_agg_tablename, "Sue", ":", ":", "Unknown", None),
            (translate_rope_s_agg_tablename, "Yao", ":", ":", "Unknown", None),
        ]


def test_insert_translate_sound_agg_into_translate_core_raw_table_PopulatesTable_Scenario0():
    # ESTABLISH
    a23_str = "amy23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_TRLROPE_SOUND_AGG_SQLSTR)
        trlrope_dimen = wx.translate_rope
        translate_rope_s_agg_tablename = create_prime_tablename(
            trlrope_dimen, "s", "agg"
        )
        insert_into_clause = f"""INSERT INTO {translate_rope_s_agg_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.otx_rope}
, {wx.inx_rope}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({spark7}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({spark7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        cursor.execute(CREATE_TRLNAME_SOUND_AGG_SQLSTR)
        trlname_dimen = wx.translate_name
        translate_name_s_agg_tablename = create_prime_tablename(
            trlname_dimen, "s", "agg"
        )
        insert_into_clause = f"""INSERT INTO {translate_name_s_agg_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.otx_name}
, {wx.inx_name}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({spark7}, '{bob_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        create_sound_and_heard_tables(cursor)
        translate_core_s_raw_tablename = create_prime_tablename("trlcore", "s", "raw")
        assert get_row_count(cursor, translate_rope_s_agg_tablename) == 3
        assert get_row_count(cursor, translate_name_s_agg_tablename) == 2
        assert get_row_count(cursor, translate_core_s_raw_tablename) == 0

        # WHEN
        insert_translate_sound_agg_into_translate_core_raw_table(cursor)

        # THEN
        assert get_row_count(cursor, translate_core_s_raw_tablename) == 4
        select_core_raw_sqlstr = f"SELECT * FROM {translate_core_s_raw_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [
            (translate_name_s_agg_tablename, "Bob", ":", ":", "Unknown", None),
            (translate_name_s_agg_tablename, "Sue", None, None, None, None),
            (translate_rope_s_agg_tablename, "Sue", None, None, None, None),
            (translate_rope_s_agg_tablename, "Yao", ":", ":", "Unknown", None),
        ]


def test_update_inconsistency_translate_core_raw_table_UpdatesTable_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_knot = "/"
    ukx = "Unknown"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_TRLCORE_SOUND_RAW_SQLSTR)
        trlrope_dimen = wx.translate_rope
        translate_rope_s_agg_tablename = create_prime_tablename(
            trlrope_dimen, "s", "agg"
        )
        trlname_dimen = wx.translate_name
        translate_name_s_agg_tablename = create_prime_tablename(
            trlname_dimen, "s", "agg"
        )
        trlcore_dimen = wx.translate_core
        translate_core_s_raw_tablename = create_prime_tablename(
            trlcore_dimen, "s", "raw"
        )
        insert_into_clause = f"""INSERT INTO {translate_core_s_raw_tablename} (
  source_dimen
, {wx.face_name}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
, {wx.error_message}
)"""
        values_clause = f"""
VALUES
  ('{translate_name_s_agg_tablename}', "{bob_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
, ('{translate_name_s_agg_tablename}', "{sue_str}", NULL, NULL, '{rdx}', NULL)
, ('{translate_rope_s_agg_tablename}', "{sue_str}", NULL, NULL, '{other_knot}', NULL)
, ('{translate_rope_s_agg_tablename}', "{yao_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        create_sound_and_heard_tables(cursor)
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {translate_core_s_raw_tablename} WHERE {wx.error_message} IS NOT NULL;"
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        update_inconsistency_translate_core_raw_table(cursor)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 2
        select_core_raw_sqlstr = f"SELECT * FROM {translate_core_s_raw_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        error_data_str = "Inconsistent data"
        assert rows == [
            (translate_name_s_agg_tablename, "Bob", ":", ":", "Unknown", None),
            (translate_name_s_agg_tablename, "Sue", None, None, ":", error_data_str),
            (translate_rope_s_agg_tablename, "Sue", None, None, "/", error_data_str),
            (translate_rope_s_agg_tablename, "Yao", ":", ":", "Unknown", None),
        ]


def test_insert_translate_core_raw_to_translate_core_agg_table_PopulatesTable_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_knot = "/"
    ukx = "Unknown"
    error_data_str = "Inconsistent data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_TRLCORE_SOUND_RAW_SQLSTR)
        trlrope_dimen = wx.translate_rope
        translate_rope_s_agg_tablename = create_prime_tablename(
            trlrope_dimen, "s", "agg"
        )
        trlname_dimen = wx.translate_name
        translate_name_s_agg_tablename = create_prime_tablename(
            trlname_dimen, "s", "agg"
        )
        trlcore_dimen = wx.translate_core
        translate_core_s_raw_tablename = create_prime_tablename(
            trlcore_dimen, "s", "raw"
        )
        insert_into_clause = f"""INSERT INTO {translate_core_s_raw_tablename} (
  source_dimen
, {wx.face_name}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
, {wx.error_message}
)"""
        values_clause = f"""
VALUES
  ('{translate_name_s_agg_tablename}', "{bob_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
, ('{translate_name_s_agg_tablename}', "{sue_str}", NULL, NULL, '{rdx}', '{error_data_str}')
, ('{translate_rope_s_agg_tablename}', "{sue_str}", NULL, NULL, '{other_knot}', '{error_data_str}')
, ('{translate_rope_s_agg_tablename}', "{yao_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        create_sound_and_heard_tables(cursor)
        translate_core_s_agg_tablename = create_prime_tablename(
            trlcore_dimen, "s", "agg"
        )
        assert get_row_count(cursor, translate_core_s_agg_tablename) == 0

        # WHEN
        insert_translate_core_raw_to_translate_core_agg_table(cursor)

        # THEN
        assert get_row_count(cursor, translate_core_s_agg_tablename) == 2
        select_core_raw_sqlstr = f"SELECT * FROM {translate_core_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [(bob_str, rdx, rdx, ukx), (yao_str, rdx, rdx, ukx)]


def test_insert_translate_core_agg_to_translate_core_vld_table_PopulatesTable_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "zia"
    colon_knot = ":"
    slash_knot = "/"
    other_knot = "="
    unknown_str = "Unknown"
    huh_str = "Huh"
    default_knot = default_knot_if_None()
    default_unknown = default_unknown_str_if_None()

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_TRLCORE_SOUND_AGG_SQLSTR)
        trlcore_dimen = wx.translate_core
        translate_core_s_agg_tablename = create_prime_tablename(
            trlcore_dimen, "s", "agg"
        )
        insert_into_clause = f"""INSERT INTO {translate_core_s_agg_tablename} (
  {wx.face_name}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)"""
        values_clause = f"""
VALUES
  ("{bob_str}", "{colon_knot}", "{slash_knot}", "{unknown_str}")
, ("{sue_str}", NULL, NULL, NULL)
, ("{yao_str}", NULL, '{colon_knot}', '{huh_str}')
, ("{zia_str}", "{colon_knot}", "{colon_knot}", "{huh_str}")
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
        translate_core_s_vld_tablename = create_prime_tablename(
            trlcore_dimen, "s", "vld"
        )
        assert get_row_count(cursor, translate_core_s_vld_tablename) == 0

        # WHEN
        insert_translate_core_agg_to_translate_core_vld_table(cursor)

        # THEN
        assert get_row_count(cursor, translate_core_s_vld_tablename) == 4
        select_core_raw_sqlstr = f"SELECT * FROM {translate_core_s_vld_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [
            (bob_str, colon_knot, slash_knot, unknown_str),
            (sue_str, default_knot, default_knot, default_unknown),
            (yao_str, default_knot, colon_knot, huh_str),
            (zia_str, colon_knot, colon_knot, huh_str),
        ]


def test_create_update_translate_sound_agg_inconsist_sqlstr_PopulatesTable_Scenario0():
    # ESTABLISH
    a23_str = "amy23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_knot = "/"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    error_translate_str = "Inconsistent translate core data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_TRLROPE_SOUND_AGG_SQLSTR)
        trlrope_dimen = wx.translate_rope
        translate_rope_s_agg_tablename = create_prime_tablename(
            trlrope_dimen, "s", "agg"
        )
        insert_into_clause = f"""INSERT INTO {translate_rope_s_agg_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.otx_rope}
, {wx.inx_rope}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({spark1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ({spark1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_knot}', NULL)
, ({spark2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ({spark5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({spark7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
        print(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
        translate_core_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        insert_into_clause = f"""INSERT INTO {translate_core_s_vld_tablename} (
  {wx.face_name}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)"""
        values_clause = f"""
VALUES
  ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {translate_rope_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_update_translate_sound_agg_inconsist_sqlstr(trlrope_dimen)
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 5
        select_core_raw_sqlstr = f"SELECT * FROM {translate_rope_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, yao_str, yao_inx, None, None, None, error_translate_str),
            (1, sue_str, bob_str, bob_inx, None, None, None, error_translate_str),
            (1, sue_str, bob_str, bob_str, None, "/", None, error_translate_str),
            (2, sue_str, sue_str, sue_str, ":", ":", "Unknown", error_translate_str),
            (5, sue_str, bob_str, bob_inx, ":", ":", "Unknown", error_translate_str),
            (7, yao_str, yao_str, yao_inx, ":", ":", "Unknown", None),
        ]


def test_update_translate_sound_agg_inconsist_errors_PopulatesTable_Scenario1():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_knot = "/"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    error_translate_str = "Inconsistent translate core data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trlrope_dimen = wx.translate_rope
        translate_rope_s_agg_tablename = create_prime_tablename(
            trlrope_dimen, "s", "agg"
        )
        insert_into_clause = f"""INSERT INTO {translate_rope_s_agg_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.otx_rope}
, {wx.inx_rope}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({spark1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ({spark1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_knot}', NULL)
, ({spark2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ({spark5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({spark7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        translate_core_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        insert_into_clause = f"""INSERT INTO {translate_core_s_vld_tablename} (
  {wx.face_name}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)"""
        values_clause = f"""
VALUES
  ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {translate_rope_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        update_translate_sound_agg_inconsist_errors(cursor)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 5
        select_core_raw_sqlstr = f"SELECT * FROM {translate_rope_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, yao_str, yao_inx, None, None, None, error_translate_str),
            (1, sue_str, bob_str, bob_inx, None, None, None, error_translate_str),
            (1, sue_str, bob_str, bob_str, None, "/", None, error_translate_str),
            (2, sue_str, sue_str, sue_str, ":", ":", "Unknown", error_translate_str),
            (5, sue_str, bob_str, bob_inx, ":", ":", "Unknown", error_translate_str),
            (7, yao_str, yao_str, yao_inx, ":", ":", "Unknown", None),
        ]


def test_create_update_trllabe_sound_agg_knot_error_sqlstr_PopulatesTable_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    ski_str = "Ski"
    run_str = "Run"
    fly_str = "Fly"
    fly_inx = "fli"
    ski_inx = "Skiito"
    rdx = ":"
    run_rdx_run = f"{run_str}{rdx}{run_str}"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    spark9 = 9
    error_label_str = "Knot cannot exist in LabelTerm"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_TRLLABE_SOUND_AGG_SQLSTR)
        trllabe_dimen = wx.translate_label
        trllabe_s_agg_tablename = create_prime_tablename(trllabe_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {trllabe_s_agg_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.otx_label}
, {wx.inx_label}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{bob_str}', '{fly_str}', '{fly_inx}')
, ({spark1}, '{bob_str}', '{ski_str}{rdx}', '{ski_str}')
, ({spark2}, '{bob_str}', '{run_rdx_run}', '{run_str}')
, ({spark5}, '{yao_str}', '{ski_str}', '{ski_inx}{rdx}')
, ({spark7}, '{yao_str}', '{fly_str}', '{fly_inx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
        translate_core_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {translate_core_s_vld_tablename} (
  {wx.face_name}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)
VALUES
  ('{bob_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(insert_sqlstr)
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {trllabe_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"

        testing_select_sqlstr = """
  SELECT label_agg.rowid, label_agg.otx_label, label_agg.inx_label, *
  FROM translate_label_s_agg label_agg
  JOIN translate_core_s_vld core_vld ON core_vld.face_name = label_agg.face_name
  WHERE label_agg.otx_label LIKE '%' || core_vld.otx_knot || '%'
      OR label_agg.inx_label LIKE '%' || core_vld.inx_knot || '%'
"""
        print(cursor.execute(testing_select_sqlstr).fetchall())

        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_update_trllabe_sound_agg_knot_error_sqlstr()
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 3
        select_core_raw_sqlstr = f"SELECT * FROM {trllabe_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        error_x = error_label_str
        exp_row0 = (1, bob_str, fly_str, fly_inx, None, None, None, None)
        exp_row1 = (1, bob_str, f"{ski_str}{rdx}", ski_str, None, None, None, error_x)
        exp_row2 = (2, bob_str, run_rdx_run, run_str, None, None, None, error_x)
        exp_row3 = (5, yao_str, ski_str, f"{ski_inx}{rdx}", None, None, None, error_x)
        exp_row4 = (7, yao_str, fly_str, fly_inx, None, None, None, None)
        assert rows[0] == exp_row0
        assert rows[1] == exp_row1
        assert rows[2] == exp_row2
        assert rows[3] == exp_row3
        assert rows[4] == exp_row4
        assert rows == [exp_row0, exp_row1, exp_row2, exp_row3, exp_row4]


def test_create_update_trlrope_sound_agg_knot_error_sqlstr_PopulatesTable_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    rdx = ":"
    ski_str = f"{rdx}Ski"
    spt_run_str = f"{rdx}sports{rdx}Run"
    spt_fly_str = f"{rdx}sports{rdx}Fly"
    bad_fly_str = f"sports{rdx}fli"
    bad_ski_str = "Skiito"
    bad_run_str = f"run{rdx}run"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    spark9 = 9
    error_rope_str = "Knot must exist in RopeTerm"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_TRLROPE_SOUND_AGG_SQLSTR)
        trlrope_dimen = wx.translate_rope
        trlrope_s_agg_tablename = create_prime_tablename(trlrope_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {trlrope_s_agg_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.otx_rope}
, {wx.inx_rope}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{bob_str}', '{spt_run_str}', '{spt_run_str}')
, ({spark1}, '{bob_str}', '{spt_fly_str}', '{bad_fly_str}')
, ({spark2}, '{bob_str}', '{bad_fly_str}', '{spt_fly_str}')
, ({spark5}, '{yao_str}', '{bad_ski_str}', '{bad_ski_str}')
, ({spark7}, '{yao_str}', '{spt_run_str}', '{bad_run_str}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
        translate_core_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {translate_core_s_vld_tablename} (
  {wx.face_name}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)
VALUES
  ('{bob_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(insert_sqlstr)
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {trlrope_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"

        testing_select_sqlstr = """
  SELECT rope_agg.rowid, rope_agg.otx_rope, rope_agg.inx_rope
  FROM translate_rope_s_agg rope_agg
  JOIN translate_core_s_vld core_vld ON core_vld.face_name = rope_agg.face_name
  WHERE NOT rope_agg.otx_rope LIKE core_vld.otx_knot || '%'
     OR NOT rope_agg.inx_rope LIKE core_vld.inx_knot || '%'
  """

        print(cursor.execute(testing_select_sqlstr).fetchall())

        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_update_trlrope_sound_agg_knot_error_sqlstr()
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 4
        select_core_raw_sqlstr = f"SELECT * FROM {trlrope_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        error_x = error_rope_str
        exp_row0 = (1, bob_str, spt_run_str, spt_run_str, None, None, None, None)
        exp_row1 = (1, bob_str, spt_fly_str, bad_fly_str, None, None, None, error_x)
        exp_row2 = (2, bob_str, bad_fly_str, spt_fly_str, None, None, None, error_x)
        exp_row3 = (5, yao_str, bad_ski_str, bad_ski_str, None, None, None, error_x)
        exp_row4 = (7, yao_str, spt_run_str, bad_run_str, None, None, None, error_x)
        assert rows[0] == exp_row0
        assert rows[1] == exp_row1
        assert rows[2] == exp_row2
        assert rows[3] == exp_row3
        assert rows[4] == exp_row4
        assert rows == [exp_row0, exp_row1, exp_row2, exp_row3, exp_row4]


def test_create_update_trlname_sound_agg_knot_error_sqlstr_PopulatesTable_Scenario0():
    # ESTABLISH
    rdx = ":"
    bob_str = "Bob"
    yao_str = "Yao"
    sue_otx = "Sue"
    sue_inx = "Susy"
    bad_sue_inx = f"Susy{rdx}"
    zia_otx = "Zia"
    bad_zia_otx = f"{rdx}Zia"
    zia_inx = "Ziaita"
    bad_zia_inx = f"Zia{rdx}"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    spark9 = 9
    error_name_str = "Knot cannot exist in NameTerm"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_TRLNAME_SOUND_AGG_SQLSTR)
        trlname_dimen = wx.translate_name
        trlname_s_agg_tablename = create_prime_tablename(trlname_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {trlname_s_agg_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.otx_name}
, {wx.inx_name}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{bob_str}', '{sue_otx}', '{sue_inx}')
, ({spark1}, '{bob_str}', '{sue_otx}', '{bad_sue_inx}')
, ({spark2}, '{bob_str}', '{zia_otx}', '{bad_zia_inx}')
, ({spark5}, '{yao_str}', '{bad_zia_otx}', '{bad_zia_inx}')
, ({spark7}, '{yao_str}', '{bad_zia_otx}', '{zia_inx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
        translate_core_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {translate_core_s_vld_tablename} (
  {wx.face_name}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)
VALUES
  ('{bob_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(insert_sqlstr)
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {trlname_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"

        testing_select_sqlstr = """
  SELECT name_agg.rowid, name_agg.otx_name, name_agg.inx_name
  FROM translate_name_s_agg name_agg
  JOIN translate_core_s_vld core_vld ON core_vld.face_name = name_agg.face_name
  WHERE NOT name_agg.otx_name LIKE core_vld.otx_knot || '%'
     OR NOT name_agg.inx_name LIKE core_vld.inx_knot || '%'
  """

        print(cursor.execute(testing_select_sqlstr).fetchall())

        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_update_trlname_sound_agg_knot_error_sqlstr()
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 4
        select_core_raw_sqlstr = f"SELECT * FROM {trlname_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        error_x = error_name_str
        exp_row0 = (1, bob_str, sue_otx, sue_inx, None, None, None, None)
        exp_row1 = (1, bob_str, sue_otx, bad_sue_inx, None, None, None, error_x)
        exp_row2 = (2, bob_str, zia_otx, bad_zia_inx, None, None, None, error_x)
        exp_row3 = (5, yao_str, bad_zia_otx, bad_zia_inx, None, None, None, error_x)
        exp_row4 = (7, yao_str, bad_zia_otx, zia_inx, None, None, None, error_x)
        assert rows[0] == exp_row0
        assert rows[1] == exp_row1
        assert rows[2] == exp_row2
        assert rows[3] == exp_row3
        assert rows[4] == exp_row4
        assert rows == [exp_row0, exp_row1, exp_row2, exp_row3, exp_row4]


def test_create_update_trltitl_sound_agg_knot_error_sqlstr_PopulatesTable_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    rdx_inx = ":"
    rdx_otx = "<"
    sue_inx = "Sue"
    sue_otx = "Suzy"
    bad_sue_otx = f"{rdx_otx}Suzy"
    swim_inx = f"{rdx_inx}swimmers"
    swim_otx = f"{rdx_otx}swimmers"
    bad_swim_otx = "swimmers"
    bad_swim_inx = "swimmers"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    spark9 = 9
    error_title_str = "Otx and inx titles must match knot."

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_TRLTITL_SOUND_AGG_SQLSTR)
        trltitl_dimen = wx.translate_title
        trltitl_s_agg_tablename = create_prime_tablename(trltitl_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {trltitl_s_agg_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.otx_title}
, {wx.inx_title}
)"""
        # TODO create values where errors will appear: groups should map to groups,
        values_clause = f"""
VALUES
  ({spark1}, '{bob_str}', '{sue_otx}', '{sue_inx}')
, ({spark1}, '{yao_str}', '{bad_sue_otx}', '{sue_inx}')
, ({spark2}, '{bob_str}', '{swim_otx}', '{swim_inx}')
, ({spark5}, '{yao_str}', '{swim_otx}', '{bad_swim_inx}')
, ({spark7}, '{yao_str}', '{bad_swim_otx}', '{swim_inx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
        translate_core_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {translate_core_s_vld_tablename} (
  {wx.face_name}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)
VALUES
  ('{bob_str}', '{rdx_otx}', '{rdx_inx}', '{ukx}')
, ('{yao_str}', '{rdx_otx}', '{rdx_inx}', '{ukx}')
;
"""
        cursor.execute(insert_sqlstr)
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {trltitl_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"

        testing_select_sqlstr = """
  SELECT title_agg.rowid, title_agg.otx_title, title_agg.inx_title
  FROM translate_title_s_agg title_agg
  JOIN translate_core_s_vld core_vld ON core_vld.face_name = title_agg.face_name
  WHERE NOT ((
            title_agg.otx_title LIKE core_vld.otx_knot || '%' 
        AND title_agg.inx_title LIKE core_vld.inx_knot || '%') 
      OR (
            NOT title_agg.otx_title LIKE core_vld.otx_knot || '%'
        AND NOT title_agg.inx_title LIKE core_vld.inx_knot || '%'
        ))
        """

        print(cursor.execute(testing_select_sqlstr).fetchall())

        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_update_trltitl_sound_agg_knot_error_sqlstr()
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 3
        select_core_raw_sqlstr = f"SELECT * FROM {trltitl_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        error_x = error_title_str
        exp_row0 = (1, bob_str, sue_otx, sue_inx, None, None, None, None)
        exp_row1 = (1, yao_str, bad_sue_otx, sue_inx, None, None, None, error_x)
        exp_row2 = (2, bob_str, swim_otx, swim_inx, None, None, None, None)
        exp_row3 = (5, yao_str, swim_otx, bad_swim_inx, None, None, None, error_x)
        exp_row4 = (7, yao_str, bad_swim_otx, swim_inx, None, None, None, error_x)
        assert rows[0] == exp_row0
        assert rows[1] == exp_row1
        print(f" {rows[2]=}")
        print(f"{exp_row2=}")
        assert rows[2] == exp_row2
        assert rows[3] == exp_row3
        assert rows[4] == exp_row4
        assert rows == [exp_row0, exp_row1, exp_row2, exp_row3, exp_row4]


def test_update_translate_sound_agg_knot_errors_UpdatesTables_Scenario0():
    # ESTABLISH
    bob_str = "bob"
    casa_str = "Casa"
    rdx = ":"
    ukx = "Unknown"
    sue_inx = "Sue"
    bad_sue_otx = f"{rdx}Suzy"
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_TRLLABE_SOUND_AGG_SQLSTR)
        cursor.execute(CREATE_TRLROPE_SOUND_AGG_SQLSTR)
        cursor.execute(CREATE_TRLNAME_SOUND_AGG_SQLSTR)
        cursor.execute(CREATE_TRLTITL_SOUND_AGG_SQLSTR)
        trllabe_s_agg_tablename = create_prime_tablename(wx.translate_label, "s", "agg")
        trlrope_s_agg_tablename = create_prime_tablename(wx.translate_rope, "s", "agg")
        trlname_s_agg_tablename = create_prime_tablename(wx.translate_name, "s", "agg")
        trltitl_s_agg_tablename = create_prime_tablename(wx.translate_title, "s", "agg")
        insert_trllabe_sqlstr = f"""
INSERT INTO {trllabe_s_agg_tablename} ({wx.spark_num}, {wx.face_name}, {wx.otx_label}, {wx.inx_label})
VALUES ({spark1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
        insert_trlrope_sqlstr = f"""
INSERT INTO {trlrope_s_agg_tablename} ({wx.spark_num}, {wx.face_name}, {wx.otx_rope}, {wx.inx_rope})
VALUES ({spark1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
        insert_trlname_sqlstr = f"""
INSERT INTO {trlname_s_agg_tablename} ({wx.spark_num}, {wx.face_name}, {wx.otx_name}, {wx.inx_name})
VALUES ({spark1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
        insert_trltitl_sqlstr = f"""
INSERT INTO {trltitl_s_agg_tablename} ({wx.spark_num}, {wx.face_name}, {wx.otx_title}, {wx.inx_title})
VALUES ({spark1}, '{bob_str}', '{bad_sue_otx}', '{sue_inx}');"""
        cursor.execute(insert_trllabe_sqlstr)
        cursor.execute(insert_trlrope_sqlstr)
        cursor.execute(insert_trlname_sqlstr)
        cursor.execute(insert_trltitl_sqlstr)

        trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        cursor.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
        insert_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename} (
{wx.face_name}, {wx.otx_knot}, {wx.inx_knot}, {wx.unknown_str})
VALUES ('{bob_str}', '{rdx}', '{rdx}', '{ukx}');"""
        cursor.execute(insert_sqlstr)
        trllabe_error_count_sqlstr = f"SELECT COUNT(*) FROM {trllabe_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"
        trlrope_error_count_sqlstr = f"SELECT COUNT(*) FROM {trlrope_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"
        trlname_error_count_sqlstr = f"SELECT COUNT(*) FROM {trlname_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"
        trltitl_error_count_sqlstr = f"SELECT COUNT(*) FROM {trltitl_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"
        assert cursor.execute(trllabe_error_count_sqlstr).fetchone()[0] == 0
        assert cursor.execute(trlrope_error_count_sqlstr).fetchone()[0] == 0
        assert cursor.execute(trlname_error_count_sqlstr).fetchone()[0] == 0
        assert cursor.execute(trltitl_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        update_translate_sound_agg_knot_errors(cursor)

        # THEN
        assert cursor.execute(trllabe_error_count_sqlstr).fetchone()[0] == 1
        assert cursor.execute(trlrope_error_count_sqlstr).fetchone()[0] == 1
        assert cursor.execute(trlname_error_count_sqlstr).fetchone()[0] == 1
        assert cursor.execute(trltitl_error_count_sqlstr).fetchone()[0] == 1
        assert get_row_count(cursor, trltitl_s_agg_tablename) == 1
        select_core_raw_sqlstr = f"SELECT {wx.spark_num}, {wx.face_name}, {wx.otx_label}, {wx.inx_label} FROM {trllabe_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        exp_row0 = (1, bob_str, f"{casa_str}{rdx}", casa_str)
        assert rows[0] == exp_row0
        assert rows == [exp_row0]


def test_create_insert_translate_sound_vld_table_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_knot = "/"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    error_translate_str = "Inconsistent translate core data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trlrope_dimen = wx.translate_rope
        translate_rope_s_agg_tablename = create_prime_tablename(
            trlrope_dimen, "s", "agg"
        )
        insert_into_clause = f"""INSERT INTO {translate_rope_s_agg_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.otx_rope}
, {wx.inx_rope}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
, {wx.error_message}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL, '{error_translate_str}')
, ({spark1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL, '{error_translate_str}')
, ({spark1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_knot}', NULL, '{error_translate_str}')
, ({spark2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', '{error_translate_str}')
, ({spark5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', '{error_translate_str}')
, ({spark1}, '{yao_str}', '{yao_str}', '{yao_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ({spark7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ({spark7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}', NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        translate_rope_s_vld_tablename = create_prime_tablename("trlrope", "s", "vld")
        assert get_row_count(cursor, translate_rope_s_agg_tablename) == 8
        assert get_row_count(cursor, translate_rope_s_vld_tablename) == 0

        # WHEN
        sqlstr = create_insert_translate_sound_vld_table_sqlstr(trlrope_dimen)
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert get_row_count(cursor, translate_rope_s_vld_tablename) == 3
        select_translate_rope_s_vld_sqlstr = (
            f"SELECT * FROM {translate_rope_s_vld_tablename}"
        )
        cursor.execute(select_translate_rope_s_vld_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (spark1, yao_str, yao_str, yao_str),
            (spark7, bob_str, bob_str, bob_inx),
            (spark7, yao_str, yao_str, yao_inx),
        ]


def test_insert_translate_sound_agg_tables_to_translate_sound_vld_table_PopulatesTable_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_knot = "/"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7
    error_translate_str = "Inconsistent translate core data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trlrope_dimen = wx.translate_rope
        translate_rope_s_agg_tablename = create_prime_tablename(
            trlrope_dimen, "s", "agg"
        )
        insert_into_clause = f"""INSERT INTO {translate_rope_s_agg_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.otx_rope}
, {wx.inx_rope}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
, {wx.error_message}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL, '{error_translate_str}')
, ({spark1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL, '{error_translate_str}')
, ({spark1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_knot}', NULL, '{error_translate_str}')
, ({spark2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', '{error_translate_str}')
, ({spark5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', '{error_translate_str}')
, ({spark1}, '{yao_str}', '{yao_str}', '{yao_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ({spark7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ({spark7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}', NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        translate_rope_s_vld_tablename = create_prime_tablename("trlrope", "s", "vld")
        assert get_row_count(cursor, translate_rope_s_agg_tablename) == 8
        assert get_row_count(cursor, translate_rope_s_vld_tablename) == 0

        # WHEN
        insert_translate_sound_agg_tables_to_translate_sound_vld_table(cursor)

        # THEN
        assert get_row_count(cursor, translate_rope_s_vld_tablename) == 3
        select_translate_rope_s_vld_sqlstr = (
            f"SELECT * FROM {translate_rope_s_vld_tablename}"
        )
        cursor.execute(select_translate_rope_s_vld_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (spark1, yao_str, yao_str, yao_str),
            (spark7, bob_str, bob_str, bob_inx),
            (spark7, yao_str, yao_str, yao_inx),
        ]


def test_etl_translate_sound_agg_tables_to_translate_sound_vld_tables_Scenario0_PopulatesTable():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_knot = "/"
    ukx = "Unknown"
    spark1 = 1
    spark2 = 2
    spark5 = 5
    spark7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trlname_dimen = wx.translate_name
        translate_name_s_agg_tablename = create_prime_tablename(
            trlname_dimen, "s", "agg"
        )
        insert_into_clause = f"""INSERT INTO {translate_name_s_agg_tablename} (
  {wx.spark_num}
, {wx.face_name}
, {wx.otx_name}
, {wx.inx_name}
, {wx.otx_knot}
, {wx.inx_knot}
, {wx.unknown_str}
)"""
        values_clause = f"""
VALUES
  ({spark1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({spark1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ({spark1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_knot}', NULL)
, ({spark2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ({spark5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({spark1}, '{yao_str}', '{yao_str}', '{yao_str}', '{rdx}', '{rdx}', '{ukx}')
, ({spark7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', NULL)
, ({spark7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({spark7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}')
, ({spark7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        insert_translate_sound_agg_into_translate_core_raw_table(cursor)
        translate_core_s_raw_tablename = create_prime_tablename("trlcore", "s", "raw")
        translate_core_s_agg_tablename = create_prime_tablename("trlcore", "s", "agg")
        translate_name_s_vld_tablename = create_prime_tablename("trlname", "s", "vld")
        assert get_row_count(cursor, translate_name_s_agg_tablename) == 10
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {translate_name_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0
        assert get_row_count(cursor, translate_core_s_raw_tablename) == 6
        assert get_row_count(cursor, translate_core_s_agg_tablename) == 0
        assert get_row_count(cursor, translate_name_s_vld_tablename) == 0

        # WHEN
        etl_translate_sound_agg_tables_to_translate_sound_vld_tables(cursor)

        # THEN
        translate_name_s_agg_select = f"SELECT * FROM {translate_name_s_agg_tablename};"
        print(f"{cursor.execute(translate_name_s_agg_select).fetchall()=}\n")
        translate_core_s_raw_select = f"SELECT * FROM {translate_core_s_raw_tablename};"
        print(f"{cursor.execute(translate_core_s_raw_select).fetchall()=}\n")
        translate_core_s_agg_select = f"SELECT * FROM {translate_core_s_agg_tablename};"
        print(f"{cursor.execute(translate_core_s_agg_select).fetchall()=}\n")
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 5
        assert get_row_count(cursor, translate_core_s_agg_tablename) == 2
        assert get_row_count(cursor, translate_name_s_vld_tablename) == 3
        select_translate_name_s_vld_sqlstr = (
            f"SELECT * FROM {translate_name_s_vld_tablename}"
        )
        cursor.execute(select_translate_name_s_vld_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (spark1, yao_str, yao_str, yao_str),
            (spark7, bob_str, bob_str, bob_inx),
            (spark7, yao_str, yao_str, yao_inx),
        ]


def test_etl_translate_sound_agg_tables_to_translate_sound_vld_tables_Scenario1_UpdatesErrors():
    # ESTABLISH
    bob_str = "bob"
    casa_str = "Casa"
    rdx = ":"
    ukx = "Unknown"
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trllabe_s_agg_tablename = create_prime_tablename(wx.translate_label, "s", "agg")
        trlrope_s_agg_tablename = create_prime_tablename(wx.translate_rope, "s", "agg")
        trlname_s_agg_tablename = create_prime_tablename(wx.translate_name, "s", "agg")
        insert_trllabe_sqlstr = f"""
INSERT INTO {trllabe_s_agg_tablename} ({wx.spark_num}, {wx.face_name}, {wx.otx_label}, {wx.inx_label})
VALUES ({spark1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
        insert_trlrope_sqlstr = f"""
INSERT INTO {trlrope_s_agg_tablename} ({wx.spark_num}, {wx.face_name}, {wx.otx_rope}, {wx.inx_rope})
VALUES ({spark1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
        insert_trlname_sqlstr = f"""
INSERT INTO {trlname_s_agg_tablename} ({wx.spark_num}, {wx.face_name}, {wx.otx_name}, {wx.inx_name})
VALUES ({spark1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
        cursor.execute(insert_trllabe_sqlstr)
        cursor.execute(insert_trlrope_sqlstr)
        cursor.execute(insert_trlname_sqlstr)

        trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename} (
{wx.face_name}, {wx.otx_knot}, {wx.inx_knot}, {wx.unknown_str})
VALUES ('{bob_str}', '{rdx}', '{rdx}', '{ukx}');"""
        cursor.execute(insert_sqlstr)
        trllabe_error_count_sqlstr = f"SELECT COUNT(*) FROM {trllabe_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"
        trlrope_error_count_sqlstr = f"SELECT COUNT(*) FROM {trlrope_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"
        trlname_error_count_sqlstr = f"SELECT COUNT(*) FROM {trlname_s_agg_tablename} WHERE {wx.error_message} IS NOT NULL;"
        assert cursor.execute(trllabe_error_count_sqlstr).fetchone()[0] == 0
        assert cursor.execute(trlrope_error_count_sqlstr).fetchone()[0] == 0
        assert cursor.execute(trlname_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        etl_translate_sound_agg_tables_to_translate_sound_vld_tables(cursor)

        # THEN
        assert cursor.execute(trllabe_error_count_sqlstr).fetchone()[0] == 1
        assert cursor.execute(trlrope_error_count_sqlstr).fetchone()[0] == 1
        assert cursor.execute(trlname_error_count_sqlstr).fetchone()[0] == 1
        select_core_raw_sqlstr = f"SELECT {wx.spark_num}, {wx.face_name}, {wx.otx_label}, {wx.inx_label} FROM {trllabe_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        exp_row0 = (1, bob_str, f"{casa_str}{rdx}", casa_str)
        assert rows[0] == exp_row0
        assert rows == [exp_row0]


def test_populate_translate_core_vld_with_missing_face_names_Scenario0_Populates1MissingTranslateCoreRow():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    casa_str = "Casa"
    rdx = ":"
    ukx = "Unknown"
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blrpern_str = wx.belief_voiceunit
        blrpern_s_agg_tablename = create_prime_tablename(blrpern_str, "s", "agg", "put")
        insert_blrpern_sqlstr = f"""
INSERT INTO {blrpern_s_agg_tablename} ({wx.spark_num}, {wx.face_name}, {wx.belief_name}, {wx.voice_name})
VALUES ({spark1}, '{bob_str}', '{bob_str}', '{bob_str}');"""
        cursor.execute(insert_blrpern_sqlstr)

        trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        assert get_row_count(cursor, trlcore_s_vld_tablename) == 0

        # WHEN
        populate_translate_core_vld_with_missing_face_names(cursor)

        # THEN
        assert get_row_count(cursor, trlcore_s_vld_tablename) == 1
        select_core_vld_sqlstr = f"SELECT {wx.face_name}, {wx.otx_knot}, {wx.inx_knot}, {wx.unknown_str} FROM {trlcore_s_vld_tablename}"
        cursor.execute(select_core_vld_sqlstr)
        rows = cursor.fetchall()
        x_knot = default_knot_if_None()
        exp_row0 = (bob_str, x_knot, x_knot, default_unknown_str_if_None())
        assert rows[0] == exp_row0
        assert rows == [exp_row0]


def test_populate_translate_core_vld_with_missing_face_names_Scenario1_PopulatesSomeMissingTranslateCoreRows():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    rdx = ":"
    ukx = "Unknown"
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blrpern_str = wx.belief_voiceunit
        blrpern_s_agg_tablename = create_prime_tablename(blrpern_str, "s", "agg", "put")
        insert_blrpern_sqlstr = f"""
INSERT INTO {blrpern_s_agg_tablename} ({wx.spark_num}, {wx.face_name}, {wx.belief_name}, {wx.voice_name})
VALUES ({spark1}, '{bob_str}', '{bob_str}', '{bob_str}'), ({spark1}, '{yao_str}', '{yao_str}', '{yao_str}');"""
        cursor.execute(insert_blrpern_sqlstr)

        trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename} (
{wx.face_name}, {wx.otx_knot}, {wx.inx_knot}, {wx.unknown_str})
VALUES ('{bob_str}', '{rdx}', '{rdx}', '{ukx}');"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, trlcore_s_vld_tablename) == 1

        # WHEN
        populate_translate_core_vld_with_missing_face_names(cursor)

        # THEN
        assert get_row_count(cursor, trlcore_s_vld_tablename) == 2
        select_core_vld_sqlstr = f"SELECT {wx.face_name}, {wx.otx_knot}, {wx.inx_knot}, {wx.unknown_str} FROM {trlcore_s_vld_tablename} ORDER BY {wx.face_name}"
        cursor.execute(select_core_vld_sqlstr)
        rows = cursor.fetchall()
        default_knot = default_knot_if_None()
        default_unknown = default_unknown_str_if_None()
        exp_row0 = (bob_str, rdx, rdx, ukx)
        exp_row1 = (yao_str, default_knot, default_knot, default_unknown)
        assert rows[0] == exp_row0
        assert rows[1] == exp_row1
        assert rows == [exp_row0, exp_row1]


def test_etl_translate_sound_agg_tables_to_translate_sound_vld_tables_Scenario2_Populates1MissingTranslateCoreRow():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    casa_str = "Casa"
    rdx = ":"
    ukx = "Unknown"
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blrpern_str = wx.belief_voiceunit
        blrpern_s_agg_tablename = create_prime_tablename(blrpern_str, "s", "agg", "put")
        insert_blrpern_sqlstr = f"""
INSERT INTO {blrpern_s_agg_tablename} ({wx.spark_num}, {wx.face_name}, {wx.belief_name}, {wx.voice_name})
VALUES ({spark1}, '{bob_str}', '{bob_str}', '{bob_str}');"""
        cursor.execute(insert_blrpern_sqlstr)

        trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        assert get_row_count(cursor, trlcore_s_vld_tablename) == 0

        # WHEN
        etl_translate_sound_agg_tables_to_translate_sound_vld_tables(cursor)

        # THEN
        assert get_row_count(cursor, trlcore_s_vld_tablename) == 1
        select_core_vld_sqlstr = f"SELECT * FROM {trlcore_s_vld_tablename}"
        cursor.execute(select_core_vld_sqlstr)
        rows = cursor.fetchall()
        x_knot = default_knot_if_None()
        exp_row0 = (bob_str, x_knot, x_knot, default_unknown_str_if_None())
        assert rows[0] == exp_row0
        assert rows == [exp_row0]


def test_etl_translate_sound_agg_tables_to_translate_sound_vld_tables_Scenario3_PopulatesSomeMissingTranslateCoreRows():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    rdx = ":"
    ukx = "Unknown"
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blrpern_str = wx.belief_voiceunit
        blrpern_s_agg_tablename = create_prime_tablename(blrpern_str, "s", "agg", "put")
        insert_blrpern_sqlstr = f"""
INSERT INTO {blrpern_s_agg_tablename} ({wx.spark_num}, {wx.face_name}, {wx.belief_name}, {wx.voice_name})
VALUES ({spark1}, '{bob_str}', '{bob_str}', '{bob_str}'), ({spark1}, '{yao_str}', '{yao_str}', '{yao_str}');"""
        cursor.execute(insert_blrpern_sqlstr)

        trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename} (
{wx.face_name}, {wx.otx_knot}, {wx.inx_knot}, {wx.unknown_str})
VALUES ('{bob_str}', '{rdx}', '{rdx}', '{ukx}');"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, trlcore_s_vld_tablename) == 1

        # WHEN
        etl_translate_sound_agg_tables_to_translate_sound_vld_tables(cursor)

        # THEN
        assert get_row_count(cursor, trlcore_s_vld_tablename) == 2
        select_core_vld_sqlstr = f"SELECT * FROM {trlcore_s_vld_tablename}"
        cursor.execute(select_core_vld_sqlstr)
        rows = cursor.fetchall()
        default_knot = default_knot_if_None()
        default_unknown = default_unknown_str_if_None()
        exp_row0 = (bob_str, rdx, rdx, ukx)
        exp_row1 = (yao_str, default_knot, default_knot, default_unknown)
        assert rows[0] == exp_row0
        assert rows[1] == exp_row1
        assert rows == [exp_row0, exp_row1]
