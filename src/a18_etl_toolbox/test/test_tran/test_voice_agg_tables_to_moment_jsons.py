from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    create_select_query,
    db_table_exists,
    get_row_count,
)
from src.a00_data_toolbox.file_toolbox import open_file
from src.a04_reason_logic.test._util.a04_str import moment_label_str
from src.a12_hub_toolbox.a12_path import create_moment_json_path
from src.a15_moment_logic.moment_config import get_moment_dimens
from src.a15_moment_logic.moment_main import get_from_json as momentunit_get_from_json
from src.a15_moment_logic.test._util.a15_str import (
    moment_budunit_str,
    moment_paybook_str,
    moment_timeline_hour_str,
    moment_timeline_month_str,
    moment_timeline_weekday_str,
    moment_timeoffi_str,
    momentunit_str,
)
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.test._util.a18_str import moment_event_time_agg_str
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename,
    get_dimen_abbv7,
    get_moment_voice_select1_sqlstrs,
)
from src.a18_etl_toolbox.transformers import (
    create_sound_and_voice_tables,
    etl_voice_agg_tables_to_moment_jsons,
)


def test_get_moment_voice_select1_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH
    a23_str = "amy23"

    # WHEN
    fu2_select_sqlstrs = get_moment_voice_select1_sqlstrs(a23_str)

    # THEN
    assert fu2_select_sqlstrs
    expected_fu2_select_dimens = set(get_moment_dimens())
    assert set(fu2_select_sqlstrs.keys()) == expected_fu2_select_dimens


def test_get_moment_voice_select1_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    a23_str = "amy23"

    # WHEN
    fu2_select_sqlstrs = get_moment_voice_select1_sqlstrs(moment_label=a23_str)

    # THEN
    gen_blfpayy_sqlstr = fu2_select_sqlstrs.get(moment_paybook_str())
    gen_momentbud_sqlstr = fu2_select_sqlstrs.get(moment_budunit_str())
    gen_blfhour_sqlstr = fu2_select_sqlstrs.get(moment_timeline_hour_str())
    gen_blfmont_sqlstr = fu2_select_sqlstrs.get(moment_timeline_month_str())
    gen_blfweek_sqlstr = fu2_select_sqlstrs.get(moment_timeline_weekday_str())
    gen_blfoffi_sqlstr = fu2_select_sqlstrs.get(moment_timeoffi_str())
    gen_momentunit_sqlstr = fu2_select_sqlstrs.get(momentunit_str())
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        blfpayy_abbv7 = get_dimen_abbv7(moment_paybook_str())
        momentbud_abbv7 = get_dimen_abbv7(moment_budunit_str())
        blfhour_abbv7 = get_dimen_abbv7(moment_timeline_hour_str())
        blfmont_abbv7 = get_dimen_abbv7(moment_timeline_month_str())
        blfweek_abbv7 = get_dimen_abbv7(moment_timeline_weekday_str())
        blfoffi_abbv7 = get_dimen_abbv7(moment_timeoffi_str())
        momentunit_abbv7 = get_dimen_abbv7(momentunit_str())
        blfpayy_v_agg = create_prime_tablename(blfpayy_abbv7, "v", "agg")
        momentbud_v_agg = create_prime_tablename(momentbud_abbv7, "v", "agg")
        blfhour_v_agg = create_prime_tablename(blfhour_abbv7, "v", "agg")
        blfmont_v_agg = create_prime_tablename(blfmont_abbv7, "v", "agg")
        blfweek_v_agg = create_prime_tablename(blfweek_abbv7, "v", "agg")
        blfoffi_v_agg = create_prime_tablename(blfoffi_abbv7, "v", "agg")
        momentunit_v_agg = create_prime_tablename(momentunit_abbv7, "v", "agg")
        where_dict = {moment_label_str(): a23_str}
        blfpayy_sql = create_select_query(cursor, blfpayy_v_agg, [], where_dict, True)
        momentbud_sql = create_select_query(
            cursor, momentbud_v_agg, [], where_dict, True
        )
        blfhour_sql = create_select_query(cursor, blfhour_v_agg, [], where_dict, True)
        blfmont_sql = create_select_query(cursor, blfmont_v_agg, [], where_dict, True)
        blfweek_sql = create_select_query(cursor, blfweek_v_agg, [], where_dict, True)
        blfoffi_sql = create_select_query(cursor, blfoffi_v_agg, [], where_dict, True)
        momentunit_sql = create_select_query(
            cursor, momentunit_v_agg, [], where_dict, True
        )
        blfpayy_sqlstr_ref = f"{blfpayy_abbv7.upper()}_FU2_SELECT_SQLSTR"
        momentbud_sqlstr_ref = f"{momentbud_abbv7.upper()}_FU2_SELECT_SQLSTR"
        blfhour_sqlstr_ref = f"{blfhour_abbv7.upper()}_FU2_SELECT_SQLSTR"
        blfmont_sqlstr_ref = f"{blfmont_abbv7.upper()}_FU2_SELECT_SQLSTR"
        blfweek_sqlstr_ref = f"{blfweek_abbv7.upper()}_FU2_SELECT_SQLSTR"
        blfoffi_sqlstr_ref = f"{blfoffi_abbv7.upper()}_FU2_SELECT_SQLSTR"
        momentunit_sqlstr_ref = f"{momentunit_abbv7.upper()}_FU2_SELECT_SQLSTR"
        qa23_str = "'amy23'"
        blank = ""
        print(f"""{blfpayy_sqlstr_ref} = "{blfpayy_sql.replace(qa23_str, blank)}" """)
        print(
            f"""{momentbud_sqlstr_ref} = "{momentbud_sql.replace(qa23_str, blank)}" """
        )
        print(f"""{blfhour_sqlstr_ref} = "{blfhour_sql.replace(qa23_str, blank)}" """)
        print(f"""{blfmont_sqlstr_ref} = "{blfmont_sql.replace(qa23_str, blank)}" """)
        print(f"""{blfweek_sqlstr_ref} = "{blfweek_sql.replace(qa23_str, blank)}" """)
        print(f"""{blfoffi_sqlstr_ref} = "{blfoffi_sql.replace(qa23_str, blank)}" """)
        print(
            f"""{momentunit_sqlstr_ref} = "{momentunit_sql.replace(qa23_str, blank)}" """
        )
        assert gen_blfpayy_sqlstr == blfpayy_sql
        assert gen_momentbud_sqlstr == momentbud_sql
        assert gen_blfhour_sqlstr == blfhour_sql
        assert gen_blfmont_sqlstr == blfmont_sql
        assert gen_blfweek_sqlstr == blfweek_sql
        assert gen_blfoffi_sqlstr == blfoffi_sql
        assert gen_momentunit_sqlstr == momentunit_sql
        static_example_sqlstr = f"SELECT moment_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, knot, job_listen_rotations FROM momentunit_v_agg WHERE moment_label = '{a23_str}'"
        assert gen_momentunit_sqlstr == static_example_sqlstr


