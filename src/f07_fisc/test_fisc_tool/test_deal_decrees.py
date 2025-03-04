from src.f00_instrument.file import save_json, count_dirs_files, save_file
from src.f02_bud.group import awardlink_shop
from src.f02_bud.bud import budunit_shop, BudUnit
from src.f04_gift.atom_config import base_str
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
from os.path import exists as os_path_exists


def test_DecreeUnit_Exists():
    # ESTABLISH / WHEN
    x_decreeunit = DecreeUnit()
    # THEN
    assert not x_decreeunit.parent_cell_dir
    assert not x_decreeunit.cell_dir
    assert not x_decreeunit.cell_ancestors
    assert not x_decreeunit.cell_mandate
    assert not x_decreeunit.cell_celldepth


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
        celldepth=3,
        budadjust=bob_budadjust,
        budevent_facts=dirty_facts,
    )
    b_sue_cell = cellunit_shop(bob_str, b_sue_ancs, e7, 0, budadjust=b_sue_ba)
    bs_yao_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, budadjust=bs_yao_ba)
    bsy_zia_cell = cellunit_shop(bob_str, bs_yao_ancs, e7, 0, budadjust=bsy_zia_ba)
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


# def test_set_deal_tree_decrees_Scenario0_NoFacts(env_dir_setup_cleanup):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord"
#     tp5 = 5
#     bob_str = "Bob"
#     das = []
#     event7 = 7
#     # create cell file
#     bob_cell = cellunit_shop(bob_str, [], event7, celldepth=0)
#     bob_cell.load_budevent(budunit_shop("Bob", a23_str))
#     bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [])
#     cellunit_save_to_dir(bob_root_dir, bob_cell)
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}

#     # WHEN
#     set_deal_trees_decrees(mstr_dir, a23_str)

#     # THEN
#     assert cellunit_get_from_dir(bob_root_dir).boss_facts == {}


# def test_set_deal_tree_decrees_Scenario0_SetsFilesRootBossFactsCreatedWithBudEventFactsOnly(
# def test_set_deal_tree_decrees_Scenario1_SetsFilesRootBossFactsCreatedWithFoundFactsOnly():
#     assert 1 == 2


# def test_set_deal_tree_decrees_Scenario2_SetsFilesRootBossFactsCreatedWithFoundFactsAndBudEventFacts():
#     assert 1 == 2


# def test_set_deal_trees_decrees_SetsFiles_Scenario0_RootOnlyNoFacts(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord"
#     tp5 = 5
#     bob_str = "Bob"
#     das = []
#     event7 = 7
#     # create cell files
#     cellunit_add_json_file(mstr_dir, a23_str, bob_str, tp5, event7, das)
#     # create budevent files
#     mop_budunit = get_bob_mop_without_reason_budunit_example()
#     bob7_budevent_path = create_budevent_path(mstr_dir, a23_str, bob_str, event7)
#     save_file(bob7_budevent_path, None, mop_budunit.get_json())
#     # create found_facts files
#     bob5_found_facts = {}
#     save_json(bob5_found, None, bob5_found_facts)
#     # create paths for budadjusts
#     bob5_adjust_path = budadjust_path(mstr_dir, a23_str, bob_str, tp5, das)
#     bob5_adjust_ledger_path = adjust_ledger_path(mstr_dir, a23_str, bob_str, tp5, das)
#     assert os_path_exists(bob5_adjust_path) is False
#     assert os_path_exists(bob5_adjust_ledger_path) is False

#     # WHEN
#     set_deal_trees_decrees(mstr_dir, a23_str)

#     # THEN
#     assert os_path_exists(bob5_adjust_path)
#     assert os_path_exists(bob5_adjust_ledger_path)


