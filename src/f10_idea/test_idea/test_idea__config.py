from src.f00_instrument.file import save_json, create_path
from src.f01_road.deal import (
    quota_str,
    deal_time_str,
    tran_time_str,
    bridge_str,
    celldepth_str,
    owner_name_str,
    fisc_title_str,
    world_id_str,
)
from src.f02_bud.bud_tool import (
    bud_acct_membership_str,
    bud_acctunit_str,
    bud_item_awardlink_str,
    bud_item_factunit_str,
    bud_item_teamlink_str,
    bud_item_healerlink_str,
    bud_item_reason_premiseunit_str,
    bud_item_reasonunit_str,
    bud_itemunit_str,
    budunit_str,
)
from src.f03_chrono.chrono import (
    c400_number_str,
    monthday_distortion_str,
    timeline_title_str,
    yr1_jan1_offset_str,
)
from src.f04_kick.atom_config import (
    get_atom_args_dimen_mapping,
    get_atom_config_dict,
    get_bud_dimens,
    get_delete_key_name,
    get_all_bud_dimen_delete_keys,
    jkeys_str,
    jvalues_str,
    normal_specs_str,
    column_order_str,
    atom_delete,
    atom_insert,
    atom_update,
    face_name_str,
    event_int_str,
    acct_name_str,
    group_label_str,
    parent_road_str,
    item_title_str,
    road_str,
    base_str,
    team_tag_str,
    awardee_tag_str,
    healer_name_str,
    numor_str,
    denom_str,
    addin_str,
    base_item_active_requisite_str,
    begin_str,
    close_str,
    credit_belief_str,
    debtit_belief_str,
    credit_vote_str,
    debtit_vote_str,
    credor_respect_str,
    debtor_respect_str,
    fopen_str,
    fnigh_str,
    gogo_want_str,
    mass_str,
    morph_str,
    pledge_str,
    stop_want_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
    give_force_str,
    take_force_str,
)
from src.f05_fund_metric.fund_metric_config import (
    get_all_fund_metric_args,
    get_fund_metric_args_sqlite_datatype_dict,
)
from src.f08_fisc.fisc_config import (
    get_fisc_args_dimen_mapping,
    get_fisc_config_dict,
    get_fisc_dimens,
    fiscunit_str,
    fisc_dealunit_str,
    fisc_cashbook_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    fisc_timeoffi_str,
    amount_str,
    month_title_str,
    hour_title_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_title_str,
    weekday_order_str,
    offi_time_str,
)
from src.f09_pidgin.pidgin_config import (
    pidginunit_str,
    otx_bridge_str,
    inx_bridge_str,
    unknown_word_str,
    otx_title_str,
    inx_title_str,
    otx_road_str,
    inx_road_str,
    otx_name_str,
    inx_name_str,
    otx_label_str,
    inx_label_str,
    map_otx2inx_str,
    map_name_str,
    map_label_str,
    map_title_str,
    map_road_str,
    get_pidgin_dimens,
    get_pidgin_config_dict,
    get_pidgin_args_dimen_mapping,
)
from src.f10_idea.idea_config import (
    idea_category_str,
    get_idea_categorys,
    get_idea_elements_sort_order,
    get_idea_sqlite_types,
    get_idea_dimen_ref,
    idea_number_str,
    allowed_crud_str,
    attributes_str,
    dimens_str,
    otx_key_str,
    insert_one_time_str,
    insert_mulitple_str,
    delete_insert_update_str,
    insert_update_str,
    delete_insert_str,
    delete_update_str,
    build_order_str,
    get_allowed_curds,
    get_idearef_from_file,
    get_quick_ideas_column_ref,
    config_file_dir,
    get_idea_config_filename,
    get_idea_config_dict,
    get_idea_format_filenames,
    get_idea_format_filename,
    get_idea_numbers,
    idea_format_00021_bud_acctunit_v0_0_0,
    idea_format_00020_bud_acct_membership_v0_0_0,
    idea_format_00013_itemunit_v0_0_0,
)
from os import getcwd as os_getcwd
from copy import copy as copy_copy


def test_str_functions_ReturnObj():
    # ESTABLISH / WHEN / THEN
    assert idea_category_str() == "idea_category"
    assert build_order_str() == "build_order"
    assert idea_number_str() == "idea_number"
    assert allowed_crud_str() == "allowed_crud"
    assert attributes_str() == "attributes"
    assert dimens_str() == "dimens"
    assert otx_key_str() == "otx_key"
    assert insert_one_time_str() == "INSERT_ONE_TIME"
    assert insert_mulitple_str() == "INSERT_MULITPLE"
    assert delete_insert_update_str() == "DELETE_INSERT_UPDATE"
    assert insert_update_str() == "INSERT_UPDATE"
    assert delete_insert_str() == "DELETE_INSERT"
    assert delete_update_str() == "DELETE_UPDATE"

    assert get_idea_categorys() == {"bud", "fisc", "pidgin"}


