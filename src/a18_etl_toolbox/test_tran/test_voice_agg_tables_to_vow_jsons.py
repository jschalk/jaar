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
    gen_vowpayy_sqlstr = fu2_select_sqlstrs.get(vow_paybook_str())
    gen_vowdeal_sqlstr = fu2_select_sqlstrs.get(vow_dealunit_str())
    gen_vowhour_sqlstr = fu2_select_sqlstrs.get(vow_timeline_hour_str())
    gen_vowmont_sqlstr = fu2_select_sqlstrs.get(vow_timeline_month_str())
    gen_vowweek_sqlstr = fu2_select_sqlstrs.get(vow_timeline_weekday_str())
    gen_vowoffi_sqlstr = fu2_select_sqlstrs.get(vow_timeoffi_str())
    gen_vowunit_sqlstr = fu2_select_sqlstrs.get(vowunit_str())
    with sqlite3_connect(":memory:") as vow_db_conn:
        cursor = vow_db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        vowpayy_abbv7 = get_dimen_abbv7(vow_paybook_str())
        vowdeal_abbv7 = get_dimen_abbv7(vow_dealunit_str())
        vowhour_abbv7 = get_dimen_abbv7(vow_timeline_hour_str())
        vowmont_abbv7 = get_dimen_abbv7(vow_timeline_month_str())
        vowweek_abbv7 = get_dimen_abbv7(vow_timeline_weekday_str())
        vowoffi_abbv7 = get_dimen_abbv7(vow_timeoffi_str())
        vowunit_abbv7 = get_dimen_abbv7(vowunit_str())
        vowpayy_v_agg = create_prime_tablename(vowpayy_abbv7, "v", "agg")
        vowdeal_v_agg = create_prime_tablename(vowdeal_abbv7, "v", "agg")
        vowhour_v_agg = create_prime_tablename(vowhour_abbv7, "v", "agg")
        vowmont_v_agg = create_prime_tablename(vowmont_abbv7, "v", "agg")
        vowweek_v_agg = create_prime_tablename(vowweek_abbv7, "v", "agg")
        vowoffi_v_agg = create_prime_tablename(vowoffi_abbv7, "v", "agg")
        vowunit_v_agg = create_prime_tablename(vowunit_abbv7, "v", "agg")
        where_dict = {vow_label_str(): a23_str}
        vowpayy_sql = create_select_query(cursor, vowpayy_v_agg, [], where_dict, True)
        vowdeal_sql = create_select_query(cursor, vowdeal_v_agg, [], where_dict, True)
        vowhour_sql = create_select_query(cursor, vowhour_v_agg, [], where_dict, True)
        vowmont_sql = create_select_query(cursor, vowmont_v_agg, [], where_dict, True)
        vowweek_sql = create_select_query(cursor, vowweek_v_agg, [], where_dict, True)
        vowoffi_sql = create_select_query(cursor, vowoffi_v_agg, [], where_dict, True)
        vowunit_sql = create_select_query(cursor, vowunit_v_agg, [], where_dict, True)
        vowpayy_sqlstr_ref = f"{vowpayy_abbv7.upper()}_FU2_SELECT_SQLSTR"
        vowdeal_sqlstr_ref = f"{vowdeal_abbv7.upper()}_FU2_SELECT_SQLSTR"
        vowhour_sqlstr_ref = f"{vowhour_abbv7.upper()}_FU2_SELECT_SQLSTR"
        vowmont_sqlstr_ref = f"{vowmont_abbv7.upper()}_FU2_SELECT_SQLSTR"
        vowweek_sqlstr_ref = f"{vowweek_abbv7.upper()}_FU2_SELECT_SQLSTR"
        vowoffi_sqlstr_ref = f"{vowoffi_abbv7.upper()}_FU2_SELECT_SQLSTR"
        vowunit_sqlstr_ref = f"{vowunit_abbv7.upper()}_FU2_SELECT_SQLSTR"
        qa23_str = "'accord23'"
        blank = ""
        print(f"""{vowpayy_sqlstr_ref} = "{vowpayy_sql.replace(qa23_str, blank)}" """)
        print(f"""{vowdeal_sqlstr_ref} = "{vowdeal_sql.replace(qa23_str, blank)}" """)
        print(f"""{vowhour_sqlstr_ref} = "{vowhour_sql.replace(qa23_str, blank)}" """)
        print(f"""{vowmont_sqlstr_ref} = "{vowmont_sql.replace(qa23_str, blank)}" """)
        print(f"""{vowweek_sqlstr_ref} = "{vowweek_sql.replace(qa23_str, blank)}" """)
        print(f"""{vowoffi_sqlstr_ref} = "{vowoffi_sql.replace(qa23_str, blank)}" """)
        print(f"""{vowunit_sqlstr_ref} = "{vowunit_sql.replace(qa23_str, blank)}" """)
        assert gen_vowpayy_sqlstr == vowpayy_sql
        assert gen_vowdeal_sqlstr == vowdeal_sql
        assert gen_vowhour_sqlstr == vowhour_sql
        assert gen_vowmont_sqlstr == vowmont_sql
        assert gen_vowweek_sqlstr == vowweek_sql
        assert gen_vowoffi_sqlstr == vowoffi_sql
        assert gen_vowunit_sqlstr == vowunit_sql
        static_example_sqlstr = f"SELECT vow_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, bridge, job_listen_rotations FROM vowunit_v_agg WHERE vow_label = '{a23_str}'"
        assert gen_vowunit_sqlstr == static_example_sqlstr


def test_etl_voice_agg_tables_to_vow_jsons_Scenario0_CreateFilesWithOnlyVowLabel(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    vow_mstr_dir = get_module_temp_dir()
    vowunit_v_agg_tablename = create_prime_tablename(vowunit_str(), "v", "agg")
    print(f"{vowunit_v_agg_tablename=}")

    with sqlite3_connect(":memory:") as vow_db_conn:
        cursor = vow_db_conn.cursor()
        create_sound_and_voice_tables(cursor)

        insert_raw_sqlstr = f"""
INSERT INTO {vowunit_v_agg_tablename} ({vow_label_str()})
VALUES ('{accord23_str}'), ('{accord45_str}')
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, vowunit_v_agg_tablename) == 2
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
