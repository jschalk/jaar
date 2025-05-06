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
from src.a16_pidgin_logic._utils.str_a16 import (
    pidgin_road_str,
    inx_bridge_str,
    otx_bridge_str,
    inx_road_str,
    otx_road_str,
    unknown_word_str,
)
from src.a17_idea_logic.idea_db_tool import create_idea_sorted_table
from src.a17_idea_logic._utils.str_a17 import (
    brick_valid_str,
    idea_number_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename,
    create_sound_and_voice_tables,
    CREATE_FISCASH_SOUND_RAW_SQLSTR,
    CREATE_PIDROAD_SOUND_RAW_SQLSTR,
    CREATE_PIDROAD_SOUND_AGG_SQLSTR,
    CREATE_BUDACCT_SOUND_PUT_RAW_STR,
    CREATE_BUDACCT_SOUND_PUT_AGG_STR,
    create_sound_raw_update_inconsist_error_message_sqlstr,
)
from src.a18_etl_toolbox.transformers import (
    insert_sound_raw_selects_into_sound_agg_tables,
    set_sound_tables_raw_error_message,
)
from sqlite3 import connect as sqlite3_connect


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ExecutedSqlUpdatesTableCorrectly_Scenario0():
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
        cursor.execute(CREATE_PIDROAD_SOUND_RAW_SQLSTR)
        pidroad_str = "pidgin_road"
        pidroad_s_raw_tablename = create_prime_tablename(pidroad_str, "s", "raw")
        insert_into_clause = f"""INSERT INTO {pidroad_s_raw_tablename} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
, "error_message"
)"""
        b117 = "br00117"
        b045 = "br00045"
        b077 = "br00077"
        values_clause = f"""
VALUES
  ('{b117}', {event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL, NULL)
, ('{b117}', {event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL, NULL)
, ('{b077}', {event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL, NULL)
, ('{b045}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        error_count_sqlstr = f"SELECT COUNT(*) FROM {pidroad_s_raw_tablename} WHERE error_message IS NOT NULL"
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
            cursor, pidroad_str
        )
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 2


def test_set_sound_tables_raw_error_message_UpdatesTableCorrectly_Scenario0():
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
        create_sound_and_voice_tables(cursor)
        pidroad_s_raw_tablename = create_prime_tablename(pidgin_road_str(), "s", "raw")
        insert_into_clause = f"""INSERT INTO {pidroad_s_raw_tablename} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
, "error_message"
)"""
        b117 = "br00117"
        b045 = "br00045"
        b077 = "br00077"
        values_clause = f"""
