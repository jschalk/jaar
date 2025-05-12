from src.a00_data_toolbox.file_toolbox import save_json, create_path
from src.a02_finance_logic._utils.strs_a02 import (
    quota_str,
    deal_time_str,
    tran_time_str,
    bridge_str,
    celldepth_str,
    owner_name_str,
    fisc_tag_str,
    world_id_str,
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
    acct_name_str,
    addin_str,
    awardee_label_str,
    base_str,
    base_item_active_requisite_str,
    begin_str,
    denom_str,
    event_int_str,
    face_name_str,
    fbase_str,
    fneed_str,
    group_label_str,
    healer_name_str,
    item_way_str,
    numor_str,
    team_label_str,
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
    need_str,
    pledge_str,
    stop_want_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
    give_force_str,
    take_force_str,
    nigh_str,
    open_str,
)
from src.a07_calendar_logic._utils.str_a07 import (
    c400_number_str,
    monthday_distortion_str,
    timeline_tag_str,
    yr1_jan1_offset_str,
)
from src.a08_bud_atom_logic._utils.str_a08 import (
    jkeys_str,
    jvalues_str,
    normal_specs_str,
    column_order_str,
    atom_delete,
    atom_insert,
    atom_update,
)
from src.a08_bud_atom_logic.atom_config import (
    get_atom_args_dimen_mapping,
    get_atom_config_dict,
    get_bud_dimens,
    get_delete_key_name,
    get_all_bud_dimen_delete_keys,
)
from src.a10_bud_calc.bud_calc_config import (
    get_all_bud_calc_args,
    get_bud_calc_args_sqlite_datatype_dict,
)
from src.a15_fisc_logic._utils.str_a15 import (
    fiscunit_str,
    fisc_dealunit_str,
    fisc_cashbook_str,
    fisc_timeline_hour_str,
    fisc_timeline_month_str,
    fisc_timeline_weekday_str,
    fisc_timeoffi_str,
    amount_str,
    month_tag_str,
    hour_tag_str,
    cumlative_minute_str,
    cumlative_day_str,
    weekday_tag_str,
    weekday_order_str,
    offi_time_str,
)
from src.a15_fisc_logic.fisc_config import (
    get_fisc_args_dimen_mapping,
    get_fisc_config_dict,
    get_fisc_dimens,
)
from src.a16_pidgin_logic._utils.str_a16 import (
    pidginunit_str,
    otx_bridge_str,
    inx_bridge_str,
    unknown_word_str,
    otx_tag_str,
    inx_tag_str,
    otx_way_str,
    inx_way_str,
    otx_name_str,
    inx_name_str,
    otx_label_str,
    inx_label_str,
    map_otx2inx_str,
    pidgin_name_str,
    pidgin_label_str,
    pidgin_tag_str,
    pidgin_way_str,
)
from src.a16_pidgin_logic.pidgin_config import (
    get_pidgin_dimens,
    get_pidgin_config_dict,
    get_pidgin_args_dimen_mapping,
)
from src.a17_creed_logic._utils.str_a17 import (
    creed_category_str,
    get_creed_categorys,
    creed_number_str,
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
)
from src.a17_creed_logic.creed_config import (
    get_creed_elements_sort_order,
    get_creed_sqlite_types,
    get_creed_dimen_ref,
    get_allowed_curds,
    get_creedref_from_file,
    get_quick_creeds_column_ref,
    config_file_dir,
    get_creed_config_filename,
    get_creed_config_dict,
    get_creed_format_filenames,
    get_creed_format_filename,
    get_creed_numbers,
    get_default_sorted_list,
    creed_format_00021_bud_acctunit_v0_0_0,
    creed_format_00020_bud_acct_membership_v0_0_0,
    creed_format_00013_itemunit_v0_0_0,
)
from os import getcwd as os_getcwd
from copy import copy as copy_copy


