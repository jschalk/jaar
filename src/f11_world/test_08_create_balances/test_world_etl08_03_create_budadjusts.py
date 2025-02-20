from src.f00_instrument.file import open_json, save_json, count_dirs_files, save_file
from src.f05_listen.hub_path import (
    create_budevent_path,
    create_deal_node_budadjust_path as budadjust_path,
    create_deal_node_found_facts_path as found_facts_path,
)
from src.f05_listen.hub_tool import save_arbitrary_dealnode
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.example_worlds import get_mop_with_reason_budunit_example
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


# create a world with, deal_node.json, found facts and bud events
# for every found_fact change budevent to that fact
# create agenda (different than if found_fact was not applied)
def test_create_budadjusts_SetsFiles_Scenario0_RootOnlyNoFacts(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord"
    tp5 = 5
    bob_str = "Bob"
    das = []
    event7 = 7
    # create deal_node files
    save_arbitrary_dealnode(mstr_dir, a23_str, bob_str, tp5, das, event7)
    mop_budunit = get_mop_with_reason_budunit_example()
    # create budevent files
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
    fizz_world.create_budadjusts_SetsFiles()

    # THEN
    assert os_path_exists(bob_tp5_budadjust_path)
