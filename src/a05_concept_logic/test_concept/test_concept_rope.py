from src.a01_term_logic.rope import create_rope
from src.a04_reason_logic.reason_concept import (
    factunit_shop,
    premiseunit_shop,
    reasonunit_shop,
)
from src.a05_concept_logic.concept import conceptunit_shop


def test_ConceptUnit_find_replace_rope_CorrectlyModifies_parent_rope():
    # ESTABLISH Concept with _parent_rope that will be different
    old_casa_str = "casa1"
    old_root_label = "ZZ"
    old_casa_rope = create_rope(old_root_label, old_casa_str)
    bloomers_str = "bloomers"
    old_bloomers_rope = create_rope(old_casa_rope, bloomers_str)
    roses_str = "roses"
    old_roses_rope = create_rope(old_bloomers_rope, roses_str)
    x_concept = conceptunit_shop(roses_str, parent_rope=old_bloomers_rope)
    assert create_rope(x_concept.parent_rope) == old_bloomers_rope
    assert create_rope(x_concept.parent_rope, x_concept.concept_label) == old_roses_rope

    # WHEN
    new_casa = "casa2"
    new_casa_rope = create_rope(old_root_label, new_casa)
    x_concept.find_replace_rope(old_rope=old_casa_rope, new_rope=new_casa_rope)

    # THEN
    new_bloomers_rope = create_rope(new_casa_rope, bloomers_str)
    new_roses_rope = create_rope(new_bloomers_rope, roses_str)
    assert create_rope(x_concept.parent_rope) == new_bloomers_rope
    assert create_rope(x_concept.parent_rope, x_concept.concept_label) == new_roses_rope


def test_ConceptUnit_find_replace_rope_CorrectlyModifies_reasonunits():
    # ESTABLISH Concept with reason that will be different
    casa_str = "casa1"
    old_root_label = "ZZ"
    casa_rope = create_rope(old_root_label, casa_str)
    bloomers_str = "bloomers"
    bloomers_rope = create_rope(casa_rope, bloomers_str)
    roses_str = "roses"
    roses_rope = create_rope(bloomers_rope, roses_str)
    # reason ropes
    old_water_str = "water"
    old_water_rope = create_rope(old_root_label, old_water_str)
    rain_str = "rain"
    old_rain_rope = create_rope(old_water_rope, rain_str)
    # create reasonunit
    premise_x = premiseunit_shop(pstate=old_rain_rope)
    premises_x = {premise_x.pstate: premise_x}
    x_reason = reasonunit_shop(old_water_rope, premises=premises_x)
    reasons_x = {x_reason.rcontext: x_reason}
    x_concept = conceptunit_shop(roses_str, reasonunits=reasons_x)
    # check asserts
    assert x_concept.reasonunits.get(old_water_rope) is not None
    old_water_rain_reason = x_concept.reasonunits[old_water_rope]
    assert old_water_rain_reason.rcontext == old_water_rope
    assert old_water_rain_reason.premises.get(old_rain_rope) is not None
    water_rain_l_premise = old_water_rain_reason.premises[old_rain_rope]
    assert water_rain_l_premise.pstate == old_rain_rope

    # WHEN
    new_water_str = "h2o"
    new_water_rope = create_rope(old_root_label, new_water_str)
    assert x_concept.reasonunits.get(new_water_rope) is None
    x_concept.find_replace_rope(old_rope=old_water_rope, new_rope=new_water_rope)

    # THEN
    assert x_concept.reasonunits.get(old_water_rope) is None
    assert x_concept.reasonunits.get(new_water_rope) is not None
    new_water_rain_reason = x_concept.reasonunits[new_water_rope]
    assert new_water_rain_reason.rcontext == new_water_rope
    new_rain_rope = create_rope(new_water_rope, rain_str)
    assert new_water_rain_reason.premises.get(old_rain_rope) is None
    assert new_water_rain_reason.premises.get(new_rain_rope) is not None
    new_water_rain_l_premise = new_water_rain_reason.premises[new_rain_rope]
    assert new_water_rain_l_premise.pstate == new_rain_rope

    print(f"{len(x_concept.reasonunits)=}")
    reason_obj = x_concept.reasonunits.get(new_water_rope)
    assert reason_obj is not None

    print(f"{len(reason_obj.premises)=}")
    premise_obj = reason_obj.premises.get(new_rain_rope)
    assert premise_obj is not None
    assert premise_obj.pstate == new_rain_rope


def test_ConceptUnit_find_replace_rope_CorrectlyModifies_factunits():
    # ESTABLISH Concept with factunit that will be different
    roses_str = "roses"
    old_water_str = "water"
    old_root_label = "ZZ"
    old_water_rope = create_rope(old_root_label, old_water_str)
    rain_str = "rain"
    old_rain_rope = create_rope(old_water_rope, rain_str)

    x_factunit = factunit_shop(fcontext=old_water_rope, fstate=old_rain_rope)
    factunits_x = {x_factunit.fcontext: x_factunit}
    x_concept = conceptunit_shop(roses_str, factunits=factunits_x)
    assert x_concept.factunits[old_water_rope] is not None
    old_water_rain_factunit = x_concept.factunits[old_water_rope]
    assert old_water_rain_factunit.fcontext == old_water_rope
    assert old_water_rain_factunit.fstate == old_rain_rope

    # WHEN
    new_water_str = "h2o"
    new_water_rope = create_rope(old_root_label, new_water_str)
    assert x_concept.factunits.get(new_water_rope) is None
    x_concept.find_replace_rope(old_rope=old_water_rope, new_rope=new_water_rope)

    # THEN
    assert x_concept.factunits.get(old_water_rope) is None
    assert x_concept.factunits.get(new_water_rope) is not None
    new_water_rain_factunit = x_concept.factunits[new_water_rope]
    assert new_water_rain_factunit.fcontext == new_water_rope
    new_rain_rope = create_rope(new_water_rope, rain_str)
    assert new_water_rain_factunit.fstate == new_rain_rope

    print(f"{len(x_concept.factunits)=}")
    x_factunit = x_concept.factunits.get(new_water_rope)
    assert x_factunit is not None
    assert x_factunit.fcontext == new_water_rope
    assert x_factunit.fstate == new_rain_rope


def test_ConceptUnit_get_obj_key_ReturnsCorrectInfo():
    # ESTABLISH
    red_str = "red"

    # WHEN
    red_concept = conceptunit_shop(red_str)

    # THEN
    assert red_concept.get_obj_key() == red_str


def test_ConceptUnit_set_knot_CorrectlyModifiesReasonRopeTerms():
    # ESTABLISH
    casa_str = "casa"
    casa_concept = conceptunit_shop(casa_str)
    casa_concept.set_parent_rope("")

    # WHEN
    slash_str = "/"
    casa_concept.set_knot(slash_str)

    # THEN
    assert casa_concept.knot == slash_str
