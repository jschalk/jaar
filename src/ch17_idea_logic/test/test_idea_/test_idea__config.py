from copy import copy as copy_copy
from os import getcwd as os_getcwd
from src.ch00_data_toolbox.file_toolbox import create_path, save_json
from src.ch06_belief_logic.belief_config import (
    get_all_belief_calc_args,
    get_belief_calc_args_sqlite_datatype_dict,
)
from src.ch09_belief_atom_logic.atom_config import (
    get_all_belief_dimen_delete_keys,
    get_atom_args_dimen_mapping,
    get_atom_config_dict,
    get_belief_dimens,
    get_delete_key_name,
)
from src.ch15_moment_logic.moment_config import (
    get_moment_args_dimen_mapping,
    get_moment_config_dict,
    get_moment_dimens,
)
from src.ch16_pidgin_logic.pidgin_config import (
    get_pidgin_args_dimen_mapping,
    get_pidgin_config_dict,
    get_pidgin_dimens,
    get_pidginable_args,
)
from src.ch17_idea_logic._ref.ch17_terms import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    addin_str,
    allowed_crud_str,
    amount_str,
    attributes_str,
    awardee_title_str,
    begin_str,
    belief_name_str,
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
    bud_time_str,
    build_order_str,
    c400_number_str,
    celldepth_str,
    close_str,
    column_order_str,
    credor_respect_str,
    cumulative_day_str,
    cumulative_minute_str,
    debtor_respect_str,
    delete_insert_str,
    delete_insert_update_str,
    delete_update_str,
    denom_str,
    dimens_str,
    error_message_str,
    event_int_str,
    face_name_str,
    fact_context_str,
    fact_lower_str,
    fact_state_str,
    fact_upper_str,
    fund_iota_str,
    give_force_str,
    gogo_want_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    healer_name_str,
    hour_label_str,
    idea_category_str,
    idea_number_str,
    insert_multiple_str,
    insert_one_time_str,
    insert_update_str,
    inx_knot_str,
    inx_label_str,
    inx_name_str,
    inx_rope_str,
    inx_title_str,
    jkeys_str,
    job_listen_rotations_str,
    jvalues_str,
    knot_str,
    moment_budunit_str,
    moment_label_str,
    moment_paybook_str,
    moment_timeline_hour_str,
    moment_timeline_month_str,
    moment_timeline_weekday_str,
    moment_timeoffi_str,
    momentunit_str,
    month_label_str,
    monthday_distortion_str,
    morph_str,
    normal_specs_str,
    numor_str,
    offi_time_str,
    otx_key_str,
    otx_knot_str,
    otx_label_str,
    otx_name_str,
    otx_rope_str,
    otx_title_str,
    party_title_str,
    penny_str,
    pidgin_label_str,
    pidgin_name_str,
    pidgin_rope_str,
    pidgin_title_str,
    pidginunit_str,
    plan_rope_str,
    quota_str,
    reason_active_requisite_str,
    reason_context_str,
    reason_lower_str,
    reason_state_str,
    reason_upper_str,
    respect_bit_str,
    solo_str,
    star_str,
    stop_want_str,
    take_force_str,
    task_str,
    timeline_label_str,
    tran_time_str,
    unknown_str_str,
    voice_cred_points_str,
    voice_debt_points_str,
    voice_name_str,
    voice_pool_str,
    weekday_label_str,
    weekday_order_str,
    world_name_str,
    yr1_jan1_offset_str,
)
from src.ch17_idea_logic.idea_config import (
    get_allowed_curds,
    get_default_sorted_list,
    get_idea_config_dict,
    get_idea_dimen_ref,
    get_idea_elements_sort_order,
    get_idea_format_filename,
    get_idea_format_filenames,
    get_idea_numbers,
    get_idea_sqlite_types,
    get_idearef_from_file,
    get_quick_ideas_column_ref,
    idea_config_path,
    idea_format_00013_planunit_v0_0_0,
    idea_format_00020_belief_voice_membership_v0_0_0,
    idea_format_00021_belief_voiceunit_v0_0_0,
)


