from src.f02_bud.item import itemunit_shop
from src.a04_reason_logic.reason_item import (
    reasonunit_shop,
    premiseunit_shop,
    factunit_shop,
)
from src.a01_word_logic.road import get_default_fisc_title as root_title, create_road


def test_ItemUnit_find_replace_road_CorrectlyModifies_parent_road():
    # ESTABLISH Item with _parent_road that will be different
    old_casa_str = "casa1"
    old_casa_road = create_road(root_title(), old_casa_str)
    bloomers_str = "bloomers"
    old_bloomers_road = create_road(old_casa_road, bloomers_str)
    roses_str = "roses"
    old_roses_road = create_road(old_bloomers_road, roses_str)
    x_item = itemunit_shop(roses_str, parent_road=old_bloomers_road)
    assert create_road(x_item.parent_road) == old_bloomers_road
    assert create_road(x_item.parent_road, x_item.item_title) == old_roses_road

    # WHEN
    new_casa = "casa2"
    new_casa_road = create_road(root_title(), new_casa)
    x_item.find_replace_road(old_road=old_casa_road, new_road=new_casa_road)

    # THEN
    new_bloomers_road = create_road(new_casa_road, bloomers_str)
    new_roses_road = create_road(new_bloomers_road, roses_str)
    assert create_road(x_item.parent_road) == new_bloomers_road
    assert create_road(x_item.parent_road, x_item.item_title) == new_roses_road


def test_ItemUnit_find_replace_road_CorrectlyModifies_reasonunits():
    # ESTABLISH Item with reason that will be different
    casa_str = "casa1"
    casa_road = create_road(root_title(), casa_str)
    bloomers_str = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_str)
    roses_str = "roses"
    roses_road = create_road(bloomers_road, roses_str)
    # reason roads
    old_water_str = "water"
    old_water_road = create_road(root_title(), old_water_str)
    rain_str = "rain"
    old_rain_road = create_road(old_water_road, rain_str)
    # create reasonunit
    premise_x = premiseunit_shop(need=old_rain_road)
    premises_x = {premise_x.need: premise_x}
    reason_x = reasonunit_shop(old_water_road, premises=premises_x)
    reasons_x = {reason_x.base: reason_x}
    x_item = itemunit_shop(roses_str, reasonunits=reasons_x)
    # check asserts
    assert x_item.reasonunits.get(old_water_road) is not None
    old_water_rain_reason = x_item.reasonunits[old_water_road]
    assert old_water_rain_reason.base == old_water_road
    assert old_water_rain_reason.premises.get(old_rain_road) is not None
    water_rain_l_premise = old_water_rain_reason.premises[old_rain_road]
    assert water_rain_l_premise.need == old_rain_road

    # WHEN
    new_water_str = "h2o"
    new_water_road = create_road(root_title(), new_water_str)
    assert x_item.reasonunits.get(new_water_road) is None
    x_item.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert x_item.reasonunits.get(old_water_road) is None
    assert x_item.reasonunits.get(new_water_road) is not None
    new_water_rain_reason = x_item.reasonunits[new_water_road]
    assert new_water_rain_reason.base == new_water_road
    new_rain_road = create_road(new_water_road, rain_str)
    assert new_water_rain_reason.premises.get(old_rain_road) is None
    assert new_water_rain_reason.premises.get(new_rain_road) is not None
    new_water_rain_l_premise = new_water_rain_reason.premises[new_rain_road]
    assert new_water_rain_l_premise.need == new_rain_road

    print(f"{len(x_item.reasonunits)=}")
    reason_obj = x_item.reasonunits.get(new_water_road)
    assert reason_obj is not None

    print(f"{len(reason_obj.premises)=}")
    premise_obj = reason_obj.premises.get(new_rain_road)
    assert premise_obj is not None
    assert premise_obj.need == new_rain_road


def test_ItemUnit_find_replace_road_CorrectlyModifies_factunits():
    # ESTABLISH Item with factunit that will be different
    roses_str = "roses"
    old_water_str = "water"
    old_water_road = create_road(root_title(), old_water_str)
    rain_str = "rain"
    old_rain_road = create_road(old_water_road, rain_str)

    factunit_x = factunit_shop(base=old_water_road, pick=old_rain_road)
    factunits_x = {factunit_x.base: factunit_x}
    x_item = itemunit_shop(roses_str, factunits=factunits_x)
    assert x_item.factunits[old_water_road] is not None
    old_water_rain_factunit = x_item.factunits[old_water_road]
    assert old_water_rain_factunit.base == old_water_road
    assert old_water_rain_factunit.pick == old_rain_road

    # WHEN
    new_water_str = "h2o"
    new_water_road = create_road(root_title(), new_water_str)
    assert x_item.factunits.get(new_water_road) is None
    x_item.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert x_item.factunits.get(old_water_road) is None
    assert x_item.factunits.get(new_water_road) is not None
    new_water_rain_factunit = x_item.factunits[new_water_road]
    assert new_water_rain_factunit.base == new_water_road
    new_rain_road = create_road(new_water_road, rain_str)
    assert new_water_rain_factunit.pick == new_rain_road

    print(f"{len(x_item.factunits)=}")
    factunit_obj = x_item.factunits.get(new_water_road)
    assert factunit_obj is not None
    assert factunit_obj.base == new_water_road
    assert factunit_obj.pick == new_rain_road


def test_ItemUnit_get_obj_key_ReturnsCorrectInfo():
    # ESTABLISH
    red_str = "red"

    # WHEN
    red_item = itemunit_shop(red_str)

    # THEN
    assert red_item.get_obj_key() == red_str


def test_ItemUnit_set_bridge_CorrectlyModifiesReasonRoadUnits():
    # ESTABLISH
    casa_str = "casa"
    casa_item = itemunit_shop(casa_str)
    casa_item.set_parent_road("")

    # WHEN
    slash_str = "/"
    casa_item.set_bridge(slash_str)

    # THEN
    assert casa_item.bridge == slash_str
