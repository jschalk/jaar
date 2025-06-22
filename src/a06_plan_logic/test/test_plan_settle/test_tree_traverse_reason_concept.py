from pytest import raises as pytest_raises
from src.a04_reason_logic.reason_concept import (
    premiseunit_shop,
    reasonheir_shop,
    reasonunit_shop,
)
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.test._util.example_plans import (
    get_planunit_irrational_example,
    get_planunit_with_4_levels,
)


def test_PlanUnit_ReasonUnits_create():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    wkday_str = "wkdays"
    wkday_rope = sue_plan.make_l1_rope(wkday_str)
    wed_str = "Wednesday"
    wed_rope = sue_plan.make_rope(wkday_rope, wed_str)

    wed_premise = premiseunit_shop(pstate=wed_rope)
    casa_wk_reason = reasonunit_shop(wkday_rope, {wed_premise.pstate: wed_premise})
    print(f"{type(casa_wk_reason.rcontext)=}")
    print(f"{casa_wk_reason.rcontext=}")

    # WHEN
    sue_plan.edit_concept_attr(casa_rope, reason=casa_wk_reason)

    # THEN
    casa_concept = sue_plan.get_concept_obj(casa_rope)
    assert casa_concept.reasonunits is not None
    print(casa_concept.reasonunits)
    assert casa_concept.reasonunits[wkday_rope] is not None
    assert casa_concept.reasonunits[wkday_rope] == casa_wk_reason


def test_PlanUnit_edit_concept_attr_reasonunit_CorrectlySets_knot():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope("casa")
    wk_rope = sue_plan.make_l1_rope("wkdays")
    wed_rope = sue_plan.make_rope(wk_rope, "Wednesday")

    slash_str = "/"
    before_wk_reason = reasonunit_shop(wk_rope, knot=slash_str)
    before_wk_reason.set_premise(wed_rope)
    assert before_wk_reason.knot == slash_str

    # WHEN
    sue_plan.edit_concept_attr(casa_rope, reason=before_wk_reason)

    # THEN
    casa_concept = sue_plan.get_concept_obj(casa_rope)
    wk_reasonunit = casa_concept.reasonunits.get(wk_rope)
    assert wk_reasonunit.knot != slash_str
    assert wk_reasonunit.knot == sue_plan.knot


def test_PlanUnit_edit_concept_attr_reason_rcontext_CorrectlySets_knot():
    # ESTABLISH
    slash_str = "/"
    bob_plan = planunit_shop("Bob", knot=slash_str)
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wednesday"
    casa_rope = bob_plan.make_l1_rope(casa_str)
    wk_rope = bob_plan.make_l1_rope(wk_str)
    wed_rope = bob_plan.make_rope(wk_rope, wed_str)
    bob_plan.set_l1_concept(conceptunit_shop(casa_str))
    bob_plan.set_l1_concept(conceptunit_shop(wk_str))
    bob_plan.set_concept(conceptunit_shop(wed_str), wk_rope)
    print(f"{bob_plan.conceptroot._kids.keys()=}")
    wed_concept = bob_plan.get_concept_obj(wed_rope)
    assert wed_concept.knot == slash_str
    assert wed_concept.knot == bob_plan.knot

    # WHEN
    bob_plan.edit_concept_attr(
        casa_rope, reason_rcontext=wk_rope, reason_premise=wed_rope
    )

    # THEN
    casa_concept = bob_plan.get_concept_obj(casa_rope)
    assert casa_concept.knot == slash_str
    wk_reasonunit = casa_concept.reasonunits.get(wk_rope)
    assert wk_reasonunit.knot != ","
    assert wk_reasonunit.knot == bob_plan.knot


