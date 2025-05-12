from src.a02_finance_logic.finance_config import default_fund_coin_if_None
from src.a01_way_logic.way import (
    get_default_fisc_tag as root_tag,
    create_way,
    default_bridge_if_None,
)
from src.a05_idea_logic.healer import healerlink_shop
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_team import teamunit_shop
from src.a05_idea_logic.origin import originunit_shop
from src.a05_idea_logic.idea import IdeaUnit, ideaunit_shop


def test_IdeaUnit_Exists():
    x_ideaunit = IdeaUnit()
    assert x_ideaunit
    assert x_ideaunit._kids is None
    assert x_ideaunit.mass is None
    assert x_ideaunit.idea_tag is None
    assert x_ideaunit._uid is None
    assert x_ideaunit.reasonunits is None
    assert x_ideaunit._reasonheirs is None  # calculated field
    assert x_ideaunit.teamunit is None
    assert x_ideaunit._teamheir is None  # calculated field
    assert x_ideaunit.factunits is None
    assert x_ideaunit._factheirs is None  # calculated field
    assert x_ideaunit.awardlinks is None
    assert x_ideaunit._awardlines is None  # calculated field'
    assert x_ideaunit._awardheirs is None  # calculated field'
    assert x_ideaunit._originunit is None
    assert x_ideaunit.bridge is None
    assert x_ideaunit.begin is None
    assert x_ideaunit.close is None
    assert x_ideaunit.addin is None
    assert x_ideaunit.numor is None
    assert x_ideaunit.denom is None
    assert x_ideaunit.morph is None
    assert x_ideaunit.gogo_want is None
    assert x_ideaunit.stop_want is None
    assert x_ideaunit.pledge is None
    assert x_ideaunit.problem_bool is None
    assert x_ideaunit.healerlink is None
    # calculated_fields
    assert x_ideaunit._range_evaluated is None
    assert x_ideaunit._gogo_calc is None
    assert x_ideaunit._stop_calc is None
    assert x_ideaunit._descendant_pledge_count is None
    assert x_ideaunit._is_expanded is None
    assert x_ideaunit._all_acct_cred is None
    assert x_ideaunit._all_acct_debt is None
    assert x_ideaunit._level is None
    assert x_ideaunit._active_hx is None
    assert x_ideaunit._fund_ratio is None
    assert x_ideaunit.fund_coin is None
    assert x_ideaunit._fund_onset is None
    assert x_ideaunit._fund_cease is None
    assert x_ideaunit.root is None
    assert x_ideaunit.fisc_tag is None
    assert x_ideaunit._healerlink_ratio is None


def test_ideaunit_shop_WithNoParametersReturnsObj():
    # ESTABLISH / WHEN
    x_ideaunit = ideaunit_shop()

    # THEN
    assert x_ideaunit
    assert x_ideaunit._kids == {}
    assert x_ideaunit.mass == 1
    assert x_ideaunit.idea_tag is None
    assert x_ideaunit.fisc_tag == root_tag()
    assert x_ideaunit._uid is None
    assert x_ideaunit.begin is None
    assert x_ideaunit.close is None
    assert x_ideaunit.addin is None
    assert x_ideaunit.numor is None
    assert x_ideaunit.denom is None
    assert x_ideaunit.morph is None
    assert x_ideaunit.pledge is False
    assert x_ideaunit.problem_bool is False
    assert x_ideaunit._descendant_pledge_count is None
    assert x_ideaunit._awardlines == {}
    assert x_ideaunit.awardlinks == {}
    assert x_ideaunit._awardheirs == {}
    assert x_ideaunit._is_expanded is True
    assert x_ideaunit._factheirs == {}
    assert x_ideaunit.factunits == {}
    assert x_ideaunit.healerlink == healerlink_shop()
    assert x_ideaunit._gogo_calc is None
    assert x_ideaunit._stop_calc is None
    assert x_ideaunit._level is None
    assert x_ideaunit._active_hx == {}
    assert x_ideaunit._fund_ratio is None
    assert x_ideaunit.fund_coin == default_fund_coin_if_None()
    assert x_ideaunit._fund_onset is None
    assert x_ideaunit._fund_cease is None
    assert x_ideaunit.reasonunits == {}
    assert x_ideaunit._reasonheirs == {}
    assert x_ideaunit.teamunit == teamunit_shop()
    assert x_ideaunit._teamheir is None
    assert x_ideaunit._originunit == originunit_shop()
    assert x_ideaunit.bridge == default_bridge_if_None()
    assert x_ideaunit.root is False
    assert x_ideaunit._all_acct_cred is None
    assert x_ideaunit._all_acct_debt is None
    assert x_ideaunit._healerlink_ratio == 0


def test_ideaunit_shop_Allows_massToBeZero():
    # ESTABLISH
    zero_int = 0
    # WHEN
    x_ideaunit = ideaunit_shop("run", mass=zero_int)
    # THEN
    assert x_ideaunit.mass == zero_int


