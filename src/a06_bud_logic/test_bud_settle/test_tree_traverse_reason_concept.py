from pytest import raises as pytest_raises
from src.a04_reason_logic.reason_concept import (
    premiseunit_shop,
    reasonheir_shop,
    reasonunit_shop,
)
from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_bud_logic._test_util.example_buds import (
    get_budunit_irrational_example,
    get_budunit_with_4_levels,
)
from src.a06_bud_logic.bud import budunit_shop


def test_BudUnit_ReasonUnits_create():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    wkday_str = "wkdays"
    wkday_way = sue_bud.make_l1_way(wkday_str)
    wed_str = "Wednesday"
    wed_way = sue_bud.make_way(wkday_way, wed_str)

    wed_premise = premiseunit_shop(pstate=wed_way)
    casa_wk_reason = reasonunit_shop(wkday_way, {wed_premise.pstate: wed_premise})
    print(f"{type(casa_wk_reason.rcontext)=}")
    print(f"{casa_wk_reason.rcontext=}")

    # WHEN
    sue_bud.edit_concept_attr(casa_way, reason=casa_wk_reason)

    # THEN
    casa_concept = sue_bud.get_concept_obj(casa_way)
    assert casa_concept.reasonunits is not None
    print(casa_concept.reasonunits)
    assert casa_concept.reasonunits[wkday_way] is not None
    assert casa_concept.reasonunits[wkday_way] == casa_wk_reason


def test_BudUnit_edit_concept_attr_reasonunit_CorrectlySets_bridge():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_way = sue_bud.make_l1_way("casa")
    wk_way = sue_bud.make_l1_way("wkdays")
    wed_way = sue_bud.make_way(wk_way, "Wednesday")

    slash_str = "/"
    before_wk_reason = reasonunit_shop(wk_way, bridge=slash_str)
    before_wk_reason.set_premise(wed_way)
    assert before_wk_reason.bridge == slash_str

    # WHEN
    sue_bud.edit_concept_attr(casa_way, reason=before_wk_reason)

    # THEN
    casa_concept = sue_bud.get_concept_obj(casa_way)
    wk_reasonunit = casa_concept.reasonunits.get(wk_way)
    assert wk_reasonunit.bridge != slash_str
    assert wk_reasonunit.bridge == sue_bud.bridge


def test_BudUnit_edit_concept_attr_reason_rcontext_CorrectlySets_bridge():
    # ESTABLISH
    slash_str = "/"
    bob_bud = budunit_shop("Bob", bridge=slash_str)
    casa_str = "casa"
    wk_str = "wk"
    wed_str = "Wednesday"
    casa_way = bob_bud.make_l1_way(casa_str)
    wk_way = bob_bud.make_l1_way(wk_str)
    wed_way = bob_bud.make_way(wk_way, wed_str)
    bob_bud.set_l1_concept(conceptunit_shop(casa_str))
    bob_bud.set_l1_concept(conceptunit_shop(wk_str))
    bob_bud.set_concept(conceptunit_shop(wed_str), wk_way)
    print(f"{bob_bud.conceptroot._kids.keys()=}")
    wed_concept = bob_bud.get_concept_obj(wed_way)
    assert wed_concept.bridge == slash_str
    assert wed_concept.bridge == bob_bud.bridge

    # WHEN
    bob_bud.edit_concept_attr(casa_way, reason_rcontext=wk_way, reason_premise=wed_way)

    # THEN
    casa_concept = bob_bud.get_concept_obj(casa_way)
    assert casa_concept.bridge == slash_str
    wk_reasonunit = casa_concept.reasonunits.get(wk_way)
    assert wk_reasonunit.bridge != ","
    assert wk_reasonunit.bridge == bob_bud.bridge


def test_BudUnit_set_reasonunits_status():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    wkday_str = "wkdays"
    wkday_way = sue_bud.make_l1_way(wkday_str)
    wed_str = "Wednesday"
    wed_way = sue_bud.make_way(wkday_way, wed_str)

    wed_premise = premiseunit_shop(pstate=wed_way)
    casa_wk_reason = reasonunit_shop(
        rcontext=wkday_way, premises={wed_premise.pstate: wed_premise}
    )
    print(f"{type(casa_wk_reason.rcontext)=}")
    print(f"{casa_wk_reason.rcontext=}")

    # WHEN
    sue_bud.edit_concept_attr(casa_way, reason=casa_wk_reason)

    # THEN
    casa_concept = sue_bud.get_concept_obj(casa_way)
    assert casa_concept.reasonunits is not None
    print(casa_concept.reasonunits)
    assert casa_concept.reasonunits[wkday_way] is not None
    assert casa_concept.reasonunits[wkday_way] == casa_wk_reason