def test_str_functions_ReturnObj():
    # ESTABLISH / WHEN / THEN
    assert creed_category_str() == "creed_category"
    assert build_order_str() == "build_order"
    assert creed_number_str() == "creed_number"
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

    assert get_creed_categorys() == {"bud", "fisc", "pidgin"}


def test_get_creed_elements_sort_order_ReturnsObj():
    # ESTABLISH / WHEN
    table_sorting_priority = get_creed_elements_sort_order()

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
    bud_calc_args = set(get_all_bud_calc_args().keys())
    # for bud_calc_arg in bud_calc_args.difference(table_sorting_priority):
    #     print(f"{bud_calc_arg=}")
    print(f"{bud_calc_args.difference(table_sorting_priority)=}")
    assert bud_calc_args.issubset(table_sorting_priority)

    assert table_sorting_priority[0] == world_id_str()
    assert table_sorting_priority[1] == creed_number_str()
    assert table_sorting_priority[2] == "source_dimen"
    assert table_sorting_priority[3] == "pidgin_event_int"
    assert table_sorting_priority[4] == event_int_str()
    assert table_sorting_priority[5] == face_name_str()
    assert table_sorting_priority[6] == fisc_tag_str()
    assert table_sorting_priority[7] == timeline_tag_str()
    assert table_sorting_priority[8] == offi_time_str()
    assert table_sorting_priority[9] == c400_number_str()
    assert table_sorting_priority[10] == yr1_jan1_offset_str()
    assert table_sorting_priority[11] == monthday_distortion_str()
    assert table_sorting_priority[12] == cumlative_day_str()
    assert table_sorting_priority[13] == month_tag_str()
    assert table_sorting_priority[14] == cumlative_minute_str()
    assert table_sorting_priority[15] == hour_tag_str()
    assert table_sorting_priority[16] == weekday_order_str()
    assert table_sorting_priority[17] == weekday_tag_str()
    assert table_sorting_priority[18] == owner_name_str()
    assert table_sorting_priority[19] == get_delete_key_name(owner_name_str())
    assert table_sorting_priority[20] == acct_name_str()
    assert table_sorting_priority[21] == get_delete_key_name(acct_name_str())
    assert table_sorting_priority[22] == group_label_str()
    assert table_sorting_priority[23] == get_delete_key_name(group_label_str())
    assert table_sorting_priority[24] == item_way_str()
    assert table_sorting_priority[25] == get_delete_key_name(item_way_str())
    assert table_sorting_priority[26] == base_str()
    assert table_sorting_priority[27] == get_delete_key_name(base_str())
    assert table_sorting_priority[28] == fbase_str()
    assert table_sorting_priority[29] == get_delete_key_name(fbase_str())
    assert table_sorting_priority[30] == need_str()
    assert table_sorting_priority[31] == get_delete_key_name(need_str())
    assert table_sorting_priority[32] == fneed_str()
    assert table_sorting_priority[33] == team_label_str()
    assert table_sorting_priority[34] == get_delete_key_name(team_label_str())
    assert table_sorting_priority[35] == awardee_label_str()
    assert table_sorting_priority[36] == get_delete_key_name(awardee_label_str())
    assert table_sorting_priority[37] == healer_name_str()
    assert table_sorting_priority[38] == get_delete_key_name(healer_name_str())
    assert table_sorting_priority[39] == deal_time_str()
    assert table_sorting_priority[40] == tran_time_str()
    assert table_sorting_priority[41] == begin_str()
    assert table_sorting_priority[42] == close_str()
    assert table_sorting_priority[43] == addin_str()
    assert table_sorting_priority[44] == numor_str()
    assert table_sorting_priority[45] == denom_str()
    assert table_sorting_priority[46] == morph_str()
    assert table_sorting_priority[47] == gogo_want_str()
    assert table_sorting_priority[48] == stop_want_str()
    assert table_sorting_priority[49] == base_item_active_requisite_str()
    assert table_sorting_priority[50] == credit_belief_str()
    assert table_sorting_priority[51] == debtit_belief_str()
    assert table_sorting_priority[52] == credit_vote_str()
    assert table_sorting_priority[53] == debtit_vote_str()
    assert table_sorting_priority[54] == credor_respect_str()
    assert table_sorting_priority[55] == debtor_respect_str()
    assert table_sorting_priority[56] == fopen_str()
    assert table_sorting_priority[57] == fnigh_str()
    assert table_sorting_priority[58] == "fund_pool"
    assert table_sorting_priority[59] == give_force_str()
    assert table_sorting_priority[60] == mass_str()
    assert table_sorting_priority[61] == "max_tree_traverse"
    assert table_sorting_priority[62] == nigh_str()
    assert table_sorting_priority[63] == open_str()
    assert table_sorting_priority[64] == "divisor"
    assert table_sorting_priority[65] == pledge_str()
    assert table_sorting_priority[66] == "problem_bool"
    assert table_sorting_priority[67] == take_force_str()
    assert table_sorting_priority[68] == "tally"
    assert table_sorting_priority[69] == fund_coin_str()
    assert table_sorting_priority[70] == penny_str()
    assert table_sorting_priority[71] == respect_bit_str()
    assert table_sorting_priority[72] == amount_str()
    assert table_sorting_priority[73] == otx_tag_str()
    assert table_sorting_priority[74] == inx_tag_str()
    assert table_sorting_priority[75] == otx_way_str()
    assert table_sorting_priority[76] == inx_way_str()
    assert table_sorting_priority[77] == otx_name_str()
    assert table_sorting_priority[78] == inx_name_str()
    assert table_sorting_priority[79] == otx_label_str()
    assert table_sorting_priority[80] == inx_label_str()
    assert table_sorting_priority[81] == otx_bridge_str()
    assert table_sorting_priority[82] == inx_bridge_str()
    assert table_sorting_priority[83] == bridge_str()
    assert table_sorting_priority[84] == unknown_word_str()
    assert table_sorting_priority[85] == quota_str()
    assert table_sorting_priority[86] == celldepth_str()
    assert table_sorting_priority[87] == "job_listen_rotations"
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
    all_args.update(bud_calc_args)
    all_args.add(creed_number_str())
    all_args.add(event_int_str())
    all_args.add(face_name_str())
    all_args.add("source_dimen")
    all_args.add("pidgin_event_int")
    all_args.add("error_message")
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


