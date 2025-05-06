from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    get_create_table_sqlstr,
    create_update_inconsistency_error_query,
    create_table2table_agg_insert_query,
)
from src.a06_bud_logic._utils.str_a06 import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_itemunit_str,
    bud_item_awardlink_str,
    bud_item_reasonunit_str,
    bud_item_reason_premiseunit_str,
    bud_item_teamlink_str,
    bud_item_healerlink_str,
    bud_item_factunit_str,
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
from src.a16_pidgin_logic.pidgin_config import get_pidgin_dimens
from src.a16_pidgin_logic._utils.str_a16 import (
    pidgin_label_str,
    pidgin_name_str,
    pidgin_road_str,
    pidgin_tag_str,
    pidgin_core_str,
    otx_bridge_str,
    inx_bridge_str,
    unknown_word_str,
)
from src.a17_idea_logic._utils.str_a17 import idea_category_str, idea_number_str
from src.a17_idea_logic.idea_config import get_idea_sqlite_types, get_idea_config_dict
from src.a17_idea_logic.idea_db_tool import get_default_sorted_list
from src.a18_etl_toolbox.tran_sqlstrs import (
    ALL_DIMEN_ABBV7,
    get_dimen_abbv7,
    create_prime_tablename as prime_tbl,
    get_prime_create_table_sqlstrs,
    create_sound_and_voice_tables,
    create_sound_raw_update_inconsist_error_message_sqlstr,
    create_sound_agg_insert_sqlstrs,
    create_insert_into_pidgin_core_raw_sqlstr,
)
from sqlite3 import connect as sqlite3_connect


BUD_PRIME_TABLENAMES = {
    f"{bud_acct_membership_str()}_sound_put_agg": "BUDMEMB_PUT_AGG",
    f"{bud_acct_membership_str()}_sound_put_raw": "BUDMEMB_PUT_RAW",
    f"{bud_acctunit_str()}_sound_put_agg": "BUDACCT_PUT_AGG",
    f"{bud_acctunit_str()}_sound_put_raw": "BUDACCT_PUT_RAW",
    f"{bud_item_awardlink_str()}_sound_put_agg": "BUDAWAR_PUT_AGG",
    f"{bud_item_awardlink_str()}_sound_put_raw": "BUDAWAR_PUT_RAW",
    f"{bud_item_factunit_str()}_sound_put_agg": "BUDFACT_PUT_AGG",
    f"{bud_item_factunit_str()}_sound_put_raw": "BUDFACT_PUT_RAW",
    f"{bud_item_healerlink_str()}_sound_put_agg": "BUDHEAL_PUT_AGG",
    f"{bud_item_healerlink_str()}_sound_put_raw": "BUDHEAL_PUT_RAW",
    f"{bud_item_reason_premiseunit_str()}_sound_put_agg": "BUDPREM_PUT_AGG",
    f"{bud_item_reason_premiseunit_str()}_sound_put_raw": "BUDPREM_PUT_RAW",
    f"{bud_item_reasonunit_str()}_sound_put_agg": "BUDREAS_PUT_AGG",
    f"{bud_item_reasonunit_str()}_sound_put_raw": "BUDREAS_PUT_RAW",
    f"{bud_item_teamlink_str()}_sound_put_agg": "BUDTEAM_PUT_AGG",
    f"{bud_item_teamlink_str()}_sound_put_raw": "BUDTEAM_PUT_RAW",
    f"{bud_itemunit_str()}_sound_put_agg": "BUDITEM_PUT_AGG",
    f"{bud_itemunit_str()}_sound_put_raw": "BUDITEM_PUT_RAW",
    f"{budunit_str()}_sound_put_agg": "BUDUNIT_PUT_AGG",
    f"{budunit_str()}_sound_put_raw": "BUDUNIT_PUT_RAW",
    f"{bud_acct_membership_str()}_sound_del_agg": "BUDMEMB_DEL_AGG",
    f"{bud_acct_membership_str()}_sound_del_raw": "BUDMEMB_DEL_RAW",
    f"{bud_acctunit_str()}_sound_del_agg": "BUDACCT_DEL_AGG",
    f"{bud_acctunit_str()}_sound_del_raw": "BUDACCT_DEL_RAW",
    f"{bud_item_awardlink_str()}_sound_del_agg": "BUDAWAR_DEL_AGG",
    f"{bud_item_awardlink_str()}_sound_del_raw": "BUDAWAR_DEL_RAW",
    f"{bud_item_factunit_str()}_sound_del_agg": "BUDFACT_DEL_AGG",
    f"{bud_item_factunit_str()}_sound_del_raw": "BUDFACT_DEL_RAW",
    f"{bud_item_healerlink_str()}_sound_del_agg": "BUDHEAL_DEL_AGG",
    f"{bud_item_healerlink_str()}_sound_del_raw": "BUDHEAL_DEL_RAW",
    f"{bud_item_reason_premiseunit_str()}_sound_del_agg": "BUDPREM_DEL_AGG",
    f"{bud_item_reason_premiseunit_str()}_sound_del_raw": "BUDPREM_DEL_RAW",
    f"{bud_item_reasonunit_str()}_sound_del_agg": "BUDREAS_DEL_AGG",
    f"{bud_item_reasonunit_str()}_sound_del_raw": "BUDREAS_DEL_RAW",
    f"{bud_item_teamlink_str()}_sound_del_agg": "BUDTEAM_DEL_AGG",
    f"{bud_item_teamlink_str()}_sound_del_raw": "BUDTEAM_DEL_RAW",
    f"{bud_itemunit_str()}_sound_del_agg": "BUDITEM_DEL_AGG",
    f"{bud_itemunit_str()}_sound_del_raw": "BUDITEM_DEL_RAW",
    f"{budunit_str()}_sound_del_agg": "BUDUNIT_DEL_AGG",
    f"{budunit_str()}_sound_del_raw": "BUDUNIT_DEL_RAW",
}


