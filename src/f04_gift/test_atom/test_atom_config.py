from src.f00_instrument.dict_toolbox import get_from_nested_dict
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
)
from src.f04_gift.atom_config import (
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


def test_str_functions_ReturnsObj():
    assert acct_name_str() == "acct_name"
    assert addin_str() == "addin"
    assert atom_insert() == "INSERT"
    assert atom_update() == "UPDATE"
    assert atom_delete() == "DELETE"
    assert awardee_tag_str() == "awardee_tag"
    assert base_str() == "base"
    assert begin_str() == "begin"
    assert dimen_str() == "dimen"
    assert close_str() == "close"
    assert column_order_str() == "column_order"
    assert credit_belief_str() == "credit_belief"
    assert credor_respect_str() == "credor_respect"
    assert credit_vote_str() == "credit_vote"
    assert crud_str() == "crud"
    assert debtit_belief_str() == "debtit_belief"
    assert debtor_respect_str() == "debtor_respect"
    assert debtit_vote_str() == "debtit_vote"
    assert denom_str() == "denom"
    assert fnigh_str() == "fnigh"
    assert fopen_str() == "fopen"
    assert fund_coin_str() == "fund_coin"
    assert gogo_want_str() == "gogo_want"
    assert group_label_str() == "group_label"
    assert class_type_str() == "class_type"
    assert jkeys_str() == "jkeys"
    assert jvalues_str() == "jvalues"
    assert morph_str() == "morph"
    assert nesting_order_str() == "nesting_order"
    assert normal_specs_str() == "normal_specs"
    assert normal_table_name_str() == "normal_table_name"
    assert numor_str() == "numor"
    assert parent_road_str() == "parent_road"
    assert penny_str() == "penny"
    assert respect_bit_str() == "respect_bit"
    assert road_str() == "road"
    assert sqlite_datatype_str() == "sqlite_datatype"
    assert stop_want_str() == "stop_want"
    assert team_tag_str() == "team_tag"
    assert type_AcctName_str() == "NameUnit"
    assert type_LabelUnit_str() == "LabelUnit"
    assert type_TitleUnit_str() == "TitleUnit"
    assert type_RoadUnit_str() == "RoadUnit"


def test_get_bud_dimens_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_bud_dimens() == set(get_atom_config_dict().keys())
    assert bud_acctunit_str() in get_bud_dimens()
    assert is_bud_dimen("itemroot") is False


def test_get_all_bud_dimen_keys_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    all_bud_dimen_keys = get_all_bud_dimen_keys()

    # THEN
    assert not all_bud_dimen_keys.isdisjoint({"acct_name"})
    expected_bud_keys = set()
    for bud_dimen in get_bud_dimens():
        expected_bud_keys.update(_get_atom_config_jkey_keys(bud_dimen))

    expected_bud_keys.add("owner_name")
    print(f"{expected_bud_keys=}")
    assert all_bud_dimen_keys == expected_bud_keys


def test_get_delete_key_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_delete_key_name("fizz") == "fizz_ERASE"
    assert get_delete_key_name("run") == "run_ERASE"
    assert get_delete_key_name("") is None


def test_get_all_bud_dimen_delete_keys_ReturnsObj():
    # ESTABLISH / WHEN
    all_bud_dimen_delete_keys = get_all_bud_dimen_delete_keys()

    # THEN
    assert not all_bud_dimen_delete_keys.isdisjoint({get_delete_key_name("acct_name")})
    expected_bud_delete_keys = {
        get_delete_key_name(bud_dimen_key) for bud_dimen_key in get_all_bud_dimen_keys()
    }
    print(f"{expected_bud_delete_keys=}")
    assert all_bud_dimen_delete_keys == expected_bud_delete_keys


def _check_every_crud_dict_has_element(atom_config_dict, atom_order_str):
    for dimen, dimen_dict in atom_config_dict.items():
        if dimen_dict.get(atom_insert()) is not None:
            dimen_insert = dimen_dict.get(atom_insert())
            if dimen_insert.get(atom_order_str) is None:
                x_str = f"Missing from {dimen} {atom_insert()} {dimen_insert.get(atom_order_str)=}"
                print(x_str)
                return False

        if dimen_dict.get(atom_update()) is not None:
            dimen_update = dimen_dict.get(atom_update())
            if dimen_update.get(atom_order_str) is None:
                x_str = f"Missing from {dimen} {atom_update()} {dimen_update.get(atom_order_str)=}"
                print(x_str)
                return False

        if dimen_dict.get(atom_delete()) is not None:
            dimen_delete = dimen_dict.get(atom_delete())
            if dimen_delete.get(atom_order_str) is None:
                x_str = f"Missing from {dimen} {atom_delete()} {dimen_delete.get(atom_order_str)=}"
                print(x_str)
                return False

        if dimen_dict.get(normal_specs_str()) is None:
            print(f"{dimen=} {normal_specs_str()} is missing")
            return False
    return True


def test_get_atom_config_dict_EveryCrudOperationHasDeltaUnitOrderGroup():
    # ESTABLISH
    atom_order_str = "atom_order"
    mog = atom_order_str

    # WHEN / THEN
    assert _check_every_crud_dict_has_element(get_atom_config_dict(), atom_order_str)
    # # Simple script for editing atom_config.json
    # set_mog(atom_insert(), bud_acctunit_str(), 0)
    # set_mog(atom_insert(), bud_acct_membership_str(), 1)
    # set_mog(atom_insert(), bud_itemunit_str(), 2)
    # set_mog(atom_insert(), bud_item_awardlink_str(), 3)
    # set_mog(atom_insert(), bud_item_teamlink_str(), 4)
    # set_mog(atom_insert(), bud_item_healerlink_str(), 5)
    # set_mog(atom_insert(), bud_item_factunit_str(), 6)
    # set_mog(atom_insert(), bud_item_reasonunit_str(), 7)
    # set_mog(atom_insert(), bud_item_reason_premiseunit_str(), 8)
    # set_mog(atom_update(), bud_acctunit_str(), 9)
    # set_mog(atom_update(), bud_acct_membership_str(), 10)
    # set_mog(atom_update(), bud_itemunit_str(), 11)
    # set_mog(atom_update(), bud_item_awardlink_str(), 12)
    # set_mog(atom_update(), bud_item_factunit_str(), 13)
    # set_mog(atom_update(), bud_item_reason_premiseunit_str(), 14)
    # set_mog(atom_update(), bud_item_reasonunit_str(), 15)
    # set_mog(atom_delete(), bud_item_reason_premiseunit_str(), 16)
    # set_mog(atom_delete(), bud_item_reasonunit_str(), 17)
    # set_mog(atom_delete(), bud_item_factunit_str(), 18)
    # set_mog(atom_delete(), bud_item_teamlink_str(), 19)
    # set_mog(atom_delete(), bud_item_healerlink_str(), 20)
    # set_mog(atom_delete(), bud_item_awardlink_str(), 21)
    # set_mog(atom_delete(), bud_itemunit_str(), 22)
    # set_mog(atom_delete(), bud_acct_membership_str(), 23)
    # set_mog(atom_delete(), bud_acctunit_str(), 24)
    # set_mog(atom_update(), budunit_str(), 25)

    assert 0 == q_order(atom_insert(), bud_acctunit_str())
    assert 1 == q_order(atom_insert(), bud_acct_membership_str())
    assert 2 == q_order(atom_insert(), bud_itemunit_str())
    assert 3 == q_order(atom_insert(), bud_item_awardlink_str())
    assert 4 == q_order(atom_insert(), bud_item_teamlink_str())
    assert 5 == q_order(atom_insert(), bud_item_healerlink_str())
    assert 6 == q_order(atom_insert(), bud_item_factunit_str())
    assert 7 == q_order(atom_insert(), bud_item_reasonunit_str())
    assert 8 == q_order(atom_insert(), bud_item_reason_premiseunit_str())
    assert 9 == q_order(atom_update(), bud_acctunit_str())
    assert 10 == q_order(atom_update(), bud_acct_membership_str())
    assert 11 == q_order(atom_update(), bud_itemunit_str())
    assert 12 == q_order(atom_update(), bud_item_awardlink_str())
    assert 13 == q_order(atom_update(), bud_item_factunit_str())
    assert 14 == q_order(atom_update(), bud_item_reason_premiseunit_str())
    assert 15 == q_order(atom_update(), bud_item_reasonunit_str())
    assert 16 == q_order(atom_delete(), bud_item_reason_premiseunit_str())
    assert 17 == q_order(atom_delete(), bud_item_reasonunit_str())
    assert 18 == q_order(atom_delete(), bud_item_factunit_str())
    assert 19 == q_order(atom_delete(), bud_item_teamlink_str())
    assert 20 == q_order(atom_delete(), bud_item_healerlink_str())
    assert 21 == q_order(atom_delete(), bud_item_awardlink_str())
    assert 22 == q_order(atom_delete(), bud_itemunit_str())
    assert 23 == q_order(atom_delete(), bud_acct_membership_str())
    assert 24 == q_order(atom_delete(), bud_acctunit_str())
    assert 25 == q_order(atom_update(), budunit_str())


def _get_atom_config_jkeys_len(x_dimen: str) -> int:
    jkeys_key_list = [x_dimen, jkeys_str()]
    return len(get_from_nested_dict(get_atom_config_dict(), jkeys_key_list))


def _get_atom_config_jvalues_len(x_dimen: str) -> int:
    jvalues_key_list = [x_dimen, jvalues_str()]
    return len(get_from_nested_dict(get_atom_config_dict(), jvalues_key_list))


def test_get_atom_config_dict_CheckEachDimenHasCorrectArgCount():
    # ESTABLISH
    assert _get_atom_config_jkeys_len(budunit_str()) == 0
    assert _get_atom_config_jkeys_len(bud_acctunit_str()) == 1
    assert _get_atom_config_jkeys_len(bud_acct_membership_str()) == 2
    assert _get_atom_config_jkeys_len(bud_itemunit_str()) == 2
    assert _get_atom_config_jkeys_len(bud_item_awardlink_str()) == 2
    assert _get_atom_config_jkeys_len(bud_item_reasonunit_str()) == 2
    assert _get_atom_config_jkeys_len(bud_item_reason_premiseunit_str()) == 3
    assert _get_atom_config_jkeys_len(bud_item_teamlink_str()) == 2
    assert _get_atom_config_jkeys_len(bud_item_healerlink_str()) == 2
    assert _get_atom_config_jkeys_len(bud_item_factunit_str()) == 2

    assert _get_atom_config_jvalues_len(budunit_str()) == 9
    assert _get_atom_config_jvalues_len(bud_acctunit_str()) == 2
    assert _get_atom_config_jvalues_len(bud_acct_membership_str()) == 2
    assert _get_atom_config_jvalues_len(bud_itemunit_str()) == 11
    assert _get_atom_config_jvalues_len(bud_item_awardlink_str()) == 2
    assert _get_atom_config_jvalues_len(bud_item_reasonunit_str()) == 1
    assert _get_atom_config_jvalues_len(bud_item_reason_premiseunit_str()) == 3
    assert _get_atom_config_jvalues_len(bud_item_teamlink_str()) == 0
    assert _get_atom_config_jvalues_len(bud_item_healerlink_str()) == 0
    assert _get_atom_config_jvalues_len(bud_item_factunit_str()) == 3


def _has_every_element(x_arg, x_dict) -> bool:
    arg_elements = {class_type_str(), sqlite_datatype_str(), column_order_str()}
    for arg_element in arg_elements:
        if x_dict.get(arg_element) is None:
            print(f"{arg_element} failed for {x_arg=}")
            return False
    return True


def _every_dimen_dict_has_arg_elements(dimen_dict: dict) -> bool:
    for jkey, x_dict in dimen_dict.get(jkeys_str()).items():
        if not _has_every_element(jkey, x_dict):
            return False
    if dimen_dict.get(jvalues_str()) is not None:
        for jvalue, x_dict in dimen_dict.get(jvalues_str()).items():
            if not _has_every_element(jvalue, x_dict):
                return False
    return True


def check_every_arg_dict_has_elements(atom_config_dict):
    for dimen_key, dimen_dict in atom_config_dict.items():
        print(f"{dimen_key=}")
        assert _every_dimen_dict_has_arg_elements(dimen_dict)
    return True


def test_atom_config_AllArgsHave_class_type_sqlite_datatype():
    # ESTABLISH / WHEN / THEN
    assert check_every_arg_dict_has_elements(get_atom_config_dict())


def check_necessary_nesting_order_exists() -> bool:
    atom_config = get_atom_config_dict()
    multi_jkey_dict = {}
    for atom_key, atom_value in atom_config.items():
        jkeys = atom_value.get(jkeys_str())
        if len(jkeys) > 1:
            multi_jkey_dict[atom_key] = jkeys
    # print(f"{multi_jkey_dict.keys()=}")
    for atom_key, jkeys in multi_jkey_dict.items():
        for jkey_key, jkeys_dict in jkeys.items():
            jkey_nesting_order = jkeys_dict.get(nesting_order_str())
            print(f"{atom_key=} {jkey_key=} {jkey_nesting_order=}")
            if jkey_nesting_order is None:
                return False
    return True


def test_atom_config_NestingOrderExistsWhenNeeded():
    # When ChangUnit places an AtomUnit in a nested dictionary ChangUnit.atomunits
    # the order of required argments decides the location. The order must always be
    # the same. All atom_config elements with two or more required args
    # must assign to each of those args a nesting order

    # ESTABLISH
    # grab every atom_config with multiple required args
    assert check_necessary_nesting_order_exists()


def _get_atom_config_jvalue_keys(x_dimen: str) -> set[str]:
    jvalues_key_list = [x_dimen, jvalues_str()]
    return set(get_from_nested_dict(get_atom_config_dict(), jvalues_key_list).keys())


def _get_atom_config_jkey_keys(x_dimen: str) -> set[str]:
    jkeys_key_list = [x_dimen, jkeys_str()]
    return set(get_from_nested_dict(get_atom_config_dict(), jkeys_key_list).keys())


def unique_jvalues():
    jvalue_keys = set()
    jvalue_key_count = 0
    for atom_dimen in get_atom_config_dict().keys():
        new_jvalue_keys = _get_atom_config_jvalue_keys(atom_dimen)
        jvalue_key_count += len(new_jvalue_keys)
        jvalue_keys.update(new_jvalue_keys)
        # print(f"{atom_dimen} {_get_atom_config_jvalue_keys(atom_dimen)}")
    return jvalue_keys, jvalue_key_count


def test_get_atom_config_dict_CheckEveryOptionalArgHasUniqueKey():
    # ESTABLISH / WHEN
    jvalue_keys, jvalue_key_count = unique_jvalues()

    # THEN
    print(f"{jvalue_key_count=} {len(jvalue_keys)=}")
    assert jvalue_key_count == len(jvalue_keys)


def unique_jkeys():
    jkey_keys = set()
    jkey_key_count = 0
    for atom_dimen in get_atom_config_dict().keys():
        new_jkey_keys = _get_atom_config_jkey_keys(atom_dimen)
        if road_str() in new_jkey_keys:
            new_jkey_keys.remove(road_str())
        if base_str() in new_jkey_keys:
            new_jkey_keys.remove(base_str())
        if acct_name_str() in new_jkey_keys:
            new_jkey_keys.remove(acct_name_str())
        if group_label_str() in new_jkey_keys:
            new_jkey_keys.remove(group_label_str())
        print(f"{atom_dimen} {new_jkey_keys=}")
        jkey_key_count += len(new_jkey_keys)
        jkey_keys.update(new_jkey_keys)
    return jkey_keys, jkey_key_count


def test_get_atom_config_dict_SomeRequiredArgAreUnique():
    # ESTABLISH / WHEN
    jkey_keys, jkey_key_count = unique_jkeys()

    # THEN
    print(f"{jkey_key_count=} {len(jkey_keys)=}")
    assert jkey_key_count == len(jkey_keys)


def test_get_sorted_jkey_keys_ReturnsObj_bud_acctunit():
    # ESTABLISH
    x_dimen = bud_acctunit_str()

    # WHEN
    x_sorted_jkey_keys = get_sorted_jkey_keys(x_dimen)

    # THEN
    assert x_sorted_jkey_keys == [acct_name_str()]


def test_get_sorted_jkey_keys_ReturnsObj_bud_item_reason_premiseunit():
    # ESTABLISH
    x_dimen = bud_item_reason_premiseunit_str()

    # WHEN
    x_sorted_jkey_keys = get_sorted_jkey_keys(x_dimen)

    # THEN
    assert x_sorted_jkey_keys == [road_str(), base_str(), "need"]


def test_get_flattened_atom_table_build_ReturnsCorrectObj():
    # ESTABLISH / WHEN
    atom_columns = get_flattened_atom_table_build()

    # THEN
    assert len(atom_columns) == 107
    assert atom_columns.get("budunit_UPDATE_credor_respect") == "INTEGER"
    # print(f"{atom_columns.keys()=}")


def test_get_normalized_bud_table_build_ReturnsCorrectObj():
    # ESTABLISH / WHEN
    normalized_bud_table_build = get_normalized_bud_table_build()
    nx = normalized_bud_table_build

    # THEN
    assert len(nx) == 10
    cat_budunit = nx.get(budunit_str())
    cat_acctunit = nx.get(bud_acctunit_str())
    cat_membership = nx.get(bud_acct_membership_str())
    cat_item = nx.get(bud_itemunit_str())
    cat_awardlink = nx.get(bud_item_awardlink_str())
    cat_reason = nx.get(bud_item_reasonunit_str())
    cat_premise = nx.get(bud_item_reason_premiseunit_str())
    cat_teamlink = nx.get(bud_item_teamlink_str())
    cat_healerlink = nx.get(bud_item_healerlink_str())
    cat_fact = nx.get(bud_item_factunit_str())

    assert cat_budunit is not None
    assert cat_acctunit is not None
    assert cat_membership is not None
    assert cat_item is not None
    assert cat_awardlink is not None
    assert cat_reason is not None
    assert cat_premise is not None
    assert cat_teamlink is not None
    assert cat_healerlink is not None
    assert cat_fact is not None

    normal_specs_budunit = cat_budunit.get(normal_specs_str())
    normal_specs_acctunit = cat_acctunit.get(normal_specs_str())
    normal_specs_membership = cat_membership.get(normal_specs_str())
    normal_specs_item = cat_item.get(normal_specs_str())
    normal_specs_awardlink = cat_awardlink.get(normal_specs_str())
    normal_specs_reason = cat_reason.get(normal_specs_str())
    normal_specs_premise = cat_premise.get(normal_specs_str())
    normal_specs_teamlink = cat_teamlink.get(normal_specs_str())
    normal_specs_healerlink = cat_healerlink.get(normal_specs_str())
    normal_specs_fact = cat_fact.get(normal_specs_str())

    columns_str = "columns"
    print(f"{cat_budunit.keys()=}")
    print(f"{normal_specs_str()=}")
    assert normal_specs_budunit is not None
    assert normal_specs_acctunit is not None
    assert normal_specs_membership is not None
    assert normal_specs_item is not None
    assert normal_specs_awardlink is not None
    assert normal_specs_reason is not None
    assert normal_specs_premise is not None
    assert normal_specs_teamlink is not None
    assert normal_specs_healerlink is not None
    assert normal_specs_fact is not None

    table_name_budunit = normal_specs_budunit.get(normal_table_name_str())
    table_name_acctunit = normal_specs_acctunit.get(normal_table_name_str())
    table_name_membership = normal_specs_membership.get(normal_table_name_str())
    table_name_item = normal_specs_item.get(normal_table_name_str())
    table_name_awardlink = normal_specs_awardlink.get(normal_table_name_str())
    table_name_reason = normal_specs_reason.get(normal_table_name_str())
    table_name_premise = normal_specs_premise.get(normal_table_name_str())
    table_name_teamlink = normal_specs_teamlink.get(normal_table_name_str())
    table_name_healerlink = normal_specs_healerlink.get(normal_table_name_str())
    table_name_fact = normal_specs_fact.get(normal_table_name_str())

    assert table_name_budunit == "bud"
    assert table_name_acctunit == "acctunit"
    assert table_name_membership == "membership"
    assert table_name_item == "item"
    assert table_name_awardlink == "awardlink"
    assert table_name_reason == "reason"
    assert table_name_premise == "premise"
    assert table_name_teamlink == "teamlink"
    assert table_name_healerlink == "healerlink"
    assert table_name_fact == "fact"

    assert len(cat_budunit) == 2
    assert cat_budunit.get(columns_str) is not None

    budunit_columns = cat_budunit.get(columns_str)
    assert len(budunit_columns) == 10
    assert budunit_columns.get("uid") is not None
    assert budunit_columns.get("max_tree_traverse") is not None
    assert budunit_columns.get(credor_respect_str()) is not None
    assert budunit_columns.get(debtor_respect_str()) is not None
    assert budunit_columns.get("fund_pool") is not None
    assert budunit_columns.get(fund_coin_str()) is not None
    assert budunit_columns.get(respect_bit_str()) is not None
    assert budunit_columns.get(penny_str()) is not None
    assert budunit_columns.get("deal_time_int") is not None
    assert budunit_columns.get("tally") is not None

    assert len(cat_acctunit) == 2
    acctunit_columns = cat_acctunit.get(columns_str)
    assert len(acctunit_columns) == 4
    assert acctunit_columns.get("uid") is not None
    assert acctunit_columns.get(acct_name_str()) is not None
    assert acctunit_columns.get(credit_belief_str()) is not None
    assert acctunit_columns.get(debtit_belief_str()) is not None

    acct_name_dict = acctunit_columns.get(acct_name_str())
    assert len(acct_name_dict) == 2
    assert acct_name_dict.get(sqlite_datatype_str()) == "TEXT"
    assert acct_name_dict.get("nullable") is False
    debtit_belief_dict = acctunit_columns.get("debtit_belief")
    assert len(acct_name_dict) == 2
    assert debtit_belief_dict.get(sqlite_datatype_str()) == "INTEGER"
    assert debtit_belief_dict.get("nullable") is True

    assert len(cat_item) == 2
    item_columns = cat_item.get(columns_str)
    assert len(item_columns) == 14
    assert item_columns.get("uid") is not None
    assert item_columns.get(parent_road_str()) is not None
    assert item_columns.get(begin_str()) is not None
    assert item_columns.get(close_str()) is not None

    gogo_want_dict = item_columns.get(gogo_want_str())
    stop_want_dict = item_columns.get(stop_want_str())
    assert len(gogo_want_dict) == 2
    assert len(stop_want_dict) == 2
    assert gogo_want_dict.get(sqlite_datatype_str()) == "REAL"
    assert stop_want_dict.get(sqlite_datatype_str()) == "REAL"
    assert gogo_want_dict.get("nullable") is True
    assert stop_want_dict.get("nullable") is True


def test_get_atom_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_atom_args_dimen_mapping = get_atom_args_dimen_mapping()

    # THEN
    assert x_atom_args_dimen_mapping
    assert x_atom_args_dimen_mapping.get(stop_want_str())
    assert x_atom_args_dimen_mapping.get(stop_want_str()) == {bud_itemunit_str()}
    assert x_atom_args_dimen_mapping.get(parent_road_str())
    road_dimens = x_atom_args_dimen_mapping.get(road_str())
    assert bud_item_factunit_str() in road_dimens
    assert bud_item_teamlink_str() in road_dimens
    assert len(road_dimens) == 6
    assert len(x_atom_args_dimen_mapping) == 43


def get_class_type(x_dimen: str, x_arg: str) -> str:
    atom_config_dict = get_atom_config_dict()
    dimen_dict = atom_config_dict.get(x_dimen)
    optional_dict = dimen_dict.get(jvalues_str())
    required_dict = dimen_dict.get(jkeys_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = dimen_dict.get(jvalues_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(class_type_str())


def test_get_class_type_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_class_type(bud_acctunit_str(), acct_name_str()) == type_AcctName_str()
    assert get_class_type(bud_itemunit_str(), gogo_want_str()) == "float"


def test_get_allowed_class_types_ReturnsObj():
    # ESTABLISH
    x_allowed_class_types = {
        "int",
        type_AcctName_str(),
        type_LabelUnit_str(),
        type_TitleUnit_str(),
        type_RoadUnit_str(),
        "float",
        "bool",
        "TimeLinePoint",
    }

    # WHEN / THEN
    assert get_allowed_class_types() == x_allowed_class_types


def test_get_atom_config_dict_ValidatePythonTypes():
    # make sure all atom config python types are valid and repeated args are the same
    # ESTABLISH WHEN / THEN
    assert all_atom_config_class_types_are_valid(get_allowed_class_types())


def all_atom_config_class_types_are_valid(allowed_class_types):
    x_atom_args_dimen_mapping = get_atom_args_dimen_mapping()
    for x_atom_arg, dimens in x_atom_args_dimen_mapping.items():
        old_class_type = None
        x_class_type = ""
        for x_dimen in dimens:
            x_class_type = get_class_type(x_dimen, x_atom_arg)
            # print(f"{x_class_type=} {x_atom_arg=} {x_dimen=}")
            if x_class_type not in allowed_class_types:
                return False

            if old_class_type is None:
                old_class_type = x_class_type
            # confirm each atom_arg has same data type in all dimens
            print(f"{x_class_type=} {old_class_type=} {x_atom_arg=} {x_dimen=}")
            if x_class_type != old_class_type:
                return False
            old_class_type = x_class_type
    return True


def all_atom_args_class_types_are_correct(x_class_types) -> bool:
    x_atom_args_dimen_mapping = get_atom_args_dimen_mapping()
    x_sorted_class_types = sorted(list(x_class_types.keys()))
    for x_atom_arg in x_sorted_class_types:
        x_dimens = list(x_atom_args_dimen_mapping.get(x_atom_arg))
        x_dimen = x_dimens[0]
        x_class_type = get_class_type(x_dimen, x_atom_arg)
        print(
            f"assert x_class_types.get({x_atom_arg}) == {x_class_type} {x_class_types.get(x_atom_arg)=}"
        )
        if x_class_types.get(x_atom_arg) != x_class_type:
            return False
    return True


def test_get_atom_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_class_types = get_atom_args_class_types()

    # THEN
    assert x_class_types.get(acct_name_str()) == type_AcctName_str()
    assert x_class_types.get(addin_str()) == "float"
    assert x_class_types.get(awardee_tag_str()) == type_LabelUnit_str()
    assert x_class_types.get(base_str()) == type_RoadUnit_str()
    assert x_class_types.get("base_item_active_requisite") == "bool"
    assert x_class_types.get(begin_str()) == "float"
    assert x_class_types.get(respect_bit_str()) == "float"
    assert x_class_types.get(close_str()) == "float"
    assert x_class_types.get(credit_belief_str()) == "int"
    assert x_class_types.get(credit_vote_str()) == "int"
    assert x_class_types.get(credor_respect_str()) == "int"
    assert x_class_types.get(debtit_belief_str()) == "int"
    assert x_class_types.get(debtit_vote_str()) == "int"
    assert x_class_types.get(debtor_respect_str()) == "int"
    assert x_class_types.get(denom_str()) == "int"
    assert x_class_types.get("divisor") == "int"
    assert x_class_types.get(fnigh_str()) == "float"
    assert x_class_types.get(fopen_str()) == "float"
    assert x_class_types.get(fund_coin_str()) == "float"
    assert x_class_types.get("fund_pool") == "float"
    assert x_class_types.get("give_force") == "float"
    assert x_class_types.get(gogo_want_str()) == "float"
    assert x_class_types.get(group_label_str()) == type_LabelUnit_str()
    assert x_class_types.get(healer_name_str()) == type_AcctName_str()
    assert x_class_types.get("item_title") == type_TitleUnit_str()
    assert x_class_types.get("mass") == "int"
    assert x_class_types.get("max_tree_traverse") == "int"
    assert x_class_types.get(morph_str()) == "bool"
    assert x_class_types.get("need") == type_RoadUnit_str()
    assert x_class_types.get("nigh") == "float"
    assert x_class_types.get(numor_str()) == "int"
    assert x_class_types.get("open") == "float"
    assert x_class_types.get(parent_road_str()) == type_RoadUnit_str()
    assert x_class_types.get(penny_str()) == "float"
    assert x_class_types.get("pick") == type_RoadUnit_str()
    assert x_class_types.get("pledge") == "bool"
    assert x_class_types.get("problem_bool") == "bool"
    assert x_class_types.get("deal_time_int") == "TimeLinePoint"
    assert x_class_types.get(road_str()) == type_RoadUnit_str()
    assert x_class_types.get(stop_want_str()) == "float"
    assert x_class_types.get("take_force") == "float"
    assert x_class_types.get("tally") == "int"
    assert x_class_types.get(team_tag_str()) == type_LabelUnit_str()
    assert x_class_types.keys() == get_atom_args_dimen_mapping().keys()
    assert all_atom_args_class_types_are_correct(x_class_types)