def test_get_creed_sqlite_types_ReturnsObj():
    # ESTABLISH / WHEN
    sqlite_types = get_creed_sqlite_types()

    # THEN
    assert set(sqlite_types.keys()) == set(get_creed_elements_sort_order())
    assert sqlite_types.get(creed_number_str()) == "TEXT"
    assert sqlite_types.get(face_name_str()) == "TEXT"
    assert sqlite_types.get("pidgin_event_int") == "INTEGER"
    assert sqlite_types.get(event_int_str()) == "INTEGER"
    assert sqlite_types.get(fisc_tag_str()) == "TEXT"
    assert sqlite_types.get(owner_name_str()) == "TEXT"
    assert sqlite_types.get(acct_name_str()) == "TEXT"
    assert sqlite_types.get(group_label_str()) == "TEXT"
    assert sqlite_types.get(item_way_str()) == "TEXT"
    assert sqlite_types.get(base_str()) == "TEXT"
    assert sqlite_types.get("need") == "TEXT"
    assert sqlite_types.get("fneed") == "TEXT"
    assert sqlite_types.get(team_label_str()) == "TEXT"
    assert sqlite_types.get(awardee_label_str()) == "TEXT"
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
    assert sqlite_types.get(month_tag_str()) == "TEXT"
    assert sqlite_types.get(hour_tag_str()) == "TEXT"
    assert sqlite_types.get(cumlative_minute_str()) == "INTEGER"
    assert sqlite_types.get(cumlative_day_str()) == "INTEGER"
    assert sqlite_types.get(weekday_tag_str()) == "TEXT"
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
    assert sqlite_types.get(timeline_tag_str()) == "TEXT"
    assert sqlite_types.get("error_message") == "TEXT"

    # sourcery skip: no-loop-in-tests
    for x_arg, datatype in get_bud_calc_args_sqlite_datatype_dict().items():
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