def test_ALL_DIMEN_ABBV7_has_all_dimens():
    # ESTABLISH / WHEN / THEN
    assert len(ALL_DIMEN_ABBV7) == len(get_idea_config_dict())


def test_create_prime_tablename_ReturnsObj():
    # ESTABLISH
    budunit_dimen = budunit_str()
    budacct_dimen = bud_acctunit_str()
    budmemb_dimen = bud_acct_membership_str()
    buditem_dimen = bud_itemunit_str()
    budawar_dimen = bud_item_awardlink_str()
    budreas_dimen = bud_item_reasonunit_str()
    budprem_dimen = bud_item_reason_premiseunit_str()
    budteam_dimen = bud_item_teamlink_str()
    budheal_dimen = bud_item_healerlink_str()
    budfact_dimen = bud_item_factunit_str()
    fisunit_dimen = fiscunit_str()
    fiscash_dimen = fisc_cashbook_str()
    fisdeal_dimen = fisc_dealunit_str()
    fishour_dimen = fisc_timeline_hour_str()
    fismont_dimen = fisc_timeline_month_str()
    fisweek_dimen = fisc_timeline_weekday_str()
    fisoffi_dimen = fisc_timeoffi_str()
    pidname_dimen = pidgin_name_str()
    pidtagg_dimen = pidgin_tag_str()
    pidroad_dimen = pidgin_road_str()
    pidlabe_dimen = pidgin_label_str()
    raw_str = "raw"
    agg_str = "agg"
    put_str = "put"
    del_str = "del"

    # WHEN / THEN
    assert prime_tbl("budunit", "s", agg_str, put_str) == f"{budunit_dimen}_s_put_agg"
    assert prime_tbl("budacct", "s", agg_str, put_str) == f"{budacct_dimen}_s_put_agg"
    assert prime_tbl("budmemb", "s", agg_str, put_str) == f"{budmemb_dimen}_s_put_agg"
    assert prime_tbl("buditem", "s", agg_str, put_str) == f"{buditem_dimen}_s_put_agg"
    assert prime_tbl("budawar", "s", agg_str, put_str) == f"{budawar_dimen}_s_put_agg"
    assert prime_tbl("budreas", "s", agg_str, put_str) == f"{budreas_dimen}_s_put_agg"
    assert prime_tbl("budprem", "s", agg_str, put_str) == f"{budprem_dimen}_s_put_agg"
    assert prime_tbl("budteam", "s", agg_str, put_str) == f"{budteam_dimen}_s_put_agg"
    assert prime_tbl("budheal", "s", agg_str, put_str) == f"{budheal_dimen}_s_put_agg"
    assert prime_tbl("budfact", "s", agg_str, put_str) == f"{budfact_dimen}_s_put_agg"
    assert prime_tbl("budfact", "s", agg_str, del_str) == f"{budfact_dimen}_s_del_agg"
    assert prime_tbl("fisunit", "s", agg_str) == f"{fisunit_dimen}_s_agg"
    assert prime_tbl("fiscash", "s", agg_str) == f"{fiscash_dimen}_s_agg"
    assert prime_tbl("fisdeal", "s", agg_str) == f"{fisdeal_dimen}_s_agg"
    assert prime_tbl("fishour", "s", agg_str) == f"{fishour_dimen}_s_agg"
    assert prime_tbl("fismont", "s", agg_str) == f"{fismont_dimen}_s_agg"
    assert prime_tbl("fisweek", "s", agg_str) == f"{fisweek_dimen}_s_agg"
    assert prime_tbl("fisoffi", "s", agg_str) == f"{fisoffi_dimen}_s_agg"
    assert prime_tbl("pidname", "s", agg_str) == f"{pidname_dimen}_s_agg"
    assert prime_tbl("pidtagg", "s", agg_str) == f"{pidtagg_dimen}_s_agg"
    assert prime_tbl("pidroad", "s", agg_str) == f"{pidroad_dimen}_s_agg"
    assert prime_tbl("pidlabe", "s", agg_str) == f"{pidlabe_dimen}_s_agg"
    assert prime_tbl("pidlabe", "v", agg_str) == f"{pidlabe_dimen}_v_agg"
    assert prime_tbl("pidlabe", "s", raw_str) == f"{pidlabe_dimen}_s_raw"
    assert prime_tbl("pidlabe", "k", raw_str) == f"{pidlabe_dimen}_raw"
    assert prime_tbl("bud_acctunit", "k", raw_str) == "bud_acctunit_raw"


