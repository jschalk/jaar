from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import (
    create_insert_into_clause_str as get_insert_sql,
    create_select_query as get_select_sql,
    create_table2table_agg_insert_query,
    create_update_inconsistency_error_query,
    db_table_exists,
    get_create_table_sqlstr,
    get_table_columns,
)
from src.a06_plan_logic._test_util.a06_str import (
    plan_acct_membership_str,
    plan_acctunit_str,
    plan_concept_awardlink_str,
    plan_concept_factunit_str,
    plan_concept_healerlink_str,
    plan_concept_laborlink_str,
    plan_concept_reason_premiseunit_str,
    plan_concept_reasonunit_str,
    plan_conceptunit_str,
    planunit_str,
)
from src.a08_plan_atom_logic.atom_config import get_delete_key_name, get_plan_dimens
from src.a09_pack_logic._test_util.a09_str import event_int_str, face_name_str
from src.a15_vow_logic._test_util.a15_str import (
    vow_dealunit_str,
    vow_paybook_str,
    vow_timeline_hour_str,
    vow_timeline_month_str,
    vow_timeline_weekday_str,
    vow_timeoffi_str,
    vowunit_str,
)
from src.a15_vow_logic.vow_config import get_vow_dimens
from src.a16_pidgin_logic._test_util.a16_str import (
    inx_bridge_str,
    otx_bridge_str,
    pidgin_core_str,
    pidgin_label_str,
    pidgin_name_str,
    pidgin_title_str,
    pidgin_way_str,
    unknown_str_str,
)
from src.a16_pidgin_logic.pidgin_config import find_set_otx_inx_args, get_pidgin_dimens
from src.a17_idea_logic._test_util.a17_str import idea_category_str, idea_number_str
from src.a17_idea_logic.idea_config import (
    get_default_sorted_list,
    get_idea_config_dict,
    get_idea_sqlite_types,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    ALL_DIMEN_ABBV7,
    create_insert_into_pidgin_core_raw_sqlstr,
    create_insert_missing_face_name_into_pidgin_core_vld_sqlstr,
    create_insert_pidgin_core_agg_into_vld_sqlstr,
    create_insert_pidgin_sound_vld_table_sqlstr,
    create_prime_tablename as prime_tbl,
    create_sound_agg_insert_sqlstrs,
    create_sound_and_voice_tables,
    create_sound_raw_update_inconsist_error_message_sqlstr,
    get_dimen_abbv7,
    get_insert_into_sound_vld_sqlstrs,
    get_insert_into_voice_raw_sqlstrs,
    get_plan_voice_agg_tablenames,
    get_prime_create_table_sqlstrs,
    get_vow_plan_sound_agg_tablenames,
)

PLAN_PRIME_TABLENAMES = {
    f"{plan_acct_membership_str()}_sound_put_agg": "PLANMEMB_PUT_AGG",
    f"{plan_acct_membership_str()}_sound_put_raw": "PLANMEMB_PUT_RAW",
    f"{plan_acctunit_str()}_sound_put_agg": "PLANACCT_PUT_AGG",
    f"{plan_acctunit_str()}_sound_put_raw": "PLANACCT_PUT_RAW",
    f"{plan_concept_awardlink_str()}_sound_put_agg": "PLANAWAR_PUT_AGG",
    f"{plan_concept_awardlink_str()}_sound_put_raw": "PLANAWAR_PUT_RAW",
    f"{plan_concept_factunit_str()}_sound_put_agg": "PLANFACT_PUT_AGG",
    f"{plan_concept_factunit_str()}_sound_put_raw": "PLANFACT_PUT_RAW",
    f"{plan_concept_healerlink_str()}_sound_put_agg": "PLANHEAL_PUT_AGG",
    f"{plan_concept_healerlink_str()}_sound_put_raw": "PLANHEAL_PUT_RAW",
    f"{plan_concept_reason_premiseunit_str()}_sound_put_agg": "PLANPREM_PUT_AGG",
    f"{plan_concept_reason_premiseunit_str()}_sound_put_raw": "PLANPREM_PUT_RAW",
    f"{plan_concept_reasonunit_str()}_sound_put_agg": "PLANREAS_PUT_AGG",
    f"{plan_concept_reasonunit_str()}_sound_put_raw": "PLANREAS_PUT_RAW",
    f"{plan_concept_laborlink_str()}_sound_put_agg": "PLANLABO_PUT_AGG",
    f"{plan_concept_laborlink_str()}_sound_put_raw": "PLANLABO_PUT_RAW",
    f"{plan_conceptunit_str()}_sound_put_agg": "PLANCONC_PUT_AGG",
    f"{plan_conceptunit_str()}_sound_put_raw": "PLANCONC_PUT_RAW",
    f"{planunit_str()}_sound_put_agg": "PLANUNIT_PUT_AGG",
    f"{planunit_str()}_sound_put_raw": "PLANUNIT_PUT_RAW",
    f"{plan_acct_membership_str()}_sound_del_agg": "PLANMEMB_DEL_AGG",
    f"{plan_acct_membership_str()}_sound_del_raw": "PLANMEMB_DEL_RAW",
    f"{plan_acctunit_str()}_sound_del_agg": "PLANACCT_DEL_AGG",
    f"{plan_acctunit_str()}_sound_del_raw": "PLANACCT_DEL_RAW",
    f"{plan_concept_awardlink_str()}_sound_del_agg": "PLANAWAR_DEL_AGG",
    f"{plan_concept_awardlink_str()}_sound_del_raw": "PLANAWAR_DEL_RAW",
    f"{plan_concept_factunit_str()}_sound_del_agg": "PLANFACT_DEL_AGG",
    f"{plan_concept_factunit_str()}_sound_del_raw": "PLANFACT_DEL_RAW",
    f"{plan_concept_healerlink_str()}_sound_del_agg": "PLANHEAL_DEL_AGG",
    f"{plan_concept_healerlink_str()}_sound_del_raw": "PLANHEAL_DEL_RAW",
    f"{plan_concept_reason_premiseunit_str()}_sound_del_agg": "PLANPREM_DEL_AGG",
    f"{plan_concept_reason_premiseunit_str()}_sound_del_raw": "PLANPREM_DEL_RAW",
    f"{plan_concept_reasonunit_str()}_sound_del_agg": "PLANREAS_DEL_AGG",
    f"{plan_concept_reasonunit_str()}_sound_del_raw": "PLANREAS_DEL_RAW",
    f"{plan_concept_laborlink_str()}_sound_del_agg": "PLANLABO_DEL_AGG",
    f"{plan_concept_laborlink_str()}_sound_del_raw": "PLANLABO_DEL_RAW",
    f"{plan_conceptunit_str()}_sound_del_agg": "PLANCONC_DEL_AGG",
    f"{plan_conceptunit_str()}_sound_del_raw": "PLANCONC_DEL_RAW",
    f"{planunit_str()}_sound_del_agg": "PLANUNIT_DEL_AGG",
    f"{planunit_str()}_sound_del_raw": "PLANUNIT_DEL_RAW",
}