def test_get_creed_config_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_creed_config_filename() == "creed_config.json"


def test_config_file_dir_ReturnsObj() -> str:
    src_dir = create_path(os_getcwd(), "src")
    assert config_file_dir() == create_path(src_dir, "a17_creed_logic")


def test_get_creed_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    x_creed_config = get_creed_config_dict()

    # THEN
    assert x_creed_config
    creed_config_dimens = set(x_creed_config.keys())
    assert fiscunit_str() in creed_config_dimens
    assert fisc_dealunit_str() in creed_config_dimens
    assert fisc_cashbook_str() in creed_config_dimens
    assert fisc_timeline_hour_str() in creed_config_dimens
    assert fisc_timeline_month_str() in creed_config_dimens
    assert fisc_timeline_weekday_str() in creed_config_dimens
    assert fisc_timeoffi_str() in creed_config_dimens
    assert bud_acct_membership_str() in creed_config_dimens
    assert bud_acctunit_str() in creed_config_dimens
    assert bud_item_awardlink_str() in creed_config_dimens
    assert bud_item_factunit_str() in creed_config_dimens
    assert bud_item_teamlink_str() in creed_config_dimens
    assert bud_item_healerlink_str() in creed_config_dimens
    assert bud_item_reason_premiseunit_str() in creed_config_dimens
    assert bud_item_reasonunit_str() in creed_config_dimens
    assert bud_itemunit_str() in creed_config_dimens
    assert budunit_str() in creed_config_dimens
    assert pidgin_name_str() in creed_config_dimens
    assert pidgin_label_str() in creed_config_dimens
    assert pidgin_tag_str() in creed_config_dimens
    assert pidgin_way_str() in creed_config_dimens
    assert get_bud_dimens().issubset(creed_config_dimens)
    assert get_fisc_dimens().issubset(creed_config_dimens)
    assert get_pidgin_dimens().issubset(creed_config_dimens)
    assert len(x_creed_config) == 21
    _validate_creed_config(x_creed_config)


