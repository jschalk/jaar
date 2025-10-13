from copy import copy as copy_copy
from os import getcwd as os_getcwd
from src.ch01_py.file_toolbox import create_path, save_json
from src.ch07_belief_logic.belief_config import (
    get_all_belief_calc_args,
    get_belief_calc_args_sqlite_datatype_dict,
)
from src.ch09_belief_atom.atom_config import (
    get_all_belief_dimen_delete_keys,
    get_atom_args_dimen_mapping,
    get_atom_config_dict,
    get_belief_dimens,
)
from src.ch15_moment.moment_config import (
    get_moment_args_dimen_mapping,
    get_moment_config_dict,
    get_moment_dimens,
)
from src.ch16_translate.translate_config import (
    get_translate_args_dimen_mapping,
    get_translate_config_dict,
    get_translate_dimens,
    get_translateable_args,
)
from src.ch17_idea.idea_config import (
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
from src.ref.keywords import Ch17Keywords as wx


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
    translate_args = set(get_translate_args_dimen_mapping().keys())
    assert translate_args.issubset(set(table_sorting_priority))
    all_belief_dimen_delete_keys = get_all_belief_dimen_delete_keys()
    print(f"missing {all_belief_dimen_delete_keys.difference(table_sorting_priority)}")
    assert all_belief_dimen_delete_keys.issubset(table_sorting_priority)
    belief_calc_args = set(get_all_belief_calc_args().keys())
    # for belief_calc_arg in belief_calc_args.difference(table_sorting_priority):
    #     print(f"{belief_calc_arg=}")
    print(f"{belief_calc_args.difference(table_sorting_priority)=}")
    assert belief_calc_args.issubset(table_sorting_priority)
    translateable_otx_cols = {f"{trl_arg}_otx" for trl_arg in get_translateable_args()}
    translateable_inx_cols = {f"{trl_arg}_inx" for trl_arg in get_translateable_args()}
    x_delete_keys = all_belief_dimen_delete_keys
    translateable_delete_otx_cols = {f"{trl_arg}_otx" for trl_arg in x_delete_keys}
    translateable_delete_inx_cols = {f"{trl_arg}_inx" for trl_arg in x_delete_keys}
    print(f"{translateable_delete_otx_cols=}")
    print(f"{translateable_delete_inx_cols=}")
    assert translateable_otx_cols.issubset(table_sorting_priority)
    assert translateable_inx_cols.issubset(table_sorting_priority)
    assert translateable_delete_otx_cols.issubset(table_sorting_priority)
    assert translateable_delete_inx_cols.issubset(table_sorting_priority)

    # all the suffix otx/inx columns are only used in one table
    assert table_sorting_priority[0] == "world_name"
    assert table_sorting_priority[1] == "idea_number"
    assert table_sorting_priority[2] == "source_dimen"
    assert table_sorting_priority[3] == "translate_spark_num"
    assert table_sorting_priority[4] == wx.spark_num
    assert table_sorting_priority[5] == wx.face_name
    assert table_sorting_priority[6] == "face_name_otx"
    assert table_sorting_priority[7] == "face_name_inx"
    assert table_sorting_priority[8] == wx.moment_label
    assert table_sorting_priority[9] == "moment_label_otx"
    assert table_sorting_priority[10] == "moment_label_inx"
    assert table_sorting_priority[11] == "epoch_label"
    assert table_sorting_priority[12] == "epoch_label_otx"
    assert table_sorting_priority[13] == "epoch_label_inx"
    assert table_sorting_priority[14] == wx.offi_time
    assert table_sorting_priority[15] == wx.c400_number
    assert table_sorting_priority[16] == wx.yr1_jan1_offset
    assert table_sorting_priority[17] == wx.monthday_index
    assert table_sorting_priority[18] == wx.cumulative_day
    assert table_sorting_priority[19] == wx.month_label
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
    assert table_sorting_priority[30] == wx.belief_name
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
    assert table_sorting_priority[75] == wx.party_title
    assert table_sorting_priority[76] == "party_title_otx"
    assert table_sorting_priority[77] == "party_title_inx"
    assert table_sorting_priority[78] == "party_title_ERASE"
    assert table_sorting_priority[79] == "party_title_ERASE_otx"
    assert table_sorting_priority[80] == "party_title_ERASE_inx"
    assert table_sorting_priority[81] == wx.solo
    assert table_sorting_priority[82] == wx.awardee_title
    assert table_sorting_priority[83] == "awardee_title_otx"
    assert table_sorting_priority[84] == "awardee_title_inx"
    assert table_sorting_priority[85] == "awardee_title_ERASE"
    assert table_sorting_priority[86] == "awardee_title_ERASE_otx"
    assert table_sorting_priority[87] == "awardee_title_ERASE_inx"
    assert table_sorting_priority[88] == wx.healer_name
    assert table_sorting_priority[89] == "healer_name_otx"
    assert table_sorting_priority[90] == "healer_name_inx"
    assert table_sorting_priority[91] == "healer_name_ERASE"
    assert table_sorting_priority[92] == "healer_name_ERASE_otx"
    assert table_sorting_priority[93] == "healer_name_ERASE_inx"
    assert table_sorting_priority[94] == wx.bud_time
    assert table_sorting_priority[95] == wx.tran_time
    assert table_sorting_priority[96] == wx.begin
    assert table_sorting_priority[97] == wx.close
    assert table_sorting_priority[98] == wx.addin
    assert table_sorting_priority[99] == wx.numor
    assert table_sorting_priority[100] == wx.denom
    assert table_sorting_priority[101] == wx.morph
    assert table_sorting_priority[102] == wx.gogo_want
    assert table_sorting_priority[103] == wx.stop_want
    assert table_sorting_priority[104] == wx.reason_active_requisite
    assert table_sorting_priority[105] == wx.voice_cred_lumen
    assert table_sorting_priority[106] == wx.voice_debt_lumen
    assert table_sorting_priority[107] == wx.group_cred_lumen
    assert table_sorting_priority[108] == wx.group_debt_lumen
    assert table_sorting_priority[109] == wx.credor_respect
    assert table_sorting_priority[110] == wx.debtor_respect
    assert table_sorting_priority[111] == wx.fact_lower
    assert table_sorting_priority[112] == wx.fact_upper
    assert table_sorting_priority[113] == wx.fund_pool
    assert table_sorting_priority[114] == wx.give_force
    assert table_sorting_priority[115] == wx.star
    assert table_sorting_priority[116] == wx.max_tree_traverse
    assert table_sorting_priority[117] == wx.reason_upper
    assert table_sorting_priority[118] == wx.reason_lower
    assert table_sorting_priority[119] == wx.reason_divisor
    assert table_sorting_priority[120] == wx.pledge
    assert table_sorting_priority[121] == wx.problem_bool
    assert table_sorting_priority[122] == wx.take_force
    assert table_sorting_priority[123] == wx.tally
    assert table_sorting_priority[124] == wx.fund_grain
    assert table_sorting_priority[125] == wx.money_grain
    assert table_sorting_priority[126] == wx.respect_grain
    assert table_sorting_priority[127] == wx.amount
    assert table_sorting_priority[128] == wx.otx_label
    assert table_sorting_priority[129] == wx.inx_label
    assert table_sorting_priority[130] == wx.otx_rope
    assert table_sorting_priority[131] == wx.inx_rope
    assert table_sorting_priority[132] == wx.otx_name
    assert table_sorting_priority[133] == wx.inx_name
    assert table_sorting_priority[134] == wx.otx_title
    assert table_sorting_priority[135] == wx.inx_title
    assert table_sorting_priority[136] == wx.otx_knot
    assert table_sorting_priority[137] == wx.inx_knot
    assert table_sorting_priority[138] == wx.knot
    assert table_sorting_priority[139] == wx.unknown_str
    assert table_sorting_priority[140] == wx.quota
    assert table_sorting_priority[141] == wx.celldepth
    assert table_sorting_priority[142] == wx.job_listen_rotations
    assert table_sorting_priority[143] == wx.error_message
    assert table_sorting_priority[144] == "_belief_name_is_labor"
    assert table_sorting_priority[145] == wx.active
    assert table_sorting_priority[146] == wx.task
    assert table_sorting_priority[147] == wx.status
    assert table_sorting_priority[148] == wx.credor_pool
    assert table_sorting_priority[149] == wx.debtor_pool
    assert table_sorting_priority[150] == wx.rational
    assert table_sorting_priority[151] == wx.fund_give
    assert table_sorting_priority[152] == wx.fund_take
    assert table_sorting_priority[153] == wx.fund_onset
    assert table_sorting_priority[154] == wx.fund_cease
    assert table_sorting_priority[155] == wx.fund_ratio
    assert table_sorting_priority[156] == wx.fund_agenda_give
    assert table_sorting_priority[157] == wx.fund_agenda_take
    assert table_sorting_priority[158] == wx.fund_agenda_ratio_give
    assert table_sorting_priority[159] == wx.fund_agenda_ratio_take
    assert table_sorting_priority[160] == wx.inallocable_voice_debt_lumen
    assert table_sorting_priority[161] == wx.gogo_calc
    assert table_sorting_priority[162] == wx.stop_calc
    assert table_sorting_priority[163] == wx.tree_level
    assert table_sorting_priority[164] == wx.range_evaluated
    assert table_sorting_priority[165] == wx.descendant_pledge_count
    assert table_sorting_priority[166] == wx.healerunit_ratio
    assert table_sorting_priority[167] == wx.all_voice_cred
    assert table_sorting_priority[168] == wx.keeps_justified
    assert table_sorting_priority[169] == wx.offtrack_fund
    assert table_sorting_priority[170] == "_reason_active_heir"
    assert table_sorting_priority[171] == "irrational_voice_debt_lumen"
    assert table_sorting_priority[172] == wx.sum_healerunit_plans_fund_total
    assert table_sorting_priority[173] == wx.keeps_buildable
    assert table_sorting_priority[174] == wx.all_voice_debt
    assert table_sorting_priority[175] == wx.tree_traverse_count
    assert table_sorting_priority[176] == "funds"
    assert table_sorting_priority[177] == "fund_rank"
    assert table_sorting_priority[178] == "pledges_count"

    assert len(table_sorting_priority) == 179
    all_args = copy_copy(atom_args)
    all_args.update(all_belief_dimen_delete_keys)
    all_args.update(moment_args)
    all_args.update(translate_args)
    all_args.update(belief_calc_args)
    all_args.update(translateable_otx_cols)
    all_args.update(translateable_inx_cols)
    all_args.update(translateable_delete_otx_cols)
    all_args.update(translateable_delete_inx_cols)
    all_args.add(wx.idea_number)
    all_args.add(wx.spark_num)
    all_args.add(wx.face_name)
    all_args.add("source_dimen")
    all_args.add("translate_spark_num")
    all_args.add(wx.error_message)
    all_args.add(wx.world_name)
    all_args.add("funds")  # kpi columns
    all_args.add("fund_rank")  # kpi columns
    all_args.add("pledges_count")  # kpi columns
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
    assert sqlite_types.get(wx.idea_number) == "TEXT"
    assert sqlite_types.get(wx.face_name) == "TEXT"
    assert sqlite_types.get("translate_spark_num") == "INTEGER"
    assert sqlite_types.get(wx.spark_num) == "INTEGER"
    assert sqlite_types.get(wx.moment_label) == "TEXT"
    assert sqlite_types.get(wx.belief_name) == "TEXT"
    assert sqlite_types.get(wx.voice_name) == "TEXT"
    assert sqlite_types.get(wx.group_title) == "TEXT"
    assert sqlite_types.get(wx.plan_rope) == "TEXT"
    assert sqlite_types.get(wx.reason_context) == "TEXT"
    assert sqlite_types.get(wx.reason_state) == "TEXT"
    assert sqlite_types.get(wx.fact_state) == "TEXT"
    assert sqlite_types.get(wx.party_title) == "TEXT"
    assert sqlite_types.get(wx.awardee_title) == "TEXT"
    assert sqlite_types.get(wx.healer_name) == "TEXT"
    assert sqlite_types.get(wx.offi_time) == "INTEGER"
    assert sqlite_types.get(wx.bud_time) == "INTEGER"
    assert sqlite_types.get(wx.tran_time) == "INTEGER"
    assert sqlite_types.get(wx.begin) == "REAL"
    assert sqlite_types.get(wx.close) == "REAL"
    assert sqlite_types.get(wx.addin) == "REAL"
    assert sqlite_types.get(wx.numor) == "INTEGER"
    assert sqlite_types.get(wx.denom) == "INTEGER"
    assert sqlite_types.get(wx.morph) == "INTEGER"
    assert sqlite_types.get(wx.gogo_want) == "REAL"
    assert sqlite_types.get(wx.stop_want) == "REAL"
    assert sqlite_types.get(wx.reason_active_requisite) == "INTEGER"
    assert sqlite_types.get(wx.voice_cred_lumen) == "REAL"
    assert sqlite_types.get(wx.voice_debt_lumen) == "REAL"
    assert sqlite_types.get(wx.group_cred_lumen) == "REAL"
    assert sqlite_types.get(wx.group_debt_lumen) == "REAL"
    assert sqlite_types.get(wx.credor_respect) == "REAL"
    assert sqlite_types.get(wx.debtor_respect) == "REAL"
    assert sqlite_types.get(wx.fact_lower) == "REAL"
    assert sqlite_types.get(wx.fact_upper) == "REAL"
    assert sqlite_types.get(wx.fund_pool) == "REAL"
    assert sqlite_types.get(wx.give_force) == "REAL"
    assert sqlite_types.get(wx.star) == "INTEGER"
    assert sqlite_types.get(wx.max_tree_traverse) == "INTEGER"
    assert sqlite_types.get(wx.reason_upper) == "REAL"
    assert sqlite_types.get(wx.reason_lower) == "REAL"
    assert sqlite_types.get(wx.reason_divisor) == "INTEGER"
    assert sqlite_types.get(wx.problem_bool) == "INTEGER"
    assert sqlite_types.get(wx.take_force) == "REAL"
    assert sqlite_types.get(wx.tally) == "INTEGER"
    assert sqlite_types.get(wx.fund_grain) == "REAL"
    assert sqlite_types.get(wx.money_grain) == "REAL"
    assert sqlite_types.get(wx.pledge) == "INTEGER"
    assert sqlite_types.get(wx.respect_grain) == "REAL"
    assert sqlite_types.get(wx.amount) == "REAL"
    assert sqlite_types.get(wx.month_label) == "TEXT"
    assert sqlite_types.get(wx.hour_label) == "TEXT"
    assert sqlite_types.get(wx.cumulative_minute) == "INTEGER"
    assert sqlite_types.get(wx.cumulative_day) == "INTEGER"
    assert sqlite_types.get(wx.weekday_label) == "TEXT"
    assert sqlite_types.get(wx.weekday_order) == "INTEGER"
    assert sqlite_types.get(wx.otx_knot) == "TEXT"
    assert sqlite_types.get(wx.inx_knot) == "TEXT"
    assert sqlite_types.get(wx.unknown_str) == "TEXT"
    assert sqlite_types.get(wx.knot) == "TEXT"
    assert sqlite_types.get(wx.c400_number) == "INTEGER"
    assert sqlite_types.get(wx.yr1_jan1_offset) == "INTEGER"
    assert sqlite_types.get(wx.quota) == "REAL"
    assert sqlite_types.get(wx.celldepth) == "INTEGER"
    assert sqlite_types.get(wx.monthday_index) == "INTEGER"
    assert sqlite_types.get(wx.epoch_label) == "TEXT"
    assert sqlite_types.get(wx.error_message) == "TEXT"
    assert sqlite_types.get(wx.solo) == "INTEGER"

    # sourcery skip: no-loop-in-tests
    for x_arg, datatype in get_belief_calc_args_sqlite_datatype_dict().items():
        print(f"{x_arg=} {datatype=} {sqlite_types.get(x_arg)=}")
        assert sqlite_types.get(x_arg) == datatype

    assert set(sqlite_types.values()) == {"TEXT", "INTEGER", "REAL"}


def test_get_allowed_curds_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_allowed_curds() == {
        wx.insert_one_time,
        wx.insert_multiple,
        wx.delete_insert_update,
        wx.insert_update,
        wx.delete_insert,
        wx.delete_update,
        wx.INSERT,
        wx.DELETE,
        wx.UPDATE,
    }


def test_idea_config_path_ReturnsObj_Idea() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch17_idea")
    assert idea_config_path() == create_path(chapter_dir, "idea_config.json")


def test_get_idea_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    x_idea_config = get_idea_config_dict()

    # THEN
    assert x_idea_config
    idea_config_dimens = set(x_idea_config.keys())
    assert wx.momentunit in idea_config_dimens
    assert wx.moment_budunit in idea_config_dimens
    assert wx.moment_paybook in idea_config_dimens
    assert wx.moment_epoch_hour in idea_config_dimens
    assert wx.moment_epoch_month in idea_config_dimens
    assert wx.moment_epoch_weekday in idea_config_dimens
    assert wx.moment_timeoffi in idea_config_dimens
    assert wx.belief_voice_membership in idea_config_dimens
    assert wx.belief_voiceunit in idea_config_dimens
    assert wx.belief_plan_awardunit in idea_config_dimens
    assert wx.belief_plan_factunit in idea_config_dimens
    assert wx.belief_plan_partyunit in idea_config_dimens
    assert wx.belief_plan_healerunit in idea_config_dimens
    assert wx.belief_plan_reason_caseunit in idea_config_dimens
    assert wx.belief_plan_reasonunit in idea_config_dimens
    assert wx.belief_planunit in idea_config_dimens
    assert wx.beliefunit in idea_config_dimens
    assert wx.translate_name in idea_config_dimens
    assert wx.translate_title in idea_config_dimens
    assert wx.translate_label in idea_config_dimens
    assert wx.translate_rope in idea_config_dimens
    assert get_belief_dimens().issubset(idea_config_dimens)
    assert get_moment_dimens().issubset(idea_config_dimens)
    assert get_translate_dimens().issubset(idea_config_dimens)
    assert len(x_idea_config) == 21
    _validate_idea_config(x_idea_config)


def get_idea_categorys():
    return {"belief", "moment", "translate"}


def _validate_idea_config(x_idea_config: dict):
    atom_config_dict = get_atom_config_dict()
    moment_config_dict = get_moment_config_dict()
    translate_config_dict = get_translate_config_dict()
    # for every idea_format file there exists a unique idea_number with leading zeros to make 5 digits
    for idea_dimen, idea_dict in x_idea_config.items():
        print(f"{idea_dimen=}")
        assert idea_dict.get(wx.idea_category) in get_idea_categorys()
        assert idea_dict.get(wx.jkeys) is not None
        assert idea_dict.get(wx.jvalues) is not None
        assert idea_dict.get(wx.allowed_crud) is not None
        assert idea_dict.get(wx.UPDATE) is None
        assert idea_dict.get(wx.INSERT) is None
        assert idea_dict.get(wx.DELETE) is None
        assert idea_dict.get(wx.normal_specs) is None
        if idea_dict.get(wx.idea_category) == "belief":
            sub_dimen = atom_config_dict.get(idea_dimen)
        elif idea_dict.get(wx.idea_category) == "moment":
            sub_dimen = moment_config_dict.get(idea_dimen)
        elif idea_dict.get(wx.idea_category) == "translate":
            sub_dimen = translate_config_dict.get(idea_dimen)

        assert idea_dict.get(wx.allowed_crud) in get_allowed_curds()

        if idea_dimen in {
            wx.moment_epoch_hour,
            wx.moment_epoch_month,
            wx.moment_epoch_weekday,
            wx.momentunit,
            "map_otx2inx",
            wx.translate_title,
            wx.translate_name,
            wx.translate_label,
            wx.translate_rope,
        }:
            assert idea_dict.get(wx.allowed_crud) == wx.insert_one_time
        elif idea_dimen in {
            wx.moment_budunit,
            wx.moment_paybook,
            wx.moment_timeoffi,
        }:
            assert idea_dict.get(wx.allowed_crud) == wx.insert_multiple
        elif (
            sub_dimen.get(wx.UPDATE) != None
            and sub_dimen.get(wx.INSERT) != None
            and sub_dimen.get(wx.DELETE) != None
        ):
            assert idea_dict.get(wx.allowed_crud) == wx.delete_insert_update
        elif (
            sub_dimen.get(wx.UPDATE) != None
            and sub_dimen.get(wx.INSERT) != None
            and sub_dimen.get(wx.DELETE) is None
        ):
            assert idea_dict.get(wx.allowed_crud) == wx.insert_update
        elif (
            sub_dimen.get(wx.UPDATE) is None
            and sub_dimen.get(wx.INSERT) != None
            and sub_dimen.get(wx.DELETE) != None
        ):
            assert idea_dict.get(wx.allowed_crud) == wx.delete_insert
        elif (
            sub_dimen.get(wx.UPDATE) != None
            and sub_dimen.get(wx.INSERT) is None
            and sub_dimen.get(wx.DELETE) != None
        ):
            assert idea_dict.get(wx.allowed_crud) == wx.delete_update
        elif (
            sub_dimen.get(wx.UPDATE) != None
            and sub_dimen.get(wx.INSERT) is None
            and sub_dimen.get(wx.DELETE) is None
        ):
            assert idea_dict.get(wx.allowed_crud) == wx.UPDATE
        elif (
            sub_dimen.get(wx.UPDATE) is None
            and sub_dimen.get(wx.INSERT) != None
            and sub_dimen.get(wx.DELETE) is None
        ):
            assert idea_dict.get(wx.allowed_crud) == wx.INSERT
        elif (
            sub_dimen.get(wx.UPDATE) is None
            and sub_dimen.get(wx.INSERT) is None
            and sub_dimen.get(wx.DELETE) != None
        ):
            assert idea_dict.get(wx.allowed_crud) == wx.DELETE
        else:
            test_str = f"{wx.allowed_crud} not checked by test"
            assert idea_dict.get(wx.allowed_crud) == test_str

        sub_jkeys_keys = set(sub_dimen.get(wx.jkeys).keys())
        idea_jkeys_keys = set(idea_dict.get(wx.jkeys).keys())
        # print(f"    {sub_jkeys_keys=}")
        # print(f"  {idea_jkeys_keys=}")
        assert wx.face_name in idea_jkeys_keys
        assert wx.spark_num in idea_jkeys_keys
        if idea_dict.get(wx.idea_category) != "translate":
            assert wx.moment_label in idea_jkeys_keys
        if idea_dict.get(wx.idea_category) == "belief":
            idea_jkeys_keys.remove(wx.moment_label)
            idea_jkeys_keys.remove(wx.belief_name)
        idea_jkeys_keys.remove(wx.face_name)
        idea_jkeys_keys.remove(wx.spark_num)
        assert sub_jkeys_keys == idea_jkeys_keys

        sub_jvalues_keys = set(sub_dimen.get(wx.jvalues).keys())
        print(f"  {sub_jvalues_keys=}")
        if wx.moment_label in sub_jvalues_keys:
            sub_jvalues_keys.remove(wx.moment_label)

        idea_jvalues_dict = idea_dict.get(wx.jvalues)
        idea_jvalues_keys = set(idea_jvalues_dict.keys())
        # print(f"  {sub_jvalues_keys=}")
        # print(f"{idea_jvalues_keys=}")
        assert sub_jvalues_keys == idea_jvalues_keys

        assert wx.moment_label not in idea_jvalues_keys

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
        #     jvalue_column_order = jvalue_dict.get(wx.column_order)
        #     assert jvalue_column_order != None
        #     list_ref_arg = sort_list[jvalue_column_order]
        #     assert list_ref_arg != None
        #     assert jvalue == list_ref_arg

        # # for jkey in idea_jkeys_keys:
        #     print(f"{jkey=} {idea_jkeys_dict=}")
        #     jkey_dict = idea_jkeys_dict.get(jkey)
        #     jkey_column_order = jkey_dict.get(wx.column_order)
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
        dimen: set(dict.get(wx.jkeys).keys())
        for dimen, dict in get_idea_config_dict().items()
    }

    valid_idea_dimens = set()
    valid_idea_dimens.update(get_belief_dimens())
    valid_idea_dimens.update(get_moment_dimens())
    valid_idea_dimens.update(get_translate_dimens())
    print("get_idea_config_dict")
    config_dict = get_idea_config_dict()

    # for every idea_format file there exists a unique idea_number with leading zeros to make 5 digits
    idea_numbers_set = set()
    for idea_filename in idea_filenames:
        ref_dict = get_idearef_from_file(idea_filename)
        # print(f"{idea_filename=} {ref_dict.get(wx.idea_number)=}")
        idea_number_value = ref_dict.get(wx.idea_number)
        assert idea_number_value
        assert idea_number_value[2:8] == idea_filename[12:17]
        idea_numbers_set.add(idea_number_value)

        format_dimens = ref_dict.get(wx.dimens)
        assert format_dimens is not None
        assert len(format_dimens) > 0
        for idea_format_dimen in format_dimens:
            assert idea_format_dimen in valid_idea_dimens

        assert ref_dict.get(wx.attributes)
        idea_format_attributes = ref_dict.get(wx.attributes)
        for idea_attribute, attr_dict in idea_format_attributes.items():
            # print(f"{idea_attribute=}")
            assert wx.otx_key in set(attr_dict.keys())
            otx_key_value = attr_dict.get(wx.otx_key)
            for idea_format_dimen in format_dimens:
                format_config = config_dict.get(idea_format_dimen)
                dimen_required_attrs = set(format_config.get(wx.jkeys).keys())
                dimen_optional_attrs = set(format_config.get(wx.jvalues).keys())
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
        idea_attrs = set(ref_dict.get(wx.attributes).keys())
        idea_attrs_list = get_default_sorted_list(idea_attrs)
        if idea_attrs_list[-1].find("_ERASE") > 0:
            delete_attr_with_erase = idea_attrs_list[-1]
            delete_attr_without_erase = delete_attr_with_erase.replace("_ERASE", "")
            idea_attrs.remove(delete_attr_with_erase)
            idea_attrs.add(delete_attr_without_erase)

        for x_dimen, dimen_keys in all_dimen_keys_dict.items():
            # if x_dimen == wx.belief_plan_factunit and x_dimen in format_dimens:
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

    # assert wx.face_name in idea_format_attributes
    # assert wx.spark_num in idea_format_attributes

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
    dimen_dict[wx.build_order] = build_order
    x_idea_config[dimen] = dimen_dict
    save_json(idea_config_path(), None, x_idea_config)


