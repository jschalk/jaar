from src.a00_data_toolbox.dict_toolbox import get_from_nested_dict
from src.a06_believer_logic.test._util.a06_str import (
    LabelTerm_str,
    NameTerm_str,
    RopeTerm_str,
    TitleTerm_str,
    addin_str,
    awardee_title_str,
    begin_str,
    believer_partner_membership_str,
    believer_partnerunit_str,
    believer_plan_awardlink_str,
    believer_plan_factunit_str,
    believer_plan_healerlink_str,
    believer_plan_laborlink_str,
    believer_plan_reason_caseunit_str,
    believer_plan_reasonunit_str,
    believer_planunit_str,
    believerunit_str,
    close_str,
    credor_respect_str,
    debtor_respect_str,
    denom_str,
    fact_context_str,
    fact_lower_str,
    fact_upper_str,
    fund_iota_str,
    gogo_want_str,
    group_cred_points_str,
    group_debt_points_str,
    group_title_str,
    healer_name_str,
    labor_title_str,
    morph_str,
    numor_str,
    parent_rope_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
    partner_pool_str,
    penny_str,
    plan_rope_str,
    reason_context_str,
    respect_bit_str,
    stop_want_str,
)
from src.a08_believer_atom_logic.atom_config import (
    get_all_believer_dimen_delete_keys,
    get_all_believer_dimen_keys,
    get_allowed_class_types,
    get_atom_args_class_types,
    get_atom_args_dimen_mapping,
    get_atom_config_dict,
    get_atom_order as q_order,
    get_believer_dimens,
    get_delete_key_name,
    get_flattened_atom_table_build,
    get_normalized_believer_table_build,
    get_sorted_jkey_keys,
    is_believer_dimen,
    set_mog,
)
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    class_type_str,
    column_order_str,
    crud_str,
    dimen_str,
    jkeys_str,
    jvalues_str,
    nesting_order_str,
    normal_specs_str,
    normal_table_name_str,
    sqlite_datatype_str,
)


def test_get_believer_dimens_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_believer_dimens() == set(get_atom_config_dict().keys())
    assert believer_partnerunit_str() in get_believer_dimens()
    assert is_believer_dimen("planroot") is False


def test_get_all_believer_dimen_keys_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    all_believer_dimen_keys = get_all_believer_dimen_keys()

    # THEN
    assert not all_believer_dimen_keys.isdisjoint({"partner_name"})
    expected_believer_keys = set()
    for believer_dimen in get_believer_dimens():
        expected_believer_keys.update(_get_atom_config_jkey_keys(believer_dimen))

    expected_believer_keys.add("believer_name")
    print(f"{expected_believer_keys=}")
    assert all_believer_dimen_keys == expected_believer_keys


def test_get_delete_key_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_delete_key_name("Fay") == "Fay_ERASE"
    assert get_delete_key_name("run") == "run_ERASE"
    assert get_delete_key_name("") is None


def test_get_all_believer_dimen_delete_keys_ReturnsObj():
    # ESTABLISH / WHEN
    all_believer_dimen_delete_keys = get_all_believer_dimen_delete_keys()

    # THEN
    assert not all_believer_dimen_delete_keys.isdisjoint(
        {get_delete_key_name("partner_name")}
    )
    expected_believer_delete_keys = {
        get_delete_key_name(believer_dimen_key)
        for believer_dimen_key in get_all_believer_dimen_keys()
    }
    print(f"{expected_believer_delete_keys=}")
    assert all_believer_dimen_delete_keys == expected_believer_delete_keys


def _check_every_crud_dict_has_element(atom_config_dict, atom_order_str):
    for dimen, dimen_dict in atom_config_dict.items():
        if dimen_dict.get(INSERT_str()) is not None:
            dimen_insert = dimen_dict.get(INSERT_str())
            if dimen_insert.get(atom_order_str) is None:
                x_str = f"Missing from {dimen} {INSERT_str()} {dimen_insert.get(atom_order_str)=}"
                print(x_str)
                return False

        if dimen_dict.get(UPDATE_str()) is not None:
            dimen_update = dimen_dict.get(UPDATE_str())
            if dimen_update.get(atom_order_str) is None:
                x_str = f"Missing from {dimen} {UPDATE_str()} {dimen_update.get(atom_order_str)=}"
                print(x_str)
                return False

        if dimen_dict.get(DELETE_str()) is not None:
            dimen_delete = dimen_dict.get(DELETE_str())
            if dimen_delete.get(atom_order_str) is None:
                x_str = f"Missing from {dimen} {DELETE_str()} {dimen_delete.get(atom_order_str)=}"
                print(x_str)
                return False

        if dimen_dict.get(normal_specs_str()) is None:
            print(f"{dimen=} {normal_specs_str()} is missing")
            return False
    return True