def _validate_creed_config(x_creed_config: dict):
    atom_config_dict = get_atom_config_dict()
    fisc_config_dict = get_fisc_config_dict()
    pidgin_config_dict = get_pidgin_config_dict()
    # for every creed_format file there exists a unique creed_number with leading zeros to make 5 digits
    for creed_dimen, creed_dict in x_creed_config.items():
        print(f"{creed_dimen=}")
        assert creed_dict.get(creed_category_str()) in get_creed_categorys()
        assert creed_dict.get(jkeys_str()) is not None
        assert creed_dict.get(jvalues_str()) is not None
        assert creed_dict.get(allowed_crud_str()) is not None
        assert creed_dict.get(atom_update()) is None
        assert creed_dict.get(atom_insert()) is None
        assert creed_dict.get(atom_delete()) is None
        assert creed_dict.get(normal_specs_str()) is None
        if creed_dict.get(creed_category_str()) == "bud":
            sub_dimen = atom_config_dict.get(creed_dimen)
        elif creed_dict.get(creed_category_str()) == "fisc":
            sub_dimen = fisc_config_dict.get(creed_dimen)
        elif creed_dict.get(creed_category_str()) == "pidgin":
            sub_dimen = pidgin_config_dict.get(creed_dimen)

        assert creed_dict.get(allowed_crud_str()) in get_allowed_curds()

        if creed_dimen in {
            fisc_timeline_hour_str(),
            fisc_timeline_month_str(),
            fisc_timeline_weekday_str(),
            fiscunit_str(),
            map_otx2inx_str(),
            pidgin_label_str(),
            pidgin_name_str(),
            pidgin_tag_str(),
            pidgin_way_str(),
        }:
            assert creed_dict.get(allowed_crud_str()) == insert_one_time_str()
        elif creed_dimen in {
            fisc_dealunit_str(),
            fisc_cashbook_str(),
            fisc_timeoffi_str(),
        }:
            assert creed_dict.get(allowed_crud_str()) == insert_mulitple_str()
        elif (
            sub_dimen.get(atom_update()) != None
            and sub_dimen.get(atom_insert()) != None
            and sub_dimen.get(atom_delete()) != None
        ):
            assert creed_dict.get(allowed_crud_str()) == delete_insert_update_str()
        elif (
            sub_dimen.get(atom_update()) != None
            and sub_dimen.get(atom_insert()) != None
            and sub_dimen.get(atom_delete()) is None
        ):
            assert creed_dict.get(allowed_crud_str()) == insert_update_str()
        elif (
            sub_dimen.get(atom_update()) is None
            and sub_dimen.get(atom_insert()) != None
            and sub_dimen.get(atom_delete()) != None
        ):
            assert creed_dict.get(allowed_crud_str()) == delete_insert_str()
        elif (
            sub_dimen.get(atom_update()) != None
            and sub_dimen.get(atom_insert()) is None
            and sub_dimen.get(atom_delete()) != None
        ):
            assert creed_dict.get(allowed_crud_str()) == delete_update_str()
        elif (
            sub_dimen.get(atom_update()) != None
            and sub_dimen.get(atom_insert()) is None
            and sub_dimen.get(atom_delete()) is None
        ):
            assert creed_dict.get(allowed_crud_str()) == atom_update()
        elif (
            sub_dimen.get(atom_update()) is None
            and sub_dimen.get(atom_insert()) != None
            and sub_dimen.get(atom_delete()) is None
        ):
            assert creed_dict.get(allowed_crud_str()) == atom_insert()
        elif (
            sub_dimen.get(atom_update()) is None
            and sub_dimen.get(atom_insert()) is None
            and sub_dimen.get(atom_delete()) != None
        ):
            assert creed_dict.get(allowed_crud_str()) == atom_delete()
        else:
            test_str = f"{allowed_crud_str()} not checked by test"
            assert creed_dict.get(allowed_crud_str()) == test_str

        sub_jkeys_keys = set(sub_dimen.get(jkeys_str()).keys())
        creed_jkeys_keys = set(creed_dict.get(jkeys_str()).keys())
        # print(f"    {sub_jkeys_keys=}")
        # print(f"  {creed_jkeys_keys=}")
        assert face_name_str() in creed_jkeys_keys
        assert event_int_str() in creed_jkeys_keys
        if creed_dict.get(creed_category_str()) != "pidgin":
            assert fisc_tag_str() in creed_jkeys_keys
        if creed_dict.get(creed_category_str()) == "bud":
            creed_jkeys_keys.remove(fisc_tag_str())
            creed_jkeys_keys.remove(owner_name_str())
        creed_jkeys_keys.remove(face_name_str())
        creed_jkeys_keys.remove(event_int_str())
        assert sub_jkeys_keys == creed_jkeys_keys

        sub_jvalues_keys = set(sub_dimen.get(jvalues_str()).keys())
        print(f"  {sub_jvalues_keys=}")
        if fisc_tag_str() in sub_jvalues_keys:
            sub_jvalues_keys.remove(fisc_tag_str())

        creed_jvalues_dict = creed_dict.get(jvalues_str())
        creed_jvalues_keys = set(creed_jvalues_dict.keys())
        # print(f"  {sub_jvalues_keys=}")
        # print(f"{creed_jvalues_keys=}")
        assert sub_jvalues_keys == creed_jvalues_keys

        assert fisc_tag_str() not in creed_jvalues_keys

        # sort_list = get_creed_elements_sort_order()
        # x_count = 0
        # sort_dict1 = {}
        # sort_dict2 = {}
        # for creed_arg in sort_list:
        #     sort_dict1[x_count] = creed_arg
        #     sort_dict1[creed_arg] = x_count

        # for jvalue in creed_jvalues_keys:
        #     print(f"{jvalue=} {creed_jvalues_dict=}")
        #     jvalue_dict = creed_jvalues_dict.get(jvalue)
        #     jvalue_column_order = jvalue_dict.get(column_order_str())
        #     assert jvalue_column_order != None
        #     list_ref_arg = sort_list[jvalue_column_order]
        #     assert list_ref_arg != None
        #     assert jvalue == list_ref_arg

        # # for jkey in creed_jkeys_keys:
        #     print(f"{jkey=} {creed_jkeys_dict=}")
        #     jkey_dict = creed_jkeys_dict.get(jkey)
        #     jkey_column_order = jkey_dict.get(column_order_str())
        #     assert jkey_column_order != None
        #     list_ref_arg = sort_list[jkey_column_order]
        #     assert list_ref_arg != None
        #     assert jkey == list_ref_arg


