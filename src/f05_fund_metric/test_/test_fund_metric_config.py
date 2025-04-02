# from src.f00_instrument.dict_toolbox import get_from_nested_dict
from src.f00_instrument.file import open_json, save_json, create_path
from src.f02_bud.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_itemunit_str,
    bud_item_awardlink_str,
    bud_item_reasonunit_str,
    bud_item_reason_premiseunit_str,
    bud_item_teamlink_str,
    bud_item_healerlink_str,
    bud_item_factunit_str,
    bud_groupunit_str,
)

from src.f04_vow.atom_config import (
    get_bud_dimens,
    get_all_bud_dimen_keys,
    get_delete_key_name,
    get_all_bud_dimen_delete_keys,
    is_bud_dimen,
    get_atom_config_dict,
    get_atom_args_dimen_mapping,
    get_allowed_class_types,
    get_atom_args_class_types,
    get_atom_order as q_order,
    get_sorted_jkey_keys,
    set_mog,
    get_flattened_atom_table_build,
    get_normalized_bud_table_build,
    acct_name_str,
    addin_str,
    atom_insert,
    atom_delete,
    atom_update,
    awardee_tag_str,
    base_str,
    begin_str,
    dimen_str,
    close_str,
    column_order_str,
    credit_belief_str,
    credor_respect_str,
    credit_vote_str,
    crud_str,
    debtit_belief_str,
    debtor_respect_str,
    debtit_vote_str,
    denom_str,
    event_int_str,
    fnigh_str,
    fopen_str,
    fund_coin_str,
    gogo_want_str,
    group_label_str,
    healer_name_str,
    class_type_str,
    jkeys_str,
    jvalues_str,
    morph_str,
    nesting_order_str,
    normal_specs_str,
    normal_table_name_str,
    numor_str,
    parent_road_str,
    penny_str,
    respect_bit_str,
    road_str,
    sqlite_datatype_str,
    stop_want_str,
    team_tag_str,
    type_AcctName_str,
    type_LabelUnit_str,
    type_TitleUnit_str,
    type_RoadUnit_str,
)
from src.f05_fund_metric.fund_metric_config import (
    jmetrics_str,
    fund_take_str,
    fund_give_str,
    get_fund_metric_config_filename,
    config_file_path,
    get_fund_metric_config_dict,
    get_all_fund_metric_args,
)
from os.path import exists as os_path_exists
from os import getcwd as os_getcwd


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert jmetrics_str() == "jmetrics"
    assert fund_take_str() == "fund_take"
    assert fund_give_str() == "fund_give"


def test_get_fund_metric_config_dict_Exists():
    # ESTABLISH
    src_dir = create_path(os_getcwd(), "src")
    expected_dir = create_path(src_dir, "f05_fund_metric")

    # WHEN / THEN
    assert get_fund_metric_config_filename() == "fund_metric_config.json"
    expected_path = create_path(expected_dir, get_fund_metric_config_filename())
    assert config_file_path() == expected_path
    assert os_path_exists(config_file_path())


def test_get_fund_metric_config_dict_ReturnsObj_CheckLevel0Keys():
    # ESTABLISH / WHEN
    fund_metric_config = get_fund_metric_config_dict()
    fund_metric_config_keys = set(fund_metric_config.keys())

    # THEN
    assert budunit_str() in fund_metric_config_keys
    assert bud_acctunit_str() in fund_metric_config_keys
    assert bud_acct_membership_str() in fund_metric_config_keys
    assert bud_itemunit_str() in fund_metric_config_keys
    assert bud_item_awardlink_str() in fund_metric_config_keys
    assert bud_item_reasonunit_str() in fund_metric_config_keys
    assert bud_item_reason_premiseunit_str() in fund_metric_config_keys
    assert bud_item_teamlink_str() in fund_metric_config_keys
    assert bud_item_healerlink_str() in fund_metric_config_keys
    assert bud_item_factunit_str() in fund_metric_config_keys
    assert bud_groupunit_str() in fund_metric_config_keys
    assert len(get_fund_metric_config_dict()) == 11
    atom_config_dict = get_atom_config_dict()
    atom_config_dimens = set(atom_config_dict.keys())
    assert atom_config_dimens.issubset(fund_metric_config_keys)
    assert fund_metric_config_keys.difference(atom_config_dimens) == {
        bud_groupunit_str()
    }


def test_get_fund_metric_config_dict_ReturnsObj_CheckLevel1Keys():
    # ESTABLISH / WHEN
    fund_metric_config = get_fund_metric_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests
    for level1_key, aspect_dict in fund_metric_config.items():
        aspect_keys = set(aspect_dict.keys())
        print(f"{level1_key=} {aspect_keys=}")
        assert "abbreviation" in aspect_keys
        assert jkeys_str() in aspect_keys
        assert jvalues_str() in aspect_keys
        assert jmetrics_str() in aspect_keys
        assert len(aspect_keys) == 4


def test_get_fund_metric_config_dict_ReturnsObj_CheckLevel2_And_Level3_Keys():
    # ESTABLISH / WHEN
    fund_metric_config = get_fund_metric_config_dict()

    # THEN
    atom_config = get_atom_config_dict()
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, aspect_dict in fund_metric_config.items():
        if level1_key in atom_config.keys():
            atom_dimen = atom_config.get(level1_key)
            for level2_key, fm_aspect_dict in aspect_dict.items():
                if level2_key == jkeys_str():
                    atom_args = atom_dimen.get(jkeys_str())
                    atom_arg_keys = set(atom_args)
                    fm_aspect_keys = set(fm_aspect_dict.keys())
                    print(
                        f"{level1_key=} {level2_key=} {fm_aspect_keys=} {atom_arg_keys=}"
                    )
                    assert fm_aspect_keys == atom_arg_keys
                elif level2_key == jvalues_str():
                    atom_args = atom_dimen.get(jvalues_str())
                    atom_arg_keys = set(atom_args)
                    fm_aspect_keys = set(fm_aspect_dict.keys())
                    assert fm_aspect_keys == atom_arg_keys

    budunit_aspect = fund_metric_config.get(budunit_str())
    budacct_aspect = fund_metric_config.get(bud_acctunit_str())
    budmemb_aspect = fund_metric_config.get(bud_acct_membership_str())
    buditem_aspect = fund_metric_config.get(bud_itemunit_str())
    budawar_aspect = fund_metric_config.get(bud_item_awardlink_str())
    budreas_aspect = fund_metric_config.get(bud_item_reasonunit_str())
    budprem_aspect = fund_metric_config.get(bud_item_reason_premiseunit_str())
    budteam_aspect = fund_metric_config.get(bud_item_teamlink_str())
    budheal_aspect = fund_metric_config.get(bud_item_healerlink_str())
    budfact_aspect = fund_metric_config.get(bud_item_factunit_str())
    budgrou_aspect = fund_metric_config.get(bud_groupunit_str())

    budunit_jmetrics_keys = set(budunit_aspect.get(jmetrics_str()))
    budacct_jmetrics_keys = set(budacct_aspect.get(jmetrics_str()))
    budmemb_jmetrics_keys = set(budmemb_aspect.get(jmetrics_str()))
    buditem_jmetrics_keys = set(buditem_aspect.get(jmetrics_str()))
    budawar_jmetrics_keys = set(budawar_aspect.get(jmetrics_str()))
    budreas_jmetrics_keys = set(budreas_aspect.get(jmetrics_str()))
    budprem_jmetrics_keys = set(budprem_aspect.get(jmetrics_str()))
    budteam_jmetrics_keys = set(budteam_aspect.get(jmetrics_str()))
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
    expected_buditem_jmetrics_keys = {
        "_active",
        "_all_acct_cred",
        "_all_acct_debt",
        "_descendant_pledge_count",
        "_fund_ratio",
        "_fund_coin",
        "_fund_onset",
        "_fund_cease",
        "_healerlink_ratio",
        "_level",
        "_range_evaluated",
        "_task",
        "_gogo_calc",
        "_stop_calc",
    }
    assert expected_buditem_jmetrics_keys == buditem_jmetrics_keys
    expected_budawar_jmetrics_keys = {"_fund_give", "_fund_take"}
    assert expected_budawar_jmetrics_keys == budawar_jmetrics_keys
    expected_budreas_jmetrics_keys = {"_status", "_task", "_base_item_active_value"}
    assert expected_budreas_jmetrics_keys == budreas_jmetrics_keys
    expected_budprem_jmetrics_keys = {"_status", "_task"}
    assert expected_budprem_jmetrics_keys == budprem_jmetrics_keys
    expected_budteam_jmetrics_keys = {"_owner_name_team"}
    assert expected_budteam_jmetrics_keys == budteam_jmetrics_keys
    expected_budgrou_jmetrics_keys = {
        "_fund_give",
        "_fund_take",
        "_fund_agenda_give",
        "_fund_agenda_take",
        "_credor_pool",
        "_debtor_pool",
        "_fund_coin",
    }
    assert expected_budgrou_jmetrics_keys == budgrou_jmetrics_keys

    assert budunit_jmetrics_keys  # Non-empty
    assert budacct_jmetrics_keys  # Non-empty
    assert budmemb_jmetrics_keys  # Non-empty
    assert buditem_jmetrics_keys  # Non-empty
    assert budawar_jmetrics_keys  # Non-empty
    assert budreas_jmetrics_keys  # Non-empty
    assert budprem_jmetrics_keys  # Non-empty
    assert budteam_jmetrics_keys  # Non-empty
    assert not budheal_jmetrics_keys  # empty
    assert not budfact_jmetrics_keys  # empty
    assert budgrou_jmetrics_keys  # Non-empty


