from pytest import raises as pytest_raises
from src.ch02_rope_logic.rope import default_knot_if_None
from src.ch03_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
    validate_fund_pool,
    validate_respect_num,
)
from src.ch06_plan_logic.plan import get_default_moment_label as root_label
from src.ch07_belief_logic._ref.ch07_keywords import (
    Ch02Keywords as wx,
    Ch03Keywords as wx,
    Ch04Keywords as wx,
    credor_respect_str,
    debtor_respect_str,
    keeps_buildable_str,
    keeps_justified_str,
    last_pack_id_str,
    max_tree_traverse_str,
    moment_label_str,
    offtrack_fund_str,
    offtrack_kids_star_set_str,
    planroot_str,
    reason_contexts_str,
    sum_healerunit_share_str,
    tally_str,
    tree_traverse_count_str,
    voices_str,
)
from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop


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
    assert x_belief.fund_iota is None
    assert x_belief.respect_bit is None
    assert x_belief.penny is None
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
        keeps_buildable_str(),
        keeps_justified_str(),
        offtrack_fund_str(),
        offtrack_kids_star_set_str(),
        "_range_inheritors",
        wx.rational,
        reason_contexts_str(),
        sum_healerunit_share_str(),
        tree_traverse_count_str(),
        voices_str(),
        wx.knot,
        planroot_str(),
        credor_respect_str(),
        debtor_respect_str(),
        wx.groupunits,
        moment_label_str(),
        wx.fund_iota,
        wx.fund_pool,
        last_pack_id_str(),
        max_tree_traverse_str(),
        wx.belief_name,
        wx.penny,
        wx.respect_bit,
        tally_str(),
    }


def test_beliefunit_shop_ReturnsObjectWithFilledFields():
    # ESTABLISH
    sue_str = "Sue"
    iowa_moment_label = "Iowa"
    slash_knot = "/"
    x_fund_pool = 555
    x_fund_iota = 7
    x_respect_bit = 5
    x_penny = 1

    # WHEN
    x_belief = beliefunit_shop(
        belief_name=sue_str,
        moment_label=iowa_moment_label,
        knot=slash_knot,
        fund_pool=x_fund_pool,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
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
    assert x_belief.fund_iota == x_fund_iota
    assert x_belief.respect_bit == x_respect_bit
    assert x_belief.penny == x_penny
    assert x_belief.credor_respect == validate_respect_num()
    assert x_belief.debtor_respect == validate_respect_num()
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
    assert x_belief.moment_label == root_label()
    assert x_belief.knot == default_knot_if_None()
    assert x_belief.fund_pool == validate_fund_pool()
    assert x_belief.fund_iota == default_fund_iota_if_None()
    assert x_belief.respect_bit == default_RespectBit_if_None()
    assert x_belief.penny == filter_penny()
    assert x_belief.planroot.fund_iota == x_belief.fund_iota
    assert x_belief.planroot.knot == x_belief.knot
    assert x_belief.planroot.root
    assert x_belief.planroot.uid == 1
    assert x_belief.planroot.tree_level == 0
    assert x_belief.planroot.moment_label == x_belief.moment_label
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
    assert sue_belief.fund_pool == validate_fund_pool()

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
    assert zia_belief.fund_iota == 1
    assert zia_belief.fund_pool == x_fund_pool

    # WHEN
    new_fund_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_belief.set_fund_pool(new_fund_pool)

    # THEN
    assert (
        str(excinfo.value)
        == f"Belief '{zia_str}' cannot set fund_pool='{new_fund_pool}'. It is not divisible by fund_iota '{zia_belief.fund_iota}'"
    )
