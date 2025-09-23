from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import (
    create_insert_into_clause_str as get_insert_sql,
    create_select_query as get_select_sql,
    create_table2table_agg_insert_query,
    create_update_inconsistency_error_query,
    db_table_exists,
    get_create_table_sqlstr,
    get_table_columns,
)
from src.ch09_belief_atom_logic.atom_config import (
    get_belief_dimens,
    get_delete_key_name,
)
from src.ch15_moment_logic.moment_config import get_moment_dimens
from src.ch16_pidgin_logic.pidgin_config import find_set_otx_inx_args, get_pidgin_dimens
from src.ch17_idea_logic.idea_config import (
    get_default_sorted_list,
    get_idea_config_dict,
    get_idea_sqlite_types,
)
from src.ch18_etl_toolbox._ref.ch18_keywords import (
    belief_plan_awardunit_str,
    belief_plan_factunit_str,
    belief_plan_healerunit_str,
    belief_plan_partyunit_str,
    belief_plan_reason_caseunit_str,
    belief_plan_reasonunit_str,
    belief_planunit_str,
    belief_voice_membership_str,
    belief_voiceunit_str,
    beliefunit_str,
    error_message_str,
    event_int_str,
    face_name_str,
    idea_category_str,
    idea_number_str,
    inx_knot_str,
    moment_timeline_hour_str,
    otx_knot_str,
    pidgin_core_str,
    pidgin_label_str,
    pidgin_rope_str,
    pidgin_title_str,
    unknown_str_str,
)
from src.ch18_etl_toolbox.tran_sqlstrs import (
    ALL_DIMEN_ABBV7,
    create_insert_into_pidgin_core_raw_sqlstr,
    create_insert_missing_face_name_into_pidgin_core_vld_sqlstr,
    create_insert_pidgin_core_agg_into_vld_sqlstr,
    create_insert_pidgin_sound_vld_table_sqlstr,
    create_prime_tablename as prime_tbl,
    create_sound_agg_insert_sqlstrs,
    create_sound_and_heard_tables,
    create_sound_raw_update_inconsist_error_message_sqlstr,
    get_belief_heard_agg_tablenames,
    get_dimen_abbv7,
    get_insert_into_heard_raw_sqlstrs,
    get_insert_into_sound_vld_sqlstrs,
    get_moment_belief_sound_agg_tablenames,
    get_prime_create_table_sqlstrs,
)

BELIEF_PRIME_TABLENAMES = {
    f"{belief_voice_membership_str()}_sound_put_agg": "BLRMEMB_PUT_AGG",
    f"{belief_voice_membership_str()}_sound_put_raw": "BLRMEMB_PUT_RAW",
    f"{belief_voiceunit_str()}_sound_put_agg": "BLRPERN_PUT_AGG",
    f"{belief_voiceunit_str()}_sound_put_raw": "BLRPERN_PUT_RAW",
    f"{belief_plan_awardunit_str()}_sound_put_agg": "BLRAWAR_PUT_AGG",
    f"{belief_plan_awardunit_str()}_sound_put_raw": "BLRAWAR_PUT_RAW",
    f"{belief_plan_factunit_str()}_sound_put_agg": "BLRFACT_PUT_AGG",
    f"{belief_plan_factunit_str()}_sound_put_raw": "BLRFACT_PUT_RAW",
    f"{belief_plan_healerunit_str()}_sound_put_agg": "BLRHEAL_PUT_AGG",
    f"{belief_plan_healerunit_str()}_sound_put_raw": "BLRHEAL_PUT_RAW",
    f"{belief_plan_reason_caseunit_str()}_sound_put_agg": "BLRPREM_PUT_AGG",
    f"{belief_plan_reason_caseunit_str()}_sound_put_raw": "BLRPREM_PUT_RAW",
    f"{belief_plan_reasonunit_str()}_sound_put_agg": "BLRREAS_PUT_AGG",
    f"{belief_plan_reasonunit_str()}_sound_put_raw": "BLRREAS_PUT_RAW",
    f"{belief_plan_partyunit_str()}_sound_put_agg": "BLRLABO_PUT_AGG",
    f"{belief_plan_partyunit_str()}_sound_put_raw": "BLRLABO_PUT_RAW",
    f"{belief_planunit_str()}_sound_put_agg": "BLRPLAN_PUT_AGG",
    f"{belief_planunit_str()}_sound_put_raw": "BLRPLAN_PUT_RAW",
    f"{beliefunit_str()}_sound_put_agg": "BLRUNIT_PUT_AGG",
    f"{beliefunit_str()}_sound_put_raw": "BLRUNIT_PUT_RAW",
    f"{belief_voice_membership_str()}_sound_del_agg": "BLRMEMB_DEL_AGG",
    f"{belief_voice_membership_str()}_sound_del_raw": "BLRMEMB_DEL_RAW",
    f"{belief_voiceunit_str()}_sound_del_agg": "BLRPERN_DEL_AGG",
    f"{belief_voiceunit_str()}_sound_del_raw": "BLRPERN_DEL_RAW",
    f"{belief_plan_awardunit_str()}_sound_del_agg": "BLRAWAR_DEL_AGG",
    f"{belief_plan_awardunit_str()}_sound_del_raw": "BLRAWAR_DEL_RAW",
    f"{belief_plan_factunit_str()}_sound_del_agg": "BLRFACT_DEL_AGG",
    f"{belief_plan_factunit_str()}_sound_del_raw": "BLRFACT_DEL_RAW",
    f"{belief_plan_healerunit_str()}_sound_del_agg": "BLRHEAL_DEL_AGG",
    f"{belief_plan_healerunit_str()}_sound_del_raw": "BLRHEAL_DEL_RAW",
    f"{belief_plan_reason_caseunit_str()}_sound_del_agg": "BLRPREM_DEL_AGG",
    f"{belief_plan_reason_caseunit_str()}_sound_del_raw": "BLRPREM_DEL_RAW",
    f"{belief_plan_reasonunit_str()}_sound_del_agg": "BLRREAS_DEL_AGG",
    f"{belief_plan_reasonunit_str()}_sound_del_raw": "BLRREAS_DEL_RAW",
    f"{belief_plan_partyunit_str()}_sound_del_agg": "BLRLABO_DEL_AGG",
    f"{belief_plan_partyunit_str()}_sound_del_raw": "BLRLABO_DEL_RAW",
    f"{belief_planunit_str()}_sound_del_agg": "BLRPLAN_DEL_AGG",
    f"{belief_planunit_str()}_sound_del_raw": "BLRPLAN_DEL_RAW",
    f"{beliefunit_str()}_sound_del_agg": "BLRUNIT_DEL_AGG",
    f"{beliefunit_str()}_sound_del_raw": "BLRUNIT_DEL_RAW",
}


