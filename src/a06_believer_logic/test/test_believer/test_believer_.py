from pytest import raises as pytest_raises
from src.a01_term_logic.rope import default_knot_if_None
from src.a02_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
    validate_fund_pool,
    validate_respect_num,
)
from src.a02_finance_logic.test._util.a02_str import fund_pool_str, knot_str
from src.a05_plan_logic.plan import get_default_belief_label as root_label
from src.a06_believer_logic.believer import BelieverUnit, believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    _keeps_buildable_str,
    _keeps_justified_str,
    _offtrack_fund_str,
    _offtrack_kids_mass_set_str,
    _rational_str,
    _reason_rcontexts_str,
    _sum_healerlink_share_str,
    _tree_traverse_count_str,
    belief_label_str,
    believer_name_str,
    credor_respect_str,
    debtor_respect_str,
    fund_iota_str,
    last_pack_id_str,
    max_tree_traverse_str,
    penny_str,
    respect_bit_str,
    tally_str,
)


def test_BelieverUnit_Exists():
    # ESTABLISH /  WHEN
    x_believer = BelieverUnit()

    # THEN
    assert x_believer
    assert x_believer.belief_label is None
    assert x_believer.believer_name is None
    assert x_believer.tally is None
    assert x_believer.persons is None
    assert x_believer.planroot is None
    assert x_believer.credor_respect is None
    assert x_believer.debtor_respect is None
    assert x_believer.max_tree_traverse is None
    assert x_believer.knot is None
    assert x_believer.fund_pool is None
    assert x_believer.fund_iota is None
    assert x_believer.respect_bit is None
    assert x_believer.penny is None
    assert x_believer.last_pack_id is None
    # calculated attr
    assert x_believer._plan_dict is None
    assert x_believer._keep_dict is None
    assert x_believer._healers_dict is None
    assert x_believer._tree_traverse_count is None
    assert x_believer._rational is None
    assert x_believer._keeps_justified is None
    assert x_believer._keeps_buildable is None
    assert x_believer._sum_healerlink_share is None
    assert x_believer._offtrack_kids_mass_set is None
    assert x_believer._offtrack_fund is None
    assert x_believer._reason_rcontexts is None
    assert x_believer._range_inheritors is None
    assert str(type(x_believer.planroot)).find("None") == 8
    obj_attrs = set(x_believer.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        "_plan_dict",
        "_healers_dict",
        "_keep_dict",
        _keeps_buildable_str(),
        _keeps_justified_str(),
        _offtrack_fund_str(),
        _offtrack_kids_mass_set_str(),
        "_range_inheritors",
        _rational_str(),
        _reason_rcontexts_str(),
        _sum_healerlink_share_str(),
        _tree_traverse_count_str(),
        "persons",
        knot_str(),
        "planroot",
        credor_respect_str(),
        debtor_respect_str(),
        "_groupunits",
        belief_label_str(),
        fund_iota_str(),
        fund_pool_str(),
        last_pack_id_str(),
        max_tree_traverse_str(),
        believer_name_str(),
        penny_str(),
        respect_bit_str(),
        tally_str(),
    }


def test_believerunit_shop_ReturnsObjectWithFilledFields():
    # ESTABLISH
    sue_str = "Sue"
    iowa_belief_label = "Iowa"
    slash_knot = "/"
    x_fund_pool = 555
    x_fund_iota = 7
    x_respect_bit = 5
    x_penny = 1

    # WHEN
    x_believer = believerunit_shop(
        believer_name=sue_str,
        belief_label=iowa_belief_label,
        knot=slash_knot,
        fund_pool=x_fund_pool,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )

    # THEN
    assert x_believer
    assert x_believer.believer_name == sue_str
    assert x_believer.belief_label == iowa_belief_label
    assert x_believer.tally == 1
    assert x_believer.persons == {}
    assert x_believer.planroot is not None
    assert x_believer.max_tree_traverse == 3
    assert x_believer.knot == slash_knot
    assert x_believer.fund_pool == x_fund_pool
    assert x_believer.fund_iota == x_fund_iota
    assert x_believer.respect_bit == x_respect_bit
    assert x_believer.penny == x_penny
    assert x_believer.credor_respect == validate_respect_num()
    assert x_believer.debtor_respect == validate_respect_num()
    assert not x_believer.last_pack_id
    # calculated attr
    assert x_believer._plan_dict == {}
    assert x_believer._keep_dict == {}
    assert x_believer._healers_dict == {}
    assert not x_believer._tree_traverse_count
    assert x_believer._rational is False
    assert x_believer._keeps_justified is False
    assert x_believer._keeps_buildable is False
    assert x_believer._sum_healerlink_share == 0
    assert x_believer._offtrack_kids_mass_set == set()
    assert not x_believer._offtrack_fund
    assert x_believer._reason_rcontexts == set()
    assert x_believer._range_inheritors == {}
    print(f"{type(x_believer.planroot)=}") == 0
    assert str(type(x_believer.planroot)).find(".plan.PlanUnit'>") > 0


