from pytest import raises as pytest_raises
from src.a01_term_logic.rope import to_rope
from src.a05_plan_logic.plan import (
    get_default_belief_label as root_label,
    planunit_shop,
)
from src.a06_owner_logic.owner import ownerunit_shop
from src.a06_owner_logic.test._util.example_owners import (
    get_ownerunit_with_4_levels_and_2reasons_2facts,
)


def test_OwnerUnit_edit_plan_label_FailsWhenPlanDoesNotExist():
    # ESTABLISH
    yao_owner = ownerunit_shop("Yao")

    casa_str = "casa"
    casa_rope = yao_owner.make_l1_rope(casa_str)
    swim_str = "swim"
    yao_owner.set_l1_plan(planunit_shop(casa_str))
    yao_owner.set_plan(planunit_shop(swim_str), parent_rope=casa_rope)

    # WHEN / THEN
    no_plan_rope = yao_owner.make_l1_rope("bees")
    with pytest_raises(Exception) as excinfo:
        yao_owner.edit_plan_label(old_rope=no_plan_rope, new_plan_label="birds")
    assert str(excinfo.value) == f"Plan old_rope='{no_plan_rope}' does not exist"


def test_OwnerUnit_edit_plan_label_RaisesErrorForLevel0PlanWhen_belief_label_isNone():
    # ESTABLISH
    yao_str = "Yao"
    yao_owner = ownerunit_shop(owner_name=yao_str)

    casa_str = "casa"
    casa_rope = yao_owner.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = yao_owner.make_rope(casa_rope, swim_str)
    yao_owner.set_l1_plan(planunit_shop(casa_str))
    yao_owner.set_plan(planunit_shop(swim_str), parent_rope=casa_rope)
    assert yao_owner.owner_name == yao_str
    assert yao_owner.planroot.plan_label == yao_owner.belief_label
    casa_plan = yao_owner.get_plan_obj(casa_rope)
    assert casa_plan.parent_rope == to_rope(yao_owner.belief_label)
    swim_plan = yao_owner.get_plan_obj(swim_rope)
    root_rope = to_rope(yao_owner.belief_label)
    assert swim_plan.parent_rope == casa_rope

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        moon_str = "moon"
        yao_owner.edit_plan_label(old_rope=root_rope, new_plan_label=moon_str)
    assert (
        str(excinfo.value)
        == f"Cannot set planroot to string different than '{yao_owner.belief_label}'"
    )

    assert yao_owner.planroot.plan_label != moon_str
    assert yao_owner.planroot.plan_label == yao_owner.belief_label


def test_OwnerUnit_edit_plan_label_RaisesErrorForLevel0When_belief_label_IsDifferent():
    # ESTABLISH
    yao_str = "Yao"
    yao_owner = ownerunit_shop(owner_name=yao_str)
    casa_str = "casa"
    casa_rope = yao_owner.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = yao_owner.make_rope(casa_rope, swim_str)
    yao_owner.set_l1_plan(planunit_shop(casa_str))
    yao_owner.set_plan(planunit_shop(swim_str), parent_rope=casa_rope)
    sun_str = "sun"
    yao_owner.belief_label = sun_str
    yao_owner.planroot.belief_label = sun_str
    assert yao_owner.owner_name == yao_str
    assert yao_owner.belief_label == sun_str
    assert yao_owner.planroot.belief_label == sun_str
    assert yao_owner.planroot.plan_label == root_label()
    casa_plan = yao_owner.get_plan_obj(casa_rope)
    assert casa_plan.parent_rope == to_rope(root_label())
    swim_plan = yao_owner.get_plan_obj(swim_rope)
    assert swim_plan.parent_rope == casa_rope

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_str = "moon"
        root_rope = to_rope(root_label())
        yao_owner.edit_plan_label(old_rope=root_rope, new_plan_label=moon_str)
    assertion_str = f"Cannot set planroot to string different than '{sun_str}'"
    assert str(excinfo.value) == assertion_str


