from src._world.world import worldunit_shop
from pytest import raises as pytest_raises


def test_WorldUnit_set_credor_respect_CorrectlySetsAttr():
    # ESTABLISH
    zia_world = worldunit_shop("Zia")

    # WHEN
    x_credor_respect = 77
    zia_world.set_credor_respect(x_credor_respect)

    # THEN
    assert zia_world._credor_respect == x_credor_respect


def test_WorldUnit_set_credor_respect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_text = "Zia"
    zia_world = worldunit_shop(zia_text)
    x_credor_respect = 23
    zia_world.set_credor_respect(x_credor_respect)
    assert zia_world._bit == 1
    assert zia_world._credor_respect == x_credor_respect

    # WHEN
    new_credor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_world.set_credor_respect(new_credor_respect)
    assert (
        str(excinfo.value)
        == f"World '{zia_text}' cannot set _credor_respect='{new_credor_respect}'. It is not divisible by bit '{zia_world._bit}'"
    )


def test_WorldUnit_set_debtor_resepect_CorrectlySetsInt():
    # ESTABLISH
    zia_text = "Zia"
    zia_world = worldunit_shop(_owner_id=zia_text)
    zia_debtor_respect = 13
    assert zia_world._debtor_respect != zia_debtor_respect

    # WHEN
    zia_world.set_debtor_resepect(zia_debtor_respect)
    # THEN
    assert zia_world._debtor_respect == zia_debtor_respect


def test_WorldUnit_set_debtor_resepect_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_text = "Zia"
    zia_world = worldunit_shop(zia_text)
    x_debtor_respect = 23
    zia_world.set_debtor_resepect(x_debtor_respect)
    assert zia_world._bit == 1
    assert zia_world._debtor_respect == x_debtor_respect

    # WHEN
    new_debtor_respect = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_world.set_debtor_resepect(new_debtor_respect)
    assert (
        str(excinfo.value)
        == f"World '{zia_text}' cannot set _debtor_respect='{new_debtor_respect}'. It is not divisible by bit '{zia_world._bit}'"
    )


def test_WorldUnit_set_char_respect_CorrectlySetsAttrs():
    # ESTABLISH
    zia_text = "Zia"
    old_credor_respect = 77
    old_debtor_respect = 88
    old_fund_pool = 99
    zia_text = "Zia"
    zia_world = worldunit_shop(zia_text)
    zia_world.set_credor_respect(old_credor_respect)
    zia_world.set_debtor_resepect(old_debtor_respect)
    zia_world.set_fund_pool(old_fund_pool)
    assert zia_world._credor_respect == old_credor_respect
    assert zia_world._debtor_respect == old_debtor_respect
    assert zia_world._fund_pool == old_fund_pool

    # WHEN
    new_char_pool = 200
    zia_world.set_char_respect(new_char_pool)

    # THEN
    assert zia_world._credor_respect == new_char_pool
    assert zia_world._debtor_respect == new_char_pool
    assert zia_world._fund_pool == new_char_pool
