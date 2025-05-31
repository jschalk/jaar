from pytest import raises as pytest_raises
from src.a01_term_logic.way import (
    get_default_fisc_way,
    to_way,
)
from src.a01_term_logic.way import get_default_fisc_label as root_label
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic._test_util.example_buds import (
    get_budunit_with_4_levels_and_2reasons_2facts,
)
from src.a06_bud_logic.bud import budunit_shop


def test_BudUnit_edit_concept_label_FailsWhenConceptDoesNotExist():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")

    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    swim_str = "swim"
    yao_bud.set_l1_concept(conceptunit_shop(casa_str))
    yao_bud.set_concept(conceptunit_shop(swim_str), parent_way=casa_way)

    # WHEN / THEN
    no_concept_way = yao_bud.make_l1_way("bees")
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_concept_label(old_way=no_concept_way, new_concept_label="birds")
    assert str(excinfo.value) == f"Concept old_way='{no_concept_way}' does not exist"


def test_BudUnit_edit_concept_label_RaisesErrorForLevel0ConceptWhen_fisc_label_isNone():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(owner_name=yao_str)

    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    swim_str = "swim"
    swim_way = yao_bud.make_way(casa_way, swim_str)
    yao_bud.set_l1_concept(conceptunit_shop(casa_str))
    yao_bud.set_concept(conceptunit_shop(swim_str), parent_way=casa_way)
    assert yao_bud.owner_name == yao_str
    assert yao_bud.conceptroot.concept_label == yao_bud.fisc_label
    casa_concept = yao_bud.get_concept_obj(casa_way)
    assert casa_concept.parent_way == to_way(yao_bud.fisc_label)
    swim_concept = yao_bud.get_concept_obj(swim_way)
    root_way = to_way(yao_bud.fisc_label)
    assert swim_concept.parent_way == casa_way

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        moon_str = "moon"
        yao_bud.edit_concept_label(old_way=root_way, new_concept_label=moon_str)
    assert (
        str(excinfo.value)
        == f"Cannot set conceptroot to string different than '{yao_bud.fisc_label}'"
    )

    assert yao_bud.conceptroot.concept_label != moon_str
    assert yao_bud.conceptroot.concept_label == yao_bud.fisc_label


def test_BudUnit_edit_concept_label_RaisesErrorForLevel0When_fisc_label_IsDifferent():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(owner_name=yao_str)
    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    swim_str = "swim"
    swim_way = yao_bud.make_way(casa_way, swim_str)
    yao_bud.set_l1_concept(conceptunit_shop(casa_str))
    yao_bud.set_concept(conceptunit_shop(swim_str), parent_way=casa_way)
    sun_str = "sun"
    yao_bud.fisc_label = sun_str
    yao_bud.conceptroot.fisc_label = sun_str
    assert yao_bud.owner_name == yao_str
    assert yao_bud.fisc_label == sun_str
    assert yao_bud.conceptroot.fisc_label == sun_str
    assert yao_bud.conceptroot.concept_label == root_label()
    casa_concept = yao_bud.get_concept_obj(casa_way)
    assert casa_concept.parent_way == get_default_fisc_way()
    swim_concept = yao_bud.get_concept_obj(swim_way)
    assert swim_concept.parent_way == casa_way

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_str = "moon"
        yao_bud.edit_concept_label(
            old_way=get_default_fisc_way(), new_concept_label=moon_str
        )
    assert (
        str(excinfo.value)
        == f"Cannot set conceptroot to string different than '{sun_str}'"
    )