# # The way acct_agenda_ledgers work is that parent_deal node has it's facts
# #
# def test_set_deal_trees_decrees_SetsFiles_Scenario1_TwoNodesNoFacts(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord"
#     tp5 = 5
#     bob_str = "Bob"
#     yao_str = "Yao"
#     das = []
#     das_yao = [yao_str]
#     event7 = 7
#     # create cell files
#     cellunit_add_json_file(mstr_dir, a23_str, bob_str, tp5, event7, das)
#     cellunit_add_json_file(mstr_dir, a23_str, bob_str, tp5, event7, das_yao)
#     # create budevent files
#     mop_budunit = get_bob_mop_with_reason_budunit_example()
#     sport_budunit = get_yao_run_with_reason_budunit_example()
#     bob7_budevent_path = create_budevent_path(mstr_dir, a23_str, bob_str, event7)
#     yao7_budevent_path = create_budevent_path(mstr_dir, a23_str, yao_str, event7)
#     save_file(bob7_budevent_path, None, mop_budunit.get_json())
#     save_file(yao7_budevent_path, None, sport_budunit.get_json())
#     # create found_facts files
#     bob5_found_facts = {}
#     bob5_yao_found_facts = {}
#     save_json(bob5_found, None, bob5_found_facts)
#     save_json(bob5_yao_found, None, bob5_yao_found_facts)
#     # create paths for budadjusts, acct_agenda_adjust_ledgers
#     bob5_budadjust_path = budadjust_path(mstr_dir, a23_str, bob_str, tp5, das)
#     bob5_yao_budadjust_p = budadjust_path(mstr_dir, a23_str, bob_str, tp5, das_yao)
#     bob5_adjust_ledger = adjust_ledger_path(mstr_dir, a23_str, bob_str, tp5, das)
#     bob5_yao_adjust_ledg = adjust_ledger_path(mstr_dir, a23_str, bob_str, tp5, das_yao)
#     assert os_path_exists(bob5_budadjust_path) is False
#     assert os_path_exists(bob5_yao_budadjust_p) is False
#     assert os_path_exists(bob5_adjust_ledger) is False
#     assert os_path_exists(bob5_yao_adjust_ledg) is False

#     # WHEN
#     set_deal_trees_decrees(mstr_dir, a23_str)

#     # THEN
#     assert os_path_exists(bob5_budadjust_path)
#     assert os_path_exists(bob5_yao_budadjust_p)
#     assert os_path_exists(bob5_adjust_ledger)
#     assert os_path_exists(bob5_yao_adjust_ledg)
#     assert 1 == 2


# def test_set_deal_trees_decrees_SetsFiles_Scenario2_TwoNodesWithFacts(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     a23_str = "accord"
#     tp5 = 5
#     bob_str = "Bob"
#     yao_str = "Yao"
#     das = []
#     das_yao = [yao_str]
#     event7 = 7
#     # create cell files
#     cellunit_add_json_file(mstr_dir, a23_str, bob_str, tp5, event7, das)
#     cellunit_add_json_file(mstr_dir, a23_str, bob_str, tp5, event7, das_yao)
#     # create budevent files
#     bob_mop_budunit = get_bob_mop_fact_clean_budunit_example()
#     yao_run_budunit = get_yao_run_rain_fact_budunit_example()
#     bob7_budevent_path = create_budevent_path(mstr_dir, a23_str, bob_str, event7)
#     yao7_budevent_path = create_budevent_path(mstr_dir, a23_str, yao_str, event7)
#     save_file(bob7_budevent_path, None, bob_mop_budunit.get_json())
#     save_file(yao7_budevent_path, None, yao_run_budunit.get_json())
#     # create found_facts files
#     casa_road = bob_mop_budunit.make_l1_road("casa")
#     floor_road = bob_mop_budunit.make_road(casa_road, "floor status")
#     dirty_road = bob_mop_budunit.make_road(floor_road, "dirty")
#     weather_road = yao_run_budunit.make_l1_road("weather")
#     snow_road = yao_run_budunit.make_road(weather_road, "snowing")
#     bob5_found_facts = {floor_road: {base_str(): floor_road, "pick": dirty_road}}
#     bob5_yao_found_facts = {weather_road: {base_str(): weather_road, "pick": snow_road}}
#     print(f"{bob5_yao_found_path=}")
#     save_json(bob5_found, None, bob5_found_facts)
#     save_json(bob5_yao_found_path, None, bob5_yao_found_facts)
#     # create paths for budadjusts
#     bob5_adjust_path = budadjust_path(mstr_dir, a23_str, bob_str, tp5, das)
#     bob5_yao_adjust_path = budadjust_path(mstr_dir, a23_str, bob_str, tp5, das_yao)
#     bob5_adjust_ledger = adjust_ledger_path(mstr_dir, a23_str, bob_str, tp5, das)
#     bob5_yao_adjust_ledg = adjust_ledger_path(mstr_dir, a23_str, bob_str, tp5, das_yao)
#     assert os_path_exists(bob5_adjust_path) is False
#     assert os_path_exists(bob5_yao_adjust_path) is False
#     assert os_path_exists(bob5_adjust_ledger) is False
#     assert os_path_exists(bob5_yao_adjust_ledg) is False
#     assert bob_mop_budunit.get_factunits_dict() != bob5_found_facts
#     assert yao_run_budunit.get_factunits_dict() != bob5_yao_found_facts

