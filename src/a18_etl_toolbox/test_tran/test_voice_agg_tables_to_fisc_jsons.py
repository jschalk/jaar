from src.a00_data_toolbox.file_toolbox import open_file
from src.a00_data_toolbox.db_toolbox import (
    get_row_count,
    db_table_exists,
    create_select_query,
)
from src.a02_finance_logic._test_util.a02_str import fisc_label_str
from src.a12_hub_tools.hub_path import create_fisc_json_path
from src.a15_fisc_logic.fisc import get_from_json as fiscunit_get_from_json
from src.a15_fisc_logic.fisc_config import get_fisc_dimens
from src.a15_fisc_logic._test_util.a15_str import (
    fiscunit_str,
    fisc_cashbook_str,
    fisc_dealunit_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    fisc_timeoffi_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    get_dimen_abbv7,
    create_prime_tablename,
    get_fisc_voice_select1_sqlstrs,
)
from src.a18_etl_toolbox.transformers import (
    create_sound_and_voice_tables,
    etl_voice_agg_tables_to_fisc_jsons,
)
from src.a18_etl_toolbox._test_util.env_a18 import (
    get_module_temp_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_get_fisc_voice_select1_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    fu2_select_sqlstrs = get_fisc_voice_select1_sqlstrs(a23_str)

    # THEN
    assert fu2_select_sqlstrs
    expected_fu2_select_dimens = set(get_fisc_dimens())
    assert set(fu2_select_sqlstrs.keys()) == expected_fu2_select_dimens


def test_get_fisc_voice_select1_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    fu2_select_sqlstrs = get_fisc_voice_select1_sqlstrs(fisc_label=a23_str)

    # THEN
    gen_fiscash_sqlstr = fu2_select_sqlstrs.get(fisc_cashbook_str())
    gen_fisdeal_sqlstr = fu2_select_sqlstrs.get(fisc_dealunit_str())
    gen_fishour_sqlstr = fu2_select_sqlstrs.get(fisc_timeline_hour_str())
    gen_fismont_sqlstr = fu2_select_sqlstrs.get(fisc_timeline_month_str())
    gen_fisweek_sqlstr = fu2_select_sqlstrs.get(fisc_timeline_weekday_str())
    gen_fisoffi_sqlstr = fu2_select_sqlstrs.get(fisc_timeoffi_str())
    gen_fisunit_sqlstr = fu2_select_sqlstrs.get(fiscunit_str())
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        fiscash_abbv7 = get_dimen_abbv7(fisc_cashbook_str())
        fisdeal_abbv7 = get_dimen_abbv7(fisc_dealunit_str())
        fishour_abbv7 = get_dimen_abbv7(fisc_timeline_hour_str())
        fismont_abbv7 = get_dimen_abbv7(fisc_timeline_month_str())
        fisweek_abbv7 = get_dimen_abbv7(fisc_timeline_weekday_str())
        fisoffi_abbv7 = get_dimen_abbv7(fisc_timeoffi_str())
        fisunit_abbv7 = get_dimen_abbv7(fiscunit_str())
        fiscash_v_agg = create_prime_tablename(fiscash_abbv7, "v", "agg")
        fisdeal_v_agg = create_prime_tablename(fisdeal_abbv7, "v", "agg")
        fishour_v_agg = create_prime_tablename(fishour_abbv7, "v", "agg")
        fismont_v_agg = create_prime_tablename(fismont_abbv7, "v", "agg")
        fisweek_v_agg = create_prime_tablename(fisweek_abbv7, "v", "agg")
        fisoffi_v_agg = create_prime_tablename(fisoffi_abbv7, "v", "agg")
        fisunit_v_agg = create_prime_tablename(fisunit_abbv7, "v", "agg")
        where_dict = {fisc_label_str(): a23_str}
        fiscash_sql = create_select_query(cursor, fiscash_v_agg, [], where_dict, True)
        fisdeal_sql = create_select_query(cursor, fisdeal_v_agg, [], where_dict, True)
        fishour_sql = create_select_query(cursor, fishour_v_agg, [], where_dict, True)
        fismont_sql = create_select_query(cursor, fismont_v_agg, [], where_dict, True)
        fisweek_sql = create_select_query(cursor, fisweek_v_agg, [], where_dict, True)
        fisoffi_sql = create_select_query(cursor, fisoffi_v_agg, [], where_dict, True)
        fisunit_sql = create_select_query(cursor, fisunit_v_agg, [], where_dict, True)
        fiscash_sqlstr_ref = f"{fiscash_abbv7.upper()}_FU2_SELECT_SQLSTR"
        fisdeal_sqlstr_ref = f"{fisdeal_abbv7.upper()}_FU2_SELECT_SQLSTR"
        fishour_sqlstr_ref = f"{fishour_abbv7.upper()}_FU2_SELECT_SQLSTR"
        fismont_sqlstr_ref = f"{fismont_abbv7.upper()}_FU2_SELECT_SQLSTR"
        fisweek_sqlstr_ref = f"{fisweek_abbv7.upper()}_FU2_SELECT_SQLSTR"
        fisoffi_sqlstr_ref = f"{fisoffi_abbv7.upper()}_FU2_SELECT_SQLSTR"
        fisunit_sqlstr_ref = f"{fisunit_abbv7.upper()}_FU2_SELECT_SQLSTR"
        qa23_str = "'accord23'"
        blank = ""
        print(f"""{fiscash_sqlstr_ref} = "{fiscash_sql.replace(qa23_str, blank)}" """)
        print(f"""{fisdeal_sqlstr_ref} = "{fisdeal_sql.replace(qa23_str, blank)}" """)
        print(f"""{fishour_sqlstr_ref} = "{fishour_sql.replace(qa23_str, blank)}" """)
        print(f"""{fismont_sqlstr_ref} = "{fismont_sql.replace(qa23_str, blank)}" """)
        print(f"""{fisweek_sqlstr_ref} = "{fisweek_sql.replace(qa23_str, blank)}" """)
        print(f"""{fisoffi_sqlstr_ref} = "{fisoffi_sql.replace(qa23_str, blank)}" """)
        print(f"""{fisunit_sqlstr_ref} = "{fisunit_sql.replace(qa23_str, blank)}" """)
        assert gen_fiscash_sqlstr == fiscash_sql
        assert gen_fisdeal_sqlstr == fisdeal_sql
        assert gen_fishour_sqlstr == fishour_sql
        assert gen_fismont_sqlstr == fismont_sql
        assert gen_fisweek_sqlstr == fisweek_sql
        assert gen_fisoffi_sqlstr == fisoffi_sql
        assert gen_fisunit_sqlstr == fisunit_sql
        static_example_sqlstr = f"SELECT fisc_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_coin, penny, respect_bit, bridge, job_listen_rotations FROM fiscunit_v_agg WHERE fisc_label = '{a23_str}'"
        assert gen_fisunit_sqlstr == static_example_sqlstr


def test_etl_voice_agg_tables_to_fisc_jsons_Scenario0_CreateFilesWithOnlyFiscLabel(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    fisc_mstr_dir = get_module_temp_dir()
    fisunit_v_agg_tablename = create_prime_tablename(fiscunit_str(), "v", "agg")
    print(f"{fisunit_v_agg_tablename=}")

    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_sound_and_voice_tables(cursor)

        insert_raw_sqlstr = f"""
INSERT INTO {fisunit_v_agg_tablename} ({fisc_label_str()})
VALUES ('{accord23_str}'), ('{accord45_str}')
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, fisunit_v_agg_tablename) == 2
        fisc_event_time_agg_str = "fisc_event_time_agg"
        assert db_table_exists(cursor, fisc_event_time_agg_str) is False

        accord23_json_path = create_fisc_json_path(fisc_mstr_dir, accord23_str)
        accord45_json_path = create_fisc_json_path(fisc_mstr_dir, accord45_str)
        assert os_path_exists(accord23_json_path) is False
        assert os_path_exists(accord45_json_path) is False

        # WHEN
        etl_voice_agg_tables_to_fisc_jsons(cursor, fisc_mstr_dir)

    # THEN
    assert os_path_exists(accord23_json_path)
    assert os_path_exists(accord45_json_path)
    accord23_fisc = fiscunit_get_from_json(open_file(accord23_json_path))
    accord45_fisc = fiscunit_get_from_json(open_file(accord45_json_path))
    assert accord23_fisc.fisc_label == accord23_str
    assert accord45_fisc.fisc_label == accord45_str
