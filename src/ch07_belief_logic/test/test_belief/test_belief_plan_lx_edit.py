from pytest import raises as pytest_raises
from src.ch01_rope_logic.rope import to_rope
from src.ch06_plan_logic.plan import (
    get_default_moment_label as root_label,
    planunit_shop,
)
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.test._util.example_beliefs import (
    get_beliefunit_with_4_levels_and_2reasons_2facts,
)


def test_BeliefUnit_edit_plan_label_FailsWhenPlanDoesNotExist():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")

    casa_str = "casa"
    casa_rope = yao_belief.make_l1_rope(casa_str)
    swim_str = "swim"
    yao_belief.set_l1_plan(planunit_shop(casa_str))
    yao_belief.set_plan(planunit_shop(swim_str), parent_rope=casa_rope)

    # WHEN / THEN
    no_plan_rope = yao_belief.make_l1_rope("bees")
    with pytest_raises(Exception) as excinfo:
        yao_belief.edit_plan_label(old_rope=no_plan_rope, new_plan_label="birds")
    assert str(excinfo.value) == f"Plan old_rope='{no_plan_rope}' does not exist"


def test_BeliefUnit_edit_plan_label_RaisesErrorForLevel0PlanWhen_moment_label_isNone():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(belief_name=yao_str)

    casa_str = "casa"
    casa_rope = yao_belief.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = yao_belief.make_rope(casa_rope, swim_str)
    yao_belief.set_l1_plan(planunit_shop(casa_str))
    yao_belief.set_plan(planunit_shop(swim_str), parent_rope=casa_rope)
    assert yao_belief.belief_name == yao_str
    assert yao_belief.planroot.plan_label == yao_belief.moment_label
    casa_plan = yao_belief.get_plan_obj(casa_rope)
    assert casa_plan.parent_rope == to_rope(yao_belief.moment_label)
    swim_plan = yao_belief.get_plan_obj(swim_rope)
    root_rope = to_rope(yao_belief.moment_label)
    assert swim_plan.parent_rope == casa_rope

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        moon_str = "moon"
        yao_belief.edit_plan_label(old_rope=root_rope, new_plan_label=moon_str)
    assert (
        str(excinfo.value)
        == f"Cannot set a root Plan to string different than '{yao_belief.moment_label}'"
    )

    assert yao_belief.planroot.plan_label != moon_str
    assert yao_belief.planroot.plan_label == yao_belief.moment_label


def test_BeliefUnit_edit_plan_label_RaisesErrorForLevel0When_moment_label_IsDifferent():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(belief_name=yao_str)
    casa_str = "casa"
    casa_rope = yao_belief.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = yao_belief.make_rope(casa_rope, swim_str)
    yao_belief.set_l1_plan(planunit_shop(casa_str))
    yao_belief.set_plan(planunit_shop(swim_str), parent_rope=casa_rope)
    sun_str = "sun"
    yao_belief.moment_label = sun_str
    yao_belief.planroot.moment_label = sun_str
    assert yao_belief.belief_name == yao_str
    assert yao_belief.moment_label == sun_str
    assert yao_belief.planroot.moment_label == sun_str
    assert yao_belief.planroot.plan_label == root_label()
    casa_plan = yao_belief.get_plan_obj(casa_rope)
    assert casa_plan.parent_rope == to_rope(root_label())
    swim_plan = yao_belief.get_plan_obj(swim_rope)
    assert swim_plan.parent_rope == casa_rope

    # WHEN
    with pytest_raises(Exception) as excinfo:
        moon_str = "moon"
        root_rope = to_rope(root_label())
        yao_belief.edit_plan_label(old_rope=root_rope, new_plan_label=moon_str)

    # THEN
    assertion_str = f"Cannot set a root Plan to string different than '{sun_str}'"
    assert str(excinfo.value) == assertion_str


