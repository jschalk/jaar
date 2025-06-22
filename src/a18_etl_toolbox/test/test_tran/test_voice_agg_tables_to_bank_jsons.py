from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    create_select_query,
    db_table_exists,
    get_row_count,
)
from src.a00_data_toolbox.file_toolbox import open_file
from src.a02_finance_logic.test._util.a02_str import bank_label_str
from src.a12_hub_toolbox.hub_path import create_bank_json_path
from src.a15_bank_logic.bank import get_from_json as bankunit_get_from_json
from src.a15_bank_logic.bank_config import get_bank_dimens
from src.a15_bank_logic.test._util.a15_str import (
    bank_budunit_str,
    bank_paybook_str,
    bank_timeline_hour_str,
    bank_timeline_month_str,
    bank_timeline_weekday_str,
    bank_timeoffi_str,
    bankunit_str,
)
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.test._util.a18_str import bank_event_time_agg_str
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename,
    get_bank_voice_select1_sqlstrs,
    get_dimen_abbv7,
)
from src.a18_etl_toolbox.transformers import (
    create_sound_and_voice_tables,
    etl_voice_agg_tables_to_bank_jsons,
)


def test_get_bank_voice_select1_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    fu2_select_sqlstrs = get_bank_voice_select1_sqlstrs(a23_str)

    # THEN
    assert fu2_select_sqlstrs
    expected_fu2_select_dimens = set(get_bank_dimens())
    assert set(fu2_select_sqlstrs.keys()) == expected_fu2_select_dimens


def test_get_bank_voice_select1_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    a23_str = "accord23"

    # WHEN
    fu2_select_sqlstrs = get_bank_voice_select1_sqlstrs(bank_label=a23_str)

    # THEN
    gen_bnkpayy_sqlstr = fu2_select_sqlstrs.get(bank_paybook_str())
    gen_bankbud_sqlstr = fu2_select_sqlstrs.get(bank_budunit_str())
    gen_bnkhour_sqlstr = fu2_select_sqlstrs.get(bank_timeline_hour_str())
    gen_bnkmont_sqlstr = fu2_select_sqlstrs.get(bank_timeline_month_str())
    gen_bnkweek_sqlstr = fu2_select_sqlstrs.get(bank_timeline_weekday_str())
    gen_bnkoffi_sqlstr = fu2_select_sqlstrs.get(bank_timeoffi_str())
    gen_bankunit_sqlstr = fu2_select_sqlstrs.get(bankunit_str())
    with sqlite3_connect(":memory:") as bank_db_conn:
        cursor = bank_db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        bnkpayy_abbv7 = get_dimen_abbv7(bank_paybook_str())
        bankbud_abbv7 = get_dimen_abbv7(bank_budunit_str())
        bnkhour_abbv7 = get_dimen_abbv7(bank_timeline_hour_str())
        bnkmont_abbv7 = get_dimen_abbv7(bank_timeline_month_str())
        bnkweek_abbv7 = get_dimen_abbv7(bank_timeline_weekday_str())
        bnkoffi_abbv7 = get_dimen_abbv7(bank_timeoffi_str())
        bankunit_abbv7 = get_dimen_abbv7(bankunit_str())
        bnkpayy_v_agg = create_prime_tablename(bnkpayy_abbv7, "v", "agg")
        bankbud_v_agg = create_prime_tablename(bankbud_abbv7, "v", "agg")
        bnkhour_v_agg = create_prime_tablename(bnkhour_abbv7, "v", "agg")
        bnkmont_v_agg = create_prime_tablename(bnkmont_abbv7, "v", "agg")
        bnkweek_v_agg = create_prime_tablename(bnkweek_abbv7, "v", "agg")
        bnkoffi_v_agg = create_prime_tablename(bnkoffi_abbv7, "v", "agg")
        bankunit_v_agg = create_prime_tablename(bankunit_abbv7, "v", "agg")
        where_dict = {bank_label_str(): a23_str}
        bnkpayy_sql = create_select_query(cursor, bnkpayy_v_agg, [], where_dict, True)
        bankbud_sql = create_select_query(cursor, bankbud_v_agg, [], where_dict, True)
        bnkhour_sql = create_select_query(cursor, bnkhour_v_agg, [], where_dict, True)
        bnkmont_sql = create_select_query(cursor, bnkmont_v_agg, [], where_dict, True)
        bnkweek_sql = create_select_query(cursor, bnkweek_v_agg, [], where_dict, True)
        bnkoffi_sql = create_select_query(cursor, bnkoffi_v_agg, [], where_dict, True)
        bankunit_sql = create_select_query(cursor, bankunit_v_agg, [], where_dict, True)
        bnkpayy_sqlstr_ref = f"{bnkpayy_abbv7.upper()}_FU2_SELECT_SQLSTR"
        bankbud_sqlstr_ref = f"{bankbud_abbv7.upper()}_FU2_SELECT_SQLSTR"
        bnkhour_sqlstr_ref = f"{bnkhour_abbv7.upper()}_FU2_SELECT_SQLSTR"
        bnkmont_sqlstr_ref = f"{bnkmont_abbv7.upper()}_FU2_SELECT_SQLSTR"
        bnkweek_sqlstr_ref = f"{bnkweek_abbv7.upper()}_FU2_SELECT_SQLSTR"
        bnkoffi_sqlstr_ref = f"{bnkoffi_abbv7.upper()}_FU2_SELECT_SQLSTR"
        bankunit_sqlstr_ref = f"{bankunit_abbv7.upper()}_FU2_SELECT_SQLSTR"
        qa23_str = "'accord23'"
        blank = ""
        print(f"""{bnkpayy_sqlstr_ref} = "{bnkpayy_sql.replace(qa23_str, blank)}" """)
        print(f"""{bankbud_sqlstr_ref} = "{bankbud_sql.replace(qa23_str, blank)}" """)
        print(f"""{bnkhour_sqlstr_ref} = "{bnkhour_sql.replace(qa23_str, blank)}" """)
        print(f"""{bnkmont_sqlstr_ref} = "{bnkmont_sql.replace(qa23_str, blank)}" """)
        print(f"""{bnkweek_sqlstr_ref} = "{bnkweek_sql.replace(qa23_str, blank)}" """)
        print(f"""{bnkoffi_sqlstr_ref} = "{bnkoffi_sql.replace(qa23_str, blank)}" """)
        print(f"""{bankunit_sqlstr_ref} = "{bankunit_sql.replace(qa23_str, blank)}" """)
        assert gen_bnkpayy_sqlstr == bnkpayy_sql
        assert gen_bankbud_sqlstr == bankbud_sql
        assert gen_bnkhour_sqlstr == bnkhour_sql
        assert gen_bnkmont_sqlstr == bnkmont_sql
        assert gen_bnkweek_sqlstr == bnkweek_sql
        assert gen_bnkoffi_sqlstr == bnkoffi_sql
        assert gen_bankunit_sqlstr == bankunit_sql
        static_example_sqlstr = f"SELECT bank_label, timeline_label, c400_number, yr1_jan1_offset, monthday_distortion, fund_iota, penny, respect_bit, knot, job_listen_rotations FROM bankunit_v_agg WHERE bank_label = '{a23_str}'"
        assert gen_bankunit_sqlstr == static_example_sqlstr


