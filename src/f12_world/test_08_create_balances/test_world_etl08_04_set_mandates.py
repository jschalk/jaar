from src.f00_data_toolboxs.file_toolbox import open_json
from src.f06_listen.cell import cellunit_shop
from src.f06_listen.hub_path import (
    create_cell_dir_path as cell_dir,
    create_cell_acct_mandate_ledger_path as mandate_path,
)
from src.f06_listen.hub_tool import cellunit_save_to_dir
from src.f12_world.world import worldunit_shop
from src.f12_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_set_cell_tree_cell_mandates_SetsRootAttr_Scenario0_Depth0NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord"
    tp5 = 5
    bob_str = "Bob"
    das = []
    event7 = 7
    # create cell file
    bob_cell = cellunit_shop(bob_str, [], event7, celldepth=0)
    bob_root_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [])
    bob_bob_dir = cell_dir(mstr_dir, a23_str, bob_str, tp5, [bob_str])
    cellunit_save_to_dir(bob_root_dir, bob_cell)
    cellunit_save_to_dir(bob_bob_dir, bob_cell)
    bob_root_mandate_path = mandate_path(mstr_dir, a23_str, bob_str, tp5, [])
    bob_bob_mandate_path = mandate_path(mstr_dir, a23_str, bob_str, tp5, [bob_str])
    assert os_path_exists(bob_root_mandate_path) is False
    assert os_path_exists(bob_bob_mandate_path) is False

    # WHEN
    fizz_world.set_cell_tree_cell_mandates()

    # THEN
    assert os_path_exists(bob_root_mandate_path)
    assert os_path_exists(bob_bob_mandate_path)
    assert open_json(bob_root_mandate_path) == {bob_str: 1000}
    assert open_json(bob_bob_mandate_path) == {bob_str: 1000}
