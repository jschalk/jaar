from pytest import raises as pytest_raises
from src.bud.examples.example_buds import (
    get_budunit_with_4_levels,
    get_budunit_irrational_example,
)
from src.bud.idea import ideaunit_shop
from src.bud.reason_idea import premiseunit_shop, reasonunit_shop, reasonheir_shop
from src.bud.bud import budunit_shop


def test_BudUnit_ReasonUnits_create():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    weekday_str = "weekdays"
    weekday_road = sue_bud.make_l1_road(weekday_str)
    wed_str = "Wednesday"
    wed_road = sue_bud.make_road(weekday_road, wed_str)

    wed_premise = premiseunit_shop(need=wed_road)
    casa_wk_reason = reasonunit_shop(weekday_road, {wed_premise.need: wed_premise})
    print(f"{type(casa_wk_reason.base)=}")
    print(f"{casa_wk_reason.base=}")

    # WHEN
    sue_bud.edit_idea_attr(casa_road, reason=casa_wk_reason)

    # THEN
    casa_idea = sue_bud.get_idea_obj(casa_road)
    assert casa_idea.reasonunits is not None
    print(casa_idea.reasonunits)
    assert casa_idea.reasonunits[weekday_road] is not None
    assert casa_idea.reasonunits[weekday_road] == casa_wk_reason


def test_BudUnit_edit_idea_attr_reasonunit_CorrectlySets_delimiter():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_road = sue_bud.make_l1_road("casa")
    week_road = sue_bud.make_l1_road("weekdays")
    wed_road = sue_bud.make_road(week_road, "Wednesday")

    slash_str = "/"
    before_week_reason = reasonunit_shop(week_road, delimiter=slash_str)
    before_week_reason.set_premise(wed_road)
    assert before_week_reason.delimiter == slash_str

    # WHEN
    sue_bud.edit_idea_attr(casa_road, reason=before_week_reason)

    # THEN
    casa_idea = sue_bud.get_idea_obj(casa_road)
    week_reasonunit = casa_idea.reasonunits.get(week_road)
    assert week_reasonunit.delimiter != slash_str
    assert week_reasonunit.delimiter == sue_bud._road_delimiter


def test_BudUnit_edit_idea_attr_reason_base_CorrectlySets_delimiter():
    # ESTABLISH
    slash_str = "/"
    bob_bud = budunit_shop("Bob", _road_delimiter=slash_str)
    casa_str = "casa"
    week_str = "week"
    wed_str = "Wednesday"
    casa_road = bob_bud.make_l1_road(casa_str)
    week_road = bob_bud.make_l1_road(week_str)
    wed_road = bob_bud.make_road(week_road, wed_str)
    bob_bud.set_l1_idea(ideaunit_shop(casa_str))
    bob_bud.set_l1_idea(ideaunit_shop(week_str))
    bob_bud.set_idea(ideaunit_shop(wed_str), week_road)
    print(f"{bob_bud._idearoot._kids.keys()=}")
    wed_idea = bob_bud.get_idea_obj(wed_road)
    assert wed_idea._road_delimiter == slash_str
    assert wed_idea._road_delimiter == bob_bud._road_delimiter

    # WHEN
    bob_bud.edit_idea_attr(casa_road, reason_base=week_road, reason_premise=wed_road)

    # THEN
    casa_idea = bob_bud.get_idea_obj(casa_road)
    assert casa_idea._road_delimiter == slash_str
    week_reasonunit = casa_idea.reasonunits.get(week_road)
    assert week_reasonunit.delimiter != ","
    assert week_reasonunit.delimiter == bob_bud._road_delimiter


def test_BudUnit_set_reasonunits_status():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    weekday_str = "weekdays"
    weekday_road = sue_bud.make_l1_road(weekday_str)
    wed_str = "Wednesday"
    wed_road = sue_bud.make_road(weekday_road, wed_str)

    wed_premise = premiseunit_shop(need=wed_road)
    casa_wk_reason = reasonunit_shop(
        base=weekday_road, premises={wed_premise.need: wed_premise}
    )
    print(f"{type(casa_wk_reason.base)=}")
    print(f"{casa_wk_reason.base=}")

    # WHEN
    sue_bud.edit_idea_attr(casa_road, reason=casa_wk_reason)

    # THEN
    casa_idea = sue_bud.get_idea_obj(casa_road)
    assert casa_idea.reasonunits is not None
    print(casa_idea.reasonunits)
    assert casa_idea.reasonunits[weekday_road] is not None
    assert casa_idea.reasonunits[weekday_road] == casa_wk_reason


