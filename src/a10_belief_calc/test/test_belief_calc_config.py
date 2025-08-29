# from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd
from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.test._util.a01_str import knot_str
from src.a03_group_logic.test._util.a03_str import (
    awardee_title_str,
    credor_pool_str,
    debtor_pool_str,
    fund_agenda_give_str,
    fund_agenda_ratio_give_str,
    fund_agenda_ratio_take_str,
    fund_agenda_take_str,
    fund_give_str,
    fund_take_str,
    give_force_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    inallocable_voice_debt_points_str,
    irrational_voice_debt_points_str,
    respect_bit_str,
    take_force_str,
    voice_cred_points_str,
    voice_debt_points_str,
)
from src.a04_reason_logic.test._util.a04_str import (
    belief_name_str,
    chore_str,
    fact_context_str,
    fact_lower_str,
    fact_state_str,
    fact_upper_str,
    moment_label_str,
    party_title_str,
    reason_active_requisite_str,
    reason_context_str,
    reason_divisor_str,
    reason_lower_str,
    reason_state_str,
    reason_upper_str,
    status_str,
)
from src.a05_plan_logic.test._util.a05_str import (
    all_voice_cred_str,
    all_voice_debt_str,
    descendant_task_count_str,
    fund_cease_str,
    fund_onset_str,
    fund_ratio_str,
    gogo_calc_str,
    healerunit_ratio_str,
    problem_bool_str,
    range_evaluated_str,
    star_str,
    stop_calc_str,
    task_str,
)
from src.a06_belief_logic.test._util.a06_str import (
    LabelTerm_str,
    NameTerm_str,
    RopeTerm_str,
    TitleTerm_str,
    addin_str,
    awardee_title_str,
    begin_str,
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
    close_str,
    credor_respect_str,
    debtor_respect_str,
    denom_str,
    fact_context_str,
    fact_lower_str,
    fact_state_str,
    fact_upper_str,
    fund_iota_str,
    fund_pool_str,
    gogo_want_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    healer_name_str,
    max_tree_traverse_str,
    morph_str,
    numor_str,
    offtrack_fund_str,
    penny_str,
    plan_rope_str,
    rational_str,
    reason_context_str,
    reason_lower_str,
    reason_state_str,
    reason_upper_str,
    stop_want_str,
    sum_healerunit_share_str,
    tally_str,
    tree_traverse_count_str,
    voice_cred_points_str,
    voice_debt_points_str,
    voice_name_str,
)
from src.a08_belief_atom_logic.atom_config import get_atom_config_dict
from src.a08_belief_atom_logic.test._util.a08_str import (
    class_type_str,
    jkeys_str,
    jvalues_str,
    sqlite_datatype_str,
)
from src.a10_belief_calc.belief_calc_config import (
    belief_calc_config_path,
    get_all_belief_calc_args,
    get_belief_calc_args_sqlite_datatype_dict,
    get_belief_calc_args_type_dict,
    get_belief_calc_config_dict,
    get_belief_calc_dimen_args,
    get_belief_calc_dimens,
)
from src.a10_belief_calc.test._util.a10_str import belief_groupunit_str, jmetrics_str


def test_get_belief_calc_config_dict_Exists():
    # ESTABLISH
    src_dir = create_path(os_getcwd(), "src")
    expected_dir = create_path(src_dir, "a10_belief_calc")

    # WHEN
    config_path = belief_calc_config_path()
    # THEN
    expected_path = create_path(expected_dir, "belief_calc_config.json")
    assert config_path == expected_path
    assert os_path_exists(belief_calc_config_path())


def test_get_belief_calc_config_dict_ReturnsObj_CheckLevel0Keys():
    # ESTABLISH / WHEN
    belief_calc_config = get_belief_calc_config_dict()
    belief_calc_config_keys = set(belief_calc_config.keys())

    # THEN
    assert beliefunit_str() in belief_calc_config_keys
    assert belief_voiceunit_str() in belief_calc_config_keys
    assert belief_voice_membership_str() in belief_calc_config_keys
    assert belief_planunit_str() in belief_calc_config_keys
    assert belief_plan_awardunit_str() in belief_calc_config_keys
    assert belief_plan_reasonunit_str() in belief_calc_config_keys
    assert belief_plan_reason_caseunit_str() in belief_calc_config_keys
    assert belief_plan_partyunit_str() in belief_calc_config_keys
    assert belief_plan_healerunit_str() in belief_calc_config_keys
    assert belief_plan_factunit_str() in belief_calc_config_keys
    assert belief_groupunit_str() in belief_calc_config_keys
    assert len(get_belief_calc_config_dict()) == 11
    atom_config_dict = get_atom_config_dict()
    atom_config_dimens = set(atom_config_dict.keys())
    assert atom_config_dimens.issubset(belief_calc_config_keys)
    assert belief_calc_config_keys.difference(atom_config_dimens) == {
        belief_groupunit_str()
    }


