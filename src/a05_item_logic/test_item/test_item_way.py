from src.a05_item_logic.item import itemunit_shop
from src.a04_reason_logic.reason_item import (
    reasonunit_shop,
    premiseunit_shop,
    factunit_shop,
)
from src.a01_way_logic.way import get_default_fisc_tag as root_tag, create_way


def test_ItemUnit_find_replace_way_CorrectlyModifies_parent_way():
    # ESTABLISH Item with _parent_way that will be different
    old_casa_str = "casa1"
    old_casa_way = create_way(root_tag(), old_casa_str)
    bloomers_str = "bloomers"
    old_bloomers_way = create_way(old_casa_way, bloomers_str)
    roses_str = "roses"
    old_roses_way = create_way(old_bloomers_way, roses_str)
    x_item = itemunit_shop(roses_str, parent_way=old_bloomers_way)
    assert create_way(x_item.parent_way) == old_bloomers_way
    assert create_way(x_item.parent_way, x_item.item_tag) == old_roses_way

    # WHEN
    new_casa = "casa2"
    new_casa_way = create_way(root_tag(), new_casa)
    x_item.find_replace_way(old_way=old_casa_way, new_way=new_casa_way)

    # THEN
    new_bloomers_way = create_way(new_casa_way, bloomers_str)
    new_roses_way = create_way(new_bloomers_way, roses_str)
    assert create_way(x_item.parent_way) == new_bloomers_way
    assert create_way(x_item.parent_way, x_item.item_tag) == new_roses_way


def test_ItemUnit_find_replace_way_CorrectlyModifies_reasonunits():
    # ESTABLISH Item with reason that will be different
    casa_str = "casa1"
    casa_way = create_way(root_tag(), casa_str)
    bloomers_str = "bloomers"
    bloomers_way = create_way(casa_way, bloomers_str)
    roses_str = "roses"
    roses_way = create_way(bloomers_way, roses_str)
    # reason ways
    old_water_str = "water"
    old_water_way = create_way(root_tag(), old_water_str)
    rain_str = "rain"
    old_rain_way = create_way(old_water_way, rain_str)
    # create reasonunit
    premise_x = premiseunit_shop(need=old_rain_way)
    premises_x = {premise_x.need: premise_x}
    reason_x = reasonunit_shop(old_water_way, premises=premises_x)
    reasons_x = {reason_x.base: reason_x}
    x_item = itemunit_shop(roses_str, reasonunits=reasons_x)
    # check asserts
    assert x_item.reasonunits.get(old_water_way) is not None
    old_water_rain_reason = x_item.reasonunits[old_water_way]
    assert old_water_rain_reason.base == old_water_way
    assert old_water_rain_reason.premises.get(old_rain_way) is not None
    water_rain_l_premise = old_water_rain_reason.premises[old_rain_way]
    assert water_rain_l_premise.need == old_rain_way

    # WHEN
    new_water_str = "h2o"
    new_water_way = create_way(root_tag(), new_water_str)
    assert x_item.reasonunits.get(new_water_way) is None
    x_item.find_replace_way(old_way=old_water_way, new_way=new_water_way)

    # THEN
    assert x_item.reasonunits.get(old_water_way) is None
    assert x_item.reasonunits.get(new_water_way) is not None
    new_water_rain_reason = x_item.reasonunits[new_water_way]
    assert new_water_rain_reason.base == new_water_way
    new_rain_way = create_way(new_water_way, rain_str)
    assert new_water_rain_reason.premises.get(old_rain_way) is None
    assert new_water_rain_reason.premises.get(new_rain_way) is not None
    new_water_rain_l_premise = new_water_rain_reason.premises[new_rain_way]
    assert new_water_rain_l_premise.need == new_rain_way

    print(f"{len(x_item.reasonunits)=}")
    reason_obj = x_item.reasonunits.get(new_water_way)
    assert reason_obj is not None

    print(f"{len(reason_obj.premises)=}")
    premise_obj = reason_obj.premises.get(new_rain_way)
    assert premise_obj is not None
    assert premise_obj.need == new_rain_way


def test_ItemUnit_find_replace_way_CorrectlyModifies_factunits():
    # ESTABLISH Item with factunit that will be different
    roses_str = "roses"
    old_water_str = "water"
    old_water_way = create_way(root_tag(), old_water_str)
    rain_str = "rain"
    old_rain_way = create_way(old_water_way, rain_str)

    x_factunit = factunit_shop(fbase=old_water_way, fneed=old_rain_way)
    factunits_x = {x_factunit.fbase: x_factunit}
    x_item = itemunit_shop(roses_str, factunits=factunits_x)
    assert x_item.factunits[old_water_way] is not None
    old_water_rain_factunit = x_item.factunits[old_water_way]
    assert old_water_rain_factunit.fbase == old_water_way
    assert old_water_rain_factunit.fneed == old_rain_way

    # WHEN
    new_water_str = "h2o"
    new_water_way = create_way(root_tag(), new_water_str)
    assert x_item.factunits.get(new_water_way) is None
    x_item.find_replace_way(old_way=old_water_way, new_way=new_water_way)

    # THEN
    assert x_item.factunits.get(old_water_way) is None
    assert x_item.factunits.get(new_water_way) is not None
    new_water_rain_factunit = x_item.factunits[new_water_way]
    assert new_water_rain_factunit.fbase == new_water_way
    new_rain_way = create_way(new_water_way, rain_str)
    assert new_water_rain_factunit.fneed == new_rain_way

    print(f"{len(x_item.factunits)=}")
    x_factunit = x_item.factunits.get(new_water_way)
    assert x_factunit is not None
    assert x_factunit.fbase == new_water_way
    assert x_factunit.fneed == new_rain_way


def test_ItemUnit_get_obj_key_ReturnsCorrectInfo():
    # ESTABLISH
    red_str = "red"

    # WHEN
    red_item = itemunit_shop(red_str)

    # THEN
    assert red_item.get_obj_key() == red_str


def test_ItemUnit_set_bridge_CorrectlyModifiesReasonWayUnits():
    # ESTABLISH
    casa_str = "casa"
    casa_item = itemunit_shop(casa_str)
    casa_item.set_parent_way("")

    # WHEN
    slash_str = "/"
    casa_item.set_bridge(slash_str)

    # THEN
    assert casa_item.bridge == slash_str
