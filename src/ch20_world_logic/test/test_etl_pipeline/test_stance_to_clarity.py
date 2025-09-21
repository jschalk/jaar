from os.path import exists as os_path_exists
from pandas import DataFrame
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_row_count
from src.a00_data_toolbox.file_toolbox import create_path
from src.ch17_idea_logic.idea_db_tool import create_idea_sorted_table, upsert_sheet
from src.ch18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.ch18_etl_toolbox.transformers import get_max_brick_agg_event_int
from src.ch20_world_logic._ref.ch20_terms import (
    belief_name_str,
    brick_agg_str,
    bud_time_str,
    celldepth_str,
    cumulative_minute_str,
    event_int_str,
    events_brick_agg_str,
    events_brick_valid_str,
    face_name_str,
    hour_label_str,
    inx_name_str,
    moment_label_str,
    moment_ote1_agg_str,
    otx_name_str,
    quota_str,
    voice_name_str,
)
from src.ch20_world_logic.test._util.ch20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as worlds_dir,
)
from src.ch20_world_logic.world import WorldUnit, worldunit_shop


def test_WorldUnit_stance_sheets_to_clarity_mstr_Scenario0_CreatesDatabaseFile(
    env_dir_setup_cleanup,
):  # sourcery skip: extract-method
    # ESTABLISH:
    fay_str = "Fay34"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    # delete_dir(fay_world.worlds_dir)
    sue_str = "Sue"
    sue_inx = "Suzy"
    ex_filename = "stance_Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00113_columns = [
        face_name_str(),
        moment_label_str(),
        belief_name_str(),
        voice_name_str(),
        otx_name_str(),
        inx_name_str(),
    ]
    a23_str = "amy2345"
    tp37 = 37
    br00113_str = "br00113"
    br00113row0 = [sue_str, a23_str, sue_str, sue_str, sue_str, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(input_file_path, br00113_ex0_str, br00113_df)

    br00001_columns = [
        face_name_str(),
        moment_label_str(),
        belief_name_str(),
        bud_time_str(),
        quota_str(),
        celldepth_str(),
    ]
    tp37 = 37
    sue_quota = 235
    sue_celldepth = 3
    br1row0 = [sue_str, a23_str, sue_str, tp37, sue_quota, sue_celldepth]
    br00001_1df = DataFrame([br1row0], columns=br00001_columns)
    br00001_ex0_str = "example0_br00001"
    upsert_sheet(input_file_path, br00001_ex0_str, br00001_1df)
    fay_db_path = fay_world.get_world_db_path()
    assert not os_path_exists(fay_db_path)

    # WHEN
    fay_world.stance_sheets_to_clarity_mstr()

    # THEN
    assert os_path_exists(fay_db_path)
    with sqlite3_connect(fay_db_path) as db_conn:
        br00113_raw = f"{br00113_str}_brick_raw"
        br00113_agg = f"{br00113_str}_brick_agg"
        br00113_valid = f"{br00113_str}_brick_valid"
        events_brick_valid_tablename = events_brick_valid_str()
        pidname_sound_raw = create_prime_tablename("pidname", "s", "raw")
        pidname_sound_agg = create_prime_tablename("pidname", "s", "agg")
        pidname_sound_vld = create_prime_tablename("pidname", "s", "vld")
        pidcore_sound_raw = create_prime_tablename("pidcore", "s", "raw")
        pidcore_sound_agg = create_prime_tablename("pidcore", "s", "agg")
        pidcore_sound_vld = create_prime_tablename("pidcore", "s", "vld")
        momentunit_sound_raw = create_prime_tablename("momentunit", "s", "raw")
        momentunit_sound_agg = create_prime_tablename("momentunit", "s", "agg")
        blrunit_sound_put_raw = create_prime_tablename("beliefunit", "s", "raw", "put")
        blrunit_sound_put_agg = create_prime_tablename("beliefunit", "s", "agg", "put")
        blrpern_sound_put_raw = create_prime_tablename("blrpern", "s", "raw", "put")
        blrpern_sound_put_agg = create_prime_tablename("blrpern", "s", "agg", "put")
        momentunit_heard_raw = create_prime_tablename("momentunit", "h", "raw")
        momentunit_heard_agg = create_prime_tablename("momentunit", "h", "agg")
        blrunit_heard_put_raw = create_prime_tablename("beliefunit", "h", "raw", "put")
        blrunit_heard_put_agg = create_prime_tablename("beliefunit", "h", "agg", "put")
        blrpern_heard_put_raw = create_prime_tablename("blrpern", "h", "raw", "put")
        blrpern_heard_put_agg = create_prime_tablename("blrpern", "h", "agg", "put")

        cursor = db_conn.cursor()
        assert get_row_count(cursor, br00113_raw) == 1
        assert get_row_count(cursor, br00113_agg) == 1
        assert get_row_count(cursor, events_brick_agg_str()) == 2
        assert get_row_count(cursor, events_brick_valid_tablename) == 2
        assert get_row_count(cursor, br00113_valid) == 2
        assert get_row_count(cursor, pidname_sound_raw) == 2
        assert get_row_count(cursor, momentunit_sound_raw) == 4
        assert get_row_count(cursor, blrunit_sound_put_raw) == 4
        assert get_row_count(cursor, blrpern_sound_put_raw) == 2
        assert get_row_count(cursor, pidname_sound_agg) == 1
        assert get_row_count(cursor, momentunit_sound_agg) == 1
        assert get_row_count(cursor, blrunit_sound_put_agg) == 1
        assert get_row_count(cursor, blrpern_sound_put_agg) == 1
        assert get_row_count(cursor, pidcore_sound_raw) == 1
        assert get_row_count(cursor, pidcore_sound_agg) == 1
        assert get_row_count(cursor, pidcore_sound_vld) == 1
        assert get_row_count(cursor, pidname_sound_vld) == 1
        assert get_row_count(cursor, momentunit_heard_raw) == 1
        assert get_row_count(cursor, blrunit_heard_put_raw) == 1
        assert get_row_count(cursor, blrpern_heard_put_raw) == 1
        assert get_row_count(cursor, momentunit_heard_agg) == 1
        assert get_row_count(cursor, blrunit_heard_put_agg) == 1
        assert get_row_count(cursor, blrpern_heard_put_agg) == 1
        assert get_row_count(cursor, moment_ote1_agg_str()) == 1
    db_conn.close()


def create_brick_agg_record(world: WorldUnit, event_int: int):
    sue_str = "Sue"
    minute_360 = 360
    hour6am = "6am"
    agg_br00003_tablename = f"br00003_{brick_agg_str()}"
    agg_br00003_columns = [
        event_int_str(),
        face_name_str(),
        moment_label_str(),
        cumulative_minute_str(),
        hour_label_str(),
    ]
    with sqlite3_connect(world.get_world_db_path()) as db_conn:
        cursor = db_conn.cursor()
        create_idea_sorted_table(cursor, agg_br00003_tablename, agg_br00003_columns)
        insert_into_clause = f"""INSERT INTO {agg_br00003_tablename} (
  {event_int_str()}
, {face_name_str()}
, {moment_label_str()}
, {cumulative_minute_str()}
, {hour_label_str()}
)"""
        values_clause = f"""VALUES ('{event_int}', '{sue_str}', '{world.world_name}', '{minute_360}', '{hour6am}');"""
        insert_sqlstr = f"{insert_into_clause} {values_clause}"
        cursor.execute(insert_sqlstr)
    db_conn.close()


def test_WorldUnit_stance_sheets_to_clarity_mstr_Scenario1_DatabaseFileExists(
    env_dir_setup_cleanup,
):  # sourcery skip: extract-method
    # ESTABLISH:
    fay_str = "Fay34"
    fay_world = worldunit_shop(fay_str, worlds_dir())
    event5 = 5
    create_brick_agg_record(fay_world, event5)
    # delete_dir(fay_world.worlds_dir)
    sue_str = "Sue"
    sue_inx = "Suzy"
    ex_filename = "stance_Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    br00113_columns = [
        face_name_str(),
        moment_label_str(),
        belief_name_str(),
        voice_name_str(),
        otx_name_str(),
        inx_name_str(),
    ]
    a23_str = "amy2345"
    br00113_str = "br00113"
    br00113row0 = [sue_str, a23_str, sue_str, sue_str, sue_str, sue_inx]
    br00113_df = DataFrame([br00113row0], columns=br00113_columns)
    br00113_ex0_str = f"example0_{br00113_str}"
    upsert_sheet(input_file_path, br00113_ex0_str, br00113_df)
    fay_db_path = fay_world.get_world_db_path()
    assert os_path_exists(fay_db_path)
    with sqlite3_connect(fay_db_path) as db_conn0:
        cursor0 = db_conn0.cursor()
        assert get_max_brick_agg_event_int(cursor0) == event5
    db_conn0.close()
    assert os_path_exists(input_file_path)

    # WHEN
    fay_world.stance_sheets_to_clarity_mstr()

    # THEN
    assert os_path_exists(fay_db_path)
    with sqlite3_connect(fay_db_path) as db_conn1:
        cursor1 = db_conn1.cursor()
        assert get_max_brick_agg_event_int(cursor1) != event5
        assert get_max_brick_agg_event_int(cursor1) == event5 + 1
        select_sqlstr = f"SELECT * FROM {events_brick_agg_str()}"
        cursor1.execute(select_sqlstr)
        rows = cursor1.fetchall()
        assert len(rows) == 2
    db_conn1.close()
    assert not os_path_exists(input_file_path)
