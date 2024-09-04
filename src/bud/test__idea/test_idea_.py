from src._road.finance import default_fund_coin_if_none
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src.bud.healer import healerhold_shop
from src.bud.group import awardlink_shop
from src.bud.reason_team import teamunit_shop
from src.bud.origin import originunit_shop
from src.bud.idea import IdeaUnit, ideaunit_shop


def test_IdeaUnit_Exists():
    x_ideaunit = IdeaUnit()
    assert x_ideaunit
    assert x_ideaunit._kids is None
    assert x_ideaunit._mass is None
    assert x_ideaunit._label is None
    assert x_ideaunit._uid is None
    assert x_ideaunit._reasonunits is None
    assert x_ideaunit._reasonheirs is None  # calculated field
    assert x_ideaunit._teamunit is None
    assert x_ideaunit._teamheir is None  # calculated field
    assert x_ideaunit._factunits is None
    assert x_ideaunit._factheirs is None  # calculated field
    assert x_ideaunit._awardlinks is None
    assert x_ideaunit._awardlines is None  # calculated field'
    assert x_ideaunit._awardheirs is None  # calculated field'
    assert x_ideaunit._originunit is None
    assert x_ideaunit._road_delimiter is None
    assert x_ideaunit._begin is None
    assert x_ideaunit._close is None
    assert x_ideaunit._addin is None
    assert x_ideaunit._numor is None
    assert x_ideaunit._denom is None
    assert x_ideaunit._morph is None
    assert x_ideaunit._gogo_want is None
    assert x_ideaunit._stop_want is None
    assert x_ideaunit.pledge is None
    assert x_ideaunit._problem_bool is None
    assert x_ideaunit._healerhold is None
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
    assert x_ideaunit._fund_coin is None
    assert x_ideaunit._fund_onset is None
    assert x_ideaunit._fund_cease is None
    assert x_ideaunit._root is None
    assert x_ideaunit._bud_real_id is None
    assert x_ideaunit._healerhold_ratio is None


def test_ideaunit_shop_WithNoParametersReturnsObj():
    # ESTABLISH / WHEN
    x_ideaunit = ideaunit_shop()

    # THEN
    assert x_ideaunit
    assert x_ideaunit._kids == {}
    assert x_ideaunit._mass == 1
    assert x_ideaunit._label is None
    assert x_ideaunit._bud_real_id == root_label()
    assert x_ideaunit._uid is None
    assert x_ideaunit._begin is None
    assert x_ideaunit._close is None
    assert x_ideaunit._addin is None
    assert x_ideaunit._numor is None
    assert x_ideaunit._denom is None
    assert x_ideaunit._morph is None
    assert x_ideaunit.pledge is False
    assert x_ideaunit._problem_bool is False
    assert x_ideaunit._descendant_pledge_count is None
    assert x_ideaunit._awardlines == {}
    assert x_ideaunit._awardlinks == {}
    assert x_ideaunit._awardheirs == {}
    assert x_ideaunit._is_expanded is True
    assert x_ideaunit._factheirs == {}
    assert x_ideaunit._factunits == {}
    assert x_ideaunit._healerhold == healerhold_shop()
    assert x_ideaunit._gogo_calc is None
    assert x_ideaunit._stop_calc is None
    assert x_ideaunit._level is None
    assert x_ideaunit._active_hx == {}
    assert x_ideaunit._fund_ratio is None
    assert x_ideaunit._fund_coin == default_fund_coin_if_none()
    assert x_ideaunit._fund_onset is None
    assert x_ideaunit._fund_cease is None
    assert x_ideaunit._reasonunits == {}
    assert x_ideaunit._reasonheirs == {}
    assert x_ideaunit._teamunit == teamunit_shop()
    assert x_ideaunit._teamheir is None
    assert x_ideaunit._originunit == originunit_shop()
    assert x_ideaunit._road_delimiter == default_road_delimiter_if_none()
    assert x_ideaunit._root is False
    assert x_ideaunit._all_acct_cred is None
    assert x_ideaunit._all_acct_debt is None
    assert x_ideaunit._healerhold_ratio == 0


def test_ideaunit_shop_Allows_massToBeZero():
    # ESTABLISH
    zero_int = 0
    # WHEN
    x_ideaunit = ideaunit_shop("run", _mass=zero_int)
    # THEN
    assert x_ideaunit._mass == zero_int


def test_ideaunit_shop_Allows_doesNotAllow_massToBeNegative():
    # ESTABLISH
    negative_int = -4
    # WHEN
    x_ideaunit = ideaunit_shop("run", _mass=negative_int)
    # THEN
    zero_int = 0
    assert x_ideaunit._mass == zero_int


