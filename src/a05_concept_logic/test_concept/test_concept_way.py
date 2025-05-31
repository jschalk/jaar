from src.a01_term_logic.way import create_way
from src.a01_term_logic.way import get_default_fisc_label as root_label
from src.a04_reason_logic.reason_concept import (
    factunit_shop,
    premiseunit_shop,
    reasonunit_shop,
)
from src.a05_concept_logic.concept import conceptunit_shop


def test_ConceptUnit_find_replace_way_CorrectlyModifies_parent_way():
    # ESTABLISH Concept with _parent_way that will be different
    old_casa_str = "casa1"
    old_casa_way = create_way(root_label(), old_casa_str)
    bloomers_str = "bloomers"
    old_bloomers_way = create_way(old_casa_way, bloomers_str)
    roses_str = "roses"
    old_roses_way = create_way(old_bloomers_way, roses_str)
    x_concept = conceptunit_shop(roses_str, parent_way=old_bloomers_way)
    assert create_way(x_concept.parent_way) == old_bloomers_way
    assert create_way(x_concept.parent_way, x_concept.concept_label) == old_roses_way

    # WHEN
    new_casa = "casa2"
    new_casa_way = create_way(root_label(), new_casa)
    x_concept.find_replace_way(old_way=old_casa_way, new_way=new_casa_way)

    # THEN
    new_bloomers_way = create_way(new_casa_way, bloomers_str)
    new_roses_way = create_way(new_bloomers_way, roses_str)
    assert create_way(x_concept.parent_way) == new_bloomers_way
    assert create_way(x_concept.parent_way, x_concept.concept_label) == new_roses_way


def test_ConceptUnit_find_replace_way_CorrectlyModifies_reasonunits():
    # ESTABLISH Concept with reason that will be different
    casa_str = "casa1"
    casa_way = create_way(root_label(), casa_str)
    bloomers_str = "bloomers"
    bloomers_way = create_way(casa_way, bloomers_str)
    roses_str = "roses"
    roses_way = create_way(bloomers_way, roses_str)
    # reason ways
    old_water_str = "water"
    old_water_way = create_way(root_label(), old_water_str)
    rain_str = "rain"
    old_rain_way = create_way(old_water_way, rain_str)
    # create reasonunit
    premise_x = premiseunit_shop(pstate=old_rain_way)
    premises_x = {premise_x.pstate: premise_x}
    x_reason = reasonunit_shop(old_water_way, premises=premises_x)
    reasons_x = {x_reason.rcontext: x_reason}
    x_concept = conceptunit_shop(roses_str, reasonunits=reasons_x)
    # check asserts
    assert x_concept.reasonunits.get(old_water_way) is not None
    old_water_rain_reason = x_concept.reasonunits[old_water_way]
    assert old_water_rain_reason.rcontext == old_water_way
    assert old_water_rain_reason.premises.get(old_rain_way) is not None
    water_rain_l_premise = old_water_rain_reason.premises[old_rain_way]
    assert water_rain_l_premise.pstate == old_rain_way

    # WHEN
    new_water_str = "h2o"
    new_water_way = create_way(root_label(), new_water_str)
    assert x_concept.reasonunits.get(new_water_way) is None
    x_concept.find_replace_way(old_way=old_water_way, new_way=new_water_way)

    # THEN
    assert x_concept.reasonunits.get(old_water_way) is None
    assert x_concept.reasonunits.get(new_water_way) is not None
    new_water_rain_reason = x_concept.reasonunits[new_water_way]
    assert new_water_rain_reason.rcontext == new_water_way
    new_rain_way = create_way(new_water_way, rain_str)
    assert new_water_rain_reason.premises.get(old_rain_way) is None
    assert new_water_rain_reason.premises.get(new_rain_way) is not None
    new_water_rain_l_premise = new_water_rain_reason.premises[new_rain_way]
    assert new_water_rain_l_premise.pstate == new_rain_way

    print(f"{len(x_concept.reasonunits)=}")
    reason_obj = x_concept.reasonunits.get(new_water_way)
    assert reason_obj is not None

    print(f"{len(reason_obj.premises)=}")
    premise_obj = reason_obj.premises.get(new_rain_way)
    assert premise_obj is not None
    assert premise_obj.pstate == new_rain_way


def test_ConceptUnit_find_replace_way_CorrectlyModifies_factunits():
    # ESTABLISH Concept with factunit that will be different
    roses_str = "roses"
    old_water_str = "water"
    old_water_way = create_way(root_label(), old_water_str)
    rain_str = "rain"
    old_rain_way = create_way(old_water_way, rain_str)

    x_factunit = factunit_shop(fcontext=old_water_way, fstate=old_rain_way)
    factunits_x = {x_factunit.fcontext: x_factunit}
    x_concept = conceptunit_shop(roses_str, factunits=factunits_x)
    assert x_concept.factunits[old_water_way] is not None
    old_water_rain_factunit = x_concept.factunits[old_water_way]
    assert old_water_rain_factunit.fcontext == old_water_way
    assert old_water_rain_factunit.fstate == old_rain_way

    # WHEN
    new_water_str = "h2o"
    new_water_way = create_way(root_label(), new_water_str)
    assert x_concept.factunits.get(new_water_way) is None
    x_concept.find_replace_way(old_way=old_water_way, new_way=new_water_way)

    # THEN
    assert x_concept.factunits.get(old_water_way) is None
    assert x_concept.factunits.get(new_water_way) is not None
    new_water_rain_factunit = x_concept.factunits[new_water_way]
    assert new_water_rain_factunit.fcontext == new_water_way
    new_rain_way = create_way(new_water_way, rain_str)
    assert new_water_rain_factunit.fstate == new_rain_way

    print(f"{len(x_concept.factunits)=}")
    x_factunit = x_concept.factunits.get(new_water_way)
    assert x_factunit is not None
    assert x_factunit.fcontext == new_water_way
    assert x_factunit.fstate == new_rain_way


def test_ConceptUnit_get_obj_key_ReturnsCorrectInfo():
    # ESTABLISH
    red_str = "red"

    # WHEN
    red_concept = conceptunit_shop(red_str)

    # THEN
    assert red_concept.get_obj_key() == red_str


def test_ConceptUnit_set_bridge_CorrectlyModifiesReasonWayTerms():
    # ESTABLISH
    casa_str = "casa"
    casa_concept = conceptunit_shop(casa_str)
    casa_concept.set_parent_way("")

    # WHEN
    slash_str = "/"
    casa_concept.set_bridge(slash_str)

    # THEN
    assert casa_concept.bridge == slash_str
