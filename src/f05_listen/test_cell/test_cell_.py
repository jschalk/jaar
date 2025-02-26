from src.f05_listen.cell import CellUnit, cellunit_shop, CELL_NODE_QUOTA_DEFAULT


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
    assert x_cellunit.found_facts is None
    assert x_cellunit.boss_facts is None


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

    # WHEN
    x_cellunit = cellunit_shop(
        bob_sue_ancestors,
        bob_sue_event7,
        bob_sue_celldepth3,
        bob_sue_deal_owner,
        bob_sue_penny2,
        bob_sue_quota300,
    )

    # THEN
    assert x_cellunit.ancestors == bob_sue_ancestors
    assert x_cellunit.event_int == bob_sue_event7
    assert x_cellunit.celldepth == bob_sue_celldepth3
    assert x_cellunit.deal_owner_name == bob_sue_deal_owner
    assert x_cellunit.penny == bob_sue_penny2
    assert x_cellunit.quota == bob_sue_quota300
    assert x_cellunit.budadjust is None
    assert x_cellunit.found_facts is None
    assert x_cellunit.boss_facts is None


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
    assert x_cell_dict.get("found_facts") is None
    assert x_cell_dict.get("boss_facts") is None
