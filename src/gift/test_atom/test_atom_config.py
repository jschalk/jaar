from src.gift.atom_config import (
    atom_insert,
    atom_delete,
    atom_update,
    category_ref,
    is_category_ref,
    get_atom_config_dict,
    get_atom_order as q_order,
    set_mog,
    get_flattened_atom_table_build,
    get_normalized_bud_table_build,
    required_args_text,
    optional_args_text,
    normal_table_name_text,
    normal_specs_text,
    sqlite_datatype_text,
    python_type_text,
    nesting_order_str,
    budunit_text,
    bud_acctunit_text,
    bud_acct_membership_text,
    bud_ideaunit_text,
    bud_idea_awardlink_text,
    bud_idea_reasonunit_text,
    bud_idea_reason_premiseunit_text,
    bud_idea_grouphold_text,
    bud_idea_range_push_text,
    bud_idea_healerhold_text,
    bud_idea_factunit_text,
    get_sorted_required_arg_keys,
)


def test_budunit_text_ReturnsObj():
    assert budunit_text() == "budunit"


def test_bud_acctunit_text_ReturnsObj():
    assert bud_acctunit_text() == "bud_acctunit"


def test_bud_acct_membership_text_ReturnsObj():
    assert bud_acct_membership_text() == "bud_acct_membership"


def test_bud_ideaunit_text_ReturnsObj():
    assert bud_ideaunit_text() == "bud_ideaunit"


def test_bud_idea_awardlink_text_ReturnsObj():
    assert bud_idea_awardlink_text() == "bud_idea_awardlink"


def test_bud_idea_reasonunit_text_ReturnsObj():
    assert bud_idea_reasonunit_text() == "bud_idea_reasonunit"


def test_bud_idea_reason_premiseunit_text_ReturnsObj():
    assert bud_idea_reason_premiseunit_text() == "bud_idea_reason_premiseunit"


def test_bud_idea_grouphold_text_ReturnsObj():
    assert bud_idea_grouphold_text() == "bud_idea_grouphold"


def test_bud_idea_grouphold_text_ReturnsObj():
    assert bud_idea_range_push_text() == "bud_idea_range_push"


def test_bud_idea_healerhold_text_ReturnsObj():
    assert bud_idea_healerhold_text() == "bud_idea_healerhold"


def test_bud_idea_factunit_text_ReturnsObj():
    assert bud_idea_factunit_text() == "bud_idea_factunit"


def test_atom_config_HasCorrect_category():
    assert category_ref() == {
        budunit_text(),
        bud_acctunit_text(),
        bud_acct_membership_text(),
        bud_ideaunit_text(),
        bud_idea_awardlink_text(),
        bud_idea_reasonunit_text(),
        bud_idea_reason_premiseunit_text(),
        bud_idea_grouphold_text(),
        bud_idea_range_push_text(),
        bud_idea_healerhold_text(),
        bud_idea_factunit_text(),
    }
    assert bud_acctunit_text() in category_ref()
    assert is_category_ref("idearoot") is False


def check_every_crud_dict_has_element(atom_config_dict, atom_order_text):
    for category, category_dict in atom_config_dict.items():
        if category_dict.get(atom_insert()) is not None:
            category_insert = category_dict.get(atom_insert())
            if category_insert.get(atom_order_text) is None:
                print(
                    f"Missing from {category} {atom_insert()} {category_insert.get(atom_order_text)=}"
                )
                return False

        if category_dict.get(atom_update()) is not None:
            category_update = category_dict.get(atom_update())
            if category_update.get(atom_order_text) is None:
                print(
                    f"Missing from {category} {atom_update()} {category_update.get(atom_order_text)=}"
                )
                return False

        if category_dict.get(atom_delete()) is not None:
            category_delete = category_dict.get(atom_delete())
            if category_delete.get(atom_order_text) is None:
                print(
                    f"Missing from {category} {atom_delete()} {category_delete.get(atom_order_text)=}"
                )
                return False

        treasury_only_text = "treasury_only"
        if category_dict.get(treasury_only_text) is None:
            print(f"{category=} missing {treasury_only_text}")
            return False

        print(f"{category_dict.get(treasury_only_text)=}")
        if category_dict.get(treasury_only_text) not in [True, False]:
            print(
                f"{category=} {treasury_only_text} value '{category_dict.get(treasury_only_text)}' not acceptable"
            )
            return False

        if category_dict.get(treasury_only_text) is None:
            print(f"{category=} missing {treasury_only_text}")
            return False

        calculated_attrs_text = "calculated_attrs"
        if category_dict.get(calculated_attrs_text) is None:
            print(f"{category=} {calculated_attrs_text} is missing")
            return False

        if category_dict.get(normal_specs_text()) is None:
            print(f"{category=} {normal_specs_text()} is missing")
            return False
    return True


