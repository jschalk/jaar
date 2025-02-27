from src.f02_bud.bud import budunit_shop
from src.f05_listen.cell import (
    CellUnit,
    cellunit_shop,
    CELL_NODE_QUOTA_DEFAULT,
    get_cellunit_from_dict,
)
from src.f05_listen.examples.example_listen import (
    example_casa_clean_factunit as clean_factunit,
    example_casa_dirty_factunit as dirty_factunit,
    example_sky_blue_factunit as sky_blue_factunit,
)
from copy import deepcopy as copy_deepcopy


def test_CELL_NODE_QUOTA_DEFAULT_value():
    # ESTABLISH / WHEN / THEN
    assert CELL_NODE_QUOTA_DEFAULT == 1000


def test_CellUnit_Exists():
    # ESTABLISH / WHEN
    x_cellunit = CellUnit()
    # THEN
    assert not x_cellunit.ancestors
    assert not x_cellunit.event_int
    assert not x_cellunit.celldepth
    assert not x_cellunit.deal_owner_name
    assert not x_cellunit.penny
    assert not x_cellunit.quota
    assert not x_cellunit.budadjust
    assert not x_cellunit._reason_bases
    assert not x_cellunit.budevent_facts
    assert not x_cellunit.found_facts
    assert not x_cellunit.boss_facts


def test_cellunit_shop_ReturnsObj_Scenario0_WithoutParameters():
    # ESTABLISH
    bob_str = "Bob"
    # WHEN
    x_cellunit = cellunit_shop(bob_str)
    # THEN
    assert x_cellunit.deal_owner_name == bob_str
    assert x_cellunit.ancestors == []
    assert not x_cellunit.event_int
    assert x_cellunit.celldepth == 0
    assert x_cellunit.penny == 1
    assert x_cellunit.quota == CELL_NODE_QUOTA_DEFAULT
    assert x_cellunit.budadjust.get_dict() == budunit_shop(bob_str).get_dict()
    assert x_cellunit.budevent_facts == {}
    assert x_cellunit._reason_bases == set()
    assert x_cellunit.found_facts == {}
    assert x_cellunit.boss_facts == {}


def test_cellunit_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    bob_sue_ancestors = [bob_str, sue_str]
    bob_sue_event7 = 7
    bob_sue_deal_owner = yao_str
    bob_sue_celldepth3 = 3
    bob_sue_penny2 = 2
    bob_sue_quota300 = 300
    bob_sue_bud = budunit_shop(sue_str)
    bob_sue_bud.add_acctunit(bob_str, 7, 13)
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    bob_sue_budevent_factunits = {clean_fact.base: clean_fact}
    bob_sue_found_factunits = {dirty_fact.base: dirty_fact}
    bob_sue_boss_factunits = {sky_blue_fact.base: sky_blue_fact}

    # WHEN
    x_cellunit = cellunit_shop(
        bob_sue_deal_owner,
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_penny2,
        bob_sue_quota300,
        bob_sue_bud,
        bob_sue_budevent_factunits,
        bob_sue_found_factunits,
        bob_sue_boss_factunits,
    )

    # THEN
    assert x_cellunit.ancestors == bob_sue_ancestors
    assert x_cellunit.event_int == bob_sue_event7
    assert x_cellunit.celldepth == bob_sue_celldepth3
    assert x_cellunit.deal_owner_name == bob_sue_deal_owner
    assert x_cellunit.penny == bob_sue_penny2
    assert x_cellunit.quota == bob_sue_quota300
    assert x_cellunit.budadjust == bob_sue_bud
    assert x_cellunit._reason_bases == set()
    assert x_cellunit.budevent_facts == bob_sue_budevent_factunits
    assert x_cellunit.found_facts == bob_sue_found_factunits
    assert x_cellunit.boss_facts == bob_sue_boss_factunits


def test_cellunit_shop_ReturnsObj_Scenario2_WithReasonBases():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str, "accord23")
    casa_road = sue_bud.make_l1_road("casa")
    mop_road = sue_bud.make_road(casa_road, "mop")
    clean_fact = clean_factunit()
    sue_bud.add_item(clean_factunit().pick)
    sue_bud.add_item(mop_road, pledge=True)
    sue_bud.edit_reason(mop_road, clean_fact.base, clean_fact.pick)

    # WHEN
    x_cellunit = cellunit_shop(sue_str, budadjust=sue_bud)

    # THEN
    assert x_cellunit.deal_owner_name == sue_str
    assert x_cellunit.budadjust == sue_bud
    assert x_cellunit._reason_bases == sue_bud.get_reason_bases()
    assert len(x_cellunit._reason_bases) == 1


