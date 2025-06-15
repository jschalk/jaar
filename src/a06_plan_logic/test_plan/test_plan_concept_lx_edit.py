from pytest import raises as pytest_raises
from src.a01_term_logic.rope import to_rope
from src.a05_concept_logic.concept import (
    conceptunit_shop,
    get_default_vow_label as root_label,
)
from src.a06_plan_logic._test_util.example_plans import (
    get_planunit_with_4_levels_and_2reasons_2facts,
)
from src.a06_plan_logic.plan import planunit_shop


def test_PlanUnit_edit_concept_label_FailsWhenConceptDoesNotExist():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")

    casa_str = "casa"
    casa_rope = yao_plan.make_l1_rope(casa_str)
    swim_str = "swim"
    yao_plan.set_l1_concept(conceptunit_shop(casa_str))
    yao_plan.set_concept(conceptunit_shop(swim_str), parent_rope=casa_rope)

    # WHEN / THEN
    no_concept_rope = yao_plan.make_l1_rope("bees")
    with pytest_raises(Exception) as excinfo:
        yao_plan.edit_concept_label(old_rope=no_concept_rope, new_concept_label="birds")
    assert str(excinfo.value) == f"Concept old_rope='{no_concept_rope}' does not exist"


def test_PlanUnit_edit_concept_label_RaisesErrorForLevel0ConceptWhen_vow_label_isNone():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(owner_name=yao_str)

    casa_str = "casa"
    casa_rope = yao_plan.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = yao_plan.make_rope(casa_rope, swim_str)
    yao_plan.set_l1_concept(conceptunit_shop(casa_str))
    yao_plan.set_concept(conceptunit_shop(swim_str), parent_rope=casa_rope)
    assert yao_plan.owner_name == yao_str
    assert yao_plan.conceptroot.concept_label == yao_plan.vow_label
    casa_concept = yao_plan.get_concept_obj(casa_rope)
    assert casa_concept.parent_rope == to_rope(yao_plan.vow_label)
    swim_concept = yao_plan.get_concept_obj(swim_rope)
    root_rope = to_rope(yao_plan.vow_label)
    assert swim_concept.parent_rope == casa_rope

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        moon_str = "moon"
        yao_plan.edit_concept_label(old_rope=root_rope, new_concept_label=moon_str)
    assert (
        str(excinfo.value)
        == f"Cannot set conceptroot to string different than '{yao_plan.vow_label}'"
    )

    assert yao_plan.conceptroot.concept_label != moon_str
    assert yao_plan.conceptroot.concept_label == yao_plan.vow_label


def test_PlanUnit_edit_concept_label_RaisesErrorForLevel0When_vow_label_IsDifferent():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(owner_name=yao_str)
    casa_str = "casa"
    casa_rope = yao_plan.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = yao_plan.make_rope(casa_rope, swim_str)
    yao_plan.set_l1_concept(conceptunit_shop(casa_str))
    yao_plan.set_concept(conceptunit_shop(swim_str), parent_rope=casa_rope)
    sun_str = "sun"
    yao_plan.vow_label = sun_str
    yao_plan.conceptroot.vow_label = sun_str
    assert yao_plan.owner_name == yao_str
    assert yao_plan.vow_label == sun_str
    assert yao_plan.conceptroot.vow_label == sun_str
    assert yao_plan.conceptroot.concept_label == root_label()
    casa_concept = yao_plan.get_concept_obj(casa_rope)
    assert casa_concept.parent_rope == to_rope(root_label())
    swim_concept = yao_plan.get_concept_obj(swim_rope)
    assert swim_concept.parent_rope == casa_rope

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_str = "moon"
        root_rope = to_rope(root_label())
        yao_plan.edit_concept_label(old_rope=root_rope, new_concept_label=moon_str)
    assertion_str = f"Cannot set conceptroot to string different than '{sun_str}'"
    assert str(excinfo.value) == assertion_str


