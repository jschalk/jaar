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
    _inallocable_debtit_belief_str,
    _irrational_debtit_belief_str,
    awardee_title_str,
    credit_belief_str,
    credit_vote_str,
    debtit_belief_str,
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
    _descendant_pledge_count_str,
    _fund_cease_str,
    _fund_onset_str,
    _fund_ratio_str,
    _gogo_calc_str,
    _healerlink_ratio_str,
    _range_evaluated_str,
    _stop_calc_str,
    mass_str,
    pledge_str,
    problem_bool_str,
)
from src.a06_bud_logic._test_util.a06_str import (
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
    bud_acct_membership_str,
    bud_acctunit_str,
    bud_concept_awardlink_str,
    bud_concept_factunit_str,
    bud_concept_healerlink_str,
    bud_concept_laborlink_str,
    bud_concept_reason_premiseunit_str,
    bud_concept_reasonunit_str,
    bud_conceptunit_str,
    budunit_str,
    close_str,
    concept_way_str,
    credit_belief_str,
    credit_vote_str,
    credor_respect_str,
    debtit_belief_str,
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
    pnigh_str,
    popen_str,
    pstate_str,
    rcontext_str,
    stop_want_str,
    tally_str,
)
from src.a08_bud_atom_logic._test_util.a08_str import (
    class_type_str,
    jkeys_str,
    jvalues_str,
    sqlite_datatype_str,
)
from src.a08_bud_atom_logic.atom_config import get_atom_config_dict
from src.a10_bud_calc._test_util.a10_str import bud_groupunit_str, jmetrics_str
from src.a10_bud_calc.bud_calc_config import (
    config_file_path,
    get_all_bud_calc_args,
    get_bud_calc_args_sqlite_datatype_dict,
    get_bud_calc_args_type_dict,
    get_bud_calc_config_dict,
    get_bud_calc_config_filename,
    get_bud_calc_dimen_args,
    get_bud_calc_dimens,
)


def test_get_bud_calc_config_dict_Exists():
    # ESTABLISH
    src_dir = create_path(os_getcwd(), "src")
    expected_dir = create_path(src_dir, "a10_bud_calc")

    # WHEN / THEN
    assert get_bud_calc_config_filename() == "bud_calc_config.json"
    expected_path = create_path(expected_dir, get_bud_calc_config_filename())
    assert config_file_path() == expected_path
    assert os_path_exists(config_file_path())


def test_get_bud_calc_config_dict_ReturnsObj_CheckLevel0Keys():
    # ESTABLISH / WHEN
    bud_calc_config = get_bud_calc_config_dict()
    bud_calc_config_keys = set(bud_calc_config.keys())

    # THEN
    assert budunit_str() in bud_calc_config_keys
    assert bud_acctunit_str() in bud_calc_config_keys
    assert bud_acct_membership_str() in bud_calc_config_keys
    assert bud_conceptunit_str() in bud_calc_config_keys
    assert bud_concept_awardlink_str() in bud_calc_config_keys
    assert bud_concept_reasonunit_str() in bud_calc_config_keys
    assert bud_concept_reason_premiseunit_str() in bud_calc_config_keys
    assert bud_concept_laborlink_str() in bud_calc_config_keys
    assert bud_concept_healerlink_str() in bud_calc_config_keys
    assert bud_concept_factunit_str() in bud_calc_config_keys
    assert bud_groupunit_str() in bud_calc_config_keys
    assert len(get_bud_calc_config_dict()) == 11
    atom_config_dict = get_atom_config_dict()
    atom_config_dimens = set(atom_config_dict.keys())
    assert atom_config_dimens.issubset(bud_calc_config_keys)
    assert bud_calc_config_keys.difference(atom_config_dimens) == {bud_groupunit_str()}


def test_get_bud_calc_config_dict_ReturnsObj_CheckLevel1Keys():
    # ESTABLISH / WHEN
    bud_calc_config = get_bud_calc_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests
    for level1_key, aspect_dict in bud_calc_config.items():
        aspect_keys = set(aspect_dict.keys())
        print(f"{level1_key=} {aspect_keys=}")
        assert "abbreviation" in aspect_keys
        assert jkeys_str() in aspect_keys
        assert jvalues_str() in aspect_keys
        assert jmetrics_str() in aspect_keys
        assert len(aspect_keys) == 4