def get_all_dimen_columns_set(x_dimen: str) -> set[str]:
    if x_dimen == pidgin_core_str():
        return {
            event_int_str(),
            face_name_str(),
            otx_knot_str(),
            inx_knot_str(),
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
    columns.add(error_message_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_pidgin_sound_agg_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add(error_message_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_moment_sound_agg_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add(error_message_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_moment_sound_vld_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_pidgin_sound_vld_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.remove(otx_knot_str())
    columns.remove(inx_knot_str())
    columns.remove(unknown_str_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_pidgin_core_raw_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.remove(event_int_str())
    columns.add("source_dimen")
    columns.add(error_message_str())
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


def create_moment_heard_raw_table_sqlstr(x_dimen):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "h", "raw")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = find_set_otx_inx_args(columns)
    columns.add(error_message_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_moment_heard_agg_table_sqlstr(x_dimen: str):
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "h", "agg")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.remove(event_int_str())
    columns.remove(face_name_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_sound_put_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add(idea_number_str())
    columns.add(error_message_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_sound_put_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns.add(error_message_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_sound_put_vld_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_sound_del_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns.add(idea_number_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_sound_del_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns.add(error_message_str())
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_sound_del_vld_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_heard_put_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "h", "raw", "put")
    columns = set()
    columns = get_all_dimen_columns_set(x_dimen)
    columns = find_set_otx_inx_args(columns)
    columns.add("pidgin_event_int")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_heard_put_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "h", "agg", "put")
    columns = get_all_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_heard_del_raw_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "h", "raw", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns = find_set_otx_inx_args(columns)
    columns.add("pidgin_event_int")
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def create_belief_heard_del_agg_table_sqlstr(x_dimen: str) -> str:
    tablename = prime_tbl(get_dimen_abbv7(x_dimen), "h", "agg", "del")
    columns = get_del_dimen_columns_set(x_dimen)
    columns = get_default_sorted_list(columns)
    return get_create_table_sqlstr(tablename, columns, get_idea_sqlite_types())


def test_get_prime_create_table_sqlstrs_ReturnsObj_PidginDimensCheck():
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


def test_get_prime_create_table_sqlstrs_ReturnsObj_PidginCoreDimensPidgin():
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


def test_get_prime_create_table_sqlstrs_ReturnsObj_CheckMomentDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    idea_config = get_idea_config_dict()
    moment_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "moment"
    }

    for x_dimen in moment_dimens_config:
        # print(f"{abbv7} {x_dimen} checking...")
        s_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw")
        s_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg")
        s_vld_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld")
        v_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "h", "raw")
        v_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "h", "agg")
        expected_s_raw_sqlstr = create_pidgin_sound_raw_table_sqlstr(x_dimen)
        expected_s_agg_sqlstr = create_moment_sound_agg_table_sqlstr(x_dimen)
        expected_s_vld_sqlstr = create_moment_sound_vld_table_sqlstr(x_dimen)
        expected_h_raw_sqlstr = create_moment_heard_raw_table_sqlstr(x_dimen)
        expected_h_agg_sqlstr = create_moment_heard_agg_table_sqlstr(x_dimen)
        abbv7 = get_dimen_abbv7(x_dimen)
        print(f'CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR= """{expected_s_raw_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR= """{expected_s_agg_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_SOUND_VLD_SQLSTR= """{expected_s_vld_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_HEARD_RAW_SQLSTR= """{expected_h_raw_sqlstr}"""')
        print(f'CREATE_{abbv7.upper()}_HEARD_AGG_SQLSTR= """{expected_h_agg_sqlstr}"""')
        # print(f'"{s_raw_tablename}": CREATE_{abbv7.upper()}_SOUND_RAW_SQLSTR,')
        # print(f'"{s_agg_tablename}": CREATE_{abbv7.upper()}_SOUND_AGG_SQLSTR,')
        # print(f'"{s_vld_tablename}": CREATE_{abbv7.upper()}_SOUND_VLD_SQLSTR,')
        # print(f'"{v_raw_tablename}": CREATE_{abbv7.upper()}_HEARD_RAW_SQLSTR,')
        # print(f'"{v_agg_tablename}": CREATE_{abbv7.upper()}_HEARD_AGG_SQLSTR,')
        assert expected_s_raw_sqlstr == create_table_sqlstrs.get(s_raw_tablename)
        assert expected_s_agg_sqlstr == create_table_sqlstrs.get(s_agg_tablename)
        assert expected_s_vld_sqlstr == create_table_sqlstrs.get(s_vld_tablename)
        assert expected_h_raw_sqlstr == create_table_sqlstrs.get(v_raw_tablename)
        assert expected_h_agg_sqlstr == create_table_sqlstrs.get(v_agg_tablename)


def test_get_prime_create_table_sqlstrs_ReturnsObj_CheckBeliefDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    belief_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in get_idea_config_dict().items()
        if dimen_config.get(idea_category_str()) == "belief"
    }

    for x_dimen in belief_dimens_config:
        # print(f"{x_dimen} checking...")
        s_put_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw", "put")
        s_put_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg", "put")
        s_put_vld_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld", "put")
        s_del_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "raw", "del")
        s_del_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "agg", "del")
        s_del_vld_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "s", "vld", "del")
        v_put_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "h", "raw", "put")
        v_put_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "h", "agg", "put")
        v_del_raw_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "h", "raw", "del")
        v_del_agg_tablename = prime_tbl(get_dimen_abbv7(x_dimen), "h", "agg", "del")

        expected_s_put_raw_sqlstr = create_belief_sound_put_raw_table_sqlstr(x_dimen)
        expected_s_put_agg_sqlstr = create_belief_sound_put_agg_table_sqlstr(x_dimen)
        expected_s_put_vld_sqlstr = create_belief_sound_put_vld_table_sqlstr(x_dimen)
        expected_s_del_raw_sqlstr = create_belief_sound_del_raw_table_sqlstr(x_dimen)
        expected_s_del_agg_sqlstr = create_belief_sound_del_agg_table_sqlstr(x_dimen)
        expected_s_del_vld_sqlstr = create_belief_sound_del_vld_table_sqlstr(x_dimen)
        expected_h_put_raw_sqlstr = create_belief_heard_put_raw_table_sqlstr(x_dimen)
        expected_h_put_agg_sqlstr = create_belief_heard_put_agg_table_sqlstr(x_dimen)
        expected_h_del_raw_sqlstr = create_belief_heard_del_raw_table_sqlstr(x_dimen)
        expected_h_del_agg_sqlstr = create_belief_heard_del_agg_table_sqlstr(x_dimen)
        abbv7 = get_dimen_abbv7(x_dimen)
        # print(f"{x_dimen=} {abbv7=}")
        print("")
        print(f'CREATE_{abbv7}_SOUND_PUT_RAW_STR= "{expected_s_put_raw_sqlstr}"')
        print(f'CREATE_{abbv7}_SOUND_PUT_AGG_STR= "{expected_s_put_agg_sqlstr}"')
        print(f'CREATE_{abbv7}_SOUND_PUT_VLD_STR= "{expected_s_put_vld_sqlstr}"')
        print(f'CREATE_{abbv7}_SOUND_DEL_RAW_STR= "{expected_s_del_raw_sqlstr}"')
        print(f'CREATE_{abbv7}_SOUND_DEL_AGG_STR= "{expected_s_del_agg_sqlstr}"')
        print(f'CREATE_{abbv7}_SOUND_DEL_VLD_STR= "{expected_s_del_vld_sqlstr}"')
        print(f'CREATE_{abbv7}_HEARD_PUT_RAW_STR= "{expected_h_put_raw_sqlstr}"')
        print(f'CREATE_{abbv7}_HEARD_PUT_AGG_STR= "{expected_h_put_agg_sqlstr}"')
        print(f'CREATE_{abbv7}_HEARD_DEL_RAW_STR= "{expected_h_del_raw_sqlstr}"')
        print(f'CREATE_{abbv7}_HEARD_DEL_AGG_STR= "{expected_h_del_agg_sqlstr}"')

        # print(f'"{s_put_raw_tablename}": CREATE_{abbv7}_SOUND_PUT_RAW_STR,')
        # print(f'"{s_put_agg_tablename}": CREATE_{abbv7}_SOUND_PUT_AGG_STR,')
        # print(f'"{s_put_vld_tablename}": CREATE_{abbv7}_SOUND_PUT_VLD_STR,')
        # print(f'"{s_del_raw_tablename}": CREATE_{abbv7}_SOUND_DEL_RAW_STR,')
        # print(f'"{s_del_agg_tablename}": CREATE_{abbv7}_SOUND_DEL_AGG_STR,')
        # print(f'"{s_del_vld_tablename}": CREATE_{abbv7}_SOUND_DEL_VLD_STR,')
        # print(f'"{v_put_raw_tablename}": CREATE_{abbv7}_HEARD_PUT_RAW_STR,')
        # print(f'"{v_put_agg_tablename}": CREATE_{abbv7}_HEARD_PUT_AGG_STR,')
        # print(f'"{v_del_raw_tablename}": CREATE_{abbv7}_HEARD_DEL_RAW_STR,')
        # print(f'"{v_del_agg_tablename}": CREATE_{abbv7}_HEARD_DEL_AGG_STR,')
        assert expected_s_put_raw_sqlstr == sqlstrs.get(s_put_raw_tablename)
        assert expected_s_put_agg_sqlstr == sqlstrs.get(s_put_agg_tablename)
        assert expected_s_put_vld_sqlstr == sqlstrs.get(s_put_vld_tablename)
        assert expected_s_del_raw_sqlstr == sqlstrs.get(s_del_raw_tablename)
        assert expected_s_del_agg_sqlstr == sqlstrs.get(s_del_agg_tablename)
        assert expected_s_del_vld_sqlstr == sqlstrs.get(s_del_vld_tablename)
        assert expected_h_put_raw_sqlstr == sqlstrs.get(v_put_raw_tablename)
        assert expected_h_put_agg_sqlstr == sqlstrs.get(v_put_agg_tablename)
        assert expected_h_del_raw_sqlstr == sqlstrs.get(v_del_raw_tablename)
        assert expected_h_del_agg_sqlstr == sqlstrs.get(v_del_agg_tablename)