def test_agenda_returned_WhenNoReasonsExist():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()

    # WHEN
    sue_bud.settle_bud()

    # THEN
    casa_way = sue_bud.make_l1_way("casa")
    assert sue_bud.get_concept_obj(casa_way)._task is True
    cat_way = sue_bud.make_l1_way("cat have dinner")
    assert sue_bud.get_concept_obj(cat_way)._task is True


def test_BudUnit_reasonheirs_AreCorrectlyInherited_v1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_way = sue_bud.make_l1_way("casa")
    wk_way = sue_bud.make_l1_way("wkdays")
    tue_way = sue_bud.make_way(wk_way, "Tuesday")
    casa_wk_build_reasonunit = reasonunit_shop(wk_way)
    casa_wk_build_reasonunit.set_premise(tue_way)
    sue_bud.edit_concept_attr(casa_way, reason=casa_wk_build_reasonunit)
    casa_concept = sue_bud.get_concept_obj(casa_way)
    assert casa_concept.reasonunits != {}
    assert casa_concept.get_reasonunit(wk_way)
    assert casa_concept.get_reasonunit(wk_way) == casa_wk_build_reasonunit
    assert not casa_concept.get_reasonheir(wk_way)

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert casa_concept.get_reasonheir(wk_way)
    assert len(casa_concept.get_reasonheir(wk_way).premises) == 1
    assert casa_concept.get_reasonheir(wk_way).get_premise(tue_way)
    premise_tue = casa_concept.get_reasonheir(wk_way).get_premise(tue_way)
    tue_premise = premiseunit_shop(pstate=tue_way)
    tue_premise._status = False
    tue_premise._task = False
    premises = {tue_premise.pstate: tue_premise}
    built_wk_reasonheir = reasonheir_shop(
        rcontext=wk_way,
        premises=premises,
        _status=False,
        _rconcept_active_value=True,
    )
    tue_task = built_wk_reasonheir.premises.get(premise_tue.pstate)._task
    assert premise_tue._task == tue_task
    assert premise_tue == built_wk_reasonheir.premises[premise_tue.pstate]
    wk_reasonheir = casa_concept.get_reasonheir(wk_way)
    assert wk_reasonheir.premises == built_wk_reasonheir.premises
    assert casa_concept.get_reasonheir(wk_way) == built_wk_reasonheir


def test_BudUnit_reasonheirs_AreCorrectlyInheritedTo4LevelsFromRoot():
    # ESTABLISH
    a4_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = a4_bud.make_l1_way(casa_str)
    wk_str = "wkdays"
    wk_way = a4_bud.make_l1_way(wk_str)
    wed_str = "Wednesday"
    wed_way = a4_bud.make_way(wk_way, wed_str)

    wed_premise = premiseunit_shop(pstate=wed_way)
    wed_premise._status = False
    wed_premise._task = False

    premises_x = {wed_premise.pstate: wed_premise}
    casa_wk_build_reasonunit = reasonunit_shop(rcontext=wk_way, premises=premises_x)
    casa_wk_built_reasonheir = reasonheir_shop(
        rcontext=wk_way,
        premises=premises_x,
        _status=False,
        _rconcept_active_value=True,
    )
    a4_bud.edit_concept_attr(casa_way, reason=casa_wk_build_reasonunit)

    # WHEN
    rla_str = "hp"
    rla_way = a4_bud.make_way(casa_way, rla_str)
    a4_bud.set_concept(conceptunit_shop(rla_str), parent_way=rla_way)
    cost_str = "cost_quantification"
    cost_way = a4_bud.make_way(rla_way, cost_str)
    a4_bud.set_concept(conceptunit_shop(cost_str), parent_way=cost_way)
    a4_bud.settle_bud()

    # THEN
    casa_concept = a4_bud.conceptroot._kids[casa_str]
    rla_concept = casa_concept._kids[rla_str]
    cost_concept = rla_concept._kids[cost_str]

    # 1
    casa_wk_calc_reasonheir = casa_concept._reasonheirs[wk_way]
    assert casa_wk_calc_reasonheir == casa_wk_built_reasonheir

    # 2
    rla_wk_reasonheir = rla_concept._reasonheirs[wk_way]
    assert rla_wk_reasonheir.rcontext == casa_wk_built_reasonheir.rcontext
    assert rla_wk_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        rla_wk_reasonheir.rconcept_active_requisite
        == casa_wk_built_reasonheir.rconcept_active_requisite
    )
    assert rla_wk_reasonheir._status == casa_wk_built_reasonheir._status
    assert rla_wk_reasonheir._task == casa_wk_built_reasonheir._task
    assert rla_wk_reasonheir._rconcept_active_value
    assert rla_wk_reasonheir._rconcept_active_value != casa_wk_built_reasonheir

    # 3
    cost_wk_reasonheir = cost_concept._reasonheirs[wk_way]
    assert cost_wk_reasonheir.rcontext == casa_wk_built_reasonheir.rcontext
    assert cost_wk_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        cost_wk_reasonheir.rconcept_active_requisite
        == casa_wk_built_reasonheir.rconcept_active_requisite
    )
    assert cost_wk_reasonheir._status == casa_wk_built_reasonheir._status
    assert cost_wk_reasonheir._task == casa_wk_built_reasonheir._task
    assert cost_wk_reasonheir._rconcept_active_value
    assert cost_wk_reasonheir._rconcept_active_value != casa_wk_built_reasonheir


