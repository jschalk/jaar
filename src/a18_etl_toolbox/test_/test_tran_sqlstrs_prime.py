from src.a00_data_toolbox.db_toolbox import (
    db_table_exists,
    create_select_inconsistency_query,
    create_update_inconsistency_error_query,
    get_create_table_sqlstr,
    create_table2table_agg_insert_query,
    get_table_columns,
    required_columns_exist,
    create_select_query,
    get_db_tables,
)
from src.a02_finance_logic._utils.strs_a02 import (
    fisc_tag_str,
    owner_name_str,
    deal_time_str,
    tran_time_str,
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
from src.a07_calendar_logic._utils.str_a07 import (
    c400_number_str,
    monthday_distortion_str,
    timeline_tag_str,
    yr1_jan1_offset_str,
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
)
from src.a17_idea_logic._utils.str_a17 import idea_category_str, idea_number_str
from src.a17_idea_logic.idea_config import (
    get_idea_sqlite_types,
    get_idea_config_dict,
    get_idea_numbers,
)
from src.a17_idea_logic.idea_db_tool import (
    get_pragma_table_fetchall,
    get_default_sorted_list,
    get_idea_into_dimen_raw_query,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    ALL_DIMEN_ABBV7,
    get_dimen_abbv7,
    create_prime_tablename as prime_tbl,
    get_prime_create_table_sqlstrs,
    create_sound_and_voice_tables,
    get_pidgin_update_inconsist_error_message_sqlstrs,
    get_sound_pidgin_update_inconsist_error_message_sqlstrs,
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


def create_agg_table_sqlstr(abbv7, sqlite_types) -> str:
    pass
    #  prime_tbl(abbv7, "s", "agg")


def get_all_dimen_columns_set(x_dimen: str) -> set[str]:
    x_config = get_idea_config_dict().get(x_dimen)
    columns = set(x_config.get("jkeys").keys())
    columns.update(set(x_config.get("jvalues").keys()))
    return columns


def get_del_dimen_columns_set(x_dimen: str) -> list[str]:
    x_config = get_idea_config_dict().get(x_dimen)
    columns_set = set(x_config.get("jkeys").keys())
    columns_set.update(set(x_config.get("jvalues").keys()))
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
    columns.add("pidgin_event_int")
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
        expected_s_raw_sqlstr = create_pf_sound_raw_table_sqlstr(x_dimen)
        expected_s_agg_sqlstr = create_pf_sound_agg_table_sqlstr(x_dimen)

        abbv7 = get_dimen_abbv7(x_dimen)
        # print(f'CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR= """{expected_s_raw_sqlstr}"""')
        # print(f'CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR= """{expected_s_agg_sqlstr}"""')

        print(f'"{s_raw_tablename}": CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR,')
        print(f'"{s_agg_tablename}": CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR,')
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
    pidgin_dimens_count = len(get_pidgin_dimens()) * 2
    fisc_dimens_count = len(get_fisc_dimens()) * 4
    bud_dimens_count = len(get_bud_dimens()) * 8
    print(f"{pidgin_dimens_count=}")
    print(f"{fisc_dimens_count=}")
    print(f"{bud_dimens_count=}")
    all_dimens_count = pidgin_dimens_count + fisc_dimens_count + bud_dimens_count
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

        assert not db_table_exists(cursor, budunit_s_agg_table)
        assert not db_table_exists(cursor, budacct_s_agg_table)
        assert not db_table_exists(cursor, budmemb_s_agg_table)
        assert not db_table_exists(cursor, budfact_s_del_table)
        assert not db_table_exists(cursor, fisunit_s_agg_table)
        assert not db_table_exists(cursor, pidlabe_s_agg_table)
        assert not db_table_exists(cursor, fishour_v_agg_table)
        assert not db_table_exists(cursor, pidlabe_s_raw_table)

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
        assert cursor.fetchone()[0] == 116
        assert db_table_exists(cursor, budunit_s_agg_table)
        assert db_table_exists(cursor, budacct_s_agg_table)
        assert db_table_exists(cursor, budmemb_s_agg_table)
        assert db_table_exists(cursor, budfact_s_del_table)
        assert db_table_exists(cursor, fisunit_s_agg_table)
        assert db_table_exists(cursor, pidlabe_s_agg_table)
        assert db_table_exists(cursor, fishour_v_agg_table)
        assert db_table_exists(cursor, pidlabe_s_raw_table)


def test_get_sound_pidgin_update_inconsist_error_message_sqlstrs_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    sound_pidgin_sqlstrs = get_sound_pidgin_update_inconsist_error_message_sqlstrs()

    # THEN
    assert set(sound_pidgin_sqlstrs.keys()) == get_pidgin_dimens()
    idea_config = get_idea_config_dict()
    idea_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "pidgin"
    }

    exclude_cols = {
        idea_number_str(),
        event_int_str(),
        face_name_str(),
        "error_message",
    }
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_voice_tables(cursor)

        for x_dimen in idea_config:
            # for db_table in get_db_tables(conn):
            #     # if db_table.find(x_dimen) > 0:
            #     print(f"{db_table=}")

            # print(f"{x_dimen} checking...")
            x_sqlstr = sound_pidgin_sqlstrs.get(x_dimen)
            abbv7 = get_dimen_abbv7(x_dimen)
            x_tablename = prime_tbl(abbv7, "s", "raw")
            dimen_config = idea_config.get(x_dimen)
            dimen_focus_columns = set(dimen_config.get("jkeys").keys())
            generated_dimen_sqlstr = create_update_inconsistency_error_query(
                cursor, x_tablename, dimen_focus_columns, exclude_cols
            )
            # print(
            #     f"""{x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = \"\"\"{generated_dimen_sqlstr}\"\"\""""
            # )
            # print(
            #     f"""\"{x_dimen}\": {x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,"""
            # )
            print(generated_dimen_sqlstr)
            print(f"""            {x_sqlstr=}""")
            assert x_sqlstr == generated_dimen_sqlstr


# def test_get_fisc_inconsistency_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     fisc_inconsistency_sqlstrs = get_fisc_inconsistency_sqlstrs()

#     # THEN
#     assert fisc_inconsistency_sqlstrs.keys() == get_fisc_dimens()
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         # if dimen_config.get(idea_category_str()) != "pidgin"
#         # if dimen_config.get(idea_category_str()) == "bud"
#         if dimen_config.get(idea_category_str()) == "fisc"
#     }

#     exclude_cols = {
#         idea_number_str(),
#         event_int_str(),
#         face_name_str(),
#         "error_message",
#     }
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_fisc_prime_tables(cursor)

#         for x_dimen in sorted(idea_config):
#             # print(f"{x_dimen} checking...")
#             x_sqlstr = fisc_inconsistency_sqlstrs.get(x_dimen)
#             x_tablename = f"{x_dimen}_raw"
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             generated_dimen_sqlstr = create_select_inconsistency_query(
#                 cursor, x_tablename, dimen_focus_columns, exclude_cols
#             )
#             print(f'{x_dimen}_INCONSISTENCY_SQLSTR ="""{generated_dimen_sqlstr}"""')
#             print(f'{x_sqlstr=}"""')
#             assert x_sqlstr == generated_dimen_sqlstr


# def test_get_bud_inconsistency_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     bud_inconsistency_sqlstrs = get_bud_inconsistency_sqlstrs()

#     # THEN
#     assert bud_inconsistency_sqlstrs.keys() == get_bud_dimens()
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "bud"
#     }

#     exclude_cols = {idea_number_str(), "error_message"}
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_bud_prime_tables(cursor)

#         for x_dimen in sorted(idea_config):
#             # print(f"{x_dimen} checking...")
#             x_sqlstr = bud_inconsistency_sqlstrs.get(x_dimen)
#             x_tablename = f"{x_dimen}_put_raw"
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             generated_dimen_sqlstr = create_select_inconsistency_query(
#                 cursor, x_tablename, dimen_focus_columns, exclude_cols
#             )
#             print(
#                 f'{x_dimen.upper()}_INCONSISTENCY_SQLSTR ="""{generated_dimen_sqlstr}"""'
#             )
#             assert x_sqlstr == generated_dimen_sqlstr


# def test_get_fisc_update_inconsist_error_message_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     fisc_update_error_sqlstrs = get_fisc_update_inconsist_error_message_sqlstrs()

#     # THEN
#     assert set(fisc_update_error_sqlstrs.keys()) == get_fisc_dimens()
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "fisc"
#     }

#     exclude_cols = {
#         idea_number_str(),
#         event_int_str(),
#         face_name_str(),
#         "error_message",
#     }
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_fisc_prime_tables(cursor)
#         create_bud_prime_tables(cursor)

#         for x_dimen in idea_config:
#             print(f"{x_dimen} checking...")
#             x_sqlstr = fisc_update_error_sqlstrs.get(x_dimen)
#             x_tablename = f"{x_dimen}_raw"
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             generated_dimen_sqlstr = create_update_inconsistency_error_query(
#                 cursor, x_tablename, dimen_focus_columns, exclude_cols
#             )
#             # print(
#             #     f"""{x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = \"\"\"{generated_dimen_sqlstr}\"\"\""""
#             # )
#             # print(
#             #     f"""\"{x_dimen}\": {x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,"""
#             # )
#             # print(f"""            {x_sqlstr=}""")
#             assert x_sqlstr == generated_dimen_sqlstr


# def test_get_pidgin_update_inconsist_error_message_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     pidgin_update_error_sqlstrs = get_pidgin_update_inconsist_error_message_sqlstrs()

#     # THEN
#     assert set(pidgin_update_error_sqlstrs.keys()) == get_pidgin_dimens()
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "pidgin"
#     }

#     exclude_cols = {
#         idea_number_str(),
#         event_int_str(),
#         face_name_str(),
#         "error_message",
#     }
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_pidgin_prime_tables(cursor)

#         for x_dimen in idea_config:
#             # print(f"{x_dimen} checking...")
#             x_sqlstr = pidgin_update_error_sqlstrs.get(x_dimen)
#             x_tablename = f"{x_dimen}_raw"
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             generated_dimen_sqlstr = create_update_inconsistency_error_query(
#                 cursor, x_tablename, dimen_focus_columns, exclude_cols
#             )
#             # print(
#             #     f"""{x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = \"\"\"{generated_dimen_sqlstr}\"\"\""""
#             # )
#             # print(
#             #     f"""\"{x_dimen}\": {x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,"""
#             # )
#             # print(f"""            {x_sqlstr=}""")
#             assert x_sqlstr == generated_dimen_sqlstr


# def test_get_bud_put_update_inconsist_error_message_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     bud_update_error_sqlstrs = get_bud_put_update_inconsist_error_message_sqlstrs()

#     # THEN
#     assert set(bud_update_error_sqlstrs.keys()) == get_bud_dimens()
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "bud"
#     }

#     exclude_cols = {idea_number_str(), "error_message"}
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_bud_prime_tables(cursor)

#         for x_dimen in idea_config:
#             # print(f"{x_dimen} checking...")
#             x_sqlstr = bud_update_error_sqlstrs.get(x_dimen)
#             x_tablename = f"{x_dimen}_put_raw"
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             generated_dimen_sqlstr = create_update_inconsistency_error_query(
#                 cursor, x_tablename, dimen_focus_columns, exclude_cols
#             )
#             abbv7 = get_dimen_abbv7(x_dimen)
#             print(
#                 f"""{abbv7.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR = \"\"\"{generated_dimen_sqlstr}\"\"\""""
#             )
#             # print(
#             #     f"""\"{x_dimen}\": {x_dimen.upper()}_SET_INCONSISTENCY_ERROR_MESSAGE_SQLSTR,"""
#             # )
#             # print(f"""            {x_sqlstr=}""")
#             assert x_sqlstr == generated_dimen_sqlstr


# def test_get_fisc_insert_agg_from_raw_sqlstrs_ReturnsObj():
#     # sourcery skip: extract-method, no-loop-in-tests
#     # ESTABLISH / WHEN
#     fisc_insert_agg_sqlstrs = get_fisc_insert_agg_from_raw_sqlstrs()

#     # THEN
#     assert set(fisc_insert_agg_sqlstrs.keys()) == get_fisc_dimens()
#     x_exclude_cols = {
#         idea_number_str(),
#         event_int_str(),
#         face_name_str(),
#         "error_message",
#     }
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "fisc"
#     }
#     with sqlite3_connect(":memory:") as fisc_db_conn:
#         cursor = fisc_db_conn.cursor()
#         create_fisc_prime_tables(cursor)

#         for x_dimen in idea_config:
#             print(f"{x_dimen} checking...")
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             dimen_focus_columns.remove(event_int_str())
#             dimen_focus_columns.remove(face_name_str())
#             dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
#             raw_tablename = f"{x_dimen}_raw"
#             agg_tablename = f"{x_dimen}_agg"

#             expected_table2table_agg_insert_sqlstr = (
#                 create_table2table_agg_insert_query(
#                     cursor,
#                     src_table=raw_tablename,
#                     dst_table=agg_tablename,
#                     focus_cols=dimen_focus_columns,
#                     exclude_cols=x_exclude_cols,
#                 )
#             )
#             x_sqlstr = fisc_insert_agg_sqlstrs.get(x_dimen)
#             # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
#             # print(
#             #     f'{x_dimen.upper()}_AGG_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
#             # )
#             assert x_sqlstr == expected_table2table_agg_insert_sqlstr

#         generated_fiscunit_sqlstr = create_table2table_agg_insert_query(
#             cursor,
#             src_table=f"{fiscunit_str()}_raw",
#             dst_table=f"{fiscunit_str()}_agg",
#             focus_cols=[fisc_tag_str()],
#             exclude_cols=x_exclude_cols,
#         )
#         assert FISUNIT_AGG_INSERT_SQLSTR == generated_fiscunit_sqlstr
#         columns_header = f"""{fisc_tag_str()}, {timeline_tag_str()}, {c400_number_str()}, {yr1_jan1_offset_str()}, {monthday_distortion_str()}, fund_coin, penny, respect_bit, bridge, job_listen_rotations"""
#         tablename = "fiscunit"
#         expected_fiscunit_sqlstr = f"""INSERT INTO {tablename}_agg ({columns_header})
# SELECT {fisc_tag_str()}, MAX({timeline_tag_str()}), MAX({c400_number_str()}), MAX({yr1_jan1_offset_str()}), MAX({monthday_distortion_str()}), MAX(fund_coin), MAX(penny), MAX(respect_bit), MAX(bridge), MAX(job_listen_rotations)
# FROM {tablename}_raw
# WHERE error_message IS NULL
# GROUP BY {fisc_tag_str()}
# ;
# """
#         assert FISUNIT_AGG_INSERT_SQLSTR == expected_fiscunit_sqlstr

#     assert len(idea_config) == len(fisc_insert_agg_sqlstrs)


# def test_get_pidgin_insert_agg_from_raw_sqlstrs_ReturnsObj():
#     # sourcery skip: extract-method, no-loop-in-tests
#     # ESTABLISH / WHEN
#     pidgin_insert_agg_sqlstrs = get_pidgin_insert_agg_from_raw_sqlstrs()

#     # THEN
#     assert set(pidgin_insert_agg_sqlstrs.keys()) == get_pidgin_dimens()
#     x_exclude_cols = {
#         idea_number_str(),
#         event_int_str(),
#         face_name_str(),
#         "error_message",
#     }
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "pidgin"
#     }
#     with sqlite3_connect(":memory:") as db_conn:
#         cursor = db_conn.cursor()
#         create_pidgin_prime_tables(cursor)

#         for x_dimen in idea_config:
#             # print(f"{x_dimen} checking...")
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             dimen_focus_columns.remove(event_int_str())
#             dimen_focus_columns.remove(face_name_str())
#             dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
#             raw_tablename = f"{x_dimen}_raw"
#             agg_tablename = f"{x_dimen}_agg"

#             expected_table2table_agg_insert_sqlstr = (
#                 create_table2table_agg_insert_query(
#                     cursor,
#                     src_table=raw_tablename,
#                     dst_table=agg_tablename,
#                     focus_cols=dimen_focus_columns,
#                     exclude_cols=x_exclude_cols,
#                 )
#             )
#             x_sqlstr = pidgin_insert_agg_sqlstrs.get(x_dimen)
#             # print(f'"{x_dimen}": {x_dimen.upper()}_AGG_INSERT_SQLSTR,')
#             # print(
#             #     f'{x_dimen.upper()}_AGG_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
#             # )
#             assert x_sqlstr == expected_table2table_agg_insert_sqlstr

#     assert len(idea_config) == len(pidgin_insert_agg_sqlstrs)


# def test_get_bud_insert_put_agg_from_raw_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     bud_insert_agg_sqlstrs = get_bud_insert_put_agg_from_raw_sqlstrs()

#     # THEN
#     assert set(bud_insert_agg_sqlstrs.keys()) == get_bud_dimens()
#     x_exclude_cols = {
#         idea_number_str(),
#         "error_message",
#     }
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "bud"
#     }
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_bud_prime_tables(cursor)

#         for x_dimen in idea_config:
#             print(f"{x_dimen} checking...")
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
#             raw_tablename = f"{x_dimen}_put_raw"
#             agg_tablename = f"{x_dimen}_put_agg"

#             expected_table2table_agg_insert_sqlstr = (
#                 create_table2table_agg_insert_query(
#                     cursor,
#                     src_table=raw_tablename,
#                     dst_table=agg_tablename,
#                     focus_cols=dimen_focus_columns,
#                     exclude_cols=x_exclude_cols,
#                 )
#             )
#             x_sqlstr = bud_insert_agg_sqlstrs.get(x_dimen)
#             # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
#             # print(
#             #     f'{x_dimen.upper()}_AGG_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
#             # )
#             assert x_sqlstr == expected_table2table_agg_insert_sqlstr


# def test_get_bud_insert_del_agg_from_raw_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     bud_insert_agg_sqlstrs = get_bud_insert_del_agg_from_raw_sqlstrs()

#     # THEN
#     assert set(bud_insert_agg_sqlstrs.keys()) == get_bud_dimens()
#     x_exclude_cols = {
#         idea_number_str(),
#         "error_message",
#     }
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) == "bud"
#     }
#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_bud_prime_tables(cursor)

#         for x_dimen in idea_config:
#             # print(f"{x_dimen} checking...")
#             dimen_config = idea_config.get(x_dimen)
#             dimen_focus_columns = set(dimen_config.get("jkeys").keys())
#             dimen_focus_columns = get_default_sorted_list(dimen_focus_columns)
#             dimen_focus_columns[-1] = get_delete_key_name(dimen_focus_columns[-1])
#             raw_tablename = f"{x_dimen}_del_raw"
#             agg_tablename = f"{x_dimen}_del_agg"

#             expected_table2table_agg_insert_sqlstr = (
#                 create_table2table_agg_insert_query(
#                     cursor,
#                     src_table=raw_tablename,
#                     dst_table=agg_tablename,
#                     focus_cols=dimen_focus_columns,
#                     exclude_cols=x_exclude_cols,
#                 )
#             )
#             x_sqlstr = bud_insert_agg_sqlstrs.get(x_dimen)
#             # print(f'"{x_dimen}": BUD_AGG_INSERT_SQLSTR,')
#             # print(
#             #     f'{abbv(agg_tablename)}_INSERT_SQLSTR = """{expected_table2table_agg_insert_sqlstr}"""'
#             # )
#             assert x_sqlstr == expected_table2table_agg_insert_sqlstr


# def test_get_idea_stageble_put_dimens_HasAll_idea_numbersForAll_dimens():
#     # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
#     # ESTABLISH / WHEN
#     # THEN
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) != "pidgin"
#         # if dimen_config.get(idea_category_str()) == "fisc"
#     }
#     with sqlite3_connect(":memory:") as fisc_db_conn:
#         cursor = fisc_db_conn.cursor()
#         create_all_idea_tables(cursor)
#         create_fisc_prime_tables(cursor)
#         create_bud_prime_tables(cursor)

#         idea_raw2dimen_count = 0
#         idea_dimen_combo_checked_count = 0
#         sorted_idea_numbers = sorted(get_idea_numbers())
#         expected_idea_stagable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
#         for x_dimen in sorted(idea_config):
#             dimen_config = idea_config.get(x_dimen)
#             dimen_key_columns = set(dimen_config.get("jkeys").keys())
#             dimen_value_columns = set(dimen_config.get("jvalues").keys())
#             for idea_number in sorted_idea_numbers:
#                 src_columns = get_table_columns(cursor, f"{idea_number}_raw")
#                 expected_stagable = dimen_key_columns.issubset(src_columns)
#                 if idea_number == "br00050":
#                     print(f"{x_dimen} {idea_number} checking... {src_columns}")
#                 src_tablename = f"{idea_number}_raw"
#                 gen_stablable = required_columns_exist(
#                     cursor, src_tablename, dimen_key_columns
#                 )
#                 assert expected_stagable == gen_stablable

#                 idea_dimen_combo_checked_count += 1
#                 if required_columns_exist(cursor, src_tablename, dimen_key_columns):
#                     expected_idea_stagable_dimens.get(idea_number).append(x_dimen)
#                     idea_raw2dimen_count += 1
#                     src_cols_set = set(src_columns)
#                     existing_value_col = src_cols_set.intersection(dimen_value_columns)
#                     # print(
#                     #     f"{x_dimen} {idea_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
#                     # )
#                     # print(
#                     #     f"{idea_raw2dimen_count} {idea_number} {x_dimen} keys:{dimen_key_columns}, values: {existing_value_col}"
#                     # )
#                     generated_sqlstr = get_idea_into_dimen_raw_query(
#                         conn_or_cursor=cursor,
#                         idea_number=idea_number,
#                         x_dimen=x_dimen,
#                         x_jkeys=dimen_key_columns,
#                     )
#                     # check sqlstr is correct?
#                     assert generated_sqlstr != ""

#     idea_stageble_dimen_list = sorted(list(expected_idea_stagable_dimens))
#     print(f"{expected_idea_stagable_dimens=}")
#     assert idea_dimen_combo_checked_count == 680
#     assert idea_raw2dimen_count == 100
#     assert get_idea_stageble_put_dimens() == expected_idea_stagable_dimens


# def test_IDEA_STAGEBLE_DEL_DIMENS_HasAll_idea_numbersForAll_dimens():
#     # sourcery skip: extract-method, no-loop-in-tests, no-conditionals-in-tests
#     # ESTABLISH / WHEN
#     # THEN
#     idea_config = get_idea_config_dict()
#     idea_config = {
#         x_dimen: dimen_config
#         for x_dimen, dimen_config in idea_config.items()
#         if dimen_config.get(idea_category_str()) != "pidgin"
#         # if dimen_config.get(idea_category_str()) == "fisc"
#     }
#     with sqlite3_connect(":memory:") as fisc_db_conn:
#         cursor = fisc_db_conn.cursor()
#         create_all_idea_tables(cursor)
#         create_fisc_prime_tables(cursor)
#         create_bud_prime_tables(cursor)

#         idea_raw2dimen_count = 0
#         idea_dimen_combo_checked_count = 0
#         sorted_idea_numbers = sorted(get_idea_numbers())
#         x_idea_stagable_dimens = {i_num: [] for i_num in sorted_idea_numbers}
#         for x_dimen in sorted(idea_config):
#             dimen_config = idea_config.get(x_dimen)
#             dimen_key_columns = set(dimen_config.get("jkeys").keys())
#             dimen_key_columns = get_default_sorted_list(dimen_key_columns)
#             dimen_key_columns[-1] = get_delete_key_name(dimen_key_columns[-1])
#             dimen_key_columns = set(dimen_key_columns)
#             for idea_number in sorted_idea_numbers:
#                 src_columns = get_table_columns(cursor, f"{idea_number}_raw")
#                 expected_stagable = dimen_key_columns.issubset(src_columns)
#                 src_tablename = f"{idea_number}_raw"
#                 gen_stablable = required_columns_exist(
#                     cursor, src_tablename, dimen_key_columns
#                 )
#                 assert expected_stagable == gen_stablable

#                 idea_dimen_combo_checked_count += 1
#                 if required_columns_exist(cursor, src_tablename, dimen_key_columns):
#                     x_idea_stagable_dimens.get(idea_number).append(x_dimen)
#                     idea_raw2dimen_count += 1
#                     src_cols_set = set(src_columns)
#                     # print(
#                     #     f"{x_dimen} {idea_number} checking... {dimen_key_columns=} {dimen_value_columns=} {src_cols_set=}"
#                     # )
#                     print(
#                         f"{idea_raw2dimen_count} {idea_number} {x_dimen} keys:{dimen_key_columns}"
#                     )
#                     generated_sqlstr = get_idea_into_dimen_raw_query(
#                         conn_or_cursor=cursor,
#                         idea_number=idea_number,
#                         x_dimen=x_dimen,
#                         x_jkeys=dimen_key_columns,
#                     )
#                     # check sqlstr is correct?
#                     assert generated_sqlstr != ""
#     expected_idea_stagable_dimens = {
#         x_idea_number: stagable_dimens
#         for x_idea_number, stagable_dimens in x_idea_stagable_dimens.items()
#         if stagable_dimens != []
#     }
#     idea_stageble_dimen_list = sorted(list(expected_idea_stagable_dimens))
#     print(f"{expected_idea_stagable_dimens=}")
#     assert idea_dimen_combo_checked_count == 680
#     assert idea_raw2dimen_count == 10
#     assert IDEA_STAGEBLE_DEL_DIMENS == expected_idea_stagable_dimens


# def test_CREATE_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
#     # ESTABLISH
#     expected_create_table_sqlstr = f"""
# CREATE TABLE IF NOT EXISTS fisc_event_time_agg (
#   {fisc_tag_str()} TEXT
# , {event_int_str()} INTEGER
# , agg_time INTEGER
# , error_message TEXT
# )
# ;
# """
#     # WHEN / THEN
#     assert CREATE_FISC_EVENT_TIME_AGG_SQLSTR == expected_create_table_sqlstr


# def test_INSERT_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
#     # ESTABLISH
#     expected_INSERT_sqlstr = f"""
# INSERT INTO fisc_event_time_agg ({fisc_tag_str()}, {event_int_str()}, agg_time)
# SELECT {fisc_tag_str()}, {event_int_str()}, agg_time
# FROM (
#     SELECT {fisc_tag_str()}, {event_int_str()}, {tran_time_str()} as agg_time
#     FROM fisc_cashbook_raw
#     GROUP BY {fisc_tag_str()}, {event_int_str()}, {tran_time_str()}
#     UNION
#     SELECT {fisc_tag_str()}, {event_int_str()}, {deal_time_str()} as agg_time
#     FROM fisc_dealunit_raw
#     GROUP BY {fisc_tag_str()}, {event_int_str()}, {deal_time_str()}
# )
# ORDER BY {fisc_tag_str()}, {event_int_str()}, agg_time
# ;
# """
#     # WHEN / THEN
#     assert INSERT_FISC_EVENT_TIME_AGG_SQLSTR == expected_INSERT_sqlstr


# def test_UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR_Exists():
#     # ESTABLISH
#     expected_UPDATE_sqlstr = f"""
# WITH EventTimeOrdered AS (
#     SELECT {fisc_tag_str()}, {event_int_str()}, agg_time,
#            LAG(agg_time) OVER (PARTITION BY {fisc_tag_str()} ORDER BY {event_int_str()}) AS prev_agg_time
#     FROM fisc_event_time_agg
# )
# UPDATE fisc_event_time_agg
# SET error_message = CASE
#          WHEN EventTimeOrdered.prev_agg_time > EventTimeOrdered.agg_time
#          THEN 'not sorted'
#          ELSE 'sorted'
#        END
# FROM EventTimeOrdered
# WHERE EventTimeOrdered.{event_int_str()} = fisc_event_time_agg.{event_int_str()}
#     AND EventTimeOrdered.{fisc_tag_str()} = fisc_event_time_agg.{fisc_tag_str()}
#     AND EventTimeOrdered.agg_time = fisc_event_time_agg.agg_time
# ;
# """
#     # WHEN / THEN
#     assert UPDATE_ERROR_MESSAGE_FISC_EVENT_TIME_AGG_SQLSTR == expected_UPDATE_sqlstr


# def test_CREATE_FISC_OTE1_AGG_SQLSTR_Exists():
#     # ESTABLISH
#     expected_create_table_sqlstr = f"""
# CREATE TABLE IF NOT EXISTS fisc_ote1_agg (
#   {fisc_tag_str()} TEXT
# , {owner_name_str()} TEXT
# , {event_int_str()} INTEGER
# , {deal_time_str()} INTEGER
# , error_message TEXT
# )
# ;
# """
#     # WHEN / THEN
#     assert CREATE_FISC_OTE1_AGG_SQLSTR == expected_create_table_sqlstr


# def test_INSERT_FISC_OTE1_AGG_SQLSTR_Exists():
#     # ESTABLISH
#     expected_INSERT_sqlstr = f"""
# INSERT INTO fisc_ote1_agg ({fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()})
# SELECT {fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
# FROM (
#     SELECT {fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
#     FROM fisc_dealunit_raw
#     GROUP BY {fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
# )
# ORDER BY {fisc_tag_str()}, {owner_name_str()}, {event_int_str()}, {deal_time_str()}
# ;
# """
#     # WHEN / THEN
#     assert INSERT_FISC_OTE1_AGG_SQLSTR == expected_INSERT_sqlstr


# def test_get_fisc_fu1_select_sqlstrs_ReturnsObj_HasAllNeededKeys():
#     # ESTABLISH
#     a23_str = "accord23"

#     # WHEN
#     fu1_select_sqlstrs = get_fisc_fu1_select_sqlstrs(a23_str)

#     # THEN
#     assert fu1_select_sqlstrs
#     expected_fu1_select_dimens = set(get_fisc_dimens())
#     assert set(fu1_select_sqlstrs.keys()) == expected_fu1_select_dimens


# def test_get_fisc_fu1_select_sqlstrs_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH
#     a23_str = "accord23"

#     # WHEN
#     fu1_select_sqlstrs = get_fisc_fu1_select_sqlstrs(fisc_tag=a23_str)

#     # THEN
#     gen_fiscash_sqlstr = fu1_select_sqlstrs.get(fisc_cashbook_str())
#     gen_fisdeal_sqlstr = fu1_select_sqlstrs.get(fisc_dealunit_str())
#     gen_fishour_sqlstr = fu1_select_sqlstrs.get(fisc_timeline_hour_str())
#     gen_fismont_sqlstr = fu1_select_sqlstrs.get(fisc_timeline_month_str())
#     gen_fisweek_sqlstr = fu1_select_sqlstrs.get(fisc_timeline_weekday_str())
#     gen_fisoffi_sqlstr = fu1_select_sqlstrs.get(fisc_timeoffi_str())
#     gen_fisunit_sqlstr = fu1_select_sqlstrs.get(fiscunit_str())
#     with sqlite3_connect(":memory:") as fisc_db_conn:
#         cursor = fisc_db_conn.cursor()
#         create_fisc_prime_tables(cursor)
#         fiscash_agg = f"{fisc_cashbook_str()}_agg"
#         fisdeal_agg = f"{fisc_dealunit_str()}_agg"
#         fishour_agg = f"{fisc_timeline_hour_str()}_agg"
#         fismont_agg = f"{fisc_timeline_month_str()}_agg"
#         fisweek_agg = f"{fisc_timeline_weekday_str()}_agg"
#         fisoffi_agg = f"{fisc_timeoffi_str()}_agg"
#         fiscunit_agg = f"{fiscunit_str()}_agg"
#         where_dict = {fisc_tag_str(): a23_str}
#         fiscash_sql = create_select_query(cursor, fiscash_agg, [], where_dict, True)
#         fisdeal_sql = create_select_query(cursor, fisdeal_agg, [], where_dict, True)
#         fishour_sql = create_select_query(cursor, fishour_agg, [], where_dict, True)
#         fismont_sql = create_select_query(cursor, fismont_agg, [], where_dict, True)
#         fisweek_sql = create_select_query(cursor, fisweek_agg, [], where_dict, True)
#         fisoffi_sql = create_select_query(cursor, fisoffi_agg, [], where_dict, True)
#         fisunit_sql = create_select_query(cursor, fiscunit_agg, [], where_dict, True)
#         print(f"""FISUNIT_FU1_SELECT_SQLSTR = "{fisunit_sql}\"""")
#         assert gen_fiscash_sqlstr == fiscash_sql
#         assert gen_fisdeal_sqlstr == fisdeal_sql
#         assert gen_fishour_sqlstr == fishour_sql
#         assert gen_fismont_sqlstr == fismont_sql
#         assert gen_fisweek_sqlstr == fisweek_sql
#         assert gen_fisoffi_sqlstr == fisoffi_sql
#         assert gen_fisunit_sqlstr == fisunit_sql
