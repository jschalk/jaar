from src.f02_bud.bud import budunit_shop, BudUnit
from src.f05_listen.cell import cellunit_shop
from src.f05_listen.hub_path import (
    create_budevent_path,
    create_cell_dir_path as cell_dir,
)
from src.f05_listen.hub_tool import (
    cellunit_save_to_dir,
    cellunit_get_from_dir,
    save_arbitrary_budevent,
)
from src.f07_fisc.fisc_tool import set_deal_trees_decrees, DecreeUnit
from src.f07_fisc.examples.example_fiscs import (
    example_casa_clean_factunit,
    example_casa_dirty_factunit,
)
from src.f07_fisc.examples.fisc_env import env_dir_setup_cleanup, get_test_fisc_mstr_dir


def test_DecreeUnit_Exists():
    # ESTABLISH / WHEN
    x_decreeunit = DecreeUnit()
    # THEN
    assert not x_decreeunit.parent_cell_dir
    assert not x_decreeunit.cell_dir
    assert not x_decreeunit.cell_ancestors
    assert not x_decreeunit.cell_mandate
    assert not x_decreeunit.cell_celldepth
    assert not x_decreeunit.root_cell_bool


def _example_empty_bob_budunit() -> BudUnit:
    a23_str = "accord23"
    return budunit_shop("Bob", a23_str)


def get_bob_mop_without_reason_budunit_example() -> BudUnit:
    bob_bud = _example_empty_bob_budunit()
    casa_str = "casa"
    floor_str = "floor status"
    clean_str = "clean"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_road = bob_bud.make_l1_road(casa_str)
    floor_road = bob_bud.make_road(casa_road, floor_str)
    clean_road = bob_bud.make_road(floor_road, clean_str)
    dirty_road = bob_bud.make_road(floor_road, dirty_str)
    mop_road = bob_bud.make_road(casa_road, mop_str)
    bob_bud.add_item(casa_road, 1)
    bob_bud.add_item(floor_road, 1)
    bob_bud.add_item(clean_road, 1)
    bob_bud.add_item(dirty_road, 1)
    bob_bud.add_item(mop_road, 1, pledge=True)
    return bob_bud


def get_bob_mop_with_reason_budunit_example() -> BudUnit:
    """owner_name: bob, fisc_title: accord23"""
    bob_bud = get_bob_mop_without_reason_budunit_example()
    casa_str = "casa"
    floor_str = "floor status"
    dirty_str = "dirty"
    mop_str = "mop"
    casa_road = bob_bud.make_l1_road(casa_str)
    floor_road = bob_bud.make_road(casa_road, floor_str)
    dirty_road = bob_bud.make_road(floor_road, dirty_str)
    mop_road = bob_bud.make_road(casa_road, mop_str)
    bob_bud.edit_item_attr(mop_road, reason_base=floor_road, reason_premise=dirty_road)
    return bob_bud


def get_bob_mop_fact_clean_budunit_example() -> BudUnit:
    bob_bud = get_bob_mop_with_reason_budunit_example()
    bob_bud.add_acctunit("Bob")
    casa_road = bob_bud.make_l1_road("casa")
    floor_road = bob_bud.make_road(casa_road, "floor status")
    clean_road = bob_bud.make_road(floor_road, "clean")
    bob_bud.add_fact(floor_road, clean_road)
    return bob_bud


def get_yao_run_with_reason_budunit_example() -> BudUnit:
    yao_bud = budunit_shop("Yao", "accord23")
    sport_str = "sport"
    participate_str = "participate"
    ski_str = "skiing"
    run_str = "running"
    weather_str = "weather"
    raining_str = "raining"
    snowing_str = "snowing"
    sport_road = yao_bud.make_l1_road(sport_str)
    participate_road = yao_bud.make_road(sport_road, participate_str)
    ski_road = yao_bud.make_road(participate_road, ski_str)
    run_road = yao_bud.make_road(participate_road, run_str)
    weather_road = yao_bud.make_l1_road(weather_str)
    rain_road = yao_bud.make_road(weather_road, raining_str)
    snow_road = yao_bud.make_road(weather_road, snowing_str)
    yao_bud.add_item(participate_road)
    yao_bud.add_item(ski_road, 5, pledge=True)
    yao_bud.add_item(run_road, 1, pledge=True)
    yao_bud.add_item(weather_road)
    yao_bud.add_item(rain_road)
    yao_bud.add_item(snow_road)
    yao_bud.edit_item_attr(ski_road, reason_base=weather_road, reason_premise=snow_road)
    yao_bud.edit_item_attr(run_road, reason_base=weather_road, reason_premise=rain_road)
    return yao_bud


