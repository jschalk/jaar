from pytest import raises as pytest_raises
from src.a06_owner_logic.owner import ownerunit_shop


def test_OwnerUnit_set_credor_respect_CorrectlySetsAttr():
    # ESTABLISH
    zia_owner = ownerunit_shop("Zia")

    # WHEN
    x_credor_respect = 77
    zia_owner.set_credor_respect(x_credor_respect)

    # THEN
    assert zia_owner.credor_respect == x_credor_respect


def test_OwnerUnit_set_credor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_str = "Zia"
    zia_owner = ownerunit_shop(zia_str)
    x_credor_respect = 23
    zia_owner.set_credor_respect(x_credor_respect)
    assert zia_owner.respect_bit == 1
    assert zia_owner.credor_respect == x_credor_respect

    # WHEN
    new_credor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_owner.set_credor_respect(new_credor_respect)
    assert (
        str(excinfo.value)
        == f"Owner '{zia_str}' cannot set credor_respect='{new_credor_respect}'. It is not divisible by bit '{zia_owner.respect_bit}'"
    )


def test_OwnerUnit_set_debtor_respect_CorrectlySetsInt():
    # ESTABLISH
    zia_str = "Zia"
    zia_owner = ownerunit_shop(owner_name=zia_str)
    zia_debtor_respect = 13
    assert zia_owner.debtor_respect != zia_debtor_respect

    # WHEN
    zia_owner.set_debtor_respect(zia_debtor_respect)
    # THEN
    assert zia_owner.debtor_respect == zia_debtor_respect


def test_OwnerUnit_set_debtor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_str = "Zia"
    zia_owner = ownerunit_shop(zia_str)
    x_debtor_respect = 23
    zia_owner.set_debtor_respect(x_debtor_respect)
    assert zia_owner.respect_bit == 1
    assert zia_owner.debtor_respect == x_debtor_respect

    # WHEN
    new_debtor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_owner.set_debtor_respect(new_debtor_respect)
    assert (
        str(excinfo.value)
        == f"Owner '{zia_str}' cannot set debtor_respect='{new_debtor_respect}'. It is not divisible by bit '{zia_owner.respect_bit}'"
    )


def test_OwnerUnit_set_acct_respect_CorrectlySetsAttrs():
    # ESTABLISH
    zia_str = "Zia"
    old_credor_respect = 77
    old_debtor_respect = 88
    old_fund_pool = 99
    zia_str = "Zia"
    zia_owner = ownerunit_shop(zia_str)
    zia_owner.set_credor_respect(old_credor_respect)
    zia_owner.set_debtor_respect(old_debtor_respect)
    zia_owner.set_fund_pool(old_fund_pool)
    assert zia_owner.credor_respect == old_credor_respect
    assert zia_owner.debtor_respect == old_debtor_respect
    assert zia_owner.fund_pool == old_fund_pool

    # WHEN
    new_acct_pool = 200
    zia_owner.set_acct_respect(new_acct_pool)

    # THEN
    assert zia_owner.credor_respect == new_acct_pool
    assert zia_owner.debtor_respect == new_acct_pool
    assert zia_owner.fund_pool == new_acct_pool