def test_BudUnit_find_replace_way_CorrectlyModifies_kids_Scenario1():
    # ESTABLISH Concept with kids that will be different
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)

    old_casa_str = "casa"
    old_casa_way = yao_bud.make_l1_way(old_casa_str)
    bloomers_str = "bloomers"
    old_bloomers_way = yao_bud.make_way(old_casa_way, bloomers_str)
    roses_str = "roses"
    old_roses_way = yao_bud.make_way(old_bloomers_way, roses_str)
    red_str = "red"
    old_red_way = yao_bud.make_way(old_roses_way, red_str)

    yao_bud.set_l1_concept(conceptunit_shop(old_casa_str))
    yao_bud.set_concept(conceptunit_shop(bloomers_str), parent_way=old_casa_way)
    yao_bud.set_concept(conceptunit_shop(roses_str), parent_way=old_bloomers_way)
    yao_bud.set_concept(conceptunit_shop(red_str), parent_way=old_roses_way)
    r_concept_roses = yao_bud.get_concept_obj(old_roses_way)
    r_concept_bloomers = yao_bud.get_concept_obj(old_bloomers_way)

    assert r_concept_bloomers._kids.get(roses_str) is not None
    assert r_concept_roses.parent_way == old_bloomers_way
    assert r_concept_roses._kids.get(red_str) is not None
    r_concept_red = r_concept_roses._kids.get(red_str)
    assert r_concept_red.parent_way == old_roses_way

    # WHEN
    new_casa_str = "casita"
    new_casa_way = yao_bud.make_l1_way(new_casa_str)
    yao_bud.edit_concept_label(old_way=old_casa_way, new_concept_label=new_casa_str)

    # THEN
    assert yao_bud.conceptroot._kids.get(new_casa_str) is not None
    assert yao_bud.conceptroot._kids.get(old_casa_str) is None

    assert r_concept_bloomers.parent_way == new_casa_way
    assert r_concept_bloomers._kids.get(roses_str) is not None

    r_concept_roses = r_concept_bloomers._kids.get(roses_str)
    new_bloomers_way = yao_bud.make_way(new_casa_way, bloomers_str)
    assert r_concept_roses.parent_way == new_bloomers_way
    assert r_concept_roses._kids.get(red_str) is not None
    r_concept_red = r_concept_roses._kids.get(red_str)
    new_roses_way = yao_bud.make_way(new_bloomers_way, roses_str)
    assert r_concept_red.parent_way == new_roses_way


def test_bud_edit_concept_label_Modifies_factunits():
    # ESTABLISH bud with factunits that will be different
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)

    casa_str = "casa"
    casa_way = yao_bud.make_l1_way(casa_str)
    bloomers_str = "bloomers"
    bloomers_way = yao_bud.make_way(casa_way, bloomers_str)
    roses_str = "roses"
    roses_way = yao_bud.make_way(bloomers_way, roses_str)
    old_water_str = "water"
    old_water_way = yao_bud.make_l1_way(old_water_str)
    rain_str = "rain"
    old_rain_way = yao_bud.make_way(old_water_way, rain_str)

    yao_bud.set_l1_concept(conceptunit_shop(casa_str))
    yao_bud.set_concept(conceptunit_shop(roses_str), parent_way=bloomers_way)
    yao_bud.set_concept(conceptunit_shop(rain_str), parent_way=old_water_way)
    yao_bud.add_fact(fcontext=old_water_way, fstate=old_rain_way)

    concept_x = yao_bud.get_concept_obj(roses_way)
    assert yao_bud.conceptroot.factunits[old_water_way] is not None
    old_water_rain_factunit = yao_bud.conceptroot.factunits[old_water_way]
    assert old_water_rain_factunit.fcontext == old_water_way
    assert old_water_rain_factunit.fstate == old_rain_way

    # WHEN
    new_water_str = "h2o"
    new_water_way = yao_bud.make_l1_way(new_water_str)
    yao_bud.set_l1_concept(conceptunit_shop(new_water_str))
    assert yao_bud.conceptroot.factunits.get(new_water_way) is None
    yao_bud.edit_concept_label(old_way=old_water_way, new_concept_label=new_water_str)

    # THEN
    assert yao_bud.conceptroot.factunits.get(old_water_way) is None
    assert yao_bud.conceptroot.factunits.get(new_water_way) is not None
    new_water_rain_factunit = yao_bud.conceptroot.factunits[new_water_way]
    assert new_water_rain_factunit.fcontext == new_water_way
    new_rain_way = yao_bud.make_way(new_water_way, rain_str)
    assert new_water_rain_factunit.fstate == new_rain_way

    assert yao_bud.conceptroot.factunits.get(new_water_way)
    x_factunit = yao_bud.conceptroot.factunits.get(new_water_way)
    # for factunit_key, x_factunit in yao_bud.conceptroot.factunits.items():
    #     assert factunit_key == new_water_way
    assert x_factunit.fcontext == new_water_way
    assert x_factunit.fstate == new_rain_way


