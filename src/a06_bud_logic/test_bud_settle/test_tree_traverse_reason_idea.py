from src.a04_reason_logic.reason_idea import (
    premiseunit_shop,
    reasonunit_shop,
    reasonheir_shop,
)
from src.a05_idea_logic.idea import ideaunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_irrational_example,
)
from pytest import raises as pytest_raises


def test_BudUnit_ReasonUnits_create():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    weekday_str = "weekdays"
    weekday_way = sue_bud.make_l1_way(weekday_str)
    wed_str = "Wednesday"
    wed_way = sue_bud.make_way(weekday_way, wed_str)

    wed_premise = premiseunit_shop(branch=wed_way)
    casa_wk_reason = reasonunit_shop(weekday_way, {wed_premise.branch: wed_premise})
    print(f"{type(casa_wk_reason.context)=}")
    print(f"{casa_wk_reason.context=}")

    # WHEN
    sue_bud.edit_idea_attr(casa_way, reason=casa_wk_reason)

    # THEN
    casa_idea = sue_bud.get_idea_obj(casa_way)
    assert casa_idea.reasonunits is not None
    print(casa_idea.reasonunits)
    assert casa_idea.reasonunits[weekday_way] is not None
    assert casa_idea.reasonunits[weekday_way] == casa_wk_reason


def test_BudUnit_edit_idea_attr_reasonunit_CorrectlySets_bridge():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_way = sue_bud.make_l1_way("casa")
    week_way = sue_bud.make_l1_way("weekdays")
    wed_way = sue_bud.make_way(week_way, "Wednesday")

    slash_str = "/"
    before_week_reason = reasonunit_shop(week_way, bridge=slash_str)
    before_week_reason.set_premise(wed_way)
    assert before_week_reason.bridge == slash_str

    # WHEN
    sue_bud.edit_idea_attr(casa_way, reason=before_week_reason)

    # THEN
    casa_idea = sue_bud.get_idea_obj(casa_way)
    week_reasonunit = casa_idea.reasonunits.get(week_way)
    assert week_reasonunit.bridge != slash_str
    assert week_reasonunit.bridge == sue_bud.bridge


def test_BudUnit_edit_idea_attr_reason_context_CorrectlySets_bridge():
    # ESTABLISH
    slash_str = "/"
    bob_bud = budunit_shop("Bob", bridge=slash_str)
    casa_str = "casa"
    week_str = "week"
    wed_str = "Wednesday"
    casa_way = bob_bud.make_l1_way(casa_str)
    week_way = bob_bud.make_l1_way(week_str)
    wed_way = bob_bud.make_way(week_way, wed_str)
    bob_bud.set_l1_idea(ideaunit_shop(casa_str))
    bob_bud.set_l1_idea(ideaunit_shop(week_str))
    bob_bud.set_idea(ideaunit_shop(wed_str), week_way)
    print(f"{bob_bud.idearoot._kids.keys()=}")
    wed_idea = bob_bud.get_idea_obj(wed_way)
    assert wed_idea.bridge == slash_str
    assert wed_idea.bridge == bob_bud.bridge

    # WHEN
    bob_bud.edit_idea_attr(casa_way, reason_context=week_way, reason_premise=wed_way)

    # THEN
    casa_idea = bob_bud.get_idea_obj(casa_way)
    assert casa_idea.bridge == slash_str
    week_reasonunit = casa_idea.reasonunits.get(week_way)
    assert week_reasonunit.bridge != ","
    assert week_reasonunit.bridge == bob_bud.bridge


def test_BudUnit_set_reasonunits_status():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    weekday_str = "weekdays"
    weekday_way = sue_bud.make_l1_way(weekday_str)
    wed_str = "Wednesday"
    wed_way = sue_bud.make_way(weekday_way, wed_str)

    wed_premise = premiseunit_shop(branch=wed_way)
    casa_wk_reason = reasonunit_shop(
        context=weekday_way, premises={wed_premise.branch: wed_premise}
    )
    print(f"{type(casa_wk_reason.context)=}")
    print(f"{casa_wk_reason.context=}")

    # WHEN
    sue_bud.edit_idea_attr(casa_way, reason=casa_wk_reason)

    # THEN
    casa_idea = sue_bud.get_idea_obj(casa_way)
    assert casa_idea.reasonunits is not None
    print(casa_idea.reasonunits)
    assert casa_idea.reasonunits[weekday_way] is not None
    assert casa_idea.reasonunits[weekday_way] == casa_wk_reason