def test_get_fund_metric_config_dict_ReturnsObj_CheckAbbreviations():
    # ESTABLISH / WHEN
    fund_metric_config = get_fund_metric_config_dict()

    # THEN
    budunit_aspect = fund_metric_config.get(budunit_str())
    budacct_aspect = fund_metric_config.get(bud_acctunit_str())
    budmemb_aspect = fund_metric_config.get(bud_acct_membership_str())
    buditem_aspect = fund_metric_config.get(bud_itemunit_str())
    budawar_aspect = fund_metric_config.get(bud_item_awardlink_str())
    budreas_aspect = fund_metric_config.get(bud_item_reasonunit_str())
    budprem_aspect = fund_metric_config.get(bud_item_reason_premiseunit_str())
    budteam_aspect = fund_metric_config.get(bud_item_teamlink_str())
    budheal_aspect = fund_metric_config.get(bud_item_healerlink_str())
    budfact_aspect = fund_metric_config.get(bud_item_factunit_str())
    budgrou_aspect = fund_metric_config.get(bud_groupunit_str())
    abbr_str = "abbreviation"
    assert budunit_aspect.get(abbr_str) == "budunit"
    assert budacct_aspect.get(abbr_str) == "budacct"
    assert budmemb_aspect.get(abbr_str) == "budmemb"
    assert buditem_aspect.get(abbr_str) == "buditem"
    assert budawar_aspect.get(abbr_str) == "budawar"
    assert budreas_aspect.get(abbr_str) == "budreas"
    assert budprem_aspect.get(abbr_str) == "budprem"
    assert budteam_aspect.get(abbr_str) == "budteam"
    assert budheal_aspect.get(abbr_str) == "budheal"
    assert budfact_aspect.get(abbr_str) == "budfact"
    assert budgrou_aspect.get(abbr_str) == "budgrou"


def test_get_all_fund_metric_args_ReturnsObj():
    # ESTABLISH / WHEN
    all_fund_metric_args = get_all_fund_metric_args()

    # THEN
    assert all_fund_metric_args
    assert stop_want_str() in all_fund_metric_args
    assert parent_road_str() in all_fund_metric_args
    assert "_fund_give" in all_fund_metric_args

    # fund_metric_config = get_fund_metric_config_dict()
    # bud_acctunit_aspects = fund_metric_config.get("bud_acctunit")
    # budacct_jmetrics_dict = bud_acctunit_aspects.get("jmetrics")
    # road_fund_metric_aspects = budacct_jmetrics_dict.get("_fund_give")
    # assert bud_item_factunit_str() in road_fund_metric_aspects
    # assert bud_item_teamlink_str() in road_fund_metric_aspects
    # assert len(road_fund_metric_aspects) == 6
    assert len(all_fund_metric_args) == 75


def test_get_fund_metric_config_dict_ReturnsObj_CheckArgDataTypesKeysExist():
    # ESTABLISH / WHEN
    fund_metric_config = get_fund_metric_config_dict()

    # THEN
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    for level1_key, aspect_dict in fund_metric_config.items():
        for level2_key, fm_aspect_dict in aspect_dict.items():
            if level2_key in {jkeys_str(), jvalues_str(), jmetrics_str()}:
                for level3_key, attr_dict in fm_aspect_dict.items():
                    print(
                        f"{level1_key=} {level2_key=} {level3_key=} {set(attr_dict.keys())=}"
                    )
                    assert set(attr_dict.keys()) == {"class_type", "sqlite_datatype"}