def test_agenda_returned_WhenNoReasonsExist():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()

    # WHEN
    sue_bud.settle_bud()

    # THEN
    casa_road = sue_bud.make_l1_road("casa")
    assert sue_bud.get_idea_obj(casa_road)._task is True
    cat_road = sue_bud.make_l1_road("cat have dinner")
    assert sue_bud.get_idea_obj(cat_road)._task is True


def test_BudUnit_reasonheirs_AreCorrectlyInherited_v1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    print(f"{sue_bud._fiscal_id=}")
    print(f"{sue_bud._idearoot._label=}")
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    week_label = "weekdays"
    week_road = sue_bud.make_l1_road(week_label)
    wed_str = "Wednesday"
    wed_road = sue_bud.make_road(week_road, wed_str)

    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = False
    wed_premise._task = False
    premises = {wed_premise.need: wed_premise}
    casa_wk_build_reasonunit = reasonunit_shop(week_road, premises=premises)
    casa_wk_built_reasonheir = reasonheir_shop(
        base=week_road,
        premises=premises,
        _status=False,
        _base_idea_active_value=True,
    )
    print(f"{casa_wk_build_reasonunit.base=}")
    sue_bud.edit_idea_attr(casa_road, reason=casa_wk_build_reasonunit)
    casa_idea = sue_bud.get_idea_obj(casa_road)
    assert casa_idea.reasonunits != {}
    # print(casa_idea.reasonunits)
    assert casa_idea.reasonunits[week_road] is not None
    assert casa_idea.reasonunits[week_road] == casa_wk_build_reasonunit
    weekdays_str = "weekdays"
    try:
        casa_idea._reasonheirs[week_road]
    except KeyError as e:
        assert str(e) == f"'{sue_bud.make_l1_road(weekdays_str)}'"

    # WHEN
    sue_bud.settle_bud()

    # THEN
    casa_wk_cal_reasonheir = casa_idea._reasonheirs[week_road]
    print(f"{len(casa_wk_cal_reasonheir.premises)=}")
    assert len(casa_wk_cal_reasonheir.premises) == 1
    premise_wed = casa_wk_cal_reasonheir.premises.get(wed_road)
    wed_task = casa_wk_built_reasonheir.premises.get(premise_wed.need)._task
    assert premise_wed._task == wed_task
    assert premise_wed == casa_wk_built_reasonheir.premises[premise_wed.need]
    # for premise in casa_wk_cal_reasonheir.premises.values():
    #     # assert premise_task == casa_wk_built_reasonheir.premises[premise.need]._task
    #     assert (
    #         premise._task == casa_wk_built_reasonheir.premises[premise.need]._task
    #     )
    #     assert premise == casa_wk_built_reasonheir.premises[premise.need]
    assert casa_wk_cal_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert casa_wk_cal_reasonheir == casa_wk_built_reasonheir