def test_get_belief_calc_config_dict_ReturnsObj_CheckLevel1Keys():
    # ESTABLISH / WHEN
    belief_calc_config = get_belief_calc_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests
    for level1_key, aspect_dict in belief_calc_config.items():
        aspect_keys = set(aspect_dict.keys())
        print(f"{level1_key=} {aspect_keys=}")
        assert "abbreviation" in aspect_keys
        assert jkeys_str() in aspect_keys
        assert jvalues_str() in aspect_keys
        assert jmetrics_str() in aspect_keys
        assert len(aspect_keys) == 4


def test_get_belief_calc_config_dict_ReturnsObj_CheckLevel2_And_Level3_Keys():
    # ESTABLISH / WHEN
    belief_calc_config = get_belief_calc_config_dict()

    # THEN
    atom_config = get_atom_config_dict()
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, aspect_dict in belief_calc_config.items():
        if level1_key in atom_config.keys():
            atom_dimen = atom_config.get(level1_key)
            for level2_key, fm_aspect_dict in aspect_dict.items():
                if level2_key == jkeys_str():
                    atom_args = atom_dimen.get(jkeys_str())
                    dimen_keys = set(atom_args)
                    dimen_keys.add(moment_label_str())
                    dimen_keys.add(belief_name_str())
                    fm_aspect_keys = set(fm_aspect_dict.keys())
                    print(
                        f"{level1_key=} {level2_key=} {fm_aspect_keys=} {dimen_keys=}"
                    )
                    assert fm_aspect_keys == dimen_keys
                elif level2_key == jvalues_str():
                    atom_args = atom_dimen.get(jvalues_str())
                    dimen_keys = set(atom_args)
                    fm_aspect_keys = set(fm_aspect_dict.keys())
                    assert fm_aspect_keys == dimen_keys

    blrunit_aspect = belief_calc_config.get(beliefunit_str())
    blrpern_aspect = belief_calc_config.get(belief_voiceunit_str())
    blrmemb_aspect = belief_calc_config.get(belief_voice_membership_str())
    blrplan_aspect = belief_calc_config.get(belief_planunit_str())
    blrawar_aspect = belief_calc_config.get(belief_plan_awardunit_str())
    blrreas_aspect = belief_calc_config.get(belief_plan_reasonunit_str())
    blrprem_aspect = belief_calc_config.get(belief_plan_reason_caseunit_str())
    blrlabo_aspect = belief_calc_config.get(belief_plan_partyunit_str())
    blrheal_aspect = belief_calc_config.get(belief_plan_healerunit_str())
    blrfact_aspect = belief_calc_config.get(belief_plan_factunit_str())
    blrgrou_aspect = belief_calc_config.get(belief_groupunit_str())

    blrunit_jmetrics_keys = set(blrunit_aspect.get(jmetrics_str()))
    blrpern_jmetrics_keys = set(blrpern_aspect.get(jmetrics_str()))
    blrmemb_jmetrics_keys = set(blrmemb_aspect.get(jmetrics_str()))
    blrplan_jmetrics_keys = set(blrplan_aspect.get(jmetrics_str()))
    blrawar_jmetrics_keys = set(blrawar_aspect.get(jmetrics_str()))
    blrreas_jmetrics_keys = set(blrreas_aspect.get(jmetrics_str()))
    blrprem_jmetrics_keys = set(blrprem_aspect.get(jmetrics_str()))
    blrlabo_jmetrics_keys = set(blrlabo_aspect.get(jmetrics_str()))
    blrheal_jmetrics_keys = set(blrheal_aspect.get(jmetrics_str()))
    blrfact_jmetrics_keys = set(blrfact_aspect.get(jmetrics_str()))
    blrgrou_jmetrics_keys = set(blrgrou_aspect.get(jmetrics_str()))

    expected_blrunit_jmetrics_keys = {
        "tree_traverse_count",
        "rational",
        "keeps_justified",
        "keeps_buildable",
        "sum_healerunit_share",
        "offtrack_fund",
    }
    assert expected_blrunit_jmetrics_keys == blrunit_jmetrics_keys
    expected_blrpern_jmetrics_keys = {
        "credor_pool",
        "debtor_pool",
        "irrational_voice_debt_points",
        "inallocable_voice_debt_points",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_agenda_ratio_give",
        "fund_agenda_ratio_take",
    }
    assert expected_blrpern_jmetrics_keys == blrpern_jmetrics_keys
    expected_blrmemb_jmetrics_keys = {
        "credor_pool",
        "debtor_pool",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_agenda_ratio_give",
        "fund_agenda_ratio_take",
    }
    assert expected_blrmemb_jmetrics_keys == blrmemb_jmetrics_keys
    expected_blrplan_jmetrics_keys = {
        "active",
        "all_voice_cred",
        "all_voice_debt",
        "descendant_task_count",
        "fund_ratio",
        "fund_iota",
        "fund_onset",
        "fund_cease",
        "healerunit_ratio",
        "level",
        "range_evaluated",
        "chore",
        "gogo_calc",
        "stop_calc",
    }
    assert expected_blrplan_jmetrics_keys == blrplan_jmetrics_keys
    expected_blrawar_jmetrics_keys = {"fund_give", "fund_take"}
    assert expected_blrawar_jmetrics_keys == blrawar_jmetrics_keys
    expected_blrreas_jmetrics_keys = {
        "status",
        "chore",
        "_reason_active_heir",
    }
    assert expected_blrreas_jmetrics_keys == blrreas_jmetrics_keys
    expected_blrprem_jmetrics_keys = {"status", "chore"}
    assert expected_blrprem_jmetrics_keys == blrprem_jmetrics_keys
    expected_blrlabo_jmetrics_keys = {"_belief_name_is_labor"}
    assert expected_blrlabo_jmetrics_keys == blrlabo_jmetrics_keys
    expected_blrgrou_jmetrics_keys = {
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
        "credor_pool",
        "debtor_pool",
        "fund_iota",
    }
    assert expected_blrgrou_jmetrics_keys == blrgrou_jmetrics_keys

    assert blrunit_jmetrics_keys  # Non-empty
    assert blrpern_jmetrics_keys  # Non-empty
    assert blrmemb_jmetrics_keys  # Non-empty
    assert blrplan_jmetrics_keys  # Non-empty
    assert blrawar_jmetrics_keys  # Non-empty
    assert blrreas_jmetrics_keys  # Non-empty
    assert blrprem_jmetrics_keys  # Non-empty
    assert blrlabo_jmetrics_keys  # Non-empty
    assert not blrheal_jmetrics_keys  # empty
    assert not blrfact_jmetrics_keys  # empty
    assert blrgrou_jmetrics_keys  # Non-empty


