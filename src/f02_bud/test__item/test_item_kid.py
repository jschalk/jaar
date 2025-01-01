from src.f01_road.road import get_default_cmty_idea as root_idea, create_road
from src.f02_bud.item import itemunit_shop
from pytest import raises as pytest_raises


def test_get_kids_in_range_GetsCorrectItems():
    # ESTABLISH
    mon_str = "months"
    mon_item = itemunit_shop(mon_str, begin=0, close=366)
    jan_str = "Jan"
    feb_str = "Feb"
    mar_str = "Mar"
    mon_item.add_kid(itemunit_shop(jan_str))
    mon_item.add_kid(itemunit_shop(feb_str))
    mon_item.add_kid(itemunit_shop(mar_str))
    jan_item = mon_item._kids.get(jan_str)
    feb_item = mon_item._kids.get(feb_str)
    mar_item = mon_item._kids.get(mar_str)
    jan_item._gogo_calc = 0
    jan_item._stop_calc = 31
    feb_item._gogo_calc = 31
    feb_item._stop_calc = 60
    mar_item._gogo_calc = 60
    mar_item._stop_calc = 91

    # WHEN / THEN
    assert len(mon_item.get_kids_in_range(x_gogo=100, x_stop=120)) == 0
    assert len(mon_item.get_kids_in_range(x_gogo=0, x_stop=31)) == 1
    assert len(mon_item.get_kids_in_range(x_gogo=5, x_stop=5)) == 1
    assert len(mon_item.get_kids_in_range(x_gogo=0, x_stop=61)) == 3
    assert len(mon_item.get_kids_in_range(x_gogo=31, x_stop=31)) == 1
    assert set(mon_item.get_kids_in_range(x_gogo=31, x_stop=31).keys()) == {feb_str}
    assert list(mon_item.get_kids_in_range(x_gogo=31, x_stop=31).values()) == [feb_item]


def test_get_kids_in_range_EmptyParametersReturnsAll_kids():
    # ESTABLISH
    mon_str = "366months"
    mon_item = itemunit_shop(mon_str)
    jan_str = "Jan"
    feb29_str = "Feb29"
    mar_str = "Mar"
    mon_item.add_kid(itemunit_shop(jan_str))
    mon_item.add_kid(itemunit_shop(feb29_str))
    mon_item.add_kid(itemunit_shop(mar_str))

    # WHEN / THEN
    assert len(mon_item.get_kids_in_range()) == 3


def test_ItemUnit_get_descendants_ReturnsNoRoadUnits():
    # ESTABLISH
    nation_str = "nation-state"
    nation_item = itemunit_shop(nation_str, _parent_road=root_idea())

    # WHEN
    nation_descendants = nation_item.get_descendant_roads_from_kids()

    # THEN
    assert nation_descendants == {}


def test_ItemUnit_get_descendants_Returns3DescendantsRoadUnits():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_idea(), nation_str)
    nation_item = itemunit_shop(nation_str, _parent_road=root_idea())

    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    usa_item = itemunit_shop(usa_str, _parent_road=nation_road)
    nation_item.add_kid(usa_item)

    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    texas_item = itemunit_shop(texas_str, _parent_road=usa_road)
    usa_item.add_kid(texas_item)

    iowa_str = "Iowa"
    iowa_road = create_road(usa_road, iowa_str)
    iowa_item = itemunit_shop(iowa_str, _parent_road=usa_road)
    usa_item.add_kid(iowa_item)

    # WHEN
    nation_descendants = nation_item.get_descendant_roads_from_kids()

    # THEN
    assert len(nation_descendants) == 3
    assert nation_descendants.get(usa_road) is not None
    assert nation_descendants.get(texas_road) is not None
    assert nation_descendants.get(iowa_road) is not None


def test_ItemUnit_get_descendants_ErrorRaisedIfInfiniteLoop():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_idea(), nation_str)
    nation_item = itemunit_shop(nation_str, _parent_road=root_idea())
    nation_item.add_kid(nation_item)
    max_count = 1000

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        nation_item.get_descendant_roads_from_kids()
    assert (
        str(excinfo.value)
        == f"Item '{nation_item.get_road()}' either has an infinite loop or more than {max_count} descendants."
    )


def test_ItemUnit_clear_kids_CorrectlySetsAttr():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_idea(), nation_str)
    nation_item = itemunit_shop(nation_str, _parent_road=root_idea())
    nation_item.add_kid(itemunit_shop("USA", _parent_road=nation_road))
    nation_item.add_kid(itemunit_shop("France", _parent_road=nation_road))
    assert len(nation_item._kids) == 2

    # WHEN
    nation_item.clear_kids()

    # THEN
    assert len(nation_item._kids) == 0


def test_ItemUnit_get_kid_ReturnsCorrectObj():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_idea(), nation_str)
    nation_item = itemunit_shop(nation_str, _parent_road=root_idea())

    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    nation_item.add_kid(itemunit_shop(usa_str, _parent_road=nation_road))

    france_str = "France"
    france_road = create_road(nation_road, france_str)
    nation_item.add_kid(itemunit_shop(france_str, _parent_road=nation_road))
    assert len(nation_item._kids) == 2

    # WHEN
    france_item = nation_item.get_kid(france_str)

    # THEN
    assert france_item._idee == france_str


def test_ItemUnit_del_kid_CorrectModifiesAttr():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_idea(), nation_str)
    nation_item = itemunit_shop(nation_str, _parent_road=root_idea())

    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    nation_item.add_kid(itemunit_shop(usa_str, _parent_road=nation_road))

    france_str = "France"
    france_road = create_road(nation_road, france_str)
    nation_item.add_kid(itemunit_shop(france_str, _parent_road=nation_road))
    assert len(nation_item._kids) == 2

    # WHEN
    nation_item.del_kid(france_str)

    # THEN
    assert len(nation_item._kids) == 1


def test_ItemUnit_get_kids_mass_sum_ReturnsObj_Scenario0():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_idea(), nation_str)
    nation_item = itemunit_shop(nation_str, _parent_road=root_idea())
    usa_str = "USA"
    usa_item = itemunit_shop(usa_str, _parent_road=nation_road)
    nation_item.add_kid(usa_item)
    france_str = "France"
    france_item = itemunit_shop(france_str, _parent_road=nation_road)
    nation_item.add_kid(france_item)

    # WHEN / THEN
    assert nation_item.get_kids_mass_sum() == 2


def test_ItemUnit_get_kids_mass_sum_ReturnsObj_Scenario1():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_idea(), nation_str)
    nation_item = itemunit_shop(nation_str, _parent_road=root_idea())
    usa_str = "USA"
    usa_item = itemunit_shop(usa_str, mass=0, _parent_road=nation_road)
    nation_item.add_kid(usa_item)
    france_str = "France"
    france_item = itemunit_shop(france_str, mass=0, _parent_road=nation_road)
    nation_item.add_kid(france_item)

    # WHEN / THEN
    assert nation_item.get_kids_mass_sum() == 0

    # WHEN
    france_str = "France"
    france_item = itemunit_shop(france_str, mass=3, _parent_road=nation_road)
    nation_item.add_kid(france_item)

    # WHEN / THEN
    assert nation_item.get_kids_mass_sum() == 3