def test_BudUnit_reasonheirs_AreCorrectlyInheritedTo4LevelsFromRoot():
    # ESTABLISH
    a4_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_road = a4_bud.make_l1_road(casa_str)
    week_str = "weekdays"
    week_road = a4_bud.make_l1_road(week_str)
    wed_str = "Wednesday"
    wed_road = a4_bud.make_road(week_road, wed_str)

    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = False
    wed_premise._task = False

    premises_x = {wed_premise.need: wed_premise}
    casa_wk_build_reasonunit = reasonunit_shop(base=week_road, premises=premises_x)
    casa_wk_built_reasonheir = reasonheir_shop(
        base=week_road,
        premises=premises_x,
        _status=False,
        _base_idea_active_value=True,
    )
    a4_bud.edit_idea_attr(casa_road, reason=casa_wk_build_reasonunit)

    # WHEN
    rla_str = "hp"
    rla_road = a4_bud.make_road(casa_road, rla_str)
    a4_bud.set_idea(ideaunit_shop(rla_str), parent_road=rla_road)
    cost_str = "cost_quantification"
    cost_road = a4_bud.make_road(rla_road, cost_str)
    a4_bud.set_idea(ideaunit_shop(cost_str), parent_road=cost_road)
    a4_bud.settle_bud()

    # THEN
    casa_idea = a4_bud._idearoot._kids[casa_str]
    rla_idea = casa_idea._kids[rla_str]
    cost_idea = rla_idea._kids[cost_str]

    # 1
    casa_wk_calc_reasonheir = casa_idea._reasonheirs[week_road]
    assert casa_wk_calc_reasonheir == casa_wk_built_reasonheir

    # 2
    rla_week_reasonheir = rla_idea._reasonheirs[week_road]
    assert rla_week_reasonheir.base == casa_wk_built_reasonheir.base
    assert rla_week_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        rla_week_reasonheir.base_idea_active_requisite
        == casa_wk_built_reasonheir.base_idea_active_requisite
    )
    assert rla_week_reasonheir._status == casa_wk_built_reasonheir._status
    assert rla_week_reasonheir._task == casa_wk_built_reasonheir._task
    assert rla_week_reasonheir._base_idea_active_value
    assert rla_week_reasonheir._base_idea_active_value != casa_wk_built_reasonheir

    # 3
    cost_week_reasonheir = cost_idea._reasonheirs[week_road]
    assert cost_week_reasonheir.base == casa_wk_built_reasonheir.base
    assert cost_week_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        cost_week_reasonheir.base_idea_active_requisite
        == casa_wk_built_reasonheir.base_idea_active_requisite
    )
    assert cost_week_reasonheir._status == casa_wk_built_reasonheir._status
    assert cost_week_reasonheir._task == casa_wk_built_reasonheir._task
    assert cost_week_reasonheir._base_idea_active_value
    assert cost_week_reasonheir._base_idea_active_value != casa_wk_built_reasonheir


def test_BudUnit_reasonheirs_AreCorrectlyInheritedTo4LevelsFromLevel2():
    a4_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_road = a4_bud.make_l1_road(casa_str)
    week_label = "weekdays"
    week_road = a4_bud.make_l1_road(week_label)
    wed_str = "Wednesday"
    wed_road = a4_bud.make_road(week_road, wed_str)

    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = False
    wed_premise._task = False
    premises = {wed_premise.need: wed_premise}
    casa_wk_build_reasonunit = reasonunit_shop(week_road, premises=premises)
    casa_wk_built_reasonheir = reasonheir_shop(
        base=week_road,
        premises=premises,
        _status=False,
        _base_idea_active_value=True,
    )
    a4_bud.edit_idea_attr(casa_road, reason=casa_wk_build_reasonunit)
    rla_str = "hp"
    rla_road = a4_bud.make_road(casa_road, rla_str)
    a4_bud.set_idea(ideaunit_shop(rla_str), parent_road=rla_road)
    cost_str = "cost_quantification"
    cost_road = a4_bud.make_road(rla_road, cost_str)
    a4_bud.set_idea(ideaunit_shop(cost_str), parent_road=cost_road)

    casa_idea = a4_bud._idearoot.get_kid(casa_str)
    rla_idea = casa_idea.get_kid(rla_str)
    cost_idea = rla_idea.get_kid(cost_str)

    assert a4_bud._idearoot._reasonheirs == {}
    assert casa_idea._reasonheirs == {}
    assert rla_idea._reasonheirs == {}
    assert cost_idea._reasonheirs == {}

    # WHEN
    a4_bud.settle_bud()

    # THEN
    assert a4_bud._idearoot._reasonheirs == {}  # casa_wk_built_reasonheir

    # 1
    assert casa_idea._reasonheirs[week_road] == casa_wk_built_reasonheir

    # 2
    rla_week_reasonheir = rla_idea._reasonheirs[week_road]
    assert rla_week_reasonheir.base == casa_wk_built_reasonheir.base
    assert rla_week_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        rla_week_reasonheir.base_idea_active_requisite
        == casa_wk_built_reasonheir.base_idea_active_requisite
    )
    assert rla_week_reasonheir._status == casa_wk_built_reasonheir._status
    assert rla_week_reasonheir._task == casa_wk_built_reasonheir._task
    assert rla_week_reasonheir._base_idea_active_value
    assert rla_week_reasonheir._base_idea_active_value != casa_wk_built_reasonheir

    # 3
    cost_week_reasonheir = cost_idea._reasonheirs[week_road]
    assert cost_week_reasonheir.base == casa_wk_built_reasonheir.base
    assert cost_week_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        cost_week_reasonheir.base_idea_active_requisite
        == casa_wk_built_reasonheir.base_idea_active_requisite
    )
    assert cost_week_reasonheir._status == casa_wk_built_reasonheir._status
    assert cost_week_reasonheir._task == casa_wk_built_reasonheir._task
    assert cost_week_reasonheir._base_idea_active_value
    assert cost_week_reasonheir._base_idea_active_value != casa_wk_built_reasonheir