def create_agg_table_sqlstr(abbv7, sqlite_types) -> str:
    pass
    #  prime_tbl(abbv7, "s", "agg")


def get_all_dimen_columns_set(x_dimen: str) -> set[str]:
    if x_dimen == pidgin_core_str():
        return {
            event_int_str(),
            face_name_str(),
            otx_bridge_str(),
            inx_bridge_str(),
            unknown_word_str(),
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


def create_pf_sound_raw_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add(idea_number_str())
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_pf_sound_agg_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_pf_sound_vld_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
    columns = get_all_dimen_columns_set(x_dimen)
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


def create_fisc_voice_raw_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add("pidgin_event_int")
    columns.add("error_message")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_fisc_voice_agg_table_sqlstr(x_dimen):
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
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_bud_voice_put_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw", "put")
    columns = get_all_dimen_columns_set(x_dimen)
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
        expected_s_raw_sqlstr = create_pf_sound_raw_table_sqlstr(x_dimen)
        expected_s_agg_sqlstr = create_pf_sound_agg_table_sqlstr(x_dimen)
        expected_s_vld_sqlstr = create_pf_sound_vld_table_sqlstr(x_dimen)

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
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    pidgin_dimens_config = {pidgin_core_str(): {}}

    for x_dimen in pidgin_dimens_config:
        s_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw")
        s_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
        expected_s_raw_sqlstr = create_pidgin_core_raw_table_sqlstr(x_dimen)
        expected_s_agg_sqlstr = create_pidgin_core_agg_table_sqlstr(x_dimen)

        abbv7 = get_dimen_abbv7(x_dimen)
        print(f'CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR= """{expected_s_raw_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR= """{expected_s_agg_sqlstr}"""')

        # print(f'"{s_raw_tablename}": CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR,')
        # print(f'"{s_agg_tablename}": CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR,')
        assert expected_s_raw_sqlstr == create_table_sqlstrs.get(s_raw_tablename)
        assert expected_s_agg_sqlstr == create_table_sqlstrs.get(s_agg_tablename)


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
        v_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw")
        v_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "agg")
        expected_s_raw_sqlstr = create_pf_sound_raw_table_sqlstr(x_dimen)
        expected_s_agg_sqlstr = create_pf_sound_agg_table_sqlstr(x_dimen)
        expected_v_raw_sqlstr = create_fisc_voice_raw_table_sqlstr(x_dimen)
        expected_v_agg_sqlstr = create_fisc_voice_agg_table_sqlstr(x_dimen)
        abbv7 = get_dimen_abbv7(x_dimen)
        print(f'CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR= """{expected_s_raw_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR= """{expected_s_agg_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_VOICE_RAW_SQLSTR= """{expected_v_raw_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_VOICE_AGG_SQLSTR= """{expected_v_agg_sqlstr}"""')

        # print(f'"{s_raw_tablename}": CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR,')
        # print(f'"{s_agg_tablename}": CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR,')
        # print(f'"{v_raw_tablename}": CREATE_{abbv7.upper()}_VOICE_RAW_SQLSTR,')
        # print(f'"{v_agg_tablename}": CREATE_{abbv7.upper()}_VOICE_AGG_SQLSTR,')
        assert expected_s_raw_sqlstr == create_table_sqlstrs.get(s_raw_tablename)
        assert expected_s_agg_sqlstr == create_table_sqlstrs.get(s_agg_tablename)
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
        s_del_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw", "del")
        s_del_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg", "del")
        v_put_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw", "put")
        v_put_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "agg", "put")
        v_del_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "raw", "del")
        v_del_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "v", "agg", "del")

        expected_s_put_raw_sqlstr = create_bud_sound_put_raw_table_sqlstr(x_dimen)
        expected_s_put_agg_sqlstr = create_bud_sound_put_agg_table_sqlstr(x_dimen)
        expected_s_del_raw_sqlstr = create_bud_sound_del_raw_table_sqlstr(x_dimen)
        expected_s_del_agg_sqlstr = create_bud_sound_del_agg_table_sqlstr(x_dimen)
        expected_v_put_raw_sqlstr = create_bud_voice_put_raw_table_sqlstr(x_dimen)
        expected_v_put_agg_sqlstr = create_bud_voice_put_agg_table_sqlstr(x_dimen)
        expected_v_del_raw_sqlstr = create_bud_voice_del_raw_table_sqlstr(x_dimen)
        expected_v_del_agg_sqlstr = create_bud_voice_del_agg_table_sqlstr(x_dimen)
        abbv7 = get_dimen_abbv7(x_dimen)
        print(f'CREATE_{abbv7}_SOUND_PUT_RAW_STR= "{expected_s_put_raw_sqlstr}"')
        print(f'CREATE_{abbv7}_SOUND_PUT_AGG_STR= "{expected_s_put_agg_sqlstr}"')
        print(f'CREATE_{abbv7}_SOUND_DEL_RAW_STR= "{expected_s_del_raw_sqlstr}"')
        print(f'CREATE_{abbv7}_SOUND_DEL_AGG_STR= "{expected_s_del_agg_sqlstr}"')
        print(f'CREATE_{abbv7}_VOICE_PUT_RAW_STR= "{expected_v_put_raw_sqlstr}"')
        print(f'CREATE_{abbv7}_VOICE_PUT_AGG_STR= "{expected_v_put_agg_sqlstr}"')
        print(f'CREATE_{abbv7}_VOICE_DEL_RAW_STR= "{expected_v_del_raw_sqlstr}"')
        print(f'CREATE_{abbv7}_VOICE_DEL_AGG_STR= "{expected_v_del_agg_sqlstr}"')

        # print(f'"{s_put_raw_tablename}": CREATE_{abbv7}_SOUND_PUT_RAW_STR,')
        # print(f'"{s_put_agg_tablename}": CREATE_{abbv7}_SOUND_PUT_AGG_STR,')
        # print(f'"{s_del_raw_tablename}": CREATE_{abbv7}_SOUND_DEL_RAW_STR,')
        # print(f'"{s_del_agg_tablename}": CREATE_{abbv7}_SOUND_DEL_AGG_STR,')
        # print(f'"{v_put_raw_tablename}": CREATE_{abbv7}_VOICE_PUT_RAW_STR,')
        # print(f'"{v_put_agg_tablename}": CREATE_{abbv7}_VOICE_PUT_AGG_STR,')
        # print(f'"{v_del_raw_tablename}": CREATE_{abbv7}_VOICE_DEL_RAW_STR,')
        # print(f'"{v_del_agg_tablename}": CREATE_{abbv7}_VOICE_DEL_AGG_STR,')
        assert expected_s_put_raw_sqlstr == sqlstrs.get(s_put_raw_tablename)
        assert expected_s_put_agg_sqlstr == sqlstrs.get(s_put_agg_tablename)
        assert expected_s_del_raw_sqlstr == sqlstrs.get(s_del_raw_tablename)
        assert expected_s_del_agg_sqlstr == sqlstrs.get(s_del_agg_tablename)
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
    fisc_dimens_count = len(get_fisc_dimens()) * 4
    bud_dimens_count = len(get_bud_dimens()) * 8
    print(f"{pidgin_dimens_count=}")
    print(f"{fisc_dimens_count=}")
    print(f"{bud_dimens_count=}")
    all_dimens_count = pidgin_dimens_count + fisc_dimens_count + bud_dimens_count
    pidgin_core_count = 2
    all_dimens_count += pidgin_core_count
    assert len(create_table_sqlstrs) == all_dimens_count