def test_believerunit_shop_ReturnsObjectWithCorrectEmptyField():
    # ESTABLISH / WHEN
    x_believer = believerunit_shop()

    # THEN
    assert x_believer.believer_name == ""
    assert x_believer.belief_label == root_label()
    assert x_believer.knot == default_knot_if_None()
    assert x_believer.fund_pool == validate_fund_pool()
    assert x_believer.fund_iota == default_fund_iota_if_None()
    assert x_believer.respect_bit == default_RespectBit_if_None()
    assert x_believer.penny == filter_penny()
    assert x_believer.planroot.fund_iota == x_believer.fund_iota
    assert x_believer.planroot.knot == x_believer.knot
    assert x_believer.planroot.root
    assert x_believer.planroot._uid == 1
    assert x_believer.planroot._level == 0
    assert x_believer.planroot.belief_label == x_believer.belief_label
    assert x_believer.planroot.knot == x_believer.knot
    assert x_believer.planroot.parent_rope == ""


def test_BelieverUnit_set_max_tree_traverse_CorrectlySetsInt():
    # ESTABLISH
    zia_str = "Zia"
    zia_believer = believerunit_shop(believer_name=zia_str)
    assert zia_believer.max_tree_traverse == 3

    # WHEN
    zia_believer.set_max_tree_traverse(x_int=11)

    # THEN
    assert zia_believer.max_tree_traverse == 11


def test_BelieverUnit_set_max_tree_traverse_RaisesError_Scenario0():
    # ESTABLISH
    zia_str = "Zia"
    zia_believer = believerunit_shop(believer_name=zia_str)
    assert zia_believer.max_tree_traverse == 3
    zia_tree_traverse = 1

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_believer.set_max_tree_traverse(x_int=zia_tree_traverse)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: '1' must be number that is 2 or greater"
    )


def test_BelieverUnit_set_max_tree_traverse_RaisesError_Scenario1():
    # ESTABLISH
    zia_str = "Zia"
    zia_believer = believerunit_shop(believer_name=zia_str)
    assert zia_believer.max_tree_traverse == 3

    # WHEN / THEN
    zia_tree_traverse = 3.5
    with pytest_raises(Exception) as excinfo:
        zia_believer.set_max_tree_traverse(x_int=zia_tree_traverse)
    assert (
        str(excinfo.value)
        == f"set_max_tree_traverse: '{zia_tree_traverse}' must be number that is 2 or greater"
    )


def test_BelieverUnit_make_rope_ReturnsObj():
    # ESTABLISH
    x_belief_label = "amy45"
    slash_knot = "/"
    sue_str = "Sue"
    sue_believer = believerunit_shop(sue_str, x_belief_label, knot=slash_knot)
    casa_str = "casa"
    v1_casa_rope = sue_believer.make_l1_rope(casa_str)

    # WHEN
    v2_casa_rope = sue_believer.make_l1_rope(casa_str)

    # THEN
    assert v1_casa_rope == v2_casa_rope


def test_BelieverUnit_set_last_pack_id_SetsAttrCorrectly():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue", "Texas")
    assert sue_believer.last_pack_id is None

    # WHEN
    x_last_pack_id = 89
    sue_believer.set_last_pack_id(x_last_pack_id)

    # THEN
    assert sue_believer.last_pack_id == x_last_pack_id


def test_BelieverUnit_set_last_pack_id_RaisesError():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue", "Texas")
    old_last_pack_id = 89
    sue_believer.set_last_pack_id(old_last_pack_id)

    # WHEN / THEN
    new_last_pack_id = 72
    assert new_last_pack_id < old_last_pack_id
    with pytest_raises(Exception) as excinfo:
        sue_believer.set_last_pack_id(new_last_pack_id)
    assert (
        str(excinfo.value)
        == f"Cannot set _last_pack_id to {new_last_pack_id} because it is less than {old_last_pack_id}."
    )


def test_BelieverUnit_del_last_pack_id_SetsAttrCorrectly():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue", "Texas")
    old_last_pack_id = 89
    sue_believer.set_last_pack_id(old_last_pack_id)
    assert sue_believer.last_pack_id is not None

    # WHEN
    sue_believer.del_last_pack_id()

    # WHEN
    assert sue_believer.last_pack_id is None


def test_BelieverUnit_set_fund_pool_CorrectlySetsAttr():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue", "Texas")
    sue_fund_pool = 99000
    assert sue_believer.fund_pool == validate_fund_pool()

    # WHEN
    sue_believer.set_fund_pool(sue_fund_pool)

    # THEN
    assert sue_believer.fund_pool == 99000


def test_BelieverUnit_set_fund_pool_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_str = "Zia"
    zia_believer = believerunit_shop(zia_str)
    x_fund_pool = 23
    zia_believer.set_fund_pool(x_fund_pool)
    assert zia_believer.fund_iota == 1
    assert zia_believer.fund_pool == x_fund_pool

    # WHEN
    new_fund_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_believer.set_fund_pool(new_fund_pool)
    assert (
        str(excinfo.value)
        == f"Believer '{zia_str}' cannot set fund_pool='{new_fund_pool}'. It is not divisible by fund_iota '{zia_believer.fund_iota}'"
    )