def test_get_idea_elements_sort_order_ReturnsObj():
    # ESTABLISH / WHEN
    table_sorting_priority = get_idea_elements_sort_order()

    # THEN
    atom_args = set(get_atom_args_dimen_mapping().keys())
    assert atom_args.issubset(set(table_sorting_priority))
    fisc_args = set(get_fisc_args_dimen_mapping().keys())
    print(f"{fisc_args=}")
    print(f"{fisc_args.difference(set(table_sorting_priority))=}")
    assert fisc_args.issubset(set(table_sorting_priority))
    pidgin_args = set(get_pidgin_args_dimen_mapping().keys())
    assert pidgin_args.issubset(set(table_sorting_priority))
    all_bud_dimen_delete_keys = get_all_bud_dimen_delete_keys()
    print(f"missing {all_bud_dimen_delete_keys.difference(table_sorting_priority)}")
    assert all_bud_dimen_delete_keys.issubset(table_sorting_priority)
    fund_metric_args = set(get_all_fund_metric_args().keys())
    # for fund_metric_arg in fund_metric_args.difference(table_sorting_priority):
    #     print(f"{fund_metric_arg=}")
    print(f"{fund_metric_args.difference(table_sorting_priority)=}")
    assert fund_metric_args.issubset(table_sorting_priority)

    assert table_sorting_priority[0] == world_id_str()
    assert table_sorting_priority[1] == idea_number_str()
    assert table_sorting_priority[2] == face_name_str()
    assert table_sorting_priority[3] == event_int_str()
    assert table_sorting_priority[4] == fisc_title_str()
    assert table_sorting_priority[5] == timeline_title_str()
    assert table_sorting_priority[6] == offi_time_str()
    assert table_sorting_priority[7] == c400_number_str()
    assert table_sorting_priority[8] == yr1_jan1_offset_str()
    assert table_sorting_priority[9] == monthday_distortion_str()
    assert table_sorting_priority[10] == cumlative_day_str()
    assert table_sorting_priority[11] == month_title_str()
    assert table_sorting_priority[12] == cumlative_minute_str()
    assert table_sorting_priority[13] == hour_title_str()
    assert table_sorting_priority[14] == weekday_order_str()
    assert table_sorting_priority[15] == weekday_title_str()
    assert table_sorting_priority[16] == owner_name_str()
    assert table_sorting_priority[17] == get_delete_key_name(owner_name_str())
    assert table_sorting_priority[18] == acct_name_str()
    assert table_sorting_priority[19] == get_delete_key_name(acct_name_str())
    assert table_sorting_priority[20] == group_label_str()
    assert table_sorting_priority[21] == get_delete_key_name(group_label_str())
    assert table_sorting_priority[22] == parent_road_str()
    assert table_sorting_priority[23] == get_delete_key_name(parent_road_str())
    assert table_sorting_priority[24] == item_title_str()
    assert table_sorting_priority[25] == get_delete_key_name(item_title_str())
    assert table_sorting_priority[26] == road_str()
    assert table_sorting_priority[27] == get_delete_key_name(road_str())
    assert table_sorting_priority[28] == base_str()
    assert table_sorting_priority[29] == get_delete_key_name(base_str())
    assert table_sorting_priority[30] == f"{base_str()}_EXCISE"
    assert table_sorting_priority[31] == "need"
    assert table_sorting_priority[32] == get_delete_key_name("need")
    assert table_sorting_priority[33] == "pick"
    assert table_sorting_priority[34] == team_tag_str()
    assert table_sorting_priority[35] == get_delete_key_name(team_tag_str())
    assert table_sorting_priority[36] == awardee_tag_str()
    assert table_sorting_priority[37] == get_delete_key_name(awardee_tag_str())
    assert table_sorting_priority[38] == healer_name_str()
    assert table_sorting_priority[39] == get_delete_key_name(healer_name_str())
    assert table_sorting_priority[40] == deal_time_str()
    assert table_sorting_priority[41] == tran_time_str()
    assert table_sorting_priority[42] == begin_str()
    assert table_sorting_priority[43] == close_str()
    assert table_sorting_priority[44] == addin_str()
    assert table_sorting_priority[45] == numor_str()
    assert table_sorting_priority[46] == denom_str()
    assert table_sorting_priority[47] == morph_str()
    assert table_sorting_priority[48] == gogo_want_str()
    assert table_sorting_priority[49] == stop_want_str()
    assert table_sorting_priority[50] == base_item_active_requisite_str()
    assert table_sorting_priority[51] == credit_belief_str()
    assert table_sorting_priority[52] == debtit_belief_str()
    assert table_sorting_priority[53] == credit_vote_str()
    assert table_sorting_priority[54] == debtit_vote_str()
    assert table_sorting_priority[55] == credor_respect_str()
    assert table_sorting_priority[56] == debtor_respect_str()
    assert table_sorting_priority[57] == fopen_str()
    assert table_sorting_priority[58] == fnigh_str()
    assert table_sorting_priority[59] == "fund_pool"
    assert table_sorting_priority[60] == give_force_str()
    assert table_sorting_priority[61] == mass_str()
    assert table_sorting_priority[62] == "max_tree_traverse"
    assert table_sorting_priority[63] == "nigh"
    assert table_sorting_priority[64] == "open"
    assert table_sorting_priority[65] == "divisor"
    assert table_sorting_priority[66] == pledge_str()
    assert table_sorting_priority[67] == "problem_bool"
    assert table_sorting_priority[68] == take_force_str()
    assert table_sorting_priority[69] == "tally"
    assert table_sorting_priority[70] == fund_coin_str()
    assert table_sorting_priority[71] == penny_str()
    assert table_sorting_priority[72] == respect_bit_str()
    assert table_sorting_priority[73] == amount_str()
    assert table_sorting_priority[74] == otx_title_str()
    assert table_sorting_priority[75] == inx_title_str()
    assert table_sorting_priority[76] == otx_road_str()
    assert table_sorting_priority[77] == inx_road_str()
    assert table_sorting_priority[78] == otx_name_str()
    assert table_sorting_priority[79] == inx_name_str()
    assert table_sorting_priority[80] == otx_label_str()
    assert table_sorting_priority[81] == inx_label_str()
    assert table_sorting_priority[82] == otx_bridge_str()
    assert table_sorting_priority[83] == inx_bridge_str()
    assert table_sorting_priority[84] == bridge_str()
    assert table_sorting_priority[85] == unknown_word_str()
    assert table_sorting_priority[86] == quota_str()
    assert table_sorting_priority[87] == celldepth_str()
    assert table_sorting_priority[88] == "error_message"
    assert table_sorting_priority[89] == "_owner_name_team"
    assert table_sorting_priority[90] == "_active"
    assert table_sorting_priority[91] == "_task"
    assert table_sorting_priority[92] == "_status"
    assert table_sorting_priority[93] == "_credor_pool"
    assert table_sorting_priority[94] == "_debtor_pool"
    assert table_sorting_priority[95] == "_rational"
    assert table_sorting_priority[96] == "_fund_give"
    assert table_sorting_priority[97] == "_fund_take"
    assert table_sorting_priority[98] == "_fund_onset"
    assert table_sorting_priority[99] == "_fund_cease"
    assert table_sorting_priority[100] == "_fund_ratio"
    assert table_sorting_priority[101] == "_fund_agenda_give"
    assert table_sorting_priority[102] == "_fund_agenda_take"
    assert table_sorting_priority[103] == "_fund_agenda_ratio_give"
    assert table_sorting_priority[104] == "_fund_agenda_ratio_take"
    assert table_sorting_priority[105] == "_inallocable_debtit_belief"
    assert table_sorting_priority[106] == "_gogo_calc"
    assert table_sorting_priority[107] == "_stop_calc"
    assert table_sorting_priority[108] == "_level"
    assert table_sorting_priority[109] == "_range_evaluated"
    assert table_sorting_priority[110] == "_descendant_pledge_count"
    assert table_sorting_priority[111] == "_healerlink_ratio"
    assert table_sorting_priority[112] == "_all_acct_cred"
    assert table_sorting_priority[113] == "_keeps_justified"
    assert table_sorting_priority[114] == "_offtrack_fund"
    assert table_sorting_priority[115] == "_base_item_active_value"
    assert table_sorting_priority[116] == "_irrational_debtit_belief"
    assert table_sorting_priority[117] == "_sum_healerlink_share"
    assert table_sorting_priority[118] == "_keeps_buildable"
    assert table_sorting_priority[119] == "_all_acct_debt"
    assert table_sorting_priority[120] == "_tree_traverse_count"
    assert len(table_sorting_priority) == 121
    all_args = copy_copy(atom_args)
    all_args.update(all_bud_dimen_delete_keys)
    all_args.update(fisc_args)
    all_args.update(pidgin_args)
    all_args.update(fund_metric_args)
    all_args.add(idea_number_str())
    all_args.add(event_int_str())
    all_args.add(face_name_str())
    all_args.add("error_message")
    all_args.add(f"{base_str()}_EXCISE")
    assert all_args == set(table_sorting_priority)

    x_no_underscore_set = {x_arg.replace("_", "") for x_arg in table_sorting_priority}
    # x_dict = {}
    # for x_arg in sorted(table_sorting_priority):
    #     y_arg = x_arg.replace("_", "")
    #     if x_dict.get(y_arg) is None:
    #         x_dict[y_arg] = 0
    #     x_dict[y_arg] = x_dict.get(y_arg) + 1
    # print(f"{x_dict=}")
    assert len(x_no_underscore_set) == len(table_sorting_priority)


