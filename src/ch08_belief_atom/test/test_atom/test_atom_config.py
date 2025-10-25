from src.ch01_py.dict_toolbox import get_from_nested_dict
from src.ch07_belief_logic.belief_config import get_belief_config_dict
from src.ch08_belief_atom._ref.ch08_semantic_types import CRUD_command
from src.ch08_belief_atom.atom_config import (
    get_all_belief_dimen_delete_keys,
    get_all_belief_dimen_keys,
    get_allowed_class_types,
    get_atom_args_class_types,
    get_atom_args_dimen_mapping,
    get_atom_config_dict,
    get_atom_order as q_order,
    get_belief_dimens,
    get_delete_key_name,
    get_flattened_atom_table_build,
    get_normalized_belief_table_build,
    get_sorted_jkey_keys,
    is_belief_dimen,
    set_mog,
)
from src.ref.keywords import Ch08Keywords as kw


def test_CRUD_command_Exists():
    # ESTABLISH / WHEN / THEN
    assert CRUD_command(kw.UPDATE) == str(kw.UPDATE)
    assert CRUD_command(kw.DELETE) == str(kw.DELETE)
    assert CRUD_command(kw.INSERT) == str(kw.INSERT)


def test_get_belief_dimens_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_belief_dimens() == set(get_atom_config_dict().keys())
    assert kw.belief_voiceunit in get_belief_dimens()
    assert is_belief_dimen(kw.planroot) is False


def test_get_all_belief_dimen_keys_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    all_belief_dimen_keys = get_all_belief_dimen_keys()

    # THEN
    assert not all_belief_dimen_keys.isdisjoint({kw.voice_name})
    expected_belief_keys = set()
    for belief_dimen in get_belief_dimens():
        expected_belief_keys.update(_get_atom_config_jkey_keys(belief_dimen))

    expected_belief_keys.add(kw.belief_name)
    print(f"{expected_belief_keys=}")
    assert all_belief_dimen_keys == expected_belief_keys


def test_get_delete_key_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_delete_key_name("Fay") == "Fay_ERASE"
    assert get_delete_key_name("run") == "run_ERASE"
    assert get_delete_key_name("") is None


def test_get_all_belief_dimen_delete_keys_ReturnsObj():
    # ESTABLISH / WHEN
    all_belief_dimen_delete_keys = get_all_belief_dimen_delete_keys()

    # THEN
    assert not all_belief_dimen_delete_keys.isdisjoint(
        {get_delete_key_name(kw.voice_name)}
    )
    expected_belief_delete_keys = {
        get_delete_key_name(belief_dimen_key)
        for belief_dimen_key in get_all_belief_dimen_keys()
    }
    print(f"{expected_belief_delete_keys=}")
    assert all_belief_dimen_delete_keys == expected_belief_delete_keys


def test_get_atom_config_dict_ReturnsObj_Mirrors_belief_config():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    atom_config_dict = get_atom_config_dict()

    # THEN
    belief_config_dict = get_belief_config_dict()
    atom_config_dimens = set(atom_config_dict.keys())
    belief_config_dimens = set(belief_config_dict.keys())
    assert atom_config_dimens.issubset(belief_config_dimens)
    assert belief_config_dimens.difference(atom_config_dimens) == {kw.belief_groupunit}
    for atom_dimen, dimen_dict in atom_config_dict.items():
        for attr_key, atom_attr_dict in dimen_dict.items():
            if attr_key in kw.jkeys:
                atom_attr_keys = set(atom_attr_dict.keys())
                print(f"{atom_dimen=} {attr_key=} {len(atom_attr_keys)=}")
                belief_jkeys_dict = belief_config_dict.get(atom_dimen).get(kw.jkeys)
                belief_jkeys_keys = set(belief_jkeys_dict.keys())
                print(f"{atom_dimen=} {attr_key=} {len(belief_jkeys_keys)=}")
                assert atom_attr_keys.issubset(belief_jkeys_keys)
            elif attr_key in kw.jvalues:
                atom_attr_keys = set(atom_attr_dict.keys())
                print(f"{atom_dimen=} {attr_key=} {len(atom_attr_keys)=}")
                belief_dict = belief_config_dict.get(atom_dimen).get(kw.jvalues)
                belief_keys = set(belief_dict.keys())
                print(f"{atom_dimen=} {attr_key=} {len(belief_keys)=}")
                assert atom_attr_keys.issubset(belief_keys)