def test_get_belief_calc_config_dict_ReturnsObj_CheckAbbreviations():
    # ESTABLISH / WHEN
    belief_calc_config = get_belief_calc_config_dict()

    # THEN
    blrunit_aspect = belief_calc_config.get(beliefunit_str())
    blrpern_aspect = belief_calc_config.get(belief_voiceunit_str())
    blrmemb_aspect = belief_calc_config.get(belief_voice_membership_str())
    blrplan_aspect = belief_calc_config.get(belief_planunit_str())
    blrawar_aspect = belief_calc_config.get(belief_plan_awardunit_str())
    blrreas_aspect = belief_calc_config.get(belief_plan_reasonunit_str())
    blrprem_aspect = belief_calc_config.get(belief_plan_reason_caseunit_str())
    blrlabo_aspect = belief_calc_config.get(belief_plan_partyunit_str())
    blrheal_aspect = belief_calc_config.get(belief_plan_healerunit_str())
    blrfact_aspect = belief_calc_config.get(belief_plan_factunit_str())
    blrgrou_aspect = belief_calc_config.get(belief_groupunit_str())
    abbr_str = "abbreviation"
    assert blrunit_aspect.get(abbr_str) == "blrunit"
    assert blrpern_aspect.get(abbr_str) == "blrpern"
    assert blrmemb_aspect.get(abbr_str) == "blrmemb"
    assert blrplan_aspect.get(abbr_str) == "blrplan"
    assert blrawar_aspect.get(abbr_str) == "blrawar"
    assert blrreas_aspect.get(abbr_str) == "blrreas"
    assert blrprem_aspect.get(abbr_str) == "blrprem"
    assert blrlabo_aspect.get(abbr_str) == "blrlabo"
    assert blrheal_aspect.get(abbr_str) == "blrheal"
    assert blrfact_aspect.get(abbr_str) == "blrfact"
    assert blrgrou_aspect.get(abbr_str) == "blrgrou"


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

    # belief_calc_config = get_belief_calc_config_dict()
    # belief_voiceunit_aspects = belief_calc_config.get("belief_voiceunit")
    # blrpern_jmetrics_dict = belief_voiceunit_aspects.get("jmetrics")
    # rope_belief_calc_aspects = blrpern_jmetrics_dict.get("fund_give")
    # assert belief_plan_factunit_str() in rope_belief_calc_aspects
    # assert belief_plan_partyunit_str() in rope_belief_calc_aspects
    # assert len(rope_belief_calc_aspects) == 6
    assert len(all_belief_calc_args) == 77