def test_agenda_returned_WhenNoReasonsExist():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()

    # WHEN
    sue_bud.settle_bud()

    # THEN
    casa_way = sue_bud.make_l1_way("casa")
    assert sue_bud.get_idea_obj(casa_way)._task is True
    cat_way = sue_bud.make_l1_way("cat have dinner")
    assert sue_bud.get_idea_obj(cat_way)._task is True


def test_BudUnit_reasonheirs_AreCorrectlyInherited_v1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_way = sue_bud.make_l1_way("casa")
    week_way = sue_bud.make_l1_way("weekdays")
    tue_way = sue_bud.make_way(week_way, "Tuesday")
    casa_wk_build_reasonunit = reasonunit_shop(week_way)
    casa_wk_build_reasonunit.set_premise(tue_way)
    sue_bud.edit_idea_attr(casa_way, reason=casa_wk_build_reasonunit)
    casa_idea = sue_bud.get_idea_obj(casa_way)
    assert casa_idea.reasonunits != {}
    assert casa_idea.get_reasonunit(week_way)
    assert casa_idea.get_reasonunit(week_way) == casa_wk_build_reasonunit
    assert not casa_idea.get_reasonheir(week_way)

    # WHEN
    sue_bud.settle_bud()

    # THEN
    assert casa_idea.get_reasonheir(week_way)
    assert len(casa_idea.get_reasonheir(week_way).premises) == 1
    assert casa_idea.get_reasonheir(week_way).get_premise(tue_way)
    premise_tue = casa_idea.get_reasonheir(week_way).get_premise(tue_way)
    tue_premise = premiseunit_shop(branch=tue_way)
    tue_premise._status = False
    tue_premise._task = False
    premises = {tue_premise.branch: tue_premise}
    built_week_reasonheir = reasonheir_shop(
        context=week_way,
        premises=premises,
        _status=False,
        _context_idea_active_value=True,
    )
    tue_task = built_week_reasonheir.premises.get(premise_tue.branch)._task
    assert premise_tue._task == tue_task
    assert premise_tue == built_week_reasonheir.premises[premise_tue.branch]
    week_reasonheir = casa_idea.get_reasonheir(week_way)
    assert week_reasonheir.premises == built_week_reasonheir.premises
    assert casa_idea.get_reasonheir(week_way) == built_week_reasonheir