def _check_every_crud_dict_has_element(atom_config_dict, atom_order_str):
    for dimen, dimen_dict in atom_config_dict.items():
        if dimen_dict.get(kw.INSERT) is not None:
            dimen_insert = dimen_dict.get(kw.INSERT)
            if dimen_insert.get(atom_order_str) is None:
                x_str = f"Missing from {dimen} {kw.INSERT} {dimen_insert.get(atom_order_str)=}"
                print(x_str)
                return False

        if dimen_dict.get(kw.UPDATE) is not None:
            dimen_update = dimen_dict.get(kw.UPDATE)
            if dimen_update.get(atom_order_str) is None:
                x_str = f"Missing from {dimen} {kw.UPDATE} {dimen_update.get(atom_order_str)=}"
                print(x_str)
                return False

        if dimen_dict.get(kw.DELETE) is not None:
            dimen_delete = dimen_dict.get(kw.DELETE)
            if dimen_delete.get(atom_order_str) is None:
                x_str = f"Missing from {dimen} {kw.DELETE} {dimen_delete.get(atom_order_str)=}"
                print(x_str)
                return False

        if dimen_dict.get(kw.normal_specs) is None:
            print(f"{dimen=} {kw.normal_specs} is missing")
            return False
    return True


def test_get_atom_config_dict_EveryCrudOperationHasBeliefDeltaOrderGroup():
    # ESTABLISH
    atom_order_str = "atom_order"
    mog = atom_order_str

    # WHEN / THEN
    assert _check_every_crud_dict_has_element(get_atom_config_dict(), atom_order_str)
    # # Simple script for editing atom_config.json
    # set_mog(kw.INSERT, kw.belief_voiceunit, 0)
    # set_mog(kw.INSERT, kw.belief_voice_membership, 1)
    # set_mog(kw.INSERT, kw.belief_planunit, 2)
    # set_mog(kw.INSERT, kw.belief_plan_awardunit, 3)
    # set_mog(kw.INSERT, kw.belief_plan_partyunit, 4)
    # set_mog(kw.INSERT, kw.belief_plan_healerunit, 5)
    # set_mog(kw.INSERT, kw.belief_plan_factunit, 6)
    # set_mog(kw.INSERT, kw.belief_plan_reasonunit, 7)
    # set_mog(kw.INSERT, kw.belief_plan_reason_caseunit, 8)
    # set_mog(kw.UPDATE, kw.belief_voiceunit, 9)
    # set_mog(kw.UPDATE, kw.belief_voice_membership, 10)
    # set_mog(kw.UPDATE, kw.belief_planunit, 11)
    # set_mog(kw.UPDATE, kw.belief_plan_awardunit, 12)
    # set_mog(kw.UPDATE, kw.belief_plan_factunit, 13)
    # set_mog(kw.UPDATE, kw.belief_plan_reason_caseunit, 14)
    # set_mog(kw.UPDATE, kw.belief_plan_reasonunit, 15)
    # set_mog(kw.DELETE, kw.belief_plan_reason_caseunit, 16)
    # set_mog(kw.DELETE, kw.belief_plan_reasonunit, 17)
    # set_mog(kw.DELETE, kw.belief_plan_factunit, 18)
    # set_mog(kw.DELETE, kw.belief_plan_partyunit, 19)
    # set_mog(kw.DELETE, kw.belief_plan_healerunit, 20)
    # set_mog(kw.DELETE, kw.belief_plan_awardunit, 21)
    # set_mog(kw.DELETE, kw.belief_planunit, 22)
    # set_mog(kw.DELETE, kw.belief_voice_membership, 23)
    # set_mog(kw.DELETE, kw.belief_voiceunit, 24)
    # set_mog(kw.UPDATE, kw.beliefunit, 25)

    assert 0 == q_order(kw.INSERT, kw.belief_voiceunit)
    assert 1 == q_order(kw.INSERT, kw.belief_voice_membership)
    assert 2 == q_order(kw.INSERT, kw.belief_planunit)
    assert 3 == q_order(kw.INSERT, kw.belief_plan_awardunit)
    assert 4 == q_order(kw.INSERT, kw.belief_plan_partyunit)
    assert 5 == q_order(kw.INSERT, kw.belief_plan_healerunit)
    assert 6 == q_order(kw.INSERT, kw.belief_plan_factunit)
    assert 7 == q_order(kw.INSERT, kw.belief_plan_reasonunit)
    assert 8 == q_order(kw.INSERT, kw.belief_plan_reason_caseunit)
    assert 9 == q_order(kw.UPDATE, kw.belief_voiceunit)
    assert 10 == q_order(kw.UPDATE, kw.belief_voice_membership)
    assert 11 == q_order(kw.UPDATE, kw.belief_planunit)
    assert 12 == q_order(kw.UPDATE, kw.belief_plan_awardunit)
    assert 13 == q_order(kw.UPDATE, kw.belief_plan_factunit)
    assert 14 == q_order(kw.UPDATE, kw.belief_plan_reason_caseunit)
    assert 15 == q_order(kw.UPDATE, kw.belief_plan_reasonunit)
    assert 16 == q_order(kw.DELETE, kw.belief_plan_reason_caseunit)
    assert 17 == q_order(kw.DELETE, kw.belief_plan_reasonunit)
    assert 18 == q_order(kw.DELETE, kw.belief_plan_factunit)
    assert 19 == q_order(kw.DELETE, kw.belief_plan_partyunit)
    assert 20 == q_order(kw.DELETE, kw.belief_plan_healerunit)
    assert 21 == q_order(kw.DELETE, kw.belief_plan_awardunit)
    assert 22 == q_order(kw.DELETE, kw.belief_planunit)
    assert 23 == q_order(kw.DELETE, kw.belief_voice_membership)
    assert 24 == q_order(kw.DELETE, kw.belief_voiceunit)
    assert 25 == q_order(kw.UPDATE, kw.beliefunit)


