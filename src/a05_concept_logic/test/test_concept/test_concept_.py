from src.a01_term_logic.rope import create_rope, default_knot_if_None
from src.a01_term_logic.test._util.a01_str import knot_str, parent_rope_str
from src.a02_finance_logic.finance_config import default_fund_iota_if_None
from src.a02_finance_logic.test._util.a02_str import fund_iota_str
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a04_reason_logic.test._util.a04_str import _chore_str
from src.a05_concept_logic.concept import (
    ConceptUnit,
    conceptunit_shop,
    get_default_belief_label,
)
from src.a05_concept_logic.healer import healerlink_shop
from src.a05_concept_logic.test._util.a05_str import (
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
    concept_label_str,
    denom_str,
    fund_iota_str,
    gogo_want_str,
    healerlink_str,
    knot_str,
    mass_str,
    morph_str,
    numor_str,
    problem_bool_str,
    stop_want_str,
    task_str,
)


def test_get_default_belief_label_ReturnsObj():
    assert get_default_belief_label() == "ZZ"


def test_ConceptUnit_Exists():
    x_conceptunit = ConceptUnit()
    assert x_conceptunit
    assert x_conceptunit._kids is None
    assert x_conceptunit.mass is None
    assert x_conceptunit.concept_label is None
    assert x_conceptunit._uid is None
    assert x_conceptunit.reasonunits is None
    assert x_conceptunit._reasonheirs is None  # calculated field
    assert x_conceptunit.laborunit is None
    assert x_conceptunit._laborheir is None  # calculated field
    assert x_conceptunit.factunits is None
    assert x_conceptunit._factheirs is None  # calculated field
    assert x_conceptunit.awardlinks is None
    assert x_conceptunit._awardlines is None  # calculated field'
    assert x_conceptunit._awardheirs is None  # calculated field'
    assert x_conceptunit.knot is None
    assert x_conceptunit.begin is None
    assert x_conceptunit.close is None
    assert x_conceptunit.addin is None
    assert x_conceptunit.numor is None
    assert x_conceptunit.denom is None
    assert x_conceptunit.morph is None
    assert x_conceptunit.gogo_want is None
    assert x_conceptunit.stop_want is None
    assert x_conceptunit.task is None
    assert x_conceptunit.problem_bool is None
    assert x_conceptunit.healerlink is None
    # calculated_fields
    assert x_conceptunit._range_evaluated is None
    assert x_conceptunit._gogo_calc is None
    assert x_conceptunit._stop_calc is None
    assert x_conceptunit._descendant_task_count is None
    assert x_conceptunit._is_expanded is None
    assert x_conceptunit._all_acct_cred is None
    assert x_conceptunit._all_acct_debt is None
    assert x_conceptunit._level is None
    assert x_conceptunit._active_hx is None
    assert x_conceptunit._fund_ratio is None
    assert x_conceptunit.fund_iota is None
    assert x_conceptunit._fund_onset is None
    assert x_conceptunit._fund_cease is None
    assert x_conceptunit.root is None
    assert x_conceptunit.belief_label is None
    assert x_conceptunit._healerlink_ratio is None
    obj_attrs = set(x_conceptunit.__dict__.keys())
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
        concept_label_str(),
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


def test_conceptunit_shop_WithNoParametersReturnsObj():
    # ESTABLISH / WHEN
    x_conceptunit = conceptunit_shop()

    # THEN
    assert x_conceptunit
    assert x_conceptunit._kids == {}
    assert x_conceptunit.mass == 1
    assert x_conceptunit.concept_label is None
    assert x_conceptunit.belief_label == get_default_belief_label()
    assert x_conceptunit._uid is None
    assert x_conceptunit.begin is None
    assert x_conceptunit.close is None
    assert x_conceptunit.addin is None
    assert x_conceptunit.numor is None
    assert x_conceptunit.denom is None
    assert x_conceptunit.morph is None
    assert x_conceptunit.task is False
    assert x_conceptunit.problem_bool is False
    assert x_conceptunit._descendant_task_count is None
    assert x_conceptunit._awardlines == {}
    assert x_conceptunit.awardlinks == {}
    assert x_conceptunit._awardheirs == {}
    assert x_conceptunit._is_expanded is True
    assert x_conceptunit._factheirs == {}
    assert x_conceptunit.factunits == {}
    assert x_conceptunit.healerlink == healerlink_shop()
    assert x_conceptunit._gogo_calc is None
    assert x_conceptunit._stop_calc is None
    assert x_conceptunit._level is None
    assert x_conceptunit._active_hx == {}
    assert x_conceptunit._fund_ratio is None
    assert x_conceptunit.fund_iota == default_fund_iota_if_None()
    assert x_conceptunit._fund_onset is None
    assert x_conceptunit._fund_cease is None
    assert x_conceptunit.reasonunits == {}
    assert x_conceptunit._reasonheirs == {}
    assert x_conceptunit.laborunit == laborunit_shop()
    assert x_conceptunit._laborheir is None
    assert x_conceptunit.knot == default_knot_if_None()
    assert x_conceptunit.root is False
    assert x_conceptunit._all_acct_cred is None
    assert x_conceptunit._all_acct_debt is None
    assert x_conceptunit._healerlink_ratio == 0