def test_get_atom_config_dict_EveryCrudOperationHasChangeOrderGroup():
    # ESTABLISH
    atom_order_text = "atom_order"
    mog = atom_order_text

    # WHEN / THEN
    assert check_every_crud_dict_has_element(get_atom_config_dict(), atom_order_text)
    # # Simple script for editing atom_config.json
    # set_mog(atom_insert(), bud_acctunit_text(), 0)
    # set_mog(atom_insert(), bud_acct_membership_text(), 1)
    # set_mog(atom_insert(), bud_ideaunit_text(), 2)
    # set_mog(atom_insert(), bud_idea_awardlink_text(), 3)
    # set_mog(atom_insert(), bud_idea_grouphold_text(), 4)
    # set_mog(atom_insert(), bud_idea_healerhold_text(), 5)
    # set_mog(atom_insert(), bud_idea_range_push_text(), 6)
    # set_mog(atom_insert(), bud_idea_factunit_text(), 7)
    # set_mog(atom_insert(), bud_idea_reasonunit_text(), 8)
    # set_mog(atom_insert(), bud_idea_reason_premiseunit_text(), 9)
    # set_mog(atom_update(), bud_acctunit_text(), 10)
    # set_mog(atom_update(), bud_acct_membership_text(), 11)
    # set_mog(atom_update(), bud_ideaunit_text(), 12)
    # set_mog(atom_update(), bud_idea_awardlink_text(), 13)
    # set_mog(atom_update(), bud_idea_factunit_text(), 14)
    # set_mog(atom_update(), bud_idea_reason_premiseunit_text(), 15)
    # set_mog(atom_update(), bud_idea_reasonunit_text(), 16)
    # set_mog(atom_delete(), bud_idea_reason_premiseunit_text(), 17)
    # set_mog(atom_delete(), bud_idea_reasonunit_text(), 18)
    # set_mog(atom_delete(), bud_idea_factunit_text(), 19)
    # set_mog(atom_delete(), bud_idea_range_push_text(), 20)
    # set_mog(atom_delete(), bud_idea_grouphold_text(), 21)
    # set_mog(atom_delete(), bud_idea_healerhold_text(), 22)
    # set_mog(atom_delete(), bud_idea_awardlink_text(), 23)
    # set_mog(atom_delete(), bud_ideaunit_text(), 24)
    # set_mog(atom_delete(), bud_acct_membership_text(), 25)
    # set_mog(atom_delete(), bud_acctunit_text(), 26)
    # set_mog(atom_update(), budunit_text(), 27)

    assert 0 == q_order(atom_insert(), bud_acctunit_text())
    assert 1 == q_order(atom_insert(), bud_acct_membership_text())
    assert 2 == q_order(atom_insert(), bud_ideaunit_text())
    assert 3 == q_order(atom_insert(), bud_idea_awardlink_text())
    assert 4 == q_order(atom_insert(), bud_idea_grouphold_text())
    assert 5 == q_order(atom_insert(), bud_idea_healerhold_text())
    assert 6 == q_order(atom_insert(), bud_idea_range_push_text())
    assert 7 == q_order(atom_insert(), bud_idea_factunit_text())
    assert 8 == q_order(atom_insert(), bud_idea_reasonunit_text())
    assert 9 == q_order(atom_insert(), bud_idea_reason_premiseunit_text())
    assert 10 == q_order(atom_update(), bud_acctunit_text())
    assert 11 == q_order(atom_update(), bud_acct_membership_text())
    assert 12 == q_order(atom_update(), bud_ideaunit_text())
    assert 13 == q_order(atom_update(), bud_idea_awardlink_text())
    assert 14 == q_order(atom_update(), bud_idea_factunit_text())
    assert 15 == q_order(atom_update(), bud_idea_reason_premiseunit_text())
    assert 16 == q_order(atom_update(), bud_idea_reasonunit_text())
    assert 17 == q_order(atom_delete(), bud_idea_reason_premiseunit_text())
    assert 18 == q_order(atom_delete(), bud_idea_reasonunit_text())
    assert 19 == q_order(atom_delete(), bud_idea_factunit_text())
    assert 20 == q_order(atom_delete(), bud_idea_range_push_text())
    assert 21 == q_order(atom_delete(), bud_idea_grouphold_text())
    assert 22 == q_order(atom_delete(), bud_idea_healerhold_text())
    assert 23 == q_order(atom_delete(), bud_idea_awardlink_text())
    assert 24 == q_order(atom_delete(), bud_ideaunit_text())
    assert 25 == q_order(atom_delete(), bud_acct_membership_text())
    assert 26 == q_order(atom_delete(), bud_acctunit_text())
    assert 27 == q_order(atom_update(), budunit_text())