def test_BudUnit_reasonheirs_AreCorrectlyInheritedTo4LevelsFromLevel2():
    a4_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = a4_bud.make_l1_way(casa_str)
    wk_concept_label = "wkdays"
    wk_way = a4_bud.make_l1_way(wk_concept_label)
    wed_str = "Wednesday"
    wed_way = a4_bud.make_way(wk_way, wed_str)

    wed_premise = premiseunit_shop(pstate=wed_way)
    wed_premise._status = False
    wed_premise._task = False
    premises = {wed_premise.pstate: wed_premise}
    casa_wk_build_reasonunit = reasonunit_shop(wk_way, premises=premises)
    casa_wk_built_reasonheir = reasonheir_shop(
        rcontext=wk_way,
        premises=premises,
        _status=False,
        _rconcept_active_value=True,
    )
    a4_bud.edit_concept_attr(casa_way, reason=casa_wk_build_reasonunit)
    rla_str = "hp"
    rla_way = a4_bud.make_way(casa_way, rla_str)
    a4_bud.set_concept(conceptunit_shop(rla_str), parent_way=rla_way)
    cost_str = "cost_quantification"
    cost_way = a4_bud.make_way(rla_way, cost_str)
    a4_bud.set_concept(conceptunit_shop(cost_str), parent_way=cost_way)

    casa_concept = a4_bud.conceptroot.get_kid(casa_str)
    rla_concept = casa_concept.get_kid(rla_str)
    cost_concept = rla_concept.get_kid(cost_str)

    assert a4_bud.conceptroot._reasonheirs == {}
    assert casa_concept._reasonheirs == {}
    assert rla_concept._reasonheirs == {}
    assert cost_concept._reasonheirs == {}

    # WHEN
    a4_bud.settle_bud()

    # THEN
    assert a4_bud.conceptroot._reasonheirs == {}  # casa_wk_built_reasonheir

    # 1
    assert casa_concept._reasonheirs[wk_way] == casa_wk_built_reasonheir

    # 2
    rla_wk_reasonheir = rla_concept._reasonheirs[wk_way]
    assert rla_wk_reasonheir.rcontext == casa_wk_built_reasonheir.rcontext
    assert rla_wk_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        rla_wk_reasonheir.rconcept_active_requisite
        == casa_wk_built_reasonheir.rconcept_active_requisite
    )
    assert rla_wk_reasonheir._status == casa_wk_built_reasonheir._status
    assert rla_wk_reasonheir._task == casa_wk_built_reasonheir._task
    assert rla_wk_reasonheir._rconcept_active_value
    assert rla_wk_reasonheir._rconcept_active_value != casa_wk_built_reasonheir

    # 3
    cost_wk_reasonheir = cost_concept._reasonheirs[wk_way]
    assert cost_wk_reasonheir.rcontext == casa_wk_built_reasonheir.rcontext
    assert cost_wk_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        cost_wk_reasonheir.rconcept_active_requisite
        == casa_wk_built_reasonheir.rconcept_active_requisite
    )
    assert cost_wk_reasonheir._status == casa_wk_built_reasonheir._status
    assert cost_wk_reasonheir._task == casa_wk_built_reasonheir._task
    assert cost_wk_reasonheir._rconcept_active_value
    assert cost_wk_reasonheir._rconcept_active_value != casa_wk_built_reasonheir