def test_ideaunit_shop_Allows_doesNotAllow_massToBeNegative():
    # ESTABLISH
    negative_int = -4
    # WHEN
    x_ideaunit = ideaunit_shop("run", mass=negative_int)
    # THEN
    zero_int = 0
    assert x_ideaunit.mass == zero_int


def test_ideaunit_shop_NonNoneParametersReturnsObj():
    # ESTABLISH
    x_healerlink = healerlink_shop({"Sue", "Yao"})
    x_problem_bool = True
    x_fund_coin = 88

    # WHEN
    x_ideaunit = ideaunit_shop(
        healerlink=x_healerlink, problem_bool=x_problem_bool, fund_coin=x_fund_coin
    )

    # THEN
    assert x_ideaunit.healerlink == x_healerlink
    assert x_ideaunit.problem_bool == x_problem_bool
    assert x_ideaunit.fund_coin == x_fund_coin


def test_ideaunit_shop_ReturnsObjWith_awardlinks():
    # ESTABLISH
    biker_give_force = 12
    biker_take_force = 15
    biker_awardlink = awardlink_shop("bikers2", biker_give_force, biker_take_force)
    swim_group_label = "swimmers"
    swim_give_force = 29
    swim_take_force = 32
    swim_awardlink = awardlink_shop(swim_group_label, swim_give_force, swim_take_force)
    x_awardlinks = {
        swim_awardlink.awardee_label: swim_awardlink,
        biker_awardlink.awardee_label: biker_awardlink,
    }

    # WHEN
    sport_str = "sport"
    sport_idea = ideaunit_shop(idea_tag=sport_str, awardlinks=x_awardlinks)

    # THEN
    assert sport_idea.awardlinks == x_awardlinks


def test_ideaunit_shop_ReturnsObjWithParameters():
    # ESTABLISH
    sport_gogo_want = 5
    sport_stop_want = 13

    # WHEN
    sport_str = "sport"
    sport_idea = ideaunit_shop(
        sport_str, gogo_want=sport_gogo_want, stop_want=sport_stop_want
    )

    # THEN
    assert sport_idea.gogo_want == sport_gogo_want
    assert sport_idea.stop_want == sport_stop_want


def test_IdeaUnit_get_obj_key_ReturnsObj():
    # ESTABLISH
    round_str = "round_stuff"
    round_way = create_way(root_tag(), round_str)
    ball_str = "ball"

    # WHEN
    ball_idea = ideaunit_shop(idea_tag=ball_str, parent_way=round_way)

    # THEN
    assert ball_idea.get_obj_key() == ball_str


def test_IdeaUnit_get_way_ReturnsObj():
    # ESTABLISH
    round_str = "round_stuff"
    slash_str = "/"
    round_way = create_way(root_tag(), round_str, bridge=slash_str)
    ball_str = "ball"

    # WHEN
    ball_idea = ideaunit_shop(ball_str, parent_way=round_way, bridge=slash_str)

    # THEN
    ball_way = create_way(round_way, ball_str, bridge=slash_str)
    assert ball_idea.get_idea_way() == ball_way


def test_IdeaUnit_set_parent_way_SetsAttr():
    # ESTABLISH
    round_str = "round_stuff"
    slash_str = "/"
    round_way = create_way(root_tag(), round_str, bridge=slash_str)
    ball_str = "ball"
    ball_idea = ideaunit_shop(ball_str, parent_way=round_way, bridge=slash_str)
    assert ball_idea.parent_way == round_way

    # WHEN
    sports_way = create_way(root_tag(), "sports", bridge=slash_str)
    ball_idea.set_parent_way(parent_way=sports_way)

    # THEN
    assert ball_idea.parent_way == sports_way


def test_IdeaUnit_clear_descendant_pledge_count_ClearsCorrectly():
    # ESTABLISH
    ball_str = "ball"
    ball_idea = ideaunit_shop(ball_str, _descendant_pledge_count=55)
    assert ball_idea._descendant_pledge_count == 55

    # WHEN
    ball_idea.clear_descendant_pledge_count()

    # THEN
    assert ball_idea._descendant_pledge_count is None


def test_IdeaUnit_add_to_descendant_pledge_count_CorrectlyAdds():
    # ESTABLISH
    ball_str = "ball"
    ball_idea = ideaunit_shop(ball_str, _descendant_pledge_count=55)
    ball_idea.clear_descendant_pledge_count()
    assert ball_idea._descendant_pledge_count is None

    # WHEN
    ball_idea.add_to_descendant_pledge_count(44)

    # THEN
    assert ball_idea._descendant_pledge_count == 44

    # WHEN
    ball_idea.add_to_descendant_pledge_count(33)

    # THEN
    assert ball_idea._descendant_pledge_count == 77


