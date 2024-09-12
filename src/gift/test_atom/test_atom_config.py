from src._instrument.python_tool import get_nested_value
from src.bud.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_awardlink_str,
    bud_idea_reasonunit_str,
    bud_idea_reason_premiseunit_str,
    bud_idea_teamlink_str,
    bud_idea_healerlink_str,
    bud_idea_factunit_str,
)
from src.gift.atom_config import (
    atom_insert,
    atom_delete,
    atom_update,
    category_ref,
    is_category_ref,
    get_atom_config_dict,
    get_atom_args_category_mapping,
    get_allowed_python_types,
    get_atom_args_python_types,
    get_atom_order as q_order,
    set_mog,
    get_flattened_atom_table_build,
    get_normalized_bud_table_build,
    required_args_str,
    optional_args_str,
    category_str,
    crud_str_str,
    normal_table_name_str,
    normal_specs_str,
    sqlite_datatype_str,
    python_type_str,
    nesting_order_str,
    column_order_str,
    get_sorted_required_arg_keys,
    parent_road_str,
    road_str,
    acct_id_str,
    group_id_str,
    begin_str,
    close_str,
    addin_str,
    numor_str,
    denom_str,
    morph_str,
    gogo_want_str,
    stop_want_str,
    base_str,
)
from copy import deepcopy as copy_deepcopy


def test_required_args_str_ReturnsObj():
    assert required_args_str() == "required_args"


def test_optional_args_str_ReturnsObj():
    assert optional_args_str() == "optional_args"


def test_column_order_str_ReturnsObj():
    assert column_order_str() == "column_order"


def test_category_str_ReturnsObj():
    assert category_str() == "category"


def test_atom_insert_ReturnsObj():
    assert atom_insert() == "INSERT"


def test_atom_update_ReturnsObj():
    assert atom_update() == "UPDATE"


def test_atom_delete_ReturnsObj():
    assert atom_delete() == "DELETE"


def test_crud_str_str_ReturnsObj():
    assert crud_str_str() == "crud_str"


def test_atom_config_HasCorrect_category():
    assert category_ref() == {
        budunit_str(),
        bud_acctunit_str(),
        bud_acct_membership_str(),
        bud_ideaunit_str(),
        bud_idea_awardlink_str(),
        bud_idea_reasonunit_str(),
        bud_idea_reason_premiseunit_str(),
        bud_idea_teamlink_str(),
        bud_idea_healerlink_str(),
        bud_idea_factunit_str(),
    }
    assert bud_acctunit_str() in category_ref()
    assert is_category_ref("idearoot") is False


def test_begin_str_ReturnsObj():
    assert begin_str() == "begin"


def test_close_str_ReturnsObj():
    assert close_str() == "close"


def test_addin_str_ReturnsObj():
    assert addin_str() == "addin"


def test_numor_str_ReturnsObj():
    assert numor_str() == "numor"


def test_denom_str_ReturnsObj():
    assert denom_str() == "denom"


def test_morph_str_ReturnsObj():
    assert morph_str() == "morph"


def test_gogo_want_str_ReturnsObj():
    assert gogo_want_str() == "gogo_want"


def test_stop_want_str_ReturnsObj():
    assert stop_want_str() == "stop_want"


def check_every_crud_dict_has_element(atom_config_dict, atom_order_str):
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


