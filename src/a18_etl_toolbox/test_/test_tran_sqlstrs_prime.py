from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    get_table_columns,
    create_update_inconsistency_error_query,
    create_table2table_agg_insert_query,
    create_insert_into_clause_str as get_insert_sql,
    create_select_query as get_select_sql,
)
from src.a06_bud_logic._utils.str_a06 import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_conceptunit_str,
    bud_concept_awardlink_str,
    bud_concept_reasonunit_str,
    bud_concept_reason_premiseunit_str,
    bud_concept_laborlink_str,
    bud_concept_healerlink_str,
    bud_concept_factunit_str,
    event_int_str,
    face_name_str,
)
from src.a08_bud_atom_logic.atom_config import get_bud_dimens, get_delete_key_name
from src.a15_fisc_logic._utils.str_a15 import (
    fiscunit_str,
    fisc_cashbook_str,
    fisc_dealunit_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    fisc_timeoffi_str,
)
from src.a15_fisc_logic.fisc_config import get_fisc_dimens
from src.a16_pidgin_logic.pidgin_config import get_pidgin_dimens, find_set_otx_inx_args
from src.a16_pidgin_logic._utils.str_a16 import (
    pidgin_title_str,
    pidgin_name_str,
    pidgin_way_str,
    pidgin_label_str,
    pidgin_core_str,
    otx_bridge_str,
    inx_bridge_str,
    unknown_term_str,
)
from src.a17_idea_logic._utils.str_a17 import idea_category_str, idea_number_str
from src.a17_idea_logic.idea_config import (
    get_idea_sqlite_types,
    get_idea_config_dict,
    get_default_sorted_list,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    ALL_DIMEN_ABBV7,
    get_dimen_abbv7,
    create_prime_tablename as prime_tbl,
    get_prime_create_table_sqlstrs,
    get_bud_voice_agg_tablenames,
    get_fisc_bud_sound_agg_tablenames,
    create_sound_and_voice_tables,
    create_sound_raw_update_inconsist_error_message_sqlstr,
    create_sound_agg_insert_sqlstrs,
    create_insert_into_pidgin_core_raw_sqlstr,
    create_insert_pidgin_core_agg_into_vld_sqlstr,
    create_insert_missing_face_name_into_pidgin_core_vld_sqlstr,
    create_insert_pidgin_sound_vld_table_sqlstr,
    get_insert_into_voice_raw_sqlstrs,
    get_insert_into_sound_vld_sqlstrs,
)
from sqlite3 import connect as sqlite3_connect


