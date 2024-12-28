from src.f02_bud.acct import acctunit_shop
from src.f02_bud.bud_tool import (
    bud_acctunit_str,
    bud_acct_membership_str,
    budunit_str,
)
from src.f04_gift.atom_config import (
    atom_insert,
    atom_delete,
    acct_name_str,
    group_id_str,
    credit_belief_str,
    debtit_belief_str,
)
from src.f04_gift.atom import AtomUnit, atomunit_shop


def test_AtomUnit_exists():
    # ESTABLISH / WHEN
    x_atomunit = AtomUnit()

    # THEN
    assert x_atomunit.category is None
    assert x_atomunit.crud_str is None
    assert x_atomunit.jkeys is None
    assert x_atomunit.jvalues is None
    assert x_atomunit.atom_order is None


def test_atomunit_shop_ReturnsCorrectObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_credit_belief = 55
    bob_debtit_belief = 66
    bob_acctunit = acctunit_shop(bob_str, bob_credit_belief, bob_debtit_belief)
    cw_str = "_credit_belief"
    dw_str = "_debtit_belief"
    bob_required_dict = {acct_name_str(): "huh"}
    bob_optional_dict = {cw_str: bob_acctunit.get_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_acctunit.get_dict().get(dw_str)
    acctunit_str = bud_acctunit_str()

    # WHEN
    x_atomunit = atomunit_shop(
        category=acctunit_str,
        crud_str=atom_insert(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    print(f"{x_atomunit=}")
    assert x_atomunit.category == acctunit_str
    assert x_atomunit.crud_str == atom_insert()
    assert x_atomunit.jkeys == bob_required_dict
    assert x_atomunit.jvalues == bob_optional_dict


def test_AtomUnit_set_jkey_CorrectlySetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    acctunit_str = bud_acctunit_str()
    acctunit_atomunit = atomunit_shop(acctunit_str, atom_insert())
    assert acctunit_atomunit.jkeys == {}

    # WHEN
    acctunit_atomunit.set_jkey(x_key=acct_name_str(), x_value=bob_str)

    # THEN
    assert acctunit_atomunit.jkeys == {acct_name_str(): bob_str}


def test_AtomUnit_set_jvalue_CorrectlySetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    acctunit_str = bud_acctunit_str()
    acctunit_atomunit = atomunit_shop(acctunit_str, atom_insert())
    assert acctunit_atomunit.jvalues == {}

    # WHEN
    acctunit_atomunit.set_jvalue(x_key=acct_name_str(), x_value=bob_str)

    # THEN
    assert acctunit_atomunit.jvalues == {acct_name_str(): bob_str}


def test_AtomUnit_get_value_ReturnsCorrectObj():
    # ESTABLISH
    bob_str = "Bob"
    acctunit_str = bud_acctunit_str()
    acctunit_atomunit = atomunit_shop(acctunit_str, atom_insert())
    acctunit_atomunit.set_jkey(x_key=acct_name_str(), x_value=bob_str)

    # WHEN / THEN
    assert acctunit_atomunit.get_value(acct_name_str()) == bob_str


def test_AtomUnit_is_jvalues_valid_ReturnsCorrectBoolean():
    # WHEN
    acctunit_str = bud_acctunit_str()
    bob_insert_atomunit = atomunit_shop(acctunit_str, crud_str=atom_insert())
    assert bob_insert_atomunit.is_jvalues_valid()

    # WHEN
    bob_insert_atomunit.set_jvalue(credit_belief_str(), 55)
    # THEN
    assert len(bob_insert_atomunit.jvalues) == 1
    assert bob_insert_atomunit.is_jvalues_valid()

    # WHEN
    bob_insert_atomunit.set_jvalue(debtit_belief_str(), 66)
    # THEN
    assert len(bob_insert_atomunit.jvalues) == 2
    assert bob_insert_atomunit.is_jvalues_valid()

    # WHEN
    bob_insert_atomunit.set_jvalue("x_x_x", 77)
    # THEN
    assert len(bob_insert_atomunit.jvalues) == 3
    assert bob_insert_atomunit.is_jvalues_valid() is False


def test_AtomUnit_is_valid_ReturnsCorrectBoolean_AcctUnit_INSERT():
    bob_str = "Bob"
    bob_credit_belief = 55
    bob_debtit_belief = 66
    bob_acctunit = acctunit_shop(bob_str, bob_credit_belief, bob_debtit_belief)
    acctunit_str = bud_acctunit_str()

    # WHEN
    bob_insert_atomunit = atomunit_shop(acctunit_str, crud_str=atom_insert())

    # THEN
    assert bob_insert_atomunit.is_jkeys_valid() is False
    assert bob_insert_atomunit.is_jvalues_valid()
    assert bob_insert_atomunit.is_valid() is False

    # WHEN
    bob_insert_atomunit.set_jvalue("x_x_x", 12)

    # THEN
    assert bob_insert_atomunit.is_jkeys_valid() is False
    assert bob_insert_atomunit.is_jvalues_valid() is False
    assert bob_insert_atomunit.is_valid() is False

    # WHEN
    bob_insert_atomunit.set_jkey(acct_name_str(), bob_str)

    # THEN
    assert bob_insert_atomunit.is_jkeys_valid()
    assert bob_insert_atomunit.is_jvalues_valid() is False
    assert bob_insert_atomunit.is_valid() is False

    # WHEN
    bob_insert_atomunit.jvalues = {}
    cw_str = credit_belief_str()
    dw_str = debtit_belief_str()
    bob_insert_atomunit.set_jvalue(cw_str, bob_acctunit.get_dict().get(cw_str))
    bob_insert_atomunit.set_jvalue(dw_str, bob_acctunit.get_dict().get(dw_str))

    # THEN
    assert bob_insert_atomunit.is_jkeys_valid()
    assert bob_insert_atomunit.is_jvalues_valid()
    assert bob_insert_atomunit.is_valid()

    # WHEN
    bob_insert_atomunit.crud_str = None

    # THEN
    assert bob_insert_atomunit.is_jkeys_valid() is False
    assert bob_insert_atomunit.is_valid() is False

    # WHEN
    bob_insert_atomunit.crud_str = atom_insert()

    # THEN
    assert bob_insert_atomunit.is_jkeys_valid()
    assert bob_insert_atomunit.is_valid()


def test_AtomUnit_get_value_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_credit_belief = 55
    bob_debtit_belief = 66
    bob_acctunit = acctunit_shop(bob_str, bob_credit_belief, bob_debtit_belief)
    acctunit_str = bud_acctunit_str()
    bob_insert_atomunit = atomunit_shop(acctunit_str, atom_insert())
    cw_str = credit_belief_str()
    dw_str = debtit_belief_str()
    print(f"{bob_acctunit.get_dict()=}")
    # bob_acctunit_dict = {acct_name_str(): bob_acctunit.get_dict().get(acct_name_str())}
    # print(f"{bob_acctunit_dict=}")
    bob_insert_atomunit.set_jkey(acct_name_str(), bob_str)
    bob_insert_atomunit.set_jvalue(cw_str, bob_acctunit.get_dict().get(cw_str))
    bob_insert_atomunit.set_jvalue(dw_str, bob_acctunit.get_dict().get(dw_str))
    assert bob_insert_atomunit.is_valid()

    # WHEN / THEN
    assert bob_insert_atomunit.get_value(cw_str) == bob_credit_belief
    assert bob_insert_atomunit.get_value(dw_str) == bob_debtit_belief


def test_AtomUnit_is_valid_ReturnsCorrectBoolean_AcctUnit_DELETE():
    bob_str = "Bob"
    acctunit_str = bud_acctunit_str()
    delete_str = atom_delete()

    # WHEN
    bob_delete_atomunit = atomunit_shop(acctunit_str, crud_str=delete_str)

    # THEN
    assert bob_delete_atomunit.is_jkeys_valid() is False
    assert bob_delete_atomunit.is_valid() is False

    # WHEN
    bob_delete_atomunit.set_jkey(acct_name_str(), bob_str)

    # THEN
    assert bob_delete_atomunit.is_jkeys_valid()
    assert bob_delete_atomunit.is_valid()


def test_AtomUnit_is_valid_ReturnsCorrectBoolean_budunit():
    # ESTABLISH / WHEN
    bob_update_atomunit = atomunit_shop(budunit_str(), atom_insert())

    # THEN
    assert bob_update_atomunit.is_jkeys_valid()
    assert bob_update_atomunit.is_valid() is False

    # WHEN
    bob_update_atomunit.set_jvalue("max_tree_traverse", 14)

    # THEN
    assert bob_update_atomunit.is_jkeys_valid()
    assert bob_update_atomunit.is_valid()


def test_AtomUnit_set_atom_order_SetCorrectAttr():
    # ESTABLISH
    bob_str = "Bob"
    bob_credit_belief = 55
    bob_debtit_belief = 66
    acctunit_str = bud_acctunit_str()
    bob_insert_atomunit = atomunit_shop(acctunit_str, atom_insert())
    cw_str = credit_belief_str()
    dw_str = debtit_belief_str()
    bob_insert_atomunit.set_jkey(acct_name_str(), bob_str)
    bob_insert_atomunit.set_jvalue(cw_str, bob_credit_belief)
    bob_insert_atomunit.set_jvalue(dw_str, bob_debtit_belief)
    assert bob_insert_atomunit.is_valid()

    # WHEN / THEN
    assert bob_insert_atomunit.get_value(cw_str) == bob_credit_belief
    assert bob_insert_atomunit.get_value(dw_str) == bob_debtit_belief


def test_AtomUnit_set_arg_SetsAny_jkey_jvalue():
    # ESTABLISH
    bob_str = "Bob"
    bob_credit_belief = 55
    bob_debtit_belief = 66
    acctunit_str = bud_acctunit_str()
    bob_insert_atomunit = atomunit_shop(acctunit_str, atom_insert())
    cw_str = credit_belief_str()
    dw_str = debtit_belief_str()

    # WHEN
    bob_insert_atomunit.set_arg(acct_name_str(), bob_str)
    bob_insert_atomunit.set_arg(cw_str, bob_credit_belief)
    bob_insert_atomunit.set_arg(dw_str, bob_debtit_belief)

    # THEN
    assert bob_insert_atomunit.get_value(acct_name_str()) == bob_str
    assert bob_insert_atomunit.get_value(cw_str) == bob_credit_belief
    assert bob_insert_atomunit.get_value(dw_str) == bob_debtit_belief
    assert bob_insert_atomunit.get_value(acct_name_str()) == bob_str
    assert bob_insert_atomunit.is_valid()


def test_AtomUnit_get_nesting_order_args_ReturnsObj_bud_acctunit():
    # ESTABLISH
    sue_str = "Sue"
    sue_insert_atomunit = atomunit_shop(bud_acctunit_str(), atom_insert())
    sue_insert_atomunit.set_arg(acct_name_str(), sue_str)
    print(f"{sue_insert_atomunit.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [sue_str]
    assert sue_insert_atomunit.get_nesting_order_args() == ordered_jkeys


def test_AtomUnit_get_nesting_order_args_ReturnsObj_bud_acct_membership():
    # ESTABLISH
    sue_str = "Sue"
    iowa_str = ";Iowa"
    sue_insert_atomunit = atomunit_shop(bud_acct_membership_str(), atom_insert())
    sue_insert_atomunit.set_arg(group_id_str(), iowa_str)
    sue_insert_atomunit.set_arg(acct_name_str(), sue_str)
    print(f"{sue_insert_atomunit.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [sue_str, iowa_str]
    assert sue_insert_atomunit.get_nesting_order_args() == ordered_jkeys