def test_create_sound_and_voice_tables_CreatesFiscRawTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 0
        agg_str = "agg"
        raw_str = "raw"
        put_str = "put"
        del_str = "del"
        budunit_s_agg_table = prime_tbl("budunit", "s", agg_str, put_str)
        budacct_s_agg_table = prime_tbl("budacct", "s", agg_str, put_str)
        budmemb_s_agg_table = prime_tbl("budmemb", "s", agg_str, put_str)
        budfact_s_del_table = prime_tbl("budfact", "s", agg_str, del_str)
        fisunit_s_agg_table = prime_tbl("fisunit", "s", agg_str)
        pidlabe_s_agg_table = prime_tbl("pidlabe", "s", agg_str)
        fishour_v_agg_table = prime_tbl("fishour", "v", agg_str)
        pidlabe_s_raw_table = prime_tbl("pidlabe", "s", raw_str)
        pidcore_s_raw_table = prime_tbl("pidcore", "s", raw_str)
        pidcore_s_agg_table = prime_tbl("pidcore", "s", agg_str)

        assert not db_table_exists(cursor, budunit_s_agg_table)
        assert not db_table_exists(cursor, budacct_s_agg_table)
        assert not db_table_exists(cursor, budmemb_s_agg_table)
        assert not db_table_exists(cursor, budfact_s_del_table)
        assert not db_table_exists(cursor, fisunit_s_agg_table)
        assert not db_table_exists(cursor, pidlabe_s_agg_table)
        assert not db_table_exists(cursor, fishour_v_agg_table)
        assert not db_table_exists(cursor, pidlabe_s_raw_table)
        assert not db_table_exists(cursor, pidcore_s_raw_table)
        assert not db_table_exists(cursor, pidcore_s_agg_table)

        # WHEN
        create_sound_and_voice_tables(cursor)

        # THEN
        cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        # print(f"{cursor.fetchall()=}")
        # x_count = 0
        # for x_row in cursor.fetchall():
        #     print(f"{x_count} {x_row[1]=}")
        #     x_count += 1
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 122
        assert db_table_exists(cursor, budunit_s_agg_table)
        assert db_table_exists(cursor, budacct_s_agg_table)
        assert db_table_exists(cursor, budmemb_s_agg_table)
        assert db_table_exists(cursor, budfact_s_del_table)
        assert db_table_exists(cursor, fisunit_s_agg_table)
        assert db_table_exists(cursor, pidlabe_s_agg_table)
        assert db_table_exists(cursor, fishour_v_agg_table)
        assert db_table_exists(cursor, pidlabe_s_raw_table)
        assert db_table_exists(cursor, pidcore_s_raw_table)
        assert db_table_exists(cursor, pidcore_s_agg_table)


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario0_PidginDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = pidgin_label_str()
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
SELECT event_int, face_name, otx_label
FROM pidgin_label_s_raw
GROUP BY event_int, face_name, otx_label
HAVING MIN(inx_label) != MAX(inx_label)
    OR MIN(otx_bridge) != MAX(otx_bridge)
    OR MIN(inx_bridge) != MAX(inx_bridge)
    OR MIN(unknown_word) != MAX(unknown_word)
)
UPDATE pidgin_label_s_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = pidgin_label_s_raw.event_int
    AND inconsistency_rows.face_name = pidgin_label_s_raw.face_name
    AND inconsistency_rows.otx_label = pidgin_label_s_raw.otx_label
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
SELECT fisc_tag, cumlative_minute
FROM fisc_timeline_hour_s_raw
GROUP BY fisc_tag, cumlative_minute
HAVING MIN(hour_tag) != MAX(hour_tag)
)
UPDATE fisc_timeline_hour_s_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.fisc_tag = fisc_timeline_hour_s_raw.fisc_tag
    AND inconsistency_rows.cumlative_minute = fisc_timeline_hour_s_raw.cumlative_minute
