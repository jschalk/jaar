from src.ch01_rope_logic.rope import create_rope, default_knot_if_None
from src.ch02_finance_logic.finance_config import default_fund_iota_if_None
from src.ch03_group_logic.group import awardunit_shop
from src.ch03_group_logic.labor import laborunit_shop
from src.ch06_plan_logic._ref.ch06_terms import (
    active_hx_str,
    active_str,
    addin_str,
    all_voice_cred_str,
    all_voice_debt_str,
    awardheirs_str,
    awardlines_str,
    awardunits_str,
    begin_str,
    chore_str,
    close_str,
    denom_str,
    descendant_task_count_str,
    factheirs_str,
    factunits_str,
    fund_cease_str,
    fund_iota_str,
    fund_onset_str,
    fund_ratio_str,
    gogo_calc_str,
    gogo_want_str,
    healerunit_ratio_str,
    healerunit_str,
    is_expanded_str,
    kids_str,
    knot_str,
    laborheir_str,
    laborunit_str,
    moment_label_str,
    morph_str,
    numor_str,
    parent_rope_str,
    plan_label_str,
    problem_bool_str,
    range_evaluated_str,
    reasonheirs_str,
    reasonunits_str,
    star_str,
    stop_calc_str,
    stop_want_str,
    task_str,
    tree_level_str,
    uid_str,
)
from src.ch06_plan_logic.healer import healerunit_shop
from src.ch06_plan_logic.plan import PlanUnit, get_default_moment_label, planunit_shop


def test_get_default_moment_label_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_default_moment_label() == "ZZ"


def test_PlanUnit_Exists():
    # ESTABLISH
    x_planunit = PlanUnit()

    # WHEN / THEN
    assert x_planunit
    assert x_planunit.kids is None
    assert x_planunit.star is None
    assert x_planunit.plan_label is None
    assert x_planunit.uid is None
    assert x_planunit.reasonunits is None
    assert x_planunit.reasonheirs is None  # calculated field
    assert x_planunit.laborunit is None
    assert x_planunit.laborheir is None  # calculated field
    assert x_planunit.factunits is None
    assert x_planunit.factheirs is None  # calculated field
    assert x_planunit.awardunits is None
    assert x_planunit.awardlines is None  # calculated field'
    assert x_planunit.awardheirs is None  # calculated field'
    assert x_planunit.knot is None
    assert x_planunit.begin is None
    assert x_planunit.close is None
    assert x_planunit.addin is None
    assert x_planunit.numor is None
    assert x_planunit.denom is None
    assert x_planunit.morph is None
    assert x_planunit.gogo_want is None
    assert x_planunit.stop_want is None
    assert x_planunit.task is None
    assert x_planunit.problem_bool is None
    assert x_planunit.healerunit is None
    # calculated_fields
    assert x_planunit.range_evaluated is None
    assert x_planunit.gogo_calc is None
    assert x_planunit.stop_calc is None
    assert x_planunit.descendant_task_count is None
    assert x_planunit.is_expanded is None
    assert x_planunit.all_voice_cred is None
    assert x_planunit.all_voice_debt is None
    assert x_planunit.tree_level is None
    assert x_planunit.active_hx is None
    assert x_planunit.fund_ratio is None
    assert x_planunit.fund_iota is None
    assert x_planunit.fund_onset is None
    assert x_planunit.fund_cease is None
    assert x_planunit.root is None
    assert x_planunit.moment_label is None
    assert x_planunit.healerunit_ratio is None
    obj_attrs = set(x_planunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        active_str(),
        active_hx_str(),
        all_voice_cred_str(),
        all_voice_debt_str(),
        awardheirs_str(),
        awardlines_str(),
        descendant_task_count_str(),
        factheirs_str(),
        fund_cease_str(),
        fund_onset_str(),
        fund_ratio_str(),
        gogo_calc_str(),
        healerunit_ratio_str(),
        is_expanded_str(),
        kids_str(),
        laborheir_str(),
        tree_level_str(),
        range_evaluated_str(),
        reasonheirs_str(),
        stop_calc_str(),
        chore_str(),
        uid_str(),
        addin_str(),
        awardunits_str(),
        begin_str(),
        knot_str(),
        close_str(),
        plan_label_str(),
        denom_str(),
        factunits_str(),
        moment_label_str(),
        fund_iota_str(),
        gogo_want_str(),
        healerunit_str(),
        laborunit_str(),
        star_str(),
        morph_str(),
        numor_str(),
        parent_rope_str(),
        task_str(),
        problem_bool_str(),
        reasonunits_str(),
        "root",
        stop_want_str(),
    }


