from pytest import raises as pytest_raises
from src.a04_reason_logic.reason_plan import (
    caseunit_shop,
    reasonheir_shop,
    reasonunit_shop,
)
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.example_believers import (
    get_believerunit_irrational_example,
    get_believerunit_with_4_levels,
)


def test_BelieverUnit_ReasonUnits_create():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    sem_jour_str = "sem_jours"
    sem_jour_rope = sue_believer.make_l1_rope(sem_jour_str)
    wed_str = "Wed"
    wed_rope = sue_believer.make_rope(sem_jour_rope, wed_str)

    wed_case = caseunit_shop(reason_state=wed_rope)
    casa_wk_reason = reasonunit_shop(sem_jour_rope, {wed_case.reason_state: wed_case})
    print(f"{type(casa_wk_reason.reason_context)=}")
    print(f"{casa_wk_reason.reason_context=}")

    # WHEN
    sue_believer.edit_plan_attr(casa_rope, reason=casa_wk_reason)

    # THEN
    casa_plan = sue_believer.get_plan_obj(casa_rope)
    assert casa_plan.reasonunits is not None
    print(casa_plan.reasonunits)
    assert casa_plan.reasonunits[sem_jour_rope] is not None
    assert casa_plan.reasonunits[sem_jour_rope] == casa_wk_reason


def test_BelieverUnit_edit_plan_attr_reasonunit_CorrectlySets_knot():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    casa_rope = sue_believer.make_l1_rope("casa")
    wk_rope = sue_believer.make_l1_rope("sem_jours")
    wed_rope = sue_believer.make_rope(wk_rope, "Wed")

    slash_str = "/"
    before_wk_reason = reasonunit_shop(wk_rope, knot=slash_str)
    before_wk_reason.set_case(wed_rope)
    assert before_wk_reason.knot == slash_str

    # WHEN
    sue_believer.edit_plan_attr(casa_rope, reason=before_wk_reason)

    # THEN
    casa_plan = sue_believer.get_plan_obj(casa_rope)
    wk_reasonunit = casa_plan.reasonunits.get(wk_rope)
    assert wk_reasonunit.knot != slash_str
    assert wk_reasonunit.knot == sue_believer.knot


def test_BelieverUnit_edit_plan_attr_reason_context_CorrectlySets_knot():
    # ESTABLISH
    slash_str = "/"
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
    wed_plan = bob_believer.get_plan_obj(wed_rope)
    assert wed_plan.knot == slash_str
    assert wed_plan.knot == bob_believer.knot

    # WHEN
    bob_believer.edit_plan_attr(casa_rope, reason_context=wk_rope, reason_case=wed_rope)

    # THEN
    casa_plan = bob_believer.get_plan_obj(casa_rope)
    assert casa_plan.knot == slash_str
    wk_reasonunit = casa_plan.reasonunits.get(wk_rope)
    assert wk_reasonunit.knot != ","
    assert wk_reasonunit.knot == bob_believer.knot


def test_BelieverUnit_set_reasonunits_status():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    sem_jour_str = "sem_jours"
    sem_jour_rope = sue_believer.make_l1_rope(sem_jour_str)
    wed_str = "Wed"
    wed_rope = sue_believer.make_rope(sem_jour_rope, wed_str)

    wed_case = caseunit_shop(reason_state=wed_rope)
    casa_wk_reason = reasonunit_shop(
        reason_context=sem_jour_rope, cases={wed_case.reason_state: wed_case}
    )
    print(f"{type(casa_wk_reason.reason_context)=}")
    print(f"{casa_wk_reason.reason_context=}")

    # WHEN
    sue_believer.edit_plan_attr(casa_rope, reason=casa_wk_reason)

    # THEN
    casa_plan = sue_believer.get_plan_obj(casa_rope)
    assert casa_plan.reasonunits is not None
    print(casa_plan.reasonunits)
    assert casa_plan.reasonunits[sem_jour_rope] is not None
    assert casa_plan.reasonunits[sem_jour_rope] == casa_wk_reason


