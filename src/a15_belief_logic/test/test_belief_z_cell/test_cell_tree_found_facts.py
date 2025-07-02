from src.a06_owner_logic.owner import ownerunit_shop
from src.a11_bud_logic.cell import cellunit_shop
from src.a12_hub_toolbox.hub_path import create_cell_dir_path as cell_dir
from src.a12_hub_toolbox.hub_tool import cellunit_get_from_dir, cellunit_save_to_dir
from src.a15_belief_logic.belief_cell import set_cell_trees_found_facts
from src.a15_belief_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_belief_logic.test._util.example_beliefs import example_casa_clean_factunit


def test_set_cell_trees_found_facts_Scenario0_RootOnly_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    a23_str = "amy23"
    time5 = 5
    das = []
    bob5_dir = cell_dir(belief_mstr_dir, a23_str, bob_str, time5, das)
    bob5_cell = cellunit_shop(bob_str, ownerevent_facts={})
    cellunit_save_to_dir(bob5_dir, bob5_cell)
    assert bob5_cell.get_ownerevents_quota_ledger() == {}
    assert cellunit_get_from_dir(bob5_dir).found_facts == {}

    # WHEN
    set_cell_trees_found_facts(belief_mstr_dir, a23_str)

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
    a23_str = "amy23"
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
    cellunit_get_from_dir(bob5_dir).get_ownerevents_quota_ledger() == {}
    cellunit_get_from_dir(bob5_yao_dir).get_ownerevents_quota_ledger() == {}
    cellunit_get_from_dir(bob5_yao_sue_dir).get_ownerevents_quota_ledger() == {}
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
    a23_str = "amy23"
    time5 = 5
    clean_fact = example_casa_clean_factunit()
    das = []
    das_y = [yao_str]
    das_ys = [yao_str, sue_str]
    bob5_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das)
    bob5_yao_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das_y)
    bob5_yao_sue_dir = cell_dir(mstr_dir, a23_str, bob_str, time5, das_ys)
    bob5_ownerevent = ownerunit_shop(bob_str, a23_str)
    bob5_yao_ownerevent = ownerunit_shop(yao_str, a23_str)
    bob5_yao_sue_ownerevent = ownerunit_shop(sue_str, a23_str)
    bob5_ownerevent.add_acctunit(yao_str)
    bob5_yao_ownerevent.add_acctunit(sue_str)
    bob5_yao_sue_ownerevent.add_acctunit(bob_str)
    bob5_yao_sue_ownerevent.add_plan(clean_fact.fstate, 1)
    bob5_yao_sue_ownerevent.add_fact(clean_fact.fcontext, clean_fact.fstate)
    bob5_cell = cellunit_shop(bob_str, das, owneradjust=bob5_ownerevent)
    bob5_yao_cell = cellunit_shop(bob_str, das_y, owneradjust=bob5_yao_ownerevent)
    clean_facts = {clean_fact.fcontext: clean_fact}
    bob5_yao_sue_cell = cellunit_shop(
        bob_str,
        das_ys,
        owneradjust=bob5_yao_sue_ownerevent,
        ownerevent_facts=clean_facts,
    )
    assert bob5_cell.get_ownerevents_quota_ledger() == {yao_str: 1000}
    assert bob5_yao_cell.get_ownerevents_quota_ledger() == {sue_str: 1000}
    assert bob5_yao_sue_cell.get_ownerevents_quota_ledger() == {bob_str: 1000}
    assert bob5_cell.ownerevent_facts == {}
    assert bob5_yao_cell.ownerevent_facts == {}
    assert bob5_yao_sue_cell.ownerevent_facts == clean_facts
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
