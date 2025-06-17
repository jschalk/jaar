from pytest import raises as pytest_raises
from src.a01_term_logic.rope import default_knot_if_None
from src.a02_finance_logic._util.a02_str import (
    fund_pool_str,
    knot_str,
    owner_name_str,
    vow_label_str,
)
from src.a02_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
    validate_fund_pool,
    validate_respect_num,
)
from src.a05_concept_logic.concept import get_default_vow_label as root_label
from src.a06_plan_logic._util.a06_str import (
    _keeps_buildable_str,
    _keeps_justified_str,
    _offtrack_fund_str,
    _offtrack_kids_mass_set_str,
    _rational_str,
    _reason_rcontexts_str,
    _sum_healerlink_share_str,
    _tree_traverse_count_str,
    credor_respect_str,
    debtor_respect_str,
    fund_iota_str,
    last_pack_id_str,
    max_tree_traverse_str,
    penny_str,
    respect_bit_str,
    tally_str,
)
from src.a06_plan_logic.plan import PlanUnit, planunit_shop


def test_PlanUnit_Exists():
    # ESTABLISH /  WHEN
    x_plan = PlanUnit()

    # THEN
    assert x_plan
    assert x_plan.vow_label is None
    assert x_plan.owner_name is None
    assert x_plan.tally is None
    assert x_plan.accts is None
    assert x_plan.conceptroot is None
    assert x_plan.credor_respect is None
    assert x_plan.debtor_respect is None
    assert x_plan.max_tree_traverse is None
    assert x_plan.knot is None
    assert x_plan.fund_pool is None
    assert x_plan.fund_iota is None
    assert x_plan.respect_bit is None
    assert x_plan.penny is None
    assert x_plan.last_pack_id is None
    # calculated attr
    assert x_plan._concept_dict is None
    assert x_plan._keep_dict is None
    assert x_plan._healers_dict is None
    assert x_plan._tree_traverse_count is None
    assert x_plan._rational is None
    assert x_plan._keeps_justified is None
    assert x_plan._keeps_buildable is None
    assert x_plan._sum_healerlink_share is None
    assert x_plan._offtrack_kids_mass_set is None
    assert x_plan._offtrack_fund is None
    assert x_plan._reason_rcontexts is None
    assert x_plan._range_inheritors is None
    assert str(type(x_plan.conceptroot)).find("None") == 8
    obj_attrs = set(x_plan.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        "_concept_dict",
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
        "accts",
        knot_str(),
        "conceptroot",
        credor_respect_str(),
        debtor_respect_str(),
        "_groupunits",
        vow_label_str(),
        fund_iota_str(),
        fund_pool_str(),
        last_pack_id_str(),
        max_tree_traverse_str(),
        owner_name_str(),
        penny_str(),
        respect_bit_str(),
        tally_str(),
    }


def test_planunit_shop_ReturnsObjectWithFilledFields():
    # ESTABLISH
    sue_str = "Sue"
    iowa_vow_label = "Iowa"
    slash_knot = "/"
    x_fund_pool = 555
    x_fund_iota = 7
    x_respect_bit = 5
    x_penny = 1

    # WHEN
    x_plan = planunit_shop(
        owner_name=sue_str,
        vow_label=iowa_vow_label,
        knot=slash_knot,
        fund_pool=x_fund_pool,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )

    # THEN
    assert x_plan
    assert x_plan.owner_name == sue_str
    assert x_plan.vow_label == iowa_vow_label
    assert x_plan.tally == 1
    assert x_plan.accts == {}
    assert x_plan.conceptroot is not None
    assert x_plan.max_tree_traverse == 3
    assert x_plan.knot == slash_knot
    assert x_plan.fund_pool == x_fund_pool
    assert x_plan.fund_iota == x_fund_iota
    assert x_plan.respect_bit == x_respect_bit
    assert x_plan.penny == x_penny
    assert x_plan.credor_respect == validate_respect_num()
    assert x_plan.debtor_respect == validate_respect_num()
    assert not x_plan.last_pack_id
    # calculated attr
    assert x_plan._concept_dict == {}
    assert x_plan._keep_dict == {}
    assert x_plan._healers_dict == {}
    assert not x_plan._tree_traverse_count
    assert x_plan._rational is False
    assert x_plan._keeps_justified is False
    assert x_plan._keeps_buildable is False
    assert x_plan._sum_healerlink_share == 0
    assert x_plan._offtrack_kids_mass_set == set()
    assert not x_plan._offtrack_fund
    assert x_plan._reason_rcontexts == set()
    assert x_plan._range_inheritors == {}
    print(f"{type(x_plan.conceptroot)=}") == 0
    assert str(type(x_plan.conceptroot)).find(".concept.ConceptUnit'>") > 0


