# from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from os import getcwd as os_getcwd
from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.test._util.a01_str import knot_str
from src.a02_finance_logic.test._util.a02_str import owner_name_str, vow_label_str
from src.a03_group_logic.test._util.a03_str import (
    _credor_pool_str,
    _debtor_pool_str,
    _fund_agenda_give_str,
    _fund_agenda_ratio_give_str,
    _fund_agenda_ratio_take_str,
    _fund_agenda_take_str,
    _fund_give_str,
    _fund_take_str,
    _inallocable_debt_score_str,
    _irrational_debt_score_str,
    awardee_title_str,
    credit_score_str,
    credit_vote_str,
    debt_score_str,
    debt_vote_str,
    fund_give_str,
    fund_take_str,
    give_force_str,
    group_title_str,
    respect_bit_str,
    take_force_str,
)
from src.a04_reason_logic.test._util.a04_str import (
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
from src.a05_concept_logic.test._util.a05_str import (
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
from src.a06_plan_logic.test._util.a06_str import (
    LabelTerm_str,
    NameTerm_str,
    RopeTerm_str,
    TitleTerm_str,
    _offtrack_fund_str,
    _rational_str,
    _sum_healerlink_share_str,
    _tree_traverse_count_str,
    acct_name_str,
    addin_str,
    awardee_title_str,
    begin_str,
    close_str,
    concept_rope_str,
    credit_score_str,
    credit_vote_str,
    credor_respect_str,
    debt_score_str,
    debt_vote_str,
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
from src.a08_plan_atom_logic.atom_config import get_atom_config_dict
from src.a08_plan_atom_logic.test._util.a08_str import (
    class_type_str,
    jkeys_str,
    jvalues_str,
    sqlite_datatype_str,
)
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
from src.a10_plan_calc.test._util.a10_str import jmetrics_str, plan_groupunit_str


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

    plnunit_aspect = plan_calc_config.get(planunit_str())
    plnacct_aspect = plan_calc_config.get(plan_acctunit_str())
    plnmemb_aspect = plan_calc_config.get(plan_acct_membership_str())
    plnconc_aspect = plan_calc_config.get(plan_conceptunit_str())
    plnawar_aspect = plan_calc_config.get(plan_concept_awardlink_str())
    plnreas_aspect = plan_calc_config.get(plan_concept_reasonunit_str())
    plnprem_aspect = plan_calc_config.get(plan_concept_reason_premiseunit_str())
    plnlabo_aspect = plan_calc_config.get(plan_concept_laborlink_str())
    plnheal_aspect = plan_calc_config.get(plan_concept_healerlink_str())
    plnfact_aspect = plan_calc_config.get(plan_concept_factunit_str())
    plngrou_aspect = plan_calc_config.get(plan_groupunit_str())

    plnunit_jmetrics_keys = set(plnunit_aspect.get(jmetrics_str()))
    plnacct_jmetrics_keys = set(plnacct_aspect.get(jmetrics_str()))
    plnmemb_jmetrics_keys = set(plnmemb_aspect.get(jmetrics_str()))
    plnconc_jmetrics_keys = set(plnconc_aspect.get(jmetrics_str()))
    plnawar_jmetrics_keys = set(plnawar_aspect.get(jmetrics_str()))
    plnreas_jmetrics_keys = set(plnreas_aspect.get(jmetrics_str()))
    plnprem_jmetrics_keys = set(plnprem_aspect.get(jmetrics_str()))
    plnlabo_jmetrics_keys = set(plnlabo_aspect.get(jmetrics_str()))
    plnheal_jmetrics_keys = set(plnheal_aspect.get(jmetrics_str()))
    plnfact_jmetrics_keys = set(plnfact_aspect.get(jmetrics_str()))
    plngrou_jmetrics_keys = set(plngrou_aspect.get(jmetrics_str()))

    expected_plnunit_jmetrics_keys = {
        "_tree_traverse_count",
        "_rational",
        "_keeps_justified",
        "_keeps_buildable",
        "_sum_healerlink_share",
        "_offtrack_fund",
    }
    assert expected_plnunit_jmetrics_keys == plnunit_jmetrics_keys
    expected_plnacct_jmetrics_keys = {
        "_credor_pool",
        "_debtor_pool",
        "_irrational_debt_score",
        "_inallocable_debt_score",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    assert expected_plnacct_jmetrics_keys == plnacct_jmetrics_keys
    expected_plnmemb_jmetrics_keys = {
        "_credor_pool",
        "_debtor_pool",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    assert expected_plnmemb_jmetrics_keys == plnmemb_jmetrics_keys
    expected_plnconc_jmetrics_keys = {
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
    assert expected_plnconc_jmetrics_keys == plnconc_jmetrics_keys
    expected_plnawar_jmetrics_keys = {"_fund_give", "_fund_take"}
    assert expected_plnawar_jmetrics_keys == plnawar_jmetrics_keys
    expected_plnreas_jmetrics_keys = {
        "_status",
        "_chore",
        "_rconcept_active_value",
    }
    assert expected_plnreas_jmetrics_keys == plnreas_jmetrics_keys
    expected_plnprem_jmetrics_keys = {"_status", "_chore"}
    assert expected_plnprem_jmetrics_keys == plnprem_jmetrics_keys
    expected_plnlabo_jmetrics_keys = {"_owner_name_labor"}
    assert expected_plnlabo_jmetrics_keys == plnlabo_jmetrics_keys
    expected_plngrou_jmetrics_keys = {
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_credor_pool",
        "_debtor_pool",
        "fund_iota",
    }
    assert expected_plngrou_jmetrics_keys == plngrou_jmetrics_keys

    assert plnunit_jmetrics_keys  # Non-empty
    assert plnacct_jmetrics_keys  # Non-empty
    assert plnmemb_jmetrics_keys  # Non-empty
    assert plnconc_jmetrics_keys  # Non-empty
    assert plnawar_jmetrics_keys  # Non-empty
    assert plnreas_jmetrics_keys  # Non-empty
    assert plnprem_jmetrics_keys  # Non-empty
    assert plnlabo_jmetrics_keys  # Non-empty
    assert not plnheal_jmetrics_keys  # empty
    assert not plnfact_jmetrics_keys  # empty
    assert plngrou_jmetrics_keys  # Non-empty


def test_get_plan_calc_config_dict_ReturnsObj_CheckAbbreviations():
    # ESTABLISH / WHEN
    plan_calc_config = get_plan_calc_config_dict()

    # THEN
    plnunit_aspect = plan_calc_config.get(planunit_str())
    plnacct_aspect = plan_calc_config.get(plan_acctunit_str())
    plnmemb_aspect = plan_calc_config.get(plan_acct_membership_str())
    plnconc_aspect = plan_calc_config.get(plan_conceptunit_str())
    plnawar_aspect = plan_calc_config.get(plan_concept_awardlink_str())
    plnreas_aspect = plan_calc_config.get(plan_concept_reasonunit_str())
    plnprem_aspect = plan_calc_config.get(plan_concept_reason_premiseunit_str())
    plnlabo_aspect = plan_calc_config.get(plan_concept_laborlink_str())
    plnheal_aspect = plan_calc_config.get(plan_concept_healerlink_str())
    plnfact_aspect = plan_calc_config.get(plan_concept_factunit_str())
    plngrou_aspect = plan_calc_config.get(plan_groupunit_str())
    abbr_str = "abbreviation"
    assert plnunit_aspect.get(abbr_str) == "plnunit"
    assert plnacct_aspect.get(abbr_str) == "plnacct"
    assert plnmemb_aspect.get(abbr_str) == "plnmemb"
    assert plnconc_aspect.get(abbr_str) == "plnconc"
    assert plnawar_aspect.get(abbr_str) == "plnawar"
    assert plnreas_aspect.get(abbr_str) == "plnreas"
    assert plnprem_aspect.get(abbr_str) == "plnprem"
    assert plnlabo_aspect.get(abbr_str) == "plnlabo"
    assert plnheal_aspect.get(abbr_str) == "plnheal"
    assert plnfact_aspect.get(abbr_str) == "plnfact"
    assert plngrou_aspect.get(abbr_str) == "plngrou"


def test_get_all_plan_calc_args_ReturnsObj():
    # ESTABLISH / WHEN
    all_plan_calc_args = get_all_plan_calc_args()

    # THEN
    assert all_plan_calc_args
    assert stop_want_str() in all_plan_calc_args
    assert concept_rope_str() in all_plan_calc_args
    assert "_fund_give" in all_plan_calc_args
    assert all_plan_calc_args.get("_fund_give") == {
        "plan_concept_awardlink",
        "plan_acct_membership",
        "plan_groupunit",
        "plan_acctunit",
    }

    # plan_calc_config = get_plan_calc_config_dict()
    # plan_acctunit_aspects = plan_calc_config.get("plan_acctunit")
    # plnacct_jmetrics_dict = plan_acctunit_aspects.get("jmetrics")
    # rope_plan_calc_aspects = plnacct_jmetrics_dict.get("_fund_give")
    # assert plan_concept_factunit_str() in rope_plan_calc_aspects
    # assert plan_concept_laborlink_str() in rope_plan_calc_aspects
    # assert len(rope_plan_calc_aspects) == 6
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
        debt_score_str(),
        "_fund_agenda_ratio_take",
        "_inallocable_debt_score",
        "_fund_agenda_ratio_give",
        "_fund_agenda_take",
        "_fund_take",
        "_debtor_pool",
        "_irrational_debt_score",
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
        concept_rope_str(),
        begin_str(),
    }
    assert plan_groupunit_args == {
        vow_label_str(),
        owner_name_str(),
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
    plnacct = plan_acctunit_str()
    plnmemb = plan_acct_membership_str()
    plnconc = plan_conceptunit_str()
    plnawar = plan_concept_awardlink_str()
    plnreas = plan_concept_reasonunit_str()
    plnprem = plan_concept_reason_premiseunit_str()
    plnlabo = plan_concept_laborlink_str()
    plnheal = plan_concept_healerlink_str()
    plnfact = plan_concept_factunit_str()
    plngrou = plan_groupunit_str()
    assert g_class_type(cfig, plnmemb, jk, acct_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, plnmemb, jk, acct_name_str()) == "TEXT"
    assert g_class_type(cfig, plnmemb, jk, group_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, plnmemb, jk, group_title_str()) == "TEXT"
    assert g_class_type(cfig, plnmemb, jm, _credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, plnmemb, jm, _credor_pool_str()) == "REAL"
    assert g_class_type(cfig, plnmemb, jm, _debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, plnmemb, jm, _debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, plnmemb, jm, _fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, plnmemb, jm, _fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, plnmemb, jm, _fund_agenda_ratio_give_str()) == "float"
    assert g_sqlitetype(cfig, plnmemb, jm, _fund_agenda_ratio_give_str()) == "REAL"
    assert g_class_type(cfig, plnmemb, jm, _fund_agenda_ratio_take_str()) == "float"
    assert g_sqlitetype(cfig, plnmemb, jm, _fund_agenda_ratio_take_str()) == "REAL"
    assert g_class_type(cfig, plnmemb, jm, _fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, plnmemb, jm, _fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, plnmemb, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, plnmemb, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, plnmemb, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, plnmemb, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, plnmemb, jv, credit_vote_str()) == "float"
    assert g_sqlitetype(cfig, plnmemb, jv, credit_vote_str()) == "REAL"
    assert g_class_type(cfig, plnmemb, jv, debt_vote_str()) == "float"
    assert g_sqlitetype(cfig, plnmemb, jv, debt_vote_str()) == "REAL"
    assert g_class_type(cfig, plnacct, jk, acct_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, plnacct, jk, acct_name_str()) == "TEXT"
    assert g_class_type(cfig, plnacct, jm, _credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, plnacct, jm, _credor_pool_str()) == "REAL"
    assert g_class_type(cfig, plnacct, jm, _debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, plnacct, jm, _debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, plnacct, jm, _fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, plnacct, jm, _fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, plnacct, jm, _fund_agenda_ratio_give_str()) == "float"
    assert g_sqlitetype(cfig, plnacct, jm, _fund_agenda_ratio_give_str()) == "REAL"
    assert g_class_type(cfig, plnacct, jm, _fund_agenda_ratio_take_str()) == "float"
    assert g_sqlitetype(cfig, plnacct, jm, _fund_agenda_ratio_take_str()) == "REAL"
    assert g_class_type(cfig, plnacct, jm, _fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, plnacct, jm, _fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, plnacct, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, plnacct, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, plnacct, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, plnacct, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, plnacct, jm, _inallocable_debt_score_str()) == "float"
    assert g_sqlitetype(cfig, plnacct, jm, _inallocable_debt_score_str()) == "REAL"
    assert g_class_type(cfig, plnacct, jm, _irrational_debt_score_str()) == "float"
    assert g_sqlitetype(cfig, plnacct, jm, _irrational_debt_score_str()) == "REAL"
    assert g_class_type(cfig, plnacct, jv, credit_score_str()) == "float"
    assert g_sqlitetype(cfig, plnacct, jv, credit_score_str()) == "REAL"
    assert g_class_type(cfig, plnacct, jv, debt_score_str()) == "float"
    assert g_sqlitetype(cfig, plnacct, jv, debt_score_str()) == "REAL"

    assert g_class_type(cfig, plngrou, jk, group_title_str()) == "TitleTerm"
    assert g_sqlitetype(cfig, plngrou, jk, group_title_str()) == "TEXT"
    assert g_class_type(cfig, plngrou, jv, knot_str()) == "str"
    assert g_sqlitetype(cfig, plngrou, jv, knot_str()) == "TEXT"
    assert g_class_type(cfig, plngrou, jm, _debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, plngrou, jm, _debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, plngrou, jm, _credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, plngrou, jm, _credor_pool_str()) == "REAL"
    assert g_class_type(cfig, plngrou, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, plngrou, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, plngrou, jm, _fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, plngrou, jm, _fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, plngrou, jm, _fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, plngrou, jm, _fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, plngrou, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, plngrou, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, plngrou, jm, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, plngrou, jm, fund_iota_str()) == "REAL"

    assert g_class_type(cfig, plnawar, jk, awardee_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, plnawar, jk, awardee_title_str()) == "TEXT"
    assert g_class_type(cfig, plnawar, jk, concept_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, plnawar, jk, concept_rope_str()) == "TEXT"
    assert g_class_type(cfig, plnawar, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, plnawar, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, plnawar, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, plnawar, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, plnawar, jv, give_force_str()) == "float"
    assert g_sqlitetype(cfig, plnawar, jv, give_force_str()) == "REAL"
    assert g_class_type(cfig, plnawar, jv, take_force_str()) == "float"
    assert g_sqlitetype(cfig, plnawar, jv, take_force_str()) == "REAL"
    assert g_class_type(cfig, plnfact, jk, fcontext_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, plnfact, jk, fcontext_str()) == "TEXT"
    assert g_class_type(cfig, plnfact, jk, concept_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, plnfact, jk, concept_rope_str()) == "TEXT"
    assert g_class_type(cfig, plnfact, jv, fnigh_str()) == "float"
    assert g_sqlitetype(cfig, plnfact, jv, fnigh_str()) == "REAL"
    assert g_class_type(cfig, plnfact, jv, fopen_str()) == "float"
    assert g_sqlitetype(cfig, plnfact, jv, fopen_str()) == "REAL"
    assert g_class_type(cfig, plnfact, jv, fstate_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, plnfact, jv, fstate_str()) == "TEXT"
    assert g_class_type(cfig, plnheal, jk, healer_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, plnheal, jk, healer_name_str()) == "TEXT"
    assert g_class_type(cfig, plnheal, jk, concept_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, plnheal, jk, concept_rope_str()) == "TEXT"
    assert g_class_type(cfig, plnprem, jk, rcontext_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, plnprem, jk, rcontext_str()) == "TEXT"
    assert g_class_type(cfig, plnprem, jk, pstate_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, plnprem, jk, pstate_str()) == "TEXT"
    assert g_class_type(cfig, plnprem, jk, concept_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, plnprem, jk, concept_rope_str()) == "TEXT"
    assert g_class_type(cfig, plnprem, jm, _status_str()) == "int"
    assert g_sqlitetype(cfig, plnprem, jm, _status_str()) == "INTEGER"
    assert g_class_type(cfig, plnprem, jm, _chore_str()) == "int"
    assert g_sqlitetype(cfig, plnprem, jm, _chore_str()) == "INTEGER"
    assert g_class_type(cfig, plnprem, jv, pdivisor_str()) == "int"
    assert g_sqlitetype(cfig, plnprem, jv, pdivisor_str()) == "INTEGER"
    assert g_class_type(cfig, plnprem, jv, pnigh_str()) == "float"
    assert g_sqlitetype(cfig, plnprem, jv, pnigh_str()) == "REAL"
    assert g_class_type(cfig, plnprem, jv, popen_str()) == "float"
    assert g_sqlitetype(cfig, plnprem, jv, popen_str()) == "REAL"
    assert g_class_type(cfig, plnreas, jk, rcontext_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, plnreas, jk, rcontext_str()) == "TEXT"
    assert g_class_type(cfig, plnreas, jk, concept_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, plnreas, jk, concept_rope_str()) == "TEXT"
    assert g_class_type(cfig, plnreas, jm, "_rconcept_active_value") == "int"
    assert g_sqlitetype(cfig, plnreas, jm, "_rconcept_active_value") == "INTEGER"
    assert g_class_type(cfig, plnreas, jm, _status_str()) == "int"
    assert g_sqlitetype(cfig, plnreas, jm, _status_str()) == "INTEGER"
    assert g_class_type(cfig, plnreas, jm, _chore_str()) == "int"
    assert g_sqlitetype(cfig, plnreas, jm, _chore_str()) == "INTEGER"
    assert g_class_type(cfig, plnreas, jv, rconcept_active_requisite_str()) == "bool"
    assert g_sqlitetype(cfig, plnreas, jv, rconcept_active_requisite_str()) == "INTEGER"
    assert g_class_type(cfig, plnlabo, jk, concept_rope_str()) == RopeTerm_str()
    assert g_sqlitetype(cfig, plnlabo, jk, concept_rope_str()) == "TEXT"
    assert g_class_type(cfig, plnlabo, jk, labor_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, plnlabo, jk, labor_title_str()) == "TEXT"
    assert g_class_type(cfig, plnlabo, jm, "_owner_name_labor") == "int"
    assert g_sqlitetype(cfig, plnlabo, jm, "_owner_name_labor") == "INTEGER"
    assert g_class_type(cfig, plnconc, jm, "_active") == "int"
    assert g_sqlitetype(cfig, plnconc, jm, "_active") == "INTEGER"
    assert g_class_type(cfig, plnconc, jm, _all_acct_cred_str()) == "int"
    assert g_sqlitetype(cfig, plnconc, jm, _all_acct_cred_str()) == "INTEGER"
    assert g_class_type(cfig, plnconc, jm, _all_acct_debt_str()) == "int"
    assert g_sqlitetype(cfig, plnconc, jm, _all_acct_debt_str()) == "INTEGER"
    assert g_class_type(cfig, plnconc, jm, _descendant_task_count_str()) == "int"
    assert g_sqlitetype(cfig, plnconc, jm, _descendant_task_count_str()) == "INTEGER"
    assert g_class_type(cfig, plnconc, jm, _fund_cease_str()) == "float"
    assert g_sqlitetype(cfig, plnconc, jm, _fund_cease_str()) == "REAL"
    assert g_class_type(cfig, plnconc, jm, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, plnconc, jm, fund_iota_str()) == "REAL"
    assert g_class_type(cfig, plnconc, jm, _fund_onset_str()) == "float"
    assert g_sqlitetype(cfig, plnconc, jm, _fund_onset_str()) == "REAL"
    assert g_class_type(cfig, plnconc, jm, _fund_ratio_str()) == "float"
    assert g_sqlitetype(cfig, plnconc, jm, _fund_ratio_str()) == "REAL"
    assert g_class_type(cfig, plnconc, jm, _gogo_calc_str()) == "float"
    assert g_sqlitetype(cfig, plnconc, jm, _gogo_calc_str()) == "REAL"
    assert g_class_type(cfig, plnconc, jm, _healerlink_ratio_str()) == "float"
    assert g_sqlitetype(cfig, plnconc, jm, _healerlink_ratio_str()) == "REAL"
    assert g_class_type(cfig, plnconc, jm, "_level") == "int"
    assert g_sqlitetype(cfig, plnconc, jm, "_level") == "INTEGER"
    assert g_class_type(cfig, plnconc, jm, _range_evaluated_str()) == "int"
    assert g_sqlitetype(cfig, plnconc, jm, _range_evaluated_str()) == "INTEGER"
    assert g_class_type(cfig, plnconc, jm, _stop_calc_str()) == "float"
    assert g_sqlitetype(cfig, plnconc, jm, _stop_calc_str()) == "REAL"
    assert g_class_type(cfig, plnconc, jm, _chore_str()) == "int"
    assert g_sqlitetype(cfig, plnconc, jm, _chore_str()) == "INTEGER"
    assert g_class_type(cfig, plnconc, jv, addin_str()) == "float"
    assert g_sqlitetype(cfig, plnconc, jv, addin_str()) == "REAL"
    assert g_class_type(cfig, plnconc, jv, begin_str()) == "float"
    assert g_sqlitetype(cfig, plnconc, jv, begin_str()) == "REAL"
    assert g_class_type(cfig, plnconc, jv, close_str()) == "float"
    assert g_sqlitetype(cfig, plnconc, jv, close_str()) == "REAL"
    assert g_class_type(cfig, plnconc, jv, denom_str()) == "int"
    assert g_sqlitetype(cfig, plnconc, jv, denom_str()) == "INTEGER"
    assert g_class_type(cfig, plnconc, jv, gogo_want_str()) == "float"
    assert g_sqlitetype(cfig, plnconc, jv, gogo_want_str()) == "REAL"
    assert g_class_type(cfig, plnconc, jv, mass_str()) == "int"
    assert g_sqlitetype(cfig, plnconc, jv, mass_str()) == "INTEGER"
    assert g_class_type(cfig, plnconc, jv, morph_str()) == "bool"
    assert g_sqlitetype(cfig, plnconc, jv, morph_str()) == "INTEGER"
    assert g_class_type(cfig, plnconc, jv, numor_str()) == "int"
    assert g_sqlitetype(cfig, plnconc, jv, numor_str()) == "INTEGER"
    assert g_class_type(cfig, plnconc, jv, task_str()) == "bool"
    assert g_sqlitetype(cfig, plnconc, jv, task_str()) == "INTEGER"
    assert g_class_type(cfig, plnconc, jv, problem_bool_str()) == "bool"
    assert g_sqlitetype(cfig, plnconc, jv, problem_bool_str()) == "INTEGER"
    assert g_class_type(cfig, plnconc, jv, stop_want_str()) == "float"
    assert g_sqlitetype(cfig, plnconc, jv, stop_want_str()) == "REAL"
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
    assert plan_calc_args_type_dict.get(debt_vote_str()) == "int"
    assert plan_calc_args_type_dict.get(_inallocable_debt_score_str()) == "float"
    assert plan_calc_args_type_dict.get(_irrational_debt_score_str()) == "float"
    assert plan_calc_args_type_dict.get(credit_score_str()) == "float"
    assert plan_calc_args_type_dict.get(debt_score_str()) == "float"
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
    assert plan_calc_args_type_dict.get(concept_rope_str()) == RopeTerm_str()
    assert plan_calc_args_type_dict.get(give_force_str()) == "float"
    assert plan_calc_args_type_dict.get(take_force_str()) == "float"
    assert plan_calc_args_type_dict.get(rcontext_str()) == RopeTerm_str()
    assert plan_calc_args_type_dict.get(fnigh_str()) == "float"
    assert plan_calc_args_type_dict.get(fopen_str()) == "float"
    assert plan_calc_args_type_dict.get(fstate_str()) == RopeTerm_str()
    assert plan_calc_args_type_dict.get(healer_name_str()) == NameTerm_str()
    assert plan_calc_args_type_dict.get(pstate_str()) == RopeTerm_str()
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
