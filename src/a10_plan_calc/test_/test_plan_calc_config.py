# from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd
from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic._test_util.a01_str import bridge_str
from src.a02_finance_logic._test_util.a02_str import owner_name_str, vow_label_str
from src.a03_group_logic._test_util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    _inallocable_debtit_score_str,
    _irrational_debtit_score_str,
    awardee_title_str,
    credit_score_str,
    credit_vote_str,
    debtit_score_str,
    debtit_vote_str,
    fund_give_str,
    fund_take_str,
    give_force_str,
    group_title_str,
    respect_bit_str,
    take_force_str,
)
from src.a04_reason_logic._test_util.a04_str import (
    _chore_str,
    _status_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    fstate_str,
    labor_title_str,
    pdivisor_str,
    pnigh_str,
    popen_str,
    pstate_str,
    rconcept_active_requisite_str,
    rcontext_str,
)
from src.a05_concept_logic._test_util.a05_str import (
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
from src.a06_plan_logic._test_util.a06_str import (
    LabelTerm_str,
    NameTerm_str,
    TitleTerm_str,
    WayTerm_str,
    _offtrack_fund_str,
    _rational_str,
    _sum_healerlink_share_str,
    _tree_traverse_count_str,
    acct_name_str,
    addin_str,
    awardee_title_str,
    begin_str,
    close_str,
    concept_way_str,
    credit_score_str,
    credit_vote_str,
    credor_respect_str,
    debtit_score_str,
    debtit_vote_str,
    debtor_respect_str,
    denom_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    fstate_str,
    fund_iota_str,
    fund_pool_str,
    gogo_want_str,
    group_title_str,
    healer_name_str,
    max_tree_traverse_str,
    morph_str,
    numor_str,
    penny_str,
    plan_acct_membership_str,
    plan_acctunit_str,
    plan_concept_awardlink_str,
    plan_concept_factunit_str,
    plan_concept_healerlink_str,
    plan_concept_laborlink_str,
    plan_concept_reason_premiseunit_str,
    plan_concept_reasonunit_str,
    plan_conceptunit_str,
    planunit_str,
    pnigh_str,
    popen_str,
    pstate_str,
    rcontext_str,
    stop_want_str,
    tally_str,
)
from src.a08_plan_atom_logic._test_util.a08_str import (
    class_type_str,
    jkeys_str,
    jvalues_str,
    sqlite_datatype_str,
)
from src.a08_plan_atom_logic.atom_config import get_atom_config_dict
from src.a10_plan_calc._test_util.a10_str import jmetrics_str, plan_groupunit_str
from src.a10_plan_calc.plan_calc_config import (
    config_file_path,
    get_all_plan_calc_args,
    get_plan_calc_args_sqlite_datatype_dict,
    get_plan_calc_args_type_dict,
    get_plan_calc_config_dict,
    get_plan_calc_config_filename,
    get_plan_calc_dimen_args,
    get_plan_calc_dimens,
)


def test_get_plan_calc_config_dict_Exists():
    # ESTABLISH
    src_dir = create_path(os_getcwd(), "src")
    expected_dir = create_path(src_dir, "a10_plan_calc")

    # WHEN / THEN
    assert get_plan_calc_config_filename() == "plan_calc_config.json"
    expected_path = create_path(expected_dir, get_plan_calc_config_filename())
    assert config_file_path() == expected_path
    assert os_path_exists(config_file_path())


def test_get_plan_calc_config_dict_ReturnsObj_CheckLevel0Keys():
    # ESTABLISH / WHEN
    plan_calc_config = get_plan_calc_config_dict()
    plan_calc_config_keys = set(plan_calc_config.keys())

    # THEN
    assert planunit_str() in plan_calc_config_keys
    assert plan_acctunit_str() in plan_calc_config_keys
    assert plan_acct_membership_str() in plan_calc_config_keys
    assert plan_conceptunit_str() in plan_calc_config_keys
    assert plan_concept_awardlink_str() in plan_calc_config_keys
    assert plan_concept_reasonunit_str() in plan_calc_config_keys
    assert plan_concept_reason_premiseunit_str() in plan_calc_config_keys
    assert plan_concept_laborlink_str() in plan_calc_config_keys
    assert plan_concept_healerlink_str() in plan_calc_config_keys
    assert plan_concept_factunit_str() in plan_calc_config_keys
    assert plan_groupunit_str() in plan_calc_config_keys
    assert len(get_plan_calc_config_dict()) == 11
    atom_config_dict = get_atom_config_dict()
    atom_config_dimens = set(atom_config_dict.keys())
    assert atom_config_dimens.issubset(plan_calc_config_keys)
    assert plan_calc_config_keys.difference(atom_config_dimens) == {
        plan_groupunit_str()
    }


def test_get_plan_calc_config_dict_ReturnsObj_CheckLevel1Keys():
    # ESTABLISH / WHEN
    plan_calc_config = get_plan_calc_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests
    for level1_key, aspect_dict in plan_calc_config.items():
        aspect_keys = set(aspect_dict.keys())
        print(f"{level1_key=} {aspect_keys=}")
        assert "abbreviation" in aspect_keys
        assert jkeys_str() in aspect_keys
        assert jvalues_str() in aspect_keys
        assert jmetrics_str() in aspect_keys
        assert len(aspect_keys) == 4


def test_get_plan_calc_config_dict_ReturnsObj_CheckLevel2_And_Level3_Keys():
    # ESTABLISH / WHEN
    plan_calc_config = get_plan_calc_config_dict()

    # THEN
    atom_config = get_atom_config_dict()
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, aspect_dict in plan_calc_config.items():
        if level1_key in atom_config.keys():
            atom_dimen = atom_config.get(level1_key)
            for level2_key, fm_aspect_dict in aspect_dict.items():
                if level2_key == jkeys_str():
                    atom_args = atom_dimen.get(jkeys_str())
                    dimen_keys = set(atom_args)
                    dimen_keys.add(vow_label_str())
                    dimen_keys.add(owner_name_str())
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

    planunit_aspect = plan_calc_config.get(planunit_str())
    planacct_aspect = plan_calc_config.get(plan_acctunit_str())
    planmemb_aspect = plan_calc_config.get(plan_acct_membership_str())
    planconc_aspect = plan_calc_config.get(plan_conceptunit_str())
    planawar_aspect = plan_calc_config.get(plan_concept_awardlink_str())
    planreas_aspect = plan_calc_config.get(plan_concept_reasonunit_str())
    planprem_aspect = plan_calc_config.get(plan_concept_reason_premiseunit_str())
    planlabo_aspect = plan_calc_config.get(plan_concept_laborlink_str())
    planheal_aspect = plan_calc_config.get(plan_concept_healerlink_str())
    planfact_aspect = plan_calc_config.get(plan_concept_factunit_str())
    plangrou_aspect = plan_calc_config.get(plan_groupunit_str())

    planunit_jmetrics_keys = set(planunit_aspect.get(jmetrics_str()))
    planacct_jmetrics_keys = set(planacct_aspect.get(jmetrics_str()))
    planmemb_jmetrics_keys = set(planmemb_aspect.get(jmetrics_str()))
    planconc_jmetrics_keys = set(planconc_aspect.get(jmetrics_str()))
    planawar_jmetrics_keys = set(planawar_aspect.get(jmetrics_str()))
    planreas_jmetrics_keys = set(planreas_aspect.get(jmetrics_str()))
    planprem_jmetrics_keys = set(planprem_aspect.get(jmetrics_str()))
    planlabo_jmetrics_keys = set(planlabo_aspect.get(jmetrics_str()))
    planheal_jmetrics_keys = set(planheal_aspect.get(jmetrics_str()))
    planfact_jmetrics_keys = set(planfact_aspect.get(jmetrics_str()))
    plangrou_jmetrics_keys = set(plangrou_aspect.get(jmetrics_str()))

    expected_planunit_jmetrics_keys = {
        "_tree_traverse_count",
        "_rational",
        "_keeps_justified",
        "_keeps_buildable",
        "_sum_healerlink_share",
        "_offtrack_fund",
    }
    assert expected_planunit_jmetrics_keys == planunit_jmetrics_keys
    expected_planacct_jmetrics_keys = {
        "_credor_pool",
        "_debtor_pool",
        "_irrational_debtit_score",
        "_inallocable_debtit_score",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    assert expected_planacct_jmetrics_keys == planacct_jmetrics_keys
    expected_planmemb_jmetrics_keys = {
        "_credor_pool",
        "_debtor_pool",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    assert expected_planmemb_jmetrics_keys == planmemb_jmetrics_keys
    expected_planconc_jmetrics_keys = {
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
    assert expected_planconc_jmetrics_keys == planconc_jmetrics_keys
    expected_planawar_jmetrics_keys = {"_fund_give", "_fund_take"}
    assert expected_planawar_jmetrics_keys == planawar_jmetrics_keys
    expected_planreas_jmetrics_keys = {
        "_status",
        "_chore",
        "_rconcept_active_value",
    }
    assert expected_planreas_jmetrics_keys == planreas_jmetrics_keys
    expected_planprem_jmetrics_keys = {"_status", "_chore"}
    assert expected_planprem_jmetrics_keys == planprem_jmetrics_keys
    expected_planlabo_jmetrics_keys = {"_owner_name_labor"}
    assert expected_planlabo_jmetrics_keys == planlabo_jmetrics_keys
    expected_plangrou_jmetrics_keys = {
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_credor_pool",
        "_debtor_pool",
        "fund_iota",
    }
    assert expected_plangrou_jmetrics_keys == plangrou_jmetrics_keys

    assert planunit_jmetrics_keys  # Non-empty
    assert planacct_jmetrics_keys  # Non-empty
    assert planmemb_jmetrics_keys  # Non-empty
    assert planconc_jmetrics_keys  # Non-empty
    assert planawar_jmetrics_keys  # Non-empty
    assert planreas_jmetrics_keys  # Non-empty
    assert planprem_jmetrics_keys  # Non-empty
    assert planlabo_jmetrics_keys  # Non-empty
    assert not planheal_jmetrics_keys  # empty
    assert not planfact_jmetrics_keys  # empty
    assert plangrou_jmetrics_keys  # Non-empty


def test_get_plan_calc_config_dict_ReturnsObj_CheckAbbreviations():
    # ESTABLISH / WHEN
    plan_calc_config = get_plan_calc_config_dict()

    # THEN
    planunit_aspect = plan_calc_config.get(planunit_str())
    planacct_aspect = plan_calc_config.get(plan_acctunit_str())
    planmemb_aspect = plan_calc_config.get(plan_acct_membership_str())
    planconc_aspect = plan_calc_config.get(plan_conceptunit_str())
    planawar_aspect = plan_calc_config.get(plan_concept_awardlink_str())
    planreas_aspect = plan_calc_config.get(plan_concept_reasonunit_str())
    planprem_aspect = plan_calc_config.get(plan_concept_reason_premiseunit_str())
    planlabo_aspect = plan_calc_config.get(plan_concept_laborlink_str())
    planheal_aspect = plan_calc_config.get(plan_concept_healerlink_str())
    planfact_aspect = plan_calc_config.get(plan_concept_factunit_str())
    plangrou_aspect = plan_calc_config.get(plan_groupunit_str())
    abbr_str = "abbreviation"
    assert planunit_aspect.get(abbr_str) == "planunit"
    assert planacct_aspect.get(abbr_str) == "planacct"
    assert planmemb_aspect.get(abbr_str) == "planmemb"
    assert planconc_aspect.get(abbr_str) == "planconc"
    assert planawar_aspect.get(abbr_str) == "planawar"
    assert planreas_aspect.get(abbr_str) == "planreas"
    assert planprem_aspect.get(abbr_str) == "planprem"
    assert planlabo_aspect.get(abbr_str) == "planlabo"
    assert planheal_aspect.get(abbr_str) == "planheal"
    assert planfact_aspect.get(abbr_str) == "planfact"
    assert plangrou_aspect.get(abbr_str) == "plangrou"


def test_get_all_plan_calc_args_ReturnsObj():
    # ESTABLISH / WHEN
    all_plan_calc_args = get_all_plan_calc_args()

    # THEN
    assert all_plan_calc_args
    assert stop_want_str() in all_plan_calc_args
    assert concept_way_str() in all_plan_calc_args
    assert "_fund_give" in all_plan_calc_args
    assert all_plan_calc_args.get("_fund_give") == {
        "plan_concept_awardlink",
        "plan_acct_membership",
        "plan_groupunit",
        "plan_acctunit",
    }

    # plan_calc_config = get_plan_calc_config_dict()
    # plan_acctunit_aspects = plan_calc_config.get("plan_acctunit")
    # planacct_jmetrics_dict = plan_acctunit_aspects.get("jmetrics")
    # way_plan_calc_aspects = planacct_jmetrics_dict.get("_fund_give")
    # assert plan_concept_factunit_str() in way_plan_calc_aspects
    # assert plan_concept_laborlink_str() in way_plan_calc_aspects
    # assert len(way_plan_calc_aspects) == 6
    assert len(all_plan_calc_args) == 76


def test_get_plan_calc_config_dict_ReturnsObj_CheckArgDataTypesKeysExist():
    # ESTABLISH / WHEN
    plan_calc_config = get_plan_calc_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, aspect_dict in plan_calc_config.items():
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


def test_get_plan_calc_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    plan_calc_dimens = get_plan_calc_dimens()

    # THEN
    expected_plan_calc_dimens = {
        planunit_str(),
        plan_acctunit_str(),
        plan_acct_membership_str(),
        plan_conceptunit_str(),
        plan_concept_awardlink_str(),
        plan_concept_reasonunit_str(),
        plan_concept_reason_premiseunit_str(),
        plan_concept_laborlink_str(),
        plan_concept_healerlink_str(),
        plan_concept_factunit_str(),
        plan_groupunit_str(),
    }
    assert plan_calc_dimens == expected_plan_calc_dimens
    assert plan_calc_dimens == set(get_plan_calc_config_dict().keys())


def test_get_plan_calc_dimen_args_ReturnsObj():
    # ESTABLISH / WHEN
    plan_acctunit_args = get_plan_calc_dimen_args(plan_acctunit_str())
    plan_conceptunit_args = get_plan_calc_dimen_args(plan_conceptunit_str())
    plan_groupunit_args = get_plan_calc_dimen_args(plan_groupunit_str())

    #  THEN
    print(f"{plan_acctunit_args=}")
    print(f"{plan_groupunit_args=}")
    assert plan_acctunit_args == {
        vow_label_str(),
        owner_name_str(),
        "_fund_agenda_give",
        "_credor_pool",
        "_fund_give",
        credit_score_str(),
        acct_name_str(),
        debtit_score_str(),
        "_fund_agenda_ratio_take",
        "_inallocable_debtit_score",
        "_fund_agenda_ratio_give",
        "_fund_agenda_take",
        "_fund_take",
        "_debtor_pool",
        "_irrational_debtit_score",
    }
    assert plan_conceptunit_args == {
        vow_label_str(),
        owner_name_str(),
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
        concept_way_str(),
        begin_str(),
    }
    assert plan_groupunit_args == {
        vow_label_str(),
        owner_name_str(),
        "_debtor_pool",
        "_credor_pool",
        "_fund_give",
        "group_title",
        "bridge",
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


def test_get_plan_calc_config_dict_ReturnsObj_CheckArgDataTypesCorrect():
    # ESTABLISH / WHEN
    cfig = get_plan_calc_config_dict()
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
    planunit = planunit_str()
    planacct = plan_acctunit_str()
    planmemb = plan_acct_membership_str()
    planconc = plan_conceptunit_str()
    planawar = plan_concept_awardlink_str()
    planreas = plan_concept_reasonunit_str()
    planprem = plan_concept_reason_premiseunit_str()
    planlabo = plan_concept_laborlink_str()
    planheal = plan_concept_healerlink_str()
    planfact = plan_concept_factunit_str()
    plangrou = plan_groupunit_str()
    assert g_class_type(cfig, planmemb, jk, acct_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, planmemb, jk, acct_name_str()) == "TEXT"
    assert g_class_type(cfig, planmemb, jk, group_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, planmemb, jk, group_title_str()) == "TEXT"
    assert g_class_type(cfig, planmemb, jm, _credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, planmemb, jm, _credor_pool_str()) == "REAL"
    assert g_class_type(cfig, planmemb, jm, _debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, planmemb, jm, _debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, planmemb, jm, _fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, planmemb, jm, _fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, planmemb, jm, _fund_agenda_ratio_give_str()) == "float"
    assert g_sqlitetype(cfig, planmemb, jm, _fund_agenda_ratio_give_str()) == "REAL"
    assert g_class_type(cfig, planmemb, jm, _fund_agenda_ratio_take_str()) == "float"
    assert g_sqlitetype(cfig, planmemb, jm, _fund_agenda_ratio_take_str()) == "REAL"
    assert g_class_type(cfig, planmemb, jm, _fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, planmemb, jm, _fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, planmemb, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, planmemb, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, planmemb, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, planmemb, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, planmemb, jv, credit_vote_str()) == "float"
    assert g_sqlitetype(cfig, planmemb, jv, credit_vote_str()) == "REAL"
    assert g_class_type(cfig, planmemb, jv, debtit_vote_str()) == "float"
    assert g_sqlitetype(cfig, planmemb, jv, debtit_vote_str()) == "REAL"
    assert g_class_type(cfig, planacct, jk, acct_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, planacct, jk, acct_name_str()) == "TEXT"
    assert g_class_type(cfig, planacct, jm, _credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, planacct, jm, _credor_pool_str()) == "REAL"
    assert g_class_type(cfig, planacct, jm, _debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, planacct, jm, _debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, planacct, jm, _fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, planacct, jm, _fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, planacct, jm, _fund_agenda_ratio_give_str()) == "float"
    assert g_sqlitetype(cfig, planacct, jm, _fund_agenda_ratio_give_str()) == "REAL"
    assert g_class_type(cfig, planacct, jm, _fund_agenda_ratio_take_str()) == "float"
    assert g_sqlitetype(cfig, planacct, jm, _fund_agenda_ratio_take_str()) == "REAL"
    assert g_class_type(cfig, planacct, jm, _fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, planacct, jm, _fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, planacct, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, planacct, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, planacct, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, planacct, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, planacct, jm, _inallocable_debtit_score_str()) == "float"
    assert g_sqlitetype(cfig, planacct, jm, _inallocable_debtit_score_str()) == "REAL"
    assert g_class_type(cfig, planacct, jm, _irrational_debtit_score_str()) == "float"
    assert g_sqlitetype(cfig, planacct, jm, _irrational_debtit_score_str()) == "REAL"
    assert g_class_type(cfig, planacct, jv, credit_score_str()) == "float"
    assert g_sqlitetype(cfig, planacct, jv, credit_score_str()) == "REAL"
    assert g_class_type(cfig, planacct, jv, debtit_score_str()) == "float"
    assert g_sqlitetype(cfig, planacct, jv, debtit_score_str()) == "REAL"

    assert g_class_type(cfig, plangrou, jk, group_title_str()) == "TitleTerm"
    assert g_sqlitetype(cfig, plangrou, jk, group_title_str()) == "TEXT"
    assert g_class_type(cfig, plangrou, jv, bridge_str()) == "str"
    assert g_sqlitetype(cfig, plangrou, jv, bridge_str()) == "TEXT"
    assert g_class_type(cfig, plangrou, jm, _debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, plangrou, jm, _debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, plangrou, jm, _credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, plangrou, jm, _credor_pool_str()) == "REAL"
    assert g_class_type(cfig, plangrou, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, plangrou, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, plangrou, jm, _fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, plangrou, jm, _fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, plangrou, jm, _fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, plangrou, jm, _fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, plangrou, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, plangrou, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, plangrou, jm, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, plangrou, jm, fund_iota_str()) == "REAL"

    assert g_class_type(cfig, planawar, jk, awardee_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, planawar, jk, awardee_title_str()) == "TEXT"
    assert g_class_type(cfig, planawar, jk, concept_way_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, planawar, jk, concept_way_str()) == "TEXT"
    assert g_class_type(cfig, planawar, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, planawar, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, planawar, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, planawar, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, planawar, jv, give_force_str()) == "float"
    assert g_sqlitetype(cfig, planawar, jv, give_force_str()) == "REAL"
    assert g_class_type(cfig, planawar, jv, take_force_str()) == "float"
    assert g_sqlitetype(cfig, planawar, jv, take_force_str()) == "REAL"
    assert g_class_type(cfig, planfact, jk, fcontext_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, planfact, jk, fcontext_str()) == "TEXT"
    assert g_class_type(cfig, planfact, jk, concept_way_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, planfact, jk, concept_way_str()) == "TEXT"
    assert g_class_type(cfig, planfact, jv, fnigh_str()) == "float"
    assert g_sqlitetype(cfig, planfact, jv, fnigh_str()) == "REAL"
    assert g_class_type(cfig, planfact, jv, fopen_str()) == "float"
    assert g_sqlitetype(cfig, planfact, jv, fopen_str()) == "REAL"
    assert g_class_type(cfig, planfact, jv, fstate_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, planfact, jv, fstate_str()) == "TEXT"
    assert g_class_type(cfig, planheal, jk, healer_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, planheal, jk, healer_name_str()) == "TEXT"
    assert g_class_type(cfig, planheal, jk, concept_way_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, planheal, jk, concept_way_str()) == "TEXT"
    assert g_class_type(cfig, planprem, jk, rcontext_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, planprem, jk, rcontext_str()) == "TEXT"
    assert g_class_type(cfig, planprem, jk, pstate_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, planprem, jk, pstate_str()) == "TEXT"
    assert g_class_type(cfig, planprem, jk, concept_way_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, planprem, jk, concept_way_str()) == "TEXT"
    assert g_class_type(cfig, planprem, jm, _status_str()) == "int"
    assert g_sqlitetype(cfig, planprem, jm, _status_str()) == "INTEGER"
    assert g_class_type(cfig, planprem, jm, _chore_str()) == "int"
    assert g_sqlitetype(cfig, planprem, jm, _chore_str()) == "INTEGER"
    assert g_class_type(cfig, planprem, jv, pdivisor_str()) == "int"
    assert g_sqlitetype(cfig, planprem, jv, pdivisor_str()) == "INTEGER"
    assert g_class_type(cfig, planprem, jv, pnigh_str()) == "float"
    assert g_sqlitetype(cfig, planprem, jv, pnigh_str()) == "REAL"
    assert g_class_type(cfig, planprem, jv, popen_str()) == "float"
    assert g_sqlitetype(cfig, planprem, jv, popen_str()) == "REAL"
    assert g_class_type(cfig, planreas, jk, rcontext_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, planreas, jk, rcontext_str()) == "TEXT"
    assert g_class_type(cfig, planreas, jk, concept_way_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, planreas, jk, concept_way_str()) == "TEXT"
    assert g_class_type(cfig, planreas, jm, "_rconcept_active_value") == "int"
    assert g_sqlitetype(cfig, planreas, jm, "_rconcept_active_value") == "INTEGER"
    assert g_class_type(cfig, planreas, jm, _status_str()) == "int"
    assert g_sqlitetype(cfig, planreas, jm, _status_str()) == "INTEGER"
    assert g_class_type(cfig, planreas, jm, _chore_str()) == "int"
    assert g_sqlitetype(cfig, planreas, jm, _chore_str()) == "INTEGER"
    assert g_class_type(cfig, planreas, jv, rconcept_active_requisite_str()) == "bool"
    assert (
        g_sqlitetype(cfig, planreas, jv, rconcept_active_requisite_str()) == "INTEGER"
    )
    assert g_class_type(cfig, planlabo, jk, concept_way_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, planlabo, jk, concept_way_str()) == "TEXT"
    assert g_class_type(cfig, planlabo, jk, labor_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, planlabo, jk, labor_title_str()) == "TEXT"
    assert g_class_type(cfig, planlabo, jm, "_owner_name_labor") == "int"
    assert g_sqlitetype(cfig, planlabo, jm, "_owner_name_labor") == "INTEGER"
    assert g_class_type(cfig, planconc, jm, "_active") == "int"
    assert g_sqlitetype(cfig, planconc, jm, "_active") == "INTEGER"
    assert g_class_type(cfig, planconc, jm, _all_acct_cred_str()) == "int"
    assert g_sqlitetype(cfig, planconc, jm, _all_acct_cred_str()) == "INTEGER"
    assert g_class_type(cfig, planconc, jm, _all_acct_debt_str()) == "int"
    assert g_sqlitetype(cfig, planconc, jm, _all_acct_debt_str()) == "INTEGER"
    assert g_class_type(cfig, planconc, jm, _descendant_task_count_str()) == "int"
    assert g_sqlitetype(cfig, planconc, jm, _descendant_task_count_str()) == "INTEGER"
    assert g_class_type(cfig, planconc, jm, _fund_cease_str()) == "float"
    assert g_sqlitetype(cfig, planconc, jm, _fund_cease_str()) == "REAL"
    assert g_class_type(cfig, planconc, jm, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, planconc, jm, fund_iota_str()) == "REAL"
    assert g_class_type(cfig, planconc, jm, _fund_onset_str()) == "float"
    assert g_sqlitetype(cfig, planconc, jm, _fund_onset_str()) == "REAL"
    assert g_class_type(cfig, planconc, jm, _fund_ratio_str()) == "float"
    assert g_sqlitetype(cfig, planconc, jm, _fund_ratio_str()) == "REAL"
    assert g_class_type(cfig, planconc, jm, _gogo_calc_str()) == "float"
    assert g_sqlitetype(cfig, planconc, jm, _gogo_calc_str()) == "REAL"
    assert g_class_type(cfig, planconc, jm, _healerlink_ratio_str()) == "float"
    assert g_sqlitetype(cfig, planconc, jm, _healerlink_ratio_str()) == "REAL"
    assert g_class_type(cfig, planconc, jm, "_level") == "int"
    assert g_sqlitetype(cfig, planconc, jm, "_level") == "INTEGER"
    assert g_class_type(cfig, planconc, jm, _range_evaluated_str()) == "int"
    assert g_sqlitetype(cfig, planconc, jm, _range_evaluated_str()) == "INTEGER"
    assert g_class_type(cfig, planconc, jm, _stop_calc_str()) == "float"
    assert g_sqlitetype(cfig, planconc, jm, _stop_calc_str()) == "REAL"
    assert g_class_type(cfig, planconc, jm, _chore_str()) == "int"
    assert g_sqlitetype(cfig, planconc, jm, _chore_str()) == "INTEGER"
    assert g_class_type(cfig, planconc, jv, addin_str()) == "float"
    assert g_sqlitetype(cfig, planconc, jv, addin_str()) == "REAL"
    assert g_class_type(cfig, planconc, jv, begin_str()) == "float"
    assert g_sqlitetype(cfig, planconc, jv, begin_str()) == "REAL"
    assert g_class_type(cfig, planconc, jv, close_str()) == "float"
    assert g_sqlitetype(cfig, planconc, jv, close_str()) == "REAL"
    assert g_class_type(cfig, planconc, jv, denom_str()) == "int"
    assert g_sqlitetype(cfig, planconc, jv, denom_str()) == "INTEGER"
    assert g_class_type(cfig, planconc, jv, gogo_want_str()) == "float"
    assert g_sqlitetype(cfig, planconc, jv, gogo_want_str()) == "REAL"
    assert g_class_type(cfig, planconc, jv, mass_str()) == "int"
    assert g_sqlitetype(cfig, planconc, jv, mass_str()) == "INTEGER"
    assert g_class_type(cfig, planconc, jv, morph_str()) == "bool"
    assert g_sqlitetype(cfig, planconc, jv, morph_str()) == "INTEGER"
    assert g_class_type(cfig, planconc, jv, numor_str()) == "int"
    assert g_sqlitetype(cfig, planconc, jv, numor_str()) == "INTEGER"
    assert g_class_type(cfig, planconc, jv, task_str()) == "bool"
    assert g_sqlitetype(cfig, planconc, jv, task_str()) == "INTEGER"
    assert g_class_type(cfig, planconc, jv, problem_bool_str()) == "bool"
    assert g_sqlitetype(cfig, planconc, jv, problem_bool_str()) == "INTEGER"
    assert g_class_type(cfig, planconc, jv, stop_want_str()) == "float"
    assert g_sqlitetype(cfig, planconc, jv, stop_want_str()) == "REAL"
    assert g_class_type(cfig, planunit, jm, "_keeps_buildable") == "int"
    assert g_sqlitetype(cfig, planunit, jm, "_keeps_buildable") == "INTEGER"
    assert g_class_type(cfig, planunit, jm, "_keeps_justified") == "int"
    assert g_sqlitetype(cfig, planunit, jm, "_keeps_justified") == "INTEGER"
    assert g_class_type(cfig, planunit, jm, _offtrack_fund_str()) == "float"
    assert g_sqlitetype(cfig, planunit, jm, _offtrack_fund_str()) == "REAL"
    assert g_class_type(cfig, planunit, jm, _rational_str()) == "bool"
    assert g_sqlitetype(cfig, planunit, jm, _rational_str()) == "INTEGER"
    assert g_class_type(cfig, planunit, jm, _sum_healerlink_share_str()) == "float"
    assert g_sqlitetype(cfig, planunit, jm, _sum_healerlink_share_str()) == "REAL"
    assert g_class_type(cfig, planunit, jm, _tree_traverse_count_str()) == "int"
    assert g_sqlitetype(cfig, planunit, jm, _tree_traverse_count_str()) == "INTEGER"
    assert g_class_type(cfig, planunit, jv, credor_respect_str()) == "float"
    assert g_sqlitetype(cfig, planunit, jv, credor_respect_str()) == "REAL"
    assert g_class_type(cfig, planunit, jv, debtor_respect_str()) == "float"
    assert g_sqlitetype(cfig, planunit, jv, debtor_respect_str()) == "REAL"
    assert g_class_type(cfig, planunit, jv, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, planunit, jv, fund_iota_str()) == "REAL"
    assert g_class_type(cfig, planunit, jv, fund_pool_str()) == "float"
    assert g_sqlitetype(cfig, planunit, jv, fund_pool_str()) == "REAL"
    assert g_class_type(cfig, planunit, jv, max_tree_traverse_str()) == "int"
    assert g_sqlitetype(cfig, planunit, jv, max_tree_traverse_str()) == "INTEGER"
    assert g_class_type(cfig, planunit, jv, penny_str()) == "float"
    assert g_sqlitetype(cfig, planunit, jv, penny_str()) == "REAL"
    assert g_class_type(cfig, planunit, jv, respect_bit_str()) == "float"
    assert g_sqlitetype(cfig, planunit, jv, respect_bit_str()) == "REAL"
    assert g_class_type(cfig, planunit, jv, tally_str()) == "int"
    assert g_sqlitetype(cfig, planunit, jv, tally_str()) == "INTEGER"


def test_get_plan_calc_config_dict_ReturnsObj_EachArgHasOneClassType():
    # ESTABLISH
    plan_calc_config_dict = get_plan_calc_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for plan_calc_dimen, dimen_dict in plan_calc_config_dict.items():
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


def test_get_plan_calc_config_dict_ReturnsObj_EachArgHasOne_sqlite_datatype():
    # ESTABLISH
    plan_calc_config_dict = get_plan_calc_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for plan_calc_dimen, dimen_dict in plan_calc_config_dict.items():
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
    sqlite_datatype_dict = get_plan_calc_args_sqlite_datatype_dict()

    # THEN
    for x_arg, arg_types in all_args.items():
        # print(
        #     f"""assert plan_calc_args_type_dict.get("{x_arg}") == "{list(arg_types)[0]}" """
        # )
        print(f""""{x_arg}": "{list(arg_types)[0]}",""")
        assert list(arg_types)[0] == sqlite_datatype_dict.get(x_arg)


def test_get_plan_calc_args_type_dict_ReturnsObj():
    # ESTABLISH
    plan_calc_config_dict = get_plan_calc_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for plan_calc_dimen, dimen_dict in plan_calc_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues", "jmetrics"}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(class_type_str())
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN
    plan_calc_args_type_dict = get_plan_calc_args_type_dict()

    # THEN
    assert plan_calc_args_type_dict.get(acct_name_str()) == NameTerm_str()
    assert plan_calc_args_type_dict.get(group_title_str()) == TitleTerm_str()
    assert plan_calc_args_type_dict.get(_credor_pool_str()) == "float"
    assert plan_calc_args_type_dict.get(_debtor_pool_str()) == "float"
    assert plan_calc_args_type_dict.get(_fund_agenda_give_str()) == "float"
    assert plan_calc_args_type_dict.get(_fund_agenda_ratio_give_str()) == "float"
    assert plan_calc_args_type_dict.get(_fund_agenda_ratio_take_str()) == "float"
    assert plan_calc_args_type_dict.get(_fund_agenda_take_str()) == "float"
    assert plan_calc_args_type_dict.get(_fund_give_str()) == "float"
    assert plan_calc_args_type_dict.get(_fund_take_str()) == "float"
    assert plan_calc_args_type_dict.get(credit_vote_str()) == "int"
    assert plan_calc_args_type_dict.get(debtit_vote_str()) == "int"
    assert plan_calc_args_type_dict.get(_inallocable_debtit_score_str()) == "float"
    assert plan_calc_args_type_dict.get(_irrational_debtit_score_str()) == "float"
    assert plan_calc_args_type_dict.get(credit_score_str()) == "float"
    assert plan_calc_args_type_dict.get(debtit_score_str()) == "float"
    assert plan_calc_args_type_dict.get(addin_str()) == "float"
    assert plan_calc_args_type_dict.get(begin_str()) == "float"
    assert plan_calc_args_type_dict.get(close_str()) == "float"
    assert plan_calc_args_type_dict.get(denom_str()) == "int"
    assert plan_calc_args_type_dict.get(gogo_want_str()) == "float"
    assert plan_calc_args_type_dict.get(mass_str()) == "int"
    assert plan_calc_args_type_dict.get(morph_str()) == "bool"
    assert plan_calc_args_type_dict.get(numor_str()) == "int"
    assert plan_calc_args_type_dict.get(task_str()) == "bool"
    assert plan_calc_args_type_dict.get(problem_bool_str()) == "bool"
    assert plan_calc_args_type_dict.get(stop_want_str()) == "float"
    assert plan_calc_args_type_dict.get(awardee_title_str()) == TitleTerm_str()
    assert plan_calc_args_type_dict.get(concept_way_str()) == WayTerm_str()
    assert plan_calc_args_type_dict.get(give_force_str()) == "float"
    assert plan_calc_args_type_dict.get(take_force_str()) == "float"
    assert plan_calc_args_type_dict.get(rcontext_str()) == WayTerm_str()
    assert plan_calc_args_type_dict.get(fnigh_str()) == "float"
    assert plan_calc_args_type_dict.get(fopen_str()) == "float"
    assert plan_calc_args_type_dict.get(fstate_str()) == WayTerm_str()
    assert plan_calc_args_type_dict.get(healer_name_str()) == NameTerm_str()
    assert plan_calc_args_type_dict.get(pstate_str()) == WayTerm_str()
    assert plan_calc_args_type_dict.get("_status") == "int"
    assert plan_calc_args_type_dict.get("_chore") == "int"
    assert plan_calc_args_type_dict.get(pdivisor_str()) == "int"
    assert plan_calc_args_type_dict.get(pnigh_str()) == "float"
    assert plan_calc_args_type_dict.get(popen_str()) == "float"
    assert plan_calc_args_type_dict.get("_rconcept_active_value") == "int"
    assert plan_calc_args_type_dict.get("rconcept_active_requisite") == "bool"
    assert plan_calc_args_type_dict.get(labor_title_str()) == TitleTerm_str()
    assert plan_calc_args_type_dict.get("_owner_name_labor") == "int"
    assert plan_calc_args_type_dict.get("_active") == "int"
    assert plan_calc_args_type_dict.get(_all_acct_cred_str()) == "int"
    assert plan_calc_args_type_dict.get(_all_acct_debt_str()) == "int"
    assert plan_calc_args_type_dict.get(_descendant_task_count_str()) == "int"
    assert plan_calc_args_type_dict.get(_fund_cease_str()) == "float"
    assert plan_calc_args_type_dict.get(_fund_onset_str()) == "float"
    assert plan_calc_args_type_dict.get(_fund_ratio_str()) == "float"
    assert plan_calc_args_type_dict.get(_gogo_calc_str()) == "float"
    assert plan_calc_args_type_dict.get("_healerlink_ratio") == "float"
    assert plan_calc_args_type_dict.get("_level") == "int"
    assert plan_calc_args_type_dict.get(_range_evaluated_str()) == "int"
    assert plan_calc_args_type_dict.get(_stop_calc_str()) == "float"
    assert plan_calc_args_type_dict.get("_keeps_buildable") == "int"
    assert plan_calc_args_type_dict.get("_keeps_justified") == "int"
    assert plan_calc_args_type_dict.get(_offtrack_fund_str()) == "int"
    assert plan_calc_args_type_dict.get(_rational_str()) == "bool"
    assert plan_calc_args_type_dict.get(_sum_healerlink_share_str()) == "float"
    assert plan_calc_args_type_dict.get(_tree_traverse_count_str()) == "int"
    assert plan_calc_args_type_dict.get(credor_respect_str()) == "float"
    assert plan_calc_args_type_dict.get(debtor_respect_str()) == "float"
    assert plan_calc_args_type_dict.get(fund_iota_str()) == "float"
    assert plan_calc_args_type_dict.get(fund_pool_str()) == "float"
    assert plan_calc_args_type_dict.get(max_tree_traverse_str()) == "int"
    assert plan_calc_args_type_dict.get(penny_str()) == "float"
    assert plan_calc_args_type_dict.get(respect_bit_str()) == "float"
    assert plan_calc_args_type_dict.get(tally_str()) == "int"
    assert len(plan_calc_args_type_dict) == 72