def test_ALL_DIMEN_ABBV7_has_all_dimens():
    # ESTABLISH / WHEN / THEN
    assert len(ALL_DIMEN_ABBV7) == len(get_idea_config_dict())


def get_all_dimen_columns_set(x_dimen: str) -> set[str]:
    if x_dimen == pidgin_core_str():
        return {
            event_int_str(),
            face_name_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_str_str(),
        }
    x_config = get_idea_config_dict().get(x_dimen)
    columns = set(x_config.get("jkeys").keys())
    columns.update(set(x_config.get("jvalues").keys()))
    return columns


def get_del_dimen_columns_set(x_dimen: str) -> list[str]:
    x_config = get_idea_config_dict().get(x_dimen)
    columns_set = set(x_config.get("jkeys").keys())
    columns_list = get_default_sorted_list(columns_set)
    columns_list[-1] = get_delete_key_name(columns_list[-1])
    return set(columns_list)


def create_pidgin_sound_raw_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add(idea_number_str())
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_pidgin_sound_agg_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_vow_sound_agg_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_vow_sound_vld_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_pidgin_sound_vld_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.remove(otx_bridge_str())
    columns.remove(inx_bridge_str())
    columns.remove(unknown_str_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_pidgin_core_raw_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.remove(event_int_str())
    columns.add("source_dimen")
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_pidgin_core_agg_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.remove(event_int_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_pidgin_core_vld_table_sqlstr(x_dimen):
    agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
    vld_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
    sqlstr = create_pidgin_core_agg_table_sqlstr(x_dimen)
    sqlstr = sqlstr.replace(agg_tablename, vld_tablename)
    return sqlstr


def create_vow_voice_raw_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = find_set_otx_inx_args(columns)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_vow_voice_agg_table_sqlstr(x_dimen: str):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.remove(event_int_str())
    columns.remove(face_name_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_plan_sound_put_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add(idea_number_str())
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_plan_sound_put_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_plan_sound_put_vld_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_plan_sound_del_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns.add(idea_number_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_plan_sound_del_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_plan_sound_del_vld_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_plan_voice_put_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw", "put")
    columns = set()
    columns = get_all_dimen_columns_set(x_dimen)
    columns = find_set_otx_inx_args(columns)
    columns.add("pidgin_event_int")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_plan_voice_put_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "agg", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_plan_voice_del_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns = find_set_otx_inx_args(columns)
    columns.add("pidgin_event_int")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_plan_voice_del_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "agg", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def test_get_prime_create_table_sqlstrs_ReturnsObj_CheckPidginDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    idea_config = get_idea_config_dict()
    pidgin_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "pidgin"
    }

    for x_dimen in pidgin_dimens_config:
        s_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw")
        s_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
        s_vld_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
        expected_s_raw_sqlstr = create_pidgin_sound_raw_table_sqlstr(x_dimen)
        expected_s_agg_sqlstr = create_pidgin_sound_agg_table_sqlstr(x_dimen)
        expected_s_vld_sqlstr = create_pidgin_sound_vld_table_sqlstr(x_dimen)

        abbv7 = get_dimen_abbv7(x_dimen)
        print(f'CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR= """{expected_s_raw_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR= """{expected_s_agg_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_SOUND_VLD_SQLSTR= """{expected_s_vld_sqlstr}"""')

        # print(f'"{s_raw_tablename}": CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR,')
        # print(f'"{s_agg_tablename}": CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR,')
        # print(f'"{s_vld_tablename}": CREATE_{abbv7.upper()}_SOUND_VLD_SQLSTR,')
        assert expected_s_raw_sqlstr == create_table_sqlstrs.get(s_raw_tablename)
        assert expected_s_agg_sqlstr == create_table_sqlstrs.get(s_agg_tablename)
        assert expected_s_vld_sqlstr == create_table_sqlstrs.get(s_vld_tablename)


def test_get_prime_create_table_sqlstrs_ReturnsObj_CheckPidginCoreDimens():
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    x_dimen = pidgin_core_str()
    s_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw")
    s_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
    s_vld_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
    expected_s_raw_sqlstr = create_pidgin_core_raw_table_sqlstr(x_dimen)
    expected_s_agg_sqlstr = create_pidgin_core_agg_table_sqlstr(x_dimen)
    expected_s_vld_sqlstr = create_pidgin_core_vld_table_sqlstr(x_dimen)

    abbv7 = get_dimen_abbv7(x_dimen)
    # print(f'CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR= """{expected_s_raw_sqlstr}"""')
    # print(f'CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR= """{expected_s_agg_sqlstr}"""')
    # print(f'CREATE_{abbv7.upper()}_SOUND_VLD_SQLSTR= """{expected_s_vld_sqlstr}"""')

    print(f'"{s_raw_tablename}": CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR,')
    print(f'"{s_agg_tablename}": CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR,')
    print(f'"{s_vld_tablename}": CREATE_{abbv7.upper()}_SOUND_VLD_SQLSTR,')
    assert expected_s_raw_sqlstr == create_table_sqlstrs.get(s_raw_tablename)
    assert expected_s_agg_sqlstr == create_table_sqlstrs.get(s_agg_tablename)
    assert expected_s_vld_sqlstr == create_table_sqlstrs.get(s_vld_tablename)


def test_get_prime_create_table_sqlstrs_ReturnsObj_CheckVowDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    idea_config = get_idea_config_dict()
    vow_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "vow"
    }

    for x_dimen in vow_dimens_config:
        # print(f"{abbv7} {x_dimen} checking...")
        s_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw")
        s_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
        s_vld_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
        v_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw")
        v_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "agg")
        expected_s_raw_sqlstr = create_pidgin_sound_raw_table_sqlstr(x_dimen)
        expected_s_agg_sqlstr = create_vow_sound_agg_table_sqlstr(x_dimen)
        expected_s_vld_sqlstr = create_vow_sound_vld_table_sqlstr(x_dimen)
        expected_v_raw_sqlstr = create_vow_voice_raw_table_sqlstr(x_dimen)
        expected_v_agg_sqlstr = create_vow_voice_agg_table_sqlstr(x_dimen)
        abbv7 = get_dimen_abbv7(x_dimen)
        print(f'CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR= """{expected_s_raw_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR= """{expected_s_agg_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_SOUND_VLD_SQLSTR= """{expected_s_vld_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_VOICE_RAW_SQLSTR= """{expected_v_raw_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_VOICE_AGG_SQLSTR= """{expected_v_agg_sqlstr}"""')
        # print(f'"{s_raw_tablename}": CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR,')
        # print(f'"{s_agg_tablename}": CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR,')
        # print(f'"{s_vld_tablename}": CREATE_{abbv7.upper()}_SOUND_VLD_SQLSTR,')
        # print(f'"{v_raw_tablename}": CREATE_{abbv7.upper()}_VOICE_RAW_SQLSTR,')
        # print(f'"{v_agg_tablename}": CREATE_{abbv7.upper()}_VOICE_AGG_SQLSTR,')
        assert expected_s_raw_sqlstr == create_table_sqlstrs.get(s_raw_tablename)
        assert expected_s_agg_sqlstr == create_table_sqlstrs.get(s_agg_tablename)
        assert expected_s_vld_sqlstr == create_table_sqlstrs.get(s_vld_tablename)
        assert expected_v_raw_sqlstr == create_table_sqlstrs.get(v_raw_tablename)
        assert expected_v_agg_sqlstr == create_table_sqlstrs.get(v_agg_tablename)


def test_get_prime_create_table_sqlstrs_ReturnsObj_CheckPlanDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    plan_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in get_idea_config_dict().items()
        if dimen_config.get(idea_category_str()) == "plan"
    }

    for x_dimen in plan_dimens_config:
        # print(f"{x_dimen} checking...")
        s_put_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw", "put")
        s_put_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg", "put")
        s_put_vld_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld", "put")
        s_del_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw", "del")
        s_del_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg", "del")
        s_del_vld_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld", "del")
        v_put_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw", "put")
        v_put_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "agg", "put")
        v_del_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw", "del")
        v_del_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "agg", "del")

        expected_s_put_raw_sqlstr = create_plan_sound_put_raw_table_sqlstr(x_dimen)
        expected_s_put_agg_sqlstr = create_plan_sound_put_agg_table_sqlstr(x_dimen)
        expected_s_put_vld_sqlstr = create_plan_sound_put_vld_table_sqlstr(x_dimen)
        expected_s_del_raw_sqlstr = create_plan_sound_del_raw_table_sqlstr(x_dimen)
        expected_s_del_agg_sqlstr = create_plan_sound_del_agg_table_sqlstr(x_dimen)
        expected_s_del_vld_sqlstr = create_plan_sound_del_vld_table_sqlstr(x_dimen)
        expected_v_put_raw_sqlstr = create_plan_voice_put_raw_table_sqlstr(x_dimen)
        expected_v_put_agg_sqlstr = create_plan_voice_put_agg_table_sqlstr(x_dimen)
        expected_v_del_raw_sqlstr = create_plan_voice_del_raw_table_sqlstr(x_dimen)
        expected_v_del_agg_sqlstr = create_plan_voice_del_agg_table_sqlstr(x_dimen)
        abbv7 = get_dimen_abbv7(x_dimen)
        print(f"{x_dimen=} {abbv7=}")
        # print(f'CREATE_{abbv7}_SOUND_PUT_RAW_STR= "{expected_s_put_raw_sqlstr}"')
        # print(f'CREATE_{abbv7}_SOUND_PUT_AGG_STR= "{expected_s_put_agg_sqlstr}"')
        # print(f'CREATE_{abbv7}_SOUND_PUT_VLD_STR= "{expected_s_put_vld_sqlstr}"')
        # print(f'CREATE_{abbv7}_SOUND_DEL_RAW_STR= "{expected_s_del_raw_sqlstr}"')
        # print(f'CREATE_{abbv7}_SOUND_DEL_AGG_STR= "{expected_s_del_agg_sqlstr}"')
        # print(f'CREATE_{abbv7}_SOUND_DEL_VLD_STR= "{expected_s_del_vld_sqlstr}"')
        # print(f'CREATE_{abbv7}_VOICE_PUT_RAW_STR= "{expected_v_put_raw_sqlstr}"')
        # print(f'CREATE_{abbv7}_VOICE_PUT_AGG_STR= "{expected_v_put_agg_sqlstr}"')
        # print(f'CREATE_{abbv7}_VOICE_DEL_RAW_STR= "{expected_v_del_raw_sqlstr}"')
        # print(f'CREATE_{abbv7}_VOICE_DEL_AGG_STR= "{expected_v_del_agg_sqlstr}"')

        # print(f'"{s_put_raw_tablename}": CREATE_{abbv7}_SOUND_PUT_RAW_STR,')
        # print(f'"{s_put_agg_tablename}": CREATE_{abbv7}_SOUND_PUT_AGG_STR,')
        # print(f'"{s_put_vld_tablename}": CREATE_{abbv7}_SOUND_PUT_VLD_STR,')
        # print(f'"{s_del_raw_tablename}": CREATE_{abbv7}_SOUND_DEL_RAW_STR,')
        # print(f'"{s_del_agg_tablename}": CREATE_{abbv7}_SOUND_DEL_AGG_STR,')
        # print(f'"{s_del_vld_tablename}": CREATE_{abbv7}_SOUND_DEL_VLD_STR,')
        # print(f'"{v_put_raw_tablename}": CREATE_{abbv7}_VOICE_PUT_RAW_STR,')
        # print(f'"{v_put_agg_tablename}": CREATE_{abbv7}_VOICE_PUT_AGG_STR,')
        # print(f'"{v_del_raw_tablename}": CREATE_{abbv7}_VOICE_DEL_RAW_STR,')
        # print(f'"{v_del_agg_tablename}": CREATE_{abbv7}_VOICE_DEL_AGG_STR,')
        assert expected_s_put_raw_sqlstr == sqlstrs.get(s_put_raw_tablename)
        assert expected_s_put_agg_sqlstr == sqlstrs.get(s_put_agg_tablename)
        assert expected_s_put_vld_sqlstr == sqlstrs.get(s_put_vld_tablename)
        assert expected_s_del_raw_sqlstr == sqlstrs.get(s_del_raw_tablename)
        assert expected_s_del_agg_sqlstr == sqlstrs.get(s_del_agg_tablename)
        assert expected_s_del_vld_sqlstr == sqlstrs.get(s_del_vld_tablename)
        assert expected_v_put_raw_sqlstr == sqlstrs.get(v_put_raw_tablename)
        assert expected_v_put_agg_sqlstr == sqlstrs.get(v_put_agg_tablename)
        assert expected_v_del_raw_sqlstr == sqlstrs.get(v_del_raw_tablename)
        assert expected_v_del_agg_sqlstr == sqlstrs.get(v_del_agg_tablename)


