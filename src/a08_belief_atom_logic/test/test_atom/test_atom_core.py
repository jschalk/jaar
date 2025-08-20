from src.a03_group_logic.partner import partnerunit_shop
from src.a06_belief_logic.test._util.a06_str import (
    belief_partner_membership_str,
    belief_partnerunit_str,
    beliefunit_str,
    group_title_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
)
from src.a08_belief_atom_logic.atom_main import BeliefAtom, beliefatom_shop
from src.a08_belief_atom_logic.test._util.a08_str import DELETE_str, INSERT_str


def test_BeliefAtom_Exists():
    # ESTABLISH / WHEN
    x_beliefatom = BeliefAtom()

    # THEN
    assert x_beliefatom.dimen is None
    assert x_beliefatom.crud_str is None
    assert x_beliefatom.jkeys is None
    assert x_beliefatom.jvalues is None
    assert x_beliefatom.atom_order is None


def test_beliefatom_shop_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_partner_cred_points = 55
    bob_partner_debt_points = 66
    bob_partnerunit = partnerunit_shop(
        bob_str, bob_partner_cred_points, bob_partner_debt_points
    )
    cw_str = "_partner_cred_points"
    dw_str = "_partner_debt_points"
    bob_required_dict = {partner_name_str(): "huh"}
    bob_optional_dict = {cw_str: bob_partnerunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_partnerunit.to_dict().get(dw_str)
    partnerunit_str = belief_partnerunit_str()

    # WHEN
    x_beliefatom = beliefatom_shop(
        dimen=partnerunit_str,
        crud_str=INSERT_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    print(f"{x_beliefatom=}")
    assert x_beliefatom.dimen == partnerunit_str
    assert x_beliefatom.crud_str == INSERT_str()
    assert x_beliefatom.jkeys == bob_required_dict
    assert x_beliefatom.jvalues == bob_optional_dict


def test_BeliefAtom_set_jkey_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    partnerunit_str = belief_partnerunit_str()
    partnerunit_beliefatom = beliefatom_shop(partnerunit_str, INSERT_str())
    assert partnerunit_beliefatom.jkeys == {}

    # WHEN
    partnerunit_beliefatom.set_jkey(x_key=partner_name_str(), x_value=bob_str)

    # THEN
    assert partnerunit_beliefatom.jkeys == {partner_name_str(): bob_str}


def test_BeliefAtom_set_jvalue_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    partnerunit_str = belief_partnerunit_str()
    partnerunit_beliefatom = beliefatom_shop(partnerunit_str, INSERT_str())
    assert partnerunit_beliefatom.jvalues == {}

    # WHEN
    partnerunit_beliefatom.set_jvalue(x_key=partner_name_str(), x_value=bob_str)

    # THEN
    assert partnerunit_beliefatom.jvalues == {partner_name_str(): bob_str}


def test_BeliefAtom_get_value_ReturnsObj_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    partnerunit_str = belief_partnerunit_str()
    partnerunit_beliefatom = beliefatom_shop(partnerunit_str, INSERT_str())
    partnerunit_beliefatom.set_jkey(x_key=partner_name_str(), x_value=bob_str)

    # WHEN / THEN
    assert partnerunit_beliefatom.get_value(partner_name_str()) == bob_str


def test_BeliefAtom_is_jvalues_valid_ReturnsBoolean():
    # ESTABLISH / WHEN
    partnerunit_str = belief_partnerunit_str()
    bob_insert_beliefatom = beliefatom_shop(partnerunit_str, crud_str=INSERT_str())
    assert bob_insert_beliefatom.is_jvalues_valid()

    # WHEN
    bob_insert_beliefatom.set_jvalue(partner_cred_points_str(), 55)
    # THEN
    assert len(bob_insert_beliefatom.jvalues) == 1
    assert bob_insert_beliefatom.is_jvalues_valid()

    # WHEN
    bob_insert_beliefatom.set_jvalue(partner_debt_points_str(), 66)
    # THEN
    assert len(bob_insert_beliefatom.jvalues) == 2
    assert bob_insert_beliefatom.is_jvalues_valid()

    # WHEN
    bob_insert_beliefatom.set_jvalue("x_x_x", 77)
    # THEN
    assert len(bob_insert_beliefatom.jvalues) == 3
    assert bob_insert_beliefatom.is_jvalues_valid() is False


def test_BeliefAtom_is_valid_ReturnsBoolean_PartnerUnit_INSERT():
    # ESTABLISH
    bob_str = "Bob"
    bob_partner_cred_points = 55
    bob_partner_debt_points = 66
    bob_partnerunit = partnerunit_shop(
        bob_str, bob_partner_cred_points, bob_partner_debt_points
    )
    partnerunit_str = belief_partnerunit_str()

    # WHEN
    bob_insert_beliefatom = beliefatom_shop(partnerunit_str, crud_str=INSERT_str())

    # THEN
    assert bob_insert_beliefatom.is_jkeys_valid() is False
    assert bob_insert_beliefatom.is_jvalues_valid()
    assert bob_insert_beliefatom.is_valid() is False

    # WHEN
    bob_insert_beliefatom.set_jvalue("x_x_x", 12)

    # THEN
    assert bob_insert_beliefatom.is_jkeys_valid() is False
    assert bob_insert_beliefatom.is_jvalues_valid() is False
    assert bob_insert_beliefatom.is_valid() is False

    # WHEN
    bob_insert_beliefatom.set_jkey(partner_name_str(), bob_str)

    # THEN
    assert bob_insert_beliefatom.is_jkeys_valid()
    assert bob_insert_beliefatom.is_jvalues_valid() is False
    assert bob_insert_beliefatom.is_valid() is False

    # WHEN
    bob_insert_beliefatom.jvalues = {}
    cw_str = partner_cred_points_str()
    dw_str = partner_debt_points_str()
    bob_insert_beliefatom.set_jvalue(cw_str, bob_partnerunit.to_dict().get(cw_str))
    bob_insert_beliefatom.set_jvalue(dw_str, bob_partnerunit.to_dict().get(dw_str))

    # THEN
    assert bob_insert_beliefatom.is_jkeys_valid()
    assert bob_insert_beliefatom.is_jvalues_valid()
    assert bob_insert_beliefatom.is_valid()

    # WHEN
    bob_insert_beliefatom.crud_str = None

    # THEN
    assert bob_insert_beliefatom.is_jkeys_valid() is False
    assert bob_insert_beliefatom.is_valid() is False

    # WHEN
    bob_insert_beliefatom.crud_str = INSERT_str()

    # THEN
    assert bob_insert_beliefatom.is_jkeys_valid()
    assert bob_insert_beliefatom.is_valid()


def test_BeliefAtom_get_value_ReturnsObj_Scenario1():
    # ESTABLISH
    bob_str = "Bob"
    bob_partner_cred_points = 55
    bob_partner_debt_points = 66
    bob_partnerunit = partnerunit_shop(
        bob_str, bob_partner_cred_points, bob_partner_debt_points
    )
    partnerunit_str = belief_partnerunit_str()
    bob_insert_beliefatom = beliefatom_shop(partnerunit_str, INSERT_str())
    cw_str = partner_cred_points_str()
    dw_str = partner_debt_points_str()
    print(f"{bob_partnerunit.to_dict()=}")
    # bob_partnerunit_dict = {partner_name_str(): bob_partnerunit.to_dict().get(partner_name_str())}
    # print(f"{bob_partnerunit_dict=}")
    bob_insert_beliefatom.set_jkey(partner_name_str(), bob_str)
    bob_insert_beliefatom.set_jvalue(cw_str, bob_partnerunit.to_dict().get(cw_str))
    bob_insert_beliefatom.set_jvalue(dw_str, bob_partnerunit.to_dict().get(dw_str))
    assert bob_insert_beliefatom.is_valid()

    # WHEN / THEN
    assert bob_insert_beliefatom.get_value(cw_str) == bob_partner_cred_points
    assert bob_insert_beliefatom.get_value(dw_str) == bob_partner_debt_points


def test_BeliefAtom_is_valid_ReturnsBoolean_PartnerUnit_DELETE():
    # ESTABLISH
    bob_str = "Bob"
    partnerunit_str = belief_partnerunit_str()
    delete_str = DELETE_str()

    # WHEN
    bob_delete_beliefatom = beliefatom_shop(partnerunit_str, crud_str=delete_str)

    # THEN
    assert bob_delete_beliefatom.is_jkeys_valid() is False
    assert bob_delete_beliefatom.is_valid() is False

    # WHEN
    bob_delete_beliefatom.set_jkey(partner_name_str(), bob_str)

    # THEN
    assert bob_delete_beliefatom.is_jkeys_valid()
    assert bob_delete_beliefatom.is_valid()


def test_BeliefAtom_is_valid_ReturnsBoolean_beliefunit():
    # ESTABLISH / WHEN
    bob_update_beliefatom = beliefatom_shop(beliefunit_str(), INSERT_str())

    # THEN
    assert bob_update_beliefatom.is_jkeys_valid()
    assert bob_update_beliefatom.is_valid() is False

    # WHEN
    bob_update_beliefatom.set_jvalue("max_tree_traverse", 14)

    # THEN
    assert bob_update_beliefatom.is_jkeys_valid()
    assert bob_update_beliefatom.is_valid()


def test_BeliefAtom_set_atom_order_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    bob_partner_cred_points = 55
    bob_partner_debt_points = 66
    partnerunit_str = belief_partnerunit_str()
    bob_insert_beliefatom = beliefatom_shop(partnerunit_str, INSERT_str())
    cw_str = partner_cred_points_str()
    dw_str = partner_debt_points_str()
    bob_insert_beliefatom.set_jkey(partner_name_str(), bob_str)
    bob_insert_beliefatom.set_jvalue(cw_str, bob_partner_cred_points)
    bob_insert_beliefatom.set_jvalue(dw_str, bob_partner_debt_points)
    assert bob_insert_beliefatom.is_valid()

    # WHEN / THEN
    assert bob_insert_beliefatom.get_value(cw_str) == bob_partner_cred_points
    assert bob_insert_beliefatom.get_value(dw_str) == bob_partner_debt_points


def test_BeliefAtom_set_arg_SetsAny_jkey_jvalue():
    # ESTABLISH
    bob_str = "Bob"
    bob_partner_cred_points = 55
    bob_partner_debt_points = 66
    partnerunit_str = belief_partnerunit_str()
    bob_insert_beliefatom = beliefatom_shop(partnerunit_str, INSERT_str())
    cw_str = partner_cred_points_str()
    dw_str = partner_debt_points_str()

    # WHEN
    bob_insert_beliefatom.set_arg(partner_name_str(), bob_str)
    bob_insert_beliefatom.set_arg(cw_str, bob_partner_cred_points)
    bob_insert_beliefatom.set_arg(dw_str, bob_partner_debt_points)

    # THEN
    assert bob_insert_beliefatom.get_value(partner_name_str()) == bob_str
    assert bob_insert_beliefatom.get_value(cw_str) == bob_partner_cred_points
    assert bob_insert_beliefatom.get_value(dw_str) == bob_partner_debt_points
    assert bob_insert_beliefatom.get_value(partner_name_str()) == bob_str
    assert bob_insert_beliefatom.is_valid()


def test_BeliefAtom_get_nesting_order_args_ReturnsObj_belief_partnerunit():
    # ESTABLISH
    sue_str = "Sue"
    sue_insert_beliefatom = beliefatom_shop(belief_partnerunit_str(), INSERT_str())
    sue_insert_beliefatom.set_arg(partner_name_str(), sue_str)
    print(f"{sue_insert_beliefatom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [sue_str]
    assert sue_insert_beliefatom.get_nesting_order_args() == ordered_jkeys


def test_BeliefAtom_get_nesting_order_args_ReturnsObj_belief_partner_membership():
    # ESTABLISH
    sue_str = "Sue"
    iowa_str = ";Iowa"
    sue_insert_beliefatom = beliefatom_shop(
        belief_partner_membership_str(), INSERT_str()
    )
    sue_insert_beliefatom.set_arg(group_title_str(), iowa_str)
    sue_insert_beliefatom.set_arg(partner_name_str(), sue_str)
    print(f"{sue_insert_beliefatom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [sue_str, iowa_str]
    assert sue_insert_beliefatom.get_nesting_order_args() == ordered_jkeys
