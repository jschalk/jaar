from src.f00_instrument.dict_toolbox import get_dict_from_json
from src.f00_instrument.file import open_file, save_file, create_path, count_dirs_files
from src.f01_road.deal import time_int_str
from src.f02_bud.bud import budunit_shop
from src.f04_gift.atom_config import fisc_title_str, owner_name_str
from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_owners_dir_path,
    create_episodes_dir_path,
    create_timepoint_dir_path,
    create_fisc_owner_time_csv_path,
    create_fisc_owner_time_json_path,
)
from src.f07_fisc.fisc import fiscunit_shop
from src.f08_pidgin.pidgin_config import event_int_str
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_create_deal_ledger_depth_dir_Scenaro0_DealEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    accord23_str = "accord23"
    fiscs_dir = create_path(fizz_world._fisc_mstr_dir, "fiscals")
    accord23_fisc = fiscunit_shop(accord23_str, fiscs_dir)
    a23_json_path = create_fisc_json_path(fizz_world._fisc_mstr_dir, accord23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    a23_owners_path = create_owners_dir_path(fizz_world._fisc_mstr_dir, accord23_str)
    assert count_dirs_files(a23_owners_path) == 0

    # WHEN
    fizz_world.create_deal_ledger_depth_dir()

    # THEN
    assert count_dirs_files(a23_owners_path) == 0


# def test_WorldUnit_create_deal_ledger_depth_dir_Scenaro1_DealExists(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     fisc_mstr_dir = fizz_world._fisc_mstr_dir
#     a23_str = "accord23"
#     fiscs_dir = create_path(fisc_mstr_dir, "fiscals")
#     accord23_fisc = fiscunit_shop(a23_str, fiscs_dir)
#     bob_str = "Bob"
#     deal1_time_int = 37
#     deal1_magnitude = 450
#     accord23_fisc.add_dealepisode(bob_str, deal1_time_int, deal1_magnitude)
#     a23_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
#     save_file(a23_json_path, None, accord23_fisc.get_json())
#     a23_owners_path = create_owners_dir_path(fisc_mstr_dir, a23_str)
#     a23_bob_episodes_dir = create_episodes_dir_path(fisc_mstr_dir, a23_str, bob_str)
#     deal1_timepoint = create_timepoint_dir_path(
#         fisc_mstr_dir, a23_str, bob_str, deal1_time_int
#     )
#     assert count_dirs_files(a23_owners_path) == 0
#     assert os_path_exists(a23_bob_episodes_dir) is False
#     assert os_path_exists(deal1_timepoint) is False

#     # WHEN
#     fizz_world.create_deal_ledger_depth_dir()

#     # THEN
#     assert os_path_exists(a23_bob_episodes_dir)
#     assert os_path_exists(deal1_timepoint)
#     assert 1 == 2

# bob_str = "Bob"
# sue_str = "Sue"
# event3 = 3
# event7 = 7
# accord23_str = "accord23"
# accord45_str = "accord45"
# timepoint55 = 55
# timepoint66 = 66
# fisc_mstr_dir = fizz_world._fisc_mstr_dir


#     a23_event_time_p = create_fisc_owner_time_csv_path(fisc_mstr_dir, accord23_str)
#     a45_event_time_p = create_fisc_owner_time_csv_path(fisc_mstr_dir, accord45_str)
#     a23_event_time_csv = f"""{fisc_title_str()},{owner_name_str()},{event_int_str()},{time_int_str()},error_message
# {accord23_str},{bob_str},{event3},{timepoint55},
# """
#     a45_event_time_csv = f"""{fisc_title_str()},{owner_name_str()},{event_int_str()},{time_int_str()},error_message
# {accord45_str},{sue_str},{event3},{timepoint55},
# {accord45_str},{sue_str},{event7},{timepoint66},
# """
#     save_file(a23_event_time_p, None, a23_event_time_csv)
#     save_file(a45_event_time_p, None, a45_event_time_csv)
#     assert os_path_exists(a23_event_time_p)
#     assert os_path_exists(a45_event_time_p)
#     a23_event_time_json_path = create_fisc_owner_time_json_path(
#         fisc_mstr_dir, accord23_str
#     )
#     a45_event_time_json_path = create_fisc_owner_time_json_path(
#         fisc_mstr_dir, accord45_str
#     )
#     assert os_path_exists(a23_event_time_json_path) is False
#     assert os_path_exists(a45_event_time_json_path) is False

#     # WHEN
#     fizz_world.fisc_owner_time_agg_csvs2jsons()

#     # THEN
#     assert os_path_exists(a23_event_time_json_path)
#     assert os_path_exists(a45_event_time_json_path)
#     a23_event_time_dict = get_dict_from_json(open_file(a23_event_time_json_path))
#     a45_event_time_dict = get_dict_from_json(open_file(a45_event_time_json_path))
#     assert a23_event_time_dict == {bob_str: {str(event3): timepoint55}}
#     assert a45_event_time_dict == {
#         sue_str: {str(event3): timepoint55, str(event7): timepoint66}
#     }