def test_get_idea_elements_sort_order_ReturnsObj():
    # ESTABLISH / WHEN
    table_sorting_priority = get_idea_elements_sort_order()

    # THEN
    atom_args = set(get_atom_args_dimen_mapping().keys())
    assert atom_args.issubset(set(table_sorting_priority))
    moment_args = set(get_moment_args_dimen_mapping().keys())
    print(f"{moment_args=}")
    print(f"{moment_args.difference(set(table_sorting_priority))=}")
    assert moment_args.issubset(set(table_sorting_priority))
    pidgin_args = set(get_pidgin_args_dimen_mapping().keys())
    assert pidgin_args.issubset(set(table_sorting_priority))
    all_belief_dimen_delete_keys = get_all_belief_dimen_delete_keys()
    print(f"missing {all_belief_dimen_delete_keys.difference(table_sorting_priority)}")
    assert all_belief_dimen_delete_keys.issubset(table_sorting_priority)
    belief_calc_args = set(get_all_belief_calc_args().keys())
    # for belief_calc_arg in belief_calc_args.difference(table_sorting_priority):
    #     print(f"{belief_calc_arg=}")
    print(f"{belief_calc_args.difference(table_sorting_priority)=}")
    assert belief_calc_args.issubset(table_sorting_priority)
    pidginable_otx_cols = {f"{pid_arg}_otx" for pid_arg in get_pidginable_args()}
    pidginable_inx_cols = {f"{pid_arg}_inx" for pid_arg in get_pidginable_args()}
    x_delete_keys = all_belief_dimen_delete_keys
    pidginable_delete_otx_cols = {f"{pid_arg}_otx" for pid_arg in x_delete_keys}
    pidginable_delete_inx_cols = {f"{pid_arg}_inx" for pid_arg in x_delete_keys}
    print(f"{pidginable_delete_otx_cols=}")
    print(f"{pidginable_delete_inx_cols=}")
    assert pidginable_otx_cols.issubset(table_sorting_priority)
    assert pidginable_inx_cols.issubset(table_sorting_priority)
    assert pidginable_delete_otx_cols.issubset(table_sorting_priority)
    assert pidginable_delete_inx_cols.issubset(table_sorting_priority)

    # all the suffix otx/inx columns are only used in one table
    assert table_sorting_priority[0] == "world_name"
    assert table_sorting_priority[1] == "idea_number"
    assert table_sorting_priority[2] == "source_dimen"
    assert table_sorting_priority[3] == "pidgin_event_int"
    assert table_sorting_priority[4] == "event_int"
    assert table_sorting_priority[5] == "face_name"
    assert table_sorting_priority[6] == "face_name_otx"
    assert table_sorting_priority[7] == "face_name_inx"
    assert table_sorting_priority[8] == "moment_label"
    assert table_sorting_priority[9] == "moment_label_otx"
    assert table_sorting_priority[10] == "moment_label_inx"
    assert table_sorting_priority[11] == "timeline_label"
    assert table_sorting_priority[12] == "timeline_label_otx"
    assert table_sorting_priority[13] == "timeline_label_inx"
    assert table_sorting_priority[14] == "offi_time"
    assert table_sorting_priority[15] == "c400_number"
    assert table_sorting_priority[16] == "yr1_jan1_offset"
    assert table_sorting_priority[17] == "monthday_distortion"
    assert table_sorting_priority[18] == "cumulative_day"
    assert table_sorting_priority[19] == "month_label"
    assert table_sorting_priority[20] == "month_label_otx"
    assert table_sorting_priority[21] == "month_label_inx"
    assert table_sorting_priority[22] == "cumulative_minute"
    assert table_sorting_priority[23] == "hour_label"
    assert table_sorting_priority[24] == "hour_label_otx"
    assert table_sorting_priority[25] == "hour_label_inx"
    assert table_sorting_priority[26] == "weekday_order"
    assert table_sorting_priority[27] == "weekday_label"
    assert table_sorting_priority[28] == "weekday_label_otx"
    assert table_sorting_priority[29] == "weekday_label_inx"
    assert table_sorting_priority[30] == "belief_name"
    assert table_sorting_priority[31] == "belief_name_otx"
    assert table_sorting_priority[32] == "belief_name_inx"
    assert table_sorting_priority[33] == "belief_name_ERASE"
    assert table_sorting_priority[34] == "belief_name_ERASE_otx"
    assert table_sorting_priority[35] == "belief_name_ERASE_inx"
    assert table_sorting_priority[36] == "voice_name"
    assert table_sorting_priority[37] == "voice_name_otx"
    assert table_sorting_priority[38] == "voice_name_inx"
    assert table_sorting_priority[39] == "voice_name_ERASE"
    assert table_sorting_priority[40] == "voice_name_ERASE_otx"
    assert table_sorting_priority[41] == "voice_name_ERASE_inx"
    assert table_sorting_priority[42] == "group_title"
    assert table_sorting_priority[43] == "group_title_otx"
    assert table_sorting_priority[44] == "group_title_inx"
    assert table_sorting_priority[45] == "group_title_ERASE"
    assert table_sorting_priority[46] == "group_title_ERASE_otx"
    assert table_sorting_priority[47] == "group_title_ERASE_inx"
    assert table_sorting_priority[48] == "plan_rope"
    assert table_sorting_priority[49] == "plan_rope_otx"
    assert table_sorting_priority[50] == "plan_rope_inx"
    assert table_sorting_priority[51] == "plan_rope_ERASE"
    assert table_sorting_priority[52] == "plan_rope_ERASE_otx"
    assert table_sorting_priority[53] == "plan_rope_ERASE_inx"
    assert table_sorting_priority[54] == "reason_context"
    assert table_sorting_priority[55] == "reason_context_otx"
    assert table_sorting_priority[56] == "reason_context_inx"
    assert table_sorting_priority[57] == "reason_context_ERASE"
    assert table_sorting_priority[58] == "reason_context_ERASE_otx"
    assert table_sorting_priority[59] == "reason_context_ERASE_inx"
    assert table_sorting_priority[60] == "fact_context"
    assert table_sorting_priority[61] == "fact_context_otx"
    assert table_sorting_priority[62] == "fact_context_inx"
    assert table_sorting_priority[63] == "fact_context_ERASE"
    assert table_sorting_priority[64] == "fact_context_ERASE_otx"
    assert table_sorting_priority[65] == "fact_context_ERASE_inx"
    assert table_sorting_priority[66] == "reason_state"
    assert table_sorting_priority[67] == "reason_state_otx"
    assert table_sorting_priority[68] == "reason_state_inx"
    assert table_sorting_priority[69] == "reason_state_ERASE"
    assert table_sorting_priority[70] == "reason_state_ERASE_otx"
    assert table_sorting_priority[71] == "reason_state_ERASE_inx"
    assert table_sorting_priority[72] == "fact_state"
    assert table_sorting_priority[73] == "fact_state_otx"
    assert table_sorting_priority[74] == "fact_state_inx"
    assert table_sorting_priority[75] == "party_title"
    assert table_sorting_priority[76] == "party_title_otx"
    assert table_sorting_priority[77] == "party_title_inx"
    assert table_sorting_priority[78] == "party_title_ERASE"
    assert table_sorting_priority[79] == "party_title_ERASE_otx"
    assert table_sorting_priority[80] == "party_title_ERASE_inx"
    assert table_sorting_priority[81] == "solo"
    assert table_sorting_priority[82] == "awardee_title"
    assert table_sorting_priority[83] == "awardee_title_otx"
    assert table_sorting_priority[84] == "awardee_title_inx"
    assert table_sorting_priority[85] == "awardee_title_ERASE"
    assert table_sorting_priority[86] == "awardee_title_ERASE_otx"
    assert table_sorting_priority[87] == "awardee_title_ERASE_inx"
    assert table_sorting_priority[88] == "healer_name"
    assert table_sorting_priority[89] == "healer_name_otx"
    assert table_sorting_priority[90] == "healer_name_inx"
    assert table_sorting_priority[91] == "healer_name_ERASE"
    assert table_sorting_priority[92] == "healer_name_ERASE_otx"
    assert table_sorting_priority[93] == "healer_name_ERASE_inx"
    assert table_sorting_priority[94] == "bud_time"
    assert table_sorting_priority[95] == "tran_time"
    assert table_sorting_priority[96] == "begin"
    assert table_sorting_priority[97] == "close"
    assert table_sorting_priority[98] == "addin"
    assert table_sorting_priority[99] == "numor"
    assert table_sorting_priority[100] == "denom"
    assert table_sorting_priority[101] == "morph"
    assert table_sorting_priority[102] == "gogo_want"
    assert table_sorting_priority[103] == "stop_want"
    assert table_sorting_priority[104] == "reason_active_requisite"
    assert table_sorting_priority[105] == "voice_cred_points"
    assert table_sorting_priority[106] == "voice_debt_points"
    assert table_sorting_priority[107] == "group_cred_points"
    assert table_sorting_priority[108] == "group_debt_points"
    assert table_sorting_priority[109] == "credor_respect"
    assert table_sorting_priority[110] == "debtor_respect"
    assert table_sorting_priority[111] == "fact_lower"
    assert table_sorting_priority[112] == "fact_upper"
    assert table_sorting_priority[113] == "fund_pool"
    assert table_sorting_priority[114] == "give_force"
    assert table_sorting_priority[115] == "star"
    assert table_sorting_priority[116] == "max_tree_traverse"
    assert table_sorting_priority[117] == "reason_upper"
    assert table_sorting_priority[118] == "reason_lower"
    assert table_sorting_priority[119] == "reason_divisor"
    assert table_sorting_priority[120] == "task"
    assert table_sorting_priority[121] == "problem_bool"
    assert table_sorting_priority[122] == "take_force"
    assert table_sorting_priority[123] == "tally"
    assert table_sorting_priority[124] == "fund_iota"
    assert table_sorting_priority[125] == "penny"
    assert table_sorting_priority[126] == "respect_bit"
    assert table_sorting_priority[127] == "amount"
    assert table_sorting_priority[128] == "otx_label"
    assert table_sorting_priority[129] == "inx_label"
    assert table_sorting_priority[130] == "otx_rope"
    assert table_sorting_priority[131] == "inx_rope"
    assert table_sorting_priority[132] == "otx_name"
    assert table_sorting_priority[133] == "inx_name"
    assert table_sorting_priority[134] == "otx_title"
    assert table_sorting_priority[135] == "inx_title"
    assert table_sorting_priority[136] == "otx_knot"
    assert table_sorting_priority[137] == "inx_knot"
    assert table_sorting_priority[138] == "knot"
    assert table_sorting_priority[139] == "unknown_str"
    assert table_sorting_priority[140] == "quota"
    assert table_sorting_priority[141] == "celldepth"
    assert table_sorting_priority[142] == job_listen_rotations_str()
    assert table_sorting_priority[143] == error_message_str()
    assert table_sorting_priority[144] == "_belief_name_is_labor"
    assert table_sorting_priority[145] == "active"
    assert table_sorting_priority[146] == "chore"
    assert table_sorting_priority[147] == "status"
    assert table_sorting_priority[148] == "credor_pool"
    assert table_sorting_priority[149] == "debtor_pool"
    assert table_sorting_priority[150] == "rational"
    assert table_sorting_priority[151] == "fund_give"
    assert table_sorting_priority[152] == "fund_take"
    assert table_sorting_priority[153] == "fund_onset"
    assert table_sorting_priority[154] == "fund_cease"
    assert table_sorting_priority[155] == "fund_ratio"
    assert table_sorting_priority[156] == "fund_agenda_give"
    assert table_sorting_priority[157] == "fund_agenda_take"
    assert table_sorting_priority[158] == "fund_agenda_ratio_give"
    assert table_sorting_priority[159] == "fund_agenda_ratio_take"
    assert table_sorting_priority[160] == "inallocable_voice_debt_points"
    assert table_sorting_priority[161] == "gogo_calc"
    assert table_sorting_priority[162] == "stop_calc"
    assert table_sorting_priority[163] == "tree_level"
    assert table_sorting_priority[164] == "range_evaluated"
    assert table_sorting_priority[165] == "descendant_task_count"
    assert table_sorting_priority[166] == "healerunit_ratio"
    assert table_sorting_priority[167] == "all_voice_cred"
    assert table_sorting_priority[168] == "keeps_justified"
    assert table_sorting_priority[169] == "offtrack_fund"
    assert table_sorting_priority[170] == "_reason_active_heir"
    assert table_sorting_priority[171] == "irrational_voice_debt_points"
    assert table_sorting_priority[172] == "sum_healerunit_share"
    assert table_sorting_priority[173] == "keeps_buildable"
    assert table_sorting_priority[174] == "all_voice_debt"
    assert table_sorting_priority[175] == "tree_traverse_count"
    assert table_sorting_priority[176] == "funds"
    assert table_sorting_priority[177] == "fund_rank"
    assert table_sorting_priority[178] == "tasks_count"

    assert len(table_sorting_priority) == 179
    all_args = copy_copy(atom_args)
    all_args.update(all_belief_dimen_delete_keys)
    all_args.update(moment_args)
    all_args.update(pidgin_args)
    all_args.update(belief_calc_args)
    all_args.update(pidginable_otx_cols)
    all_args.update(pidginable_inx_cols)
    all_args.update(pidginable_delete_otx_cols)
    all_args.update(pidginable_delete_inx_cols)
    all_args.add(idea_number_str())
    all_args.add(event_int_str())
    all_args.add(face_name_str())
    all_args.add("source_dimen")
    all_args.add("pidgin_event_int")
    all_args.add(error_message_str())
    all_args.add(world_name_str())
    all_args.add("funds")  # kpi columns
    all_args.add("fund_rank")  # kpi columns
    all_args.add("tasks_count")  # kpi columns
    assert all_args == set(table_sorting_priority)

    x_no_underscoore_set = {x_arg.replace("_", "") for x_arg in table_sorting_priority}
    # x_dict = {}
    # for x_arg in sorted(table_sorting_priority):
    #     y_arg = x_arg.replace("_", "")
    #     if x_dict.get(y_arg) is None:
    #         x_dict[y_arg] = 0
    #     x_dict[y_arg] = x_dict.get(y_arg) + 1
    # print(f"{x_dict=}")
    assert len(x_no_underscoore_set) == len(table_sorting_priority)


