from os.path import exists as os_path_exists
from pandas import DataFrame
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import get_row_count
from src.a00_data_toolbox.file_toolbox import create_path
from src.a06_believer_logic.test._util.a06_str import person_name_str
from src.a09_pack_logic.test._util.a09_str import face_name_str
from src.a11_bud_logic.test._util.a11_str import (
    belief_label_str,
    believer_name_str,
    bud_time_str,
    celldepth_str,
    quota_str,
)
from src.a16_pidgin_logic.test._util.a16_str import inx_name_str, otx_name_str
from src.a17_idea_logic.idea_db_tool import upsert_sheet
from src.a18_etl_toolbox.test._util.a18_str import (
    belief_ote1_agg_str,
    events_brick_agg_str,
    events_brick_valid_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.a20_world_logic.test._util.a20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as worlds_dir,
)
from src.a20_world_logic.world import worldunit_shop


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
        belief_label_str(),
        believer_name_str(),
        person_name_str(),
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
        belief_label_str(),
        believer_name_str(),
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
    fay_db_path = fay_world.get_db_path()
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
        beliefunit_sound_raw = create_prime_tablename("beliefunit", "s", "raw")
        beliefunit_sound_agg = create_prime_tablename("beliefunit", "s", "agg")
        blrunit_sound_put_raw = create_prime_tablename(
            "believerunit", "s", "raw", "put"
        )
        blrunit_sound_put_agg = create_prime_tablename(
            "believerunit", "s", "agg", "put"
        )
        blrpern_sound_put_raw = create_prime_tablename("blrpern", "s", "raw", "put")
        blrpern_sound_put_agg = create_prime_tablename("blrpern", "s", "agg", "put")
        beliefunit_voice_raw = create_prime_tablename("beliefunit", "v", "raw")
        beliefunit_voice_agg = create_prime_tablename("beliefunit", "v", "agg")
        blrunit_voice_put_raw = create_prime_tablename(
            "believerunit", "v", "raw", "put"
        )
        blrunit_voice_put_agg = create_prime_tablename(
            "believerunit", "v", "agg", "put"
        )
        blrpern_voice_put_raw = create_prime_tablename("blrpern", "v", "raw", "put")
        blrpern_voice_put_agg = create_prime_tablename("blrpern", "v", "agg", "put")

        cursor = db_conn.cursor()
        assert get_row_count(cursor, br00113_raw) == 1
        assert get_row_count(cursor, br00113_agg) == 1
        assert get_row_count(cursor, events_brick_agg_str()) == 2
        assert get_row_count(cursor, events_brick_valid_tablename) == 2
        assert get_row_count(cursor, br00113_valid) == 2
        assert get_row_count(cursor, pidname_sound_raw) == 2
        assert get_row_count(cursor, beliefunit_sound_raw) == 4
        assert get_row_count(cursor, blrunit_sound_put_raw) == 4
        assert get_row_count(cursor, blrpern_sound_put_raw) == 2
        assert get_row_count(cursor, pidname_sound_agg) == 1
        assert get_row_count(cursor, beliefunit_sound_agg) == 1
        assert get_row_count(cursor, blrunit_sound_put_agg) == 1
        assert get_row_count(cursor, blrpern_sound_put_agg) == 1
        assert get_row_count(cursor, pidcore_sound_raw) == 1
        assert get_row_count(cursor, pidcore_sound_agg) == 1
        assert get_row_count(cursor, pidcore_sound_vld) == 1
        assert get_row_count(cursor, pidname_sound_vld) == 1
        assert get_row_count(cursor, beliefunit_voice_raw) == 1
        assert get_row_count(cursor, blrunit_voice_put_raw) == 1
        assert get_row_count(cursor, blrpern_voice_put_raw) == 1
        assert get_row_count(cursor, beliefunit_voice_agg) == 1
        assert get_row_count(cursor, blrunit_voice_put_agg) == 1
        assert get_row_count(cursor, blrpern_voice_put_agg) == 1
        assert get_row_count(cursor, belief_ote1_agg_str()) == 1
    db_conn.close()
