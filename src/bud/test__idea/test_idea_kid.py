from src._road.road import get_default_real_id_roadnode as root_label, create_road
from src.bud.idea import ideaunit_shop
from pytest import raises as pytest_raises


def test_get_kids_in_range_GetsCorrectIdeas():
    # ESTABLISH
    mon366_text = "366months"
    mon366_idea = ideaunit_shop(_label=mon366_text, _begin=0, _close=366)
    jan_text = "Jan"
    feb29_text = "Feb29"
    mar_text = "Mar"
    mon366_idea.add_kid(idea_kid=ideaunit_shop(_label=jan_text, _begin=0, _close=31))
    mon366_idea.add_kid(idea_kid=ideaunit_shop(_label=feb29_text, _begin=31, _close=60))
    mon366_idea.add_kid(idea_kid=ideaunit_shop(_label=mar_text, _begin=31, _close=91))

    # WHEN / THEN
    assert len(mon366_idea.get_kids_in_range(begin=100, close=120)) == 0
    assert len(mon366_idea.get_kids_in_range(begin=0, close=31)) == 1
    assert len(mon366_idea.get_kids_in_range(begin=5, close=5)) == 1
    assert len(mon366_idea.get_kids_in_range(begin=0, close=61)) == 3
    assert mon366_idea.get_kids_in_range(begin=31, close=31)[0]._label == feb29_text


# def test_IdeaUnit_vaild_DenomCorrectInheritsBeginAndClose():
#     # ESTABLISH
#     casa_text = "casa"
#     clean_text = "clean"
#     # parent idea
#     casa_idea = ideaunit_shop(_label=casa_text, _begin=22.0, _close=66.0)
#     # kid idea
#     clean_idea = ideaunit_shop(_label=clean_text, _numor=1, _denom=11.0, _reest=False)

#     # WHEN
#     casa_idea.add_kid(idea_kid=clean_idea)

#     # THEN
#     assert casa_idea._kids[clean_text]._begin == 2
#     assert casa_idea._kids[clean_text]._close == 6
#     kid_idea_expected = ideaunit_shop(
#         clean_text, _numor=1, _denom=11.0, _reest=False, _begin=2, _close=6
#     )
#     assert casa_idea._kids[clean_text] == kid_idea_expected


# def test_IdeaUnit_invaild_DenomThrowsError():
#     # ESTABLISH
#     casa_text = "casa"
#     parent_idea = ideaunit_shop(_label=casa_text)
#     casa_text = "casa"
#     casa_road = create_road(root_label(), casa_text)
#     clean_text = "clean"
#     clean_road = create_road(casa_road, clean_text)
#     print(f"{clean_road=}")
#     kid_idea = ideaunit_shop(
#         clean_text, _parent_road=casa_road, _numor=1, _denom=11.0, _reest=False
#     )
#     # WHEN / THEN
#     with pytest_raises(Exception) as excinfo:
#         parent_idea.add_kid(idea_kid=kid_idea)
#     print(f"{str(excinfo.value)=}")
#     assert (
#         str(excinfo.value)
#         == f"Idea {clean_road} cannot have numor,denom,reest if parent does not have begin/close range"
#     )


def test_IdeaUnit_get_descendants_ReturnsNoRoadUnits():
    # ESTABLISH
    nation_text = "nation-state"
    nation_idea = ideaunit_shop(_label=nation_text, _parent_road=root_label())

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
    nation_idea.add_kid(idea_kid=usa_idea)

    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    texas_idea = ideaunit_shop(texas_text, _parent_road=usa_road)
    usa_idea.add_kid(idea_kid=texas_idea)

    iowa_text = "Iowa"
    iowa_road = create_road(usa_road, iowa_text)
    iowa_idea = ideaunit_shop(iowa_text, _parent_road=usa_road)
    usa_idea.add_kid(idea_kid=iowa_idea)

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
    nation_idea.add_kid(idea_kid=nation_idea)
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
