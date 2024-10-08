from src.f02_bud.bud import budunit_shop
from src.f02_bud.item import itemunit_shop
from src.f02_bud.examples.example_buds import (
    get_budunit_with_4_levels_and_2reasons_2facts,
)
from pytest import raises as pytest_raises
from src.f01_road.road import get_default_fiscal_id_roadnode as root_label


def test_BudUnit_edit_item_label_FailsWhenItemDoesNotExist():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")

    casa_str = "casa"
    casa_road = yao_bud.make_l1_road(casa_str)
    swim_str = "swim"
    yao_bud.set_l1_item(itemunit_shop(casa_str))
    yao_bud.set_item(itemunit_shop(swim_str), parent_road=casa_road)

    # WHEN / THEN
    no_item_road = yao_bud.make_l1_road("bees")
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_item_label(old_road=no_item_road, new_label="pigeons")
    assert str(excinfo.value) == f"Item old_road='{no_item_road}' does not exist"


def test_BudUnit_edit_item_label_RaisesErrorForLevel0ItemWhen_fiscal_id_isNone():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(_owner_id=yao_str)

    casa_str = "casa"
    casa_road = yao_bud.make_l1_road(casa_str)
    swim_str = "swim"
    swim_road = yao_bud.make_road(casa_road, swim_str)
    yao_bud.set_l1_item(itemunit_shop(casa_str))
    yao_bud.set_item(itemunit_shop(swim_str), parent_road=casa_road)
    assert yao_bud._owner_id == yao_str
    assert yao_bud._itemroot._label == yao_bud._fiscal_id
    casa_item = yao_bud.get_item_obj(casa_road)
    assert casa_item._parent_road == yao_bud._fiscal_id
    swim_item = yao_bud.get_item_obj(swim_road)
    assert swim_item._parent_road == casa_road

    # WHEN
    moon_str = "moon"
    yao_bud.edit_item_label(old_road=yao_bud._fiscal_id, new_label=moon_str)

    # THEN
    # with pytest_raises(Exception) as excinfo:
    #     moon_str = "moon"
    #     yao_bud.edit_item_label(old_road=yao_bud._fiscal_id, new_label=moon_str)
    # assert (
    #     str(excinfo.value)
    #     == f"Cannot set itemroot to string other than '{yao_bud._fiscal_id}'"
    # )

    assert yao_bud._itemroot._label != moon_str
    assert yao_bud._itemroot._label == yao_bud._fiscal_id


def test_BudUnit_edit_item_label_RaisesErrorForLevel0When_fiscal_id_IsDifferent():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(_owner_id=yao_str)
    casa_str = "casa"
    casa_road = yao_bud.make_l1_road(casa_str)
    swim_str = "swim"
    swim_road = yao_bud.make_road(casa_road, swim_str)
    yao_bud.set_l1_item(itemunit_shop(casa_str))
    yao_bud.set_item(itemunit_shop(swim_str), parent_road=casa_road)
    sun_str = "sun"
    yao_bud._fiscal_id = sun_str
    yao_bud._itemroot._bud_fiscal_id = sun_str
    assert yao_bud._owner_id == yao_str
    assert yao_bud._fiscal_id == sun_str
    assert yao_bud._itemroot._bud_fiscal_id == sun_str
    assert yao_bud._itemroot._label == root_label()
    casa_item = yao_bud.get_item_obj(casa_road)
    assert casa_item._parent_road == root_label()
    swim_item = yao_bud.get_item_obj(swim_road)
    assert swim_item._parent_road == casa_road

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_str = "moon"
        yao_bud.edit_item_label(old_road=root_label(), new_label=moon_str)
    assert (
        str(excinfo.value)
        == f"Cannot set itemroot to string different than '{sun_str}'"
    )