def test_agenda_returned_WhenNoReasonsExist():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()

    # WHEN
    sue_believer.settle_believer()

    # THEN
    casa_rope = sue_believer.make_l1_rope("casa")
    assert sue_believer.get_plan_obj(casa_rope)._chore is True
    cat_rope = sue_believer.make_l1_rope("cat have dinner")
    assert sue_believer.get_plan_obj(cat_rope)._chore is True


def test_BelieverUnit_reasonheirs_AreCorrectlyInherited_v1():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    casa_rope = sue_believer.make_l1_rope("casa")
    wk_rope = sue_believer.make_l1_rope("sem_jours")
    tue_rope = sue_believer.make_rope(wk_rope, "Tue")
    casa_wk_build_reasonunit = reasonunit_shop(wk_rope)
    casa_wk_build_reasonunit.set_case(tue_rope)
    sue_believer.edit_plan_attr(casa_rope, reason=casa_wk_build_reasonunit)
    casa_plan = sue_believer.get_plan_obj(casa_rope)
    assert casa_plan.reasonunits != {}
    assert casa_plan.get_reasonunit(wk_rope)
    assert casa_plan.get_reasonunit(wk_rope) == casa_wk_build_reasonunit
    assert not casa_plan.get_reasonheir(wk_rope)

    # WHEN
    sue_believer.settle_believer()

    # THEN
    assert casa_plan.get_reasonheir(wk_rope)
    assert len(casa_plan.get_reasonheir(wk_rope).cases) == 1
    assert casa_plan.get_reasonheir(wk_rope).get_case(tue_rope)
    case_tue = casa_plan.get_reasonheir(wk_rope).get_case(tue_rope)
    tue_case = caseunit_shop(reason_state=tue_rope)
    tue_case._status = False
    tue_case._chore = False
    cases = {tue_case.reason_state: tue_case}
    built_wk_reasonheir = reasonheir_shop(
        reason_context=wk_rope,
        cases=cases,
        _status=False,
        _rplan_active_value=True,
    )
    tue_chore = built_wk_reasonheir.cases.get(case_tue.reason_state)._chore
    assert case_tue._chore == tue_chore
    assert case_tue == built_wk_reasonheir.cases[case_tue.reason_state]
    wk_reasonheir = casa_plan.get_reasonheir(wk_rope)
    assert wk_reasonheir.cases == built_wk_reasonheir.cases
    assert casa_plan.get_reasonheir(wk_rope) == built_wk_reasonheir


