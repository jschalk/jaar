# from src.ch01_py.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd
from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import create_path
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
from src.ch07_belief_logic.belief_main import BeliefUnit, VoiceUnit
from src.ref.keywords import Ch07Keywords as kw


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
    assert kw.beliefunit in belief_config_keys
    assert kw.belief_voiceunit in belief_config_keys
    assert kw.belief_voice_membership in belief_config_keys
    assert kw.belief_planunit in belief_config_keys
    assert kw.belief_plan_awardunit in belief_config_keys
    assert kw.belief_plan_reasonunit in belief_config_keys
    assert kw.belief_plan_reason_caseunit in belief_config_keys
    assert kw.belief_plan_partyunit in belief_config_keys
    assert kw.belief_plan_healerunit in belief_config_keys
    assert kw.belief_plan_factunit in belief_config_keys
    assert kw.belief_groupunit in belief_config_keys
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
        assert kw.jkeys in attribute_keys
        assert kw.jvalues in attribute_keys
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
    blrunit_attribute = belief_config.get(kw.beliefunit)
    blfvoce_attribute = belief_config.get(kw.belief_voiceunit)
    blrmemb_attribute = belief_config.get(kw.belief_voice_membership)
    blrplan_attribute = belief_config.get(kw.belief_planunit)
    blrawar_attribute = belief_config.get(kw.belief_plan_awardunit)
    blrreas_attribute = belief_config.get(kw.belief_plan_reasonunit)
    blrcase_attribute = belief_config.get(kw.belief_plan_reason_caseunit)
    blrlabo_attribute = belief_config.get(kw.belief_plan_partyunit)
    blrheal_attribute = belief_config.get(kw.belief_plan_healerunit)
    blrfact_attribute = belief_config.get(kw.belief_plan_factunit)
    blrgrou_attribute = belief_config.get(kw.belief_groupunit)
    abbr_str = "abbreviation"
    assert blrunit_attribute.get(abbr_str) == "blrunit"
    assert blfvoce_attribute.get(abbr_str) == "blfvoce"
    assert blrmemb_attribute.get(abbr_str) == "blrmemb"
    assert blrplan_attribute.get(abbr_str) == "blrplan"
    assert blrawar_attribute.get(abbr_str) == "blrawar"
    assert blrreas_attribute.get(abbr_str) == "blrreas"
    assert blrcase_attribute.get(abbr_str) == "blrcase"
    assert blrlabo_attribute.get(abbr_str) == "blrlabo"
    assert blrheal_attribute.get(abbr_str) == "blrheal"
    assert blrfact_attribute.get(abbr_str) == "blrfact"
    assert blrgrou_attribute.get(abbr_str) == "blrgrou"


def test_get_all_belief_calc_args_ReturnsObj():
    # ESTABLISH / WHEN
    all_belief_calc_args = get_all_belief_calc_args()

    # THEN
    assert all_belief_calc_args
    assert kw.stop_want in all_belief_calc_args
    assert kw.plan_rope in all_belief_calc_args
    assert "fund_give" in all_belief_calc_args
    assert all_belief_calc_args.get("fund_give") == {
        "belief_plan_awardunit",
        "belief_voice_membership",
        "belief_groupunit",
        "belief_voiceunit",
    }

    assert len(all_belief_calc_args) == 78


def test_get_belief_config_dict_ReturnsObj_CheckArgDataTypesKeysExist():
    # ESTABLISH / WHEN
    belief_config = get_belief_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, attribute_dict in belief_config.items():
        for level2_key, fm_attribute_dict in attribute_dict.items():
            if level2_key in {kw.jkeys, kw.jvalues}:
                for level3_key, attr_dict in fm_attribute_dict.items():
                    print(
                        f"{level1_key=} {level2_key=} {level3_key=} {set(attr_dict.keys())=}"
                    )
                    assert set(attr_dict.keys()) == {
                        kw.class_type,
                        kw.sqlite_datatype,
                        "populate_by_cashout",
                    }


def test_get_belief_calc_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    belief_calc_dimens = get_belief_calc_dimens()

    # THEN
    expected_belief_calc_dimens = {
        kw.beliefunit,
        kw.belief_voiceunit,
        kw.belief_voice_membership,
        kw.belief_planunit,
        kw.belief_plan_awardunit,
        kw.belief_plan_reasonunit,
        kw.belief_plan_reason_caseunit,
        kw.belief_plan_partyunit,
        kw.belief_plan_healerunit,
        kw.belief_plan_factunit,
        kw.belief_groupunit,
    }
    assert belief_calc_dimens == expected_belief_calc_dimens
    assert belief_calc_dimens == set(get_belief_config_dict().keys())


