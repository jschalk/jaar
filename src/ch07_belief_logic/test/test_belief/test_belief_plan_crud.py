from pytest import raises as pytest_raises
from src.ch03_voice.group import awardunit_shop
from src.ch03_voice.labor import laborunit_shop
from src.ch04_rope.rope import create_rope, default_knot_if_None, is_sub_rope, to_rope
from src.ch05_reason.reason import caseunit_shop, factunit_shop, reasonunit_shop
from src.ch06_plan.healer import healerunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch07_belief_logic.test._util.ch07_examples import get_beliefunit_with_4_levels


def test_BeliefUnit_set_plan_ScenarioXX_RaisesErrorWhen_parent_rope_IsInvalid():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia")
    invalid_rootlabel_swim_rope = create_rope("swimming")
    casa_str = "casa"
    casa_plan = planunit_shop(casa_str)
    assert invalid_rootlabel_swim_rope != zia_belief.planroot.get_plan_rope()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_belief.set_plan_obj(casa_plan, parent_rope=invalid_rootlabel_swim_rope)
    exception_str = f"set_plan failed because parent_rope '{invalid_rootlabel_swim_rope}' has an invalid root rope. Should be {zia_belief.planroot.get_plan_rope()}."
    assert str(excinfo.value) == exception_str


def test_BeliefUnit_set_plan_ScenarioXX_RaisesErrorWhen_parent_rope_PlanDoesNotExist():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia")
    swim_rope = zia_belief.make_l1_rope("swimming")
    casa_str = "casa"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_belief.set_plan_obj(
            planunit_shop(casa_str),
            parent_rope=swim_rope,
            create_missing_ancestors=False,
        )
    exception_str = f"set_plan failed because '{swim_rope}' plan does not exist."
    assert str(excinfo.value) == exception_str