def test_get_creed_format_filenames_ReturnsObj():
    # ESTABLISH
    creed_filenames_set = get_creed_format_filenames()
    creed_filenames_sorted = list(creed_filenames_set)
    creed_filenames_sorted.sort(key=lambda x: x)
    # print(creed_filenames_sorted)

    # THEN
    assert creed_format_00021_bud_acctunit_v0_0_0() in creed_filenames_set
    assert creed_format_00020_bud_acct_membership_v0_0_0() in creed_filenames_set
    assert creed_format_00013_itemunit_v0_0_0() in creed_filenames_set

    # WHEN / THEN
    assert _validate_creed_format_files(creed_filenames_sorted)


def _validate_creed_format_files(creed_filenames: set[str]):
    all_dimen_keys_dict = {
        dimen: set(dict.get(jkeys_str()).keys())
        for dimen, dict in get_creed_config_dict().items()
    }

    valid_creed_dimens = set()
    valid_creed_dimens.update(get_bud_dimens())
    valid_creed_dimens.update(get_fisc_dimens())
    valid_creed_dimens.update(get_pidgin_dimens())
    config_dict = get_creed_config_dict()

    # for every creed_format file there exists a unique creed_number with leading zeros to make 5 digits
    creed_numbers_set = set()
    for creed_filename in creed_filenames:
        ref_dict = get_creedref_from_file(creed_filename)
        # print(f"{creed_filename=} {ref_dict.get(creed_number_str())=}")
        creed_number_value = ref_dict.get(creed_number_str())
        assert creed_number_value
        assert creed_number_value[2:8] == creed_filename[13:18]
        creed_numbers_set.add(creed_number_value)

        format_dimens = ref_dict.get(dimens_str())
        assert format_dimens is not None
        assert len(format_dimens) > 0
        for creed_format_dimen in format_dimens:
            assert creed_format_dimen in valid_creed_dimens

        assert ref_dict.get(attributes_str())
        creed_format_attributes = ref_dict.get(attributes_str())
        for creed_attribute, attr_dict in creed_format_attributes.items():
            # print(f"{creed_attribute=}")
            assert otx_key_str() in set(attr_dict.keys())
            otx_key_value = attr_dict.get(otx_key_str())
            for creed_format_dimen in format_dimens:
                format_config = config_dict.get(creed_format_dimen)
                dimen_required_attrs = set(format_config.get(jkeys_str()).keys())
                dimen_optional_attrs = set(format_config.get(jvalues_str()).keys())
                attr_in_required = creed_attribute in dimen_required_attrs
                attr_in_optional = creed_attribute in dimen_optional_attrs
                attr_in_keys = attr_in_required or attr_in_optional
                assert_fail_str = (
                    f"{creed_format_dimen=} {creed_attribute=} {otx_key_value=}"
                )
                if attr_in_keys and otx_key_value:
                    assert attr_in_required, assert_fail_str
                elif attr_in_keys:
                    assert attr_in_optional, assert_fail_str
        # check all implied dimens are there
        creed_attrs = set(ref_dict.get(attributes_str()).keys())
        creed_attrs_list = get_default_sorted_list(creed_attrs)
        if creed_attrs_list[-1].find("_ERASE") > 0:
            delete_attr_with_erase = creed_attrs_list[-1]
            delete_attr_without_erase = delete_attr_with_erase.replace("_ERASE", "")
            creed_attrs.remove(delete_attr_with_erase)
            creed_attrs.add(delete_attr_without_erase)

        for x_dimen, dimen_keys in all_dimen_keys_dict.items():
            # if x_dimen == bud_item_factunit_str() and x_dimen in format_dimens:
            #     print(f"{creed_number_value}  {x_dimen=} {creed_attrs_list=}")
            if dimen_keys.issubset(creed_attrs):
                if x_dimen not in format_dimens:
                    print(f"MISSING {x_dimen=} {creed_number_value} {creed_attrs=}")
                assert x_dimen in format_dimens
            else:
                # dimen_keys_list = get_default_sorted_list(dimen_keys)
                #     creed_attrs_list[-1] = creed_attrs_list[-1].removesuffix("_ERASE")
                #     creed_attrs = set(creed_attrs_list)
                if x_dimen in format_dimens:
                    print(
                        f"SHOULDNT BE {x_dimen=} {creed_number_value} : {get_default_sorted_list(creed_attrs)}"
                    )
                    # print(
                    #     f"SHOULDNT BE {x_dimen=} {creed_number_value} : {get_default_sorted_list(dimen_keys)}"
                    # )
                assert x_dimen not in format_dimens

    # assert face_name_str() in creed_format_attributes
    # assert event_int_str() in creed_format_attributes

    # confirm every creednumber is unique
    assert len(creed_numbers_set) == len(creed_filenames)
    assert creed_numbers_set == get_creed_numbers()

    return True


