from src.f00_instrument.file import save_json, save_file
from src.f05_listen.hub_path import (
    create_budevent_path,
)
from src.f05_listen.hub_tool import cellunit_add_json_file
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.example_worlds import get_mop_with_reason_budunit_example
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


# def test_create_budadjusts_SetsFiles_Scenario0_RootOnlyNoFacts(env_dir_setup_cleanup):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     mstr_dir = fizz_world._fisc_mstr_dir
#     a23_str = "accord"
#     tp5 = 5
#     bob_str = "Bob"
#     das = []
#     event7 = 7
#     # create cell_node files
#     cellunit_add_json_file(mstr_dir, a23_str, bob_str, tp5, event7, das)
#     mop_budunit = get_mop_with_reason_budunit_example()
#     # create budevent files
#     bob7_budevent_path = create_budevent_path(mstr_dir, a23_str, bob_str, event7)
#     save_file(bob7_budevent_path, None, mop_budunit.get_json())
#     # create found_facts files
#     bob5_found_facts = {}
#     save_json(bob5_found, None, bob5_found_facts)
#     # create paths for budadjusts
#     bob5_budadjust_path = budadjust_path(mstr_dir, a23_str, bob_str, tp5, das)
#     # create paths for adjust_ledger_paths
#     bob5_budadjust_path = budadjust_path(mstr_dir, a23_str, bob_str, tp5, das)
#     bob5_adjust_ledger_path = adjust_ledger_path(mstr_dir, a23_str, bob_str, tp5, das)
#     assert os_path_exists(bob5_budadjust_path) is False
#     assert os_path_exists(bob5_adjust_ledger_path) is False

#     # WHEN
#     fizz_world.modify_deal_trees_with_boss_facts()

#     # THEN
#     assert os_path_exists(bob5_budadjust_path)
#     assert os_path_exists(bob5_adjust_ledger_path)


# create a world with, cell_node.json, found facts and bud events
# for every found_fact change budevent to that fact
# create agenda (different than if found_fact was not applied)
# create a budevent such that changing facts changes agenda output

# use graphics_bool to figure out what agenda_ledger output we want to measure