def test_etl_voice_agg_tables_to_bank_jsons_Scenario0_CreateFilesWithOnlyBankLabel(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    bank_mstr_dir = get_module_temp_dir()
    bankunit_v_agg_tablename = create_prime_tablename(bankunit_str(), "v", "agg")
    print(f"{bankunit_v_agg_tablename=}")

    with sqlite3_connect(":memory:") as bank_db_conn:
        cursor = bank_db_conn.cursor()
        create_sound_and_voice_tables(cursor)

        insert_raw_sqlstr = f"""
INSERT INTO {bankunit_v_agg_tablename} ({bank_label_str()})
VALUES ('{accord23_str}'), ('{accord45_str}')
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, bankunit_v_agg_tablename) == 2
        assert db_table_exists(cursor, bank_event_time_agg_str()) is False

        accord23_json_path = create_bank_json_path(bank_mstr_dir, accord23_str)
        accord45_json_path = create_bank_json_path(bank_mstr_dir, accord45_str)
        print(f"{accord23_json_path=}")
        print(f"{accord45_json_path=}")
        assert os_path_exists(accord23_json_path) is False
        assert os_path_exists(accord45_json_path) is False

        # WHEN
        etl_voice_agg_tables_to_bank_jsons(cursor, bank_mstr_dir)

    # THEN
    assert os_path_exists(accord23_json_path)
    assert os_path_exists(accord45_json_path)
    accord23_bank = bankunit_get_from_json(open_file(accord23_json_path))
    accord45_bank = bankunit_get_from_json(open_file(accord45_json_path))
    assert accord23_bank.bank_label == accord23_str
    assert accord45_bank.bank_label == accord45_str