;
"""
        # print(update_sqlstr)
        assert update_sqlstr == static_example_sqlstr


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario2_BudDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = bud_item_awardlink_str()
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
SELECT event_int, face_name, fisc_tag, owner_name, road, awardee_title
FROM bud_item_awardlink_s_put_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, awardee_title
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
)
UPDATE bud_item_awardlink_s_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = bud_item_awardlink_s_put_raw.event_int
    AND inconsistency_rows.face_name = bud_item_awardlink_s_put_raw.face_name
    AND inconsistency_rows.fisc_tag = bud_item_awardlink_s_put_raw.fisc_tag
    AND inconsistency_rows.owner_name = bud_item_awardlink_s_put_raw.owner_name
    AND inconsistency_rows.road = bud_item_awardlink_s_put_raw.road
    AND inconsistency_rows.awardee_title = bud_item_awardlink_s_put_raw.awardee_title
;
"""
        # print(update_sqlstr)
        assert update_sqlstr == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario0_PidginDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = pidgin_label_str()
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

        static_example_sqlstr = """INSERT INTO pidgin_label_s_agg (event_int, face_name, otx_label, inx_label, otx_bridge, inx_bridge, unknown_word)
SELECT event_int, face_name, otx_label, MAX(inx_label), MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_word)
FROM pidgin_label_s_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, otx_label
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
        dimen_focus_columns.remove("event_int")
        dimen_focus_columns.remove("face_name")
        dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
        exclude_cols = {
            idea_number_str(),
            event_int_str(),
            face_name_str(),
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

        static_example_sqlstr = """INSERT INTO fisc_timeline_hour_s_agg (fisc_tag, cumlative_minute, hour_tag)
