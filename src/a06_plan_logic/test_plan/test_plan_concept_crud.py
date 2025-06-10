from pytest import raises as pytest_raises
from src.a01_term_logic.way import create_way, default_bridge_if_None, to_way
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_plan_logic._test_util.example_plans import get_planunit_with_4_levels
from src.a06_plan_logic.plan import planunit_shop


def test_PlanUnit_set_concept_RaisesErrorWhen_parent_way_IsInvalid():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    invalid_rootlabel_swim_way = create_way("swimming")
    assert invalid_rootlabel_swim_way != zia_plan.vow_label
    casa_str = "casa"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_concept(
            conceptunit_shop(casa_str), parent_way=invalid_rootlabel_swim_way
        )
    exception_str = f"set_concept failed because parent_way '{invalid_rootlabel_swim_way}' has an invalid root label. Should be {zia_plan.vow_label}."
    assert str(excinfo.value) == exception_str


def test_PlanUnit_set_concept_RaisesErrorWhen_parent_way_ConceptDoesNotExist():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    swim_way = zia_plan.make_l1_way("swimming")
    casa_str = "casa"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_concept(
            conceptunit_shop(casa_str),
            parent_way=swim_way,
            create_missing_ancestors=False,
        )
    exception_str = f"set_concept failed because '{swim_way}' concept does not exist."
    assert str(excinfo.value) == exception_str


