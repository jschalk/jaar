from src.a00_data_toolbox.db_toolbox import get_table_columns, get_row_count
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import (
    bud_acctunit_str,
    face_name_str,
    acct_name_str,
    event_int_str,
    credit_belief_str,
    debtit_belief_str,
)
from src.a16_pidgin_logic.pidgin import (
    default_bridge_if_None,
    default_unknown_word_if_None,
)
from src.a16_pidgin_logic._utils.str_a16 import (
    pidgin_road_str,
    pidgin_name_str,
    pidgin_core_str,
    inx_bridge_str,
    otx_bridge_str,
    inx_road_str,
    otx_road_str,
    inx_name_str,
    otx_name_str,
    unknown_word_str,
)
from src.a17_idea_logic._utils.str_a17 import idea_number_str
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename,
    create_sound_and_voice_tables,
    CREATE_PIDROAD_SOUND_AGG_SQLSTR,
    CREATE_PIDNAME_SOUND_AGG_SQLSTR,
    CREATE_PIDCORE_SOUND_RAW_SQLSTR,
    CREATE_PIDCORE_SOUND_AGG_SQLSTR,
    CREATE_PIDCORE_SOUND_VLD_SQLSTR,
    create_insert_into_pidgin_core_raw_sqlstr,
    create_update_inconsist_pidgin_dimen_agg_sqlstr,
    create_insert_pidgin_sound_vld_table_sqlstr,
)
from src.a18_etl_toolbox.transformers import (
    insert_sound_raw_selects_into_sound_agg_tables,
    set_sound_raw_tables_error_message,
    etl_sound_raw_tables_to_sound_agg_tables,
    insert_pidgin_sound_agg_into_pidgin_core_raw_table,
    insert_pidgin_core_agg_to_pidgin_core_vld_table,
    update_inconsistency_pidgin_core_raw_table,
    insert_pidgin_core_raw_to_pidgin_core_agg_table,
    update_inconsistency_pidgin_sound_agg_tables,
    insert_pidgin_sound_agg_tables_to_pidgin_sound_vld_table,
    etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables,
    etl_sound_agg_tables_to_pidgin_core_raw_table,
)
from sqlite3 import connect as sqlite3_connect