def test_BeliefUnit_set_plan_ScenarioXX_RaisesErrorWhen_plan_label_IsNotLabel():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia")
    swim_rope = zia_belief.make_l1_rope("swimming")
    casa_str = "casa"
    casa_rope = zia_belief.make_l1_rope(casa_str)
    run_str = "run"
    run_rope = zia_belief.make_rope(casa_rope, run_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_belief.set_plan_obj(planunit_shop(run_rope), parent_rope=swim_rope)
    exception_str = f"set_plan failed because '{run_rope}' is not a LabelTerm."
    assert str(excinfo.value) == exception_str


def test_BeliefUnit_set_plan_ScenarioXX_SetsAttr():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia")
    casa_str = "casa"
    root_plan_rope = zia_belief.planroot.get_plan_rope()
    assert not zia_belief.planroot.kids.get(casa_str)

    # WHEN
    zia_belief.set_plan_obj(planunit_shop(casa_str), parent_rope=root_plan_rope)

    # THEN
    print(f"{zia_belief.planroot.kids.keys()=}")
    assert zia_belief.planroot.kids.get(casa_str)


def test_BeliefUnit_plan_exists_ReturnsObj():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia")
    casa_str = "casa"
    casa_rope = zia_belief.make_l1_rope(casa_str)
    assert zia_belief.plan_exists(casa_rope) is False

    # WHEN
    zia_belief.set_plan_obj(
        planunit_shop(casa_str), parent_rope=zia_belief.planroot.get_plan_rope()
    )

    # THEN
    assert zia_belief.plan_exists(casa_rope)


def test_BeliefUnit_set_l1_plan_SetsAttr():
    # ESTABLISH
    zia_belief = beliefunit_shop("Zia")
    casa_str = "casa"
    casa_rope = zia_belief.make_l1_rope(casa_str)
    assert not zia_belief.planroot.kids.get(casa_rope)

    # WHEN
    zia_belief.set_l1_plan(planunit_shop(casa_str))

    # THEN
    assert not zia_belief.planroot.kids.get(casa_rope)


def test_BeliefUnit_add_plan_SetsAttr_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    slash_str = "/"
    bob_beliefunit = beliefunit_shop(bob_str, knot=slash_str)
    casa_rope = bob_beliefunit.make_l1_rope("casa")
    assert not bob_beliefunit.plan_exists(casa_rope)

    # WHEN
    bob_beliefunit.add_plan(casa_rope)

    # THEN
    assert bob_beliefunit.plan_exists(casa_rope)
    casa_planunit = bob_beliefunit.get_plan_obj(casa_rope)
    assert casa_planunit.knot == bob_beliefunit.knot
    assert not casa_planunit.pledge


def test_BeliefUnit_add_plan_SetsAttr_Scenario1():
    # ESTABLISH
    bob_str = "Bob"
    bob_beliefunit = beliefunit_shop(bob_str)
    casa_rope = bob_beliefunit.make_l1_rope("casa")
    casa_star = 13
    casa_pledge = True

    # WHEN
    bob_beliefunit.add_plan(casa_rope, star=casa_star, pledge=casa_pledge)

    # THEN
    casa_planunit = bob_beliefunit.get_plan_obj(casa_rope)
    assert casa_planunit.star == casa_star
    assert casa_planunit.pledge


def test_BeliefUnit_add_plan_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_beliefunit = beliefunit_shop(bob_str)
    casa_rope = bob_beliefunit.make_l1_rope("casa")
    casa_star = 13

    # WHEN
    casa_planunit = bob_beliefunit.add_plan(casa_rope, star=casa_star)

    # THEN
    assert casa_planunit.plan_label == "casa"
    assert casa_planunit.star == casa_star


def test_BeliefUnit_set_plan_ScenarioXX_AddsPlanObjWithNonDefault_knot():
    # ESTABLISH
    slash_str = "/"
    assert slash_str != default_knot_if_None()
    bob_belief = beliefunit_shop("Bob", knot=slash_str)
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wed"
    casa_rope = bob_belief.make_l1_rope(casa_str)
    wk_rope = bob_belief.make_l1_rope(wk_str)
    wed_rope = bob_belief.make_rope(wk_rope, wed_str)
    bob_belief.set_l1_plan(planunit_shop(casa_str))
    bob_belief.set_l1_plan(planunit_shop(wk_str))
    bob_belief.set_plan_obj(planunit_shop(wed_str), wk_rope)
    print(f"{bob_belief.planroot.kids.keys()=}")
    assert len(bob_belief.planroot.kids) == 2
    wed_plan = bob_belief.get_plan_obj(wed_rope)
    assert wed_plan.knot == slash_str
    assert wed_plan.knot == bob_belief.knot

    # WHEN
    bob_belief.edit_plan_attr(casa_rope, reason_context=wk_rope, reason_case=wed_rope)

    # THEN
    casa_plan = bob_belief.get_plan_obj(casa_rope)
    assert casa_plan.reasonunits.get(wk_rope) is not None


def test_BeliefUnit_set_plan_ScenarioXX_CanCreateMissingPlanUnits():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    ww2_rope = sue_belief.make_l1_rope("ww2")
    battles_rope = sue_belief.make_rope(ww2_rope, "battles")
    coralsea_rope = sue_belief.make_rope(battles_rope, "coralsea")
    saratoga_plan = planunit_shop("USS Saratoga")
    assert sue_belief.plan_exists(battles_rope) is False
    assert sue_belief.plan_exists(coralsea_rope) is False

    # WHEN
    sue_belief.set_plan_obj(saratoga_plan, parent_rope=coralsea_rope)

    # THEN
    assert sue_belief.plan_exists(battles_rope)
    assert sue_belief.plan_exists(coralsea_rope)


def test_BeliefUnit_del_plan_obj_Level0CannotBeDeleted():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    root_rope = sue_belief.planroot.get_plan_rope()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_belief.del_plan_obj(rope=root_rope)
    assert str(excinfo.value) == "Planroot cannot be deleted"


def test_BeliefUnit_del_plan_obj_Level1CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    wk_str = "sem_jours"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    sun_str = "Sun"
    sun_rope = sue_belief.make_rope(wk_rope, sun_str)
    assert sue_belief.get_plan_obj(wk_rope)
    assert sue_belief.get_plan_obj(sun_rope)

    # WHEN
    sue_belief.del_plan_obj(rope=wk_rope)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_belief.get_plan_obj(wk_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{wk_rope}'"
    new_sun_rope = sue_belief.make_l1_rope("Sun")
    with pytest_raises(Exception) as excinfo:
        sue_belief.get_plan_obj(new_sun_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{new_sun_rope}'"


def test_BeliefUnit_del_plan_obj_Level1CanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    wk_str = "sem_jours"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    sun_str = "Sun"
    old_sun_rope = sue_belief.make_rope(wk_rope, sun_str)
    assert sue_belief.get_plan_obj(old_sun_rope)

    # WHEN
    sue_belief.del_plan_obj(rope=wk_rope, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_belief.get_plan_obj(old_sun_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{old_sun_rope}'"
    new_sun_rope = sue_belief.make_l1_rope(sun_str)
    assert sue_belief.get_plan_obj(new_sun_rope)
    new_sun_plan = sue_belief.get_plan_obj(new_sun_rope)
    assert new_sun_plan.parent_rope == sue_belief.planroot.get_plan_rope()


def test_BeliefUnit_del_plan_obj_LevelNCanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    nation_str = "nation"
    nation_rope = sue_belief.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_belief.make_rope(nation_rope, usa_str)
    texas_str = "Texas"
    oregon_str = "Oregon"
    usa_texas_rope = sue_belief.make_rope(usa_rope, texas_str)
    usa_oregon_rope = sue_belief.make_rope(usa_rope, oregon_str)
    nation_texas_rope = sue_belief.make_rope(nation_rope, texas_str)
    nation_oregon_rope = sue_belief.make_rope(nation_rope, oregon_str)
    assert sue_belief.plan_exists(usa_rope)
    assert sue_belief.plan_exists(usa_texas_rope)
    assert sue_belief.plan_exists(usa_oregon_rope)
    assert sue_belief.plan_exists(nation_texas_rope) is False
    assert sue_belief.plan_exists(nation_oregon_rope) is False

    # WHEN
    sue_belief.del_plan_obj(rope=usa_rope, del_children=False)

    # THEN
    assert sue_belief.plan_exists(nation_texas_rope)
    assert sue_belief.plan_exists(nation_oregon_rope)
    assert sue_belief.plan_exists(usa_texas_rope) is False
    assert sue_belief.plan_exists(usa_oregon_rope) is False
    assert sue_belief.plan_exists(usa_rope) is False


def test_BeliefUnit_del_plan_obj_Level2CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    sem_jour_rope = sue_belief.make_l1_rope("sem_jours")
    mon_rope = sue_belief.make_rope(sem_jour_rope, "Mon")
    assert sue_belief.get_plan_obj(mon_rope)

    # WHEN
    sue_belief.del_plan_obj(rope=mon_rope)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_belief.get_plan_obj(mon_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{mon_rope}'"


def test_BeliefUnit_del_plan_obj_LevelNCanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    nation_str = "nation"
    nation_rope = sue_belief.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_belief.make_rope(nation_rope, usa_str)
    texas_str = "Texas"
    usa_texas_rope = sue_belief.make_rope(usa_rope, texas_str)
    assert sue_belief.get_plan_obj(usa_texas_rope)

    # WHEN
    sue_belief.del_plan_obj(rope=usa_texas_rope)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_belief.get_plan_obj(usa_texas_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{usa_texas_rope}'"


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario00_Star():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    print(f"{casa_rope=}")
    old_star = sue_belief.planroot.kids[casa_str].star
    assert old_star == 30

    # WHEN
    sue_belief.edit_plan_attr(casa_rope, star=23)

    # THEN
    new_star = sue_belief.planroot.kids[casa_str].star
    assert new_star == 23


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario01_uid():
    # ESTABLISH:
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    # uid: int = None,
    sue_belief.planroot.kids[casa_str].uid = 34
    x_uid = sue_belief.planroot.kids[casa_str].uid
    assert x_uid == 34

    # WHEN
    sue_belief.edit_plan_attr(casa_rope, uid=23)

    # THEN
    uid_new = sue_belief.planroot.kids[casa_str].uid
    assert uid_new == 23


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario02_begin_close():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    # begin: float = None,
    # close: float = None,
    sue_belief.planroot.kids[casa_str].begin = 39
    x_begin = sue_belief.planroot.kids[casa_str].begin
    assert x_begin == 39

    # WHEN
    sue_belief.planroot.kids[casa_str].close = 43

    # THEN
    x_close = sue_belief.planroot.kids[casa_str].close
    assert x_close == 43

    # WHEN
    sue_belief.edit_plan_attr(casa_rope, begin=25, close=29)

    # THEN
    assert sue_belief.planroot.kids[casa_str].begin == 25
    assert sue_belief.planroot.kids[casa_str].close == 29


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario03_gogo_want_stop_want():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    # gogo_want: float = None,
    # stop_want: float = None,
    sue_belief.planroot.kids[casa_str].gogo_want = 439
    x_gogo_want = sue_belief.planroot.kids[casa_str].gogo_want
    assert x_gogo_want == 439

    # WHEN
    sue_belief.planroot.kids[casa_str].stop_want = 443

    # THEN
    x_stop_want = sue_belief.planroot.kids[casa_str].stop_want
    assert x_stop_want == 443

    # WHEN
    sue_belief.edit_plan_attr(casa_rope, gogo_want=425, stop_want=429)

    # THEN
    assert sue_belief.planroot.kids[casa_str].gogo_want == 425
    assert sue_belief.planroot.kids[casa_str].stop_want == 429


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario04_factunits():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    # factunit: factunit_shop = None,
    # sue_belief.planroot.kids[casa_str].factunits = None
    assert sue_belief.planroot.kids[casa_str].factunits == {}
    sem_jours_rope = sue_belief.make_l1_rope("sem_jours")
    fact_rope = sue_belief.make_rope(sem_jours_rope, "Sun")
    x_factunit = factunit_shop(fact_context=fact_rope, fact_state=fact_rope)

    casa_factunits = sue_belief.planroot.kids[casa_str].factunits
    print(f"{casa_factunits=}")

    # WHEN
    sue_belief.edit_plan_attr(casa_rope, factunit=x_factunit)
    casa_factunits = sue_belief.planroot.kids[casa_str].factunits
    print(f"{casa_factunits=}")

    # THEN
    assert sue_belief.planroot.kids[casa_str].factunits == {
        x_factunit.fact_context: x_factunit
    }


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario05_awardunit():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    # awardunit: dict = None,
    sue_belief.planroot.kids[casa_str].awardunits = {
        "fun": awardunit_shop(awardee_title="fun", give_force=1, take_force=7)
    }
    awardunits = sue_belief.planroot.kids[casa_str].awardunits
    assert awardunits == {
        "fun": awardunit_shop(awardee_title="fun", give_force=1, take_force=7)
    }
    x_awardunit = awardunit_shop(awardee_title="fun", give_force=4, take_force=8)

    # WHEN
    sue_belief.edit_plan_attr(casa_rope, awardunit=x_awardunit)

    # THEN
    assert sue_belief.planroot.kids[casa_str].awardunits == {"fun": x_awardunit}


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario06_is_expanded():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    # is_expanded: dict = None,
    sue_belief.planroot.kids[casa_str].is_expanded = "what"
    is_expanded = sue_belief.planroot.kids[casa_str].is_expanded
    assert is_expanded == "what"

    # WHEN
    sue_belief.edit_plan_attr(casa_rope, is_expanded=True)

    # THEN
    assert sue_belief.planroot.kids[casa_str].is_expanded is True


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario07_pledge():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    # pledge: dict = None,
    sue_belief.planroot.kids[casa_str].pledge = "funfun3"
    pledge = sue_belief.planroot.kids[casa_str].pledge
    assert pledge == "funfun3"

    # WHEN
    sue_belief.edit_plan_attr(casa_rope, pledge=True)

    # THEN
    assert sue_belief.planroot.kids[casa_str].pledge is True


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario08_healerunit():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    # healerunit:
    sue_belief.planroot.kids[casa_str].healerunit = "fun3rol"
    src_healerunit = sue_belief.planroot.kids[casa_str].healerunit
    assert src_healerunit == "fun3rol"
    sue_str = "Sue"
    yao_str = "Yao"

    # WHEN
    x_healerunit = healerunit_shop({sue_str, yao_str})
    sue_belief.add_voiceunit(sue_str)
    sue_belief.add_voiceunit(yao_str)
    sue_belief.edit_plan_attr(casa_rope, healerunit=x_healerunit)

    # THEN
    assert sue_belief.planroot.kids[casa_str].healerunit == x_healerunit


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario09_problem_bool():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    # _problem_bool: bool
    sue_belief.planroot.kids[casa_str].problem_bool = "fun3rol"
    src_problem_bool = sue_belief.planroot.kids[casa_str].problem_bool
    assert src_problem_bool == "fun3rol"
    x_problem_bool = True

    # WHEN
    sue_belief.edit_plan_attr(casa_rope, problem_bool=x_problem_bool)

    # THEN
    assert sue_belief.planroot.kids[casa_str].problem_bool == x_problem_bool


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario10_laborunit():
    # ESTABLISH
    xio_belief = beliefunit_shop("Xio")
    run_str = "run"
    run_rope = xio_belief.make_l1_rope(run_str)
    xio_belief.set_l1_plan(planunit_shop(run_str))
    run_plan = xio_belief.get_plan_obj(run_rope)
    sue_str = "Sue"
    sue_laborunit = laborunit_shop()
    sue_laborunit.add_party(sue_str)
    assert run_plan.laborunit == laborunit_shop()

    # WHEN
    xio_belief.edit_plan_attr(run_rope, laborunit=sue_laborunit)

    # THEN
    assert run_plan.laborunit == sue_laborunit


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario11_reasonunit():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    sem_jour_str = "sem_jours"
    sem_jour_rope = sue_belief.make_l1_rope(sem_jour_str)
    wed_str = "Wed"
    wed_rope = sue_belief.make_rope(sem_jour_rope, wed_str)

    wed_case = caseunit_shop(reason_state=wed_rope)
    casa_wk_reason = reasonunit_shop(sem_jour_rope, {wed_case.reason_state: wed_case})
    print(f"{type(casa_wk_reason.reason_context)=}")
    print(f"{casa_wk_reason.reason_context=}")

    # WHEN
    sue_belief.edit_plan_attr(casa_rope, reason=casa_wk_reason)

    # THEN
    casa_plan = sue_belief.get_plan_obj(casa_rope)
    assert casa_plan.reasonunits is not None
    print(casa_plan.reasonunits)
    assert casa_plan.reasonunits[sem_jour_rope] is not None
    assert casa_plan.reasonunits[sem_jour_rope] == casa_wk_reason


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario12_reasonunit_knot():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    casa_rope = sue_belief.make_l1_rope("casa")
    wk_rope = sue_belief.make_l1_rope("sem_jours")
    wed_rope = sue_belief.make_rope(wk_rope, "Wed")

    slash_str = "/"
    before_wk_reason = reasonunit_shop(wk_rope, knot=slash_str)
    before_wk_reason.set_case(wed_rope)
    assert before_wk_reason.knot == slash_str

    # WHEN
    sue_belief.edit_plan_attr(casa_rope, reason=before_wk_reason)

    # THEN
    casa_plan = sue_belief.get_plan_obj(casa_rope)
    wk_reasonunit = casa_plan.reasonunits.get(wk_rope)
    assert wk_reasonunit.knot != slash_str
    assert wk_reasonunit.knot == sue_belief.knot


def test_BeliefUnit_edit_plan_attr_SetNestedPlanUnitAttr_Scenario13_reason_context_knot():
    # ESTABLISH
    slash_str = "/"
    bob_belief = beliefunit_shop("Bob", knot=slash_str)
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wed"
    casa_rope = bob_belief.make_l1_rope(casa_str)
    wk_rope = bob_belief.make_l1_rope(wk_str)
    wed_rope = bob_belief.make_rope(wk_rope, wed_str)
    bob_belief.set_l1_plan(planunit_shop(casa_str))
    bob_belief.set_l1_plan(planunit_shop(wk_str))
    bob_belief.set_plan_obj(planunit_shop(wed_str), wk_rope)
    print(f"{bob_belief.planroot.kids.keys()=}")
    wed_plan = bob_belief.get_plan_obj(wed_rope)
    assert wed_plan.knot == slash_str
    assert wed_plan.knot == bob_belief.knot

    # WHEN
    bob_belief.edit_plan_attr(casa_rope, reason_context=wk_rope, reason_case=wed_rope)

    # THEN
    casa_plan = bob_belief.get_plan_obj(casa_rope)
    assert casa_plan.knot == slash_str
    wk_reasonunit = casa_plan.reasonunits.get(wk_rope)
    assert wk_reasonunit.knot != ","
    assert wk_reasonunit.knot == bob_belief.knot


def test_BeliefUnit_edit_plan_attr_RaisesError_SetNestedPlanUnitAttr_Scenario13_reason_context_knot():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob")
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wed"
    casa_rope = bob_belief.make_l1_rope(casa_str)
    wk_rope = bob_belief.make_l1_rope(wk_str)
    incorrect_wed_rope = bob_belief.make_l1_rope(wed_str)
    assert not is_sub_rope(wk_rope, incorrect_wed_rope)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_belief.edit_plan_attr(
            casa_rope, reason_context=wk_rope, reason_case=incorrect_wed_rope
        )
    exception_str = f"""Plan cannot edit reason because reason_case is not sub_rope to reason_context 
reason_context: {wk_rope}
reason_case:    {incorrect_wed_rope}"""
    assert str(excinfo.value) == exception_str


def test_BeliefUnit_edit_plan_attr_RaisesError_Scenario15_When_healerunit_healer_names_DoNotExist():
    # ESTABLISH
    yao_belief = beliefunit_shop("Yao")
    casa_str = "casa"
    casa_rope = yao_belief.make_l1_rope(casa_str)
    yao_belief.set_l1_plan(planunit_shop(casa_str))
    jour_str = "jour_range"
    jour_plan = planunit_shop(jour_str, begin=44, close=110)
    yao_belief.set_l1_plan(jour_plan)

    casa_plan = yao_belief.get_plan_obj(casa_rope)
    assert casa_plan.begin is None
    assert casa_plan.close is None

    # WHEN / THEN
    sue_str = "Sue"
    x_healerunit = healerunit_shop({sue_str})
    with pytest_raises(Exception) as excinfo:
        yao_belief.edit_plan_attr(casa_rope, healerunit=x_healerunit)
    exception_str = f"Plan cannot edit healerunit because group_title '{sue_str}' does not exist as group in Belief"
    assert str(excinfo.value) == exception_str


def test_BeliefUnit_set_plan_ScenarioXX_MustReorderKidsDictToBeAlphabetical():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob")
    casa_str = "casa"
    bob_belief.set_l1_plan(planunit_shop(casa_str))
    swim_str = "swim"
    bob_belief.set_l1_plan(planunit_shop(swim_str))

    # WHEN
    plan_list = list(bob_belief.planroot.kids.values())

    # THEN
    assert plan_list[0].plan_label == casa_str


def test_BeliefUnit_set_plan_ScenarioXX_adoptee_RaisesErrorIfAdopteePlanDoesNotHaveParent():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_belief.make_l1_rope(sports_str)
    bob_belief.set_l1_plan(planunit_shop(sports_str))
    swim_str = "swim"
    bob_belief.set_plan_obj(planunit_shop(swim_str), parent_rope=sports_rope)

    # WHEN / THEN
    summer_str = "summer"
    hike_str = "hike"
    hike_rope = bob_belief.make_rope(sports_rope, hike_str)
    with pytest_raises(Exception) as excinfo:
        bob_belief.set_plan_obj(
            plan_kid=planunit_shop(summer_str),
            parent_rope=sports_rope,
            adoptees=[swim_str, hike_str],
        )
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{hike_rope}'"


def test_BeliefUnit_set_plan_ScenarioXX_adoptee_AddsAdoptee():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_belief.make_l1_rope(sports_str)
    bob_belief.set_l1_plan(planunit_shop(sports_str))
    swim_str = "swim"
    bob_belief.set_plan_obj(planunit_shop(swim_str), parent_rope=sports_rope)
    hike_str = "hike"
    bob_belief.set_plan_obj(planunit_shop(hike_str), parent_rope=sports_rope)

    sports_swim_rope = bob_belief.make_rope(sports_rope, swim_str)
    sports_hike_rope = bob_belief.make_rope(sports_rope, hike_str)
    assert bob_belief.plan_exists(sports_swim_rope)
    assert bob_belief.plan_exists(sports_hike_rope)
    summer_str = "summer"
    summer_rope = bob_belief.make_rope(sports_rope, summer_str)
    summer_swim_rope = bob_belief.make_rope(summer_rope, swim_str)
    summer_hike_rope = bob_belief.make_rope(summer_rope, hike_str)
    assert bob_belief.plan_exists(summer_swim_rope) is False
    assert bob_belief.plan_exists(summer_hike_rope) is False

    # WHEN / THEN
    bob_belief.set_plan_obj(
        plan_kid=planunit_shop(summer_str),
        parent_rope=sports_rope,
        adoptees=[swim_str, hike_str],
    )

    # THEN
    summer_plan = bob_belief.get_plan_obj(summer_rope)
    print(f"{summer_plan.kids.keys()=}")
    assert bob_belief.plan_exists(summer_swim_rope)
    assert bob_belief.plan_exists(summer_hike_rope)
    assert bob_belief.plan_exists(sports_swim_rope) is False
    assert bob_belief.plan_exists(sports_hike_rope) is False


def test_BeliefUnit_set_plan_ScenarioXX_bundling_SetsNewParentWithstarEqualToSumOfAdoptedPlans():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_belief.make_l1_rope(sports_str)
    bob_belief.set_l1_plan(planunit_shop(sports_str, star=2))
    swim_str = "swim"
    swim_star = 3
    bob_belief.set_plan_obj(planunit_shop(swim_str, star=swim_star), sports_rope)
    hike_str = "hike"
    hike_star = 5
    bob_belief.set_plan_obj(planunit_shop(hike_str, star=hike_star), sports_rope)
    bball_str = "bball"
    bball_star = 7
    bob_belief.set_plan_obj(planunit_shop(bball_str, star=bball_star), sports_rope)

    sports_swim_rope = bob_belief.make_rope(sports_rope, swim_str)
    sports_hike_rope = bob_belief.make_rope(sports_rope, hike_str)
    sports_bball_rope = bob_belief.make_rope(sports_rope, bball_str)
    assert bob_belief.get_plan_obj(sports_swim_rope).star == swim_star
    assert bob_belief.get_plan_obj(sports_hike_rope).star == hike_star
    assert bob_belief.get_plan_obj(sports_bball_rope).star == bball_star
    summer_str = "summer"
    summer_rope = bob_belief.make_rope(sports_rope, summer_str)
    summer_swim_rope = bob_belief.make_rope(summer_rope, swim_str)
    summer_hike_rope = bob_belief.make_rope(summer_rope, hike_str)
    summer_bball_rope = bob_belief.make_rope(summer_rope, bball_str)
    assert bob_belief.plan_exists(summer_swim_rope) is False
    assert bob_belief.plan_exists(summer_hike_rope) is False
    assert bob_belief.plan_exists(summer_bball_rope) is False

    # WHEN / THEN
    bob_belief.set_plan_obj(
        plan_kid=planunit_shop(summer_str),
        parent_rope=sports_rope,
        adoptees=[swim_str, hike_str],
        bundling=True,
    )

    # THEN
    assert bob_belief.get_plan_obj(summer_rope).star == swim_star + hike_star
    assert bob_belief.get_plan_obj(summer_swim_rope).star == swim_star
    assert bob_belief.get_plan_obj(summer_hike_rope).star == hike_star
    assert bob_belief.plan_exists(summer_bball_rope) is False
    assert bob_belief.plan_exists(sports_swim_rope) is False
    assert bob_belief.plan_exists(sports_hike_rope) is False
    assert bob_belief.plan_exists(sports_bball_rope)


def test_BeliefUnit_del_plan_obj_DeletingBundledPlanReturnsPlansToOriginalState():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_belief.make_l1_rope(sports_str)
    bob_belief.set_l1_plan(planunit_shop(sports_str, star=2))
    swim_str = "swim"
    swim_star = 3
    bob_belief.set_plan_obj(planunit_shop(swim_str, star=swim_star), sports_rope)
    hike_str = "hike"
    hike_star = 5
    bob_belief.set_plan_obj(planunit_shop(hike_str, star=hike_star), sports_rope)
    bball_str = "bball"
    bball_star = 7
    bob_belief.set_plan_obj(planunit_shop(bball_str, star=bball_star), sports_rope)

    sports_swim_rope = bob_belief.make_rope(sports_rope, swim_str)
    sports_hike_rope = bob_belief.make_rope(sports_rope, hike_str)
    sports_bball_rope = bob_belief.make_rope(sports_rope, bball_str)
    assert bob_belief.get_plan_obj(sports_swim_rope).star == swim_star
    assert bob_belief.get_plan_obj(sports_hike_rope).star == hike_star
    assert bob_belief.get_plan_obj(sports_bball_rope).star == bball_star
    summer_str = "summer"
    summer_rope = bob_belief.make_rope(sports_rope, summer_str)
    summer_swim_rope = bob_belief.make_rope(summer_rope, swim_str)
    summer_hike_rope = bob_belief.make_rope(summer_rope, hike_str)
    summer_bball_rope = bob_belief.make_rope(summer_rope, bball_str)
    assert bob_belief.plan_exists(summer_swim_rope) is False
    assert bob_belief.plan_exists(summer_hike_rope) is False
    assert bob_belief.plan_exists(summer_bball_rope) is False
    bob_belief.set_plan_obj(
        plan_kid=planunit_shop(summer_str),
        parent_rope=sports_rope,
        adoptees=[swim_str, hike_str],
        bundling=True,
    )
    assert bob_belief.get_plan_obj(summer_rope).star == swim_star + hike_star
    assert bob_belief.get_plan_obj(summer_swim_rope).star == swim_star
    assert bob_belief.get_plan_obj(summer_hike_rope).star == hike_star
    assert bob_belief.plan_exists(summer_bball_rope) is False
    assert bob_belief.plan_exists(sports_swim_rope) is False
    assert bob_belief.plan_exists(sports_hike_rope) is False
    assert bob_belief.plan_exists(sports_bball_rope)
    print(f"{bob_belief._plan_dict.keys()=}")

    # WHEN
    bob_belief.del_plan_obj(rope=summer_rope, del_children=False)

    # THEN
    sports_swim_plan = bob_belief.get_plan_obj(sports_swim_rope)
    sports_hike_plan = bob_belief.get_plan_obj(sports_hike_rope)
    sports_bball_plan = bob_belief.get_plan_obj(sports_bball_rope)
    assert sports_swim_plan.star == swim_star
    assert sports_hike_plan.star == hike_star
    assert sports_bball_plan.star == bball_star


def test_BeliefUnit_edit_plan_attr_DeletesPlanUnit_awardunits():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)
    yao_str = "Yao"
    zia_str = "Zia"
    Xio_str = "Xio"
    yao_belief.add_voiceunit(yao_str)
    yao_belief.add_voiceunit(zia_str)
    yao_belief.add_voiceunit(Xio_str)

    swim_str = "swim"
    swim_rope = yao_belief.make_l1_rope(swim_str)

    yao_belief.set_l1_plan(planunit_shop(swim_str))
    awardunit_yao = awardunit_shop(yao_str, give_force=10)
    awardunit_zia = awardunit_shop(zia_str, give_force=10)
    awardunit_Xio = awardunit_shop(Xio_str, give_force=10)

    swim_plan = yao_belief.get_plan_obj(swim_rope)
    yao_belief.edit_plan_attr(swim_rope, awardunit=awardunit_yao)
    yao_belief.edit_plan_attr(swim_rope, awardunit=awardunit_zia)
    yao_belief.edit_plan_attr(swim_rope, awardunit=awardunit_Xio)

    assert len(swim_plan.awardunits) == 3
    assert len(yao_belief.planroot.kids[swim_str].awardunits) == 3

    # WHEN
    yao_belief.edit_plan_attr(swim_rope, awardunit_del=yao_str)

    # THEN
    swim_plan = yao_belief.get_plan_obj(swim_rope)
    print(f"{swim_plan.plan_label=}")
    print(f"{swim_plan.awardunits=}")
    print(f"{swim_plan.awardheirs=}")

    assert len(yao_belief.planroot.kids[swim_str].awardunits) == 2


def test_BeliefUnit__get_filtered_awardunits_plan_RemovesVoice_awardunits():
    # ESTABLISH
    bob_str = "Bob"
    example_belief = beliefunit_shop(bob_str)
    xia_str = "Xia"
    run_str = ";runners"
    hike_str = ";hikers"
    example_belief.add_voiceunit(xia_str)
    example_belief.get_voice(xia_str).add_membership(run_str)

    sports_str = "sports"
    sports_rope = example_belief.make_l1_rope(sports_str)
    example_belief.set_l1_plan(planunit_shop(sports_str))
    example_belief.edit_plan_attr(sports_rope, awardunit=awardunit_shop(run_str))
    example_belief.edit_plan_attr(sports_rope, awardunit=awardunit_shop(hike_str))
    example_belief_sports_plan = example_belief.get_plan_obj(sports_rope)
    assert len(example_belief_sports_plan.awardunits) == 2
    bob_belief = beliefunit_shop(bob_str)
    bob_belief.add_voiceunit(xia_str)
    bob_belief.get_voice(xia_str).add_membership(run_str)
    print(f"{example_belief_sports_plan.awardunits=}")

    # WHEN
    cleaned_plan = bob_belief._get_filtered_awardunits_plan(example_belief_sports_plan)

    # THEN
    assert len(cleaned_plan.awardunits) == 1
    assert list(cleaned_plan.awardunits.keys()) == [run_str]


def test_BeliefUnit__get_filtered_awardunits_plan_RemovesGroup_awardunit():
    # ESTABLISH
    bob_str = "Bob"
    example_belief = beliefunit_shop(bob_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    example_belief.add_voiceunit(xia_str)
    example_belief.add_voiceunit(zoa_str)

    swim_str = "swim"
    swim_rope = example_belief.make_l1_rope(swim_str)
    example_belief.set_l1_plan(planunit_shop(swim_str))
    example_belief.edit_plan_attr(swim_rope, awardunit=awardunit_shop(xia_str))
    example_belief.edit_plan_attr(swim_rope, awardunit=awardunit_shop(zoa_str))
    example_belief_swim_plan = example_belief.get_plan_obj(swim_rope)
    assert len(example_belief_swim_plan.awardunits) == 2
    bob_belief = beliefunit_shop(bob_str)
    bob_belief.add_voiceunit(xia_str)

    # WHEN
    cleaned_plan = bob_belief._get_filtered_awardunits_plan(example_belief_swim_plan)

    # THEN
    assert len(cleaned_plan.awardunits) == 1
    assert list(cleaned_plan.awardunits.keys()) == [xia_str]


def test_BeliefUnit_set_plan_ScenarioXX_SetsPlan_awardunits():
    # ESTABLISH
    bob_str = "Bob"
    example_belief = beliefunit_shop(bob_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    example_belief.add_voiceunit(xia_str)
    example_belief.add_voiceunit(zoa_str)

    casa_str = "casa"
    casa_rope = example_belief.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = example_belief.make_l1_rope(swim_str)
    example_belief.set_l1_plan(planunit_shop(casa_str))
    example_belief.set_l1_plan(planunit_shop(swim_str))
    example_belief.edit_plan_attr(swim_rope, awardunit=awardunit_shop(xia_str))
    example_belief.edit_plan_attr(swim_rope, awardunit=awardunit_shop(zoa_str))
    example_belief_swim_plan = example_belief.get_plan_obj(swim_rope)
    assert len(example_belief_swim_plan.awardunits) == 2
    bob_belief = beliefunit_shop(bob_str)
    bob_belief.add_voiceunit(xia_str)

    # WHEN
    bob_belief.set_l1_plan(example_belief_swim_plan, create_missing_plans=False)

    # THEN
    bob_belief_swim_plan = bob_belief.get_plan_obj(swim_rope)
    assert len(bob_belief_swim_plan.awardunits) == 1
    assert list(bob_belief_swim_plan.awardunits.keys()) == [xia_str]


def test_BeliefUnit_get_plan_obj_ReturnsPlan():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    nation_str = "nation"
    nation_rope = sue_belief.make_l1_rope(nation_str)
    brazil_str = "Brazil"
    brazil_rope = sue_belief.make_rope(nation_rope, brazil_str)

    # WHEN
    brazil_plan = sue_belief.get_plan_obj(rope=brazil_rope)

    # THEN
    assert brazil_plan is not None
    assert brazil_plan.plan_label == brazil_str

    # WHEN
    wk_str = "sem_jours"
    wk_rope = sue_belief.make_l1_rope(wk_str)
    wk_plan = sue_belief.get_plan_obj(rope=wk_rope)

    # THEN
    assert wk_plan is not None
    assert wk_plan.plan_label == wk_str

    # WHEN
    root_plan = sue_belief.get_plan_obj(sue_belief.planroot.get_plan_rope())

    # THEN
    assert root_plan is not None
    assert root_plan.get_plan_rope() == sue_belief.planroot.get_plan_rope()

    # WHEN / THEN
    bobdylan_str = "bobdylan"
    wrong_rope = sue_belief.make_l1_rope(bobdylan_str)
    with pytest_raises(Exception) as excinfo:
        sue_belief.get_plan_obj(rope=wrong_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{wrong_rope}'"


def test_BeliefUnit_plan_exists_ReturnsBool():
    # ESTABLISH
    sue_belief = get_beliefunit_with_4_levels()
    cat_rope = sue_belief.make_l1_rope("cat have dinner")
    wk_rope = sue_belief.make_l1_rope("sem_jours")
    casa_rope = sue_belief.make_l1_rope("casa")
    nation_rope = sue_belief.make_l1_rope("nation")
    sun_rope = sue_belief.make_rope(wk_rope, "Sun")
    mon_rope = sue_belief.make_rope(wk_rope, "Mon")
    tue_rope = sue_belief.make_rope(wk_rope, "Tue")
    wed_rope = sue_belief.make_rope(wk_rope, "Wed")
    thu_rope = sue_belief.make_rope(wk_rope, "Thur")
    fri_rope = sue_belief.make_rope(wk_rope, "Fri")
    sat_rope = sue_belief.make_rope(wk_rope, "Sat")
    france_rope = sue_belief.make_rope(nation_rope, "France")
    brazil_rope = sue_belief.make_rope(nation_rope, "Brazil")
    usa_rope = sue_belief.make_rope(nation_rope, "USA")
    texas_rope = sue_belief.make_rope(usa_rope, "Texas")
    oregon_rope = sue_belief.make_rope(usa_rope, "Oregon")
    # do not exist in belief
    sports_rope = sue_belief.make_l1_rope("sports")
    swim_rope = sue_belief.make_rope(sports_rope, "swimming")
    idaho_rope = sue_belief.make_rope(usa_rope, "Idaho")
    japan_rope = sue_belief.make_rope(nation_rope, "Japan")

    # WHEN / THEN
    assert sue_belief.plan_exists("") is False
    assert sue_belief.plan_exists(None) is False
    assert sue_belief.plan_exists(sue_belief.planroot.get_plan_rope())
    assert sue_belief.plan_exists(cat_rope)
    assert sue_belief.plan_exists(wk_rope)
    assert sue_belief.plan_exists(casa_rope)
    assert sue_belief.plan_exists(nation_rope)
    assert sue_belief.plan_exists(sun_rope)
    assert sue_belief.plan_exists(mon_rope)
    assert sue_belief.plan_exists(tue_rope)
    assert sue_belief.plan_exists(wed_rope)
    assert sue_belief.plan_exists(thu_rope)
    assert sue_belief.plan_exists(fri_rope)
    assert sue_belief.plan_exists(sat_rope)
    assert sue_belief.plan_exists(usa_rope)
    assert sue_belief.plan_exists(france_rope)
    assert sue_belief.plan_exists(brazil_rope)
    assert sue_belief.plan_exists(texas_rope)
    assert sue_belief.plan_exists(oregon_rope)
    assert sue_belief.plan_exists(to_rope("B")) is False
    assert sue_belief.plan_exists(sports_rope) is False
    assert sue_belief.plan_exists(swim_rope) is False
    assert sue_belief.plan_exists(idaho_rope) is False
    assert sue_belief.plan_exists(japan_rope) is False


def test_BeliefUnit_set_offtrack_fund_ReturnsObj():
    # ESTABLISH
    bob_beliefunit = beliefunit_shop("Bob")
    assert not bob_beliefunit.offtrack_fund

    # WHEN
    bob_beliefunit.set_offtrack_fund() == 0

    # THEN
    assert bob_beliefunit.offtrack_fund == 0

    # ESTABLISH
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wed"
    casa_rope = bob_beliefunit.make_l1_rope(casa_str)
    wk_rope = bob_beliefunit.make_l1_rope(wk_str)
    wed_rope = bob_beliefunit.make_rope(wk_rope, wed_str)
    casa_plan = planunit_shop(casa_str, fund_onset=70, fund_cease=170)
    wk_plan = planunit_shop(wk_str, fund_onset=70, fund_cease=75)
    wed_plan = planunit_shop(wed_str, fund_onset=72, fund_cease=75)
    casa_plan.parent_rope = bob_beliefunit.planroot.get_plan_rope()
    wk_plan.parent_rope = bob_beliefunit.planroot.get_plan_rope()
    wed_plan.parent_rope = wk_rope
    bob_beliefunit.set_l1_plan(casa_plan)
    bob_beliefunit.set_l1_plan(wk_plan)
    bob_beliefunit.set_plan_obj(wed_plan, wk_rope)
    bob_beliefunit.offtrack_kids_star_set.add(casa_rope)
    bob_beliefunit.offtrack_kids_star_set.add(wk_rope)
    assert bob_beliefunit.offtrack_fund == 0

    # WHEN
    bob_beliefunit.set_offtrack_fund()

    # THEN
    assert bob_beliefunit.offtrack_fund == 105

    # WHEN
    bob_beliefunit.offtrack_kids_star_set.add(wed_rope)
    bob_beliefunit.set_offtrack_fund()

    # THEN
    assert bob_beliefunit.offtrack_fund == 108


def test_BeliefUnit_allot_offtrack_fund_SetsCharUnit_fund_take_fund_give():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    bob_beliefunit = beliefunit_shop(bob_str)
    bob_beliefunit.add_voiceunit(bob_str)
    bob_beliefunit.add_voiceunit(yao_str, voice_cred_lumen=2)
    bob_beliefunit.add_voiceunit(sue_str, voice_debt_lumen=2)
    bob_beliefunit.set_offtrack_fund()
    assert bob_beliefunit.offtrack_fund == 0

    # WHEN
    bob_beliefunit._allot_offtrack_fund()

    # THEN
    assert bob_beliefunit.get_voice(bob_str).fund_give == 0
    assert bob_beliefunit.get_voice(bob_str).fund_take == 0
    assert bob_beliefunit.get_voice(yao_str).fund_give == 0
    assert bob_beliefunit.get_voice(yao_str).fund_take == 0
    assert bob_beliefunit.get_voice(sue_str).fund_give == 0
    assert bob_beliefunit.get_voice(sue_str).fund_take == 0

    # WHEN
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wed"
    casa_rope = bob_beliefunit.make_l1_rope(casa_str)
    wk_rope = bob_beliefunit.make_l1_rope(wk_str)
    wed_rope = bob_beliefunit.make_rope(wk_rope, wed_str)
    casa_plan = planunit_shop(casa_str, fund_onset=70, fund_cease=170)
    wk_plan = planunit_shop(wk_str, fund_onset=70, fund_cease=75)
    wed_plan = planunit_shop(wed_str, fund_onset=72, fund_cease=75)
    casa_plan.parent_rope = bob_beliefunit.planroot.get_plan_rope()
    wk_plan.parent_rope = bob_beliefunit.planroot.get_plan_rope()
    wed_plan.parent_rope = wk_rope
    bob_beliefunit.set_l1_plan(casa_plan)
    bob_beliefunit.set_l1_plan(wk_plan)
    bob_beliefunit.set_plan_obj(wed_plan, wk_rope)
    bob_beliefunit.offtrack_kids_star_set.add(casa_rope)
    bob_beliefunit.offtrack_kids_star_set.add(wk_rope)
    bob_beliefunit.set_offtrack_fund()
    assert bob_beliefunit.offtrack_fund == 105

    # WHEN
    bob_beliefunit._allot_offtrack_fund()

    # THEN
    assert bob_beliefunit.get_voice(bob_str).fund_give == 26
    assert bob_beliefunit.get_voice(bob_str).fund_take == 26
    assert bob_beliefunit.get_voice(yao_str).fund_give == 53
    assert bob_beliefunit.get_voice(yao_str).fund_take == 26
    assert bob_beliefunit.get_voice(sue_str).fund_give == 26
    assert bob_beliefunit.get_voice(sue_str).fund_take == 53

    bob_beliefunit.offtrack_kids_star_set.add(wed_rope)
    bob_beliefunit.set_offtrack_fund()

    # THEN
    assert bob_beliefunit.offtrack_fund == 108
