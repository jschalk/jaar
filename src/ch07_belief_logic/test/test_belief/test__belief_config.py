# from src.ch01_data_toolbox.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd
from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch07_belief_logic._ref.ch07_keywords import (
    LabelTerm_str,
    NameTerm_str,
    RopePointer_str,
    TitleTerm_str,
    active_str,
    addin_str,
    all_voice_cred_str,
    all_voice_debt_str,
    awardee_title_str,
    begin_str,
    belief_groupunit_str,
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
    chore_str,
    class_type_str,
    close_str,
    credor_pool_str,
    credor_respect_str,
    debtor_pool_str,
    debtor_respect_str,
    denom_str,
    descendant_task_count_str,
    fact_context_str,
    fact_lower_str,
    fact_state_str,
    fact_upper_str,
    fund_agenda_give_str,
    fund_agenda_ratio_give_str,
    fund_agenda_ratio_take_str,
    fund_agenda_take_str,
    fund_cease_str,
    fund_give_str,
    fund_iota_str,
    fund_onset_str,
    fund_pool_str,
    fund_ratio_str,
    fund_take_str,
    give_force_str,
    gogo_calc_str,
    gogo_want_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    healer_name_str,
    healerunit_ratio_str,
    inallocable_voice_debt_points_str,
    irrational_voice_debt_points_str,
    jkeys_str,
    jvalues_str,
    keeps_buildable_str,
    keeps_justified_str,
    knot_str,
    max_tree_traverse_str,
    moment_label_str,
    morph_str,
    numor_str,
    offtrack_fund_str,
    party_title_str,
    penny_str,
    plan_rope_str,
    problem_bool_str,
    range_evaluated_str,
    rational_str,
    reason_active_requisite_str,
    reason_context_str,
    reason_divisor_str,
    reason_lower_str,
    reason_state_str,
    reason_upper_str,
    respect_bit_str,
    sqlite_datatype_str,
    star_str,
    status_str,
    stop_calc_str,
    stop_want_str,
    sum_healerunit_share_str,
    take_force_str,
    tally_str,
    task_str,
    tree_level_str,
    tree_traverse_count_str,
    voice_cred_points_str,
    voice_debt_points_str,
    voice_name_str,
)
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
    assert beliefunit_str() in belief_config_keys
    assert belief_voiceunit_str() in belief_config_keys
    assert belief_voice_membership_str() in belief_config_keys
    assert belief_planunit_str() in belief_config_keys
    assert belief_plan_awardunit_str() in belief_config_keys
    assert belief_plan_reasonunit_str() in belief_config_keys
    assert belief_plan_reason_caseunit_str() in belief_config_keys
    assert belief_plan_partyunit_str() in belief_config_keys
    assert belief_plan_healerunit_str() in belief_config_keys
    assert belief_plan_factunit_str() in belief_config_keys
    assert belief_groupunit_str() in belief_config_keys
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
        assert jkeys_str() in attribute_keys
        assert jvalues_str() in attribute_keys
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
    blrunit_attribute = belief_config.get(beliefunit_str())
    blrpern_attribute = belief_config.get(belief_voiceunit_str())
    blrmemb_attribute = belief_config.get(belief_voice_membership_str())
    blrplan_attribute = belief_config.get(belief_planunit_str())
    blrawar_attribute = belief_config.get(belief_plan_awardunit_str())
    blrreas_attribute = belief_config.get(belief_plan_reasonunit_str())
    blrprem_attribute = belief_config.get(belief_plan_reason_caseunit_str())
    blrlabo_attribute = belief_config.get(belief_plan_partyunit_str())
    blrheal_attribute = belief_config.get(belief_plan_healerunit_str())
    blrfact_attribute = belief_config.get(belief_plan_factunit_str())
    blrgrou_attribute = belief_config.get(belief_groupunit_str())
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
    assert stop_want_str() in all_belief_calc_args
    assert plan_rope_str() in all_belief_calc_args
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
            if level2_key in {jkeys_str(), jvalues_str()}:
                for level3_key, attr_dict in fm_attribute_dict.items():
                    print(
                        f"{level1_key=} {level2_key=} {level3_key=} {set(attr_dict.keys())=}"
                    )
                    assert set(attr_dict.keys()) == {
                        class_type_str(),
                        sqlite_datatype_str(),
                        "populate_by_cashout",
                    }


