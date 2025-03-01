from src.f00_instrument.file import open_json, save_json
from src.f01_road.road import create_road
from src.f02_bud.reason_item import factunit_shop
from src.f04_gift.atom_config import base_str
from src.f05_listen.cell import cellunit_shop
from src.f05_listen.hub_path import (
    create_cell_dir_path as cell_dir,
    create_cell_quota_ledger_path as quota_path,
)
from src.f05_listen.hub_tool import cellunit_save_to_dir, cellunit_get_from_dir
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup, get_test_worlds_dir
from os.path import exists as os_path_exists


def test_uphill_cell_node_budevent_facts_ChildNodeWithOneFactIsAssignedToAncestors(
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
    clean_fact = factunit_shop(casa_road, clean_road)
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
    save_json(bob_t5_quota_path, None, {yao_str: 1})
    save_json(bob_t5_yao_quota_path, None, {sue_str: 1})
    save_json(bob_t5_yao_sue_quota_path, None, {bob_str: 1})
    assert cellunit_get_from_dir(bob_t5_dir).found_facts == {}
    assert cellunit_get_from_dir(bob_t5_yao_dir).found_facts == {}
    assert cellunit_get_from_dir(bob_t5_yao_sue_dir).found_facts == {}

    # WHEN
    fizz_world.uphill_cell_node_budevent_facts()

    # THEN
    expected_found_facts = {clean_fact.base: clean_fact}
    assert cellunit_get_from_dir(bob_t5_dir).found_facts == expected_found_facts
    assert cellunit_get_from_dir(bob_t5_yao_dir).found_facts == expected_found_facts
    assert cellunit_get_from_dir(bob_t5_yao_sue_dir).found_facts == expected_found_facts