def _get_atom_config_jkeys_len(x_dimen: str) -> int:
    jkeys_key_list = [x_dimen, kw.jkeys]
    return len(get_from_nested_dict(get_atom_config_dict(), jkeys_key_list))


def _get_atom_config_jvalues_len(x_dimen: str) -> int:
    jvalues_key_list = [x_dimen, kw.jvalues]
    return len(get_from_nested_dict(get_atom_config_dict(), jvalues_key_list))


def test_get_atom_config_dict_CheckEachDimenHasCorrectArgCount():
    # ESTABLISH / WHEN / THEN
    assert _get_atom_config_jkeys_len(kw.beliefunit) == 0
    assert _get_atom_config_jkeys_len(kw.belief_voiceunit) == 1
    assert _get_atom_config_jkeys_len(kw.belief_voice_membership) == 2
    assert _get_atom_config_jkeys_len(kw.belief_planunit) == 1
    assert _get_atom_config_jkeys_len(kw.belief_plan_awardunit) == 2
    assert _get_atom_config_jkeys_len(kw.belief_plan_reasonunit) == 2
    assert _get_atom_config_jkeys_len(kw.belief_plan_reason_caseunit) == 3
    assert _get_atom_config_jkeys_len(kw.belief_plan_partyunit) == 2
    assert _get_atom_config_jkeys_len(kw.belief_plan_healerunit) == 2
    assert _get_atom_config_jkeys_len(kw.belief_plan_factunit) == 2

    assert _get_atom_config_jvalues_len(kw.beliefunit) == 8
    assert _get_atom_config_jvalues_len(kw.belief_voiceunit) == 2
    assert _get_atom_config_jvalues_len(kw.belief_voice_membership) == 2
    assert _get_atom_config_jvalues_len(kw.belief_planunit) == 11
    assert _get_atom_config_jvalues_len(kw.belief_plan_awardunit) == 2
    assert _get_atom_config_jvalues_len(kw.belief_plan_reasonunit) == 1
    assert _get_atom_config_jvalues_len(kw.belief_plan_reason_caseunit) == 3
    assert _get_atom_config_jvalues_len(kw.belief_plan_partyunit) == 1
    assert _get_atom_config_jvalues_len(kw.belief_plan_healerunit) == 0
    assert _get_atom_config_jvalues_len(kw.belief_plan_factunit) == 3