def test_get_belief_calc_config_dict_ReturnsObj_CheckArgDataTypesKeysExist():
    # ESTABLISH / WHEN
    belief_calc_config = get_belief_calc_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, aspect_dict in belief_calc_config.items():
        for level2_key, fm_aspect_dict in aspect_dict.items():
            if level2_key in {jkeys_str(), jvalues_str(), jmetrics_str()}:
                for level3_key, attr_dict in fm_aspect_dict.items():
                    print(
                        f"{level1_key=} {level2_key=} {level3_key=} {set(attr_dict.keys())=}"
                    )
                    assert set(attr_dict.keys()) == {
                        class_type_str(),
                        sqlite_datatype_str(),
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
    assert belief_calc_dimens == set(get_belief_calc_config_dict().keys())


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
        "fund_agenda_give",
        "credor_pool",
        "fund_give",
        voice_cred_points_str(),
        voice_name_str(),
        voice_debt_points_str(),
        "fund_agenda_ratio_take",
        "inallocable_voice_debt_points",
        "fund_agenda_ratio_give",
        "fund_agenda_take",
        "fund_take",
        "debtor_pool",
        "irrational_voice_debt_points",
    }
    assert belief_planunit_args == {
        moment_label_str(),
        belief_name_str(),
        morph_str(),
        denom_str(),
        "task",
        close_str(),
        addin_str(),
        numor_str(),
        "star",
        stop_want_str(),
        "gogo_calc",
        "stop_calc",
        "active",
        "fund_onset",
        "fund_cease",
        "descendant_task_count",
        "all_voice_cred",
        "all_voice_debt",
        "healerunit_ratio",
        "level",
        "chore",
        "fund_iota",
        "fund_ratio",
        "range_evaluated",
        "problem_bool",
        gogo_want_str(),
        plan_rope_str(),
        begin_str(),
    }
    assert belief_groupunit_args == {
        moment_label_str(),
        belief_name_str(),
        "debtor_pool",
        "credor_pool",
        "fund_give",
        "group_title",
        "knot",
        "fund_agenda_give",
        "fund_agenda_take",
        "fund_take",
        "fund_iota",
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


def test_get_belief_calc_config_dict_ReturnsObj_CheckArgDataTypesCorrect():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH / WHEN / THEN
    cfig = get_belief_calc_config_dict()
    # for level1_key, aspect_dict in config.items():
    #     for level2_key, fm_aspect_dict in aspect_dict.items():
    #         if level2_key in {jkeys_str(), jvalues_str(), jmetrics_str()}:
    #             for level3_key, attr_dict in fm_aspect_dict.items():
    #                 dimem = aspect_dict.get("abbreviation")
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
    jm = "jmetrics"
    beliefunit = beliefunit_str()
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
    assert g_class_type(cfig, blrmemb, jk, group_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, blrmemb, jk, group_title_str()) == "TEXT"
    assert g_class_type(cfig, blrmemb, jm, credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jm, credor_pool_str()) == "REAL"
    assert g_class_type(cfig, blrmemb, jm, debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jm, debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, blrmemb, jm, fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jm, fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, blrmemb, jm, fund_agenda_ratio_give_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jm, fund_agenda_ratio_give_str()) == "REAL"
    assert g_class_type(cfig, blrmemb, jm, fund_agenda_ratio_take_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jm, fund_agenda_ratio_take_str()) == "REAL"
    assert g_class_type(cfig, blrmemb, jm, fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jm, fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, blrmemb, jm, fund_give_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jm, fund_give_str()) == "REAL"
    assert g_class_type(cfig, blrmemb, jm, fund_take_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jm, fund_take_str()) == "REAL"
    assert g_class_type(cfig, blrmemb, jv, group_cred_points_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, group_cred_points_str()) == "REAL"
    assert g_class_type(cfig, blrmemb, jv, group_debt_points_str()) == "float"
    assert g_sqlitetype(cfig, blrmemb, jv, group_debt_points_str()) == "REAL"
    assert g_class_type(cfig, blrpern, jk, voice_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, blrpern, jk, voice_name_str()) == "TEXT"
    assert g_class_type(cfig, blrpern, jm, credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jm, credor_pool_str()) == "REAL"
    assert g_class_type(cfig, blrpern, jm, debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jm, debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, blrpern, jm, fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jm, fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, blrpern, jm, fund_agenda_ratio_give_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jm, fund_agenda_ratio_give_str()) == "REAL"
    assert g_class_type(cfig, blrpern, jm, fund_agenda_ratio_take_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jm, fund_agenda_ratio_take_str()) == "REAL"
    assert g_class_type(cfig, blrpern, jm, fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jm, fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, blrpern, jm, fund_give_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jm, fund_give_str()) == "REAL"
    assert g_class_type(cfig, blrpern, jm, fund_take_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jm, fund_take_str()) == "REAL"
    assert (
        g_class_type(cfig, blrpern, jm, inallocable_voice_debt_points_str()) == "float"
    )
    assert (
        g_sqlitetype(cfig, blrpern, jm, inallocable_voice_debt_points_str()) == "REAL"
    )
    assert (
        g_class_type(cfig, blrpern, jm, irrational_voice_debt_points_str()) == "float"
    )
    assert g_sqlitetype(cfig, blrpern, jm, irrational_voice_debt_points_str()) == "REAL"
    assert g_class_type(cfig, blrpern, jv, voice_cred_points_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, voice_cred_points_str()) == "REAL"
    assert g_class_type(cfig, blrpern, jv, voice_debt_points_str()) == "float"
    assert g_sqlitetype(cfig, blrpern, jv, voice_debt_points_str()) == "REAL"

    assert g_class_type(cfig, blrgrou, jk, group_title_str()) == "TitleTerm"
    assert g_sqlitetype(cfig, blrgrou, jk, group_title_str()) == "TEXT"
    assert g_class_type(cfig, blrgrou, jv, knot_str()) == "str"
    assert g_sqlitetype(cfig, blrgrou, jv, knot_str()) == "TEXT"
    assert g_class_type(cfig, blrgrou, jm, debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jm, debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, blrgrou, jm, credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jm, credor_pool_str()) == "REAL"
    assert g_class_type(cfig, blrgrou, jm, fund_give_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jm, fund_give_str()) == "REAL"
    assert g_class_type(cfig, blrgrou, jm, fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jm, fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, blrgrou, jm, fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jm, fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, blrgrou, jm, fund_take_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jm, fund_take_str()) == "REAL"
    assert g_class_type(cfig, blrgrou, jm, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, blrgrou, jm, fund_iota_str()) == "REAL"

    assert g_class_type(cfig, blrawar, jk, awardee_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, blrawar, jk, awardee_title_str()) == "TEXT"
    assert g_class_type(cfig, blrawar, jk, plan_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, blrawar, jk, plan_rope_str()) == "TEXT"
    assert g_class_type(cfig, blrawar, jm, fund_give_str()) == "float"
    assert g_sqlitetype(cfig, blrawar, jm, fund_give_str()) == "REAL"
    assert g_class_type(cfig, blrawar, jm, fund_take_str()) == "float"
    assert g_sqlitetype(cfig, blrawar, jm, fund_take_str()) == "REAL"
    assert g_class_type(cfig, blrawar, jv, give_force_str()) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, give_force_str()) == "REAL"
    assert g_class_type(cfig, blrawar, jv, take_force_str()) == "float"
    assert g_sqlitetype(cfig, blrawar, jv, take_force_str()) == "REAL"
    assert g_class_type(cfig, blrfact, jk, fact_context_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, blrfact, jk, fact_context_str()) == "TEXT"
    assert g_class_type(cfig, blrfact, jk, plan_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, blrfact, jk, plan_rope_str()) == "TEXT"
    assert g_class_type(cfig, blrfact, jv, fact_upper_str()) == "float"
    assert g_sqlitetype(cfig, blrfact, jv, fact_upper_str()) == "REAL"
    assert g_class_type(cfig, blrfact, jv, fact_lower_str()) == "float"
    assert g_sqlitetype(cfig, blrfact, jv, fact_lower_str()) == "REAL"
    assert g_class_type(cfig, blrfact, jv, fact_state_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, blrfact, jv, fact_state_str()) == "TEXT"
    assert g_class_type(cfig, blrheal, jk, healer_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, blrheal, jk, healer_name_str()) == "TEXT"
    assert g_class_type(cfig, blrheal, jk, plan_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, blrheal, jk, plan_rope_str()) == "TEXT"
    assert g_class_type(cfig, blrprem, jk, reason_context_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, blrprem, jk, reason_context_str()) == "TEXT"
    assert g_class_type(cfig, blrprem, jk, reason_state_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, blrprem, jk, reason_state_str()) == "TEXT"
    assert g_class_type(cfig, blrprem, jk, plan_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, blrprem, jk, plan_rope_str()) == "TEXT"
    assert g_class_type(cfig, blrprem, jm, status_str()) == "int"
    assert g_sqlitetype(cfig, blrprem, jm, status_str()) == "INTEGER"
    assert g_class_type(cfig, blrprem, jm, chore_str()) == "int"
    assert g_sqlitetype(cfig, blrprem, jm, chore_str()) == "INTEGER"
    assert g_class_type(cfig, blrprem, jv, reason_divisor_str()) == "int"
    assert g_sqlitetype(cfig, blrprem, jv, reason_divisor_str()) == "INTEGER"
    assert g_class_type(cfig, blrprem, jv, reason_upper_str()) == "float"
    assert g_sqlitetype(cfig, blrprem, jv, reason_upper_str()) == "REAL"
    assert g_class_type(cfig, blrprem, jv, reason_lower_str()) == "float"
    assert g_sqlitetype(cfig, blrprem, jv, reason_lower_str()) == "REAL"
    assert g_class_type(cfig, blrreas, jk, reason_context_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, blrreas, jk, reason_context_str()) == "TEXT"
    assert g_class_type(cfig, blrreas, jk, plan_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, blrreas, jk, plan_rope_str()) == "TEXT"
    assert g_class_type(cfig, blrreas, jm, "_reason_active_heir") == "int"
    assert g_sqlitetype(cfig, blrreas, jm, "_reason_active_heir") == "INTEGER"
    assert g_class_type(cfig, blrreas, jm, status_str()) == "int"
    assert g_sqlitetype(cfig, blrreas, jm, status_str()) == "INTEGER"
    assert g_class_type(cfig, blrreas, jm, chore_str()) == "int"
    assert g_sqlitetype(cfig, blrreas, jm, chore_str()) == "INTEGER"
    assert g_class_type(cfig, blrreas, jv, reason_active_requisite_str()) == "bool"
    assert g_sqlitetype(cfig, blrreas, jv, reason_active_requisite_str()) == "INTEGER"
    assert g_class_type(cfig, blrlabo, jk, plan_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, blrlabo, jk, plan_rope_str()) == "TEXT"
    assert g_class_type(cfig, blrlabo, jk, party_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, blrlabo, jk, party_title_str()) == "TEXT"
    assert g_class_type(cfig, blrlabo, jm, "_belief_name_is_labor") == "int"
    assert g_sqlitetype(cfig, blrlabo, jm, "_belief_name_is_labor") == "INTEGER"
    assert g_class_type(cfig, blrplan, jm, "active") == "int"
    assert g_sqlitetype(cfig, blrplan, jm, "active") == "INTEGER"
    assert g_class_type(cfig, blrplan, jm, all_voice_cred_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jm, all_voice_cred_str()) == "INTEGER"
    assert g_class_type(cfig, blrplan, jm, all_voice_debt_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jm, all_voice_debt_str()) == "INTEGER"
    assert g_class_type(cfig, blrplan, jm, descendant_task_count_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jm, descendant_task_count_str()) == "INTEGER"
    assert g_class_type(cfig, blrplan, jm, fund_cease_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jm, fund_cease_str()) == "REAL"
    assert g_class_type(cfig, blrplan, jm, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jm, fund_iota_str()) == "REAL"
    assert g_class_type(cfig, blrplan, jm, fund_onset_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jm, fund_onset_str()) == "REAL"
    assert g_class_type(cfig, blrplan, jm, fund_ratio_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jm, fund_ratio_str()) == "REAL"
    assert g_class_type(cfig, blrplan, jm, gogo_calc_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jm, gogo_calc_str()) == "REAL"
    assert g_class_type(cfig, blrplan, jm, healerunit_ratio_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jm, healerunit_ratio_str()) == "REAL"
    assert g_class_type(cfig, blrplan, jm, "level") == "int"
    assert g_sqlitetype(cfig, blrplan, jm, "level") == "INTEGER"
    assert g_class_type(cfig, blrplan, jm, range_evaluated_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jm, range_evaluated_str()) == "INTEGER"
    assert g_class_type(cfig, blrplan, jm, stop_calc_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jm, stop_calc_str()) == "REAL"
    assert g_class_type(cfig, blrplan, jm, chore_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jm, chore_str()) == "INTEGER"
    assert g_class_type(cfig, blrplan, jv, addin_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, addin_str()) == "REAL"
    assert g_class_type(cfig, blrplan, jv, begin_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, begin_str()) == "REAL"
    assert g_class_type(cfig, blrplan, jv, close_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, close_str()) == "REAL"
    assert g_class_type(cfig, blrplan, jv, denom_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, denom_str()) == "INTEGER"
    assert g_class_type(cfig, blrplan, jv, gogo_want_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, gogo_want_str()) == "REAL"
    assert g_class_type(cfig, blrplan, jv, star_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, star_str()) == "INTEGER"
    assert g_class_type(cfig, blrplan, jv, morph_str()) == "bool"
    assert g_sqlitetype(cfig, blrplan, jv, morph_str()) == "INTEGER"
    assert g_class_type(cfig, blrplan, jv, numor_str()) == "int"
    assert g_sqlitetype(cfig, blrplan, jv, numor_str()) == "INTEGER"
    assert g_class_type(cfig, blrplan, jv, task_str()) == "bool"
    assert g_sqlitetype(cfig, blrplan, jv, task_str()) == "INTEGER"
    assert g_class_type(cfig, blrplan, jv, problem_bool_str()) == "bool"
    assert g_sqlitetype(cfig, blrplan, jv, problem_bool_str()) == "INTEGER"
    assert g_class_type(cfig, blrplan, jv, stop_want_str()) == "float"
    assert g_sqlitetype(cfig, blrplan, jv, stop_want_str()) == "REAL"
    assert g_class_type(cfig, beliefunit, jm, "keeps_buildable") == "int"
    assert g_sqlitetype(cfig, beliefunit, jm, "keeps_buildable") == "INTEGER"
    assert g_class_type(cfig, beliefunit, jm, "keeps_justified") == "int"
    assert g_sqlitetype(cfig, beliefunit, jm, "keeps_justified") == "INTEGER"
    assert g_class_type(cfig, beliefunit, jm, offtrack_fund_str()) == "float"
    assert g_sqlitetype(cfig, beliefunit, jm, offtrack_fund_str()) == "REAL"
    assert g_class_type(cfig, beliefunit, jm, rational_str()) == "bool"
    assert g_sqlitetype(cfig, beliefunit, jm, rational_str()) == "INTEGER"
    assert g_class_type(cfig, beliefunit, jm, sum_healerunit_share_str()) == "float"
    assert g_sqlitetype(cfig, beliefunit, jm, sum_healerunit_share_str()) == "REAL"
    assert g_class_type(cfig, beliefunit, jm, tree_traverse_count_str()) == "int"
    assert g_sqlitetype(cfig, beliefunit, jm, tree_traverse_count_str()) == "INTEGER"
    assert g_class_type(cfig, beliefunit, jv, credor_respect_str()) == "float"
    assert g_sqlitetype(cfig, beliefunit, jv, credor_respect_str()) == "REAL"
    assert g_class_type(cfig, beliefunit, jv, debtor_respect_str()) == "float"
    assert g_sqlitetype(cfig, beliefunit, jv, debtor_respect_str()) == "REAL"
    assert g_class_type(cfig, beliefunit, jv, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, beliefunit, jv, fund_iota_str()) == "REAL"
    assert g_class_type(cfig, beliefunit, jv, fund_pool_str()) == "float"
    assert g_sqlitetype(cfig, beliefunit, jv, fund_pool_str()) == "REAL"
    assert g_class_type(cfig, beliefunit, jv, max_tree_traverse_str()) == "int"
    assert g_sqlitetype(cfig, beliefunit, jv, max_tree_traverse_str()) == "INTEGER"
    assert g_class_type(cfig, beliefunit, jv, penny_str()) == "float"
    assert g_sqlitetype(cfig, beliefunit, jv, penny_str()) == "REAL"
    assert g_class_type(cfig, beliefunit, jv, respect_bit_str()) == "float"
    assert g_sqlitetype(cfig, beliefunit, jv, respect_bit_str()) == "REAL"
    assert g_class_type(cfig, beliefunit, jv, tally_str()) == "int"
    assert g_sqlitetype(cfig, beliefunit, jv, tally_str()) == "INTEGER"