def test_conceptunit_shop_Allows_massToBeZero():
    # ESTABLISH
    zero_int = 0
    # WHEN
    x_conceptunit = conceptunit_shop("run", mass=zero_int)
    # THEN
    assert x_conceptunit.mass == zero_int


def test_conceptunit_shop_Allows_doesNotAllow_massToBeNegative():
    # ESTABLISH
    negative_int = -4
    # WHEN
    x_conceptunit = conceptunit_shop("run", mass=negative_int)
    # THEN
    zero_int = 0
    assert x_conceptunit.mass == zero_int


def test_conceptunit_shop_NonNoneParametersReturnsObj():
    # ESTABLISH
    x_healerlink = healerlink_shop({"Sue", "Yao"})
    x_problem_bool = True
    x_fund_iota = 88

    # WHEN
    x_conceptunit = conceptunit_shop(
        healerlink=x_healerlink, problem_bool=x_problem_bool, fund_iota=x_fund_iota
    )

    # THEN
    assert x_conceptunit.healerlink == x_healerlink
    assert x_conceptunit.problem_bool == x_problem_bool
    assert x_conceptunit.fund_iota == x_fund_iota


def test_conceptunit_shop_ReturnsObjWith_awardlinks():
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
    sport_concept = conceptunit_shop(concept_label=sport_str, awardlinks=x_awardlinks)

    # THEN
    assert sport_concept.awardlinks == x_awardlinks


def test_conceptunit_shop_ReturnsObjWithParameters():
    # ESTABLISH
    sport_gogo_want = 5
    sport_stop_want = 13

    # WHEN
    sport_str = "sport"
    sport_concept = conceptunit_shop(
        sport_str, gogo_want=sport_gogo_want, stop_want=sport_stop_want
    )

    # THEN
    assert sport_concept.gogo_want == sport_gogo_want
    assert sport_concept.stop_want == sport_stop_want


def test_ConceptUnit_get_obj_key_ReturnsObj():
    # ESTABLISH
    round_str = "round_stuff"
    round_rope = create_rope(get_default_belief_label(), round_str)
    ball_str = "ball"

    # WHEN
    ball_concept = conceptunit_shop(concept_label=ball_str, parent_rope=round_rope)

    # THEN
    assert ball_concept.get_obj_key() == ball_str


def test_ConceptUnit_get_rope_ReturnsObj():
    # ESTABLISH
    round_str = "round_stuff"
    slash_str = "/"
    round_rope = create_rope(get_default_belief_label(), round_str, knot=slash_str)
    ball_str = "ball"

    # WHEN
    ball_concept = conceptunit_shop(ball_str, parent_rope=round_rope, knot=slash_str)

    # THEN
    ball_rope = create_rope(round_rope, ball_str, knot=slash_str)
    assert ball_concept.get_concept_rope() == ball_rope


def test_ConceptUnit_set_parent_rope_SetsAttr():
    # ESTABLISH
    round_str = "round_stuff"
    slash_str = "/"
    round_rope = create_rope(get_default_belief_label(), round_str, knot=slash_str)
    ball_str = "ball"
    ball_concept = conceptunit_shop(ball_str, parent_rope=round_rope, knot=slash_str)
    assert ball_concept.parent_rope == round_rope

    # WHEN
    sports_rope = create_rope(get_default_belief_label(), "sports", knot=slash_str)
    ball_concept.set_parent_rope(parent_rope=sports_rope)

    # THEN
    assert ball_concept.parent_rope == sports_rope


def test_ConceptUnit_clear_descendant_task_count_ClearsCorrectly():
    # ESTABLISH
    ball_str = "ball"
    ball_concept = conceptunit_shop(ball_str, _descendant_task_count=55)
    assert ball_concept._descendant_task_count == 55

    # WHEN
    ball_concept.clear_descendant_task_count()

    # THEN
    assert ball_concept._descendant_task_count is None