def test_PlanUnit_set_reasonunits_status():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    wkday_str = "wkdays"
    wkday_rope = sue_plan.make_l1_rope(wkday_str)
    wed_str = "Wednesday"
    wed_rope = sue_plan.make_rope(wkday_rope, wed_str)

    wed_premise = premiseunit_shop(pstate=wed_rope)
    casa_wk_reason = reasonunit_shop(
        rcontext=wkday_rope, premises={wed_premise.pstate: wed_premise}
    )
    print(f"{type(casa_wk_reason.rcontext)=}")
    print(f"{casa_wk_reason.rcontext=}")

    # WHEN
    sue_plan.edit_concept_attr(casa_rope, reason=casa_wk_reason)

    # THEN
    casa_concept = sue_plan.get_concept_obj(casa_rope)
    assert casa_concept.reasonunits is not None
    print(casa_concept.reasonunits)
    assert casa_concept.reasonunits[wkday_rope] is not None
    assert casa_concept.reasonunits[wkday_rope] == casa_wk_reason


def test_agenda_returned_WhenNoReasonsExist():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()

    # WHEN
    sue_plan.settle_plan()

    # THEN
    casa_rope = sue_plan.make_l1_rope("casa")
    assert sue_plan.get_concept_obj(casa_rope)._chore is True
    cat_rope = sue_plan.make_l1_rope("cat have dinner")
    assert sue_plan.get_concept_obj(cat_rope)._chore is True


def test_PlanUnit_reasonheirs_AreCorrectlyInherited_v1():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope("casa")
    wk_rope = sue_plan.make_l1_rope("wkdays")
    tue_rope = sue_plan.make_rope(wk_rope, "Tuesday")
    casa_wk_build_reasonunit = reasonunit_shop(wk_rope)
    casa_wk_build_reasonunit.set_premise(tue_rope)
    sue_plan.edit_concept_attr(casa_rope, reason=casa_wk_build_reasonunit)
    casa_concept = sue_plan.get_concept_obj(casa_rope)
    assert casa_concept.reasonunits != {}
    assert casa_concept.get_reasonunit(wk_rope)
    assert casa_concept.get_reasonunit(wk_rope) == casa_wk_build_reasonunit
    assert not casa_concept.get_reasonheir(wk_rope)

    # WHEN
    sue_plan.settle_plan()

    # THEN
    assert casa_concept.get_reasonheir(wk_rope)
    assert len(casa_concept.get_reasonheir(wk_rope).premises) == 1
    assert casa_concept.get_reasonheir(wk_rope).get_premise(tue_rope)
    premise_tue = casa_concept.get_reasonheir(wk_rope).get_premise(tue_rope)
    tue_premise = premiseunit_shop(pstate=tue_rope)
    tue_premise._status = False
    tue_premise._chore = False
    premises = {tue_premise.pstate: tue_premise}
    built_wk_reasonheir = reasonheir_shop(
        rcontext=wk_rope,
        premises=premises,
        _status=False,
        _rconcept_active_value=True,
    )
    tue_chore = built_wk_reasonheir.premises.get(premise_tue.pstate)._chore
    assert premise_tue._chore == tue_chore
    assert premise_tue == built_wk_reasonheir.premises[premise_tue.pstate]
    wk_reasonheir = casa_concept.get_reasonheir(wk_rope)
    assert wk_reasonheir.premises == built_wk_reasonheir.premises
    assert casa_concept.get_reasonheir(wk_rope) == built_wk_reasonheir


