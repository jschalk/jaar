from src.f02_bud.bud import budunit_shop
from src.f05_listen.cell import CellUnit, cellunit_shop, CELL_NODE_QUOTA_DEFAULT
from src.f05_listen.examples.example_listen import (
    example_casa_clean_factunit as clean_factunit,
    example_casa_dirty_factunit as dirty_factunit,
    example_sky_blue_factunit as sky_blue_factunit,
)


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
    assert not x_cellunit.budevent_facts
    assert not x_cellunit.found_facts
    assert not x_cellunit.boss_facts


def test_cellunit_shop_ReturnsObj_Scenario0_WithoutParameters():
    # ESTABLISH / WHEN
    x_cellunit = cellunit_shop()
    # THEN
    assert x_cellunit.ancestors == []
    assert not x_cellunit.event_int
    assert x_cellunit.celldepth == 0
    assert not x_cellunit.deal_owner_name
    assert x_cellunit.penny == 1
    assert x_cellunit.quota == CELL_NODE_QUOTA_DEFAULT
    assert not x_cellunit.budadjust
    assert x_cellunit.budevent_facts == {}
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
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_deal_owner,
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
    assert x_cellunit.budevent_facts == bob_sue_budevent_factunits
    assert x_cellunit.found_facts == bob_sue_found_factunits
    assert x_cellunit.boss_facts == bob_sue_boss_factunits


def test_CellUnit_get_dict_ReturnsObj_Scenario0():
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
    x_cellunit = cellunit_shop(
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_deal_owner,
        bob_sue_penny2,
        bob_sue_quota300,
    )

    # WHEN
    x_cell_dict = x_cellunit.get_dict()

    # THEN
    assert list(x_cell_dict.keys()) == [
        "ancestors",
        "event_int",
        "celldepth",
        "deal_owner_name",
        "penny",
        "quota",
        "budadjust",
        "budevent_facts",
        "found_facts",
        "boss_facts",
    ]
    assert x_cell_dict.get("ancestors") == bob_sue_ancestors
    assert x_cell_dict.get("event_int") == bob_sue_event7
    assert x_cell_dict.get("celldepth") == bob_sue_celldepth3
    assert x_cell_dict.get("deal_owner_name") == bob_sue_deal_owner
    assert x_cell_dict.get("penny") == bob_sue_penny2
    assert x_cell_dict.get("quota") == bob_sue_quota300
    assert x_cell_dict.get("budadjust") is None
    assert x_cell_dict.get("budevent_facts") == {}
    assert x_cell_dict.get("found_facts") == {}
    assert x_cell_dict.get("boss_facts") == {}


def test_CellUnit_get_dict_ReturnsObj_Scenario1_WithMoreParameters():
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
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    bob_sue_budevent_factunits = {clean_fact.base: clean_fact}
    bob_sue_found_factunits = {dirty_fact.base: dirty_fact}
    bob_sue_boss_factunits = {sky_blue_fact.base: sky_blue_fact}
    x_cellunit = cellunit_shop(
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_deal_owner,
        bob_sue_penny2,
        bob_sue_quota300,
        None,
        bob_sue_budevent_factunits,
        bob_sue_found_factunits,
        bob_sue_boss_factunits,
    )

    # WHEN
    x_cell_dict = x_cellunit.get_dict()

    # THEN
    assert list(x_cell_dict.keys()) == [
        "ancestors",
        "event_int",
        "celldepth",
        "deal_owner_name",
        "penny",
        "quota",
        "budadjust",
        "budevent_facts",
        "found_facts",
        "boss_facts",
    ]
    assert x_cell_dict.get("ancestors") == bob_sue_ancestors
    assert x_cell_dict.get("event_int") == bob_sue_event7
    assert x_cell_dict.get("celldepth") == bob_sue_celldepth3
    assert x_cell_dict.get("deal_owner_name") == bob_sue_deal_owner
    assert x_cell_dict.get("penny") == bob_sue_penny2
    assert x_cell_dict.get("quota") == bob_sue_quota300
    assert x_cell_dict.get("budadjust") is None
    bob_sue_budevent_fact_dicts = {clean_fact.base: clean_fact.get_dict()}
    bob_sue_found_fact_dicts = {dirty_fact.base: dirty_fact.get_dict()}
    bob_sue_boss_fact_dicts = {sky_blue_fact.base: sky_blue_fact.get_dict()}
    assert x_cell_dict.get("budevent_facts") == bob_sue_budevent_fact_dicts
    assert x_cell_dict.get("found_facts") == bob_sue_found_fact_dicts
    assert x_cell_dict.get("boss_facts") == bob_sue_boss_fact_dicts
