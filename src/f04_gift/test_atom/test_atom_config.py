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
    get_atom_categorys,
    is_atom_category,
    get_atom_config_dict,
    get_atom_args_category_mapping,
    get_allowed_jaar_types,
    get_atom_args_jaar_types,
    get_atom_order as q_order,
    get_sorted_jkey_keys,
    set_mog,
    get_flattened_atom_table_build,
    get_normalized_bud_table_build,
    acct_id_str,
    addin_str,
    atom_insert,
    atom_delete,
    atom_update,
    awardee_id_str,
    base_str,
    begin_str,
    category_str,
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
    group_id_str,
    healer_id_str,
    jaar_type_str,
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
    team_id_str,
    type_AcctID_str,
    type_GroupID_str,
    type_IdeaUnit_str,
    type_RoadUnit_str,
)


def test_str_functions_ReturnsObj():
    assert acct_id_str() == "acct_id"
    assert addin_str() == "addin"
    assert atom_insert() == "INSERT"
    assert atom_update() == "UPDATE"
    assert atom_delete() == "DELETE"
    assert awardee_id_str() == "awardee_id"
    assert base_str() == "base"
    assert begin_str() == "begin"
    assert category_str() == "category"
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
    assert group_id_str() == "group_id"
    assert jaar_type_str() == "jaar_type"
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
    assert team_id_str() == "team_id"
    assert type_AcctID_str() == "AcctID"
    assert type_GroupID_str() == "GroupID"
    assert type_IdeaUnit_str() == "IdeaUnit"
    assert type_RoadUnit_str() == "RoadUnit"


def test_atom_config_HasCorrect_category():
    assert get_atom_categorys() == {
        budunit_str(),
        bud_acctunit_str(),
        bud_acct_membership_str(),
        bud_itemunit_str(),
        bud_item_awardlink_str(),
        bud_item_reasonunit_str(),
        bud_item_reason_premiseunit_str(),
        bud_item_teamlink_str(),
        bud_item_healerlink_str(),
        bud_item_factunit_str(),
    }
    assert bud_acctunit_str() in get_atom_categorys()
    assert is_atom_category("itemroot") is False


def _check_every_crud_dict_has_element(atom_config_dict, atom_order_str):
    for category, category_dict in atom_config_dict.items():
        if category_dict.get(atom_insert()) is not None:
            category_insert = category_dict.get(atom_insert())
            if category_insert.get(atom_order_str) is None:
                x_str = f"Missing from {category} {atom_insert()} {category_insert.get(atom_order_str)=}"
                print(x_str)
                return False

        if category_dict.get(atom_update()) is not None:
            category_update = category_dict.get(atom_update())
            if category_update.get(atom_order_str) is None:
                x_str = f"Missing from {category} {atom_update()} {category_update.get(atom_order_str)=}"
                print(x_str)
                return False

        if category_dict.get(atom_delete()) is not None:
            category_delete = category_dict.get(atom_delete())
            if category_delete.get(atom_order_str) is None:
                x_str = f"Missing from {category} {atom_delete()} {category_delete.get(atom_order_str)=}"
                print(x_str)
                return False

        if category_dict.get(normal_specs_str()) is None:
            print(f"{category=} {normal_specs_str()} is missing")
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


def _get_atom_config_jkeys_len(x_cat: str) -> int:
    jkeys_key_list = [x_cat, jkeys_str()]
    return len(get_from_nested_dict(get_atom_config_dict(), jkeys_key_list))


def _get_atom_config_jvalues_len(x_cat: str) -> int:
    jvalues_key_list = [x_cat, jvalues_str()]
    return len(get_from_nested_dict(get_atom_config_dict(), jvalues_key_list))


def test_get_atom_config_dict_CheckEachCategoryHasCorrectArgCount():
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
    arg_elements = {jaar_type_str(), sqlite_datatype_str(), column_order_str()}
    for arg_element in arg_elements:
        if x_dict.get(arg_element) is None:
            print(f"{arg_element} failed for {x_arg=}")
            return False
    return True


def _every_category_dict_has_arg_elements(category_dict: dict) -> bool:
    for jkey, x_dict in category_dict.get(jkeys_str()).items():
        if not _has_every_element(jkey, x_dict):
            return False
    if category_dict.get(jvalues_str()) is not None:
        for jvalue, x_dict in category_dict.get(jvalues_str()).items():
            if not _has_every_element(jvalue, x_dict):
                return False
    return True


def check_every_arg_dict_has_elements(atom_config_dict):
    for category_key, category_dict in atom_config_dict.items():
        print(f"{category_key=}")
        assert _every_category_dict_has_arg_elements(category_dict)
    return True


def test_atom_config_AllArgsHave_jaar_type_sqlite_datatype():
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