def test_get_idea_sqlite_types_ReturnsObj():
    # ESTABLISH / WHEN
    sqlite_types = get_idea_sqlite_types()

    # THEN
    assert set(sqlite_types.keys()) == set(get_idea_elements_sort_order())
    assert sqlite_types.get(idea_number_str()) == "TEXT"
    assert sqlite_types.get(face_name_str()) == "TEXT"
    assert sqlite_types.get("pidgin_event_int") == "INTEGER"
    assert sqlite_types.get(event_int_str()) == "INTEGER"
    assert sqlite_types.get(moment_label_str()) == "TEXT"
    assert sqlite_types.get(belief_name_str()) == "TEXT"
    assert sqlite_types.get(voice_name_str()) == "TEXT"
    assert sqlite_types.get(group_title_str()) == "TEXT"
    assert sqlite_types.get(plan_rope_str()) == "TEXT"
    assert sqlite_types.get(reason_context_str()) == "TEXT"
    assert sqlite_types.get("reason_state") == "TEXT"
    assert sqlite_types.get("fact_state") == "TEXT"
    assert sqlite_types.get(party_title_str()) == "TEXT"
    assert sqlite_types.get(awardee_title_str()) == "TEXT"
    assert sqlite_types.get(healer_name_str()) == "TEXT"
    assert sqlite_types.get(offi_time_str()) == "INTEGER"
    assert sqlite_types.get(bud_time_str()) == "INTEGER"
    assert sqlite_types.get(tran_time_str()) == "INTEGER"
    assert sqlite_types.get(begin_str()) == "REAL"
    assert sqlite_types.get(close_str()) == "REAL"
    assert sqlite_types.get(addin_str()) == "REAL"
    assert sqlite_types.get(numor_str()) == "INTEGER"
    assert sqlite_types.get(denom_str()) == "INTEGER"
    assert sqlite_types.get(morph_str()) == "INTEGER"
    assert sqlite_types.get(gogo_want_str()) == "REAL"
    assert sqlite_types.get(stop_want_str()) == "REAL"
    assert sqlite_types.get(reason_active_requisite_str()) == "INTEGER"
    assert sqlite_types.get(voice_cred_points_str()) == "REAL"
    assert sqlite_types.get(voice_debt_points_str()) == "REAL"
    assert sqlite_types.get(group_cred_points_str()) == "REAL"
    assert sqlite_types.get(group_debt_points_str()) == "REAL"
    assert sqlite_types.get(credor_respect_str()) == "REAL"
    assert sqlite_types.get(debtor_respect_str()) == "REAL"
    assert sqlite_types.get(fact_lower_str()) == "REAL"
    assert sqlite_types.get(fact_upper_str()) == "REAL"
    assert sqlite_types.get("fund_pool") == "REAL"
    assert sqlite_types.get(give_force_str()) == "REAL"
    assert sqlite_types.get(star_str()) == "INTEGER"
    assert sqlite_types.get("max_tree_traverse") == "INTEGER"
    assert sqlite_types.get("reason_upper") == "REAL"
    assert sqlite_types.get("reason_lower") == "REAL"
    assert sqlite_types.get("reason_divisor") == "INTEGER"
    assert sqlite_types.get("problem_bool") == "INTEGER"
    assert sqlite_types.get(take_force_str()) == "REAL"
    assert sqlite_types.get("tally") == "INTEGER"
    assert sqlite_types.get(fund_iota_str()) == "REAL"
    assert sqlite_types.get(penny_str()) == "REAL"
    assert sqlite_types.get(task_str()) == "INTEGER"
    assert sqlite_types.get(respect_bit_str()) == "REAL"
    assert sqlite_types.get(amount_str()) == "REAL"
    assert sqlite_types.get(month_label_str()) == "TEXT"
    assert sqlite_types.get(hour_label_str()) == "TEXT"
    assert sqlite_types.get(cumulative_minute_str()) == "INTEGER"
    assert sqlite_types.get(cumulative_day_str()) == "INTEGER"
    assert sqlite_types.get(weekday_label_str()) == "TEXT"
    assert sqlite_types.get(weekday_order_str()) == "INTEGER"
    assert sqlite_types.get(otx_knot_str()) == "TEXT"
    assert sqlite_types.get(inx_knot_str()) == "TEXT"
    assert sqlite_types.get(unknown_str_str()) == "TEXT"
    assert sqlite_types.get(knot_str()) == "TEXT"
    assert sqlite_types.get(c400_number_str()) == "INTEGER"
    assert sqlite_types.get(yr1_jan1_offset_str()) == "INTEGER"
    assert sqlite_types.get(quota_str()) == "REAL"
    assert sqlite_types.get(celldepth_str()) == "INTEGER"
    assert sqlite_types.get(monthday_distortion_str()) == "INTEGER"
    assert sqlite_types.get(timeline_label_str()) == "TEXT"
    assert sqlite_types.get(error_message_str()) == "TEXT"
    assert sqlite_types.get(solo_str()) == "INTEGER"

    # sourcery skip: no-loop-in-tests
    for x_arg, datatype in get_belief_calc_args_sqlite_datatype_dict().items():
        print(f"{x_arg=} {datatype=} {sqlite_types.get(x_arg)=}")
        assert sqlite_types.get(x_arg) == datatype

    assert set(sqlite_types.values()) == {"TEXT", "INTEGER", "REAL"}


