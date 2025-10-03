from pytest import raises as pytest_raises
from src.ch07_belief_logic.belief_main import beliefunit_shop


def test_BeliefUnit_set_credor_respect_SetsAttr():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia")

    # WHEN
    x_credor_respect = 77
    zia_belief.set_credor_respect(x_credor_respect)

    # THEN
    assert zia_belief.credor_respect == x_credor_respect


def test_BeliefUnit_set_credor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_str = "Zia"
    zia_belief = beliefunit_shop(zia_str)
    x_credor_respect = 23
    zia_belief.set_credor_respect(x_credor_respect)
    assert zia_belief.respect_grain == 1
    assert zia_belief.credor_respect == x_credor_respect

    # WHEN
    new_credor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_belief.set_credor_respect(new_credor_respect)

    # THEN
    assert (
        str(excinfo.value)
        == f"Belief '{zia_str}' cannot set credor_respect='{new_credor_respect}'. It is not divisible byrespect_grain'{zia_belief.respect_grain}'"
    )


def test_BeliefUnit_set_debtor_respect_SetsInt():
    # ESTABLISH
    zia_str = "Zia"
    zia_belief = beliefunit_shop(belief_name=zia_str)
    zia_debtor_respect = 13
    assert zia_belief.debtor_respect != zia_debtor_respect

    # WHEN
    zia_belief.set_debtor_respect(zia_debtor_respect)
    # THEN
    assert zia_belief.debtor_respect == zia_debtor_respect


def test_BeliefUnit_set_debtor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_str = "Zia"
    zia_belief = beliefunit_shop(zia_str)
    x_debtor_respect = 23
    zia_belief.set_debtor_respect(x_debtor_respect)
    assert zia_belief.respect_grain == 1
    assert zia_belief.debtor_respect == x_debtor_respect

    # WHEN
    new_debtor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_belief.set_debtor_respect(new_debtor_respect)

    # THEN
    assert (
        str(excinfo.value)
        == f"Belief '{zia_str}' cannot set debtor_respect='{new_debtor_respect}'. It is not divisible byrespect_grain'{zia_belief.respect_grain}'"
    )


def test_BeliefUnit_set_voice_respect_SetsAttrs():
    # ESTABLISH
    zia_str = "Zia"
    old_credor_respect = 77
    old_debtor_respect = 88
    old_fund_pool = 99
    zia_str = "Zia"
    zia_belief = beliefunit_shop(zia_str)
    zia_belief.set_credor_respect(old_credor_respect)
    zia_belief.set_debtor_respect(old_debtor_respect)
    zia_belief.set_fund_pool(old_fund_pool)
    assert zia_belief.credor_respect == old_credor_respect
    assert zia_belief.debtor_respect == old_debtor_respect
    assert zia_belief.fund_pool == old_fund_pool

    # WHEN
    new_voice_pool = 200
    zia_belief.set_voice_respect(new_voice_pool)

    # THEN
    assert zia_belief.credor_respect == new_voice_pool
    assert zia_belief.debtor_respect == new_voice_pool
    assert zia_belief.fund_pool == new_voice_pool