def test_etl_voice_agg_tables_to_moment_jsons_Scenario0_CreateFilesWithOnlyMomentLabel(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    amy23_str = "amy23"
    amy45_str = "amy45"
    moment_mstr_dir = get_module_temp_dir()
    momentunit_v_agg_tablename = create_prime_tablename(momentunit_str(), "v", "agg")
    print(f"{momentunit_v_agg_tablename=}")

    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_sound_and_voice_tables(cursor)

        insert_raw_sqlstr = f"""
INSERT INTO {momentunit_v_agg_tablename} ({moment_label_str()})
VALUES ('{amy23_str}'), ('{amy45_str}')
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, momentunit_v_agg_tablename) == 2
        assert db_table_exists(cursor, moment_event_time_agg_str()) is False

        amy23_json_path = create_moment_json_path(moment_mstr_dir, amy23_str)
        amy45_json_path = create_moment_json_path(moment_mstr_dir, amy45_str)
        print(f"{amy23_json_path=}")
        print(f"{amy45_json_path=}")
        assert os_path_exists(amy23_json_path) is False
        assert os_path_exists(amy45_json_path) is False

        # WHEN
        etl_voice_agg_tables_to_moment_jsons(cursor, moment_mstr_dir)

    # THEN
    assert os_path_exists(amy23_json_path)
    assert os_path_exists(amy45_json_path)
    amy23_moment = momentunit_get_from_json(open_file(amy23_json_path))
    amy45_moment = momentunit_get_from_json(open_file(amy45_json_path))
    assert amy23_moment.moment_label == amy23_str
    assert amy45_moment.moment_label == amy45_str