def test_get_prime_create_table_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    assert create_table_sqlstrs
    pidgin_dimens_count = len(get_pidgin_dimens()) * 3
    vow_dimens_count = len(get_vow_dimens()) * 5
    plan_dimens_count = len(get_plan_dimens()) * 10
    print(f"{pidgin_dimens_count=}")
    print(f"{vow_dimens_count=}")
    print(f"{plan_dimens_count=}")
    all_dimens_count = pidgin_dimens_count + vow_dimens_count + plan_dimens_count
    pidgin_core_count = 3
    all_dimens_count += pidgin_core_count
    assert len(create_table_sqlstrs) == all_dimens_count


def test_get_vow_plan_sound_agg_tablenames_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    vow_plan_sound_agg_tablenames = get_vow_plan_sound_agg_tablenames()

    # THEN
    assert vow_plan_sound_agg_tablenames
    expected_sound_agg_tablenames = set()
    for plan_dimen in get_plan_dimens():
        expected_sound_agg_tablenames.add(prime_tbl(plan_dimen, "s", "agg", "put"))
        expected_sound_agg_tablenames.add(prime_tbl(plan_dimen, "s", "agg", "del"))
    for vow_dimen in get_vow_dimens():
        expected_sound_agg_tablenames.add(prime_tbl(vow_dimen, "s", "agg"))
    print(sorted(list(expected_sound_agg_tablenames)))
    assert expected_sound_agg_tablenames == vow_plan_sound_agg_tablenames
    agg_tablenames = vow_plan_sound_agg_tablenames
    assert len(agg_tablenames) == len(get_plan_dimens()) * 2 + len(get_vow_dimens())
    assert agg_tablenames.issubset(set(get_prime_create_table_sqlstrs().keys()))