def test_get_belief_calc_dimen_args_ReturnsObj():
    # ESTABLISH / WHEN
    belief_voiceunit_args = get_belief_calc_dimen_args(kw.belief_voiceunit)
    belief_planunit_args = get_belief_calc_dimen_args(kw.belief_planunit)
    belief_groupunit_args = get_belief_calc_dimen_args(kw.belief_groupunit)

    #  THEN
    print(f"          {belief_voiceunit_args=}")
    print("")
    print(f"{set(VoiceUnit().__dict__.keys())=}")
    # print(belief_voiceunit_args.difference(set(VoiceUnit().__dict__.keys())))
    # assert belief_voiceunit_args == set(VoiceUnit().__dict__.keys())
    assert belief_voiceunit_args == {
        kw.moment_label,
        kw.belief_name,
        kw.credor_pool,
        kw.debtor_pool,
        kw.fund_agenda_give,
        kw.fund_agenda_take,
        kw.fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take,
        kw.fund_give,
        kw.fund_take,
        kw.voice_cred_lumen,
        kw.voice_debt_lumen,
        kw.voice_name,
        kw.inallocable_voice_debt_lumen,
        kw.irrational_voice_debt_lumen,
        kw.groupmark,
    }
    assert belief_planunit_args == {
        kw.moment_label,
        kw.belief_name,
        kw.morph,
        kw.denom,
        kw.pledge,
        kw.close,
        kw.addin,
        kw.numor,
        kw.star,
        kw.stop_want,
        kw.gogo_calc,
        kw.stop_calc,
        kw.plan_active,
        kw.fund_onset,
        kw.fund_cease,
        kw.descendant_pledge_count,
        kw.all_voice_cred,
        kw.all_voice_debt,
        kw.healerunit_ratio,
        kw.tree_level,
        kw.task,
        kw.fund_grain,
        kw.fund_ratio,
        kw.range_evaluated,
        kw.problem_bool,
        kw.gogo_want,
        kw.plan_rope,
        kw.begin,
    }
    print(f"{belief_groupunit_args=}")
    assert belief_groupunit_args == {
        kw.moment_label,
        kw.belief_name,
        kw.debtor_pool,
        kw.credor_pool,
        kw.fund_give,
        kw.group_title,
        kw.fund_agenda_give,
        kw.fund_agenda_take,
        kw.fund_take,
        kw.fund_grain,
    }


