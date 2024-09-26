from src.f2_bud.bud import budunit_shop
from pytest import raises as pytest_raises


def test_BudUnit_set_credor_respect_CorrectlySetsAttr():
    # ESTABLISH
    zia_bud = budunit_shop("Zia")

    # WHEN
    x_credor_respect = 77
    zia_bud.set_credor_respect(x_credor_respect)

    # THEN
    assert zia_bud.credor_respect == x_credor_respect


def test_BudUnit_set_credor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_str = "Zia"
    zia_bud = budunit_shop(zia_str)
    x_credor_respect = 23
    zia_bud.set_credor_respect(x_credor_respect)
    assert zia_bud.respect_bit == 1
    assert zia_bud.credor_respect == x_credor_respect

    # WHEN
    new_credor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_credor_respect(new_credor_respect)
    assert (
        str(excinfo.value)
        == f"Bud '{zia_str}' cannot set credor_respect='{new_credor_respect}'. It is not divisible by bit '{zia_bud.respect_bit}'"
    )


def test_BudUnit_set_debtor_respect_CorrectlySetsInt():
    # ESTABLISH
    zia_str = "Zia"
    zia_bud = budunit_shop(_owner_id=zia_str)
    zia_debtor_respect = 13
    assert zia_bud.debtor_respect != zia_debtor_respect

    # WHEN
    zia_bud.set_debtor_respect(zia_debtor_respect)
    # THEN
    assert zia_bud.debtor_respect == zia_debtor_respect


def test_BudUnit_set_debtor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_str = "Zia"
    zia_bud = budunit_shop(zia_str)
    x_debtor_respect = 23
    zia_bud.set_debtor_respect(x_debtor_respect)
    assert zia_bud.respect_bit == 1
    assert zia_bud.debtor_respect == x_debtor_respect

    # WHEN
    new_debtor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_debtor_respect(new_debtor_respect)
    assert (
        str(excinfo.value)
        == f"Bud '{zia_str}' cannot set debtor_respect='{new_debtor_respect}'. It is not divisible by bit '{zia_bud.respect_bit}'"
    )


def test_BudUnit_set_acct_respect_CorrectlySetsAttrs():
    # ESTABLISH
    zia_str = "Zia"
    old_credor_respect = 77
    old_debtor_respect = 88
    old_fund_pool = 99
    zia_str = "Zia"
    zia_bud = budunit_shop(zia_str)
    zia_bud.set_credor_respect(old_credor_respect)
    zia_bud.set_debtor_respect(old_debtor_respect)
    zia_bud.set_fund_pool(old_fund_pool)
    assert zia_bud.credor_respect == old_credor_respect
    assert zia_bud.debtor_respect == old_debtor_respect
    assert zia_bud.fund_pool == old_fund_pool

    # WHEN
    new_acct_pool = 200
    zia_bud.set_acct_respect(new_acct_pool)

    # THEN
    assert zia_bud.credor_respect == new_acct_pool
    assert zia_bud.debtor_respect == new_acct_pool
    assert zia_bud.fund_pool == new_acct_pool