def test_get_atom_config_dict_EveryCrudOperationHasChangeOrderGroup():
    # ESTABLISH
    atom_order_str = "atom_order"
    mog = atom_order_str

    # WHEN / THEN
    assert check_every_crud_dict_has_element(get_atom_config_dict(), atom_order_str)
    # # Simple script for editing atom_config.json
    # set_mog(atom_insert(), bud_acctunit_str(), 0)
    # set_mog(atom_insert(), bud_acct_membership_str(), 1)
    # set_mog(atom_insert(), bud_ideaunit_str(), 2)
    # set_mog(atom_insert(), bud_idea_awardlink_str(), 3)
    # set_mog(atom_insert(), bud_idea_teamlink_str(), 4)
    # set_mog(atom_insert(), bud_idea_healerlink_str(), 5)
    # set_mog(atom_insert(), bud_idea_factunit_str(), 6)
    # set_mog(atom_insert(), bud_idea_reasonunit_str(), 7)
    # set_mog(atom_insert(), bud_idea_reason_premiseunit_str(), 8)
    # set_mog(atom_update(), bud_acctunit_str(), 9)
    # set_mog(atom_update(), bud_acct_membership_str(), 10)
    # set_mog(atom_update(), bud_ideaunit_str(), 11)
    # set_mog(atom_update(), bud_idea_awardlink_str(), 12)
    # set_mog(atom_update(), bud_idea_factunit_str(), 13)
    # set_mog(atom_update(), bud_idea_reason_premiseunit_str(), 14)
    # set_mog(atom_update(), bud_idea_reasonunit_str(), 15)
    # set_mog(atom_delete(), bud_idea_reason_premiseunit_str(), 16)
    # set_mog(atom_delete(), bud_idea_reasonunit_str(), 17)
    # set_mog(atom_delete(), bud_idea_factunit_str(), 18)
    # set_mog(atom_delete(), bud_idea_teamlink_str(), 19)
    # set_mog(atom_delete(), bud_idea_healerlink_str(), 20)
    # set_mog(atom_delete(), bud_idea_awardlink_str(), 21)
    # set_mog(atom_delete(), bud_ideaunit_str(), 22)
    # set_mog(atom_delete(), bud_acct_membership_str(), 23)
    # set_mog(atom_delete(), bud_acctunit_str(), 24)
    # set_mog(atom_update(), budunit_str(), 25)

    assert 0 == q_order(atom_insert(), bud_acctunit_str())
    assert 1 == q_order(atom_insert(), bud_acct_membership_str())
    assert 2 == q_order(atom_insert(), bud_ideaunit_str())
    assert 3 == q_order(atom_insert(), bud_idea_awardlink_str())
    assert 4 == q_order(atom_insert(), bud_idea_teamlink_str())
    assert 5 == q_order(atom_insert(), bud_idea_healerlink_str())
    assert 6 == q_order(atom_insert(), bud_idea_factunit_str())
    assert 7 == q_order(atom_insert(), bud_idea_reasonunit_str())
    assert 8 == q_order(atom_insert(), bud_idea_reason_premiseunit_str())
    assert 9 == q_order(atom_update(), bud_acctunit_str())
    assert 10 == q_order(atom_update(), bud_acct_membership_str())
    assert 11 == q_order(atom_update(), bud_ideaunit_str())
    assert 12 == q_order(atom_update(), bud_idea_awardlink_str())
    assert 13 == q_order(atom_update(), bud_idea_factunit_str())
    assert 14 == q_order(atom_update(), bud_idea_reason_premiseunit_str())
    assert 15 == q_order(atom_update(), bud_idea_reasonunit_str())
    assert 16 == q_order(atom_delete(), bud_idea_reason_premiseunit_str())
    assert 17 == q_order(atom_delete(), bud_idea_reasonunit_str())
    assert 18 == q_order(atom_delete(), bud_idea_factunit_str())
    assert 19 == q_order(atom_delete(), bud_idea_teamlink_str())
    assert 20 == q_order(atom_delete(), bud_idea_healerlink_str())
    assert 21 == q_order(atom_delete(), bud_idea_awardlink_str())
    assert 22 == q_order(atom_delete(), bud_ideaunit_str())
    assert 23 == q_order(atom_delete(), bud_acct_membership_str())
    assert 24 == q_order(atom_delete(), bud_acctunit_str())
    assert 25 == q_order(atom_update(), budunit_str())


def _get_atom_config_required_args_len(x_cat: str) -> int:
    required_args_key_list = [x_cat, required_args_str()]
    return len(get_nested_value(get_atom_config_dict(), required_args_key_list))


def _get_atom_config_optional_args_len(x_cat: str) -> int:
    optional_args_key_list = [x_cat, optional_args_str()]
    return len(get_nested_value(get_atom_config_dict(), optional_args_key_list))


