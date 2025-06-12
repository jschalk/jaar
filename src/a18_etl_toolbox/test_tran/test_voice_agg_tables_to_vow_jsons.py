from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    create_select_query,
    db_table_exists,
    get_row_count,
)
from src.a00_data_toolbox.file_toolbox import open_file
from src.a02_finance_logic._test_util.a02_str import vow_label_str
from src.a12_hub_tools.hub_path import create_vow_json_path
from src.a15_vow_logic._test_util.a15_str import (
    vow_dealunit_str,
    vow_paybook_str,
    vow_timeline_hour_str,
    vow_timeline_month_str,
    vow_timeline_weekday_str,
    vow_timeoffi_str,
    vowunit_str,
)
from src.a15_vow_logic.vow import get_from_json as vowunit_get_from_json
from src.a15_vow_logic.vow_config import get_vow_dimens
from src.a18_etl_toolbox._test_util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox._test_util.a18_str import vow_event_time_agg_str
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename,
    get_dimen_abbv7,
    get_vow_voice_select1_sqlstrs,
)
from src.a18_etl_toolbox.transformers import (
    create_sound_and_voice_tables,
    etl_voice_agg_tables_to_vow_jsons,
)


def test_get_vow_voice_select1_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    fu2_select_sqlstrs = get_vow_voice_select1_sqlstrs(a23_str)

    # THEN
    assert fu2_select_sqlstrs
    expected_fu2_select_dimens = set(get_vow_dimens())
    assert set(fu2_select_sqlstrs.keys()) == expected_fu2_select_dimens


def test_get_vow_voice_select1_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    fu2_select_sqlstrs = get_vow_voice_select1_sqlstrs(vow_label=a23_str)

    # THEN
    gen_vowash_sqlstr = fu2_select_sqlstrs.get(vow_paybook_str())
    gen_fisdeal_sqlstr = fu2_select_sqlstrs.get(vow_dealunit_str())
    gen_fishour_sqlstr = fu2_select_sqlstrs.get(vow_timeline_hour_str())
    gen_fismont_sqlstr = fu2_select_sqlstrs.get(vow_timeline_month_str())
    gen_fisweek_sqlstr = fu2_select_sqlstrs.get(vow_timeline_weekday_str())
    gen_fisoffi_sqlstr = fu2_select_sqlstrs.get(vow_timeoffi_str())
    gen_fisunit_sqlstr = fu2_select_sqlstrs.get(vowunit_str())
    with sqlite3_connect(":memory:") as vow_db_conn:
        cursor = vow_db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        vowash_abbv7 = get_dimen_abbv7(vow_paybook_str())
        fisdeal_abbv7 = get_dimen_abbv7(vow_dealunit_str())
        fishour_abbv7 = get_dimen_abbv7(vow_timeline_hour_str())
        fismont_abbv7 = get_dimen_abbv7(vow_timeline_month_str())
        fisweek_abbv7 = get_dimen_abbv7(vow_timeline_weekday_str())
        fisoffi_abbv7 = get_dimen_abbv7(vow_timeoffi_str())
        fisunit_abbv7 = get_dimen_abbv7(vowunit_str())
        vowash_v_agg = create_prime_tablename(vowash_abbv7, "v", "agg")
        fisdeal_v_agg = create_prime_tablename(fisdeal_abbv7, "v", "agg")
        fishour_v_agg = create_prime_tablename(fishour_abbv7, "v", "agg")
        fismont_v_agg = create_prime_tablename(fismont_abbv7, "v", "agg")
        fisweek_v_agg = create_prime_tablename(fisweek_abbv7, "v", "agg")
        fisoffi_v_agg = create_prime_tablename(fisoffi_abbv7, "v", "agg")
        fisunit_v_agg = create_prime_tablename(fisunit_abbv7, "v", "agg")
        where_dict = {vow_label_str(): a23_str}
        vowash_sql = create_select_query(cursor, vowash_v_agg, [], where_dict, True)
        fisdeal_sql = create_select_query(cursor, fisdeal_v_agg, [], where_dict, True)
        fishour_sql = create_select_query(cursor, fishour_v_agg, [], where_dict, True)
        fismont_sql = create_select_query(cursor, fismont_v_agg, [], where_dict, True)
        fisweek_sql = create_select_query(cursor, fisweek_v_agg, [], where_dict, True)
        fisoffi_sql = create_select_query(cursor, fisoffi_v_agg, [], where_dict, True)
        fisunit_sql = create_select_query(cursor, fisunit_v_agg, [], where_dict, True)
        vowash_sqlstr_ref = f"{vowash_abbv7.upper()}_FU2_SELECT_SQLSTR"
        fisdeal_sqlstr_ref = f"{fisdeal_abbv7.upper()}_FU2_SELECT_SQLSTR"
        fishour_sqlstr_ref = f"{fishour_abbv7.upper()}_FU2_SELECT_SQLSTR"
        fismont_sqlstr_ref = f"{fismont_abbv7.upper()}_FU2_SELECT_SQLSTR"
        fisweek_sqlstr_ref = f"{fisweek_abbv7.upper()}_FU2_SELECT_SQLSTR"
        fisoffi_sqlstr_ref = f"{fisoffi_abbv7.upper()}_FU2_SELECT_SQLSTR"
        fisunit_sqlstr_ref = f"{fisunit_abbv7.upper()}_FU2_SELECT_SQLSTR"
        qa23_str = "'accord23'"
        blank = ""
        print(f"""{vowash_sqlstr_ref} = "{vowash_sql.replace(qa23_str, blank)}" """)
        print(f"""{fisdeal_sqlstr_ref} = "{fisdeal_sql.replace(qa23_str, blank)}" """)
        print(f"""{fishour_sqlstr_ref} = "{fishour_sql.replace(qa23_str, blank)}" """)
        print(f"""{fismont_sqlstr_ref} = "{fismont_sql.replace(qa23_str, blank)}" """)
        print(f"""{fisweek_sqlstr_ref} = "{fisweek_sql.replace(qa23_str, blank)}" """)
        print(f"""{fisoffi_sqlstr_ref} = "{fisoffi_sql.replace(qa23_str, blank)}" """)
        print(f"""{fisunit_sqlstr_ref} = "{fisunit_sql.replace(qa23_str, blank)}" """)
        assert gen_vowash_sqlstr == vowash_sql
        assert gen_fisdeal_sqlstr == fisdeal_sql
        assert gen_fishour_sqlstr == fishour_sql
        assert gen_fismont_sqlstr == fismont_sql
        assert gen_fisweek_sqlstr == fisweek_sql
        assert gen_fisoffi_sqlstr == fisoffi_sql
        assert gen_fisunit_sqlstr == fisunit_sql
        static_example_sqlstr = f"SELECT vow_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, bridge, job_listen_rotations FROM vowunit_v_agg WHERE vow_label = '{a23_str}'"
        assert gen_fisunit_sqlstr == static_example_sqlstr


