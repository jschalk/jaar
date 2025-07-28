from pytest import raises as pytest_raises
from src.a01_term_logic.rope import create_rope, default_knot_if_None, to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_plan import factunit_shop
from src.a05_plan_logic.healer import healerlink_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.example_believers import (
    get_believerunit_with_4_levels,
)


def test_BelieverUnit_set_plan_RaisesErrorWhen_parent_rope_IsInvalid():
    # ESTABLISH
    zia_believer = believerunit_shop("Zia")
    invalid_rootlabel_swim_rope = create_rope("swimming")
    assert invalid_rootlabel_swim_rope != zia_believer.belief_label
    casa_str = "casa"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_believer.set_plan(
            planunit_shop(casa_str), parent_rope=invalid_rootlabel_swim_rope
        )
    exception_str = f"set_plan failed because parent_rope '{invalid_rootlabel_swim_rope}' has an invalid root label. Should be {zia_believer.belief_label}."
    assert str(excinfo.value) == exception_str


def test_BelieverUnit_set_plan_RaisesErrorWhen_parent_rope_PlanDoesNotExist():
    # ESTABLISH
    zia_believer = believerunit_shop("Zia")
    swim_rope = zia_believer.make_l1_rope("swimming")
    casa_str = "casa"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_believer.set_plan(
            planunit_shop(casa_str),
            parent_rope=swim_rope,
            create_missing_ancestors=False,
        )
    exception_str = f"set_plan failed because '{swim_rope}' plan does not exist."
    assert str(excinfo.value) == exception_str