BUD_PRIME_TABLENAMES = {
    f"{bud_acct_membership_str()}_sound_put_agg": "BUDMEMB_PUT_AGG",
    f"{bud_acct_membership_str()}_sound_put_raw": "BUDMEMB_PUT_RAW",
    f"{bud_acctunit_str()}_sound_put_agg": "BUDACCT_PUT_AGG",
    f"{bud_acctunit_str()}_sound_put_raw": "BUDACCT_PUT_RAW",
    f"{bud_concept_awardlink_str()}_sound_put_agg": "BUDAWAR_PUT_AGG",
    f"{bud_concept_awardlink_str()}_sound_put_raw": "BUDAWAR_PUT_RAW",
    f"{bud_concept_factunit_str()}_sound_put_agg": "BUDFACT_PUT_AGG",
    f"{bud_concept_factunit_str()}_sound_put_raw": "BUDFACT_PUT_RAW",
    f"{bud_concept_healerlink_str()}_sound_put_agg": "BUDHEAL_PUT_AGG",
    f"{bud_concept_healerlink_str()}_sound_put_raw": "BUDHEAL_PUT_RAW",
    f"{bud_concept_reason_premiseunit_str()}_sound_put_agg": "BUDPREM_PUT_AGG",
    f"{bud_concept_reason_premiseunit_str()}_sound_put_raw": "BUDPREM_PUT_RAW",
    f"{bud_concept_reasonunit_str()}_sound_put_agg": "BUDREAS_PUT_AGG",
    f"{bud_concept_reasonunit_str()}_sound_put_raw": "BUDREAS_PUT_RAW",
    f"{bud_concept_laborlink_str()}_sound_put_agg": "BUDLABO_PUT_AGG",
    f"{bud_concept_laborlink_str()}_sound_put_raw": "BUDLABO_PUT_RAW",
    f"{bud_conceptunit_str()}_sound_put_agg": "BUDCONC_PUT_AGG",
    f"{bud_conceptunit_str()}_sound_put_raw": "BUDCONC_PUT_RAW",
    f"{budunit_str()}_sound_put_agg": "BUDUNIT_PUT_AGG",
    f"{budunit_str()}_sound_put_raw": "BUDUNIT_PUT_RAW",
    f"{bud_acct_membership_str()}_sound_del_agg": "BUDMEMB_DEL_AGG",
    f"{bud_acct_membership_str()}_sound_del_raw": "BUDMEMB_DEL_RAW",
    f"{bud_acctunit_str()}_sound_del_agg": "BUDACCT_DEL_AGG",
    f"{bud_acctunit_str()}_sound_del_raw": "BUDACCT_DEL_RAW",
    f"{bud_concept_awardlink_str()}_sound_del_agg": "BUDAWAR_DEL_AGG",
    f"{bud_concept_awardlink_str()}_sound_del_raw": "BUDAWAR_DEL_RAW",
    f"{bud_concept_factunit_str()}_sound_del_agg": "BUDFACT_DEL_AGG",
    f"{bud_concept_factunit_str()}_sound_del_raw": "BUDFACT_DEL_RAW",
    f"{bud_concept_healerlink_str()}_sound_del_agg": "BUDHEAL_DEL_AGG",
    f"{bud_concept_healerlink_str()}_sound_del_raw": "BUDHEAL_DEL_RAW",
    f"{bud_concept_reason_premiseunit_str()}_sound_del_agg": "BUDPREM_DEL_AGG",
    f"{bud_concept_reason_premiseunit_str()}_sound_del_raw": "BUDPREM_DEL_RAW",
    f"{bud_concept_reasonunit_str()}_sound_del_agg": "BUDREAS_DEL_AGG",
    f"{bud_concept_reasonunit_str()}_sound_del_raw": "BUDREAS_DEL_RAW",
    f"{bud_concept_laborlink_str()}_sound_del_agg": "BUDLABO_DEL_AGG",
    f"{bud_concept_laborlink_str()}_sound_del_raw": "BUDLABO_DEL_RAW",
    f"{bud_conceptunit_str()}_sound_del_agg": "BUDCONC_DEL_AGG",
    f"{bud_conceptunit_str()}_sound_del_raw": "BUDCONC_DEL_RAW",
    f"{budunit_str()}_sound_del_agg": "BUDUNIT_DEL_AGG",
    f"{budunit_str()}_sound_del_raw": "BUDUNIT_DEL_RAW",
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
            unknown_term_str(),
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


def create_fisc_sound_agg_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_fisc_sound_vld_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_pidgin_sound_vld_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.remove(otx_bridge_str())
    columns.remove(inx_bridge_str())
    columns.remove(unknown_term_str())
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


def create_fisc_voice_raw_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = find_set_otx_inx_args(columns)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_fisc_voice_agg_table_sqlstr(x_dimen: str):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.remove(event_int_str())
    columns.remove(face_name_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_bud_sound_put_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add(idea_number_str())
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_bud_sound_put_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_bud_sound_put_vld_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_bud_sound_del_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns.add(idea_number_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_bud_sound_del_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_bud_sound_del_vld_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_bud_voice_put_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw", "put")
    columns = set()
    columns = get_all_dimen_columns_set(x_dimen)
    columns = find_set_otx_inx_args(columns)
    columns.add("pidgin_event_int")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_bud_voice_put_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "agg", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_bud_voice_del_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns = find_set_otx_inx_args(columns)
    columns.add("pidgin_event_int")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_bud_voice_del_agg_table_sqlstr(x_dimen: str) -> str:
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


def test_get_prime_create_table_sqlstrs_ReturnsObj_CheckFiscDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    idea_config = get_idea_config_dict()
    fisc_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "fisc"
    }

    for x_dimen in fisc_dimens_config:
        # print(f"{abbv7} {x_dimen} checking...")
        s_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw")
        s_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
        s_vld_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
        v_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw")
        v_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "agg")
        expected_s_raw_sqlstr = create_pidgin_sound_raw_table_sqlstr(x_dimen)
        expected_s_agg_sqlstr = create_fisc_sound_agg_table_sqlstr(x_dimen)
        expected_s_vld_sqlstr = create_fisc_sound_vld_table_sqlstr(x_dimen)
        expected_v_raw_sqlstr = create_fisc_voice_raw_table_sqlstr(x_dimen)
        expected_v_agg_sqlstr = create_fisc_voice_agg_table_sqlstr(x_dimen)
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


def test_get_prime_create_table_sqlstrs_ReturnsObj_CheckBudDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    bud_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in get_idea_config_dict().items()
        if dimen_config.get(idea_category_str()) == "bud"
    }

    for x_dimen in bud_dimens_config:
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

        expected_s_put_raw_sqlstr = create_bud_sound_put_raw_table_sqlstr(x_dimen)
        expected_s_put_agg_sqlstr = create_bud_sound_put_agg_table_sqlstr(x_dimen)
        expected_s_put_vld_sqlstr = create_bud_sound_put_vld_table_sqlstr(x_dimen)
        expected_s_del_raw_sqlstr = create_bud_sound_del_raw_table_sqlstr(x_dimen)
        expected_s_del_agg_sqlstr = create_bud_sound_del_agg_table_sqlstr(x_dimen)
        expected_s_del_vld_sqlstr = create_bud_sound_del_vld_table_sqlstr(x_dimen)
        expected_v_put_raw_sqlstr = create_bud_voice_put_raw_table_sqlstr(x_dimen)
        expected_v_put_agg_sqlstr = create_bud_voice_put_agg_table_sqlstr(x_dimen)
        expected_v_del_raw_sqlstr = create_bud_voice_del_raw_table_sqlstr(x_dimen)
        expected_v_del_agg_sqlstr = create_bud_voice_del_agg_table_sqlstr(x_dimen)
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
    fisc_dimens_count = len(get_fisc_dimens()) * 5
    bud_dimens_count = len(get_bud_dimens()) * 10
    print(f"{pidgin_dimens_count=}")
    print(f"{fisc_dimens_count=}")
    print(f"{bud_dimens_count=}")
    all_dimens_count = pidgin_dimens_count + fisc_dimens_count + bud_dimens_count
    pidgin_core_count = 3
    all_dimens_count += pidgin_core_count
    assert len(create_table_sqlstrs) == all_dimens_count