def test_BudUnit_ReasonUnits_set_UnCoupledMethod():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    week_str = "weekdays"
    week_road = sue_bud.make_l1_road(week_str)
    wed_str = "Wednesday"
    wed_road = sue_bud.make_road(week_road, wed_str)

    # WHEN
    sue_bud.edit_idea_attr(
        road=casa_road, reason_base=week_road, reason_premise=wed_road
    )

    # THEN
    casa_idea1 = sue_bud.get_idea_obj(casa_road)
    assert casa_idea1.reasonunits is not None
    print(casa_idea1.reasonunits)
    assert casa_idea1.reasonunits[week_road] is not None
    assert casa_idea1.reasonunits[week_road].premises[wed_road].open is None
    assert casa_idea1.reasonunits[week_road].premises[wed_road].nigh is None

    casa_wk_reason1 = reasonunit_shop(week_road)
    casa_wk_reason1.set_premise(premise=wed_road)
    print(f" {type(casa_wk_reason1.base)=}")
    print(f" {casa_wk_reason1.base=}")
    assert casa_idea1.reasonunits[week_road] == casa_wk_reason1

    # ESTABLISH
    divisor_x = 34
    open_x = 12
    nigh_x = 12

    # WHEN
    sue_bud.edit_idea_attr(
        road=casa_road,
        reason_base=week_road,
        reason_premise=wed_road,
        reason_premise_divisor=divisor_x,
        reason_premise_open=open_x,
        reason_premise_nigh=nigh_x,
    )

    # THEN
    assert casa_idea1.reasonunits[week_road].premises[wed_road].open == 12
    assert casa_idea1.reasonunits[week_road].premises[wed_road].nigh == 12

    wed_premise2 = premiseunit_shop(
        need=wed_road, divisor=divisor_x, open=open_x, nigh=nigh_x
    )
    casa_wk_reason2 = reasonunit_shop(
        base=week_road, premises={wed_premise2.need: wed_premise2}
    )
    print(f"{type(casa_wk_reason2.base)=}")
    print(f"{casa_wk_reason2.base=}")
    assert casa_idea1.reasonunits[week_road] == casa_wk_reason2

    # WHEN
    thu_str = "Thursday"
    thu_road = sue_bud.make_road(week_road, thu_str)
    sue_bud.edit_idea_attr(
        road=casa_road,
        reason_base=week_road,
        reason_premise=thu_road,
        reason_premise_divisor=divisor_x,
        reason_premise_open=open_x,
        reason_premise_nigh=nigh_x,
    )

    # THEN
    assert len(casa_idea1.reasonunits[week_road].premises) == 2


def test_BudUnit_ReasonUnits_set_premiseIdeaWithDenomSetsPremiseDivision():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    time_str = "time"
    time_road = sue_bud.make_l1_road(time_str)
    week_str = "week"
    week_road = sue_bud.make_road(time_road, week_str)
    sue_bud.set_l1_idea(ideaunit_shop(time_str, begin=100, close=2000))
    sue_bud.set_idea(ideaunit_shop(week_str, denom=7), parent_road=time_road)

    # WHEN
    sue_bud.edit_idea_attr(
        road=casa_road,
        reason_base=time_road,
        reason_premise=week_road,
        reason_premise_open=2,
        reason_premise_nigh=5,
        reason_premise_divisor=None,
    )

    # THEN
    casa_idea1 = sue_bud.get_idea_obj(casa_road)
    assert casa_idea1.reasonunits[time_road] is not None
    assert casa_idea1.reasonunits[time_road].premises[week_road].divisor == 7
    assert casa_idea1.reasonunits[time_road].premises[week_road].open == 2
    assert casa_idea1.reasonunits[time_road].premises[week_road].nigh == 5