def test_PlanUnit_find_replace_rope_CorrectlyModifies_kids_Scenario1():
    # ESTABLISH Concept with kids that will be different
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)

    old_casa_str = "casa"
    old_casa_rope = yao_plan.make_l1_rope(old_casa_str)
    bloomers_str = "bloomers"
    old_bloomers_rope = yao_plan.make_rope(old_casa_rope, bloomers_str)
    roses_str = "roses"
    old_roses_rope = yao_plan.make_rope(old_bloomers_rope, roses_str)
    red_str = "red"
    old_red_rope = yao_plan.make_rope(old_roses_rope, red_str)

    yao_plan.set_l1_concept(conceptunit_shop(old_casa_str))
    yao_plan.set_concept(conceptunit_shop(bloomers_str), parent_rope=old_casa_rope)
    yao_plan.set_concept(conceptunit_shop(roses_str), parent_rope=old_bloomers_rope)
    yao_plan.set_concept(conceptunit_shop(red_str), parent_rope=old_roses_rope)
    r_concept_roses = yao_plan.get_concept_obj(old_roses_rope)
    r_concept_bloomers = yao_plan.get_concept_obj(old_bloomers_rope)

    assert r_concept_bloomers._kids.get(roses_str)
    assert r_concept_roses.parent_rope == old_bloomers_rope
    assert r_concept_roses._kids.get(red_str)
    r_concept_red = r_concept_roses._kids.get(red_str)
    assert r_concept_red.parent_rope == old_roses_rope

    # WHEN
    new_casa_str = "casita"
    new_casa_rope = yao_plan.make_l1_rope(new_casa_str)
    yao_plan.edit_concept_label(old_rope=old_casa_rope, new_concept_label=new_casa_str)

    # THEN
    assert yao_plan.conceptroot._kids.get(new_casa_str) is not None
    assert yao_plan.conceptroot._kids.get(old_casa_str) is None

    assert r_concept_bloomers.parent_rope == new_casa_rope
    assert r_concept_bloomers._kids.get(roses_str) is not None

    r_concept_roses = r_concept_bloomers._kids.get(roses_str)
    new_bloomers_rope = yao_plan.make_rope(new_casa_rope, bloomers_str)
    assert r_concept_roses.parent_rope == new_bloomers_rope
    assert r_concept_roses._kids.get(red_str) is not None
    r_concept_red = r_concept_roses._kids.get(red_str)
    new_roses_rope = yao_plan.make_rope(new_bloomers_rope, roses_str)
    assert r_concept_red.parent_rope == new_roses_rope


def test_plan_edit_concept_label_Modifies_factunits():
    # ESTABLISH plan with factunits that will be different
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)

    casa_str = "casa"
    casa_rope = yao_plan.make_l1_rope(casa_str)
    bloomers_str = "bloomers"
    bloomers_rope = yao_plan.make_rope(casa_rope, bloomers_str)
    roses_str = "roses"
    roses_rope = yao_plan.make_rope(bloomers_rope, roses_str)
    old_water_str = "water"
    old_water_rope = yao_plan.make_l1_rope(old_water_str)
    rain_str = "rain"
    old_rain_rope = yao_plan.make_rope(old_water_rope, rain_str)

    yao_plan.set_l1_concept(conceptunit_shop(casa_str))
    yao_plan.set_concept(conceptunit_shop(roses_str), parent_rope=bloomers_rope)
    yao_plan.set_concept(conceptunit_shop(rain_str), parent_rope=old_water_rope)
    yao_plan.add_fact(fcontext=old_water_rope, fstate=old_rain_rope)

    concept_x = yao_plan.get_concept_obj(roses_rope)
    assert yao_plan.conceptroot.factunits[old_water_rope] is not None
    old_water_rain_factunit = yao_plan.conceptroot.factunits[old_water_rope]
    assert old_water_rain_factunit.fcontext == old_water_rope
    assert old_water_rain_factunit.fstate == old_rain_rope

    # WHEN
    new_water_str = "h2o"
    new_water_rope = yao_plan.make_l1_rope(new_water_str)
    yao_plan.set_l1_concept(conceptunit_shop(new_water_str))
    assert yao_plan.conceptroot.factunits.get(new_water_rope) is None
    yao_plan.edit_concept_label(
        old_rope=old_water_rope, new_concept_label=new_water_str
    )

    # THEN
    assert yao_plan.conceptroot.factunits.get(old_water_rope) is None
    assert yao_plan.conceptroot.factunits.get(new_water_rope) is not None
    new_water_rain_factunit = yao_plan.conceptroot.factunits[new_water_rope]
    assert new_water_rain_factunit.fcontext == new_water_rope
    new_rain_rope = yao_plan.make_rope(new_water_rope, rain_str)
    assert new_water_rain_factunit.fstate == new_rain_rope

    assert yao_plan.conceptroot.factunits.get(new_water_rope)
    x_factunit = yao_plan.conceptroot.factunits.get(new_water_rope)
    # for factunit_key, x_factunit in yao_plan.conceptroot.factunits.items():
    #     assert factunit_key == new_water_rope
    assert x_factunit.fcontext == new_water_rope
    assert x_factunit.fstate == new_rain_rope


