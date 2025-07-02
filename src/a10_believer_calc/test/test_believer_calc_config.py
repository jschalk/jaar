# from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd
from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.test._util.a01_str import knot_str
from src.a03_group_logic.test._util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    _inallocable_acct_debt_points_str,
    _irrational_acct_debt_points_str,
    acct_cred_points_str,
    acct_debt_points_str,
    awardee_title_str,
    fund_give_str,
    fund_take_str,
    give_force_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    respect_bit_str,
    take_force_str,
)
from src.a04_reason_logic.test._util.a04_str import (
    _chore_str,
    _status_str,
    belief_label_str,
    believer_name_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    fstate_str,
    labor_title_str,
    pdivisor_str,
    pnigh_str,
    popen_str,
    pstate_str,
    rcontext_str,
    rplan_active_requisite_str,
)
from src.a05_plan_logic.test._util.a05_str import (
    _all_acct_cred_str,
    _all_acct_debt_str,
    _descendant_task_count_str,
    _fund_cease_str,
    _fund_onset_str,
    _fund_ratio_str,
    _gogo_calc_str,
    _healerlink_ratio_str,
    _range_evaluated_str,
    _stop_calc_str,
    mass_str,
    problem_bool_str,
    task_str,
)
from src.a06_believer_logic.test._util.a06_str import (
    LabelTerm_str,
    NameTerm_str,
    RopeTerm_str,
    TitleTerm_str,
    _offtrack_fund_str,
    _rational_str,
    _sum_healerlink_share_str,
    _tree_traverse_count_str,
    acct_cred_points_str,
    acct_debt_points_str,
    acct_name_str,
    addin_str,
    awardee_title_str,
    begin_str,
    believer_acct_membership_str,
    believer_acctunit_str,
    believer_plan_awardlink_str,
    believer_plan_factunit_str,
    believer_plan_healerlink_str,
    believer_plan_laborlink_str,
    believer_plan_reason_premiseunit_str,
    believer_plan_reasonunit_str,
    believer_planunit_str,
    believerunit_str,
    close_str,
    credor_respect_str,
    debtor_respect_str,
    denom_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    fstate_str,
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
    penny_str,
    plan_rope_str,
    pnigh_str,
    popen_str,
    pstate_str,
    rcontext_str,
    stop_want_str,
    tally_str,
)
from src.a08_believer_atom_logic.atom_config import get_atom_config_dict
from src.a08_believer_atom_logic.test._util.a08_str import (
    class_type_str,
    jkeys_str,
    jvalues_str,
    sqlite_datatype_str,
)
from src.a10_believer_calc.believer_calc_config import (
    config_believer_calc_file_path,
    get_all_believer_calc_args,
    get_believer_calc_args_sqlite_datatype_dict,
    get_believer_calc_args_type_dict,
    get_believer_calc_config_dict,
    get_believer_calc_config_filename,
    get_believer_calc_dimen_args,
    get_believer_calc_dimens,
)
from src.a10_believer_calc.test._util.a10_str import (
    believer_groupunit_str,
    jmetrics_str,
)


def test_get_believer_calc_config_dict_Exists():
    # ESTABLISH
    src_dir = create_path(os_getcwd(), "src")
    expected_dir = create_path(src_dir, "a10_believer_calc")

    # WHEN / THEN
    assert get_believer_calc_config_filename() == "believer_calc_config.json"
    expected_path = create_path(expected_dir, get_believer_calc_config_filename())
    assert config_believer_calc_file_path() == expected_path
    assert os_path_exists(config_believer_calc_file_path())


def test_get_believer_calc_config_dict_ReturnsObj_CheckLevel0Keys():
    # ESTABLISH / WHEN
    believer_calc_config = get_believer_calc_config_dict()
    believer_calc_config_keys = set(believer_calc_config.keys())

    # THEN
    assert believerunit_str() in believer_calc_config_keys
    assert believer_acctunit_str() in believer_calc_config_keys
    assert believer_acct_membership_str() in believer_calc_config_keys
    assert believer_planunit_str() in believer_calc_config_keys
    assert believer_plan_awardlink_str() in believer_calc_config_keys
    assert believer_plan_reasonunit_str() in believer_calc_config_keys
    assert believer_plan_reason_premiseunit_str() in believer_calc_config_keys
    assert believer_plan_laborlink_str() in believer_calc_config_keys
    assert believer_plan_healerlink_str() in believer_calc_config_keys
    assert believer_plan_factunit_str() in believer_calc_config_keys
    assert believer_groupunit_str() in believer_calc_config_keys
    assert len(get_believer_calc_config_dict()) == 11
    atom_config_dict = get_atom_config_dict()
    atom_config_dimens = set(atom_config_dict.keys())
    assert atom_config_dimens.issubset(believer_calc_config_keys)
    assert believer_calc_config_keys.difference(atom_config_dimens) == {
        believer_groupunit_str()
    }


