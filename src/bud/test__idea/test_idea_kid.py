from src._road.road import get_default_real_id_roadnode as root_label, create_road
from src.bud.idea import ideaunit_shop
from pytest import raises as pytest_raises


def test_get_kids_in_range_GetsCorrectIdeas():
    # ESTABLISH
    mon_text = "months"
    mon_idea = ideaunit_shop(mon_text, _begin=0, _close=366)
    jan_text = "Jan"
    feb_text = "Feb"
    mar_text = "Mar"
    mon_idea.add_kid(ideaunit_shop(jan_text))
    mon_idea.add_kid(ideaunit_shop(feb_text))
    mon_idea.add_kid(ideaunit_shop(mar_text))
    jan_idea = mon_idea._kids.get(jan_text)
    feb_idea = mon_idea._kids.get(feb_text)
    mar_idea = mon_idea._kids.get(mar_text)
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
    assert set(mon_idea.get_kids_in_range(x_gogo=31, x_stop=31).keys()) == {feb_text}
    assert list(mon_idea.get_kids_in_range(x_gogo=31, x_stop=31).values()) == [feb_idea]


def test_get_kids_in_range_EmptyParametersReturnsAll_kids():
    # ESTABLISH
    mon_text = "366months"
    mon_idea = ideaunit_shop(mon_text)
    jan_text = "Jan"
    feb29_text = "Feb29"
    mar_text = "Mar"
    mon_idea.add_kid(ideaunit_shop(jan_text))
    mon_idea.add_kid(ideaunit_shop(feb29_text))
    mon_idea.add_kid(ideaunit_shop(mar_text))

    # WHEN / THEN
    assert len(mon_idea.get_kids_in_range()) == 3


def test_IdeaUnit_get_descendants_ReturnsNoRoadUnits():
    # ESTABLISH
    nation_text = "nation-state"
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())

    # WHEN
    nation_descendants = nation_idea.get_descendant_roads_from_kids()

    # THEN
    assert nation_descendants == {}


def test_IdeaUnit_get_descendants_Returns3DescendantsRoadUnits():
    # ESTABLISH
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())

    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    usa_idea = ideaunit_shop(usa_text, _parent_road=nation_road)
    nation_idea.add_kid(usa_idea)

    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    texas_idea = ideaunit_shop(texas_text, _parent_road=usa_road)
    usa_idea.add_kid(texas_idea)

    iowa_text = "Iowa"
    iowa_road = create_road(usa_road, iowa_text)
    iowa_idea = ideaunit_shop(iowa_text, _parent_road=usa_road)
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
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())
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
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())
    nation_idea.add_kid(ideaunit_shop("USA", _parent_road=nation_road))
    nation_idea.add_kid(ideaunit_shop("France", _parent_road=nation_road))
    assert len(nation_idea._kids) == 2

    # WHEN
    nation_idea.clear_kids()

    # THEN
    assert len(nation_idea._kids) == 0


def test_IdeaUnit_get_kid_ReturnsCorrectObj():
    # ESTABLISH
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())

    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    nation_idea.add_kid(ideaunit_shop(usa_text, _parent_road=nation_road))

    france_text = "France"
    france_road = create_road(nation_road, france_text)
    nation_idea.add_kid(ideaunit_shop(france_text, _parent_road=nation_road))
    assert len(nation_idea._kids) == 2

    # WHEN
    france_idea = nation_idea.get_kid(france_text)

    # THEN
    assert france_idea._label == france_text


def test_IdeaUnit_del_kid_CorrectModifiesAttr():
    # ESTABLISH
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())

    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    nation_idea.add_kid(ideaunit_shop(usa_text, _parent_road=nation_road))

    france_text = "France"
    france_road = create_road(nation_road, france_text)
    nation_idea.add_kid(ideaunit_shop(france_text, _parent_road=nation_road))
    assert len(nation_idea._kids) == 2

    # WHEN
    nation_idea.del_kid(france_text)

    # THEN
    assert len(nation_idea._kids) == 1


def test_IdeaUnit_get_kids_mass_sum_ReturnsObj_Scenario0():
    # ESTABLISH
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())
    usa_text = "USA"
    usa_idea = ideaunit_shop(usa_text, _parent_road=nation_road)
    nation_idea.add_kid(usa_idea)
    france_text = "France"
    france_idea = ideaunit_shop(france_text, _parent_road=nation_road)
    nation_idea.add_kid(france_idea)

    # WHEN / THEN
    assert nation_idea.get_kids_mass_sum() == 2


def test_IdeaUnit_get_kids_mass_sum_ReturnsObj_Scenario1():
    # ESTABLISH
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())
    usa_text = "USA"
    usa_idea = ideaunit_shop(usa_text, _mass=0, _parent_road=nation_road)
    nation_idea.add_kid(usa_idea)
    france_text = "France"
    france_idea = ideaunit_shop(france_text, _mass=0, _parent_road=nation_road)
    nation_idea.add_kid(france_idea)

    # WHEN / THEN
    assert nation_idea.get_kids_mass_sum() == 0

    # WHEN
    france_text = "France"
    france_idea = ideaunit_shop(france_text, _mass=3, _parent_road=nation_road)
    nation_idea.add_kid(france_idea)

    # WHEN / THEN
    assert nation_idea.get_kids_mass_sum() == 3
