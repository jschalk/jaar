from pytest import raises as pytest_raises
from src.a06_plan_logic.plan import planunit_shop


def test_PlanUnit_set_credor_respect_CorrectlySetsAttr():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")

    # WHEN
    x_credor_respect = 77
    zia_plan.set_credor_respect(x_credor_respect)

    # THEN
    assert zia_plan.credor_respect == x_credor_respect


def test_PlanUnit_set_credor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_str = "Zia"
    zia_plan = planunit_shop(zia_str)
    x_credor_respect = 23
    zia_plan.set_credor_respect(x_credor_respect)
    assert zia_plan.respect_bit == 1
    assert zia_plan.credor_respect == x_credor_respect

    # WHEN
    new_credor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_credor_respect(new_credor_respect)
    assert (
        str(excinfo.value)
        == f"Plan '{zia_str}' cannot set credor_respect='{new_credor_respect}'. It is not divisible by bit '{zia_plan.respect_bit}'"
    )


def test_PlanUnit_set_debtor_respect_CorrectlySetsInt():
    # ESTABLISH
    zia_str = "Zia"
    zia_plan = planunit_shop(owner_name=zia_str)
    zia_debtor_respect = 13
    assert zia_plan.debtor_respect != zia_debtor_respect

    # WHEN
    zia_plan.set_debtor_respect(zia_debtor_respect)
    # THEN
    assert zia_plan.debtor_respect == zia_debtor_respect


def test_PlanUnit_set_debtor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_str = "Zia"
    zia_plan = planunit_shop(zia_str)
    x_debtor_respect = 23
    zia_plan.set_debtor_respect(x_debtor_respect)
    assert zia_plan.respect_bit == 1
    assert zia_plan.debtor_respect == x_debtor_respect

    # WHEN
    new_debtor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_debtor_respect(new_debtor_respect)
    assert (
        str(excinfo.value)
        == f"Plan '{zia_str}' cannot set debtor_respect='{new_debtor_respect}'. It is not divisible by bit '{zia_plan.respect_bit}'"
    )


def test_PlanUnit_set_acct_respect_CorrectlySetsAttrs():
    # ESTABLISH
    zia_str = "Zia"
    old_credor_respect = 77
    old_debtor_respect = 88
    old_fund_pool = 99
    zia_str = "Zia"
    zia_plan = planunit_shop(zia_str)
    zia_plan.set_credor_respect(old_credor_respect)
    zia_plan.set_debtor_respect(old_debtor_respect)
    zia_plan.set_fund_pool(old_fund_pool)
    assert zia_plan.credor_respect == old_credor_respect
    assert zia_plan.debtor_respect == old_debtor_respect
    assert zia_plan.fund_pool == old_fund_pool

    # WHEN
    new_acct_pool = 200
    zia_plan.set_acct_respect(new_acct_pool)

    # THEN
    assert zia_plan.credor_respect == new_acct_pool
    assert zia_plan.debtor_respect == new_acct_pool
    assert zia_plan.fund_pool == new_acct_pool