def test_get_plan_voice_agg_tablenames_ReturnsObj_PlanDimens():
    # ESTABLISH / WHEN
    plan_voice_agg_tablenames = get_plan_voice_agg_tablenames()

    # THEN
    assert plan_voice_agg_tablenames
    expected_plan_voice_agg_tablenames = {
        prime_tbl(plan_dimen, "v", "agg", "put") for plan_dimen in get_plan_dimens()
    }
    print(f"{expected_plan_voice_agg_tablenames=}")
    assert expected_plan_voice_agg_tablenames == plan_voice_agg_tablenames
    assert len(plan_voice_agg_tablenames) == len(get_plan_dimens())
    agg_tablenames = plan_voice_agg_tablenames
    assert agg_tablenames.issubset(set(get_prime_create_table_sqlstrs().keys()))


def test_create_sound_and_voice_tables_CreatesVowRawTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as vow_db_conn:
        cursor = vow_db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 0
        agg_str = "agg"
        raw_str = "raw"
        vld_str = "vld"
        put_str = "put"
        del_str = "del"
        planunit_s_put_agg_table = prime_tbl("planunit", "s", agg_str, put_str)
        planacct_s_put_agg_table = prime_tbl("planacct", "s", agg_str, put_str)
        planmemb_s_put_agg_table = prime_tbl("planmemb", "s", agg_str, put_str)
        planfact_s_del_agg_table = prime_tbl("planfact", "s", agg_str, del_str)
        planfact_s_del_vld_table = prime_tbl("planfact", "s", vld_str, del_str)
        fisunit_s_agg_table = prime_tbl("fisunit", "s", agg_str)
        fisunit_s_vld_table = prime_tbl("fisunit", "s", vld_str)
        pidtitl_s_agg_table = prime_tbl("pidtitl", "s", agg_str)
        fishour_v_agg_table = prime_tbl("fishour", "v", agg_str)
        pidtitl_s_raw_table = prime_tbl("pidtitl", "s", raw_str)
        pidcore_s_raw_table = prime_tbl("pidcore", "s", raw_str)
        pidcore_s_agg_table = prime_tbl("pidcore", "s", agg_str)
        pidcore_s_vld_table = prime_tbl("pidcore", "s", vld_str)

        assert not db_table_exists(cursor, planunit_s_put_agg_table)
        assert not db_table_exists(cursor, planacct_s_put_agg_table)
        assert not db_table_exists(cursor, planmemb_s_put_agg_table)
        assert not db_table_exists(cursor, planfact_s_del_agg_table)
        assert not db_table_exists(cursor, planfact_s_del_vld_table)
        assert not db_table_exists(cursor, fisunit_s_agg_table)
        assert not db_table_exists(cursor, fisunit_s_vld_table)
        assert not db_table_exists(cursor, pidtitl_s_agg_table)
        assert not db_table_exists(cursor, fishour_v_agg_table)
        assert not db_table_exists(cursor, pidtitl_s_raw_table)
        assert not db_table_exists(cursor, pidcore_s_raw_table)
        assert not db_table_exists(cursor, pidcore_s_agg_table)
        assert not db_table_exists(cursor, pidcore_s_vld_table)

        # WHEN
        create_sound_and_voice_tables(cursor)

        # THEN
        cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        # print(f"{cursor.fetchall()=}")
        # x_count = 0
        # for x_row in cursor.fetchall():
        #     print(f"{x_count} {x_row[1]=}")
        #     x_count += 1
        assert db_table_exists(cursor, planunit_s_put_agg_table)
        assert db_table_exists(cursor, planacct_s_put_agg_table)
        assert db_table_exists(cursor, planmemb_s_put_agg_table)
        assert db_table_exists(cursor, planfact_s_del_agg_table)
        assert db_table_exists(cursor, planfact_s_del_vld_table)
        assert db_table_exists(cursor, fisunit_s_agg_table)
        assert db_table_exists(cursor, fisunit_s_vld_table)
        assert db_table_exists(cursor, pidtitl_s_agg_table)
        assert db_table_exists(cursor, fishour_v_agg_table)
        assert db_table_exists(cursor, pidtitl_s_raw_table)
        assert db_table_exists(cursor, pidcore_s_raw_table)
        assert db_table_exists(cursor, pidcore_s_agg_table)
        assert db_table_exists(cursor, pidcore_s_vld_table)
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 150


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario0_PidginDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = pidgin_title_str()
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        # WHEN
        update_sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
            cursor, dimen
        )

        # THEN
        x_tablename = prime_tbl(dimen, "s", "raw")
        dimen_config = get_idea_config_dict().get(dimen)
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        exclude_cols = {idea_number_str(), "error_message"}
        expected_update_sqlstr = create_update_inconsistency_error_query(
            cursor, x_tablename, dimen_focus_columns, exclude_cols
        )
        assert update_sqlstr == expected_update_sqlstr

        static_example_sqlstr = """WITH inconsistency_rows AS (
SELECT event_int, face_name, otx_title
FROM pidgin_title_s_raw
GROUP BY event_int, face_name, otx_title
HAVING MIN(inx_title) != MAX(inx_title)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_str) != MAX(unknown_str)
)
UPDATE pidgin_title_s_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = pidgin_title_s_raw.event_int
    AND inconsistency_rows.face_name = pidgin_title_s_raw.face_name
    AND inconsistency_rows.otx_title = pidgin_title_s_raw.otx_title
;
"""
        print(update_sqlstr)
        assert update_sqlstr == static_example_sqlstr


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario1_VowDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = vow_timeline_hour_str()
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        # WHEN
        update_sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
            cursor, dimen
        )

        # THEN
        x_tablename = prime_tbl(dimen, "s", "raw")
        dimen_config = get_idea_config_dict().get(dimen)
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        exclude_cols = {idea_number_str(), "event_int", "face_name", "error_message"}
        expected_update_sqlstr = create_update_inconsistency_error_query(
            cursor, x_tablename, dimen_focus_columns, exclude_cols
        )
        print(expected_update_sqlstr)
        assert update_sqlstr == expected_update_sqlstr

        static_example_sqlstr = """WITH inconsistency_rows AS (
SELECT vow_label, cumlative_minute
FROM vow_timeline_hour_s_raw
GROUP BY vow_label, cumlative_minute
HAVING MIN(hour_label) != MAX(hour_label)
)
UPDATE vow_timeline_hour_s_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.vow_label = vow_timeline_hour_s_raw.vow_label
    AND inconsistency_rows.cumlative_minute = vow_timeline_hour_s_raw.cumlative_minute
;
"""
        # print(update_sqlstr)
        assert update_sqlstr == static_example_sqlstr


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario2_PlanDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = plan_concept_awardlink_str()
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        # WHEN
        update_sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
            cursor, dimen
        )

        # THEN
        x_tablename = prime_tbl(dimen, "s", "raw", "put")
        dimen_config = get_idea_config_dict().get(dimen)
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        exclude_cols = {idea_number_str(), "error_message"}
        expected_update_sqlstr = create_update_inconsistency_error_query(
            cursor, x_tablename, dimen_focus_columns, exclude_cols
        )
        print(expected_update_sqlstr)
        assert update_sqlstr == expected_update_sqlstr

        static_example_sqlstr = """WITH inconsistency_rows AS (
SELECT event_int, face_name, vow_label, owner_name, concept_way, awardee_title
FROM plan_concept_awardlink_s_put_raw
GROUP BY event_int, face_name, vow_label, owner_name, concept_way, awardee_title
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
)
UPDATE plan_concept_awardlink_s_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = plan_concept_awardlink_s_put_raw.event_int
    AND inconsistency_rows.face_name = plan_concept_awardlink_s_put_raw.face_name
    AND inconsistency_rows.vow_label = plan_concept_awardlink_s_put_raw.vow_label
    AND inconsistency_rows.owner_name = plan_concept_awardlink_s_put_raw.owner_name
    AND inconsistency_rows.concept_way = plan_concept_awardlink_s_put_raw.concept_way
    AND inconsistency_rows.awardee_title = plan_concept_awardlink_s_put_raw.awardee_title
;
"""
        print(update_sqlstr)
        assert update_sqlstr == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario0_PidginDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = pidgin_title_str()
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        # WHEN
        update_sqlstrs = create_sound_agg_insert_sqlstrs(cursor, dimen)

        # THEN
        raw_tablename = prime_tbl(dimen, "s", "raw")
        agg_tablename = prime_tbl(dimen, "s", "agg")
        dimen_config = get_idea_config_dict().get(dimen)
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        exclude_cols = {idea_number_str(), "error_message"}
        expected_insert_sqlstr = create_table2table_agg_insert_query(
            cursor,
            src_table=raw_tablename,
            dst_table=agg_tablename,
            focus_cols=dimen_focus_columns,
            exclude_cols=exclude_cols,
        )
        # print(expected_insert_sqlstr)
        assert update_sqlstrs[0] == expected_insert_sqlstr

        static_example_sqlstr = """INSERT INTO pidgin_title_s_agg (event_int, face_name, otx_title, inx_title, otx_bridge, inx_bridge, unknown_str)
SELECT event_int, face_name, otx_title, MAX(inx_title), MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_str)
FROM pidgin_title_s_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, otx_title
;
"""
        print(update_sqlstrs[0])
        assert update_sqlstrs[0] == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario1_VowDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = vow_timeline_hour_str()
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        # WHEN
        update_sqlstrs = create_sound_agg_insert_sqlstrs(cursor, dimen)

        # THEN
        raw_tablename = prime_tbl(dimen, "s", "raw")
        agg_tablename = prime_tbl(dimen, "s", "agg")
        dimen_config = get_idea_config_dict().get(dimen)
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
        exclude_cols = {
            idea_number_str(),
            "error_message",
        }
        print("yeah")
        expected_insert_sqlstr = create_table2table_agg_insert_query(
            cursor,
            src_table=raw_tablename,
            dst_table=agg_tablename,
            focus_cols=dimen_focus_columns,
            exclude_cols=exclude_cols,
        )
        print(expected_insert_sqlstr)
        assert update_sqlstrs[0] == expected_insert_sqlstr

        static_example_sqlstr = """INSERT INTO vow_timeline_hour_s_agg (event_int, face_name, vow_label, cumlative_minute, hour_label)
SELECT event_int, face_name, vow_label, cumlative_minute, MAX(hour_label)
FROM vow_timeline_hour_s_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, vow_label, cumlative_minute
;
"""
        print(update_sqlstrs[0])
        assert update_sqlstrs[0] == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario2_PlanDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = plan_concept_awardlink_str()
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        # WHEN
        update_sqlstrs = create_sound_agg_insert_sqlstrs(cursor, dimen)

        # THEN
        put_raw_tablename = prime_tbl(dimen, "s", "raw", "put")
        put_agg_tablename = prime_tbl(dimen, "s", "agg", "put")
        put_dimen_config = get_idea_config_dict().get(dimen)
        put_dimen_focus_columns = set(put_dimen_config.get("jkeys").keys())
        put_exclude_cols = {idea_number_str(), "error_message"}
        put_expected_insert_sqlstr = create_table2table_agg_insert_query(
            cursor,
            src_table=put_raw_tablename,
            dst_table=put_agg_tablename,
            focus_cols=put_dimen_focus_columns,
            exclude_cols=put_exclude_cols,
        )
        # print(put_expected_insert_sqlstr)
        assert update_sqlstrs[0] == put_expected_insert_sqlstr

        static_example_put_sqlstr = """INSERT INTO plan_concept_awardlink_s_put_agg (event_int, face_name, vow_label, owner_name, concept_way, awardee_title, give_force, take_force)
SELECT event_int, face_name, vow_label, owner_name, concept_way, awardee_title, MAX(give_force), MAX(take_force)
FROM plan_concept_awardlink_s_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, vow_label, owner_name, concept_way, awardee_title
;
"""
        # print(update_sqlstrs[0])
        assert update_sqlstrs[0] == static_example_put_sqlstr

        # del
        del_raw_tablename = prime_tbl(dimen, "s", "raw", "del")
        del_agg_tablename = prime_tbl(dimen, "s", "agg", "del")
        del_dimen_focus_columns = set(put_dimen_config.get("jkeys").keys())
        del_dimen_focus_columns = get_default_sorted_list(del_dimen_focus_columns)
        last_element = del_dimen_focus_columns.pop(-1)
        del_dimen_focus_columns.append(f"{last_element}_ERASE")
        print(f"{del_dimen_focus_columns=} {last_element}")
        del_exclude_cols = {idea_number_str(), "error_message"}
        del_expected_insert_sqlstr = create_table2table_agg_insert_query(
            cursor,
            src_table=del_raw_tablename,
            dst_table=del_agg_tablename,
            focus_cols=del_dimen_focus_columns,
            exclude_cols=del_exclude_cols,
            where_block="",
        )
        print(del_expected_insert_sqlstr)
        print(update_sqlstrs[1])
        assert update_sqlstrs[1] == del_expected_insert_sqlstr

        static_example_del_sqlstr = """INSERT INTO plan_concept_awardlink_s_del_agg (event_int, face_name, vow_label, owner_name, concept_way, awardee_title_ERASE)
SELECT event_int, face_name, vow_label, owner_name, concept_way, awardee_title_ERASE
FROM plan_concept_awardlink_s_del_raw
GROUP BY event_int, face_name, vow_label, owner_name, concept_way, awardee_title_ERASE
;
"""
        assert update_sqlstrs[1] == static_example_del_sqlstr