def test_BudUnit_ReasonUnits_set_UnCoupledMethod():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    wk_str = "wkdays"
    wk_way = sue_bud.make_l1_way(wk_str)
    wed_str = "Wednesday"
    wed_way = sue_bud.make_way(wk_way, wed_str)

    # WHEN
    sue_bud.edit_concept_attr(casa_way, reason_rcontext=wk_way, reason_premise=wed_way)

    # THEN
    casa_concept1 = sue_bud.get_concept_obj(casa_way)
    assert casa_concept1.reasonunits is not None
    print(casa_concept1.reasonunits)
    assert casa_concept1.reasonunits[wk_way] is not None
    assert casa_concept1.reasonunits[wk_way].premises[wed_way].popen is None
    assert casa_concept1.reasonunits[wk_way].premises[wed_way].pnigh is None

    casa_wk_reason1 = reasonunit_shop(wk_way)
    casa_wk_reason1.set_premise(premise=wed_way)
    print(f" {type(casa_wk_reason1.rcontext)=}")
    print(f" {casa_wk_reason1.rcontext=}")
    assert casa_concept1.reasonunits[wk_way] == casa_wk_reason1

    # ESTABLISH
    pdivisor_x = 34
    x_popen = 12
    x_pnigh = 12

    # WHEN
    sue_bud.edit_concept_attr(
        casa_way,
        reason_rcontext=wk_way,
        reason_premise=wed_way,
        pdivisor=pdivisor_x,
        popen=x_popen,
        reason_pnigh=x_pnigh,
    )

    # THEN
    assert casa_concept1.reasonunits[wk_way].premises[wed_way].popen == 12
    assert casa_concept1.reasonunits[wk_way].premises[wed_way].pnigh == 12

    wed_premise2 = premiseunit_shop(
        wed_way, pdivisor=pdivisor_x, popen=x_popen, pnigh=x_pnigh
    )
    casa_wk_reason2 = reasonunit_shop(
        rcontext=wk_way, premises={wed_premise2.pstate: wed_premise2}
    )
    print(f"{type(casa_wk_reason2.rcontext)=}")
    print(f"{casa_wk_reason2.rcontext=}")
    assert casa_concept1.reasonunits[wk_way] == casa_wk_reason2

    # WHEN
    thu_str = "Thursday"
    thu_way = sue_bud.make_way(wk_way, thu_str)
    sue_bud.edit_concept_attr(
        casa_way,
        reason_rcontext=wk_way,
        reason_premise=thu_way,
        pdivisor=pdivisor_x,
        popen=x_popen,
        reason_pnigh=x_pnigh,
    )

    # THEN
    assert len(casa_concept1.reasonunits[wk_way].premises) == 2


def test_BudUnit_ReasonUnits_set_premiseConceptWithDenomSetsPremiseDivision():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    time_str = "time"
    time_way = sue_bud.make_l1_way(time_str)
    wk_str = "wk"
    wk_way = sue_bud.make_way(time_way, wk_str)
    sue_bud.set_l1_concept(conceptunit_shop(time_str, begin=100, close=2000))
    sue_bud.set_concept(conceptunit_shop(wk_str, denom=7), parent_way=time_way)

    # WHEN
    sue_bud.edit_concept_attr(
        casa_way,
        reason_rcontext=time_way,
        reason_premise=wk_way,
        popen=2,
        reason_pnigh=5,
        pdivisor=None,
    )

    # THEN
    casa_concept1 = sue_bud.get_concept_obj(casa_way)
    assert casa_concept1.reasonunits[time_way] is not None
    assert casa_concept1.reasonunits[time_way].premises[wk_way].pdivisor == 7
    assert casa_concept1.reasonunits[time_way].premises[wk_way].popen == 2
    assert casa_concept1.reasonunits[time_way].premises[wk_way].pnigh == 5


