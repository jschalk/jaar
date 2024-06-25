from src._world.world import worldunit_shop
from pytest import raises as pytest_raises


def test_WorldUnit_set_other_credor_pool_CorrectlySetsInt():
    # GIVEN
    zia_world = worldunit_shop("Zia")
    assert zia_world._other_credor_pool is None
    # WHEN
    x_other_credor_pool = 11
    zia_world.set_other_credor_pool(x_other_credor_pool)
    # THEN
    assert zia_world._other_credor_pool == x_other_credor_pool


def test_WorldUnit_set_other_credor_pool_CorrectlySets_others_credor_weightWithEmpty_others():
    # GIVEN
    zia_world = worldunit_shop("Zia")

    # WHEN
    x_other_credor_pool = 77
    zia_world.set_other_credor_pool(
        x_other_credor_pool, update_others_credor_weight=True
    )

    # THEN
    assert zia_world._other_credor_pool == x_other_credor_pool


def test_WorldUnit_set_other_credor_pool_RaisesErrorWhenArgIsNotMultiple():
    # GIVEN
    zia_text = "Zia"
    zia_world = worldunit_shop(zia_text)
    x_other_credor_pool = 23
    zia_world.set_other_credor_pool(x_other_credor_pool)
    assert zia_world._pixel == 1
    assert zia_world._other_credor_pool == x_other_credor_pool

    # WHEN
    new_other_credor_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_world.set_other_credor_pool(new_other_credor_pool)
    assert (
        str(excinfo.value)
        == f"World '{zia_text}' cannot set _other_credor_pool='{new_other_credor_pool}'. It is not divisible by pixel '{zia_world._pixel}'"
    )


def test_WorldUnit_set_other_credor_pool_CorrectlyModifies_others_credor_weight():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_credor_weight = 73
    wei_credor_weight = 79
    zia_credor_weight = 83
    zia_world = worldunit_shop(_owner_id=zia_text)
    zia_world.add_otherunit(yao_text, credor_weight=yao_credor_weight)
    zia_world.add_otherunit(wei_text, credor_weight=wei_credor_weight)
    zia_world.add_otherunit(zia_text, credor_weight=zia_credor_weight)
    x_sum = yao_credor_weight + wei_credor_weight + zia_credor_weight
    zia_world.set_other_credor_pool(x_sum)
    assert zia_world._other_credor_pool == x_sum
    assert zia_world.get_other(yao_text).credor_weight == yao_credor_weight
    assert zia_world.get_other(wei_text).credor_weight == wei_credor_weight
    assert zia_world.get_other(zia_text).credor_weight == zia_credor_weight

    # WHEN
    new_ratio = 2
    new_sum = x_sum * new_ratio
    zia_world.set_other_credor_pool(new_sum, update_others_credor_weight=True)

    # THEN
    assert zia_world._other_credor_pool == new_sum
    new_yao_credor_weight = yao_credor_weight * new_ratio
    new_wei_credor_weight = wei_credor_weight * new_ratio
    new_zia_credor_weight = zia_credor_weight * new_ratio
    assert zia_world.get_other(yao_text).credor_weight == new_yao_credor_weight
    assert zia_world.get_other(wei_text).credor_weight == new_wei_credor_weight
    assert zia_world.get_other(zia_text).credor_weight == new_zia_credor_weight