def _get_atom_config_jvalue_keys(x_cat: str) -> set[str]:
    jvalues_key_list = [x_cat, jvalues_str()]
    return set(get_from_nested_dict(get_atom_config_dict(), jvalues_key_list).keys())


def _get_atom_config_jkey_keys(x_cat: str) -> set[str]:
    jkeys_key_list = [x_cat, jkeys_str()]
    return set(get_from_nested_dict(get_atom_config_dict(), jkeys_key_list).keys())


def unique_jvalues():
    jvalue_keys = set()
    jvalue_key_count = 0
    for atom_category in get_atom_config_dict().keys():
        new_jvalue_keys = _get_atom_config_jvalue_keys(atom_category)
        jvalue_key_count += len(new_jvalue_keys)
        jvalue_keys.update(new_jvalue_keys)
        # print(f"{atom_category} {_get_atom_config_jvalue_keys(atom_category)}")
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
    for atom_category in get_atom_config_dict().keys():
        new_jkey_keys = _get_atom_config_jkey_keys(atom_category)
        if road_str() in new_jkey_keys:
            new_jkey_keys.remove(road_str())
        if base_str() in new_jkey_keys:
            new_jkey_keys.remove(base_str())
        if acct_id_str() in new_jkey_keys:
            new_jkey_keys.remove(acct_id_str())
        if group_id_str() in new_jkey_keys:
            new_jkey_keys.remove(group_id_str())
        print(f"{atom_category} {new_jkey_keys=}")
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
    x_category = bud_acctunit_str()

    # WHEN
    x_sorted_jkey_keys = get_sorted_jkey_keys(x_category)

    # THEN
    assert x_sorted_jkey_keys == [acct_id_str()]


def test_get_sorted_jkey_keys_ReturnsObj_bud_item_reason_premiseunit():
    # ESTABLISH
    x_category = bud_item_reason_premiseunit_str()

    # WHEN
    x_sorted_jkey_keys = get_sorted_jkey_keys(x_category)

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
    assert budunit_columns.get("purview_time_id") is not None
    assert budunit_columns.get("tally") is not None

    assert len(cat_acctunit) == 2
    acctunit_columns = cat_acctunit.get(columns_str)
    assert len(acctunit_columns) == 4
    assert acctunit_columns.get("uid") is not None
    assert acctunit_columns.get(acct_id_str()) is not None
    assert acctunit_columns.get(credit_belief_str()) is not None
    assert acctunit_columns.get(debtit_belief_str()) is not None

    acct_id_dict = acctunit_columns.get(acct_id_str())
    assert len(acct_id_dict) == 2
    assert acct_id_dict.get(sqlite_datatype_str()) == "TEXT"
    assert acct_id_dict.get("nullable") is False
    debtit_belief_dict = acctunit_columns.get("debtit_belief")
    assert len(acct_id_dict) == 2
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


def test_get_atom_args_category_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_atom_args_category_mapping = get_atom_args_category_mapping()

    # THEN
    assert x_atom_args_category_mapping
    assert x_atom_args_category_mapping.get(stop_want_str())
    assert x_atom_args_category_mapping.get(stop_want_str()) == {bud_itemunit_str()}
    assert x_atom_args_category_mapping.get(parent_road_str())
    road_categorys = x_atom_args_category_mapping.get(road_str())
    assert bud_item_factunit_str() in road_categorys
    assert bud_item_teamlink_str() in road_categorys
    assert len(road_categorys) == 6
    assert len(x_atom_args_category_mapping) == 43