def test_cellunit_shop_ReturnsObj_Scenario3_clear_facts():
    # ESTABLISH
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str, "accord23")
    casa_road = sue_bud.make_l1_road("casa")
    mop_road = sue_bud.make_road(casa_road, "mop")
    clean_fact = clean_factunit()
    sue_bud.add_item(clean_factunit().pick)
    sue_bud.add_item(mop_road, pledge=True)
    sue_bud.edit_reason(mop_road, clean_fact.base, clean_fact.pick)
    sue_bud.add_fact(clean_fact.base, clean_fact.pick)
    assert len(sue_bud.get_factunits_dict()) == 1

    # WHEN
    x_cellunit = cellunit_shop(sue_str, budadjust=sue_bud)

    # THEN
    assert len(x_cellunit.budadjust.get_factunits_dict()) == 0
    assert x_cellunit.budadjust != sue_bud


def test_CellUnit_load_budevent_SetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    casa_road = yao_bud.make_l1_road("casa")
    mop_road = yao_bud.make_road(casa_road, "mop")
    clean_fact = clean_factunit()
    yao_bud.add_item(clean_factunit().pick)
    yao_bud.add_item(mop_road, pledge=True)
    yao_bud.edit_reason(mop_road, clean_fact.base, clean_fact.pick)
    yao_bud.add_fact(clean_fact.base, clean_fact.pick, create_missing_items=True)
    yao_cellunit = cellunit_shop(yao_str)
    assert yao_cellunit.budevent_facts == {}

    # WHEN
    yao_cellunit.load_budevent(yao_bud)

    # THEN
    expected_factunits = {clean_fact.base: clean_fact}
    assert yao_cellunit.budevent_facts == expected_factunits
    assert yao_cellunit._reason_bases == yao_bud.get_reason_bases()
    assert len(yao_cellunit._reason_bases) == 1
    expected_adjust_bud = copy_deepcopy(yao_bud)
    expected_adjust_bud.del_fact(clean_fact.base)
    expected_adjust_bud.settle_bud()
    expected_itemroot = expected_adjust_bud.itemroot
    generated_itemroot = yao_cellunit.budadjust.itemroot
    assert yao_cellunit.budadjust.get_dict() != yao_bud.get_dict()
    assert generated_itemroot.get_dict() == expected_itemroot.get_dict()
    assert yao_cellunit.budadjust.get_dict() == expected_adjust_bud.get_dict()


def test_CellUnit_set_found_facts_from_dict_SetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    yao_bud.add_fact(clean_fact.base, clean_fact.pick, create_missing_items=True)
    yao_found_fact_dict = {clean_fact.base: clean_fact.get_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    assert yao_cellunit.found_facts == {}

    # WHEN
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)

    # THEN
    expected_factunits = {clean_fact.base: clean_fact}
    assert yao_cellunit.found_facts == expected_factunits


def test_CellUnit_set_boss_facts_from_found_facts_SetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    clean_fact = clean_factunit()
    yao_bud = budunit_shop(yao_str, "accord23")
    yao_bud.add_fact(clean_fact.base, clean_fact.pick, create_missing_items=True)
    yao_found_fact_dict = {clean_fact.base: clean_fact.get_dict()}
    yao_cellunit = cellunit_shop(yao_str)
    yao_cellunit.set_found_facts_from_dict(yao_found_fact_dict)
    assert len(yao_cellunit.found_facts) == 1
    assert yao_cellunit.boss_facts == {}

    # WHEN
    yao_cellunit.set_boss_facts_from_found_facts()

    # THEN
    assert yao_cellunit.boss_facts == yao_cellunit.found_facts
    yao_cellunit.boss_facts["testing"] = 1
    assert yao_cellunit.boss_facts != yao_cellunit.found_facts


# TODO create tool that clears all facts attributes of facts not connected to reason