def test_OwnerUnit_find_replace_rope_CorrectlyModifies_kids_Scenario1():
    # ESTABLISH Plan with kids that will be different
    yao_str = "Yao"
    yao_owner = ownerunit_shop(yao_str)

    old_casa_str = "casa"
    old_casa_rope = yao_owner.make_l1_rope(old_casa_str)
    bloomers_str = "bloomers"
    old_bloomers_rope = yao_owner.make_rope(old_casa_rope, bloomers_str)
    roses_str = "roses"
    old_roses_rope = yao_owner.make_rope(old_bloomers_rope, roses_str)
    red_str = "red"
    old_red_rope = yao_owner.make_rope(old_roses_rope, red_str)

    yao_owner.set_l1_plan(planunit_shop(old_casa_str))
    yao_owner.set_plan(planunit_shop(bloomers_str), parent_rope=old_casa_rope)
    yao_owner.set_plan(planunit_shop(roses_str), parent_rope=old_bloomers_rope)
    yao_owner.set_plan(planunit_shop(red_str), parent_rope=old_roses_rope)
    r_plan_roses = yao_owner.get_plan_obj(old_roses_rope)
    r_plan_bloomers = yao_owner.get_plan_obj(old_bloomers_rope)

    assert r_plan_bloomers._kids.get(roses_str)
    assert r_plan_roses.parent_rope == old_bloomers_rope
    assert r_plan_roses._kids.get(red_str)
    r_plan_red = r_plan_roses._kids.get(red_str)
    assert r_plan_red.parent_rope == old_roses_rope

    # WHEN
    new_casa_str = "casita"
    new_casa_rope = yao_owner.make_l1_rope(new_casa_str)
    yao_owner.edit_plan_label(old_rope=old_casa_rope, new_plan_label=new_casa_str)

    # THEN
    assert yao_owner.planroot._kids.get(new_casa_str) is not None
    assert yao_owner.planroot._kids.get(old_casa_str) is None

    assert r_plan_bloomers.parent_rope == new_casa_rope
    assert r_plan_bloomers._kids.get(roses_str) is not None

    r_plan_roses = r_plan_bloomers._kids.get(roses_str)
    new_bloomers_rope = yao_owner.make_rope(new_casa_rope, bloomers_str)
    assert r_plan_roses.parent_rope == new_bloomers_rope
    assert r_plan_roses._kids.get(red_str) is not None
    r_plan_red = r_plan_roses._kids.get(red_str)
    new_roses_rope = yao_owner.make_rope(new_bloomers_rope, roses_str)
    assert r_plan_red.parent_rope == new_roses_rope


def test_owner_edit_plan_label_Modifies_factunits():
    # ESTABLISH owner with factunits that will be different
    yao_str = "Yao"
    yao_owner = ownerunit_shop(yao_str)

    casa_str = "casa"
    casa_rope = yao_owner.make_l1_rope(casa_str)
    bloomers_str = "bloomers"
    bloomers_rope = yao_owner.make_rope(casa_rope, bloomers_str)
    roses_str = "roses"
    roses_rope = yao_owner.make_rope(bloomers_rope, roses_str)
    old_water_str = "water"
    old_water_rope = yao_owner.make_l1_rope(old_water_str)
    rain_str = "rain"
    old_rain_rope = yao_owner.make_rope(old_water_rope, rain_str)

    yao_owner.set_l1_plan(planunit_shop(casa_str))
    yao_owner.set_plan(planunit_shop(roses_str), parent_rope=bloomers_rope)
    yao_owner.set_plan(planunit_shop(rain_str), parent_rope=old_water_rope)
    yao_owner.add_fact(fcontext=old_water_rope, fstate=old_rain_rope)

    plan_x = yao_owner.get_plan_obj(roses_rope)
    assert yao_owner.planroot.factunits[old_water_rope] is not None
    old_water_rain_factunit = yao_owner.planroot.factunits[old_water_rope]
    assert old_water_rain_factunit.fcontext == old_water_rope
    assert old_water_rain_factunit.fstate == old_rain_rope

    # WHEN
    new_water_str = "h2o"
    new_water_rope = yao_owner.make_l1_rope(new_water_str)
    yao_owner.set_l1_plan(planunit_shop(new_water_str))
    assert yao_owner.planroot.factunits.get(new_water_rope) is None
    yao_owner.edit_plan_label(old_rope=old_water_rope, new_plan_label=new_water_str)

    # THEN
    assert yao_owner.planroot.factunits.get(old_water_rope) is None
    assert yao_owner.planroot.factunits.get(new_water_rope) is not None
    new_water_rain_factunit = yao_owner.planroot.factunits[new_water_rope]
    assert new_water_rain_factunit.fcontext == new_water_rope
    new_rain_rope = yao_owner.make_rope(new_water_rope, rain_str)
    assert new_water_rain_factunit.fstate == new_rain_rope

    assert yao_owner.planroot.factunits.get(new_water_rope)
    x_factunit = yao_owner.planroot.factunits.get(new_water_rope)
    # for factunit_key, x_factunit in yao_owner.planroot.factunits.items():
    #     assert factunit_key == new_water_rope
    assert x_factunit.fcontext == new_water_rope
    assert x_factunit.fstate == new_rain_rope