def test_WorldUnit_set_other_credor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_pixelAND_correct_pixel_issuesIsFalse():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_credor_weight = 73
    wei_credor_weight = 79
    zia_credor_weight = 83
    zia_world = worldunit_shop(zia_text)
    zia_world.add_otherunit(yao_text, credor_weight=yao_credor_weight)
    zia_world.add_otherunit(wei_text, credor_weight=wei_credor_weight)
    zia_world.add_otherunit(zia_text, credor_weight=zia_credor_weight)
    x_sum = yao_credor_weight + wei_credor_weight + zia_credor_weight
    zia_world.set_other_credor_pool(x_sum)
    assert zia_world._other_credor_pool == x_sum
    assert zia_world.get_other(yao_text).credor_weight == yao_credor_weight
    assert zia_world.get_other(wei_text).credor_weight == wei_credor_weight
    assert zia_world.get_other(zia_text).credor_weight == zia_credor_weight

    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    print(f"{new_sum=}")
    new_sum = int(new_sum)
    print(f"{new_sum=}")
    zia_world.set_other_credor_pool(
        new_other_credor_pool=new_sum,
        update_others_credor_weight=True,
        correct_pixel_issues=False,
    )

    # THEN
    assert zia_world._other_credor_pool == new_sum
    other_yao_credor_weight = zia_world.get_other(yao_text).credor_weight
    other_wei_credor_weight = zia_world.get_other(wei_text).credor_weight
    other_zia_credor_weight = zia_world.get_other(zia_text).credor_weight
    assert other_yao_credor_weight == (yao_credor_weight * new_ratio) - 0.5
    assert other_wei_credor_weight == (wei_credor_weight * new_ratio) - 0.5
    assert other_zia_credor_weight == (zia_credor_weight * new_ratio) - 0.5
    assert zia_world.get_otherunits_credor_weight_sum() == 116
    assert zia_world.get_otherunits_credor_weight_sum() != zia_world._other_credor_pool


def test_WorldUnit_set_other_credor_pool_SetAttrWhenEmpty_correct_pixel_issues_IsTrue():
    # GIVEN
    zia_world = worldunit_shop("Zia")

    # WHEN
    new_sum = 5000
    zia_world.set_other_credor_pool(
        new_other_credor_pool=new_sum,
        update_others_credor_weight=True,
        correct_pixel_issues=True,
    )

    # THEN
    assert zia_world._other_credor_pool == new_sum
    assert zia_world.get_otherunits_credor_weight_sum() == 0


def test_WorldUnit_set_other_credor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_pixelAND_correct_pixel_issuesIsTrue():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_credor_weight = 73
    wei_credor_weight = 79
    zia_credor_weight = 83
    zia_world = worldunit_shop(zia_text)
    zia_world.add_otherunit(yao_text, credor_weight=yao_credor_weight)
    zia_world.add_otherunit(wei_text, credor_weight=wei_credor_weight)
    zia_world.add_otherunit(zia_text, credor_weight=zia_credor_weight)
    x_sum = yao_credor_weight + wei_credor_weight + zia_credor_weight
    zia_world.set_other_credor_pool(x_sum)
    1
    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    new_sum = int(new_sum)
    zia_world.set_other_credor_pool(
        new_other_credor_pool=new_sum,
        update_others_credor_weight=True,
        correct_pixel_issues=True,
    )

    # THEN
    assert zia_world._other_credor_pool == new_sum
    assert zia_world.get_otherunits_credor_weight_sum() == 117
    pixel_valid_yao_credor_weight = (yao_credor_weight * new_ratio) - 0.5
    pixel_valid_wei_credor_weight = (wei_credor_weight * new_ratio) - 0.5
    pixel_valid_zia_credor_weight = (zia_credor_weight * new_ratio) - 0.5
    other_yao_credor_weight = zia_world.get_other(yao_text).credor_weight
    other_wei_credor_weight = zia_world.get_other(wei_text).credor_weight
    other_zia_credor_weight = zia_world.get_other(zia_text).credor_weight
    assert other_yao_credor_weight == pixel_valid_yao_credor_weight
    assert other_wei_credor_weight == pixel_valid_wei_credor_weight
    assert other_zia_credor_weight == pixel_valid_zia_credor_weight + 1
    assert zia_world.get_otherunits_credor_weight_sum() == zia_world._other_credor_pool


def test_WorldUnit_set_other_debtor_pool_CorrectlySetsInt():
    # GIVEN
    zia_text = "Zia"
    zia_world = worldunit_shop(_owner_id=zia_text)
    assert zia_world._other_debtor_pool is None

    # WHEN
    x_other_debtor_pool = 13
    zia_world.set_other_debtor_pool(x_other_debtor_pool)
    # THEN
    assert zia_world._other_debtor_pool == x_other_debtor_pool


