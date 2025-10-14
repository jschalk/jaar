from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import create_select_query, db_table_exists, get_row_count
from src.ch01_py.file_toolbox import open_json
from src.ch10_lesson._ref.ch10_path import create_moment_json_path
from src.ch15_moment.moment_config import get_moment_dimens
from src.ch15_moment.moment_main import get_momentunit_from_dict
from src.ch18_world_etl.test._util.ch18_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch18_world_etl.tran_sqlstrs import (
    create_prime_tablename,
    get_dimen_abbv7,
    get_moment_heard_select1_sqlstrs,
)
from src.ch18_world_etl.transformers import (
    create_sound_and_heard_tables,
    etl_heard_agg_tables_to_moment_jsons,
)
from src.ref.keywords import Ch18Keywords as wx


def test_get_moment_heard_select1_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH
    a23_str = "amy23"

    # WHEN
    fu2_select_sqlstrs = get_moment_heard_select1_sqlstrs(a23_str)

    # THEN
    assert fu2_select_sqlstrs
    expected_fu2_select_dimens = set(get_moment_dimens())
    assert set(fu2_select_sqlstrs.keys()) == expected_fu2_select_dimens


def test_get_moment_heard_select1_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    a23_str = "amy23"

    # WHEN
    fu2_select_sqlstrs = get_moment_heard_select1_sqlstrs(moment_label=a23_str)

    # THEN
    gen_blfpayy_sqlstr = fu2_select_sqlstrs.get(wx.moment_paybook)
    gen_momentbud_sqlstr = fu2_select_sqlstrs.get(wx.moment_budunit)
    gen_blfhour_sqlstr = fu2_select_sqlstrs.get(wx.moment_epoch_hour)
    gen_blfmont_sqlstr = fu2_select_sqlstrs.get(wx.moment_epoch_month)
    gen_blfweek_sqlstr = fu2_select_sqlstrs.get(wx.moment_epoch_weekday)
    gen_blfoffi_sqlstr = fu2_select_sqlstrs.get(wx.moment_timeoffi)
    gen_momentunit_sqlstr = fu2_select_sqlstrs.get(wx.momentunit)
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        blfpayy_abbv7 = get_dimen_abbv7(wx.moment_paybook)
        momentbud_abbv7 = get_dimen_abbv7(wx.moment_budunit)
        blfhour_abbv7 = get_dimen_abbv7(wx.moment_epoch_hour)
        blfmont_abbv7 = get_dimen_abbv7(wx.moment_epoch_month)
        blfweek_abbv7 = get_dimen_abbv7(wx.moment_epoch_weekday)
        blfoffi_abbv7 = get_dimen_abbv7(wx.moment_timeoffi)
        momentunit_abbv7 = get_dimen_abbv7(wx.momentunit)
        blfpayy_h_agg = create_prime_tablename(blfpayy_abbv7, "h", "agg")
        momentbud_h_agg = create_prime_tablename(momentbud_abbv7, "h", "agg")
        blfhour_h_agg = create_prime_tablename(blfhour_abbv7, "h", "agg")
        blfmont_h_agg = create_prime_tablename(blfmont_abbv7, "h", "agg")
        blfweek_h_agg = create_prime_tablename(blfweek_abbv7, "h", "agg")
        blfoffi_h_agg = create_prime_tablename(blfoffi_abbv7, "h", "agg")
        momentunit_h_agg = create_prime_tablename(momentunit_abbv7, "h", "agg")
        where_dict = {wx.moment_label: a23_str}
        blfpayy_sql = create_select_query(cursor, blfpayy_h_agg, [], where_dict, True)
        momentbud_sql = create_select_query(
            cursor, momentbud_h_agg, [], where_dict, True
        )
        blfhour_sql = create_select_query(cursor, blfhour_h_agg, [], where_dict, True)
        blfmont_sql = create_select_query(cursor, blfmont_h_agg, [], where_dict, True)
        blfweek_sql = create_select_query(cursor, blfweek_h_agg, [], where_dict, True)
        blfoffi_sql = create_select_query(cursor, blfoffi_h_agg, [], where_dict, True)
        momentunit_sql = create_select_query(
            cursor, momentunit_h_agg, [], where_dict, True
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
        static_example_sqlstr = f"SELECT {wx.moment_label}, {wx.epoch_label}, {wx.c400_number}, {wx.yr1_jan1_offset}, {wx.monthday_index}, {wx.fund_grain}, {wx.money_grain}, {wx.respect_grain}, {wx.knot}, {wx.job_listen_rotations} FROM momentunit_h_agg WHERE moment_label = '{a23_str}'"
        assert gen_momentunit_sqlstr == static_example_sqlstr


def test_etl_heard_agg_tables_to_moment_jsons_Scenario0_CreateFilesWithOnlyMomentLabel(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    amy23_str = "amy23"
    amy45_str = "amy45"
    moment_mstr_dir = get_chapter_temp_dir()
    momentunit_h_agg_tablename = create_prime_tablename(wx.momentunit, "h", "agg")
    print(f"{momentunit_h_agg_tablename=}")

    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_sound_and_heard_tables(cursor)

        insert_raw_sqlstr = f"""
INSERT INTO {momentunit_h_agg_tablename} ({wx.moment_label})
VALUES ('{amy23_str}'), ('{amy45_str}')
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, momentunit_h_agg_tablename) == 2
        assert db_table_exists(cursor, wx.moment_spark_time_agg) is False

        amy23_json_path = create_moment_json_path(moment_mstr_dir, amy23_str)
        amy45_json_path = create_moment_json_path(moment_mstr_dir, amy45_str)
        print(f"{amy23_json_path=}")
        print(f"{amy45_json_path=}")
        assert os_path_exists(amy23_json_path) is False
        assert os_path_exists(amy45_json_path) is False

        # WHEN
        etl_heard_agg_tables_to_moment_jsons(cursor, moment_mstr_dir)

    # THEN
    assert os_path_exists(amy23_json_path)
    assert os_path_exists(amy45_json_path)
    amy23_moment = get_momentunit_from_dict(open_json(amy23_json_path))
    amy45_moment = get_momentunit_from_dict(open_json(amy45_json_path))
    assert amy23_moment.moment_label == amy23_str
    assert amy45_moment.moment_label == amy45_str