def test_BudUnit_ReasonUnits_set_premiseConceptWithBeginCloseSetsPremisePopen_Pnigh():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa = "casa"
    casa_way = sue_bud.make_l1_way(casa)
    time = "time"
    time_way = sue_bud.make_l1_way(time)
    rus_war = "rus_war"
    rus_war_way = sue_bud.make_way(time_way, rus_war)
    sue_bud.set_concept(
        conceptunit_shop(time, begin=100, close=2000), sue_bud.vow_label
    )
    sue_bud.set_concept(conceptunit_shop(rus_war, begin=22, close=34), time_way)

    # WHEN
    sue_bud.edit_concept_attr(
        casa_way,
        reason_rcontext=time_way,
        reason_premise=rus_war_way,
        popen=None,
        reason_pnigh=None,
        pdivisor=None,
    )

    # THEN
    casa_concept1 = sue_bud.get_concept_obj(casa_way)
    assert casa_concept1.reasonunits[time_way] is not None
    assert casa_concept1.reasonunits[time_way].premises[rus_war_way].pdivisor is None
    assert casa_concept1.reasonunits[time_way].premises[rus_war_way].popen == 22
    assert casa_concept1.reasonunits[time_way].premises[rus_war_way].pnigh == 34


def test_BudUnit_ReasonUnits_edit_concept_attr_CorrectlyDeletes_ReasonUnits_And_PremiseUnits():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_way = sue_bud.make_l1_way("casa")
    wkday_way = sue_bud.make_l1_way("wkdays")
    wed_way = sue_bud.make_way(wkday_way, "Wednesday")

    sue_bud.edit_concept_attr(
        casa_way, reason_rcontext=wkday_way, reason_premise=wed_way
    )
    thu_way = sue_bud.make_way(wkday_way, "Thursday")
    sue_bud.edit_concept_attr(
        casa_way,
        reason_rcontext=wkday_way,
        reason_premise=thu_way,
    )
    casa_concept1 = sue_bud.get_concept_obj(casa_way)
    assert len(casa_concept1.reasonunits[wkday_way].premises) == 2

    # WHEN
    sue_bud.edit_concept_attr(
        casa_way,
        reason_del_premise_rcontext=wkday_way,
        reason_del_premise_pstate=thu_way,
    )

    # THEN
    assert len(casa_concept1.reasonunits[wkday_way].premises) == 1

    # WHEN
    sue_bud.edit_concept_attr(
        casa_way,
        reason_del_premise_rcontext=wkday_way,
        reason_del_premise_pstate=wed_way,
    )

    # THEN
    with pytest_raises(KeyError) as excinfo:
        casa_concept1.reasonunits[wkday_way]
    assert str(excinfo.value) == f"'{wkday_way}'"
    assert casa_concept1.reasonunits == {}


def test_BudUnit_ReasonUnits_del_reason_premise_UncoupledMethod2():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_way = sue_bud.make_l1_way("casa")
    wkdays_way = sue_bud.make_l1_way("wkdays")
    casa_concept1 = sue_bud.get_concept_obj(casa_way)
    assert len(casa_concept1.reasonunits) == 0

    # WHEN
    with pytest_raises(Exception) as excinfo:
        casa_concept1.del_reasonunit_rcontext(wkdays_way)
    assert str(excinfo.value) == f"No ReasonUnit at '{wkdays_way}'"


def test_BudUnit_edit_concept_attr_budIsAbleToEdit_rconcept_active_requisite_AnyConceptIfInvaildThrowsError():
    # _rconcept_active_requisite: str = None
    # must be 1 of 3: bool: True, bool: False, str="Set to Ignore"
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)

    run_str = "run to casa"
    run_way = sue_bud.make_l1_way(run_str)
    sue_bud.set_concept(conceptunit_shop(run_str), sue_bud.vow_label)
    sue_bud.settle_bud()  # set tree metrics
    run_concept = sue_bud.get_concept_obj(run_way)
    assert len(run_concept.reasonunits) == 0

    # WHEN
    sue_bud.edit_concept_attr(
        run_way,
        reason_rcontext=casa_way,
        reason_rconcept_active_requisite=True,
    )

    # THEN
    assert len(run_concept.reasonunits) == 1
    reasonunit_casa = run_concept.reasonunits.get(casa_way)
    assert reasonunit_casa.rcontext == casa_way
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.rconcept_active_requisite is True

    # WHEN
    sue_bud.edit_concept_attr(
        run_way,
        reason_rcontext=casa_way,
        reason_rconcept_active_requisite=False,
    )

    # THEN
    assert len(run_concept.reasonunits) == 1
    reasonunit_casa = run_concept.reasonunits.get(casa_way)
    assert reasonunit_casa.rcontext == casa_way
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.rconcept_active_requisite is False

    # WHEN
    sue_bud.edit_concept_attr(
        run_way,
        reason_rcontext=casa_way,
        reason_rconcept_active_requisite="Set to Ignore",
    )

    # THEN
    assert len(run_concept.reasonunits) == 1
    reasonunit_casa = run_concept.reasonunits.get(casa_way)
    assert reasonunit_casa.rcontext == casa_way
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.rconcept_active_requisite is None