VALUES
  ('{b117}', {event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL, NULL)
, ('{b117}', {event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL, NULL)
, ('{b077}', {event1}, '{sue_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL, NULL)
, ('{b045}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        error_count_sqlstr = f"SELECT COUNT(*) FROM {pidroad_s_raw_tablename} WHERE error_message IS NOT NULL"
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        set_sound_tables_raw_error_message(cursor)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 2
        error_select_sqlstr = f"SELECT idea_number, event_int FROM {pidroad_s_raw_tablename} WHERE error_message IS NOT NULL"
        cursor.execute(error_select_sqlstr)
        assert cursor.fetchall() == [("br00117", 1), ("br00077", 1)]


def test_set_sound_tables_raw_error_message_UpdatesTableCorrectly_Scenario1_bud_raw_del():
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
        create_sound_and_voice_tables(cursor)
        buda_s_raw_del = create_prime_tablename(bud_acctunit_str(), "s", "raw", "del")
        insert_into_clause = f"""INSERT INTO {buda_s_raw_del} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {fisc_tag_str()}
, {owner_name_str()}
, {acct_name_str()}_ERASE
)"""
        b117 = "br00117"
        b045 = "br00045"
        b077 = "br00077"
        values_clause = f"""
VALUES
  ('{b117}', {event1}, '{sue_str}', '{a23_str}','{yao_str}', '{yao_inx}')
, ('{b117}', {event1}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_inx}')
, ('{b117}', {event1}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_inx}')
, ('{b077}', {event1}, '{sue_str}', '{a23_str}','{bob_str}', '{bob_str}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        error_count_sqlstr = f"SELECT COUNT(*) FROM {buda_s_raw_del}"
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 4
        assert "error_message" not in get_table_columns(cursor, buda_s_raw_del)

        # WHEN
        set_sound_tables_raw_error_message(cursor)

        # THEN No Error message is added and updated
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 4
        assert "error_message" not in get_table_columns(cursor, buda_s_raw_del)


# TODO copy over and use these tests?
# test_fisc_raw_tables2fisc_agg_tables_Scenario0_fisunit_WithNo_error_message
# test_fisc_raw_tables2fisc_agg_tables_Scenario1_fisunit_With_error_message
# test_fisc_raw_tables2fisc_agg_tables_Scenario2_fishour_Some_error_message
# test_fisc_raw_tables2fisc_agg_tables_Scenario3_fismont_Some_error_message
# test_fisc_raw_tables2fisc_agg_tables_Scenario4_fisweek_Some_error_message
# test_fisc_raw_tables2fisc_agg_tables_Scenario5_fisdeal_Some_error_message
# test_fisc_raw_tables2fisc_agg_tables_Scenario6_fiscash_Some_error_message


def test_insert_sound_raw_selects_into_sound_agg_tables_PopulatesValidTable_Scenario0():
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
        create_sound_and_voice_tables(cursor)
        pidroad_s_raw_tablename = create_prime_tablename("PIDROAD", "s", "raw")
        insert_into_clause = f"""INSERT INTO {pidroad_s_raw_tablename} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {otx_road_str()}
, {inx_road_str()}
, {otx_bridge_str()}
, {inx_bridge_str()}
, {unknown_word_str()}
, "error_message"
)"""
        b117 = "br00117"
        b020 = "br00020"
        b045 = "br00045"
        inconsistent_data_str = "inconsistent data"
        values_clause = f"""
VALUES
  ('{b117}', {event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL, '{inconsistent_data_str}')
, ('{b117}', {event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL, NULL)
, ('{b117}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b117}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', '{inconsistent_data_str}')
, ('{b045}', {event7}, '{yao_str}', '{yao_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', '{inconsistent_data_str}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        budacct_s_put_raw_tblname = create_prime_tablename("BUDACCT", "s", "raw", "put")
        insert_into_clause = f"""INSERT INTO {budacct_s_put_raw_tblname} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {fisc_tag_str()}
, {owner_name_str()}
, {acct_name_str()}
, {credit_belief_str()}
, {debtit_belief_str()}
, "error_message"
)"""
        values_clause = f"""
VALUES
  ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{yao_str}', NULL, NULL, '{inconsistent_data_str}')
, ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
, ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
, ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
, ('{b020}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
, ('{b020}', {event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}', NULL, NULL, NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        pidroad_s_agg_tablename = create_prime_tablename("PIDROAD", "s", "agg")
        budacct_s_put_agg_tblname = create_prime_tablename("BUDACCT", "s", "agg", "put")
        assert get_row_count(cursor, pidroad_s_raw_tablename) == 7
        assert get_row_count(cursor, budacct_s_put_raw_tblname) == 6
        assert get_row_count(cursor, pidroad_s_agg_tablename) == 0
        assert get_row_count(cursor, budacct_s_put_agg_tblname) == 0

        # WHEN
        insert_sound_raw_selects_into_sound_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, pidroad_s_agg_tablename) == 2
        assert get_row_count(cursor, budacct_s_put_agg_tblname) == 2

        select_agg_sqlstr = f"""SELECT * FROM {pidroad_s_agg_tablename};"""
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert len(rows) == 2
        # TODO identify expected output
        assert rows == [
            (event1, sue_str, bob_str, bob_inx, None, None, None),
            (event2, sue_str, sue_str, sue_str, rdx, rdx, ukx),
        ]

        select_agg_sqlstr = f"""SELECT * FROM {budacct_s_put_agg_tblname};"""
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert len(rows) == 2
        # TODO identify expected output
        assert rows == [
            (event1, sue_str, a23_str, bob_str, bob_str, None, None),
            (event1, sue_str, a23_str, yao_str, yao_str, None, None),
        ]


def test_insert_sound_raw_selects_into_sound_agg_tables_PopulatesValidTable_Scenario1_del_table():
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
    b117 = "br00117"
    b020 = "br00020"
    b045 = "br00045"
    inconsistent_data_str = "inconsistent data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        budacct_s_del_raw_tblname = create_prime_tablename("BUDACCT", "s", "raw", "del")
        insert_into_clause = f"""INSERT INTO {budacct_s_del_raw_tblname} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {fisc_tag_str()}
, {owner_name_str()}
, {acct_name_str()}_ERASE
)"""
        values_clause = f"""
VALUES
  ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{yao_str}')
, ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}')
, ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}')
, ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}')
, ('{b020}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}')
, ('{b020}', {event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        budacct_s_del_agg_tblname = create_prime_tablename("BUDACCT", "s", "agg", "del")
        assert get_row_count(cursor, budacct_s_del_raw_tblname) == 6
        assert get_row_count(cursor, budacct_s_del_agg_tblname) == 0

        # WHEN
        insert_sound_raw_selects_into_sound_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, budacct_s_del_agg_tblname) == 3

        select_agg_sqlstr = f"""SELECT * FROM {budacct_s_del_agg_tblname};"""
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        # TODO identify expected output
        assert rows == [
            (event1, sue_str, a23_str, bob_str, bob_str),
            (event1, sue_str, a23_str, bob_str, yao_str),
            (event1, sue_str, a23_str, yao_str, yao_str),
        ]