def test_get_believer_calc_config_dict_ReturnsObj_CheckLevel1Keys():
    # ESTABLISH / WHEN
    believer_calc_config = get_believer_calc_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests
    for level1_key, aspect_dict in believer_calc_config.items():
        aspect_keys = set(aspect_dict.keys())
        print(f"{level1_key=} {aspect_keys=}")
        assert "abbreviation" in aspect_keys
        assert jkeys_str() in aspect_keys
        assert jvalues_str() in aspect_keys
        assert jmetrics_str() in aspect_keys
        assert len(aspect_keys) == 4


def test_get_believer_calc_config_dict_ReturnsObj_CheckLevel2_And_Level3_Keys():
    # ESTABLISH / WHEN
    believer_calc_config = get_believer_calc_config_dict()

    # THEN
    atom_config = get_atom_config_dict()
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, aspect_dict in believer_calc_config.items():
        if level1_key in atom_config.keys():
            atom_dimen = atom_config.get(level1_key)
            for level2_key, fm_aspect_dict in aspect_dict.items():
                if level2_key == jkeys_str():
                    atom_args = atom_dimen.get(jkeys_str())
                    dimen_keys = set(atom_args)
                    dimen_keys.add(belief_label_str())
                    dimen_keys.add(believer_name_str())
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

    onrunit_aspect = believer_calc_config.get(believerunit_str())
    onracct_aspect = believer_calc_config.get(believer_acctunit_str())
    onrmemb_aspect = believer_calc_config.get(believer_acct_membership_str())
    onrplan_aspect = believer_calc_config.get(believer_planunit_str())
    onrawar_aspect = believer_calc_config.get(believer_plan_awardlink_str())
    onrreas_aspect = believer_calc_config.get(believer_plan_reasonunit_str())
    onrprem_aspect = believer_calc_config.get(believer_plan_reason_premiseunit_str())
    onrlabo_aspect = believer_calc_config.get(believer_plan_laborlink_str())
    onrheal_aspect = believer_calc_config.get(believer_plan_healerlink_str())
    onrfact_aspect = believer_calc_config.get(believer_plan_factunit_str())
    onrgrou_aspect = believer_calc_config.get(believer_groupunit_str())

    onrunit_jmetrics_keys = set(onrunit_aspect.get(jmetrics_str()))
    onracct_jmetrics_keys = set(onracct_aspect.get(jmetrics_str()))
    onrmemb_jmetrics_keys = set(onrmemb_aspect.get(jmetrics_str()))
    onrplan_jmetrics_keys = set(onrplan_aspect.get(jmetrics_str()))
    onrawar_jmetrics_keys = set(onrawar_aspect.get(jmetrics_str()))
    onrreas_jmetrics_keys = set(onrreas_aspect.get(jmetrics_str()))
    onrprem_jmetrics_keys = set(onrprem_aspect.get(jmetrics_str()))
    onrlabo_jmetrics_keys = set(onrlabo_aspect.get(jmetrics_str()))
    onrheal_jmetrics_keys = set(onrheal_aspect.get(jmetrics_str()))
    onrfact_jmetrics_keys = set(onrfact_aspect.get(jmetrics_str()))
    onrgrou_jmetrics_keys = set(onrgrou_aspect.get(jmetrics_str()))

    expected_onrunit_jmetrics_keys = {
        "_tree_traverse_count",
        "_rational",
        "_keeps_justified",
        "_keeps_buildable",
        "_sum_healerlink_share",
        "_offtrack_fund",
    }
    assert expected_onrunit_jmetrics_keys == onrunit_jmetrics_keys
    expected_onracct_jmetrics_keys = {
        "_credor_pool",
        "_debtor_pool",
        "_irrational_acct_debt_points",
        "_inallocable_acct_debt_points",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    assert expected_onracct_jmetrics_keys == onracct_jmetrics_keys
    expected_onrmemb_jmetrics_keys = {
        "_credor_pool",
        "_debtor_pool",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    assert expected_onrmemb_jmetrics_keys == onrmemb_jmetrics_keys
    expected_onrplan_jmetrics_keys = {
        "_active",
        "_all_acct_cred",
        "_all_acct_debt",
        "_descendant_task_count",
        "_fund_ratio",
        "fund_iota",
        "_fund_onset",
        "_fund_cease",
        "_healerlink_ratio",
        "_level",
        "_range_evaluated",
        "_chore",
        "_gogo_calc",
        "_stop_calc",
    }
    assert expected_onrplan_jmetrics_keys == onrplan_jmetrics_keys
    expected_onrawar_jmetrics_keys = {"_fund_give", "_fund_take"}
    assert expected_onrawar_jmetrics_keys == onrawar_jmetrics_keys
    expected_onrreas_jmetrics_keys = {
        "_status",
        "_chore",
        "_rplan_active_value",
    }
    assert expected_onrreas_jmetrics_keys == onrreas_jmetrics_keys
    expected_onrprem_jmetrics_keys = {"_status", "_chore"}
    assert expected_onrprem_jmetrics_keys == onrprem_jmetrics_keys
    expected_onrlabo_jmetrics_keys = {"_believer_name_labor"}
    assert expected_onrlabo_jmetrics_keys == onrlabo_jmetrics_keys
    expected_onrgrou_jmetrics_keys = {
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_credor_pool",
        "_debtor_pool",
        "fund_iota",
    }
    assert expected_onrgrou_jmetrics_keys == onrgrou_jmetrics_keys

    assert onrunit_jmetrics_keys  # Non-empty
    assert onracct_jmetrics_keys  # Non-empty
    assert onrmemb_jmetrics_keys  # Non-empty
    assert onrplan_jmetrics_keys  # Non-empty
    assert onrawar_jmetrics_keys  # Non-empty
    assert onrreas_jmetrics_keys  # Non-empty
    assert onrprem_jmetrics_keys  # Non-empty
    assert onrlabo_jmetrics_keys  # Non-empty
    assert not onrheal_jmetrics_keys  # empty
    assert not onrfact_jmetrics_keys  # empty
    assert onrgrou_jmetrics_keys  # Non-empty


def test_get_believer_calc_config_dict_ReturnsObj_CheckAbbreviations():
    # ESTABLISH / WHEN
    believer_calc_config = get_believer_calc_config_dict()

    # THEN
    onrunit_aspect = believer_calc_config.get(believerunit_str())
    onracct_aspect = believer_calc_config.get(believer_acctunit_str())
    onrmemb_aspect = believer_calc_config.get(believer_acct_membership_str())
    onrplan_aspect = believer_calc_config.get(believer_planunit_str())
    onrawar_aspect = believer_calc_config.get(believer_plan_awardlink_str())
    onrreas_aspect = believer_calc_config.get(believer_plan_reasonunit_str())
    onrprem_aspect = believer_calc_config.get(believer_plan_reason_premiseunit_str())
    onrlabo_aspect = believer_calc_config.get(believer_plan_laborlink_str())
    onrheal_aspect = believer_calc_config.get(believer_plan_healerlink_str())
    onrfact_aspect = believer_calc_config.get(believer_plan_factunit_str())
    onrgrou_aspect = believer_calc_config.get(believer_groupunit_str())
    abbr_str = "abbreviation"
    assert onrunit_aspect.get(abbr_str) == "onrunit"
    assert onracct_aspect.get(abbr_str) == "onracct"
    assert onrmemb_aspect.get(abbr_str) == "onrmemb"
    assert onrplan_aspect.get(abbr_str) == "onrplan"
    assert onrawar_aspect.get(abbr_str) == "onrawar"
    assert onrreas_aspect.get(abbr_str) == "onrreas"
    assert onrprem_aspect.get(abbr_str) == "onrprem"
    assert onrlabo_aspect.get(abbr_str) == "onrlabo"
    assert onrheal_aspect.get(abbr_str) == "onrheal"
    assert onrfact_aspect.get(abbr_str) == "onrfact"
    assert onrgrou_aspect.get(abbr_str) == "onrgrou"


def test_get_all_believer_calc_args_ReturnsObj():
    # ESTABLISH / WHEN
    all_believer_calc_args = get_all_believer_calc_args()

    # THEN
    assert all_believer_calc_args
    assert stop_want_str() in all_believer_calc_args
    assert plan_rope_str() in all_believer_calc_args
    assert "_fund_give" in all_believer_calc_args
    assert all_believer_calc_args.get("_fund_give") == {
        "believer_plan_awardlink",
        "believer_acct_membership",
        "believer_groupunit",
        "believer_acctunit",
    }

    # believer_calc_config = get_believer_calc_config_dict()
    # believer_acctunit_aspects = believer_calc_config.get("believer_acctunit")
    # onracct_jmetrics_dict = believer_acctunit_aspects.get("jmetrics")
    # rope_believer_calc_aspects = onracct_jmetrics_dict.get("_fund_give")
    # assert believer_plan_factunit_str() in rope_believer_calc_aspects
    # assert believer_plan_laborlink_str() in rope_believer_calc_aspects
    # assert len(rope_believer_calc_aspects) == 6
    assert len(all_believer_calc_args) == 76


def test_get_believer_calc_config_dict_ReturnsObj_CheckArgDataTypesKeysExist():
    # ESTABLISH / WHEN
    believer_calc_config = get_believer_calc_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, aspect_dict in believer_calc_config.items():
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


def test_get_believer_calc_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    believer_calc_dimens = get_believer_calc_dimens()

    # THEN
    expected_believer_calc_dimens = {
        believerunit_str(),
        believer_acctunit_str(),
        believer_acct_membership_str(),
        believer_planunit_str(),
        believer_plan_awardlink_str(),
        believer_plan_reasonunit_str(),
        believer_plan_reason_premiseunit_str(),
        believer_plan_laborlink_str(),
        believer_plan_healerlink_str(),
        believer_plan_factunit_str(),
        believer_groupunit_str(),
    }
    assert believer_calc_dimens == expected_believer_calc_dimens
    assert believer_calc_dimens == set(get_believer_calc_config_dict().keys())


def test_get_believer_calc_dimen_args_ReturnsObj():
    # ESTABLISH / WHEN
    believer_acctunit_args = get_believer_calc_dimen_args(believer_acctunit_str())
    believer_planunit_args = get_believer_calc_dimen_args(believer_planunit_str())
    believer_groupunit_args = get_believer_calc_dimen_args(believer_groupunit_str())

    #  THEN
    print(f"{believer_acctunit_args=}")
    print(f"{believer_groupunit_args=}")
    assert believer_acctunit_args == {
        belief_label_str(),
        believer_name_str(),
        "_fund_agenda_give",
        "_credor_pool",
        "_fund_give",
        acct_cred_points_str(),
        acct_name_str(),
        acct_debt_points_str(),
        "_fund_agenda_ratio_take",
        "_inallocable_acct_debt_points",
        "_fund_agenda_ratio_give",
        "_fund_agenda_take",
        "_fund_take",
        "_debtor_pool",
        "_irrational_acct_debt_points",
    }
    assert believer_planunit_args == {
        belief_label_str(),
        believer_name_str(),
        morph_str(),
        denom_str(),
        "task",
        close_str(),
        addin_str(),
        numor_str(),
        "mass",
        stop_want_str(),
        "_gogo_calc",
        "_stop_calc",
        "_active",
        "_fund_onset",
        "_fund_cease",
        "_descendant_task_count",
        "_all_acct_cred",
        "_all_acct_debt",
        "_healerlink_ratio",
        "_level",
        "_chore",
        "fund_iota",
        "_fund_ratio",
        "_range_evaluated",
        "problem_bool",
        gogo_want_str(),
        plan_rope_str(),
        begin_str(),
    }
    assert believer_groupunit_args == {
        belief_label_str(),
        believer_name_str(),
        "_debtor_pool",
        "_credor_pool",
        "_fund_give",
        "group_title",
        "knot",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_take",
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


def test_get_believer_calc_config_dict_ReturnsObj_CheckArgDataTypesCorrect():
    # ESTABLISH / WHEN
    cfig = get_believer_calc_config_dict()
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
    believerunit = believerunit_str()
    onracct = believer_acctunit_str()
    onrmemb = believer_acct_membership_str()
    onrplan = believer_planunit_str()
    onrawar = believer_plan_awardlink_str()
    onrreas = believer_plan_reasonunit_str()
    onrprem = believer_plan_reason_premiseunit_str()
    onrlabo = believer_plan_laborlink_str()
    onrheal = believer_plan_healerlink_str()
    onrfact = believer_plan_factunit_str()
    onrgrou = believer_groupunit_str()
    assert g_class_type(cfig, onrmemb, jk, acct_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, onrmemb, jk, acct_name_str()) == "TEXT"
    assert g_class_type(cfig, onrmemb, jk, group_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, onrmemb, jk, group_title_str()) == "TEXT"
    assert g_class_type(cfig, onrmemb, jm, _credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, onrmemb, jm, _credor_pool_str()) == "REAL"
    assert g_class_type(cfig, onrmemb, jm, _debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, onrmemb, jm, _debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, onrmemb, jm, _fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, onrmemb, jm, _fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, onrmemb, jm, _fund_agenda_ratio_give_str()) == "float"
    assert g_sqlitetype(cfig, onrmemb, jm, _fund_agenda_ratio_give_str()) == "REAL"
    assert g_class_type(cfig, onrmemb, jm, _fund_agenda_ratio_take_str()) == "float"
    assert g_sqlitetype(cfig, onrmemb, jm, _fund_agenda_ratio_take_str()) == "REAL"
    assert g_class_type(cfig, onrmemb, jm, _fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, onrmemb, jm, _fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, onrmemb, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, onrmemb, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, onrmemb, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, onrmemb, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, onrmemb, jv, group_cred_points_str()) == "float"
    assert g_sqlitetype(cfig, onrmemb, jv, group_cred_points_str()) == "REAL"
    assert g_class_type(cfig, onrmemb, jv, group_debt_points_str()) == "float"
    assert g_sqlitetype(cfig, onrmemb, jv, group_debt_points_str()) == "REAL"
    assert g_class_type(cfig, onracct, jk, acct_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, onracct, jk, acct_name_str()) == "TEXT"
    assert g_class_type(cfig, onracct, jm, _credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, onracct, jm, _credor_pool_str()) == "REAL"
    assert g_class_type(cfig, onracct, jm, _debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, onracct, jm, _debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, onracct, jm, _fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, onracct, jm, _fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, onracct, jm, _fund_agenda_ratio_give_str()) == "float"
    assert g_sqlitetype(cfig, onracct, jm, _fund_agenda_ratio_give_str()) == "REAL"
    assert g_class_type(cfig, onracct, jm, _fund_agenda_ratio_take_str()) == "float"
    assert g_sqlitetype(cfig, onracct, jm, _fund_agenda_ratio_take_str()) == "REAL"
    assert g_class_type(cfig, onracct, jm, _fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, onracct, jm, _fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, onracct, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, onracct, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, onracct, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, onracct, jm, _fund_take_str()) == "REAL"
    assert (
        g_class_type(cfig, onracct, jm, _inallocable_acct_debt_points_str()) == "float"
    )
    assert (
        g_sqlitetype(cfig, onracct, jm, _inallocable_acct_debt_points_str()) == "REAL"
    )
    assert (
        g_class_type(cfig, onracct, jm, _irrational_acct_debt_points_str()) == "float"
    )
    assert g_sqlitetype(cfig, onracct, jm, _irrational_acct_debt_points_str()) == "REAL"
    assert g_class_type(cfig, onracct, jv, acct_cred_points_str()) == "float"
    assert g_sqlitetype(cfig, onracct, jv, acct_cred_points_str()) == "REAL"
    assert g_class_type(cfig, onracct, jv, acct_debt_points_str()) == "float"
    assert g_sqlitetype(cfig, onracct, jv, acct_debt_points_str()) == "REAL"

    assert g_class_type(cfig, onrgrou, jk, group_title_str()) == "TitleTerm"
    assert g_sqlitetype(cfig, onrgrou, jk, group_title_str()) == "TEXT"
    assert g_class_type(cfig, onrgrou, jv, knot_str()) == "str"
    assert g_sqlitetype(cfig, onrgrou, jv, knot_str()) == "TEXT"
    assert g_class_type(cfig, onrgrou, jm, _debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, onrgrou, jm, _debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, onrgrou, jm, _credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, onrgrou, jm, _credor_pool_str()) == "REAL"
    assert g_class_type(cfig, onrgrou, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, onrgrou, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, onrgrou, jm, _fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, onrgrou, jm, _fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, onrgrou, jm, _fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, onrgrou, jm, _fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, onrgrou, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, onrgrou, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, onrgrou, jm, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, onrgrou, jm, fund_iota_str()) == "REAL"

    assert g_class_type(cfig, onrawar, jk, awardee_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, onrawar, jk, awardee_title_str()) == "TEXT"
    assert g_class_type(cfig, onrawar, jk, plan_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, onrawar, jk, plan_rope_str()) == "TEXT"
    assert g_class_type(cfig, onrawar, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, onrawar, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, onrawar, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, onrawar, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, onrawar, jv, give_force_str()) == "float"
    assert g_sqlitetype(cfig, onrawar, jv, give_force_str()) == "REAL"
    assert g_class_type(cfig, onrawar, jv, take_force_str()) == "float"
    assert g_sqlitetype(cfig, onrawar, jv, take_force_str()) == "REAL"
    assert g_class_type(cfig, onrfact, jk, fcontext_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, onrfact, jk, fcontext_str()) == "TEXT"
    assert g_class_type(cfig, onrfact, jk, plan_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, onrfact, jk, plan_rope_str()) == "TEXT"
    assert g_class_type(cfig, onrfact, jv, fnigh_str()) == "float"
    assert g_sqlitetype(cfig, onrfact, jv, fnigh_str()) == "REAL"
    assert g_class_type(cfig, onrfact, jv, fopen_str()) == "float"
    assert g_sqlitetype(cfig, onrfact, jv, fopen_str()) == "REAL"
    assert g_class_type(cfig, onrfact, jv, fstate_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, onrfact, jv, fstate_str()) == "TEXT"
    assert g_class_type(cfig, onrheal, jk, healer_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, onrheal, jk, healer_name_str()) == "TEXT"
    assert g_class_type(cfig, onrheal, jk, plan_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, onrheal, jk, plan_rope_str()) == "TEXT"
    assert g_class_type(cfig, onrprem, jk, rcontext_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, onrprem, jk, rcontext_str()) == "TEXT"
    assert g_class_type(cfig, onrprem, jk, pstate_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, onrprem, jk, pstate_str()) == "TEXT"
    assert g_class_type(cfig, onrprem, jk, plan_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, onrprem, jk, plan_rope_str()) == "TEXT"
    assert g_class_type(cfig, onrprem, jm, _status_str()) == "int"
    assert g_sqlitetype(cfig, onrprem, jm, _status_str()) == "INTEGER"
    assert g_class_type(cfig, onrprem, jm, _chore_str()) == "int"
    assert g_sqlitetype(cfig, onrprem, jm, _chore_str()) == "INTEGER"
    assert g_class_type(cfig, onrprem, jv, pdivisor_str()) == "int"
    assert g_sqlitetype(cfig, onrprem, jv, pdivisor_str()) == "INTEGER"
    assert g_class_type(cfig, onrprem, jv, pnigh_str()) == "float"
    assert g_sqlitetype(cfig, onrprem, jv, pnigh_str()) == "REAL"
    assert g_class_type(cfig, onrprem, jv, popen_str()) == "float"
    assert g_sqlitetype(cfig, onrprem, jv, popen_str()) == "REAL"
    assert g_class_type(cfig, onrreas, jk, rcontext_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, onrreas, jk, rcontext_str()) == "TEXT"
    assert g_class_type(cfig, onrreas, jk, plan_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, onrreas, jk, plan_rope_str()) == "TEXT"
    assert g_class_type(cfig, onrreas, jm, "_rplan_active_value") == "int"
    assert g_sqlitetype(cfig, onrreas, jm, "_rplan_active_value") == "INTEGER"
    assert g_class_type(cfig, onrreas, jm, _status_str()) == "int"
    assert g_sqlitetype(cfig, onrreas, jm, _status_str()) == "INTEGER"
    assert g_class_type(cfig, onrreas, jm, _chore_str()) == "int"
    assert g_sqlitetype(cfig, onrreas, jm, _chore_str()) == "INTEGER"
    assert g_class_type(cfig, onrreas, jv, rplan_active_requisite_str()) == "bool"
    assert g_sqlitetype(cfig, onrreas, jv, rplan_active_requisite_str()) == "INTEGER"
    assert g_class_type(cfig, onrlabo, jk, plan_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, onrlabo, jk, plan_rope_str()) == "TEXT"
    assert g_class_type(cfig, onrlabo, jk, labor_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, onrlabo, jk, labor_title_str()) == "TEXT"
    assert g_class_type(cfig, onrlabo, jm, "_believer_name_labor") == "int"
    assert g_sqlitetype(cfig, onrlabo, jm, "_believer_name_labor") == "INTEGER"
    assert g_class_type(cfig, onrplan, jm, "_active") == "int"
    assert g_sqlitetype(cfig, onrplan, jm, "_active") == "INTEGER"
    assert g_class_type(cfig, onrplan, jm, _all_acct_cred_str()) == "int"
    assert g_sqlitetype(cfig, onrplan, jm, _all_acct_cred_str()) == "INTEGER"
    assert g_class_type(cfig, onrplan, jm, _all_acct_debt_str()) == "int"
    assert g_sqlitetype(cfig, onrplan, jm, _all_acct_debt_str()) == "INTEGER"
    assert g_class_type(cfig, onrplan, jm, _descendant_task_count_str()) == "int"
    assert g_sqlitetype(cfig, onrplan, jm, _descendant_task_count_str()) == "INTEGER"
    assert g_class_type(cfig, onrplan, jm, _fund_cease_str()) == "float"
    assert g_sqlitetype(cfig, onrplan, jm, _fund_cease_str()) == "REAL"
    assert g_class_type(cfig, onrplan, jm, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, onrplan, jm, fund_iota_str()) == "REAL"
    assert g_class_type(cfig, onrplan, jm, _fund_onset_str()) == "float"
    assert g_sqlitetype(cfig, onrplan, jm, _fund_onset_str()) == "REAL"
    assert g_class_type(cfig, onrplan, jm, _fund_ratio_str()) == "float"
    assert g_sqlitetype(cfig, onrplan, jm, _fund_ratio_str()) == "REAL"
    assert g_class_type(cfig, onrplan, jm, _gogo_calc_str()) == "float"
    assert g_sqlitetype(cfig, onrplan, jm, _gogo_calc_str()) == "REAL"
    assert g_class_type(cfig, onrplan, jm, _healerlink_ratio_str()) == "float"
    assert g_sqlitetype(cfig, onrplan, jm, _healerlink_ratio_str()) == "REAL"
    assert g_class_type(cfig, onrplan, jm, "_level") == "int"
    assert g_sqlitetype(cfig, onrplan, jm, "_level") == "INTEGER"
    assert g_class_type(cfig, onrplan, jm, _range_evaluated_str()) == "int"
    assert g_sqlitetype(cfig, onrplan, jm, _range_evaluated_str()) == "INTEGER"
    assert g_class_type(cfig, onrplan, jm, _stop_calc_str()) == "float"
    assert g_sqlitetype(cfig, onrplan, jm, _stop_calc_str()) == "REAL"
    assert g_class_type(cfig, onrplan, jm, _chore_str()) == "int"
    assert g_sqlitetype(cfig, onrplan, jm, _chore_str()) == "INTEGER"
    assert g_class_type(cfig, onrplan, jv, addin_str()) == "float"
    assert g_sqlitetype(cfig, onrplan, jv, addin_str()) == "REAL"
    assert g_class_type(cfig, onrplan, jv, begin_str()) == "float"
    assert g_sqlitetype(cfig, onrplan, jv, begin_str()) == "REAL"
    assert g_class_type(cfig, onrplan, jv, close_str()) == "float"
    assert g_sqlitetype(cfig, onrplan, jv, close_str()) == "REAL"
    assert g_class_type(cfig, onrplan, jv, denom_str()) == "int"
    assert g_sqlitetype(cfig, onrplan, jv, denom_str()) == "INTEGER"
    assert g_class_type(cfig, onrplan, jv, gogo_want_str()) == "float"
    assert g_sqlitetype(cfig, onrplan, jv, gogo_want_str()) == "REAL"
    assert g_class_type(cfig, onrplan, jv, mass_str()) == "int"
    assert g_sqlitetype(cfig, onrplan, jv, mass_str()) == "INTEGER"
    assert g_class_type(cfig, onrplan, jv, morph_str()) == "bool"
    assert g_sqlitetype(cfig, onrplan, jv, morph_str()) == "INTEGER"
    assert g_class_type(cfig, onrplan, jv, numor_str()) == "int"
    assert g_sqlitetype(cfig, onrplan, jv, numor_str()) == "INTEGER"
    assert g_class_type(cfig, onrplan, jv, task_str()) == "bool"
    assert g_sqlitetype(cfig, onrplan, jv, task_str()) == "INTEGER"
    assert g_class_type(cfig, onrplan, jv, problem_bool_str()) == "bool"
    assert g_sqlitetype(cfig, onrplan, jv, problem_bool_str()) == "INTEGER"
    assert g_class_type(cfig, onrplan, jv, stop_want_str()) == "float"
    assert g_sqlitetype(cfig, onrplan, jv, stop_want_str()) == "REAL"
    assert g_class_type(cfig, believerunit, jm, "_keeps_buildable") == "int"
    assert g_sqlitetype(cfig, believerunit, jm, "_keeps_buildable") == "INTEGER"
    assert g_class_type(cfig, believerunit, jm, "_keeps_justified") == "int"
    assert g_sqlitetype(cfig, believerunit, jm, "_keeps_justified") == "INTEGER"
    assert g_class_type(cfig, believerunit, jm, _offtrack_fund_str()) == "float"
    assert g_sqlitetype(cfig, believerunit, jm, _offtrack_fund_str()) == "REAL"
    assert g_class_type(cfig, believerunit, jm, _rational_str()) == "bool"
    assert g_sqlitetype(cfig, believerunit, jm, _rational_str()) == "INTEGER"
    assert g_class_type(cfig, believerunit, jm, _sum_healerlink_share_str()) == "float"
    assert g_sqlitetype(cfig, believerunit, jm, _sum_healerlink_share_str()) == "REAL"
    assert g_class_type(cfig, believerunit, jm, _tree_traverse_count_str()) == "int"
    assert g_sqlitetype(cfig, believerunit, jm, _tree_traverse_count_str()) == "INTEGER"
    assert g_class_type(cfig, believerunit, jv, credor_respect_str()) == "float"
    assert g_sqlitetype(cfig, believerunit, jv, credor_respect_str()) == "REAL"
    assert g_class_type(cfig, believerunit, jv, debtor_respect_str()) == "float"
    assert g_sqlitetype(cfig, believerunit, jv, debtor_respect_str()) == "REAL"
    assert g_class_type(cfig, believerunit, jv, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, believerunit, jv, fund_iota_str()) == "REAL"
    assert g_class_type(cfig, believerunit, jv, fund_pool_str()) == "float"
    assert g_sqlitetype(cfig, believerunit, jv, fund_pool_str()) == "REAL"
    assert g_class_type(cfig, believerunit, jv, max_tree_traverse_str()) == "int"
    assert g_sqlitetype(cfig, believerunit, jv, max_tree_traverse_str()) == "INTEGER"
    assert g_class_type(cfig, believerunit, jv, penny_str()) == "float"
    assert g_sqlitetype(cfig, believerunit, jv, penny_str()) == "REAL"
    assert g_class_type(cfig, believerunit, jv, respect_bit_str()) == "float"
    assert g_sqlitetype(cfig, believerunit, jv, respect_bit_str()) == "REAL"
    assert g_class_type(cfig, believerunit, jv, tally_str()) == "int"
    assert g_sqlitetype(cfig, believerunit, jv, tally_str()) == "INTEGER"


def test_get_believer_calc_config_dict_ReturnsObj_EachArgHasOneClassType():
    # ESTABLISH
    believer_calc_config_dict = get_believer_calc_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for believer_calc_dimen, dimen_dict in believer_calc_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues", "jmetrics"}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(class_type_str())
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    for x_arg, arg_types in all_args.items():
        print(f"{x_arg=} {arg_types=}")
        assert len(arg_types) == 1


def test_get_believer_calc_config_dict_ReturnsObj_EachArgHasOne_sqlite_datatype():
    # ESTABLISH
    believer_calc_config_dict = get_believer_calc_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for believer_calc_dimen, dimen_dict in believer_calc_config_dict.items():
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
    sqlite_datatype_dict = get_believer_calc_args_sqlite_datatype_dict()

    # THEN
    for x_arg, arg_types in all_args.items():
        # print(
        #     f"""assert believer_calc_args_type_dict.get("{x_arg}") == "{list(arg_types)[0]}" """
        # )
        print(f""""{x_arg}": "{list(arg_types)[0]}",""")
        assert list(arg_types)[0] == sqlite_datatype_dict.get(x_arg)


def test_get_believer_calc_args_type_dict_ReturnsObj():
    # ESTABLISH
    believer_calc_config_dict = get_believer_calc_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for believer_calc_dimen, dimen_dict in believer_calc_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues", "jmetrics"}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(class_type_str())
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN
    believer_calc_args_type_dict = get_believer_calc_args_type_dict()

    # THEN
    assert believer_calc_args_type_dict.get(acct_name_str()) == NameTerm_str()
    assert believer_calc_args_type_dict.get(group_title_str()) == TitleTerm_str()
    assert believer_calc_args_type_dict.get(_credor_pool_str()) == "float"
    assert believer_calc_args_type_dict.get(_debtor_pool_str()) == "float"
    assert believer_calc_args_type_dict.get(_fund_agenda_give_str()) == "float"
    assert believer_calc_args_type_dict.get(_fund_agenda_ratio_give_str()) == "float"
    assert believer_calc_args_type_dict.get(_fund_agenda_ratio_take_str()) == "float"
    assert believer_calc_args_type_dict.get(_fund_agenda_take_str()) == "float"
    assert believer_calc_args_type_dict.get(_fund_give_str()) == "float"
    assert believer_calc_args_type_dict.get(_fund_take_str()) == "float"
    assert believer_calc_args_type_dict.get(group_cred_points_str()) == "int"
    assert believer_calc_args_type_dict.get(group_debt_points_str()) == "int"
    assert (
        believer_calc_args_type_dict.get(_inallocable_acct_debt_points_str()) == "float"
    )
    assert (
        believer_calc_args_type_dict.get(_irrational_acct_debt_points_str()) == "float"
    )
    assert believer_calc_args_type_dict.get(acct_cred_points_str()) == "float"
    assert believer_calc_args_type_dict.get(acct_debt_points_str()) == "float"
    assert believer_calc_args_type_dict.get(addin_str()) == "float"
    assert believer_calc_args_type_dict.get(begin_str()) == "float"
    assert believer_calc_args_type_dict.get(close_str()) == "float"
    assert believer_calc_args_type_dict.get(denom_str()) == "int"
    assert believer_calc_args_type_dict.get(gogo_want_str()) == "float"
    assert believer_calc_args_type_dict.get(mass_str()) == "int"
    assert believer_calc_args_type_dict.get(morph_str()) == "bool"
    assert believer_calc_args_type_dict.get(numor_str()) == "int"
    assert believer_calc_args_type_dict.get(task_str()) == "bool"
    assert believer_calc_args_type_dict.get(problem_bool_str()) == "bool"
    assert believer_calc_args_type_dict.get(stop_want_str()) == "float"
    assert believer_calc_args_type_dict.get(awardee_title_str()) == TitleTerm_str()
    assert believer_calc_args_type_dict.get(plan_rope_str()) == RopeTerm_str()
    assert believer_calc_args_type_dict.get(give_force_str()) == "float"
    assert believer_calc_args_type_dict.get(take_force_str()) == "float"
    assert believer_calc_args_type_dict.get(rcontext_str()) == RopeTerm_str()
    assert believer_calc_args_type_dict.get(fnigh_str()) == "float"
    assert believer_calc_args_type_dict.get(fopen_str()) == "float"
    assert believer_calc_args_type_dict.get(fstate_str()) == RopeTerm_str()
    assert believer_calc_args_type_dict.get(healer_name_str()) == NameTerm_str()
    assert believer_calc_args_type_dict.get(pstate_str()) == RopeTerm_str()
    assert believer_calc_args_type_dict.get("_status") == "int"
    assert believer_calc_args_type_dict.get("_chore") == "int"
    assert believer_calc_args_type_dict.get(pdivisor_str()) == "int"
    assert believer_calc_args_type_dict.get(pnigh_str()) == "float"
    assert believer_calc_args_type_dict.get(popen_str()) == "float"
    assert believer_calc_args_type_dict.get("_rplan_active_value") == "int"
    assert believer_calc_args_type_dict.get("rplan_active_requisite") == "bool"
    assert believer_calc_args_type_dict.get(labor_title_str()) == TitleTerm_str()
    assert believer_calc_args_type_dict.get("_believer_name_labor") == "int"
    assert believer_calc_args_type_dict.get("_active") == "int"
    assert believer_calc_args_type_dict.get(_all_acct_cred_str()) == "int"
    assert believer_calc_args_type_dict.get(_all_acct_debt_str()) == "int"
    assert believer_calc_args_type_dict.get(_descendant_task_count_str()) == "int"
    assert believer_calc_args_type_dict.get(_fund_cease_str()) == "float"
    assert believer_calc_args_type_dict.get(_fund_onset_str()) == "float"
    assert believer_calc_args_type_dict.get(_fund_ratio_str()) == "float"
    assert believer_calc_args_type_dict.get(_gogo_calc_str()) == "float"
    assert believer_calc_args_type_dict.get("_healerlink_ratio") == "float"
    assert believer_calc_args_type_dict.get("_level") == "int"
    assert believer_calc_args_type_dict.get(_range_evaluated_str()) == "int"
    assert believer_calc_args_type_dict.get(_stop_calc_str()) == "float"
    assert believer_calc_args_type_dict.get("_keeps_buildable") == "int"
    assert believer_calc_args_type_dict.get("_keeps_justified") == "int"
    assert believer_calc_args_type_dict.get(_offtrack_fund_str()) == "int"
    assert believer_calc_args_type_dict.get(_rational_str()) == "bool"
    assert believer_calc_args_type_dict.get(_sum_healerlink_share_str()) == "float"
    assert believer_calc_args_type_dict.get(_tree_traverse_count_str()) == "int"
    assert believer_calc_args_type_dict.get(credor_respect_str()) == "float"
    assert believer_calc_args_type_dict.get(debtor_respect_str()) == "float"
    assert believer_calc_args_type_dict.get(fund_iota_str()) == "float"
    assert believer_calc_args_type_dict.get(fund_pool_str()) == "float"
    assert believer_calc_args_type_dict.get(max_tree_traverse_str()) == "int"
    assert believer_calc_args_type_dict.get(penny_str()) == "float"
    assert believer_calc_args_type_dict.get(respect_bit_str()) == "float"
    assert believer_calc_args_type_dict.get(tally_str()) == "int"
    assert len(believer_calc_args_type_dict) == 72