def test_get_idea_sqlite_types_ReturnsObj():
    # ESTABLISH / WHEN
    sqlite_types = get_idea_sqlite_types()

    # THEN
    assert set(sqlite_types.keys()) == set(get_idea_elements_sort_order())
    assert sqlite_types.get(idea_number_str()) == "TEXT"
    assert sqlite_types.get(face_name_str()) == "TEXT"
    assert sqlite_types.get(event_int_str()) == "INTEGER"
    assert sqlite_types.get(fisc_title_str()) == "TEXT"
    assert sqlite_types.get(owner_name_str()) == "TEXT"
    assert sqlite_types.get(acct_name_str()) == "TEXT"
    assert sqlite_types.get(group_label_str()) == "TEXT"
    assert sqlite_types.get(parent_road_str()) == "TEXT"
    assert sqlite_types.get(item_title_str()) == "TEXT"
    assert sqlite_types.get(road_str()) == "TEXT"
    assert sqlite_types.get(base_str()) == "TEXT"
    assert sqlite_types.get("need") == "TEXT"
    assert sqlite_types.get("pick") == "TEXT"
    assert sqlite_types.get(team_tag_str()) == "TEXT"
    assert sqlite_types.get(awardee_tag_str()) == "TEXT"
    assert sqlite_types.get(healer_name_str()) == "TEXT"
    assert sqlite_types.get(offi_time_str()) == "INTEGER"
    assert sqlite_types.get(deal_time_str()) == "INTEGER"
    assert sqlite_types.get(tran_time_str()) == "INTEGER"
    assert sqlite_types.get(begin_str()) == "REAL"
    assert sqlite_types.get(close_str()) == "REAL"
    assert sqlite_types.get(addin_str()) == "REAL"
    assert sqlite_types.get(numor_str()) == "INTEGER"
    assert sqlite_types.get(denom_str()) == "INTEGER"
    assert sqlite_types.get(morph_str()) == "INTEGER"
    assert sqlite_types.get(gogo_want_str()) == "REAL"
    assert sqlite_types.get(stop_want_str()) == "REAL"
    assert sqlite_types.get(base_item_active_requisite_str()) == "INTEGER"
    assert sqlite_types.get(credit_belief_str()) == "REAL"
    assert sqlite_types.get(debtit_belief_str()) == "REAL"
    assert sqlite_types.get(credit_vote_str()) == "REAL"
    assert sqlite_types.get(debtit_vote_str()) == "REAL"
    assert sqlite_types.get(credor_respect_str()) == "REAL"
    assert sqlite_types.get(debtor_respect_str()) == "REAL"
    assert sqlite_types.get(fopen_str()) == "REAL"
    assert sqlite_types.get(fnigh_str()) == "REAL"
    assert sqlite_types.get("fund_pool") == "REAL"
    assert sqlite_types.get(give_force_str()) == "REAL"
    assert sqlite_types.get(mass_str()) == "INTEGER"
    assert sqlite_types.get("max_tree_traverse") == "INTEGER"
    assert sqlite_types.get("nigh") == "REAL"
    assert sqlite_types.get("open") == "REAL"
    assert sqlite_types.get("divisor") == "INTEGER"
    assert sqlite_types.get("problem_bool") == "INTEGER"
    assert sqlite_types.get(take_force_str()) == "REAL"
    assert sqlite_types.get("tally") == "INTEGER"
    assert sqlite_types.get(fund_coin_str()) == "REAL"
    assert sqlite_types.get(penny_str()) == "REAL"
    assert sqlite_types.get(pledge_str()) == "INTEGER"
    assert sqlite_types.get(respect_bit_str()) == "REAL"
    assert sqlite_types.get(amount_str()) == "REAL"
    assert sqlite_types.get(month_title_str()) == "TEXT"
    assert sqlite_types.get(hour_title_str()) == "TEXT"
    assert sqlite_types.get(cumlative_minute_str()) == "INTEGER"
    assert sqlite_types.get(cumlative_day_str()) == "INTEGER"
    assert sqlite_types.get(weekday_title_str()) == "TEXT"
    assert sqlite_types.get(weekday_order_str()) == "INTEGER"
    assert sqlite_types.get(otx_bridge_str()) == "TEXT"
    assert sqlite_types.get(inx_bridge_str()) == "TEXT"
    assert sqlite_types.get(unknown_word_str()) == "TEXT"
    assert sqlite_types.get(bridge_str()) == "TEXT"
    assert sqlite_types.get(c400_number_str()) == "INTEGER"
    assert sqlite_types.get(yr1_jan1_offset_str()) == "INTEGER"
    assert sqlite_types.get(quota_str()) == "REAL"
    assert sqlite_types.get(celldepth_str()) == "INT"
    assert sqlite_types.get(monthday_distortion_str()) == "INTEGER"
    assert sqlite_types.get(timeline_title_str()) == "TEXT"
    assert sqlite_types.get("error_message") == "TEXT"

    # sourcery skip: no-loop-in-tests
    for x_arg, datatype in get_fund_metric_args_sqlite_datatype_dict().items():
        print(f"{x_arg=} {datatype=} {sqlite_types.get(x_arg)=}")
        assert sqlite_types.get(x_arg) == datatype