def _has_every_element(x_arg, x_dict) -> bool:
    arg_elements = {kw.class_type, kw.sqlite_datatype, kw.column_order}
    for arg_element in arg_elements:
        if x_dict.get(arg_element) is None:
            print(f"{arg_element} failed for {x_arg=}")
            return False
    return True


def _every_dimen_dict_has_arg_elements(dimen_dict: dict) -> bool:
    for jkey, x_dict in dimen_dict.get(kw.jkeys).items():
        if not _has_every_element(jkey, x_dict):
            return False
    if dimen_dict.get(kw.jvalues) is not None:
        for jvalue, x_dict in dimen_dict.get(kw.jvalues).items():
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
        jkeys = atom_value.get(kw.jkeys)
        if len(jkeys) > 1:
            multi_jkey_dict[atom_key] = jkeys
    # print(f"{multi_jkey_dict.keys()=}")
    for atom_key, jkeys in multi_jkey_dict.items():
        for jkey_key, jkeys_dict in jkeys.items():
            jkey_nesting_order = jkeys_dict.get(kw.nesting_order)
            print(f"{atom_key=} {jkey_key=} {jkey_nesting_order=}")
            if jkey_nesting_order is None:
                return False
    return True


def test_atom_config_NestingOrderExists():
    # When ChangUnit places an BeliefAtom in a nested dictionary ChangUnit.beliefatoms
    # the order of required argments decides the location. The order must be
    # the same. All atom_config elements with two or more required args
    # must assign to each of those args a nesting order

    # ESTABLISH / WHEN / THEN
    # grab every atom_config with multiple required args
    assert check_necessary_nesting_order_exists()


def _get_atom_config_jvalue_keys(x_dimen: str) -> set[str]:
    jvalues_key_list = [x_dimen, kw.jvalues]
    return set(get_from_nested_dict(get_atom_config_dict(), jvalues_key_list).keys())


def _get_atom_config_jkey_keys(x_dimen: str) -> set[str]:
    jkeys_key_list = [x_dimen, kw.jkeys]
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
        if kw.plan_rope in new_jkey_keys:
            new_jkey_keys.remove(kw.plan_rope)
        if kw.reason_context in new_jkey_keys:
            new_jkey_keys.remove(kw.reason_context)
        if kw.voice_name in new_jkey_keys:
            new_jkey_keys.remove(kw.voice_name)
        if kw.group_title in new_jkey_keys:
            new_jkey_keys.remove(kw.group_title)
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


def test_get_sorted_jkey_keys_ReturnsObj_belief_voiceunit():
    # ESTABLISH
    x_dimen = kw.belief_voiceunit

    # WHEN
    x_sorted_jkey_keys = get_sorted_jkey_keys(x_dimen)

    # THEN
    assert x_sorted_jkey_keys == [kw.voice_name]