def test_get_allowed_curds_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_allowed_curds() == {
        insert_one_time_str(),
        insert_multiple_str(),
        delete_insert_update_str(),
        insert_update_str(),
        delete_insert_str(),
        delete_update_str(),
        INSERT_str(),
        DELETE_str(),
        UPDATE_str(),
    }


def test_idea_config_path_ReturnsObj_Idea() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    module_dir = create_path(src_dir, "ch17_idea_logic")
    assert idea_config_path() == create_path(module_dir, "idea_config.json")


def test_get_idea_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    x_idea_config = get_idea_config_dict()

    # THEN
    assert x_idea_config
    idea_config_dimens = set(x_idea_config.keys())
    assert momentunit_str() in idea_config_dimens
    assert moment_budunit_str() in idea_config_dimens
    assert moment_paybook_str() in idea_config_dimens
    assert moment_timeline_hour_str() in idea_config_dimens
    assert moment_timeline_month_str() in idea_config_dimens
    assert moment_timeline_weekday_str() in idea_config_dimens
    assert moment_timeoffi_str() in idea_config_dimens
    assert belief_voice_membership_str() in idea_config_dimens
    assert belief_voiceunit_str() in idea_config_dimens
    assert belief_plan_awardunit_str() in idea_config_dimens
    assert belief_plan_factunit_str() in idea_config_dimens
    assert belief_plan_partyunit_str() in idea_config_dimens
    assert belief_plan_healerunit_str() in idea_config_dimens
    assert belief_plan_reason_caseunit_str() in idea_config_dimens
    assert belief_plan_reasonunit_str() in idea_config_dimens
    assert belief_planunit_str() in idea_config_dimens
    assert beliefunit_str() in idea_config_dimens
    assert pidgin_name_str() in idea_config_dimens
    assert pidgin_title_str() in idea_config_dimens
    assert pidgin_label_str() in idea_config_dimens
    assert pidgin_rope_str() in idea_config_dimens
    assert get_belief_dimens().issubset(idea_config_dimens)
    assert get_moment_dimens().issubset(idea_config_dimens)
    assert get_pidgin_dimens().issubset(idea_config_dimens)
    assert len(x_idea_config) == 21
    _validate_idea_config(x_idea_config)


