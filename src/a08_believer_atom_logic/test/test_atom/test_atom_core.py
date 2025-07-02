from src.a03_group_logic.acct import acctunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_debt_points_str,
    acct_name_str,
    believer_acct_membership_str,
    believer_acctunit_str,
    believerunit_str,
    group_title_str,
)
from src.a08_believer_atom_logic.atom import BelieverAtom, believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import DELETE_str, INSERT_str


def test_BelieverAtom_exists():
    # ESTABLISH / WHEN
    x_believeratom = BelieverAtom()

    # THEN
    assert x_believeratom.dimen is None
    assert x_believeratom.crud_str is None
    assert x_believeratom.jkeys is None
    assert x_believeratom.jvalues is None
    assert x_believeratom.atom_order is None


def test_believeratom_shop_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_acct_cred_points = 55
    bob_acct_debt_points = 66
    bob_acctunit = acctunit_shop(bob_str, bob_acct_cred_points, bob_acct_debt_points)
    cw_str = "_acct_cred_points"
    dw_str = "_acct_debt_points"
    bob_required_dict = {acct_name_str(): "huh"}
    bob_optional_dict = {cw_str: bob_acctunit.get_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_acctunit.get_dict().get(dw_str)
    acctunit_str = believer_acctunit_str()

    # WHEN
    x_believeratom = believeratom_shop(
        dimen=acctunit_str,
        crud_str=INSERT_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    print(f"{x_believeratom=}")
    assert x_believeratom.dimen == acctunit_str
    assert x_believeratom.crud_str == INSERT_str()
    assert x_believeratom.jkeys == bob_required_dict
    assert x_believeratom.jvalues == bob_optional_dict


def test_BelieverAtom_set_jkey_CorrectlySetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    acctunit_str = believer_acctunit_str()
    acctunit_believeratom = believeratom_shop(acctunit_str, INSERT_str())
    assert acctunit_believeratom.jkeys == {}

    # WHEN
    acctunit_believeratom.set_jkey(x_key=acct_name_str(), x_value=bob_str)

    # THEN
    assert acctunit_believeratom.jkeys == {acct_name_str(): bob_str}


def test_BelieverAtom_set_jvalue_CorrectlySetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    acctunit_str = believer_acctunit_str()
    acctunit_believeratom = believeratom_shop(acctunit_str, INSERT_str())
    assert acctunit_believeratom.jvalues == {}

    # WHEN
    acctunit_believeratom.set_jvalue(x_key=acct_name_str(), x_value=bob_str)

    # THEN
    assert acctunit_believeratom.jvalues == {acct_name_str(): bob_str}


def test_BelieverAtom_get_value_ReturnsObj_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    acctunit_str = believer_acctunit_str()
    acctunit_believeratom = believeratom_shop(acctunit_str, INSERT_str())
    acctunit_believeratom.set_jkey(x_key=acct_name_str(), x_value=bob_str)

    # WHEN / THEN
    assert acctunit_believeratom.get_value(acct_name_str()) == bob_str


def test_BelieverAtom_is_jvalues_valid_ReturnsCorrectBoolean():
    # WHEN
    acctunit_str = believer_acctunit_str()
    bob_insert_believeratom = believeratom_shop(acctunit_str, crud_str=INSERT_str())
    assert bob_insert_believeratom.is_jvalues_valid()

    # WHEN
    bob_insert_believeratom.set_jvalue(acct_cred_points_str(), 55)
    # THEN
    assert len(bob_insert_believeratom.jvalues) == 1
    assert bob_insert_believeratom.is_jvalues_valid()

    # WHEN
    bob_insert_believeratom.set_jvalue(acct_debt_points_str(), 66)
    # THEN
    assert len(bob_insert_believeratom.jvalues) == 2
    assert bob_insert_believeratom.is_jvalues_valid()

    # WHEN
    bob_insert_believeratom.set_jvalue("x_x_x", 77)
    # THEN
    assert len(bob_insert_believeratom.jvalues) == 3
    assert bob_insert_believeratom.is_jvalues_valid() is False


def test_BelieverAtom_is_valid_ReturnsCorrectBoolean_AcctUnit_INSERT():
    bob_str = "Bob"
    bob_acct_cred_points = 55
    bob_acct_debt_points = 66
    bob_acctunit = acctunit_shop(bob_str, bob_acct_cred_points, bob_acct_debt_points)
    acctunit_str = believer_acctunit_str()

    # WHEN
    bob_insert_believeratom = believeratom_shop(acctunit_str, crud_str=INSERT_str())

    # THEN
    assert bob_insert_believeratom.is_jkeys_valid() is False
    assert bob_insert_believeratom.is_jvalues_valid()
    assert bob_insert_believeratom.is_valid() is False

    # WHEN
    bob_insert_believeratom.set_jvalue("x_x_x", 12)

    # THEN
    assert bob_insert_believeratom.is_jkeys_valid() is False
    assert bob_insert_believeratom.is_jvalues_valid() is False
    assert bob_insert_believeratom.is_valid() is False

    # WHEN
    bob_insert_believeratom.set_jkey(acct_name_str(), bob_str)

    # THEN
    assert bob_insert_believeratom.is_jkeys_valid()
    assert bob_insert_believeratom.is_jvalues_valid() is False
    assert bob_insert_believeratom.is_valid() is False

    # WHEN
    bob_insert_believeratom.jvalues = {}
    cw_str = acct_cred_points_str()
    dw_str = acct_debt_points_str()
    bob_insert_believeratom.set_jvalue(cw_str, bob_acctunit.get_dict().get(cw_str))
    bob_insert_believeratom.set_jvalue(dw_str, bob_acctunit.get_dict().get(dw_str))

    # THEN
    assert bob_insert_believeratom.is_jkeys_valid()
    assert bob_insert_believeratom.is_jvalues_valid()
    assert bob_insert_believeratom.is_valid()

    # WHEN
    bob_insert_believeratom.crud_str = None

    # THEN
    assert bob_insert_believeratom.is_jkeys_valid() is False
    assert bob_insert_believeratom.is_valid() is False

    # WHEN
    bob_insert_believeratom.crud_str = INSERT_str()

    # THEN
    assert bob_insert_believeratom.is_jkeys_valid()
    assert bob_insert_believeratom.is_valid()


def test_BelieverAtom_get_value_ReturnsObj_Scenario1():
    # ESTABLISH
    bob_str = "Bob"
    bob_acct_cred_points = 55
    bob_acct_debt_points = 66
    bob_acctunit = acctunit_shop(bob_str, bob_acct_cred_points, bob_acct_debt_points)
    acctunit_str = believer_acctunit_str()
    bob_insert_believeratom = believeratom_shop(acctunit_str, INSERT_str())
    cw_str = acct_cred_points_str()
    dw_str = acct_debt_points_str()
    print(f"{bob_acctunit.get_dict()=}")
    # bob_acctunit_dict = {acct_name_str(): bob_acctunit.get_dict().get(acct_name_str())}
    # print(f"{bob_acctunit_dict=}")
    bob_insert_believeratom.set_jkey(acct_name_str(), bob_str)
    bob_insert_believeratom.set_jvalue(cw_str, bob_acctunit.get_dict().get(cw_str))
    bob_insert_believeratom.set_jvalue(dw_str, bob_acctunit.get_dict().get(dw_str))
    assert bob_insert_believeratom.is_valid()

    # WHEN / THEN
    assert bob_insert_believeratom.get_value(cw_str) == bob_acct_cred_points
    assert bob_insert_believeratom.get_value(dw_str) == bob_acct_debt_points


def test_BelieverAtom_is_valid_ReturnsCorrectBoolean_AcctUnit_DELETE():
    bob_str = "Bob"
    acctunit_str = believer_acctunit_str()
    delete_str = DELETE_str()

    # WHEN
    bob_delete_believeratom = believeratom_shop(acctunit_str, crud_str=delete_str)

    # THEN
    assert bob_delete_believeratom.is_jkeys_valid() is False
    assert bob_delete_believeratom.is_valid() is False

    # WHEN
    bob_delete_believeratom.set_jkey(acct_name_str(), bob_str)

    # THEN
    assert bob_delete_believeratom.is_jkeys_valid()
    assert bob_delete_believeratom.is_valid()


def test_BelieverAtom_is_valid_ReturnsCorrectBoolean_believerunit():
    # ESTABLISH / WHEN
    bob_update_believeratom = believeratom_shop(believerunit_str(), INSERT_str())

    # THEN
    assert bob_update_believeratom.is_jkeys_valid()
    assert bob_update_believeratom.is_valid() is False

    # WHEN
    bob_update_believeratom.set_jvalue("max_tree_traverse", 14)

    # THEN
    assert bob_update_believeratom.is_jkeys_valid()
    assert bob_update_believeratom.is_valid()


def test_BelieverAtom_set_atom_order_SetCorrectAttr():
    # ESTABLISH
    bob_str = "Bob"
    bob_acct_cred_points = 55
    bob_acct_debt_points = 66
    acctunit_str = believer_acctunit_str()
    bob_insert_believeratom = believeratom_shop(acctunit_str, INSERT_str())
    cw_str = acct_cred_points_str()
    dw_str = acct_debt_points_str()
    bob_insert_believeratom.set_jkey(acct_name_str(), bob_str)
    bob_insert_believeratom.set_jvalue(cw_str, bob_acct_cred_points)
    bob_insert_believeratom.set_jvalue(dw_str, bob_acct_debt_points)
    assert bob_insert_believeratom.is_valid()

    # WHEN / THEN
    assert bob_insert_believeratom.get_value(cw_str) == bob_acct_cred_points
    assert bob_insert_believeratom.get_value(dw_str) == bob_acct_debt_points


def test_BelieverAtom_set_arg_SetsAny_jkey_jvalue():
    # ESTABLISH
    bob_str = "Bob"
    bob_acct_cred_points = 55
    bob_acct_debt_points = 66
    acctunit_str = believer_acctunit_str()
    bob_insert_believeratom = believeratom_shop(acctunit_str, INSERT_str())
    cw_str = acct_cred_points_str()
    dw_str = acct_debt_points_str()

    # WHEN
    bob_insert_believeratom.set_arg(acct_name_str(), bob_str)
    bob_insert_believeratom.set_arg(cw_str, bob_acct_cred_points)
    bob_insert_believeratom.set_arg(dw_str, bob_acct_debt_points)

    # THEN
    assert bob_insert_believeratom.get_value(acct_name_str()) == bob_str
    assert bob_insert_believeratom.get_value(cw_str) == bob_acct_cred_points
    assert bob_insert_believeratom.get_value(dw_str) == bob_acct_debt_points
    assert bob_insert_believeratom.get_value(acct_name_str()) == bob_str
    assert bob_insert_believeratom.is_valid()


def test_BelieverAtom_get_nesting_order_args_ReturnsObj_believer_acctunit():
    # ESTABLISH
    sue_str = "Sue"
    sue_insert_believeratom = believeratom_shop(believer_acctunit_str(), INSERT_str())
    sue_insert_believeratom.set_arg(acct_name_str(), sue_str)
    print(f"{sue_insert_believeratom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [sue_str]
    assert sue_insert_believeratom.get_nesting_order_args() == ordered_jkeys


def test_BelieverAtom_get_nesting_order_args_ReturnsObj_believer_acct_membership():
    # ESTABLISH
    sue_str = "Sue"
    iowa_str = ";Iowa"
    sue_insert_believeratom = believeratom_shop(
        believer_acct_membership_str(), INSERT_str()
    )
    sue_insert_believeratom.set_arg(group_title_str(), iowa_str)
    sue_insert_believeratom.set_arg(acct_name_str(), sue_str)
    print(f"{sue_insert_believeratom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [sue_str, iowa_str]
    assert sue_insert_believeratom.get_nesting_order_args() == ordered_jkeys
