# from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._utils.strs_a02 import (
    fisc_word_str,
    owner_name_str,
    world_id_str,
)
from src.a06_bud_logic._utils.str_a06 import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_awardlink_str,
    bud_idea_reasonunit_str,
    bud_idea_reason_premiseunit_str,
    bud_idea_laborlink_str,
    bud_idea_healerlink_str,
    bud_idea_factunit_str,
    bud_groupunit_str,
    acct_name_str,
    addin_str,
    awardee_label_str,
    rcontext_str,
    begin_str,
    close_str,
    credit_belief_str,
    credor_respect_str,
    credit_vote_str,
    debtit_belief_str,
    debtor_respect_str,
    debtit_vote_str,
    denom_str,
    fcontext_str,
    fbranch_str,
    fnigh_str,
    fopen_str,
    fund_coin_str,
    gogo_want_str,
    group_label_str,
    healer_name_str,
    morph_str,
    pbranch_str,
    pnigh_str,
    numor_str,
    popen_str,
    penny_str,
    respect_bit_str,
    idea_way_str,
    stop_want_str,
    type_NameStr_str,
    type_LabelStr_str,
    type_WordStr_str,
    type_WayStr_str,
)
from src.a08_bud_atom_logic._utils.str_a08 import (
    class_type_str,
    jkeys_str,
    jvalues_str,
    sqlite_datatype_str,
)
from src.a08_bud_atom_logic.atom_config import get_atom_config_dict
from src.a10_bud_calc._utils.str_a10 import (
    jmetrics_str,
    fund_take_str,
    fund_give_str,
)
from src.a10_bud_calc.bud_calc_config import (
    get_bud_calc_config_filename,
    config_file_path,
    get_bud_calc_config_dict,
    get_bud_calc_dimen_args,
    get_all_bud_calc_args,
    get_bud_calc_args_type_dict,
    get_bud_calc_dimens,
    get_bud_calc_args_sqlite_datatype_dict,
)
from os.path import exists as os_path_exists
from os import getcwd as os_getcwd


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert jmetrics_str() == "jmetrics"
    assert fund_take_str() == "fund_take"
    assert fund_give_str() == "fund_give"


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
    assert bud_ideaunit_str() in bud_calc_config_keys
    assert bud_idea_awardlink_str() in bud_calc_config_keys
    assert bud_idea_reasonunit_str() in bud_calc_config_keys
    assert bud_idea_reason_premiseunit_str() in bud_calc_config_keys
    assert bud_idea_laborlink_str() in bud_calc_config_keys
    assert bud_idea_healerlink_str() in bud_calc_config_keys
    assert bud_idea_factunit_str() in bud_calc_config_keys
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
                    dimen_keys.add(world_id_str())
                    dimen_keys.add(fisc_word_str())
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
    budidea_aspect = bud_calc_config.get(bud_ideaunit_str())
    budawar_aspect = bud_calc_config.get(bud_idea_awardlink_str())
    budreas_aspect = bud_calc_config.get(bud_idea_reasonunit_str())
    budprem_aspect = bud_calc_config.get(bud_idea_reason_premiseunit_str())
    budlabor_aspect = bud_calc_config.get(bud_idea_laborlink_str())
    budheal_aspect = bud_calc_config.get(bud_idea_healerlink_str())
    budfact_aspect = bud_calc_config.get(bud_idea_factunit_str())
    budgrou_aspect = bud_calc_config.get(bud_groupunit_str())

    budunit_jmetrics_keys = set(budunit_aspect.get(jmetrics_str()))
    budacct_jmetrics_keys = set(budacct_aspect.get(jmetrics_str()))
    budmemb_jmetrics_keys = set(budmemb_aspect.get(jmetrics_str()))
    budidea_jmetrics_keys = set(budidea_aspect.get(jmetrics_str()))
    budawar_jmetrics_keys = set(budawar_aspect.get(jmetrics_str()))
    budreas_jmetrics_keys = set(budreas_aspect.get(jmetrics_str()))
    budprem_jmetrics_keys = set(budprem_aspect.get(jmetrics_str()))
    budlabor_jmetrics_keys = set(budlabor_aspect.get(jmetrics_str()))
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
    expected_budidea_jmetrics_keys = {
        "_active",
        "_all_acct_cred",
        "_all_acct_debt",
        "_descendant_pledge_count",
        "_fund_ratio",
        "fund_coin",
        "_fund_onset",
        "_fund_cease",
        "_healerlink_ratio",
        "_level",
        "_range_evaluated",
        "_task",
        "_gogo_calc",
        "_stop_calc",
    }
    assert expected_budidea_jmetrics_keys == budidea_jmetrics_keys
    expected_budawar_jmetrics_keys = {"_fund_give", "_fund_take"}
    assert expected_budawar_jmetrics_keys == budawar_jmetrics_keys
    expected_budreas_jmetrics_keys = {"_status", "_task", "_rcontext_idea_active_value"}
    assert expected_budreas_jmetrics_keys == budreas_jmetrics_keys
    expected_budprem_jmetrics_keys = {"_status", "_task"}
    assert expected_budprem_jmetrics_keys == budprem_jmetrics_keys
    expected_budlabor_jmetrics_keys = {"_owner_name_labor"}
    assert expected_budlabor_jmetrics_keys == budlabor_jmetrics_keys
    expected_budgrou_jmetrics_keys = {
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_credor_pool",
        "_debtor_pool",
        "fund_coin",
    }
    assert expected_budgrou_jmetrics_keys == budgrou_jmetrics_keys

    assert budunit_jmetrics_keys  # Non-empty
    assert budacct_jmetrics_keys  # Non-empty
    assert budmemb_jmetrics_keys  # Non-empty
    assert budidea_jmetrics_keys  # Non-empty
    assert budawar_jmetrics_keys  # Non-empty
    assert budreas_jmetrics_keys  # Non-empty
    assert budprem_jmetrics_keys  # Non-empty
    assert budlabor_jmetrics_keys  # Non-empty
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
    budidea_aspect = bud_calc_config.get(bud_ideaunit_str())
    budawar_aspect = bud_calc_config.get(bud_idea_awardlink_str())
    budreas_aspect = bud_calc_config.get(bud_idea_reasonunit_str())
    budprem_aspect = bud_calc_config.get(bud_idea_reason_premiseunit_str())
    budlabor_aspect = bud_calc_config.get(bud_idea_laborlink_str())
    budheal_aspect = bud_calc_config.get(bud_idea_healerlink_str())
    budfact_aspect = bud_calc_config.get(bud_idea_factunit_str())
    budgrou_aspect = bud_calc_config.get(bud_groupunit_str())
    abbr_str = "abbreviation"
    assert budunit_aspect.get(abbr_str) == "budunit"
    assert budacct_aspect.get(abbr_str) == "budacct"
    assert budmemb_aspect.get(abbr_str) == "budmemb"
    assert budidea_aspect.get(abbr_str) == "budidea"
    assert budawar_aspect.get(abbr_str) == "budawar"
    assert budreas_aspect.get(abbr_str) == "budreas"
    assert budprem_aspect.get(abbr_str) == "budprem"
    assert budlabor_aspect.get(abbr_str) == "budlabo"
    assert budheal_aspect.get(abbr_str) == "budheal"
    assert budfact_aspect.get(abbr_str) == "budfact"
    assert budgrou_aspect.get(abbr_str) == "budgrou"


