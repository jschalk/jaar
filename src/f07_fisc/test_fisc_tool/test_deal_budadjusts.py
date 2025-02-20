from src.f00_instrument.file import open_json, save_json, count_dirs_files, save_file
from src.f02_bud.bud import budunit_shop, BudUnit
from src.f05_listen.hub_path import (
    create_budevent_path,
    create_deal_node_budadjust_path as budadjust_path,
    create_deal_node_found_facts_path as found_facts_path,
)
from src.f05_listen.hub_tool import save_arbitrary_dealnode
from src.f07_fisc.fisc_tool import create_deal_node_budadjusts
from src.f07_fisc.examples.fisc_env import env_dir_setup_cleanup, get_test_fisc_mstr_dir
from os.path import exists as os_path_exists


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
    bob_bud.add_item(floor_road)
    bob_bud.add_item(clean_road)
    bob_bud.add_item(dirty_road)
    bob_bud.add_item(mop_road, pledge=True)
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


def get_yao_run_with_reason_budunit_example() -> BudUnit:
    yao_bud = budunit_shop("Yao", "accord23")
    sport_str = "sport"
    participate_str = "participate"
    skiing_str = "skiing"
    running_str = "running"
    weather_str = "weather"
    raining_str = "raining"
    snowing_str = "snowing"
    sport_road = yao_bud.make_l1_road(sport_str)
    participate_road = yao_bud.make_road(sport_road, participate_str)
    skiing_road = yao_bud.make_road(participate_road, skiing_str)
    running_road = yao_bud.make_road(participate_road, running_str)
    weather_road = yao_bud.make_l1_road(weather_str)
    raining_road = yao_bud.make_road(weather_road, raining_str)
    snowing_road = yao_bud.make_road(weather_road, snowing_str)
    yao_bud.add_item(participate_road)
    yao_bud.add_item(skiing_road, pledge=True)
    yao_bud.add_item(running_road, pledge=True)
    yao_bud.add_item(weather_road)
    yao_bud.add_item(raining_road)
    yao_bud.add_item(snowing_road)
    yao_bud.edit_item_attr(
        skiing_road, reason_base=weather_road, reason_premise=snowing_road
    )
    yao_bud.edit_item_attr(
        running_road, reason_base=weather_road, reason_premise=raining_road
    )
    return yao_bud


# create a world with, deal_node.json, found facts and bud events
# for every found_fact change budevent to that fact
# create agenda (different than if found_fact was not applied)
def test_create_budadjusts_SetsFiles_Scenario0_RootOnlyNoFacts(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord"
    tp5 = 5
    bob_str = "Bob"
    das = []
    event7 = 7
    # create deal_node files
    save_arbitrary_dealnode(mstr_dir, a23_str, bob_str, tp5, das, event7)
    # create budevent files
    mop_budunit = get_bob_mop_without_reason_budunit_example()
    bob7_budevent_path = create_budevent_path(mstr_dir, a23_str, bob_str, event7)
    save_file(bob7_budevent_path, None, mop_budunit.get_json())
    # create found_facts files
    bob_tp5_found_facts = {}
    bob_tp5_found = found_facts_path(mstr_dir, a23_str, bob_str, tp5, das)
    save_json(bob_tp5_found, None, bob_tp5_found_facts)
    # create paths for budadjusts
    bob_tp5_budadjust_path = budadjust_path(mstr_dir, a23_str, bob_str, tp5, das)
    assert os_path_exists(bob_tp5_budadjust_path) is False

    # WHEN
    create_deal_node_budadjusts(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob_tp5_budadjust_path)


def test_create_budadjusts_SetsFiles_Scenario1_TwoNodesNoFacts(env_dir_setup_cleanup):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord"
    tp5 = 5
    bob_str = "Bob"
    yao_str = "Yao"
    das = []
    das_yao = [yao_str]
    event7 = 7
    # create deal_node files
    save_arbitrary_dealnode(mstr_dir, a23_str, bob_str, tp5, das, event7)
    save_arbitrary_dealnode(mstr_dir, a23_str, bob_str, tp5, das_yao, event7)
    # create budevent files
    mop_budunit = get_bob_mop_with_reason_budunit_example()
    sport_budunit = get_yao_run_with_reason_budunit_example()
    bob7_budevent_path = create_budevent_path(mstr_dir, a23_str, bob_str, event7)
    yao7_budevent_path = create_budevent_path(mstr_dir, a23_str, yao_str, event7)
    save_file(bob7_budevent_path, None, mop_budunit.get_json())
    save_file(yao7_budevent_path, None, sport_budunit.get_json())
    # create found_facts files
    bob_tp5_found_facts = {}
    bob_tp5_yao_found_facts = {}
    bob_tp5_found = found_facts_path(mstr_dir, a23_str, bob_str, tp5, das)
    bob_tp5_yao_found = found_facts_path(mstr_dir, a23_str, bob_str, tp5, das_yao)
    save_json(bob_tp5_found, None, bob_tp5_found_facts)
    save_json(bob_tp5_yao_found, None, bob_tp5_yao_found_facts)
    # create paths for budadjusts
    bob_tp5_budadjust_path = budadjust_path(mstr_dir, a23_str, bob_str, tp5, das)
    bob_tp5_yao_budadjust_p = budadjust_path(mstr_dir, a23_str, bob_str, tp5, das_yao)
    assert os_path_exists(bob_tp5_budadjust_path) is False
    assert os_path_exists(bob_tp5_yao_budadjust_p) is False

    # WHEN
    create_deal_node_budadjusts(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob_tp5_budadjust_path)
    assert os_path_exists(bob_tp5_yao_budadjust_p)