def test_create_insert_into_pidgin_core_raw_sqlstr_ReturnsObj():
    # ESTABLISH
    dimen = pidgin_way_str()
    # WHEN
    way_sqlstr = create_insert_into_pidgin_core_raw_sqlstr(dimen)

    # THEN
    pidgin_s_agg_tablename = prime_tbl(dimen, "s", "agg")
    pidgin_core_s_raw_tablename = prime_tbl("PIDCORE", "s", "raw")
    expected_sqlstr = f"""INSERT INTO {pidgin_core_s_raw_tablename} (source_dimen, face_name, otx_bridge, inx_bridge, unknown_str)
SELECT '{pidgin_s_agg_tablename}', face_name, otx_bridge, inx_bridge, unknown_str
FROM {pidgin_s_agg_tablename}
GROUP BY face_name, otx_bridge, inx_bridge, unknown_str
;
"""
    assert way_sqlstr == expected_sqlstr


def test_create_insert_pidgin_core_agg_into_vld_sqlstr_ReturnsObj():
    # ESTABLISH
    default_bridge = "|"
    default_unknown_str = "unknown2"

    # WHEN
    insert_sqlstr = create_insert_pidgin_core_agg_into_vld_sqlstr(
        default_bridge, default_unknown_str
    )

    # THEN
    pidcore_dimen = "PIDCORE"
    pidgin_core_s_agg_tablename = prime_tbl(pidcore_dimen, "s", "agg")
    pidgin_core_s_vld_tablename = prime_tbl(pidcore_dimen, "s", "vld")
    expected_sqlstr = f"""INSERT INTO {pidgin_core_s_vld_tablename} (face_name, otx_bridge, inx_bridge, unknown_str)
SELECT
  face_name
, IFNULL(otx_bridge, '{default_bridge}')
, IFNULL(inx_bridge, '{default_bridge}')
, IFNULL(unknown_str, '{default_unknown_str}')
FROM {pidgin_core_s_agg_tablename}
;
"""
    print(expected_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_insert_missing_face_name_into_pidgin_core_vld_sqlstr_ReturnsObj():
    # ESTABLISH
    default_bridge = "|"
    default_unknown_str = "unknown2"
    planacct_s_agg_tablename = prime_tbl(plan_acctunit_str(), "s", "agg")

    # WHEN
    insert_sqlstr = create_insert_missing_face_name_into_pidgin_core_vld_sqlstr(
        default_bridge, default_unknown_str, planacct_s_agg_tablename
    )

    # THEN
    pidcore_dimen = "PIDCORE"
    pidgin_core_s_vld_tablename = prime_tbl(pidcore_dimen, "s", "vld")
    expected_sqlstr = f"""INSERT INTO {pidgin_core_s_vld_tablename} (face_name, otx_bridge, inx_bridge, unknown_str)
SELECT
  {planacct_s_agg_tablename}.face_name
, '{default_bridge}'
, '{default_bridge}'
, '{default_unknown_str}'
FROM {planacct_s_agg_tablename} 
LEFT JOIN pidgin_core_s_vld ON pidgin_core_s_vld.face_name = {planacct_s_agg_tablename}.face_name
WHERE pidgin_core_s_vld.face_name IS NULL
GROUP BY {planacct_s_agg_tablename}.face_name
;
"""
    print(expected_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_insert_pidgin_sound_vld_table_sqlstr_ReturnsObj_pidgin_way():
    # ESTABLISH
    dimen = pidgin_way_str()
    # WHEN
    way_sqlstr = create_insert_pidgin_sound_vld_table_sqlstr(dimen)

    # THEN
    pidgin_dimen_s_agg_tablename = prime_tbl(dimen, "s", "agg")
    pidgin_dimen_s_vld_tablename = prime_tbl(dimen, "s", "vld")
    expected_way_sqlstr = f"""
INSERT INTO {pidgin_dimen_s_vld_tablename} (event_int, face_name, otx_way, inx_way)
SELECT event_int, face_name, MAX(otx_way), MAX(inx_way)
FROM {pidgin_dimen_s_agg_tablename}
WHERE error_message IS NULL
GROUP BY event_int, face_name
;
"""
    print(expected_way_sqlstr)
    assert way_sqlstr == expected_way_sqlstr


def test_create_insert_pidgin_sound_vld_table_sqlstr_ReturnsObj_pidgin_label():
    # ESTABLISH
    dimen = pidgin_label_str()
    # WHEN
    label_sqlstr = create_insert_pidgin_sound_vld_table_sqlstr(dimen)

    # THEN
    pidgin_label_s_agg_tablename = prime_tbl(dimen, "s", "agg")
    pidgin_label_s_vld_tablename = prime_tbl(dimen, "s", "vld")
    expected_label_sqlstr = f"""
INSERT INTO {pidgin_label_s_vld_tablename} (event_int, face_name, otx_label, inx_label)
SELECT event_int, face_name, MAX(otx_label), MAX(inx_label)
FROM {pidgin_label_s_agg_tablename}
WHERE error_message IS NULL
GROUP BY event_int, face_name
;
"""
    assert label_sqlstr == expected_label_sqlstr


def test_get_insert_into_sound_vld_sqlstrs_ReturnsObj_PlanDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    plan_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "plan"
    }

    # WHEN
    insert_s_vld_sqlstrs = get_insert_into_sound_vld_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        for plan_dimen in plan_dimens_config:
            # print(f"{plan_dimen=}")
            s_put_agg_tablename = prime_tbl(plan_dimen, "s", "agg", "put")
            s_del_agg_tablename = prime_tbl(plan_dimen, "s", "agg", "del")
            s_put_vld_tablename = prime_tbl(plan_dimen, "s", "vld", "put")
            s_del_vld_tablename = prime_tbl(plan_dimen, "s", "vld", "del")
            s_put_agg_cols = get_table_columns(cursor, s_put_agg_tablename)
            s_del_agg_cols = get_table_columns(cursor, s_del_agg_tablename)
            s_put_agg_cols.remove("error_message")
            s_del_agg_cols.remove("error_message")
            s_put_vld_cols = get_table_columns(cursor, s_put_vld_tablename)
            s_del_vld_cols = get_table_columns(cursor, s_del_vld_tablename)
            s_put_vld_tbl = s_put_vld_tablename
            s_del_vld_tbl = s_del_vld_tablename
            s_put_agg_tbl = s_put_agg_tablename
            s_del_agg_tbl = s_del_agg_tablename
            s_put_vld_insert_sql = get_insert_sql(cursor, s_put_vld_tbl, s_put_vld_cols)
            s_del_vld_insert_sql = get_insert_sql(cursor, s_del_vld_tbl, s_del_vld_cols)
            s_put_agg_select_sql = get_select_sql(
                cursor, s_put_agg_tbl, s_put_agg_cols, flat_bool=True
            )
            s_del_agg_select_sql = get_select_sql(
                cursor, s_del_agg_tbl, s_del_agg_cols, flat_bool=True
            )
            where_clause = "WHERE error_message IS NULL"
            s_put_agg_select_sql = f"{s_put_agg_select_sql}{where_clause}"
            s_del_agg_select_sql = f"{s_del_agg_select_sql}{where_clause}"
            s_put_vld_insert_select = f"{s_put_vld_insert_sql} {s_put_agg_select_sql}"
            s_del_vld_insert_select = f"{s_del_vld_insert_sql} {s_del_agg_select_sql}"
            # print(f"{s_put_vld_insert_sql=}")
            # create_select_query(cursor=)
            abbv7 = get_dimen_abbv7(plan_dimen)
            put_sqlstr_ref = f"INSERT_{abbv7.upper()}_SOUND_VLD_PUT_SQLSTR"
            del_sqlstr_ref = f"INSERT_{abbv7.upper()}_SOUND_VLD_DEL_SQLSTR"
            print(f'{put_sqlstr_ref}= "{s_put_vld_insert_select}"')
            print(f'{del_sqlstr_ref}= "{s_del_vld_insert_select}"')
            # print(f"""'{s_put_vld_tablename}': {put_sqlstr_ref},""")
            # print(f"""'{s_del_vld_tablename}': {del_sqlstr_ref},""")
            assert insert_s_vld_sqlstrs.get(s_put_vld_tbl) == s_put_vld_insert_select
            assert insert_s_vld_sqlstrs.get(s_del_vld_tbl) == s_del_vld_insert_select


def test_get_insert_into_sound_vld_sqlstrs_ReturnsObj_VowDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    vow_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "vow"
    }

    # WHEN
    insert_s_vld_sqlstrs = get_insert_into_sound_vld_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        for vow_dimen in vow_dimens_config:
            # print(f"{vow_dimen=}")
            s_agg_tablename = prime_tbl(vow_dimen, "s", "agg")
            s_vld_tablename = prime_tbl(vow_dimen, "s", "vld")
            s_agg_cols = get_table_columns(cursor, s_agg_tablename)
            s_agg_cols.remove("error_message")
            s_vld_cols = get_table_columns(cursor, s_vld_tablename)
            s_vld_tbl = s_vld_tablename
            s_agg_tbl = s_agg_tablename
            s_vld_insert_sql = get_insert_sql(cursor, s_vld_tbl, s_vld_cols)
            s_agg_select_sql = get_select_sql(
                cursor, s_agg_tbl, s_agg_cols, flat_bool=True
            )
            where_clause = "WHERE error_message IS NULL"
            s_agg_select_sql = f"{s_agg_select_sql}{where_clause}"
            s_vld_insert_select = f"{s_vld_insert_sql} {s_agg_select_sql}"
            # create_select_query(cursor=)
            abbv7 = get_dimen_abbv7(vow_dimen)
            sqlstr_ref = f"INSERT_{abbv7.upper()}_SOUND_VLD_SQLSTR"
            print(f'{sqlstr_ref}= "{s_vld_insert_select}"')
            # print(f""""{s_vld_tablename}": {sqlstr_ref},""")
            assert insert_s_vld_sqlstrs.get(s_vld_tbl) == s_vld_insert_select