def test_planunit_shop_WithNoParametersReturnsObj():
    # ESTABLISH / WHEN
    x_planunit = planunit_shop()

    # THEN
    assert x_planunit
    assert x_planunit.kids == {}
    assert x_planunit.star == 1
    assert x_planunit.plan_label is None
    assert x_planunit.moment_label == get_default_moment_label()
    assert x_planunit.uid is None
    assert x_planunit.begin is None
    assert x_planunit.close is None
    assert x_planunit.addin is None
    assert x_planunit.numor is None
    assert x_planunit.denom is None
    assert x_planunit.morph is None
    assert x_planunit.task is False
    assert x_planunit.problem_bool is False
    assert x_planunit.descendant_task_count is None
    assert x_planunit.awardlines == {}
    assert x_planunit.awardunits == {}
    assert x_planunit.awardheirs == {}
    assert x_planunit.is_expanded is True
    assert x_planunit.factheirs == {}
    assert x_planunit.factunits == {}
    assert x_planunit.healerunit == healerunit_shop()
    assert x_planunit.gogo_calc is None
    assert x_planunit.stop_calc is None
    assert x_planunit.tree_level is None
    assert x_planunit.active_hx == {}
    assert x_planunit.fund_ratio is None
    assert x_planunit.fund_iota == default_fund_iota_if_None()
    assert x_planunit.fund_onset is None
    assert x_planunit.fund_cease is None
    assert x_planunit.reasonunits == {}
    assert x_planunit.reasonheirs == {}
    assert x_planunit.laborunit == laborunit_shop()
    assert x_planunit.laborheir is None
    assert x_planunit.knot == default_knot_if_None()
    assert x_planunit.root is False
    assert x_planunit.all_voice_cred is None
    assert x_planunit.all_voice_debt is None
    assert x_planunit.healerunit_ratio == 0


def test_planunit_shop_Allows_starToBeZero():
    # ESTABLISH
    zero_int = 0
    # WHEN
    x_planunit = planunit_shop("run", star=zero_int)
    # THEN
    assert x_planunit.star == zero_int


def test_planunit_shop_Allows_doesNotAllow_starToBeNegative():
    # ESTABLISH
    negative_int = -4
    # WHEN
    x_planunit = planunit_shop("run", star=negative_int)
    # THEN
    zero_int = 0
    assert x_planunit.star == zero_int


def test_planunit_shop_NonNoneParametersReturnsObj():
    # ESTABLISH
    x_healerunit = healerunit_shop({"Sue", "Yao"})
    x_problem_bool = True
    x_fund_iota = 88

    # WHEN
    x_planunit = planunit_shop(
        healerunit=x_healerunit, problem_bool=x_problem_bool, fund_iota=x_fund_iota
    )

    # THEN
    assert x_planunit.healerunit == x_healerunit
    assert x_planunit.problem_bool == x_problem_bool
    assert x_planunit.fund_iota == x_fund_iota


def test_planunit_shop_ReturnsObjWith_awardunits():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    biker_give_force = 12
    biker_take_force = 15
    biker_awardunit = awardunit_shop("bikers2", biker_give_force, biker_take_force)
    swim_group_title = "swimmers"
    swim_give_force = 29
    swim_take_force = 32
    swim_awardunit = awardunit_shop(swim_group_title, swim_give_force, swim_take_force)
    x_awardunits = {
        swim_awardunit.awardee_title: swim_awardunit,
        biker_awardunit.awardee_title: biker_awardunit,
    }

    # WHEN
    sport_str = "sport"
    sport_plan = planunit_shop(plan_label=sport_str, awardunits=x_awardunits)

    # THEN
    assert sport_plan.awardunits == x_awardunits