def test_IdeaUnit_is_math_ReturnsObj():
    # ESTABLISH
    swim_str = "swim"
    swim_idea = ideaunit_shop(swim_str)
    assert not swim_idea.is_math()
    # WHEN
    swim_idea.begin = 9
    # THEN
    assert not swim_idea.is_math()
    # WHEN
    swim_idea.close = 10
    # THEN
    assert swim_idea.is_math()
    # WHEN
    swim_idea.begin = None
    # THEN
    assert not swim_idea.is_math()


def test_IdeaUnit_clear_gogo_calc_stop_calc_SetsAttr():
    # ESTABLISH
    time_str = "time"
    time_idea = ideaunit_shop(time_str)
    time_idea._range_evaluated = True
    time_idea._gogo_calc = 3
    time_idea._stop_calc = 4
    assert time_idea._range_evaluated
    assert time_idea._gogo_calc
    assert time_idea._stop_calc

    # WHEN
    time_idea.clear_gogo_calc_stop_calc()

    # THEN
    assert not time_idea._range_evaluated
    assert not time_idea._gogo_calc
    assert not time_idea._stop_calc


def test_IdeaUnit_mold_gogo_calc_stop_calc_SetsAttr_denom():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_str, denom=time_denom)
    init_gogo_calc = 21
    init_stop_calc = 42
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea.denom = time_denom
    assert not time_idea._range_evaluated
    assert time_idea._gogo_calc
    assert time_idea._stop_calc

    # WHEN
    time_idea._mold_gogo_calc_stop_calc()

    # THEN
    assert time_idea._range_evaluated
    assert time_idea._gogo_calc == init_gogo_calc / time_denom
    assert time_idea._stop_calc == init_stop_calc / time_denom
    assert time_idea._gogo_calc == 3
    assert time_idea._stop_calc == 6


def test_IdeaUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_FullRangeCovered():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 45
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea.denom = time_denom
    assert time_idea._gogo_calc
    assert time_idea._stop_calc

    # WHEN
    time_idea._mold_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == 0
    assert time_idea._stop_calc == time_denom
    assert time_idea._gogo_calc == 0
    assert time_idea._stop_calc == 7


def test_IdeaUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_PartialRangeCovered():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 24
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea.denom = time_denom
    assert time_idea._gogo_calc
    assert time_idea._stop_calc

    # WHEN
    time_idea._mold_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == 0
    assert time_idea._stop_calc == (init_stop_calc - init_gogo_calc) % time_denom
    assert time_idea._gogo_calc == 0
    assert time_idea._stop_calc == 3


def test_IdeaUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario1_PartialRangeCovered():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 25
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea.denom = time_denom
    assert time_idea._gogo_calc
    assert time_idea._stop_calc

    # WHEN
    time_idea._mold_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == init_gogo_calc % time_denom
    assert time_idea._stop_calc == init_stop_calc % time_denom
    assert time_idea._gogo_calc == 1
    assert time_idea._stop_calc == 4


def test_IdeaUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario0_NoModifications():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 40
    time_idea.gogo_want = gogo_want
    time_idea.stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea.denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._mold_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == gogo_want
    assert time_idea._stop_calc == stop_want
    assert time_idea._gogo_calc == 30
    assert time_idea._stop_calc == 40


def test_IdeaUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifiyBoth():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 50
    time_idea.gogo_want = gogo_want
    time_idea.stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea.denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._mold_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc
    assert time_idea._gogo_calc == 21
    assert time_idea._stop_calc == 45


def test_IdeaUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifyLeft():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 40
    time_idea.gogo_want = gogo_want
    time_idea.stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea.denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._mold_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == stop_want
    assert time_idea._gogo_calc == 21
    assert time_idea._stop_calc == 40


def test_IdeaUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario2_ModifyRight():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 50
    time_idea.gogo_want = gogo_want
    time_idea.stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea.denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._mold_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == gogo_want
    assert time_idea._stop_calc == init_stop_calc
    assert time_idea._gogo_calc == 30
    assert time_idea._stop_calc == 45


def test_IdeaUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsLeft():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 15
    time_idea.gogo_want = gogo_want
    time_idea.stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea.denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._mold_gogo_calc_stop_calc()

    # THEN
    assert not time_idea._gogo_calc
    assert not time_idea._stop_calc


def test_IdeaUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsRight():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 60
    stop_want = 65
    time_idea.gogo_want = gogo_want
    time_idea.stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea.denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._mold_gogo_calc_stop_calc()

    # THEN
    assert not time_idea._gogo_calc
    assert not time_idea._stop_calc


def test_IdeaUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario4_None():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = None
    init_stop_calc = None
    gogo_want = 21
    stop_want = 45
    time_idea.gogo_want = gogo_want
    time_idea.stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea.denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._mold_gogo_calc_stop_calc()

    # THEN
    assert not time_idea._gogo_calc
    assert not time_idea._stop_calc