def get_yao_run_rain_fact_budunit_example() -> BudUnit:
    yao_bud = get_yao_run_with_reason_budunit_example()
    weather_road = yao_bud.make_l1_road("weather")
    rain_road = yao_bud.make_road(weather_road, "raining")
    yao_bud.add_fact(weather_road, rain_road)
    return yao_bud


# create a world with, cell.json, found facts and bud events
# for every found_fact change budevent to that fact
# create agenda (different than if found_fact was not applied)
def test_set_deal_tree_decrees_SetsRootAttr_Scenario0_Depth0NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord"
    tp5 = 5
    bob_str = "Bob"
    das = []
    event7 = 7
    # create cell file
    bob_cell = cellunit_shop(bob_str, [], event7, celldepth=0)
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [])
    bob_bob_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [bob_str])
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_bob_dir, bob_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}

    # WHEN
    set_deal_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}


def test_set_deal_tree_decrees_SetsRootAttr_Scenario1_Depth0AndOne_budevent_fact(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord"
    tp5 = 5
    bob_str = "Bob"
    das = []
    event7 = 7
    bob_budadjust = get_bob_mop_with_reason_budunit_example()
    # create cell file
    clean_fact = example_casa_clean_factunit()
    clean_facts = {clean_fact.base: clean_fact}
    bob_cell = cellunit_shop(
        bob_str, [], event7, 0, budadjust=bob_budadjust, budevent_facts=clean_facts
    )
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [])
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}

    # WHEN
    set_deal_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == clean_facts


def test_set_deal_tree_decrees_SetsRootAttr_Scenario2_Depth0AndOne_found_fact(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord"
    tp5 = 5
    bob_str = "Bob"
    das = []
    event7 = 7
    bob_budadjust = get_bob_mop_with_reason_budunit_example()
    # create cell file
    clean_fact = example_casa_clean_factunit()
    clean_facts = {clean_fact.base: clean_fact}
    bob_cell = cellunit_shop(
        bob_str,
        [],
        event7,
        celldepth=0,
        budadjust=bob_budadjust,
        found_facts=clean_facts,
    )
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [])
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}

    # WHEN
    set_deal_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == clean_facts


def test_set_deal_tree_decrees_SetsChildCells_Scenario3_Depth1AndZero_boss_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"
    tp5 = 5
    bob_str = "Bob"
    sue_str = "Sue"
    bob_ancs = []
    bob_sue_ancs = [sue_str]
    e7 = 7
    bob_budadjust = get_bob_mop_without_reason_budunit_example()
    bob_budadjust.add_acctunit(sue_str, 1)
    bob_sue_budadjust = budunit_shop(sue_str, a23_str)
    # create cell file
    bob_cell = cellunit_shop(
        bob_str, bob_ancs, event_int=e7, celldepth=2, budadjust=bob_budadjust
    )
    bob_sue_cell = cellunit_shop(
        bob_str, bob_sue_ancs, event_int=e7, celldepth=0, budadjust=bob_sue_budadjust
    )
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_sue_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, bob_sue_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}

    # WHEN
    set_deal_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}


def test_set_deal_tree_decrees_SetsChildCells_Scenario3_Depth1And_boss_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"
    tp5 = 5
    bob_str = "Bob"
    sue_str = "Sue"
    bob_ancs = []
    bob_sue_ancs = [sue_str]
    e7 = 7
    bob_budadjust = get_bob_mop_with_reason_budunit_example()
    bob_budadjust.add_acctunit(sue_str, 1)
    bob_sue_budadjust = get_bob_mop_with_reason_budunit_example()
    bob_sue_budadjust.set_owner_name(sue_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.base: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=2,
        budadjust=bob_budadjust,
        budevent_facts=dirty_facts,
    )
    bob_sue_cell = cellunit_shop(
        bob_str, bob_sue_ancs, event_int=e7, celldepth=0, budadjust=bob_sue_budadjust
    )
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_sue_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, bob_sue_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}

    # WHEN
    set_deal_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts


