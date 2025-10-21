from sqlite3 import connect as sqlite3_connect
from src.ch18_world_etl.tran_sqlstrs import (
    CREATE_BLFVOCE_SOUND_PUT_AGG_STR,
    CREATE_TRLCORE_SOUND_VLD_SQLSTR,
    create_knot_exists_in_label_error_update_sqlstr,
    create_knot_exists_in_name_error_update_sqlstr,
    create_prime_tablename,
)
from src.ch18_world_etl.transformers import set_moment_belief_sound_agg_knot_errors
from src.ref.keywords import Ch18Keywords as kw


def test_create_knot_exists_in_name_error_update_sqlstr_ReturnsObj_PopulatesTable_Scenario0():
    # ESTABLISH
    a23_str = "amy23"
    sue_str = "Sue"
    yao_str = "Yao"
    colon = ":"
    bob_str = f"{colon}Bob"
    comma = ","
    ukx = "Unknown"
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_BLFVOCE_SOUND_PUT_AGG_STR)
        blfvoce_dimen = kw.belief_voiceunit
        blfvoce_s_agg_put = create_prime_tablename(blfvoce_dimen, "s", "agg", "put")
        insert_blfvoce_sqlstr = f"""INSERT INTO {blfvoce_s_agg_put} (
  {kw.spark_num}, {kw.face_name}, {kw.moment_label}, {kw.belief_name}, {kw.voice_name})
VALUES
  ({spark1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
, ({spark1}, '{sue_str}', '{a23_str}', '{yao_str}', '{bob_str}')
;
"""
        cursor.execute(insert_blfvoce_sqlstr)
        cursor.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
        trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename} (
  {kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
VALUES
  ('{sue_str}', '{colon}', '{colon}', '{ukx}')
, ('{yao_str}', '{comma}', '{comma}', '{ukx}')
;
"""
        cursor.execute(insert_trlcore_sqlstr)
        error_count_sqlstr = f"SELECT COUNT(*) FROM {blfvoce_s_agg_put} WHERE {kw.error_message} IS NOT NULL"
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_knot_exists_in_name_error_update_sqlstr(
            blfvoce_s_agg_put, kw.voice_name
        )
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 1
        select_core_raw_sqlstr = f"SELECT * FROM {blfvoce_s_agg_put}"
        cursor.execute(select_core_raw_sqlstr)
        name_knot_str = f"Knot cannot exist in NameTerm column {kw.voice_name}"
        assert cursor.fetchall() == [
            (spark1, sue_str, a23_str, yao_str, yao_str, None, None, None),
            (spark1, sue_str, a23_str, yao_str, bob_str, None, None, name_knot_str),
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
    spark1 = 1

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_BLFVOCE_SOUND_PUT_AGG_STR)
        blfvoce_dimen = kw.belief_voiceunit
        blfvoce_s_agg_put = create_prime_tablename(blfvoce_dimen, "s", "agg", "put")
        insert_blfvoce_sqlstr = f"""INSERT INTO {blfvoce_s_agg_put} (
  {kw.spark_num}, {kw.face_name}, {kw.moment_label}, {kw.belief_name}, {kw.voice_name})
VALUES
  ({spark1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
, ({spark1}, '{sue_str}', '{a23_str}', '{yao_str}', '{bob_str}')
, ({spark1}, '{sue_str}', '{a45_str}', '{yao_str}', '{bob_str}')
;
"""
        cursor.execute(insert_blfvoce_sqlstr)
        cursor.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
        trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename} (
  {kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
VALUES
  ('{sue_str}', '{colon}', '{colon}', '{ukx}')
, ('{yao_str}', '{comma}', '{comma}', '{ukx}')
;
"""
        cursor.execute(insert_trlcore_sqlstr)
        error_count_sqlstr = f"SELECT COUNT(*) FROM {blfvoce_s_agg_put} WHERE {kw.error_message} IS NOT NULL"
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        sqlstr = create_knot_exists_in_label_error_update_sqlstr(
            blfvoce_s_agg_put, kw.moment_label
        )
        print(f"{sqlstr=}")
        cursor.execute(sqlstr)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 1
        select_core_raw_sqlstr = f"SELECT * FROM {blfvoce_s_agg_put}"
        cursor.execute(select_core_raw_sqlstr)
        label_knot_str = f"Knot cannot exist in LabelTerm column {kw.moment_label}"
        assert cursor.fetchall() == [
            (spark1, sue_str, a23_str, yao_str, yao_str, None, None, None),
            (spark1, sue_str, a23_str, yao_str, bob_str, None, None, None),
            (spark1, sue_str, a45_str, yao_str, bob_str, None, None, label_knot_str),
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
    spark1 = 1
    spark7 = 7

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        cursor.execute(CREATE_BLFVOCE_SOUND_PUT_AGG_STR)
        blfvoce_dimen = kw.belief_voiceunit
        blfvoce_s_agg_put = create_prime_tablename(blfvoce_dimen, "s", "agg", "put")
        insert_blfvoce_sqlstr = f"""INSERT INTO {blfvoce_s_agg_put} (
  {kw.spark_num}, {kw.face_name}, {kw.moment_label}, {kw.belief_name}, {kw.voice_name})
VALUES
  ({spark1}, '{sue_str}', '{a23_str}', '{yao_str}', '{yao_str}')
, ({spark1}, '{sue_str}', '{a23_str}', '{yao_str}', '{bob_str}')
, ({spark1}, '{sue_str}', '{a45_str}', '{yao_str}', '{yao_str}')
;
"""
        cursor.execute(insert_blfvoce_sqlstr)
        cursor.execute(CREATE_TRLCORE_SOUND_VLD_SQLSTR)
        trlcore_s_vld_tablename = create_prime_tablename("trlcore", "s", "vld")
        insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename} (
  {kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
VALUES
  ('{sue_str}', '{colon}', '{colon}', '{ukx}')
, ('{yao_str}', '{comma}', '{comma}', '{ukx}')
;
"""
        cursor.execute(insert_trlcore_sqlstr)
        error_count_sqlstr = f"SELECT COUNT(*) FROM {blfvoce_s_agg_put} WHERE {kw.error_message} IS NOT NULL"
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 0

        # WHEN
        set_moment_belief_sound_agg_knot_errors(cursor)

        # THEN
        assert cursor.execute(error_count_sqlstr).fetchone()[0] == 2
        select_core_raw_sqlstr = f"SELECT * FROM {blfvoce_s_agg_put} ORDER BY {kw.moment_label}, {kw.belief_name}, {kw.voice_name}"
        cursor.execute(select_core_raw_sqlstr)
        name_knot_str = f"Knot cannot exist in NameTerm column {kw.voice_name}"
        label_knot_str = f"Knot cannot exist in LabelTerm column {kw.moment_label}"
        rows = cursor.fetchall()
        print(f"{rows=}")
        assert rows == [
            (spark1, sue_str, a45_str, yao_str, yao_str, None, None, label_knot_str),
            (spark1, sue_str, a23_str, yao_str, bob_str, None, None, name_knot_str),
            (spark1, sue_str, a23_str, yao_str, yao_str, None, None, None),
        ]
