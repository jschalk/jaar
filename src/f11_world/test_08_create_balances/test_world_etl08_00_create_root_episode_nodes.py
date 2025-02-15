from src.f00_instrument.file import save_file, open_json, save_json, count_dirs_files
from src.f01_road.deal import (
    ledger_depth_str,
    owner_name_str,
    quota_str,
    DEFAULT_DEPTH_LEDGER,
)
from src.f04_gift.atom_config import event_int_str, penny_str
from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_owners_dir_path,
    create_episode_node_state_path,
    create_fisc_ote1_json_path,
)
from src.f07_fisc.fisc import fiscunit_shop
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_create_root_episode_nodes_Scenaro0_DealEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    accord23_str = "accord23"
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    accord23_fisc = fiscunit_shop(accord23_str, fisc_mstr_dir)
    a23_json_path = create_fisc_json_path(fizz_world._fisc_mstr_dir, accord23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    print(f"{a23_json_path=}")
    a23_owners_path = create_owners_dir_path(fizz_world._fisc_mstr_dir, accord23_str)
    assert count_dirs_files(a23_owners_path) == 0

    # WHEN
    fizz_world.create_root_episode_nodes()

    # THEN
    assert count_dirs_files(a23_owners_path) == 0


def test_WorldUnit_create_root_episode_nodes_Scenaro1_DealExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"

    # Create FiscUnit with bob deal at time 37
    accord23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    bob_str = "Bob"
    timepoint37 = 37
    deal1_quota = 450
    accord23_fisc.add_dealepisode(bob_str, timepoint37, deal1_quota)
    a23_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    assert os_path_exists(a23_json_path)

    # Create event time mapping owner_time_agg for time 37
    event3 = 3
    event7 = 7
    timepoint66 = 66
    a23_ote1_dict = {bob_str: {str(timepoint37): event3, str(timepoint66): event7}}
    a23_ote1_json_path = create_fisc_ote1_json_path(fisc_mstr_dir, a23_str)
    print(f"{a23_ote1_json_path=}")
    save_json(a23_ote1_json_path, None, a23_ote1_dict)
    assert os_path_exists(a23_ote1_json_path)

    # timepoint37 episode_node path
    tp37_episode_node_json_path = create_episode_node_state_path(
        fisc_mstr_dir, a23_str, bob_str, timepoint37
    )
    assert os_path_exists(tp37_episode_node_json_path) is False

    # WHEN
    fizz_world.create_root_episode_nodes()

    # THEN
    assert os_path_exists(tp37_episode_node_json_path)
    ledger_state_dict = open_json(tp37_episode_node_json_path)
    print(f"{ledger_state_dict=}")
    assert ledger_state_dict.get(ledger_depth_str()) == DEFAULT_DEPTH_LEDGER
    assert ledger_state_dict.get(owner_name_str()) == bob_str
    assert ledger_state_dict.get(quota_str()) == deal1_quota
    assert ledger_state_dict.get(event_int_str()) == event3


def test_WorldUnit_create_root_episode_nodes_Scenaro2_DealExistsButNoBudExistsInEventsPast(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"

    # Create FiscUnit with bob deal at time 37
    accord23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    bob_str = "Bob"
    timepoint37 = 37
    deal1_quota = 450
    accord23_fisc.add_dealepisode(bob_str, timepoint37, deal1_quota)
    a23_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    assert os_path_exists(a23_json_path)

    # Create event time mapping owner_time_agg for time 37
    event3 = 3
    event7 = 7
    timepoint40 = 40
    timepoint66 = 66
    a23_ote1_dict = {bob_str: {str(timepoint40): event3, str(timepoint66): event7}}
    a23_ote1_json_path = create_fisc_ote1_json_path(fisc_mstr_dir, a23_str)
    print(f"{a23_ote1_json_path=}")
    save_json(a23_ote1_json_path, None, a23_ote1_dict)
    assert os_path_exists(a23_ote1_json_path)
    tp37_episode_node_json_path = create_episode_node_state_path(
        fisc_mstr_dir, a23_str, bob_str, timepoint37
    )
    assert os_path_exists(tp37_episode_node_json_path) is False

    # WHEN
    fizz_world.create_root_episode_nodes()

    # THEN
    assert os_path_exists(tp37_episode_node_json_path)
    ledger_state_dict = open_json(tp37_episode_node_json_path)
    print(f"{ledger_state_dict=}")
    assert ledger_state_dict.get(ledger_depth_str()) == DEFAULT_DEPTH_LEDGER
    assert ledger_state_dict.get(owner_name_str()) == bob_str
    assert ledger_state_dict.get(quota_str()) == deal1_quota
    assert not ledger_state_dict.get(event_int_str())


def test_WorldUnit_create_root_episode_nodes_Scenaro3_DealExistsNotPerfectMatch_time_int_event_int(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"
    a23_penny = 2

    # Create FiscUnit with bob deal at time 37
    accord23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir, penny=a23_penny)
    print(f"{accord23_fisc.penny=}")
    bob_str = "Bob"
    timepoint37 = 37
    deal1_quota = 450
    deal1_ledger_depth = 3
    accord23_fisc.add_dealepisode(
        bob_str, timepoint37, deal1_quota, ledger_depth=deal1_ledger_depth
    )
    a23_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    assert os_path_exists(a23_json_path)

    # Create event time mapping owner_time_agg for time 37
    event3 = 3
    event7 = 7
    timepoint30 = 30
    timepoint66 = 66
    a23_ote1_dict = {bob_str: {str(timepoint30): event3, str(timepoint66): event7}}
    a23_ote1_json_path = create_fisc_ote1_json_path(fisc_mstr_dir, a23_str)
    print(f"{a23_ote1_json_path=}")
    save_json(a23_ote1_json_path, None, a23_ote1_dict)
    assert os_path_exists(a23_ote1_json_path)

    # destination of episode_node json
    tp37_episode_node_json_path = create_episode_node_state_path(
        fisc_mstr_dir, a23_str, bob_str, timepoint37
    )
    assert os_path_exists(tp37_episode_node_json_path) is False

    # WHEN
    fizz_world.create_root_episode_nodes()

    # THEN
    assert os_path_exists(tp37_episode_node_json_path)
    ledger_state_dict = open_json(tp37_episode_node_json_path)
    assert ledger_state_dict.get(ledger_depth_str()) == deal1_ledger_depth
    assert ledger_state_dict.get(owner_name_str()) == bob_str
    assert ledger_state_dict.get(quota_str()) == deal1_quota
    assert ledger_state_dict.get(event_int_str()) == event3
    assert ledger_state_dict.get(penny_str()) == a23_penny
    print(ledger_state_dict.get("ancestor"))
    assert not ledger_state_dict.get("ancestor")
    assert len(ledger_state_dict) == 6
