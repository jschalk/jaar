from src.f00_instrument.file import open_json, save_json
from src.f01_road.road import create_road
from src.f04_gift.atom_config import base_str
from src.f05_listen.hub_path import (
    create_cell_budevent_facts_path as bude_facts_path,
    create_cell_found_facts_path as found_facts_path,
    create_cell_quota_ledger_path as quota_path,
)
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup, get_test_worlds_dir
from os.path import exists as os_path_exists


def test_uphill_deal_node_budevent_facts_Scenario0_RootOnly_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"
    bob_str = "Bob"
    time5 = 5
    das = []
    bob_t5_be_facts_path = bude_facts_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_be_quota_path = quota_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
    be_facts_dict = {}
    save_json(bob_t5_be_facts_path, None, be_facts_dict)
    save_json(bob_t5_be_quota_path, None, {})
    bob_t5_found_path = found_facts_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
    assert os_path_exists(bob_t5_found_path) is False

    # WHEN
    fizz_world.uphill_deal_node_budevent_facts()

    # THEN
    assert os_path_exists(bob_t5_found_path)
    assert open_json(bob_t5_found_path) == {}


def test_uphill_deal_node_budevent_facts_Scenario1_ChildNode_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    mstr_dir = fizz_world._fisc_mstr_dir
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    a23_str = "accord23"
    time5 = 5
    das = []
    das_y = [yao_str]
    das_ys = [yao_str, sue_str]
    bob_t5_bef_path = bude_facts_path(mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_yao_bef_path = bude_facts_path(mstr_dir, a23_str, bob_str, time5, das_y)
    bob_t5_yao_sue_bef_path = bude_facts_path(mstr_dir, a23_str, bob_str, time5, das_ys)
    bob_t5_quota_path = quota_path(mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_yao_quota_path = quota_path(mstr_dir, a23_str, bob_str, time5, das_y)
    bob_t5_yao_sue_quota_path = quota_path(mstr_dir, a23_str, bob_str, time5, das_ys)
    save_json(bob_t5_bef_path, None, {})
    save_json(bob_t5_yao_bef_path, None, {})
    save_json(bob_t5_yao_sue_bef_path, None, {})
    save_json(bob_t5_quota_path, None, {})
    save_json(bob_t5_yao_quota_path, None, {})
    save_json(bob_t5_yao_sue_quota_path, None, {})
    bob_t5_found_path = found_facts_path(mstr_dir, a23_str, bob_str, time5, das)
    assert os_path_exists(bob_t5_found_path) is False

    # WHEN
    fizz_world.uphill_deal_node_budevent_facts()

    # THEN
    assert os_path_exists(bob_t5_found_path)
    assert open_json(bob_t5_found_path) == {}


def test_uphill_deal_node_budevent_facts_Scenario2_ChildNodeWithOneFactIsAssignedToAncestors(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    mstr_dir = fizz_world._fisc_mstr_dir
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    a23_str = "accord23"
    time5 = 5
    casa_road = create_road(a23_str, "casa")
    clean_road = create_road(casa_road, "clean")
    bob_t5_be_facts = {}
    bob_t5_yao_be_facts = {}
    bob_t5_yao_sue_be_facts = {casa_road: {base_str(): casa_road, "pick": clean_road}}
    das = []
    das_y = [yao_str]
    das_ys = [yao_str, sue_str]
    bob_t5_bef_path = bude_facts_path(mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_yao_bef_path = bude_facts_path(mstr_dir, a23_str, bob_str, time5, das_y)
    bob_t5_yao_sue_bef_path = bude_facts_path(mstr_dir, a23_str, bob_str, time5, das_ys)
    bob_t5_quota_path = quota_path(mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_yao_quota_path = quota_path(mstr_dir, a23_str, bob_str, time5, das_y)
    bob_t5_yao_sue_quota_path = quota_path(mstr_dir, a23_str, bob_str, time5, das_ys)
    save_json(bob_t5_bef_path, None, bob_t5_be_facts)
    save_json(bob_t5_yao_bef_path, None, bob_t5_yao_be_facts)
    save_json(bob_t5_yao_sue_bef_path, None, bob_t5_yao_sue_be_facts)
    save_json(bob_t5_quota_path, None, {yao_str: 1})
    save_json(bob_t5_yao_quota_path, None, {sue_str: 1})
    save_json(bob_t5_yao_sue_quota_path, None, {bob_str: 1})
    bob_t5_found = found_facts_path(mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_yao_found = found_facts_path(mstr_dir, a23_str, bob_str, time5, das_y)
    bob_t5_yao_sue_found = found_facts_path(mstr_dir, a23_str, bob_str, time5, das_ys)
    assert os_path_exists(bob_t5_found) is False
    assert os_path_exists(bob_t5_yao_found) is False
    assert os_path_exists(bob_t5_yao_sue_found) is False

    # WHEN
    fizz_world.uphill_deal_node_budevent_facts()

    # THEN
    assert os_path_exists(bob_t5_found)
    assert os_path_exists(bob_t5_yao_found)
    assert os_path_exists(bob_t5_yao_sue_found)
    assert open_json(bob_t5_found) == bob_t5_yao_sue_be_facts
    assert open_json(bob_t5_yao_found) == bob_t5_yao_sue_be_facts
    assert open_json(bob_t5_yao_sue_found) == bob_t5_yao_sue_be_facts