def test_get_atom_config_dict_CheckEachCategoryHasCorrectArgCount():
    # ESTABLISH
    assert _get_atom_config_required_args_len(budunit_str()) == 0
    assert _get_atom_config_required_args_len(bud_acctunit_str()) == 1
    assert _get_atom_config_required_args_len(bud_acct_membership_str()) == 2
    assert _get_atom_config_required_args_len(bud_ideaunit_str()) == 2
    assert _get_atom_config_required_args_len(bud_idea_awardlink_str()) == 2
    assert _get_atom_config_required_args_len(bud_idea_reasonunit_str()) == 2
    assert _get_atom_config_required_args_len(bud_idea_reason_premiseunit_str()) == 3
    assert _get_atom_config_required_args_len(bud_idea_teamlink_str()) == 2
    assert _get_atom_config_required_args_len(bud_idea_healerlink_str()) == 2
    assert _get_atom_config_required_args_len(bud_idea_factunit_str()) == 2

    assert _get_atom_config_optional_args_len(budunit_str()) == 9
    assert _get_atom_config_optional_args_len(bud_acctunit_str()) == 2
    assert _get_atom_config_optional_args_len(bud_acct_membership_str()) == 2
    assert _get_atom_config_optional_args_len(bud_ideaunit_str()) == 11
    assert _get_atom_config_optional_args_len(bud_idea_awardlink_str()) == 2
    assert _get_atom_config_optional_args_len(bud_idea_reasonunit_str()) == 1
    assert _get_atom_config_optional_args_len(bud_idea_reason_premiseunit_str()) == 3
    assert _get_atom_config_optional_args_len(bud_idea_teamlink_str()) == 0
    assert _get_atom_config_optional_args_len(bud_idea_healerlink_str()) == 0
    assert _get_atom_config_optional_args_len(bud_idea_factunit_str()) == 3


def _has_every_element(x_arg, x_dict) -> bool:
    arg_elements = {python_type_str(), sqlite_datatype_str(), column_order_str()}
    for arg_element in arg_elements:
        if x_dict.get(arg_element) is None:
            print(f"{arg_element} failed for {x_arg=}")
            return False
    return True


def _every_category_dict_has_arg_elements(category_dict: dict) -> bool:
    for required_arg, x_dict in category_dict.get(required_args_str()).items():
        if not _has_every_element(required_arg, x_dict):
            return False
    if category_dict.get(optional_args_str()) is not None:
        for optional_arg, x_dict in category_dict.get(optional_args_str()).items():
            if not _has_every_element(optional_arg, x_dict):
                return False
    return True


def check_every_arg_dict_has_elements(atom_config_dict):
    for category_key, category_dict in atom_config_dict.items():
        print(f"{category_key=}")
        assert _every_category_dict_has_arg_elements(category_dict)
    return True


def test_atom_config_AllArgsHave_python_type_sqlite_datatype():
    # ESTABLISH / WHEN / THEN
    assert check_every_arg_dict_has_elements(get_atom_config_dict())


def check_necessary_nesting_order_exists() -> bool:
    atom_config = get_atom_config_dict()
    multi_required_arg_dict = {}
    for atom_key, atom_value in atom_config.items():
        required_args = atom_value.get(required_args_str())
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


def _get_atom_config_optional_arg_keys(x_cat: str) -> set[str]:
    optional_args_key_list = [x_cat, optional_args_str()]
    return set(get_nested_value(get_atom_config_dict(), optional_args_key_list).keys())


def _get_atom_config_required_arg_keys(x_cat: str) -> set[str]:
    required_args_key_list = [x_cat, required_args_str()]
    return set(get_nested_value(get_atom_config_dict(), required_args_key_list).keys())


def unique_optional_args():
    optional_arg_keys = set()
    optional_arg_key_count = 0
    for atom_category in get_atom_config_dict().keys():
        new_optional_arg_keys = _get_atom_config_optional_arg_keys(atom_category)
        optional_arg_key_count += len(new_optional_arg_keys)
        optional_arg_keys.update(new_optional_arg_keys)
        # print(f"{atom_category} {_get_atom_config_optional_arg_keys(atom_category)}")
    return optional_arg_keys, optional_arg_key_count