def test_BudUnit_ReasonUnits_set_premiseIdeaWithBeginCloseSetsPremiseOpen_Nigh():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa = "casa"
    casa_road = sue_bud.make_l1_road(casa)
    time = "time"
    time_road = sue_bud.make_l1_road(time)
    rus_war = "rus_war"
    rus_war_road = sue_bud.make_road(time_road, rus_war)
    sue_bud.set_idea(ideaunit_shop(time, begin=100, close=2000), sue_bud._fiscal_id)
    sue_bud.set_idea(ideaunit_shop(rus_war, begin=22, close=34), time_road)

    # WHEN
    sue_bud.edit_idea_attr(
        road=casa_road,
        reason_base=time_road,
        reason_premise=rus_war_road,
        reason_premise_open=None,
        reason_premise_nigh=None,
        reason_premise_divisor=None,
    )

    # THEN
    casa_idea1 = sue_bud.get_idea_obj(casa_road)
    assert casa_idea1.reasonunits[time_road] is not None
    assert casa_idea1.reasonunits[time_road].premises[rus_war_road].divisor is None
    assert casa_idea1.reasonunits[time_road].premises[rus_war_road].open == 22
    assert casa_idea1.reasonunits[time_road].premises[rus_war_road].nigh == 34


def test_BudUnit_ReasonUnits_edit_idea_attr_CorrectlyDeletes_ReasonUnits_And_PremiseUnits():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_road = sue_bud.make_l1_road("casa")
    weekday_road = sue_bud.make_l1_road("weekdays")
    wed_road = sue_bud.make_road(weekday_road, "Wednesday")

    sue_bud.edit_idea_attr(
        road=casa_road, reason_base=weekday_road, reason_premise=wed_road
    )
    thu_road = sue_bud.make_road(weekday_road, "Thursday")
    sue_bud.edit_idea_attr(
        road=casa_road,
        reason_base=weekday_road,
        reason_premise=thu_road,
    )
    casa_idea1 = sue_bud.get_idea_obj(casa_road)
    assert len(casa_idea1.reasonunits[weekday_road].premises) == 2

    # WHEN
    sue_bud.edit_idea_attr(
        road=casa_road,
        reason_del_premise_base=weekday_road,
        reason_del_premise_need=thu_road,
    )

    # THEN
    assert len(casa_idea1.reasonunits[weekday_road].premises) == 1

    # WHEN
    sue_bud.edit_idea_attr(
        road=casa_road,
        reason_del_premise_base=weekday_road,
        reason_del_premise_need=wed_road,
    )

    # THEN
    with pytest_raises(KeyError) as excinfo:
        casa_idea1.reasonunits[weekday_road]
    assert str(excinfo.value) == f"'{weekday_road}'"
    assert casa_idea1.reasonunits == {}


def test_BudUnit_ReasonUnits_del_reason_premise_UncoupledMethod2():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_road = sue_bud.make_l1_road("casa")
    weekdays_road = sue_bud.make_l1_road("weekdays")
    casa_idea1 = sue_bud.get_idea_obj(casa_road)
    assert len(casa_idea1.reasonunits) == 0

    # WHEN
    with pytest_raises(Exception) as excinfo:
        casa_idea1.del_reasonunit_base(weekdays_road)
    assert str(excinfo.value) == f"No ReasonUnit at '{weekdays_road}'"