def test_planunit_shop_ReturnsObjWithParameters():
    # ESTABLISH
    sport_gogo_want = 5
    sport_stop_want = 13

    # WHEN
    sport_str = "sport"
    sport_plan = planunit_shop(
        sport_str, gogo_want=sport_gogo_want, stop_want=sport_stop_want
    )

    # THEN
    assert sport_plan.gogo_want == sport_gogo_want
    assert sport_plan.stop_want == sport_stop_want


def test_PlanUnit_get_obj_key_ReturnsInfo():
    # ESTABLISH
    red_str = "red"

    # WHEN
    red_plan = planunit_shop(red_str)

    # THEN
    assert red_plan.get_obj_key() == red_str


def test_PlanUnit_set_knot_SetsAttr():
    # ESTABLISH
    casa_str = "casa"
    casa_plan = planunit_shop(casa_str)
    casa_plan.set_parent_rope("")

    # WHEN
    slash_str = "/"
    casa_plan.set_knot(slash_str)

    # THEN
    assert casa_plan.knot == slash_str


def test_PlanUnit_get_obj_key_ReturnsObj():
    # ESTABLISH
    round_str = "round_stuff"
    round_rope = create_rope(get_default_moment_label(), round_str)
    ball_str = "ball"

    # WHEN
    ball_plan = planunit_shop(plan_label=ball_str, parent_rope=round_rope)

    # THEN
    assert ball_plan.get_obj_key() == ball_str


def test_PlanUnit_get_rope_ReturnsObj():
    # ESTABLISH
    round_str = "round_stuff"
    slash_str = "/"
    round_rope = create_rope(get_default_moment_label(), round_str, knot=slash_str)
    ball_str = "ball"

    # WHEN
    ball_plan = planunit_shop(ball_str, parent_rope=round_rope, knot=slash_str)

    # THEN
    ball_rope = create_rope(round_rope, ball_str, knot=slash_str)
    assert ball_plan.get_plan_rope() == ball_rope


def test_PlanUnit_set_parent_rope_SetsAttr():
    # ESTABLISH
    round_str = "round_stuff"
    slash_str = "/"
    round_rope = create_rope(get_default_moment_label(), round_str, knot=slash_str)
    ball_str = "ball"
    ball_plan = planunit_shop(ball_str, parent_rope=round_rope, knot=slash_str)
    assert ball_plan.parent_rope == round_rope

    # WHEN
    sports_rope = create_rope(get_default_moment_label(), "sports", knot=slash_str)
    ball_plan.set_parent_rope(parent_rope=sports_rope)

    # THEN
    assert ball_plan.parent_rope == sports_rope


def test_PlanUnit_clear_descendant_task_count_ClearsAttrs():
    # ESTABLISH
    ball_str = "ball"
    ball_plan = planunit_shop(ball_str, descendant_task_count=55)
    assert ball_plan.descendant_task_count == 55

    # WHEN
    ball_plan.clear_descendant_task_count()

    # THEN
    assert ball_plan.descendant_task_count is None


def test_PlanUnit_add_to_descendant_task_count_AddsToCount():
    # ESTABLISH
    ball_str = "ball"
    ball_plan = planunit_shop(ball_str, descendant_task_count=55)
    ball_plan.clear_descendant_task_count()
    assert not ball_plan.descendant_task_count

    # WHEN
    ball_plan.add_to_descendant_task_count(44)

    # THEN
    assert ball_plan.descendant_task_count == 44

    # WHEN
    ball_plan.add_to_descendant_task_count(33)

    # THEN
    assert ball_plan.descendant_task_count == 77


