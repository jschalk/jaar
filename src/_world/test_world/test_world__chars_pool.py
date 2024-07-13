from src._world.world import worldunit_shop
from pytest import raises as pytest_raises


def test_WorldUnit_set_char_credor_pool_CorrectlySetsInt():
    # GIVEN
    zia_world = worldunit_shop("Zia")
    assert zia_world._char_credor_pool is None
    # WHEN
    x_char_credor_pool = 11
    zia_world.set_char_credor_pool(x_char_credor_pool)
    # THEN
    assert zia_world._char_credor_pool == x_char_credor_pool


def test_WorldUnit_set_char_credor_pool_CorrectlySets_chars_credor_weightWithEmpty_chars():
    # GIVEN
    zia_world = worldunit_shop("Zia")

    # WHEN
    x_char_credor_pool = 77
    zia_world.set_char_credor_pool(x_char_credor_pool, update_chars_credor_weight=True)

    # THEN
    assert zia_world._char_credor_pool == x_char_credor_pool


def test_WorldUnit_set_char_credor_pool_RaisesErrorWhenArgIsNotMultiple():
    # GIVEN
    zia_text = "Zia"
    zia_world = worldunit_shop(zia_text)
    x_char_credor_pool = 23
    zia_world.set_char_credor_pool(x_char_credor_pool)
    assert zia_world._bit == 1
    assert zia_world._char_credor_pool == x_char_credor_pool

    # WHEN
    new_char_credor_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_world.set_char_credor_pool(new_char_credor_pool)
    assert (
        str(excinfo.value)
        == f"World '{zia_text}' cannot set _char_credor_pool='{new_char_credor_pool}'. It is not divisible by bit '{zia_world._bit}'"
    )


def test_WorldUnit_set_char_credor_pool_CorrectlyModifies_chars_credor_weight():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_credor_weight = 73
    wei_credor_weight = 79
    zia_credor_weight = 83
    zia_world = worldunit_shop(_owner_id=zia_text)
    zia_world.add_charunit(yao_text, credor_weight=yao_credor_weight)
    zia_world.add_charunit(wei_text, credor_weight=wei_credor_weight)
    zia_world.add_charunit(zia_text, credor_weight=zia_credor_weight)
    x_sum = yao_credor_weight + wei_credor_weight + zia_credor_weight
    zia_world.set_char_credor_pool(x_sum)
    assert zia_world._char_credor_pool == x_sum
    assert zia_world.get_char(yao_text).credor_weight == yao_credor_weight
    assert zia_world.get_char(wei_text).credor_weight == wei_credor_weight
    assert zia_world.get_char(zia_text).credor_weight == zia_credor_weight

    # WHEN
    new_ratio = 2
    new_sum = x_sum * new_ratio
    zia_world.set_char_credor_pool(new_sum, update_chars_credor_weight=True)

    # THEN
    assert zia_world._char_credor_pool == new_sum
    new_yao_credor_weight = yao_credor_weight * new_ratio
    new_wei_credor_weight = wei_credor_weight * new_ratio
    new_zia_credor_weight = zia_credor_weight * new_ratio
    assert zia_world.get_char(yao_text).credor_weight == new_yao_credor_weight
    assert zia_world.get_char(wei_text).credor_weight == new_wei_credor_weight
    assert zia_world.get_char(zia_text).credor_weight == new_zia_credor_weight


