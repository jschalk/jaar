from src.f02_bud.bud import budunit_shop
from src.f05_listen.cell import cellunit_shop, cellunit_get_from_dict
from src.f05_listen.examples.example_listen import (
    example_casa_clean_factunit as clean_factunit,
    example_casa_dirty_factunit as dirty_factunit,
    example_sky_blue_factunit as sky_blue_factunit,
)


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
    bob_sue_mandate444 = 444
    x_cellunit = cellunit_shop(
        bob_sue_deal_owner,
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_penny2,
        bob_sue_quota300,
        mandate=bob_sue_mandate444,
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
        "mandate",
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
    assert x_cell_dict.get("mandate") == bob_sue_mandate444
    bob_sue_bud = budunit_shop(bob_sue_deal_owner)
    assert x_cell_dict.get("budadjust") == bob_sue_bud.get_dict()
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
    bob_sue_mandate444 = 444
    clean_fact = clean_factunit()
    dirty_fact = dirty_factunit()
    sky_blue_fact = sky_blue_factunit()
    bob_sue_budevent_factunits = {clean_fact.base: clean_fact}
    bob_sue_found_factunits = {dirty_fact.base: dirty_fact}
    bob_sue_boss_factunits = {sky_blue_fact.base: sky_blue_fact}
    x_cellunit = cellunit_shop(
        bob_sue_deal_owner,
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_penny2,
        bob_sue_quota300,
        None,
        bob_sue_budevent_factunits,
        bob_sue_found_factunits,
        bob_sue_boss_factunits,
        mandate=bob_sue_mandate444,
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
        "mandate",
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
    assert x_cell_dict.get("mandate") == bob_sue_mandate444
    assert x_cell_dict.get("budadjust") == budunit_shop(bob_sue_deal_owner).get_dict()
    bob_sue_budevent_fact_dicts = {clean_fact.base: clean_fact.get_dict()}
    bob_sue_found_fact_dicts = {dirty_fact.base: dirty_fact.get_dict()}
    bob_sue_boss_fact_dicts = {sky_blue_fact.base: sky_blue_fact.get_dict()}
    assert x_cell_dict.get("budevent_facts") == bob_sue_budevent_fact_dicts
    assert x_cell_dict.get("found_facts") == bob_sue_found_fact_dicts
    assert x_cell_dict.get("boss_facts") == bob_sue_boss_fact_dicts
    assert len(x_cell_dict) == 11


def test_CellUnit_get_json_ReturnsObj():
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
    bob_sue_bud = budunit_shop(bob_sue_deal_owner)
    bob_sue_bud.add_acctunit(sue_str)
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

    # WHEN
    x_cell_json = x_cellunit.get_json()

    # THEN
    assert len(x_cell_json) == 1254


def test_cellunit_get_from_dict_ReturnsObj_Scenario0_NoParameters():
    # ESTABLISH
    yao_str = "Yao"
    x_dict = {"deal_owner_name": yao_str}

    # WHEN
    gen_cellunit = cellunit_get_from_dict(x_dict)

    # THEN
    assert gen_cellunit == cellunit_shop(yao_str)


def test_cellunit_get_from_dict_ReturnsObj_Scenario1():
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
    bob_sue_bud = budunit_shop(bob_sue_deal_owner)
    bob_sue_bud.add_acctunit(sue_str)
    bob_sue_cellunit = cellunit_shop(
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
    x_cell_dict = bob_sue_cellunit.get_dict()

    # WHEN
    gen_cellunit = cellunit_get_from_dict(x_cell_dict)

    # THEN
    assert gen_cellunit == bob_sue_cellunit
