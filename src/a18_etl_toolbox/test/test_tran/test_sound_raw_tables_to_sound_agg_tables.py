from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_row_count, get_table_columns
from src.a06_believer_logic.test._util.a06_str import (
    belief_label_str,
    believer_name_str,
    believer_partnerunit_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a16_pidgin_logic.test._util.a16_str import (
    inx_knot_str,
    inx_rope_str,
    otx_knot_str,
    otx_rope_str,
    pidgin_rope_str,
    unknown_str_str,
)
from src.a17_idea_logic.test._util.a17_str import error_message_str, idea_number_str
from src.a18_etl_toolbox.tran_sqlstrs import (
    CREATE_PIDROPE_SOUND_RAW_SQLSTR,
    create_prime_tablename,
    create_sound_and_voice_tables,
    create_sound_raw_update_inconsist_error_message_sqlstr,
)
from src.a18_etl_toolbox.transformers import (
    etl_sound_raw_tables_to_sound_agg_tables,
    insert_sound_raw_selects_into_sound_agg_tables,
    set_sound_raw_tables_error_message,
)


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ExecutedSqlUpdatesTableCorrectly_Scenario0():
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
        cursor.execute(CREATE_PIDROPE_SOUND_RAW_SQLSTR)
        pidrope_str = "pidgin_rope"
        pidrope_s_raw_tablename = create_prime_tablename(pidrope_str, "s", "raw")
        insert_into_clause = f"""INSERT INTO {pidrope_s_raw_tablename} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {otx_rope_str()}
, {inx_rope_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
, {error_message_str()}
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
        error_count_sqlstr = f"SELECT COUNT(*) FROM {pidrope_s_raw_tablename} WHERE {error_message_str()} IS NOT NULL"
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
            cursor, pidrope_str
        )
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 2


def test_set_sound_raw_tables_error_message_UpdatesTableCorrectly_Scenario0():
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
        create_sound_and_voice_tables(cursor)
        pidrope_s_raw_tablename = create_prime_tablename(pidgin_rope_str(), "s", "raw")
        insert_into_clause = f"""INSERT INTO {pidrope_s_raw_tablename} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {otx_rope_str()}
, {inx_rope_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
, {error_message_str()}
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
        error_count_sqlstr = f"SELECT COUNT(*) FROM {pidrope_s_raw_tablename} WHERE {error_message_str()} IS NOT NULL"
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        set_sound_raw_tables_error_message(cursor)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 2
        error_select_sqlstr = f"SELECT idea_number, event_int FROM {pidrope_s_raw_tablename} WHERE {error_message_str()} IS NOT NULL"
        cursor.execute(error_select_sqlstr)
        assert cursor.fetchall() == [("br00117", 1), ("br00077", 1)]


def test_set_sound_raw_tables_error_message_UpdatesTableCorrectly_Scenario1_believer_raw_del():
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
        create_sound_and_voice_tables(cursor)
        believera_s_raw_del = create_prime_tablename(
            believer_partnerunit_str(), "s", "raw", "del"
        )
        insert_into_clause = f"""INSERT INTO {believera_s_raw_del} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {belief_label_str()}
, {believer_name_str()}
, {partner_name_str()}_ERASE
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
        error_count_sqlstr = f"SELECT COUNT(*) FROM {believera_s_raw_del}"
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 4
        assert error_message_str() not in get_table_columns(cursor, believera_s_raw_del)

        # WHEN
        set_sound_raw_tables_error_message(cursor)

        # THEN No Error message is added and updated
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 4
        assert error_message_str() not in get_table_columns(cursor, believera_s_raw_del)


# TODO copy over and use these tests?
# test_belief_raw_tables2belief_agg_tables_Scenario0_beliefunit_WithNo_error_message
# test_belief_raw_tables2belief_agg_tables_Scenario1_beliefunit_With_error_message
# test_belief_raw_tables2belief_agg_tables_Scenario2_blfhour_Some_error_message
# test_belief_raw_tables2belief_agg_tables_Scenario3_blfmont_Some_error_message
# test_belief_raw_tables2belief_agg_tables_Scenario4_blfweek_Some_error_message
# test_belief_raw_tables2belief_agg_tables_Scenario5_beliefbud_Some_error_message
# test_belief_raw_tables2belief_agg_tables_Scenario6_blfpayy_Some_error_message


def test_insert_sound_raw_selects_into_sound_agg_tables_PopulatesValidTable_Scenario0():
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
        create_sound_and_voice_tables(cursor)
        pidrope_s_raw_tablename = create_prime_tablename("PIDROPE", "s", "raw")
        insert_into_clause = f"""INSERT INTO {pidrope_s_raw_tablename} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {otx_rope_str()}
, {inx_rope_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
, {error_message_str()}
)"""
        b117 = "br00117"
        b020 = "br00020"
        b045 = "br00045"
        inconsistent_data_str = "Inconsistent data"
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
        blrpern_s_put_raw_tblname = create_prime_tablename("BLRPERN", "s", "raw", "put")
        insert_into_clause = f"""INSERT INTO {blrpern_s_put_raw_tblname} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {belief_label_str()}
, {believer_name_str()}
, {partner_name_str()}
, {partner_cred_points_str()}
, {partner_debt_points_str()}
, {error_message_str()}
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
        pidrope_s_agg_tablename = create_prime_tablename("PIDROPE", "s", "agg")
        blrpern_s_put_agg_tblname = create_prime_tablename("BLRPERN", "s", "agg", "put")
        assert get_row_count(cursor, pidrope_s_raw_tablename) == 7
        assert get_row_count(cursor, blrpern_s_put_raw_tblname) == 6
        assert get_row_count(cursor, pidrope_s_agg_tablename) == 0
        assert get_row_count(cursor, blrpern_s_put_agg_tblname) == 0

        # WHEN
        insert_sound_raw_selects_into_sound_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, pidrope_s_agg_tablename) == 2
        assert get_row_count(cursor, blrpern_s_put_agg_tblname) == 2

        select_agg_sqlstr = f"""SELECT * FROM {pidrope_s_agg_tablename};"""
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert len(rows) == 2
        assert rows == [
            (event1, sue_str, bob_str, bob_inx, None, None, None, None),
            (event2, sue_str, sue_str, sue_str, rdx, rdx, ukx, None),
        ]

        select_agg_sqlstr = f"""SELECT * FROM {blrpern_s_put_agg_tblname};"""
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert len(rows) == 2
        assert rows == [
            (event1, sue_str, a23_str, bob_str, bob_str, None, None, None),
            (event1, sue_str, a23_str, yao_str, yao_str, None, None, None),
        ]


def test_insert_sound_raw_selects_into_sound_agg_tables_PopulatesValidTable_Scenario1_del_table():
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
    b117 = "br00117"
    b020 = "br00020"
    b045 = "br00045"
    inconsistent_data_str = "Inconsistent data"

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        blrpern_s_del_raw_tblname = create_prime_tablename("BLRPERN", "s", "raw", "del")
        insert_into_clause = f"""INSERT INTO {blrpern_s_del_raw_tblname} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {belief_label_str()}
, {believer_name_str()}
, {partner_name_str()}_ERASE
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
        blrpern_s_del_agg_tblname = create_prime_tablename("BLRPERN", "s", "agg", "del")
        assert get_row_count(cursor, blrpern_s_del_raw_tblname) == 6
        assert get_row_count(cursor, blrpern_s_del_agg_tblname) == 0

        # WHEN
        insert_sound_raw_selects_into_sound_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, blrpern_s_del_agg_tblname) == 3

        select_agg_sqlstr = f"""SELECT * FROM {blrpern_s_del_agg_tblname};"""
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (event1, sue_str, a23_str, bob_str, bob_str, None),
            (event1, sue_str, a23_str, bob_str, yao_str, None),
            (event1, sue_str, a23_str, yao_str, yao_str, None),
        ]


def test_etl_sound_raw_tables_to_sound_agg_tables_PopulatesValidTable_Scenario0():
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
        create_sound_and_voice_tables(cursor)
        pidrope_s_raw_tablename = create_prime_tablename("PIDROPE", "s", "raw")
        insert_into_clause = f"""INSERT INTO {pidrope_s_raw_tablename} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {otx_rope_str()}
, {inx_rope_str()}
, {otx_knot_str()}
, {inx_knot_str()}
, {unknown_str_str()}
, {error_message_str()}
)"""
        b117 = "br00117"
        b020 = "br00020"
        b045 = "br00045"
        inconsistent_data_str = "Inconsistent data"
        values_clause = f"""