def test_WorldUnit_set_char_credor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_bitAND_correct_bit_issuesIsFalse():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_credor_weight = 73
    wei_credor_weight = 79
    zia_credor_weight = 83
    zia_world = worldunit_shop(zia_text)
    zia_world.add_charunit(yao_text, credor_weight=yao_credor_weight)
    zia_world.add_charunit(wei_text, credor_weight=wei_credor_weight)
    zia_world.add_charunit(zia_text, credor_weight=zia_credor_weight)
    x_sum = yao_credor_weight + wei_credor_weight + zia_credor_weight
    zia_world.set_char_credor_pool(x_sum)
    assert zia_world._char_credor_pool == x_sum
    assert zia_world.get_char(yao_text).credor_weight == yao_credor_weight
    assert zia_world.get_char(wei_text).credor_weight == wei_credor_weight
    assert zia_world.get_char(zia_text).credor_weight == zia_credor_weight

    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    print(f"{new_sum=}")
    new_sum = int(new_sum)
    print(f"{new_sum=}")
    zia_world.set_char_credor_pool(
        new_char_credor_pool=new_sum,
        update_chars_credor_weight=True,
        correct_bit_issues=False,
    )

    # THEN
    assert zia_world._char_credor_pool == new_sum
    char_yao_credor_weight = zia_world.get_char(yao_text).credor_weight
    char_wei_credor_weight = zia_world.get_char(wei_text).credor_weight
    char_zia_credor_weight = zia_world.get_char(zia_text).credor_weight
    assert char_yao_credor_weight == (yao_credor_weight * new_ratio) - 0.5
    assert char_wei_credor_weight == (wei_credor_weight * new_ratio) - 0.5
    assert char_zia_credor_weight == (zia_credor_weight * new_ratio) - 0.5
    assert zia_world.get_charunits_credor_weight_sum() == 116
    assert zia_world.get_charunits_credor_weight_sum() != zia_world._char_credor_pool


def test_WorldUnit_set_char_credor_pool_SetAttrWhenEmpty_correct_bit_issues_IsTrue():
    # GIVEN
    zia_world = worldunit_shop("Zia")

    # WHEN
    new_sum = 5000
    zia_world.set_char_credor_pool(
        new_char_credor_pool=new_sum,
        update_chars_credor_weight=True,
        correct_bit_issues=True,
    )

    # THEN
    assert zia_world._char_credor_pool == new_sum
    assert zia_world.get_charunits_credor_weight_sum() == 0


def test_WorldUnit_set_char_credor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_bitAND_correct_bit_issuesIsTrue():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_credor_weight = 73
    wei_credor_weight = 79
    zia_credor_weight = 83
    zia_world = worldunit_shop(zia_text)
    zia_world.add_charunit(yao_text, credor_weight=yao_credor_weight)
    zia_world.add_charunit(wei_text, credor_weight=wei_credor_weight)
    zia_world.add_charunit(zia_text, credor_weight=zia_credor_weight)
    x_sum = yao_credor_weight + wei_credor_weight + zia_credor_weight
    zia_world.set_char_credor_pool(x_sum)
    1
    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    new_sum = int(new_sum)
    zia_world.set_char_credor_pool(
        new_char_credor_pool=new_sum,
        update_chars_credor_weight=True,
        correct_bit_issues=True,
    )

    # THEN
    assert zia_world._char_credor_pool == new_sum
    assert zia_world.get_charunits_credor_weight_sum() == 117
    bit_valid_yao_credor_weight = (yao_credor_weight * new_ratio) - 0.5
    bit_valid_wei_credor_weight = (wei_credor_weight * new_ratio) - 0.5
    bit_valid_zia_credor_weight = (zia_credor_weight * new_ratio) - 0.5
    char_yao_credor_weight = zia_world.get_char(yao_text).credor_weight
    char_wei_credor_weight = zia_world.get_char(wei_text).credor_weight
    char_zia_credor_weight = zia_world.get_char(zia_text).credor_weight
    assert char_yao_credor_weight == bit_valid_yao_credor_weight
    assert char_wei_credor_weight == bit_valid_wei_credor_weight
    assert char_zia_credor_weight == bit_valid_zia_credor_weight + 1
    assert zia_world.get_charunits_credor_weight_sum() == zia_world._char_credor_pool


def test_WorldUnit_set_char_debtor_pool_CorrectlySetsInt():
    # GIVEN
    zia_text = "Zia"
    zia_world = worldunit_shop(_owner_id=zia_text)
    assert zia_world._char_debtor_pool is None

    # WHEN
    x_char_debtor_pool = 13
    zia_world.set_char_debtor_pool(x_char_debtor_pool)
    # THEN
    assert zia_world._char_debtor_pool == x_char_debtor_pool