def test_get_prime_create_table_sqlstrs_ReturnsObj_HasAllNeededKeys():
    # ESTABLISH / WHEN
    create_table_sqlstrs = get_prime_create_table_sqlstrs()

    # THEN
    assert create_table_sqlstrs
    pidgin_dimens_count = len(get_pidgin_dimens()) * 3
    moment_dimens_count = len(get_moment_dimens()) * 5
    belief_dimens_count = len(get_belief_dimens()) * 10
    print(f"{pidgin_dimens_count=}")
    print(f"{moment_dimens_count=}")
    print(f"{belief_dimens_count=}")
    all_dimens_count = pidgin_dimens_count + moment_dimens_count + belief_dimens_count
    pidgin_core_count = 3
    all_dimens_count += pidgin_core_count
    assert len(create_table_sqlstrs) == all_dimens_count


def test_get_moment_belief_sound_agg_tablenames_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    moment_belief_sound_agg_tablenames = get_moment_belief_sound_agg_tablenames()

    # THEN
    assert moment_belief_sound_agg_tablenames
    expected_sound_agg_tablenames = set()
    for belief_dimen in get_belief_dimens():
        expected_sound_agg_tablenames.add(prime_tbl(belief_dimen, "s", "agg", "put"))
        expected_sound_agg_tablenames.add(prime_tbl(belief_dimen, "s", "agg", "del"))
    for moment_dimen in get_moment_dimens():
        expected_sound_agg_tablenames.add(prime_tbl(moment_dimen, "s", "agg"))
    print(sorted(list(expected_sound_agg_tablenames)))
    assert expected_sound_agg_tablenames == moment_belief_sound_agg_tablenames
    agg_tablenames = moment_belief_sound_agg_tablenames
    assert len(agg_tablenames) == len(get_belief_dimens()) * 2 + len(
        get_moment_dimens()
    )
    assert agg_tablenames.issubset(set(get_prime_create_table_sqlstrs().keys()))


