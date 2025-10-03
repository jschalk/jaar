# from src.ch01_data_toolbox.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd
from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch07_belief_logic.belief_config import (
    belief_config_path,
    get_all_belief_calc_args,
    get_belief_calc_args_sqlite_datatype_dict,
    get_belief_calc_args_type_dict,
    get_belief_calc_dimen_args,
    get_belief_calc_dimens,
    get_belief_config_dict,
    max_tree_traverse_default,
)
from src.ref.ch07_keywords import Ch07Keywords as wx


def test_max_tree_traverse_default_ReturnsObj() -> str:
    # ESTABLISH / WHEN / THEN
    assert max_tree_traverse_default() == 20


def test_get_belief_config_dict_Exists():
    # ESTABLISH
    src_dir = create_path(os_getcwd(), "src")
    expected_dir = create_path(src_dir, "ch07_belief_logic")

    # WHEN
    config_path = belief_config_path()
    # THEN
    expected_path = create_path(expected_dir, "belief_config.json")
    assert config_path == expected_path
    assert os_path_exists(belief_config_path())


def test_get_belief_config_dict_ReturnsObj_CheckLevel0Keys():
    # ESTABLISH / WHEN
    belief_config = get_belief_config_dict()
    belief_config_keys = set(belief_config.keys())

    # THEN
    assert wx.beliefunit in belief_config_keys
    assert wx.belief_voiceunit in belief_config_keys
    assert wx.belief_voice_membership in belief_config_keys
    assert wx.belief_planunit in belief_config_keys
    assert wx.belief_plan_awardunit in belief_config_keys
    assert wx.belief_plan_reasonunit in belief_config_keys
    assert wx.belief_plan_reason_caseunit in belief_config_keys
    assert wx.belief_plan_partyunit in belief_config_keys
    assert wx.belief_plan_healerunit in belief_config_keys
    assert wx.belief_plan_factunit in belief_config_keys
    assert wx.belief_groupunit in belief_config_keys
    assert len(get_belief_config_dict()) == 11


def test_get_belief_config_dict_ReturnsObj_CheckLevel1Keys():
    # ESTABLISH / WHEN
    belief_config = get_belief_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests
    for level1_key, attribute_dict in belief_config.items():
        attribute_keys = set(attribute_dict.keys())
        print(f"{level1_key=} {attribute_keys=}")
        assert "abbreviation" in attribute_keys
        assert wx.jkeys in attribute_keys
        assert wx.jvalues in attribute_keys
        assert len(attribute_keys) == 3


def test_get_belief_config_dict_ReturnsObj_Check_populate_by_cashout():
    # ESTABLISH / WHEN
    belief_config = get_belief_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    abbr_str = "abbreviation"
    for level1_key, attribute_dict in belief_config.items():
        for level2_key, fm_attribute_dict in attribute_dict.items():
            if level2_key != abbr_str:
                for fm_attr_key, fm_attr_value in fm_attribute_dict.items():
                    populate_by_cashout_value = fm_attr_value.get("populate_by_cashout")
                    assertion_fail_str = f"{fm_attr_key} Value must be Boolean {populate_by_cashout_value=}"
                    assert populate_by_cashout_value in [
                        True,
                        False,
                    ], assertion_fail_str


def test_get_belief_config_dict_ReturnsObj_CheckAbbreviations():
    # ESTABLISH / WHEN
    belief_config = get_belief_config_dict()

    # THEN
    blrunit_attribute = belief_config.get(wx.beliefunit)
    blrpern_attribute = belief_config.get(wx.belief_voiceunit)
    blrmemb_attribute = belief_config.get(wx.belief_voice_membership)
    blrplan_attribute = belief_config.get(wx.belief_planunit)
    blrawar_attribute = belief_config.get(wx.belief_plan_awardunit)
    blrreas_attribute = belief_config.get(wx.belief_plan_reasonunit)
    blrprem_attribute = belief_config.get(wx.belief_plan_reason_caseunit)
    blrlabo_attribute = belief_config.get(wx.belief_plan_partyunit)
    blrheal_attribute = belief_config.get(wx.belief_plan_healerunit)
    blrfact_attribute = belief_config.get(wx.belief_plan_factunit)
    blrgrou_attribute = belief_config.get(wx.belief_groupunit)
    abbr_str = "abbreviation"
    assert blrunit_attribute.get(abbr_str) == "blrunit"
    assert blrpern_attribute.get(abbr_str) == "blrpern"
    assert blrmemb_attribute.get(abbr_str) == "blrmemb"
    assert blrplan_attribute.get(abbr_str) == "blrplan"
    assert blrawar_attribute.get(abbr_str) == "blrawar"
    assert blrreas_attribute.get(abbr_str) == "blrreas"
    assert blrprem_attribute.get(abbr_str) == "blrprem"
    assert blrlabo_attribute.get(abbr_str) == "blrlabo"
    assert blrheal_attribute.get(abbr_str) == "blrheal"
    assert blrfact_attribute.get(abbr_str) == "blrfact"
    assert blrgrou_attribute.get(abbr_str) == "blrgrou"