def test_BelieverUnit_set_plan_RaisesErrorWhen_plan_label_IsNotLabel():
    # ESTABLISH
    zia_believer = believerunit_shop("Zia")
    swim_rope = zia_believer.make_l1_rope("swimming")
    casa_str = "casa"
    casa_rope = zia_believer.make_l1_rope(casa_str)
    run_str = "run"
    run_rope = zia_believer.make_rope(casa_rope, run_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_believer.set_plan(planunit_shop(run_rope), parent_rope=swim_rope)
    exception_str = f"set_plan failed because '{run_rope}' is not a LabelTerm."
    assert str(excinfo.value) == exception_str


def test_BelieverUnit_set_plan_CorrectlySetsAttr():
    # ESTABLISH
    zia_believer = believerunit_shop("Zia")
    casa_str = "casa"
    assert not zia_believer.planroot._kids.get(casa_str)

    # WHEN
    zia_believer.set_plan(
        planunit_shop(casa_str), parent_rope=to_rope(zia_believer.belief_label)
    )

    # THEN
    print(f"{zia_believer.planroot._kids.keys()=}")
    assert zia_believer.planroot._kids.get(casa_str)


def test_BelieverUnit_plan_exists_ReturnsObj():
    # ESTABLISH
    zia_believer = believerunit_shop("Zia")
    casa_str = "casa"
    casa_rope = zia_believer.make_l1_rope(casa_str)
    assert zia_believer.plan_exists(casa_rope) is False

    # WHEN
    zia_believer.set_plan(
        planunit_shop(casa_str), parent_rope=to_rope(zia_believer.belief_label)
    )

    # THEN
    assert zia_believer.plan_exists(casa_rope)


def test_BelieverUnit_set_l1_plan_CorrectlySetsAttr():
    # ESTABLISH
    zia_believer = believerunit_shop("Zia")
    casa_str = "casa"
    casa_rope = zia_believer.make_l1_rope(casa_str)
    assert not zia_believer.planroot._kids.get(casa_rope)

    # WHEN
    zia_believer.set_l1_plan(planunit_shop(casa_str))

    # THEN
    assert not zia_believer.planroot._kids.get(casa_rope)


def test_BelieverUnit_add_plan_SetsAttr_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    slash_str = "/"
    bob_believerunit = believerunit_shop(bob_str, knot=slash_str)
    casa_rope = bob_believerunit.make_l1_rope("casa")
    assert not bob_believerunit.plan_exists(casa_rope)

    # WHEN
    bob_believerunit.add_plan(casa_rope)

    # THEN
    assert bob_believerunit.plan_exists(casa_rope)
    casa_planunit = bob_believerunit.get_plan_obj(casa_rope)
    assert casa_planunit.knot == bob_believerunit.knot
    assert not casa_planunit.task


def test_BelieverUnit_add_plan_SetsAttr_Scenario1():
    # ESTABLISH
    bob_str = "Bob"
    bob_believerunit = believerunit_shop(bob_str)
    casa_rope = bob_believerunit.make_l1_rope("casa")
    casa_mass = 13
    casa_task = True

    # WHEN
    bob_believerunit.add_plan(casa_rope, mass=casa_mass, task=casa_task)

    # THEN
    casa_planunit = bob_believerunit.get_plan_obj(casa_rope)
    assert casa_planunit.mass == casa_mass
    assert casa_planunit.task


def test_BelieverUnit_add_plan_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_believerunit = believerunit_shop(bob_str)
    casa_rope = bob_believerunit.make_l1_rope("casa")
    casa_mass = 13

    # WHEN
    casa_planunit = bob_believerunit.add_plan(casa_rope, mass=casa_mass)

    # THEN
    assert casa_planunit.plan_label == "casa"
    assert casa_planunit.mass == casa_mass


def test_BelieverUnit_set_plan_CorrectlyAddsPlanObjWithNonDefault_knot():
    # ESTABLISH
    slash_str = "/"
    assert slash_str != default_knot_if_None()
    bob_believer = believerunit_shop("Bob", knot=slash_str)
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wed"
    casa_rope = bob_believer.make_l1_rope(casa_str)
    wk_rope = bob_believer.make_l1_rope(wk_str)
    wed_rope = bob_believer.make_rope(wk_rope, wed_str)
    bob_believer.set_l1_plan(planunit_shop(casa_str))
    bob_believer.set_l1_plan(planunit_shop(wk_str))
    bob_believer.set_plan(planunit_shop(wed_str), wk_rope)
    print(f"{bob_believer.planroot._kids.keys()=}")
    assert len(bob_believer.planroot._kids) == 2
    wed_plan = bob_believer.get_plan_obj(wed_rope)
    assert wed_plan.knot == slash_str
    assert wed_plan.knot == bob_believer.knot

    # WHEN
    bob_believer.edit_plan_attr(casa_rope, reason_context=wk_rope, reason_case=wed_rope)

    # THEN
    casa_plan = bob_believer.get_plan_obj(casa_rope)
    assert casa_plan.reasonunits.get(wk_rope) is not None


def test_BelieverUnit_set_plan_CanCreateMissingPlanUnits():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    ww2_rope = sue_believer.make_l1_rope("ww2")
    battles_rope = sue_believer.make_rope(ww2_rope, "battles")
    coralsea_rope = sue_believer.make_rope(battles_rope, "coralsea")
    saratoga_plan = planunit_shop("USS Saratoga")
    assert sue_believer.plan_exists(battles_rope) is False
    assert sue_believer.plan_exists(coralsea_rope) is False

    # WHEN
    sue_believer.set_plan(saratoga_plan, parent_rope=coralsea_rope)

    # THEN
    assert sue_believer.plan_exists(battles_rope)
    assert sue_believer.plan_exists(coralsea_rope)


def test_BelieverUnit_del_plan_obj_Level0CannotBeDeleted():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    root_rope = to_rope(sue_believer.belief_label)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_believer.del_plan_obj(rope=root_rope)
    assert str(excinfo.value) == "Planroot cannot be deleted"


def test_BelieverUnit_del_plan_obj_Level1CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    wk_str = "sem_jours"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    sun_str = "Sun"
    sun_rope = sue_believer.make_rope(wk_rope, sun_str)
    assert sue_believer.get_plan_obj(wk_rope)
    assert sue_believer.get_plan_obj(sun_rope)

    # WHEN
    sue_believer.del_plan_obj(rope=wk_rope)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_believer.get_plan_obj(wk_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{wk_rope}'"
    new_sun_rope = sue_believer.make_l1_rope("Sun")
    with pytest_raises(Exception) as excinfo:
        sue_believer.get_plan_obj(new_sun_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{new_sun_rope}'"


def test_BelieverUnit_del_plan_obj_Level1CanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    wk_str = "sem_jours"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    sun_str = "Sun"
    old_sun_rope = sue_believer.make_rope(wk_rope, sun_str)
    assert sue_believer.get_plan_obj(old_sun_rope)

    # WHEN
    sue_believer.del_plan_obj(rope=wk_rope, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_believer.get_plan_obj(old_sun_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{old_sun_rope}'"
    new_sun_rope = sue_believer.make_l1_rope(sun_str)
    assert sue_believer.get_plan_obj(new_sun_rope)
    new_sun_plan = sue_believer.get_plan_obj(new_sun_rope)
    assert new_sun_plan.parent_rope == to_rope(sue_believer.belief_label)


def test_BelieverUnit_del_plan_obj_LevelNCanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    nation_str = "nation"
    nation_rope = sue_believer.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_believer.make_rope(nation_rope, usa_str)
    texas_str = "Texas"
    oregon_str = "Oregon"
    usa_texas_rope = sue_believer.make_rope(usa_rope, texas_str)
    usa_oregon_rope = sue_believer.make_rope(usa_rope, oregon_str)
    nation_texas_rope = sue_believer.make_rope(nation_rope, texas_str)
    nation_oregon_rope = sue_believer.make_rope(nation_rope, oregon_str)
    assert sue_believer.plan_exists(usa_rope)
    assert sue_believer.plan_exists(usa_texas_rope)
    assert sue_believer.plan_exists(usa_oregon_rope)
    assert sue_believer.plan_exists(nation_texas_rope) is False
    assert sue_believer.plan_exists(nation_oregon_rope) is False

    # WHEN
    sue_believer.del_plan_obj(rope=usa_rope, del_children=False)

    # THEN
    assert sue_believer.plan_exists(nation_texas_rope)
    assert sue_believer.plan_exists(nation_oregon_rope)
    assert sue_believer.plan_exists(usa_texas_rope) is False
    assert sue_believer.plan_exists(usa_oregon_rope) is False
    assert sue_believer.plan_exists(usa_rope) is False


def test_BelieverUnit_del_plan_obj_Level2CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    sem_jour_rope = sue_believer.make_l1_rope("sem_jours")
    mon_rope = sue_believer.make_rope(sem_jour_rope, "Mon")
    assert sue_believer.get_plan_obj(mon_rope)

    # WHEN
    sue_believer.del_plan_obj(rope=mon_rope)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_believer.get_plan_obj(mon_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{mon_rope}'"


def test_BelieverUnit_del_plan_obj_LevelNCanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    nation_str = "nation"
    nation_rope = sue_believer.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_believer.make_rope(nation_rope, usa_str)
    texas_str = "Texas"
    usa_texas_rope = sue_believer.make_rope(usa_rope, texas_str)
    assert sue_believer.get_plan_obj(usa_texas_rope)

    # WHEN
    sue_believer.del_plan_obj(rope=usa_texas_rope)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_believer.get_plan_obj(usa_texas_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{usa_texas_rope}'"


def test_BelieverUnit_edit_plan_attr_IsAbleToEditAnyAncestor_Plan():
    sue_believer = get_believerunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    print(f"{casa_rope=}")
    old_mass = sue_believer.planroot._kids[casa_str].mass
    assert old_mass == 30
    sue_believer.edit_plan_attr(casa_rope, mass=23)
    new_mass = sue_believer.planroot._kids[casa_str].mass
    assert new_mass == 23

    # uid: int = None,
    sue_believer.planroot._kids[casa_str]._uid = 34
    x_uid = sue_believer.planroot._kids[casa_str]._uid
    assert x_uid == 34
    sue_believer.edit_plan_attr(casa_rope, uid=23)
    uid_new = sue_believer.planroot._kids[casa_str]._uid
    assert uid_new == 23

    # begin: float = None,
    # close: float = None,
    sue_believer.planroot._kids[casa_str].begin = 39
    x_begin = sue_believer.planroot._kids[casa_str].begin
    assert x_begin == 39
    sue_believer.planroot._kids[casa_str].close = 43
    x_close = sue_believer.planroot._kids[casa_str].close
    assert x_close == 43
    sue_believer.edit_plan_attr(casa_rope, begin=25, close=29)
    assert sue_believer.planroot._kids[casa_str].begin == 25
    assert sue_believer.planroot._kids[casa_str].close == 29

    # gogo_want: float = None,
    # stop_want: float = None,
    sue_believer.planroot._kids[casa_str].gogo_want = 439
    x_gogo_want = sue_believer.planroot._kids[casa_str].gogo_want
    assert x_gogo_want == 439
    sue_believer.planroot._kids[casa_str].stop_want = 443
    x_stop_want = sue_believer.planroot._kids[casa_str].stop_want
    assert x_stop_want == 443
    sue_believer.edit_plan_attr(casa_rope, gogo_want=425, stop_want=429)
    assert sue_believer.planroot._kids[casa_str].gogo_want == 425
    assert sue_believer.planroot._kids[casa_str].stop_want == 429

    # factunit: factunit_shop = None,
    # sue_believer.planroot._kids[casa_str].factunits = None
    assert sue_believer.planroot._kids[casa_str].factunits == {}
    sem_jours_rope = sue_believer.make_l1_rope("sem_jours")
    fact_rope = sue_believer.make_rope(sem_jours_rope, "Sun")
    x_factunit = factunit_shop(f_context=fact_rope, f_state=fact_rope)

    casa_factunits = sue_believer.planroot._kids[casa_str].factunits
    print(f"{casa_factunits=}")
    sue_believer.edit_plan_attr(casa_rope, factunit=x_factunit)
    casa_factunits = sue_believer.planroot._kids[casa_str].factunits
    print(f"{casa_factunits=}")
    assert sue_believer.planroot._kids[casa_str].factunits == {
        x_factunit.f_context: x_factunit
    }

    # _descendant_task_count: int = None,
    sue_believer.planroot._kids[casa_str]._descendant_task_count = 81
    x_descendant_task_count = sue_believer.planroot._kids[
        casa_str
    ]._descendant_task_count
    assert x_descendant_task_count == 81
    sue_believer.edit_plan_attr(casa_rope, descendant_task_count=67)
    _descendant_task_count_new = sue_believer.planroot._kids[
        casa_str
    ]._descendant_task_count
    assert _descendant_task_count_new == 67

    # _all_partner_cred: bool = None,
    sue_believer.planroot._kids[casa_str]._all_partner_cred = 74
    x_all_partner_cred = sue_believer.planroot._kids[casa_str]._all_partner_cred
    assert x_all_partner_cred == 74
    sue_believer.edit_plan_attr(casa_rope, all_partner_cred=59)
    _all_partner_cred_new = sue_believer.planroot._kids[casa_str]._all_partner_cred
    assert _all_partner_cred_new == 59

    # _all_partner_debt: bool = None,
    sue_believer.planroot._kids[casa_str]._all_partner_debt = 74
    x_all_partner_debt = sue_believer.planroot._kids[casa_str]._all_partner_debt
    assert x_all_partner_debt == 74
    sue_believer.edit_plan_attr(casa_rope, all_partner_debt=59)
    _all_partner_debt_new = sue_believer.planroot._kids[casa_str]._all_partner_debt
    assert _all_partner_debt_new == 59

    # _awardlink: dict = None,
    sue_believer.planroot._kids[casa_str].awardlinks = {
        "fun": awardlink_shop(awardee_title="fun", give_force=1, take_force=7)
    }
    _awardlinks = sue_believer.planroot._kids[casa_str].awardlinks
    assert _awardlinks == {
        "fun": awardlink_shop(awardee_title="fun", give_force=1, take_force=7)
    }
    x_awardlink = awardlink_shop(awardee_title="fun", give_force=4, take_force=8)
    sue_believer.edit_plan_attr(casa_rope, awardlink=x_awardlink)
    assert sue_believer.planroot._kids[casa_str].awardlinks == {"fun": x_awardlink}

    # _is_expanded: dict = None,
    sue_believer.planroot._kids[casa_str]._is_expanded = "what"
    _is_expanded = sue_believer.planroot._kids[casa_str]._is_expanded
    assert _is_expanded == "what"
    sue_believer.edit_plan_attr(casa_rope, is_expanded=True)
    assert sue_believer.planroot._kids[casa_str]._is_expanded is True

    # task: dict = None,
    sue_believer.planroot._kids[casa_str].task = "funfun3"
    task = sue_believer.planroot._kids[casa_str].task
    assert task == "funfun3"
    sue_believer.edit_plan_attr(casa_rope, task=True)
    assert sue_believer.planroot._kids[casa_str].task is True

    # _healerlink:
    sue_believer.planroot._kids[casa_str].healerlink = "fun3rol"
    src_healerlink = sue_believer.planroot._kids[casa_str].healerlink
    assert src_healerlink == "fun3rol"
    sue_str = "Sue"
    yao_str = "Yao"
    x_healerlink = healerlink_shop({sue_str, yao_str})
    sue_believer.add_partnerunit(sue_str)
    sue_believer.add_partnerunit(yao_str)
    sue_believer.edit_plan_attr(casa_rope, healerlink=x_healerlink)
    assert sue_believer.planroot._kids[casa_str].healerlink == x_healerlink

    # _problem_bool: bool
    sue_believer.planroot._kids[casa_str].problem_bool = "fun3rol"
    src_problem_bool = sue_believer.planroot._kids[casa_str].problem_bool
    assert src_problem_bool == "fun3rol"
    x_problem_bool = True
    sue_believer.edit_plan_attr(casa_rope, problem_bool=x_problem_bool)
    assert sue_believer.planroot._kids[casa_str].problem_bool == x_problem_bool


def test_BelieverUnit_edit_plan_attr_RaisesErrorWhen_healerlink_healer_names_DoNotExist():
    # ESTABLISH
    yao_believer = believerunit_shop("Yao")
    casa_str = "casa"
    casa_rope = yao_believer.make_l1_rope(casa_str)
    yao_believer.set_l1_plan(planunit_shop(casa_str))
    jour_str = "jour_range"
    jour_plan = planunit_shop(jour_str, begin=44, close=110)
    yao_believer.set_l1_plan(jour_plan)

    casa_plan = yao_believer.get_plan_obj(casa_rope)
    assert casa_plan.begin is None
    assert casa_plan.close is None

    # WHEN / THEN
    sue_str = "Sue"
    x_healerlink = healerlink_shop({sue_str})
    with pytest_raises(Exception) as excinfo:
        yao_believer.edit_plan_attr(casa_rope, healerlink=x_healerlink)
    assert (
        str(excinfo.value)
        == f"Plan cannot edit healerlink because group_title '{sue_str}' does not exist as group in Believer"
    )


def test_BelieverUnit_set_plan_MustReorderKidsDictToBeAlphabetical():
    # ESTABLISH
    bob_believer = believerunit_shop("Bob")
    casa_str = "casa"
    bob_believer.set_l1_plan(planunit_shop(casa_str))
    swim_str = "swim"
    bob_believer.set_l1_plan(planunit_shop(swim_str))

    # WHEN
    plan_list = list(bob_believer.planroot._kids.values())

    # THEN
    assert plan_list[0].plan_label == casa_str


def test_BelieverUnit_set_plan_adoptee_RaisesErrorIfAdopteePlanDoesNotHaveCorrectParent():
    bob_believer = believerunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_believer.make_l1_rope(sports_str)
    bob_believer.set_l1_plan(planunit_shop(sports_str))
    swim_str = "swim"
    bob_believer.set_plan(planunit_shop(swim_str), parent_rope=sports_rope)

    # WHEN / THEN
    summer_str = "summer"
    hike_str = "hike"
    hike_rope = bob_believer.make_rope(sports_rope, hike_str)
    with pytest_raises(Exception) as excinfo:
        bob_believer.set_plan(
            plan_kid=planunit_shop(summer_str),
            parent_rope=sports_rope,
            adoptees=[swim_str, hike_str],
        )
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{hike_rope}'"


def test_BelieverUnit_set_plan_adoptee_CorrectlyAddsAdoptee():
    bob_believer = believerunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_believer.make_l1_rope(sports_str)
    bob_believer.set_l1_plan(planunit_shop(sports_str))
    swim_str = "swim"
    bob_believer.set_plan(planunit_shop(swim_str), parent_rope=sports_rope)
    hike_str = "hike"
    bob_believer.set_plan(planunit_shop(hike_str), parent_rope=sports_rope)

    sports_swim_rope = bob_believer.make_rope(sports_rope, swim_str)
    sports_hike_rope = bob_believer.make_rope(sports_rope, hike_str)
    assert bob_believer.plan_exists(sports_swim_rope)
    assert bob_believer.plan_exists(sports_hike_rope)
    summer_str = "summer"
    summer_rope = bob_believer.make_rope(sports_rope, summer_str)
    summer_swim_rope = bob_believer.make_rope(summer_rope, swim_str)
    summer_hike_rope = bob_believer.make_rope(summer_rope, hike_str)
    assert bob_believer.plan_exists(summer_swim_rope) is False
    assert bob_believer.plan_exists(summer_hike_rope) is False

    # WHEN / THEN
    bob_believer.set_plan(
        plan_kid=planunit_shop(summer_str),
        parent_rope=sports_rope,
        adoptees=[swim_str, hike_str],
    )

    # THEN
    summer_plan = bob_believer.get_plan_obj(summer_rope)
    print(f"{summer_plan._kids.keys()=}")
    assert bob_believer.plan_exists(summer_swim_rope)
    assert bob_believer.plan_exists(summer_hike_rope)
    assert bob_believer.plan_exists(sports_swim_rope) is False
    assert bob_believer.plan_exists(sports_hike_rope) is False


def test_BelieverUnit_set_plan_bundling_SetsNewParentWithMassEqualToSumOfAdoptedPlans():
    bob_believer = believerunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_believer.make_l1_rope(sports_str)
    bob_believer.set_l1_plan(planunit_shop(sports_str, mass=2))
    swim_str = "swim"
    swim_mass = 3
    bob_believer.set_plan(planunit_shop(swim_str, mass=swim_mass), sports_rope)
    hike_str = "hike"
    hike_mass = 5
    bob_believer.set_plan(planunit_shop(hike_str, mass=hike_mass), sports_rope)
    bball_str = "bball"
    bball_mass = 7
    bob_believer.set_plan(planunit_shop(bball_str, mass=bball_mass), sports_rope)

    sports_swim_rope = bob_believer.make_rope(sports_rope, swim_str)
    sports_hike_rope = bob_believer.make_rope(sports_rope, hike_str)
    sports_bball_rope = bob_believer.make_rope(sports_rope, bball_str)
    assert bob_believer.get_plan_obj(sports_swim_rope).mass == swim_mass
    assert bob_believer.get_plan_obj(sports_hike_rope).mass == hike_mass
    assert bob_believer.get_plan_obj(sports_bball_rope).mass == bball_mass
    summer_str = "summer"
    summer_rope = bob_believer.make_rope(sports_rope, summer_str)
    summer_swim_rope = bob_believer.make_rope(summer_rope, swim_str)
    summer_hike_rope = bob_believer.make_rope(summer_rope, hike_str)
    summer_bball_rope = bob_believer.make_rope(summer_rope, bball_str)
    assert bob_believer.plan_exists(summer_swim_rope) is False
    assert bob_believer.plan_exists(summer_hike_rope) is False
    assert bob_believer.plan_exists(summer_bball_rope) is False

    # WHEN / THEN
    bob_believer.set_plan(
        plan_kid=planunit_shop(summer_str),
        parent_rope=sports_rope,
        adoptees=[swim_str, hike_str],
        bundling=True,
    )

    # THEN
    assert bob_believer.get_plan_obj(summer_rope).mass == swim_mass + hike_mass
    assert bob_believer.get_plan_obj(summer_swim_rope).mass == swim_mass
    assert bob_believer.get_plan_obj(summer_hike_rope).mass == hike_mass
    assert bob_believer.plan_exists(summer_bball_rope) is False
    assert bob_believer.plan_exists(sports_swim_rope) is False
    assert bob_believer.plan_exists(sports_hike_rope) is False
    assert bob_believer.plan_exists(sports_bball_rope)


def test_BelieverUnit_del_plan_obj_DeletingBundledPlanReturnsPlansToOriginalState():
    bob_believer = believerunit_shop("Bob")
    sports_str = "sports"
    sports_rope = bob_believer.make_l1_rope(sports_str)
    bob_believer.set_l1_plan(planunit_shop(sports_str, mass=2))
    swim_str = "swim"
    swim_mass = 3
    bob_believer.set_plan(planunit_shop(swim_str, mass=swim_mass), sports_rope)
    hike_str = "hike"
    hike_mass = 5
    bob_believer.set_plan(planunit_shop(hike_str, mass=hike_mass), sports_rope)
    bball_str = "bball"
    bball_mass = 7
    bob_believer.set_plan(planunit_shop(bball_str, mass=bball_mass), sports_rope)

    sports_swim_rope = bob_believer.make_rope(sports_rope, swim_str)
    sports_hike_rope = bob_believer.make_rope(sports_rope, hike_str)
    sports_bball_rope = bob_believer.make_rope(sports_rope, bball_str)
    assert bob_believer.get_plan_obj(sports_swim_rope).mass == swim_mass
    assert bob_believer.get_plan_obj(sports_hike_rope).mass == hike_mass
    assert bob_believer.get_plan_obj(sports_bball_rope).mass == bball_mass
    summer_str = "summer"
    summer_rope = bob_believer.make_rope(sports_rope, summer_str)
    summer_swim_rope = bob_believer.make_rope(summer_rope, swim_str)
    summer_hike_rope = bob_believer.make_rope(summer_rope, hike_str)
    summer_bball_rope = bob_believer.make_rope(summer_rope, bball_str)
    assert bob_believer.plan_exists(summer_swim_rope) is False
    assert bob_believer.plan_exists(summer_hike_rope) is False
    assert bob_believer.plan_exists(summer_bball_rope) is False
    bob_believer.set_plan(
        plan_kid=planunit_shop(summer_str),
        parent_rope=sports_rope,
        adoptees=[swim_str, hike_str],
        bundling=True,
    )
    assert bob_believer.get_plan_obj(summer_rope).mass == swim_mass + hike_mass
    assert bob_believer.get_plan_obj(summer_swim_rope).mass == swim_mass
    assert bob_believer.get_plan_obj(summer_hike_rope).mass == hike_mass
    assert bob_believer.plan_exists(summer_bball_rope) is False
    assert bob_believer.plan_exists(sports_swim_rope) is False
    assert bob_believer.plan_exists(sports_hike_rope) is False
    assert bob_believer.plan_exists(sports_bball_rope)
    print(f"{bob_believer._plan_dict.keys()=}")

    # WHEN
    bob_believer.del_plan_obj(rope=summer_rope, del_children=False)

    # THEN
    sports_swim_plan = bob_believer.get_plan_obj(sports_swim_rope)
    sports_hike_plan = bob_believer.get_plan_obj(sports_hike_rope)
    sports_bball_plan = bob_believer.get_plan_obj(sports_bball_rope)
    assert sports_swim_plan.mass == swim_mass
    assert sports_hike_plan.mass == hike_mass
    assert sports_bball_plan.mass == bball_mass


def test_BelieverUnit_edit_plan_attr_DeletesPlanUnit_awardlinks():
    # ESTABLISH
    yao_str = "Yao"
    yao_believer = believerunit_shop(yao_str)
    yao_str = "Yao"
    zia_str = "Zia"
    Xio_str = "Xio"
    yao_believer.add_partnerunit(yao_str)
    yao_believer.add_partnerunit(zia_str)
    yao_believer.add_partnerunit(Xio_str)

    swim_str = "swim"
    swim_rope = yao_believer.make_l1_rope(swim_str)

    yao_believer.set_l1_plan(planunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)

    swim_plan = yao_believer.get_plan_obj(swim_rope)
    yao_believer.edit_plan_attr(swim_rope, awardlink=awardlink_yao)
    yao_believer.edit_plan_attr(swim_rope, awardlink=awardlink_zia)
    yao_believer.edit_plan_attr(swim_rope, awardlink=awardlink_Xio)

    assert len(swim_plan.awardlinks) == 3
    assert len(yao_believer.planroot._kids[swim_str].awardlinks) == 3

    # WHEN
    yao_believer.edit_plan_attr(swim_rope, awardlink_del=yao_str)

    # THEN
    swim_plan = yao_believer.get_plan_obj(swim_rope)
    print(f"{swim_plan.plan_label=}")
    print(f"{swim_plan.awardlinks=}")
    print(f"{swim_plan._awardheirs=}")

    assert len(yao_believer.planroot._kids[swim_str].awardlinks) == 2


def test_BelieverUnit__get_filtered_awardlinks_plan_CorrectlyRemovesPartner_awardlinks():
    # ESTABLISH
    bob_str = "Bob"
    example_believer = believerunit_shop(bob_str)
    xia_str = "Xia"
    run_str = ";runners"
    hike_str = ";hikers"
    example_believer.add_partnerunit(xia_str)
    example_believer.get_partner(xia_str).add_membership(run_str)

    sports_str = "sports"
    sports_rope = example_believer.make_l1_rope(sports_str)
    example_believer.set_l1_plan(planunit_shop(sports_str))
    example_believer.edit_plan_attr(sports_rope, awardlink=awardlink_shop(run_str))
    example_believer.edit_plan_attr(sports_rope, awardlink=awardlink_shop(hike_str))
    example_believer_sports_plan = example_believer.get_plan_obj(sports_rope)
    assert len(example_believer_sports_plan.awardlinks) == 2
    bob_believer = believerunit_shop(bob_str)
    bob_believer.add_partnerunit(xia_str)
    bob_believer.get_partner(xia_str).add_membership(run_str)
    print(f"{example_believer_sports_plan.awardlinks=}")

    # WHEN
    cleaned_plan = bob_believer._get_filtered_awardlinks_plan(
        example_believer_sports_plan
    )

    # THEN
    assert len(cleaned_plan.awardlinks) == 1
    assert list(cleaned_plan.awardlinks.keys()) == [run_str]


def test_BelieverUnit__get_filtered_awardlinks_plan_CorrectlyRemovesGroup_awardlink():
    # ESTABLISH
    bob_str = "Bob"
    example_believer = believerunit_shop(bob_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    example_believer.add_partnerunit(xia_str)
    example_believer.add_partnerunit(zoa_str)

    swim_str = "swim"
    swim_rope = example_believer.make_l1_rope(swim_str)
    example_believer.set_l1_plan(planunit_shop(swim_str))
    example_believer.edit_plan_attr(swim_rope, awardlink=awardlink_shop(xia_str))
    example_believer.edit_plan_attr(swim_rope, awardlink=awardlink_shop(zoa_str))
    example_believer_swim_plan = example_believer.get_plan_obj(swim_rope)
    assert len(example_believer_swim_plan.awardlinks) == 2
    bob_believer = believerunit_shop(bob_str)
    bob_believer.add_partnerunit(xia_str)

    # WHEN
    cleaned_plan = bob_believer._get_filtered_awardlinks_plan(
        example_believer_swim_plan
    )

    # THEN
    assert len(cleaned_plan.awardlinks) == 1
    assert list(cleaned_plan.awardlinks.keys()) == [xia_str]


def test_BelieverUnit_set_plan_SetsPlan_awardlinks():
    # ESTABLISH
    bob_str = "Bob"
    example_believer = believerunit_shop(bob_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    example_believer.add_partnerunit(xia_str)
    example_believer.add_partnerunit(zoa_str)

    casa_str = "casa"
    casa_rope = example_believer.make_l1_rope(casa_str)
    swim_str = "swim"
    swim_rope = example_believer.make_l1_rope(swim_str)
    example_believer.set_l1_plan(planunit_shop(casa_str))
    example_believer.set_l1_plan(planunit_shop(swim_str))
    example_believer.edit_plan_attr(swim_rope, awardlink=awardlink_shop(xia_str))
    example_believer.edit_plan_attr(swim_rope, awardlink=awardlink_shop(zoa_str))
    example_believer_swim_plan = example_believer.get_plan_obj(swim_rope)
    assert len(example_believer_swim_plan.awardlinks) == 2
    bob_believer = believerunit_shop(bob_str)
    bob_believer.add_partnerunit(xia_str)

    # WHEN
    bob_believer.set_l1_plan(example_believer_swim_plan, create_missing_plans=False)

    # THEN
    bob_believer_swim_plan = bob_believer.get_plan_obj(swim_rope)
    assert len(bob_believer_swim_plan.awardlinks) == 1
    assert list(bob_believer_swim_plan.awardlinks.keys()) == [xia_str]


def test_BelieverUnit_get_plan_obj_ReturnsPlan():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    nation_str = "nation"
    nation_rope = sue_believer.make_l1_rope(nation_str)
    brazil_str = "Brazil"
    brazil_rope = sue_believer.make_rope(nation_rope, brazil_str)

    # WHEN
    brazil_plan = sue_believer.get_plan_obj(rope=brazil_rope)

    # THEN
    assert brazil_plan is not None
    assert brazil_plan.plan_label == brazil_str

    # WHEN
    wk_str = "sem_jours"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    wk_plan = sue_believer.get_plan_obj(rope=wk_rope)

    # THEN
    assert wk_plan is not None
    assert wk_plan.plan_label == wk_str

    # WHEN
    root_plan = sue_believer.get_plan_obj(to_rope(sue_believer.belief_label))

    # THEN
    assert root_plan is not None
    assert root_plan.plan_label == sue_believer.belief_label

    # WHEN / THEN
    bobdylan_str = "bobdylan"
    wrong_rope = sue_believer.make_l1_rope(bobdylan_str)
    with pytest_raises(Exception) as excinfo:
        sue_believer.get_plan_obj(rope=wrong_rope)
    assert str(excinfo.value) == f"get_plan_obj failed. no plan at '{wrong_rope}'"


def test_BelieverUnit_plan_exists_ReturnsCorrectBool():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    cat_rope = sue_believer.make_l1_rope("cat have dinner")
    wk_rope = sue_believer.make_l1_rope("sem_jours")
    casa_rope = sue_believer.make_l1_rope("casa")
    nation_rope = sue_believer.make_l1_rope("nation")
    sun_rope = sue_believer.make_rope(wk_rope, "Sun")
    mon_rope = sue_believer.make_rope(wk_rope, "Mon")
    tue_rope = sue_believer.make_rope(wk_rope, "Tue")
    wed_rope = sue_believer.make_rope(wk_rope, "Wed")
    thu_rope = sue_believer.make_rope(wk_rope, "Thur")
    fri_rope = sue_believer.make_rope(wk_rope, "Fri")
    sat_rope = sue_believer.make_rope(wk_rope, "Sat")
    france_rope = sue_believer.make_rope(nation_rope, "France")
    brazil_rope = sue_believer.make_rope(nation_rope, "Brazil")
    usa_rope = sue_believer.make_rope(nation_rope, "USA")
    texas_rope = sue_believer.make_rope(usa_rope, "Texas")
    oregon_rope = sue_believer.make_rope(usa_rope, "Oregon")
    # do not exist in believer
    sports_rope = sue_believer.make_l1_rope("sports")
    swim_rope = sue_believer.make_rope(sports_rope, "swimming")
    idaho_rope = sue_believer.make_rope(usa_rope, "Idaho")
    japan_rope = sue_believer.make_rope(nation_rope, "Japan")

    # WHEN / THEN
    assert sue_believer.plan_exists("") is False
    assert sue_believer.plan_exists(None) is False
    assert sue_believer.plan_exists(to_rope(sue_believer.belief_label))
    assert sue_believer.plan_exists(cat_rope)
    assert sue_believer.plan_exists(wk_rope)
    assert sue_believer.plan_exists(casa_rope)
    assert sue_believer.plan_exists(nation_rope)
    assert sue_believer.plan_exists(sun_rope)
    assert sue_believer.plan_exists(mon_rope)
    assert sue_believer.plan_exists(tue_rope)
    assert sue_believer.plan_exists(wed_rope)
    assert sue_believer.plan_exists(thu_rope)
    assert sue_believer.plan_exists(fri_rope)
    assert sue_believer.plan_exists(sat_rope)
    assert sue_believer.plan_exists(usa_rope)
    assert sue_believer.plan_exists(france_rope)
    assert sue_believer.plan_exists(brazil_rope)
    assert sue_believer.plan_exists(texas_rope)
    assert sue_believer.plan_exists(oregon_rope)
    assert sue_believer.plan_exists(to_rope("B")) is False
    assert sue_believer.plan_exists(sports_rope) is False
    assert sue_believer.plan_exists(swim_rope) is False
    assert sue_believer.plan_exists(idaho_rope) is False
    assert sue_believer.plan_exists(japan_rope) is False


def test_BelieverUnit_set_offtrack_fund_ReturnsObj():
    # ESTABLISH
    bob_believerunit = believerunit_shop("Bob")
    assert not bob_believerunit._offtrack_fund

    # WHEN
    bob_believerunit.set_offtrack_fund() == 0

    # THEN
    assert bob_believerunit._offtrack_fund == 0

    # ESTABLISH
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wed"
    casa_rope = bob_believerunit.make_l1_rope(casa_str)
    wk_rope = bob_believerunit.make_l1_rope(wk_str)
    wed_rope = bob_believerunit.make_rope(wk_rope, wed_str)
    casa_plan = planunit_shop(casa_str, _fund_onset=70, _fund_cease=170)
    wk_plan = planunit_shop(wk_str, _fund_onset=70, _fund_cease=75)
    wed_plan = planunit_shop(wed_str, _fund_onset=72, _fund_cease=75)
    casa_plan.parent_rope = bob_believerunit.belief_label
    wk_plan.parent_rope = bob_believerunit.belief_label
    wed_plan.parent_rope = wk_rope
    bob_believerunit.set_l1_plan(casa_plan)
    bob_believerunit.set_l1_plan(wk_plan)
    bob_believerunit.set_plan(wed_plan, wk_rope)
    bob_believerunit._offtrack_kids_mass_set.add(casa_rope)
    bob_believerunit._offtrack_kids_mass_set.add(wk_rope)
    assert bob_believerunit._offtrack_fund == 0

    # WHEN
    bob_believerunit.set_offtrack_fund()

    # THEN
    assert bob_believerunit._offtrack_fund == 105

    # WHEN
    bob_believerunit._offtrack_kids_mass_set.add(wed_rope)
    bob_believerunit.set_offtrack_fund()

    # THEN
    assert bob_believerunit._offtrack_fund == 108


def test_BelieverUnit_allot_offtrack_fund_SetsCharUnit_fund_take_fund_give():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    bob_believerunit = believerunit_shop(bob_str)
    bob_believerunit.add_partnerunit(bob_str)
    bob_believerunit.add_partnerunit(yao_str, partner_cred_points=2)
    bob_believerunit.add_partnerunit(sue_str, partner_debt_points=2)
    bob_believerunit.set_offtrack_fund()
    assert bob_believerunit._offtrack_fund == 0

    # WHEN
    bob_believerunit._allot_offtrack_fund()

    # THEN
    assert bob_believerunit.get_partner(bob_str)._fund_give == 0
    assert bob_believerunit.get_partner(bob_str)._fund_take == 0
    assert bob_believerunit.get_partner(yao_str)._fund_give == 0
    assert bob_believerunit.get_partner(yao_str)._fund_take == 0
    assert bob_believerunit.get_partner(sue_str)._fund_give == 0
    assert bob_believerunit.get_partner(sue_str)._fund_take == 0

    # WHEN
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wed"
    casa_rope = bob_believerunit.make_l1_rope(casa_str)
    wk_rope = bob_believerunit.make_l1_rope(wk_str)
    wed_rope = bob_believerunit.make_rope(wk_rope, wed_str)
    casa_plan = planunit_shop(casa_str, _fund_onset=70, _fund_cease=170)
    wk_plan = planunit_shop(wk_str, _fund_onset=70, _fund_cease=75)
    wed_plan = planunit_shop(wed_str, _fund_onset=72, _fund_cease=75)
    casa_plan.parent_rope = bob_believerunit.belief_label
    wk_plan.parent_rope = bob_believerunit.belief_label
    wed_plan.parent_rope = wk_rope
    bob_believerunit.set_l1_plan(casa_plan)
    bob_believerunit.set_l1_plan(wk_plan)
    bob_believerunit.set_plan(wed_plan, wk_rope)
    bob_believerunit._offtrack_kids_mass_set.add(casa_rope)
    bob_believerunit._offtrack_kids_mass_set.add(wk_rope)
    bob_believerunit.set_offtrack_fund()
    assert bob_believerunit._offtrack_fund == 105

    # WHEN
    bob_believerunit._allot_offtrack_fund()

    # THEN
    assert bob_believerunit.get_partner(bob_str)._fund_give == 26
    assert bob_believerunit.get_partner(bob_str)._fund_take == 26
    assert bob_believerunit.get_partner(yao_str)._fund_give == 53
    assert bob_believerunit.get_partner(yao_str)._fund_take == 26
    assert bob_believerunit.get_partner(sue_str)._fund_give == 26
    assert bob_believerunit.get_partner(sue_str)._fund_take == 53

    bob_believerunit._offtrack_kids_mass_set.add(wed_rope)
    bob_believerunit.set_offtrack_fund()

    # THEN
    assert bob_believerunit._offtrack_fund == 108