def test_BelieverUnit_reasonheirs_AreCorrectlyInheritedTo4LevelsFromRoot():
    # ESTABLISH
    a4_believer = get_believerunit_with_4_levels()
    casa_str = "casa"
    casa_rope = a4_believer.make_l1_rope(casa_str)
    wk_str = "sem_jours"
    wk_rope = a4_believer.make_l1_rope(wk_str)
    wed_str = "Wed"
    wed_rope = a4_believer.make_rope(wk_rope, wed_str)

    wed_case = caseunit_shop(reason_state=wed_rope)
    wed_case._status = False
    wed_case._chore = False

    cases_x = {wed_case.reason_state: wed_case}
    casa_wk_build_reasonunit = reasonunit_shop(reason_context=wk_rope, cases=cases_x)
    casa_wk_built_reasonheir = reasonheir_shop(
        reason_context=wk_rope,
        cases=cases_x,
        _status=False,
        _rplan_active_value=True,
    )
    a4_believer.edit_plan_attr(casa_rope, reason=casa_wk_build_reasonunit)

    # WHEN
    rla_str = "hp"
    rla_rope = a4_believer.make_rope(casa_rope, rla_str)
    a4_believer.set_plan(planunit_shop(rla_str), parent_rope=rla_rope)
    cost_str = "cost_quantification"
    cost_rope = a4_believer.make_rope(rla_rope, cost_str)
    a4_believer.set_plan(planunit_shop(cost_str), parent_rope=cost_rope)
    a4_believer.settle_believer()

    # THEN
    casa_plan = a4_believer.planroot._kids[casa_str]
    rla_plan = casa_plan._kids[rla_str]
    cost_plan = rla_plan._kids[cost_str]

    # 1
    casa_wk_calc_reasonheir = casa_plan._reasonheirs[wk_rope]
    assert casa_wk_calc_reasonheir == casa_wk_built_reasonheir

    # 2
    rla_wk_reasonheir = rla_plan._reasonheirs[wk_rope]
    assert rla_wk_reasonheir.reason_context == casa_wk_built_reasonheir.reason_context
    assert rla_wk_reasonheir.cases == casa_wk_built_reasonheir.cases
    assert (
        rla_wk_reasonheir.reason_active_requisite
        == casa_wk_built_reasonheir.reason_active_requisite
    )
    assert rla_wk_reasonheir._status == casa_wk_built_reasonheir._status
    assert rla_wk_reasonheir._chore == casa_wk_built_reasonheir._chore
    assert rla_wk_reasonheir._rplan_active_value
    assert rla_wk_reasonheir._rplan_active_value != casa_wk_built_reasonheir

    # 3
    cost_wk_reasonheir = cost_plan._reasonheirs[wk_rope]
    assert cost_wk_reasonheir.reason_context == casa_wk_built_reasonheir.reason_context
    assert cost_wk_reasonheir.cases == casa_wk_built_reasonheir.cases
    assert (
        cost_wk_reasonheir.reason_active_requisite
        == casa_wk_built_reasonheir.reason_active_requisite
    )
    assert cost_wk_reasonheir._status == casa_wk_built_reasonheir._status
    assert cost_wk_reasonheir._chore == casa_wk_built_reasonheir._chore
    assert cost_wk_reasonheir._rplan_active_value
    assert cost_wk_reasonheir._rplan_active_value != casa_wk_built_reasonheir


