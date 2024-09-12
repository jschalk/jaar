from src._road.road import get_default_pecun_id_roadnode as root_label, create_road
from src.bud.idea import ideaunit_shop
from pytest import raises as pytest_raises


def test_get_kids_in_range_GetsCorrectIdeas():
    # ESTABLISH
    mon_str = "months"
    mon_idea = ideaunit_shop(mon_str, begin=0, close=366)
    jan_str = "Jan"
    feb_str = "Feb"
    mar_str = "Mar"
    mon_idea.add_kid(ideaunit_shop(jan_str))
    mon_idea.add_kid(ideaunit_shop(feb_str))
    mon_idea.add_kid(ideaunit_shop(mar_str))
    jan_idea = mon_idea._kids.get(jan_str)
    feb_idea = mon_idea._kids.get(feb_str)
    mar_idea = mon_idea._kids.get(mar_str)
    jan_idea._gogo_calc = 0
    jan_idea._stop_calc = 31
    feb_idea._gogo_calc = 31
    feb_idea._stop_calc = 60
    mar_idea._gogo_calc = 60
    mar_idea._stop_calc = 91

    # WHEN / THEN
    assert len(mon_idea.get_kids_in_range(x_gogo=100, x_stop=120)) == 0
    assert len(mon_idea.get_kids_in_range(x_gogo=0, x_stop=31)) == 1
    assert len(mon_idea.get_kids_in_range(x_gogo=5, x_stop=5)) == 1
    assert len(mon_idea.get_kids_in_range(x_gogo=0, x_stop=61)) == 3
    assert len(mon_idea.get_kids_in_range(x_gogo=31, x_stop=31)) == 1
    assert set(mon_idea.get_kids_in_range(x_gogo=31, x_stop=31).keys()) == {feb_str}
    assert list(mon_idea.get_kids_in_range(x_gogo=31, x_stop=31).values()) == [feb_idea]


def test_get_kids_in_range_EmptyParametersReturnsAll_kids():
    # ESTABLISH
    mon_str = "366months"
    mon_idea = ideaunit_shop(mon_str)
    jan_str = "Jan"
    feb29_str = "Feb29"
    mar_str = "Mar"
    mon_idea.add_kid(ideaunit_shop(jan_str))
    mon_idea.add_kid(ideaunit_shop(feb29_str))
    mon_idea.add_kid(ideaunit_shop(mar_str))

    # WHEN / THEN
    assert len(mon_idea.get_kids_in_range()) == 3


def test_IdeaUnit_get_descendants_ReturnsNoRoadUnits():
    # ESTABLISH
    nation_str = "nation-state"
    nation_idea = ideaunit_shop(nation_str, _parent_road=root_label())

    # WHEN
    nation_descendants = nation_idea.get_descendant_roads_from_kids()

    # THEN
    assert nation_descendants == {}


def test_IdeaUnit_get_descendants_Returns3DescendantsRoadUnits():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    nation_idea = ideaunit_shop(nation_str, _parent_road=root_label())

    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    usa_idea = ideaunit_shop(usa_str, _parent_road=nation_road)
    nation_idea.add_kid(usa_idea)

    texas_str = "Texas"
    texas_road = create_road(usa_road, texas_str)
    texas_idea = ideaunit_shop(texas_str, _parent_road=usa_road)
    usa_idea.add_kid(texas_idea)

    iowa_str = "Iowa"
    iowa_road = create_road(usa_road, iowa_str)
    iowa_idea = ideaunit_shop(iowa_str, _parent_road=usa_road)
    usa_idea.add_kid(iowa_idea)

    # WHEN
    nation_descendants = nation_idea.get_descendant_roads_from_kids()

    # THEN
    assert len(nation_descendants) == 3
    assert nation_descendants.get(usa_road) is not None
    assert nation_descendants.get(texas_road) is not None
    assert nation_descendants.get(iowa_road) is not None


def test_IdeaUnit_get_descendants_ErrorRaisedIfInfiniteLoop():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    nation_idea = ideaunit_shop(nation_str, _parent_road=root_label())
    nation_idea.add_kid(nation_idea)
    max_count = 1000

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        nation_idea.get_descendant_roads_from_kids()
    assert (
        str(excinfo.value)
        == f"Idea '{nation_idea.get_road()}' either has an infinite loop or more than {max_count} descendants."
    )


def test_IdeaUnit_clear_kids_CorrectlySetsAttr():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    nation_idea = ideaunit_shop(nation_str, _parent_road=root_label())
    nation_idea.add_kid(ideaunit_shop("USA", _parent_road=nation_road))
    nation_idea.add_kid(ideaunit_shop("France", _parent_road=nation_road))
    assert len(nation_idea._kids) == 2

    # WHEN
    nation_idea.clear_kids()

    # THEN
    assert len(nation_idea._kids) == 0


def test_IdeaUnit_get_kid_ReturnsCorrectObj():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    nation_idea = ideaunit_shop(nation_str, _parent_road=root_label())

    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    nation_idea.add_kid(ideaunit_shop(usa_str, _parent_road=nation_road))

    france_str = "France"
    france_road = create_road(nation_road, france_str)
    nation_idea.add_kid(ideaunit_shop(france_str, _parent_road=nation_road))
    assert len(nation_idea._kids) == 2

    # WHEN
    france_idea = nation_idea.get_kid(france_str)

    # THEN
    assert france_idea._label == france_str


def test_IdeaUnit_del_kid_CorrectModifiesAttr():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    nation_idea = ideaunit_shop(nation_str, _parent_road=root_label())

    usa_str = "USA"
    usa_road = create_road(nation_road, usa_str)
    nation_idea.add_kid(ideaunit_shop(usa_str, _parent_road=nation_road))

    france_str = "France"
    france_road = create_road(nation_road, france_str)
    nation_idea.add_kid(ideaunit_shop(france_str, _parent_road=nation_road))
    assert len(nation_idea._kids) == 2

    # WHEN
    nation_idea.del_kid(france_str)

    # THEN
    assert len(nation_idea._kids) == 1


def test_IdeaUnit_get_kids_mass_sum_ReturnsObj_Scenario0():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    nation_idea = ideaunit_shop(nation_str, _parent_road=root_label())
    usa_str = "USA"
    usa_idea = ideaunit_shop(usa_str, _parent_road=nation_road)
    nation_idea.add_kid(usa_idea)
    france_str = "France"
    france_idea = ideaunit_shop(france_str, _parent_road=nation_road)
    nation_idea.add_kid(france_idea)

    # WHEN / THEN
    assert nation_idea.get_kids_mass_sum() == 2


def test_IdeaUnit_get_kids_mass_sum_ReturnsObj_Scenario1():
    # ESTABLISH
    nation_str = "nation-state"
    nation_road = create_road(root_label(), nation_str)
    nation_idea = ideaunit_shop(nation_str, _parent_road=root_label())
    usa_str = "USA"
    usa_idea = ideaunit_shop(usa_str, mass=0, _parent_road=nation_road)
    nation_idea.add_kid(usa_idea)
    france_str = "France"
    france_idea = ideaunit_shop(france_str, mass=0, _parent_road=nation_road)
    nation_idea.add_kid(france_idea)

    # WHEN / THEN
    assert nation_idea.get_kids_mass_sum() == 0

    # WHEN
    france_str = "France"
    france_idea = ideaunit_shop(france_str, mass=3, _parent_road=nation_road)
    nation_idea.add_kid(france_idea)

    # WHEN / THEN
    assert nation_idea.get_kids_mass_sum() == 3
