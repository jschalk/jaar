from src.bud.idea import ideaunit_shop
from src.bud.reason_idea import reasonunit_shop, premiseunit_shop, factunit_shop
from src._road.road import get_default_real_id_roadnode as root_label, create_road


def test_IdeaUnit_find_replace_road_CorrectlyModifies_parent_road():
    # ESTABLISH Idea with _parent_road that will be different
    old_casa_text = "casa1"
    old_casa_road = create_road(root_label(), old_casa_text)
    bloomers_text = "bloomers"
    old_bloomers_road = create_road(old_casa_road, bloomers_text)
    roses_text = "roses"
    old_roses_road = create_road(old_bloomers_road, roses_text)
    x_idea = ideaunit_shop(roses_text, _parent_road=old_bloomers_road)
    assert create_road(x_idea._parent_road) == old_bloomers_road
    assert create_road(x_idea._parent_road, x_idea._label) == old_roses_road

    # WHEN
    new_casa = "casa2"
    new_casa_road = create_road(root_label(), new_casa)
    x_idea.find_replace_road(old_road=old_casa_road, new_road=new_casa_road)

    # THEN
    new_bloomers_road = create_road(new_casa_road, bloomers_text)
    new_roses_road = create_road(new_bloomers_road, roses_text)
    assert create_road(x_idea._parent_road) == new_bloomers_road
    assert create_road(x_idea._parent_road, x_idea._label) == new_roses_road


def test_IdeaUnit_find_replace_road_CorrectlyModifies_range_push_RoadUnits():
    # ESTABLISH Idea with range_push roadunits that will be different
    casa_text = "casa1"
    casa_road = create_road(root_label(), casa_text)
    bloomers_text = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_text)
    roses_text = "roses"
    roses_road = create_road(bloomers_road, roses_text)
    old_water_text = "water"
    old_water_road = create_road(root_label(), old_water_text)
    rain_text = "rain"
    snow_text = "snow"
    old_rain_road = create_road(old_water_road, rain_text)
    old_snow_road = create_road(old_water_road, snow_text)
    farm_text = "farm"
    farm_road = create_road(root_label(), farm_text)
    fertilizer_text = "fertilizer"
    fertilizer_road = create_road(farm_road, fertilizer_text)
    farm_road = create_road(root_label(), farm_text)
    x_idea = ideaunit_shop(roses_text, _parent_road=bloomers_road)
    x_idea.set_range_push(old_rain_road)
    x_idea.set_range_push(old_snow_road)

    assert len(x_idea._range_pushs) == 2
    assert old_rain_road in x_idea._range_pushs
    assert old_snow_road in x_idea._range_pushs

    # WHEN
    new_water_text = "h2o"
    new_water_road = create_road(root_label(), new_water_text)
    new_rain_road = create_road(new_water_road, rain_text)
    new_snow_road = create_road(new_water_road, snow_text)
    x_idea.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert len(x_idea._range_pushs) == 2
    assert new_rain_road in x_idea._range_pushs
    assert new_snow_road in x_idea._range_pushs


def test_IdeaUnit_find_replace_road_CorrectlyModifies_reasonunits():
    # ESTABLISH Idea with reason that will be different
    casa_text = "casa1"
    casa_road = create_road(root_label(), casa_text)
    bloomers_text = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_text)
    roses_text = "roses"
    roses_road = create_road(bloomers_road, roses_text)
    # reason roads
    old_water_text = "water"
    old_water_road = create_road(root_label(), old_water_text)
    rain_text = "rain"
    old_rain_road = create_road(old_water_road, rain_text)
    # create reasonunit
    premise_x = premiseunit_shop(need=old_rain_road)
    premises_x = {premise_x.need: premise_x}
    reason_x = reasonunit_shop(old_water_road, premises=premises_x)
    reasons_x = {reason_x.base: reason_x}
    x_idea = ideaunit_shop(roses_text, _reasonunits=reasons_x)
    # check asserts
    assert x_idea._reasonunits.get(old_water_road) is not None
    old_water_rain_reason = x_idea._reasonunits[old_water_road]
    assert old_water_rain_reason.base == old_water_road
    assert old_water_rain_reason.premises.get(old_rain_road) is not None
    water_rain_l_premise = old_water_rain_reason.premises[old_rain_road]
    assert water_rain_l_premise.need == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = create_road(root_label(), new_water_text)
    assert x_idea._reasonunits.get(new_water_road) is None
    x_idea.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert x_idea._reasonunits.get(old_water_road) is None
    assert x_idea._reasonunits.get(new_water_road) is not None
    new_water_rain_reason = x_idea._reasonunits[new_water_road]
    assert new_water_rain_reason.base == new_water_road
    new_rain_road = create_road(new_water_road, rain_text)
    assert new_water_rain_reason.premises.get(old_rain_road) is None
    assert new_water_rain_reason.premises.get(new_rain_road) is not None
    new_water_rain_l_premise = new_water_rain_reason.premises[new_rain_road]
    assert new_water_rain_l_premise.need == new_rain_road

    print(f"{len(x_idea._reasonunits)=}")
    reason_obj = x_idea._reasonunits.get(new_water_road)
    assert reason_obj is not None

    print(f"{len(reason_obj.premises)=}")
    premise_obj = reason_obj.premises.get(new_rain_road)
    assert premise_obj is not None
    assert premise_obj.need == new_rain_road


def test_IdeaUnit_find_replace_road_CorrectlyModifies_factunits():
    # ESTABLISH Idea with factunit that will be different
    roses_text = "roses"
    old_water_text = "water"
    old_water_road = create_road(root_label(), old_water_text)
    rain_text = "rain"
    old_rain_road = create_road(old_water_road, rain_text)

    factunit_x = factunit_shop(base=old_water_road, pick=old_rain_road)
    factunits_x = {factunit_x.base: factunit_x}
    x_idea = ideaunit_shop(roses_text, _factunits=factunits_x)
    assert x_idea._factunits[old_water_road] is not None
    old_water_rain_factunit = x_idea._factunits[old_water_road]
    assert old_water_rain_factunit.base == old_water_road
    assert old_water_rain_factunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = create_road(root_label(), new_water_text)
    assert x_idea._factunits.get(new_water_road) is None
    x_idea.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert x_idea._factunits.get(old_water_road) is None
    assert x_idea._factunits.get(new_water_road) is not None
    new_water_rain_factunit = x_idea._factunits[new_water_road]
    assert new_water_rain_factunit.base == new_water_road
    new_rain_road = create_road(new_water_road, rain_text)
    assert new_water_rain_factunit.pick == new_rain_road

    print(f"{len(x_idea._factunits)=}")
    factunit_obj = x_idea._factunits.get(new_water_road)
    assert factunit_obj is not None
    assert factunit_obj.base == new_water_road
    assert factunit_obj.pick == new_rain_road


def test_IdeaUnit_get_obj_key_ReturnsCorrectInfo():
    # ESTABLISH
    red_text = "red"

    # WHEN
    red_idea = ideaunit_shop(red_text)

    # THEN
    assert red_idea.get_obj_key() == red_text


def test_IdeaUnit_set_road_delimiter_CorrectlyModifiesReasonRoadUnits():
    # ESTABLISH
    casa_text = "casa"
    casa_idea = ideaunit_shop(casa_text)
    casa_idea.set_parent_road("")

    # WHEN
    slash_text = "/"
    casa_idea.set_road_delimiter(slash_text)

    # THEN
    assert casa_idea._road_delimiter == slash_text