def _every_category_dict_has_arg_elements(category_dict: dict) -> bool:
    for required_arg, x_dict in category_dict.get(required_args_text()).items():
        if x_dict.get(python_type_text()) is None:
            print(f"python_type_text failed for {required_arg=}")
            return False
        if x_dict.get(sqlite_datatype_text()) is None:
            print(f"sqlite_datatype_text failed for {required_arg=}")
            return False
    if category_dict.get(optional_args_text()) is not None:
        for optional_arg, x_dict in category_dict.get(optional_args_text()).items():
            if x_dict.get(python_type_text()) is None:
                print(f"python_type_text failed for {optional_arg=}")
                return False
            if x_dict.get(sqlite_datatype_text()) is None:
                print(f"sqlite_datatype_text failed for {optional_arg=}")
                return False


def check_every_arg_dict_has_elements(atom_config_dict):
    for category_key, category_dict in atom_config_dict.items():
        print(f"{category_key=}")
        _every_category_dict_has_arg_elements(category_dict)
    return True


def test_atom_config_AllArgsHave_python_type_sqlite_datatype():
    # ESTABLISH / WHEN / THEN
    assert check_every_arg_dict_has_elements(get_atom_config_dict())


def check_necessary_nesting_order_exists() -> bool:
    atom_config = get_atom_config_dict()
    multi_required_arg_dict = {}
    for atom_key, atom_value in atom_config.items():
        required_args = atom_value.get(required_args_text())
        if len(required_args) > 1:
            multi_required_arg_dict[atom_key] = required_args
    # print(f"{multi_required_arg_dict.keys()=}")
    for atom_key, required_args in multi_required_arg_dict.items():
        for required_arg_key, required_args_dict in required_args.items():
            required_arg_nesting_order = required_args_dict.get(nesting_order_str())
            print(f"{atom_key=} {required_arg_key=} {required_arg_nesting_order=}")
            if required_arg_nesting_order is None:
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


def test_get_sorted_required_arg_keys_ReturnsObj_bud_acctunit():
    # ESTABLISH
    x_category = bud_acctunit_text()

    # WHEN
    x_sorted_required_arg_keys = get_sorted_required_arg_keys(x_category)

    # THEN
    assert x_sorted_required_arg_keys == ["acct_id"]


def test_get_sorted_required_arg_keys_ReturnsObj_bud_idea_reason_premiseunit():
    # ESTABLISH
    x_category = bud_idea_reason_premiseunit_text()

    # WHEN
    x_sorted_required_arg_keys = get_sorted_required_arg_keys(x_category)

    # THEN
    assert x_sorted_required_arg_keys == ["road", "base", "need"]


def test_get_flattened_atom_table_build_ReturnsCorrectObj():
    # ESTABLISH / WHEN
    atom_columns = get_flattened_atom_table_build()

    # THEN
    assert len(atom_columns) == 111
    assert atom_columns.get("budunit_UPDATE__credor_respect") == "INTEGER"
    # print(f"{atom_columns.keys()=}")