def g_class_type(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get(kw.class_type)


def g_sqlitetype(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get(kw.sqlite_datatype)


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
    #         if level2_key in {kw.jkeys, kw.jvalues}:
    #             for level3_key, attr_dict in fm_attribute_dict.items():
    #                 dimem = attribute_dict.get("abbreviation")
    #                 x_class_type = attr_dict.get(kw.class_type)
    #                 x_sqlite_datatype = attr_dict.get(kw.sqlite_datatype)
    #                 print(
    #                     f"""    assert g_class_type(config, {dimem}, {level2_key[0:2]}, "{level3_key}") == "{x_class_type}" """
    #                 )
    #                 print(
    #                     f"""    assert g_sqlitetype(config, {dimem}, {level2_key[0:2]}, "{level3_key}") == "{x_sqlite_datatype}" """
    #                 )

    jk = "jkeys"
    jv = "jvalues"
    blfunit = kw.beliefunit
    blfvoce = kw.belief_voiceunit
    blrmemb = kw.belief_voice_membership
    blrplan = kw.belief_planunit
    blrawar = kw.belief_plan_awardunit
    blrreas = kw.belief_plan_reasonunit
    blrcase = kw.belief_plan_reason_caseunit
    blrlabo = kw.belief_plan_partyunit
    blrheal = kw.belief_plan_healerunit
    blrfact = kw.belief_plan_factunit
    blrgrou = kw.belief_groupunit
    assert g_class_type(cfig, blrmemb, jk, kw.voice_name) == kw.NameTerm
    assert g_sqlitetype(cfig, blrmemb, jk, kw.voice_name) == "TEXT"
    assert g_popcashout(cfig, blrmemb, jk, kw.voice_name) == False

    assert g_class_type(cfig, blrmemb, jk, kw.group_title) == kw.TitleTerm
    assert g_sqlitetype(cfig, blrmemb, jk, kw.group_title) == "TEXT"
    assert g_popcashout(cfig, blrmemb, jk, kw.group_title) == False

    assert g_class_type(cfig, blrmemb, jv, kw.credor_pool) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, kw.credor_pool) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, kw.credor_pool) == True

    assert g_class_type(cfig, blrmemb, jv, kw.debtor_pool) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, kw.debtor_pool) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, kw.debtor_pool) == True

    assert g_class_type(cfig, blrmemb, jv, kw.fund_agenda_give) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, kw.fund_agenda_give) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, kw.fund_agenda_give) == True

    assert g_class_type(cfig, blrmemb, jv, kw.fund_agenda_ratio_give) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, kw.fund_agenda_ratio_give) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, kw.fund_agenda_ratio_give) == True

    assert g_class_type(cfig, blrmemb, jv, kw.fund_agenda_ratio_take) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, kw.fund_agenda_ratio_take) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, kw.fund_agenda_ratio_take) == True

    assert g_class_type(cfig, blrmemb, jv, kw.fund_agenda_take) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, kw.fund_agenda_take) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, kw.fund_agenda_take) == True

    assert g_class_type(cfig, blrmemb, jv, kw.fund_give) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, kw.fund_give) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, kw.fund_give) == True

    assert g_class_type(cfig, blrmemb, jv, kw.fund_take) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, kw.fund_take) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, kw.fund_take) == True

    assert g_class_type(cfig, blrmemb, jv, kw.group_cred_lumen) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, kw.group_cred_lumen) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, kw.group_cred_lumen) == False

    assert g_class_type(cfig, blrmemb, jv, kw.group_debt_lumen) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, kw.group_debt_lumen) == "REAL"
    assert g_popcashout(cfig, blrmemb, jv, kw.group_debt_lumen) == False

    assert g_class_type(cfig, blfvoce, jk, kw.voice_name) == kw.NameTerm
    assert g_sqlitetype(cfig, blfvoce, jk, kw.voice_name) == "TEXT"
    assert g_popcashout(cfig, blfvoce, jk, kw.voice_name) == False

    assert g_class_type(cfig, blfvoce, jv, kw.credor_pool) == "float"
    assert g_sqlitetype(cfig, blfvoce, jv, kw.credor_pool) == "REAL"
    assert g_popcashout(cfig, blfvoce, jv, kw.credor_pool) == True

    assert g_class_type(cfig, blfvoce, jv, kw.debtor_pool) == "float"
    assert g_sqlitetype(cfig, blfvoce, jv, kw.debtor_pool) == "REAL"
    assert g_popcashout(cfig, blfvoce, jv, kw.debtor_pool) == True

    assert g_class_type(cfig, blfvoce, jv, kw.fund_agenda_give) == "float"
    assert g_sqlitetype(cfig, blfvoce, jv, kw.fund_agenda_give) == "REAL"
    assert g_popcashout(cfig, blfvoce, jv, kw.fund_agenda_give) == True

    assert g_class_type(cfig, blfvoce, jv, kw.fund_agenda_ratio_give) == "float"
    assert g_sqlitetype(cfig, blfvoce, jv, kw.fund_agenda_ratio_give) == "REAL"
    assert g_popcashout(cfig, blfvoce, jv, kw.fund_agenda_ratio_give) == True

    assert g_class_type(cfig, blfvoce, jv, kw.fund_agenda_ratio_take) == "float"
    assert g_sqlitetype(cfig, blfvoce, jv, kw.fund_agenda_ratio_take) == "REAL"
    assert g_popcashout(cfig, blfvoce, jv, kw.fund_agenda_ratio_take) == True

    assert g_class_type(cfig, blfvoce, jv, kw.fund_agenda_take) == "float"
    assert g_sqlitetype(cfig, blfvoce, jv, kw.fund_agenda_take) == "REAL"
    assert g_popcashout(cfig, blfvoce, jv, kw.fund_agenda_take) == True

    assert g_class_type(cfig, blfvoce, jv, kw.fund_give) == "float"
    assert g_sqlitetype(cfig, blfvoce, jv, kw.fund_give) == "REAL"
    assert g_popcashout(cfig, blfvoce, jv, kw.fund_give) == True

    assert g_class_type(cfig, blfvoce, jv, kw.fund_take) == "float"
    assert g_sqlitetype(cfig, blfvoce, jv, kw.fund_take) == "REAL"
    assert g_popcashout(cfig, blfvoce, jv, kw.fund_take) == True

    assert g_class_type(cfig, blfvoce, jv, kw.inallocable_voice_debt_lumen) == "float"
    assert g_sqlitetype(cfig, blfvoce, jv, kw.inallocable_voice_debt_lumen) == "REAL"
    assert g_popcashout(cfig, blfvoce, jv, kw.inallocable_voice_debt_lumen) == True

    assert g_class_type(cfig, blfvoce, jv, kw.irrational_voice_debt_lumen) == "float"
    assert g_sqlitetype(cfig, blfvoce, jv, kw.irrational_voice_debt_lumen) == "REAL"
    assert g_popcashout(cfig, blfvoce, jv, kw.irrational_voice_debt_lumen) == True

    assert g_class_type(cfig, blfvoce, jv, kw.voice_cred_lumen) == "float"
    assert g_sqlitetype(cfig, blfvoce, jv, kw.voice_cred_lumen) == "REAL"
    assert g_popcashout(cfig, blfvoce, jv, kw.voice_cred_lumen) == False

    assert g_class_type(cfig, blfvoce, jv, kw.voice_debt_lumen) == "float"
    assert g_sqlitetype(cfig, blfvoce, jv, kw.voice_debt_lumen) == "REAL"
    assert g_popcashout(cfig, blfvoce, jv, kw.voice_debt_lumen) == False

    assert g_class_type(cfig, blrgrou, jk, kw.group_title) == "TitleTerm"
    assert g_sqlitetype(cfig, blrgrou, jk, kw.group_title) == "TEXT"
    assert g_popcashout(cfig, blrgrou, jk, kw.group_title) == True

    assert g_class_type(cfig, blrgrou, jv, kw.debtor_pool) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, kw.debtor_pool) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, kw.debtor_pool) == True

    assert g_class_type(cfig, blrgrou, jv, kw.credor_pool) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, kw.credor_pool) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, kw.credor_pool) == True

    assert g_class_type(cfig, blrgrou, jv, kw.fund_give) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, kw.fund_give) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, kw.fund_give) == True

    assert g_class_type(cfig, blrgrou, jv, kw.fund_agenda_give) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, kw.fund_agenda_give) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, kw.fund_agenda_give) == True

    assert g_class_type(cfig, blrgrou, jv, kw.fund_agenda_take) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, kw.fund_agenda_take) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, kw.fund_agenda_take) == True

    assert g_class_type(cfig, blrgrou, jv, kw.fund_take) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, kw.fund_take) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, kw.fund_take) == True

    assert g_class_type(cfig, blrgrou, jv, kw.fund_grain) == "float"
    assert g_sqlitetype(cfig, blrgrou, jv, kw.fund_grain) == "REAL"
    assert g_popcashout(cfig, blrgrou, jv, kw.fund_grain) == True

    assert g_class_type(cfig, blrawar, jk, kw.awardee_title) == kw.TitleTerm
    assert g_sqlitetype(cfig, blrawar, jk, kw.awardee_title) == "TEXT"
    assert g_popcashout(cfig, blrawar, jk, kw.awardee_title) == False

    assert g_class_type(cfig, blrawar, jk, kw.plan_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, blrawar, jk, kw.plan_rope) == "TEXT"
    assert g_popcashout(cfig, blrawar, jk, kw.plan_rope) == False

    assert g_class_type(cfig, blrawar, jv, kw.fund_give) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, kw.fund_give) == "REAL"
    assert g_popcashout(cfig, blrawar, jv, kw.fund_give) == True

    assert g_class_type(cfig, blrawar, jv, kw.fund_take) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, kw.fund_take) == "REAL"
    assert g_popcashout(cfig, blrawar, jv, kw.fund_take) == True

    assert g_class_type(cfig, blrawar, jv, kw.give_force) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, kw.give_force) == "REAL"
    assert g_popcashout(cfig, blrawar, jv, kw.give_force) == False

    assert g_class_type(cfig, blrawar, jv, kw.take_force) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, kw.take_force) == "REAL"
    assert g_popcashout(cfig, blrawar, jv, kw.take_force) == False

    assert g_class_type(cfig, blrfact, jk, kw.fact_context) == kw.RopeTerm
    assert g_sqlitetype(cfig, blrfact, jk, kw.fact_context) == "TEXT"
    assert g_popcashout(cfig, blrfact, jk, kw.fact_context) == False

    assert g_class_type(cfig, blrfact, jk, kw.plan_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, blrfact, jk, kw.plan_rope) == "TEXT"
    assert g_popcashout(cfig, blrfact, jk, kw.plan_rope) == False

    assert g_class_type(cfig, blrfact, jv, kw.fact_upper) == kw.ContextNum
    assert g_sqlitetype(cfig, blrfact, jv, kw.fact_upper) == "REAL"
    assert g_popcashout(cfig, blrfact, jv, kw.fact_upper) == False

    assert g_class_type(cfig, blrfact, jv, kw.fact_lower) == kw.ContextNum
    assert g_sqlitetype(cfig, blrfact, jv, kw.fact_lower) == "REAL"
    assert g_popcashout(cfig, blrfact, jv, kw.fact_lower) == False

    assert g_class_type(cfig, blrfact, jv, kw.fact_state) == kw.RopeTerm
    assert g_sqlitetype(cfig, blrfact, jv, kw.fact_state) == "TEXT"
    assert g_popcashout(cfig, blrfact, jv, kw.fact_state) == False

    assert g_class_type(cfig, blrheal, jk, kw.healer_name) == kw.NameTerm
    assert g_sqlitetype(cfig, blrheal, jk, kw.healer_name) == "TEXT"
    assert g_popcashout(cfig, blrheal, jk, kw.healer_name) == False

    assert g_class_type(cfig, blrheal, jk, kw.plan_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, blrheal, jk, kw.plan_rope) == "TEXT"
    assert g_popcashout(cfig, blrheal, jk, kw.plan_rope) == False

    assert g_class_type(cfig, blrcase, jk, kw.reason_context) == kw.RopeTerm
    assert g_sqlitetype(cfig, blrcase, jk, kw.reason_context) == "TEXT"
    assert g_popcashout(cfig, blrcase, jk, kw.reason_context) == False

    assert g_class_type(cfig, blrcase, jk, kw.reason_state) == kw.RopeTerm
    assert g_sqlitetype(cfig, blrcase, jk, kw.reason_state) == "TEXT"
    assert g_popcashout(cfig, blrcase, jk, kw.reason_state) == False

    assert g_class_type(cfig, blrcase, jk, kw.plan_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, blrcase, jk, kw.plan_rope) == "TEXT"
    assert g_popcashout(cfig, blrcase, jk, kw.plan_rope) == False

    assert g_class_type(cfig, blrcase, jv, kw.case_active) == "int"
    assert g_sqlitetype(cfig, blrcase, jv, kw.case_active) == "INTEGER"
    assert g_popcashout(cfig, blrcase, jv, kw.case_active) == True

    assert g_class_type(cfig, blrcase, jv, kw.task) == "int"
    assert g_sqlitetype(cfig, blrcase, jv, kw.task) == "INTEGER"
    assert g_popcashout(cfig, blrcase, jv, kw.task) == True

    assert g_class_type(cfig, blrcase, jv, kw.reason_divisor) == "int"
    assert g_sqlitetype(cfig, blrcase, jv, kw.reason_divisor) == "INTEGER"
    assert g_popcashout(cfig, blrcase, jv, kw.reason_divisor) == False

    assert g_class_type(cfig, blrcase, jv, kw.reason_upper) == kw.ContextNum
    assert g_sqlitetype(cfig, blrcase, jv, kw.reason_upper) == "REAL"
    assert g_popcashout(cfig, blrcase, jv, kw.reason_upper) == False

    assert g_class_type(cfig, blrcase, jv, kw.reason_lower) == kw.ContextNum
    assert g_sqlitetype(cfig, blrcase, jv, kw.reason_lower) == "REAL"
    assert g_popcashout(cfig, blrcase, jv, kw.reason_lower) == False

    assert g_class_type(cfig, blrreas, jk, kw.reason_context) == kw.RopeTerm
    assert g_sqlitetype(cfig, blrreas, jk, kw.reason_context) == "TEXT"
    assert g_popcashout(cfig, blrreas, jk, kw.reason_context) == False

    assert g_class_type(cfig, blrreas, jk, kw.plan_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, blrreas, jk, kw.plan_rope) == "TEXT"
    assert g_popcashout(cfig, blrreas, jk, kw.plan_rope) == False

    assert g_class_type(cfig, blrreas, jv, kw.parent_heir_active) == "int"
    assert g_sqlitetype(cfig, blrreas, jv, kw.parent_heir_active) == "INTEGER"
    assert g_popcashout(cfig, blrreas, jv, kw.parent_heir_active) == True

    assert g_class_type(cfig, blrreas, jv, kw.reason_active) == "int"
    assert g_sqlitetype(cfig, blrreas, jv, kw.reason_active) == "INTEGER"
    assert g_popcashout(cfig, blrreas, jv, kw.reason_active) == True

    assert g_class_type(cfig, blrreas, jv, kw.task) == "int"
    assert g_sqlitetype(cfig, blrreas, jv, kw.task) == "INTEGER"
    assert g_popcashout(cfig, blrreas, jv, kw.task) == True

    assert g_class_type(cfig, blrreas, jv, kw.active_requisite) == "bool"
    assert g_sqlitetype(cfig, blrreas, jv, kw.active_requisite) == "INTEGER"
    assert g_popcashout(cfig, blrreas, jv, kw.active_requisite) == False

    assert g_class_type(cfig, blrlabo, jk, kw.plan_rope) == kw.RopeTerm
    assert g_sqlitetype(cfig, blrlabo, jk, kw.plan_rope) == "TEXT"
    assert g_popcashout(cfig, blrlabo, jk, kw.plan_rope) == False

    assert g_class_type(cfig, blrlabo, jk, kw.party_title) == kw.TitleTerm
    assert g_sqlitetype(cfig, blrlabo, jk, kw.party_title) == "TEXT"
    assert g_popcashout(cfig, blrlabo, jk, kw.party_title) == False

    assert g_class_type(cfig, blrlabo, jv, "belief_name_is_labor") == "int"
    assert g_sqlitetype(cfig, blrlabo, jv, "belief_name_is_labor") == "INTEGER"
    assert g_popcashout(cfig, blrlabo, jv, "belief_name_is_labor") == True

    assert g_class_type(cfig, blrplan, jv, "plan_active") == "int"
    assert g_sqlitetype(cfig, blrplan, jv, "plan_active") == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, "plan_active") == True

    assert g_class_type(cfig, blrplan, jv, kw.all_voice_cred) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, kw.all_voice_cred) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, kw.all_voice_cred) == True

    assert g_class_type(cfig, blrplan, jv, kw.all_voice_debt) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, kw.all_voice_debt) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, kw.all_voice_debt) == True

    assert g_class_type(cfig, blrplan, jv, kw.descendant_pledge_count) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, kw.descendant_pledge_count) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, kw.descendant_pledge_count) == True

    assert g_class_type(cfig, blrplan, jv, kw.fund_cease) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, kw.fund_cease) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, kw.fund_cease) == True

    assert g_class_type(cfig, blrplan, jv, kw.fund_grain) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, kw.fund_grain) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, kw.fund_grain) == True

    assert g_class_type(cfig, blrplan, jv, kw.fund_onset) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, kw.fund_onset) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, kw.fund_onset) == True

    assert g_class_type(cfig, blrplan, jv, kw.fund_ratio) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, kw.fund_ratio) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, kw.fund_ratio) == True

    assert g_class_type(cfig, blrplan, jv, kw.gogo_calc) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, kw.gogo_calc) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, kw.gogo_calc) == True

    assert g_class_type(cfig, blrplan, jv, kw.healerunit_ratio) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, kw.healerunit_ratio) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, kw.healerunit_ratio) == True

    assert g_class_type(cfig, blrplan, jv, kw.tree_level) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, kw.tree_level) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, kw.tree_level) == True

    assert g_class_type(cfig, blrplan, jv, kw.range_evaluated) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, kw.range_evaluated) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, kw.range_evaluated) == True

    assert g_class_type(cfig, blrplan, jv, kw.stop_calc) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, kw.stop_calc) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, kw.stop_calc) == True

    assert g_class_type(cfig, blrplan, jv, kw.task) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, kw.task) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, kw.task) == True

    assert g_class_type(cfig, blrplan, jv, kw.addin) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, kw.addin) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, kw.addin) == False

    assert g_class_type(cfig, blrplan, jv, kw.begin) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, kw.begin) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, kw.begin) == False

    assert g_class_type(cfig, blrplan, jv, kw.close) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, kw.close) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, kw.close) == False

    assert g_class_type(cfig, blrplan, jv, kw.denom) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, kw.denom) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, kw.denom) == False

    assert g_class_type(cfig, blrplan, jv, kw.gogo_want) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, kw.gogo_want) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, kw.gogo_want) == False

    assert g_class_type(cfig, blrplan, jv, kw.star) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, kw.star) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, kw.star) == False

    assert g_class_type(cfig, blrplan, jv, kw.morph) == "bool"
    assert g_sqlitetype(cfig, blrplan, jv, kw.morph) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, kw.morph) == False

    assert g_class_type(cfig, blrplan, jv, kw.numor) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, kw.numor) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, kw.numor) == False

    assert g_class_type(cfig, blrplan, jv, kw.pledge) == "bool"
    assert g_sqlitetype(cfig, blrplan, jv, kw.pledge) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, kw.pledge) == False

    assert g_class_type(cfig, blrplan, jv, kw.problem_bool) == "bool"
    assert g_sqlitetype(cfig, blrplan, jv, kw.problem_bool) == "INTEGER"
    assert g_popcashout(cfig, blrplan, jv, kw.problem_bool) == False

    assert g_class_type(cfig, blrplan, jv, kw.stop_want) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, kw.stop_want) == "REAL"
    assert g_popcashout(cfig, blrplan, jv, kw.stop_want) == False

    assert g_class_type(cfig, blfunit, jv, "keeps_buildable") == "int"
    assert g_sqlitetype(cfig, blfunit, jv, "keeps_buildable") == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, "keeps_buildable") == True

    assert g_class_type(cfig, blfunit, jv, "keeps_justified") == "int"
    assert g_sqlitetype(cfig, blfunit, jv, "keeps_justified") == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, "keeps_justified") == True

    assert g_class_type(cfig, blfunit, jv, kw.offtrack_fund) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, kw.offtrack_fund) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, kw.offtrack_fund) == True

    assert g_class_type(cfig, blfunit, jv, kw.rational) == "bool"
    assert g_sqlitetype(cfig, blfunit, jv, kw.rational) == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, kw.rational) == True

    assert (
        g_class_type(cfig, blfunit, jv, kw.sum_healerunit_plans_fund_total) == "float"
    )
    assert g_sqlitetype(cfig, blfunit, jv, kw.sum_healerunit_plans_fund_total) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, kw.sum_healerunit_plans_fund_total) == True

    assert g_class_type(cfig, blfunit, jv, kw.tree_traverse_count) == "int"
    assert g_sqlitetype(cfig, blfunit, jv, kw.tree_traverse_count) == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, kw.tree_traverse_count) == True

    assert g_class_type(cfig, blfunit, jv, kw.credor_respect) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, kw.credor_respect) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, kw.credor_respect) == False

    assert g_class_type(cfig, blfunit, jv, kw.debtor_respect) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, kw.debtor_respect) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, kw.debtor_respect) == False

    assert g_class_type(cfig, blfunit, jv, kw.fund_grain) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, kw.fund_grain) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, kw.fund_grain) == False

    assert g_class_type(cfig, blfunit, jv, kw.fund_pool) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, kw.fund_pool) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, kw.fund_pool) == False

    assert g_class_type(cfig, blfunit, jv, kw.max_tree_traverse) == "int"
    assert g_sqlitetype(cfig, blfunit, jv, kw.max_tree_traverse) == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, kw.max_tree_traverse) == False

    assert g_class_type(cfig, blfunit, jv, kw.mana_grain) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, kw.mana_grain) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, kw.mana_grain) == False

    assert g_class_type(cfig, blfunit, jv, kw.respect_grain) == "float"
    assert g_sqlitetype(cfig, blfunit, jv, kw.respect_grain) == "REAL"
    assert g_popcashout(cfig, blfunit, jv, kw.respect_grain) == False

    assert g_class_type(cfig, blfunit, jv, kw.tally) == "int"
    assert g_sqlitetype(cfig, blfunit, jv, kw.tally) == "INTEGER"
    assert g_popcashout(cfig, blfunit, jv, kw.tally) == False