def test_set_deal_tree_decrees_SetsChildCells_Scenario4_Depth3And_boss_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"
    tp5 = 5
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_ancs = []
    b_sue_ancs = [sue_str]
    bs_yao_ancs = [sue_str, yao_str]
    bsy_zia_ancs = [sue_str, yao_str, zia_str]
    e7 = 7
    bob_budadjust = get_bob_mop_with_reason_budunit_example()
    bob_budadjust.add_acctunit(sue_str, 1)
    b_sue_ba = get_bob_mop_with_reason_budunit_example()
    b_sue_ba.set_owner_name(sue_str)
    b_sue_ba.add_acctunit(yao_str, 1)
    bs_yao_ba = get_bob_mop_with_reason_budunit_example()
    bs_yao_ba.set_owner_name(yao_str)
    bs_yao_ba.add_acctunit(zia_str, 1)
    bsy_zia_ba = get_bob_mop_with_reason_budunit_example()
    bsy_zia_ba.set_owner_name(zia_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.base: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=4,
        budadjust=bob_budadjust,
        budevent_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, budadjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, budadjust=bs_yao_ba)
    bsy_zia_cell = cellunit_shop(bob_str, bsy_zia_ancs, e7, 0, budadjust=bsy_zia_ba)
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, b_sue_ancs)
    bob_sue_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bs_yao_ancs)
    bob_sue_yao_zia_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bsy_zia_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
    cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
    cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

    # WHEN
    set_deal_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == dirty_facts


def test_set_deal_tree_decrees_SetsChildCells_Scenario5_Depth2And_boss_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"
    tp5 = 5
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_ancs = []
    b_sue_ancs = [sue_str]
    bs_yao_ancs = [sue_str, yao_str]
    bsy_zia_ancs = [sue_str, yao_str, zia_str]
    e7 = 7
    bob_budadjust = get_bob_mop_with_reason_budunit_example()
    bob_budadjust.add_acctunit(sue_str, 1)
    b_sue_ba = get_bob_mop_with_reason_budunit_example()
    b_sue_ba.set_owner_name(sue_str)
    b_sue_ba.add_acctunit(yao_str, 1)
    bs_yao_ba = get_bob_mop_with_reason_budunit_example()
    bs_yao_ba.set_owner_name(yao_str)
    bs_yao_ba.add_acctunit(zia_str, 1)
    bsy_zia_ba = get_bob_mop_with_reason_budunit_example()
    bsy_zia_ba.set_owner_name(zia_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.base: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=2,
        budadjust=bob_budadjust,
        budevent_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, budadjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, budadjust=bs_yao_ba)
    bsy_zia_cell = cellunit_shop(bob_str, bsy_zia_ancs, e7, 0, budadjust=bsy_zia_ba)
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, b_sue_ancs)
    bob_sue_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bs_yao_ancs)
    bob_sue_yao_zia_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bsy_zia_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
    cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
    cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

    # WHEN
    set_deal_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}


def test_set_deal_tree_decrees_SetsChildCells_Scenario6_boss_facts_ResetAtEachCell(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"
    tp5 = 5
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    zia_str = "Zia"
    bob_ancs = []
    b_sue_ancs = [sue_str]
    bs_yao_ancs = [sue_str, yao_str]
    bsy_zia_ancs = [sue_str, yao_str, zia_str]
    e7 = 7
    bob_budadjust = get_bob_mop_with_reason_budunit_example()
    bob_budadjust.add_acctunit(sue_str, 1)
    b_sue_ba = budunit_shop(sue_str, a23_str)
    b_sue_ba.set_owner_name(sue_str)
    b_sue_ba.add_acctunit(yao_str, 1)
    bs_yao_ba = get_bob_mop_with_reason_budunit_example()
    bs_yao_ba.set_owner_name(yao_str)
    bs_yao_ba.add_acctunit(zia_str, 1)
    clean_fact = example_casa_clean_factunit()
    bs_yao_ba.add_fact(clean_fact.base, clean_fact.pick)
    bsy_zia_ba = get_bob_mop_with_reason_budunit_example()
    bsy_zia_ba.set_owner_name(zia_str)
    # create cell file
    dirty_fact = example_casa_dirty_factunit()
    dirty_facts = {dirty_fact.base: dirty_fact}
    bob_cell = cellunit_shop(
        bob_str,
        bob_ancs,
        event_int=e7,
        celldepth=3,
        budadjust=bob_budadjust,
        budevent_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, budadjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0)
    bs_yao_cell.load_budevent(bs_yao_ba)
    bsy_zia_cell = cellunit_shop(bob_str, bsy_zia_ancs, e7, 0, budadjust=bsy_zia_ba)
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bob_ancs)
    bob_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, b_sue_ancs)
    bob_sue_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bs_yao_ancs)
    bob_sue_yao_zia_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, bsy_zia_ancs)
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_sue_dir, b_sue_cell)
    cellunit_save_to_dir(bob_sue_yao_dir, bs_yao_cell)
    cellunit_save_to_dir(bob_sue_yao_zia_dir, bsy_zia_cell)
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == {}
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == {}

    # WHEN
    set_deal_trees_decrees(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    clean_facts = {clean_fact.base: clean_fact}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == clean_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == clean_facts