def test_BudUnit_reasonheirs_AreCorrectlyInheritedTo4LevelsFromRoot():
    # ESTABLISH
    a4_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = a4_bud.make_l1_way(casa_str)
    week_str = "weekdays"
    week_way = a4_bud.make_l1_way(week_str)
    wed_str = "Wednesday"
    wed_way = a4_bud.make_way(week_way, wed_str)

    wed_premise = premiseunit_shop(branch=wed_way)
    wed_premise._status = False
    wed_premise._task = False

    premises_x = {wed_premise.branch: wed_premise}
    casa_wk_build_reasonunit = reasonunit_shop(context=week_way, premises=premises_x)
    casa_wk_built_reasonheir = reasonheir_shop(
        context=week_way,
        premises=premises_x,
        _status=False,
        _context_idea_active_value=True,
    )
    a4_bud.edit_idea_attr(casa_way, reason=casa_wk_build_reasonunit)

    # WHEN
    rla_str = "hp"
    rla_way = a4_bud.make_way(casa_way, rla_str)
    a4_bud.set_idea(ideaunit_shop(rla_str), parent_way=rla_way)
    cost_str = "cost_quantification"
    cost_way = a4_bud.make_way(rla_way, cost_str)
    a4_bud.set_idea(ideaunit_shop(cost_str), parent_way=cost_way)
    a4_bud.settle_bud()

    # THEN
    casa_idea = a4_bud.idearoot._kids[casa_str]
    rla_idea = casa_idea._kids[rla_str]
    cost_idea = rla_idea._kids[cost_str]

    # 1
    casa_wk_calc_reasonheir = casa_idea._reasonheirs[week_way]
    assert casa_wk_calc_reasonheir == casa_wk_built_reasonheir

    # 2
    rla_week_reasonheir = rla_idea._reasonheirs[week_way]
    assert rla_week_reasonheir.context == casa_wk_built_reasonheir.context
    assert rla_week_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        rla_week_reasonheir.context_idea_active_requisite
        == casa_wk_built_reasonheir.context_idea_active_requisite
    )
    assert rla_week_reasonheir._status == casa_wk_built_reasonheir._status
    assert rla_week_reasonheir._task == casa_wk_built_reasonheir._task
    assert rla_week_reasonheir._context_idea_active_value
    assert rla_week_reasonheir._context_idea_active_value != casa_wk_built_reasonheir

    # 3
    cost_week_reasonheir = cost_idea._reasonheirs[week_way]
    assert cost_week_reasonheir.context == casa_wk_built_reasonheir.context
    assert cost_week_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        cost_week_reasonheir.context_idea_active_requisite
        == casa_wk_built_reasonheir.context_idea_active_requisite
    )
    assert cost_week_reasonheir._status == casa_wk_built_reasonheir._status
    assert cost_week_reasonheir._task == casa_wk_built_reasonheir._task
    assert cost_week_reasonheir._context_idea_active_value
    assert cost_week_reasonheir._context_idea_active_value != casa_wk_built_reasonheir


def test_BudUnit_reasonheirs_AreCorrectlyInheritedTo4LevelsFromLevel2():
    a4_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = a4_bud.make_l1_way(casa_str)
    week_idea_tag = "weekdays"
    week_way = a4_bud.make_l1_way(week_idea_tag)
    wed_str = "Wednesday"
    wed_way = a4_bud.make_way(week_way, wed_str)

    wed_premise = premiseunit_shop(branch=wed_way)
    wed_premise._status = False
    wed_premise._task = False
    premises = {wed_premise.branch: wed_premise}
    casa_wk_build_reasonunit = reasonunit_shop(week_way, premises=premises)
    casa_wk_built_reasonheir = reasonheir_shop(
        context=week_way,
        premises=premises,
        _status=False,
        _context_idea_active_value=True,
    )
    a4_bud.edit_idea_attr(casa_way, reason=casa_wk_build_reasonunit)
    rla_str = "hp"
    rla_way = a4_bud.make_way(casa_way, rla_str)
    a4_bud.set_idea(ideaunit_shop(rla_str), parent_way=rla_way)
    cost_str = "cost_quantification"
    cost_way = a4_bud.make_way(rla_way, cost_str)
    a4_bud.set_idea(ideaunit_shop(cost_str), parent_way=cost_way)

    casa_idea = a4_bud.idearoot.get_kid(casa_str)
    rla_idea = casa_idea.get_kid(rla_str)
    cost_idea = rla_idea.get_kid(cost_str)

    assert a4_bud.idearoot._reasonheirs == {}
    assert casa_idea._reasonheirs == {}
    assert rla_idea._reasonheirs == {}
    assert cost_idea._reasonheirs == {}

    # WHEN
    a4_bud.settle_bud()

    # THEN
    assert a4_bud.idearoot._reasonheirs == {}  # casa_wk_built_reasonheir

    # 1
    assert casa_idea._reasonheirs[week_way] == casa_wk_built_reasonheir

    # 2
    rla_week_reasonheir = rla_idea._reasonheirs[week_way]
    assert rla_week_reasonheir.context == casa_wk_built_reasonheir.context
    assert rla_week_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        rla_week_reasonheir.context_idea_active_requisite
        == casa_wk_built_reasonheir.context_idea_active_requisite
    )
    assert rla_week_reasonheir._status == casa_wk_built_reasonheir._status
    assert rla_week_reasonheir._task == casa_wk_built_reasonheir._task
    assert rla_week_reasonheir._context_idea_active_value
    assert rla_week_reasonheir._context_idea_active_value != casa_wk_built_reasonheir

    # 3
    cost_week_reasonheir = cost_idea._reasonheirs[week_way]
    assert cost_week_reasonheir.context == casa_wk_built_reasonheir.context
    assert cost_week_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        cost_week_reasonheir.context_idea_active_requisite
        == casa_wk_built_reasonheir.context_idea_active_requisite
    )
    assert cost_week_reasonheir._status == casa_wk_built_reasonheir._status
    assert cost_week_reasonheir._task == casa_wk_built_reasonheir._task
    assert cost_week_reasonheir._context_idea_active_value
    assert cost_week_reasonheir._context_idea_active_value != casa_wk_built_reasonheir


