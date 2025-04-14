from src.a06_bud_logic.bud import budunit_shop
from src.a11_deal_cell_logic.cell import cellunit_shop
from src.f06_listen.hub_path import create_cell_dir_path as cell_dir
from src.f06_listen.hub_tool import cellunit_save_to_dir, cellunit_get_from_dir
from src.f12_world.world import worldunit_shop
from src.f12_world.examples.example_worlds import (
    get_bob_mop_with_reason_budunit_example,
    example_casa_clean_factunit,
    example_casa_dirty_factunit,
)
from src.f12_world.examples.world_env import env_dir_setup_cleanup


def test_WorldUnit_set_cell_tree_decrees_SetsChildCells_Scenario6_boss_facts_ResetAtEachCell(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    mstr_dir = fizz_world._fisc_mstr_dir
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
    bs_yao_cell.eval_budevent(bs_yao_ba)
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
    fizz_world.set_cell_trees_decrees()

    # THEN
    assert cellunit_get_from_dir(bob_root_dir).boss_facts == dirty_facts
    assert cellunit_get_from_dir(bob_sue_dir).boss_facts == {}
    clean_facts = {clean_fact.base: clean_fact}
    assert cellunit_get_from_dir(bob_sue_yao_dir).boss_facts == clean_facts
    assert cellunit_get_from_dir(bob_sue_yao_zia_dir).boss_facts == clean_facts