def test_get_belief_config_dict_ReturnsObj_EachArgHasOneClassType():
    # ESTABLISH
    belief_config_dict = get_belief_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for belief_calc_dimen, dimen_dict in belief_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues"}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(kw.class_type)
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN / THEN
    for x_arg, arg_types in all_args.items():
        # print(f"{x_arg=} {arg_types=}")
        assertion_failure_str = f"{x_arg=} {arg_types=}"
        assert len(arg_types) == 1, assertion_failure_str


def test_get_belief_config_dict_ReturnsObj_EachArgHasOne_sqlite_datatype():
    # ESTABLISH
    belief_config_dict = get_belief_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for belief_calc_dimen, dimen_dict in belief_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues"}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(kw.sqlite_datatype)
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    for x_arg, arg_types in all_args.items():
        # print(f"{x_arg=} {arg_types=}")
        assertion_failure_str = f"{x_arg=} {arg_types=}"
        assert len(arg_types) == 1, assertion_failure_str

    # WHEN
    sqlite_datatype_dict = get_belief_calc_args_sqlite_datatype_dict()

    # THEN
    for x_arg, arg_types in all_args.items():
        # print(
        #     f"""assert belief_calc_args_type_dict.get("{x_arg}") == "{list(arg_types)[0]}" """
        # )
        # print(f""""{x_arg}": "{list(arg_types)[0]}",""")
        assert_failure_str = f""""{x_arg}": "{list(arg_types)[0]}","""
        assert list(arg_types)[0] == sqlite_datatype_dict.get(x_arg), assert_failure_str


