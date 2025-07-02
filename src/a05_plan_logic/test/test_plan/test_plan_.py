from src.a01_term_logic.rope import create_rope, default_knot_if_None
from src.a01_term_logic.test._util.a01_str import knot_str, parent_rope_str
from src.a02_finance_logic.finance_config import default_fund_iota_if_None
from src.a02_finance_logic.test._util.a02_str import fund_iota_str
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a04_reason_logic.test._util.a04_str import _chore_str
from src.a05_plan_logic.healer import healerlink_shop
from src.a05_plan_logic.plan import PlanUnit, get_default_belief_label, planunit_shop
from src.a05_plan_logic.test._util.a05_str import (
    _active_hx_str,
    _active_str,
    _all_acct_cred_str,
    _all_acct_debt_str,
    _awardheirs_str,
    _awardlines_str,
    _descendant_task_count_str,
    _factheirs_str,
    _fund_cease_str,
    _fund_onset_str,
    _fund_ratio_str,
    _gogo_calc_str,
    _healerlink_ratio_str,
    _is_expanded_str,
    _kids_str,
    _range_evaluated_str,
    _reasonheirs_str,
    _stop_calc_str,
    _uid_str,
    addin_str,
    begin_str,
    belief_label_str,
    close_str,
    denom_str,
    fund_iota_str,
    gogo_want_str,
    healerlink_str,
    knot_str,
    mass_str,
    morph_str,
    numor_str,
    plan_label_str,
    problem_bool_str,
    stop_want_str,
    task_str,
)


def test_get_default_belief_label_ReturnsObj():
    assert get_default_belief_label() == "ZZ"


def test_PlanUnit_Exists():
    x_planunit = PlanUnit()
    assert x_planunit
    assert x_planunit._kids is None
    assert x_planunit.mass is None
    assert x_planunit.plan_label is None
    assert x_planunit._uid is None
    assert x_planunit.reasonunits is None
    assert x_planunit._reasonheirs is None  # calculated field
    assert x_planunit.laborunit is None
    assert x_planunit._laborheir is None  # calculated field
    assert x_planunit.factunits is None
    assert x_planunit._factheirs is None  # calculated field
    assert x_planunit.awardlinks is None
    assert x_planunit._awardlines is None  # calculated field'
    assert x_planunit._awardheirs is None  # calculated field'
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
    assert x_planunit.healerlink is None
    # calculated_fields
    assert x_planunit._range_evaluated is None
    assert x_planunit._gogo_calc is None
    assert x_planunit._stop_calc is None
    assert x_planunit._descendant_task_count is None
    assert x_planunit._is_expanded is None
    assert x_planunit._all_acct_cred is None
    assert x_planunit._all_acct_debt is None
    assert x_planunit._level is None
    assert x_planunit._active_hx is None
    assert x_planunit._fund_ratio is None
    assert x_planunit.fund_iota is None
    assert x_planunit._fund_onset is None
    assert x_planunit._fund_cease is None
    assert x_planunit.root is None
    assert x_planunit.belief_label is None
    assert x_planunit._healerlink_ratio is None
    obj_attrs = set(x_planunit.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        _active_str(),
        _active_hx_str(),
        _all_acct_cred_str(),
        _all_acct_debt_str(),
        _awardheirs_str(),
        _awardlines_str(),
        _descendant_task_count_str(),
        _factheirs_str(),
        _fund_cease_str(),
        _fund_onset_str(),
        _fund_ratio_str(),
        _gogo_calc_str(),
        _healerlink_ratio_str(),
        _is_expanded_str(),
        _kids_str(),
        "_laborheir",
        "_level",
        _range_evaluated_str(),
        _reasonheirs_str(),
        _stop_calc_str(),
        _chore_str(),
        _uid_str(),
        addin_str(),
        "awardlinks",
        begin_str(),
        knot_str(),
        close_str(),
        plan_label_str(),
        denom_str(),
        "factunits",
        belief_label_str(),
        fund_iota_str(),
        gogo_want_str(),
        healerlink_str(),
        "laborunit",
        mass_str(),
        morph_str(),
        numor_str(),
        parent_rope_str(),
        task_str(),
        problem_bool_str(),
        "reasonunits",
        "root",
        stop_want_str(),
    }


