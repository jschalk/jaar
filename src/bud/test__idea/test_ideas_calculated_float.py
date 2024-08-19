from src.bud.idea import ideaunit_shop, ideas_calculated_float


def test_ideas_calculated_float_ReturnsObj_EmptyList():
    # ESTABLISH
    x_float = 3

    # WHEN / THEN
    assert ideas_calculated_float([], x_float) == x_float


def test_ideas_calculated_float_ReturnsObj_EmptyIdeaUnit():
    # ESTABLISH
    week_text = "week"
    week_idea = ideaunit_shop(week_text)
    x_float = 3

    # WHEN / THEN
    assert ideas_calculated_float([week_idea], x_float) == x_float


def test_ideas_calculated_float_ReturnsObj_1IdeaUnit_addin():
    # ESTABLISH
    week_text = "week"
    week_addin = 5
    week_idea = ideaunit_shop(week_text, _addin=week_addin)
    x_float = 3

    # WHEN
    x_calc_range = ideas_calculated_float([week_idea], x_float)

    # THEN
    assert x_calc_range == x_float + week_addin


def test_ideas_calculated_float_ReturnsObj_2IdeaUnit_addin():
    # ESTABLISH
    week_text = "week"
    week_addin = 5
    week_idea = ideaunit_shop(week_text, _addin=week_addin)
    tue_addin = 7
    tue_idea = ideaunit_shop("Tue", _addin=tue_addin)
    old_float = 3

    # WHEN
    x_calc_range = ideas_calculated_float([week_idea, tue_idea], old_float)

    # THEN
    new_float = old_float + week_addin + tue_addin
    assert x_calc_range == new_float


def test_ideas_calculated_float_ReturnsObj_2IdeaUnit_numor():
    # ESTABLISH
    week_text = "week"
    week_numor = 5
    week_idea = ideaunit_shop(week_text, _numor=week_numor)
    tue_numor = 10
    tue_idea = ideaunit_shop("Tue", _numor=tue_numor)
    old_float = 3
    idea_list = [week_idea, tue_idea]

    # WHEN
    x_calc_range = ideas_calculated_float(idea_list, old_float)

    # THEN
    new_float = old_float * week_numor * tue_numor
    assert x_calc_range == new_float


def test_ideas_calculated_float_ReturnsObj_2IdeaUnit_denom():
    # ESTABLISH
    week_text = "week"
    week_denom = 5
    week_idea = ideaunit_shop(week_text, _denom=week_denom)
    tue_denom = 2
    tue_idea = ideaunit_shop("Tue", _denom=tue_denom)
    old_float = 30
    idea_list = [week_idea, tue_idea]

    # WHEN
    x_calc_range = ideas_calculated_float(idea_list, old_float)

    # THEN
    new_float = old_float / week_denom / tue_denom
    assert x_calc_range == new_float
    assert x_calc_range == 3


def test_ideas_calculated_float_ReturnsObj_2IdeaUnit_denom_reest():
    # ESTABLISH
    week_text = "week"
    week_denom = 50
    week_idea = ideaunit_shop(week_text, _denom=week_denom, _reest=True)
    tue_denom = 20
    tue_idea = ideaunit_shop("Tue", _denom=tue_denom, _reest=True)
    old_float = 175
    idea_list = [week_idea, tue_idea]

    # WHEN
    x_calc_range = ideas_calculated_float(idea_list, old_float)

    # THEN
    new_float = (old_float % week_denom) % tue_denom
    assert x_calc_range == new_float
    assert x_calc_range == 5