def test_BudUnit_find_replace_road_CorrectlyModifies_kids_Scenario1():
    # ESTABLISH Item with kids that will be different
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)

    old_casa_str = "casa"
    old_casa_road = yao_bud.make_l1_road(old_casa_str)
    bloomers_str = "bloomers"
    old_bloomers_road = yao_bud.make_road(old_casa_road, bloomers_str)
    roses_str = "roses"
    old_roses_road = yao_bud.make_road(old_bloomers_road, roses_str)
    red_str = "red"
    old_red_road = yao_bud.make_road(old_roses_road, red_str)

    yao_bud.set_l1_item(itemunit_shop(old_casa_str))
    yao_bud.set_item(itemunit_shop(bloomers_str), parent_road=old_casa_road)
    yao_bud.set_item(itemunit_shop(roses_str), parent_road=old_bloomers_road)
    yao_bud.set_item(itemunit_shop(red_str), parent_road=old_roses_road)
    r_item_roses = yao_bud.get_item_obj(old_roses_road)
    r_item_bloomers = yao_bud.get_item_obj(old_bloomers_road)

    assert r_item_bloomers._kids.get(roses_str) is not None
    assert r_item_roses._parent_road == old_bloomers_road
    assert r_item_roses._kids.get(red_str) is not None
    r_item_red = r_item_roses._kids.get(red_str)
    assert r_item_red._parent_road == old_roses_road

    # WHEN
    new_casa_str = "casita"
    new_casa_road = yao_bud.make_l1_road(new_casa_str)
    yao_bud.edit_item_label(old_road=old_casa_road, new_label=new_casa_str)

    # THEN
    assert yao_bud._itemroot._kids.get(new_casa_str) is not None
    assert yao_bud._itemroot._kids.get(old_casa_str) is None

    assert r_item_bloomers._parent_road == new_casa_road
    assert r_item_bloomers._kids.get(roses_str) is not None

    r_item_roses = r_item_bloomers._kids.get(roses_str)
    new_bloomers_road = yao_bud.make_road(new_casa_road, bloomers_str)
    assert r_item_roses._parent_road == new_bloomers_road
    assert r_item_roses._kids.get(red_str) is not None
    r_item_red = r_item_roses._kids.get(red_str)
    new_roses_road = yao_bud.make_road(new_bloomers_road, roses_str)
    assert r_item_red._parent_road == new_roses_road


def test_bud_edit_item_label_Modifies_factunits():
    # ESTABLISH bud with factunits that will be different
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)

    casa_str = "casa"
    casa_road = yao_bud.make_l1_road(casa_str)
    bloomers_str = "bloomers"
    bloomers_road = yao_bud.make_road(casa_road, bloomers_str)
    roses_str = "roses"
    roses_road = yao_bud.make_road(bloomers_road, roses_str)
    old_water_str = "water"
    old_water_road = yao_bud.make_l1_road(old_water_str)
    rain_str = "rain"
    old_rain_road = yao_bud.make_road(old_water_road, rain_str)

    yao_bud.set_l1_item(itemunit_shop(casa_str))
    yao_bud.set_item(itemunit_shop(roses_str), parent_road=bloomers_road)
    yao_bud.set_item(itemunit_shop(rain_str), parent_road=old_water_road)
    yao_bud.set_fact(base=old_water_road, pick=old_rain_road)

    item_x = yao_bud.get_item_obj(roses_road)
    assert yao_bud._itemroot.factunits[old_water_road] is not None
    old_water_rain_factunit = yao_bud._itemroot.factunits[old_water_road]
    assert old_water_rain_factunit.base == old_water_road
    assert old_water_rain_factunit.pick == old_rain_road

    # WHEN
    new_water_str = "h2o"
    new_water_road = yao_bud.make_l1_road(new_water_str)
    yao_bud.set_l1_item(itemunit_shop(new_water_str))
    assert yao_bud._itemroot.factunits.get(new_water_road) is None
    yao_bud.edit_item_label(old_road=old_water_road, new_label=new_water_str)

    # THEN
    assert yao_bud._itemroot.factunits.get(old_water_road) is None
    assert yao_bud._itemroot.factunits.get(new_water_road) is not None
    new_water_rain_factunit = yao_bud._itemroot.factunits[new_water_road]
    assert new_water_rain_factunit.base == new_water_road
    new_rain_road = yao_bud.make_road(new_water_road, rain_str)
    assert new_water_rain_factunit.pick == new_rain_road

    assert yao_bud._itemroot.factunits.get(new_water_road)
    factunit_obj = yao_bud._itemroot.factunits.get(new_water_road)
    # for factunit_key, factunit_obj in yao_bud._itemroot.factunits.items():
    #     assert factunit_key == new_water_road
    assert factunit_obj.base == new_water_road
    assert factunit_obj.pick == new_rain_road