def test_get_atom_config_dict_EveryCrudOperationHasBelieverDeltaOrderGroup():
    # ESTABLISH
    atom_order_str = "atom_order"
    mog = atom_order_str

    # WHEN / THEN
    assert _check_every_crud_dict_has_element(get_atom_config_dict(), atom_order_str)
    # # Simple script for editing atom_config.json
    # set_mog(INSERT_str(), believer_partnerunit_str(), 0)
    # set_mog(INSERT_str(), believer_partner_membership_str(), 1)
    # set_mog(INSERT_str(), believer_planunit_str(), 2)
    # set_mog(INSERT_str(), believer_plan_awardlink_str(), 3)
    # set_mog(INSERT_str(), believer_plan_laborlink_str(), 4)
    # set_mog(INSERT_str(), believer_plan_healerlink_str(), 5)
    # set_mog(INSERT_str(), believer_plan_factunit_str(), 6)
    # set_mog(INSERT_str(), believer_plan_reasonunit_str(), 7)
    # set_mog(INSERT_str(), believer_plan_reason_caseunit_str(), 8)
    # set_mog(UPDATE_str(), believer_partnerunit_str(), 9)
    # set_mog(UPDATE_str(), believer_partner_membership_str(), 10)
    # set_mog(UPDATE_str(), believer_planunit_str(), 11)
    # set_mog(UPDATE_str(), believer_plan_awardlink_str(), 12)
    # set_mog(UPDATE_str(), believer_plan_factunit_str(), 13)
    # set_mog(UPDATE_str(), believer_plan_reason_caseunit_str(), 14)
    # set_mog(UPDATE_str(), believer_plan_reasonunit_str(), 15)
    # set_mog(DELETE_str(), believer_plan_reason_caseunit_str(), 16)
    # set_mog(DELETE_str(), believer_plan_reasonunit_str(), 17)
    # set_mog(DELETE_str(), believer_plan_factunit_str(), 18)
    # set_mog(DELETE_str(), believer_plan_laborlink_str(), 19)
    # set_mog(DELETE_str(), believer_plan_healerlink_str(), 20)
    # set_mog(DELETE_str(), believer_plan_awardlink_str(), 21)
    # set_mog(DELETE_str(), believer_planunit_str(), 22)
    # set_mog(DELETE_str(), believer_partner_membership_str(), 23)
    # set_mog(DELETE_str(), believer_partnerunit_str(), 24)
    # set_mog(UPDATE_str(), believerunit_str(), 25)

    assert 0 == q_order(INSERT_str(), believer_partnerunit_str())
    assert 1 == q_order(INSERT_str(), believer_partner_membership_str())
    assert 2 == q_order(INSERT_str(), believer_planunit_str())
    assert 3 == q_order(INSERT_str(), believer_plan_awardlink_str())
    assert 4 == q_order(INSERT_str(), believer_plan_laborlink_str())
    assert 5 == q_order(INSERT_str(), believer_plan_healerlink_str())
    assert 6 == q_order(INSERT_str(), believer_plan_factunit_str())
    assert 7 == q_order(INSERT_str(), believer_plan_reasonunit_str())
    assert 8 == q_order(INSERT_str(), believer_plan_reason_caseunit_str())
    assert 9 == q_order(UPDATE_str(), believer_partnerunit_str())
    assert 10 == q_order(UPDATE_str(), believer_partner_membership_str())
    assert 11 == q_order(UPDATE_str(), believer_planunit_str())
    assert 12 == q_order(UPDATE_str(), believer_plan_awardlink_str())
    assert 13 == q_order(UPDATE_str(), believer_plan_factunit_str())
    assert 14 == q_order(UPDATE_str(), believer_plan_reason_caseunit_str())
    assert 15 == q_order(UPDATE_str(), believer_plan_reasonunit_str())
    assert 16 == q_order(DELETE_str(), believer_plan_reason_caseunit_str())
    assert 17 == q_order(DELETE_str(), believer_plan_reasonunit_str())
    assert 18 == q_order(DELETE_str(), believer_plan_factunit_str())
    assert 19 == q_order(DELETE_str(), believer_plan_laborlink_str())
    assert 20 == q_order(DELETE_str(), believer_plan_healerlink_str())
    assert 21 == q_order(DELETE_str(), believer_plan_awardlink_str())
    assert 22 == q_order(DELETE_str(), believer_planunit_str())
    assert 23 == q_order(DELETE_str(), believer_partner_membership_str())
    assert 24 == q_order(DELETE_str(), believer_partnerunit_str())
    assert 25 == q_order(UPDATE_str(), believerunit_str())