def test_get_allowed_curds_ReturnObj():
    # ESTABLISH / WHEN / THEN
    assert get_allowed_curds() == {
        insert_one_time_str(),
        insert_mulitple_str(),
        delete_insert_update_str(),
        insert_update_str(),
        delete_insert_str(),
        delete_update_str(),
        atom_insert(),
        atom_delete(),
        atom_update(),
    }


def test_get_idea_config_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_idea_config_filename() == "idea_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "f10_idea")


def test_get_idea_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    x_idea_config = get_idea_config_dict()

    # THEN
    assert x_idea_config
    idea_config_dimens = set(x_idea_config.keys())
    assert fiscunit_str() in idea_config_dimens
    assert fisc_dealunit_str() in idea_config_dimens
    assert fisc_cashbook_str() in idea_config_dimens
    assert fisc_timeline_hour_str() in idea_config_dimens
    assert fisc_timeline_month_str() in idea_config_dimens
    assert fisc_timeline_weekday_str() in idea_config_dimens
    assert fisc_timeoffi_str() in idea_config_dimens
    assert bud_acct_membership_str() in idea_config_dimens
    assert bud_acctunit_str() in idea_config_dimens
    assert bud_item_awardlink_str() in idea_config_dimens
    assert bud_item_factunit_str() in idea_config_dimens
    assert bud_item_teamlink_str() in idea_config_dimens
    assert bud_item_healerlink_str() in idea_config_dimens
    assert bud_item_reason_premiseunit_str() in idea_config_dimens
    assert bud_item_reasonunit_str() in idea_config_dimens
    assert bud_itemunit_str() in idea_config_dimens
    assert budunit_str() in idea_config_dimens
    assert map_name_str() in idea_config_dimens
    assert map_label_str() in idea_config_dimens
    assert map_title_str() in idea_config_dimens
    assert map_road_str() in idea_config_dimens
    assert get_bud_dimens().issubset(idea_config_dimens)
    assert get_fisc_dimens().issubset(idea_config_dimens)
    assert get_pidgin_dimens().issubset(idea_config_dimens)
    assert len(x_idea_config) == 21
    _validate_idea_config(x_idea_config)