def test_planunit_shop_ReturnsObjectWithCorrectEmptyField():
    # ESTABLISH / WHEN
    x_plan = planunit_shop()

    # THEN
    assert x_plan.owner_name == ""
    assert x_plan.vow_label == root_label()
    assert x_plan.knot == default_knot_if_None()
    assert x_plan.fund_pool == validate_fund_pool()
    assert x_plan.fund_iota == default_fund_iota_if_None()
    assert x_plan.respect_bit == default_RespectBit_if_None()
    assert x_plan.penny == filter_penny()
    assert x_plan.conceptroot.fund_iota == x_plan.fund_iota
    assert x_plan.conceptroot.knot == x_plan.knot
    assert x_plan.conceptroot.root
    assert x_plan.conceptroot._uid == 1
    assert x_plan.conceptroot._level == 0
    assert x_plan.conceptroot.vow_label == x_plan.vow_label
    assert x_plan.conceptroot.knot == x_plan.knot
    assert x_plan.conceptroot.parent_rope == ""


def test_PlanUnit_set_max_tree_traverse_CorrectlySetsInt():
    # ESTABLISH
    zia_str = "Zia"
    zia_plan = planunit_shop(owner_name=zia_str)
    assert zia_plan.max_tree_traverse == 3

    # WHEN
    zia_plan.set_max_tree_traverse(x_int=11)

    # THEN
    assert zia_plan.max_tree_traverse == 11


def test_PlanUnit_set_max_tree_traverse_CorrectlyRaisesError():
    # ESTABLISH
    zia_str = "Zia"
    zia_plan = planunit_shop(owner_name=zia_str)
    assert zia_plan.max_tree_traverse == 3
    zia_tree_traverse = 1

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_max_tree_traverse(x_int=zia_tree_traverse)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: '1' must be number that is 2 or greater"
    )


def test_PlanUnit_set_max_tree_traverse_CorrectlyRaisesError():
    # ESTABLISH
    zia_str = "Zia"
    zia_plan = planunit_shop(owner_name=zia_str)
    assert zia_plan.max_tree_traverse == 3

    # WHEN / THEN
    zia_tree_traverse = 3.5
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_max_tree_traverse(x_int=zia_tree_traverse)
    assert (
        str(excinfo.value)
        == f"set_max_tree_traverse: '{zia_tree_traverse}' must be number that is 2 or greater"
    )


def test_PlanUnit_make_rope_ReturnsObj():
    # ESTABLISH
    x_vow_label = "accord45"
    slash_knot = "/"
    sue_str = "Sue"
    sue_plan = planunit_shop(sue_str, x_vow_label, knot=slash_knot)
    casa_str = "casa"
    v1_casa_rope = sue_plan.make_l1_rope(casa_str)

    # WHEN
    v2_casa_rope = sue_plan.make_l1_rope(casa_str)

    # THEN
    assert v1_casa_rope == v2_casa_rope


def test_PlanUnit_set_last_pack_id_SetsAttrCorrectly():
    # ESTABLISH
    sue_plan = planunit_shop("Sue", "Texas")
    assert sue_plan.last_pack_id is None

    # WHEN
    x_last_pack_id = 89
    sue_plan.set_last_pack_id(x_last_pack_id)

    # THEN
    assert sue_plan.last_pack_id == x_last_pack_id


def test_PlanUnit_set_last_pack_id_RaisesError():
    # ESTABLISH
    sue_plan = planunit_shop("Sue", "Texas")
    old_last_pack_id = 89
    sue_plan.set_last_pack_id(old_last_pack_id)

    # WHEN / THEN
    new_last_pack_id = 72
    assert new_last_pack_id < old_last_pack_id
    with pytest_raises(Exception) as excinfo:
        sue_plan.set_last_pack_id(new_last_pack_id)
    assert (
        str(excinfo.value)
        == f"Cannot set _last_pack_id to {new_last_pack_id} because it is less than {old_last_pack_id}."
    )


def test_PlanUnit_del_last_pack_id_SetsAttrCorrectly():
    # ESTABLISH
    sue_plan = planunit_shop("Sue", "Texas")
    old_last_pack_id = 89
    sue_plan.set_last_pack_id(old_last_pack_id)
    assert sue_plan.last_pack_id is not None

    # WHEN
    sue_plan.del_last_pack_id()

    # WHEN
    assert sue_plan.last_pack_id is None


def test_PlanUnit_set_fund_pool_CorrectlySetsAttr():
    # ESTABLISH
    sue_plan = planunit_shop("Sue", "Texas")
    sue_fund_pool = 99000
    assert sue_plan.fund_pool == validate_fund_pool()

    # WHEN
    sue_plan.set_fund_pool(sue_fund_pool)

    # THEN
    assert sue_plan.fund_pool == 99000


def test_PlanUnit_set_fund_pool_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_str = "Zia"
    zia_plan = planunit_shop(zia_str)
    x_fund_pool = 23
    zia_plan.set_fund_pool(x_fund_pool)
    assert zia_plan.fund_iota == 1
    assert zia_plan.fund_pool == x_fund_pool

    # WHEN
    new_fund_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_plan.set_fund_pool(new_fund_pool)
    assert (
        str(excinfo.value)
        == f"Plan '{zia_str}' cannot set fund_pool='{new_fund_pool}'. It is not divisible by fund_iota '{zia_plan.fund_iota}'"
    )