def test_get_fisc_bud_sound_agg_tablenames_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    fisc_bud_sound_agg_tablenames = get_fisc_bud_sound_agg_tablenames()

    # THEN
    assert fisc_bud_sound_agg_tablenames
    expected_sound_agg_tablenames = set()
    for bud_dimen in get_bud_dimens():
        expected_sound_agg_tablenames.add(prime_tbl(bud_dimen, "s", "agg", "put"))
        expected_sound_agg_tablenames.add(prime_tbl(bud_dimen, "s", "agg", "del"))
    for fisc_dimen in get_fisc_dimens():
        expected_sound_agg_tablenames.add(prime_tbl(fisc_dimen, "s", "agg"))
    print(sorted(list(expected_sound_agg_tablenames)))
    assert expected_sound_agg_tablenames == fisc_bud_sound_agg_tablenames
    agg_tablenames = fisc_bud_sound_agg_tablenames
    assert len(agg_tablenames) == len(get_bud_dimens()) * 2 + len(get_fisc_dimens())
    assert agg_tablenames.issubset(set(get_prime_create_table_sqlstrs().keys()))


def test_get_bud_voice_agg_tablenames_ReturnsObj_BudDimens():
    # ESTABLISH / WHEN
    bud_voice_agg_tablenames = get_bud_voice_agg_tablenames()

    # THEN
    assert bud_voice_agg_tablenames
    expected_bud_voice_agg_tablenames = {
        prime_tbl(bud_dimen, "v", "agg", "put") for bud_dimen in get_bud_dimens()
    }
    print(f"{expected_bud_voice_agg_tablenames=}")
    assert expected_bud_voice_agg_tablenames == bud_voice_agg_tablenames
    assert len(bud_voice_agg_tablenames) == len(get_bud_dimens())
    agg_tablenames = bud_voice_agg_tablenames
    assert agg_tablenames.issubset(set(get_prime_create_table_sqlstrs().keys()))