def test_PlanUnit_reasonheirs_AreCorrectlyInheritedTo4LevelsFromRoot():
    # ESTABLISH
    a4_plan = get_planunit_with_4_levels()
    casa_str = "casa"
    casa_rope = a4_plan.make_l1_rope(casa_str)
    wk_str = "wkdays"
    wk_rope = a4_plan.make_l1_rope(wk_str)
    wed_str = "Wednesday"
    wed_rope = a4_plan.make_rope(wk_rope, wed_str)

    wed_premise = premiseunit_shop(pstate=wed_rope)
    wed_premise._status = False
    wed_premise._chore = False

    premises_x = {wed_premise.pstate: wed_premise}
    casa_wk_build_reasonunit = reasonunit_shop(rcontext=wk_rope, premises=premises_x)
    casa_wk_built_reasonheir = reasonheir_shop(
        rcontext=wk_rope,
        premises=premises_x,
        _status=False,
        _rconcept_active_value=True,
    )
    a4_plan.edit_concept_attr(casa_rope, reason=casa_wk_build_reasonunit)

    # WHEN
    rla_str = "hp"
    rla_rope = a4_plan.make_rope(casa_rope, rla_str)
    a4_plan.set_concept(conceptunit_shop(rla_str), parent_rope=rla_rope)
    cost_str = "cost_quantification"
    cost_rope = a4_plan.make_rope(rla_rope, cost_str)
    a4_plan.set_concept(conceptunit_shop(cost_str), parent_rope=cost_rope)
    a4_plan.settle_plan()

    # THEN
    casa_concept = a4_plan.conceptroot._kids[casa_str]
    rla_concept = casa_concept._kids[rla_str]
    cost_concept = rla_concept._kids[cost_str]

    # 1
    casa_wk_calc_reasonheir = casa_concept._reasonheirs[wk_rope]
    assert casa_wk_calc_reasonheir == casa_wk_built_reasonheir

    # 2
    rla_wk_reasonheir = rla_concept._reasonheirs[wk_rope]
    assert rla_wk_reasonheir.rcontext == casa_wk_built_reasonheir.rcontext
    assert rla_wk_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        rla_wk_reasonheir.rconcept_active_requisite
        == casa_wk_built_reasonheir.rconcept_active_requisite
    )
    assert rla_wk_reasonheir._status == casa_wk_built_reasonheir._status
    assert rla_wk_reasonheir._chore == casa_wk_built_reasonheir._chore
    assert rla_wk_reasonheir._rconcept_active_value
    assert rla_wk_reasonheir._rconcept_active_value != casa_wk_built_reasonheir

    # 3
    cost_wk_reasonheir = cost_concept._reasonheirs[wk_rope]
    assert cost_wk_reasonheir.rcontext == casa_wk_built_reasonheir.rcontext
    assert cost_wk_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        cost_wk_reasonheir.rconcept_active_requisite
        == casa_wk_built_reasonheir.rconcept_active_requisite
    )
    assert cost_wk_reasonheir._status == casa_wk_built_reasonheir._status
    assert cost_wk_reasonheir._chore == casa_wk_built_reasonheir._chore
    assert cost_wk_reasonheir._rconcept_active_value
    assert cost_wk_reasonheir._rconcept_active_value != casa_wk_built_reasonheir