def test_BelieverUnit_reasonheirs_AreCorrectlyInheritedTo4LevelsFromLevel2():
    a4_believer = get_believerunit_with_4_levels()
    casa_str = "casa"
    casa_rope = a4_believer.make_l1_rope(casa_str)
    wk_plan_label = "sem_jours"
    wk_rope = a4_believer.make_l1_rope(wk_plan_label)
    wed_str = "Wed"
    wed_rope = a4_believer.make_rope(wk_rope, wed_str)

    wed_case = caseunit_shop(reason_state=wed_rope)
    wed_case._status = False
    wed_case._chore = False
    cases = {wed_case.reason_state: wed_case}
    casa_wk_build_reasonunit = reasonunit_shop(wk_rope, cases=cases)
    casa_wk_built_reasonheir = reasonheir_shop(
        reason_context=wk_rope,
        cases=cases,
        _status=False,
        _rplan_active_value=True,
    )
    a4_believer.edit_plan_attr(casa_rope, reason=casa_wk_build_reasonunit)
    rla_str = "hp"
    rla_rope = a4_believer.make_rope(casa_rope, rla_str)
    a4_believer.set_plan(planunit_shop(rla_str), parent_rope=rla_rope)
    cost_str = "cost_quantification"
    cost_rope = a4_believer.make_rope(rla_rope, cost_str)
    a4_believer.set_plan(planunit_shop(cost_str), parent_rope=cost_rope)

    casa_plan = a4_believer.planroot.get_kid(casa_str)
    rla_plan = casa_plan.get_kid(rla_str)
    cost_plan = rla_plan.get_kid(cost_str)

    assert a4_believer.planroot._reasonheirs == {}
    assert casa_plan._reasonheirs == {}
    assert rla_plan._reasonheirs == {}
    assert cost_plan._reasonheirs == {}

    # WHEN
    a4_believer.settle_believer()

    # THEN
    assert a4_believer.planroot._reasonheirs == {}  # casa_wk_built_reasonheir

    # 1
    assert casa_plan._reasonheirs[wk_rope] == casa_wk_built_reasonheir

    # 2
    rla_wk_reasonheir = rla_plan._reasonheirs[wk_rope]
    assert rla_wk_reasonheir.reason_context == casa_wk_built_reasonheir.reason_context
    assert rla_wk_reasonheir.cases == casa_wk_built_reasonheir.cases
    assert (
        rla_wk_reasonheir.reason_active_requisite
        == casa_wk_built_reasonheir.reason_active_requisite
    )
    assert rla_wk_reasonheir._status == casa_wk_built_reasonheir._status
    assert rla_wk_reasonheir._chore == casa_wk_built_reasonheir._chore
    assert rla_wk_reasonheir._rplan_active_value
    assert rla_wk_reasonheir._rplan_active_value != casa_wk_built_reasonheir

    # 3
    cost_wk_reasonheir = cost_plan._reasonheirs[wk_rope]
    assert cost_wk_reasonheir.reason_context == casa_wk_built_reasonheir.reason_context
    assert cost_wk_reasonheir.cases == casa_wk_built_reasonheir.cases
    assert (
        cost_wk_reasonheir.reason_active_requisite
        == casa_wk_built_reasonheir.reason_active_requisite
    )
    assert cost_wk_reasonheir._status == casa_wk_built_reasonheir._status
    assert cost_wk_reasonheir._chore == casa_wk_built_reasonheir._chore
    assert cost_wk_reasonheir._rplan_active_value
    assert cost_wk_reasonheir._rplan_active_value != casa_wk_built_reasonheir


def test_BelieverUnit_ReasonUnits_set_UnCoupledMethod():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    wk_str = "sem_jours"
    wk_rope = sue_believer.make_l1_rope(wk_str)
    wed_str = "Wed"
    wed_rope = sue_believer.make_rope(wk_rope, wed_str)

    # WHEN
    sue_believer.edit_plan_attr(casa_rope, reason_context=wk_rope, reason_case=wed_rope)

    # THEN
    casa_plan1 = sue_believer.get_plan_obj(casa_rope)
    assert casa_plan1.reasonunits is not None
    print(casa_plan1.reasonunits)
    assert casa_plan1.reasonunits[wk_rope] is not None
    assert casa_plan1.reasonunits[wk_rope].cases[wed_rope].reason_lower is None
    assert casa_plan1.reasonunits[wk_rope].cases[wed_rope].reason_upper is None

    casa_wk_reason1 = reasonunit_shop(wk_rope)
    casa_wk_reason1.set_case(case=wed_rope)
    print(f" {type(casa_wk_reason1.reason_context)=}")
    print(f" {casa_wk_reason1.reason_context=}")
    assert casa_plan1.reasonunits[wk_rope] == casa_wk_reason1

    # ESTABLISH
    reason_divisor_x = 34
    x_reason_lower = 12
    x_reason_upper = 12

    # WHEN
    sue_believer.edit_plan_attr(
        casa_rope,
        reason_context=wk_rope,
        reason_case=wed_rope,
        reason_divisor=reason_divisor_x,
        reason_lower=x_reason_lower,
        reason_upper=x_reason_upper,
    )

    # THEN
    assert casa_plan1.reasonunits[wk_rope].cases[wed_rope].reason_lower == 12
    assert casa_plan1.reasonunits[wk_rope].cases[wed_rope].reason_upper == 12

    wed_case2 = caseunit_shop(
        wed_rope,
        reason_divisor=reason_divisor_x,
        reason_lower=x_reason_lower,
        reason_upper=x_reason_upper,
    )
    casa_wk_reason2 = reasonunit_shop(
        reason_context=wk_rope, cases={wed_case2.reason_state: wed_case2}
    )
    print(f"{type(casa_wk_reason2.reason_context)=}")
    print(f"{casa_wk_reason2.reason_context=}")
    assert casa_plan1.reasonunits[wk_rope] == casa_wk_reason2

    # WHEN
    thu_str = "Thur"
    thu_rope = sue_believer.make_rope(wk_rope, thu_str)
    sue_believer.edit_plan_attr(
        casa_rope,
        reason_context=wk_rope,
        reason_case=thu_rope,
        reason_divisor=reason_divisor_x,
        reason_lower=x_reason_lower,
        reason_upper=x_reason_upper,
    )

    # THEN
    assert len(casa_plan1.reasonunits[wk_rope].cases) == 2


