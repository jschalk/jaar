from pytest import raises as pytest_raises
from src.ch02_rope_logic.rope import default_knot_if_None
from src.ch03_finance_logic.allot import default_grain_num_if_None, validate_pool_num
from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic._ref.ch07_keywords import Ch07Keywords as wx
from src.ch07_belief_logic._ref.ch07_semantic_types import RespectNum
from src.ch07_belief_logic.belief_main import (
    BeliefUnit,
    beliefunit_shop,
    get_default_moment_label,
)


def test_BeliefUnit_Exists():
    # ESTABLISH /  WHEN
    x_belief = BeliefUnit()

    # THEN
    assert x_belief
    assert x_belief.moment_label is None
    assert x_belief.belief_name is None
    assert x_belief.tally is None
    assert x_belief.voices is None
    assert x_belief.planroot is None
    assert x_belief.credor_respect is None
    assert x_belief.debtor_respect is None
    assert x_belief.max_tree_traverse is None
    assert x_belief.knot is None
    assert x_belief.fund_pool is None
    assert x_belief.fund_grain is None
    assert x_belief.respect_grain is None
    assert x_belief.money_grain is None
    assert x_belief.last_pack_id is None
    # calculated attr
    assert x_belief._plan_dict is None
    assert x_belief._keep_dict is None
    assert x_belief._healers_dict is None
    assert x_belief.tree_traverse_count is None
    assert x_belief.rational is None
    assert x_belief.keeps_justified is None
    assert x_belief.keeps_buildable is None
    assert x_belief.sum_healerunit_share is None
    assert x_belief.offtrack_kids_star_set is None
    assert x_belief.offtrack_fund is None
    assert x_belief.reason_contexts is None
    assert x_belief._range_inheritors is None
    assert str(type(x_belief.planroot)).find("None") == 8
    obj_attrs = set(x_belief.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        "_plan_dict",
        "_healers_dict",
        "_keep_dict",
        wx.keeps_buildable,
        wx.keeps_justified,
        wx.offtrack_fund,
        wx.offtrack_kids_star_set,
        "_range_inheritors",
        wx.rational,
        wx.reason_contexts,
        wx.sum_healerunit_share,
        wx.tree_traverse_count,
        wx.voices,
        wx.knot,
        wx.planroot,
        wx.credor_respect,
        wx.debtor_respect,
        wx.groupunits,
        wx.moment_label,
        wx.fund_grain,
        wx.fund_pool,
        wx.last_pack_id,
        wx.max_tree_traverse,
        wx.belief_name,
        wx.money_grain,
        wx.respect_grain,
        wx.tally,
    }


def test_BeliefUnit_get_nexus_label_Scenario0_Default_knot():
    # ESTABLISH
    casa_str = "casa"
    casa_planroot = planunit_shop(casa_str)
    amy_str = "Amy23"
    print(f"{casa_planroot.get_plan_rope()=}")
    x_belief = BeliefUnit(
        belief_name=amy_str, knot=casa_planroot.knot, planroot=casa_planroot
    )

    # WHEN
    nexus_label = x_belief.get_nexus_label()

    # THEN
    assert nexus_label == casa_str


def test_BeliefUnit_get_nexus_label_Scenario1_NonDefault_knot():
    # ESTABLISH
    casa_str = "casa"
    slash_str = "/"
    assert slash_str != default_knot_if_None()
    casa_planroot = planunit_shop(casa_str, knot=slash_str)
    amy_str = "Amy23"
    print(f"{casa_planroot.get_plan_rope()=}")
    x_belief = BeliefUnit(
        belief_name=amy_str, knot=casa_planroot.knot, planroot=casa_planroot
    )

    # WHEN
    nexus_label = x_belief.get_nexus_label()

    # THEN
    assert nexus_label == casa_str


def test_beliefunit_shop_ReturnsObjectWithFilledFields():
    # ESTABLISH
    sue_str = "Sue"
    iowa_moment_label = "Iowa"
    slash_knot = "/"
    x_fund_pool = 555
    x_fund_grain = 7
    x_respect_grain = 5
    x_money_grain = 1

    # WHEN
    x_belief = beliefunit_shop(
        belief_name=sue_str,
        moment_label=iowa_moment_label,
        knot=slash_knot,
        fund_pool=x_fund_pool,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        money_grain=x_money_grain,
    )

    # THEN
    assert x_belief
    assert x_belief.belief_name == sue_str
    assert x_belief.moment_label == iowa_moment_label
    assert x_belief.tally == 1
    assert x_belief.voices == {}
    assert x_belief.planroot is not None
    assert x_belief.max_tree_traverse == 3
    assert x_belief.knot == slash_knot
    assert x_belief.fund_pool == x_fund_pool
    assert x_belief.fund_grain == x_fund_grain
    assert x_belief.respect_grain == x_respect_grain
    assert x_belief.money_grain == x_money_grain
    assert x_belief.credor_respect == RespectNum(validate_pool_num())
    assert x_belief.debtor_respect == RespectNum(validate_pool_num())
    assert not x_belief.last_pack_id
    # calculated attr
    assert x_belief._plan_dict == {}
    assert x_belief._keep_dict == {}
    assert x_belief._healers_dict == {}
    assert not x_belief.tree_traverse_count
    assert x_belief.rational is False
    assert x_belief.keeps_justified is False
    assert x_belief.keeps_buildable is False
    assert x_belief.sum_healerunit_share == 0
    assert x_belief.offtrack_kids_star_set == set()
    assert not x_belief.offtrack_fund
    assert x_belief.reason_contexts == set()
    assert x_belief._range_inheritors == {}
    print(f"{type(x_belief.planroot)=}") == 0
    assert str(type(x_belief.planroot)).find(".plan.PlanUnit'>") > 0