def test_create_insert_into_pidgin_core_raw_sqlstr_ReturnsObj_PopulatesTableCorrectly_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
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
        cursor.execute(CREATE_PIDROAD_SOUND_AGG_SQLSTR)
        pidroad_dimen = pidgin_road_str()
        pidgin_road_s_agg_tablename = create_prime_tablename(pidroad_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {pidgin_road_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
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
        cursor.execute(CREATE_PIDCORE_SOUND_RAW_SQLSTR)
        pidgin_core_s_raw_tablename = create_prime_tablename("pidcore", "s", "raw")
        assert get_row_count(cursor, pidgin_core_s_raw_tablename) == 0

        # WHEN
        sqlstr = create_insert_into_pidgin_core_raw_sqlstr(pidroad_dimen)
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert get_row_count(cursor, pidgin_core_s_raw_tablename) == 3
        select_core_raw_sqlstr = f"SELECT * FROM {pidgin_core_s_raw_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        assert cursor.fetchall() == [
            (pidgin_road_s_agg_tablename, "Sue", None, None, None, None),
            (pidgin_road_s_agg_tablename, "Sue", ":", ":", "Unknown", None),
            (pidgin_road_s_agg_tablename, "Yao", ":", ":", "Unknown", None),
        ]


def test_insert_pidgin_sound_agg_into_pidgin_core_raw_table_PopulatesTableCorrectly_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
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
        cursor.execute(CREATE_PIDROAD_SOUND_AGG_SQLSTR)
        pidroad_dimen = pidgin_road_str()
        pidgin_road_s_agg_tablename = create_prime_tablename(pidroad_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {pidgin_road_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event7}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        cursor.execute(CREATE_PIDNAME_SOUND_AGG_SQLSTR)
        pidname_dimen = pidgin_name_str()
        pidgin_name_s_agg_tablename = create_prime_tablename(pidname_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {pidgin_name_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_name_str()}
, {inx_name_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        create_sound_and_voice_tables(cursor)
        pidgin_core_s_raw_tablename = create_prime_tablename("pidcore", "s", "raw")
        assert get_row_count(cursor, pidgin_road_s_agg_tablename) == 3
        assert get_row_count(cursor, pidgin_name_s_agg_tablename) == 2
        assert get_row_count(cursor, pidgin_core_s_raw_tablename) == 0

        # WHEN
        insert_pidgin_sound_agg_into_pidgin_core_raw_table(cursor)

        # THEN
        assert get_row_count(cursor, pidgin_core_s_raw_tablename) == 4
        select_core_raw_sqlstr = f"SELECT * FROM {pidgin_core_s_raw_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [
            (pidgin_name_s_agg_tablename, "Bob", ":", ":", "Unknown", None),
            (pidgin_name_s_agg_tablename, "Sue", None, None, None, None),
            (pidgin_road_s_agg_tablename, "Sue", None, None, None, None),
            (pidgin_road_s_agg_tablename, "Yao", ":", ":", "Unknown", None),
        ]


def test_update_inconsistency_pidgin_core_raw_table_UpdatesTableCorrectly_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_bridge = "/"
    ukx = "Unknown"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_PIDCORE_SOUND_RAW_SQLSTR)
        pidroad_dimen = pidgin_road_str()
        pidgin_road_s_agg_tablename = create_prime_tablename(pidroad_dimen, "s", "agg")
        pidname_dimen = pidgin_name_str()
        pidgin_name_s_agg_tablename = create_prime_tablename(pidname_dimen, "s", "agg")
        pidcore_dimen = pidgin_core_str()
        pidgin_core_s_raw_tablename = create_prime_tablename(pidcore_dimen, "s", "raw")
        insert_into_clause = f"""INSERT INTO {pidgin_core_s_raw_tablename} (
  source_dimen
, {face_name_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
, error_message
)"""
        values_clause = f"""
VALUES
  ('{pidgin_name_s_agg_tablename}', "{bob_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
, ('{pidgin_name_s_agg_tablename}', "{sue_str}", NULL, NULL, '{rdx}', NULL)
, ('{pidgin_road_s_agg_tablename}', "{sue_str}", NULL, NULL, '{other_bridge}', NULL)
, ('{pidgin_road_s_agg_tablename}', "{yao_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        create_sound_and_voice_tables(cursor)
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidgin_core_s_raw_tablename} WHERE error_message IS NOT NULL;"
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        update_inconsistency_pidgin_core_raw_table(cursor)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 2
        select_core_raw_sqlstr = f"SELECT * FROM {pidgin_core_s_raw_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        error_message = "Inconsistent data"
        assert rows == [
            (pidgin_name_s_agg_tablename, "Bob", ":", ":", "Unknown", None),
            (pidgin_name_s_agg_tablename, "Sue", None, None, ":", error_message),
            (pidgin_road_s_agg_tablename, "Sue", None, None, "/", error_message),
            (pidgin_road_s_agg_tablename, "Yao", ":", ":", "Unknown", None),
        ]


def test_insert_pidgin_core_raw_to_pidgin_core_agg_table_PopulatesTableCorrectly_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_bridge = "/"
    ukx = "Unknown"
    error_message = "Inconsistent data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_PIDCORE_SOUND_RAW_SQLSTR)
        pidroad_dimen = pidgin_road_str()
        pidgin_road_s_agg_tablename = create_prime_tablename(pidroad_dimen, "s", "agg")
        pidname_dimen = pidgin_name_str()
        pidgin_name_s_agg_tablename = create_prime_tablename(pidname_dimen, "s", "agg")
        pidcore_dimen = pidgin_core_str()
        pidgin_core_s_raw_tablename = create_prime_tablename(pidcore_dimen, "s", "raw")
        insert_into_clause = f"""INSERT INTO {pidgin_core_s_raw_tablename} (
  source_dimen
, {face_name_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
, error_message
)"""
        values_clause = f"""
VALUES
  ('{pidgin_name_s_agg_tablename}', "{bob_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
, ('{pidgin_name_s_agg_tablename}', "{sue_str}", NULL, NULL, '{rdx}', '{error_message}')
, ('{pidgin_road_s_agg_tablename}', "{sue_str}", NULL, NULL, '{other_bridge}', '{error_message}')
, ('{pidgin_road_s_agg_tablename}', "{yao_str}", "{rdx}", "{rdx}", "{ukx}", NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")

        create_sound_and_voice_tables(cursor)
        pidgin_core_s_agg_tablename = create_prime_tablename(pidcore_dimen, "s", "agg")
        assert get_row_count(cursor, pidgin_core_s_agg_tablename) == 0

        # WHEN
        insert_pidgin_core_raw_to_pidgin_core_agg_table(cursor)

        # THEN
        assert get_row_count(cursor, pidgin_core_s_agg_tablename) == 2
        select_core_raw_sqlstr = f"SELECT * FROM {pidgin_core_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [(bob_str, rdx, rdx, ukx), (yao_str, rdx, rdx, ukx)]


def test_insert_pidgin_core_agg_to_pidgin_core_vld_table_PopulatesTableCorrectly_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "zia"
    colon_bridge = ":"
    slash_bridge = "/"
    other_bridge = "="
    unknown_str = "Unknown"
    huh_str = "Huh"
    default_bridge = default_bridge_if_None()
    default_unknown = default_unknown_word_if_None()

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_PIDCORE_SOUND_AGG_SQLSTR)
        pidcore_dimen = pidgin_core_str()
        pidgin_core_s_agg_tablename = create_prime_tablename(pidcore_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {pidgin_core_s_agg_tablename} (
  {face_name_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES
  ("{bob_str}", "{colon_bridge}", "{slash_bridge}", "{unknown_str}")
, ("{sue_str}", NULL, NULL, NULL)
, ("{yao_str}", NULL, '{colon_bridge}', '{huh_str}')
, ("{zia_str}", "{colon_bridge}", "{colon_bridge}", "{huh_str}")
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
        pidgin_core_s_vld_tablename = create_prime_tablename(pidcore_dimen, "s", "vld")
        assert get_row_count(cursor, pidgin_core_s_vld_tablename) == 0

        # WHEN
        insert_pidgin_core_agg_to_pidgin_core_vld_table(cursor)

        # THEN
        assert get_row_count(cursor, pidgin_core_s_vld_tablename) == 4
        select_core_raw_sqlstr = f"SELECT * FROM {pidgin_core_s_vld_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [
            (bob_str, colon_bridge, slash_bridge, unknown_str),
            (sue_str, default_bridge, default_bridge, default_unknown),
            (yao_str, default_bridge, colon_bridge, huh_str),
            (zia_str, colon_bridge, colon_bridge, huh_str),
        ]


def test_update_inconsistency_pidgin_sound_agg_tables_ReturnsObj_PopulatesTableCorrectly_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_bridge = "/"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    error_message = "Inconsistent pidgin core data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_PIDROAD_SOUND_AGG_SQLSTR)
        pidroad_dimen = pidgin_road_str()
        pidgin_road_s_agg_tablename = create_prime_tablename(pidroad_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {pidgin_road_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_bridge}', NULL)
, ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        cursor.execute(CREATE_PIDCORE_SOUND_AGG_SQLSTR)
        pidgin_core_s_agg_tablename = create_prime_tablename("pidcore", "s", "agg")
        insert_into_clause = f"""INSERT INTO {pidgin_core_s_agg_tablename} (
  {face_name_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES
  ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidgin_road_s_agg_tablename} WHERE error_message IS NOT NULL;"
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_update_inconsist_pidgin_dimen_agg_sqlstr(pidroad_dimen)
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 5
        select_core_raw_sqlstr = f"SELECT * FROM {pidgin_road_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, yao_str, yao_inx, None, None, None, error_message),
            (1, sue_str, bob_str, bob_inx, None, None, None, error_message),
            (1, sue_str, bob_str, bob_str, None, "/", None, error_message),
            (2, sue_str, sue_str, sue_str, ":", ":", "Unknown", error_message),
            (5, sue_str, bob_str, bob_inx, ":", ":", "Unknown", error_message),
            (7, yao_str, yao_str, yao_inx, ":", ":", "Unknown", None),
        ]


def test_update_inconsistency_pidgin_sound_agg_tables_ReturnsObj_PopulatesTableCorrectly_Scenario0():
    # ESTABLISH
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_bridge = "/"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    error_message = "Inconsistent pidgin core data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        pidroad_dimen = pidgin_road_str()
        pidgin_road_s_agg_tablename = create_prime_tablename(pidroad_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {pidgin_road_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_bridge}', NULL)
, ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}')
, ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}')
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        pidgin_core_s_agg_tablename = create_prime_tablename("pidcore", "s", "agg")
        insert_into_clause = f"""INSERT INTO {pidgin_core_s_agg_tablename} (
  {face_name_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES
  ('{yao_str}', '{rdx}', '{rdx}', '{ukx}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidgin_road_s_agg_tablename} WHERE error_message IS NOT NULL;"
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        update_inconsistency_pidgin_sound_agg_tables(cursor)

        # THEN
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 5
        select_core_raw_sqlstr = f"SELECT * FROM {pidgin_road_s_agg_tablename}"
        cursor.execute(select_core_raw_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (1, sue_str, yao_str, yao_inx, None, None, None, error_message),
            (1, sue_str, bob_str, bob_inx, None, None, None, error_message),
            (1, sue_str, bob_str, bob_str, None, "/", None, error_message),
            (2, sue_str, sue_str, sue_str, ":", ":", "Unknown", error_message),
            (5, sue_str, bob_str, bob_inx, ":", ":", "Unknown", error_message),
            (7, yao_str, yao_str, yao_inx, ":", ":", "Unknown", None),
        ]


def test_create_insert_pidgin_sound_vld_table_sqlstr_ReturnsObj_PopulatesTableCorrectly_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_bridge = "/"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    error_message = "Inconsistent pidgin core data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        pidroad_dimen = pidgin_road_str()
        pidgin_road_s_agg_tablename = create_prime_tablename(pidroad_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {pidgin_road_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
, error_message
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL, '{error_message}')
, ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL, '{error_message}')
, ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_bridge}', NULL, '{error_message}')
, ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', '{error_message}')
, ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', '{error_message}')
, ({event1}, '{yao_str}', '{yao_str}', '{yao_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}', NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        pidgin_road_s_vld_tablename = create_prime_tablename("pidroad", "s", "vld")
        assert get_row_count(cursor, pidgin_road_s_agg_tablename) == 8
        assert get_row_count(cursor, pidgin_road_s_vld_tablename) == 0

        # WHEN
        sqlstr = create_insert_pidgin_sound_vld_table_sqlstr(pidroad_dimen)
        print(sqlstr)
        cursor.execute(sqlstr)

        # THEN
        assert get_row_count(cursor, pidgin_road_s_vld_tablename) == 3
        select_pidgin_road_s_vld_sqlstr = f"SELECT * FROM {pidgin_road_s_vld_tablename}"
        cursor.execute(select_pidgin_road_s_vld_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (event1, yao_str, yao_str, yao_str),
            (event7, bob_str, bob_str, bob_inx),
            (event7, yao_str, yao_str, yao_inx),
        ]


def test_insert_pidgin_sound_agg_tables_to_pidgin_sound_vld_table_ReturnsObj_PopulatesTableCorrectly_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_bridge = "/"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7
    error_message = "Inconsistent pidgin core data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        pidroad_dimen = pidgin_road_str()
        pidgin_road_s_agg_tablename = create_prime_tablename(pidroad_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {pidgin_road_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
, error_message
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL, '{error_message}')
, ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL, '{error_message}')
, ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_bridge}', NULL, '{error_message}')
, ({event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', '{error_message}')
, ({event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', '{error_message}')
, ({event1}, '{yao_str}', '{yao_str}', '{yao_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ({event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ({event7}, '{bob_str}', '{bob_str}', '{bob_inx}', NULL, NULL, '{ukx}', NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        pidgin_road_s_vld_tablename = create_prime_tablename("pidroad", "s", "vld")
        assert get_row_count(cursor, pidgin_road_s_agg_tablename) == 8
        assert get_row_count(cursor, pidgin_road_s_vld_tablename) == 0

        # WHEN
        insert_pidgin_sound_agg_tables_to_pidgin_sound_vld_table(cursor)

        # THEN
        assert get_row_count(cursor, pidgin_road_s_vld_tablename) == 3
        select_pidgin_road_s_vld_sqlstr = f"SELECT * FROM {pidgin_road_s_vld_tablename}"
        cursor.execute(select_pidgin_road_s_vld_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (event1, yao_str, yao_str, yao_str),
            (event7, bob_str, bob_str, bob_inx),
            (event7, yao_str, yao_str, yao_inx),
        ]


def test_etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables_ReturnsObj_PopulatesTableCorrectly_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    other_bridge = "/"
    ukx = "Unknown"
    event1 = 1
    event2 = 2
    event5 = 5
    event7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        pidroad_dimen = pidgin_road_str()
        pidgin_road_s_agg_tablename = create_prime_tablename(pidroad_dimen, "s", "agg")
        insert_into_clause = f"""INSERT INTO {pidgin_road_s_agg_tablename} (
  {event_int_str()}
, {face_name_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
)"""
        values_clause = f"""
VALUES
  ({event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL)
, ({event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, '{other_bridge}', NULL)
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
        etl_sound_agg_tables_to_pidgin_core_raw_table(cursor)
        pidgin_core_s_raw_tablename = create_prime_tablename("pidcore", "s", "raw")
        pidgin_core_s_agg_tablename = create_prime_tablename("pidcore", "s", "agg")
        pidgin_road_s_vld_tablename = create_prime_tablename("pidroad", "s", "vld")
        assert get_row_count(cursor, pidgin_road_s_agg_tablename) == 10
        select_error_count_sqlstr = f"SELECT COUNT(*) FROM {pidgin_road_s_agg_tablename} WHERE error_message IS NOT NULL;"
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 0
        assert get_row_count(cursor, pidgin_core_s_raw_tablename) == 6
        assert get_row_count(cursor, pidgin_core_s_agg_tablename) == 0
        assert get_row_count(cursor, pidgin_road_s_vld_tablename) == 0

        # WHEN
        etl_pidgin_sound_agg_tables_to_pidgin_sound_vld_tables(cursor)

        # THEN
        pidgin_road_s_agg_select = f"SELECT * FROM {pidgin_road_s_agg_tablename};"
        print(f"{cursor.execute(pidgin_road_s_agg_select).fetchall()=}\n")
        pidgin_core_s_raw_select = f"SELECT * FROM {pidgin_core_s_raw_tablename};"
        print(f"{cursor.execute(pidgin_core_s_raw_select).fetchall()=}\n")
        pidgin_core_s_agg_select = f"SELECT * FROM {pidgin_core_s_agg_tablename};"
        print(f"{cursor.execute(pidgin_core_s_agg_select).fetchall()=}\n")
        assert cursor.execute(select_error_count_sqlstr).fetchone()[0] == 5
        assert get_row_count(cursor, pidgin_core_s_agg_tablename) == 2
        assert get_row_count(cursor, pidgin_road_s_vld_tablename) == 3
        select_pidgin_road_s_vld_sqlstr = f"SELECT * FROM {pidgin_road_s_vld_tablename}"
        cursor.execute(select_pidgin_road_s_vld_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (event1, yao_str, yao_str, yao_str),
            (event7, bob_str, bob_str, bob_inx),
            (event7, yao_str, yao_str, yao_inx),
        ]