def test_owner_edit_plan_label_ModifiesPlanReasonUnitsScenario1():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels_and_2reasons_2facts()
    old_wkday_str = "wkdays"
    old_wkday_rope = sue_owner.make_l1_rope(old_wkday_str)
    wednesday_str = "Wednesday"
    old_wednesday_rope = sue_owner.make_rope(old_wkday_rope, wednesday_str)
    casa_plan = sue_owner.get_plan_obj(sue_owner.make_l1_rope("casa"))
    # casa_wk_reason = reasonunit_shop(wkday, premises={wed_premise.pstate: wed_premise})
    # nation_reason = reasonunit_shop(nation, premises={usa_premise.pstate: usa_premise})
    assert len(casa_plan.reasonunits) == 2
    assert casa_plan.reasonunits.get(old_wkday_rope) is not None
    wednesday_plan = sue_owner.get_plan_obj(old_wkday_rope)
    casa_wkday_reason = casa_plan.reasonunits.get(old_wkday_rope)
    assert casa_wkday_reason.premises.get(old_wednesday_rope) is not None
    assert (
        casa_wkday_reason.premises.get(old_wednesday_rope).pstate == old_wednesday_rope
    )
    new_wkday_str = "days of wk"
    new_wkday_rope = sue_owner.make_l1_rope(new_wkday_str)
    new_wednesday_rope = sue_owner.make_rope(new_wkday_rope, wednesday_str)
    assert casa_plan.reasonunits.get(new_wkday_str) is None

    # WHEN
    # for key_x, x_reason in casa_plan.reasonunits.items():
    #     print(f"Before {key_x=} {x_reason.rcontext=}")
    print(f"before {wednesday_plan.plan_label=}")
    print(f"before {wednesday_plan.parent_rope=}")
    sue_owner.edit_plan_label(old_rope=old_wkday_rope, new_plan_label=new_wkday_str)
    # for key_x, x_reason in casa_plan.reasonunits.items():
    #     print(f"after {key_x=} {x_reason.rcontext=}")
    print(f"after  {wednesday_plan.plan_label=}")
    print(f"after  {wednesday_plan.parent_rope=}")

    # THEN
    assert casa_plan.reasonunits.get(new_wkday_rope) is not None
    assert casa_plan.reasonunits.get(old_wkday_rope) is None
    casa_wkday_reason = casa_plan.reasonunits.get(new_wkday_rope)
    assert casa_wkday_reason.premises.get(new_wednesday_rope) is not None
    assert (
        casa_wkday_reason.premises.get(new_wednesday_rope).pstate == new_wednesday_rope
    )
    assert len(casa_plan.reasonunits) == 2


def test_owner_set_owner_name_CorrectlyModifiesBoth():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels_and_2reasons_2facts()
    assert sue_owner.owner_name == "Sue"
    assert sue_owner.planroot.plan_label == sue_owner.belief_label
    # mid_plan_label1 = "Yao"
    # sue_owner.edit_plan_label(old_rope=old_plan_label, new_plan_label=mid_plan_label1)
    # assert sue_owner.owner_name == old_plan_label
    # assert sue_owner.planroot.plan_label == mid_plan_label1

    # WHEN
    bob_str = "Bob"
    sue_owner.set_owner_name(new_owner_name=bob_str)

    # THEN
    assert sue_owner.owner_name == bob_str
    assert sue_owner.planroot.plan_label == sue_owner.belief_label


def test_owner_edit_plan_label_RaisesErrorIfknotIsInLabel():
    # ESTABLISH
    sue_owner = get_ownerunit_with_4_levels_and_2reasons_2facts()
    old_wkday_str = "wkdays"
    old_wkday_rope = sue_owner.make_l1_rope(old_wkday_str)

    # WHEN / THEN
    new_wkday_str = "days; of wk"
    with pytest_raises(Exception) as excinfo:
        sue_owner.edit_plan_label(old_rope=old_wkday_rope, new_plan_label=new_wkday_str)
    assert (
        str(excinfo.value)
        == f"Cannot modify '{old_wkday_rope}' because new_plan_label {new_wkday_str} contains knot {sue_owner.knot}"
    )
