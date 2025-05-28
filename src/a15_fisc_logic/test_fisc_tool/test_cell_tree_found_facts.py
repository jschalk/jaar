from src.a06_bud_logic.bud import budunit_shop
from src.a11_deal_cell_logic.cell import cellunit_shop
from src.a12_hub_tools.hub_path import create_cell_dir_path as cell_dir
from src.a12_hub_tools.hub_tool import cellunit_get_from_dir, cellunit_save_to_dir
from src.a15_fisc_logic.fisc_tool import set_cell_trees_found_facts
from src.a15_fisc_logic._test_util.example_fiscs import example_casa_clean_factunit
from src.a15_fisc_logic._test_util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_set_cell_trees_found_facts_Scenario0_RootOnly_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    a23_str = "accord23"
    time5 = 5
    das = []
    bob5_dir = cell_dir(fisc_mstr_dir, a23_str, bob_str, time5, das)
    bob5_cell = cellunit_shop(bob_str, budevent_facts={})
    cellunit_save_to_dir(bob5_dir, bob5_cell)
    assert bob5_cell.get_budevents_quota_ledger() == {}
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}

    # WHEN
    set_cell_trees_found_facts(fisc_mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}


def test_set_cell_trees_found_facts_Scenario1_ChildNode_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    a23_str = "accord23"
    time5 = 5
    das = []
    das_y = [yao_str]
    das_ys = [yao_str, sue_str]
    bob5_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das)
    bob5_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das_y)
    bob5_yao_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das_ys)
    cellunit_save_to_dir(bob5_dir, cellunit_shop(bob_str, das))
    cellunit_save_to_dir(bob5_yao_dir, cellunit_shop(bob_str, das_y))
    cellunit_save_to_dir(bob5_yao_sue_dir, cellunit_shop(bob_str, das_ys))
    cellunit_get_from_dir(bob5_dir).get_budevents_quota_ledger() == {}
    cellunit_get_from_dir(bob5_yao_dir).get_budevents_quota_ledger() == {}
    cellunit_get_from_dir(bob5_yao_sue_dir).get_budevents_quota_ledger() == {}
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}

    # WHEN
    set_cell_trees_found_facts(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}


def test_set_cell_trees_found_facts_Scenario2_ChildNodeWithOneFactIsAssignedToAncestors(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    a23_str = "accord23"
    time5 = 5
    clean_fact = example_casa_clean_factunit()
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
    bob5_yao_sue_budevent.add_concept(clean_fact.fstate, 1)
    bob5_yao_sue_budevent.add_fact(clean_fact.fcontext, clean_fact.fstate)
    bob5_cell = cellunit_shop(bob_str, das, budadjust=bob5_budevent)
    bob5_yao_cell = cellunit_shop(bob_str, das_y, budadjust=bob5_yao_budevent)
    clean_facts = {clean_fact.fcontext: clean_fact}
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
    set_cell_trees_found_facts(mstr_dir, a23_str)

    # THEN
    assert cellunit_get_from_dir(bob5_dir).found_facts == clean_facts
    assert cellunit_get_from_dir(bob5_yao_dir).found_facts == clean_facts
    assert cellunit_get_from_dir(bob5_yao_sue_dir).found_facts == clean_facts