def test_BeliefUnit_find_replace_rope_Modifies_kids_Scenario1():
    # ESTABLISH Plan with kids that will be different
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)

    old_casa_str = "casa"
    old_casa_rope = yao_belief.make_l1_rope(old_casa_str)
    bloomers_str = "bloomers"
    old_bloomers_rope = yao_belief.make_rope(old_casa_rope, bloomers_str)
    roses_str = "roses"
    old_roses_rope = yao_belief.make_rope(old_bloomers_rope, roses_str)
    red_str = "red"
    old_red_rope = yao_belief.make_rope(old_roses_rope, red_str)

    yao_belief.set_l1_plan(planunit_shop(old_casa_str))
    yao_belief.set_plan(planunit_shop(bloomers_str), parent_rope=old_casa_rope)
    yao_belief.set_plan(planunit_shop(roses_str), parent_rope=old_bloomers_rope)
    yao_belief.set_plan(planunit_shop(red_str), parent_rope=old_roses_rope)
    r_plan_roses = yao_belief.get_plan_obj(old_roses_rope)
    r_plan_bloomers = yao_belief.get_plan_obj(old_bloomers_rope)

    assert r_plan_bloomers.kids.get(roses_str)
    assert r_plan_roses.parent_rope == old_bloomers_rope
    assert r_plan_roses.kids.get(red_str)
    r_plan_red = r_plan_roses.kids.get(red_str)
    assert r_plan_red.parent_rope == old_roses_rope

    # WHEN
    new_casa_str = "casita"
    new_casa_rope = yao_belief.make_l1_rope(new_casa_str)
    yao_belief.edit_plan_label(old_rope=old_casa_rope, new_plan_label=new_casa_str)

    # THEN
    assert yao_belief.planroot.kids.get(new_casa_str) is not None
    assert yao_belief.planroot.kids.get(old_casa_str) is None

    assert r_plan_bloomers.parent_rope == new_casa_rope
    assert r_plan_bloomers.kids.get(roses_str) is not None

    r_plan_roses = r_plan_bloomers.kids.get(roses_str)
    new_bloomers_rope = yao_belief.make_rope(new_casa_rope, bloomers_str)
    assert r_plan_roses.parent_rope == new_bloomers_rope
    assert r_plan_roses.kids.get(red_str) is not None
    r_plan_red = r_plan_roses.kids.get(red_str)
    new_roses_rope = yao_belief.make_rope(new_bloomers_rope, roses_str)
    assert r_plan_red.parent_rope == new_roses_rope


def test_belief_edit_plan_label_Modifies_factunits():
    # ESTABLISH belief with factunits that will be different
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)

    casa_str = "casa"
    casa_rope = yao_belief.make_l1_rope(casa_str)
    bloomers_str = "bloomers"
    bloomers_rope = yao_belief.make_rope(casa_rope, bloomers_str)
    roses_str = "roses"
    roses_rope = yao_belief.make_rope(bloomers_rope, roses_str)
    old_water_str = "water"
    old_water_rope = yao_belief.make_l1_rope(old_water_str)
    rain_str = "rain"
    old_rain_rope = yao_belief.make_rope(old_water_rope, rain_str)

    yao_belief.set_l1_plan(planunit_shop(casa_str))
    yao_belief.set_plan(planunit_shop(roses_str), parent_rope=bloomers_rope)
    yao_belief.set_plan(planunit_shop(rain_str), parent_rope=old_water_rope)
    yao_belief.add_fact(fact_context=old_water_rope, fact_state=old_rain_rope)

    plan_x = yao_belief.get_plan_obj(roses_rope)
    assert yao_belief.planroot.factunits[old_water_rope] is not None
    old_water_rain_factunit = yao_belief.planroot.factunits[old_water_rope]
    assert old_water_rain_factunit.fact_context == old_water_rope
    assert old_water_rain_factunit.fact_state == old_rain_rope

    # WHEN
    new_water_str = "h2o"
    new_water_rope = yao_belief.make_l1_rope(new_water_str)
    yao_belief.set_l1_plan(planunit_shop(new_water_str))
    assert yao_belief.planroot.factunits.get(new_water_rope) is None
    yao_belief.edit_plan_label(old_rope=old_water_rope, new_plan_label=new_water_str)

    # THEN
    assert yao_belief.planroot.factunits.get(old_water_rope) is None
    assert yao_belief.planroot.factunits.get(new_water_rope) is not None
    new_water_rain_factunit = yao_belief.planroot.factunits[new_water_rope]
    assert new_water_rain_factunit.fact_context == new_water_rope
    new_rain_rope = yao_belief.make_rope(new_water_rope, rain_str)
    assert new_water_rain_factunit.fact_state == new_rain_rope

    assert yao_belief.planroot.factunits.get(new_water_rope)
    x_factunit = yao_belief.planroot.factunits.get(new_water_rope)
    # for factunit_key, x_factunit in yao_belief.planroot.factunits.items():
    #     assert factunit_key == new_water_rope
    assert x_factunit.fact_context == new_water_rope
    assert x_factunit.fact_state == new_rain_rope