def test_BudUnit_ReasonUnits_set_UnCoupledMethod():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    week_str = "weekdays"
    week_way = sue_bud.make_l1_way(week_str)
    wed_str = "Wednesday"
    wed_way = sue_bud.make_way(week_way, wed_str)

    # WHEN
    sue_bud.edit_idea_attr(casa_way, reason_context=week_way, reason_premise=wed_way)

    # THEN
    casa_idea1 = sue_bud.get_idea_obj(casa_way)
    assert casa_idea1.reasonunits is not None
    print(casa_idea1.reasonunits)
    assert casa_idea1.reasonunits[week_way] is not None
    assert casa_idea1.reasonunits[week_way].premises[wed_way].open is None
    assert casa_idea1.reasonunits[week_way].premises[wed_way].nigh is None

    casa_wk_reason1 = reasonunit_shop(week_way)
    casa_wk_reason1.set_premise(premise=wed_way)
    print(f" {type(casa_wk_reason1.context)=}")
    print(f" {casa_wk_reason1.context=}")
    assert casa_idea1.reasonunits[week_way] == casa_wk_reason1

    # ESTABLISH
    divisor_x = 34
    open_x = 12
    nigh_x = 12

    # WHEN
    sue_bud.edit_idea_attr(
        casa_way,
        reason_context=week_way,
        reason_premise=wed_way,
        reason_premise_divisor=divisor_x,
        reason_premise_open=open_x,
        reason_premise_nigh=nigh_x,
    )

    # THEN
    assert casa_idea1.reasonunits[week_way].premises[wed_way].open == 12
    assert casa_idea1.reasonunits[week_way].premises[wed_way].nigh == 12

    wed_premise2 = premiseunit_shop(
        branch=wed_way, divisor=divisor_x, open=open_x, nigh=nigh_x
    )
    casa_wk_reason2 = reasonunit_shop(
        context=week_way, premises={wed_premise2.branch: wed_premise2}
    )
    print(f"{type(casa_wk_reason2.context)=}")
    print(f"{casa_wk_reason2.context=}")
    assert casa_idea1.reasonunits[week_way] == casa_wk_reason2

    # WHEN
    thu_str = "Thursday"
    thu_way = sue_bud.make_way(week_way, thu_str)
    sue_bud.edit_idea_attr(
        casa_way,
        reason_context=week_way,
        reason_premise=thu_way,
        reason_premise_divisor=divisor_x,
        reason_premise_open=open_x,
        reason_premise_nigh=nigh_x,
    )

    # THEN
    assert len(casa_idea1.reasonunits[week_way].premises) == 2


def test_BudUnit_ReasonUnits_set_premiseIdeaWithDenomSetsPremiseDivision():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    time_str = "time"
    time_way = sue_bud.make_l1_way(time_str)
    week_str = "week"
    week_way = sue_bud.make_way(time_way, week_str)
    sue_bud.set_l1_idea(ideaunit_shop(time_str, begin=100, close=2000))
    sue_bud.set_idea(ideaunit_shop(week_str, denom=7), parent_way=time_way)

    # WHEN
    sue_bud.edit_idea_attr(
        casa_way,
        reason_context=time_way,
        reason_premise=week_way,
        reason_premise_open=2,
        reason_premise_nigh=5,
        reason_premise_divisor=None,
    )

    # THEN
    casa_idea1 = sue_bud.get_idea_obj(casa_way)
    assert casa_idea1.reasonunits[time_way] is not None
    assert casa_idea1.reasonunits[time_way].premises[week_way].divisor == 7
    assert casa_idea1.reasonunits[time_way].premises[week_way].open == 2
    assert casa_idea1.reasonunits[time_way].premises[week_way].nigh == 5


