from src.f01_road.finance import default_fund_coin_if_none
from src.f01_road.road import (
    get_default_fiscal_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src.f02_bud.healer import healerlink_shop
from src.f02_bud.group import awardlink_shop
from src.f02_bud.reason_team import teamunit_shop
from src.f02_bud.origin import originunit_shop
from src.f02_bud.item import ItemUnit, itemunit_shop


def test_ItemUnit_Exists():
    x_itemunit = ItemUnit()
    assert x_itemunit
    assert x_itemunit._kids is None
    assert x_itemunit.mass is None
    assert x_itemunit._label is None
    assert x_itemunit._uid is None
    assert x_itemunit.reasonunits is None
    assert x_itemunit._reasonheirs is None  # calculated field
    assert x_itemunit.teamunit is None
    assert x_itemunit._teamheir is None  # calculated field
    assert x_itemunit.factunits is None
    assert x_itemunit._factheirs is None  # calculated field
    assert x_itemunit.awardlinks is None
    assert x_itemunit._awardlines is None  # calculated field'
    assert x_itemunit._awardheirs is None  # calculated field'
    assert x_itemunit._originunit is None
    assert x_itemunit._road_delimiter is None
    assert x_itemunit.begin is None
    assert x_itemunit.close is None
    assert x_itemunit.addin is None
    assert x_itemunit.numor is None
    assert x_itemunit.denom is None
    assert x_itemunit.morph is None
    assert x_itemunit.gogo_want is None
    assert x_itemunit.stop_want is None
    assert x_itemunit.pledge is None
    assert x_itemunit.problem_bool is None
    assert x_itemunit.healerlink is None
    # calculated_fields
    assert x_itemunit._range_evaluated is None
    assert x_itemunit._gogo_calc is None
    assert x_itemunit._stop_calc is None
    assert x_itemunit._descendant_pledge_count is None
    assert x_itemunit._is_expanded is None
    assert x_itemunit._all_acct_cred is None
    assert x_itemunit._all_acct_debt is None
    assert x_itemunit._level is None
    assert x_itemunit._active_hx is None
    assert x_itemunit._fund_ratio is None
    assert x_itemunit._fund_coin is None
    assert x_itemunit._fund_onset is None
    assert x_itemunit._fund_cease is None
    assert x_itemunit._root is None
    assert x_itemunit._bud_fiscal_id is None
    assert x_itemunit._healerlink_ratio is None


def test_itemunit_shop_WithNoParametersReturnsObj():
    # ESTABLISH / WHEN
    x_itemunit = itemunit_shop()

    # THEN
    assert x_itemunit
    assert x_itemunit._kids == {}
    assert x_itemunit.mass == 1
    assert x_itemunit._label is None
    assert x_itemunit._bud_fiscal_id == root_label()
    assert x_itemunit._uid is None
    assert x_itemunit.begin is None
    assert x_itemunit.close is None
    assert x_itemunit.addin is None
    assert x_itemunit.numor is None
    assert x_itemunit.denom is None
    assert x_itemunit.morph is None
    assert x_itemunit.pledge is False
    assert x_itemunit.problem_bool is False
    assert x_itemunit._descendant_pledge_count is None
    assert x_itemunit._awardlines == {}
    assert x_itemunit.awardlinks == {}
    assert x_itemunit._awardheirs == {}
    assert x_itemunit._is_expanded is True
    assert x_itemunit._factheirs == {}
    assert x_itemunit.factunits == {}
    assert x_itemunit.healerlink == healerlink_shop()
    assert x_itemunit._gogo_calc is None
    assert x_itemunit._stop_calc is None
    assert x_itemunit._level is None
    assert x_itemunit._active_hx == {}
    assert x_itemunit._fund_ratio is None
    assert x_itemunit._fund_coin == default_fund_coin_if_none()
    assert x_itemunit._fund_onset is None
    assert x_itemunit._fund_cease is None
    assert x_itemunit.reasonunits == {}
    assert x_itemunit._reasonheirs == {}
    assert x_itemunit.teamunit == teamunit_shop()
    assert x_itemunit._teamheir is None
    assert x_itemunit._originunit == originunit_shop()
    assert x_itemunit._road_delimiter == default_road_delimiter_if_none()
    assert x_itemunit._root is False
    assert x_itemunit._all_acct_cred is None
    assert x_itemunit._all_acct_debt is None
    assert x_itemunit._healerlink_ratio == 0


def test_itemunit_shop_Allows_massToBeZero():
    # ESTABLISH
    zero_int = 0
    # WHEN
    x_itemunit = itemunit_shop("run", mass=zero_int)
    # THEN
    assert x_itemunit.mass == zero_int


def test_itemunit_shop_Allows_doesNotAllow_massToBeNegative():
    # ESTABLISH
    negative_int = -4
    # WHEN
    x_itemunit = itemunit_shop("run", mass=negative_int)
    # THEN
    zero_int = 0
    assert x_itemunit.mass == zero_int


def test_itemunit_shop_NonNoneParametersReturnsCorrectObj():
    # ESTABLISH
    x_healerlink = healerlink_shop({"Sue", "Yao"})
    x_problem_bool = True
    x_fund_coin = 88

    # WHEN
    x_itemunit = itemunit_shop(
        healerlink=x_healerlink, problem_bool=x_problem_bool, _fund_coin=x_fund_coin
    )

    # THEN
    assert x_itemunit.healerlink == x_healerlink
    assert x_itemunit.problem_bool == x_problem_bool
    assert x_itemunit._fund_coin == x_fund_coin


def test_itemunit_shop_ReturnsObjWith_awardlinks():
    # ESTABLISH
    biker_give_force = 12
    biker_take_force = 15
    biker_awardlink = awardlink_shop("bikers2", biker_give_force, biker_take_force)
    swim_group_id = "swimmers"
    swim_give_force = 29
    swim_take_force = 32
    swim_awardlink = awardlink_shop(swim_group_id, swim_give_force, swim_take_force)
    x_awardlinks = {
        swim_awardlink.awardee_id: swim_awardlink,
        biker_awardlink.awardee_id: biker_awardlink,
    }

    # WHEN
    sport_str = "sport"
    sport_item = itemunit_shop(_label=sport_str, awardlinks=x_awardlinks)

    # THEN
    assert sport_item.awardlinks == x_awardlinks


def test_itemunit_shop_ReturnsObjWithParameters():
    # ESTABLISH
    sport_gogo_want = 5
    sport_stop_want = 13

    # WHEN
    sport_str = "sport"
    sport_item = itemunit_shop(
        sport_str, gogo_want=sport_gogo_want, stop_want=sport_stop_want
    )

    # THEN
    assert sport_item.gogo_want == sport_gogo_want
    assert sport_item.stop_want == sport_stop_want


def test_ItemUnit_get_obj_key_ReturnsCorrectObj():
    # ESTABLISH
    round_str = "round_things"
    round_road = create_road(root_label(), round_str)
    ball_str = "ball"

    # WHEN
    ball_item = itemunit_shop(_label=ball_str, _parent_road=round_road)

    # THEN
    assert ball_item.get_obj_key() == ball_str


def test_ItemUnit_get_road_ReturnsCorrectObj():
    # ESTABLISH
    round_str = "round_things"
    slash_str = "/"
    round_road = create_road(root_label(), round_str, delimiter=slash_str)
    ball_str = "ball"

    # WHEN
    ball_item = itemunit_shop(
        ball_str, _parent_road=round_road, _road_delimiter=slash_str
    )

    # THEN
    ball_road = create_road(round_road, ball_str, delimiter=slash_str)
    assert ball_item.get_road() == ball_road


def test_ItemUnit_set_parent_road_SetsAttr():
    # ESTABLISH
    round_str = "round_things"
    slash_str = "/"
    round_road = create_road(root_label(), round_str, delimiter=slash_str)
    ball_str = "ball"
    ball_item = itemunit_shop(
        ball_str, _parent_road=round_road, _road_delimiter=slash_str
    )
    assert ball_item._parent_road == round_road

    # WHEN
    sports_road = create_road(root_label(), "sports", delimiter=slash_str)
    ball_item.set_parent_road(parent_road=sports_road)

    # THEN
    assert ball_item._parent_road == sports_road


def test_ItemUnit_clear_descendant_pledge_count_ClearsCorrectly():
    # ESTABLISH
    ball_str = "ball"
    ball_item = itemunit_shop(ball_str, _descendant_pledge_count=55)
    assert ball_item._descendant_pledge_count == 55

    # WHEN
    ball_item.clear_descendant_pledge_count()

    # THEN
    assert ball_item._descendant_pledge_count is None


def test_ItemUnit_add_to_descendant_pledge_count_CorrectlyAdds():
    # ESTABLISH
    ball_str = "ball"
    ball_item = itemunit_shop(ball_str, _descendant_pledge_count=55)
    ball_item.clear_descendant_pledge_count()
    assert ball_item._descendant_pledge_count is None

    # WHEN
    ball_item.add_to_descendant_pledge_count(44)

    # THEN
    assert ball_item._descendant_pledge_count == 44

    # WHEN
    ball_item.add_to_descendant_pledge_count(33)

    # THEN
    assert ball_item._descendant_pledge_count == 77


def test_ItemUnit_is_math_ReturnsObj():
    # ESTABLISH
    swim_str = "swim"
    swim_item = itemunit_shop(swim_str)
    assert not swim_item.is_math()
    # WHEN
    swim_item.begin = 9
    # THEN
    assert not swim_item.is_math()
    # WHEN
    swim_item.close = 10
    # THEN
    assert swim_item.is_math()
    # WHEN
    swim_item.begin = None
    # THEN
    assert not swim_item.is_math()


def test_ItemUnit_clear_gogo_calc_stop_calc_SetsAttr():
    # ESTABLISH
    time_str = "time"
    time_item = itemunit_shop(time_str)
    time_item._range_evaluated = True
    time_item._gogo_calc = 3
    time_item._stop_calc = 4
    assert time_item._range_evaluated
    assert time_item._gogo_calc
    assert time_item._stop_calc

    # WHEN
    time_item.clear_gogo_calc_stop_calc()

    # THEN
    assert not time_item._range_evaluated
    assert not time_item._gogo_calc
    assert not time_item._stop_calc


def test_ItemUnit_mold_gogo_calc_stop_calc_SetsAttr_denom():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_item = itemunit_shop(time_str, denom=time_denom)
    init_gogo_calc = 21
    init_stop_calc = 42
    time_item._gogo_calc = init_gogo_calc
    time_item._stop_calc = init_stop_calc
    time_item.denom = time_denom
    assert not time_item._range_evaluated
    assert time_item._gogo_calc
    assert time_item._stop_calc

    # WHEN
    time_item._mold_gogo_calc_stop_calc()

    # THEN
    assert time_item._range_evaluated
    assert time_item._gogo_calc == init_gogo_calc / time_denom
    assert time_item._stop_calc == init_stop_calc / time_denom
    assert time_item._gogo_calc == 3
    assert time_item._stop_calc == 6


def test_ItemUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_FullRangeCovered():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_item = itemunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 45
    time_item._gogo_calc = init_gogo_calc
    time_item._stop_calc = init_stop_calc
    time_item.denom = time_denom
    assert time_item._gogo_calc
    assert time_item._stop_calc

    # WHEN
    time_item._mold_gogo_calc_stop_calc()

    # THEN
    assert time_item._gogo_calc == 0
    assert time_item._stop_calc == time_denom
    assert time_item._gogo_calc == 0
    assert time_item._stop_calc == 7


def test_ItemUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario0_PartialRangeCovered():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_item = itemunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 24
    time_item._gogo_calc = init_gogo_calc
    time_item._stop_calc = init_stop_calc
    time_item.denom = time_denom
    assert time_item._gogo_calc
    assert time_item._stop_calc

    # WHEN
    time_item._mold_gogo_calc_stop_calc()

    # THEN
    assert time_item._gogo_calc == 0
    assert time_item._stop_calc == (init_stop_calc - init_gogo_calc) % time_denom
    assert time_item._gogo_calc == 0
    assert time_item._stop_calc == 3


def test_ItemUnit_mold_gogo_calc_stop_calc_SetsAttr_morph_Scenario1_PartialRangeCovered():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_item = itemunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 22
    init_stop_calc = 25
    time_item._gogo_calc = init_gogo_calc
    time_item._stop_calc = init_stop_calc
    time_item.denom = time_denom
    assert time_item._gogo_calc
    assert time_item._stop_calc

    # WHEN
    time_item._mold_gogo_calc_stop_calc()

    # THEN
    assert time_item._gogo_calc == init_gogo_calc % time_denom
    assert time_item._stop_calc == init_stop_calc % time_denom
    assert time_item._gogo_calc == 1
    assert time_item._stop_calc == 4


def test_ItemUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario0_NoModifications():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_item = itemunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 40
    time_item.gogo_want = gogo_want
    time_item.stop_want = stop_want
    time_item._gogo_calc = init_gogo_calc
    time_item._stop_calc = init_stop_calc
    time_item.denom = time_denom
    assert time_item._gogo_calc == init_gogo_calc
    assert time_item._stop_calc == init_stop_calc

    # WHEN
    time_item._mold_gogo_calc_stop_calc()

    # THEN
    assert time_item._gogo_calc == gogo_want
    assert time_item._stop_calc == stop_want
    assert time_item._gogo_calc == 30
    assert time_item._stop_calc == 40


def test_ItemUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifiyBoth():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_item = itemunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 50
    time_item.gogo_want = gogo_want
    time_item.stop_want = stop_want
    time_item._gogo_calc = init_gogo_calc
    time_item._stop_calc = init_stop_calc
    time_item.denom = time_denom
    assert time_item._gogo_calc == init_gogo_calc
    assert time_item._stop_calc == init_stop_calc

    # WHEN
    time_item._mold_gogo_calc_stop_calc()

    # THEN
    assert time_item._gogo_calc == init_gogo_calc
    assert time_item._stop_calc == init_stop_calc
    assert time_item._gogo_calc == 21
    assert time_item._stop_calc == 45


def test_ItemUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario1_ModifyLeft():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_item = itemunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 40
    time_item.gogo_want = gogo_want
    time_item.stop_want = stop_want
    time_item._gogo_calc = init_gogo_calc
    time_item._stop_calc = init_stop_calc
    time_item.denom = time_denom
    assert time_item._gogo_calc == init_gogo_calc
    assert time_item._stop_calc == init_stop_calc

    # WHEN
    time_item._mold_gogo_calc_stop_calc()

    # THEN
    assert time_item._gogo_calc == init_gogo_calc
    assert time_item._stop_calc == stop_want
    assert time_item._gogo_calc == 21
    assert time_item._stop_calc == 40


def test_ItemUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario2_ModifyRight():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_item = itemunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 30
    stop_want = 50
    time_item.gogo_want = gogo_want
    time_item.stop_want = stop_want
    time_item._gogo_calc = init_gogo_calc
    time_item._stop_calc = init_stop_calc
    time_item.denom = time_denom
    assert time_item._gogo_calc == init_gogo_calc
    assert time_item._stop_calc == init_stop_calc

    # WHEN
    time_item._mold_gogo_calc_stop_calc()

    # THEN
    assert time_item._gogo_calc == gogo_want
    assert time_item._stop_calc == init_stop_calc
    assert time_item._gogo_calc == 30
    assert time_item._stop_calc == 45


def test_ItemUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsLeft():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_item = itemunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 10
    stop_want = 15
    time_item.gogo_want = gogo_want
    time_item.stop_want = stop_want
    time_item._gogo_calc = init_gogo_calc
    time_item._stop_calc = init_stop_calc
    time_item.denom = time_denom
    assert time_item._gogo_calc == init_gogo_calc
    assert time_item._stop_calc == init_stop_calc

    # WHEN
    time_item._mold_gogo_calc_stop_calc()

    # THEN
    assert not time_item._gogo_calc
    assert not time_item._stop_calc


def test_ItemUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario3_OutOfBoundsRight():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_item = itemunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = 21
    init_stop_calc = 45
    gogo_want = 60
    stop_want = 65
    time_item.gogo_want = gogo_want
    time_item.stop_want = stop_want
    time_item._gogo_calc = init_gogo_calc
    time_item._stop_calc = init_stop_calc
    time_item.denom = time_denom
    assert time_item._gogo_calc == init_gogo_calc
    assert time_item._stop_calc == init_stop_calc

    # WHEN
    time_item._mold_gogo_calc_stop_calc()

    # THEN
    assert not time_item._gogo_calc
    assert not time_item._stop_calc


def test_ItemUnit_mold_gogo_calc_stop_calc_SetsAttr_gogo_want_stop_want_Scenario4_None():
    # ESTABLISH
    time_str = "time"
    time_denom = 7
    time_item = itemunit_shop(time_str, denom=time_denom, morph=True)
    init_gogo_calc = None
    init_stop_calc = None
    gogo_want = 21
    stop_want = 45
    time_item.gogo_want = gogo_want
    time_item.stop_want = stop_want
    time_item._gogo_calc = init_gogo_calc
    time_item._stop_calc = init_stop_calc
    time_item.denom = time_denom
    assert time_item._gogo_calc == init_gogo_calc
    assert time_item._stop_calc == init_stop_calc

    # WHEN
    time_item._mold_gogo_calc_stop_calc()

    # THEN
    assert not time_item._gogo_calc
    assert not time_item._stop_calc