def test_PlanUnit_reasonheirs_AreCorrectlyInheritedTo4LevelsFromLevel2():
    a4_plan = get_planunit_with_4_levels()
    casa_str = "casa"
    casa_rope = a4_plan.make_l1_rope(casa_str)
    wk_concept_label = "wkdays"
    wk_rope = a4_plan.make_l1_rope(wk_concept_label)
    wed_str = "Wednesday"
    wed_rope = a4_plan.make_rope(wk_rope, wed_str)

    wed_premise = premiseunit_shop(pstate=wed_rope)
    wed_premise._status = False
    wed_premise._chore = False
    premises = {wed_premise.pstate: wed_premise}
    casa_wk_build_reasonunit = reasonunit_shop(wk_rope, premises=premises)
    casa_wk_built_reasonheir = reasonheir_shop(
        rcontext=wk_rope,
        premises=premises,
        _status=False,
        _rconcept_active_value=True,
    )
    a4_plan.edit_concept_attr(casa_rope, reason=casa_wk_build_reasonunit)
    rla_str = "hp"
    rla_rope = a4_plan.make_rope(casa_rope, rla_str)
    a4_plan.set_concept(conceptunit_shop(rla_str), parent_rope=rla_rope)
    cost_str = "cost_quantification"
    cost_rope = a4_plan.make_rope(rla_rope, cost_str)
    a4_plan.set_concept(conceptunit_shop(cost_str), parent_rope=cost_rope)

    casa_concept = a4_plan.conceptroot.get_kid(casa_str)
    rla_concept = casa_concept.get_kid(rla_str)
    cost_concept = rla_concept.get_kid(cost_str)

    assert a4_plan.conceptroot._reasonheirs == {}
    assert casa_concept._reasonheirs == {}
    assert rla_concept._reasonheirs == {}
    assert cost_concept._reasonheirs == {}

    # WHEN
    a4_plan.settle_plan()

    # THEN
    assert a4_plan.conceptroot._reasonheirs == {}  # casa_wk_built_reasonheir

    # 1
    assert casa_concept._reasonheirs[wk_rope] == casa_wk_built_reasonheir

    # 2
    rla_wk_reasonheir = rla_concept._reasonheirs[wk_rope]
    assert rla_wk_reasonheir.rcontext == casa_wk_built_reasonheir.rcontext
    assert rla_wk_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        rla_wk_reasonheir.rconcept_active_requisite
        == casa_wk_built_reasonheir.rconcept_active_requisite
    )
    assert rla_wk_reasonheir._status == casa_wk_built_reasonheir._status
    assert rla_wk_reasonheir._chore == casa_wk_built_reasonheir._chore
    assert rla_wk_reasonheir._rconcept_active_value
    assert rla_wk_reasonheir._rconcept_active_value != casa_wk_built_reasonheir

    # 3
    cost_wk_reasonheir = cost_concept._reasonheirs[wk_rope]
    assert cost_wk_reasonheir.rcontext == casa_wk_built_reasonheir.rcontext
    assert cost_wk_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        cost_wk_reasonheir.rconcept_active_requisite
        == casa_wk_built_reasonheir.rconcept_active_requisite
    )
    assert cost_wk_reasonheir._status == casa_wk_built_reasonheir._status
    assert cost_wk_reasonheir._chore == casa_wk_built_reasonheir._chore
    assert cost_wk_reasonheir._rconcept_active_value
    assert cost_wk_reasonheir._rconcept_active_value != casa_wk_built_reasonheir


def test_PlanUnit_ReasonUnits_set_UnCoupledMethod():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    wk_str = "wkdays"
    wk_rope = sue_plan.make_l1_rope(wk_str)
    wed_str = "Wednesday"
    wed_rope = sue_plan.make_rope(wk_rope, wed_str)

    # WHEN
    sue_plan.edit_concept_attr(
        casa_rope, reason_rcontext=wk_rope, reason_premise=wed_rope
    )

    # THEN
    casa_concept1 = sue_plan.get_concept_obj(casa_rope)
    assert casa_concept1.reasonunits is not None
    print(casa_concept1.reasonunits)
    assert casa_concept1.reasonunits[wk_rope] is not None
    assert casa_concept1.reasonunits[wk_rope].premises[wed_rope].popen is None
    assert casa_concept1.reasonunits[wk_rope].premises[wed_rope].pnigh is None

    casa_wk_reason1 = reasonunit_shop(wk_rope)
    casa_wk_reason1.set_premise(premise=wed_rope)
    print(f" {type(casa_wk_reason1.rcontext)=}")
    print(f" {casa_wk_reason1.rcontext=}")
    assert casa_concept1.reasonunits[wk_rope] == casa_wk_reason1

    # ESTABLISH
    pdivisor_x = 34
    x_popen = 12
    x_pnigh = 12

    # WHEN
    sue_plan.edit_concept_attr(
        casa_rope,
        reason_rcontext=wk_rope,
        reason_premise=wed_rope,
        pdivisor=pdivisor_x,
        popen=x_popen,
        reason_pnigh=x_pnigh,
    )

    # THEN
    assert casa_concept1.reasonunits[wk_rope].premises[wed_rope].popen == 12
    assert casa_concept1.reasonunits[wk_rope].premises[wed_rope].pnigh == 12

    wed_premise2 = premiseunit_shop(
        wed_rope, pdivisor=pdivisor_x, popen=x_popen, pnigh=x_pnigh
    )
    casa_wk_reason2 = reasonunit_shop(
        rcontext=wk_rope, premises={wed_premise2.pstate: wed_premise2}
    )
    print(f"{type(casa_wk_reason2.rcontext)=}")
    print(f"{casa_wk_reason2.rcontext=}")
    assert casa_concept1.reasonunits[wk_rope] == casa_wk_reason2

    # WHEN
    thu_str = "Thursday"
    thu_rope = sue_plan.make_rope(wk_rope, thu_str)
    sue_plan.edit_concept_attr(
        casa_rope,
        reason_rcontext=wk_rope,
        reason_premise=thu_rope,
        pdivisor=pdivisor_x,
        popen=x_popen,
        reason_pnigh=x_pnigh,
    )

    # THEN
    assert len(casa_concept1.reasonunits[wk_rope].premises) == 2