SELECT fisc_tag, cumlative_minute, MAX(hour_tag)
FROM fisc_timeline_hour_s_raw
WHERE error_message IS NULL
GROUP BY fisc_tag, cumlative_minute
;
"""
        print(update_sqlstrs[0])
        assert update_sqlstrs[0] == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario2_BudDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = bud_item_awardlink_str()
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

        static_example_put_sqlstr = """INSERT INTO bud_item_awardlink_s_put_agg (event_int, face_name, fisc_tag, owner_name, road, awardee_title, give_force, take_force)
SELECT event_int, face_name, fisc_tag, owner_name, road, awardee_title, MAX(give_force), MAX(take_force)
FROM bud_item_awardlink_s_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, fisc_tag, owner_name, road, awardee_title
;
"""
        # print(update_sqlstrs[0])
        assert update_sqlstrs[0] == static_example_put_sqlstr

        # del
        del_raw_tablename = prime_tbl(dimen, "s", "raw", "del")
        del_agg_tablename = prime_tbl(dimen, "s", "agg", "del")
        del_exclude_cols = {idea_number_str(), "error_message"}
        del_expected_insert_sqlstr = create_table2table_agg_insert_query(
            cursor,
            src_table=del_raw_tablename,
            dst_table=del_agg_tablename,
            focus_cols=None,
            exclude_cols=del_exclude_cols,
            where_block="",
        )
        print(del_expected_insert_sqlstr)
        assert update_sqlstrs[1] == del_expected_insert_sqlstr

        static_example_del_sqlstr = """INSERT INTO bud_item_awardlink_s_del_agg (event_int, face_name, fisc_tag, owner_name, road, awardee_title_ERASE)
SELECT event_int, face_name, fisc_tag, owner_name, road, awardee_title_ERASE
FROM bud_item_awardlink_s_del_raw
GROUP BY event_int, face_name, fisc_tag, owner_name, road, awardee_title_ERASE
;
"""
        print(update_sqlstrs[1])
        assert update_sqlstrs[1] == static_example_del_sqlstr


def test_create_insert_into_pidgin_core_raw_sqlstr_ReturnsObj():
    # ESTABLISH
    dimen = pidgin_road_str()
    # WHEN
    road_sqlstr = create_insert_into_pidgin_core_raw_sqlstr(dimen)

    # THEN
    pidgin_s_agg_tablename = prime_tbl(dimen, "s", "agg")
    expected_road_sqlstr = f"""INSERT INTO pidgin_core_s_raw (source_dimen, face_name, otx_bridge, inx_bridge, unknown_word)
SELECT '{pidgin_s_agg_tablename}', face_name, MAX(otx_bridge), MAX(inx_bridge), MAX(unknown_word)
FROM {pidgin_s_agg_tablename}
GROUP BY face_name
"""
    assert road_sqlstr == expected_road_sqlstr