def _validate_idea_config(x_idea_config: dict):
    atom_config_dict = get_atom_config_dict()
    fisc_config_dict = get_fisc_config_dict()
    pidgin_config_dict = get_pidgin_config_dict()
    # for every idea_format file there exists a unique idea_number always with leading zeros to make 5 digits
    for idea_dimen, idea_dict in x_idea_config.items():
        print(f"{idea_dimen=}")
        assert idea_dict.get(idea_category_str()) in get_idea_categorys()
        assert idea_dict.get(jkeys_str()) is not None
        assert idea_dict.get(jvalues_str()) is not None
        assert idea_dict.get(allowed_crud_str()) is not None
        assert idea_dict.get(atom_update()) is None
        assert idea_dict.get(atom_insert()) is None
        assert idea_dict.get(atom_delete()) is None
        assert idea_dict.get(normal_specs_str()) is None
        if idea_dict.get(idea_category_str()) == "bud":
            sub_dimen = atom_config_dict.get(idea_dimen)
        elif idea_dict.get(idea_category_str()) == "fisc":
            sub_dimen = fisc_config_dict.get(idea_dimen)
        elif idea_dict.get(idea_category_str()) == "pidgin":
            sub_dimen = pidgin_config_dict.get(idea_dimen)

        assert idea_dict.get(allowed_crud_str()) in get_allowed_curds()

        if idea_dimen in {
            fisc_timeline_hour_str(),
            fisc_timeline_month_str(),
            fisc_timeline_weekday_str(),
            fiscunit_str(),
            map_otx2inx_str(),
            map_label_str(),
            map_name_str(),
            map_title_str(),
            map_road_str(),
        }:
            assert idea_dict.get(allowed_crud_str()) == insert_one_time_str()
        elif idea_dimen in {
            fisc_dealunit_str(),
            fisc_cashbook_str(),
            fisc_timeoffi_str(),
        }:
            assert idea_dict.get(allowed_crud_str()) == insert_mulitple_str()
        elif (
            sub_dimen.get(atom_update()) != None
            and sub_dimen.get(atom_insert()) != None
            and sub_dimen.get(atom_delete()) != None
        ):
            assert idea_dict.get(allowed_crud_str()) == delete_insert_update_str()
        elif (
            sub_dimen.get(atom_update()) != None
            and sub_dimen.get(atom_insert()) != None
            and sub_dimen.get(atom_delete()) is None
        ):
            assert idea_dict.get(allowed_crud_str()) == insert_update_str()
        elif (
            sub_dimen.get(atom_update()) is None
            and sub_dimen.get(atom_insert()) != None
            and sub_dimen.get(atom_delete()) != None
        ):
            assert idea_dict.get(allowed_crud_str()) == delete_insert_str()
        elif (
            sub_dimen.get(atom_update()) != None
            and sub_dimen.get(atom_insert()) is None
            and sub_dimen.get(atom_delete()) != None
        ):
            assert idea_dict.get(allowed_crud_str()) == delete_update_str()
        elif (
            sub_dimen.get(atom_update()) != None
            and sub_dimen.get(atom_insert()) is None
            and sub_dimen.get(atom_delete()) is None
        ):
            assert idea_dict.get(allowed_crud_str()) == atom_update()
        elif (
            sub_dimen.get(atom_update()) is None
            and sub_dimen.get(atom_insert()) != None
            and sub_dimen.get(atom_delete()) is None
        ):
            assert idea_dict.get(allowed_crud_str()) == atom_insert()
        elif (
            sub_dimen.get(atom_update()) is None
            and sub_dimen.get(atom_insert()) is None
            and sub_dimen.get(atom_delete()) != None
        ):
            assert idea_dict.get(allowed_crud_str()) == atom_delete()
        else:
            test_str = f"{allowed_crud_str()} not checked by test"
            assert idea_dict.get(allowed_crud_str()) == test_str

        sub_jkeys_keys = set(sub_dimen.get(jkeys_str()).keys())
        idea_jkeys_keys = set(idea_dict.get(jkeys_str()).keys())
        # print(f"    {sub_jkeys_keys=}")
        # print(f"  {idea_jkeys_keys=}")
        assert face_name_str() in idea_jkeys_keys
        assert event_int_str() in idea_jkeys_keys
        if idea_dict.get(idea_category_str()) != "pidgin":
            assert fisc_title_str() in idea_jkeys_keys
        if idea_dict.get(idea_category_str()) == "bud":
            idea_jkeys_keys.remove(fisc_title_str())
            idea_jkeys_keys.remove(owner_name_str())
        idea_jkeys_keys.remove(face_name_str())
        idea_jkeys_keys.remove(event_int_str())
        assert sub_jkeys_keys == idea_jkeys_keys

        sub_jvalues_keys = set(sub_dimen.get(jvalues_str()).keys())
        print(f"  {sub_jvalues_keys=}")
        if fisc_title_str() in sub_jvalues_keys:
            sub_jvalues_keys.remove(fisc_title_str())

        idea_jvalues_dict = idea_dict.get(jvalues_str())
        idea_jvalues_keys = set(idea_jvalues_dict.keys())
        # print(f"  {sub_jvalues_keys=}")
        # print(f"{idea_jvalues_keys=}")
        assert sub_jvalues_keys == idea_jvalues_keys

        assert fisc_title_str() not in idea_jvalues_keys

        # sort_list = get_idea_elements_sort_order()
        # x_count = 0
        # sort_dict1 = {}
        # sort_dict2 = {}
        # for idea_arg in sort_list:
        #     sort_dict1[x_count] = idea_arg
        #     sort_dict1[idea_arg] = x_count

        # for jvalue in idea_jvalues_keys:
        #     print(f"{jvalue=} {idea_jvalues_dict=}")
        #     jvalue_dict = idea_jvalues_dict.get(jvalue)
        #     jvalue_column_order = jvalue_dict.get(column_order_str())
        #     assert jvalue_column_order != None
        #     list_ref_arg = sort_list[jvalue_column_order]
        #     assert list_ref_arg != None
        #     assert jvalue == list_ref_arg

        # # for jkey in idea_jkeys_keys:
        #     print(f"{jkey=} {idea_jkeys_dict=}")
        #     jkey_dict = idea_jkeys_dict.get(jkey)
        #     jkey_column_order = jkey_dict.get(column_order_str())
        #     assert jkey_column_order != None
        #     list_ref_arg = sort_list[jkey_column_order]
        #     assert list_ref_arg != None
        #     assert jkey == list_ref_arg


