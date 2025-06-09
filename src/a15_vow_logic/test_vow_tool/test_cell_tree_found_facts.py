from src.a06_plan_logic.plan import planunit_shop
from src.a11_deal_cell_logic.cell import cellunit_shop
from src.a12_hub_tools.hub_path import create_cell_dir_path as cell_dir
from src.a12_hub_tools.hub_tool import cellunit_get_from_dir, cellunit_save_to_dir
from src.a15_vow_logic._test_util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_vow_logic._test_util.example_vows import example_casa_clean_factunit
from src.a15_vow_logic.vow_tool import set_cell_trees_found_facts


def test_set_cell_trees_found_facts_Scenario0_RootOnly_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    a23_str = "accord23"
    time5 = 5
    das = []
    bob5_dir = cell_dir(vow_mstr_dir, a23_str, bob_str, time5, das)
    bob5_cell = cellunit_shop(bob_str, planevent_facts={})
    cellunit_save_to_dir(bob5_dir, bob5_cell)
    assert bob5_cell.get_planevents_quota_ledger() == {}
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}

    # WHEN
    set_cell_trees_found_facts(vow_mstr_dir, a23_str)

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
    cellunit_get_from_dir(bob5_dir).get_planevents_quota_ledger() == {}
    cellunit_get_from_dir(bob5_yao_dir).get_planevents_quota_ledger() == {}
    cellunit_get_from_dir(bob5_yao_sue_dir).get_planevents_quota_ledger() == {}
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
    bob5_planevent = planunit_shop(bob_str, a23_str)
    bob5_yao_planevent = planunit_shop(yao_str, a23_str)
    bob5_yao_sue_planevent = planunit_shop(sue_str, a23_str)
    bob5_planevent.add_acctunit(yao_str)
    bob5_yao_planevent.add_acctunit(sue_str)
    bob5_yao_sue_planevent.add_acctunit(bob_str)
    bob5_yao_sue_planevent.add_concept(clean_fact.fstate, 1)
    bob5_yao_sue_planevent.add_fact(clean_fact.fcontext, clean_fact.fstate)
    bob5_cell = cellunit_shop(bob_str, das, planadjust=bob5_planevent)
    bob5_yao_cell = cellunit_shop(bob_str, das_y, planadjust=bob5_yao_planevent)
    clean_facts = {clean_fact.fcontext: clean_fact}
    bob5_yao_sue_cell = cellunit_shop(
        bob_str, das_ys, planadjust=bob5_yao_sue_planevent, planevent_facts=clean_facts
    )
    assert bob5_cell.get_planevents_quota_ledger() == {yao_str: 1000}
    assert bob5_yao_cell.get_planevents_quota_ledger() == {sue_str: 1000}
    assert bob5_yao_sue_cell.get_planevents_quota_ledger() == {bob_str: 1000}
    assert bob5_cell.planevent_facts == {}
    assert bob5_yao_cell.planevent_facts == {}
    assert bob5_yao_sue_cell.planevent_facts == clean_facts
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