def test_get_idea_config_dict_ReturnsObj_build_order():
    # ESTABLISH / WHEN
    bo = wx.build_order
    # set_idea_config_json(wx.translate_name, 0)
    # set_idea_config_json(wx.translate_title, 1)
    # set_idea_config_json(wx.translate_label, 2)
    # set_idea_config_json(wx.translate_rope, 3)
    # set_idea_config_json(wx.momentunit, 5)
    # set_idea_config_json(wx.moment_epoch_hour, 6)
    # set_idea_config_json(wx.moment_epoch_month, 7)
    # set_idea_config_json(wx.moment_epoch_weekday, 8)
    # set_idea_config_json(wx.belief_voice_membership, 9)
    # set_idea_config_json(wx.belief_voiceunit, 10)
    # set_idea_config_json(wx.belief_plan_awardunit, 11)
    # set_idea_config_json(wx.belief_plan_factunit, 12)
    # set_idea_config_json(wx.belief_plan_partyunit, 14)
    # set_idea_config_json(wx.belief_plan_healerunit, 15)
    # set_idea_config_json(wx.belief_plan_reason_caseunit, 16)
    # set_idea_config_json(wx.belief_plan_reasonunit, 17)
    # set_idea_config_json(wx.belief_planunit, 18)
    # set_idea_config_json(wx.beliefunit, 19)
    # set_idea_config_json(wx.moment_budunit, 20)
    # set_idea_config_json(wx.moment_paybook, 21)

    x_idea_config = get_idea_config_dict()

    # THEN
    assert x_idea_config.get(wx.translate_name).get(bo) == 0
    assert x_idea_config.get(wx.translate_title).get(bo) == 1
    assert x_idea_config.get(wx.translate_label).get(bo) == 2
    assert x_idea_config.get(wx.translate_rope).get(bo) == 3
    assert x_idea_config.get(wx.momentunit).get(bo) == 5
    assert x_idea_config.get(wx.moment_epoch_hour).get(bo) == 6
    assert x_idea_config.get(wx.moment_epoch_month).get(bo) == 7
    assert x_idea_config.get(wx.moment_epoch_weekday).get(bo) == 8
    assert x_idea_config.get(wx.belief_voice_membership).get(bo) == 9
    assert x_idea_config.get(wx.belief_voiceunit).get(bo) == 10
    assert x_idea_config.get(wx.belief_plan_awardunit).get(bo) == 11
    assert x_idea_config.get(wx.belief_plan_factunit).get(bo) == 12
    assert x_idea_config.get(wx.belief_plan_partyunit).get(bo) == 14
    assert x_idea_config.get(wx.belief_plan_healerunit).get(bo) == 15
    assert x_idea_config.get(wx.belief_plan_reason_caseunit).get(bo) == 16
    assert x_idea_config.get(wx.belief_plan_reasonunit).get(bo) == 17
    assert x_idea_config.get(wx.belief_planunit).get(bo) == 18
    assert x_idea_config.get(wx.beliefunit).get(bo) == 19
    assert x_idea_config.get(wx.moment_budunit).get(bo) == 20
    assert x_idea_config.get(wx.moment_paybook).get(bo) == 21


def test_get_quick_ideas_column_ref_ReturnsObj():
    # ESTABLISH / WHEN
    x_idea_quick_column_ref = get_quick_ideas_column_ref()

    # THEN
    assert len(x_idea_quick_column_ref) == len(get_idea_numbers())
    assert x_idea_quick_column_ref.get("br00000") == {
        wx.spark_num,
        wx.face_name,
        wx.c400_number,
        wx.moment_label,
        wx.fund_grain,
        wx.monthday_index,
        wx.money_grain,
        wx.respect_grain,
        wx.knot,
        wx.epoch_label,
        wx.yr1_jan1_offset,
        wx.job_listen_rotations,
    }


def _create_expected_idea_dimen_ref() -> dict[str, list[str]]:
    idea_numbers_sorted = list(get_idea_numbers())
    idea_numbers_sorted.sort(key=lambda x: x)
    expected_idea_dimen_ref = {}
    for idea_number in idea_numbers_sorted:
        idea_format_filename = get_idea_format_filename(idea_number)
        x_idearef = get_idearef_from_file(idea_format_filename)
        dimens_list = x_idearef.get(wx.dimens)
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