def test_planunit_shop_WithNoParametersReturnsObj():
    # ESTABLISH / WHEN
    x_planunit = planunit_shop()

    # THEN
    assert x_planunit
    assert x_planunit._kids == {}
    assert x_planunit.mass == 1
    assert x_planunit.plan_label is None
    assert x_planunit.belief_label == get_default_belief_label()
    assert x_planunit._uid is None
    assert x_planunit.begin is None
    assert x_planunit.close is None
    assert x_planunit.addin is None
    assert x_planunit.numor is None
    assert x_planunit.denom is None
    assert x_planunit.morph is None
    assert x_planunit.task is False
    assert x_planunit.problem_bool is False
    assert x_planunit._descendant_task_count is None
    assert x_planunit._awardlines == {}
    assert x_planunit.awardlinks == {}
    assert x_planunit._awardheirs == {}
    assert x_planunit._is_expanded is True
    assert x_planunit._factheirs == {}
    assert x_planunit.factunits == {}
    assert x_planunit.healerlink == healerlink_shop()
    assert x_planunit._gogo_calc is None
    assert x_planunit._stop_calc is None
    assert x_planunit._level is None
    assert x_planunit._active_hx == {}
    assert x_planunit._fund_ratio is None
    assert x_planunit.fund_iota == default_fund_iota_if_None()
    assert x_planunit._fund_onset is None
    assert x_planunit._fund_cease is None
    assert x_planunit.reasonunits == {}
    assert x_planunit._reasonheirs == {}
    assert x_planunit.laborunit == laborunit_shop()
    assert x_planunit._laborheir is None
    assert x_planunit.knot == default_knot_if_None()
    assert x_planunit.root is False
    assert x_planunit._all_acct_cred is None
    assert x_planunit._all_acct_debt is None
    assert x_planunit._healerlink_ratio == 0


def test_planunit_shop_Allows_massToBeZero():
    # ESTABLISH
    zero_int = 0
    # WHEN
    x_planunit = planunit_shop("run", mass=zero_int)
    # THEN
    assert x_planunit.mass == zero_int


def test_planunit_shop_Allows_doesNotAllow_massToBeNegative():
    # ESTABLISH
    negative_int = -4
    # WHEN
    x_planunit = planunit_shop("run", mass=negative_int)
    # THEN
    zero_int = 0
    assert x_planunit.mass == zero_int


def test_planunit_shop_NonNoneParametersReturnsObj():
    # ESTABLISH
    x_healerlink = healerlink_shop({"Sue", "Yao"})
    x_problem_bool = True
    x_fund_iota = 88

    # WHEN
    x_planunit = planunit_shop(
        healerlink=x_healerlink, problem_bool=x_problem_bool, fund_iota=x_fund_iota
    )

    # THEN
    assert x_planunit.healerlink == x_healerlink
    assert x_planunit.problem_bool == x_problem_bool
    assert x_planunit.fund_iota == x_fund_iota


def test_planunit_shop_ReturnsObjWith_awardlinks():
    # ESTABLISH
    biker_give_force = 12
    biker_take_force = 15
    biker_awardlink = awardlink_shop("bikers2", biker_give_force, biker_take_force)
    swim_group_title = "swimmers"
    swim_give_force = 29
    swim_take_force = 32
    swim_awardlink = awardlink_shop(swim_group_title, swim_give_force, swim_take_force)
    x_awardlinks = {
        swim_awardlink.awardee_title: swim_awardlink,
        biker_awardlink.awardee_title: biker_awardlink,
    }

    # WHEN
    sport_str = "sport"
    sport_plan = planunit_shop(plan_label=sport_str, awardlinks=x_awardlinks)

    # THEN
    assert sport_plan.awardlinks == x_awardlinks


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


def test_PlanUnit_get_obj_key_ReturnsObj():
    # ESTABLISH
    round_str = "round_stuff"
    round_rope = create_rope(get_default_belief_label(), round_str)
    ball_str = "ball"

    # WHEN
    ball_plan = planunit_shop(plan_label=ball_str, parent_rope=round_rope)

    # THEN
    assert ball_plan.get_obj_key() == ball_str