def test_WorldUnit_set_char_debtor_pool_CorrectlySets_chars_debtor_weightWithEmpty_chars():
    # GIVEN
    zia_text = "Zia"
    zia_world = worldunit_shop(_owner_id=zia_text)

    # WHEN
    x_char_debtor_pool = 77
    zia_world.set_char_debtor_pool(x_char_debtor_pool, update_chars_debtor_weight=True)

    # THEN
    assert zia_world._char_debtor_pool == x_char_debtor_pool


def test_WorldUnit_set_char_debtor_pool_RaisesErrorWhenArgIsNotMultiple():
    # GIVEN
    zia_text = "Zia"
    zia_world = worldunit_shop(zia_text)
    x_char_debtor_pool = 23
    zia_world.set_char_debtor_pool(x_char_debtor_pool, update_chars_debtor_weight=True)
    assert zia_world._bit == 1
    assert zia_world._char_debtor_pool == x_char_debtor_pool

    # WHEN
    new_char_debtor_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_world.set_char_debtor_pool(
            new_char_debtor_pool, update_chars_debtor_weight=True
        )
    assert (
        str(excinfo.value)
        == f"World '{zia_text}' cannot set _char_debtor_pool='{new_char_debtor_pool}'. It is not divisible by bit '{zia_world._bit}'"
    )


def test_WorldUnit_set_char_debtor_pool_CorrectlyModifies_chars_debtor_weight():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_world = worldunit_shop(_owner_id=zia_text)
    zia_world.add_charunit(yao_text, debtor_weight=yao_debtor_weight)
    zia_world.add_charunit(wei_text, debtor_weight=wei_debtor_weight)
    zia_world.add_charunit(zia_text, debtor_weight=zia_debtor_weight)
    x_sum = yao_debtor_weight + wei_debtor_weight + zia_debtor_weight
    zia_world.set_char_debtor_pool(x_sum)
    assert zia_world._char_debtor_pool == x_sum
    assert zia_world.get_char(yao_text).debtor_weight == yao_debtor_weight
    assert zia_world.get_char(wei_text).debtor_weight == wei_debtor_weight
    assert zia_world.get_char(zia_text).debtor_weight == zia_debtor_weight

    # WHEN
    new_ratio = 2
    new_sum = x_sum * new_ratio
    zia_world.set_char_debtor_pool(new_sum, update_chars_debtor_weight=True)

    # THEN
    assert zia_world._char_debtor_pool == new_sum
    new_yao_debtor_weight = yao_debtor_weight * new_ratio
    new_wei_debtor_weight = wei_debtor_weight * new_ratio
    new_zia_debtor_weight = zia_debtor_weight * new_ratio
    assert zia_world.get_char(yao_text).debtor_weight == new_yao_debtor_weight
    assert zia_world.get_char(wei_text).debtor_weight == new_wei_debtor_weight
    assert zia_world.get_char(zia_text).debtor_weight == new_zia_debtor_weight


def test_WorldUnit_set_char_debtor_pool_SetAttrWhenEmpty_correct_bit_issues_IsTrue():
    # GIVEN
    zia_world = worldunit_shop("Zia")

    # WHEN
    new_sum = 5000
    zia_world.set_char_debtor_pool(
        new_char_debtor_pool=new_sum,
        update_chars_debtor_weight=True,
        correct_bit_issues=True,
    )

    # THEN
    assert zia_world._char_debtor_pool == new_sum
    assert zia_world.get_charunits_debtor_weight_sum() == 0