def g_class_type(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get("class_type")


def g_sqlitetype(
    config: dict[str, dict[str, dict]], key1: str, key2: str, key3: str
) -> str:
    dimen = config.get(key1)
    j_dict = dimen.get(key2)
    j_arg = j_dict.get(key3)
    return j_arg.get("sqlite_datatype")


def test_get_fund_metric_config_dict_ReturnsObj_CheckArgDataTypesCorrect():
    # ESTABLISH / WHEN
    config = get_fund_metric_config_dict()
    # for level1_key, aspect_dict in config.items():
    #     for level2_key, fm_aspect_dict in aspect_dict.items():
    #         if level2_key in {jkeys_str(), jvalues_str(), jmetrics_str()}:
    #             for level3_key, attr_dict in fm_aspect_dict.items():
    #                 dimem = aspect_dict.get("abbreviation")
    #                 x_class_type = attr_dict.get("class_type")
    #                 x_sqlite_datatype = attr_dict.get("sqlite_datatype")
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
    buditem = bud_itemunit_str()
    budawar = bud_item_awardlink_str()
    budreas = bud_item_reasonunit_str()
    budprem = bud_item_reason_premiseunit_str()
    budteam = bud_item_teamlink_str()
    budheal = bud_item_healerlink_str()
    budfact = bud_item_factunit_str()
    budgrou = bud_groupunit_str()
    assert g_class_type(config, budmemb, jk, "acct_name") == "NameUnit"
    assert g_sqlitetype(config, budmemb, jk, "acct_name") == "TEXT"
    assert g_class_type(config, budmemb, jk, "group_label") == "LabelUnit"
    assert g_sqlitetype(config, budmemb, jk, "group_label") == "TEXT"
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
    assert g_class_type(config, budmemb, jv, "credit_vote") == "int"
    assert g_sqlitetype(config, budmemb, jv, "credit_vote") == "INTEGER"
    assert g_class_type(config, budmemb, jv, "debtit_vote") == "int"
    assert g_sqlitetype(config, budmemb, jv, "debtit_vote") == "INTEGER"
    assert g_class_type(config, budacct, jk, "acct_name") == "NameUnit"
    assert g_sqlitetype(config, budacct, jk, "acct_name") == "TEXT"
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
    assert g_class_type(config, budacct, jv, "credit_belief") == "float"
    assert g_sqlitetype(config, budacct, jv, "credit_belief") == "REAL"
    assert g_class_type(config, budacct, jv, "debtit_belief") == "float"
    assert g_sqlitetype(config, budacct, jv, "debtit_belief") == "REAL"
    assert g_class_type(config, budgrou, jk, "item_title") == "TitleUnit"
    assert g_sqlitetype(config, budgrou, jk, "item_title") == "TEXT"
    assert g_class_type(config, budgrou, jk, "parent_road") == "RoadUnit"
    assert g_sqlitetype(config, budgrou, jk, "parent_road") == "TEXT"
    assert g_class_type(config, budgrou, jm, "_credor_pool") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_credor_pool") == "REAL"
    assert g_class_type(config, budgrou, jm, "_debtor_pool") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_debtor_pool") == "REAL"
    assert g_class_type(config, budgrou, jm, "_fund_agenda_give") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_fund_agenda_give") == "REAL"
    assert g_class_type(config, budgrou, jm, "_fund_agenda_take") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_fund_agenda_take") == "REAL"
    assert g_class_type(config, budgrou, jm, "_fund_coin") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_fund_coin") == "REAL"
    assert g_class_type(config, budgrou, jm, "_fund_give") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_fund_give") == "REAL"
    assert g_class_type(config, budgrou, jm, "_fund_take") == "float"
    assert g_sqlitetype(config, budgrou, jm, "_fund_take") == "REAL"
    assert g_class_type(config, budgrou, jv, "addin") == "float"
    assert g_sqlitetype(config, budgrou, jv, "addin") == "REAL"
    assert g_class_type(config, budgrou, jv, "begin") == "float"
    assert g_sqlitetype(config, budgrou, jv, "begin") == "REAL"
    assert g_class_type(config, budgrou, jv, "close") == "float"
    assert g_sqlitetype(config, budgrou, jv, "close") == "REAL"
    assert g_class_type(config, budgrou, jv, "denom") == "int"
    assert g_sqlitetype(config, budgrou, jv, "denom") == "INTEGER"
    assert g_class_type(config, budgrou, jv, "gogo_want") == "float"
    assert g_sqlitetype(config, budgrou, jv, "gogo_want") == "REAL"
    assert g_class_type(config, budgrou, jv, "mass") == "int"
    assert g_sqlitetype(config, budgrou, jv, "mass") == "INTEGER"
    assert g_class_type(config, budgrou, jv, "morph") == "bool"
    assert g_sqlitetype(config, budgrou, jv, "morph") == "INTEGER"
    assert g_class_type(config, budgrou, jv, "numor") == "int"
    assert g_sqlitetype(config, budgrou, jv, "numor") == "INTEGER"
    assert g_class_type(config, budgrou, jv, "pledge") == "bool"
    assert g_sqlitetype(config, budgrou, jv, "pledge") == "INTEGER"
    assert g_class_type(config, budgrou, jv, "problem_bool") == "bool"
    assert g_sqlitetype(config, budgrou, jv, "problem_bool") == "INTEGER"
    assert g_class_type(config, budgrou, jv, "stop_want") == "float"
    assert g_sqlitetype(config, budgrou, jv, "stop_want") == "REAL"
    assert g_class_type(config, budawar, jk, "awardee_tag") == "LabelUnit"
    assert g_sqlitetype(config, budawar, jk, "awardee_tag") == "TEXT"
    assert g_class_type(config, budawar, jk, "road") == "RoadUnit"
    assert g_sqlitetype(config, budawar, jk, "road") == "TEXT"
    assert g_class_type(config, budawar, jm, "_fund_give") == "float"
    assert g_sqlitetype(config, budawar, jm, "_fund_give") == "REAL"
    assert g_class_type(config, budawar, jm, "_fund_take") == "float"
    assert g_sqlitetype(config, budawar, jm, "_fund_take") == "REAL"
    assert g_class_type(config, budawar, jv, "give_force") == "float"
    assert g_sqlitetype(config, budawar, jv, "give_force") == "REAL"
    assert g_class_type(config, budawar, jv, "take_force") == "float"
    assert g_sqlitetype(config, budawar, jv, "take_force") == "REAL"
    assert g_class_type(config, budfact, jk, "base") == "RoadUnit"
    assert g_sqlitetype(config, budfact, jk, "base") == "TEXT"
    assert g_class_type(config, budfact, jk, "road") == "RoadUnit"
    assert g_sqlitetype(config, budfact, jk, "road") == "TEXT"
    assert g_class_type(config, budfact, jv, "fnigh") == "float"
    assert g_sqlitetype(config, budfact, jv, "fnigh") == "REAL"
    assert g_class_type(config, budfact, jv, "fopen") == "float"
    assert g_sqlitetype(config, budfact, jv, "fopen") == "REAL"
    assert g_class_type(config, budfact, jv, "pick") == "RoadUnit"
    assert g_sqlitetype(config, budfact, jv, "pick") == "TEXT"
    assert g_class_type(config, budheal, jk, "healer_name") == "NameUnit"
    assert g_sqlitetype(config, budheal, jk, "healer_name") == "TEXT"
    assert g_class_type(config, budheal, jk, "road") == "RoadUnit"
    assert g_sqlitetype(config, budheal, jk, "road") == "TEXT"
    assert g_class_type(config, budprem, jk, "base") == "RoadUnit"
    assert g_sqlitetype(config, budprem, jk, "base") == "TEXT"
    assert g_class_type(config, budprem, jk, "need") == "RoadUnit"
    assert g_sqlitetype(config, budprem, jk, "need") == "TEXT"
    assert g_class_type(config, budprem, jk, "road") == "RoadUnit"
    assert g_sqlitetype(config, budprem, jk, "road") == "TEXT"
    assert g_class_type(config, budprem, jm, "_status") == "int"
    assert g_sqlitetype(config, budprem, jm, "_status") == "INTEGER"
    assert g_class_type(config, budprem, jm, "_task") == "int"
    assert g_sqlitetype(config, budprem, jm, "_task") == "INTEGER"
    assert g_class_type(config, budprem, jv, "divisor") == "int"
    assert g_sqlitetype(config, budprem, jv, "divisor") == "INTEGER"
    assert g_class_type(config, budprem, jv, "nigh") == "float"
    assert g_sqlitetype(config, budprem, jv, "nigh") == "REAL"
    assert g_class_type(config, budprem, jv, "open") == "float"
    assert g_sqlitetype(config, budprem, jv, "open") == "REAL"
    assert g_class_type(config, budreas, jk, "base") == "RoadUnit"
    assert g_sqlitetype(config, budreas, jk, "base") == "TEXT"
    assert g_class_type(config, budreas, jk, "road") == "RoadUnit"
    assert g_sqlitetype(config, budreas, jk, "road") == "TEXT"
    assert g_class_type(config, budreas, jm, "_base_item_active_value") == "int"
    assert g_sqlitetype(config, budreas, jm, "_base_item_active_value") == "INTEGER"
    assert g_class_type(config, budreas, jm, "_status") == "int"
    assert g_sqlitetype(config, budreas, jm, "_status") == "INTEGER"
    assert g_class_type(config, budreas, jm, "_task") == "int"
    assert g_sqlitetype(config, budreas, jm, "_task") == "INTEGER"
    assert g_class_type(config, budreas, jv, "base_item_active_requisite") == "bool"
    assert g_sqlitetype(config, budreas, jv, "base_item_active_requisite") == "INTEGER"
    assert g_class_type(config, budteam, jk, "road") == "RoadUnit"
    assert g_sqlitetype(config, budteam, jk, "road") == "TEXT"
    assert g_class_type(config, budteam, jk, "team_tag") == "LabelUnit"
    assert g_sqlitetype(config, budteam, jk, "team_tag") == "TEXT"
    assert g_class_type(config, budteam, jm, "_owner_name_team") == "int"
    assert g_sqlitetype(config, budteam, jm, "_owner_name_team") == "INTEGER"
    assert g_class_type(config, buditem, jk, "item_title") == "TitleUnit"
    assert g_sqlitetype(config, buditem, jk, "item_title") == "TEXT"
    assert g_class_type(config, buditem, jk, "parent_road") == "RoadUnit"
    assert g_sqlitetype(config, buditem, jk, "parent_road") == "TEXT"
    assert g_class_type(config, buditem, jm, "_active") == "int"
    assert g_sqlitetype(config, buditem, jm, "_active") == "INTEGER"
    assert g_class_type(config, buditem, jm, "_all_acct_cred") == "int"
    assert g_sqlitetype(config, buditem, jm, "_all_acct_cred") == "INTEGER"
    assert g_class_type(config, buditem, jm, "_all_acct_debt") == "int"
    assert g_sqlitetype(config, buditem, jm, "_all_acct_debt") == "INTEGER"
    assert g_class_type(config, buditem, jm, "_descendant_pledge_count") == "int"
    assert g_sqlitetype(config, buditem, jm, "_descendant_pledge_count") == "INTEGER"
    assert g_class_type(config, buditem, jm, "_fund_cease") == "float"
    assert g_sqlitetype(config, buditem, jm, "_fund_cease") == "REAL"
    assert g_class_type(config, buditem, jm, "_fund_coin") == "float"
    assert g_sqlitetype(config, buditem, jm, "_fund_coin") == "REAL"
    assert g_class_type(config, buditem, jm, "_fund_onset") == "float"
    assert g_sqlitetype(config, buditem, jm, "_fund_onset") == "REAL"
    assert g_class_type(config, buditem, jm, "_fund_ratio") == "float"
    assert g_sqlitetype(config, buditem, jm, "_fund_ratio") == "REAL"
    assert g_class_type(config, buditem, jm, "_gogo_calc") == "float"
    assert g_sqlitetype(config, buditem, jm, "_gogo_calc") == "REAL"
    assert g_class_type(config, buditem, jm, "_healerlink_ratio") == "float"
    assert g_sqlitetype(config, buditem, jm, "_healerlink_ratio") == "REAL"
    assert g_class_type(config, buditem, jm, "_level") == "int"
    assert g_sqlitetype(config, buditem, jm, "_level") == "INTEGER"
    assert g_class_type(config, buditem, jm, "_range_evaluated") == "int"
    assert g_sqlitetype(config, buditem, jm, "_range_evaluated") == "INTEGER"
    assert g_class_type(config, buditem, jm, "_stop_calc") == "float"
    assert g_sqlitetype(config, buditem, jm, "_stop_calc") == "REAL"
    assert g_class_type(config, buditem, jm, "_task") == "int"
    assert g_sqlitetype(config, buditem, jm, "_task") == "INTEGER"
    assert g_class_type(config, buditem, jv, "addin") == "float"
    assert g_sqlitetype(config, buditem, jv, "addin") == "REAL"
    assert g_class_type(config, buditem, jv, "begin") == "float"
    assert g_sqlitetype(config, buditem, jv, "begin") == "REAL"
    assert g_class_type(config, buditem, jv, "close") == "float"
    assert g_sqlitetype(config, buditem, jv, "close") == "REAL"
    assert g_class_type(config, buditem, jv, "denom") == "int"
    assert g_sqlitetype(config, buditem, jv, "denom") == "INTEGER"
    assert g_class_type(config, buditem, jv, "gogo_want") == "float"
    assert g_sqlitetype(config, buditem, jv, "gogo_want") == "REAL"
    assert g_class_type(config, buditem, jv, "mass") == "int"
    assert g_sqlitetype(config, buditem, jv, "mass") == "INTEGER"
    assert g_class_type(config, buditem, jv, "morph") == "bool"
    assert g_sqlitetype(config, buditem, jv, "morph") == "INTEGER"
    assert g_class_type(config, buditem, jv, "numor") == "int"
    assert g_sqlitetype(config, buditem, jv, "numor") == "INTEGER"
    assert g_class_type(config, buditem, jv, "pledge") == "bool"
    assert g_sqlitetype(config, buditem, jv, "pledge") == "INTEGER"
    assert g_class_type(config, buditem, jv, "problem_bool") == "bool"
    assert g_sqlitetype(config, buditem, jv, "problem_bool") == "INTEGER"
    assert g_class_type(config, buditem, jv, "stop_want") == "float"
    assert g_sqlitetype(config, buditem, jv, "stop_want") == "REAL"
    assert g_class_type(config, budunit, jm, "_keeps_buildable") == "int"
    assert g_sqlitetype(config, budunit, jm, "_keeps_buildable") == "INTEGER"
    assert g_class_type(config, budunit, jm, "_keeps_justified") == "int"
    assert g_sqlitetype(config, budunit, jm, "_keeps_justified") == "INTEGER"
    assert g_class_type(config, budunit, jm, "_offtrack_fund") == "int"
    assert g_sqlitetype(config, budunit, jm, "_offtrack_fund") == "INTEGER"
    assert g_class_type(config, budunit, jm, "_rational") == "bool"
    assert g_sqlitetype(config, budunit, jm, "_rational") == "INTEGER"
    assert g_class_type(config, budunit, jm, "_sum_healerlink_share") == "float"
    assert g_sqlitetype(config, budunit, jm, "_sum_healerlink_share") == "REAL"
    assert g_class_type(config, budunit, jm, "_tree_traverse_count") == "int"
    assert g_sqlitetype(config, budunit, jm, "_tree_traverse_count") == "INTEGER"
    assert g_class_type(config, budunit, jv, "credor_respect") == "float"
    assert g_sqlitetype(config, budunit, jv, "credor_respect") == "REAL"
    assert g_class_type(config, budunit, jv, "debtor_respect") == "float"
    assert g_sqlitetype(config, budunit, jv, "debtor_respect") == "REAL"
    assert g_class_type(config, budunit, jv, "fund_coin") == "float"
    assert g_sqlitetype(config, budunit, jv, "fund_coin") == "REAL"
    assert g_class_type(config, budunit, jv, "fund_pool") == "float"
    assert g_sqlitetype(config, budunit, jv, "fund_pool") == "REAL"
    assert g_class_type(config, budunit, jv, "max_tree_traverse") == "int"
    assert g_sqlitetype(config, budunit, jv, "max_tree_traverse") == "INTEGER"
    assert g_class_type(config, budunit, jv, "penny") == "float"
    assert g_sqlitetype(config, budunit, jv, "penny") == "REAL"
    assert g_class_type(config, budunit, jv, "respect_bit") == "float"
    assert g_sqlitetype(config, budunit, jv, "respect_bit") == "REAL"
    assert g_class_type(config, budunit, jv, "tally") == "int"
    assert g_sqlitetype(config, budunit, jv, "tally") == "INTEGER"


# def test_get_all_bud_dimen_keys_ReturnsObj():
#     # sourcery skip: no-loop-in-tests
#     # ESTABLISH / WHEN
#     all_bud_dimen_keys = get_all_bud_dimen_keys()

#     # THEN
#     assert not all_bud_dimen_keys.isdisjoint({"acct_name"})
#     expected_bud_keys = set()
#     for bud_dimen in get_bud_dimens():
#         expected_bud_keys.update(_get_atom_config_jkey_keys(bud_dimen))

#     expected_bud_keys.add("owner_name")
#     print(f"{expected_bud_keys=}")
#     assert all_bud_dimen_keys == expected_bud_keys


# def test_get_delete_key_name_ReturnsObj():
#     # ESTABLISH / WHEN / THEN
#     assert get_delete_key_name("fizz") == "fizz_ERASE"
#     assert get_delete_key_name("run") == "run_ERASE"
#     assert get_delete_key_name("") is None


# def test_get_all_bud_dimen_delete_keys_ReturnsObj():
#     # ESTABLISH / WHEN
#     all_bud_dimen_delete_keys = get_all_bud_dimen_delete_keys()

#     # THEN
#     assert not all_bud_dimen_delete_keys.isdisjoint({get_delete_key_name("acct_name")})
#     expected_bud_delete_keys = {
#         get_delete_key_name(bud_dimen_key) for bud_dimen_key in get_all_bud_dimen_keys()
#     }
#     print(f"{expected_bud_delete_keys=}")
#     assert all_bud_dimen_delete_keys == expected_bud_delete_keys


# def _check_every_crud_dict_has_element(atom_config_dict, atom_order_str):
#     for dimen, dimen_dict in atom_config_dict.items():
#         if dimen_dict.get(atom_insert()) is not None:
#             dimen_insert = dimen_dict.get(atom_insert())
#             if dimen_insert.get(atom_order_str) is None:
#                 x_str = f"Missing from {dimen} {atom_insert()} {dimen_insert.get(atom_order_str)=}"
#                 print(x_str)
#                 return False

#         if dimen_dict.get(atom_update()) is not None:
#             dimen_update = dimen_dict.get(atom_update())
#             if dimen_update.get(atom_order_str) is None:
#                 x_str = f"Missing from {dimen} {atom_update()} {dimen_update.get(atom_order_str)=}"
#                 print(x_str)
#                 return False

#         if dimen_dict.get(atom_delete()) is not None:
#             dimen_delete = dimen_dict.get(atom_delete())
#             if dimen_delete.get(atom_order_str) is None:
#                 x_str = f"Missing from {dimen} {atom_delete()} {dimen_delete.get(atom_order_str)=}"
#                 print(x_str)
#                 return False

#         if dimen_dict.get(normal_specs_str()) is None:
#             print(f"{dimen=} {normal_specs_str()} is missing")
#             return False
#     return True


# def test_get_atom_config_dict_EveryCrudOperationHasBudDeltaOrderGroup():
#     # ESTABLISH
#     atom_order_str = "atom_order"
#     mog = atom_order_str

#     # WHEN / THEN
#     assert _check_every_crud_dict_has_element(get_atom_config_dict(), atom_order_str)
#     # # Simple script for editing atom_config.json
#     # set_mog(atom_insert(), bud_acctunit_str(), 0)
#     # set_mog(atom_insert(), bud_acct_membership_str(), 1)
#     # set_mog(atom_insert(), bud_itemunit_str(), 2)
#     # set_mog(atom_insert(), bud_item_awardlink_str(), 3)
#     # set_mog(atom_insert(), bud_item_teamlink_str(), 4)
#     # set_mog(atom_insert(), bud_item_healerlink_str(), 5)
#     # set_mog(atom_insert(), bud_item_factunit_str(), 6)
#     # set_mog(atom_insert(), bud_item_reasonunit_str(), 7)
#     # set_mog(atom_insert(), bud_item_reason_premiseunit_str(), 8)
#     # set_mog(atom_update(), bud_acctunit_str(), 9)
#     # set_mog(atom_update(), bud_acct_membership_str(), 10)
#     # set_mog(atom_update(), bud_itemunit_str(), 11)
#     # set_mog(atom_update(), bud_item_awardlink_str(), 12)
#     # set_mog(atom_update(), bud_item_factunit_str(), 13)
#     # set_mog(atom_update(), bud_item_reason_premiseunit_str(), 14)
#     # set_mog(atom_update(), bud_item_reasonunit_str(), 15)
#     # set_mog(atom_delete(), bud_item_reason_premiseunit_str(), 16)
#     # set_mog(atom_delete(), bud_item_reasonunit_str(), 17)
#     # set_mog(atom_delete(), bud_item_factunit_str(), 18)
#     # set_mog(atom_delete(), bud_item_teamlink_str(), 19)
#     # set_mog(atom_delete(), bud_item_healerlink_str(), 20)
#     # set_mog(atom_delete(), bud_item_awardlink_str(), 21)
#     # set_mog(atom_delete(), bud_itemunit_str(), 22)
#     # set_mog(atom_delete(), bud_acct_membership_str(), 23)
#     # set_mog(atom_delete(), bud_acctunit_str(), 24)
#     # set_mog(atom_update(), budunit_str(), 25)

#     assert 0 == q_order(atom_insert(), bud_acctunit_str())
#     assert 1 == q_order(atom_insert(), bud_acct_membership_str())
#     assert 2 == q_order(atom_insert(), bud_itemunit_str())
#     assert 3 == q_order(atom_insert(), bud_item_awardlink_str())
#     assert 4 == q_order(atom_insert(), bud_item_teamlink_str())
#     assert 5 == q_order(atom_insert(), bud_item_healerlink_str())
#     assert 6 == q_order(atom_insert(), bud_item_factunit_str())
#     assert 7 == q_order(atom_insert(), bud_item_reasonunit_str())
#     assert 8 == q_order(atom_insert(), bud_item_reason_premiseunit_str())
#     assert 9 == q_order(atom_update(), bud_acctunit_str())
#     assert 10 == q_order(atom_update(), bud_acct_membership_str())
#     assert 11 == q_order(atom_update(), bud_itemunit_str())
#     assert 12 == q_order(atom_update(), bud_item_awardlink_str())
#     assert 13 == q_order(atom_update(), bud_item_factunit_str())
#     assert 14 == q_order(atom_update(), bud_item_reason_premiseunit_str())
#     assert 15 == q_order(atom_update(), bud_item_reasonunit_str())
#     assert 16 == q_order(atom_delete(), bud_item_reason_premiseunit_str())
#     assert 17 == q_order(atom_delete(), bud_item_reasonunit_str())
#     assert 18 == q_order(atom_delete(), bud_item_factunit_str())
#     assert 19 == q_order(atom_delete(), bud_item_teamlink_str())
#     assert 20 == q_order(atom_delete(), bud_item_healerlink_str())
#     assert 21 == q_order(atom_delete(), bud_item_awardlink_str())
#     assert 22 == q_order(atom_delete(), bud_itemunit_str())
#     assert 23 == q_order(atom_delete(), bud_acct_membership_str())
#     assert 24 == q_order(atom_delete(), bud_acctunit_str())
#     assert 25 == q_order(atom_update(), budunit_str())


# def _get_atom_config_jkeys_len(x_dimen: str) -> int:
#     jkeys_key_list = [x_dimen, jkeys_str()]
#     return len(get_from_nested_dict(get_atom_config_dict(), jkeys_key_list))


# def _get_atom_config_jvalues_len(x_dimen: str) -> int:
#     jvalues_key_list = [x_dimen, jvalues_str()]
#     return len(get_from_nested_dict(get_atom_config_dict(), jvalues_key_list))


# def test_get_atom_config_dict_CheckEachDimenHasCorrectArgCount():
#     # ESTABLISH
#     assert _get_atom_config_jkeys_len(budunit_str()) == 0
#     assert _get_atom_config_jkeys_len(bud_acctunit_str()) == 1
#     assert _get_atom_config_jkeys_len(bud_acct_membership_str()) == 2
#     assert _get_atom_config_jkeys_len(bud_itemunit_str()) == 2
#     assert _get_atom_config_jkeys_len(bud_item_awardlink_str()) == 2
#     assert _get_atom_config_jkeys_len(bud_item_reasonunit_str()) == 2
#     assert _get_atom_config_jkeys_len(bud_item_reason_premiseunit_str()) == 3
#     assert _get_atom_config_jkeys_len(bud_item_teamlink_str()) == 2
#     assert _get_atom_config_jkeys_len(bud_item_healerlink_str()) == 2
#     assert _get_atom_config_jkeys_len(bud_item_factunit_str()) == 2

#     assert _get_atom_config_jvalues_len(budunit_str()) == 8
#     assert _get_atom_config_jvalues_len(bud_acctunit_str()) == 2
#     assert _get_atom_config_jvalues_len(bud_acct_membership_str()) == 2
#     assert _get_atom_config_jvalues_len(bud_itemunit_str()) == 11
#     assert _get_atom_config_jvalues_len(bud_item_awardlink_str()) == 2
#     assert _get_atom_config_jvalues_len(bud_item_reasonunit_str()) == 1
#     assert _get_atom_config_jvalues_len(bud_item_reason_premiseunit_str()) == 3
#     assert _get_atom_config_jvalues_len(bud_item_teamlink_str()) == 0
#     assert _get_atom_config_jvalues_len(bud_item_healerlink_str()) == 0
#     assert _get_atom_config_jvalues_len(bud_item_factunit_str()) == 3


# def _has_every_element(x_arg, x_dict) -> bool:
#     arg_elements = {class_type_str(), sqlite_datatype_str(), column_order_str()}
#     for arg_element in arg_elements:
#         if x_dict.get(arg_element) is None:
#             print(f"{arg_element} failed for {x_arg=}")
#             return False
#     return True


# def _every_dimen_dict_has_arg_elements(dimen_dict: dict) -> bool:
#     for jkey, x_dict in dimen_dict.get(jkeys_str()).items():
#         if not _has_every_element(jkey, x_dict):
#             return False
#     if dimen_dict.get(jvalues_str()) is not None:
#         for jvalue, x_dict in dimen_dict.get(jvalues_str()).items():
#             if not _has_every_element(jvalue, x_dict):
#                 return False
#     return True


# def check_every_arg_dict_has_elements(atom_config_dict):
#     for dimen_key, dimen_dict in atom_config_dict.items():
#         print(f"{dimen_key=}")
#         assert _every_dimen_dict_has_arg_elements(dimen_dict)
#     return True


# def test_atom_config_AllArgsHave_class_type_sqlite_datatype():
#     # ESTABLISH / WHEN / THEN
#     assert check_every_arg_dict_has_elements(get_atom_config_dict())


# def check_necessary_nesting_order_exists() -> bool:
#     atom_config = get_atom_config_dict()
#     multi_jkey_dict = {}
#     for atom_key, atom_value in atom_config.items():
#         jkeys = atom_value.get(jkeys_str())
#         if len(jkeys) > 1:
#             multi_jkey_dict[atom_key] = jkeys
#     # print(f"{multi_jkey_dict.keys()=}")
#     for atom_key, jkeys in multi_jkey_dict.items():
#         for jkey_key, jkeys_dict in jkeys.items():
#             jkey_nesting_order = jkeys_dict.get(nesting_order_str())
#             print(f"{atom_key=} {jkey_key=} {jkey_nesting_order=}")
#             if jkey_nesting_order is None:
#                 return False
#     return True


# def test_atom_config_NestingOrderExistsWhenNeeded():
#     # When ChangUnit places an BudAtom in a nested dictionary ChangUnit.budatoms
#     # the order of required argments decides the location. The order must always be
#     # the same. All atom_config elements with two or more required args
#     # must assign to each of those args a nesting order

#     # ESTABLISH
#     # grab every atom_config with multiple required args
#     assert check_necessary_nesting_order_exists()


# def _get_atom_config_jvalue_keys(x_dimen: str) -> set[str]:
#     jvalues_key_list = [x_dimen, jvalues_str()]
#     return set(get_from_nested_dict(get_atom_config_dict(), jvalues_key_list).keys())


# def _get_atom_config_jkey_keys(x_dimen: str) -> set[str]:
#     jkeys_key_list = [x_dimen, jkeys_str()]
#     return set(get_from_nested_dict(get_atom_config_dict(), jkeys_key_list).keys())


# def unique_jvalues():
#     jvalue_keys = set()
#     jvalue_key_count = 0
#     for atom_dimen in get_atom_config_dict().keys():
#         new_jvalue_keys = _get_atom_config_jvalue_keys(atom_dimen)
#         jvalue_key_count += len(new_jvalue_keys)
#         jvalue_keys.update(new_jvalue_keys)
#         # print(f"{atom_dimen} {_get_atom_config_jvalue_keys(atom_dimen)}")
#     return jvalue_keys, jvalue_key_count


# def test_get_atom_config_dict_CheckEveryOptionalArgHasUniqueKey():
#     # ESTABLISH / WHEN
#     jvalue_keys, jvalue_key_count = unique_jvalues()

#     # THEN
#     print(f"{jvalue_key_count=} {len(jvalue_keys)=}")
#     assert jvalue_key_count == len(jvalue_keys)


# def unique_jkeys():
#     jkey_keys = set()
#     jkey_key_count = 0
#     for atom_dimen in get_atom_config_dict().keys():
#         new_jkey_keys = _get_atom_config_jkey_keys(atom_dimen)
#         if road_str() in new_jkey_keys:
#             new_jkey_keys.remove(road_str())
#         if base_str() in new_jkey_keys:
#             new_jkey_keys.remove(base_str())
#         if acct_name_str() in new_jkey_keys:
#             new_jkey_keys.remove(acct_name_str())
#         if group_label_str() in new_jkey_keys:
#             new_jkey_keys.remove(group_label_str())
#         print(f"{atom_dimen} {new_jkey_keys=}")
#         jkey_key_count += len(new_jkey_keys)
#         jkey_keys.update(new_jkey_keys)
#     return jkey_keys, jkey_key_count


# def test_get_atom_config_dict_SomeRequiredArgAreUnique():
#     # ESTABLISH / WHEN
#     jkey_keys, jkey_key_count = unique_jkeys()

#     # THEN
#     print(f"{jkey_key_count=} {len(jkey_keys)=}")
#     assert jkey_key_count == len(jkey_keys)


# def test_get_sorted_jkey_keys_ReturnsObj_bud_acctunit():
#     # ESTABLISH
#     x_dimen = bud_acctunit_str()

#     # WHEN
#     x_sorted_jkey_keys = get_sorted_jkey_keys(x_dimen)

#     # THEN
#     assert x_sorted_jkey_keys == [acct_name_str()]


# def test_get_sorted_jkey_keys_ReturnsObj_bud_item_reason_premiseunit():
#     # ESTABLISH
#     x_dimen = bud_item_reason_premiseunit_str()

#     # WHEN
#     x_sorted_jkey_keys = get_sorted_jkey_keys(x_dimen)

#     # THEN
#     assert x_sorted_jkey_keys == [road_str(), base_str(), "need"]


# def test_get_flattened_atom_table_build_ReturnsObj():
#     # ESTABLISH / WHEN
#     atom_columns = get_flattened_atom_table_build()

#     # THEN
#     assert len(atom_columns) == 106
#     assert atom_columns.get("budunit_UPDATE_credor_respect") == "INTEGER"
#     # print(f"{atom_columns.keys()=}")


# def test_get_normalized_bud_table_build_ReturnsObj():
#     # ESTABLISH / WHEN
#     normalized_bud_table_build = get_normalized_bud_table_build()
#     nx = normalized_bud_table_build

#     # THEN
#     assert len(nx) == 10
#     cat_budunit = nx.get(budunit_str())
#     cat_acctunit = nx.get(bud_acctunit_str())
#     cat_membership = nx.get(bud_acct_membership_str())
#     cat_item = nx.get(bud_itemunit_str())
#     cat_awardlink = nx.get(bud_item_awardlink_str())
#     cat_reason = nx.get(bud_item_reasonunit_str())
#     cat_premise = nx.get(bud_item_reason_premiseunit_str())
#     cat_teamlink = nx.get(bud_item_teamlink_str())
#     cat_healerlink = nx.get(bud_item_healerlink_str())
#     cat_fact = nx.get(bud_item_factunit_str())

#     assert cat_budunit is not None
#     assert cat_acctunit is not None
#     assert cat_membership is not None
#     assert cat_item is not None
#     assert cat_awardlink is not None
#     assert cat_reason is not None
#     assert cat_premise is not None
#     assert cat_teamlink is not None
#     assert cat_healerlink is not None
#     assert cat_fact is not None

#     normal_specs_budunit = cat_budunit.get(normal_specs_str())
#     normal_specs_acctunit = cat_acctunit.get(normal_specs_str())
#     normal_specs_membership = cat_membership.get(normal_specs_str())
#     normal_specs_item = cat_item.get(normal_specs_str())
#     normal_specs_awardlink = cat_awardlink.get(normal_specs_str())
#     normal_specs_reason = cat_reason.get(normal_specs_str())
#     normal_specs_premise = cat_premise.get(normal_specs_str())
#     normal_specs_teamlink = cat_teamlink.get(normal_specs_str())
#     normal_specs_healerlink = cat_healerlink.get(normal_specs_str())
#     normal_specs_fact = cat_fact.get(normal_specs_str())

#     columns_str = "columns"
#     print(f"{cat_budunit.keys()=}")
#     print(f"{normal_specs_str()=}")
#     assert normal_specs_budunit is not None
#     assert normal_specs_acctunit is not None
#     assert normal_specs_membership is not None
#     assert normal_specs_item is not None
#     assert normal_specs_awardlink is not None
#     assert normal_specs_reason is not None
#     assert normal_specs_premise is not None
#     assert normal_specs_teamlink is not None
#     assert normal_specs_healerlink is not None
#     assert normal_specs_fact is not None

#     table_name_budunit = normal_specs_budunit.get(normal_table_name_str())
#     table_name_acctunit = normal_specs_acctunit.get(normal_table_name_str())
#     table_name_membership = normal_specs_membership.get(normal_table_name_str())
#     table_name_item = normal_specs_item.get(normal_table_name_str())
#     table_name_awardlink = normal_specs_awardlink.get(normal_table_name_str())
#     table_name_reason = normal_specs_reason.get(normal_table_name_str())
#     table_name_premise = normal_specs_premise.get(normal_table_name_str())
#     table_name_teamlink = normal_specs_teamlink.get(normal_table_name_str())
#     table_name_healerlink = normal_specs_healerlink.get(normal_table_name_str())
#     table_name_fact = normal_specs_fact.get(normal_table_name_str())

#     assert table_name_budunit == "bud"
#     assert table_name_acctunit == "acctunit"
#     assert table_name_membership == "membership"
#     assert table_name_item == "item"
#     assert table_name_awardlink == "awardlink"
#     assert table_name_reason == "reason"
#     assert table_name_premise == "premise"
#     assert table_name_teamlink == "teamlink"
#     assert table_name_healerlink == "healerlink"
#     assert table_name_fact == "fact"

#     assert len(cat_budunit) == 2
#     assert cat_budunit.get(columns_str) is not None

#     budunit_columns = cat_budunit.get(columns_str)
#     assert len(budunit_columns) == 9
#     assert budunit_columns.get("uid") is not None
#     assert budunit_columns.get("max_tree_traverse") is not None
#     assert budunit_columns.get(credor_respect_str()) is not None
#     assert budunit_columns.get(debtor_respect_str()) is not None
#     assert budunit_columns.get("fund_pool") is not None
#     assert budunit_columns.get(fund_coin_str()) is not None
#     assert budunit_columns.get(respect_bit_str()) is not None
#     assert budunit_columns.get(penny_str()) is not None
#     assert budunit_columns.get("tally") is not None

#     assert len(cat_acctunit) == 2
#     acctunit_columns = cat_acctunit.get(columns_str)
#     assert len(acctunit_columns) == 4
#     assert acctunit_columns.get("uid") is not None
#     assert acctunit_columns.get(acct_name_str()) is not None
#     assert acctunit_columns.get(credit_belief_str()) is not None
#     assert acctunit_columns.get(debtit_belief_str()) is not None

#     acct_name_dict = acctunit_columns.get(acct_name_str())
#     assert len(acct_name_dict) == 2
#     assert acct_name_dict.get(sqlite_datatype_str()) == "TEXT"
#     assert acct_name_dict.get("nullable") is False
#     debtit_belief_dict = acctunit_columns.get("debtit_belief")
#     assert len(acct_name_dict) == 2
#     assert debtit_belief_dict.get(sqlite_datatype_str()) == "INTEGER"
#     assert debtit_belief_dict.get("nullable") is True

#     assert len(cat_item) == 2
#     item_columns = cat_item.get(columns_str)
#     assert len(item_columns) == 14
#     assert item_columns.get("uid") is not None
#     assert item_columns.get(parent_road_str()) is not None
#     assert item_columns.get(begin_str()) is not None
#     assert item_columns.get(close_str()) is not None

#     gogo_want_dict = item_columns.get(gogo_want_str())
#     stop_want_dict = item_columns.get(stop_want_str())
#     assert len(gogo_want_dict) == 2
#     assert len(stop_want_dict) == 2
#     assert gogo_want_dict.get(sqlite_datatype_str()) == "REAL"
#     assert stop_want_dict.get(sqlite_datatype_str()) == "REAL"
#     assert gogo_want_dict.get("nullable") is True
#     assert stop_want_dict.get("nullable") is True


# def test_get_atom_args_dimen_mapping_ReturnsObj():
#     # ESTABLISH / WHEN
#     x_atom_args_dimen_mapping = get_atom_args_dimen_mapping()

#     # THEN
#     assert x_atom_args_dimen_mapping
#     assert x_atom_args_dimen_mapping.get(stop_want_str())
#     assert x_atom_args_dimen_mapping.get(stop_want_str()) == {bud_itemunit_str()}
#     assert x_atom_args_dimen_mapping.get(parent_road_str())
#     road_dimens = x_atom_args_dimen_mapping.get(road_str())
#     assert bud_item_factunit_str() in road_dimens
#     assert bud_item_teamlink_str() in road_dimens
#     assert len(road_dimens) == 6
#     assert len(x_atom_args_dimen_mapping) == 42


# def get_class_type(x_dimen: str, x_arg: str) -> str:
#     atom_config_dict = get_atom_config_dict()
#     dimen_dict = atom_config_dict.get(x_dimen)
#     optional_dict = dimen_dict.get(jvalues_str())
#     required_dict = dimen_dict.get(jkeys_str())
#     arg_dict = {}
#     if optional_dict.get(x_arg):
#         arg_dict = dimen_dict.get(jvalues_str()).get(x_arg)
#     if required_dict.get(x_arg):
#         arg_dict = required_dict.get(x_arg)
#     return arg_dict.get(class_type_str())


# def test_get_class_type_ReturnsObj():
#     # ESTABLISH / WHEN / THEN
#     assert get_class_type(bud_acctunit_str(), acct_name_str()) == type_AcctName_str()
#     assert get_class_type(bud_itemunit_str(), gogo_want_str()) == "float"


# def test_get_allowed_class_types_ReturnsObj():
#     # ESTABLISH
#     x_allowed_class_types = {
#         "int",
#         type_AcctName_str(),
#         type_LabelUnit_str(),
#         type_TitleUnit_str(),
#         type_RoadUnit_str(),
#         "float",
#         "bool",
#         "TimeLinePoint",
#     }

#     # WHEN / THEN
#     assert get_allowed_class_types() == x_allowed_class_types


# def test_get_atom_config_dict_ValidatePythonTypes():
#     # make sure all atom config python types are valid and repeated args are the same
#     # ESTABLISH WHEN / THEN
#     assert all_atom_config_class_types_are_valid(get_allowed_class_types())


# def all_atom_config_class_types_are_valid(allowed_class_types):
#     x_atom_args_dimen_mapping = get_atom_args_dimen_mapping()
#     for x_atom_arg, dimens in x_atom_args_dimen_mapping.items():
#         old_class_type = None
#         x_class_type = ""
#         for x_dimen in dimens:
#             x_class_type = get_class_type(x_dimen, x_atom_arg)
#             # print(f"{x_class_type=} {x_atom_arg=} {x_dimen=}")
#             if x_class_type not in allowed_class_types:
#                 return False

#             if old_class_type is None:
#                 old_class_type = x_class_type
#             # confirm each atom_arg has same data type in all dimens
#             print(f"{x_class_type=} {old_class_type=} {x_atom_arg=} {x_dimen=}")
#             if x_class_type != old_class_type:
#                 return False
#             old_class_type = x_class_type
#     return True


# def all_atom_args_class_types_are_correct(x_class_types) -> bool:
#     x_atom_args_dimen_mapping = get_atom_args_dimen_mapping()
#     x_sorted_class_types = sorted(list(x_class_types.keys()))
#     for x_atom_arg in x_sorted_class_types:
#         x_dimens = list(x_atom_args_dimen_mapping.get(x_atom_arg))
#         x_dimen = x_dimens[0]
#         x_class_type = get_class_type(x_dimen, x_atom_arg)
#         print(
#             f"assert x_class_types.get({x_atom_arg}) == {x_class_type} {x_class_types.get(x_atom_arg)=}"
#         )
#         if x_class_types.get(x_atom_arg) != x_class_type:
#             return False
#     return True


# def test_get_atom_args_class_types_ReturnsObj():
#     # ESTABLISH / WHEN
#     x_class_types = get_atom_args_class_types()

#     # THEN
#     assert x_class_types.get(acct_name_str()) == type_AcctName_str()
#     assert x_class_types.get(addin_str()) == "float"
#     assert x_class_types.get(awardee_tag_str()) == type_LabelUnit_str()
#     assert x_class_types.get(base_str()) == type_RoadUnit_str()
#     assert x_class_types.get("base_item_active_requisite") == "bool"
#     assert x_class_types.get(begin_str()) == "float"
#     assert x_class_types.get(respect_bit_str()) == "float"
#     assert x_class_types.get(close_str()) == "float"
#     assert x_class_types.get(credit_belief_str()) == "int"
#     assert x_class_types.get(credit_vote_str()) == "int"
#     assert x_class_types.get(credor_respect_str()) == "int"
#     assert x_class_types.get(debtit_belief_str()) == "int"
#     assert x_class_types.get(debtit_vote_str()) == "int"
#     assert x_class_types.get(debtor_respect_str()) == "int"
#     assert x_class_types.get(denom_str()) == "int"
#     assert x_class_types.get("divisor") == "int"
#     assert x_class_types.get(fnigh_str()) == "float"
#     assert x_class_types.get(fopen_str()) == "float"
#     assert x_class_types.get(fund_coin_str()) == "float"
#     assert x_class_types.get("fund_pool") == "float"
#     assert x_class_types.get("give_force") == "float"
#     assert x_class_types.get(gogo_want_str()) == "float"
#     assert x_class_types.get(group_label_str()) == type_LabelUnit_str()
#     assert x_class_types.get(healer_name_str()) == type_AcctName_str()
#     assert x_class_types.get("item_title") == type_TitleUnit_str()
#     assert x_class_types.get("mass") == "int"
#     assert x_class_types.get("max_tree_traverse") == "int"
#     assert x_class_types.get(morph_str()) == "bool"
#     assert x_class_types.get("need") == type_RoadUnit_str()
#     assert x_class_types.get("nigh") == "float"
#     assert x_class_types.get(numor_str()) == "int"
#     assert x_class_types.get("open") == "float"
#     assert x_class_types.get(parent_road_str()) == type_RoadUnit_str()
#     assert x_class_types.get(penny_str()) == "float"
#     assert x_class_types.get("pick") == type_RoadUnit_str()
#     assert x_class_types.get("pledge") == "bool"
#     assert x_class_types.get("problem_bool") == "bool"
#     assert x_class_types.get(road_str()) == type_RoadUnit_str()
#     assert x_class_types.get(stop_want_str()) == "float"
#     assert x_class_types.get("take_force") == "float"
#     assert x_class_types.get("tally") == "int"
#     assert x_class_types.get(team_tag_str()) == type_LabelUnit_str()
#     assert x_class_types.keys() == get_atom_args_dimen_mapping().keys()
#     assert all_atom_args_class_types_are_correct(x_class_types)