def test_ideaunit_shop_NonNoneParametersReturnsCorrectObj():
    # ESTABLISH
    x_healerhold = healerhold_shop({"Sue", "Yao"})
    x_problem_bool = True
    x_fund_coin = 88

    # WHEN
    x_ideaunit = ideaunit_shop(
        _healerhold=x_healerhold, _problem_bool=x_problem_bool, _fund_coin=x_fund_coin
    )

    # THEN
    assert x_ideaunit._healerhold == x_healerhold
    assert x_ideaunit._problem_bool == x_problem_bool
    assert x_ideaunit._fund_coin == x_fund_coin


def test_ideaunit_shop_ReturnsObjWith_awardlinks():
    # ESTABLISH
    biker_give_force = 12
    biker_take_force = 15
    biker_awardlink = awardlink_shop("bikers2", biker_give_force, biker_take_force)
    swim_group_id = "swimmers"
    swim_give_force = 29
    swim_take_force = 32
    swim_awardlink = awardlink_shop(swim_group_id, swim_give_force, swim_take_force)
    x_awardlinks = {
        swim_awardlink.group_id: swim_awardlink,
        biker_awardlink.group_id: biker_awardlink,
    }

    # WHEN
    sport_text = "sport"
    sport_idea = ideaunit_shop(_label=sport_text, _awardlinks=x_awardlinks)

    # THEN
    assert sport_idea._awardlinks == x_awardlinks


def test_ideaunit_shop_ReturnsObjWithParameters():
    # ESTABLISH
    sport_gogo_want = 5
    sport_stop_want = 13

    # WHEN
    sport_text = "sport"
    sport_idea = ideaunit_shop(
        sport_text, _gogo_want=sport_gogo_want, _stop_want=sport_stop_want
    )

    # THEN
    assert sport_idea._gogo_want == sport_gogo_want
    assert sport_idea._stop_want == sport_stop_want


def test_IdeaUnit_get_obj_key_ReturnsCorrectObj():
    # ESTABLISH
    round_text = "round_things"
    round_road = create_road(root_label(), round_text)
    ball_text = "ball"

    # WHEN
    ball_idea = ideaunit_shop(_label=ball_text, _parent_road=round_road)

    # THEN
    assert ball_idea.get_obj_key() == ball_text


def test_IdeaUnit_get_road_ReturnsCorrectObj():
    # ESTABLISH
    round_text = "round_things"
    slash_text = "/"
    round_road = create_road(root_label(), round_text, delimiter=slash_text)
    ball_text = "ball"

    # WHEN
    ball_idea = ideaunit_shop(
        ball_text, _parent_road=round_road, _road_delimiter=slash_text
    )

    # THEN
    ball_road = create_road(round_road, ball_text, delimiter=slash_text)
    assert ball_idea.get_road() == ball_road


def test_IdeaUnit_set_parent_road_SetsAttr():
    # ESTABLISH
    round_text = "round_things"
    slash_text = "/"
    round_road = create_road(root_label(), round_text, delimiter=slash_text)
    ball_text = "ball"
    ball_idea = ideaunit_shop(
        ball_text, _parent_road=round_road, _road_delimiter=slash_text
    )
    assert ball_idea._parent_road == round_road

    # WHEN
    sports_road = create_road(root_label(), "sports", delimiter=slash_text)
    ball_idea.set_parent_road(parent_road=sports_road)

    # THEN
    assert ball_idea._parent_road == sports_road


def test_IdeaUnit_clear_descendant_pledge_count_ClearsCorrectly():
    # ESTABLISH
    ball_text = "ball"
    ball_idea = ideaunit_shop(ball_text, _descendant_pledge_count=55)
    assert ball_idea._descendant_pledge_count == 55

    # WHEN
    ball_idea.clear_descendant_pledge_count()

    # THEN
    assert ball_idea._descendant_pledge_count is None


def test_IdeaUnit_add_to_descendant_pledge_count_CorrectlyAdds():
    # ESTABLISH
    ball_text = "ball"
    ball_idea = ideaunit_shop(ball_text, _descendant_pledge_count=55)
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
    swim_text = "swim"
    swim_idea = ideaunit_shop(swim_text)
    assert not swim_idea.is_math()
    # WHEN
    swim_idea._begin = 9
    # THEN
    assert not swim_idea.is_math()
    # WHEN
    swim_idea._close = 10
    # THEN
    assert swim_idea.is_math()
    # WHEN
    swim_idea._begin = None
    # THEN
    assert not swim_idea.is_math()


def test_IdeaUnit_clear_gogo_calc_stop_calc_SetsAttr():
    # ESTABLISH
    time_text = "time"
    time_idea = ideaunit_shop(time_text)
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