def test_get_insert_into_voice_raw_sqlstrs_ReturnsObj_PlanDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    plan_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "plan"
    }

    # WHEN
    insert_v_raw_sqlstrs = get_insert_into_voice_raw_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        for plan_dimen in plan_dimens_config:
            # print(f"{plan_dimen=}")
            s_put_vld_tablename = prime_tbl(plan_dimen, "s", "vld", "put")
            s_del_vld_tablename = prime_tbl(plan_dimen, "s", "vld", "del")
            v_put_raw_tablename = prime_tbl(plan_dimen, "v", "raw", "put")
            v_del_raw_tablename = prime_tbl(plan_dimen, "v", "raw", "del")
            s_put_cols = get_table_columns(cursor, s_put_vld_tablename)
            s_del_cols = get_table_columns(cursor, s_del_vld_tablename)
            # s_put_cols = set(s_put_cols).remove("error_message")
            # s_del_cols = set(s_del_cols).remove("error_message")
            v_put_raw_cols = get_table_columns(cursor, v_put_raw_tablename)
            v_del_raw_cols = get_table_columns(cursor, v_del_raw_tablename)
            v_put_cols = find_set_otx_inx_args(v_put_raw_cols)
            v_del_cols = find_set_otx_inx_args(v_del_raw_cols)
            v_put_cols.remove("pidgin_event_int")
            v_del_cols.remove("pidgin_event_int")
            v_put_cols = {col for col in v_put_cols if col[-3:] != "inx"}
            v_del_cols = {col for col in v_del_cols if col[-3:] != "inx"}
            v_put_raw_tbl = v_put_raw_tablename
            v_del_raw_tbl = v_del_raw_tablename
            s_put_vld_tbl = s_put_vld_tablename
            s_del_vld_tbl = s_del_vld_tablename
            v_put_raw_insert_sql = get_insert_sql(cursor, v_put_raw_tbl, v_put_cols)
            v_del_raw_insert_sql = get_insert_sql(cursor, v_del_raw_tbl, v_del_cols)
            s_put_vld_select_sql = get_select_sql(
                cursor, s_put_vld_tbl, s_put_cols, flat_bool=True
            )
            s_del_vld_select_sql = get_select_sql(
                cursor, s_del_vld_tbl, s_del_cols, flat_bool=True
            )
            v_put_raw_insert_select = f"{v_put_raw_insert_sql} {s_put_vld_select_sql}"
            v_del_raw_insert_select = f"{v_del_raw_insert_sql} {s_del_vld_select_sql}"
            # create_select_query(cursor=)
            abbv7 = get_dimen_abbv7(plan_dimen)
            put_sqlstr_ref = f"INSERT_{abbv7.upper()}_VOICE_RAW_PUT_SQLSTR"
            del_sqlstr_ref = f"INSERT_{abbv7.upper()}_VOICE_RAW_DEL_SQLSTR"
            print(f'{put_sqlstr_ref}= "{v_put_raw_insert_select}"')
            print(f'{del_sqlstr_ref}= "{v_del_raw_insert_select}"')
            # print(f"""'{v_put_raw_tablename}': {put_sqlstr_ref},""")
            # print(f"""'{v_del_raw_tablename}': {del_sqlstr_ref},""")
            assert insert_v_raw_sqlstrs.get(v_put_raw_tbl) == v_put_raw_insert_select
            assert insert_v_raw_sqlstrs.get(v_del_raw_tbl) == v_del_raw_insert_select