def test_get_normalized_bud_table_build_ReturnsCorrectObj():
    # ESTABLISH / WHEN
    normalized_bud_table_build = get_normalized_bud_table_build()
    nx = normalized_bud_table_build

    # THEN
    assert len(nx) == 11
    cat_budunit = nx.get(budunit_text())
    cat_acctunit = nx.get(bud_acctunit_text())
    cat_membership = nx.get(bud_acct_membership_text())
    cat_idea = nx.get(bud_ideaunit_text())
    cat_awardlink = nx.get(bud_idea_awardlink_text())
    cat_reason = nx.get(bud_idea_reasonunit_text())
    cat_premise = nx.get(bud_idea_reason_premiseunit_text())
    cat_grouphold = nx.get(bud_idea_grouphold_text())
    cat_healerhold = nx.get(bud_idea_healerhold_text())
    cat_fact = nx.get(bud_idea_factunit_text())
    cat_range_push = nx.get(bud_idea_range_push_text())

    assert cat_budunit is not None
    assert cat_acctunit is not None
    assert cat_membership is not None
    assert cat_idea is not None
    assert cat_awardlink is not None
    assert cat_reason is not None
    assert cat_premise is not None
    assert cat_grouphold is not None
    assert cat_healerhold is not None
    assert cat_fact is not None
    assert cat_range_push is not None

    normal_specs_budunit = cat_budunit.get(normal_specs_text())
    normal_specs_acctunit = cat_acctunit.get(normal_specs_text())
    normal_specs_membership = cat_membership.get(normal_specs_text())
    normal_specs_idea = cat_idea.get(normal_specs_text())
    normal_specs_awardlink = cat_awardlink.get(normal_specs_text())
    normal_specs_reason = cat_reason.get(normal_specs_text())
    normal_specs_premise = cat_premise.get(normal_specs_text())
    normal_specs_grouphold = cat_grouphold.get(normal_specs_text())
    normal_specs_healerhold = cat_healerhold.get(normal_specs_text())
    normal_specs_fact = cat_fact.get(normal_specs_text())
    normal_specs_range_push = cat_range_push.get(normal_specs_text())

    columns_text = "columns"
    print(f"{cat_budunit.keys()=}")
    print(f"{normal_specs_text()=}")
    assert normal_specs_budunit is not None
    assert normal_specs_acctunit is not None
    assert normal_specs_membership is not None
    assert normal_specs_idea is not None
    assert normal_specs_awardlink is not None
    assert normal_specs_reason is not None
    assert normal_specs_premise is not None
    assert normal_specs_grouphold is not None
    assert normal_specs_healerhold is not None
    assert normal_specs_fact is not None
    assert normal_specs_range_push is not None

    table_name_budunit = normal_specs_budunit.get(normal_table_name_text())
    table_name_acctunit = normal_specs_acctunit.get(normal_table_name_text())
    table_name_membership = normal_specs_membership.get(normal_table_name_text())
    table_name_idea = normal_specs_idea.get(normal_table_name_text())
    table_name_awardlink = normal_specs_awardlink.get(normal_table_name_text())
    table_name_reason = normal_specs_reason.get(normal_table_name_text())
    table_name_premise = normal_specs_premise.get(normal_table_name_text())
    table_name_grouphold = normal_specs_grouphold.get(normal_table_name_text())
    table_name_healerhold = normal_specs_healerhold.get(normal_table_name_text())
    table_name_fact = normal_specs_fact.get(normal_table_name_text())
    table_name_range_push = normal_specs_range_push.get(normal_table_name_text())

    assert table_name_budunit == "bud"
    assert table_name_acctunit == "acctunit"
    assert table_name_membership == "membership"
    assert table_name_idea == "idea"
    assert table_name_awardlink == "awardlink"
    assert table_name_reason == "reason"
    assert table_name_premise == "premise"
    assert table_name_grouphold == "grouphold"
    assert table_name_healerhold == "healerhold"
    assert table_name_fact == "fact"
    assert table_name_range_push == "range_push"

    assert len(cat_budunit) == 2
    assert cat_budunit.get(columns_text) is not None

    budunit_columns = cat_budunit.get(columns_text)
    assert len(budunit_columns) == 10
    assert budunit_columns.get("uid") is not None
    assert budunit_columns.get("_max_tree_traverse") is not None
    assert budunit_columns.get("_monetary_desc") is not None
    assert budunit_columns.get("_credor_respect") is not None
    assert budunit_columns.get("_debtor_respect") is not None
    assert budunit_columns.get("_fund_pool") is not None
    assert budunit_columns.get("_fund_coin") is not None
    assert budunit_columns.get("_bit") is not None
    assert budunit_columns.get("_penny") is not None
    assert budunit_columns.get("_tally") is not None

    assert len(cat_acctunit) == 2
    acctunit_columns = cat_acctunit.get(columns_text)
    assert len(acctunit_columns) == 4
    assert acctunit_columns.get("uid") is not None
    assert acctunit_columns.get("acct_id") is not None
    assert acctunit_columns.get("credit_score") is not None
    assert acctunit_columns.get("debtit_score") is not None

    acct_id_dict = acctunit_columns.get("acct_id")
    assert len(acct_id_dict) == 2
    assert acct_id_dict.get(sqlite_datatype_text()) == "TEXT"
    assert acct_id_dict.get("nullable") is False
    debtit_score_dict = acctunit_columns.get("debtit_score")
    assert len(acct_id_dict) == 2
    assert debtit_score_dict.get(sqlite_datatype_text()) == "INTEGER"
    assert debtit_score_dict.get("nullable") == True