def test_IdeaUnit_transform_gogo_calc_stop_calc_SetsAttr_denom():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom)
    init_gogo_calc = 21
    init_stop_calc = 42
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea._denom = time_denom
    assert not time_idea._range_evaluated
    assert time_idea._gogo_calc
    assert time_idea._stop_calc

    # WHEN
    time_idea._transform_gogo_calc_stop_calc()

    # THEN
    assert time_idea._range_evaluated
    assert time_idea._gogo_calc == init_gogo_calc / time_denom
    assert time_idea._stop_calc == init_stop_calc / time_denom
    assert time_idea._gogo_calc == 3
    assert time_idea._stop_calc == 6


def test_IdeaUnit_transform_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_FullRangeCovered():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom, _morph=True)
    init_gogo_calc = 22
    init_stop_calc = 45
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea._denom = time_denom
    assert time_idea._gogo_calc
    assert time_idea._stop_calc

    # WHEN
    time_idea._transform_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == 0
    assert time_idea._stop_calc == time_denom
    assert time_idea._gogo_calc == 0
    assert time_idea._stop_calc == 7


def test_IdeaUnit_transform_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_PartialRangeCovered():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom, _morph=True)
    init_gogo_calc = 21
    init_stop_calc = 24
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea._denom = time_denom
    assert time_idea._gogo_calc
    assert time_idea._stop_calc

    # WHEN
    time_idea._transform_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == 0
    assert time_idea._stop_calc == (init_stop_calc - init_gogo_calc) % time_denom
    assert time_idea._gogo_calc == 0
    assert time_idea._stop_calc == 3


def test_IdeaUnit_transform_gogo_calc_stop_calc_SetsAttr_morph_Scenario1_PartialRangeCovered():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom, _morph=True)
    init_gogo_calc = 22
    init_stop_calc = 25
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea._denom = time_denom
    assert time_idea._gogo_calc
    assert time_idea._stop_calc

    # WHEN
    time_idea._transform_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == init_gogo_calc % time_denom
    assert time_idea._stop_calc == init_stop_calc % time_denom
    assert time_idea._gogo_calc == 1
    assert time_idea._stop_calc == 4


def test_IdeaUnit_transform_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario0_NoFilter():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom, _morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 40
    time_idea._gogo_want = gogo_want
    time_idea._stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea._denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._transform_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == gogo_want
    assert time_idea._stop_calc == stop_want
    assert time_idea._gogo_calc == 30
    assert time_idea._stop_calc == 40


def test_IdeaUnit_transform_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_FilterBoth():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom, _morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 50
    time_idea._gogo_want = gogo_want
    time_idea._stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea._denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._transform_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc
    assert time_idea._gogo_calc == 21
    assert time_idea._stop_calc == 45


def test_IdeaUnit_transform_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_FilterLeft():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom, _morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 40
    time_idea._gogo_want = gogo_want
    time_idea._stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea._denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._transform_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == stop_want
    assert time_idea._gogo_calc == 21
    assert time_idea._stop_calc == 40


def test_IdeaUnit_transform_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario2_FilterRight():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom, _morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 50
    time_idea._gogo_want = gogo_want
    time_idea._stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea._denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._transform_gogo_calc_stop_calc()

    # THEN
    assert time_idea._gogo_calc == gogo_want
    assert time_idea._stop_calc == init_stop_calc
    assert time_idea._gogo_calc == 30
    assert time_idea._stop_calc == 45


def test_IdeaUnit_transform_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsLeft():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom, _morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 15
    time_idea._gogo_want = gogo_want
    time_idea._stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea._denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._transform_gogo_calc_stop_calc()

    # THEN
    assert not time_idea._gogo_calc
    assert not time_idea._stop_calc


def test_IdeaUnit_transform_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsRight():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom, _morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 60
    stop_want = 65
    time_idea._gogo_want = gogo_want
    time_idea._stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea._denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._transform_gogo_calc_stop_calc()

    # THEN
    assert not time_idea._gogo_calc
    assert not time_idea._stop_calc


def test_IdeaUnit_transform_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario4_None():
    # ESTABLISH
    time_text = "time"
    time_denom = 7
    time_idea = ideaunit_shop(time_text, _denom=time_denom, _morph=True)
    init_gogo_calc = None
    init_stop_calc = None
    gogo_want = 21
    stop_want = 45
    time_idea._gogo_want = gogo_want
    time_idea._stop_want = stop_want
    time_idea._gogo_calc = init_gogo_calc
    time_idea._stop_calc = init_stop_calc
    time_idea._denom = time_denom
    assert time_idea._gogo_calc == init_gogo_calc
    assert time_idea._stop_calc == init_stop_calc

    # WHEN
    time_idea._transform_gogo_calc_stop_calc()

    # THEN
    assert not time_idea._gogo_calc
    assert not time_idea._stop_calc