def test_get_belief_calc_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    belief_calc_dimens = get_belief_calc_dimens()

    # THEN
    expected_belief_calc_dimens = {
        beliefunit_str(),
        belief_voiceunit_str(),
        belief_voice_membership_str(),
        belief_planunit_str(),
        belief_plan_awardunit_str(),
        belief_plan_reasonunit_str(),
        belief_plan_reason_caseunit_str(),
        belief_plan_partyunit_str(),
        belief_plan_healerunit_str(),
        belief_plan_factunit_str(),
        belief_groupunit_str(),
    }
    assert belief_calc_dimens == expected_belief_calc_dimens
    assert belief_calc_dimens == set(get_belief_config_dict().keys())


def test_get_belief_calc_dimen_args_ReturnsObj():
    # ESTABLISH / WHEN
    belief_voiceunit_args = get_belief_calc_dimen_args(belief_voiceunit_str())
    belief_planunit_args = get_belief_calc_dimen_args(belief_planunit_str())
    belief_groupunit_args = get_belief_calc_dimen_args(belief_groupunit_str())

    #  THEN
    print(f"{belief_voiceunit_args=}")
    print(f"{belief_groupunit_args=}")
    assert belief_voiceunit_args == {
        moment_label_str(),
        belief_name_str(),
        fund_agenda_give_str(),
        credor_pool_str(),
        fund_give_str(),
        voice_cred_points_str(),
        voice_name_str(),
        voice_debt_points_str(),
        fund_agenda_ratio_take_str(),
        inallocable_voice_debt_points_str(),
        fund_agenda_ratio_give_str(),
        fund_agenda_take_str(),
        fund_take_str(),
        debtor_pool_str(),
        irrational_voice_debt_points_str(),
    }
    assert belief_planunit_args == {
        moment_label_str(),
        belief_name_str(),
        morph_str(),
        denom_str(),
        task_str(),
        close_str(),
        addin_str(),
        numor_str(),
        star_str(),
        stop_want_str(),
        gogo_calc_str(),
        stop_calc_str(),
        active_str(),
        fund_onset_str(),
        fund_cease_str(),
        descendant_task_count_str(),
        all_voice_cred_str(),
        all_voice_debt_str(),
        healerunit_ratio_str(),
        tree_level_str(),
        chore_str(),
        fund_iota_str(),
        fund_ratio_str(),
        range_evaluated_str(),
        problem_bool_str(),
        gogo_want_str(),
        plan_rope_str(),
        begin_str(),
    }
    assert belief_groupunit_args == {
        moment_label_str(),
        belief_name_str(),
        debtor_pool_str(),
        credor_pool_str(),
        fund_give_str(),
        group_title_str(),
        knot_str(),
        fund_agenda_give_str(),
        fund_agenda_take_str(),
        fund_take_str(),
        fund_iota_str(),
    }