def test_get_belief_heard_agg_tablenames_ReturnsObj_BeliefDimens():
    # ESTABLISH / WHEN
    belief_heard_agg_tablenames = get_belief_heard_agg_tablenames()

    # THEN
    assert belief_heard_agg_tablenames
    expected_belief_heard_agg_tablenames = {
        prime_tbl(belief_dimen, "h", "agg", "put")
        for belief_dimen in get_belief_dimens()
    }
    print(f"{expected_belief_heard_agg_tablenames=}")
    assert expected_belief_heard_agg_tablenames == belief_heard_agg_tablenames
    assert len(belief_heard_agg_tablenames) == len(get_belief_dimens())
    agg_tablenames = belief_heard_agg_tablenames
    assert agg_tablenames.issubset(set(get_prime_create_table_sqlstrs().keys()))


def test_create_sound_and_heard_tables_CreatesMomentRawTables():
    # ESTABLISH
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
        assert cursor.fetchone()[0] == 0
        agg_str = "agg"
        raw_str = "raw"
        vld_str = "vld"
        put_str = "put"
        del_str = "del"
        blrunit_s_put_agg_table = prime_tbl("beliefunit", "s", agg_str, put_str)
        blrpern_s_put_agg_table = prime_tbl("blrpern", "s", agg_str, put_str)
        blrmemb_s_put_agg_table = prime_tbl("blrmemb", "s", agg_str, put_str)
        blrfact_s_del_agg_table = prime_tbl("blrfact", "s", agg_str, del_str)
        blrfact_s_del_vld_table = prime_tbl("blrfact", "s", vld_str, del_str)
        momentunit_s_agg_table = prime_tbl("momentunit", "s", agg_str)
        momentunit_s_vld_table = prime_tbl("momentunit", "s", vld_str)
        pidtitl_s_agg_table = prime_tbl("pidtitl", "s", agg_str)
        blfhour_h_agg_table = prime_tbl("blfhour", "h", agg_str)
        pidtitl_s_raw_table = prime_tbl("pidtitl", "s", raw_str)
        pidcore_s_raw_table = prime_tbl("pidcore", "s", raw_str)
        pidcore_s_agg_table = prime_tbl("pidcore", "s", agg_str)
        pidcore_s_vld_table = prime_tbl("pidcore", "s", vld_str)

        assert not db_table_exists(cursor, blrunit_s_put_agg_table)
        assert not db_table_exists(cursor, blrpern_s_put_agg_table)
        assert not db_table_exists(cursor, blrmemb_s_put_agg_table)
        assert not db_table_exists(cursor, blrfact_s_del_agg_table)
        assert not db_table_exists(cursor, blrfact_s_del_vld_table)
        assert not db_table_exists(cursor, momentunit_s_agg_table)
        assert not db_table_exists(cursor, momentunit_s_vld_table)
        assert not db_table_exists(cursor, pidtitl_s_agg_table)
        assert not db_table_exists(cursor, blfhour_h_agg_table)
        assert not db_table_exists(cursor, pidtitl_s_raw_table)
        assert not db_table_exists(cursor, pidcore_s_raw_table)
        assert not db_table_exists(cursor, pidcore_s_agg_table)
        assert not db_table_exists(cursor, pidcore_s_vld_table)

        # WHEN
        create_sound_and_heard_tables(cursor)

        # THEN
        cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")
        # print(f"{cursor.fetchall()=}")
        # x_count = 0
        # for x_row in cursor.fetchall():
        #     print(f"{x_count} {x_row[1]=}")
        #     x_count += 1
        assert db_table_exists(cursor, blrunit_s_put_agg_table)
        assert db_table_exists(cursor, blrpern_s_put_agg_table)
        assert db_table_exists(cursor, blrmemb_s_put_agg_table)
        assert db_table_exists(cursor, blrfact_s_del_agg_table)
        assert db_table_exists(cursor, blrfact_s_del_vld_table)
        assert db_table_exists(cursor, momentunit_s_agg_table)
        assert db_table_exists(cursor, momentunit_s_vld_table)
        assert db_table_exists(cursor, pidtitl_s_agg_table)
        assert db_table_exists(cursor, blfhour_h_agg_table)
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
        create_sound_and_heard_tables(cursor)

        # WHEN
        update_sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
            cursor, dimen
        )

        # THEN
        x_tablename = prime_tbl(dimen, "s", "raw")
        dimen_config = get_idea_config_dict().get(dimen)
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        exclude_cols = {idea_number_str(), error_message_str()}
        expected_update_sqlstr = create_update_inconsistency_error_query(
            cursor,
            x_tablename,
            dimen_focus_columns,
            exclude_cols,
            error_holder_column=error_message_str(),
            error_str="Inconsistent data",
        )
        assert update_sqlstr == expected_update_sqlstr

        static_example_sqlstr = """WITH inconsistency_rows AS (
SELECT event_int, face_name, otx_title
FROM pidgin_title_s_raw
GROUP BY event_int, face_name, otx_title
HAVING MIN(inx_title) != MAX(inx_title)
    OR MIN(otx_knot) != MAX(otx_knot)
    OR MIN(inx_knot) != MAX(inx_knot)
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


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario1_MomentDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = moment_timeline_hour_str()
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)

        # WHEN
        update_sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
            cursor, dimen
        )

        # THEN
        x_tablename = prime_tbl(dimen, "s", "raw")
        dimen_config = get_idea_config_dict().get(dimen)
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        exclude_cols = {
            idea_number_str(),
            "event_int",
            "face_name",
            error_message_str(),
        }
        expected_update_sqlstr = create_update_inconsistency_error_query(
            cursor,
            x_tablename,
            dimen_focus_columns,
            exclude_cols,
            error_holder_column=error_message_str(),
            error_str="Inconsistent data",
        )
        print(expected_update_sqlstr)
        assert update_sqlstr == expected_update_sqlstr

        static_example_sqlstr = """WITH inconsistency_rows AS (
SELECT moment_label, cumulative_minute
FROM moment_timeline_hour_s_raw
GROUP BY moment_label, cumulative_minute
HAVING MIN(hour_label) != MAX(hour_label)
)
UPDATE moment_timeline_hour_s_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.moment_label = moment_timeline_hour_s_raw.moment_label
    AND inconsistency_rows.cumulative_minute = moment_timeline_hour_s_raw.cumulative_minute
