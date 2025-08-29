from sqlite3 import connect as sqlite3_connect
from src.a18_etl_toolbox.test._util.a18_str import (
    belief_name_str,
    belief_voiceunit_str,
    error_message_str,
    event_int_str,
    face_name_str,
    inx_knot_str,
    moment_label_str,
    otx_knot_str,
    unknown_str_str,
    voice_name_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    CREATE_BLRPERN_SOUND_PUT_AGG_STR,
    CREATE_PIDCORE_SOUND_VLD_SQLSTR,
    create_knot_exists_in_label_error_update_sqlstr,
    create_knot_exists_in_name_error_update_sqlstr,
    create_prime_tablename,
)
from src.a18_etl_toolbox.transformers import set_moment_belief_sound_agg_knot_errors


def test_create_knot_exists_in_name_error_update_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    a23_str = "amy23"
    sue_str = "Sue"
    yao_str = "Yao"
    colon = ":"
    bob_str = f"{colon}Bob"
    comma = ","
    ukx = "Unknown"
    event1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_BLRPERN_SOUND_PUT_AGG_STR)
        blrpern_dimen = belief_voiceunit_str()
        blrpern_s_agg_put = create_prime_tablename(blrpern_dimen, "s", "agg", "put")
        insert_blrpern_sqlstr = f"""INSERT INTO {blrpern_s_agg_put} (
  {event_int_str()}, {face_name_str()}, {moment_label_str()}, {belief_name_str()}, {voice_name_str()})
VALUES
  ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
, ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{bob_str}')
;
"""
        cursor.execute(insert_blrpern_sqlstr)
        cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
        pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename} (
  {face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES
  ('{sue_str}', '{colon}', '{colon}', '{ukx}')
, ('{yao_str}', '{comma}', '{comma}', '{ukx}')
;
"""
        cursor.execute(insert_pidcore_sqlstr)
        error_count_sqlstr = f"SELECT COUNT(*) FROM {blrpern_s_agg_put} WHERE {error_message_str()} IS NOT NULL"
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_knot_exists_in_name_error_update_sqlstr(
            blrpern_s_agg_put, voice_name_str()
        )
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 1
        select_core_raw_sqlstr = f"SELECT * FROM {blrpern_s_agg_put}"
        cursor.execute(select_core_raw_sqlstr)
        name_knot_str = f"Knot cannot exist in NameTerm column {voice_name_str()}"
        assert cursor.fetchall() == [
            (event1, sue_str, a23_str, yao_str, yao_str, None, None, None),
            (event1, sue_str, a23_str, yao_str, bob_str, None, None, name_knot_str),
        ]


def test_create_knot_exists_in_label_error_update_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    colon = ":"
    bob_str = f"{colon}Bob"
    a23_str = "amy23"
    a45_str = f"{colon}amy45"
    comma = ","
    ukx = "Unknown"
    event1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_BLRPERN_SOUND_PUT_AGG_STR)
        blrpern_dimen = belief_voiceunit_str()
        blrpern_s_agg_put = create_prime_tablename(blrpern_dimen, "s", "agg", "put")
        insert_blrpern_sqlstr = f"""INSERT INTO {blrpern_s_agg_put} (
  {event_int_str()}, {face_name_str()}, {moment_label_str()}, {belief_name_str()}, {voice_name_str()})
VALUES
  ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
, ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{bob_str}')
, ({event1}, '{sue_str}', '{a45_str}', '{yao_str}', '{bob_str}')
;
"""
        cursor.execute(insert_blrpern_sqlstr)
        cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
        pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename} (
  {face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES
  ('{sue_str}', '{colon}', '{colon}', '{ukx}')
, ('{yao_str}', '{comma}', '{comma}', '{ukx}')
;
"""
        cursor.execute(insert_pidcore_sqlstr)
        error_count_sqlstr = f"SELECT COUNT(*) FROM {blrpern_s_agg_put} WHERE {error_message_str()} IS NOT NULL"
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_knot_exists_in_label_error_update_sqlstr(
            blrpern_s_agg_put, moment_label_str()
        )
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 1
        select_core_raw_sqlstr = f"SELECT * FROM {blrpern_s_agg_put}"
        cursor.execute(select_core_raw_sqlstr)
        label_knot_str = f"Knot cannot exist in LabelTerm column {moment_label_str()}"
        assert cursor.fetchall() == [
            (event1, sue_str, a23_str, yao_str, yao_str, None, None, None),
            (event1, sue_str, a23_str, yao_str, bob_str, None, None, None),
            (event1, sue_str, a45_str, yao_str, bob_str, None, None, label_knot_str),
        ]


def test_set_moment_belief_sound_agg_knot_errors_PopulatesTable_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    yao_str = "Yao"
    colon = ":"
    bob_str = f"{colon}Bob"
    a23_str = "amy23"
    a45_str = f"{colon}amy45"
    comma = ","
    ukx = "Unknown"
    event1 = 1
    event7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_BLRPERN_SOUND_PUT_AGG_STR)
        blrpern_dimen = belief_voiceunit_str()
        blrpern_s_agg_put = create_prime_tablename(blrpern_dimen, "s", "agg", "put")
        insert_blrpern_sqlstr = f"""INSERT INTO {blrpern_s_agg_put} (
  {event_int_str()}, {face_name_str()}, {moment_label_str()}, {belief_name_str()}, {voice_name_str()})
VALUES
  ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
, ({event1}, '{sue_str}', '{a23_str}', '{yao_str}', '{bob_str}')
, ({event1}, '{sue_str}', '{a45_str}', '{yao_str}', '{yao_str}')
;
"""
        cursor.execute(insert_blrpern_sqlstr)
        cursor.execute(CREATE_PIDCORE_SOUND_VLD_SQLSTR)
        pidcore_s_vld_tablename = create_prime_tablename("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename} (
  {face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES
  ('{sue_str}', '{colon}', '{colon}', '{ukx}')
, ('{yao_str}', '{comma}', '{comma}', '{ukx}')
;
"""
        cursor.execute(insert_pidcore_sqlstr)
        error_count_sqlstr = f"SELECT COUNT(*) FROM {blrpern_s_agg_put} WHERE {error_message_str()} IS NOT NULL"
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        set_moment_belief_sound_agg_knot_errors(cursor)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 2
        select_core_raw_sqlstr = f"SELECT * FROM {blrpern_s_agg_put} ORDER BY {moment_label_str()}, {belief_name_str()}, {voice_name_str()}"
        cursor.execute(select_core_raw_sqlstr)
        name_knot_str = f"Knot cannot exist in NameTerm column {voice_name_str()}"
        label_knot_str = f"Knot cannot exist in LabelTerm column {moment_label_str()}"
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [
            (event1, sue_str, a45_str, yao_str, yao_str, None, None, label_knot_str),
            (event1, sue_str, a23_str, yao_str, bob_str, None, None, name_knot_str),
            (event1, sue_str, a23_str, yao_str, yao_str, None, None, None),
        ]