def test_PlanUnit_ReasonUnits_set_premiseConceptWithDenomSetsPremiseDivision():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    time_str = "time"
    time_rope = sue_plan.make_l1_rope(time_str)
    wk_str = "wk"
    wk_rope = sue_plan.make_rope(time_rope, wk_str)
    sue_plan.set_l1_concept(conceptunit_shop(time_str, begin=100, close=2000))
    sue_plan.set_concept(conceptunit_shop(wk_str, denom=7), parent_rope=time_rope)

    # WHEN
    sue_plan.edit_concept_attr(
        casa_rope,
        reason_rcontext=time_rope,
        reason_premise=wk_rope,
        popen=2,
        reason_pnigh=5,
        pdivisor=None,
    )

    # THEN
    casa_concept1 = sue_plan.get_concept_obj(casa_rope)
    assert casa_concept1.reasonunits[time_rope] is not None
    assert casa_concept1.reasonunits[time_rope].premises[wk_rope].pdivisor == 7
    assert casa_concept1.reasonunits[time_rope].premises[wk_rope].popen == 2
    assert casa_concept1.reasonunits[time_rope].premises[wk_rope].pnigh == 5


def test_PlanUnit_ReasonUnits_set_premiseConceptWithBeginCloseSetsPremisePopen_Pnigh():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa = "casa"
    casa_rope = sue_plan.make_l1_rope(casa)
    time = "time"
    time_rope = sue_plan.make_l1_rope(time)
    rus_war = "rus_war"
    rus_war_rope = sue_plan.make_rope(time_rope, rus_war)
    sue_plan.set_concept(
        conceptunit_shop(time, begin=100, close=2000), sue_plan.belief_label
    )
    sue_plan.set_concept(conceptunit_shop(rus_war, begin=22, close=34), time_rope)

    # WHEN
    sue_plan.edit_concept_attr(
        casa_rope,
        reason_rcontext=time_rope,
        reason_premise=rus_war_rope,
        popen=None,
        reason_pnigh=None,
        pdivisor=None,
    )

    # THEN
    casa_concept1 = sue_plan.get_concept_obj(casa_rope)
    assert casa_concept1.reasonunits[time_rope] is not None
    assert casa_concept1.reasonunits[time_rope].premises[rus_war_rope].pdivisor is None
    assert casa_concept1.reasonunits[time_rope].premises[rus_war_rope].popen == 22
    assert casa_concept1.reasonunits[time_rope].premises[rus_war_rope].pnigh == 34