def test_beliefunit_shop_ReturnsObjectWithCorrectEmptyField():
    # ESTABLISH / WHEN
    x_belief = beliefunit_shop()

    # THEN
    assert x_belief.belief_name == ""
    assert x_belief.moment_label == get_default_moment_label()
    assert x_belief.knot == default_knot_if_None()
    assert x_belief.fund_pool == validate_pool_num()
    assert x_belief.fund_grain == default_grain_num_if_None()
    assert x_belief.respect_grain == default_grain_num_if_None()
    assert x_belief.money_grain == default_grain_num_if_None()
    assert x_belief.planroot.fund_grain == x_belief.fund_grain
    assert x_belief.planroot.knot == x_belief.knot
    assert x_belief.planroot.uid == 1
    assert x_belief.planroot.tree_level == 0
    assert x_belief.planroot.knot == x_belief.knot
    assert x_belief.planroot.parent_rope == ""


def test_BeliefUnit_set_max_tree_traverse_SetsInt():
    # ESTABLISH
    zia_str = "Zia"
    zia_belief = beliefunit_shop(belief_name=zia_str)
    assert zia_belief.max_tree_traverse == 3

    # WHEN
    zia_belief.set_max_tree_traverse(x_int=11)

    # THEN
    assert zia_belief.max_tree_traverse == 11


def test_BeliefUnit_set_max_tree_traverse_RaisesError_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    zia_belief = beliefunit_shop(belief_name=zia_str)
    assert zia_belief.max_tree_traverse == 3
    zia_tree_traverse = 1

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_belief.set_max_tree_traverse(x_int=zia_tree_traverse)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: '1' must be number that is 2 or greater"
    )


def test_BeliefUnit_set_max_tree_traverse_RaisesError_Scenario1():
    # ESTABLISH
    zia_str = "Zia"
    zia_belief = beliefunit_shop(belief_name=zia_str)
    assert zia_belief.max_tree_traverse == 3

    # WHEN / THEN
    zia_tree_traverse = 3.5
    with pytest_raises(Exception) as excinfo:
        zia_belief.set_max_tree_traverse(x_int=zia_tree_traverse)
    assert (
        str(excinfo.value)
        == f"set_max_tree_traverse: '{zia_tree_traverse}' must be number that is 2 or greater"
    )


def test_BeliefUnit_make_rope_ReturnsObj():
    # ESTABLISH
    x_moment_label = "amy45"
    slash_knot = "/"
    sue_str = "Sue"
    sue_belief = beliefunit_shop(sue_str, x_moment_label, knot=slash_knot)
    casa_str = "casa"
    v1_casa_rope = sue_belief.make_l1_rope(casa_str)

    # WHEN
    v2_casa_rope = sue_belief.make_l1_rope(casa_str)

    # THEN
    assert v1_casa_rope == v2_casa_rope


def test_BeliefUnit_set_last_pack_id_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue", "Texas")
    assert sue_belief.last_pack_id is None

    # WHEN
    x_last_pack_id = 89
    sue_belief.set_last_pack_id(x_last_pack_id)

    # THEN
    assert sue_belief.last_pack_id == x_last_pack_id


def test_BeliefUnit_set_last_pack_id_RaisesError():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue", "Texas")
    old_last_pack_id = 89
    sue_belief.set_last_pack_id(old_last_pack_id)

    # WHEN / THEN
    new_last_pack_id = 72
    assert new_last_pack_id < old_last_pack_id
    with pytest_raises(Exception) as excinfo:
        sue_belief.set_last_pack_id(new_last_pack_id)
    assert (
        str(excinfo.value)
        == f"Cannot set _last_pack_id to {new_last_pack_id} because it is less than {old_last_pack_id}."
    )


def test_BeliefUnit_del_last_pack_id_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue", "Texas")
    old_last_pack_id = 89
    sue_belief.set_last_pack_id(old_last_pack_id)
    assert sue_belief.last_pack_id is not None

    # WHEN
    sue_belief.del_last_pack_id()

    # THEN
    assert sue_belief.last_pack_id is None


def test_BeliefUnit_set_fund_pool_SetsAttr():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue", "Texas")
    sue_fund_pool = 99000
    assert sue_belief.fund_pool == validate_pool_num()

    # WHEN
    sue_belief.set_fund_pool(sue_fund_pool)

    # THEN
    assert sue_belief.fund_pool == 99000


def test_BeliefUnit_set_fund_pool_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_str = "Zia"
    zia_belief = beliefunit_shop(zia_str)
    x_fund_pool = 23
    zia_belief.set_fund_pool(x_fund_pool)
    assert zia_belief.fund_grain == 1
    assert zia_belief.fund_pool == x_fund_pool

    # WHEN
    new_fund_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_belief.set_fund_pool(new_fund_pool)

    # THEN
    assert (
        str(excinfo.value)
        == f"Belief '{zia_str}' cannot set fund_pool='{new_fund_pool}'. It is not divisible by fund_grain '{zia_belief.fund_grain}'"
    )
