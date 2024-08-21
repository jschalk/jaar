from src._road.range_toolbox import RangeUnit
from src.bud.idea import ideaunit_shop, ideas_calculated_range


def test_ideas_calculated_range_ReturnsObj_EmptyList():
    # ESTABLISH
    x_rangeunit = RangeUnit(3, 8)

    # WHEN / THEN
    assert ideas_calculated_range([], x_rangeunit.gogo, x_rangeunit.stop) == x_rangeunit


def test_ideas_calculated_range_ReturnsObj_EmptyIdeaUnit():
    # ESTABLISH
    week_text = "week"
    week_idea = ideaunit_shop(week_text)
    x_rangeunit = RangeUnit(3, 8)

    # WHEN / THEN
    assert (
        ideas_calculated_range([week_idea], x_rangeunit.gogo, x_rangeunit.stop)
        == x_rangeunit
    )


def test_ideas_calculated_range_ReturnsObj_1IdeaUnit_addin():
    # ESTABLISH
    week_text = "week"
    week_addin = 5
    week_idea = ideaunit_shop(week_text, _addin=week_addin)
    old_gogo = 3
    old_stop = 8
    old_rangeunit = RangeUnit(old_gogo, old_stop)

    # WHEN
    new_rangeunit = ideas_calculated_range(
        [week_idea], old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_gogo + week_addin
    new_stop = old_stop + week_addin
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop


def test_ideas_calculated_range_ReturnsObj_2IdeaUnit_addin():
    # ESTABLISH
    week_text = "week"
    week_addin = 5
    week_idea = ideaunit_shop(week_text, _addin=week_addin)
    tue_addin = 7
    tue_idea = ideaunit_shop("Tue", _addin=tue_addin)
    old_gogo = 3
    old_stop = 8
    old_rangeunit = RangeUnit(old_gogo, old_stop)

    # WHEN
    new_rangeunit = ideas_calculated_range(
        [week_idea, tue_idea], old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_gogo + week_addin + tue_addin
    new_stop = old_stop + week_addin + tue_addin
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop


def test_ideas_calculated_range_ReturnsObj_2IdeaUnit_numor():
    # ESTABLISH
    week_text = "week"
    week_numor = 5
    week_idea = ideaunit_shop(week_text, _numor=week_numor)
    tue_numor = 10
    tue_idea = ideaunit_shop("Tue", _numor=tue_numor)
    old_gogo = 3
    old_stop = 8
    old_rangeunit = RangeUnit(old_gogo, old_stop)
    idea_list = [week_idea, tue_idea]

    # WHEN
    new_rangeunit = ideas_calculated_range(
        idea_list, old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_gogo * week_numor * tue_numor
    new_stop = old_stop * week_numor * tue_numor
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop


def test_ideas_calculated_range_ReturnsObj_2IdeaUnit_denom():
    # ESTABLISH
    week_text = "week"
    week_denom = 5
    week_idea = ideaunit_shop(week_text, _denom=week_denom)
    tue_denom = 2
    tue_idea = ideaunit_shop("Tue", _denom=tue_denom)
    old_gogo = 30
    old_stop = 80
    old_rangeunit = RangeUnit(old_gogo, old_stop)

    idea_list = [week_idea, tue_idea]

    # WHEN
    new_rangeunit = ideas_calculated_range(
        idea_list, old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = old_rangeunit.gogo / week_denom / tue_denom
    new_stop = old_rangeunit.stop / week_denom / tue_denom
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop
    assert new_rangeunit.gogo == 3
    assert new_rangeunit.stop == 8


def test_ideas_calculated_range_ReturnsObj_2IdeaUnit_denom_morph():
    # ESTABLISH
    week_text = "week"
    week_denom = 50
    week_idea = ideaunit_shop(week_text, _denom=week_denom, _morph=True)
    tue_denom = 20
    tue_idea = ideaunit_shop("Tue", _denom=tue_denom, _morph=True)
    old_gogo = 175
    old_stop = 186
    old_rangeunit = RangeUnit(old_gogo, old_stop)
    idea_list = [week_idea, tue_idea]

    # WHEN
    new_rangeunit = ideas_calculated_range(
        idea_list, old_rangeunit.gogo, old_rangeunit.stop
    )

    # THEN
    new_gogo = (old_rangeunit.gogo % week_denom) % tue_denom
    new_stop = (old_rangeunit.stop % week_denom) % tue_denom
    assert new_rangeunit.gogo == new_gogo
    assert new_rangeunit.stop == new_stop
    assert new_rangeunit.gogo == 5
    assert new_rangeunit.stop == 16