def test_get_atom_config_dict_CheckEveryOptionalArgHasUniqueKey():
    # ESTABLISH / WHEN
    optional_arg_keys, optional_arg_key_count = unique_optional_args()

    # THEN
    print(f"{optional_arg_key_count=} {len(optional_arg_keys)=}")
    assert optional_arg_key_count == len(optional_arg_keys)


def unique_required_args():
    required_arg_keys = set()
    required_arg_key_count = 0
    for atom_category in get_atom_config_dict().keys():
        new_required_arg_keys = _get_atom_config_required_arg_keys(atom_category)
        if road_str() in new_required_arg_keys:
            new_required_arg_keys.remove(road_str())
        if base_str() in new_required_arg_keys:
            new_required_arg_keys.remove(base_str())
        if acct_id_str() in new_required_arg_keys:
            new_required_arg_keys.remove(acct_id_str())
        if group_id_str() in new_required_arg_keys:
            new_required_arg_keys.remove(group_id_str())
        print(f"{atom_category} {new_required_arg_keys=}")
        required_arg_key_count += len(new_required_arg_keys)
        required_arg_keys.update(new_required_arg_keys)
    return required_arg_keys, required_arg_key_count


def test_get_atom_config_dict_SomeRequiredArgAreUnique():
    # ESTABLISH / WHEN
    required_arg_keys, required_arg_key_count = unique_required_args()

    # THEN
    print(f"{required_arg_key_count=} {len(required_arg_keys)=}")
    assert required_arg_key_count == len(required_arg_keys)


def test_get_sorted_required_arg_keys_ReturnsObj_bud_acctunit():
    # ESTABLISH
    x_category = bud_acctunit_str()

    # WHEN
    x_sorted_required_arg_keys = get_sorted_required_arg_keys(x_category)

    # THEN
    assert x_sorted_required_arg_keys == [acct_id_str()]