;
"""
        # print(update_sqlstr)
        assert update_sqlstr == static_example_sqlstr


def test_create_sound_raw_update_inconsist_error_message_sqlstr_ReturnsObj_Scenario2_BeliefDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = belief_plan_awardunit_str()
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)

        # WHEN
        update_sqlstr = create_sound_raw_update_inconsist_error_message_sqlstr(
            cursor, dimen
        )

        # THEN
        x_tablename = prime_tbl(dimen, "s", "raw", "put")
        dimen_config = get_idea_config_dict().get(dimen)
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        exclude_cols = {idea_number_str(), error_message_str()}
        expected_update_sqlstr = create_update_inconsistency_error_query(
            cursor,
            x_tablename,
            dimen_focus_columns,
            exclude_cols,
            error_holder_column=error_message_str(),
            error_str="Inconsistent data",
        )
        print(expected_update_sqlstr)
        assert update_sqlstr == expected_update_sqlstr

        static_example_sqlstr = """WITH inconsistency_rows AS (
SELECT event_int, face_name, moment_label, belief_name, plan_rope, awardee_title
FROM belief_plan_awardunit_s_put_raw
GROUP BY event_int, face_name, moment_label, belief_name, plan_rope, awardee_title
HAVING MIN(give_force) != MAX(give_force)
    OR MIN(take_force) != MAX(take_force)
)
UPDATE belief_plan_awardunit_s_put_raw
SET error_message = 'Inconsistent data'
FROM inconsistency_rows
WHERE inconsistency_rows.event_int = belief_plan_awardunit_s_put_raw.event_int
    AND inconsistency_rows.face_name = belief_plan_awardunit_s_put_raw.face_name
    AND inconsistency_rows.moment_label = belief_plan_awardunit_s_put_raw.moment_label
    AND inconsistency_rows.belief_name = belief_plan_awardunit_s_put_raw.belief_name
    AND inconsistency_rows.plan_rope = belief_plan_awardunit_s_put_raw.plan_rope
    AND inconsistency_rows.awardee_title = belief_plan_awardunit_s_put_raw.awardee_title
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
        create_sound_and_heard_tables(cursor)

        # WHEN
        update_sqlstrs = create_sound_agg_insert_sqlstrs(cursor, dimen)

        # THEN
        raw_tablename = prime_tbl(dimen, "s", "raw")
        agg_tablename = prime_tbl(dimen, "s", "agg")
        dimen_config = get_idea_config_dict().get(dimen)
        dimen_focus_columns = set(dimen_config.get("jkeys").keys())
        exclude_cols = {idea_number_str(), error_message_str()}
        expected_insert_sqlstr = create_table2table_agg_insert_query(
            cursor,
            src_table=raw_tablename,
            dst_table=agg_tablename,
            focus_cols=dimen_focus_columns,
            exclude_cols=exclude_cols,
            where_block="WHERE error_message IS NULL",
        )
        # print(expected_insert_sqlstr)
        assert update_sqlstrs[0] == expected_insert_sqlstr

        static_example_sqlstr = """INSERT INTO pidgin_title_s_agg (event_int, face_name, otx_title, inx_title, otx_knot, inx_knot, unknown_str)
SELECT event_int, face_name, otx_title, MAX(inx_title), MAX(otx_knot), MAX(inx_knot), MAX(unknown_str)
FROM pidgin_title_s_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, otx_title
;
"""
        print(update_sqlstrs[0])
        assert update_sqlstrs[0] == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario1_MomentDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = moment_timeline_hour_str()
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)

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
            error_message_str(),
        }
        print("yeah")
        expected_insert_sqlstr = create_table2table_agg_insert_query(
            cursor,
            src_table=raw_tablename,
            dst_table=agg_tablename,
            focus_cols=dimen_focus_columns,
            exclude_cols=exclude_cols,
            where_block="WHERE error_message IS NULL",
        )
        print(expected_insert_sqlstr)
        assert update_sqlstrs[0] == expected_insert_sqlstr

        static_example_sqlstr = """INSERT INTO moment_timeline_hour_s_agg (event_int, face_name, moment_label, cumulative_minute, hour_label)
SELECT event_int, face_name, moment_label, cumulative_minute, MAX(hour_label)
FROM moment_timeline_hour_s_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, moment_label, cumulative_minute
;
"""
        print(update_sqlstrs[0])
        assert update_sqlstrs[0] == static_example_sqlstr


