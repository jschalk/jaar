from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import get_row_count
from src.ch16_lire_logic.lire_main import (
    default_knot_if_None,
    default_unknown_str_if_None,
)
from src.ch18_etl_toolbox._ref.ch18_keywords import (
    belief_name_str,
    belief_voiceunit_str,
    error_message_str,
    event_int_str,
    face_name_str,
    inx_knot_str,
    inx_label_str,
    inx_name_str,
    inx_rope_str,
    inx_title_str,
    lire_core_str,
    lire_label_str,
    lire_name_str,
    lire_rope_str,
    lire_title_str,
    moment_label_str,
    otx_knot_str,
    otx_label_str,
    otx_name_str,
    otx_rope_str,
    otx_title_str,
    unknown_str_str,
    voice_name_str,
)
from src.ch18_etl_toolbox.tran_sqlstrs import (
    CREATE_LIRCORE_SOUND_AGG_SQLSTR,
    CREATE_LIRCORE_SOUND_RAW_SQLSTR,
    CREATE_LIRCORE_SOUND_VLD_SQLSTR,
    CREATE_LIRLABE_SOUND_AGG_SQLSTR,
    CREATE_LIRNAME_SOUND_AGG_SQLSTR,
    CREATE_LIRROPE_SOUND_AGG_SQLSTR,
    CREATE_LIRTITL_SOUND_AGG_SQLSTR,
    create_insert_into_lire_core_raw_sqlstr,
    create_insert_lire_sound_vld_table_sqlstr,
    create_prime_tablename,
    create_sound_and_heard_tables,
    create_update_lire_sound_agg_inconsist_sqlstr,
    create_update_lirlabe_sound_agg_knot_error_sqlstr,
    create_update_lirname_sound_agg_knot_error_sqlstr,
    create_update_lirrope_sound_agg_knot_error_sqlstr,
    create_update_lirtitl_sound_agg_knot_error_sqlstr,
)
from src.ch18_etl_toolbox.transformers import (
    etl_lire_sound_agg_tables_to_lire_sound_vld_tables,
    insert_lire_core_agg_to_lire_core_vld_table,
    insert_lire_core_raw_to_lire_core_agg_table,
    insert_lire_sound_agg_into_lire_core_raw_table,
    insert_lire_sound_agg_tables_to_lire_sound_vld_table,
    populate_lire_core_vld_with_missing_face_names,
    update_inconsistency_lire_core_raw_table,
    update_lire_sound_agg_inconsist_errors,
    update_lire_sound_agg_knot_errors,
)


def test_create_insert_into_lire_core_raw_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    a23_str = "amy23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_LIRROPE_SOUND_AGG_SQLSTR)
        lirrope_dimen = lire_rope_str()
        lire_rope_s_agg_tablename = create_prime_tablename(lirrope_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lire_rope_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_rope_str()}
, {inx_rope_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
, ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_LIRCORE_SOUND_RAW_SQLSTR)
        lire_core_s_raw_tablename = create_prime_tablename("lircore", "s", "raw")
        assert get_row_count(cursor, lire_core_s_raw_tablename) == 0

        # WHEN
        sqlstr = create_insert_into_lire_core_raw_sqlstr(lirrope_dimen)
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert get_row_count(cursor, lire_core_s_raw_tablename) == 3
        select_core_raw_sqlstr = f"SELECT * FROM {lire_core_s_raw_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        assert cursor.fetchall() == [
            (lire_rope_s_agg_tablename, "Sue", None, None, None, None),
            (lire_rope_s_agg_tablename, "Sue", ":", ":", "Unknown", None),
            (lire_rope_s_agg_tablename, "Yao", ":", ":", "Unknown", None),
        ]


def test_insert_lire_sound_agg_into_lire_core_raw_table_PopulatesTable_Scenario0():
    # ESTABLISH
    a23_str = "amy23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_LIRROPE_SOUND_AGG_SQLSTR)
        lirrope_dimen = lire_rope_str()
        lire_rope_s_agg_tablename = create_prime_tablename(lirrope_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lire_rope_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_rope_str()}
, {inx_rope_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event7}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        cursor.execute(CREATE_LIRNAME_SOUND_AGG_SQLSTR)
        lirname_dimen = lire_name_str()
        lire_name_s_agg_tablename = create_prime_tablename(lirname_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lire_name_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_name_str()}
, {inx_name_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        create_sound_and_heard_tables(cursor)
        lire_core_s_raw_tablename = create_prime_tablename("lircore", "s", "raw")
        assert get_row_count(cursor, lire_rope_s_agg_tablename) == 3
        assert get_row_count(cursor, lire_name_s_agg_tablename) == 2
        assert get_row_count(cursor, lire_core_s_raw_tablename) == 0

        # WHEN
        insert_lire_sound_agg_into_lire_core_raw_table(cursor)

        # THEN
        assert get_row_count(cursor, lire_core_s_raw_tablename) == 4
        select_core_raw_sqlstr = f"SELECT * FROM {lire_core_s_raw_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [
            (lire_name_s_agg_tablename, "Bob", ":", ":", "Unknown", None),
            (lire_name_s_agg_tablename, "Sue", None, None, None, None),
            (lire_rope_s_agg_tablename, "Sue", None, None, None, None),
            (lire_rope_s_agg_tablename, "Yao", ":", ":", "Unknown", None),
        ]