def test_get_idea_format_filenames_ReturnsObj():
    # ESTABLISH
    idea_filenames_set = get_idea_format_filenames()
    idea_filenames_sorted = list(idea_filenames_set)
    idea_filenames_sorted.sort(key=lambda x: x)
    print(idea_filenames_sorted)

    # THEN
    assert idea_format_00021_bud_acctunit_v0_0_0() in idea_filenames_set
    assert idea_format_00020_bud_acct_membership_v0_0_0() in idea_filenames_set
    assert idea_format_00013_itemunit_v0_0_0() in idea_filenames_set

    # WHEN / THEN
    assert _validate_idea_format_files(idea_filenames_sorted)


def _validate_idea_format_files(idea_filenames: set[str]):
    valid_idea_dimens = set()
    valid_idea_dimens.update(get_bud_dimens())
    valid_idea_dimens.update(get_fisc_dimens())
    valid_idea_dimens.update(get_pidgin_dimens())
    config_dict = get_idea_config_dict()

    # for every idea_format file there exists a unique idea_number always with leading zeros to make 5 digits
    idea_numbers_set = set()
    for idea_filename in idea_filenames:
        ref_dict = get_idearef_from_file(idea_filename)
        print(f"{idea_filename=} {ref_dict.get(idea_number_str())=}")
        idea_number_value = ref_dict.get(idea_number_str())
        assert idea_number_value
        assert idea_number_value[2:8] == idea_filename[12:17]
        idea_numbers_set.add(idea_number_value)

        format_dimens = ref_dict.get(dimens_str())
        assert format_dimens is not None
        assert len(format_dimens) > 0
        for idea_format_dimen in format_dimens:
            assert idea_format_dimen in valid_idea_dimens

        assert ref_dict.get(attributes_str()) is not None
        idea_format_attributes = ref_dict.get(attributes_str())
        for idea_attribute, attr_dict in idea_format_attributes.items():
            assert otx_key_str() in set(attr_dict.keys())
            otx_key_value = attr_dict.get(otx_key_str())
            for idea_format_dimen in format_dimens:
                format_config = config_dict.get(idea_format_dimen)
                dimen_required_keys = set(format_config.get(jkeys_str()).keys())
                dimen_optional_keys = set(format_config.get(jvalues_str()).keys())
                attr_in_required = idea_attribute in dimen_required_keys
                attr_in_optional = idea_attribute in dimen_optional_keys
                attr_in_keys = attr_in_required or attr_in_optional
                assert_fail_str = (
                    f"{idea_format_dimen=} {idea_attribute=} {otx_key_value=}"
                )
                if attr_in_keys and otx_key_value:
                    assert attr_in_required, assert_fail_str
                elif attr_in_keys:
                    assert attr_in_optional, assert_fail_str

    # assert face_name_str() in idea_format_attributes
    # assert event_int_str() in idea_format_attributes

    # confirm every ideanumber is unique
    assert len(idea_numbers_set) == len(idea_filenames)
    assert idea_numbers_set == get_idea_numbers()

    return True