def _get_atom_config_jkeys_len(x_dimen: str) -> int:
    jkeys_key_list = [x_dimen, jkeys_str()]
    return len(get_from_nested_dict(get_atom_config_dict(), jkeys_key_list))


def _get_atom_config_jvalues_len(x_dimen: str) -> int:
    jvalues_key_list = [x_dimen, jvalues_str()]
    return len(get_from_nested_dict(get_atom_config_dict(), jvalues_key_list))


def test_get_atom_config_dict_CheckEachDimenHasCorrectArgCount():
    # ESTABLISH
    assert _get_atom_config_jkeys_len(believerunit_str()) == 0
    assert _get_atom_config_jkeys_len(believer_partnerunit_str()) == 1
    assert _get_atom_config_jkeys_len(believer_partner_membership_str()) == 2
    assert _get_atom_config_jkeys_len(believer_planunit_str()) == 1
    assert _get_atom_config_jkeys_len(believer_plan_awardlink_str()) == 2
    assert _get_atom_config_jkeys_len(believer_plan_reasonunit_str()) == 2
    assert _get_atom_config_jkeys_len(believer_plan_reason_caseunit_str()) == 3
    assert _get_atom_config_jkeys_len(believer_plan_laborlink_str()) == 2
    assert _get_atom_config_jkeys_len(believer_plan_healerlink_str()) == 2
    assert _get_atom_config_jkeys_len(believer_plan_factunit_str()) == 2

    assert _get_atom_config_jvalues_len(believerunit_str()) == 8
    assert _get_atom_config_jvalues_len(believer_partnerunit_str()) == 2
    assert _get_atom_config_jvalues_len(believer_partner_membership_str()) == 2
    assert _get_atom_config_jvalues_len(believer_planunit_str()) == 11
    assert _get_atom_config_jvalues_len(believer_plan_awardlink_str()) == 2
    assert _get_atom_config_jvalues_len(believer_plan_reasonunit_str()) == 1
    assert _get_atom_config_jvalues_len(believer_plan_reason_caseunit_str()) == 3
    assert _get_atom_config_jvalues_len(believer_plan_laborlink_str()) == 0
    assert _get_atom_config_jvalues_len(believer_plan_healerlink_str()) == 0
    assert _get_atom_config_jvalues_len(believer_plan_factunit_str()) == 3


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
    # When ChangUnit places an BelieverAtom in a nested dictionary ChangUnit.believeratoms
    # the order of required argments decides the location. The order must be
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
        if plan_rope_str() in new_jkey_keys:
            new_jkey_keys.remove(plan_rope_str())
        if reason_context_str() in new_jkey_keys:
            new_jkey_keys.remove(reason_context_str())
        if partner_name_str() in new_jkey_keys:
            new_jkey_keys.remove(partner_name_str())
        if group_title_str() in new_jkey_keys:
            new_jkey_keys.remove(group_title_str())
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


def test_get_sorted_jkey_keys_ReturnsObj_believer_partnerunit():
    # ESTABLISH
    x_dimen = believer_partnerunit_str()

    # WHEN
    x_sorted_jkey_keys = get_sorted_jkey_keys(x_dimen)

    # THEN
    assert x_sorted_jkey_keys == [partner_name_str()]


def test_get_sorted_jkey_keys_ReturnsObj_believer_plan_reason_caseunit():
    # ESTABLISH
    x_dimen = believer_plan_reason_caseunit_str()

    # WHEN
    x_sorted_jkey_keys = get_sorted_jkey_keys(x_dimen)

    # THEN
    assert x_sorted_jkey_keys == [plan_rope_str(), reason_context_str(), "reason_state"]


def test_get_flattened_atom_table_build_ReturnsObj():
    # ESTABLISH / WHEN
    atom_columns = get_flattened_atom_table_build()

    # THEN
    assert len(atom_columns) == 103
    assert atom_columns.get("believerunit_UPDATE_credor_respect") == "REAL"
    # print(f"{atom_columns.keys()=}")