def test_PlanUnit_ReasonUnits_edit_concept_attr_CorrectlyDeletes_ReasonUnits_And_PremiseUnits():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope("casa")
    wkday_rope = sue_plan.make_l1_rope("wkdays")
    wed_rope = sue_plan.make_rope(wkday_rope, "Wednesday")

    sue_plan.edit_concept_attr(
        casa_rope, reason_rcontext=wkday_rope, reason_premise=wed_rope
    )
    thu_rope = sue_plan.make_rope(wkday_rope, "Thursday")
    sue_plan.edit_concept_attr(
        casa_rope,
        reason_rcontext=wkday_rope,
        reason_premise=thu_rope,
    )
    casa_concept1 = sue_plan.get_concept_obj(casa_rope)
    assert len(casa_concept1.reasonunits[wkday_rope].premises) == 2

    # WHEN
    sue_plan.edit_concept_attr(
        casa_rope,
        reason_del_premise_rcontext=wkday_rope,
        reason_del_premise_pstate=thu_rope,
    )

    # THEN
    assert len(casa_concept1.reasonunits[wkday_rope].premises) == 1

    # WHEN
    sue_plan.edit_concept_attr(
        casa_rope,
        reason_del_premise_rcontext=wkday_rope,
        reason_del_premise_pstate=wed_rope,
    )

    # THEN
    with pytest_raises(KeyError) as excinfo:
        casa_concept1.reasonunits[wkday_rope]
    assert str(excinfo.value) == f"'{wkday_rope}'"
    assert casa_concept1.reasonunits == {}


def test_PlanUnit_ReasonUnits_del_reason_premise_UncoupledMethod2():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_rope = sue_plan.make_l1_rope("casa")
    wkdays_rope = sue_plan.make_l1_rope("wkdays")
    casa_concept1 = sue_plan.get_concept_obj(casa_rope)
    assert len(casa_concept1.reasonunits) == 0

    # WHEN
    with pytest_raises(Exception) as excinfo:
        casa_concept1.del_reasonunit_rcontext(wkdays_rope)
    assert str(excinfo.value) == f"No ReasonUnit at '{wkdays_rope}'"


def test_PlanUnit_edit_concept_attr_planIsAbleToEdit_rconcept_active_requisite_AnyConceptIfInvaildThrowsError():
    # _rconcept_active_requisite: str = None
    # must be 1 of 3: bool: True, bool: False, str="Set to Ignore"
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)

    run_str = "run to casa"
    run_rope = sue_plan.make_l1_rope(run_str)
    sue_plan.set_concept(conceptunit_shop(run_str), sue_plan.belief_label)
    sue_plan.settle_plan()  # set tree metrics
    run_concept = sue_plan.get_concept_obj(run_rope)
    assert len(run_concept.reasonunits) == 0

    # WHEN
    sue_plan.edit_concept_attr(
        run_rope,
        reason_rcontext=casa_rope,
        reason_rconcept_active_requisite=True,
    )

    # THEN
    assert len(run_concept.reasonunits) == 1
    reasonunit_casa = run_concept.reasonunits.get(casa_rope)
    assert reasonunit_casa.rcontext == casa_rope
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.rconcept_active_requisite is True

    # WHEN
    sue_plan.edit_concept_attr(
        run_rope,
        reason_rcontext=casa_rope,
        reason_rconcept_active_requisite=False,
    )

    # THEN
    assert len(run_concept.reasonunits) == 1
    reasonunit_casa = run_concept.reasonunits.get(casa_rope)
    assert reasonunit_casa.rcontext == casa_rope
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.rconcept_active_requisite is False

    # WHEN
    sue_plan.edit_concept_attr(
        run_rope,
        reason_rcontext=casa_rope,
        reason_rconcept_active_requisite="Set to Ignore",
    )

    # THEN
    assert len(run_concept.reasonunits) == 1
    reasonunit_casa = run_concept.reasonunits.get(casa_rope)
    assert reasonunit_casa.rcontext == casa_rope
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.rconcept_active_requisite is None