def test_get_creed_format_filename_ReturnsObj():
    # ESTABLISH
    br00021_str = "br00021"
    br00020_str = "br00020"
    br00013_str = "br00013"

    # WHEN
    br00021_filename = get_creed_format_filename(br00021_str)
    br00020_filename = get_creed_format_filename(br00020_str)
    br00013_filename = get_creed_format_filename(br00013_str)

    # THEN
    assert br00021_filename == creed_format_00021_bud_acctunit_v0_0_0()
    assert br00020_filename == creed_format_00020_bud_acct_membership_v0_0_0()
    assert br00013_filename == creed_format_00013_itemunit_v0_0_0()

    all_set = {get_creed_format_filename(br) for br in get_creed_numbers()}
    assert all_set == get_creed_format_filenames()


def set_creed_config_json(dimen: str, build_order: int):
    x_creed_config = get_creed_config_dict()
    dimen_dict = x_creed_config.get(dimen)
    dimen_dict[build_order_str()] = build_order
    x_creed_config[dimen] = dimen_dict
    save_json(config_file_dir(), get_creed_config_filename(), x_creed_config)


def test_get_creed_config_dict_ReturnsObj_build_order():
    # ESTABLISH / WHEN
    bo = build_order_str()
    # set_creed_config_json(pidgin_name_str(), 0)
    # set_creed_config_json(pidgin_label_str(), 1)
    # set_creed_config_json(pidgin_tag_str(), 2)
    # set_creed_config_json(pidgin_way_str(), 3)
    # set_creed_config_json(fiscunit_str(), 5)
    # set_creed_config_json(fisc_timeline_hour_str(), 6)
    # set_creed_config_json(fisc_timeline_month_str(), 7)
    # set_creed_config_json(fisc_timeline_weekday_str(), 8)
    # set_creed_config_json(bud_acct_membership_str(), 9)
    # set_creed_config_json(bud_acctunit_str(), 10)
    # set_creed_config_json(bud_item_awardlink_str(), 11)
    # set_creed_config_json(bud_item_factunit_str(), 12)
    # set_creed_config_json(bud_item_teamlink_str(), 14)
    # set_creed_config_json(bud_item_healerlink_str(), 15)
    # set_creed_config_json(bud_item_reason_premiseunit_str(), 16)
    # set_creed_config_json(bud_item_reasonunit_str(), 17)
    # set_creed_config_json(bud_itemunit_str(), 18)
    # set_creed_config_json(budunit_str(), 19)
    # set_creed_config_json(fisc_dealunit_str(), 20)
    # set_creed_config_json(fisc_cashbook_str(), 21)

    x_creed_config = get_creed_config_dict()

    # THEN
    assert x_creed_config.get(pidgin_name_str()).get(bo) == 0
    assert x_creed_config.get(pidgin_label_str()).get(bo) == 1
    assert x_creed_config.get(pidgin_tag_str()).get(bo) == 2
    assert x_creed_config.get(pidgin_way_str()).get(bo) == 3
    assert x_creed_config.get(fiscunit_str()).get(bo) == 5
    assert x_creed_config.get(fisc_timeline_hour_str()).get(bo) == 6
    assert x_creed_config.get(fisc_timeline_month_str()).get(bo) == 7
    assert x_creed_config.get(fisc_timeline_weekday_str()).get(bo) == 8
    assert x_creed_config.get(bud_acct_membership_str()).get(bo) == 9
    assert x_creed_config.get(bud_acctunit_str()).get(bo) == 10
    assert x_creed_config.get(bud_item_awardlink_str()).get(bo) == 11
    assert x_creed_config.get(bud_item_factunit_str()).get(bo) == 12
    assert x_creed_config.get(bud_item_teamlink_str()).get(bo) == 14
    assert x_creed_config.get(bud_item_healerlink_str()).get(bo) == 15
    assert x_creed_config.get(bud_item_reason_premiseunit_str()).get(bo) == 16
    assert x_creed_config.get(bud_item_reasonunit_str()).get(bo) == 17
    assert x_creed_config.get(bud_itemunit_str()).get(bo) == 18
    assert x_creed_config.get(budunit_str()).get(bo) == 19
    assert x_creed_config.get(fisc_dealunit_str()).get(bo) == 20
    assert x_creed_config.get(fisc_cashbook_str()).get(bo) == 21