def test_PlanUnit_is_math_ReturnsObj():
    # ESTABLISH
    swim_str = "swim"
    swim_plan = planunit_shop(swim_str)
    assert not swim_plan.is_math()
    # WHEN
    swim_plan.begin = 9
    # THEN
    assert not swim_plan.is_math()
    # WHEN
    swim_plan.close = 10
    # THEN
    assert swim_plan.is_math()
    # WHEN
    swim_plan.begin = None
    # THEN
    assert not swim_plan.is_math()


def test_PlanUnit_clear_gogo_calc_stop_calc_SetsAttr():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_plan = planunit_shop(num_range_str)
    num_range_plan.range_evaluated = True
    num_range_plan.gogo_calc = 3
    num_range_plan.stop_calc = 4
    assert num_range_plan.range_evaluated
    assert num_range_plan.gogo_calc
    assert num_range_plan.stop_calc

    # WHEN
    num_range_plan.clear_gogo_calc_stop_calc()

    # THEN
    assert not num_range_plan.range_evaluated
    assert not num_range_plan.gogo_calc
    assert not num_range_plan.stop_calc


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_denom():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom)
    init_gogo_calc = 21
    init_stop_calc = 42
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert not num_range_plan.range_evaluated
    assert num_range_plan.gogo_calc
    assert num_range_plan.stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.range_evaluated
    assert num_range_plan.gogo_calc == init_gogo_calc / num_range_denom
    assert num_range_plan.stop_calc == init_stop_calc / num_range_denom
    assert num_range_plan.gogo_calc == 3
    assert num_range_plan.stop_calc == 6


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_FullRangeCovered():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 45
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc
    assert num_range_plan.stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == 0
    assert num_range_plan.stop_calc == num_range_denom
    assert num_range_plan.gogo_calc == 0
    assert num_range_plan.stop_calc == 7


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_PartialRangeCovered():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 24
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc
    assert num_range_plan.stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == 0
    assert (
        num_range_plan.stop_calc == (init_stop_calc - init_gogo_calc) % num_range_denom
    )
    assert num_range_plan.gogo_calc == 0
    assert num_range_plan.stop_calc == 3


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario1_PartialRangeCovered():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 25
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc
    assert num_range_plan.stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == init_gogo_calc % num_range_denom
    assert num_range_plan.stop_calc == init_stop_calc % num_range_denom
    assert num_range_plan.gogo_calc == 1
    assert num_range_plan.stop_calc == 4


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario0_NoModifications():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 40
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == gogo_want
    assert num_range_plan.stop_calc == stop_want
    assert num_range_plan.gogo_calc == 30
    assert num_range_plan.stop_calc == 40


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifiyBoth():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 50
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc
    assert num_range_plan.gogo_calc == 21
    assert num_range_plan.stop_calc == 45


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifyLeft():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 40
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == stop_want
    assert num_range_plan.gogo_calc == 21
    assert num_range_plan.stop_calc == 40


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario2_ModifyRight():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 50
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert num_range_plan.gogo_calc == gogo_want
    assert num_range_plan.stop_calc == init_stop_calc
    assert num_range_plan.gogo_calc == 30
    assert num_range_plan.stop_calc == 45


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsLeft():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 15
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert not num_range_plan.gogo_calc
    assert not num_range_plan.stop_calc


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsRight():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 60
    stop_want = 65
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert not num_range_plan.gogo_calc
    assert not num_range_plan.stop_calc


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario4_None():
    # ESTABLISH
    num_range_str = "num_range"
    num_range_denom = 7
    num_range_plan = planunit_shop(num_range_str, denom=num_range_denom, morph=True)
    init_gogo_calc = None
    init_stop_calc = None
    gogo_want = 21
    stop_want = 45
    num_range_plan.gogo_want = gogo_want
    num_range_plan.stop_want = stop_want
    num_range_plan.gogo_calc = init_gogo_calc
    num_range_plan.stop_calc = init_stop_calc
    num_range_plan.denom = num_range_denom
    assert num_range_plan.gogo_calc == init_gogo_calc
    assert num_range_plan.stop_calc == init_stop_calc

    # WHEN
    num_range_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert not num_range_plan.gogo_calc
    assert not num_range_plan.stop_calc