def get_idea_categorys():
    return {"belief", "moment", "pidgin"}


def _validate_idea_config(x_idea_config: dict):
    atom_config_dict = get_atom_config_dict()
    moment_config_dict = get_moment_config_dict()
    pidgin_config_dict = get_pidgin_config_dict()
    # for every idea_format file there exists a unique idea_number with leading zeros to make 5 digits
    for idea_dimen, idea_dict in x_idea_config.items():
        print(f"{idea_dimen=}")
        assert idea_dict.get(idea_category_str()) in get_idea_categorys()
        assert idea_dict.get(jkeys_str()) is not None
        assert idea_dict.get(jvalues_str()) is not None
        assert idea_dict.get(allowed_crud_str()) is not None
        assert idea_dict.get(UPDATE_str()) is None
        assert idea_dict.get(INSERT_str()) is None
        assert idea_dict.get(DELETE_str()) is None
        assert idea_dict.get(normal_specs_str()) is None
        if idea_dict.get(idea_category_str()) == "belief":
            sub_dimen = atom_config_dict.get(idea_dimen)
        elif idea_dict.get(idea_category_str()) == "moment":
            sub_dimen = moment_config_dict.get(idea_dimen)
        elif idea_dict.get(idea_category_str()) == "pidgin":
            sub_dimen = pidgin_config_dict.get(idea_dimen)

        assert idea_dict.get(allowed_crud_str()) in get_allowed_curds()

        if idea_dimen in {
            moment_timeline_hour_str(),
            moment_timeline_month_str(),
            moment_timeline_weekday_str(),
            momentunit_str(),
            "map_otx2inx",
            pidgin_title_str(),
            pidgin_name_str(),
            pidgin_label_str(),
            pidgin_rope_str(),
        }:
            assert idea_dict.get(allowed_crud_str()) == insert_one_time_str()
        elif idea_dimen in {
            moment_budunit_str(),
            moment_paybook_str(),
            moment_timeoffi_str(),
        }:
            assert idea_dict.get(allowed_crud_str()) == insert_multiple_str()
        elif (
            sub_dimen.get(UPDATE_str()) != None
            and sub_dimen.get(INSERT_str()) != None
            and sub_dimen.get(DELETE_str()) != None
        ):
            assert idea_dict.get(allowed_crud_str()) == delete_insert_update_str()
        elif (
            sub_dimen.get(UPDATE_str()) != None
            and sub_dimen.get(INSERT_str()) != None
            and sub_dimen.get(DELETE_str()) is None
        ):
            assert idea_dict.get(allowed_crud_str()) == insert_update_str()
        elif (
            sub_dimen.get(UPDATE_str()) is None
            and sub_dimen.get(INSERT_str()) != None
            and sub_dimen.get(DELETE_str()) != None
        ):
            assert idea_dict.get(allowed_crud_str()) == delete_insert_str()
        elif (
            sub_dimen.get(UPDATE_str()) != None
            and sub_dimen.get(INSERT_str()) is None
            and sub_dimen.get(DELETE_str()) != None
        ):
            assert idea_dict.get(allowed_crud_str()) == delete_update_str()
        elif (
            sub_dimen.get(UPDATE_str()) != None
            and sub_dimen.get(INSERT_str()) is None
            and sub_dimen.get(DELETE_str()) is None
        ):
            assert idea_dict.get(allowed_crud_str()) == UPDATE_str()
        elif (
            sub_dimen.get(UPDATE_str()) is None
            and sub_dimen.get(INSERT_str()) != None
            and sub_dimen.get(DELETE_str()) is None
        ):
            assert idea_dict.get(allowed_crud_str()) == INSERT_str()
        elif (
            sub_dimen.get(UPDATE_str()) is None
            and sub_dimen.get(INSERT_str()) is None
            and sub_dimen.get(DELETE_str()) != None
        ):
            assert idea_dict.get(allowed_crud_str()) == DELETE_str()
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
            assert moment_label_str() in idea_jkeys_keys
        if idea_dict.get(idea_category_str()) == "belief":
            idea_jkeys_keys.remove(moment_label_str())
            idea_jkeys_keys.remove(belief_name_str())
        idea_jkeys_keys.remove(face_name_str())
        idea_jkeys_keys.remove(event_int_str())
        assert sub_jkeys_keys == idea_jkeys_keys

        sub_jvalues_keys = set(sub_dimen.get(jvalues_str()).keys())
        print(f"  {sub_jvalues_keys=}")
        if moment_label_str() in sub_jvalues_keys:
            sub_jvalues_keys.remove(moment_label_str())

        idea_jvalues_dict = idea_dict.get(jvalues_str())
        idea_jvalues_keys = set(idea_jvalues_dict.keys())
        # print(f"  {sub_jvalues_keys=}")
        # print(f"{idea_jvalues_keys=}")
        assert sub_jvalues_keys == idea_jvalues_keys

        assert moment_label_str() not in idea_jvalues_keys

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
    print(f"{len(idea_filenames_sorted)=}")

    # THEN
    assert idea_format_00021_belief_voiceunit_v0_0_0() in idea_filenames_set
    assert idea_format_00020_belief_voice_membership_v0_0_0() in idea_filenames_set
    assert idea_format_00013_planunit_v0_0_0() in idea_filenames_set

    # WHEN / THEN
    print("validate")
    assert _validate_idea_format_files(idea_filenames_sorted)