def test_bud_edit_item_label_ModifiesItemReasonUnitsScenario1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()
    old_weekday_str = "weekdays"
    old_weekday_road = sue_bud.make_l1_road(old_weekday_str)
    wednesday_str = "Wednesday"
    old_wednesday_road = sue_bud.make_road(old_weekday_road, wednesday_str)
    casa_item = sue_bud.get_item_obj(sue_bud.make_l1_road("casa"))
    # casa_wk_reason = reasonunit_shop(weekday, premises={wed_premise.need: wed_premise})
    # nation_reason = reasonunit_shop(nationstate, premises={usa_premise.need: usa_premise})
    assert len(casa_item.reasonunits) == 2
    assert casa_item.reasonunits.get(old_weekday_road) is not None
    wednesday_item = sue_bud.get_item_obj(old_weekday_road)
    casa_weekday_reason = casa_item.reasonunits.get(old_weekday_road)
    assert casa_weekday_reason.premises.get(old_wednesday_road) is not None
    assert (
        casa_weekday_reason.premises.get(old_wednesday_road).need == old_wednesday_road
    )
    new_weekday_str = "days of week"
    new_weekday_road = sue_bud.make_l1_road(new_weekday_str)
    new_wednesday_road = sue_bud.make_road(new_weekday_road, wednesday_str)
    assert casa_item.reasonunits.get(new_weekday_str) is None

    # WHEN
    # for key_x, reason_x in casa_item.reasonunits.items():
    #     print(f"Before {key_x=} {reason_x.base=}")
    print(f"BEFORE {wednesday_item._label=}")
    print(f"BEFORE {wednesday_item._parent_road=}")
    sue_bud.edit_item_label(old_road=old_weekday_road, new_label=new_weekday_str)
    # for key_x, reason_x in casa_item.reasonunits.items():
    #     print(f"AFTER {key_x=} {reason_x.base=}")
    print(f"AFTER {wednesday_item._label=}")
    print(f"AFTER {wednesday_item._parent_road=}")

    # THEN
    assert casa_item.reasonunits.get(new_weekday_road) is not None
    assert casa_item.reasonunits.get(old_weekday_road) is None
    casa_weekday_reason = casa_item.reasonunits.get(new_weekday_road)
    assert casa_weekday_reason.premises.get(new_wednesday_road) is not None
    assert (
        casa_weekday_reason.premises.get(new_wednesday_road).need == new_wednesday_road
    )
    assert len(casa_item.reasonunits) == 2


def test_bud_set_owner_id_CorrectlyModifiesBoth():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()
    assert sue_bud._owner_id == "Sue"
    assert sue_bud._itemroot._label == sue_bud._fiscal_id
    # mid_label1 = "Yao"
    # sue_bud.edit_item_label(old_road=old_label, new_label=mid_label1)
    # assert sue_bud._owner_id == old_label
    # assert sue_bud._itemroot._label == mid_label1

    # WHEN
    bob_str = "Bob"
    sue_bud.set_owner_id(new_owner_id=bob_str)

    # THEN
    assert sue_bud._owner_id == bob_str
    assert sue_bud._itemroot._label == sue_bud._fiscal_id


def test_bud_edit_item_label_RaisesErrorIfdelimiterIsInLabel():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()
    old_weekday_str = "weekdays"
    old_weekday_road = sue_bud.make_l1_road(old_weekday_str)

    # WHEN / THEN
    new_weekday_str = "days; of week"
    with pytest_raises(Exception) as excinfo:
        sue_bud.edit_item_label(old_road=old_weekday_road, new_label=new_weekday_str)
    assert (
        str(excinfo.value)
        == f"Cannot modify '{old_weekday_road}' because new_label {new_weekday_str} contains delimiter {sue_bud._road_delimiter}"
    )