def test_get_sorted_jkey_keys_ReturnsObj_belief_plan_reason_caseunit():
    # ESTABLISH
    x_dimen = kw.belief_plan_reason_caseunit

    # WHEN
    x_sorted_jkey_keys = get_sorted_jkey_keys(x_dimen)

    # THEN
    assert x_sorted_jkey_keys == [
        kw.plan_rope,
        kw.reason_context,
        kw.reason_state,
    ]


def test_get_flattened_atom_table_build_ReturnsObj():
    # ESTABLISH / WHEN
    atom_columns = get_flattened_atom_table_build()

    # THEN
    assert len(atom_columns) == 104
    assert atom_columns.get("beliefunit_UPDATE_credor_respect") == "REAL"
    # print(f"{atom_columns.keys()=}")


def test_get_normalized_belief_table_build_ReturnsObj():
    # ESTABLISH / WHEN
    normalized_belief_table_build = get_normalized_belief_table_build()
    nx = normalized_belief_table_build

    # THEN
    assert len(nx) == 10
    cat_beliefunit = nx.get(kw.beliefunit)
    cat_voiceunit = nx.get(kw.belief_voiceunit)
    cat_membership = nx.get(kw.belief_voice_membership)
    cat_plan = nx.get(kw.belief_planunit)
    cat_awardunit = nx.get(kw.belief_plan_awardunit)
    cat_reason = nx.get(kw.belief_plan_reasonunit)
    cat_case = nx.get(kw.belief_plan_reason_caseunit)
    cat_partyunit = nx.get(kw.belief_plan_partyunit)
    cat_healerunit = nx.get(kw.belief_plan_healerunit)
    cat_fact = nx.get(kw.belief_plan_factunit)

    assert cat_beliefunit is not None
    assert cat_voiceunit is not None
    assert cat_membership is not None
    assert cat_plan is not None
    assert cat_awardunit is not None
    assert cat_reason is not None
    assert cat_case is not None
    assert cat_partyunit is not None
    assert cat_healerunit is not None
    assert cat_fact is not None

    normal_specs_beliefunit = cat_beliefunit.get(kw.normal_specs)
    normal_specs_voiceunit = cat_voiceunit.get(kw.normal_specs)
    normal_specs_membership = cat_membership.get(kw.normal_specs)
    normal_specs_plan = cat_plan.get(kw.normal_specs)
    normal_specs_awardunit = cat_awardunit.get(kw.normal_specs)
    normal_specs_reason = cat_reason.get(kw.normal_specs)
    normal_specs_case = cat_case.get(kw.normal_specs)
    normal_specs_partyunit = cat_partyunit.get(kw.normal_specs)
    normal_specs_healerunit = cat_healerunit.get(kw.normal_specs)
    normal_specs_fact = cat_fact.get(kw.normal_specs)

    columns_str = "columns"
    print(f"{cat_beliefunit.keys()=}")
    print(f"{kw.normal_specs=}")
    assert normal_specs_beliefunit is not None
    assert normal_specs_voiceunit is not None
    assert normal_specs_membership is not None
    assert normal_specs_plan is not None
    assert normal_specs_awardunit is not None
    assert normal_specs_reason is not None
    assert normal_specs_case is not None
    assert normal_specs_partyunit is not None
    assert normal_specs_healerunit is not None
    assert normal_specs_fact is not None

    table_name_beliefunit = normal_specs_beliefunit.get(kw.normal_table_name)
    table_name_voiceunit = normal_specs_voiceunit.get(kw.normal_table_name)
    table_name_membership = normal_specs_membership.get(kw.normal_table_name)
    table_name_plan = normal_specs_plan.get(kw.normal_table_name)
    table_name_awardunit = normal_specs_awardunit.get(kw.normal_table_name)
    table_name_reason = normal_specs_reason.get(kw.normal_table_name)
    table_name_case = normal_specs_case.get(kw.normal_table_name)
    table_name_partyunit = normal_specs_partyunit.get(kw.normal_table_name)
    table_name_healerunit = normal_specs_healerunit.get(kw.normal_table_name)
    table_name_fact = normal_specs_fact.get(kw.normal_table_name)

    assert table_name_beliefunit == "belief"
    assert table_name_voiceunit == "voiceunit"
    assert table_name_membership == "membership"
    assert table_name_plan == "plan"
    assert table_name_awardunit == "awardunit"
    assert table_name_reason == "reason"
    assert table_name_case == "case"
    assert table_name_partyunit == "partyunit"
    assert table_name_healerunit == kw.healerunit
    assert table_name_fact == "fact"

    assert len(cat_beliefunit) == 2
    assert cat_beliefunit.get(columns_str) is not None

    beliefunit_columns = cat_beliefunit.get(columns_str)
    assert len(beliefunit_columns) == 9
    assert beliefunit_columns.get(kw.uid) is not None
    assert beliefunit_columns.get(kw.max_tree_traverse) is not None
    assert beliefunit_columns.get(kw.credor_respect) is not None
    assert beliefunit_columns.get(kw.debtor_respect) is not None
    assert beliefunit_columns.get(kw.fund_pool) is not None
    assert beliefunit_columns.get(kw.fund_grain) is not None
    assert beliefunit_columns.get(kw.respect_grain) is not None
    assert beliefunit_columns.get(kw.mana_grain) is not None
    assert beliefunit_columns.get(kw.tally) is not None

    assert len(cat_voiceunit) == 2
    voiceunit_columns = cat_voiceunit.get(columns_str)
    assert len(voiceunit_columns) == 4
    assert voiceunit_columns.get(kw.uid) is not None
    assert voiceunit_columns.get(kw.voice_name) is not None
    assert voiceunit_columns.get(kw.voice_cred_lumen) is not None
    assert voiceunit_columns.get(kw.voice_debt_lumen) is not None

    voice_name_dict = voiceunit_columns.get(kw.voice_name)
    assert len(voice_name_dict) == 2
    assert voice_name_dict.get(kw.sqlite_datatype) == "TEXT"
    assert voice_name_dict.get("nullable") is False
    voice_debt_lumen_dict = voiceunit_columns.get("voice_debt_lumen")
    assert len(voice_name_dict) == 2
    assert voice_debt_lumen_dict.get(kw.sqlite_datatype) == "REAL"
    assert voice_debt_lumen_dict.get("nullable") is True

    assert len(cat_plan) == 2
    plan_columns = cat_plan.get(columns_str)
    assert len(plan_columns) == 13
    assert plan_columns.get(kw.uid) is not None
    assert plan_columns.get(kw.plan_rope) is not None
    assert plan_columns.get(kw.begin) is not None
    assert plan_columns.get(kw.close) is not None

    gogo_want_dict = plan_columns.get(kw.gogo_want)
    stop_want_dict = plan_columns.get(kw.stop_want)
    assert len(gogo_want_dict) == 2
    assert len(stop_want_dict) == 2
    assert gogo_want_dict.get(kw.sqlite_datatype) == "REAL"
    assert stop_want_dict.get(kw.sqlite_datatype) == "REAL"
    assert gogo_want_dict.get("nullable") is True
    assert stop_want_dict.get("nullable") is True