def test_create_sound_agg_insert_sqlstrs_ReturnsObj_Scenario2_BeliefDimen():
    # sourcery skip: extract-method
    # ESTABLISH
    dimen = belief_plan_awardunit_str()
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)

        # WHEN
        update_sqlstrs = create_sound_agg_insert_sqlstrs(cursor, dimen)

        # THEN
        put_raw_tablename = prime_tbl(dimen, "s", "raw", "put")
        put_agg_tablename = prime_tbl(dimen, "s", "agg", "put")
        put_dimen_config = get_idea_config_dict().get(dimen)
        put_dimen_focus_columns = set(put_dimen_config.get("jkeys").keys())
        put_exclude_cols = {idea_number_str(), error_message_str()}
        put_expected_insert_sqlstr = create_table2table_agg_insert_query(
            cursor,
            src_table=put_raw_tablename,
            dst_table=put_agg_tablename,
            focus_cols=put_dimen_focus_columns,
            exclude_cols=put_exclude_cols,
            where_block="WHERE error_message IS NULL",
        )
        # print(put_expected_insert_sqlstr)
        assert update_sqlstrs[0] == put_expected_insert_sqlstr

        static_example_put_sqlstr = """INSERT INTO belief_plan_awardunit_s_put_agg (event_int, face_name, moment_label, belief_name, plan_rope, awardee_title, give_force, take_force)
SELECT event_int, face_name, moment_label, belief_name, plan_rope, awardee_title, MAX(give_force), MAX(take_force)
FROM belief_plan_awardunit_s_put_raw
WHERE error_message IS NULL
GROUP BY event_int, face_name, moment_label, belief_name, plan_rope, awardee_title
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
        del_exclude_cols = {idea_number_str(), error_message_str()}
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

        static_example_del_sqlstr = """INSERT INTO belief_plan_awardunit_s_del_agg (event_int, face_name, moment_label, belief_name, plan_rope, awardee_title_ERASE)
SELECT event_int, face_name, moment_label, belief_name, plan_rope, awardee_title_ERASE
FROM belief_plan_awardunit_s_del_raw
GROUP BY event_int, face_name, moment_label, belief_name, plan_rope, awardee_title_ERASE
;
"""
        assert update_sqlstrs[1] == static_example_del_sqlstr


def test_create_insert_into_pidgin_core_raw_sqlstr_ReturnsObj():
    # ESTABLISH
    dimen = pidgin_rope_str()
    # WHEN
    rope_sqlstr = create_insert_into_pidgin_core_raw_sqlstr(dimen)

    # THEN
    pidgin_s_agg_tablename = prime_tbl(dimen, "s", "agg")
    pidgin_core_s_raw_tablename = prime_tbl("PIDCORE", "s", "raw")
    expected_sqlstr = f"""INSERT INTO {pidgin_core_s_raw_tablename} (source_dimen, face_name, otx_knot, inx_knot, unknown_str)