def test_WorldUnit_set_other_debtor_pool_CorrectlySets_others_debtor_weightWithEmpty_others():
    # GIVEN
    zia_text = "Zia"
    zia_world = worldunit_shop(_owner_id=zia_text)

    # WHEN
    x_other_debtor_pool = 77
    zia_world.set_other_debtor_pool(
        x_other_debtor_pool, update_others_debtor_weight=True
    )

    # THEN
    assert zia_world._other_debtor_pool == x_other_debtor_pool


def test_WorldUnit_set_other_debtor_pool_RaisesErrorWhenArgIsNotMultiple():
    # GIVEN
    zia_text = "Zia"
    zia_world = worldunit_shop(zia_text)
    x_other_debtor_pool = 23
    zia_world.set_other_debtor_pool(
        x_other_debtor_pool, update_others_debtor_weight=True
    )
    assert zia_world._pixel == 1
    assert zia_world._other_debtor_pool == x_other_debtor_pool

    # WHEN
    new_other_debtor_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_world.set_other_debtor_pool(
            new_other_debtor_pool, update_others_debtor_weight=True
        )
    assert (
        str(excinfo.value)
        == f"World '{zia_text}' cannot set _other_debtor_pool='{new_other_debtor_pool}'. It is not divisible by pixel '{zia_world._pixel}'"
    )


def test_WorldUnit_set_other_debtor_pool_CorrectlyModifies_others_debtor_weight():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_world = worldunit_shop(_owner_id=zia_text)
    zia_world.add_otherunit(yao_text, debtor_weight=yao_debtor_weight)
    zia_world.add_otherunit(wei_text, debtor_weight=wei_debtor_weight)
    zia_world.add_otherunit(zia_text, debtor_weight=zia_debtor_weight)
    x_sum = yao_debtor_weight + wei_debtor_weight + zia_debtor_weight
    zia_world.set_other_debtor_pool(x_sum)
    assert zia_world._other_debtor_pool == x_sum
    assert zia_world.get_other(yao_text).debtor_weight == yao_debtor_weight
    assert zia_world.get_other(wei_text).debtor_weight == wei_debtor_weight
    assert zia_world.get_other(zia_text).debtor_weight == zia_debtor_weight

    # WHEN
    new_ratio = 2
    new_sum = x_sum * new_ratio
    zia_world.set_other_debtor_pool(new_sum, update_others_debtor_weight=True)

    # THEN
    assert zia_world._other_debtor_pool == new_sum
    new_yao_debtor_weight = yao_debtor_weight * new_ratio
    new_wei_debtor_weight = wei_debtor_weight * new_ratio
    new_zia_debtor_weight = zia_debtor_weight * new_ratio
    assert zia_world.get_other(yao_text).debtor_weight == new_yao_debtor_weight
    assert zia_world.get_other(wei_text).debtor_weight == new_wei_debtor_weight
    assert zia_world.get_other(zia_text).debtor_weight == new_zia_debtor_weight


def test_WorldUnit_set_other_debtor_pool_SetAttrWhenEmpty_correct_pixel_issues_IsTrue():
    # GIVEN
    zia_world = worldunit_shop("Zia")

    # WHEN
    new_sum = 5000
    zia_world.set_other_debtor_pool(
        new_other_debtor_pool=new_sum,
        update_others_debtor_weight=True,
        correct_pixel_issues=True,
    )

    # THEN
    assert zia_world._other_debtor_pool == new_sum
    assert zia_world.get_otherunits_debtor_weight_sum() == 0