def _validate_idea_format_files(idea_filenames: set[str]):
    all_dimen_keys_dict = {
        dimen: set(dict.get(jkeys_str()).keys())
        for dimen, dict in get_idea_config_dict().items()
    }

    valid_idea_dimens = set()
    valid_idea_dimens.update(get_belief_dimens())
    valid_idea_dimens.update(get_moment_dimens())
    valid_idea_dimens.update(get_pidgin_dimens())
    print("get_idea_config_dict")
    config_dict = get_idea_config_dict()

    # for every idea_format file there exists a unique idea_number with leading zeros to make 5 digits
    idea_numbers_set = set()
    for idea_filename in idea_filenames:
        ref_dict = get_idearef_from_file(idea_filename)
        # print(f"{idea_filename=} {ref_dict.get(idea_number_str())=}")
        idea_number_value = ref_dict.get(idea_number_str())
        assert idea_number_value
        assert idea_number_value[2:8] == idea_filename[12:17]
        idea_numbers_set.add(idea_number_value)

        format_dimens = ref_dict.get(dimens_str())
        assert format_dimens is not None
        assert len(format_dimens) > 0
        for idea_format_dimen in format_dimens:
            assert idea_format_dimen in valid_idea_dimens

        assert ref_dict.get(attributes_str())
        idea_format_attributes = ref_dict.get(attributes_str())
        for idea_attribute, attr_dict in idea_format_attributes.items():
            # print(f"{idea_attribute=}")
            assert otx_key_str() in set(attr_dict.keys())
            otx_key_value = attr_dict.get(otx_key_str())
            for idea_format_dimen in format_dimens:
                format_config = config_dict.get(idea_format_dimen)
                dimen_required_attrs = set(format_config.get(jkeys_str()).keys())
                dimen_optional_attrs = set(format_config.get(jvalues_str()).keys())
                attr_in_required = idea_attribute in dimen_required_attrs
                attr_in_optional = idea_attribute in dimen_optional_attrs
                attr_in_keys = attr_in_required or attr_in_optional
                assert_fail_str = (
                    f"{idea_format_dimen=} {idea_attribute=} {otx_key_value=}"
                )
                if attr_in_keys and otx_key_value:
                    assert attr_in_required, assert_fail_str
                elif attr_in_keys:
                    assert attr_in_optional, assert_fail_str
        # check all implied dimens are there
        idea_attrs = set(ref_dict.get(attributes_str()).keys())
        idea_attrs_list = get_default_sorted_list(idea_attrs)
        if idea_attrs_list[-1].find("_ERASE") > 0:
            delete_attr_with_erase = idea_attrs_list[-1]
            delete_attr_without_erase = delete_attr_with_erase.replace("_ERASE", "")
            idea_attrs.remove(delete_attr_with_erase)
            idea_attrs.add(delete_attr_without_erase)

        for x_dimen, dimen_keys in all_dimen_keys_dict.items():
            # if x_dimen == belief_plan_factunit_str() and x_dimen in format_dimens:
            #     print(f"{idea_number_value}  {x_dimen=} {idea_attrs_list=}")
            if dimen_keys.issubset(idea_attrs):
                if x_dimen not in format_dimens:
                    print(f"MISSING {x_dimen=} {idea_number_value} {idea_attrs=}")
                assert x_dimen in format_dimens
            else:
                # dimen_keys_list = get_default_sorted_list(dimen_keys)
                #     idea_attrs_list[-1] = idea_attrs_list[-1].removesuffix("_ERASE")
                #     idea_attrs = set(idea_attrs_list)
                if x_dimen in format_dimens:
                    print(
                        f"SHOULDNT BE {x_dimen=} {idea_number_value} : {get_default_sorted_list(idea_attrs)}"
                    )
                    # print(
                    #     f"SHOULDNT BE {x_dimen=} {idea_number_value} : {get_default_sorted_list(dimen_keys)}"
                    # )
                assert x_dimen not in format_dimens

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
    assert br00021_filename == idea_format_00021_belief_voiceunit_v0_0_0()
    assert br00020_filename == idea_format_00020_belief_voice_membership_v0_0_0()
    assert br00013_filename == idea_format_00013_planunit_v0_0_0()

    all_set = {get_idea_format_filename(br) for br in get_idea_numbers()}
    assert all_set == get_idea_format_filenames()