def test_get_sorted_required_arg_keys_ReturnsObj_bud_idea_reason_premiseunit():
    # ESTABLISH
    x_category = bud_idea_reason_premiseunit_str()

    # WHEN
    x_sorted_required_arg_keys = get_sorted_required_arg_keys(x_category)

    # THEN
    assert x_sorted_required_arg_keys == [road_str(), base_str(), "need"]


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
    cat_idea = nx.get(bud_ideaunit_str())
    cat_awardlink = nx.get(bud_idea_awardlink_str())
    cat_reason = nx.get(bud_idea_reasonunit_str())
    cat_premise = nx.get(bud_idea_reason_premiseunit_str())
    cat_teamlink = nx.get(bud_idea_teamlink_str())
    cat_healerlink = nx.get(bud_idea_healerlink_str())
    cat_fact = nx.get(bud_idea_factunit_str())

    assert cat_budunit is not None
    assert cat_acctunit is not None
    assert cat_membership is not None
    assert cat_idea is not None
    assert cat_awardlink is not None
    assert cat_reason is not None
    assert cat_premise is not None
    assert cat_teamlink is not None
    assert cat_healerlink is not None
    assert cat_fact is not None

    normal_specs_budunit = cat_budunit.get(normal_specs_str())
    normal_specs_acctunit = cat_acctunit.get(normal_specs_str())
    normal_specs_membership = cat_membership.get(normal_specs_str())
    normal_specs_idea = cat_idea.get(normal_specs_str())
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
    assert normal_specs_idea is not None
    assert normal_specs_awardlink is not None
    assert normal_specs_reason is not None
    assert normal_specs_premise is not None
    assert normal_specs_teamlink is not None
    assert normal_specs_healerlink is not None
    assert normal_specs_fact is not None

    table_name_budunit = normal_specs_budunit.get(normal_table_name_str())
    table_name_acctunit = normal_specs_acctunit.get(normal_table_name_str())
    table_name_membership = normal_specs_membership.get(normal_table_name_str())
    table_name_idea = normal_specs_idea.get(normal_table_name_str())
    table_name_awardlink = normal_specs_awardlink.get(normal_table_name_str())
    table_name_reason = normal_specs_reason.get(normal_table_name_str())
    table_name_premise = normal_specs_premise.get(normal_table_name_str())
    table_name_teamlink = normal_specs_teamlink.get(normal_table_name_str())
    table_name_healerlink = normal_specs_healerlink.get(normal_table_name_str())
    table_name_fact = normal_specs_fact.get(normal_table_name_str())

    assert table_name_budunit == "bud"
    assert table_name_acctunit == "acctunit"
    assert table_name_membership == "membership"
    assert table_name_idea == "idea"
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
    assert budunit_columns.get("monetary_desc") is not None
    assert budunit_columns.get("credor_respect") is not None
    assert budunit_columns.get("debtor_respect") is not None
    assert budunit_columns.get("fund_pool") is not None
    assert budunit_columns.get("fund_coin") is not None
    assert budunit_columns.get("bit") is not None
    assert budunit_columns.get("penny") is not None
    assert budunit_columns.get("tally") is not None

    assert len(cat_acctunit) == 2
    acctunit_columns = cat_acctunit.get(columns_str)
    assert len(acctunit_columns) == 4
    assert acctunit_columns.get("uid") is not None
    assert acctunit_columns.get(acct_id_str()) is not None
    assert acctunit_columns.get("credit_belief") is not None
    assert acctunit_columns.get("debtit_belief") is not None

    acct_id_dict = acctunit_columns.get(acct_id_str())
    assert len(acct_id_dict) == 2
    assert acct_id_dict.get(sqlite_datatype_str()) == "TEXT"
    assert acct_id_dict.get("nullable") is False
    debtit_belief_dict = acctunit_columns.get("debtit_belief")
    assert len(acct_id_dict) == 2
    assert debtit_belief_dict.get(sqlite_datatype_str()) == "INTEGER"
    assert debtit_belief_dict.get("nullable") is True

    assert len(cat_idea) == 2
    idea_columns = cat_idea.get(columns_str)
    assert len(idea_columns) == 14
    assert idea_columns.get("uid") is not None
    assert idea_columns.get(parent_road_str()) is not None
    assert idea_columns.get(begin_str()) is not None
    assert idea_columns.get(close_str()) is not None

    gogo_want_dict = idea_columns.get(gogo_want_str())
    stop_want_dict = idea_columns.get(stop_want_str())
    assert len(gogo_want_dict) == 2
    assert len(stop_want_dict) == 2
    assert gogo_want_dict.get(sqlite_datatype_str()) == "PECUN"
    assert stop_want_dict.get(sqlite_datatype_str()) == "PECUN"
    assert gogo_want_dict.get("nullable") is True
    assert stop_want_dict.get("nullable") is True


def test_get_atom_args_category_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_atom_args_category_mapping = get_atom_args_category_mapping()

    # THEN
    assert x_atom_args_category_mapping
    assert x_atom_args_category_mapping.get(stop_want_str())
    assert x_atom_args_category_mapping.get(stop_want_str()) == {bud_ideaunit_str()}
    assert x_atom_args_category_mapping.get(parent_road_str())
    road_categorys = x_atom_args_category_mapping.get(road_str())
    assert bud_idea_factunit_str() in road_categorys
    assert bud_idea_teamlink_str() in road_categorys
    assert len(road_categorys) == 6
    assert len(x_atom_args_category_mapping) == 41


def get_python_type(x_category: str, x_arg: str) -> str:
    atom_config_dict = get_atom_config_dict()
    category_dict = atom_config_dict.get(x_category)
    optional_dict = category_dict.get(optional_args_str())
    required_dict = category_dict.get(required_args_str())
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = category_dict.get(optional_args_str()).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(python_type_str())


def test_get_python_type_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_python_type(bud_acctunit_str(), acct_id_str()) == "AcctID"
    assert get_python_type(bud_ideaunit_str(), gogo_want_str()) == "float"


def test_get_allowed_python_types_ReturnsObj():
    # ESTABLISH
    x_allowed_python_types = {
        "RoadUnit",
        "int",
        "AcctID",
        "GroupID",
        "float",
        "bool",
        "RoadNode",
        "str",
    }

    # WHEN / THEN
    assert get_allowed_python_types() == x_allowed_python_types