def test_get_quick_creeds_column_ref_ReturnsObj():
    # ESTABLISH / WHEN
    x_creed_quick_column_ref = get_quick_creeds_column_ref()

    # THEN
    assert len(x_creed_quick_column_ref) == len(get_creed_numbers())
    assert x_creed_quick_column_ref.get("br00000") == {
        event_int_str(),
        face_name_str(),
        c400_number_str(),
        fisc_tag_str(),
        fund_coin_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        bridge_str(),
        timeline_tag_str(),
        yr1_jan1_offset_str(),
        "job_listen_rotations",
    }


def _create_expected_creed_dimen_ref() -> dict[str, list[str]]:
    creed_numbers_sorted = list(get_creed_numbers())
    creed_numbers_sorted.sort(key=lambda x: x)
    expected_creed_dimen_ref = {}
    for creed_number in creed_numbers_sorted:
        creed_format_filename = get_creed_format_filename(creed_number)
        x_creedref = get_creedref_from_file(creed_format_filename)
        dimens_list = x_creedref.get(dimens_str())
        for x_dimen in dimens_list:
            if expected_creed_dimen_ref.get(x_dimen) is None:
                expected_creed_dimen_ref[x_dimen] = {creed_number}
            else:
                expected_creed_dimen_ref.get(x_dimen).add(creed_number)
    return expected_creed_dimen_ref


def test_get_creed_dimen_ref_ReturnsObj():
    # ESTABLISH
    expected_creed_dimen_ref = _create_expected_creed_dimen_ref()
    print(f"{expected_creed_dimen_ref=}")

    # WHEN / THEN
    assert get_creed_dimen_ref() == expected_creed_dimen_ref