def test_get_atom_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_atom_args_dimen_mapping = get_atom_args_dimen_mapping()

    # THEN
    assert x_atom_args_dimen_mapping
    assert x_atom_args_dimen_mapping.get(kw.stop_want)
    assert x_atom_args_dimen_mapping.get(kw.stop_want) == {kw.belief_planunit}
    assert x_atom_args_dimen_mapping.get(kw.plan_rope)
    rope_dimens = x_atom_args_dimen_mapping.get(kw.plan_rope)
    assert kw.belief_plan_factunit in rope_dimens
    assert kw.belief_plan_partyunit in rope_dimens
    assert len(rope_dimens) == 7
    assert len(x_atom_args_dimen_mapping) == 42


def get_class_type(x_dimen: str, x_arg: str) -> str:
    atom_config_dict = get_atom_config_dict()
    dimen_dict = atom_config_dict.get(x_dimen)
    optional_dict = dimen_dict.get(kw.jvalues)
    required_dict = dimen_dict.get(kw.jkeys)
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = dimen_dict.get(kw.jvalues).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(kw.class_type)


def test_get_class_type_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_class_type(kw.belief_voiceunit, kw.voice_name) == kw.NameTerm
    assert get_class_type(kw.belief_planunit, kw.gogo_want) == "float"