def test_BudUnit_edit_idea_attr_budIsAbleToEdit_base_idea_active_requisite_AnyIdeaIfInvaildThrowsError():
    # _base_idea_active_requisite: str = None
    # must be 1 of 3: bool: True, bool: False, str="Set to Ignore"
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)

    commute_str = "commute to casa"
    commute_road = sue_bud.make_l1_road(commute_str)
    sue_bud.set_idea(ideaunit_shop(commute_str), sue_bud._fiscal_id)
    sue_bud.settle_bud()  # set tree metrics
    commute_idea = sue_bud.get_idea_obj(commute_road)
    assert len(commute_idea.reasonunits) == 0

    # WHEN
    sue_bud.edit_idea_attr(
        road=commute_road,
        reason_base=casa_road,
        reason_base_idea_active_requisite=True,
    )

    # THEN
    assert len(commute_idea.reasonunits) == 1
    reasonunit_casa = commute_idea.reasonunits.get(casa_road)
    assert reasonunit_casa.base == casa_road
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.base_idea_active_requisite is True

    # WHEN
    sue_bud.edit_idea_attr(
        road=commute_road,
        reason_base=casa_road,
        reason_base_idea_active_requisite=False,
    )

    # THEN
    assert len(commute_idea.reasonunits) == 1
    reasonunit_casa = commute_idea.reasonunits.get(casa_road)
    assert reasonunit_casa.base == casa_road
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.base_idea_active_requisite is False

    # WHEN
    sue_bud.edit_idea_attr(
        road=commute_road,
        reason_base=casa_road,
        reason_base_idea_active_requisite="Set to Ignore",
    )

    # THEN
    assert len(commute_idea.reasonunits) == 1
    reasonunit_casa = commute_idea.reasonunits.get(casa_road)
    assert reasonunit_casa.base == casa_road
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.base_idea_active_requisite is None


def test_BudUnit_ReasonUnits_IdeaUnit_active_InfluencesReasonUnitStatus():
    # ESTABLISH an Bud with 5 ideas, 1 Fact:
    # 1. idea(...,weekdays) exists
    # 2. idea(...,weekdays,wednesday) exists
    # 3. idea(...,weekdays,thursday) exists
    sue_bud = get_budunit_with_4_levels()
    casa_str = "casa"
    casa_road = sue_bud.make_l1_road(casa_str)
    weekdays_str = "weekdays"
    weekdays_road = sue_bud.make_l1_road(weekdays_str)
    wed_str = "Wednesday"
    wed_road = sue_bud.make_road(weekdays_road, wed_str)
    thu_str = "Thursday"
    thu_road = sue_bud.make_road(weekdays_road, thu_str)

    # 4. idea(...,casa) with
    # 4.1 ReasonUnit: base=weekdays_road, need=thu_road
    # 4.2 .active = False
    sue_bud.edit_idea_attr(
        road=casa_road,
        reason_base=weekdays_road,
        reason_premise=thu_road,
    )
    sue_bud.settle_bud()  # set tree metrics
    casa_idea = sue_bud.get_idea_obj(casa_road)
    assert casa_idea._active is False

    # 5. idea(...,commute to casa) with
    # 5.1. ReasonUnit: idea(base=...,casa) has .base_idea_active_requisite = True
    # 5.2. idea(...,casa).active = False
    commute_str = "commute to casa"
    commute_road = sue_bud.make_l1_road(commute_str)
    sue_bud.set_idea(ideaunit_shop(commute_str), sue_bud._fiscal_id)
    sue_bud.edit_idea_attr(
        road=commute_road,
        reason_base=casa_road,
        reason_base_idea_active_requisite=True,
    )
    commute_idea = sue_bud.get_idea_obj(commute_road)
    sue_bud.settle_bud()
    assert commute_idea._active is False

    # Fact: base: (...,weekdays) pick: (...,weekdays,wednesday)
    sue_bud.set_fact(base=weekdays_road, pick=wed_road)
    sue_bud.settle_bud()

    assert casa_idea._active is False
    assert commute_idea._active is False

    # WHEN
    print("before changing fact")
    sue_bud.set_fact(base=weekdays_road, pick=thu_road)
    print("after changing fact")
    sue_bud.settle_bud()
    assert casa_idea._active is True

    # THEN
    assert commute_idea._active is True


def test_BudUnit_settle_bud_SetsRationalAttrToFalseWhen_max_tree_traverse_Is1():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    assert sue_bud._rational is False
    # sue_bud.settle_bud()
    sue_bud._rational = True
    assert sue_bud._rational

    # WHEN
    # hack bud to set _max_tree_traverse = 1 (not allowed, should be 2 or more)
    sue_bud._max_tree_traverse = 1
    sue_bud.settle_bud()

    # THEN
    assert not sue_bud._rational


def test_BudUnit_tree_traverse_count_SetByTotalNumberOfTreeTraversesEndsStatusIsDetected():
    # ESTABLISH
    sue_bud = get_budunit_with_4_levels()
    assert sue_bud._max_tree_traverse != 2

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