def test_BelieverUnit_ReasonUnits_set_casePlanWithDenomSetsCaseDivision():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    ziet_str = "ziet"
    ziet_rope = sue_believer.make_l1_rope(ziet_str)
    wk_str = "wk"
    wk_rope = sue_believer.make_rope(ziet_rope, wk_str)
    sue_believer.set_l1_plan(planunit_shop(ziet_str, begin=100, close=2000))
    sue_believer.set_plan(planunit_shop(wk_str, denom=7), parent_rope=ziet_rope)

    # WHEN
    sue_believer.edit_plan_attr(
        casa_rope,
        reason_context=ziet_rope,
        reason_case=wk_rope,
        reason_lower=2,
        reason_upper=5,
        reason_divisor=None,
    )

    # THEN
    casa_plan1 = sue_believer.get_plan_obj(casa_rope)
    assert casa_plan1.reasonunits[ziet_rope] is not None
    assert casa_plan1.reasonunits[ziet_rope].cases[wk_rope].reason_divisor == 7
    assert casa_plan1.reasonunits[ziet_rope].cases[wk_rope].reason_lower == 2
    assert casa_plan1.reasonunits[ziet_rope].cases[wk_rope].reason_upper == 5


def test_BelieverUnit_ReasonUnits_set_casePlanWithBeginCloseSetsCasereason_lower_reason_upper():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    casa = "casa"
    casa_rope = sue_believer.make_l1_rope(casa)
    ziet = "ziet"
    ziet_rope = sue_believer.make_l1_rope(ziet)
    rus_war = "rus_war"
    rus_war_rope = sue_believer.make_rope(ziet_rope, rus_war)
    sue_believer.set_plan(
        planunit_shop(ziet, begin=100, close=2000), sue_believer.belief_label
    )
    sue_believer.set_plan(planunit_shop(rus_war, begin=22, close=34), ziet_rope)

    # WHEN
    sue_believer.edit_plan_attr(
        casa_rope,
        reason_context=ziet_rope,
        reason_case=rus_war_rope,
        reason_lower=None,
        reason_upper=None,
        reason_divisor=None,
    )

    # THEN
    casa_plan1 = sue_believer.get_plan_obj(casa_rope)
    assert casa_plan1.reasonunits[ziet_rope] is not None
    assert casa_plan1.reasonunits[ziet_rope].cases[rus_war_rope].reason_divisor is None
    assert casa_plan1.reasonunits[ziet_rope].cases[rus_war_rope].reason_lower == 22
    assert casa_plan1.reasonunits[ziet_rope].cases[rus_war_rope].reason_upper == 34