def test_get_bud_calc_config_dict_ReturnsObj_CheckLevel2_And_Level3_Keys():
    # ESTABLISH / WHEN
    bud_calc_config = get_bud_calc_config_dict()

    # THEN
    atom_config = get_atom_config_dict()
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, aspect_dict in bud_calc_config.items():
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

    budunit_aspect = bud_calc_config.get(budunit_str())
    budacct_aspect = bud_calc_config.get(bud_acctunit_str())
    budmemb_aspect = bud_calc_config.get(bud_acct_membership_str())
    budconc_aspect = bud_calc_config.get(bud_conceptunit_str())
    budawar_aspect = bud_calc_config.get(bud_concept_awardlink_str())
    budreas_aspect = bud_calc_config.get(bud_concept_reasonunit_str())
    budprem_aspect = bud_calc_config.get(bud_concept_reason_premiseunit_str())
    budlabo_aspect = bud_calc_config.get(bud_concept_laborlink_str())
    budheal_aspect = bud_calc_config.get(bud_concept_healerlink_str())
    budfact_aspect = bud_calc_config.get(bud_concept_factunit_str())
    budgrou_aspect = bud_calc_config.get(bud_groupunit_str())

    budunit_jmetrics_keys = set(budunit_aspect.get(jmetrics_str()))
    budacct_jmetrics_keys = set(budacct_aspect.get(jmetrics_str()))
    budmemb_jmetrics_keys = set(budmemb_aspect.get(jmetrics_str()))
    budconc_jmetrics_keys = set(budconc_aspect.get(jmetrics_str()))
    budawar_jmetrics_keys = set(budawar_aspect.get(jmetrics_str()))
    budreas_jmetrics_keys = set(budreas_aspect.get(jmetrics_str()))
    budprem_jmetrics_keys = set(budprem_aspect.get(jmetrics_str()))
    budlabo_jmetrics_keys = set(budlabo_aspect.get(jmetrics_str()))
    budheal_jmetrics_keys = set(budheal_aspect.get(jmetrics_str()))
    budfact_jmetrics_keys = set(budfact_aspect.get(jmetrics_str()))
    budgrou_jmetrics_keys = set(budgrou_aspect.get(jmetrics_str()))

    expected_budunit_jmetrics_keys = {
        "_tree_traverse_count",
        "_rational",
        "_keeps_justified",
        "_keeps_buildable",
        "_sum_healerlink_share",
        "_offtrack_fund",
    }
    assert expected_budunit_jmetrics_keys == budunit_jmetrics_keys
    expected_budacct_jmetrics_keys = {
        "_credor_pool",
        "_debtor_pool",
        "_irrational_debtit_belief",
        "_inallocable_debtit_belief",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    assert expected_budacct_jmetrics_keys == budacct_jmetrics_keys
    expected_budmemb_jmetrics_keys = {
        "_credor_pool",
        "_debtor_pool",
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_agenda_ratio_give",
        "_fund_agenda_ratio_take",
    }
    assert expected_budmemb_jmetrics_keys == budmemb_jmetrics_keys
    expected_budconc_jmetrics_keys = {
        "_active",
        "_all_acct_cred",
        "_all_acct_debt",
        "_descendant_pledge_count",
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
    assert expected_budconc_jmetrics_keys == budconc_jmetrics_keys
    expected_budawar_jmetrics_keys = {"_fund_give", "_fund_take"}
    assert expected_budawar_jmetrics_keys == budawar_jmetrics_keys
    expected_budreas_jmetrics_keys = {
        "_status",
        "_chore",
        "_rconcept_active_value",
    }
    assert expected_budreas_jmetrics_keys == budreas_jmetrics_keys
    expected_budprem_jmetrics_keys = {"_status", "_chore"}
    assert expected_budprem_jmetrics_keys == budprem_jmetrics_keys
    expected_budlabo_jmetrics_keys = {"_owner_name_labor"}
    assert expected_budlabo_jmetrics_keys == budlabo_jmetrics_keys
    expected_budgrou_jmetrics_keys = {
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_credor_pool",
        "_debtor_pool",
        "fund_iota",
    }
    assert expected_budgrou_jmetrics_keys == budgrou_jmetrics_keys

    assert budunit_jmetrics_keys  # Non-empty
    assert budacct_jmetrics_keys  # Non-empty
    assert budmemb_jmetrics_keys  # Non-empty
    assert budconc_jmetrics_keys  # Non-empty
    assert budawar_jmetrics_keys  # Non-empty
    assert budreas_jmetrics_keys  # Non-empty
    assert budprem_jmetrics_keys  # Non-empty
    assert budlabo_jmetrics_keys  # Non-empty
    assert not budheal_jmetrics_keys  # empty
    assert not budfact_jmetrics_keys  # empty
    assert budgrou_jmetrics_keys  # Non-empty


def test_get_bud_calc_config_dict_ReturnsObj_CheckAbbreviations():
    # ESTABLISH / WHEN
    bud_calc_config = get_bud_calc_config_dict()

    # THEN
    budunit_aspect = bud_calc_config.get(budunit_str())
    budacct_aspect = bud_calc_config.get(bud_acctunit_str())
    budmemb_aspect = bud_calc_config.get(bud_acct_membership_str())
    budconc_aspect = bud_calc_config.get(bud_conceptunit_str())
    budawar_aspect = bud_calc_config.get(bud_concept_awardlink_str())
    budreas_aspect = bud_calc_config.get(bud_concept_reasonunit_str())
    budprem_aspect = bud_calc_config.get(bud_concept_reason_premiseunit_str())
    budlabo_aspect = bud_calc_config.get(bud_concept_laborlink_str())
    budheal_aspect = bud_calc_config.get(bud_concept_healerlink_str())
    budfact_aspect = bud_calc_config.get(bud_concept_factunit_str())
    budgrou_aspect = bud_calc_config.get(bud_groupunit_str())
    abbr_str = "abbreviation"
    assert budunit_aspect.get(abbr_str) == "budunit"
    assert budacct_aspect.get(abbr_str) == "budacct"
    assert budmemb_aspect.get(abbr_str) == "budmemb"
    assert budconc_aspect.get(abbr_str) == "budconc"
    assert budawar_aspect.get(abbr_str) == "budawar"
    assert budreas_aspect.get(abbr_str) == "budreas"
    assert budprem_aspect.get(abbr_str) == "budprem"
    assert budlabo_aspect.get(abbr_str) == "budlabo"
    assert budheal_aspect.get(abbr_str) == "budheal"
    assert budfact_aspect.get(abbr_str) == "budfact"
    assert budgrou_aspect.get(abbr_str) == "budgrou"


def test_get_all_bud_calc_args_ReturnsObj():
    # ESTABLISH / WHEN
    all_bud_calc_args = get_all_bud_calc_args()

    # THEN
    assert all_bud_calc_args
    assert stop_want_str() in all_bud_calc_args
    assert concept_way_str() in all_bud_calc_args
    assert "_fund_give" in all_bud_calc_args
    assert all_bud_calc_args.get("_fund_give") == {
        "bud_concept_awardlink",
        "bud_acct_membership",
        "bud_groupunit",
        "bud_acctunit",
    }

    # bud_calc_config = get_bud_calc_config_dict()
    # bud_acctunit_aspects = bud_calc_config.get("bud_acctunit")
    # budacct_jmetrics_dict = bud_acctunit_aspects.get("jmetrics")
    # way_bud_calc_aspects = budacct_jmetrics_dict.get("_fund_give")
    # assert bud_concept_factunit_str() in way_bud_calc_aspects
    # assert bud_concept_laborlink_str() in way_bud_calc_aspects
    # assert len(way_bud_calc_aspects) == 6
    assert len(all_bud_calc_args) == 76


def test_get_bud_calc_config_dict_ReturnsObj_CheckArgDataTypesKeysExist():
    # ESTABLISH / WHEN
    bud_calc_config = get_bud_calc_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, aspect_dict in bud_calc_config.items():
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


def test_get_bud_calc_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    bud_calc_dimens = get_bud_calc_dimens()

    # THEN
    expected_bud_calc_dimens = {
        budunit_str(),
        bud_acctunit_str(),
        bud_acct_membership_str(),
        bud_conceptunit_str(),
        bud_concept_awardlink_str(),
        bud_concept_reasonunit_str(),
        bud_concept_reason_premiseunit_str(),
        bud_concept_laborlink_str(),
        bud_concept_healerlink_str(),
        bud_concept_factunit_str(),
        bud_groupunit_str(),
    }
    assert bud_calc_dimens == expected_bud_calc_dimens
    assert bud_calc_dimens == set(get_bud_calc_config_dict().keys())


def test_get_bud_calc_dimen_args_ReturnsObj():
    # ESTABLISH / WHEN
    bud_acctunit_args = get_bud_calc_dimen_args(bud_acctunit_str())
    bud_conceptunit_args = get_bud_calc_dimen_args(bud_conceptunit_str())
    bud_groupunit_args = get_bud_calc_dimen_args(bud_groupunit_str())

    #  THEN
    print(f"{bud_acctunit_args=}")
    print(f"{bud_groupunit_args=}")
    assert bud_acctunit_args == {
        vow_label_str(),
        owner_name_str(),
        "_fund_agenda_give",
        "_credor_pool",
        "_fund_give",
        credit_belief_str(),
        acct_name_str(),
        debtit_belief_str(),
        "_fund_agenda_ratio_take",
        "_inallocable_debtit_belief",
        "_fund_agenda_ratio_give",
        "_fund_agenda_take",
        "_fund_take",
        "_debtor_pool",
        "_irrational_debtit_belief",
    }
    assert bud_conceptunit_args == {
        vow_label_str(),
        owner_name_str(),
        morph_str(),
        denom_str(),
        "pledge",
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
        "_descendant_pledge_count",
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
    assert bud_groupunit_args == {
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


def test_get_bud_calc_config_dict_ReturnsObj_CheckArgDataTypesCorrect():
    # ESTABLISH / WHEN
    cfig = get_bud_calc_config_dict()
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
    budunit = budunit_str()
    budacct = bud_acctunit_str()
    budmemb = bud_acct_membership_str()
    budconc = bud_conceptunit_str()
    budawar = bud_concept_awardlink_str()
    budreas = bud_concept_reasonunit_str()
    budprem = bud_concept_reason_premiseunit_str()
    budlabo = bud_concept_laborlink_str()
    budheal = bud_concept_healerlink_str()
    budfact = bud_concept_factunit_str()
    budgrou = bud_groupunit_str()
    assert g_class_type(cfig, budmemb, jk, acct_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, budmemb, jk, acct_name_str()) == "TEXT"
    assert g_class_type(cfig, budmemb, jk, group_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, budmemb, jk, group_title_str()) == "TEXT"
    assert g_class_type(cfig, budmemb, jm, _credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, budmemb, jm, _credor_pool_str()) == "REAL"
    assert g_class_type(cfig, budmemb, jm, _debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, budmemb, jm, _debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, budmemb, jm, _fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, budmemb, jm, _fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, budmemb, jm, _fund_agenda_ratio_give_str()) == "float"
    assert g_sqlitetype(cfig, budmemb, jm, _fund_agenda_ratio_give_str()) == "REAL"
    assert g_class_type(cfig, budmemb, jm, _fund_agenda_ratio_take_str()) == "float"
    assert g_sqlitetype(cfig, budmemb, jm, _fund_agenda_ratio_take_str()) == "REAL"
    assert g_class_type(cfig, budmemb, jm, _fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, budmemb, jm, _fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, budmemb, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, budmemb, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, budmemb, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, budmemb, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, budmemb, jv, credit_vote_str()) == "float"
    assert g_sqlitetype(cfig, budmemb, jv, credit_vote_str()) == "REAL"
    assert g_class_type(cfig, budmemb, jv, debtit_vote_str()) == "float"
    assert g_sqlitetype(cfig, budmemb, jv, debtit_vote_str()) == "REAL"
    assert g_class_type(cfig, budacct, jk, acct_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, budacct, jk, acct_name_str()) == "TEXT"
    assert g_class_type(cfig, budacct, jm, _credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, budacct, jm, _credor_pool_str()) == "REAL"
    assert g_class_type(cfig, budacct, jm, _debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, budacct, jm, _debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, budacct, jm, _fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, budacct, jm, _fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, budacct, jm, _fund_agenda_ratio_give_str()) == "float"
    assert g_sqlitetype(cfig, budacct, jm, _fund_agenda_ratio_give_str()) == "REAL"
    assert g_class_type(cfig, budacct, jm, _fund_agenda_ratio_take_str()) == "float"
    assert g_sqlitetype(cfig, budacct, jm, _fund_agenda_ratio_take_str()) == "REAL"
    assert g_class_type(cfig, budacct, jm, _fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, budacct, jm, _fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, budacct, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, budacct, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, budacct, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, budacct, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, budacct, jm, _inallocable_debtit_belief_str()) == "float"
    assert g_sqlitetype(cfig, budacct, jm, _inallocable_debtit_belief_str()) == "REAL"
    assert g_class_type(cfig, budacct, jm, _irrational_debtit_belief_str()) == "float"
    assert g_sqlitetype(cfig, budacct, jm, _irrational_debtit_belief_str()) == "REAL"
    assert g_class_type(cfig, budacct, jv, credit_belief_str()) == "float"
    assert g_sqlitetype(cfig, budacct, jv, credit_belief_str()) == "REAL"
    assert g_class_type(cfig, budacct, jv, debtit_belief_str()) == "float"
    assert g_sqlitetype(cfig, budacct, jv, debtit_belief_str()) == "REAL"

    assert g_class_type(cfig, budgrou, jk, group_title_str()) == "TitleTerm"
    assert g_sqlitetype(cfig, budgrou, jk, group_title_str()) == "TEXT"
    assert g_class_type(cfig, budgrou, jv, bridge_str()) == "str"
    assert g_sqlitetype(cfig, budgrou, jv, bridge_str()) == "TEXT"
    assert g_class_type(cfig, budgrou, jm, _debtor_pool_str()) == "float"
    assert g_sqlitetype(cfig, budgrou, jm, _debtor_pool_str()) == "REAL"
    assert g_class_type(cfig, budgrou, jm, _credor_pool_str()) == "float"
    assert g_sqlitetype(cfig, budgrou, jm, _credor_pool_str()) == "REAL"
    assert g_class_type(cfig, budgrou, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, budgrou, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, budgrou, jm, _fund_agenda_give_str()) == "float"
    assert g_sqlitetype(cfig, budgrou, jm, _fund_agenda_give_str()) == "REAL"
    assert g_class_type(cfig, budgrou, jm, _fund_agenda_take_str()) == "float"
    assert g_sqlitetype(cfig, budgrou, jm, _fund_agenda_take_str()) == "REAL"
    assert g_class_type(cfig, budgrou, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, budgrou, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, budgrou, jm, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, budgrou, jm, fund_iota_str()) == "REAL"

    assert g_class_type(cfig, budawar, jk, awardee_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, budawar, jk, awardee_title_str()) == "TEXT"
    assert g_class_type(cfig, budawar, jk, concept_way_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, budawar, jk, concept_way_str()) == "TEXT"
    assert g_class_type(cfig, budawar, jm, _fund_give_str()) == "float"
    assert g_sqlitetype(cfig, budawar, jm, _fund_give_str()) == "REAL"
    assert g_class_type(cfig, budawar, jm, _fund_take_str()) == "float"
    assert g_sqlitetype(cfig, budawar, jm, _fund_take_str()) == "REAL"
    assert g_class_type(cfig, budawar, jv, give_force_str()) == "float"
    assert g_sqlitetype(cfig, budawar, jv, give_force_str()) == "REAL"
    assert g_class_type(cfig, budawar, jv, take_force_str()) == "float"
    assert g_sqlitetype(cfig, budawar, jv, take_force_str()) == "REAL"
    assert g_class_type(cfig, budfact, jk, fcontext_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, budfact, jk, fcontext_str()) == "TEXT"
    assert g_class_type(cfig, budfact, jk, concept_way_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, budfact, jk, concept_way_str()) == "TEXT"
    assert g_class_type(cfig, budfact, jv, fnigh_str()) == "float"
    assert g_sqlitetype(cfig, budfact, jv, fnigh_str()) == "REAL"
    assert g_class_type(cfig, budfact, jv, fopen_str()) == "float"
    assert g_sqlitetype(cfig, budfact, jv, fopen_str()) == "REAL"
    assert g_class_type(cfig, budfact, jv, fstate_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, budfact, jv, fstate_str()) == "TEXT"
    assert g_class_type(cfig, budheal, jk, healer_name_str()) == NameTerm_str()
    assert g_sqlitetype(cfig, budheal, jk, healer_name_str()) == "TEXT"
    assert g_class_type(cfig, budheal, jk, concept_way_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, budheal, jk, concept_way_str()) == "TEXT"
    assert g_class_type(cfig, budprem, jk, rcontext_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, budprem, jk, rcontext_str()) == "TEXT"
    assert g_class_type(cfig, budprem, jk, pstate_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, budprem, jk, pstate_str()) == "TEXT"
    assert g_class_type(cfig, budprem, jk, concept_way_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, budprem, jk, concept_way_str()) == "TEXT"
    assert g_class_type(cfig, budprem, jm, _status_str()) == "int"
    assert g_sqlitetype(cfig, budprem, jm, _status_str()) == "INTEGER"
    assert g_class_type(cfig, budprem, jm, _chore_str()) == "int"
    assert g_sqlitetype(cfig, budprem, jm, _chore_str()) == "INTEGER"
    assert g_class_type(cfig, budprem, jv, pdivisor_str()) == "int"
    assert g_sqlitetype(cfig, budprem, jv, pdivisor_str()) == "INTEGER"
    assert g_class_type(cfig, budprem, jv, pnigh_str()) == "float"
    assert g_sqlitetype(cfig, budprem, jv, pnigh_str()) == "REAL"
    assert g_class_type(cfig, budprem, jv, popen_str()) == "float"
    assert g_sqlitetype(cfig, budprem, jv, popen_str()) == "REAL"
    assert g_class_type(cfig, budreas, jk, rcontext_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, budreas, jk, rcontext_str()) == "TEXT"
    assert g_class_type(cfig, budreas, jk, concept_way_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, budreas, jk, concept_way_str()) == "TEXT"
    assert g_class_type(cfig, budreas, jm, "_rconcept_active_value") == "int"
    assert g_sqlitetype(cfig, budreas, jm, "_rconcept_active_value") == "INTEGER"
    assert g_class_type(cfig, budreas, jm, _status_str()) == "int"
    assert g_sqlitetype(cfig, budreas, jm, _status_str()) == "INTEGER"
    assert g_class_type(cfig, budreas, jm, _chore_str()) == "int"
    assert g_sqlitetype(cfig, budreas, jm, _chore_str()) == "INTEGER"
    assert g_class_type(cfig, budreas, jv, rconcept_active_requisite_str()) == "bool"
    assert g_sqlitetype(cfig, budreas, jv, rconcept_active_requisite_str()) == "INTEGER"
    assert g_class_type(cfig, budlabo, jk, concept_way_str()) == WayTerm_str()
    assert g_sqlitetype(cfig, budlabo, jk, concept_way_str()) == "TEXT"
    assert g_class_type(cfig, budlabo, jk, labor_title_str()) == TitleTerm_str()
    assert g_sqlitetype(cfig, budlabo, jk, labor_title_str()) == "TEXT"
    assert g_class_type(cfig, budlabo, jm, "_owner_name_labor") == "int"
    assert g_sqlitetype(cfig, budlabo, jm, "_owner_name_labor") == "INTEGER"
    assert g_class_type(cfig, budconc, jm, "_active") == "int"
    assert g_sqlitetype(cfig, budconc, jm, "_active") == "INTEGER"
    assert g_class_type(cfig, budconc, jm, _all_acct_cred_str()) == "int"
    assert g_sqlitetype(cfig, budconc, jm, _all_acct_cred_str()) == "INTEGER"
    assert g_class_type(cfig, budconc, jm, _all_acct_debt_str()) == "int"
    assert g_sqlitetype(cfig, budconc, jm, _all_acct_debt_str()) == "INTEGER"
    assert g_class_type(cfig, budconc, jm, _descendant_pledge_count_str()) == "int"
    assert g_sqlitetype(cfig, budconc, jm, _descendant_pledge_count_str()) == "INTEGER"
    assert g_class_type(cfig, budconc, jm, _fund_cease_str()) == "float"
    assert g_sqlitetype(cfig, budconc, jm, _fund_cease_str()) == "REAL"
    assert g_class_type(cfig, budconc, jm, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, budconc, jm, fund_iota_str()) == "REAL"
    assert g_class_type(cfig, budconc, jm, _fund_onset_str()) == "float"
    assert g_sqlitetype(cfig, budconc, jm, _fund_onset_str()) == "REAL"
    assert g_class_type(cfig, budconc, jm, _fund_ratio_str()) == "float"
    assert g_sqlitetype(cfig, budconc, jm, _fund_ratio_str()) == "REAL"
    assert g_class_type(cfig, budconc, jm, _gogo_calc_str()) == "float"
    assert g_sqlitetype(cfig, budconc, jm, _gogo_calc_str()) == "REAL"
    assert g_class_type(cfig, budconc, jm, _healerlink_ratio_str()) == "float"
    assert g_sqlitetype(cfig, budconc, jm, _healerlink_ratio_str()) == "REAL"
    assert g_class_type(cfig, budconc, jm, "_level") == "int"
    assert g_sqlitetype(cfig, budconc, jm, "_level") == "INTEGER"
    assert g_class_type(cfig, budconc, jm, _range_evaluated_str()) == "int"
    assert g_sqlitetype(cfig, budconc, jm, _range_evaluated_str()) == "INTEGER"
    assert g_class_type(cfig, budconc, jm, _stop_calc_str()) == "float"
    assert g_sqlitetype(cfig, budconc, jm, _stop_calc_str()) == "REAL"
    assert g_class_type(cfig, budconc, jm, _chore_str()) == "int"
    assert g_sqlitetype(cfig, budconc, jm, _chore_str()) == "INTEGER"
    assert g_class_type(cfig, budconc, jv, addin_str()) == "float"
    assert g_sqlitetype(cfig, budconc, jv, addin_str()) == "REAL"
    assert g_class_type(cfig, budconc, jv, begin_str()) == "float"
    assert g_sqlitetype(cfig, budconc, jv, begin_str()) == "REAL"
    assert g_class_type(cfig, budconc, jv, close_str()) == "float"
    assert g_sqlitetype(cfig, budconc, jv, close_str()) == "REAL"
    assert g_class_type(cfig, budconc, jv, denom_str()) == "int"
    assert g_sqlitetype(cfig, budconc, jv, denom_str()) == "INTEGER"
    assert g_class_type(cfig, budconc, jv, gogo_want_str()) == "float"
    assert g_sqlitetype(cfig, budconc, jv, gogo_want_str()) == "REAL"
    assert g_class_type(cfig, budconc, jv, mass_str()) == "int"
    assert g_sqlitetype(cfig, budconc, jv, mass_str()) == "INTEGER"
    assert g_class_type(cfig, budconc, jv, morph_str()) == "bool"
    assert g_sqlitetype(cfig, budconc, jv, morph_str()) == "INTEGER"
    assert g_class_type(cfig, budconc, jv, numor_str()) == "int"
    assert g_sqlitetype(cfig, budconc, jv, numor_str()) == "INTEGER"
    assert g_class_type(cfig, budconc, jv, pledge_str()) == "bool"
    assert g_sqlitetype(cfig, budconc, jv, pledge_str()) == "INTEGER"
    assert g_class_type(cfig, budconc, jv, problem_bool_str()) == "bool"
    assert g_sqlitetype(cfig, budconc, jv, problem_bool_str()) == "INTEGER"
    assert g_class_type(cfig, budconc, jv, stop_want_str()) == "float"
    assert g_sqlitetype(cfig, budconc, jv, stop_want_str()) == "REAL"
    assert g_class_type(cfig, budunit, jm, "_keeps_buildable") == "int"
    assert g_sqlitetype(cfig, budunit, jm, "_keeps_buildable") == "INTEGER"
    assert g_class_type(cfig, budunit, jm, "_keeps_justified") == "int"
    assert g_sqlitetype(cfig, budunit, jm, "_keeps_justified") == "INTEGER"
    assert g_class_type(cfig, budunit, jm, _offtrack_fund_str()) == "float"
    assert g_sqlitetype(cfig, budunit, jm, _offtrack_fund_str()) == "REAL"
    assert g_class_type(cfig, budunit, jm, _rational_str()) == "bool"
    assert g_sqlitetype(cfig, budunit, jm, _rational_str()) == "INTEGER"
    assert g_class_type(cfig, budunit, jm, _sum_healerlink_share_str()) == "float"
    assert g_sqlitetype(cfig, budunit, jm, _sum_healerlink_share_str()) == "REAL"
    assert g_class_type(cfig, budunit, jm, _tree_traverse_count_str()) == "int"
    assert g_sqlitetype(cfig, budunit, jm, _tree_traverse_count_str()) == "INTEGER"
    assert g_class_type(cfig, budunit, jv, credor_respect_str()) == "float"
    assert g_sqlitetype(cfig, budunit, jv, credor_respect_str()) == "REAL"
    assert g_class_type(cfig, budunit, jv, debtor_respect_str()) == "float"
    assert g_sqlitetype(cfig, budunit, jv, debtor_respect_str()) == "REAL"
    assert g_class_type(cfig, budunit, jv, fund_iota_str()) == "float"
    assert g_sqlitetype(cfig, budunit, jv, fund_iota_str()) == "REAL"
    assert g_class_type(cfig, budunit, jv, fund_pool_str()) == "float"
    assert g_sqlitetype(cfig, budunit, jv, fund_pool_str()) == "REAL"
    assert g_class_type(cfig, budunit, jv, max_tree_traverse_str()) == "int"
    assert g_sqlitetype(cfig, budunit, jv, max_tree_traverse_str()) == "INTEGER"
    assert g_class_type(cfig, budunit, jv, penny_str()) == "float"
    assert g_sqlitetype(cfig, budunit, jv, penny_str()) == "REAL"
    assert g_class_type(cfig, budunit, jv, respect_bit_str()) == "float"
    assert g_sqlitetype(cfig, budunit, jv, respect_bit_str()) == "REAL"
    assert g_class_type(cfig, budunit, jv, tally_str()) == "int"
    assert g_sqlitetype(cfig, budunit, jv, tally_str()) == "INTEGER"


def test_get_bud_calc_config_dict_ReturnsObj_EachArgHasOneClassType():
    # ESTABLISH
    bud_calc_config_dict = get_bud_calc_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for bud_calc_dimen, dimen_dict in bud_calc_config_dict.items():
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


def test_get_bud_calc_config_dict_ReturnsObj_EachArgHasOne_sqlite_datatype():
    # ESTABLISH
    bud_calc_config_dict = get_bud_calc_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for bud_calc_dimen, dimen_dict in bud_calc_config_dict.items():
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
    sqlite_datatype_dict = get_bud_calc_args_sqlite_datatype_dict()

    # THEN
    for x_arg, arg_types in all_args.items():
        # print(
        #     f"""assert bud_calc_args_type_dict.get("{x_arg}") == "{list(arg_types)[0]}" """
        # )
        print(f""""{x_arg}": "{list(arg_types)[0]}",""")
        assert list(arg_types)[0] == sqlite_datatype_dict.get(x_arg)


def test_get_bud_calc_args_type_dict_ReturnsObj():
    # ESTABLISH
    bud_calc_config_dict = get_bud_calc_config_dict()
    all_args = {}
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for bud_calc_dimen, dimen_dict in bud_calc_config_dict.items():
        for dimen_key, args_dict in dimen_dict.items():
            if dimen_key in {"jkeys", "jvalues", "jmetrics"}:
                for x_arg, arg_dict in args_dict.items():
                    arg_type = arg_dict.get(class_type_str())
                    if all_args.get(x_arg) is None:
                        all_args[x_arg] = set()
                    all_args.get(x_arg).add(arg_type)

    # WHEN
    bud_calc_args_type_dict = get_bud_calc_args_type_dict()

    # THEN
    assert bud_calc_args_type_dict.get(acct_name_str()) == NameTerm_str()
    assert bud_calc_args_type_dict.get(group_title_str()) == TitleTerm_str()
    assert bud_calc_args_type_dict.get(_credor_pool_str()) == "float"
    assert bud_calc_args_type_dict.get(_debtor_pool_str()) == "float"
    assert bud_calc_args_type_dict.get(_fund_agenda_give_str()) == "float"
    assert bud_calc_args_type_dict.get(_fund_agenda_ratio_give_str()) == "float"
    assert bud_calc_args_type_dict.get(_fund_agenda_ratio_take_str()) == "float"
    assert bud_calc_args_type_dict.get(_fund_agenda_take_str()) == "float"
    assert bud_calc_args_type_dict.get(_fund_give_str()) == "float"
    assert bud_calc_args_type_dict.get(_fund_take_str()) == "float"
    assert bud_calc_args_type_dict.get(credit_vote_str()) == "int"
    assert bud_calc_args_type_dict.get(debtit_vote_str()) == "int"
    assert bud_calc_args_type_dict.get(_inallocable_debtit_belief_str()) == "float"
    assert bud_calc_args_type_dict.get(_irrational_debtit_belief_str()) == "float"
    assert bud_calc_args_type_dict.get(credit_belief_str()) == "float"
    assert bud_calc_args_type_dict.get(debtit_belief_str()) == "float"
    assert bud_calc_args_type_dict.get(addin_str()) == "float"
    assert bud_calc_args_type_dict.get(begin_str()) == "float"
    assert bud_calc_args_type_dict.get(close_str()) == "float"
    assert bud_calc_args_type_dict.get(denom_str()) == "int"
    assert bud_calc_args_type_dict.get(gogo_want_str()) == "float"
    assert bud_calc_args_type_dict.get(mass_str()) == "int"
    assert bud_calc_args_type_dict.get(morph_str()) == "bool"
    assert bud_calc_args_type_dict.get(numor_str()) == "int"
    assert bud_calc_args_type_dict.get(pledge_str()) == "bool"
    assert bud_calc_args_type_dict.get(problem_bool_str()) == "bool"
    assert bud_calc_args_type_dict.get(stop_want_str()) == "float"
    assert bud_calc_args_type_dict.get(awardee_title_str()) == TitleTerm_str()
    assert bud_calc_args_type_dict.get(concept_way_str()) == WayTerm_str()
    assert bud_calc_args_type_dict.get(give_force_str()) == "float"
    assert bud_calc_args_type_dict.get(take_force_str()) == "float"
    assert bud_calc_args_type_dict.get(rcontext_str()) == WayTerm_str()
    assert bud_calc_args_type_dict.get(fnigh_str()) == "float"
    assert bud_calc_args_type_dict.get(fopen_str()) == "float"
    assert bud_calc_args_type_dict.get(fstate_str()) == WayTerm_str()
    assert bud_calc_args_type_dict.get(healer_name_str()) == NameTerm_str()
    assert bud_calc_args_type_dict.get(pstate_str()) == WayTerm_str()
    assert bud_calc_args_type_dict.get("_status") == "int"
    assert bud_calc_args_type_dict.get("_chore") == "int"
    assert bud_calc_args_type_dict.get(pdivisor_str()) == "int"
    assert bud_calc_args_type_dict.get(pnigh_str()) == "float"
    assert bud_calc_args_type_dict.get(popen_str()) == "float"
    assert bud_calc_args_type_dict.get("_rconcept_active_value") == "int"
    assert bud_calc_args_type_dict.get("rconcept_active_requisite") == "bool"
    assert bud_calc_args_type_dict.get(labor_title_str()) == TitleTerm_str()
    assert bud_calc_args_type_dict.get("_owner_name_labor") == "int"
    assert bud_calc_args_type_dict.get("_active") == "int"
    assert bud_calc_args_type_dict.get(_all_acct_cred_str()) == "int"
    assert bud_calc_args_type_dict.get(_all_acct_debt_str()) == "int"
    assert bud_calc_args_type_dict.get(_descendant_pledge_count_str()) == "int"
    assert bud_calc_args_type_dict.get(_fund_cease_str()) == "float"
    assert bud_calc_args_type_dict.get(_fund_onset_str()) == "float"
    assert bud_calc_args_type_dict.get(_fund_ratio_str()) == "float"
    assert bud_calc_args_type_dict.get(_gogo_calc_str()) == "float"
    assert bud_calc_args_type_dict.get("_healerlink_ratio") == "float"
    assert bud_calc_args_type_dict.get("_level") == "int"
    assert bud_calc_args_type_dict.get(_range_evaluated_str()) == "int"
    assert bud_calc_args_type_dict.get(_stop_calc_str()) == "float"
    assert bud_calc_args_type_dict.get("_keeps_buildable") == "int"
    assert bud_calc_args_type_dict.get("_keeps_justified") == "int"
    assert bud_calc_args_type_dict.get(_offtrack_fund_str()) == "int"
    assert bud_calc_args_type_dict.get(_rational_str()) == "bool"
    assert bud_calc_args_type_dict.get(_sum_healerlink_share_str()) == "float"
    assert bud_calc_args_type_dict.get(_tree_traverse_count_str()) == "int"
    assert bud_calc_args_type_dict.get(credor_respect_str()) == "float"
    assert bud_calc_args_type_dict.get(debtor_respect_str()) == "float"
    assert bud_calc_args_type_dict.get(fund_iota_str()) == "float"
    assert bud_calc_args_type_dict.get(fund_pool_str()) == "float"
    assert bud_calc_args_type_dict.get(max_tree_traverse_str()) == "int"
    assert bud_calc_args_type_dict.get(penny_str()) == "float"
    assert bud_calc_args_type_dict.get(respect_bit_str()) == "float"
    assert bud_calc_args_type_dict.get(tally_str()) == "int"
    assert len(bud_calc_args_type_dict) == 72