def test_WorldUnit_set_other_debtor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_pixelAND_correct_pixel_issuesIsFalse():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_world = worldunit_shop(zia_text)
    zia_world.add_otherunit(yao_text, debtor_weight=yao_debtor_weight)
    zia_world.add_otherunit(wei_text, debtor_weight=wei_debtor_weight)
    zia_world.add_otherunit(zia_text, debtor_weight=zia_debtor_weight)
    x_sum = yao_debtor_weight + wei_debtor_weight + zia_debtor_weight
    zia_world.set_other_debtor_pool(x_sum)
    assert zia_world._other_debtor_pool == x_sum
    assert zia_world.get_other(yao_text).debtor_weight == yao_debtor_weight
    assert zia_world.get_other(wei_text).debtor_weight == wei_debtor_weight
    assert zia_world.get_other(zia_text).debtor_weight == zia_debtor_weight

    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    print(f"{new_sum=}")
    new_sum = int(new_sum)
    print(f"{new_sum=}")
    zia_world.set_other_debtor_pool(
        new_other_debtor_pool=new_sum,
        update_others_debtor_weight=True,
        correct_pixel_issues=False,
    )

    # THEN
    assert zia_world._other_debtor_pool == new_sum
    other_yao_debtor_weight = zia_world.get_other(yao_text).debtor_weight
    other_wei_debtor_weight = zia_world.get_other(wei_text).debtor_weight
    other_zia_debtor_weight = zia_world.get_other(zia_text).debtor_weight
    assert other_yao_debtor_weight == (yao_debtor_weight * new_ratio) - 0.5
    assert other_wei_debtor_weight == (wei_debtor_weight * new_ratio) - 0.5
    assert other_zia_debtor_weight == (zia_debtor_weight * new_ratio) - 0.5
    assert zia_world.get_otherunits_debtor_weight_sum() == 116
    assert zia_world.get_otherunits_debtor_weight_sum() != zia_world._other_debtor_pool


def test_WorldUnit_set_other_debtor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_pixelAND_correct_pixel_issuesIsTrue():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_world = worldunit_shop(zia_text)
    zia_world.add_otherunit(yao_text, debtor_weight=yao_debtor_weight)
    zia_world.add_otherunit(wei_text, debtor_weight=wei_debtor_weight)
    zia_world.add_otherunit(zia_text, debtor_weight=zia_debtor_weight)
    x_sum = yao_debtor_weight + wei_debtor_weight + zia_debtor_weight
    zia_world.set_other_debtor_pool(x_sum)
    1
    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    new_sum = int(new_sum)
    zia_world.set_other_debtor_pool(
        new_other_debtor_pool=new_sum,
        update_others_debtor_weight=True,
        correct_pixel_issues=True,
    )

    # THEN
    assert zia_world._other_debtor_pool == new_sum
    assert zia_world.get_otherunits_debtor_weight_sum() == 117
    pixel_valid_yao_debtor_weight = (yao_debtor_weight * new_ratio) - 0.5
    pixel_valid_wei_debtor_weight = (wei_debtor_weight * new_ratio) - 0.5
    pixel_valid_zia_debtor_weight = (zia_debtor_weight * new_ratio) - 0.5
    other_yao_debtor_weight = zia_world.get_other(yao_text).debtor_weight
    other_wei_debtor_weight = zia_world.get_other(wei_text).debtor_weight
    other_zia_debtor_weight = zia_world.get_other(zia_text).debtor_weight
    assert other_yao_debtor_weight == pixel_valid_yao_debtor_weight
    assert other_wei_debtor_weight == pixel_valid_wei_debtor_weight
    assert other_zia_debtor_weight == pixel_valid_zia_debtor_weight + 1
    assert zia_world.get_otherunits_debtor_weight_sum() == zia_world._other_debtor_pool


def test_WorldUnit_set_other_pool_CorrectlySetsAttrs():
    # GIVEN
    zia_text = "Zia"
    old_other_credor_pool = 77
    old_other_debtor_pool = 88
    zia_text = "Zia"
    zia_world = worldunit_shop(zia_text)
    zia_world.set_other_credor_pool(old_other_credor_pool)
    zia_world.set_other_debtor_pool(old_other_debtor_pool)
    assert zia_world._other_credor_pool == old_other_credor_pool
    assert zia_world._other_debtor_pool == old_other_debtor_pool

    # WHEN
    new_other_pool = 200
    zia_world.set_other_pool(new_other_pool)

    # THEN
    assert zia_world._other_credor_pool == new_other_pool
    assert zia_world._other_debtor_pool == new_other_pool