def set_idea_config_json(dimen: str, build_order: int):
    x_idea_config = get_idea_config_dict()
    dimen_dict = x_idea_config.get(dimen)
    dimen_dict[build_order_str()] = build_order
    x_idea_config[dimen] = dimen_dict
    save_json(idea_config_path(), None, x_idea_config)


def test_get_idea_config_dict_ReturnsObj_build_order():
    # ESTABLISH / WHEN
    bo = build_order_str()
    # set_idea_config_json(pidgin_name_str(), 0)
    # set_idea_config_json(pidgin_title_str(), 1)
    # set_idea_config_json(pidgin_label_str(), 2)
    # set_idea_config_json(pidgin_rope_str(), 3)
    # set_idea_config_json(momentunit_str(), 5)
    # set_idea_config_json(moment_timeline_hour_str(), 6)
    # set_idea_config_json(moment_timeline_month_str(), 7)
    # set_idea_config_json(moment_timeline_weekday_str(), 8)
    # set_idea_config_json(belief_voice_membership_str(), 9)
    # set_idea_config_json(belief_voiceunit_str(), 10)
    # set_idea_config_json(belief_plan_awardunit_str(), 11)
    # set_idea_config_json(belief_plan_factunit_str(), 12)
    # set_idea_config_json(belief_plan_partyunit_str(), 14)
    # set_idea_config_json(belief_plan_healerunit_str(), 15)
    # set_idea_config_json(belief_plan_reason_caseunit_str(), 16)
    # set_idea_config_json(belief_plan_reasonunit_str(), 17)
    # set_idea_config_json(belief_planunit_str(), 18)
    # set_idea_config_json(beliefunit_str(), 19)
    # set_idea_config_json(moment_budunit_str(), 20)
    # set_idea_config_json(moment_paybook_str(), 21)

    x_idea_config = get_idea_config_dict()

    # THEN
    assert x_idea_config.get(pidgin_name_str()).get(bo) == 0
    assert x_idea_config.get(pidgin_title_str()).get(bo) == 1
    assert x_idea_config.get(pidgin_label_str()).get(bo) == 2
    assert x_idea_config.get(pidgin_rope_str()).get(bo) == 3
    assert x_idea_config.get(momentunit_str()).get(bo) == 5
    assert x_idea_config.get(moment_timeline_hour_str()).get(bo) == 6
    assert x_idea_config.get(moment_timeline_month_str()).get(bo) == 7
    assert x_idea_config.get(moment_timeline_weekday_str()).get(bo) == 8
    assert x_idea_config.get(belief_voice_membership_str()).get(bo) == 9
    assert x_idea_config.get(belief_voiceunit_str()).get(bo) == 10
    assert x_idea_config.get(belief_plan_awardunit_str()).get(bo) == 11
    assert x_idea_config.get(belief_plan_factunit_str()).get(bo) == 12
    assert x_idea_config.get(belief_plan_partyunit_str()).get(bo) == 14
    assert x_idea_config.get(belief_plan_healerunit_str()).get(bo) == 15
    assert x_idea_config.get(belief_plan_reason_caseunit_str()).get(bo) == 16
    assert x_idea_config.get(belief_plan_reasonunit_str()).get(bo) == 17
    assert x_idea_config.get(belief_planunit_str()).get(bo) == 18
    assert x_idea_config.get(beliefunit_str()).get(bo) == 19
    assert x_idea_config.get(moment_budunit_str()).get(bo) == 20
    assert x_idea_config.get(moment_paybook_str()).get(bo) == 21


def test_get_quick_ideas_column_ref_ReturnsObj():
    # ESTABLISH / WHEN
    x_idea_quick_column_ref = get_quick_ideas_column_ref()

    # THEN
    assert len(x_idea_quick_column_ref) == len(get_idea_numbers())
    assert x_idea_quick_column_ref.get("br00000") == {
        event_int_str(),
        face_name_str(),
        c400_number_str(),
        moment_label_str(),
        fund_iota_str(),
        monthday_distortion_str(),
        penny_str(),
        respect_bit_str(),
        knot_str(),
        timeline_label_str(),
        yr1_jan1_offset_str(),
        job_listen_rotations_str(),
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
                expected_idea_dimen_ref[x_dimen] = {idea_number}
            else:
                expected_idea_dimen_ref.get(x_dimen).add(idea_number)
    return expected_idea_dimen_ref


def test_get_idea_dimen_ref_ReturnsObj():
    # ESTABLISH
    expected_idea_dimen_ref = _create_expected_idea_dimen_ref()
    print(f"{expected_idea_dimen_ref=}")

    # WHEN / THEN
    assert get_idea_dimen_ref() == expected_idea_dimen_ref