def test_get_allowed_class_types_ReturnsObj():
    # ESTABLISH
    x_allowed_class_types = {
        "int",
        kw.ContextNum,
        kw.NameTerm,
        kw.TitleTerm,
        kw.LabelTerm,
        kw.RopeTerm,
        "float",
        "bool",
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
    assert x_class_types.get(kw.voice_name) == kw.NameTerm
    assert x_class_types.get(kw.addin) == "float"
    assert x_class_types.get(kw.awardee_title) == kw.TitleTerm
    assert x_class_types.get(kw.reason_context) == kw.RopeTerm
    assert x_class_types.get(kw.active_requisite) == "bool"
    assert x_class_types.get(kw.begin) == "float"
    assert x_class_types.get(kw.respect_grain) == "float"
    assert x_class_types.get(kw.close) == "float"
    assert x_class_types.get(kw.voice_cred_lumen) == "float"
    assert x_class_types.get(kw.group_cred_lumen) == "float"
    assert x_class_types.get(kw.credor_respect) == "float"
    assert x_class_types.get(kw.voice_debt_lumen) == "float"
    assert x_class_types.get(kw.group_debt_lumen) == "float"
    assert x_class_types.get(kw.debtor_respect) == "float"
    assert x_class_types.get(kw.denom) == "int"
    assert x_class_types.get(kw.reason_divisor) == "int"
    assert x_class_types.get(kw.fact_context) == kw.RopeTerm
    assert x_class_types.get(kw.fact_upper) == kw.ContextNum
    assert x_class_types.get(kw.fact_lower) == kw.ContextNum
    assert x_class_types.get(kw.fund_grain) == "float"
    assert x_class_types.get(kw.fund_pool) == "float"
    assert x_class_types.get(kw.give_force) == "float"
    assert x_class_types.get(kw.gogo_want) == "float"
    assert x_class_types.get(kw.group_title) == kw.TitleTerm
    assert x_class_types.get(kw.healer_name) == kw.NameTerm
    assert x_class_types.get(kw.star) == "int"
    assert x_class_types.get(kw.max_tree_traverse) == "int"
    assert x_class_types.get(kw.morph) == "bool"
    assert x_class_types.get(kw.reason_state) == kw.RopeTerm
    assert x_class_types.get(kw.reason_upper) == kw.ContextNum
    assert x_class_types.get(kw.numor) == "int"
    assert x_class_types.get(kw.reason_lower) == kw.ContextNum
    assert x_class_types.get(kw.mana_grain) == "float"
    assert x_class_types.get(kw.fact_state) == kw.RopeTerm
    assert x_class_types.get(kw.pledge) == "bool"
    assert x_class_types.get(kw.problem_bool) == "bool"
    assert x_class_types.get(kw.plan_rope) == kw.RopeTerm
    assert x_class_types.get(kw.solo) == "int"
    assert x_class_types.get(kw.stop_want) == "float"
    assert x_class_types.get(kw.take_force) == "float"
    assert x_class_types.get(kw.tally) == "int"
    assert x_class_types.get(kw.party_title) == kw.TitleTerm
    assert x_class_types.keys() == get_atom_args_dimen_mapping().keys()
    assert all_atom_args_class_types_are_correct(x_class_types)