def test_update_inconsistency_lire_core_raw_table_UpdatesTable_Scenario0():
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
        cursor.execute(CREATE_LIRCORE_SOUND_RAW_SQLSTR)
        lirrope_dimen = lire_rope_str()
        lire_rope_s_agg_tablename = create_prime_tablename(lirrope_dimen, "s", "agg")
        lirname_dimen = lire_name_str()
        lire_name_s_agg_tablename = create_prime_tablename(lirname_dimen, "s", "agg")
        lircore_dimen = lire_core_str()
        lire_core_s_raw_tablename = create_prime_tablename(lircore_dimen, "s", "raw")
        insert_into_clause = f"""INSERT INTO {lire_core_s_raw_tablename} (
  source_dimen
, {face_name_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
, {error_message_str()}
)"""
        values_clause = f"""
VALUES
  ('{lire_name_s_agg_tablename}', "{bob_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
, ('{lire_name_s_agg_tablename}', "{sue_str}", NULL, NULL, '{rdx}', NULL)
, ('{lire_rope_s_agg_tablename}', "{sue_str}", NULL, NULL, '{other_knot}', NULL)
, ('{lire_rope_s_agg_tablename}', "{yao_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        create_sound_and_heard_tables(cursor)
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {lire_core_s_raw_tablename} WHERE {error_message_str()} IS NOT NULL;"
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        update_inconsistency_lire_core_raw_table(cursor)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 2
        select_core_raw_sqlstr = f"SELECT * FROM {lire_core_s_raw_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        error_data_str = "Inconsistent data"
        assert rows == [
            (lire_name_s_agg_tablename, "Bob", ":", ":", "Unknown", None),
            (lire_name_s_agg_tablename, "Sue", None, None, ":", error_data_str),
            (lire_rope_s_agg_tablename, "Sue", None, None, "/", error_data_str),
            (lire_rope_s_agg_tablename, "Yao", ":", ":", "Unknown", None),
        ]


def test_insert_lire_core_raw_to_lire_core_agg_table_PopulatesTable_Scenario0():
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
        cursor.execute(CREATE_LIRCORE_SOUND_RAW_SQLSTR)
        lirrope_dimen = lire_rope_str()
        lire_rope_s_agg_tablename = create_prime_tablename(lirrope_dimen, "s", "agg")
        lirname_dimen = lire_name_str()
        lire_name_s_agg_tablename = create_prime_tablename(lirname_dimen, "s", "agg")
        lircore_dimen = lire_core_str()
        lire_core_s_raw_tablename = create_prime_tablename(lircore_dimen, "s", "raw")
        insert_into_clause = f"""INSERT INTO {lire_core_s_raw_tablename} (
  source_dimen
, {face_name_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
, {error_message_str()}
)"""
        values_clause = f"""
VALUES
  ('{lire_name_s_agg_tablename}', "{bob_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
, ('{lire_name_s_agg_tablename}', "{sue_str}", NULL, NULL, '{rdx}', '{error_data_str}')
, ('{lire_rope_s_agg_tablename}', "{sue_str}", NULL, NULL, '{other_knot}', '{error_data_str}')
, ('{lire_rope_s_agg_tablename}', "{yao_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        create_sound_and_heard_tables(cursor)
        lire_core_s_agg_tablename = create_prime_tablename(lircore_dimen, "s", "agg")
        assert get_row_count(cursor, lire_core_s_agg_tablename) == 0

        # WHEN
        insert_lire_core_raw_to_lire_core_agg_table(cursor)

        # THEN
        assert get_row_count(cursor, lire_core_s_agg_tablename) == 2
        select_core_raw_sqlstr = f"SELECT * FROM {lire_core_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [(bob_str, rdx, rdx, ukx), (yao_str, rdx, rdx, ukx)]


def test_insert_lire_core_agg_to_lire_core_vld_table_PopulatesTable_Scenario0():
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
        cursor.execute(CREATE_LIRCORE_SOUND_AGG_SQLSTR)
        lircore_dimen = lire_core_str()
        lire_core_s_agg_tablename = create_prime_tablename(lircore_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lire_core_s_agg_tablename} (
  {face_name_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
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
        cursor.execute(CREATE_LIRCORE_SOUND_VLD_SQLSTR)
        lire_core_s_vld_tablename = create_prime_tablename(lircore_dimen, "s", "vld")
        assert get_row_count(cursor, lire_core_s_vld_tablename) == 0

        # WHEN
        insert_lire_core_agg_to_lire_core_vld_table(cursor)

        # THEN
        assert get_row_count(cursor, lire_core_s_vld_tablename) == 4
        select_core_raw_sqlstr = f"SELECT * FROM {lire_core_s_vld_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [
            (bob_str, colon_knot, slash_knot, unknown_str),
            (sue_str, default_knot, default_knot, default_unknown),
            (yao_str, default_knot, colon_knot, huh_str),
            (zia_str, colon_knot, colon_knot, huh_str),
        ]


def test_create_update_lire_sound_agg_inconsist_sqlstr_PopulatesTable_Scenario0():
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
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    error_lire_str = "Inconsistent lire core data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_LIRROPE_SOUND_AGG_SQLSTR)
        lirrope_dimen = lire_rope_str()
        lire_rope_s_agg_tablename = create_prime_tablename(lirrope_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lire_rope_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_rope_str()}
, {inx_rope_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_knot}', NULL)
, ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_LIRCORE_SOUND_VLD_SQLSTR)
        print(CREATE_LIRCORE_SOUND_VLD_SQLSTR)
        lire_core_s_vld_tablename = create_prime_tablename("lircore", "s", "vld")
        insert_into_clause = f"""INSERT INTO {lire_core_s_vld_tablename} (
  {face_name_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
)"""
        values_clause = f"""
VALUES
  ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {lire_rope_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_update_lire_sound_agg_inconsist_sqlstr(lirrope_dimen)
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 5
        select_core_raw_sqlstr = f"SELECT * FROM {lire_rope_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, yao_str, yao_inx, None, None, None, error_lire_str),
            (1, sue_str, bob_str, bob_inx, None, None, None, error_lire_str),
            (1, sue_str, bob_str, bob_str, None, "/", None, error_lire_str),
            (2, sue_str, sue_str, sue_str, ":", ":", "Unknown", error_lire_str),
            (5, sue_str, bob_str, bob_inx, ":", ":", "Unknown", error_lire_str),
            (7, yao_str, yao_str, yao_inx, ":", ":", "Unknown", None),
        ]


def test_update_lire_sound_agg_inconsist_errors_PopulatesTable_Scenario1():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_knot = "/"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    error_lire_str = "Inconsistent lire core data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        lirrope_dimen = lire_rope_str()
        lire_rope_s_agg_tablename = create_prime_tablename(lirrope_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lire_rope_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_rope_str()}
, {inx_rope_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_knot}', NULL)
, ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        lire_core_s_vld_tablename = create_prime_tablename("lircore", "s", "vld")
        insert_into_clause = f"""INSERT INTO {lire_core_s_vld_tablename} (
  {face_name_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
)"""
        values_clause = f"""
VALUES
  ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {lire_rope_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        update_lire_sound_agg_inconsist_errors(cursor)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 5
        select_core_raw_sqlstr = f"SELECT * FROM {lire_rope_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, yao_str, yao_inx, None, None, None, error_lire_str),
            (1, sue_str, bob_str, bob_inx, None, None, None, error_lire_str),
            (1, sue_str, bob_str, bob_str, None, "/", None, error_lire_str),
            (2, sue_str, sue_str, sue_str, ":", ":", "Unknown", error_lire_str),
            (5, sue_str, bob_str, bob_inx, ":", ":", "Unknown", error_lire_str),
            (7, yao_str, yao_str, yao_inx, ":", ":", "Unknown", None),
        ]


def test_create_update_lirlabe_sound_agg_knot_error_sqlstr_PopulatesTable_Scenario0():
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
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event9 = 9
    error_label_str = "Knot cannot exist in LabelTerm"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_LIRLABE_SOUND_AGG_SQLSTR)
        lirlabe_dimen = lire_label_str()
        lirlabe_s_agg_tablename = create_prime_tablename(lirlabe_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lirlabe_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_label_str()}
, {inx_label_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{bob_str}', '{fly_str}', '{fly_inx}')
, ({event1}, '{bob_str}', '{ski_str}{rdx}', '{ski_str}')
, ({event2}, '{bob_str}', '{run_rdx_run}', '{run_str}')
, ({event5}, '{yao_str}', '{ski_str}', '{ski_inx}{rdx}')
, ({event7}, '{yao_str}', '{fly_str}', '{fly_inx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_LIRCORE_SOUND_VLD_SQLSTR)
        lire_core_s_vld_tablename = create_prime_tablename("lircore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {lire_core_s_vld_tablename} (
  {face_name_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
)
VALUES
  ('{bob_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(insert_sqlstr)
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {lirlabe_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"

        testing_select_sqlstr = """
  SELECT label_agg.rowid, label_agg.otx_label, label_agg.inx_label, *
  FROM lire_label_s_agg label_agg
  JOIN lire_core_s_vld core_vld ON core_vld.face_name = label_agg.face_name
  WHERE label_agg.otx_label LIKE '%' || core_vld.otx_knot || '%'
      OR label_agg.inx_label LIKE '%' || core_vld.inx_knot || '%'
"""
        print(cursor.execute(testing_select_sqlstr).fetchall())

        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_update_lirlabe_sound_agg_knot_error_sqlstr()
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 3
        select_core_raw_sqlstr = f"SELECT * FROM {lirlabe_s_agg_tablename}"
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


def test_create_update_lirrope_sound_agg_knot_error_sqlstr_PopulatesTable_Scenario0():
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
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event9 = 9
    error_rope_str = "Knot must exist in RopeTerm"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_LIRROPE_SOUND_AGG_SQLSTR)
        lirrope_dimen = lire_rope_str()
        lirrope_s_agg_tablename = create_prime_tablename(lirrope_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lirrope_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_rope_str()}
, {inx_rope_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{bob_str}', '{spt_run_str}', '{spt_run_str}')
, ({event1}, '{bob_str}', '{spt_fly_str}', '{bad_fly_str}')
, ({event2}, '{bob_str}', '{bad_fly_str}', '{spt_fly_str}')
, ({event5}, '{yao_str}', '{bad_ski_str}', '{bad_ski_str}')
, ({event7}, '{yao_str}', '{spt_run_str}', '{bad_run_str}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_LIRCORE_SOUND_VLD_SQLSTR)
        lire_core_s_vld_tablename = create_prime_tablename("lircore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {lire_core_s_vld_tablename} (
  {face_name_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
)
VALUES
  ('{bob_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(insert_sqlstr)
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {lirrope_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"

        testing_select_sqlstr = """
  SELECT rope_agg.rowid, rope_agg.otx_rope, rope_agg.inx_rope
  FROM lire_rope_s_agg rope_agg
  JOIN lire_core_s_vld core_vld ON core_vld.face_name = rope_agg.face_name
  WHERE NOT rope_agg.otx_rope LIKE core_vld.otx_knot || '%'
     OR NOT rope_agg.inx_rope LIKE core_vld.inx_knot || '%'
  """

        print(cursor.execute(testing_select_sqlstr).fetchall())

        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_update_lirrope_sound_agg_knot_error_sqlstr()
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 4
        select_core_raw_sqlstr = f"SELECT * FROM {lirrope_s_agg_tablename}"
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


def test_create_update_lirname_sound_agg_knot_error_sqlstr_PopulatesTable_Scenario0():
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
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event9 = 9
    error_name_str = "Knot cannot exist in NameTerm"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_LIRNAME_SOUND_AGG_SQLSTR)
        lirname_dimen = lire_name_str()
        lirname_s_agg_tablename = create_prime_tablename(lirname_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lirname_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_name_str()}
, {inx_name_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{bob_str}', '{sue_otx}', '{sue_inx}')
, ({event1}, '{bob_str}', '{sue_otx}', '{bad_sue_inx}')
, ({event2}, '{bob_str}', '{zia_otx}', '{bad_zia_inx}')
, ({event5}, '{yao_str}', '{bad_zia_otx}', '{bad_zia_inx}')
, ({event7}, '{yao_str}', '{bad_zia_otx}', '{zia_inx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_LIRCORE_SOUND_VLD_SQLSTR)
        lire_core_s_vld_tablename = create_prime_tablename("lircore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {lire_core_s_vld_tablename} (
  {face_name_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
)
VALUES
  ('{bob_str}', '{rdx}', '{rdx}', '{ukx}')
, ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(insert_sqlstr)
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {lirname_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"

        testing_select_sqlstr = """
  SELECT name_agg.rowid, name_agg.otx_name, name_agg.inx_name
  FROM lire_name_s_agg name_agg
  JOIN lire_core_s_vld core_vld ON core_vld.face_name = name_agg.face_name
  WHERE NOT name_agg.otx_name LIKE core_vld.otx_knot || '%'
     OR NOT name_agg.inx_name LIKE core_vld.inx_knot || '%'
  """

        print(cursor.execute(testing_select_sqlstr).fetchall())

        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_update_lirname_sound_agg_knot_error_sqlstr()
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 4
        select_core_raw_sqlstr = f"SELECT * FROM {lirname_s_agg_tablename}"
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


def test_create_update_lirtitl_sound_agg_knot_error_sqlstr_PopulatesTable_Scenario0():
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
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    event9 = 9
    error_title_str = "Otx and inx titles must match knot."

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_LIRTITL_SOUND_AGG_SQLSTR)
        lirtitl_dimen = lire_title_str()
        lirtitl_s_agg_tablename = create_prime_tablename(lirtitl_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lirtitl_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_title_str()}
, {inx_title_str()}
)"""
        # TODO create values where errors will appear: groups should map to groups,
        values_clause = f"""
VALUES
  ({event1}, '{bob_str}', '{sue_otx}', '{sue_inx}')
, ({event1}, '{yao_str}', '{bad_sue_otx}', '{sue_inx}')
, ({event2}, '{bob_str}', '{swim_otx}', '{swim_inx}')
, ({event5}, '{yao_str}', '{swim_otx}', '{bad_swim_inx}')
, ({event7}, '{yao_str}', '{bad_swim_otx}', '{swim_inx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_LIRCORE_SOUND_VLD_SQLSTR)
        lire_core_s_vld_tablename = create_prime_tablename("lircore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {lire_core_s_vld_tablename} (
  {face_name_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
)
VALUES
  ('{bob_str}', '{rdx_otx}', '{rdx_inx}', '{ukx}')
, ('{yao_str}', '{rdx_otx}', '{rdx_inx}', '{ukx}')
;
"""
        cursor.execute(insert_sqlstr)
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {lirtitl_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"

        testing_select_sqlstr = """
  SELECT title_agg.rowid, title_agg.otx_title, title_agg.inx_title
  FROM lire_title_s_agg title_agg
  JOIN lire_core_s_vld core_vld ON core_vld.face_name = title_agg.face_name
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
        sqlstr = create_update_lirtitl_sound_agg_knot_error_sqlstr()
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 3
        select_core_raw_sqlstr = f"SELECT * FROM {lirtitl_s_agg_tablename}"
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


def test_update_lire_sound_agg_knot_errors_UpdatesTables_Scenario0():
    # ESTABLISH
    bob_str = "bob"
    casa_str = "Casa"
    rdx = ":"
    ukx = "Unknown"
    sue_inx = "Sue"
    bad_sue_otx = f"{rdx}Suzy"
    event1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_LIRLABE_SOUND_AGG_SQLSTR)
        cursor.execute(CREATE_LIRROPE_SOUND_AGG_SQLSTR)
        cursor.execute(CREATE_LIRNAME_SOUND_AGG_SQLSTR)
        cursor.execute(CREATE_LIRTITL_SOUND_AGG_SQLSTR)
        lirlabe_s_agg_tablename = create_prime_tablename(lire_label_str(), "s", "agg")
        lirrope_s_agg_tablename = create_prime_tablename(lire_rope_str(), "s", "agg")
        lirname_s_agg_tablename = create_prime_tablename(lire_name_str(), "s", "agg")
        lirtitl_s_agg_tablename = create_prime_tablename(lire_title_str(), "s", "agg")
        insert_lirlabe_sqlstr = f"""
INSERT INTO {lirlabe_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_label_str()}, {inx_label_str()})
VALUES ({event1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
        insert_lirrope_sqlstr = f"""
INSERT INTO {lirrope_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_rope_str()}, {inx_rope_str()})
VALUES ({event1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
        insert_lirname_sqlstr = f"""
INSERT INTO {lirname_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
VALUES ({event1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
        insert_lirtitl_sqlstr = f"""
INSERT INTO {lirtitl_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_title_str()}, {inx_title_str()})
VALUES ({event1}, '{bob_str}', '{bad_sue_otx}', '{sue_inx}');"""
        cursor.execute(insert_lirlabe_sqlstr)
        cursor.execute(insert_lirrope_sqlstr)
        cursor.execute(insert_lirname_sqlstr)
        cursor.execute(insert_lirtitl_sqlstr)

        lircore_s_vld_tablename = create_prime_tablename("lircore", "s", "vld")
        cursor.execute(CREATE_LIRCORE_SOUND_VLD_SQLSTR)
        insert_sqlstr = f"""INSERT INTO {lircore_s_vld_tablename} (
{face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES ('{bob_str}', '{rdx}', '{rdx}', '{ukx}');"""
        cursor.execute(insert_sqlstr)
        lirlabe_error_count_sqlstr = f"SELECT COUNT(*) FROM {lirlabe_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"
        lirrope_error_count_sqlstr = f"SELECT COUNT(*) FROM {lirrope_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"
        lirname_error_count_sqlstr = f"SELECT COUNT(*) FROM {lirname_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"
        lirtitl_error_count_sqlstr = f"SELECT COUNT(*) FROM {lirtitl_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"
        assert cursor.execute(lirlabe_error_count_sqlstr).fetchone()[0] == 0
        assert cursor.execute(lirrope_error_count_sqlstr).fetchone()[0] == 0
        assert cursor.execute(lirname_error_count_sqlstr).fetchone()[0] == 0
        assert cursor.execute(lirtitl_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        update_lire_sound_agg_knot_errors(cursor)

        # THEN
        assert cursor.execute(lirlabe_error_count_sqlstr).fetchone()[0] == 1
        assert cursor.execute(lirrope_error_count_sqlstr).fetchone()[0] == 1
        assert cursor.execute(lirname_error_count_sqlstr).fetchone()[0] == 1
        assert cursor.execute(lirtitl_error_count_sqlstr).fetchone()[0] == 1
        assert get_row_count(cursor, lirtitl_s_agg_tablename) == 1
        select_core_raw_sqlstr = f"SELECT {event_int_str()}, {face_name_str()}, {otx_label_str()}, {inx_label_str()} FROM {lirlabe_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        exp_row0 = (1, bob_str, f"{casa_str}{rdx}", casa_str)
        assert rows[0] == exp_row0
        assert rows == [exp_row0]


def test_create_insert_lire_sound_vld_table_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_knot = "/"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    error_lire_str = "Inconsistent lire core data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        lirrope_dimen = lire_rope_str()
        lire_rope_s_agg_tablename = create_prime_tablename(lirrope_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lire_rope_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_rope_str()}
, {inx_rope_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
, {error_message_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL, '{error_lire_str}')
, ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL, '{error_lire_str}')
, ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_knot}', NULL, '{error_lire_str}')
, ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', '{error_lire_str}')
, ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', '{error_lire_str}')
, ({event1}, '{yao_str}', '{yao_str}', '{yao_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}', NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        lire_rope_s_vld_tablename = create_prime_tablename("lirrope", "s", "vld")
        assert get_row_count(cursor, lire_rope_s_agg_tablename) == 8
        assert get_row_count(cursor, lire_rope_s_vld_tablename) == 0

        # WHEN
        sqlstr = create_insert_lire_sound_vld_table_sqlstr(lirrope_dimen)
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert get_row_count(cursor, lire_rope_s_vld_tablename) == 3
        select_lire_rope_s_vld_sqlstr = f"SELECT * FROM {lire_rope_s_vld_tablename}"
        cursor.execute(select_lire_rope_s_vld_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (event1, yao_str, yao_str, yao_str),
            (event7, bob_str, bob_str, bob_inx),
            (event7, yao_str, yao_str, yao_inx),
        ]


def test_insert_lire_sound_agg_tables_to_lire_sound_vld_table_PopulatesTable_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_knot = "/"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    error_lire_str = "Inconsistent lire core data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        lirrope_dimen = lire_rope_str()
        lire_rope_s_agg_tablename = create_prime_tablename(lirrope_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lire_rope_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_rope_str()}
, {inx_rope_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
, {error_message_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL, '{error_lire_str}')
, ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL, '{error_lire_str}')
, ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_knot}', NULL, '{error_lire_str}')
, ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', '{error_lire_str}')
, ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', '{error_lire_str}')
, ({event1}, '{yao_str}', '{yao_str}', '{yao_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}', NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        lire_rope_s_vld_tablename = create_prime_tablename("lirrope", "s", "vld")
        assert get_row_count(cursor, lire_rope_s_agg_tablename) == 8
        assert get_row_count(cursor, lire_rope_s_vld_tablename) == 0

        # WHEN
        insert_lire_sound_agg_tables_to_lire_sound_vld_table(cursor)

        # THEN
        assert get_row_count(cursor, lire_rope_s_vld_tablename) == 3
        select_lire_rope_s_vld_sqlstr = f"SELECT * FROM {lire_rope_s_vld_tablename}"
        cursor.execute(select_lire_rope_s_vld_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (event1, yao_str, yao_str, yao_str),
            (event7, bob_str, bob_str, bob_inx),
            (event7, yao_str, yao_str, yao_inx),
        ]


def test_etl_lire_sound_agg_tables_to_lire_sound_vld_tables_Scenario0_PopulatesTable():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_knot = "/"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        lirname_dimen = lire_name_str()
        lire_name_s_agg_tablename = create_prime_tablename(lirname_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {lire_name_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_name_str()}
, {inx_name_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_knot}', NULL)
, ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({event1}, '{yao_str}', '{yao_str}', '{yao_str}', '{rdx}', '{rdx}', '{ukx}')
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', NULL)
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}')
, ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        insert_lire_sound_agg_into_lire_core_raw_table(cursor)
        lire_core_s_raw_tablename = create_prime_tablename("lircore", "s", "raw")
        lire_core_s_agg_tablename = create_prime_tablename("lircore", "s", "agg")
        lire_name_s_vld_tablename = create_prime_tablename("lirname", "s", "vld")
        assert get_row_count(cursor, lire_name_s_agg_tablename) == 10
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {lire_name_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0
        assert get_row_count(cursor, lire_core_s_raw_tablename) == 6
        assert get_row_count(cursor, lire_core_s_agg_tablename) == 0
        assert get_row_count(cursor, lire_name_s_vld_tablename) == 0

        # WHEN
        etl_lire_sound_agg_tables_to_lire_sound_vld_tables(cursor)

        # THEN
        lire_name_s_agg_select = f"SELECT * FROM {lire_name_s_agg_tablename};"
        print(f"{cursor.execute(lire_name_s_agg_select).fetchall()=}\n")
        lire_core_s_raw_select = f"SELECT * FROM {lire_core_s_raw_tablename};"
        print(f"{cursor.execute(lire_core_s_raw_select).fetchall()=}\n")
        lire_core_s_agg_select = f"SELECT * FROM {lire_core_s_agg_tablename};"
        print(f"{cursor.execute(lire_core_s_agg_select).fetchall()=}\n")
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 5
        assert get_row_count(cursor, lire_core_s_agg_tablename) == 2
        assert get_row_count(cursor, lire_name_s_vld_tablename) == 3
        select_lire_name_s_vld_sqlstr = f"SELECT * FROM {lire_name_s_vld_tablename}"
        cursor.execute(select_lire_name_s_vld_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (event1, yao_str, yao_str, yao_str),
            (event7, bob_str, bob_str, bob_inx),
            (event7, yao_str, yao_str, yao_inx),
        ]


def test_etl_lire_sound_agg_tables_to_lire_sound_vld_tables_Scenario1_UpdatesErrors():
    # ESTABLISH
    bob_str = "bob"
    casa_str = "Casa"
    rdx = ":"
    ukx = "Unknown"
    event1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        lirlabe_s_agg_tablename = create_prime_tablename(lire_label_str(), "s", "agg")
        lirrope_s_agg_tablename = create_prime_tablename(lire_rope_str(), "s", "agg")
        lirname_s_agg_tablename = create_prime_tablename(lire_name_str(), "s", "agg")
        insert_lirlabe_sqlstr = f"""
INSERT INTO {lirlabe_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_label_str()}, {inx_label_str()})
VALUES ({event1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
        insert_lirrope_sqlstr = f"""
INSERT INTO {lirrope_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_rope_str()}, {inx_rope_str()})
VALUES ({event1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
        insert_lirname_sqlstr = f"""
INSERT INTO {lirname_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
VALUES ({event1}, '{bob_str}', '{casa_str}{rdx}', '{casa_str}');"""
        cursor.execute(insert_lirlabe_sqlstr)
        cursor.execute(insert_lirrope_sqlstr)
        cursor.execute(insert_lirname_sqlstr)

        lircore_s_vld_tablename = create_prime_tablename("lircore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {lircore_s_vld_tablename} (
{face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES ('{bob_str}', '{rdx}', '{rdx}', '{ukx}');"""
        cursor.execute(insert_sqlstr)
        lirlabe_error_count_sqlstr = f"SELECT COUNT(*) FROM {lirlabe_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"
        lirrope_error_count_sqlstr = f"SELECT COUNT(*) FROM {lirrope_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"
        lirname_error_count_sqlstr = f"SELECT COUNT(*) FROM {lirname_s_agg_tablename} WHERE {error_message_str()} IS NOT NULL;"
        assert cursor.execute(lirlabe_error_count_sqlstr).fetchone()[0] == 0
        assert cursor.execute(lirrope_error_count_sqlstr).fetchone()[0] == 0
        assert cursor.execute(lirname_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        etl_lire_sound_agg_tables_to_lire_sound_vld_tables(cursor)

        # THEN
        assert cursor.execute(lirlabe_error_count_sqlstr).fetchone()[0] == 1
        assert cursor.execute(lirrope_error_count_sqlstr).fetchone()[0] == 1
        assert cursor.execute(lirname_error_count_sqlstr).fetchone()[0] == 1
        select_core_raw_sqlstr = f"SELECT {event_int_str()}, {face_name_str()}, {otx_label_str()}, {inx_label_str()} FROM {lirlabe_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        exp_row0 = (1, bob_str, f"{casa_str}{rdx}", casa_str)
        assert rows[0] == exp_row0
        assert rows == [exp_row0]


def test_populate_lire_core_vld_with_missing_face_names_Scenario0_Populates1MissingLireCoreRow():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    casa_str = "Casa"
    rdx = ":"
    ukx = "Unknown"
    event1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blrpern_str = belief_voiceunit_str()
        blrpern_s_agg_tablename = create_prime_tablename(blrpern_str, "s", "agg", "put")
        insert_blrpern_sqlstr = f"""
INSERT INTO {blrpern_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {belief_name_str()}, {voice_name_str()})
VALUES ({event1}, '{bob_str}', '{bob_str}', '{bob_str}');"""
        cursor.execute(insert_blrpern_sqlstr)

        lircore_s_vld_tablename = create_prime_tablename("lircore", "s", "vld")
        assert get_row_count(cursor, lircore_s_vld_tablename) == 0

        # WHEN
        populate_lire_core_vld_with_missing_face_names(cursor)

        # THEN
        assert get_row_count(cursor, lircore_s_vld_tablename) == 1
        select_core_vld_sqlstr = f"SELECT {face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()} FROM {lircore_s_vld_tablename}"
        cursor.execute(select_core_vld_sqlstr)
        rows = cursor.fetchall()
        x_knot = default_knot_if_None()
        exp_row0 = (bob_str, x_knot, x_knot, default_unknown_str_if_None())
        assert rows[0] == exp_row0
        assert rows == [exp_row0]


def test_populate_lire_core_vld_with_missing_face_names_Scenario1_PopulatesSomeMissingLireCoreRows():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    rdx = ":"
    ukx = "Unknown"
    event1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blrpern_str = belief_voiceunit_str()
        blrpern_s_agg_tablename = create_prime_tablename(blrpern_str, "s", "agg", "put")
        insert_blrpern_sqlstr = f"""
INSERT INTO {blrpern_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {belief_name_str()}, {voice_name_str()})
VALUES ({event1}, '{bob_str}', '{bob_str}', '{bob_str}'), ({event1}, '{yao_str}', '{yao_str}', '{yao_str}');"""
        cursor.execute(insert_blrpern_sqlstr)

        lircore_s_vld_tablename = create_prime_tablename("lircore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {lircore_s_vld_tablename} (
{face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES ('{bob_str}', '{rdx}', '{rdx}', '{ukx}');"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, lircore_s_vld_tablename) == 1

        # WHEN
        populate_lire_core_vld_with_missing_face_names(cursor)

        # THEN
        assert get_row_count(cursor, lircore_s_vld_tablename) == 2
        select_core_vld_sqlstr = f"SELECT {face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()} FROM {lircore_s_vld_tablename} ORDER BY {face_name_str()}"
        cursor.execute(select_core_vld_sqlstr)
        rows = cursor.fetchall()
        default_knot = default_knot_if_None()
        default_unknown = default_unknown_str_if_None()
        exp_row0 = (bob_str, rdx, rdx, ukx)
        exp_row1 = (yao_str, default_knot, default_knot, default_unknown)
        assert rows[0] == exp_row0
        assert rows[1] == exp_row1
        assert rows == [exp_row0, exp_row1]


def test_etl_lire_sound_agg_tables_to_lire_sound_vld_tables_Scenario2_Populates1MissingLireCoreRow():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    casa_str = "Casa"
    rdx = ":"
    ukx = "Unknown"
    event1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blrpern_str = belief_voiceunit_str()
        blrpern_s_agg_tablename = create_prime_tablename(blrpern_str, "s", "agg", "put")
        insert_blrpern_sqlstr = f"""
INSERT INTO {blrpern_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {belief_name_str()}, {voice_name_str()})
VALUES ({event1}, '{bob_str}', '{bob_str}', '{bob_str}');"""
        cursor.execute(insert_blrpern_sqlstr)

        lircore_s_vld_tablename = create_prime_tablename("lircore", "s", "vld")
        assert get_row_count(cursor, lircore_s_vld_tablename) == 0

        # WHEN
        etl_lire_sound_agg_tables_to_lire_sound_vld_tables(cursor)

        # THEN
        assert get_row_count(cursor, lircore_s_vld_tablename) == 1
        select_core_vld_sqlstr = f"SELECT * FROM {lircore_s_vld_tablename}"
        cursor.execute(select_core_vld_sqlstr)
        rows = cursor.fetchall()
        x_knot = default_knot_if_None()
        exp_row0 = (bob_str, x_knot, x_knot, default_unknown_str_if_None())
        assert rows[0] == exp_row0
        assert rows == [exp_row0]


def test_etl_lire_sound_agg_tables_to_lire_sound_vld_tables_Scenario3_PopulatesSomeMissingLireCoreRows():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    rdx = ":"
    ukx = "Unknown"
    event1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blrpern_str = belief_voiceunit_str()
        blrpern_s_agg_tablename = create_prime_tablename(blrpern_str, "s", "agg", "put")
        insert_blrpern_sqlstr = f"""
INSERT INTO {blrpern_s_agg_tablename} ({event_int_str()}, {face_name_str()}, {belief_name_str()}, {voice_name_str()})
VALUES ({event1}, '{bob_str}', '{bob_str}', '{bob_str}'), ({event1}, '{yao_str}', '{yao_str}', '{yao_str}');"""
        cursor.execute(insert_blrpern_sqlstr)

        lircore_s_vld_tablename = create_prime_tablename("lircore", "s", "vld")
        insert_sqlstr = f"""INSERT INTO {lircore_s_vld_tablename} (
{face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES ('{bob_str}', '{rdx}', '{rdx}', '{ukx}');"""
        cursor.execute(insert_sqlstr)
        assert get_row_count(cursor, lircore_s_vld_tablename) == 1

        # WHEN
        etl_lire_sound_agg_tables_to_lire_sound_vld_tables(cursor)

        # THEN
        assert get_row_count(cursor, lircore_s_vld_tablename) == 2
        select_core_vld_sqlstr = f"SELECT * FROM {lircore_s_vld_tablename}"
        cursor.execute(select_core_vld_sqlstr)
        rows = cursor.fetchall()
        default_knot = default_knot_if_None()
        default_unknown = default_unknown_str_if_None()
        exp_row0 = (bob_str, rdx, rdx, ukx)
        exp_row1 = (yao_str, default_knot, default_knot, default_unknown)
        assert rows[0] == exp_row0
        assert rows[1] == exp_row1
        assert rows == [exp_row0, exp_row1]