def g_class_type(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get(class_type_str())


def g_sqlitetype(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get(sqlite_datatype_str())


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
    #         if level2_key in {jkeys_str(), jvalues_str()}:
    #             for level3_key, attr_dict in fm_attribute_dict.items():
    #                 dimem = attribute_dict.get("abbreviation")
    #                 x_class_type = attr_dict.get(class_type_str())
    #                 x_sqlite_datatype = attr_dict.get(sqlite_datatype_str())
    #                 print(
    #                     f"""    assert g_class_type(config, {dimem}, {level2_key[0:2]}, "{level3_key}") == "{x_class_type}" """
    #                 )
    #                 print(
    #                     f"""    assert g_sqlitetype(config, {dimem}, {level2_key[0:2]}, "{level3_key}") == "{x_sqlite_datatype}" """
    #                 )

    jk = "jkeys"
    jv = "jvalues"
    blfunit = beliefunit_str()
    blrpern = belief_voiceunit_str()
    blrmemb = belief_voice_membership_str()
    blrplan = belief_planunit_str()
    blrawar = belief_plan_awardunit_str()
    blrreas = belief_plan_reasonunit_str()
    blrprem = belief_plan_reason_caseunit_str()
    blrlabo = belief_plan_partyunit_str()
    blrheal = belief_plan_healerunit_str()
    blrfact = belief_plan_factunit_str()
    blrgrou = belief_groupunit_str()
    assert g_class_type(cfig, blrmemb, jk, voice_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, blrmemb, jk, voice_name_str()) == "TEXT"
    assert g_popcashout(cfig, blrmemb, jk, voice_name_str()) == False

    assert g_class_type(cfig, blrmemb, jk, group_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, blrmemb, jk, group_title_str()) == "TEXT"
    assert g_popcashout(cfig, blrmemb, jk, group_title_str()) == False

    assert g_class_type(cfig, blrmemb, jv, credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, credor_pool_str()) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, credor_pool_str()) == True

    assert g_class_type(cfig, blrmemb, jv, debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, debtor_pool_str()) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, debtor_pool_str()) == True

    assert g_class_type(cfig, blrmemb, jv, fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, fund_agenda_give_str()) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, fund_agenda_give_str()) == True

    assert g_class_type(cfig, blrmemb, jv, fund_agenda_ratio_give_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, fund_agenda_ratio_give_str()) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, fund_agenda_ratio_give_str()) == True

    assert g_class_type(cfig, blrmemb, jv, fund_agenda_ratio_take_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, fund_agenda_ratio_take_str()) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, fund_agenda_ratio_take_str()) == True

    assert g_class_type(cfig, blrmemb, jv, fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, fund_agenda_take_str()) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, fund_agenda_take_str()) == True

    assert g_class_type(cfig, blrmemb, jv, fund_give_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, fund_give_str()) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, fund_give_str()) == True

    assert g_class_type(cfig, blrmemb, jv, fund_take_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, fund_take_str()) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, fund_take_str()) == True

    assert g_class_type(cfig, blrmemb, jv, group_cred_points_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, group_cred_points_str()) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, group_cred_points_str()) == False

    assert g_class_type(cfig, blrmemb, jv, group_debt_points_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, group_debt_points_str()) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, group_debt_points_str()) == False

    assert g_class_type(cfig, blrpern, jk, voice_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, blrpern, jk, voice_name_str()) == "TEXT"
    assert g_popcashout(cfig, blrpern, jk, voice_name_str()) == False

    assert g_class_type(cfig, blrpern, jv, credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, credor_pool_str()) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, credor_pool_str()) == True

    assert g_class_type(cfig, blrpern, jv, debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, debtor_pool_str()) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, debtor_pool_str()) == True

    assert g_class_type(cfig, blrpern, jv, fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, fund_agenda_give_str()) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, fund_agenda_give_str()) == True

    assert g_class_type(cfig, blrpern, jv, fund_agenda_ratio_give_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, fund_agenda_ratio_give_str()) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, fund_agenda_ratio_give_str()) == True

    assert g_class_type(cfig, blrpern, jv, fund_agenda_ratio_take_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, fund_agenda_ratio_take_str()) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, fund_agenda_ratio_take_str()) == True

    assert g_class_type(cfig, blrpern, jv, fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, fund_agenda_take_str()) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, fund_agenda_take_str()) == True

    assert g_class_type(cfig, blrpern, jv, fund_give_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, fund_give_str()) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, fund_give_str()) == True

    assert g_class_type(cfig, blrpern, jv, fund_take_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, fund_take_str()) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, fund_take_str()) == True

    assert (
        g_class_type(cfig, blrpern, jv, inallocable_voice_debt_points_str()) == "float"
    )
    assert (
        g_sqlitetype(cfig, blrpern, jv, inallocable_voice_debt_points_str()) == "REAL"
    )
    assert g_popcashout(cfig, blrpern, jv, inallocable_voice_debt_points_str()) == True

    assert (
        g_class_type(cfig, blrpern, jv, irrational_voice_debt_points_str()) == "float"
    )
    assert g_sqlitetype(cfig, blrpern, jv, irrational_voice_debt_points_str()) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, irrational_voice_debt_points_str()) == True

    assert g_class_type(cfig, blrpern, jv, voice_cred_points_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, voice_cred_points_str()) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, voice_cred_points_str()) == False

    assert g_class_type(cfig, blrpern, jv, voice_debt_points_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, voice_debt_points_str()) == "REAL"
    assert g_popcashout(cfig, blrpern, jv, voice_debt_points_str()) == False

    assert g_class_type(cfig, blrgrou, jk, group_title_str()) == "TitleTerm"
    assert g_sqlitetype(cfig, blrgrou, jk, group_title_str()) == "TEXT"
    assert g_popcashout(cfig, blrgrou, jk, group_title_str()) == True

    assert g_class_type(cfig, blrgrou, jv, knot_str()) == "str"
    assert g_sqlitetype(cfig, blrgrou, jv, knot_str()) == "TEXT"
    assert g_popcashout(cfig, blrgrou, jv, knot_str()) == True

    assert g_class_type(cfig, blrgrou, jv, debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, debtor_pool_str()) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, debtor_pool_str()) == True

    assert g_class_type(cfig, blrgrou, jv, credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, credor_pool_str()) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, credor_pool_str()) == True

    assert g_class_type(cfig, blrgrou, jv, fund_give_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, fund_give_str()) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, fund_give_str()) == True

    assert g_class_type(cfig, blrgrou, jv, fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, fund_agenda_give_str()) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, fund_agenda_give_str()) == True

    assert g_class_type(cfig, blrgrou, jv, fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, fund_agenda_take_str()) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, fund_agenda_take_str()) == True

    assert g_class_type(cfig, blrgrou, jv, fund_take_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, fund_take_str()) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, fund_take_str()) == True

    assert g_class_type(cfig, blrgrou, jv, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, fund_iota_str()) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, fund_iota_str()) == True

    assert g_class_type(cfig, blrawar, jk, awardee_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, blrawar, jk, awardee_title_str()) == "TEXT"
    assert g_popcashout(cfig, blrawar, jk, awardee_title_str()) == False

    assert g_class_type(cfig, blrawar, jk, plan_rope_str()) == RopePointer_str()
    assert g_sqlitetype(cfig, blrawar, jk, plan_rope_str()) == "TEXT"
    assert g_popcashout(cfig, blrawar, jk, plan_rope_str()) == False

    assert g_class_type(cfig, blrawar, jv, fund_give_str()) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, fund_give_str()) == "REAL"
    assert g_popcashout(cfig, blrawar, jv, fund_give_str()) == True

    assert g_class_type(cfig, blrawar, jv, fund_take_str()) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, fund_take_str()) == "REAL"
    assert g_popcashout(cfig, blrawar, jv, fund_take_str()) == True

    assert g_class_type(cfig, blrawar, jv, give_force_str()) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, give_force_str()) == "REAL"
    assert g_popcashout(cfig, blrawar, jv, give_force_str()) == False

    assert g_class_type(cfig, blrawar, jv, take_force_str()) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, take_force_str()) == "REAL"
    assert g_popcashout(cfig, blrawar, jv, take_force_str()) == False

    assert g_class_type(cfig, blrfact, jk, fact_context_str()) == RopePointer_str()
    assert g_sqlitetype(cfig, blrfact, jk, fact_context_str()) == "TEXT"
    assert g_popcashout(cfig, blrfact, jk, fact_context_str()) == False

    assert g_class_type(cfig, blrfact, jk, plan_rope_str()) == RopePointer_str()
    assert g_sqlitetype(cfig, blrfact, jk, plan_rope_str()) == "TEXT"
    assert g_popcashout(cfig, blrfact, jk, plan_rope_str()) == False

    assert g_class_type(cfig, blrfact, jv, fact_upper_str()) == "float"
    assert g_sqlitetype(cfig, blrfact, jv, fact_upper_str()) == "REAL"
    assert g_popcashout(cfig, blrfact, jv, fact_upper_str()) == False

    assert g_class_type(cfig, blrfact, jv, fact_lower_str()) == "float"
    assert g_sqlitetype(cfig, blrfact, jv, fact_lower_str()) == "REAL"
    assert g_popcashout(cfig, blrfact, jv, fact_lower_str()) == False

    assert g_class_type(cfig, blrfact, jv, fact_state_str()) == RopePointer_str()
    assert g_sqlitetype(cfig, blrfact, jv, fact_state_str()) == "TEXT"
    assert g_popcashout(cfig, blrfact, jv, fact_state_str()) == False

    assert g_class_type(cfig, blrheal, jk, healer_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, blrheal, jk, healer_name_str()) == "TEXT"
    assert g_popcashout(cfig, blrheal, jk, healer_name_str()) == False

    assert g_class_type(cfig, blrheal, jk, plan_rope_str()) == RopePointer_str()
    assert g_sqlitetype(cfig, blrheal, jk, plan_rope_str()) == "TEXT"
    assert g_popcashout(cfig, blrheal, jk, plan_rope_str()) == False

    assert g_class_type(cfig, blrprem, jk, reason_context_str()) == RopePointer_str()
    assert g_sqlitetype(cfig, blrprem, jk, reason_context_str()) == "TEXT"
    assert g_popcashout(cfig, blrprem, jk, reason_context_str()) == False

    assert g_class_type(cfig, blrprem, jk, reason_state_str()) == RopePointer_str()
    assert g_sqlitetype(cfig, blrprem, jk, reason_state_str()) == "TEXT"
    assert g_popcashout(cfig, blrprem, jk, reason_state_str()) == False

    assert g_class_type(cfig, blrprem, jk, plan_rope_str()) == RopePointer_str()
    assert g_sqlitetype(cfig, blrprem, jk, plan_rope_str()) == "TEXT"
    assert g_popcashout(cfig, blrprem, jk, plan_rope_str()) == False

    assert g_class_type(cfig, blrprem, jv, status_str()) == "int"
    assert g_sqlitetype(cfig, blrprem, jv, status_str()) == "INTEGER"
    assert g_popcashout(cfig, blrprem, jv, status_str()) == True

    assert g_class_type(cfig, blrprem, jv, chore_str()) == "int"
    assert g_sqlitetype(cfig, blrprem, jv, chore_str()) == "INTEGER"
    assert g_popcashout(cfig, blrprem, jv, chore_str()) == True

    assert g_class_type(cfig, blrprem, jv, reason_divisor_str()) == "int"
    assert g_sqlitetype(cfig, blrprem, jv, reason_divisor_str()) == "INTEGER"
    assert g_popcashout(cfig, blrprem, jv, reason_divisor_str()) == False

    assert g_class_type(cfig, blrprem, jv, reason_upper_str()) == "float"
    assert g_sqlitetype(cfig, blrprem, jv, reason_upper_str()) == "REAL"
    assert g_popcashout(cfig, blrprem, jv, reason_upper_str()) == False

    assert g_class_type(cfig, blrprem, jv, reason_lower_str()) == "float"
    assert g_sqlitetype(cfig, blrprem, jv, reason_lower_str()) == "REAL"
    assert g_popcashout(cfig, blrprem, jv, reason_lower_str()) == False

    assert g_class_type(cfig, blrreas, jk, reason_context_str()) == RopePointer_str()
    assert g_sqlitetype(cfig, blrreas, jk, reason_context_str()) == "TEXT"
    assert g_popcashout(cfig, blrreas, jk, reason_context_str()) == False

    assert g_class_type(cfig, blrreas, jk, plan_rope_str()) == RopePointer_str()
    assert g_sqlitetype(cfig, blrreas, jk, plan_rope_str()) == "TEXT"
    assert g_popcashout(cfig, blrreas, jk, plan_rope_str()) == False

    assert g_class_type(cfig, blrreas, jv, "_reason_active_heir") == "int"
    assert g_sqlitetype(cfig, blrreas, jv, "_reason_active_heir") == "INTEGER"
    assert g_popcashout(cfig, blrreas, jv, "_reason_active_heir") == True

    assert g_class_type(cfig, blrreas, jv, status_str()) == "int"
    assert g_sqlitetype(cfig, blrreas, jv, status_str()) == "INTEGER"
    assert g_popcashout(cfig, blrreas, jv, status_str()) == True

    assert g_class_type(cfig, blrreas, jv, chore_str()) == "int"
    assert g_sqlitetype(cfig, blrreas, jv, chore_str()) == "INTEGER"
    assert g_popcashout(cfig, blrreas, jv, chore_str()) == True

    assert g_class_type(cfig, blrreas, jv, reason_active_requisite_str()) == "bool"
    assert g_sqlitetype(cfig, blrreas, jv, reason_active_requisite_str()) == "INTEGER"
    assert g_popcashout(cfig, blrreas, jv, reason_active_requisite_str()) == False

    assert g_class_type(cfig, blrlabo, jk, plan_rope_str()) == RopePointer_str()
    assert g_sqlitetype(cfig, blrlabo, jk, plan_rope_str()) == "TEXT"
    assert g_popcashout(cfig, blrlabo, jk, plan_rope_str()) == False

    assert g_class_type(cfig, blrlabo, jk, party_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, blrlabo, jk, party_title_str()) == "TEXT"
    assert g_popcashout(cfig, blrlabo, jk, party_title_str()) == False

    assert g_class_type(cfig, blrlabo, jv, "_belief_name_is_labor") == "int"
    assert g_sqlitetype(cfig, blrlabo, jv, "_belief_name_is_labor") == "INTEGER"
    assert g_popcashout(cfig, blrlabo, jv, "_belief_name_is_labor") == True

    assert g_class_type(cfig, blrplan, jv, "active") == "int"
    assert g_sqlitetype(cfig, blrplan, jv, "active") == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, "active") == True

    assert g_class_type(cfig, blrplan, jv, all_voice_cred_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, all_voice_cred_str()) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, all_voice_cred_str()) == True

    assert g_class_type(cfig, blrplan, jv, all_voice_debt_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, all_voice_debt_str()) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, all_voice_debt_str()) == True

    assert g_class_type(cfig, blrplan, jv, descendant_task_count_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, descendant_task_count_str()) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, descendant_task_count_str()) == True

    assert g_class_type(cfig, blrplan, jv, fund_cease_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, fund_cease_str()) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, fund_cease_str()) == True

    assert g_class_type(cfig, blrplan, jv, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, fund_iota_str()) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, fund_iota_str()) == True

    assert g_class_type(cfig, blrplan, jv, fund_onset_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, fund_onset_str()) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, fund_onset_str()) == True

    assert g_class_type(cfig, blrplan, jv, fund_ratio_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, fund_ratio_str()) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, fund_ratio_str()) == True

    assert g_class_type(cfig, blrplan, jv, gogo_calc_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, gogo_calc_str()) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, gogo_calc_str()) == True

    assert g_class_type(cfig, blrplan, jv, healerunit_ratio_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, healerunit_ratio_str()) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, healerunit_ratio_str()) == True

    assert g_class_type(cfig, blrplan, jv, tree_level_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, tree_level_str()) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, tree_level_str()) == True

    assert g_class_type(cfig, blrplan, jv, range_evaluated_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, range_evaluated_str()) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, range_evaluated_str()) == True

    assert g_class_type(cfig, blrplan, jv, stop_calc_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, stop_calc_str()) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, stop_calc_str()) == True

    assert g_class_type(cfig, blrplan, jv, chore_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, chore_str()) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, chore_str()) == True

    assert g_class_type(cfig, blrplan, jv, addin_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, addin_str()) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, addin_str()) == False

    assert g_class_type(cfig, blrplan, jv, begin_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, begin_str()) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, begin_str()) == False

    assert g_class_type(cfig, blrplan, jv, close_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, close_str()) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, close_str()) == False

    assert g_class_type(cfig, blrplan, jv, denom_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, denom_str()) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, denom_str()) == False

    assert g_class_type(cfig, blrplan, jv, gogo_want_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, gogo_want_str()) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, gogo_want_str()) == False

    assert g_class_type(cfig, blrplan, jv, star_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, star_str()) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, star_str()) == False

    assert g_class_type(cfig, blrplan, jv, morph_str()) == "bool"
    assert g_sqlitetype(cfig, blrplan, jv, morph_str()) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, morph_str()) == False

    assert g_class_type(cfig, blrplan, jv, numor_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, numor_str()) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, numor_str()) == False

    assert g_class_type(cfig, blrplan, jv, task_str()) == "bool"
    assert g_sqlitetype(cfig, blrplan, jv, task_str()) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, task_str()) == False

    assert g_class_type(cfig, blrplan, jv, problem_bool_str()) == "bool"
    assert g_sqlitetype(cfig, blrplan, jv, problem_bool_str()) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, problem_bool_str()) == False

    assert g_class_type(cfig, blrplan, jv, stop_want_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, stop_want_str()) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, stop_want_str()) == False

    assert g_class_type(cfig, blfunit, jv, "keeps_buildable") == "int"
    assert g_sqlitetype(cfig, blfunit, jv, "keeps_buildable") == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, "keeps_buildable") == True

    assert g_class_type(cfig, blfunit, jv, "keeps_justified") == "int"
    assert g_sqlitetype(cfig, blfunit, jv, "keeps_justified") == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, "keeps_justified") == True

    assert g_class_type(cfig, blfunit, jv, offtrack_fund_str()) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, offtrack_fund_str()) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, offtrack_fund_str()) == True

    assert g_class_type(cfig, blfunit, jv, rational_str()) == "bool"
    assert g_sqlitetype(cfig, blfunit, jv, rational_str()) == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, rational_str()) == True

    assert g_class_type(cfig, blfunit, jv, sum_healerunit_share_str()) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, sum_healerunit_share_str()) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, sum_healerunit_share_str()) == True

    assert g_class_type(cfig, blfunit, jv, tree_traverse_count_str()) == "int"
    assert g_sqlitetype(cfig, blfunit, jv, tree_traverse_count_str()) == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, tree_traverse_count_str()) == True

    assert g_class_type(cfig, blfunit, jv, credor_respect_str()) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, credor_respect_str()) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, credor_respect_str()) == False

    assert g_class_type(cfig, blfunit, jv, debtor_respect_str()) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, debtor_respect_str()) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, debtor_respect_str()) == False

    assert g_class_type(cfig, blfunit, jv, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, fund_iota_str()) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, fund_iota_str()) == False

    assert g_class_type(cfig, blfunit, jv, fund_pool_str()) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, fund_pool_str()) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, fund_pool_str()) == False

    assert g_class_type(cfig, blfunit, jv, max_tree_traverse_str()) == "int"
    assert g_sqlitetype(cfig, blfunit, jv, max_tree_traverse_str()) == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, max_tree_traverse_str()) == False

    assert g_class_type(cfig, blfunit, jv, penny_str()) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, penny_str()) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, penny_str()) == False

    assert g_class_type(cfig, blfunit, jv, respect_bit_str()) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, respect_bit_str()) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, respect_bit_str()) == False

    assert g_class_type(cfig, blfunit, jv, tally_str()) == "int"
    assert g_sqlitetype(cfig, blfunit, jv, tally_str()) == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, tally_str()) == False