def test_get_normalized_believer_table_build_ReturnsObj():
    # ESTABLISH / WHEN
    normalized_believer_table_build = get_normalized_believer_table_build()
    nx = normalized_believer_table_build

    # THEN
    assert len(nx) == 10
    cat_believerunit = nx.get(believerunit_str())
    cat_partnerunit = nx.get(believer_partnerunit_str())
    cat_membership = nx.get(believer_partner_membership_str())
    cat_plan = nx.get(believer_planunit_str())
    cat_awardlink = nx.get(believer_plan_awardlink_str())
    cat_reason = nx.get(believer_plan_reasonunit_str())
    cat_case = nx.get(believer_plan_reason_caseunit_str())
    cat_laborlink = nx.get(believer_plan_laborlink_str())
    cat_healerlink = nx.get(believer_plan_healerlink_str())
    cat_fact = nx.get(believer_plan_factunit_str())

    assert cat_believerunit is not None
    assert cat_partnerunit is not None
    assert cat_membership is not None
    assert cat_plan is not None
    assert cat_awardlink is not None
    assert cat_reason is not None
    assert cat_case is not None
    assert cat_laborlink is not None
    assert cat_healerlink is not None
    assert cat_fact is not None

    normal_specs_believerunit = cat_believerunit.get(normal_specs_str())
    normal_specs_partnerunit = cat_partnerunit.get(normal_specs_str())
    normal_specs_membership = cat_membership.get(normal_specs_str())
    normal_specs_plan = cat_plan.get(normal_specs_str())
    normal_specs_awardlink = cat_awardlink.get(normal_specs_str())
    normal_specs_reason = cat_reason.get(normal_specs_str())
    normal_specs_case = cat_case.get(normal_specs_str())
    normal_specs_laborlink = cat_laborlink.get(normal_specs_str())
    normal_specs_healerlink = cat_healerlink.get(normal_specs_str())
    normal_specs_fact = cat_fact.get(normal_specs_str())

    columns_str = "columns"
    print(f"{cat_believerunit.keys()=}")
    print(f"{normal_specs_str()=}")
    assert normal_specs_believerunit is not None
    assert normal_specs_partnerunit is not None
    assert normal_specs_membership is not None
    assert normal_specs_plan is not None
    assert normal_specs_awardlink is not None
    assert normal_specs_reason is not None
    assert normal_specs_case is not None
    assert normal_specs_laborlink is not None
    assert normal_specs_healerlink is not None
    assert normal_specs_fact is not None

    table_name_believerunit = normal_specs_believerunit.get(normal_table_name_str())
    table_name_partnerunit = normal_specs_partnerunit.get(normal_table_name_str())
    table_name_membership = normal_specs_membership.get(normal_table_name_str())
    table_name_plan = normal_specs_plan.get(normal_table_name_str())
    table_name_awardlink = normal_specs_awardlink.get(normal_table_name_str())
    table_name_reason = normal_specs_reason.get(normal_table_name_str())
    table_name_case = normal_specs_case.get(normal_table_name_str())
    table_name_laborlink = normal_specs_laborlink.get(normal_table_name_str())
    table_name_healerlink = normal_specs_healerlink.get(normal_table_name_str())
    table_name_fact = normal_specs_fact.get(normal_table_name_str())

    assert table_name_believerunit == "believer"
    assert table_name_partnerunit == "partnerunit"
    assert table_name_membership == "membership"
    assert table_name_plan == "plan"
    assert table_name_awardlink == "awardlink"
    assert table_name_reason == "reason"
    assert table_name_case == "case"
    assert table_name_laborlink == "laborlink"
    assert table_name_healerlink == "healerlink"
    assert table_name_fact == "fact"

    assert len(cat_believerunit) == 2
    assert cat_believerunit.get(columns_str) is not None

    believerunit_columns = cat_believerunit.get(columns_str)
    assert len(believerunit_columns) == 9
    assert believerunit_columns.get("uid") is not None
    assert believerunit_columns.get("max_tree_traverse") is not None
    assert believerunit_columns.get(credor_respect_str()) is not None
    assert believerunit_columns.get(debtor_respect_str()) is not None
    assert believerunit_columns.get("fund_pool") is not None
    assert believerunit_columns.get(fund_iota_str()) is not None
    assert believerunit_columns.get(respect_bit_str()) is not None
    assert believerunit_columns.get(penny_str()) is not None
    assert believerunit_columns.get("tally") is not None

    assert len(cat_partnerunit) == 2
    partnerunit_columns = cat_partnerunit.get(columns_str)
    assert len(partnerunit_columns) == 4
    assert partnerunit_columns.get("uid") is not None
    assert partnerunit_columns.get(partner_name_str()) is not None
    assert partnerunit_columns.get(partner_cred_points_str()) is not None
    assert partnerunit_columns.get(partner_debt_points_str()) is not None

    partner_name_dict = partnerunit_columns.get(partner_name_str())
    assert len(partner_name_dict) == 2
    assert partner_name_dict.get(sqlite_datatype_str()) == "TEXT"
    assert partner_name_dict.get("nullable") is False
    partner_debt_points_dict = partnerunit_columns.get("partner_debt_points")
    assert len(partner_name_dict) == 2
    assert partner_debt_points_dict.get(sqlite_datatype_str()) == "REAL"
    assert partner_debt_points_dict.get("nullable") is True

    assert len(cat_plan) == 2
    plan_columns = cat_plan.get(columns_str)
    assert len(plan_columns) == 13
    assert plan_columns.get("uid") is not None
    assert plan_columns.get(plan_rope_str()) is not None
    assert plan_columns.get(begin_str()) is not None
    assert plan_columns.get(close_str()) is not None

    gogo_want_dict = plan_columns.get(gogo_want_str())
    stop_want_dict = plan_columns.get(stop_want_str())
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
    assert x_atom_args_dimen_mapping.get(stop_want_str()) == {believer_planunit_str()}
    assert x_atom_args_dimen_mapping.get(plan_rope_str())
    rope_dimens = x_atom_args_dimen_mapping.get(plan_rope_str())
    assert believer_plan_factunit_str() in rope_dimens
    assert believer_plan_laborlink_str() in rope_dimens
    assert len(rope_dimens) == 7
    assert len(x_atom_args_dimen_mapping) == 41


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
    assert (
        get_class_type(believer_partnerunit_str(), partner_name_str()) == NameTerm_str()
    )
    assert get_class_type(believer_planunit_str(), gogo_want_str()) == "float"