def get_jaar_type(x_category: str, x_arg: str) -> str:
    atom_config_dict = get_atom_config_dict()
    category_dict = atom_config_dict.get(x_category)
    optional_dict = category_dict.get(jvalues_str())
    required_dict = category_dict.get(jkeys_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = category_dict.get(jvalues_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(jaar_type_str())


def test_get_jaar_type_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_jaar_type(bud_acctunit_str(), acct_id_str()) == type_AcctID_str()
    assert get_jaar_type(bud_itemunit_str(), gogo_want_str()) == "float"


def test_get_allowed_jaar_types_ReturnsObj():
    # ESTABLISH
    x_allowed_jaar_types = {
        "int",
        type_AcctID_str(),
        type_GroupID_str(),
        type_IdeaUnit_str(),
        type_RoadUnit_str(),
        "float",
        "bool",
        "TimeLinePoint",
    }

    # WHEN / THEN
    assert get_allowed_jaar_types() == x_allowed_jaar_types


def test_get_atom_config_dict_ValidatePythonTypes():
    # make sure all atom config python types are valid and repeated args are the same
    # ESTABLISH WHEN / THEN
    assert all_atom_config_jaar_types_are_valid(get_allowed_jaar_types())


def all_atom_config_jaar_types_are_valid(allowed_jaar_types):
    x_atom_args_category_mapping = get_atom_args_category_mapping()
    for x_atom_arg, categorys in x_atom_args_category_mapping.items():
        old_jaar_type = None
        x_jaar_type = ""
        for x_category in categorys:
            x_jaar_type = get_jaar_type(x_category, x_atom_arg)
            # print(f"{x_jaar_type=} {x_atom_arg=} {x_category=}")
            if x_jaar_type not in allowed_jaar_types:
                return False

            if old_jaar_type is None:
                old_jaar_type = x_jaar_type
            # confirm each atom_arg has same data type in all categorys
            print(f"{x_jaar_type=} {old_jaar_type=} {x_atom_arg=} {x_category=}")
            if x_jaar_type != old_jaar_type:
                return False
            old_jaar_type = x_jaar_type
    return True


def all_atom_args_jaar_types_are_correct(x_jaar_types) -> bool:
    x_atom_args_category_mapping = get_atom_args_category_mapping()
    x_sorted_jaar_types = sorted(list(x_jaar_types.keys()))
    for x_atom_arg in x_sorted_jaar_types:
        x_categorys = list(x_atom_args_category_mapping.get(x_atom_arg))
        x_category = x_categorys[0]
        x_jaar_type = get_jaar_type(x_category, x_atom_arg)
        print(
            f"assert x_jaar_types.get({x_atom_arg}) == {x_jaar_type} {x_jaar_types.get(x_atom_arg)=}"
        )
        if x_jaar_types.get(x_atom_arg) != x_jaar_type:
            return False
    return True


def test_get_atom_args_jaar_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_jaar_types = get_atom_args_jaar_types()

    # THEN
    assert x_jaar_types.get(acct_id_str()) == type_AcctID_str()
    assert x_jaar_types.get(addin_str()) == "float"
    assert x_jaar_types.get(awardee_id_str()) == type_GroupID_str()
    assert x_jaar_types.get(base_str()) == type_RoadUnit_str()
    assert x_jaar_types.get("base_item_active_requisite") == "bool"
    assert x_jaar_types.get(begin_str()) == "float"
    assert x_jaar_types.get(respect_bit_str()) == "float"
    assert x_jaar_types.get(close_str()) == "float"
    assert x_jaar_types.get(credit_belief_str()) == "int"
    assert x_jaar_types.get(credit_vote_str()) == "int"
    assert x_jaar_types.get(credor_respect_str()) == "int"
    assert x_jaar_types.get(debtit_belief_str()) == "int"
    assert x_jaar_types.get(debtit_vote_str()) == "int"
    assert x_jaar_types.get(debtor_respect_str()) == "int"
    assert x_jaar_types.get(denom_str()) == "int"
    assert x_jaar_types.get("divisor") == "int"
    assert x_jaar_types.get(fnigh_str()) == "float"
    assert x_jaar_types.get(fopen_str()) == "float"
    assert x_jaar_types.get(fund_coin_str()) == "float"
    assert x_jaar_types.get("fund_pool") == "float"
    assert x_jaar_types.get("give_force") == "float"
    assert x_jaar_types.get(gogo_want_str()) == "float"
    assert x_jaar_types.get(group_id_str()) == type_GroupID_str()
    assert x_jaar_types.get(healer_id_str()) == type_GroupID_str()
    assert x_jaar_types.get("label") == type_IdeaUnit_str()
    assert x_jaar_types.get("mass") == "int"
    assert x_jaar_types.get("max_tree_traverse") == "int"
    assert x_jaar_types.get(morph_str()) == "bool"
    assert x_jaar_types.get("need") == type_RoadUnit_str()
    assert x_jaar_types.get("nigh") == "float"
    assert x_jaar_types.get(numor_str()) == "int"
    assert x_jaar_types.get("open") == "float"
    assert x_jaar_types.get(parent_road_str()) == type_RoadUnit_str()
    assert x_jaar_types.get(penny_str()) == "float"
    assert x_jaar_types.get("pick") == type_RoadUnit_str()
    assert x_jaar_types.get("pledge") == "bool"
    assert x_jaar_types.get("problem_bool") == "bool"
    assert x_jaar_types.get("purview_time_id") == "TimeLinePoint"
    assert x_jaar_types.get(road_str()) == type_RoadUnit_str()
    assert x_jaar_types.get(stop_want_str()) == "float"
    assert x_jaar_types.get("take_force") == "float"
    assert x_jaar_types.get("tally") == "int"
    assert x_jaar_types.get(team_id_str()) == type_GroupID_str()
    assert x_jaar_types.keys() == get_atom_args_category_mapping().keys()
    assert all_atom_args_jaar_types_are_correct(x_jaar_types)