def test_PlanUnit_set_concept_RaisesErrorWhen_concept_label_IsNotLabel():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    swim_way = zia_plan.make_l1_way("swimming")
    casa_str = "casa"
    casa_way = zia_plan.make_l1_way(casa_str)
    run_str = "run"
    run_way = zia_plan.make_way(casa_way, run_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_concept(conceptunit_shop(run_way), parent_way=swim_way)
    exception_str = f"set_concept failed because '{run_way}' is not a LabelTerm."
    assert str(excinfo.value) == exception_str


def test_PlanUnit_set_concept_CorrectlySetsAttr():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    casa_str = "casa"
    assert not zia_plan.conceptroot._kids.get(casa_str)

    # WHEN
    zia_plan.set_concept(
        conceptunit_shop(casa_str), parent_way=to_way(zia_plan.vow_label)
    )

    # THEN
    print(f"{zia_plan.conceptroot._kids.keys()=}")
    assert zia_plan.conceptroot._kids.get(casa_str)


def test_PlanUnit_concept_exists_ReturnsObj():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    casa_str = "casa"
    casa_way = zia_plan.make_l1_way(casa_str)
    assert zia_plan.concept_exists(casa_way) is False

    # WHEN
    zia_plan.set_concept(
        conceptunit_shop(casa_str), parent_way=to_way(zia_plan.vow_label)
    )

    # THEN
    assert zia_plan.concept_exists(casa_way)


def test_PlanUnit_set_l1_concept_CorrectlySetsAttr():
    # ESTABLISH
    zia_plan = planunit_shop("Zia")
    casa_str = "casa"
    casa_way = zia_plan.make_l1_way(casa_str)
    assert not zia_plan.conceptroot._kids.get(casa_way)

    # WHEN
    zia_plan.set_l1_concept(conceptunit_shop(casa_str))

    # THEN
    assert not zia_plan.conceptroot._kids.get(casa_way)


def test_PlanUnit_add_concept_SetsAttr_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    slash_str = "/"
    bob_planunit = planunit_shop(bob_str, bridge=slash_str)
    casa_way = bob_planunit.make_l1_way("casa")
    assert not bob_planunit.concept_exists(casa_way)

    # WHEN
    bob_planunit.add_concept(casa_way)

    # THEN
    assert bob_planunit.concept_exists(casa_way)
    casa_conceptunit = bob_planunit.get_concept_obj(casa_way)
    assert casa_conceptunit.bridge == bob_planunit.bridge
    assert not casa_conceptunit.task


def test_PlanUnit_add_concept_SetsAttr_Scenario1():
    # ESTABLISH
    bob_str = "Bob"
    bob_planunit = planunit_shop(bob_str)
    casa_way = bob_planunit.make_l1_way("casa")
    casa_mass = 13
    casa_task = True

    # WHEN
    bob_planunit.add_concept(casa_way, mass=casa_mass, task=casa_task)

    # THEN
    casa_conceptunit = bob_planunit.get_concept_obj(casa_way)
    assert casa_conceptunit.mass == casa_mass
    assert casa_conceptunit.task


def test_PlanUnit_add_concept_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_planunit = planunit_shop(bob_str)
    casa_way = bob_planunit.make_l1_way("casa")
    casa_mass = 13

    # WHEN
    casa_conceptunit = bob_planunit.add_concept(casa_way, mass=casa_mass)

    # THEN
    assert casa_conceptunit.concept_label == "casa"
    assert casa_conceptunit.mass == casa_mass


def test_PlanUnit_set_concept_CorrectlyAddsConceptObjWithNonDefault_bridge():
    # ESTABLISH
    slash_str = "/"
    assert slash_str != default_bridge_if_None()
    bob_plan = planunit_shop("Bob", bridge=slash_str)
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wednesday"
    casa_way = bob_plan.make_l1_way(casa_str)
    wk_way = bob_plan.make_l1_way(wk_str)
    wed_way = bob_plan.make_way(wk_way, wed_str)
    bob_plan.set_l1_concept(conceptunit_shop(casa_str))
    bob_plan.set_l1_concept(conceptunit_shop(wk_str))
    bob_plan.set_concept(conceptunit_shop(wed_str), wk_way)
    print(f"{bob_plan.conceptroot._kids.keys()=}")
    assert len(bob_plan.conceptroot._kids) == 2
    wed_concept = bob_plan.get_concept_obj(wed_way)
    assert wed_concept.bridge == slash_str
    assert wed_concept.bridge == bob_plan.bridge

    # WHEN
    bob_plan.edit_concept_attr(casa_way, reason_rcontext=wk_way, reason_premise=wed_way)

    # THEN
    casa_concept = bob_plan.get_concept_obj(casa_way)
    assert casa_concept.reasonunits.get(wk_way) is not None


def test_PlanUnit_set_concept_CanCreateMissingConceptUnits():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    ww2_way = sue_plan.make_l1_way("ww2")
    battles_way = sue_plan.make_way(ww2_way, "battles")
    coralsea_way = sue_plan.make_way(battles_way, "coralsea")
    saratoga_concept = conceptunit_shop("USS Saratoga")
    assert sue_plan.concept_exists(battles_way) is False
    assert sue_plan.concept_exists(coralsea_way) is False

    # WHEN
    sue_plan.set_concept(saratoga_concept, parent_way=coralsea_way)

    # THEN
    assert sue_plan.concept_exists(battles_way)
    assert sue_plan.concept_exists(coralsea_way)


def test_PlanUnit_del_concept_obj_Level0CannotBeDeleted():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    root_way = to_way(sue_plan.vow_label)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.del_concept_obj(way=root_way)
    assert str(excinfo.value) == "Conceptroot cannot be deleted"


def test_PlanUnit_del_concept_obj_Level1CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    wk_str = "wkdays"
    wk_way = sue_plan.make_l1_way(wk_str)
    sun_str = "Sunday"
    sun_way = sue_plan.make_way(wk_way, sun_str)
    assert sue_plan.get_concept_obj(wk_way)
    assert sue_plan.get_concept_obj(sun_way)

    # WHEN
    sue_plan.del_concept_obj(way=wk_way)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_concept_obj(wk_way)
    assert str(excinfo.value) == f"get_concept_obj failed. no concept at '{wk_way}'"
    new_sunday_way = sue_plan.make_l1_way("Sunday")
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_concept_obj(new_sunday_way)
    assert (
        str(excinfo.value)
        == f"get_concept_obj failed. no concept at '{new_sunday_way}'"
    )


def test_PlanUnit_del_concept_obj_Level1CanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    wk_str = "wkdays"
    wk_way = sue_plan.make_l1_way(wk_str)
    sun_str = "Sunday"
    old_sunday_way = sue_plan.make_way(wk_way, sun_str)
    assert sue_plan.get_concept_obj(old_sunday_way)

    # WHEN
    sue_plan.del_concept_obj(way=wk_way, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_concept_obj(old_sunday_way)
    assert (
        str(excinfo.value)
        == f"get_concept_obj failed. no concept at '{old_sunday_way}'"
    )
    new_sunday_way = sue_plan.make_l1_way(sun_str)
    assert sue_plan.get_concept_obj(new_sunday_way)
    new_sunday_concept = sue_plan.get_concept_obj(new_sunday_way)
    assert new_sunday_concept.parent_way == to_way(sue_plan.vow_label)


def test_PlanUnit_del_concept_obj_LevelNCanBeDeleted_ChildrenInherited():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    nation_str = "nation"
    nation_way = sue_plan.make_l1_way(nation_str)
    usa_str = "USA"
    usa_way = sue_plan.make_way(nation_way, usa_str)
    texas_str = "Texas"
    oregon_str = "Oregon"
    usa_texas_way = sue_plan.make_way(usa_way, texas_str)
    usa_oregon_way = sue_plan.make_way(usa_way, oregon_str)
    nation_texas_way = sue_plan.make_way(nation_way, texas_str)
    nation_oregon_way = sue_plan.make_way(nation_way, oregon_str)
    assert sue_plan.concept_exists(usa_way)
    assert sue_plan.concept_exists(usa_texas_way)
    assert sue_plan.concept_exists(usa_oregon_way)
    assert sue_plan.concept_exists(nation_texas_way) is False
    assert sue_plan.concept_exists(nation_oregon_way) is False

    # WHEN
    sue_plan.del_concept_obj(way=usa_way, del_children=False)

    # THEN
    assert sue_plan.concept_exists(nation_texas_way)
    assert sue_plan.concept_exists(nation_oregon_way)
    assert sue_plan.concept_exists(usa_texas_way) is False
    assert sue_plan.concept_exists(usa_oregon_way) is False
    assert sue_plan.concept_exists(usa_way) is False


def test_PlanUnit_del_concept_obj_Level2CanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    wkday_way = sue_plan.make_l1_way("wkdays")
    monday_way = sue_plan.make_way(wkday_way, "Monday")
    assert sue_plan.get_concept_obj(monday_way)

    # WHEN
    sue_plan.del_concept_obj(way=monday_way)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_concept_obj(monday_way)
    assert str(excinfo.value) == f"get_concept_obj failed. no concept at '{monday_way}'"


def test_PlanUnit_del_concept_obj_LevelNCanBeDeleted_ChildrenDeleted():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    nation_str = "nation"
    nation_way = sue_plan.make_l1_way(nation_str)
    usa_str = "USA"
    usa_way = sue_plan.make_way(nation_way, usa_str)
    texas_str = "Texas"
    usa_texas_way = sue_plan.make_way(usa_way, texas_str)
    assert sue_plan.get_concept_obj(usa_texas_way)

    # WHEN
    sue_plan.del_concept_obj(way=usa_texas_way)

    # THEN
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_concept_obj(usa_texas_way)
    assert (
        str(excinfo.value) == f"get_concept_obj failed. no concept at '{usa_texas_way}'"
    )


def test_PlanUnit_edit_concept_attr_IsAbleToEditAnyAncestor_Concept():
    sue_plan = get_planunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_plan.make_l1_way(casa_str)
    print(f"{casa_way=}")
    old_mass = sue_plan.conceptroot._kids[casa_str].mass
    assert old_mass == 30
    sue_plan.edit_concept_attr(casa_way, mass=23)
    new_mass = sue_plan.conceptroot._kids[casa_str].mass
    assert new_mass == 23

    # uid: int = None,
    sue_plan.conceptroot._kids[casa_str]._uid = 34
    x_uid = sue_plan.conceptroot._kids[casa_str]._uid
    assert x_uid == 34
    sue_plan.edit_concept_attr(casa_way, uid=23)
    uid_new = sue_plan.conceptroot._kids[casa_str]._uid
    assert uid_new == 23

    # begin: float = None,
    # close: float = None,
    sue_plan.conceptroot._kids[casa_str].begin = 39
    x_begin = sue_plan.conceptroot._kids[casa_str].begin
    assert x_begin == 39
    sue_plan.conceptroot._kids[casa_str].close = 43
    x_close = sue_plan.conceptroot._kids[casa_str].close
    assert x_close == 43
    sue_plan.edit_concept_attr(casa_way, begin=25, close=29)
    assert sue_plan.conceptroot._kids[casa_str].begin == 25
    assert sue_plan.conceptroot._kids[casa_str].close == 29

    # gogo_want: float = None,
    # stop_want: float = None,
    sue_plan.conceptroot._kids[casa_str].gogo_want = 439
    x_gogo_want = sue_plan.conceptroot._kids[casa_str].gogo_want
    assert x_gogo_want == 439
    sue_plan.conceptroot._kids[casa_str].stop_want = 443
    x_stop_want = sue_plan.conceptroot._kids[casa_str].stop_want
    assert x_stop_want == 443
    sue_plan.edit_concept_attr(casa_way, gogo_want=425, stop_want=429)
    assert sue_plan.conceptroot._kids[casa_str].gogo_want == 425
    assert sue_plan.conceptroot._kids[casa_str].stop_want == 429

    # factunit: factunit_shop = None,
    # sue_plan.conceptroot._kids[casa_str].factunits = None
    assert sue_plan.conceptroot._kids[casa_str].factunits == {}
    wkdays_way = sue_plan.make_l1_way("wkdays")
    fact_way = sue_plan.make_way(wkdays_way, "Sunday")
    x_factunit = factunit_shop(fcontext=fact_way, fstate=fact_way)

    casa_factunits = sue_plan.conceptroot._kids[casa_str].factunits
    print(f"{casa_factunits=}")
    sue_plan.edit_concept_attr(casa_way, factunit=x_factunit)
    casa_factunits = sue_plan.conceptroot._kids[casa_str].factunits
    print(f"{casa_factunits=}")
    assert sue_plan.conceptroot._kids[casa_str].factunits == {
        x_factunit.fcontext: x_factunit
    }

    # _descendant_task_count: int = None,
    sue_plan.conceptroot._kids[casa_str]._descendant_task_count = 81
    x_descendant_task_count = sue_plan.conceptroot._kids[
        casa_str
    ]._descendant_task_count
    assert x_descendant_task_count == 81
    sue_plan.edit_concept_attr(casa_way, descendant_task_count=67)
    _descendant_task_count_new = sue_plan.conceptroot._kids[
        casa_str
    ]._descendant_task_count
    assert _descendant_task_count_new == 67

    # _all_acct_cred: bool = None,
    sue_plan.conceptroot._kids[casa_str]._all_acct_cred = 74
    x_all_acct_cred = sue_plan.conceptroot._kids[casa_str]._all_acct_cred
    assert x_all_acct_cred == 74
    sue_plan.edit_concept_attr(casa_way, all_acct_cred=59)
    _all_acct_cred_new = sue_plan.conceptroot._kids[casa_str]._all_acct_cred
    assert _all_acct_cred_new == 59

    # _all_acct_debt: bool = None,
    sue_plan.conceptroot._kids[casa_str]._all_acct_debt = 74
    x_all_acct_debt = sue_plan.conceptroot._kids[casa_str]._all_acct_debt
    assert x_all_acct_debt == 74
    sue_plan.edit_concept_attr(casa_way, all_acct_debt=59)
    _all_acct_debt_new = sue_plan.conceptroot._kids[casa_str]._all_acct_debt
    assert _all_acct_debt_new == 59

    # _awardlink: dict = None,
    sue_plan.conceptroot._kids[casa_str].awardlinks = {
        "fun": awardlink_shop(awardee_title="fun", give_force=1, take_force=7)
    }
    _awardlinks = sue_plan.conceptroot._kids[casa_str].awardlinks
    assert _awardlinks == {
        "fun": awardlink_shop(awardee_title="fun", give_force=1, take_force=7)
    }
    x_awardlink = awardlink_shop(awardee_title="fun", give_force=4, take_force=8)
    sue_plan.edit_concept_attr(casa_way, awardlink=x_awardlink)
    assert sue_plan.conceptroot._kids[casa_str].awardlinks == {"fun": x_awardlink}

    # _is_expanded: dict = None,
    sue_plan.conceptroot._kids[casa_str]._is_expanded = "what"
    _is_expanded = sue_plan.conceptroot._kids[casa_str]._is_expanded
    assert _is_expanded == "what"
    sue_plan.edit_concept_attr(casa_way, is_expanded=True)
    assert sue_plan.conceptroot._kids[casa_str]._is_expanded is True

    # task: dict = None,
    sue_plan.conceptroot._kids[casa_str].task = "funfun3"
    task = sue_plan.conceptroot._kids[casa_str].task
    assert task == "funfun3"
    sue_plan.edit_concept_attr(casa_way, task=True)
    assert sue_plan.conceptroot._kids[casa_str].task is True

    # _healerlink:
    sue_plan.conceptroot._kids[casa_str].healerlink = "fun3rol"
    src_healerlink = sue_plan.conceptroot._kids[casa_str].healerlink
    assert src_healerlink == "fun3rol"
    sue_str = "Sue"
    yao_str = "Yao"
    x_healerlink = healerlink_shop({sue_str, yao_str})
    sue_plan.add_acctunit(sue_str)
    sue_plan.add_acctunit(yao_str)
    sue_plan.edit_concept_attr(casa_way, healerlink=x_healerlink)
    assert sue_plan.conceptroot._kids[casa_str].healerlink == x_healerlink

    # _problem_bool: bool
    sue_plan.conceptroot._kids[casa_str].problem_bool = "fun3rol"
    src_problem_bool = sue_plan.conceptroot._kids[casa_str].problem_bool
    assert src_problem_bool == "fun3rol"
    x_problem_bool = True
    sue_plan.edit_concept_attr(casa_way, problem_bool=x_problem_bool)
    assert sue_plan.conceptroot._kids[casa_str].problem_bool == x_problem_bool


def test_PlanUnit_edit_concept_attr_RaisesErrorWhen_healerlink_healer_names_DoNotExist():
    # ESTABLISH
    yao_plan = planunit_shop("Yao")
    casa_str = "casa"
    casa_way = yao_plan.make_l1_way(casa_str)
    yao_plan.set_l1_concept(conceptunit_shop(casa_str))
    day_str = "day_range"
    day_concept = conceptunit_shop(day_str, begin=44, close=110)
    day_way = yao_plan.make_l1_way(day_str)
    yao_plan.set_l1_concept(day_concept)

    casa_concept = yao_plan.get_concept_obj(casa_way)
    assert casa_concept.begin is None
    assert casa_concept.close is None

    # WHEN / THEN
    sue_str = "Sue"
    x_healerlink = healerlink_shop({sue_str})
    with pytest_raises(Exception) as excinfo:
        yao_plan.edit_concept_attr(casa_way, healerlink=x_healerlink)
    assert (
        str(excinfo.value)
        == f"Concept cannot edit healerlink because group_title '{sue_str}' does not exist as group in Plan"
    )


def test_PlanUnit_set_concept_MustReorderKidsDictToBeAlphabetical():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")
    casa_str = "casa"
    bob_plan.set_l1_concept(conceptunit_shop(casa_str))
    swim_str = "swim"
    bob_plan.set_l1_concept(conceptunit_shop(swim_str))

    # WHEN
    concept_list = list(bob_plan.conceptroot._kids.values())

    # THEN
    assert concept_list[0].concept_label == casa_str


def test_PlanUnit_set_concept_adoptee_RaisesErrorIfAdopteeConceptDoesNotHaveCorrectParent():
    bob_plan = planunit_shop("Bob")
    sports_str = "sports"
    sports_way = bob_plan.make_l1_way(sports_str)
    bob_plan.set_l1_concept(conceptunit_shop(sports_str))
    swim_str = "swim"
    bob_plan.set_concept(conceptunit_shop(swim_str), parent_way=sports_way)

    # WHEN / THEN
    summer_str = "summer"
    hike_str = "hike"
    hike_way = bob_plan.make_way(sports_way, hike_str)
    with pytest_raises(Exception) as excinfo:
        bob_plan.set_concept(
            concept_kid=conceptunit_shop(summer_str),
            parent_way=sports_way,
            adoptees=[swim_str, hike_str],
        )
    assert str(excinfo.value) == f"get_concept_obj failed. no concept at '{hike_way}'"


def test_PlanUnit_set_concept_adoptee_CorrectlyAddsAdoptee():
    bob_plan = planunit_shop("Bob")
    sports_str = "sports"
    sports_way = bob_plan.make_l1_way(sports_str)
    bob_plan.set_l1_concept(conceptunit_shop(sports_str))
    swim_str = "swim"
    bob_plan.set_concept(conceptunit_shop(swim_str), parent_way=sports_way)
    hike_str = "hike"
    bob_plan.set_concept(conceptunit_shop(hike_str), parent_way=sports_way)

    sports_swim_way = bob_plan.make_way(sports_way, swim_str)
    sports_hike_way = bob_plan.make_way(sports_way, hike_str)
    assert bob_plan.concept_exists(sports_swim_way)
    assert bob_plan.concept_exists(sports_hike_way)
    summer_str = "summer"
    summer_way = bob_plan.make_way(sports_way, summer_str)
    summer_swim_way = bob_plan.make_way(summer_way, swim_str)
    summer_hike_way = bob_plan.make_way(summer_way, hike_str)
    assert bob_plan.concept_exists(summer_swim_way) is False
    assert bob_plan.concept_exists(summer_hike_way) is False

    # WHEN / THEN
    bob_plan.set_concept(
        concept_kid=conceptunit_shop(summer_str),
        parent_way=sports_way,
        adoptees=[swim_str, hike_str],
    )

    # THEN
    summer_concept = bob_plan.get_concept_obj(summer_way)
    print(f"{summer_concept._kids.keys()=}")
    assert bob_plan.concept_exists(summer_swim_way)
    assert bob_plan.concept_exists(summer_hike_way)
    assert bob_plan.concept_exists(sports_swim_way) is False
    assert bob_plan.concept_exists(sports_hike_way) is False


def test_PlanUnit_set_concept_bundling_SetsNewParentWithMassEqualToSumOfAdoptedConcepts():
    bob_plan = planunit_shop("Bob")
    sports_str = "sports"
    sports_way = bob_plan.make_l1_way(sports_str)
    bob_plan.set_l1_concept(conceptunit_shop(sports_str, mass=2))
    swim_str = "swim"
    swim_mass = 3
    bob_plan.set_concept(conceptunit_shop(swim_str, mass=swim_mass), sports_way)
    hike_str = "hike"
    hike_mass = 5
    bob_plan.set_concept(conceptunit_shop(hike_str, mass=hike_mass), sports_way)
    bball_str = "bball"
    bball_mass = 7
    bob_plan.set_concept(conceptunit_shop(bball_str, mass=bball_mass), sports_way)

    sports_swim_way = bob_plan.make_way(sports_way, swim_str)
    sports_hike_way = bob_plan.make_way(sports_way, hike_str)
    sports_bball_way = bob_plan.make_way(sports_way, bball_str)
    assert bob_plan.get_concept_obj(sports_swim_way).mass == swim_mass
    assert bob_plan.get_concept_obj(sports_hike_way).mass == hike_mass
    assert bob_plan.get_concept_obj(sports_bball_way).mass == bball_mass
    summer_str = "summer"
    summer_way = bob_plan.make_way(sports_way, summer_str)
    summer_swim_way = bob_plan.make_way(summer_way, swim_str)
    summer_hike_way = bob_plan.make_way(summer_way, hike_str)
    summer_bball_way = bob_plan.make_way(summer_way, bball_str)
    assert bob_plan.concept_exists(summer_swim_way) is False
    assert bob_plan.concept_exists(summer_hike_way) is False
    assert bob_plan.concept_exists(summer_bball_way) is False

    # WHEN / THEN
    bob_plan.set_concept(
        concept_kid=conceptunit_shop(summer_str),
        parent_way=sports_way,
        adoptees=[swim_str, hike_str],
        bundling=True,
    )

    # THEN
    assert bob_plan.get_concept_obj(summer_way).mass == swim_mass + hike_mass
    assert bob_plan.get_concept_obj(summer_swim_way).mass == swim_mass
    assert bob_plan.get_concept_obj(summer_hike_way).mass == hike_mass
    assert bob_plan.concept_exists(summer_bball_way) is False
    assert bob_plan.concept_exists(sports_swim_way) is False
    assert bob_plan.concept_exists(sports_hike_way) is False
    assert bob_plan.concept_exists(sports_bball_way)


def test_PlanUnit_del_concept_obj_DeletingBundledConceptReturnsConceptsToOriginalState():
    bob_plan = planunit_shop("Bob")
    sports_str = "sports"
    sports_way = bob_plan.make_l1_way(sports_str)
    bob_plan.set_l1_concept(conceptunit_shop(sports_str, mass=2))
    swim_str = "swim"
    swim_mass = 3
    bob_plan.set_concept(conceptunit_shop(swim_str, mass=swim_mass), sports_way)
    hike_str = "hike"
    hike_mass = 5
    bob_plan.set_concept(conceptunit_shop(hike_str, mass=hike_mass), sports_way)
    bball_str = "bball"
    bball_mass = 7
    bob_plan.set_concept(conceptunit_shop(bball_str, mass=bball_mass), sports_way)

    sports_swim_way = bob_plan.make_way(sports_way, swim_str)
    sports_hike_way = bob_plan.make_way(sports_way, hike_str)
    sports_bball_way = bob_plan.make_way(sports_way, bball_str)
    assert bob_plan.get_concept_obj(sports_swim_way).mass == swim_mass
    assert bob_plan.get_concept_obj(sports_hike_way).mass == hike_mass
    assert bob_plan.get_concept_obj(sports_bball_way).mass == bball_mass
    summer_str = "summer"
    summer_way = bob_plan.make_way(sports_way, summer_str)
    summer_swim_way = bob_plan.make_way(summer_way, swim_str)
    summer_hike_way = bob_plan.make_way(summer_way, hike_str)
    summer_bball_way = bob_plan.make_way(summer_way, bball_str)
    assert bob_plan.concept_exists(summer_swim_way) is False
    assert bob_plan.concept_exists(summer_hike_way) is False
    assert bob_plan.concept_exists(summer_bball_way) is False
    bob_plan.set_concept(
        concept_kid=conceptunit_shop(summer_str),
        parent_way=sports_way,
        adoptees=[swim_str, hike_str],
        bundling=True,
    )
    assert bob_plan.get_concept_obj(summer_way).mass == swim_mass + hike_mass
    assert bob_plan.get_concept_obj(summer_swim_way).mass == swim_mass
    assert bob_plan.get_concept_obj(summer_hike_way).mass == hike_mass
    assert bob_plan.concept_exists(summer_bball_way) is False
    assert bob_plan.concept_exists(sports_swim_way) is False
    assert bob_plan.concept_exists(sports_hike_way) is False
    assert bob_plan.concept_exists(sports_bball_way)
    print(f"{bob_plan._concept_dict.keys()=}")

    # WHEN
    bob_plan.del_concept_obj(way=summer_way, del_children=False)

    # THEN
    sports_swim_concept = bob_plan.get_concept_obj(sports_swim_way)
    sports_hike_concept = bob_plan.get_concept_obj(sports_hike_way)
    sports_bball_concept = bob_plan.get_concept_obj(sports_bball_way)
    assert sports_swim_concept.mass == swim_mass
    assert sports_hike_concept.mass == hike_mass
    assert sports_bball_concept.mass == bball_mass


def test_PlanUnit_edit_concept_attr_DeletesConceptUnit_awardlinks():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)
    yao_str = "Yao"
    zia_str = "Zia"
    Xio_str = "Xio"
    yao_plan.add_acctunit(yao_str)
    yao_plan.add_acctunit(zia_str)
    yao_plan.add_acctunit(Xio_str)

    swim_str = "swim"
    swim_way = yao_plan.make_l1_way(swim_str)

    yao_plan.set_l1_concept(conceptunit_shop(swim_str))
    awardlink_yao = awardlink_shop(yao_str, give_force=10)
    awardlink_zia = awardlink_shop(zia_str, give_force=10)
    awardlink_Xio = awardlink_shop(Xio_str, give_force=10)

    swim_concept = yao_plan.get_concept_obj(swim_way)
    yao_plan.edit_concept_attr(swim_way, awardlink=awardlink_yao)
    yao_plan.edit_concept_attr(swim_way, awardlink=awardlink_zia)
    yao_plan.edit_concept_attr(swim_way, awardlink=awardlink_Xio)

    assert len(swim_concept.awardlinks) == 3
    assert len(yao_plan.conceptroot._kids[swim_str].awardlinks) == 3

    # WHEN
    yao_plan.edit_concept_attr(swim_way, awardlink_del=yao_str)

    # THEN
    swim_concept = yao_plan.get_concept_obj(swim_way)
    print(f"{swim_concept.concept_label=}")
    print(f"{swim_concept.awardlinks=}")
    print(f"{swim_concept._awardheirs=}")

    assert len(yao_plan.conceptroot._kids[swim_str].awardlinks) == 2


def test_PlanUnit__get_filtered_awardlinks_concept_CorrectlyRemovesAcct_awardlinks():
    # ESTABLISH
    bob_str = "Bob"
    example_plan = planunit_shop(bob_str)
    xia_str = "Xia"
    run_str = ";runners"
    hike_str = ";hikers"
    example_plan.add_acctunit(xia_str)
    example_plan.get_acct(xia_str).add_membership(run_str)

    sports_str = "sports"
    sports_way = example_plan.make_l1_way(sports_str)
    example_plan.set_l1_concept(conceptunit_shop(sports_str))
    example_plan.edit_concept_attr(sports_way, awardlink=awardlink_shop(run_str))
    example_plan.edit_concept_attr(sports_way, awardlink=awardlink_shop(hike_str))
    example_plan_sports_concept = example_plan.get_concept_obj(sports_way)
    assert len(example_plan_sports_concept.awardlinks) == 2
    bob_plan = planunit_shop(bob_str)
    bob_plan.add_acctunit(xia_str)
    bob_plan.get_acct(xia_str).add_membership(run_str)
    print(f"{example_plan_sports_concept.awardlinks=}")

    # WHEN
    cleaned_concept = bob_plan._get_filtered_awardlinks_concept(
        example_plan_sports_concept
    )

    # THEN
    assert len(cleaned_concept.awardlinks) == 1
    assert list(cleaned_concept.awardlinks.keys()) == [run_str]


def test_PlanUnit__get_filtered_awardlinks_concept_CorrectlyRemovesGroup_awardlink():
    # ESTABLISH
    bob_str = "Bob"
    example_plan = planunit_shop(bob_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    example_plan.add_acctunit(xia_str)
    example_plan.add_acctunit(zoa_str)

    swim_str = "swim"
    swim_way = example_plan.make_l1_way(swim_str)
    example_plan.set_l1_concept(conceptunit_shop(swim_str))
    example_plan.edit_concept_attr(swim_way, awardlink=awardlink_shop(xia_str))
    example_plan.edit_concept_attr(swim_way, awardlink=awardlink_shop(zoa_str))
    example_plan_swim_concept = example_plan.get_concept_obj(swim_way)
    assert len(example_plan_swim_concept.awardlinks) == 2
    bob_plan = planunit_shop(bob_str)
    bob_plan.add_acctunit(xia_str)

    # WHEN
    cleaned_concept = bob_plan._get_filtered_awardlinks_concept(
        example_plan_swim_concept
    )

    # THEN
    assert len(cleaned_concept.awardlinks) == 1
    assert list(cleaned_concept.awardlinks.keys()) == [xia_str]


def test_PlanUnit_set_concept_CorrectlyCleansConcept_awardlinks():
    # ESTABLISH
    bob_str = "Bob"
    example_plan = planunit_shop(bob_str)
    xia_str = "Xia"
    zoa_str = "Zoa"
    example_plan.add_acctunit(xia_str)
    example_plan.add_acctunit(zoa_str)

    casa_str = "casa"
    casa_way = example_plan.make_l1_way(casa_str)
    swim_str = "swim"
    swim_way = example_plan.make_l1_way(swim_str)
    example_plan.set_l1_concept(conceptunit_shop(casa_str))
    example_plan.set_l1_concept(conceptunit_shop(swim_str))
    example_plan.edit_concept_attr(swim_way, awardlink=awardlink_shop(xia_str))
    example_plan.edit_concept_attr(swim_way, awardlink=awardlink_shop(zoa_str))
    example_plan_swim_concept = example_plan.get_concept_obj(swim_way)
    assert len(example_plan_swim_concept.awardlinks) == 2

    # WHEN
    bob_plan = planunit_shop(bob_str)
    bob_plan.add_acctunit(xia_str)
    bob_plan.set_l1_concept(example_plan_swim_concept, create_missing_concepts=False)

    # THEN
    bob_plan_swim_concept = bob_plan.get_concept_obj(swim_way)
    assert len(bob_plan_swim_concept.awardlinks) == 1
    assert list(bob_plan_swim_concept.awardlinks.keys()) == [xia_str]


def test_PlanUnit_get_concept_obj_ReturnsConcept():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    nation_str = "nation"
    nation_way = sue_plan.make_l1_way(nation_str)
    brazil_str = "Brazil"
    brazil_way = sue_plan.make_way(nation_way, brazil_str)

    # WHEN
    brazil_concept = sue_plan.get_concept_obj(way=brazil_way)

    # THEN
    assert brazil_concept is not None
    assert brazil_concept.concept_label == brazil_str

    # WHEN
    wk_str = "wkdays"
    wk_way = sue_plan.make_l1_way(wk_str)
    wk_concept = sue_plan.get_concept_obj(way=wk_way)

    # THEN
    assert wk_concept is not None
    assert wk_concept.concept_label == wk_str

    # WHEN
    root_concept = sue_plan.get_concept_obj(to_way(sue_plan.vow_label))

    # THEN
    assert root_concept is not None
    assert root_concept.concept_label == sue_plan.vow_label

    # WHEN / THEN
    bobdylan_str = "bobdylan"
    wrong_way = sue_plan.make_l1_way(bobdylan_str)
    with pytest_raises(Exception) as excinfo:
        sue_plan.get_concept_obj(way=wrong_way)
    assert str(excinfo.value) == f"get_concept_obj failed. no concept at '{wrong_way}'"


def test_PlanUnit_concept_exists_ReturnsCorrectBool():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    cat_way = sue_plan.make_l1_way("cat have dinner")
    wk_way = sue_plan.make_l1_way("wkdays")
    casa_way = sue_plan.make_l1_way("casa")
    nation_way = sue_plan.make_l1_way("nation")
    sun_way = sue_plan.make_way(wk_way, "Sunday")
    mon_way = sue_plan.make_way(wk_way, "Monday")
    tue_way = sue_plan.make_way(wk_way, "Tuesday")
    wed_way = sue_plan.make_way(wk_way, "Wednesday")
    thu_way = sue_plan.make_way(wk_way, "Thursday")
    fri_way = sue_plan.make_way(wk_way, "Friday")
    sat_way = sue_plan.make_way(wk_way, "Saturday")
    france_way = sue_plan.make_way(nation_way, "France")
    brazil_way = sue_plan.make_way(nation_way, "Brazil")
    usa_way = sue_plan.make_way(nation_way, "USA")
    texas_way = sue_plan.make_way(usa_way, "Texas")
    oregon_way = sue_plan.make_way(usa_way, "Oregon")
    # do not exist in plan
    sports_way = sue_plan.make_l1_way("sports")
    swim_way = sue_plan.make_way(sports_way, "swimming")
    idaho_way = sue_plan.make_way(usa_way, "Idaho")
    japan_way = sue_plan.make_way(nation_way, "Japan")

    # WHEN / THEN
    assert sue_plan.concept_exists("") is False
    assert sue_plan.concept_exists(None) is False
    assert sue_plan.concept_exists(to_way(sue_plan.vow_label))
    assert sue_plan.concept_exists(cat_way)
    assert sue_plan.concept_exists(wk_way)
    assert sue_plan.concept_exists(casa_way)
    assert sue_plan.concept_exists(nation_way)
    assert sue_plan.concept_exists(sun_way)
    assert sue_plan.concept_exists(mon_way)
    assert sue_plan.concept_exists(tue_way)
    assert sue_plan.concept_exists(wed_way)
    assert sue_plan.concept_exists(thu_way)
    assert sue_plan.concept_exists(fri_way)
    assert sue_plan.concept_exists(sat_way)
    assert sue_plan.concept_exists(usa_way)
    assert sue_plan.concept_exists(france_way)
    assert sue_plan.concept_exists(brazil_way)
    assert sue_plan.concept_exists(texas_way)
    assert sue_plan.concept_exists(oregon_way)
    assert sue_plan.concept_exists(to_way("B")) is False
    assert sue_plan.concept_exists(sports_way) is False
    assert sue_plan.concept_exists(swim_way) is False
    assert sue_plan.concept_exists(idaho_way) is False
    assert sue_plan.concept_exists(japan_way) is False


def test_PlanUnit_set_offtrack_fund_ReturnsObj():
    # ESTABLISH
    bob_planunit = planunit_shop("Bob")
    assert not bob_planunit._offtrack_fund

    # WHEN
    bob_planunit.set_offtrack_fund() == 0

    # THEN
    assert bob_planunit._offtrack_fund == 0

    # ESTABLISH
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wednesday"
    casa_way = bob_planunit.make_l1_way(casa_str)
    wk_way = bob_planunit.make_l1_way(wk_str)
    wed_way = bob_planunit.make_way(wk_way, wed_str)
    casa_concept = conceptunit_shop(casa_str, _fund_onset=70, _fund_cease=170)
    wk_concept = conceptunit_shop(wk_str, _fund_onset=70, _fund_cease=75)
    wed_concept = conceptunit_shop(wed_str, _fund_onset=72, _fund_cease=75)
    casa_concept.parent_way = bob_planunit.vow_label
    wk_concept.parent_way = bob_planunit.vow_label
    wed_concept.parent_way = wk_way
    bob_planunit.set_l1_concept(casa_concept)
    bob_planunit.set_l1_concept(wk_concept)
    bob_planunit.set_concept(wed_concept, wk_way)
    bob_planunit._offtrack_kids_mass_set.add(casa_way)
    bob_planunit._offtrack_kids_mass_set.add(wk_way)
    assert bob_planunit._offtrack_fund == 0

    # WHEN
    bob_planunit.set_offtrack_fund()

    # THEN
    assert bob_planunit._offtrack_fund == 105

    # WHEN
    bob_planunit._offtrack_kids_mass_set.add(wed_way)
    bob_planunit.set_offtrack_fund()

    # THEN
    assert bob_planunit._offtrack_fund == 108


def test_PlanUnit_allot_offtrack_fund_SetsCharUnit_fund_take_fund_give():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    bob_planunit = planunit_shop(bob_str)
    bob_planunit.add_acctunit(bob_str)
    bob_planunit.add_acctunit(yao_str, credit_score=2)
    bob_planunit.add_acctunit(sue_str, debtit_score=2)
    bob_planunit.set_offtrack_fund()
    assert bob_planunit._offtrack_fund == 0

    # WHEN
    bob_planunit._allot_offtrack_fund()

    # THEN
    assert bob_planunit.get_acct(bob_str)._fund_give == 0
    assert bob_planunit.get_acct(bob_str)._fund_take == 0
    assert bob_planunit.get_acct(yao_str)._fund_give == 0
    assert bob_planunit.get_acct(yao_str)._fund_take == 0
    assert bob_planunit.get_acct(sue_str)._fund_give == 0
    assert bob_planunit.get_acct(sue_str)._fund_take == 0

    # WHEN
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wednesday"
    casa_way = bob_planunit.make_l1_way(casa_str)
    wk_way = bob_planunit.make_l1_way(wk_str)
    wed_way = bob_planunit.make_way(wk_way, wed_str)
    casa_concept = conceptunit_shop(casa_str, _fund_onset=70, _fund_cease=170)
    wk_concept = conceptunit_shop(wk_str, _fund_onset=70, _fund_cease=75)
    wed_concept = conceptunit_shop(wed_str, _fund_onset=72, _fund_cease=75)
    casa_concept.parent_way = bob_planunit.vow_label
    wk_concept.parent_way = bob_planunit.vow_label
    wed_concept.parent_way = wk_way
    bob_planunit.set_l1_concept(casa_concept)
    bob_planunit.set_l1_concept(wk_concept)
    bob_planunit.set_concept(wed_concept, wk_way)
    bob_planunit._offtrack_kids_mass_set.add(casa_way)
    bob_planunit._offtrack_kids_mass_set.add(wk_way)
    bob_planunit.set_offtrack_fund()
    assert bob_planunit._offtrack_fund == 105

    # WHEN
    bob_planunit._allot_offtrack_fund()

    # THEN
    assert bob_planunit.get_acct(bob_str)._fund_give == 26
    assert bob_planunit.get_acct(bob_str)._fund_take == 26
    assert bob_planunit.get_acct(yao_str)._fund_give == 53
    assert bob_planunit.get_acct(yao_str)._fund_take == 26
    assert bob_planunit.get_acct(sue_str)._fund_give == 26
    assert bob_planunit.get_acct(sue_str)._fund_take == 53

    bob_planunit._offtrack_kids_mass_set.add(wed_way)
    bob_planunit.set_offtrack_fund()

    # THEN
    assert bob_planunit._offtrack_fund == 108