def test_plan_edit_concept_label_ModifiesConceptReasonUnitsScenario1():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels_and_2reasons_2facts()
    old_wkday_str = "wkdays"
    old_wkday_rope = sue_plan.make_l1_rope(old_wkday_str)
    wednesday_str = "Wednesday"
    old_wednesday_rope = sue_plan.make_rope(old_wkday_rope, wednesday_str)
    casa_concept = sue_plan.get_concept_obj(sue_plan.make_l1_rope("casa"))
    # casa_wk_reason = reasonunit_shop(wkday, premises={wed_premise.pstate: wed_premise})
    # nation_reason = reasonunit_shop(nation, premises={usa_premise.pstate: usa_premise})
    assert len(casa_concept.reasonunits) == 2
    assert casa_concept.reasonunits.get(old_wkday_rope) is not None
    wednesday_concept = sue_plan.get_concept_obj(old_wkday_rope)
    casa_wkday_reason = casa_concept.reasonunits.get(old_wkday_rope)
    assert casa_wkday_reason.premises.get(old_wednesday_rope) is not None
    assert (
        casa_wkday_reason.premises.get(old_wednesday_rope).pstate == old_wednesday_rope
    )
    new_wkday_str = "days of wk"
    new_wkday_rope = sue_plan.make_l1_rope(new_wkday_str)
    new_wednesday_rope = sue_plan.make_rope(new_wkday_rope, wednesday_str)
    assert casa_concept.reasonunits.get(new_wkday_str) is None

    # WHEN
    # for key_x, x_reason in casa_concept.reasonunits.items():
    #     print(f"Before {key_x=} {x_reason.rcontext=}")
    print(f"before {wednesday_concept.concept_label=}")
    print(f"before {wednesday_concept.parent_rope=}")
    sue_plan.edit_concept_label(
        old_rope=old_wkday_rope, new_concept_label=new_wkday_str
    )
    # for key_x, x_reason in casa_concept.reasonunits.items():
    #     print(f"after {key_x=} {x_reason.rcontext=}")
    print(f"after  {wednesday_concept.concept_label=}")
    print(f"after  {wednesday_concept.parent_rope=}")

    # THEN
    assert casa_concept.reasonunits.get(new_wkday_rope) is not None
    assert casa_concept.reasonunits.get(old_wkday_rope) is None
    casa_wkday_reason = casa_concept.reasonunits.get(new_wkday_rope)
    assert casa_wkday_reason.premises.get(new_wednesday_rope) is not None
    assert (
        casa_wkday_reason.premises.get(new_wednesday_rope).pstate == new_wednesday_rope
    )
    assert len(casa_concept.reasonunits) == 2


def test_plan_set_owner_name_CorrectlyModifiesBoth():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels_and_2reasons_2facts()
    assert sue_plan.owner_name == "Sue"
    assert sue_plan.conceptroot.concept_label == sue_plan.vow_label
    # mid_concept_label1 = "Yao"
    # sue_plan.edit_concept_label(old_rope=old_concept_label, new_concept_label=mid_concept_label1)
    # assert sue_plan.owner_name == old_concept_label
    # assert sue_plan.conceptroot.concept_label == mid_concept_label1

    # WHEN
    bob_str = "Bob"
    sue_plan.set_owner_name(new_owner_name=bob_str)

    # THEN
    assert sue_plan.owner_name == bob_str
    assert sue_plan.conceptroot.concept_label == sue_plan.vow_label


def test_plan_edit_concept_label_RaisesErrorIfknotIsInLabel():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels_and_2reasons_2facts()
    old_wkday_str = "wkdays"
    old_wkday_rope = sue_plan.make_l1_rope(old_wkday_str)

    # WHEN / THEN
    new_wkday_str = "days; of wk"
    with pytest_raises(Exception) as excinfo:
        sue_plan.edit_concept_label(
            old_rope=old_wkday_rope, new_concept_label=new_wkday_str
        )
    assert (
        str(excinfo.value)
        == f"Cannot modify '{old_wkday_rope}' because new_concept_label {new_wkday_str} contains knot {sue_plan.knot}"
    )