#     # WHEN
#     set_deal_trees_decrees(mstr_dir, a23_str)

#     # THEN
#     assert os_path_exists(bob5_adjust_path)
#     assert os_path_exists(bob5_yao_adjust_path)
#     assert os_path_exists(bob5_adjust_ledger)
#     assert os_path_exists(bob5_yao_adjust_ledg)
#     bob5_budadjust = open_bud_file(bob5_adjust_path)
#     bob5_yao_budadjust = open_bud_file(bob5_yao_adjust_path)
#     print(f"{bob5_yao_budadjust.get_item_dict().keys()=}")
#     print(f"{bob5_yao_budadjust.get_factunits_dict().keys()=}")
#     assert bob5_budadjust.get_factunits_dict() == bob5_found_facts
#     assert bob5_budadjust.get_fact(floor_road).pick == dirty_road
#     assert bob5_yao_budadjust.get_factunits_dict() != {}
#     assert bob5_found_facts == bob5_budadjust.get_factunits_dict()
#     assert bob5_yao_found_facts == bob5_yao_budadjust.get_factunits_dict()
#     assert open_json(bob5_adjust_ledger) == {}
#     assert open_json(bob5_yao_adjust_ledg) == {}


# def test_set_deal_trees_decrees_SetsFiles_Scenario3_Populated_adjust_ledger(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     a23_str = "accord"
#     bob_str = "Bob"
#     yao_str = "Yao"
#     sue_str = "Sue"
#     # create bud with agenda that will having meaning (net distribution of quota>0 for at least 2 accts)
#     bob_mop_budunit = budunit_shop(bob_str, a23_str)
#     bob_mop_budunit.add_acctunit(yao_str)
#     bob_mop_budunit.add_acctunit(sue_str)
#     casa_road = bob_mop_budunit.make_l1_road("casa")
#     floor_road = bob_mop_budunit.make_road(casa_road, "floor status")
#     clean_road = bob_mop_budunit.make_road(floor_road, "clean")
#     dirty_road = bob_mop_budunit.make_road(floor_road, "dirty")
#     mop_road = bob_mop_budunit.make_road(casa_road, "mop")
#     sport_road = bob_mop_budunit.make_l1_road("sport")
#     run_road = bob_mop_budunit.make_road(sport_road, "run")
#     # mop pledge, with reason
#     bob_mop_budunit.add_item(floor_road, 3)
#     bob_mop_budunit.add_item(clean_road, 3)
#     bob_mop_budunit.add_item(dirty_road, 3)
#     bob_mop_budunit.add_item(mop_road, 3, pledge=True)
#     bob_mop_budunit.edit_reason(mop_road, floor_road, dirty_road)
#     bob_mop_budunit.edit_item_attr(mop_road, awardlink=awardlink_shop(yao_str, 5, 3))
#     bob_mop_budunit.edit_item_attr(mop_road, awardlink=awardlink_shop(sue_str, 1, 7))
#     bob_mop_budunit.add_fact(floor_road, clean_road)
#     # run pledge, no reason
#     bob_mop_budunit.add_item(sport_road, 2)
#     bob_mop_budunit.add_item(run_road, 2, pledge=True)
#     bob_mop_budunit.edit_item_attr(run_road, awardlink=awardlink_shop(yao_str, 11, 13))
#     bob_mop_budunit.edit_item_attr(run_road, awardlink=awardlink_shop(sue_str, 17, 29))