def test_etl_voice_agg_tables_to_vow_jsons_Scenario0_CreateFilesWithOnlyVowLabel(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    vow_mstr_dir = get_module_temp_dir()
    fisunit_v_agg_tablename = create_prime_tablename(vowunit_str(), "v", "agg")
    print(f"{fisunit_v_agg_tablename=}")

    with sqlite3_connect(":memory:") as vow_db_conn:
        cursor = vow_db_conn.cursor()
        create_sound_and_voice_tables(cursor)

        insert_raw_sqlstr = f"""
INSERT INTO {fisunit_v_agg_tablename} ({vow_label_str()})
VALUES ('{accord23_str}'), ('{accord45_str}')
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, fisunit_v_agg_tablename) == 2
        assert db_table_exists(cursor, vow_event_time_agg_str()) is False

        accord23_json_path = create_vow_json_path(vow_mstr_dir, accord23_str)
        accord45_json_path = create_vow_json_path(vow_mstr_dir, accord45_str)
        assert os_path_exists(accord23_json_path) is False
        assert os_path_exists(accord45_json_path) is False

        # WHEN
        etl_voice_agg_tables_to_vow_jsons(cursor, vow_mstr_dir)

    # THEN
    assert os_path_exists(accord23_json_path)
    assert os_path_exists(accord45_json_path)
    accord23_vow = vowunit_get_from_json(open_file(accord23_json_path))
    accord45_vow = vowunit_get_from_json(open_file(accord45_json_path))
    assert accord23_vow.vow_label == accord23_str
    assert accord45_vow.vow_label == accord45_str