def test_BudUnit_ReasonUnits_set_premiseIdeaWithBeginCloseSetsPremiseOpen_Nigh():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa = "casa"
    casa_way = sue_bud.make_l1_way(casa)
    time = "time"
    time_way = sue_bud.make_l1_way(time)
    rus_war = "rus_war"
    rus_war_way = sue_bud.make_way(time_way, rus_war)
    sue_bud.set_idea(ideaunit_shop(time, begin=100, close=2000), sue_bud.fisc_tag)
    sue_bud.set_idea(ideaunit_shop(rus_war, begin=22, close=34), time_way)

    # WHEN
    sue_bud.edit_idea_attr(
        casa_way,
        reason_context=time_way,
        reason_premise=rus_war_way,
        reason_premise_open=None,
        reason_premise_nigh=None,
        reason_premise_divisor=None,
    )

    # THEN
    casa_idea1 = sue_bud.get_idea_obj(casa_way)
    assert casa_idea1.reasonunits[time_way] is not None
    assert casa_idea1.reasonunits[time_way].premises[rus_war_way].divisor is None
    assert casa_idea1.reasonunits[time_way].premises[rus_war_way].open == 22
    assert casa_idea1.reasonunits[time_way].premises[rus_war_way].nigh == 34


def test_BudUnit_ReasonUnits_edit_idea_attr_CorrectlyDeletes_ReasonUnits_And_PremiseUnits():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_way = sue_bud.make_l1_way("casa")
    weekday_way = sue_bud.make_l1_way("weekdays")
    wed_way = sue_bud.make_way(weekday_way, "Wednesday")

    sue_bud.edit_idea_attr(casa_way, reason_context=weekday_way, reason_premise=wed_way)
    thu_way = sue_bud.make_way(weekday_way, "Thursday")
    sue_bud.edit_idea_attr(
        casa_way,
        reason_context=weekday_way,
        reason_premise=thu_way,
    )
    casa_idea1 = sue_bud.get_idea_obj(casa_way)
    assert len(casa_idea1.reasonunits[weekday_way].premises) == 2

    # WHEN
    sue_bud.edit_idea_attr(
        casa_way,
        reason_del_premise_context=weekday_way,
        reason_del_premise_branch=thu_way,
    )

    # THEN
    assert len(casa_idea1.reasonunits[weekday_way].premises) == 1

    # WHEN
    sue_bud.edit_idea_attr(
        casa_way,
        reason_del_premise_context=weekday_way,
        reason_del_premise_branch=wed_way,
    )

    # THEN
    with pytest_raises(KeyError) as excinfo:
        casa_idea1.reasonunits[weekday_way]
    assert str(excinfo.value) == f"'{weekday_way}'"
    assert casa_idea1.reasonunits == {}


def test_BudUnit_ReasonUnits_del_reason_premise_UncoupledMethod2():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_way = sue_bud.make_l1_way("casa")
    weekdays_way = sue_bud.make_l1_way("weekdays")
    casa_idea1 = sue_bud.get_idea_obj(casa_way)
    assert len(casa_idea1.reasonunits) == 0

    # WHEN
    with pytest_raises(Exception) as excinfo:
        casa_idea1.del_reasonunit_context(weekdays_way)
    assert str(excinfo.value) == f"No ReasonUnit at '{weekdays_way}'"


