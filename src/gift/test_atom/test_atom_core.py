from src.bud.acct import acctunit_shop
from src.gift.atom import AtomUnit, atomunit_shop, atom_insert, atom_delete


def test_AtomUnit_exists():
    # ESTABLISH / WHEN
    x_atomunit = AtomUnit()

    # THEN
    assert x_atomunit.category is None
    assert x_atomunit.crud_text is None
    assert x_atomunit.required_args is None
    assert x_atomunit.optional_args is None
    assert x_atomunit.atom_order is None


def test_atomunit_shop_ReturnsCorrectObj():
    # ESTABLISH
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    bob_acctunit = acctunit_shop(bob_text, bob_credor_weight, bob_debtor_weight)
    cw_text = "_credor_weight"
    dw_text = "_debtor_weight"
    bob_required_dict = {"acct_id": "huh"}
    bob_optional_dict = {cw_text: bob_acctunit.get_dict().get(cw_text)}
    bob_optional_dict[dw_text] = bob_acctunit.get_dict().get(dw_text)
    acctunit_text = "bud_acctunit"

    # WHEN
    x_atomunit = atomunit_shop(
        category=acctunit_text,
        crud_text=atom_insert(),
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )

    # THEN
    print(f"{x_atomunit=}")
    assert x_atomunit.category == acctunit_text
    assert x_atomunit.crud_text == atom_insert()
    assert x_atomunit.required_args == bob_required_dict
    assert x_atomunit.optional_args == bob_optional_dict


def test_AtomUnit_set_required_arg_CorrectlySetsAttr():
    # ESTABLISH
    bob_text = "Bob"
    acctunit_text = "bud_acctunit"
    acctunit_atomunit = atomunit_shop(acctunit_text, atom_insert())
    assert acctunit_atomunit.required_args == {}

    # WHEN
    acct_id_text = "acct_id"
    acctunit_atomunit.set_required_arg(x_key=acct_id_text, x_value=bob_text)

    # THEN
    assert acctunit_atomunit.required_args == {acct_id_text: bob_text}


def test_AtomUnit_set_optional_arg_CorrectlySetsAttr():
    # ESTABLISH
    bob_text = "Bob"
    acctunit_text = "bud_acctunit"
    acctunit_atomunit = atomunit_shop(acctunit_text, atom_insert())
    assert acctunit_atomunit.optional_args == {}

    # WHEN
    acct_id_text = "acct_id"
    acctunit_atomunit.set_optional_arg(x_key=acct_id_text, x_value=bob_text)

    # THEN
    assert acctunit_atomunit.optional_args == {acct_id_text: bob_text}


def test_AtomUnit_get_value_ReturnsCorrectObj():
    # ESTABLISH
    bob_text = "Bob"
    acctunit_text = "bud_acctunit"
    acctunit_atomunit = atomunit_shop(acctunit_text, atom_insert())
    acct_id_text = "acct_id"
    acctunit_atomunit.set_required_arg(x_key=acct_id_text, x_value=bob_text)

    # WHEN / THEN
    assert acctunit_atomunit.get_value(acct_id_text) == bob_text


def test_AtomUnit_is_optional_args_valid_ReturnsCorrectBoolean():
    # WHEN
    acctunit_text = "bud_acctunit"
    bob_insert_atomunit = atomunit_shop(acctunit_text, crud_text=atom_insert())
    assert bob_insert_atomunit.is_optional_args_valid()

    # WHEN
    bob_insert_atomunit.set_optional_arg("credor_weight", 55)
    # THEN
    assert len(bob_insert_atomunit.optional_args) == 1
    assert bob_insert_atomunit.is_optional_args_valid()

    # WHEN
    bob_insert_atomunit.set_optional_arg("debtor_weight", 66)
    # THEN
    assert len(bob_insert_atomunit.optional_args) == 2
    assert bob_insert_atomunit.is_optional_args_valid()

    # WHEN
    bob_insert_atomunit.set_optional_arg("x_x_x", 77)
    # THEN
    assert len(bob_insert_atomunit.optional_args) == 3
    assert bob_insert_atomunit.is_optional_args_valid() is False


