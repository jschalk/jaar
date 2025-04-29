from src.a02_finance_logic.test.range_toolbox import RangeUnit
from src.a05_item_logic.item import itemunit_shop, items_calculated_range


def test_items_calculated_range_ReturnsObj_EmptyList():
    # ESTABLISH
    x_rangeunit = RangeUnit(3, 8)

    # WHEN / THEN
    assert items_calculated_range([], x_rangeunit.gogo, x_rangeunit.stop) == x_rangeunit


def test_items_calculated_range_ReturnsObj_EmptyItemUnit():
    # ESTABLISH
    week_str = "week"
    week_item = itemunit_shop(week_str)
    x_rangeunit = RangeUnit(3, 8)

    # WHEN / THEN
    assert (
        items_calculated_range([week_item], x_rangeunit.gogo, x_rangeunit.stop)
        == x_rangeunit
    )


def test_items_calculated_range_ReturnsObj_1ItemUnit_addin():
    # ESTABLISH
    week_str = "week"
    week_addin = 5
    week_item = itemunit_shop(week_str, addin=week_addin)
    old_gogo = 3
    old_stop = 8
    old_rangeunit = RangeUnit(old_gogo, old_stop)

    # WHEN
    new_rangeunit = items_calculated_range(
        [week_item], old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_gogo + week_addin
    new_stop = old_stop + week_addin
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop


def test_items_calculated_range_ReturnsObj_2ItemUnit_addin():
    # ESTABLISH
    week_str = "week"
    week_addin = 5
    week_item = itemunit_shop(week_str, addin=week_addin)
    tue_addin = 7
    tue_item = itemunit_shop("Tue", addin=tue_addin)
    old_gogo = 3
    old_stop = 8
    old_rangeunit = RangeUnit(old_gogo, old_stop)

    # WHEN
    new_rangeunit = items_calculated_range(
        [week_item, tue_item], old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_gogo + week_addin + tue_addin
    new_stop = old_stop + week_addin + tue_addin
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop


def test_items_calculated_range_ReturnsObj_2ItemUnit_numor():
    # ESTABLISH
    week_str = "week"
    week_numor = 5
    week_item = itemunit_shop(week_str, numor=week_numor)
    tue_numor = 10
    tue_item = itemunit_shop("Tue", numor=tue_numor)
    old_gogo = 3
    old_stop = 8
    old_rangeunit = RangeUnit(old_gogo, old_stop)
    item_list = [week_item, tue_item]

    # WHEN
    new_rangeunit = items_calculated_range(
        item_list, old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_gogo * week_numor * tue_numor
    new_stop = old_stop * week_numor * tue_numor
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop


def test_items_calculated_range_ReturnsObj_2ItemUnit_denom():
    # ESTABLISH
    week_str = "week"
    week_denom = 5
    week_item = itemunit_shop(week_str, denom=week_denom)
    tue_denom = 2
    tue_item = itemunit_shop("Tue", denom=tue_denom)
    old_gogo = 30
    old_stop = 80
    old_rangeunit = RangeUnit(old_gogo, old_stop)

    item_list = [week_item, tue_item]

    # WHEN
    new_rangeunit = items_calculated_range(
        item_list, old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_rangeunit.gogo / week_denom / tue_denom
    new_stop = old_rangeunit.stop / week_denom / tue_denom
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop
    assert new_rangeunit.gogo == 3
    assert new_rangeunit.stop == 8


def test_items_calculated_range_ReturnsObj_2ItemUnit_denom_morph():
    # ESTABLISH
    week_str = "week"
    week_denom = 50
    week_item = itemunit_shop(week_str, denom=week_denom, morph=True)
    tue_denom = 20
    tue_item = itemunit_shop("Tue", denom=tue_denom, morph=True)
    old_gogo = 175
    old_stop = 186
    old_rangeunit = RangeUnit(old_gogo, old_stop)
    item_list = [week_item, tue_item]

    # WHEN
    new_rangeunit = items_calculated_range(
        item_list, old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = (old_rangeunit.gogo % week_denom) % tue_denom
    new_stop = (old_rangeunit.stop % week_denom) % tue_denom
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop
    assert new_rangeunit.gogo == 5
    assert new_rangeunit.stop == 16
