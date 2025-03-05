from src.f00_instrument.file import open_json, save_json
from src.f01_road.deal import quota_str
from src.f05_listen.hub_path import (
    create_cell_json_path,
)
from src.f05_listen.hub_tool import cellunit_add_json_file
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.example_worlds import (
    get_bob_mop_with_reason_budunit_example,
)
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists

# set acct_adjust_ledgers in cell
# run allot_nested_scale to get root allotment
# save root allotment as json