def test_BelieverUnit_ReasonUnits_edit_plan_attr_CorrectlyDeletes_ReasonUnits_And_CaseUnits():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    casa_rope = sue_believer.make_l1_rope("casa")
    sem_jour_rope = sue_believer.make_l1_rope("sem_jours")
    wed_rope = sue_believer.make_rope(sem_jour_rope, "Wed")

    sue_believer.edit_plan_attr(
        casa_rope, reason_context=sem_jour_rope, reason_case=wed_rope
    )
    thu_rope = sue_believer.make_rope(sem_jour_rope, "Thur")
    sue_believer.edit_plan_attr(
        casa_rope,
        reason_context=sem_jour_rope,
        reason_case=thu_rope,
    )
    casa_plan1 = sue_believer.get_plan_obj(casa_rope)
    assert len(casa_plan1.reasonunits[sem_jour_rope].cases) == 2

    # WHEN
    sue_believer.edit_plan_attr(
        casa_rope,
        reason_del_case_reason_context=sem_jour_rope,
        reason_del_case_reason_state=thu_rope,
    )

    # THEN
    assert len(casa_plan1.reasonunits[sem_jour_rope].cases) == 1

    # WHEN
    sue_believer.edit_plan_attr(
        casa_rope,
        reason_del_case_reason_context=sem_jour_rope,
        reason_del_case_reason_state=wed_rope,
    )

    # THEN
    with pytest_raises(KeyError) as excinfo:
        casa_plan1.reasonunits[sem_jour_rope]
    assert str(excinfo.value) == f"'{sem_jour_rope}'"
    assert casa_plan1.reasonunits == {}


def test_BelieverUnit_ReasonUnits_del_reason_case_UncoupledMethod2():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    casa_rope = sue_believer.make_l1_rope("casa")
    sem_jours_rope = sue_believer.make_l1_rope("sem_jours")
    casa_plan1 = sue_believer.get_plan_obj(casa_rope)
    assert len(casa_plan1.reasonunits) == 0

    # WHEN
    with pytest_raises(Exception) as excinfo:
        casa_plan1.del_reasonunit_reason_context(sem_jours_rope)
    assert str(excinfo.value) == f"No ReasonUnit at '{sem_jours_rope}'"


def test_BelieverUnit_edit_plan_attr_believerIsAbleToEdit_reason_active_requisite_AnyPlanIfInvaildThrowsError():
    # _reason_active_requisite: str = None
    # must be 1 of 3: bool: True, bool: False, str="Set to Ignore"
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)

    run_str = "run to casa"
    run_rope = sue_believer.make_l1_rope(run_str)
    sue_believer.set_plan(planunit_shop(run_str), sue_believer.belief_label)
    sue_believer.settle_believer()  # set tree metrics
    run_plan = sue_believer.get_plan_obj(run_rope)
    assert len(run_plan.reasonunits) == 0

    # WHEN
    sue_believer.edit_plan_attr(
        run_rope,
        reason_context=casa_rope,
        reason_plan_active_requisite=True,
    )

    # THEN
    assert len(run_plan.reasonunits) == 1
    reasonunit_casa = run_plan.reasonunits.get(casa_rope)
    assert reasonunit_casa.reason_context == casa_rope
    assert len(reasonunit_casa.cases) == 0
    assert reasonunit_casa.reason_active_requisite is True

    # WHEN
    sue_believer.edit_plan_attr(
        run_rope,
        reason_context=casa_rope,
        reason_plan_active_requisite=False,
    )

    # THEN
    assert len(run_plan.reasonunits) == 1
    reasonunit_casa = run_plan.reasonunits.get(casa_rope)
    assert reasonunit_casa.reason_context == casa_rope
    assert len(reasonunit_casa.cases) == 0
    assert reasonunit_casa.reason_active_requisite is False

    # WHEN
    sue_believer.edit_plan_attr(
        run_rope,
        reason_context=casa_rope,
        reason_plan_active_requisite="Set to Ignore",
    )

    # THEN
    assert len(run_plan.reasonunits) == 1
    reasonunit_casa = run_plan.reasonunits.get(casa_rope)
    assert reasonunit_casa.reason_context == casa_rope
    assert len(reasonunit_casa.cases) == 0
    assert reasonunit_casa.reason_active_requisite is None