#     mstr_dir = get_test_fisc_mstr_dir()
#     tp5 = 5
#     das = []
#     das_yao = [yao_str]
#     event7 = 7
#     quota700 = 70088
#     quota900 = 900
#     # create cell files
#     cellunit_add_json_file(mstr_dir, a23_str, bob_str, tp5, event7, das, quota700)
#     cellunit_add_json_file(mstr_dir, a23_str, bob_str, tp5, event7, das_yao, quota900)
#     # create budevent files
#     bob_mop_budunit
#     yao_run_budunit = get_yao_run_rain_fact_budunit_example()
#     bob7_budevent_path = create_budevent_path(mstr_dir, a23_str, bob_str, event7)
#     yao7_budevent_path = create_budevent_path(mstr_dir, a23_str, yao_str, event7)
#     save_file(bob7_budevent_path, None, bob_mop_budunit.get_json())
#     save_file(yao7_budevent_path, None, yao_run_budunit.get_json())
#     # create found_facts files
#     weather_road = yao_run_budunit.make_l1_road("weather")
#     snow_road = yao_run_budunit.make_road(weather_road, "snowing")
#     bob5_found_facts = {floor_road: {base_str(): floor_road, "pick": dirty_road}}
#     bob5_yao_found_facts = {weather_road: {base_str(): weather_road, "pick": snow_road}}
#     print(f"{bob5_yao_found_path=}")
#     save_json(bob5_found, None, bob5_found_facts)
#     save_json(bob5_yao_found_path, None, bob5_yao_found_facts)
#     # create paths for budadjusts
#     bob5_adjust_path = budadjust_path(mstr_dir, a23_str, bob_str, tp5, das)
#     bob5_yao_adjust_path = budadjust_path(mstr_dir, a23_str, bob_str, tp5, das_yao)
#     bob5_adjust_ledger = adjust_ledger_path(mstr_dir, a23_str, bob_str, tp5, das)
#     bob5_yao_adjust_ledg = adjust_ledger_path(mstr_dir, a23_str, bob_str, tp5, das_yao)
#     assert os_path_exists(bob5_adjust_path) is False
#     assert os_path_exists(bob5_yao_adjust_path) is False
#     assert os_path_exists(bob5_adjust_ledger) is False
#     assert os_path_exists(bob5_yao_adjust_ledg) is False
#     assert bob_mop_budunit.get_factunits_dict() != bob5_found_facts
#     assert yao_run_budunit.get_factunits_dict() != bob5_yao_found_facts

#     # WHEN
#     set_deal_trees_decrees(mstr_dir, a23_str)

#     # THEN
#     assert os_path_exists(bob5_adjust_path)
#     assert os_path_exists(bob5_yao_adjust_path)
#     assert os_path_exists(bob5_adjust_ledger)
#     assert os_path_exists(bob5_yao_adjust_ledg)
#     bob5_budadjust = open_bud_file(bob5_adjust_path)
#     bob5_yao_budadjust = open_bud_file(bob5_yao_adjust_path)
#     print(f"{bob5_yao_budadjust.get_item_dict().keys()=}")
#     print(f"{bob5_yao_budadjust.get_factunits_dict().keys()=}")
#     assert bob5_budadjust.get_factunits_dict() == bob5_found_facts
#     assert bob5_budadjust.get_fact(floor_road).pick == dirty_road
#     assert bob5_yao_budadjust.get_factunits_dict() != {}
#     assert bob5_found_facts == bob5_budadjust.get_factunits_dict()
#     assert bob5_yao_found_facts == bob5_yao_budadjust.get_factunits_dict()
#     assert open_json(bob5_adjust_ledger) == {sue_str: -10124, yao_str: 10124}
#     assert open_json(bob5_yao_adjust_ledg) == {}