SELECT '{pidgin_s_agg_tablename}', face_name, otx_knot, inx_knot, unknown_str
FROM {pidgin_s_agg_tablename}
GROUP BY face_name, otx_knot, inx_knot, unknown_str
;
"""
    assert rope_sqlstr == expected_sqlstr


def test_create_insert_pidgin_core_agg_into_vld_sqlstr_ReturnsObj():
    # ESTABLISH
    default_knot = "|"
    default_unknown_str = "unknown2"

    # WHEN
    insert_sqlstr = create_insert_pidgin_core_agg_into_vld_sqlstr(
        default_knot, default_unknown_str
    )

    # THEN
    pidcore_dimen = "PIDCORE"
    pidgin_core_s_agg_tablename = prime_tbl(pidcore_dimen, "s", "agg")
    pidgin_core_s_vld_tablename = prime_tbl(pidcore_dimen, "s", "vld")
    expected_sqlstr = f"""INSERT INTO {pidgin_core_s_vld_tablename} (face_name, otx_knot, inx_knot, unknown_str)
SELECT
  face_name
, IFNULL(otx_knot, '{default_knot}')
, IFNULL(inx_knot, '{default_knot}')
, IFNULL(unknown_str, '{default_unknown_str}')
FROM {pidgin_core_s_agg_tablename}
;
"""
    print(expected_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_insert_missing_face_name_into_pidgin_core_vld_sqlstr_ReturnsObj():
    # ESTABLISH
    default_knot = "|"
    default_unknown_str = "unknown2"
    blrpern_s_agg_tablename = prime_tbl(belief_voiceunit_str(), "s", "agg")

    # WHEN
    insert_sqlstr = create_insert_missing_face_name_into_pidgin_core_vld_sqlstr(
        default_knot, default_unknown_str, blrpern_s_agg_tablename
    )

    # THEN
    pidcore_dimen = "PIDCORE"
    pidgin_core_s_vld_tablename = prime_tbl(pidcore_dimen, "s", "vld")
    expected_sqlstr = f"""INSERT INTO {pidgin_core_s_vld_tablename} (face_name, otx_knot, inx_knot, unknown_str)
SELECT
  {blrpern_s_agg_tablename}.face_name
, '{default_knot}'
, '{default_knot}'
, '{default_unknown_str}'
FROM {blrpern_s_agg_tablename} 
LEFT JOIN pidgin_core_s_vld ON pidgin_core_s_vld.face_name = {blrpern_s_agg_tablename}.face_name
WHERE pidgin_core_s_vld.face_name IS NULL
GROUP BY {blrpern_s_agg_tablename}.face_name
;
"""
    print(expected_sqlstr)
    assert insert_sqlstr == expected_sqlstr


def test_create_insert_pidgin_sound_vld_table_sqlstr_ReturnsObj_pidgin_rope():
    # ESTABLISH
    dimen = pidgin_rope_str()
    # WHEN
    rope_sqlstr = create_insert_pidgin_sound_vld_table_sqlstr(dimen)

    # THEN
    pidgin_dimen_s_agg_tablename = prime_tbl(dimen, "s", "agg")
    pidgin_dimen_s_vld_tablename = prime_tbl(dimen, "s", "vld")
    expected_rope_sqlstr = f"""