def test_BudUnit_edit_idea_attr_budIsAbleToEdit_context_idea_active_requisite_AnyIdeaIfInvaildThrowsError():
    # _context_idea_active_requisite: str = None
    # must be 1 of 3: bool: True, bool: False, str="Set to Ignore"
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)

    run_str = "run to casa"
    run_way = sue_bud.make_l1_way(run_str)
    sue_bud.set_idea(ideaunit_shop(run_str), sue_bud.fisc_tag)
    sue_bud.settle_bud()  # set tree metrics
    run_idea = sue_bud.get_idea_obj(run_way)
    assert len(run_idea.reasonunits) == 0

    # WHEN
    sue_bud.edit_idea_attr(
        run_way,
        reason_context=casa_way,
        reason_context_idea_active_requisite=True,
    )

    # THEN
    assert len(run_idea.reasonunits) == 1
    reasonunit_casa = run_idea.reasonunits.get(casa_way)
    assert reasonunit_casa.context == casa_way
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.context_idea_active_requisite is True

    # WHEN
    sue_bud.edit_idea_attr(
        run_way,
        reason_context=casa_way,
        reason_context_idea_active_requisite=False,
    )

    # THEN
    assert len(run_idea.reasonunits) == 1
    reasonunit_casa = run_idea.reasonunits.get(casa_way)
    assert reasonunit_casa.context == casa_way
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.context_idea_active_requisite is False

    # WHEN
    sue_bud.edit_idea_attr(
        run_way,
        reason_context=casa_way,
        reason_context_idea_active_requisite="Set to Ignore",
    )

    # THEN
    assert len(run_idea.reasonunits) == 1
    reasonunit_casa = run_idea.reasonunits.get(casa_way)
    assert reasonunit_casa.context == casa_way
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.context_idea_active_requisite is None


def test_BudUnit_ReasonUnits_IdeaUnit_active_InfluencesReasonUnitStatus():
    # ESTABLISH an Bud with 5 ideas, 1 Fact:
    # 1. idea(...,weekdays) exists
    # 2. idea(...,weekdays,wednesday) exists
    # 3. idea(...,weekdays,thursday) exists
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_way = sue_bud.make_l1_way(casa_str)
    weekdays_str = "weekdays"
    weekdays_way = sue_bud.make_l1_way(weekdays_str)
    wed_str = "Wednesday"
    wed_way = sue_bud.make_way(weekdays_way, wed_str)
    thu_str = "Thursday"
    thu_way = sue_bud.make_way(weekdays_way, thu_str)

    # 4. idea(...,casa) with
    # 4.1 ReasonUnit: context=weekdays_way, branch=thu_way
    # 4.2 .active = False
    sue_bud.edit_idea_attr(
        casa_way,
        reason_context=weekdays_way,
        reason_premise=thu_way,
    )
    sue_bud.settle_bud()  # set tree metrics
    casa_idea = sue_bud.get_idea_obj(casa_way)
    assert casa_idea._active is False

    # 5. idea(...,run to casa) with
    # 5.1. ReasonUnit: idea(context=...,casa) has .context_idea_active_requisite = True
    # 5.2. idea(...,casa).active = False
    run_str = "run to casa"
    run_way = sue_bud.make_l1_way(run_str)
    sue_bud.set_idea(ideaunit_shop(run_str), sue_bud.fisc_tag)
    sue_bud.edit_idea_attr(
        run_way,
        reason_context=casa_way,
        reason_context_idea_active_requisite=True,
    )
    run_idea = sue_bud.get_idea_obj(run_way)
    sue_bud.settle_bud()
    assert run_idea._active is False

    # Fact: context: (...,weekdays) fbranch: (...,weekdays,wednesday)
    sue_bud.add_fact(fcontext=weekdays_way, fbranch=wed_way)
    sue_bud.settle_bud()

    assert casa_idea._active is False
    assert run_idea._active is False

    # WHEN
    print("before changing fact")
    sue_bud.add_fact(fcontext=weekdays_way, fbranch=thu_way)
    print("after changing fact")
    sue_bud.settle_bud()
    assert casa_idea._active is True

    # THEN
    assert run_idea._active is True


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
    # for idea_key in sue_bud._idea_dict.keys():
    #     print(f"{idea_key=}")

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