def test_get_allowed_class_types_ReturnsObj():
    # ESTABLISH
    x_allowed_class_types = {
        "int",
        NameTerm_str(),
        TitleTerm_str(),
        LabelTerm_str(),
        RopeTerm_str(),
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
    assert x_class_types.get(partner_name_str()) == NameTerm_str()
    assert x_class_types.get(addin_str()) == "float"
    assert x_class_types.get(awardee_title_str()) == TitleTerm_str()
    assert x_class_types.get(reason_context_str()) == RopeTerm_str()
    assert x_class_types.get("reason_active_requisite") == "bool"
    assert x_class_types.get(begin_str()) == "float"
    assert x_class_types.get(respect_bit_str()) == "float"
    assert x_class_types.get(close_str()) == "float"
    assert x_class_types.get(partner_cred_points_str()) == "float"
    assert x_class_types.get(group_cred_points_str()) == "float"
    assert x_class_types.get(credor_respect_str()) == "float"
    assert x_class_types.get(partner_debt_points_str()) == "float"
    assert x_class_types.get(group_debt_points_str()) == "float"
    assert x_class_types.get(debtor_respect_str()) == "float"
    assert x_class_types.get(denom_str()) == "int"
    assert x_class_types.get("reason_divisor") == "int"
    assert x_class_types.get(fact_context_str()) == RopeTerm_str()
    assert x_class_types.get(fact_upper_str()) == "float"
    assert x_class_types.get(fact_lower_str()) == "float"
    assert x_class_types.get(fund_iota_str()) == "float"
    assert x_class_types.get("fund_pool") == "float"
    assert x_class_types.get("give_force") == "float"
    assert x_class_types.get(gogo_want_str()) == "float"
    assert x_class_types.get(group_title_str()) == TitleTerm_str()
    assert x_class_types.get(healer_name_str()) == NameTerm_str()
    assert x_class_types.get("mass") == "int"
    assert x_class_types.get("max_tree_traverse") == "int"
    assert x_class_types.get(morph_str()) == "bool"
    assert x_class_types.get("reason_state") == RopeTerm_str()
    assert x_class_types.get("reason_upper") == "float"
    assert x_class_types.get(numor_str()) == "int"
    assert x_class_types.get("reason_lower") == "float"
    assert x_class_types.get(penny_str()) == "float"
    assert x_class_types.get("fact_state") == RopeTerm_str()
    assert x_class_types.get("task") == "bool"
    assert x_class_types.get("problem_bool") == "bool"
    assert x_class_types.get(plan_rope_str()) == RopeTerm_str()
    assert x_class_types.get(stop_want_str()) == "float"
    assert x_class_types.get("take_force") == "float"
    assert x_class_types.get("tally") == "int"
    assert x_class_types.get(labor_title_str()) == TitleTerm_str()
    assert x_class_types.keys() == get_atom_args_dimen_mapping().keys()
    assert all_atom_args_class_types_are_correct(x_class_types)