def test_ConceptUnit_add_to_descendant_task_count_CorrectlyAdds():
    # ESTABLISH
    ball_str = "ball"
    ball_concept = conceptunit_shop(ball_str, _descendant_task_count=55)
    ball_concept.clear_descendant_task_count()
    assert ball_concept._descendant_task_count is None

    # WHEN
    ball_concept.add_to_descendant_task_count(44)

    # THEN
    assert ball_concept._descendant_task_count == 44

    # WHEN
    ball_concept.add_to_descendant_task_count(33)

    # THEN
    assert ball_concept._descendant_task_count == 77


def test_ConceptUnit_is_math_ReturnsObj():
    # ESTABLISH
    swim_str = "swim"
    swim_concept = conceptunit_shop(swim_str)
    assert not swim_concept.is_math()
    # WHEN
    swim_concept.begin = 9
    # THEN
    assert not swim_concept.is_math()
    # WHEN
    swim_concept.close = 10
    # THEN
    assert swim_concept.is_math()
    # WHEN
    swim_concept.begin = None
    # THEN
    assert not swim_concept.is_math()


def test_ConceptUnit_clear_gogo_calc_stop_calc_SetsAttr():
    # ESTABLISH
    time_str = "time"
    time_concept = conceptunit_shop(time_str)
    time_concept._range_evaluated = True
    time_concept._gogo_calc = 3
    time_concept._stop_calc = 4
    assert time_concept._range_evaluated
    assert time_concept._gogo_calc
    assert time_concept._stop_calc

    # WHEN
    time_concept.clear_gogo_calc_stop_calc()

    # THEN
    assert not time_concept._range_evaluated
    assert not time_concept._gogo_calc
    assert not time_concept._stop_calc


def test_ConceptUnit_mold_gogo_calc_stop_calc_SetsAttr_denom():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_concept = conceptunit_shop(time_str, denom=time_denom)
    init_gogo_calc = 21
    init_stop_calc = 42
    time_concept._gogo_calc = init_gogo_calc
    time_concept._stop_calc = init_stop_calc
    time_concept.denom = time_denom
    assert not time_concept._range_evaluated
    assert time_concept._gogo_calc
    assert time_concept._stop_calc

    # WHEN
    time_concept._mold_gogo_calc_stop_calc()

    # THEN
    assert time_concept._range_evaluated
    assert time_concept._gogo_calc == init_gogo_calc / time_denom
    assert time_concept._stop_calc == init_stop_calc / time_denom
    assert time_concept._gogo_calc == 3
    assert time_concept._stop_calc == 6


def test_ConceptUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_FullRangeCovered():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_concept = conceptunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 45
    time_concept._gogo_calc = init_gogo_calc
    time_concept._stop_calc = init_stop_calc
    time_concept.denom = time_denom
    assert time_concept._gogo_calc
    assert time_concept._stop_calc

    # WHEN
    time_concept._mold_gogo_calc_stop_calc()

    # THEN
    assert time_concept._gogo_calc == 0
    assert time_concept._stop_calc == time_denom
    assert time_concept._gogo_calc == 0
    assert time_concept._stop_calc == 7


def test_ConceptUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_PartialRangeCovered():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_concept = conceptunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 24
    time_concept._gogo_calc = init_gogo_calc
    time_concept._stop_calc = init_stop_calc
    time_concept.denom = time_denom
    assert time_concept._gogo_calc
    assert time_concept._stop_calc

    # WHEN
    time_concept._mold_gogo_calc_stop_calc()

    # THEN
    assert time_concept._gogo_calc == 0
    assert time_concept._stop_calc == (init_stop_calc - init_gogo_calc) % time_denom
    assert time_concept._gogo_calc == 0
    assert time_concept._stop_calc == 3


def test_ConceptUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario1_PartialRangeCovered():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_concept = conceptunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 25
    time_concept._gogo_calc = init_gogo_calc
    time_concept._stop_calc = init_stop_calc
    time_concept.denom = time_denom
    assert time_concept._gogo_calc
    assert time_concept._stop_calc

    # WHEN
    time_concept._mold_gogo_calc_stop_calc()

    # THEN
    assert time_concept._gogo_calc == init_gogo_calc % time_denom
    assert time_concept._stop_calc == init_stop_calc % time_denom
    assert time_concept._gogo_calc == 1
    assert time_concept._stop_calc == 4