def test_get_belief_calc_config_dict_ReturnsObj_EachArgHasOneClassType():
    # ESTABLISH
    belief_calc_config_dict = get_belief_calc_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for belief_calc_dimen, dimen_dict in belief_calc_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues", "jmetrics"}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(class_type_str())
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN / THEN
    for x_arg, arg_types in all_args.items():
        print(f"{x_arg=} {arg_types=}")
        assert len(arg_types) == 1


def test_get_belief_calc_config_dict_ReturnsObj_EachArgHasOne_sqlite_datatype():
    # ESTABLISH
    belief_calc_config_dict = get_belief_calc_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for belief_calc_dimen, dimen_dict in belief_calc_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues", "jmetrics"}:
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
    belief_calc_config_dict = get_belief_calc_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for belief_calc_dimen, dimen_dict in belief_calc_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues", "jmetrics"}:
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
    assert belief_calc_args_type_dict.get(plan_rope_str()) == RopeTerm_str()
    assert belief_calc_args_type_dict.get(give_force_str()) == "float"
    assert belief_calc_args_type_dict.get(take_force_str()) == "float"
    assert belief_calc_args_type_dict.get(reason_context_str()) == RopeTerm_str()
    assert belief_calc_args_type_dict.get(fact_upper_str()) == "float"
    assert belief_calc_args_type_dict.get(fact_lower_str()) == "float"
    assert belief_calc_args_type_dict.get(fact_state_str()) == RopeTerm_str()
    assert belief_calc_args_type_dict.get(healer_name_str()) == NameTerm_str()
    assert belief_calc_args_type_dict.get(reason_state_str()) == RopeTerm_str()
    assert belief_calc_args_type_dict.get("status") == "int"
    assert belief_calc_args_type_dict.get("chore") == "int"
    assert belief_calc_args_type_dict.get(reason_divisor_str()) == "int"
    assert belief_calc_args_type_dict.get(reason_upper_str()) == "float"
    assert belief_calc_args_type_dict.get(reason_lower_str()) == "float"
    assert belief_calc_args_type_dict.get("_reason_active_heir") == "int"
    assert belief_calc_args_type_dict.get("reason_active_requisite") == "bool"
    assert belief_calc_args_type_dict.get(party_title_str()) == TitleTerm_str()
    assert belief_calc_args_type_dict.get("_belief_name_is_labor") == "int"
    assert belief_calc_args_type_dict.get("active") == "int"
    assert belief_calc_args_type_dict.get(all_voice_cred_str()) == "int"
    assert belief_calc_args_type_dict.get(all_voice_debt_str()) == "int"
    assert belief_calc_args_type_dict.get(descendant_task_count_str()) == "int"
    assert belief_calc_args_type_dict.get(fund_cease_str()) == "float"
    assert belief_calc_args_type_dict.get(fund_onset_str()) == "float"
    assert belief_calc_args_type_dict.get(fund_ratio_str()) == "float"
    assert belief_calc_args_type_dict.get(gogo_calc_str()) == "float"
    assert belief_calc_args_type_dict.get("healerunit_ratio") == "float"
    assert belief_calc_args_type_dict.get("level") == "int"
    assert belief_calc_args_type_dict.get(range_evaluated_str()) == "int"
    assert belief_calc_args_type_dict.get(stop_calc_str()) == "float"
    assert belief_calc_args_type_dict.get("keeps_buildable") == "int"
    assert belief_calc_args_type_dict.get("keeps_justified") == "int"
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