def test_PlanUnit_get_rope_ReturnsObj():
    # ESTABLISH
    round_str = "round_stuff"
    slash_str = "/"
    round_rope = create_rope(get_default_belief_label(), round_str, knot=slash_str)
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
    round_rope = create_rope(get_default_belief_label(), round_str, knot=slash_str)
    ball_str = "ball"
    ball_plan = planunit_shop(ball_str, parent_rope=round_rope, knot=slash_str)
    assert ball_plan.parent_rope == round_rope

    # WHEN
    sports_rope = create_rope(get_default_belief_label(), "sports", knot=slash_str)
    ball_plan.set_parent_rope(parent_rope=sports_rope)

    # THEN
    assert ball_plan.parent_rope == sports_rope


def test_PlanUnit_clear_descendant_task_count_ClearsCorrectly():
    # ESTABLISH
    ball_str = "ball"
    ball_plan = planunit_shop(ball_str, _descendant_task_count=55)
    assert ball_plan._descendant_task_count == 55

    # WHEN
    ball_plan.clear_descendant_task_count()

    # THEN
    assert ball_plan._descendant_task_count is None


def test_PlanUnit_add_to_descendant_task_count_CorrectlyAdds():
    # ESTABLISH
    ball_str = "ball"
    ball_plan = planunit_shop(ball_str, _descendant_task_count=55)
    ball_plan.clear_descendant_task_count()
    assert ball_plan._descendant_task_count is None

    # WHEN
    ball_plan.add_to_descendant_task_count(44)

    # THEN
    assert ball_plan._descendant_task_count == 44

    # WHEN
    ball_plan.add_to_descendant_task_count(33)

    # THEN
    assert ball_plan._descendant_task_count == 77


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
    time_str = "time"
    time_plan = planunit_shop(time_str)
    time_plan._range_evaluated = True
    time_plan._gogo_calc = 3
    time_plan._stop_calc = 4
    assert time_plan._range_evaluated
    assert time_plan._gogo_calc
    assert time_plan._stop_calc

    # WHEN
    time_plan.clear_gogo_calc_stop_calc()

    # THEN
    assert not time_plan._range_evaluated
    assert not time_plan._gogo_calc
    assert not time_plan._stop_calc


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_denom():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_plan = planunit_shop(time_str, denom=time_denom)
    init_gogo_calc = 21
    init_stop_calc = 42
    time_plan._gogo_calc = init_gogo_calc
    time_plan._stop_calc = init_stop_calc
    time_plan.denom = time_denom
    assert not time_plan._range_evaluated
    assert time_plan._gogo_calc
    assert time_plan._stop_calc

    # WHEN
    time_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert time_plan._range_evaluated
    assert time_plan._gogo_calc == init_gogo_calc / time_denom
    assert time_plan._stop_calc == init_stop_calc / time_denom
    assert time_plan._gogo_calc == 3
    assert time_plan._stop_calc == 6


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_FullRangeCovered():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_plan = planunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 45
    time_plan._gogo_calc = init_gogo_calc
    time_plan._stop_calc = init_stop_calc
    time_plan.denom = time_denom
    assert time_plan._gogo_calc
    assert time_plan._stop_calc

    # WHEN
    time_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert time_plan._gogo_calc == 0
    assert time_plan._stop_calc == time_denom
    assert time_plan._gogo_calc == 0
    assert time_plan._stop_calc == 7


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_PartialRangeCovered():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_plan = planunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 24
    time_plan._gogo_calc = init_gogo_calc
    time_plan._stop_calc = init_stop_calc
    time_plan.denom = time_denom
    assert time_plan._gogo_calc
    assert time_plan._stop_calc

    # WHEN
    time_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert time_plan._gogo_calc == 0
    assert time_plan._stop_calc == (init_stop_calc - init_gogo_calc) % time_denom
    assert time_plan._gogo_calc == 0
    assert time_plan._stop_calc == 3


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario1_PartialRangeCovered():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_plan = planunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 25
    time_plan._gogo_calc = init_gogo_calc
    time_plan._stop_calc = init_stop_calc
    time_plan.denom = time_denom
    assert time_plan._gogo_calc
    assert time_plan._stop_calc

    # WHEN
    time_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert time_plan._gogo_calc == init_gogo_calc % time_denom
    assert time_plan._stop_calc == init_stop_calc % time_denom
    assert time_plan._gogo_calc == 1
    assert time_plan._stop_calc == 4


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario0_NoModifications():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_plan = planunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 40
    time_plan.gogo_want = gogo_want
    time_plan.stop_want = stop_want
    time_plan._gogo_calc = init_gogo_calc
    time_plan._stop_calc = init_stop_calc
    time_plan.denom = time_denom
    assert time_plan._gogo_calc == init_gogo_calc
    assert time_plan._stop_calc == init_stop_calc

    # WHEN
    time_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert time_plan._gogo_calc == gogo_want
    assert time_plan._stop_calc == stop_want
    assert time_plan._gogo_calc == 30
    assert time_plan._stop_calc == 40


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifiyBoth():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_plan = planunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 50
    time_plan.gogo_want = gogo_want
    time_plan.stop_want = stop_want
    time_plan._gogo_calc = init_gogo_calc
    time_plan._stop_calc = init_stop_calc
    time_plan.denom = time_denom
    assert time_plan._gogo_calc == init_gogo_calc
    assert time_plan._stop_calc == init_stop_calc

    # WHEN
    time_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert time_plan._gogo_calc == init_gogo_calc
    assert time_plan._stop_calc == init_stop_calc
    assert time_plan._gogo_calc == 21
    assert time_plan._stop_calc == 45


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifyLeft():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_plan = planunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 40
    time_plan.gogo_want = gogo_want
    time_plan.stop_want = stop_want
    time_plan._gogo_calc = init_gogo_calc
    time_plan._stop_calc = init_stop_calc
    time_plan.denom = time_denom
    assert time_plan._gogo_calc == init_gogo_calc
    assert time_plan._stop_calc == init_stop_calc

    # WHEN
    time_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert time_plan._gogo_calc == init_gogo_calc
    assert time_plan._stop_calc == stop_want
    assert time_plan._gogo_calc == 21
    assert time_plan._stop_calc == 40


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario2_ModifyRight():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_plan = planunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 50
    time_plan.gogo_want = gogo_want
    time_plan.stop_want = stop_want
    time_plan._gogo_calc = init_gogo_calc
    time_plan._stop_calc = init_stop_calc
    time_plan.denom = time_denom
    assert time_plan._gogo_calc == init_gogo_calc
    assert time_plan._stop_calc == init_stop_calc

    # WHEN
    time_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert time_plan._gogo_calc == gogo_want
    assert time_plan._stop_calc == init_stop_calc
    assert time_plan._gogo_calc == 30
    assert time_plan._stop_calc == 45


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsLeft():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_plan = planunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 15
    time_plan.gogo_want = gogo_want
    time_plan.stop_want = stop_want
    time_plan._gogo_calc = init_gogo_calc
    time_plan._stop_calc = init_stop_calc
    time_plan.denom = time_denom
    assert time_plan._gogo_calc == init_gogo_calc
    assert time_plan._stop_calc == init_stop_calc

    # WHEN
    time_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert not time_plan._gogo_calc
    assert not time_plan._stop_calc


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsRight():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_plan = planunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 60
    stop_want = 65
    time_plan.gogo_want = gogo_want
    time_plan.stop_want = stop_want
    time_plan._gogo_calc = init_gogo_calc
    time_plan._stop_calc = init_stop_calc
    time_plan.denom = time_denom
    assert time_plan._gogo_calc == init_gogo_calc
    assert time_plan._stop_calc == init_stop_calc

    # WHEN
    time_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert not time_plan._gogo_calc
    assert not time_plan._stop_calc


def test_PlanUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario4_None():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_plan = planunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = None
    init_stop_calc = None
    gogo_want = 21
    stop_want = 45
    time_plan.gogo_want = gogo_want
    time_plan.stop_want = stop_want
    time_plan._gogo_calc = init_gogo_calc
    time_plan._stop_calc = init_stop_calc
    time_plan.denom = time_denom
    assert time_plan._gogo_calc == init_gogo_calc
    assert time_plan._stop_calc == init_stop_calc

    # WHEN
    time_plan._mold_gogo_calc_stop_calc()

    # THEN
    assert not time_plan._gogo_calc
    assert not time_plan._stop_calc