def test_PlanUnit_ReasonUnits_ConceptUnit_active_InfluencesReasonUnitStatus():
    # ESTABLISH an Plan with 5 concepts, 1 Fact:
    # 1. concept(...,wkdays) exists
    # 2. concept(...,wkdays,wednesday) exists
    # 3. concept(...,wkdays,thursday) exists
    sue_plan = get_planunit_with_4_levels()
    casa_str = "casa"
    casa_rope = sue_plan.make_l1_rope(casa_str)
    wkdays_str = "wkdays"
    wkdays_rope = sue_plan.make_l1_rope(wkdays_str)
    wed_str = "Wednesday"
    wed_rope = sue_plan.make_rope(wkdays_rope, wed_str)
    thu_str = "Thursday"
    thu_rope = sue_plan.make_rope(wkdays_rope, thu_str)

    # 4. concept(...,casa) with
    # 4.1 ReasonUnit: rcontext=wkdays_rope, pstate=thu_rope
    # 4.2 .active = False
    sue_plan.edit_concept_attr(
        casa_rope,
        reason_rcontext=wkdays_rope,
        reason_premise=thu_rope,
    )
    sue_plan.settle_plan()  # set tree metrics
    casa_concept = sue_plan.get_concept_obj(casa_rope)
    assert casa_concept._active is False

    # 5. concept(...,run to casa) with
    # 5.1. ReasonUnit: concept(rcontext=...,casa) has .rconcept_active_requisite = True
    # 5.2. concept(...,casa).active = False
    run_str = "run to casa"
    run_rope = sue_plan.make_l1_rope(run_str)
    sue_plan.set_concept(conceptunit_shop(run_str), sue_plan.belief_label)
    sue_plan.edit_concept_attr(
        run_rope,
        reason_rcontext=casa_rope,
        reason_rconcept_active_requisite=True,
    )
    run_concept = sue_plan.get_concept_obj(run_rope)
    sue_plan.settle_plan()
    assert run_concept._active is False

    # Fact: rcontext: (...,wkdays) fstate: (...,wkdays,wednesday)
    sue_plan.add_fact(fcontext=wkdays_rope, fstate=wed_rope)
    sue_plan.settle_plan()

    assert casa_concept._active is False
    assert run_concept._active is False

    # WHEN
    print("before changing fact")
    sue_plan.add_fact(fcontext=wkdays_rope, fstate=thu_rope)
    print("after changing fact")
    sue_plan.settle_plan()
    assert casa_concept._active is True

    # THEN
    assert run_concept._active is True


def test_PlanUnit_settle_plan_SetsRationalAttrToFalseWhen_max_tree_traverse_Is1():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    assert sue_plan._rational is False
    # sue_plan.settle_plan()
    sue_plan._rational = True
    assert sue_plan._rational

    # WHEN
    # hack plan to set _max_tree_traverse = 1 (not allowed, should be 2 or more)
    sue_plan.max_tree_traverse = 1
    sue_plan.settle_plan()

    # THEN
    assert not sue_plan._rational


def test_PlanUnit_tree_traverse_count_SetByTotalNumberOfTreeTraversesEndsStatusIsDetected():
    # ESTABLISH
    sue_plan = get_planunit_with_4_levels()
    assert sue_plan.max_tree_traverse != 2

    # WHEN
    sue_plan.settle_plan()
    # for concept_key in sue_plan._concept_dict.keys():
    #     print(f"{concept_key=}")

    # THEN
    assert sue_plan._tree_traverse_count == 2


def test_PlanUnit_tree_traverse_count_CorrectlyCountsTreeTraversesForIrrationalPlans():
    # ESTABLISH irrational plan
    sue_plan = get_planunit_irrational_example()
    sue_plan.settle_plan()
    assert sue_plan._tree_traverse_count == 3

    # WHEN
    sue_plan.set_max_tree_traverse(21)
    sue_plan.settle_plan()

    # THEN
    assert sue_plan._tree_traverse_count == 21