def test_get_all_bud_calc_args_ReturnsObj():
    # ESTABLISH / WHEN
    all_bud_calc_args = get_all_bud_calc_args()

    # THEN
    assert all_bud_calc_args
    assert stop_want_str() in all_bud_calc_args
    assert idea_way_str() in all_bud_calc_args
    assert "_fund_give" in all_bud_calc_args
    assert all_bud_calc_args.get("_fund_give") == {
        "bud_idea_awardlink",
        "bud_acct_membership",
        "bud_groupunit",
        "bud_acctunit",
    }

    # bud_calc_config = get_bud_calc_config_dict()
    # bud_acctunit_aspects = bud_calc_config.get("bud_acctunit")
    # budacct_jmetrics_dict = bud_acctunit_aspects.get("jmetrics")
    # way_bud_calc_aspects = budacct_jmetrics_dict.get("_fund_give")
    # assert bud_idea_factunit_str() in way_bud_calc_aspects
    # assert bud_idea_laborlink_str() in way_bud_calc_aspects
    # assert len(way_bud_calc_aspects) == 6
    assert len(all_bud_calc_args) == 77


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
        bud_ideaunit_str(),
        bud_idea_awardlink_str(),
        bud_idea_reasonunit_str(),
        bud_idea_reason_premiseunit_str(),
        bud_idea_laborlink_str(),
        bud_idea_healerlink_str(),
        bud_idea_factunit_str(),
        bud_groupunit_str(),
    }
    assert bud_calc_dimens == expected_bud_calc_dimens
    assert bud_calc_dimens == set(get_bud_calc_config_dict().keys())