def test_AtomUnit_is_valid_ReturnsCorrectBoolean_AcctUnit_INSERT():
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    bob_acctunit = acctunit_shop(bob_text, bob_credor_weight, bob_debtor_weight)
    acctunit_text = "bud_acctunit"

    # WHEN
    bob_insert_atomunit = atomunit_shop(acctunit_text, crud_text=atom_insert())

    # THEN
    assert bob_insert_atomunit.is_required_args_valid() is False
    assert bob_insert_atomunit.is_optional_args_valid()
    assert bob_insert_atomunit.is_valid() is False

    # WHEN
    bob_insert_atomunit.set_optional_arg("x_x_x", 12)

    # THEN
    assert bob_insert_atomunit.is_required_args_valid() is False
    assert bob_insert_atomunit.is_optional_args_valid() is False
    assert bob_insert_atomunit.is_valid() is False

    # WHEN
    acct_id_text = "acct_id"
    bob_insert_atomunit.set_required_arg(acct_id_text, bob_text)

    # THEN
    assert bob_insert_atomunit.is_required_args_valid()
    assert bob_insert_atomunit.is_optional_args_valid() is False
    assert bob_insert_atomunit.is_valid() is False

    # WHEN
    bob_insert_atomunit.optional_args = {}
    cw_text = "credor_weight"
    dw_text = "debtor_weight"
    bob_insert_atomunit.set_optional_arg(cw_text, bob_acctunit.get_dict().get(cw_text))
    bob_insert_atomunit.set_optional_arg(dw_text, bob_acctunit.get_dict().get(dw_text))

    # THEN
    assert bob_insert_atomunit.is_required_args_valid()
    assert bob_insert_atomunit.is_optional_args_valid()
    assert bob_insert_atomunit.is_valid()

    # WHEN
    bob_insert_atomunit.crud_text = None

    # THEN
    assert bob_insert_atomunit.is_required_args_valid() is False
    assert bob_insert_atomunit.is_valid() is False

    # WHEN
    bob_insert_atomunit.crud_text = atom_insert()

    # THEN
    assert bob_insert_atomunit.is_required_args_valid()
    assert bob_insert_atomunit.is_valid()


def test_AtomUnit_get_value_ReturnsObj():
    # ESTABLISH
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    bob_acctunit = acctunit_shop(bob_text, bob_credor_weight, bob_debtor_weight)
    acctunit_text = "bud_acctunit"
    bob_insert_atomunit = atomunit_shop(acctunit_text, atom_insert())
    acct_id_text = "acct_id"
    cw_text = "credor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_acctunit.get_dict()=}")
    # bob_acctunit_dict = {acct_id_text: bob_acctunit.get_dict().get(acct_id_text)}
    # print(f"{bob_acctunit_dict=}")
    bob_insert_atomunit.set_required_arg(acct_id_text, bob_text)
    bob_insert_atomunit.set_optional_arg(cw_text, bob_acctunit.get_dict().get(cw_text))
    bob_insert_atomunit.set_optional_arg(dw_text, bob_acctunit.get_dict().get(dw_text))
    assert bob_insert_atomunit.is_valid()

    # WHEN / THEN
    assert bob_insert_atomunit.get_value(cw_text) == bob_credor_weight
    assert bob_insert_atomunit.get_value(dw_text) == bob_debtor_weight


def test_AtomUnit_is_valid_ReturnsCorrectBoolean_AcctUnit_DELETE():
    bob_text = "Bob"
    acctunit_text = "bud_acctunit"
    delete_text = atom_delete()

    # WHEN
    bob_delete_atomunit = atomunit_shop(acctunit_text, crud_text=delete_text)

    # THEN
    assert bob_delete_atomunit.is_required_args_valid() is False
    assert bob_delete_atomunit.is_valid() is False

    # WHEN
    bob_delete_atomunit.set_required_arg("acct_id", bob_text)

    # THEN
    assert bob_delete_atomunit.is_required_args_valid()
    assert bob_delete_atomunit.is_valid()


def test_AtomUnit_set_atom_order_SetCorrectAttr():
    # ESTABLISH
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    acctunit_text = "bud_acctunit"
    bob_insert_atomunit = atomunit_shop(acctunit_text, atom_insert())
    acct_id_text = "acct_id"
    cw_text = "credor_weight"
    dw_text = "debtor_weight"
    bob_insert_atomunit.set_required_arg(acct_id_text, bob_text)
    bob_insert_atomunit.set_optional_arg(cw_text, bob_credor_weight)
    bob_insert_atomunit.set_optional_arg(dw_text, bob_debtor_weight)
    assert bob_insert_atomunit.is_valid()

    # WHEN / THEN
    assert bob_insert_atomunit.get_value(cw_text) == bob_credor_weight
    assert bob_insert_atomunit.get_value(dw_text) == bob_debtor_weight


def test_AtomUnit_set_arg_SetsAny_required_arg_optional_arg():
    # ESTABLISH
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    acctunit_text = "bud_acctunit"
    bob_insert_atomunit = atomunit_shop(acctunit_text, atom_insert())
    acct_id_text = "acct_id"
    cw_text = "credor_weight"
    dw_text = "debtor_weight"

    # WHEN
    bob_insert_atomunit.set_arg(acct_id_text, bob_text)
    bob_insert_atomunit.set_arg(cw_text, bob_credor_weight)
    bob_insert_atomunit.set_arg(dw_text, bob_debtor_weight)

    # THEN
    assert bob_insert_atomunit.get_value(acct_id_text) == bob_text
    assert bob_insert_atomunit.get_value(cw_text) == bob_credor_weight
    assert bob_insert_atomunit.get_value(dw_text) == bob_debtor_weight
    assert bob_insert_atomunit.get_value(acct_id_text) == bob_text
    assert bob_insert_atomunit.is_valid()