def test_get_idea_format_filename_ReturnsObj():
    # ESTABLISH
    br00021_str = "br00021"
    br00020_str = "br00020"
    br00013_str = "br00013"

    # WHEN
    br00021_filename = get_idea_format_filename(br00021_str)
    br00020_filename = get_idea_format_filename(br00020_str)
    br00013_filename = get_idea_format_filename(br00013_str)

    # THEN
    assert br00021_filename == idea_format_00021_bud_acctunit_v0_0_0()
    assert br00020_filename == idea_format_00020_bud_acct_membership_v0_0_0()
    assert br00013_filename == idea_format_00013_itemunit_v0_0_0()

    all_set = {get_idea_format_filename(br) for br in get_idea_numbers()}
    assert all_set == get_idea_format_filenames()


def set_idea_config_json(dimen: str, build_order: int):
    x_idea_config = get_idea_config_dict()
    dimen_dict = x_idea_config.get(dimen)
    dimen_dict[build_order_str()] = build_order
    x_idea_config[dimen] = dimen_dict
    save_json(config_file_dir(), get_idea_config_filename(), x_idea_config)


def test_get_idea_config_dict_ReturnsObj_build_order():
    # ESTABLISH / WHEN
    bo = build_order_str()
    # set_idea_config_json(map_name_str(), 0)
    # set_idea_config_json(map_label_str(), 1)
    # set_idea_config_json(map_title_str(), 2)
    # set_idea_config_json(map_road_str(), 3)
    # set_idea_config_json(fiscunit_str(), 5)
    # set_idea_config_json(fisc_timeline_hour_str(), 6)
    # set_idea_config_json(fisc_timeline_month_str(), 7)
    # set_idea_config_json(fisc_timeline_weekday_str(), 8)
    # set_idea_config_json(bud_acct_membership_str(), 9)
    # set_idea_config_json(bud_acctunit_str(), 10)
    # set_idea_config_json(bud_item_awardlink_str(), 11)
    # set_idea_config_json(bud_item_factunit_str(), 12)
    # set_idea_config_json(bud_item_teamlink_str(), 14)
    # set_idea_config_json(bud_item_healerlink_str(), 15)
    # set_idea_config_json(bud_item_reason_premiseunit_str(), 16)
    # set_idea_config_json(bud_item_reasonunit_str(), 17)
    # set_idea_config_json(bud_itemunit_str(), 18)
    # set_idea_config_json(budunit_str(), 19)
    # set_idea_config_json(fisc_dealunit_str(), 20)
    # set_idea_config_json(fisc_cashbook_str(), 21)

    x_idea_config = get_idea_config_dict()

    # THEN
    assert x_idea_config.get(map_name_str()).get(bo) == 0
    assert x_idea_config.get(map_label_str()).get(bo) == 1
    assert x_idea_config.get(map_title_str()).get(bo) == 2
    assert x_idea_config.get(map_road_str()).get(bo) == 3
    assert x_idea_config.get(fiscunit_str()).get(bo) == 5
    assert x_idea_config.get(fisc_timeline_hour_str()).get(bo) == 6
    assert x_idea_config.get(fisc_timeline_month_str()).get(bo) == 7
    assert x_idea_config.get(fisc_timeline_weekday_str()).get(bo) == 8
    assert x_idea_config.get(bud_acct_membership_str()).get(bo) == 9
    assert x_idea_config.get(bud_acctunit_str()).get(bo) == 10
    assert x_idea_config.get(bud_item_awardlink_str()).get(bo) == 11
    assert x_idea_config.get(bud_item_factunit_str()).get(bo) == 12
    assert x_idea_config.get(bud_item_teamlink_str()).get(bo) == 14
    assert x_idea_config.get(bud_item_healerlink_str()).get(bo) == 15
    assert x_idea_config.get(bud_item_reason_premiseunit_str()).get(bo) == 16
    assert x_idea_config.get(bud_item_reasonunit_str()).get(bo) == 17
    assert x_idea_config.get(bud_itemunit_str()).get(bo) == 18
    assert x_idea_config.get(budunit_str()).get(bo) == 19
    assert x_idea_config.get(fisc_dealunit_str()).get(bo) == 20
    assert x_idea_config.get(fisc_cashbook_str()).get(bo) == 21


