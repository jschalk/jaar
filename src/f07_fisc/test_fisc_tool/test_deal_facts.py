from src.f00_instrument.file import open_json, save_json
from src.f01_road.road import create_road
from src.f04_gift.atom_config import base_str
from src.f05_listen.cell import cellunit_shop
from src.f05_listen.hub_path import (
    create_cell_dir_path as cell_dir,
    create_cell_found_facts_path as found_facts_path,
    create_cell_quota_ledger_path as quota_path,
)
from src.f05_listen.hub_tool import cellunit_get_from_dir, cellunit_save_to_dir
from src.f07_fisc.fisc_tool import uphill_cell_node_budevent_facts
from src.f07_fisc.examples.example_fiscs import example_casa_clean_factunit
from src.f07_fisc.examples.fisc_env import env_dir_setup_cleanup, get_test_fisc_mstr_dir
from os.path import exists as os_path_exists


def test_uphill_cell_node_budevent_facts_Scenario0_RootOnly_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    bob_str = "Bob"
    a23_str = "accord23"
    time5 = 5
    das = []
    bob_t5_dir = cell_dir(fisc_mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_be_quota_path = quota_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_cell = cellunit_shop(bob_str, budevent_facts={})
    cellunit_save_to_dir(bob_t5_dir, bob_t5_cell)
    save_json(bob_t5_be_quota_path, None, {})
    bob_t5_found_path = found_facts_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
    assert os_path_exists(bob_t5_found_path) is False

    # WHEN
    uphill_cell_node_budevent_facts(fisc_mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob_t5_found_path)
    assert open_json(bob_t5_found_path) == {}


def test_uphill_cell_node_budevent_facts_Scenario1_ChildNode_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    a23_str = "accord23"
    time5 = 5
    das = []
    das_y = [yao_str]
    das_ys = [yao_str, sue_str]
    bob_t5_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das_y)
    bob_t5_yao_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das_ys)
    bob_t5_quota_path = quota_path(mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_yao_quota_path = quota_path(mstr_dir, a23_str, bob_str, time5, das_y)
    bob_t5_yao_sue_quota_path = quota_path(mstr_dir, a23_str, bob_str, time5, das_ys)
    cellunit_save_to_dir(bob_t5_dir, cellunit_shop(bob_str, das))
    cellunit_save_to_dir(bob_t5_yao_dir, cellunit_shop(bob_str, das_y))
    cellunit_save_to_dir(bob_t5_yao_sue_dir, cellunit_shop(bob_str, das_ys))
    save_json(bob_t5_quota_path, None, {})
    save_json(bob_t5_yao_quota_path, None, {})
    save_json(bob_t5_yao_sue_quota_path, None, {})
    bob_t5_found_path = found_facts_path(mstr_dir, a23_str, bob_str, time5, das)
    assert os_path_exists(bob_t5_found_path) is False

    # WHEN
    uphill_cell_node_budevent_facts(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob_t5_found_path)
    assert open_json(bob_t5_found_path) == {}


def test_uphill_cell_node_budevent_facts_Scenario2_ChildNodeWithOneFactIsAssignedToAncestors(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    a23_str = "accord23"
    time5 = 5
    casa_road = create_road(a23_str, "casa")
    clean_road = create_road(casa_road, "clean")
    bob_t5_be_facts = {}
    bob_t5_yao_be_facts = {}
    # bob_t5_yao_sue_be_facts = {casa_road: {base_str(): casa_road, "pick": clean_road}}
    clean_fact = example_casa_clean_factunit()
    bob_t5_yao_sue_be_facts = {clean_fact.base: clean_fact}
    das = []
    das_y = [yao_str]
    das_ys = [yao_str, sue_str]
    bob_t5_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das_y)
    bob_t5_yao_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das_ys)
    bob_t5_quota_path = quota_path(mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_yao_quota_path = quota_path(mstr_dir, a23_str, bob_str, time5, das_y)
    bob_t5_yao_sue_quota_path = quota_path(mstr_dir, a23_str, bob_str, time5, das_ys)
    bob_t5_cell = cellunit_shop(bob_str, das, budevent_facts=bob_t5_be_facts)
    bob_t5_yao_cell = cellunit_shop(bob_str, das_y, budevent_facts=bob_t5_yao_be_facts)
    bob_t5_yao_sue_cell = cellunit_shop(
        bob_str, das_ys, budevent_facts=bob_t5_yao_sue_be_facts
    )
    cellunit_save_to_dir(bob_t5_dir, bob_t5_cell)
    cellunit_save_to_dir(bob_t5_yao_dir, bob_t5_yao_cell)
    cellunit_save_to_dir(bob_t5_yao_sue_dir, bob_t5_yao_sue_cell)
    # save_json(bob_t5_dir, None, bob_t5_be_facts)
    # save_json(bob_t5_yao_dir, None, bob_t5_yao_be_facts)
    # save_json(bob_t5_yao_sue_dir, None, bob_t5_yao_sue_be_facts)
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
    uphill_cell_node_budevent_facts(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob_t5_found)
    assert os_path_exists(bob_t5_yao_found)
    assert os_path_exists(bob_t5_yao_sue_found)
    expected_found_facts = {clean_fact.base: clean_fact.get_dict()}
    assert open_json(bob_t5_found) == expected_found_facts
    assert open_json(bob_t5_yao_found) == expected_found_facts
    assert open_json(bob_t5_yao_sue_found) == expected_found_facts