def test_get_atom_config_dict_ValidatePythonTypes():
    # make sure all atom config python types are valid and repeated args are the same
    # ESTABLISH WHEN / THEN
    assert all_atom_config_python_types_are_valid(get_allowed_python_types())


def all_atom_config_python_types_are_valid(allowed_python_types):
    x_atom_args_category_mapping = get_atom_args_category_mapping()
    for x_atom_arg, categorys in x_atom_args_category_mapping.items():
        old_python_type = None
        x_python_type = ""
        for x_category in categorys:
            x_python_type = get_python_type(x_category, x_atom_arg)
            # print(f"{x_python_type=} {x_atom_arg=} {x_category=}")
            if x_python_type not in allowed_python_types:
                return False

            if old_python_type is None:
                old_python_type = x_python_type
            # confirm each atom_arg has same data type in all categorys
            print(f"{x_python_type=} {old_python_type=} {x_atom_arg=} {x_category=}")
            if x_python_type != old_python_type:
                return False
            old_python_type = x_python_type
    return True


def all_atom_args_python_types_are_correct(x_python_types) -> bool:
    x_atom_args_category_mapping = get_atom_args_category_mapping()
    x_sorted_python_types = sorted(list(x_python_types.keys()))
    for x_atom_arg in x_sorted_python_types:
        x_categorys = list(x_atom_args_category_mapping.get(x_atom_arg))
        x_category = x_categorys[0]
        x_python_type = get_python_type(x_category, x_atom_arg)
        print(f"assert x_python_types.get({x_atom_arg} == {x_python_type}")
        if x_python_types.get(x_atom_arg) != x_python_type:
            return False
    return True


def test_get_atom_args_python_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_python_types = get_atom_args_python_types()

    # THEN
    assert all_atom_args_python_types_are_correct(x_python_types)
    assert x_python_types.keys() == get_atom_args_category_mapping().keys()
    assert x_python_types.get("acct_id") == "AcctID"
    assert x_python_types.get("addin") == "float"
    assert x_python_types.get("base") == "RoadUnit"
    assert x_python_types.get("base_idea_active_requisite") == "bool"
    assert x_python_types.get("begin") == "float"
    assert x_python_types.get("bit") == "float"
    assert x_python_types.get("close") == "float"
    assert x_python_types.get("credit_belief") == "int"
    assert x_python_types.get("credit_vote") == "int"
    assert x_python_types.get("credor_respect") == "int"
    assert x_python_types.get("debtit_belief") == "int"
    assert x_python_types.get("debtit_vote") == "int"
    assert x_python_types.get("debtor_respect") == "int"
    assert x_python_types.get("denom") == "int"
    assert x_python_types.get("divisor") == "int"
    assert x_python_types.get("fnigh") == "float"
    assert x_python_types.get("fopen") == "float"
    assert x_python_types.get("fund_coin") == "float"
    assert x_python_types.get("fund_pool") == "float"
    assert x_python_types.get("give_force") == "float"
    assert x_python_types.get("gogo_want") == "float"
    assert x_python_types.get("group_id") == "GroupID"
    assert x_python_types.get("healer_id") == "GroupID"
    assert x_python_types.get("label") == "RoadNode"
    assert x_python_types.get("mass") == "int"
    assert x_python_types.get("max_tree_traverse") == "int"
    assert x_python_types.get("monetary_desc") == "str"
    assert x_python_types.get("morph") == "bool"
    assert x_python_types.get("need") == "RoadUnit"
    assert x_python_types.get("nigh") == "float"
    assert x_python_types.get("numor") == "int"
    assert x_python_types.get("open") == "float"
    assert x_python_types.get("parent_road") == "RoadUnit"
    assert x_python_types.get("penny") == "float"
    assert x_python_types.get("pick") == "RoadUnit"
    assert x_python_types.get("pledge") == "bool"
    assert x_python_types.get("problem_bool") == "bool"
    assert x_python_types.get("road") == "RoadUnit"
    assert x_python_types.get("stop_want") == "float"
    assert x_python_types.get("take_force") == "float"
    assert x_python_types.get("tally") == "int"