def test_BudUnit_ReasonUnits_ConceptUnit_active_InfluencesReasonUnitStatus():
    # ESTABLISH an Bud with 5 concepts, 1 Fact:
    # 1. concept(...,wkdays) exists
    # 2. concept(...,wkdays,wednesday) exists
    # 3. concept(...,wkdays,thursday) exists
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    wkdays_str = "wkdays"
    wkdays_way = sue_bud.make_l1_way(wkdays_str)
    wed_str = "Wednesday"
    wed_way = sue_bud.make_way(wkdays_way, wed_str)
    thu_str = "Thursday"
    thu_way = sue_bud.make_way(wkdays_way, thu_str)

    # 4. concept(...,casa) with
    # 4.1 ReasonUnit: rcontext=wkdays_way, pstate=thu_way
    # 4.2 .active = False
    sue_bud.edit_concept_attr(
        casa_way,
        reason_rcontext=wkdays_way,
        reason_premise=thu_way,
    )
    sue_bud.settle_bud()  # set tree metrics
    casa_concept = sue_bud.get_concept_obj(casa_way)
    assert casa_concept._active is False

    # 5. concept(...,run to casa) with
    # 5.1. ReasonUnit: concept(rcontext=...,casa) has .rconcept_active_requisite = True
    # 5.2. concept(...,casa).active = False
    run_str = "run to casa"
    run_way = sue_bud.make_l1_way(run_str)
    sue_bud.set_concept(conceptunit_shop(run_str), sue_bud.vow_label)
    sue_bud.edit_concept_attr(
        run_way,
        reason_rcontext=casa_way,
        reason_rconcept_active_requisite=True,
    )
    run_concept = sue_bud.get_concept_obj(run_way)
    sue_bud.settle_bud()
    assert run_concept._active is False

    # Fact: rcontext: (...,wkdays) fstate: (...,wkdays,wednesday)
    sue_bud.add_fact(fcontext=wkdays_way, fstate=wed_way)
    sue_bud.settle_bud()

    assert casa_concept._active is False
    assert run_concept._active is False

    # WHEN
    print("before changing fact")
    sue_bud.add_fact(fcontext=wkdays_way, fstate=thu_way)
    print("after changing fact")
    sue_bud.settle_bud()
    assert casa_concept._active is True

    # THEN
    assert run_concept._active is True


def test_BudUnit_settle_bud_SetsRationalAttrToFalseWhen_max_tree_traverse_Is1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    assert sue_bud._rational is False
    # sue_bud.settle_bud()
    sue_bud._rational = True
    assert sue_bud._rational

    # WHEN
    # hack bud to set _max_tree_traverse = 1 (not allowed, should be 2 or more)
    sue_bud.max_tree_traverse = 1
    sue_bud.settle_bud()

    # THEN
    assert not sue_bud._rational


def test_BudUnit_tree_traverse_count_SetByTotalNumberOfTreeTraversesEndsStatusIsDetected():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    assert sue_bud.max_tree_traverse != 2

    # WHEN
    sue_bud.settle_bud()
    # for concept_key in sue_bud._concept_dict.keys():
    #     print(f"{concept_key=}")

    # THEN
    assert sue_bud._tree_traverse_count == 2


def test_BudUnit_tree_traverse_count_CorrectlyCountsTreeTraversesForIrrationalBuds():
    # ESTABLISH irrational bud
    sue_bud = get_budunit_irrational_example()
    sue_bud.settle_bud()
    assert sue_bud._tree_traverse_count == 3

    # WHEN
    sue_bud.set_max_tree_traverse(21)
    sue_bud.settle_bud()

    # THEN
    assert sue_bud._tree_traverse_count == 21
