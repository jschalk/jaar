from src.a05_idea_logic.idea import ideaunit_shop
from src.a04_reason_logic.reason_idea import (
    reasonunit_shop,
    premiseunit_shop,
    factunit_shop,
)
from src.a01_way_logic.way import get_default_fisc_tag as root_tag, create_way


def test_IdeaUnit_find_replace_way_CorrectlyModifies_parent_way():
    # ESTABLISH Idea with _parent_way that will be different
    old_casa_str = "casa1"
    old_casa_way = create_way(root_tag(), old_casa_str)
    bloomers_str = "bloomers"
    old_bloomers_way = create_way(old_casa_way, bloomers_str)
    roses_str = "roses"
    old_roses_way = create_way(old_bloomers_way, roses_str)
    x_idea = ideaunit_shop(roses_str, parent_way=old_bloomers_way)
    assert create_way(x_idea.parent_way) == old_bloomers_way
    assert create_way(x_idea.parent_way, x_idea.idea_tag) == old_roses_way

    # WHEN
    new_casa = "casa2"
    new_casa_way = create_way(root_tag(), new_casa)
    x_idea.find_replace_way(old_way=old_casa_way, new_way=new_casa_way)

    # THEN
    new_bloomers_way = create_way(new_casa_way, bloomers_str)
    new_roses_way = create_way(new_bloomers_way, roses_str)
    assert create_way(x_idea.parent_way) == new_bloomers_way
    assert create_way(x_idea.parent_way, x_idea.idea_tag) == new_roses_way


def test_IdeaUnit_find_replace_way_CorrectlyModifies_reasonunits():
    # ESTABLISH Idea with reason that will be different
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
    premise_x = premiseunit_shop(branch=old_rain_way)
    premises_x = {premise_x.branch: premise_x}
    x_reason = reasonunit_shop(old_water_way, premises=premises_x)
    reasons_x = {x_reason.context: x_reason}
    x_idea = ideaunit_shop(roses_str, reasonunits=reasons_x)
    # check asserts
    assert x_idea.reasonunits.get(old_water_way) is not None
    old_water_rain_reason = x_idea.reasonunits[old_water_way]
    assert old_water_rain_reason.context == old_water_way
    assert old_water_rain_reason.premises.get(old_rain_way) is not None
    water_rain_l_premise = old_water_rain_reason.premises[old_rain_way]
    assert water_rain_l_premise.branch == old_rain_way

    # WHEN
    new_water_str = "h2o"
    new_water_way = create_way(root_tag(), new_water_str)
    assert x_idea.reasonunits.get(new_water_way) is None
    x_idea.find_replace_way(old_way=old_water_way, new_way=new_water_way)

    # THEN
    assert x_idea.reasonunits.get(old_water_way) is None
    assert x_idea.reasonunits.get(new_water_way) is not None
    new_water_rain_reason = x_idea.reasonunits[new_water_way]
    assert new_water_rain_reason.context == new_water_way
    new_rain_way = create_way(new_water_way, rain_str)
    assert new_water_rain_reason.premises.get(old_rain_way) is None
    assert new_water_rain_reason.premises.get(new_rain_way) is not None
    new_water_rain_l_premise = new_water_rain_reason.premises[new_rain_way]
    assert new_water_rain_l_premise.branch == new_rain_way

    print(f"{len(x_idea.reasonunits)=}")
    reason_obj = x_idea.reasonunits.get(new_water_way)
    assert reason_obj is not None

    print(f"{len(reason_obj.premises)=}")
    premise_obj = reason_obj.premises.get(new_rain_way)
    assert premise_obj is not None
    assert premise_obj.branch == new_rain_way


def test_IdeaUnit_find_replace_way_CorrectlyModifies_factunits():
    # ESTABLISH Idea with factunit that will be different
    roses_str = "roses"
    old_water_str = "water"
    old_water_way = create_way(root_tag(), old_water_str)
    rain_str = "rain"
    old_rain_way = create_way(old_water_way, rain_str)

    x_factunit = factunit_shop(fcontext=old_water_way, fbranch=old_rain_way)
    factunits_x = {x_factunit.fcontext: x_factunit}
    x_idea = ideaunit_shop(roses_str, factunits=factunits_x)
    assert x_idea.factunits[old_water_way] is not None
    old_water_rain_factunit = x_idea.factunits[old_water_way]
    assert old_water_rain_factunit.fcontext == old_water_way
    assert old_water_rain_factunit.fbranch == old_rain_way

    # WHEN
    new_water_str = "h2o"
    new_water_way = create_way(root_tag(), new_water_str)
    assert x_idea.factunits.get(new_water_way) is None
    x_idea.find_replace_way(old_way=old_water_way, new_way=new_water_way)

    # THEN
    assert x_idea.factunits.get(old_water_way) is None
    assert x_idea.factunits.get(new_water_way) is not None
    new_water_rain_factunit = x_idea.factunits[new_water_way]
    assert new_water_rain_factunit.fcontext == new_water_way
    new_rain_way = create_way(new_water_way, rain_str)
    assert new_water_rain_factunit.fbranch == new_rain_way

    print(f"{len(x_idea.factunits)=}")
    x_factunit = x_idea.factunits.get(new_water_way)
    assert x_factunit is not None
    assert x_factunit.fcontext == new_water_way
    assert x_factunit.fbranch == new_rain_way


def test_IdeaUnit_get_obj_key_ReturnsCorrectInfo():
    # ESTABLISH
    red_str = "red"

    # WHEN
    red_idea = ideaunit_shop(red_str)

    # THEN
    assert red_idea.get_obj_key() == red_str


def test_IdeaUnit_set_bridge_CorrectlyModifiesReasonWayStrs():
    # ESTABLISH
    casa_str = "casa"
    casa_idea = ideaunit_shop(casa_str)
    casa_idea.set_parent_way("")

    # WHEN
    slash_str = "/"
    casa_idea.set_bridge(slash_str)

    # THEN
    assert casa_idea.bridge == slash_str