def test_BelieverUnit_ReasonUnits_PlanUnit_active_InfluencesReasonUnitStatus():
    # ESTABLISH an Believer with 5 plans, 1 Fact:
    # 1. plan(...,sem_jours) exists
    # 2. plan(...,sem_jours,wed) exists
    # 3. plan(...,sem_jours,thur) exists
    sue_believer = get_believerunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_believer.make_l1_rope(casa_str)
    sem_jours_str = "sem_jours"
    sem_jours_rope = sue_believer.make_l1_rope(sem_jours_str)
    wed_str = "Wed"
    wed_rope = sue_believer.make_rope(sem_jours_rope, wed_str)
    thu_str = "Thur"
    thu_rope = sue_believer.make_rope(sem_jours_rope, thu_str)

    # 4. plan(...,casa) with
    # 4.1 ReasonUnit: reason_context=sem_jours_rope, reason_state=thu_rope
    # 4.2 .active = False
    sue_believer.edit_plan_attr(
        casa_rope,
        reason_context=sem_jours_rope,
        reason_case=thu_rope,
    )
    sue_believer.settle_believer()  # set tree metrics
    casa_plan = sue_believer.get_plan_obj(casa_rope)
    assert casa_plan._active is False

    # 5. plan(...,run to casa) with
    # 5.1. ReasonUnit: plan(reason_context=...,casa) has .reason_active_requisite = True
    # 5.2. plan(...,casa).active = False
    run_str = "run to casa"
    run_rope = sue_believer.make_l1_rope(run_str)
    sue_believer.set_plan(planunit_shop(run_str), sue_believer.belief_label)
    sue_believer.edit_plan_attr(
        run_rope,
        reason_context=casa_rope,
        reason_plan_active_requisite=True,
    )
    run_plan = sue_believer.get_plan_obj(run_rope)
    sue_believer.settle_believer()
    assert run_plan._active is False

    # Fact: reason_context: (...,sem_jours) fact_state: (...,sem_jours,wed)
    sue_believer.add_fact(fact_context=sem_jours_rope, fact_state=wed_rope)
    sue_believer.settle_believer()

    assert casa_plan._active is False
    assert run_plan._active is False

    # WHEN
    print("before changing fact")
    sue_believer.add_fact(fact_context=sem_jours_rope, fact_state=thu_rope)
    print("after changing fact")
    sue_believer.settle_believer()
    assert casa_plan._active is True

    # THEN
    assert run_plan._active is True


def test_BelieverUnit_settle_believer_SetsRationalAttrToFalseWhen_max_tree_traverse_Is1():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    assert sue_believer._rational is False
    # sue_believer.settle_believer()
    sue_believer._rational = True
    assert sue_believer._rational

    # WHEN
    # hack believer to set _max_tree_traverse = 1 (not allowed, should be 2 or more)
    sue_believer.max_tree_traverse = 1
    sue_believer.settle_believer()

    # THEN
    assert not sue_believer._rational


def test_BelieverUnit_tree_traverse_count_SetByTotalNumberOfTreeTraversesEndsStatusIsDetected():
    # ESTABLISH
    sue_believer = get_believerunit_with_4_levels()
    assert sue_believer.max_tree_traverse != 2

    # WHEN
    sue_believer.settle_believer()
    # for plan_key in sue_believer._plan_dict.keys():
    #     print(f"{plan_key=}")

    # THEN
    assert sue_believer._tree_traverse_count == 2


def test_BelieverUnit_tree_traverse_count_CorrectlyCountsTreeTraversesForIrrationalBelievers():
    # ESTABLISH irrational believer
    sue_believer = get_believerunit_irrational_example()
    sue_believer.settle_believer()
    assert sue_believer._tree_traverse_count == 3

    # WHEN
    sue_believer.set_max_tree_traverse(21)
    sue_believer.settle_believer()

    # THEN
    assert sue_believer._tree_traverse_count == 21