def test_get_quick_ideas_column_ref_ReturnsObj():
    # ESTABLISH / WHEN
    x_idea_quick_column_ref = get_quick_ideas_column_ref()

    # THEN
    assert len(x_idea_quick_column_ref) == len(get_idea_numbers())
    assert x_idea_quick_column_ref.get("br00000") == {
        face_name_str(),
        event_int_str(),
        c400_number_str(),
        fisc_title_str(),
        fund_coin_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        bridge_str(),
        timeline_title_str(),
        yr1_jan1_offset_str(),
    }


def _create_expected_idea_dimen_ref() -> dict[str, list[str]]:
    idea_numbers_sorted = list(get_idea_numbers())
    idea_numbers_sorted.sort(key=lambda x: x)
    expected_idea_dimen_ref = {}
    for idea_number in idea_numbers_sorted:
        idea_format_filename = get_idea_format_filename(idea_number)
        x_idearef = get_idearef_from_file(idea_format_filename)
        dimens_list = x_idearef.get(dimens_str())
        for x_dimen in dimens_list:
            if expected_idea_dimen_ref.get(x_dimen) is None:
                expected_idea_dimen_ref[x_dimen] = [idea_number]
            else:
                expected_idea_dimen_ref.get(x_dimen).append(idea_number)
    return expected_idea_dimen_ref


def test_get_idea_dimen_ref_ReturnsObj():
    # ESTABLISH
    expected_idea_dimen_ref = _create_expected_idea_dimen_ref()
    print(f"{expected_idea_dimen_ref=}")

    # WHEN / THEN
    assert get_idea_dimen_ref() == expected_idea_dimen_ref