def test_get_all_belief_calc_args_ReturnsObj():
    # ESTABLISH / WHEN
    all_belief_calc_args = get_all_belief_calc_args()

    # THEN
    assert all_belief_calc_args
    assert wx.stop_want in all_belief_calc_args
    assert wx.plan_rope in all_belief_calc_args
    assert "fund_give" in all_belief_calc_args
    assert all_belief_calc_args.get("fund_give") == {
        "belief_plan_awardunit",
        "belief_voice_membership",
        "belief_groupunit",
        "belief_voiceunit",
    }

    assert len(all_belief_calc_args) == 77


def test_get_belief_config_dict_ReturnsObj_CheckArgDataTypesKeysExist():
    # ESTABLISH / WHEN
    belief_config = get_belief_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, attribute_dict in belief_config.items():
        for level2_key, fm_attribute_dict in attribute_dict.items():
            if level2_key in {wx.jkeys, wx.jvalues}:
                for level3_key, attr_dict in fm_attribute_dict.items():
                    print(
                        f"{level1_key=} {level2_key=} {level3_key=} {set(attr_dict.keys())=}"
                    )
                    assert set(attr_dict.keys()) == {
                        wx.class_type,
                        wx.sqlite_datatype,
                        "populate_by_cashout",
                    }


def test_get_belief_calc_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    belief_calc_dimens = get_belief_calc_dimens()

    # THEN
    expected_belief_calc_dimens = {
        wx.beliefunit,
        wx.belief_voiceunit,
        wx.belief_voice_membership,
        wx.belief_planunit,
        wx.belief_plan_awardunit,
        wx.belief_plan_reasonunit,
        wx.belief_plan_reason_caseunit,
        wx.belief_plan_partyunit,
        wx.belief_plan_healerunit,
        wx.belief_plan_factunit,
        wx.belief_groupunit,
    }
    assert belief_calc_dimens == expected_belief_calc_dimens
    assert belief_calc_dimens == set(get_belief_config_dict().keys())


def test_get_belief_calc_dimen_args_ReturnsObj():
    # ESTABLISH / WHEN
    belief_voiceunit_args = get_belief_calc_dimen_args(wx.belief_voiceunit)
    belief_planunit_args = get_belief_calc_dimen_args(wx.belief_planunit)
    belief_groupunit_args = get_belief_calc_dimen_args(wx.belief_groupunit)

    #  THEN
    print(f"{belief_voiceunit_args=}")
    print(f"{belief_groupunit_args=}")
    assert belief_voiceunit_args == {
        wx.moment_label,
        wx.belief_name,
        wx.fund_agenda_give,
        wx.credor_pool,
        wx.fund_give,
        wx.voice_cred_points,
        wx.voice_name,
        wx.voice_debt_points,
        wx.fund_agenda_ratio_take,
        wx.inallocable_voice_debt_points,
        wx.fund_agenda_ratio_give,
        wx.fund_agenda_take,
        wx.fund_take,
        wx.debtor_pool,
        wx.irrational_voice_debt_points,
    }
    assert belief_planunit_args == {
        wx.moment_label,
        wx.belief_name,
        wx.morph,
        wx.denom,
        wx.pledge,
        wx.close,
        wx.addin,
        wx.numor,
        wx.star,
        wx.stop_want,
        wx.gogo_calc,
        wx.stop_calc,
        wx.active,
        wx.fund_onset,
        wx.fund_cease,
        wx.descendant_pledge_count,
        wx.all_voice_cred,
        wx.all_voice_debt,
        wx.healerunit_ratio,
        wx.tree_level,
        wx.task,
        wx.fund_grain,
        wx.fund_ratio,
        wx.range_evaluated,
        wx.problem_bool,
        wx.gogo_want,
        wx.plan_rope,
        wx.begin,
    }
    assert belief_groupunit_args == {
        wx.moment_label,
        wx.belief_name,
        wx.debtor_pool,
        wx.credor_pool,
        wx.fund_give,
        wx.group_title,
        wx.knot,
        wx.fund_agenda_give,
        wx.fund_agenda_take,
        wx.fund_take,
        wx.fund_grain,
    }