def test_bud_edit_concept_label_ModifiesConceptReasonUnitsScenario1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()
    old_wkday_str = "wkdays"
    old_wkday_way = sue_bud.make_l1_way(old_wkday_str)
    wednesday_str = "Wednesday"
    old_wednesday_way = sue_bud.make_way(old_wkday_way, wednesday_str)
    casa_concept = sue_bud.get_concept_obj(sue_bud.make_l1_way("casa"))
    # casa_wk_reason = reasonunit_shop(wkday, premises={wed_premise.pstate: wed_premise})
    # nation_reason = reasonunit_shop(nation, premises={usa_premise.pstate: usa_premise})
    assert len(casa_concept.reasonunits) == 2
    assert casa_concept.reasonunits.get(old_wkday_way) is not None
    wednesday_concept = sue_bud.get_concept_obj(old_wkday_way)
    casa_wkday_reason = casa_concept.reasonunits.get(old_wkday_way)
    assert casa_wkday_reason.premises.get(old_wednesday_way) is not None
    assert casa_wkday_reason.premises.get(old_wednesday_way).pstate == old_wednesday_way
    new_wkday_str = "days of wk"
    new_wkday_way = sue_bud.make_l1_way(new_wkday_str)
    new_wednesday_way = sue_bud.make_way(new_wkday_way, wednesday_str)
    assert casa_concept.reasonunits.get(new_wkday_str) is None

    # WHEN
    # for key_x, x_reason in casa_concept.reasonunits.items():
    #     print(f"Before {key_x=} {x_reason.rcontext=}")
    print(f"before {wednesday_concept.concept_label=}")
    print(f"before {wednesday_concept.parent_way=}")
    sue_bud.edit_concept_label(old_way=old_wkday_way, new_concept_label=new_wkday_str)
    # for key_x, x_reason in casa_concept.reasonunits.items():
    #     print(f"after {key_x=} {x_reason.rcontext=}")
    print(f"after  {wednesday_concept.concept_label=}")
    print(f"after  {wednesday_concept.parent_way=}")

    # THEN
    assert casa_concept.reasonunits.get(new_wkday_way) is not None
    assert casa_concept.reasonunits.get(old_wkday_way) is None
    casa_wkday_reason = casa_concept.reasonunits.get(new_wkday_way)
    assert casa_wkday_reason.premises.get(new_wednesday_way) is not None
    assert casa_wkday_reason.premises.get(new_wednesday_way).pstate == new_wednesday_way
    assert len(casa_concept.reasonunits) == 2


def test_bud_set_owner_name_CorrectlyModifiesBoth():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()
    assert sue_bud.owner_name == "Sue"
    assert sue_bud.conceptroot.concept_label == sue_bud.fisc_label
    # mid_concept_label1 = "Yao"
    # sue_bud.edit_concept_label(old_way=old_concept_label, new_concept_label=mid_concept_label1)
    # assert sue_bud.owner_name == old_concept_label
    # assert sue_bud.conceptroot.concept_label == mid_concept_label1

    # WHEN
    bob_str = "Bob"
    sue_bud.set_owner_name(new_owner_name=bob_str)

    # THEN
    assert sue_bud.owner_name == bob_str
    assert sue_bud.conceptroot.concept_label == sue_bud.fisc_label


def test_bud_edit_concept_label_RaisesErrorIfbridgeIsInLabel():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels_and_2reasons_2facts()
    old_wkday_str = "wkdays"
    old_wkday_way = sue_bud.make_l1_way(old_wkday_str)

    # WHEN / THEN
    new_wkday_str = "days; of wk"
    with pytest_raises(Exception) as excinfo:
        sue_bud.edit_concept_label(
            old_way=old_wkday_way, new_concept_label=new_wkday_str
        )
    assert (
        str(excinfo.value)
        == f"Cannot modify '{old_wkday_way}' because new_concept_label {new_wkday_str} contains bridge {sue_bud.bridge}"
    )