def test_belief_edit_plan_label_ModifiesPlanReasonUnitsScenario1():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels_and_2reasons_2facts()
    old_sem_jour_str = "sem_jours"
    old_sem_jour_rope = sue_belief.make_l1_rope(old_sem_jour_str)
    wed_str = "Wed"
    old_wed_rope = sue_belief.make_rope(old_sem_jour_rope, wed_str)
    casa_plan = sue_belief.get_plan_obj(sue_belief.make_l1_rope("casa"))
    # casa_wk_reason = reasonunit_shop(sem_jour, cases={wed_case.reason_state: wed_case})
    # nation_reason = reasonunit_shop(nation, cases={usa_case.reason_state: usa_case})
    assert len(casa_plan.reasonunits) == 2
    assert casa_plan.reasonunits.get(old_sem_jour_rope) is not None
    wed_plan = sue_belief.get_plan_obj(old_sem_jour_rope)
    casa_sem_jour_reason = casa_plan.reasonunits.get(old_sem_jour_rope)
    assert casa_sem_jour_reason.cases.get(old_wed_rope) is not None
    assert casa_sem_jour_reason.cases.get(old_wed_rope).reason_state == old_wed_rope
    new_sem_jour_str = "jours des sem"
    new_sem_jour_rope = sue_belief.make_l1_rope(new_sem_jour_str)
    new_wed_rope = sue_belief.make_rope(new_sem_jour_rope, wed_str)
    assert casa_plan.reasonunits.get(new_sem_jour_str) is None

    # WHEN
    # for key_x, x_reason in casa_plan.reasonunits.items():
    #     print(f"Before {key_x=} {x_reason.reason_context=}")
    print(f"before {wed_plan.plan_label=}")
    print(f"before {wed_plan.parent_rope=}")
    sue_belief.edit_plan_label(
        old_rope=old_sem_jour_rope, new_plan_label=new_sem_jour_str
    )
    # for key_x, x_reason in casa_plan.reasonunits.items():
    #     print(f"after {key_x=} {x_reason.reason_context=}")
    print(f"after  {wed_plan.plan_label=}")
    print(f"after  {wed_plan.parent_rope=}")

    # THEN
    assert casa_plan.reasonunits.get(new_sem_jour_rope) is not None
    assert casa_plan.reasonunits.get(old_sem_jour_rope) is None
    casa_sem_jour_reason = casa_plan.reasonunits.get(new_sem_jour_rope)
    assert casa_sem_jour_reason.cases.get(new_wed_rope) is not None
    assert casa_sem_jour_reason.cases.get(new_wed_rope).reason_state == new_wed_rope
    assert len(casa_plan.reasonunits) == 2


def test_belief_set_belief_name_ModifiesBoth():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels_and_2reasons_2facts()
    assert sue_belief.belief_name == "Sue"
    assert sue_belief.planroot.plan_label == sue_belief.moment_label
    # mid_plan_label1 = "Yao"
    # sue_belief.edit_plan_label(old_rope=old_plan_label, new_plan_label=mid_plan_label1)
    # assert sue_belief.belief_name == old_plan_label
    # assert sue_belief.planroot.plan_label == mid_plan_label1

    # WHEN
    bob_str = "Bob"
    sue_belief.set_belief_name(new_belief_name=bob_str)

    # THEN
    assert sue_belief.belief_name == bob_str
    assert sue_belief.planroot.plan_label == sue_belief.moment_label


def test_belief_edit_plan_label_RaisesErrorIfknotIsInLabel():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels_and_2reasons_2facts()
    old_sem_jour_str = "sem_jours"
    old_sem_jour_rope = sue_belief.make_l1_rope(old_sem_jour_str)

    # WHEN / THEN
    new_sem_jour_str = "jours; des wk"
    with pytest_raises(Exception) as excinfo:
        sue_belief.edit_plan_label(
            old_rope=old_sem_jour_rope, new_plan_label=new_sem_jour_str
        )
    assert (
        str(excinfo.value)
        == f"Cannot modify '{old_sem_jour_rope}' because new_plan_label {new_sem_jour_str} contains knot {sue_belief.knot}"
    )