def g_class_type(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get(wx.class_type)


def g_sqlitetype(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get(wx.sqlite_datatype)


def g_popcashout(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get("populate_by_cashout")


def test_get_belief_config_dict_ReturnsObj_CheckArgDataTypesCorrect():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH / WHEN
    cfig = get_belief_config_dict()

    # THEN
    # for level1_key, attribute_dict in config.items():
    #     for level2_key, fm_attribute_dict in attribute_dict.items():
    #         if level2_key in {wx.jkeys, wx.jvalues}:
    #             for level3_key, attr_dict in fm_attribute_dict.items():
    #                 dimem = attribute_dict.get("abbreviation")
    #                 x_class_type = attr_dict.get(wx.class_type)
    #                 x_sqlite_datatype = attr_dict.get(wx.sqlite_datatype)
    #                 print(
    #                     f"""    assert g_class_type(config, {dimem}, {level2_key[0:2]}, "{level3_key}") == "{x_class_type}" """
    #                 )
    #                 print(
    #                     f"""    assert g_sqlitetype(config, {dimem}, {level2_key[0:2]}, "{level3_key}") == "{x_sqlite_datatype}" """
    #                 )

    jk = "jkeys"
    jv = "jvalues"
    blfunit = wx.beliefunit
    blrpern = wx.belief_voiceunit
    blrmemb = wx.belief_voice_membership
    blrplan = wx.belief_planunit
    blrawar = wx.belief_plan_awardunit
    blrreas = wx.belief_plan_reasonunit
    blrprem = wx.belief_plan_reason_caseunit
    blrlabo = wx.belief_plan_partyunit
    blrheal = wx.belief_plan_healerunit
    blrfact = wx.belief_plan_factunit
    blrgrou = wx.belief_groupunit
    assert g_class_type(cfig, blrmemb, jk, wx.voice_name) == wx.NameTerm
    assert g_sqlitetype(cfig, blrmemb, jk, wx.voice_name) == "TEXT"
    assert g_popcashout(cfig, blrmemb, jk, wx.voice_name) == False

    assert g_class_type(cfig, blrmemb, jk, wx.group_title) == wx.TitleTerm
    assert g_sqlitetype(cfig, blrmemb, jk, wx.group_title) == "TEXT"
    assert g_popcashout(cfig, blrmemb, jk, wx.group_title) == False

    assert g_class_type(cfig, blrmemb, jv, wx.credor_pool) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, wx.credor_pool) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, wx.credor_pool) == True

    assert g_class_type(cfig, blrmemb, jv, wx.debtor_pool) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, wx.debtor_pool) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, wx.debtor_pool) == True

    assert g_class_type(cfig, blrmemb, jv, wx.fund_agenda_give) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, wx.fund_agenda_give) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, wx.fund_agenda_give) == True

    assert g_class_type(cfig, blrmemb, jv, wx.fund_agenda_ratio_give) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, wx.fund_agenda_ratio_give) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, wx.fund_agenda_ratio_give) == True

    assert g_class_type(cfig, blrmemb, jv, wx.fund_agenda_ratio_take) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, wx.fund_agenda_ratio_take) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, wx.fund_agenda_ratio_take) == True

    assert g_class_type(cfig, blrmemb, jv, wx.fund_agenda_take) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, wx.fund_agenda_take) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, wx.fund_agenda_take) == True

    assert g_class_type(cfig, blrmemb, jv, wx.fund_give) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, wx.fund_give) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, wx.fund_give) == True

    assert g_class_type(cfig, blrmemb, jv, wx.fund_take) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, wx.fund_take) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, wx.fund_take) == True

    assert g_class_type(cfig, blrmemb, jv, wx.group_cred_points) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, wx.group_cred_points) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, wx.group_cred_points) == False

    assert g_class_type(cfig, blrmemb, jv, wx.group_debt_points) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, wx.group_debt_points) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, wx.group_debt_points) == False

    assert g_class_type(cfig, blrpern, jk, wx.voice_name) == wx.NameTerm
    assert g_sqlitetype(cfig, blrpern, jk, wx.voice_name) == "TEXT"
    assert g_popcashout(cfig, blrpern, jk, wx.voice_name) == False

    assert g_class_type(cfig, blrpern, jv, wx.credor_pool) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, wx.credor_pool) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, wx.credor_pool) == True

    assert g_class_type(cfig, blrpern, jv, wx.debtor_pool) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, wx.debtor_pool) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, wx.debtor_pool) == True

    assert g_class_type(cfig, blrpern, jv, wx.fund_agenda_give) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, wx.fund_agenda_give) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, wx.fund_agenda_give) == True

    assert g_class_type(cfig, blrpern, jv, wx.fund_agenda_ratio_give) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, wx.fund_agenda_ratio_give) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, wx.fund_agenda_ratio_give) == True

    assert g_class_type(cfig, blrpern, jv, wx.fund_agenda_ratio_take) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, wx.fund_agenda_ratio_take) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, wx.fund_agenda_ratio_take) == True

    assert g_class_type(cfig, blrpern, jv, wx.fund_agenda_take) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, wx.fund_agenda_take) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, wx.fund_agenda_take) == True

    assert g_class_type(cfig, blrpern, jv, wx.fund_give) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, wx.fund_give) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, wx.fund_give) == True

    assert g_class_type(cfig, blrpern, jv, wx.fund_take) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, wx.fund_take) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, wx.fund_take) == True

    assert g_class_type(cfig, blrpern, jv, wx.inallocable_voice_debt_points) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, wx.inallocable_voice_debt_points) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, wx.inallocable_voice_debt_points) == True

    assert g_class_type(cfig, blrpern, jv, wx.irrational_voice_debt_points) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, wx.irrational_voice_debt_points) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, wx.irrational_voice_debt_points) == True

    assert g_class_type(cfig, blrpern, jv, wx.voice_cred_points) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, wx.voice_cred_points) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, wx.voice_cred_points) == False

    assert g_class_type(cfig, blrpern, jv, wx.voice_debt_points) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, wx.voice_debt_points) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, wx.voice_debt_points) == False

    assert g_class_type(cfig, blrgrou, jk, wx.group_title) == "TitleTerm"
    assert g_sqlitetype(cfig, blrgrou, jk, wx.group_title) == "TEXT"
    assert g_popcashout(cfig, blrgrou, jk, wx.group_title) == True

    assert g_class_type(cfig, blrgrou, jv, wx.knot) == "str"
    assert g_sqlitetype(cfig, blrgrou, jv, wx.knot) == "TEXT"
    assert g_popcashout(cfig, blrgrou, jv, wx.knot) == True

    assert g_class_type(cfig, blrgrou, jv, wx.debtor_pool) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, wx.debtor_pool) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, wx.debtor_pool) == True

    assert g_class_type(cfig, blrgrou, jv, wx.credor_pool) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, wx.credor_pool) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, wx.credor_pool) == True

    assert g_class_type(cfig, blrgrou, jv, wx.fund_give) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, wx.fund_give) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, wx.fund_give) == True

    assert g_class_type(cfig, blrgrou, jv, wx.fund_agenda_give) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, wx.fund_agenda_give) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, wx.fund_agenda_give) == True

    assert g_class_type(cfig, blrgrou, jv, wx.fund_agenda_take) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, wx.fund_agenda_take) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, wx.fund_agenda_take) == True

    assert g_class_type(cfig, blrgrou, jv, wx.fund_take) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, wx.fund_take) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, wx.fund_take) == True

    assert g_class_type(cfig, blrgrou, jv, wx.fund_grain) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, wx.fund_grain) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, wx.fund_grain) == True

    assert g_class_type(cfig, blrawar, jk, wx.awardee_title) == wx.TitleTerm
    assert g_sqlitetype(cfig, blrawar, jk, wx.awardee_title) == "TEXT"
    assert g_popcashout(cfig, blrawar, jk, wx.awardee_title) == False

    assert g_class_type(cfig, blrawar, jk, wx.plan_rope) == wx.RopeTerm
    assert g_sqlitetype(cfig, blrawar, jk, wx.plan_rope) == "TEXT"
    assert g_popcashout(cfig, blrawar, jk, wx.plan_rope) == False

    assert g_class_type(cfig, blrawar, jv, wx.fund_give) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, wx.fund_give) == "REAL"
    assert g_popcashout(cfig, blrawar, jv, wx.fund_give) == True

    assert g_class_type(cfig, blrawar, jv, wx.fund_take) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, wx.fund_take) == "REAL"
    assert g_popcashout(cfig, blrawar, jv, wx.fund_take) == True

    assert g_class_type(cfig, blrawar, jv, wx.give_force) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, wx.give_force) == "REAL"
    assert g_popcashout(cfig, blrawar, jv, wx.give_force) == False

    assert g_class_type(cfig, blrawar, jv, wx.take_force) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, wx.take_force) == "REAL"
    assert g_popcashout(cfig, blrawar, jv, wx.take_force) == False

    assert g_class_type(cfig, blrfact, jk, wx.fact_context) == wx.RopeTerm
    assert g_sqlitetype(cfig, blrfact, jk, wx.fact_context) == "TEXT"
    assert g_popcashout(cfig, blrfact, jk, wx.fact_context) == False

    assert g_class_type(cfig, blrfact, jk, wx.plan_rope) == wx.RopeTerm
    assert g_sqlitetype(cfig, blrfact, jk, wx.plan_rope) == "TEXT"
    assert g_popcashout(cfig, blrfact, jk, wx.plan_rope) == False

    assert g_class_type(cfig, blrfact, jv, wx.fact_upper) == "float"
    assert g_sqlitetype(cfig, blrfact, jv, wx.fact_upper) == "REAL"
    assert g_popcashout(cfig, blrfact, jv, wx.fact_upper) == False

    assert g_class_type(cfig, blrfact, jv, wx.fact_lower) == "float"
    assert g_sqlitetype(cfig, blrfact, jv, wx.fact_lower) == "REAL"
    assert g_popcashout(cfig, blrfact, jv, wx.fact_lower) == False

    assert g_class_type(cfig, blrfact, jv, wx.fact_state) == wx.RopeTerm
    assert g_sqlitetype(cfig, blrfact, jv, wx.fact_state) == "TEXT"
    assert g_popcashout(cfig, blrfact, jv, wx.fact_state) == False

    assert g_class_type(cfig, blrheal, jk, wx.healer_name) == wx.NameTerm
    assert g_sqlitetype(cfig, blrheal, jk, wx.healer_name) == "TEXT"
    assert g_popcashout(cfig, blrheal, jk, wx.healer_name) == False

    assert g_class_type(cfig, blrheal, jk, wx.plan_rope) == wx.RopeTerm
    assert g_sqlitetype(cfig, blrheal, jk, wx.plan_rope) == "TEXT"
    assert g_popcashout(cfig, blrheal, jk, wx.plan_rope) == False

    assert g_class_type(cfig, blrprem, jk, wx.reason_context) == wx.RopeTerm
    assert g_sqlitetype(cfig, blrprem, jk, wx.reason_context) == "TEXT"
    assert g_popcashout(cfig, blrprem, jk, wx.reason_context) == False

    assert g_class_type(cfig, blrprem, jk, wx.reason_state) == wx.RopeTerm
    assert g_sqlitetype(cfig, blrprem, jk, wx.reason_state) == "TEXT"
    assert g_popcashout(cfig, blrprem, jk, wx.reason_state) == False

    assert g_class_type(cfig, blrprem, jk, wx.plan_rope) == wx.RopeTerm
    assert g_sqlitetype(cfig, blrprem, jk, wx.plan_rope) == "TEXT"
    assert g_popcashout(cfig, blrprem, jk, wx.plan_rope) == False

    assert g_class_type(cfig, blrprem, jv, wx.status) == "int"
    assert g_sqlitetype(cfig, blrprem, jv, wx.status) == "INTEGER"
    assert g_popcashout(cfig, blrprem, jv, wx.status) == True

    assert g_class_type(cfig, blrprem, jv, wx.task) == "int"
    assert g_sqlitetype(cfig, blrprem, jv, wx.task) == "INTEGER"
    assert g_popcashout(cfig, blrprem, jv, wx.task) == True

    assert g_class_type(cfig, blrprem, jv, wx.reason_divisor) == "int"
    assert g_sqlitetype(cfig, blrprem, jv, wx.reason_divisor) == "INTEGER"
    assert g_popcashout(cfig, blrprem, jv, wx.reason_divisor) == False

    assert g_class_type(cfig, blrprem, jv, wx.reason_upper) == "float"
    assert g_sqlitetype(cfig, blrprem, jv, wx.reason_upper) == "REAL"
    assert g_popcashout(cfig, blrprem, jv, wx.reason_upper) == False

    assert g_class_type(cfig, blrprem, jv, wx.reason_lower) == "float"
    assert g_sqlitetype(cfig, blrprem, jv, wx.reason_lower) == "REAL"
    assert g_popcashout(cfig, blrprem, jv, wx.reason_lower) == False

    assert g_class_type(cfig, blrreas, jk, wx.reason_context) == wx.RopeTerm
    assert g_sqlitetype(cfig, blrreas, jk, wx.reason_context) == "TEXT"
    assert g_popcashout(cfig, blrreas, jk, wx.reason_context) == False

    assert g_class_type(cfig, blrreas, jk, wx.plan_rope) == wx.RopeTerm
    assert g_sqlitetype(cfig, blrreas, jk, wx.plan_rope) == "TEXT"
    assert g_popcashout(cfig, blrreas, jk, wx.plan_rope) == False

    assert g_class_type(cfig, blrreas, jv, "_reason_active_heir") == "int"
    assert g_sqlitetype(cfig, blrreas, jv, "_reason_active_heir") == "INTEGER"
    assert g_popcashout(cfig, blrreas, jv, "_reason_active_heir") == True

    assert g_class_type(cfig, blrreas, jv, wx.status) == "int"
    assert g_sqlitetype(cfig, blrreas, jv, wx.status) == "INTEGER"
    assert g_popcashout(cfig, blrreas, jv, wx.status) == True

    assert g_class_type(cfig, blrreas, jv, wx.task) == "int"
    assert g_sqlitetype(cfig, blrreas, jv, wx.task) == "INTEGER"
    assert g_popcashout(cfig, blrreas, jv, wx.task) == True

    assert g_class_type(cfig, blrreas, jv, wx.reason_active_requisite) == "bool"
    assert g_sqlitetype(cfig, blrreas, jv, wx.reason_active_requisite) == "INTEGER"
    assert g_popcashout(cfig, blrreas, jv, wx.reason_active_requisite) == False

    assert g_class_type(cfig, blrlabo, jk, wx.plan_rope) == wx.RopeTerm
    assert g_sqlitetype(cfig, blrlabo, jk, wx.plan_rope) == "TEXT"
    assert g_popcashout(cfig, blrlabo, jk, wx.plan_rope) == False

    assert g_class_type(cfig, blrlabo, jk, wx.party_title) == wx.TitleTerm
    assert g_sqlitetype(cfig, blrlabo, jk, wx.party_title) == "TEXT"
    assert g_popcashout(cfig, blrlabo, jk, wx.party_title) == False

    assert g_class_type(cfig, blrlabo, jv, "_belief_name_is_labor") == "int"
    assert g_sqlitetype(cfig, blrlabo, jv, "_belief_name_is_labor") == "INTEGER"
    assert g_popcashout(cfig, blrlabo, jv, "_belief_name_is_labor") == True

    assert g_class_type(cfig, blrplan, jv, "active") == "int"
    assert g_sqlitetype(cfig, blrplan, jv, "active") == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, "active") == True

    assert g_class_type(cfig, blrplan, jv, wx.all_voice_cred) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, wx.all_voice_cred) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, wx.all_voice_cred) == True

    assert g_class_type(cfig, blrplan, jv, wx.all_voice_debt) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, wx.all_voice_debt) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, wx.all_voice_debt) == True

    assert g_class_type(cfig, blrplan, jv, wx.descendant_pledge_count) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, wx.descendant_pledge_count) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, wx.descendant_pledge_count) == True

    assert g_class_type(cfig, blrplan, jv, wx.fund_cease) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, wx.fund_cease) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, wx.fund_cease) == True

    assert g_class_type(cfig, blrplan, jv, wx.fund_grain) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, wx.fund_grain) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, wx.fund_grain) == True

    assert g_class_type(cfig, blrplan, jv, wx.fund_onset) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, wx.fund_onset) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, wx.fund_onset) == True

    assert g_class_type(cfig, blrplan, jv, wx.fund_ratio) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, wx.fund_ratio) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, wx.fund_ratio) == True

    assert g_class_type(cfig, blrplan, jv, wx.gogo_calc) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, wx.gogo_calc) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, wx.gogo_calc) == True

    assert g_class_type(cfig, blrplan, jv, wx.healerunit_ratio) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, wx.healerunit_ratio) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, wx.healerunit_ratio) == True

    assert g_class_type(cfig, blrplan, jv, wx.tree_level) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, wx.tree_level) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, wx.tree_level) == True

    assert g_class_type(cfig, blrplan, jv, wx.range_evaluated) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, wx.range_evaluated) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, wx.range_evaluated) == True

    assert g_class_type(cfig, blrplan, jv, wx.stop_calc) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, wx.stop_calc) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, wx.stop_calc) == True

    assert g_class_type(cfig, blrplan, jv, wx.task) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, wx.task) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, wx.task) == True

    assert g_class_type(cfig, blrplan, jv, wx.addin) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, wx.addin) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, wx.addin) == False

    assert g_class_type(cfig, blrplan, jv, wx.begin) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, wx.begin) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, wx.begin) == False

    assert g_class_type(cfig, blrplan, jv, wx.close) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, wx.close) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, wx.close) == False

    assert g_class_type(cfig, blrplan, jv, wx.denom) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, wx.denom) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, wx.denom) == False

    assert g_class_type(cfig, blrplan, jv, wx.gogo_want) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, wx.gogo_want) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, wx.gogo_want) == False

    assert g_class_type(cfig, blrplan, jv, wx.star) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, wx.star) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, wx.star) == False

    assert g_class_type(cfig, blrplan, jv, wx.morph) == "bool"
    assert g_sqlitetype(cfig, blrplan, jv, wx.morph) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, wx.morph) == False

    assert g_class_type(cfig, blrplan, jv, wx.numor) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, wx.numor) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, wx.numor) == False

    assert g_class_type(cfig, blrplan, jv, wx.pledge) == "bool"
    assert g_sqlitetype(cfig, blrplan, jv, wx.pledge) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, wx.pledge) == False

    assert g_class_type(cfig, blrplan, jv, wx.problem_bool) == "bool"
    assert g_sqlitetype(cfig, blrplan, jv, wx.problem_bool) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, wx.problem_bool) == False

    assert g_class_type(cfig, blrplan, jv, wx.stop_want) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, wx.stop_want) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, wx.stop_want) == False

    assert g_class_type(cfig, blfunit, jv, "keeps_buildable") == "int"
    assert g_sqlitetype(cfig, blfunit, jv, "keeps_buildable") == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, "keeps_buildable") == True

    assert g_class_type(cfig, blfunit, jv, "keeps_justified") == "int"
    assert g_sqlitetype(cfig, blfunit, jv, "keeps_justified") == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, "keeps_justified") == True

    assert g_class_type(cfig, blfunit, jv, wx.offtrack_fund) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, wx.offtrack_fund) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, wx.offtrack_fund) == True

    assert g_class_type(cfig, blfunit, jv, wx.rational) == "bool"
    assert g_sqlitetype(cfig, blfunit, jv, wx.rational) == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, wx.rational) == True

    assert g_class_type(cfig, blfunit, jv, wx.sum_healerunit_share) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, wx.sum_healerunit_share) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, wx.sum_healerunit_share) == True

    assert g_class_type(cfig, blfunit, jv, wx.tree_traverse_count) == "int"
    assert g_sqlitetype(cfig, blfunit, jv, wx.tree_traverse_count) == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, wx.tree_traverse_count) == True

    assert g_class_type(cfig, blfunit, jv, wx.credor_respect) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, wx.credor_respect) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, wx.credor_respect) == False

    assert g_class_type(cfig, blfunit, jv, wx.debtor_respect) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, wx.debtor_respect) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, wx.debtor_respect) == False

    assert g_class_type(cfig, blfunit, jv, wx.fund_grain) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, wx.fund_grain) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, wx.fund_grain) == False

    assert g_class_type(cfig, blfunit, jv, wx.fund_pool) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, wx.fund_pool) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, wx.fund_pool) == False

    assert g_class_type(cfig, blfunit, jv, wx.max_tree_traverse) == "int"
    assert g_sqlitetype(cfig, blfunit, jv, wx.max_tree_traverse) == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, wx.max_tree_traverse) == False

    assert g_class_type(cfig, blfunit, jv, wx.money_grain) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, wx.money_grain) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, wx.money_grain) == False

    assert g_class_type(cfig, blfunit, jv, wx.respect_grain) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, wx.respect_grain) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, wx.respect_grain) == False

    assert g_class_type(cfig, blfunit, jv, wx.tally) == "int"
    assert g_sqlitetype(cfig, blfunit, jv, wx.tally) == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, wx.tally) == False