def test_create_sound_and_voice_tables_CreatesFiscRawTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 0
        agg_str = "agg"
        raw_str = "raw"
        vld_str = "vld"
        put_str = "put"
        del_str = "del"
        budunit_s_put_agg_table = prime_tbl("budunit", "s", agg_str, put_str)
        budacct_s_put_agg_table = prime_tbl("budacct", "s", agg_str, put_str)
        budmemb_s_put_agg_table = prime_tbl("budmemb", "s", agg_str, put_str)
        budfact_s_del_agg_table = prime_tbl("budfact", "s", agg_str, del_str)
        budfact_s_del_vld_table = prime_tbl("budfact", "s", vld_str, del_str)
        fisunit_s_agg_table = prime_tbl("fisunit", "s", agg_str)
        fisunit_s_vld_table = prime_tbl("fisunit", "s", vld_str)
        pidtitl_s_agg_table = prime_tbl("pidtitl", "s", agg_str)
        fishour_v_agg_table = prime_tbl("fishour", "v", agg_str)
        pidtitl_s_raw_table = prime_tbl("pidtitl", "s", raw_str)
        pidcore_s_raw_table = prime_tbl("pidcore", "s", raw_str)
        pidcore_s_agg_table = prime_tbl("pidcore", "s", agg_str)
        pidcore_s_vld_table = prime_tbl("pidcore", "s", vld_str)

        assert not db_table_exists(cursor, budunit_s_put_agg_table)
        assert not db_table_exists(cursor, budacct_s_put_agg_table)
        assert not db_table_exists(cursor, budmemb_s_put_agg_table)
        assert not db_table_exists(cursor, budfact_s_del_agg_table)
        assert not db_table_exists(cursor, budfact_s_del_vld_table)
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
        assert db_table_exists(cursor, budunit_s_put_agg_table)
        assert db_table_exists(cursor, budacct_s_put_agg_table)
        assert db_table_exists(cursor, budmemb_s_put_agg_table)
        assert db_table_exists(cursor, budfact_s_del_agg_table)
        assert db_table_exists(cursor, budfact_s_del_vld_table)
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
    OR MIN(unknown_term) != MAX(unknown_term)
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


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario1_FiscDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = fisc_timeline_hour_str()
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
SELECT fisc_label, cumlative_minute
FROM fisc_timeline_hour_s_raw
GROUP BY fisc_label, cumlative_minute
HAVING MIN(hour_label) != MAX(hour_label)
)
UPDATE fisc_timeline_hour_s_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_label = fisc_timeline_hour_s_raw.fisc_label
    AND inconsistency_rows.cumlative_minute = fisc_timeline_hour_s_raw.cumlative_minute
;
"""
        # print(update_sqlstr)
        assert update_sqlstr == static_example_sqlstr


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario2_BudDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = bud_concept_awardlink_str()
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
SELECT event_int, face_name, fisc_label, owner_name, concept_way, awardee_title
FROM bud_concept_awardlink_s_put_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, awardee_title
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
)
UPDATE bud_concept_awardlink_s_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_concept_awardlink_s_put_raw.event_int
    AND inconsistency_rows.face_name = bud_concept_awardlink_s_put_raw.face_name
    AND inconsistency_rows.fisc_label = bud_concept_awardlink_s_put_raw.fisc_label
    AND inconsistency_rows.owner_name = bud_concept_awardlink_s_put_raw.owner_name
    AND inconsistency_rows.concept_way = bud_concept_awardlink_s_put_raw.concept_way
    AND inconsistency_rows.awardee_title = bud_concept_awardlink_s_put_raw.awardee_title
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

        static_example_sqlstr = """INSERT INTO pidgin_title_s_agg (event_int, face_name, otx_title, inx_title, otx_bridge, inx_bridge, unknown_term)
SELECT event_int, face_name, otx_title, MAX(inx_title), MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_term)
FROM pidgin_title_s_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, otx_title
;
"""
        print(update_sqlstrs[0])
        assert update_sqlstrs[0] == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario1_FiscDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = fisc_timeline_hour_str()
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

        static_example_sqlstr = """INSERT INTO fisc_timeline_hour_s_agg (event_int, face_name, fisc_label, cumlative_minute, hour_label)