def test_get_insert_into_voice_raw_sqlstrs_ReturnsObj_VowDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    vow_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "vow"
    }

    # WHEN
    insert_v_raw_sqlstrs = get_insert_into_voice_raw_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        for vow_dimen in vow_dimens_config:
            # print(f"{vow_dimen=}")
            s_vld_tablename = prime_tbl(vow_dimen, "s", "vld")
            v_raw_tablename = prime_tbl(vow_dimen, "v", "raw")
            s_cols = get_table_columns(cursor, s_vld_tablename)
            v_raw_cols = get_table_columns(cursor, v_raw_tablename)
            v_raw_cols.remove("error_message")
            v_cols = find_set_otx_inx_args(v_raw_cols)
            v_cols = {col for col in v_cols if col[-3:] != "inx"}
            v_raw_tbl = v_raw_tablename
            s_vld_tbl = s_vld_tablename
            v_raw_insert_sql = get_insert_sql(cursor, v_raw_tbl, v_cols)
            s_vld_select_sql = get_select_sql(cursor, s_vld_tbl, s_cols, flat_bool=True)
            v_raw_insert_select = f"{v_raw_insert_sql} {s_vld_select_sql}"
            # create_select_query(cursor=)
            abbv7 = get_dimen_abbv7(vow_dimen)
            sqlstr_ref = f"INSERT_{abbv7.upper()}_VOICE_RAW_SQLSTR"
            print(f'{sqlstr_ref}= "{v_raw_insert_select}"')
            # print(f""""{v_raw_tablename}": {sqlstr_ref},""")
            assert insert_v_raw_sqlstrs.get(v_raw_tbl) == v_raw_insert_select