def test_get_belief_config_dict_ReturnsObj_EachArgHasOneClassType():
    # ESTABLISH
    belief_config_dict = get_belief_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for belief_calc_dimen, dimen_dict in belief_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues"}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(wx.class_type)
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN / THEN
    for x_arg, arg_types in all_args.items():
        print(f"{x_arg=} {arg_types=}")
        assert len(arg_types) == 1


def test_get_belief_config_dict_ReturnsObj_EachArgHasOne_sqlite_datatype():
    # ESTABLISH
    belief_config_dict = get_belief_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for belief_calc_dimen, dimen_dict in belief_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues"}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(wx.sqlite_datatype)
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    for x_arg, arg_types in all_args.items():
        print(f"{x_arg=} {arg_types=}")
        assert len(arg_types) == 1

    # WHEN
    sqlite_datatype_dict = get_belief_calc_args_sqlite_datatype_dict()

    # THEN
    for x_arg, arg_types in all_args.items():
        # print(
        #     f"""assert belief_calc_args_type_dict.get("{x_arg}") == "{list(arg_types)[0]}" """
        # )
        print(f""""{x_arg}": "{list(arg_types)[0]}",""")
        assert list(arg_types)[0] == sqlite_datatype_dict.get(x_arg)


def test_get_belief_calc_args_type_dict_ReturnsObj():
    # ESTABLISH
    belief_config_dict = get_belief_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for belief_calc_dimen, dimen_dict in belief_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues"}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(wx.class_type)
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN
    belief_calc_args_type_dict = get_belief_calc_args_type_dict()

    # THEN
    assert belief_calc_args_type_dict.get(wx.voice_name) == wx.NameTerm
    assert belief_calc_args_type_dict.get(wx.group_title) == wx.TitleTerm
    assert belief_calc_args_type_dict.get(wx.credor_pool) == "float"
    assert belief_calc_args_type_dict.get(wx.debtor_pool) == "float"
    assert belief_calc_args_type_dict.get(wx.fund_agenda_give) == "float"
    assert belief_calc_args_type_dict.get(wx.fund_agenda_ratio_give) == "float"
    assert belief_calc_args_type_dict.get(wx.fund_agenda_ratio_take) == "float"
    assert belief_calc_args_type_dict.get(wx.fund_agenda_take) == "float"
    assert belief_calc_args_type_dict.get(wx.fund_give) == "float"
    assert belief_calc_args_type_dict.get(wx.fund_take) == "float"
    assert belief_calc_args_type_dict.get(wx.group_cred_points) == "int"
    assert belief_calc_args_type_dict.get(wx.group_debt_points) == "int"
    assert belief_calc_args_type_dict.get(wx.inallocable_voice_debt_points) == "float"
    assert belief_calc_args_type_dict.get(wx.irrational_voice_debt_points) == "float"
    assert belief_calc_args_type_dict.get(wx.voice_cred_points) == "float"
    assert belief_calc_args_type_dict.get(wx.voice_debt_points) == "float"
    assert belief_calc_args_type_dict.get(wx.addin) == "float"
    assert belief_calc_args_type_dict.get(wx.begin) == "float"
    assert belief_calc_args_type_dict.get(wx.close) == "float"
    assert belief_calc_args_type_dict.get(wx.denom) == "int"
    assert belief_calc_args_type_dict.get(wx.gogo_want) == "float"
    assert belief_calc_args_type_dict.get(wx.star) == "int"
    assert belief_calc_args_type_dict.get(wx.morph) == "bool"
    assert belief_calc_args_type_dict.get(wx.numor) == "int"
    assert belief_calc_args_type_dict.get(wx.pledge) == "bool"
    assert belief_calc_args_type_dict.get(wx.problem_bool) == "bool"
    assert belief_calc_args_type_dict.get(wx.stop_want) == "float"
    assert belief_calc_args_type_dict.get(wx.awardee_title) == wx.TitleTerm
    assert belief_calc_args_type_dict.get(wx.plan_rope) == wx.RopeTerm
    assert belief_calc_args_type_dict.get(wx.give_force) == "float"
    assert belief_calc_args_type_dict.get(wx.take_force) == "float"
    assert belief_calc_args_type_dict.get(wx.reason_context) == wx.RopeTerm
    assert belief_calc_args_type_dict.get(wx.fact_upper) == "float"
    assert belief_calc_args_type_dict.get(wx.fact_lower) == "float"
    assert belief_calc_args_type_dict.get(wx.fact_state) == wx.RopeTerm
    assert belief_calc_args_type_dict.get(wx.healer_name) == wx.NameTerm
    assert belief_calc_args_type_dict.get(wx.reason_state) == wx.RopeTerm
    assert belief_calc_args_type_dict.get(wx.status) == "int"
    assert belief_calc_args_type_dict.get(wx.task) == "int"
    assert belief_calc_args_type_dict.get(wx.reason_divisor) == "int"
    assert belief_calc_args_type_dict.get(wx.reason_upper) == "float"
    assert belief_calc_args_type_dict.get(wx.reason_lower) == "float"
    assert belief_calc_args_type_dict.get("_reason_active_heir") == "int"
    assert belief_calc_args_type_dict.get(wx.reason_active_requisite) == "bool"
    assert belief_calc_args_type_dict.get(wx.party_title) == wx.TitleTerm
    assert belief_calc_args_type_dict.get("_belief_name_is_labor") == "int"
    assert belief_calc_args_type_dict.get(wx.active) == "int"
    assert belief_calc_args_type_dict.get(wx.all_voice_cred) == "int"
    assert belief_calc_args_type_dict.get(wx.all_voice_debt) == "int"
    assert belief_calc_args_type_dict.get(wx.descendant_pledge_count) == "int"
    assert belief_calc_args_type_dict.get(wx.fund_cease) == "float"
    assert belief_calc_args_type_dict.get(wx.fund_onset) == "float"
    assert belief_calc_args_type_dict.get(wx.fund_ratio) == "float"
    assert belief_calc_args_type_dict.get(wx.gogo_calc) == "float"
    assert belief_calc_args_type_dict.get("healerunit_ratio") == "float"
    assert belief_calc_args_type_dict.get(wx.tree_level) == "int"
    assert belief_calc_args_type_dict.get(wx.range_evaluated) == "int"
    assert belief_calc_args_type_dict.get(wx.stop_calc) == "float"
    assert belief_calc_args_type_dict.get(wx.keeps_buildable) == "int"
    assert belief_calc_args_type_dict.get(wx.keeps_justified) == "int"
    assert belief_calc_args_type_dict.get(wx.offtrack_fund) == "int"
    assert belief_calc_args_type_dict.get(wx.rational) == "bool"
    assert belief_calc_args_type_dict.get(wx.sum_healerunit_share) == "float"
    assert belief_calc_args_type_dict.get(wx.tree_traverse_count) == "int"
    assert belief_calc_args_type_dict.get(wx.credor_respect) == "float"
    assert belief_calc_args_type_dict.get(wx.debtor_respect) == "float"
    assert belief_calc_args_type_dict.get(wx.fund_grain) == "float"
    assert belief_calc_args_type_dict.get(wx.fund_pool) == "float"
    assert belief_calc_args_type_dict.get(wx.max_tree_traverse) == "int"
    assert belief_calc_args_type_dict.get(wx.money_grain) == "float"
    assert belief_calc_args_type_dict.get(wx.respect_grain) == "float"
    assert belief_calc_args_type_dict.get(wx.tally) == "int"
    assert len(belief_calc_args_type_dict) == 72