SELECT event_int, face_name, fisc_label, cumlative_minute, MAX(hour_label)
FROM fisc_timeline_hour_s_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, cumlative_minute
;
"""
        print(update_sqlstrs[0])
        assert update_sqlstrs[0] == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario2_BudDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = bud_concept_awardlink_str()
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

        static_example_put_sqlstr = """INSERT INTO bud_concept_awardlink_s_put_agg (event_int, face_name, fisc_label, owner_name, concept_way, awardee_title, give_force, take_force)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, awardee_title, MAX(give_force), MAX(take_force)
FROM bud_concept_awardlink_s_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, awardee_title
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

        static_example_del_sqlstr = """INSERT INTO bud_concept_awardlink_s_del_agg (event_int, face_name, fisc_label, owner_name, concept_way, awardee_title_ERASE)
SELECT event_int, face_name, fisc_label, owner_name, concept_way, awardee_title_ERASE
FROM bud_concept_awardlink_s_del_raw
GROUP BY event_int, face_name, fisc_label, owner_name, concept_way, awardee_title_ERASE
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
    expected_sqlstr = f"""INSERT INTO {pidgin_core_s_raw_tablename} (source_dimen, face_name, otx_bridge, inx_bridge, unknown_term)
SELECT '{pidgin_s_agg_tablename}', face_name, otx_bridge, inx_bridge, unknown_term
FROM {pidgin_s_agg_tablename}
GROUP BY face_name, otx_bridge, inx_bridge, unknown_term
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
    expected_sqlstr = f"""INSERT INTO {pidgin_core_s_vld_tablename} (face_name, otx_bridge, inx_bridge, unknown_term)
SELECT
  face_name
, IFNULL(otx_bridge, '{default_bridge}')
, IFNULL(inx_bridge, '{default_bridge}')
, IFNULL(unknown_term, '{default_unknown_str}')
FROM {pidgin_core_s_agg_tablename}
;
"""
    print(expected_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_insert_missing_face_name_into_pidgin_core_vld_sqlstr_ReturnsObj():
    # ESTABLISH
    default_bridge = "|"
    default_unknown_str = "unknown2"
    budacct_s_agg_tablename = prime_tbl(bud_acctunit_str(), "s", "agg")

    # WHEN
    insert_sqlstr = create_insert_missing_face_name_into_pidgin_core_vld_sqlstr(
        default_bridge, default_unknown_str, budacct_s_agg_tablename
    )

    # THEN
    pidcore_dimen = "PIDCORE"
    pidgin_core_s_vld_tablename = prime_tbl(pidcore_dimen, "s", "vld")
    expected_sqlstr = f"""INSERT INTO {pidgin_core_s_vld_tablename} (face_name, otx_bridge, inx_bridge, unknown_term)
SELECT
  {budacct_s_agg_tablename}.face_name
, '{default_bridge}'
, '{default_bridge}'
, '{default_unknown_str}'
FROM {budacct_s_agg_tablename} 
LEFT JOIN pidgin_core_s_vld ON pidgin_core_s_vld.face_name = {budacct_s_agg_tablename}.face_name
WHERE pidgin_core_s_vld.face_name IS NULL
GROUP BY {budacct_s_agg_tablename}.face_name
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


def test_get_insert_into_sound_vld_sqlstrs_ReturnsObj_BudDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    bud_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "bud"
    }

    # WHEN
    insert_s_vld_sqlstrs = get_insert_into_sound_vld_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        for bud_dimen in bud_dimens_config:
            # print(f"{bud_dimen=}")
            s_put_agg_tablename = prime_tbl(bud_dimen, "s", "agg", "put")
            s_del_agg_tablename = prime_tbl(bud_dimen, "s", "agg", "del")
            s_put_vld_tablename = prime_tbl(bud_dimen, "s", "vld", "put")
            s_del_vld_tablename = prime_tbl(bud_dimen, "s", "vld", "del")
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
            abbv7 = get_dimen_abbv7(bud_dimen)
            put_sqlstr_ref = f"INSERT_{abbv7.upper()}_SOUND_VLD_PUT_SQLSTR"
            del_sqlstr_ref = f"INSERT_{abbv7.upper()}_SOUND_VLD_DEL_SQLSTR"
            print(f'{put_sqlstr_ref}= "{s_put_vld_insert_select}"')
            print(f'{del_sqlstr_ref}= "{s_del_vld_insert_select}"')
            # print(f"""'{s_put_vld_tablename}': {put_sqlstr_ref},""")
            # print(f"""'{s_del_vld_tablename}': {del_sqlstr_ref},""")
            assert insert_s_vld_sqlstrs.get(s_put_vld_tbl) == s_put_vld_insert_select
            assert insert_s_vld_sqlstrs.get(s_del_vld_tbl) == s_del_vld_insert_select


def test_get_insert_into_sound_vld_sqlstrs_ReturnsObj_FiscDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    fisc_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "fisc"
    }

    # WHEN
    insert_s_vld_sqlstrs = get_insert_into_sound_vld_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        for fisc_dimen in fisc_dimens_config:
            # print(f"{fisc_dimen=}")
            s_agg_tablename = prime_tbl(fisc_dimen, "s", "agg")
            s_vld_tablename = prime_tbl(fisc_dimen, "s", "vld")
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
            abbv7 = get_dimen_abbv7(fisc_dimen)
            sqlstr_ref = f"INSERT_{abbv7.upper()}_SOUND_VLD_SQLSTR"
            print(f'{sqlstr_ref}= "{s_vld_insert_select}"')
            # print(f""""{s_vld_tablename}": {sqlstr_ref},""")
            assert insert_s_vld_sqlstrs.get(s_vld_tbl) == s_vld_insert_select


def test_get_insert_into_voice_raw_sqlstrs_ReturnsObj_BudDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    bud_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "bud"
    }

    # WHEN
    insert_v_raw_sqlstrs = get_insert_into_voice_raw_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        for bud_dimen in bud_dimens_config:
            # print(f"{bud_dimen=}")
            s_put_vld_tablename = prime_tbl(bud_dimen, "s", "vld", "put")
            s_del_vld_tablename = prime_tbl(bud_dimen, "s", "vld", "del")
            v_put_raw_tablename = prime_tbl(bud_dimen, "v", "raw", "put")
            v_del_raw_tablename = prime_tbl(bud_dimen, "v", "raw", "del")
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
            abbv7 = get_dimen_abbv7(bud_dimen)
            put_sqlstr_ref = f"INSERT_{abbv7.upper()}_VOICE_RAW_PUT_SQLSTR"
            del_sqlstr_ref = f"INSERT_{abbv7.upper()}_VOICE_RAW_DEL_SQLSTR"
            print(f'{put_sqlstr_ref}= "{v_put_raw_insert_select}"')
            print(f'{del_sqlstr_ref}= "{v_del_raw_insert_select}"')
            # print(f"""'{v_put_raw_tablename}': {put_sqlstr_ref},""")
            # print(f"""'{v_del_raw_tablename}': {del_sqlstr_ref},""")
            assert insert_v_raw_sqlstrs.get(v_put_raw_tbl) == v_put_raw_insert_select
            assert insert_v_raw_sqlstrs.get(v_del_raw_tbl) == v_del_raw_insert_select


def test_get_insert_into_voice_raw_sqlstrs_ReturnsObj_FiscDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    fisc_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "fisc"
    }

    # WHEN
    insert_v_raw_sqlstrs = get_insert_into_voice_raw_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        for fisc_dimen in fisc_dimens_config:
            # print(f"{fisc_dimen=}")
            s_vld_tablename = prime_tbl(fisc_dimen, "s", "vld")
            v_raw_tablename = prime_tbl(fisc_dimen, "v", "raw")
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
            abbv7 = get_dimen_abbv7(fisc_dimen)
            sqlstr_ref = f"INSERT_{abbv7.upper()}_VOICE_RAW_SQLSTR"
            print(f'{sqlstr_ref}= "{v_raw_insert_select}"')
            # print(f""""{v_raw_tablename}": {sqlstr_ref},""")
            assert insert_v_raw_sqlstrs.get(v_raw_tbl) == v_raw_insert_select