def test_get_bud_calc_dimen_args_ReturnsObj():
    # ESTABLISH / WHEN
    bud_acctunit_args = get_bud_calc_dimen_args(bud_acctunit_str())
    bud_ideaunit_args = get_bud_calc_dimen_args(bud_ideaunit_str())
    bud_groupunit_args = get_bud_calc_dimen_args(bud_groupunit_str())

    #  THEN
    print(f"{bud_acctunit_args=}")
    print(f"{bud_groupunit_args=}")
    assert bud_acctunit_args == {
        world_id_str(),
        fisc_word_str(),
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
    assert bud_ideaunit_args == {
        world_id_str(),
        fisc_word_str(),
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
        "_task",
        "fund_coin",
        "_fund_ratio",
        "_range_evaluated",
        "problem_bool",
        gogo_want_str(),
        idea_way_str(),
        begin_str(),
    }
    assert bud_groupunit_args == {
        world_id_str(),
        fisc_word_str(),
        owner_name_str(),
        "_debtor_pool",
        "_credor_pool",
        "_fund_give",
        "group_label",
        "bridge",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_fund_take",
        "fund_coin",
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
    config = get_bud_calc_config_dict()
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
    budidea = bud_ideaunit_str()
    budawar = bud_idea_awardlink_str()
    budreas = bud_idea_reasonunit_str()
    budprem = bud_idea_reason_premiseunit_str()
    budlabor = bud_idea_laborlink_str()
    budheal = bud_idea_healerlink_str()
    budfact = bud_idea_factunit_str()
    budgrou = bud_groupunit_str()
    assert g_class_type(config, budmemb, jk, acct_name_str()) == type_NameStr_str()
    assert g_sqlitetype(config, budmemb, jk, acct_name_str()) == "TEXT"
    assert g_class_type(config, budmemb, jk, group_label_str()) == type_LabelStr_str()
    assert g_sqlitetype(config, budmemb, jk, group_label_str()) == "TEXT"
    assert g_class_type(config, budmemb, jm, "_credor_pool") == "float"
    assert g_sqlitetype(config, budmemb, jm, "_credor_pool") == "REAL"
    assert g_class_type(config, budmemb, jm, "_debtor_pool") == "float"
    assert g_sqlitetype(config, budmemb, jm, "_debtor_pool") == "REAL"
    assert g_class_type(config, budmemb, jm, "_fund_agenda_give") == "float"
    assert g_sqlitetype(config, budmemb, jm, "_fund_agenda_give") == "REAL"
    assert g_class_type(config, budmemb, jm, "_fund_agenda_ratio_give") == "float"
    assert g_sqlitetype(config, budmemb, jm, "_fund_agenda_ratio_give") == "REAL"
    assert g_class_type(config, budmemb, jm, "_fund_agenda_ratio_take") == "float"
    assert g_sqlitetype(config, budmemb, jm, "_fund_agenda_ratio_take") == "REAL"
    assert g_class_type(config, budmemb, jm, "_fund_agenda_take") == "float"
    assert g_sqlitetype(config, budmemb, jm, "_fund_agenda_take") == "REAL"
    assert g_class_type(config, budmemb, jm, "_fund_give") == "float"
    assert g_sqlitetype(config, budmemb, jm, "_fund_give") == "REAL"
    assert g_class_type(config, budmemb, jm, "_fund_take") == "float"
    assert g_sqlitetype(config, budmemb, jm, "_fund_take") == "REAL"
    assert g_class_type(config, budmemb, jv, credit_vote_str()) == "float"
    assert g_sqlitetype(config, budmemb, jv, credit_vote_str()) == "REAL"
    assert g_class_type(config, budmemb, jv, debtit_vote_str()) == "float"
    assert g_sqlitetype(config, budmemb, jv, debtit_vote_str()) == "REAL"
    assert g_class_type(config, budacct, jk, acct_name_str()) == type_NameStr_str()
    assert g_sqlitetype(config, budacct, jk, acct_name_str()) == "TEXT"
    assert g_class_type(config, budacct, jm, "_credor_pool") == "float"
    assert g_sqlitetype(config, budacct, jm, "_credor_pool") == "REAL"
    assert g_class_type(config, budacct, jm, "_debtor_pool") == "float"
    assert g_sqlitetype(config, budacct, jm, "_debtor_pool") == "REAL"
    assert g_class_type(config, budacct, jm, "_fund_agenda_give") == "float"
    assert g_sqlitetype(config, budacct, jm, "_fund_agenda_give") == "REAL"
    assert g_class_type(config, budacct, jm, "_fund_agenda_ratio_give") == "float"
    assert g_sqlitetype(config, budacct, jm, "_fund_agenda_ratio_give") == "REAL"
    assert g_class_type(config, budacct, jm, "_fund_agenda_ratio_take") == "float"
    assert g_sqlitetype(config, budacct, jm, "_fund_agenda_ratio_take") == "REAL"
    assert g_class_type(config, budacct, jm, "_fund_agenda_take") == "float"
    assert g_sqlitetype(config, budacct, jm, "_fund_agenda_take") == "REAL"
    assert g_class_type(config, budacct, jm, "_fund_give") == "float"
    assert g_sqlitetype(config, budacct, jm, "_fund_give") == "REAL"
    assert g_class_type(config, budacct, jm, "_fund_take") == "float"
    assert g_sqlitetype(config, budacct, jm, "_fund_take") == "REAL"
    assert g_class_type(config, budacct, jm, "_inallocable_debtit_belief") == "float"
    assert g_sqlitetype(config, budacct, jm, "_inallocable_debtit_belief") == "REAL"
    assert g_class_type(config, budacct, jm, "_irrational_debtit_belief") == "float"
    assert g_sqlitetype(config, budacct, jm, "_irrational_debtit_belief") == "REAL"
    assert g_class_type(config, budacct, jv, credit_belief_str()) == "float"
    assert g_sqlitetype(config, budacct, jv, credit_belief_str()) == "REAL"
    assert g_class_type(config, budacct, jv, debtit_belief_str()) == "float"
    assert g_sqlitetype(config, budacct, jv, debtit_belief_str()) == "REAL"

    assert g_class_type(config, budgrou, jk, group_label_str()) == "LabelStr"
    assert g_sqlitetype(config, budgrou, jk, group_label_str()) == "TEXT"
    assert g_class_type(config, budgrou, jv, "bridge") == "str"
    assert g_sqlitetype(config, budgrou, jv, "bridge") == "TEXT"
    assert g_class_type(config, budgrou, jm, "_debtor_pool") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_debtor_pool") == "REAL"
    assert g_class_type(config, budgrou, jm, "_credor_pool") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_credor_pool") == "REAL"
    assert g_class_type(config, budgrou, jm, "_fund_give") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_fund_give") == "REAL"
    assert g_class_type(config, budgrou, jm, "_fund_agenda_give") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_fund_agenda_give") == "REAL"
    assert g_class_type(config, budgrou, jm, "_fund_agenda_take") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_fund_agenda_take") == "REAL"
    assert g_class_type(config, budgrou, jm, "_fund_take") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_fund_take") == "REAL"
    assert g_class_type(config, budgrou, jm, "fund_coin") == "float"
    assert g_sqlitetype(config, budgrou, jm, "fund_coin") == "REAL"

    assert g_class_type(config, budawar, jk, awardee_label_str()) == type_LabelStr_str()
    assert g_sqlitetype(config, budawar, jk, awardee_label_str()) == "TEXT"
    assert g_class_type(config, budawar, jk, idea_way_str()) == type_WayStr_str()
    assert g_sqlitetype(config, budawar, jk, idea_way_str()) == "TEXT"
    assert g_class_type(config, budawar, jm, "_fund_give") == "float"
    assert g_sqlitetype(config, budawar, jm, "_fund_give") == "REAL"
    assert g_class_type(config, budawar, jm, "_fund_take") == "float"
    assert g_sqlitetype(config, budawar, jm, "_fund_take") == "REAL"
    assert g_class_type(config, budawar, jv, "give_force") == "float"
    assert g_sqlitetype(config, budawar, jv, "give_force") == "REAL"
    assert g_class_type(config, budawar, jv, "take_force") == "float"
    assert g_sqlitetype(config, budawar, jv, "take_force") == "REAL"
    assert g_class_type(config, budfact, jk, fcontext_str()) == type_WayStr_str()
    assert g_sqlitetype(config, budfact, jk, fcontext_str()) == "TEXT"
    assert g_class_type(config, budfact, jk, idea_way_str()) == type_WayStr_str()
    assert g_sqlitetype(config, budfact, jk, idea_way_str()) == "TEXT"
    assert g_class_type(config, budfact, jv, fnigh_str()) == "float"
    assert g_sqlitetype(config, budfact, jv, fnigh_str()) == "REAL"
    assert g_class_type(config, budfact, jv, fopen_str()) == "float"
    assert g_sqlitetype(config, budfact, jv, fopen_str()) == "REAL"
    assert g_class_type(config, budfact, jv, fbranch_str()) == type_WayStr_str()
    assert g_sqlitetype(config, budfact, jv, fbranch_str()) == "TEXT"
    assert g_class_type(config, budheal, jk, healer_name_str()) == type_NameStr_str()
    assert g_sqlitetype(config, budheal, jk, healer_name_str()) == "TEXT"
    assert g_class_type(config, budheal, jk, idea_way_str()) == type_WayStr_str()
    assert g_sqlitetype(config, budheal, jk, idea_way_str()) == "TEXT"
    assert g_class_type(config, budprem, jk, rcontext_str()) == type_WayStr_str()
    assert g_sqlitetype(config, budprem, jk, rcontext_str()) == "TEXT"
    assert g_class_type(config, budprem, jk, pbranch_str()) == type_WayStr_str()
    assert g_sqlitetype(config, budprem, jk, pbranch_str()) == "TEXT"
    assert g_class_type(config, budprem, jk, idea_way_str()) == type_WayStr_str()
    assert g_sqlitetype(config, budprem, jk, idea_way_str()) == "TEXT"
    assert g_class_type(config, budprem, jm, "_status") == "int"
    assert g_sqlitetype(config, budprem, jm, "_status") == "INTEGER"
    assert g_class_type(config, budprem, jm, "_task") == "int"
    assert g_sqlitetype(config, budprem, jm, "_task") == "INTEGER"
    assert g_class_type(config, budprem, jv, "pdivisor") == "int"
    assert g_sqlitetype(config, budprem, jv, "pdivisor") == "INTEGER"
    assert g_class_type(config, budprem, jv, pnigh_str()) == "float"
    assert g_sqlitetype(config, budprem, jv, pnigh_str()) == "REAL"
    assert g_class_type(config, budprem, jv, popen_str()) == "float"
    assert g_sqlitetype(config, budprem, jv, popen_str()) == "REAL"
    assert g_class_type(config, budreas, jk, rcontext_str()) == type_WayStr_str()
    assert g_sqlitetype(config, budreas, jk, rcontext_str()) == "TEXT"
    assert g_class_type(config, budreas, jk, idea_way_str()) == type_WayStr_str()
    assert g_sqlitetype(config, budreas, jk, idea_way_str()) == "TEXT"
    assert g_class_type(config, budreas, jm, "_rcontext_idea_active_value") == "int"
    assert g_sqlitetype(config, budreas, jm, "_rcontext_idea_active_value") == "INTEGER"
    assert g_class_type(config, budreas, jm, "_status") == "int"
    assert g_sqlitetype(config, budreas, jm, "_status") == "INTEGER"
    assert g_class_type(config, budreas, jm, "_task") == "int"
    assert g_sqlitetype(config, budreas, jm, "_task") == "INTEGER"
    assert g_class_type(config, budreas, jv, "rcontext_idea_active_requisite") == "bool"
    assert (
        g_sqlitetype(config, budreas, jv, "rcontext_idea_active_requisite") == "INTEGER"
    )
    assert g_class_type(config, budlabor, jk, idea_way_str()) == type_WayStr_str()
    assert g_sqlitetype(config, budlabor, jk, idea_way_str()) == "TEXT"
    assert g_class_type(config, budlabor, jk, "labor_label") == type_LabelStr_str()
    assert g_sqlitetype(config, budlabor, jk, "labor_label") == "TEXT"
    assert g_class_type(config, budlabor, jm, "_owner_name_labor") == "int"
    assert g_sqlitetype(config, budlabor, jm, "_owner_name_labor") == "INTEGER"
    assert g_class_type(config, budidea, jm, "_active") == "int"
    assert g_sqlitetype(config, budidea, jm, "_active") == "INTEGER"
    assert g_class_type(config, budidea, jm, "_all_acct_cred") == "int"
    assert g_sqlitetype(config, budidea, jm, "_all_acct_cred") == "INTEGER"
    assert g_class_type(config, budidea, jm, "_all_acct_debt") == "int"
    assert g_sqlitetype(config, budidea, jm, "_all_acct_debt") == "INTEGER"
    assert g_class_type(config, budidea, jm, "_descendant_pledge_count") == "int"
    assert g_sqlitetype(config, budidea, jm, "_descendant_pledge_count") == "INTEGER"
    assert g_class_type(config, budidea, jm, "_fund_cease") == "float"
    assert g_sqlitetype(config, budidea, jm, "_fund_cease") == "REAL"
    assert g_class_type(config, budidea, jm, "fund_coin") == "float"
    assert g_sqlitetype(config, budidea, jm, "fund_coin") == "REAL"
    assert g_class_type(config, budidea, jm, "_fund_onset") == "float"
    assert g_sqlitetype(config, budidea, jm, "_fund_onset") == "REAL"
    assert g_class_type(config, budidea, jm, "_fund_ratio") == "float"
    assert g_sqlitetype(config, budidea, jm, "_fund_ratio") == "REAL"
    assert g_class_type(config, budidea, jm, "_gogo_calc") == "float"
    assert g_sqlitetype(config, budidea, jm, "_gogo_calc") == "REAL"
    assert g_class_type(config, budidea, jm, "_healerlink_ratio") == "float"
    assert g_sqlitetype(config, budidea, jm, "_healerlink_ratio") == "REAL"
    assert g_class_type(config, budidea, jm, "_level") == "int"
    assert g_sqlitetype(config, budidea, jm, "_level") == "INTEGER"
    assert g_class_type(config, budidea, jm, "_range_evaluated") == "int"
    assert g_sqlitetype(config, budidea, jm, "_range_evaluated") == "INTEGER"
    assert g_class_type(config, budidea, jm, "_stop_calc") == "float"
    assert g_sqlitetype(config, budidea, jm, "_stop_calc") == "REAL"
    assert g_class_type(config, budidea, jm, "_task") == "int"
    assert g_sqlitetype(config, budidea, jm, "_task") == "INTEGER"
    assert g_class_type(config, budidea, jv, addin_str()) == "float"
    assert g_sqlitetype(config, budidea, jv, addin_str()) == "REAL"
    assert g_class_type(config, budidea, jv, begin_str()) == "float"
    assert g_sqlitetype(config, budidea, jv, begin_str()) == "REAL"
    assert g_class_type(config, budidea, jv, close_str()) == "float"
    assert g_sqlitetype(config, budidea, jv, close_str()) == "REAL"
    assert g_class_type(config, budidea, jv, denom_str()) == "int"
    assert g_sqlitetype(config, budidea, jv, denom_str()) == "INTEGER"
    assert g_class_type(config, budidea, jv, gogo_want_str()) == "float"
    assert g_sqlitetype(config, budidea, jv, gogo_want_str()) == "REAL"
    assert g_class_type(config, budidea, jv, "mass") == "int"
    assert g_sqlitetype(config, budidea, jv, "mass") == "INTEGER"
    assert g_class_type(config, budidea, jv, morph_str()) == "bool"
    assert g_sqlitetype(config, budidea, jv, morph_str()) == "INTEGER"
    assert g_class_type(config, budidea, jv, numor_str()) == "int"
    assert g_sqlitetype(config, budidea, jv, numor_str()) == "INTEGER"
    assert g_class_type(config, budidea, jv, "pledge") == "bool"
    assert g_sqlitetype(config, budidea, jv, "pledge") == "INTEGER"
    assert g_class_type(config, budidea, jv, "problem_bool") == "bool"
    assert g_sqlitetype(config, budidea, jv, "problem_bool") == "INTEGER"
    assert g_class_type(config, budidea, jv, stop_want_str()) == "float"
    assert g_sqlitetype(config, budidea, jv, stop_want_str()) == "REAL"
    assert g_class_type(config, budunit, jm, "_keeps_buildable") == "int"
    assert g_sqlitetype(config, budunit, jm, "_keeps_buildable") == "INTEGER"
    assert g_class_type(config, budunit, jm, "_keeps_justified") == "int"
    assert g_sqlitetype(config, budunit, jm, "_keeps_justified") == "INTEGER"
    assert g_class_type(config, budunit, jm, "_offtrack_fund") == "float"
    assert g_sqlitetype(config, budunit, jm, "_offtrack_fund") == "REAL"
    assert g_class_type(config, budunit, jm, "_rational") == "bool"
    assert g_sqlitetype(config, budunit, jm, "_rational") == "INTEGER"
    assert g_class_type(config, budunit, jm, "_sum_healerlink_share") == "float"
    assert g_sqlitetype(config, budunit, jm, "_sum_healerlink_share") == "REAL"
    assert g_class_type(config, budunit, jm, "_tree_traverse_count") == "int"
    assert g_sqlitetype(config, budunit, jm, "_tree_traverse_count") == "INTEGER"
    assert g_class_type(config, budunit, jv, credor_respect_str()) == "float"
    assert g_sqlitetype(config, budunit, jv, credor_respect_str()) == "REAL"
    assert g_class_type(config, budunit, jv, debtor_respect_str()) == "float"
    assert g_sqlitetype(config, budunit, jv, debtor_respect_str()) == "REAL"
    assert g_class_type(config, budunit, jv, fund_coin_str()) == "float"
    assert g_sqlitetype(config, budunit, jv, fund_coin_str()) == "REAL"
    assert g_class_type(config, budunit, jv, "fund_pool") == "float"
    assert g_sqlitetype(config, budunit, jv, "fund_pool") == "REAL"
    assert g_class_type(config, budunit, jv, "max_tree_traverse") == "int"
    assert g_sqlitetype(config, budunit, jv, "max_tree_traverse") == "INTEGER"
    assert g_class_type(config, budunit, jv, penny_str()) == "float"
    assert g_sqlitetype(config, budunit, jv, penny_str()) == "REAL"
    assert g_class_type(config, budunit, jv, respect_bit_str()) == "float"
    assert g_sqlitetype(config, budunit, jv, respect_bit_str()) == "REAL"
    assert g_class_type(config, budunit, jv, "tally") == "int"
    assert g_sqlitetype(config, budunit, jv, "tally") == "INTEGER"


def test_get_bud_calc_config_dict_ReturnObj_EachArgHasOneClassType():
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


def test_get_bud_calc_config_dict_ReturnObj_EachArgHasOne_sqlite_datatype():
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


def test_get_bud_calc_args_type_dict_ReturnObj():
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
    assert bud_calc_args_type_dict.get(acct_name_str()) == type_NameStr_str()
    assert bud_calc_args_type_dict.get(group_label_str()) == type_LabelStr_str()
    assert bud_calc_args_type_dict.get("_credor_pool") == "float"
    assert bud_calc_args_type_dict.get("_debtor_pool") == "float"
    assert bud_calc_args_type_dict.get("_fund_agenda_give") == "float"
    assert bud_calc_args_type_dict.get("_fund_agenda_ratio_give") == "float"
    assert bud_calc_args_type_dict.get("_fund_agenda_ratio_take") == "float"
    assert bud_calc_args_type_dict.get("_fund_agenda_take") == "float"
    assert bud_calc_args_type_dict.get("_fund_give") == "float"
    assert bud_calc_args_type_dict.get("_fund_take") == "float"
    assert bud_calc_args_type_dict.get(credit_vote_str()) == "int"
    assert bud_calc_args_type_dict.get(debtit_vote_str()) == "int"
    assert bud_calc_args_type_dict.get("_inallocable_debtit_belief") == "float"
    assert bud_calc_args_type_dict.get("_irrational_debtit_belief") == "float"
    assert bud_calc_args_type_dict.get(credit_belief_str()) == "float"
    assert bud_calc_args_type_dict.get(debtit_belief_str()) == "float"
    assert bud_calc_args_type_dict.get(addin_str()) == "float"
    assert bud_calc_args_type_dict.get(begin_str()) == "float"
    assert bud_calc_args_type_dict.get(close_str()) == "float"
    assert bud_calc_args_type_dict.get(denom_str()) == "int"
    assert bud_calc_args_type_dict.get(gogo_want_str()) == "float"
    assert bud_calc_args_type_dict.get("mass") == "int"
    assert bud_calc_args_type_dict.get(morph_str()) == "bool"
    assert bud_calc_args_type_dict.get(numor_str()) == "int"
    assert bud_calc_args_type_dict.get("pledge") == "bool"
    assert bud_calc_args_type_dict.get("problem_bool") == "bool"
    assert bud_calc_args_type_dict.get(stop_want_str()) == "float"
    assert bud_calc_args_type_dict.get(awardee_label_str()) == type_LabelStr_str()
    assert bud_calc_args_type_dict.get(idea_way_str()) == type_WayStr_str()
    assert bud_calc_args_type_dict.get("give_force") == "float"
    assert bud_calc_args_type_dict.get("take_force") == "float"
    assert bud_calc_args_type_dict.get(rcontext_str()) == type_WayStr_str()
    assert bud_calc_args_type_dict.get(fnigh_str()) == "float"
    assert bud_calc_args_type_dict.get(fopen_str()) == "float"
    assert bud_calc_args_type_dict.get(fbranch_str()) == type_WayStr_str()
    assert bud_calc_args_type_dict.get(healer_name_str()) == type_NameStr_str()
    assert bud_calc_args_type_dict.get(pbranch_str()) == type_WayStr_str()
    assert bud_calc_args_type_dict.get("_status") == "int"
    assert bud_calc_args_type_dict.get("_task") == "int"
    assert bud_calc_args_type_dict.get("pdivisor") == "int"
    assert bud_calc_args_type_dict.get(pnigh_str()) == "float"
    assert bud_calc_args_type_dict.get(popen_str()) == "float"
    assert bud_calc_args_type_dict.get("_rcontext_idea_active_value") == "int"
    assert bud_calc_args_type_dict.get("rcontext_idea_active_requisite") == "bool"
    assert bud_calc_args_type_dict.get("labor_label") == type_LabelStr_str()
    assert bud_calc_args_type_dict.get("_owner_name_labor") == "int"
    assert bud_calc_args_type_dict.get("_active") == "int"
    assert bud_calc_args_type_dict.get("_all_acct_cred") == "int"
    assert bud_calc_args_type_dict.get("_all_acct_debt") == "int"
    assert bud_calc_args_type_dict.get("_descendant_pledge_count") == "int"
    assert bud_calc_args_type_dict.get("_fund_cease") == "float"
    assert bud_calc_args_type_dict.get("_fund_onset") == "float"
    assert bud_calc_args_type_dict.get("_fund_ratio") == "float"
    assert bud_calc_args_type_dict.get("_gogo_calc") == "float"
    assert bud_calc_args_type_dict.get("_healerlink_ratio") == "float"
    assert bud_calc_args_type_dict.get("_level") == "int"
    assert bud_calc_args_type_dict.get("_range_evaluated") == "int"
    assert bud_calc_args_type_dict.get("_stop_calc") == "float"
    assert bud_calc_args_type_dict.get("_keeps_buildable") == "int"
    assert bud_calc_args_type_dict.get("_keeps_justified") == "int"
    assert bud_calc_args_type_dict.get("_offtrack_fund") == "int"
    assert bud_calc_args_type_dict.get("_rational") == "bool"
    assert bud_calc_args_type_dict.get("_sum_healerlink_share") == "float"
    assert bud_calc_args_type_dict.get("_tree_traverse_count") == "int"
    assert bud_calc_args_type_dict.get(credor_respect_str()) == "float"
    assert bud_calc_args_type_dict.get(debtor_respect_str()) == "float"
    assert bud_calc_args_type_dict.get(fund_coin_str()) == "float"
    assert bud_calc_args_type_dict.get("fund_pool") == "float"
    assert bud_calc_args_type_dict.get("max_tree_traverse") == "int"
    assert bud_calc_args_type_dict.get(penny_str()) == "float"
    assert bud_calc_args_type_dict.get(respect_bit_str()) == "float"
    assert bud_calc_args_type_dict.get("tally") == "int"
    assert len(bud_calc_args_type_dict) == 72