def test_get_belief_calc_args_type_dict_ReturnsObj():
    # ESTABLISH
    belief_config_dict = get_belief_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for belief_calc_dimen, dimen_dict in belief_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues"}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(kw.class_type)
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN
    belief_calc_args_type_dict = get_belief_calc_args_type_dict()

    # THEN
    assert belief_calc_args_type_dict.get(kw.voice_name) == kw.NameTerm
    assert belief_calc_args_type_dict.get(kw.group_title) == kw.TitleTerm
    assert belief_calc_args_type_dict.get(kw.case_active) == "int"
    assert belief_calc_args_type_dict.get(kw.credor_pool) == "float"
    assert belief_calc_args_type_dict.get(kw.debtor_pool) == "float"
    assert belief_calc_args_type_dict.get(kw.fund_agenda_give) == "float"
    assert belief_calc_args_type_dict.get(kw.fund_agenda_ratio_give) == "float"
    assert belief_calc_args_type_dict.get(kw.fund_agenda_ratio_take) == "float"
    assert belief_calc_args_type_dict.get(kw.fund_agenda_take) == "float"
    assert belief_calc_args_type_dict.get(kw.fund_give) == "float"
    assert belief_calc_args_type_dict.get(kw.fund_take) == "float"
    assert belief_calc_args_type_dict.get(kw.group_cred_lumen) == "int"
    assert belief_calc_args_type_dict.get(kw.group_debt_lumen) == "int"
    assert belief_calc_args_type_dict.get(kw.inallocable_voice_debt_lumen) == "float"
    assert belief_calc_args_type_dict.get(kw.irrational_voice_debt_lumen) == "float"
    assert belief_calc_args_type_dict.get(kw.voice_cred_lumen) == "float"
    assert belief_calc_args_type_dict.get(kw.voice_debt_lumen) == "float"
    assert belief_calc_args_type_dict.get(kw.addin) == "float"
    assert belief_calc_args_type_dict.get(kw.begin) == "float"
    assert belief_calc_args_type_dict.get(kw.close) == "float"
    assert belief_calc_args_type_dict.get(kw.denom) == "int"
    assert belief_calc_args_type_dict.get(kw.gogo_want) == "float"
    assert belief_calc_args_type_dict.get(kw.star) == "int"
    assert belief_calc_args_type_dict.get(kw.morph) == "bool"
    assert belief_calc_args_type_dict.get(kw.numor) == "int"
    assert belief_calc_args_type_dict.get(kw.pledge) == "bool"
    assert belief_calc_args_type_dict.get(kw.problem_bool) == "bool"
    assert belief_calc_args_type_dict.get(kw.stop_want) == "float"
    assert belief_calc_args_type_dict.get(kw.awardee_title) == kw.TitleTerm
    assert belief_calc_args_type_dict.get(kw.plan_rope) == kw.RopeTerm
    assert belief_calc_args_type_dict.get(kw.give_force) == "float"
    assert belief_calc_args_type_dict.get(kw.take_force) == "float"
    assert belief_calc_args_type_dict.get(kw.reason_context) == kw.RopeTerm
    assert belief_calc_args_type_dict.get(kw.fact_upper) == kw.ContextNum
    assert belief_calc_args_type_dict.get(kw.fact_lower) == kw.ContextNum
    assert belief_calc_args_type_dict.get(kw.fact_state) == kw.RopeTerm
    assert belief_calc_args_type_dict.get(kw.healer_name) == kw.NameTerm
    assert belief_calc_args_type_dict.get(kw.reason_state) == kw.RopeTerm
    assert belief_calc_args_type_dict.get(kw.reason_active) == "int"
    assert belief_calc_args_type_dict.get(kw.task) == "int"
    assert belief_calc_args_type_dict.get(kw.reason_divisor) == "int"
    assert belief_calc_args_type_dict.get(kw.reason_upper) == kw.ContextNum
    assert belief_calc_args_type_dict.get(kw.reason_lower) == kw.ContextNum
    assert belief_calc_args_type_dict.get(kw.parent_heir_active) == "int"
    assert belief_calc_args_type_dict.get(kw.active_requisite) == "bool"
    assert belief_calc_args_type_dict.get(kw.party_title) == kw.TitleTerm
    assert belief_calc_args_type_dict.get("belief_name_is_labor") == "int"
    assert belief_calc_args_type_dict.get(kw.plan_active) == "int"
    assert belief_calc_args_type_dict.get(kw.all_voice_cred) == "int"
    assert belief_calc_args_type_dict.get(kw.all_voice_debt) == "int"
    assert belief_calc_args_type_dict.get(kw.descendant_pledge_count) == "int"
    assert belief_calc_args_type_dict.get(kw.fund_cease) == "float"
    assert belief_calc_args_type_dict.get(kw.fund_onset) == "float"
    assert belief_calc_args_type_dict.get(kw.fund_ratio) == "float"
    assert belief_calc_args_type_dict.get(kw.gogo_calc) == "float"
    assert belief_calc_args_type_dict.get("healerunit_ratio") == "float"
    assert belief_calc_args_type_dict.get(kw.tree_level) == "int"
    assert belief_calc_args_type_dict.get(kw.range_evaluated) == "int"
    assert belief_calc_args_type_dict.get(kw.stop_calc) == "float"
    assert belief_calc_args_type_dict.get(kw.keeps_buildable) == "int"
    assert belief_calc_args_type_dict.get(kw.keeps_justified) == "int"
    assert belief_calc_args_type_dict.get(kw.offtrack_fund) == "int"
    assert belief_calc_args_type_dict.get(kw.rational) == "bool"
    assert belief_calc_args_type_dict.get(kw.sum_healerunit_plans_fund_total) == "float"
    assert belief_calc_args_type_dict.get(kw.tree_traverse_count) == "int"
    assert belief_calc_args_type_dict.get(kw.credor_respect) == "float"
    assert belief_calc_args_type_dict.get(kw.debtor_respect) == "float"
    assert belief_calc_args_type_dict.get(kw.fund_grain) == "float"
    assert belief_calc_args_type_dict.get(kw.fund_pool) == "float"
    assert belief_calc_args_type_dict.get(kw.max_tree_traverse) == "int"
    assert belief_calc_args_type_dict.get(kw.mana_grain) == "float"
    assert belief_calc_args_type_dict.get(kw.respect_grain) == "float"
    assert belief_calc_args_type_dict.get(kw.tally) == "int"
    assert len(belief_calc_args_type_dict) == 73