def test_get_belief_config_dict_ReturnsObj_EachArgHasOneClassType():
    # ESTABLISH
    belief_config_dict = get_belief_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for belief_calc_dimen, dimen_dict in belief_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues"}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(class_type_str())
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
                    arg_type = arg_dict.get(sqlite_datatype_str())
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
                    arg_type = arg_dict.get(class_type_str())
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN
    belief_calc_args_type_dict = get_belief_calc_args_type_dict()

    # THEN
    assert belief_calc_args_type_dict.get(voice_name_str()) == NameTerm_str()
    assert belief_calc_args_type_dict.get(group_title_str()) == TitleTerm_str()
    assert belief_calc_args_type_dict.get(credor_pool_str()) == "float"
    assert belief_calc_args_type_dict.get(debtor_pool_str()) == "float"
    assert belief_calc_args_type_dict.get(fund_agenda_give_str()) == "float"
    assert belief_calc_args_type_dict.get(fund_agenda_ratio_give_str()) == "float"
    assert belief_calc_args_type_dict.get(fund_agenda_ratio_take_str()) == "float"
    assert belief_calc_args_type_dict.get(fund_agenda_take_str()) == "float"
    assert belief_calc_args_type_dict.get(fund_give_str()) == "float"
    assert belief_calc_args_type_dict.get(fund_take_str()) == "float"
    assert belief_calc_args_type_dict.get(group_cred_points_str()) == "int"
    assert belief_calc_args_type_dict.get(group_debt_points_str()) == "int"
    assert (
        belief_calc_args_type_dict.get(inallocable_voice_debt_points_str()) == "float"
    )
    assert belief_calc_args_type_dict.get(irrational_voice_debt_points_str()) == "float"
    assert belief_calc_args_type_dict.get(voice_cred_points_str()) == "float"
    assert belief_calc_args_type_dict.get(voice_debt_points_str()) == "float"
    assert belief_calc_args_type_dict.get(addin_str()) == "float"
    assert belief_calc_args_type_dict.get(begin_str()) == "float"
    assert belief_calc_args_type_dict.get(close_str()) == "float"
    assert belief_calc_args_type_dict.get(denom_str()) == "int"
    assert belief_calc_args_type_dict.get(gogo_want_str()) == "float"
    assert belief_calc_args_type_dict.get(star_str()) == "int"
    assert belief_calc_args_type_dict.get(morph_str()) == "bool"
    assert belief_calc_args_type_dict.get(numor_str()) == "int"
    assert belief_calc_args_type_dict.get(task_str()) == "bool"
    assert belief_calc_args_type_dict.get(problem_bool_str()) == "bool"
    assert belief_calc_args_type_dict.get(stop_want_str()) == "float"
    assert belief_calc_args_type_dict.get(awardee_title_str()) == TitleTerm_str()
    assert belief_calc_args_type_dict.get(plan_rope_str()) == RopePointer_str()
    assert belief_calc_args_type_dict.get(give_force_str()) == "float"
    assert belief_calc_args_type_dict.get(take_force_str()) == "float"
    assert belief_calc_args_type_dict.get(reason_context_str()) == RopePointer_str()
    assert belief_calc_args_type_dict.get(fact_upper_str()) == "float"
    assert belief_calc_args_type_dict.get(fact_lower_str()) == "float"
    assert belief_calc_args_type_dict.get(fact_state_str()) == RopePointer_str()
    assert belief_calc_args_type_dict.get(healer_name_str()) == NameTerm_str()
    assert belief_calc_args_type_dict.get(reason_state_str()) == RopePointer_str()
    assert belief_calc_args_type_dict.get(status_str()) == "int"
    assert belief_calc_args_type_dict.get(chore_str()) == "int"
    assert belief_calc_args_type_dict.get(reason_divisor_str()) == "int"
    assert belief_calc_args_type_dict.get(reason_upper_str()) == "float"
    assert belief_calc_args_type_dict.get(reason_lower_str()) == "float"
    assert belief_calc_args_type_dict.get("_reason_active_heir") == "int"
    assert belief_calc_args_type_dict.get(reason_active_requisite_str()) == "bool"
    assert belief_calc_args_type_dict.get(party_title_str()) == TitleTerm_str()
    assert belief_calc_args_type_dict.get("_belief_name_is_labor") == "int"
    assert belief_calc_args_type_dict.get(active_str()) == "int"
    assert belief_calc_args_type_dict.get(all_voice_cred_str()) == "int"
    assert belief_calc_args_type_dict.get(all_voice_debt_str()) == "int"
    assert belief_calc_args_type_dict.get(descendant_task_count_str()) == "int"
    assert belief_calc_args_type_dict.get(fund_cease_str()) == "float"
    assert belief_calc_args_type_dict.get(fund_onset_str()) == "float"
    assert belief_calc_args_type_dict.get(fund_ratio_str()) == "float"
    assert belief_calc_args_type_dict.get(gogo_calc_str()) == "float"
    assert belief_calc_args_type_dict.get("healerunit_ratio") == "float"
    assert belief_calc_args_type_dict.get(tree_level_str()) == "int"
    assert belief_calc_args_type_dict.get(range_evaluated_str()) == "int"
    assert belief_calc_args_type_dict.get(stop_calc_str()) == "float"
    assert belief_calc_args_type_dict.get(keeps_buildable_str()) == "int"
    assert belief_calc_args_type_dict.get(keeps_justified_str()) == "int"
    assert belief_calc_args_type_dict.get(offtrack_fund_str()) == "int"
    assert belief_calc_args_type_dict.get(rational_str()) == "bool"
    assert belief_calc_args_type_dict.get(sum_healerunit_share_str()) == "float"
    assert belief_calc_args_type_dict.get(tree_traverse_count_str()) == "int"
    assert belief_calc_args_type_dict.get(credor_respect_str()) == "float"
    assert belief_calc_args_type_dict.get(debtor_respect_str()) == "float"
    assert belief_calc_args_type_dict.get(fund_iota_str()) == "float"
    assert belief_calc_args_type_dict.get(fund_pool_str()) == "float"
    assert belief_calc_args_type_dict.get(max_tree_traverse_str()) == "int"
    assert belief_calc_args_type_dict.get(penny_str()) == "float"
    assert belief_calc_args_type_dict.get(respect_bit_str()) == "float"
    assert belief_calc_args_type_dict.get(tally_str()) == "int"
    assert len(belief_calc_args_type_dict) == 72