def test_WorldUnit_set_char_debtor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_bitAND_correct_bit_issuesIsFalse():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_world = worldunit_shop(zia_text)
    zia_world.add_charunit(yao_text, debtor_weight=yao_debtor_weight)
    zia_world.add_charunit(wei_text, debtor_weight=wei_debtor_weight)
    zia_world.add_charunit(zia_text, debtor_weight=zia_debtor_weight)
    x_sum = yao_debtor_weight + wei_debtor_weight + zia_debtor_weight
    zia_world.set_char_debtor_pool(x_sum)
    assert zia_world._char_debtor_pool == x_sum
    assert zia_world.get_char(yao_text).debtor_weight == yao_debtor_weight
    assert zia_world.get_char(wei_text).debtor_weight == wei_debtor_weight
    assert zia_world.get_char(zia_text).debtor_weight == zia_debtor_weight

    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    print(f"{new_sum=}")
    new_sum = int(new_sum)
    print(f"{new_sum=}")
    zia_world.set_char_debtor_pool(
        new_char_debtor_pool=new_sum,
        update_chars_debtor_weight=True,
        correct_bit_issues=False,
    )

    # THEN
    assert zia_world._char_debtor_pool == new_sum
    char_yao_debtor_weight = zia_world.get_char(yao_text).debtor_weight
    char_wei_debtor_weight = zia_world.get_char(wei_text).debtor_weight
    char_zia_debtor_weight = zia_world.get_char(zia_text).debtor_weight
    assert char_yao_debtor_weight == (yao_debtor_weight * new_ratio) - 0.5
    assert char_wei_debtor_weight == (wei_debtor_weight * new_ratio) - 0.5
    assert char_zia_debtor_weight == (zia_debtor_weight * new_ratio) - 0.5
    assert zia_world.get_charunits_debtor_weight_sum() == 116
    assert zia_world.get_charunits_debtor_weight_sum() != zia_world._char_debtor_pool


def test_WorldUnit_set_char_debtor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_bitAND_correct_bit_issuesIsTrue():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_world = worldunit_shop(zia_text)
    zia_world.add_charunit(yao_text, debtor_weight=yao_debtor_weight)
    zia_world.add_charunit(wei_text, debtor_weight=wei_debtor_weight)
    zia_world.add_charunit(zia_text, debtor_weight=zia_debtor_weight)
    x_sum = yao_debtor_weight + wei_debtor_weight + zia_debtor_weight
    zia_world.set_char_debtor_pool(x_sum)
    1
    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    new_sum = int(new_sum)
    zia_world.set_char_debtor_pool(
        new_char_debtor_pool=new_sum,
        update_chars_debtor_weight=True,
        correct_bit_issues=True,
    )

    # THEN
    assert zia_world._char_debtor_pool == new_sum
    assert zia_world.get_charunits_debtor_weight_sum() == 117
    bit_valid_yao_debtor_weight = (yao_debtor_weight * new_ratio) - 0.5
    bit_valid_wei_debtor_weight = (wei_debtor_weight * new_ratio) - 0.5
    bit_valid_zia_debtor_weight = (zia_debtor_weight * new_ratio) - 0.5
    char_yao_debtor_weight = zia_world.get_char(yao_text).debtor_weight
    char_wei_debtor_weight = zia_world.get_char(wei_text).debtor_weight
    char_zia_debtor_weight = zia_world.get_char(zia_text).debtor_weight
    assert char_yao_debtor_weight == bit_valid_yao_debtor_weight
    assert char_wei_debtor_weight == bit_valid_wei_debtor_weight
    assert char_zia_debtor_weight == bit_valid_zia_debtor_weight + 1
    assert zia_world.get_charunits_debtor_weight_sum() == zia_world._char_debtor_pool


def test_WorldUnit_set_char_pool_CorrectlySetsAttrs():
    # GIVEN
    zia_text = "Zia"
    old_char_credor_pool = 77
    old_char_debtor_pool = 88
    old_bud_pool = 99
    zia_text = "Zia"
    zia_world = worldunit_shop(zia_text)
    zia_world.set_char_credor_pool(old_char_credor_pool)
    zia_world.set_char_debtor_pool(old_char_debtor_pool)
    zia_world.set_bud_pool(old_bud_pool)
    assert zia_world._char_credor_pool == old_char_credor_pool
    assert zia_world._char_debtor_pool == old_char_debtor_pool
    assert zia_world._bud_pool == old_bud_pool

    # WHEN
    new_char_pool = 200
    zia_world.set_char_pool(new_char_pool)

    # THEN
    assert zia_world._char_credor_pool == new_char_pool
    assert zia_world._char_debtor_pool == new_char_pool
    assert zia_world._bud_pool == new_char_pool