INSERT INTO {pidgin_dimen_s_vld_tablename} (event_int, face_name, otx_rope, inx_rope)
SELECT event_int, face_name, MAX(otx_rope), MAX(inx_rope)
FROM {pidgin_dimen_s_agg_tablename}
WHERE error_message IS NULL
GROUP BY event_int, face_name
;
"""
    print(expected_rope_sqlstr)
    assert rope_sqlstr == expected_rope_sqlstr


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


def test_get_insert_into_sound_vld_sqlstrs_ReturnsObj_BeliefDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    belief_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "belief"
    }

    # WHEN
    insert_s_vld_sqlstrs = get_insert_into_sound_vld_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)

        for belief_dimen in belief_dimens_config:
            # print(f"{belief_dimen=}")
            s_put_agg_tablename = prime_tbl(belief_dimen, "s", "agg", "put")
            s_del_agg_tablename = prime_tbl(belief_dimen, "s", "agg", "del")
            s_put_vld_tablename = prime_tbl(belief_dimen, "s", "vld", "put")
            s_del_vld_tablename = prime_tbl(belief_dimen, "s", "vld", "del")
            s_put_agg_cols = get_table_columns(cursor, s_put_agg_tablename)
            s_del_agg_cols = get_table_columns(cursor, s_del_agg_tablename)
            s_put_agg_cols.remove(error_message_str())
            s_del_agg_cols.remove(error_message_str())
            s_put_agg_cols = set(s_put_agg_cols)
            s_del_agg_cols = set(s_del_agg_cols)
            s_put_vld_cols = set(get_table_columns(cursor, s_put_vld_tablename))
            s_del_vld_cols = set(get_table_columns(cursor, s_del_vld_tablename))
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
            abbv7 = get_dimen_abbv7(belief_dimen)
            put_sqlstr_ref = f"INSERT_{abbv7.upper()}_SOUND_VLD_PUT_SQLSTR"
            del_sqlstr_ref = f"INSERT_{abbv7.upper()}_SOUND_VLD_DEL_SQLSTR"
            print(f'{put_sqlstr_ref}= "{s_put_vld_insert_select}"')
            print(f'{del_sqlstr_ref}= "{s_del_vld_insert_select}"')
            # print(f"""'{s_put_vld_tablename}': {put_sqlstr_ref},""")
            # print(f"""'{s_del_vld_tablename}': {del_sqlstr_ref},""")
            assert insert_s_vld_sqlstrs.get(s_put_vld_tbl) == s_put_vld_insert_select
            assert insert_s_vld_sqlstrs.get(s_del_vld_tbl) == s_del_vld_insert_select


def test_get_insert_into_sound_vld_sqlstrs_ReturnsObj_MomentDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    moment_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "moment"
    }

    # WHEN
    insert_s_vld_sqlstrs = get_insert_into_sound_vld_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)

        for moment_dimen in moment_dimens_config:
            # print(f"{moment_dimen=}")
            s_agg_tablename = prime_tbl(moment_dimen, "s", "agg")
            s_vld_tablename = prime_tbl(moment_dimen, "s", "vld")
            s_agg_cols = get_table_columns(cursor, s_agg_tablename)
            s_agg_cols.remove(error_message_str())
            s_agg_cols = set(s_agg_cols)
            s_vld_cols = set(get_table_columns(cursor, s_vld_tablename))
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
            abbv7 = get_dimen_abbv7(moment_dimen)
            sqlstr_ref = f"INSERT_{abbv7.upper()}_SOUND_VLD_SQLSTR"
            print(f'{sqlstr_ref}= "{s_vld_insert_select}"')
            # print(f""""{s_vld_tablename}": {sqlstr_ref},""")
            assert insert_s_vld_sqlstrs.get(s_vld_tbl) == s_vld_insert_select


def test_get_insert_into_heard_raw_sqlstrs_ReturnsObj_BeliefDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    belief_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "belief"
    }

    # WHEN
    insert_h_raw_sqlstrs = get_insert_into_heard_raw_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)

        for belief_dimen in belief_dimens_config:
            # print(f"{belief_dimen=}")
            s_put_vld_tablename = prime_tbl(belief_dimen, "s", "vld", "put")
            s_del_vld_tablename = prime_tbl(belief_dimen, "s", "vld", "del")
            v_put_raw_tablename = prime_tbl(belief_dimen, "h", "raw", "put")
            v_del_raw_tablename = prime_tbl(belief_dimen, "h", "raw", "del")
            s_put_cols = set(get_table_columns(cursor, s_put_vld_tablename))
            s_del_cols = set(get_table_columns(cursor, s_del_vld_tablename))
            # s_put_cols = set(s_put_cols).remove(error_message_str())
            # s_del_cols = set(s_del_cols).remove(error_message_str())
            v_put_raw_cols = set(get_table_columns(cursor, v_put_raw_tablename))
            v_del_raw_cols = set(get_table_columns(cursor, v_del_raw_tablename))
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
            abbv7 = get_dimen_abbv7(belief_dimen)
            put_sqlstr_ref = f"INSERT_{abbv7.upper()}_HEARD_RAW_PUT_SQLSTR"
            del_sqlstr_ref = f"INSERT_{abbv7.upper()}_HEARD_RAW_DEL_SQLSTR"
            print(f'{put_sqlstr_ref}= "{v_put_raw_insert_select}"')
            print(f'{del_sqlstr_ref}= "{v_del_raw_insert_select}"')
            # print(f"""'{v_put_raw_tablename}': {put_sqlstr_ref},""")
            # print(f"""'{v_del_raw_tablename}': {del_sqlstr_ref},""")
            assert insert_h_raw_sqlstrs.get(v_put_raw_tbl) == v_put_raw_insert_select
            assert insert_h_raw_sqlstrs.get(v_del_raw_tbl) == v_del_raw_insert_select


def test_get_insert_into_heard_raw_sqlstrs_ReturnsObj_MomentDimens():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    idea_config = get_idea_config_dict()
    moment_dimens_config = {
        x_dimen: dimen_config
        for x_dimen, dimen_config in idea_config.items()
        if dimen_config.get(idea_category_str()) == "moment"
    }

    # WHEN
    insert_h_raw_sqlstrs = get_insert_into_heard_raw_sqlstrs()

    # THEN
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_sound_and_heard_tables(cursor)

        for moment_dimen in moment_dimens_config:
            # print(f"{moment_dimen=}")
            s_vld_tablename = prime_tbl(moment_dimen, "s", "vld")
            v_raw_tablename = prime_tbl(moment_dimen, "h", "raw")
            s_cols = set(get_table_columns(cursor, s_vld_tablename))
            v_raw_cols = get_table_columns(cursor, v_raw_tablename)
            v_raw_cols.remove(error_message_str())
            v_cols = find_set_otx_inx_args(v_raw_cols)
            v_cols = {col for col in v_cols if col[-3:] != "inx"}
            v_raw_tbl = v_raw_tablename
            s_vld_tbl = s_vld_tablename
            v_raw_insert_sql = get_insert_sql(cursor, v_raw_tbl, v_cols)
            s_vld_select_sql = get_select_sql(cursor, s_vld_tbl, s_cols, flat_bool=True)
            v_raw_insert_select = f"{v_raw_insert_sql} {s_vld_select_sql}"
            # create_select_query(cursor=)
            abbv7 = get_dimen_abbv7(moment_dimen)
            sqlstr_ref = f"INSERT_{abbv7.upper()}_HEARD_RAW_SQLSTR"
            print(f'{sqlstr_ref}= "{v_raw_insert_select}"')
            # print(f""""{v_raw_tablename}": {sqlstr_ref},""")
            assert insert_h_raw_sqlstrs.get(v_raw_tbl) == v_raw_insert_select