def test_ConceptUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario0_NoModifications():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_concept = conceptunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 40
    time_concept.gogo_want = gogo_want
    time_concept.stop_want = stop_want
    time_concept._gogo_calc = init_gogo_calc
    time_concept._stop_calc = init_stop_calc
    time_concept.denom = time_denom
    assert time_concept._gogo_calc == init_gogo_calc
    assert time_concept._stop_calc == init_stop_calc

    # WHEN
    time_concept._mold_gogo_calc_stop_calc()

    # THEN
    assert time_concept._gogo_calc == gogo_want
    assert time_concept._stop_calc == stop_want
    assert time_concept._gogo_calc == 30
    assert time_concept._stop_calc == 40


def test_ConceptUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifiyBoth():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_concept = conceptunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 50
    time_concept.gogo_want = gogo_want
    time_concept.stop_want = stop_want
    time_concept._gogo_calc = init_gogo_calc
    time_concept._stop_calc = init_stop_calc
    time_concept.denom = time_denom
    assert time_concept._gogo_calc == init_gogo_calc
    assert time_concept._stop_calc == init_stop_calc

    # WHEN
    time_concept._mold_gogo_calc_stop_calc()

    # THEN
    assert time_concept._gogo_calc == init_gogo_calc
    assert time_concept._stop_calc == init_stop_calc
    assert time_concept._gogo_calc == 21
    assert time_concept._stop_calc == 45


def test_ConceptUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifyLeft():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_concept = conceptunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 40
    time_concept.gogo_want = gogo_want
    time_concept.stop_want = stop_want
    time_concept._gogo_calc = init_gogo_calc
    time_concept._stop_calc = init_stop_calc
    time_concept.denom = time_denom
    assert time_concept._gogo_calc == init_gogo_calc
    assert time_concept._stop_calc == init_stop_calc

    # WHEN
    time_concept._mold_gogo_calc_stop_calc()

    # THEN
    assert time_concept._gogo_calc == init_gogo_calc
    assert time_concept._stop_calc == stop_want
    assert time_concept._gogo_calc == 21
    assert time_concept._stop_calc == 40


def test_ConceptUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario2_ModifyRight():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_concept = conceptunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 50
    time_concept.gogo_want = gogo_want
    time_concept.stop_want = stop_want
    time_concept._gogo_calc = init_gogo_calc
    time_concept._stop_calc = init_stop_calc
    time_concept.denom = time_denom
    assert time_concept._gogo_calc == init_gogo_calc
    assert time_concept._stop_calc == init_stop_calc

    # WHEN
    time_concept._mold_gogo_calc_stop_calc()

    # THEN
    assert time_concept._gogo_calc == gogo_want
    assert time_concept._stop_calc == init_stop_calc
    assert time_concept._gogo_calc == 30
    assert time_concept._stop_calc == 45


def test_ConceptUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsLeft():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_concept = conceptunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 15
    time_concept.gogo_want = gogo_want
    time_concept.stop_want = stop_want
    time_concept._gogo_calc = init_gogo_calc
    time_concept._stop_calc = init_stop_calc
    time_concept.denom = time_denom
    assert time_concept._gogo_calc == init_gogo_calc
    assert time_concept._stop_calc == init_stop_calc

    # WHEN
    time_concept._mold_gogo_calc_stop_calc()

    # THEN
    assert not time_concept._gogo_calc
    assert not time_concept._stop_calc


def test_ConceptUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsRight():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_concept = conceptunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 60
    stop_want = 65
    time_concept.gogo_want = gogo_want
    time_concept.stop_want = stop_want
    time_concept._gogo_calc = init_gogo_calc
    time_concept._stop_calc = init_stop_calc
    time_concept.denom = time_denom
    assert time_concept._gogo_calc == init_gogo_calc
    assert time_concept._stop_calc == init_stop_calc

    # WHEN
    time_concept._mold_gogo_calc_stop_calc()

    # THEN
    assert not time_concept._gogo_calc
    assert not time_concept._stop_calc


def test_ConceptUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario4_None():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_concept = conceptunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = None
    init_stop_calc = None
    gogo_want = 21
    stop_want = 45
    time_concept.gogo_want = gogo_want
    time_concept.stop_want = stop_want
    time_concept._gogo_calc = init_gogo_calc
    time_concept._stop_calc = init_stop_calc
    time_concept.denom = time_denom
    assert time_concept._gogo_calc == init_gogo_calc
    assert time_concept._stop_calc == init_stop_calc

    # WHEN
    time_concept._mold_gogo_calc_stop_calc()

    # THEN
    assert not time_concept._gogo_calc
    assert not time_concept._stop_calc