VALUES
  ('{b117}', {event1}, '{sue_str}', '{yao_str}', '{yao_inx}', NULL, NULL, NULL, NULL)
, ('{b117}', {event1}, '{sue_str}', '{yao_str}', '{yao_str}', NULL, NULL, NULL, NULL)
, ('{b117}', {event1}, '{sue_str}', '{bob_str}', '{bob_inx}', NULL, NULL, NULL, NULL)
, ('{b117}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b117}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {event2}, '{sue_str}', '{sue_str}', '{sue_str}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {event5}, '{sue_str}', '{bob_str}', '{bob_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
, ('{b045}', {event7}, '{yao_str}', '{bob_str}', '{yao_inx}', '{rdx}', '{rdx}', '{ukx}', NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        blrpern_s_put_raw_tblname = create_prime_tablename("BLRPERN", "s", "raw", "put")
        insert_into_clause = f"""INSERT INTO {blrpern_s_put_raw_tblname} (
  {idea_number_str()}
, {event_int_str()}
, {face_name_str()}
, {belief_label_str()}
, {believer_name_str()}
, {partner_name_str()}
, {partner_cred_points_str()}
, {partner_debt_points_str()}
, {error_message_str()}
)"""
        values_clause = f"""
VALUES
  ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{yao_str}', NULL, NULL, NULL)
, ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
, ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
, ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
, ('{b117}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
, ('{b020}', {event1}, '{sue_str}', '{a23_str}', '{bob_str}', '{bob_str}', NULL, NULL, NULL)
, ('{b020}', {event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}', NULL, NULL, NULL)
;
"""
        cursor.execute(f"{insert_into_clause} {values_clause}")
        pidrope_s_agg_tablename = create_prime_tablename("PIDROPE", "s", "agg")
        blrpern_s_put_agg_tblname = create_prime_tablename("BLRPERN", "s", "agg", "put")
        assert get_row_count(cursor, pidrope_s_raw_tablename) == 8
        assert get_row_count(cursor, blrpern_s_put_raw_tblname) == 7
        assert get_row_count(cursor, pidrope_s_agg_tablename) == 0
        assert get_row_count(cursor, blrpern_s_put_agg_tblname) == 0

        # WHEN
        etl_sound_raw_tables_to_sound_agg_tables(cursor)

        # THEN
        assert get_row_count(cursor, pidrope_s_agg_tablename) == 4
        assert get_row_count(cursor, blrpern_s_put_agg_tblname) == 3

        select_agg_sqlstr = f"""SELECT * FROM {pidrope_s_agg_tablename};"""
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (event1, sue_str, bob_str, bob_inx, None, None, None, None),
            (event2, sue_str, sue_str, sue_str, rdx, rdx, ukx, None),
            (event5, sue_str, bob_str, bob_inx, rdx, rdx, ukx, None),
            (event7, yao_str, bob_str, yao_inx, rdx, rdx, ukx, None),
        ]

        select_agg_sqlstr = f"""SELECT * FROM {blrpern_s_put_agg_tblname};"""
        cursor.execute(select_agg_sqlstr)
        rows = cursor.fetchall()
        print(rows)
        assert rows == [
            (event1, sue_str, a23_str, bob_str, bob_str, None, None, None),
            (event1, sue_str, a23_str, bob_str, yao_str, None, None, None),
            (event1, sue_str, a23_str, yao_str, yao_str, None, None, None),
        ]
