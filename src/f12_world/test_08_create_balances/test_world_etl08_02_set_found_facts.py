from src.a01_word_logic.road import create_road
from src.a04_reason_logic.reason_item import factunit_shop
from src.f02_bud.bud import budunit_shop
from src.f06_listen.cell import cellunit_shop
from src.f06_listen.hub_path import create_cell_dir_path as cell_dir
from src.f06_listen.hub_tool import cellunit_save_to_dir, cellunit_get_from_dir
from src.f12_world.world import worldunit_shop
from src.f12_world.examples.world_env import env_dir_setup_cleanup


def test_set_cell_trees_found_facts_ChildNodeWithOneFactIsAssignedToAncestors(
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
    clean_fact = factunit_shop(casa_road, clean_road)
    das = []
    das_y = [yao_str]
    das_ys = [yao_str, sue_str]
    bob5_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das)
    bob5_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das_y)
    bob5_yao_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das_ys)
    bob5_budevent = budunit_shop(bob_str, a23_str)
    bob5_yao_budevent = budunit_shop(yao_str, a23_str)
    bob5_yao_sue_budevent = budunit_shop(sue_str, a23_str)
    bob5_budevent.add_acctunit(yao_str)
    bob5_yao_budevent.add_acctunit(sue_str)
    bob5_yao_sue_budevent.add_acctunit(bob_str)
    bob5_yao_sue_budevent.add_item(clean_fact.pick, 1)
    bob5_yao_sue_budevent.add_fact(clean_fact.base, clean_fact.pick)
    bob5_cell = cellunit_shop(bob_str, das, budadjust=bob5_budevent)
    bob5_yao_cell = cellunit_shop(bob_str, das_y, budadjust=bob5_yao_budevent)
    clean_facts = {clean_fact.base: clean_fact}
    bob5_yao_sue_cell = cellunit_shop(
        bob_str, das_ys, budadjust=bob5_yao_sue_budevent, budevent_facts=clean_facts
    )
    assert bob5_cell.get_budevents_quota_ledger() == {yao_str: 1000}
    assert bob5_yao_cell.get_budevents_quota_ledger() == {sue_str: 1000}
    assert bob5_yao_sue_cell.get_budevents_quota_ledger() == {bob_str: 1000}
    assert bob5_cell.budevent_facts == {}
    assert bob5_yao_cell.budevent_facts == {}
    assert bob5_yao_sue_cell.budevent_facts == clean_facts
    cellunit_save_to_dir(bob5_dir, bob5_cell)
    cellunit_save_to_dir(bob5_yao_dir, bob5_yao_cell)
    cellunit_save_to_dir(bob5_yao_sue_dir, bob5_yao_sue_cell)
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}
    assert cellunit_get_from_dir(bob5_yao_dir).found_facts == {}
    assert cellunit_get_from_dir(bob5_yao_sue_dir).found_facts == {}

    # WHEN
    fizz_world.set_cell_trees_found_facts()

    # THEN
    assert cellunit_get_from_dir(bob5_dir).found_facts == clean_facts
    assert cellunit_get_from_dir(bob5_yao_dir).found_facts == clean_facts
    assert cellunit_get_from_dir(bob5_yao_sue_dir).found_facts == clean_facts
