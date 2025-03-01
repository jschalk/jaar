from src.f00_instrument.file import open_json, save_json, count_dirs_files
from src.f01_road.deal import owner_name_str, quota_str, celldepth_str
from src.f04_gift.atom_config import event_int_str, penny_str
from src.f05_listen.hub_path import (
    create_cell_dir_path as node_dir,
    create_cell_node_json_path as node_path,
    create_cell_quota_ledger_path as quota_path,
)
from src.f05_listen.hub_tool import save_arbitrary_budevent as save_budevent
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_create_fisc_deal_trees_Scenaro0_timepoint_Empty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"
    bob_str = "Bob"
    tp37 = 37

    a23_bob_tp37_path = node_dir(fisc_mstr_dir, a23_str, bob_str, tp37, [])
    print(f"{a23_bob_tp37_path=}")
    assert count_dirs_files(a23_bob_tp37_path) == 0

    # WHEN
    fizz_world.create_fisc_deal_trees()

    # THEN
    assert count_dirs_files(a23_bob_tp37_path) == 0


def test_WorldUnit_create_fisc_deal_trees_Scenaro1_LedgerDepth0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"
    bob_str = "Bob"
    yao_str = "Yao"
    tp37 = 37  # timepoint
    deal1_quota = 450
    deal1_celldepth = 0
    event56 = 56
    cell_node = {
        "ancestors": [],
        celldepth_str(): deal1_celldepth,
        "deal_owner_name": bob_str,
        event_int_str(): event56,
        quota_str(): deal1_quota,
    }
    a23_bob_ledger_state_path = node_path(
        fisc_mstr_dir=fisc_mstr_dir,
        fisc_title=a23_str,
        owner_name=bob_str,
        time_int=tp37,
    )
    save_json(a23_bob_ledger_state_path, None, cell_node)
    save_budevent(fisc_mstr_dir, a23_str, bob_str, event56, [[yao_str], [bob_str]])

    bob_tp37_quota_ledger_path = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37)
    bob_tp37_dir = node_dir(fisc_mstr_dir, a23_str, bob_str, tp37, [])
    assert os_path_exists(bob_tp37_quota_ledger_path) is False
    assert count_dirs_files(bob_tp37_dir) == 1

    # WHEN
    fizz_world.create_fisc_deal_trees()

    # THEN
    assert os_path_exists(bob_tp37_quota_ledger_path)
    assert open_json(bob_tp37_quota_ledger_path) == {"Bob": 225, "Yao": 225}
    assert count_dirs_files(bob_tp37_dir) == 2


def test_WorldUnit_create_fisc_deal_trees_Scenaro2_LedgerDepth1(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37  # timepoint
    deal1_quota = 450
    deal1_celldepth = 1
    event56 = 56
    cell_node = {
        "ancestors": [bob_str],
        event_int_str(): event56,
        celldepth_str(): deal1_celldepth,
        owner_name_str(): bob_str,
        penny_str(): 1,
        quota_str(): deal1_quota,
    }
    a23_bob_ledger_state_path = node_path(
        fisc_mstr_dir=fisc_mstr_dir,
        fisc_title=a23_str,
        owner_name=bob_str,
        time_int=tp37,
    )
    save_json(a23_bob_ledger_state_path, None, cell_node)
    bob_accts = [[yao_str], [bob_str], [zia_str]]
    yao_accts = [[zia_str]]
    zia_accts = [[bob_str], [yao_str]]
    bob_e56_path = save_budevent(fisc_mstr_dir, a23_str, bob_str, event56, bob_accts)
    yao_e56_path = save_budevent(fisc_mstr_dir, a23_str, yao_str, event56, yao_accts)
    zia_e56_path = save_budevent(fisc_mstr_dir, a23_str, zia_str, event56, zia_accts)
    assert os_path_exists(bob_e56_path)
    assert os_path_exists(yao_e56_path)
    assert os_path_exists(zia_e56_path)
    tp37_dir = node_dir(fisc_mstr_dir, a23_str, bob_str, tp37, [])
    bob_tp37_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [])
    bob_tp37_bob_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    bob_tp37_yao_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    bob_tp37_zia_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    tp37_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37)
    tp37_bob_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    tp37_yao_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    tp37_zia_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    assert os_path_exists(bob_tp37_node_path)
    assert os_path_exists(bob_tp37_bob_node_path) is False
    assert os_path_exists(bob_tp37_yao_node_path) is False
    assert os_path_exists(bob_tp37_zia_node_path) is False
    assert os_path_exists(tp37_quota) is False
    assert os_path_exists(tp37_bob_quota) is False
    assert os_path_exists(tp37_yao_quota) is False
    assert os_path_exists(tp37_zia_quota) is False
    assert count_dirs_files(tp37_dir) == 1

    # WHEN
    fizz_world.create_fisc_deal_trees()

    # THEN
    assert os_path_exists(tp37_quota)
    assert open_json(tp37_quota) == {bob_str: 150, yao_str: 150, zia_str: 150}
    print(f"{bob_tp37_bob_node_path=}")
    print(f"{bob_tp37_yao_node_path=}")
    print(f"{bob_tp37_zia_node_path=}")
    assert os_path_exists(bob_tp37_node_path)
    assert os_path_exists(bob_tp37_bob_node_path)
    assert os_path_exists(bob_tp37_yao_node_path)
    assert os_path_exists(bob_tp37_zia_node_path)
    assert os_path_exists(tp37_quota)
    assert os_path_exists(tp37_bob_quota)
    assert os_path_exists(tp37_yao_quota)
    assert os_path_exists(tp37_zia_quota)
    assert count_dirs_files(tp37_dir) == 11
    bob_tp37_bob_dict = open_json(bob_tp37_bob_node_path)
    assert bob_tp37_bob_dict.get("ancestors") == [bob_str, bob_str]
    assert bob_tp37_bob_dict.get("event_int") == 56
    assert bob_tp37_bob_dict.get("celldepth") == 0
    assert bob_tp37_bob_dict.get("deal_owner_name") == bob_str
    assert bob_tp37_bob_dict.get("penny") == 1
    assert bob_tp37_bob_dict.get("quota") == 150
    bob_tp37_yao_dict = open_json(bob_tp37_yao_node_path)
    assert bob_tp37_yao_dict.get("ancestors") == [bob_str, yao_str]
    assert bob_tp37_yao_dict.get("event_int") == 56
    assert bob_tp37_yao_dict.get("celldepth") == 0
    assert bob_tp37_yao_dict.get("deal_owner_name") == bob_str
    assert bob_tp37_yao_dict.get("penny") == 1
    assert bob_tp37_yao_dict.get("quota") == 150
    bob_tp37_zia_dict = open_json(bob_tp37_zia_node_path)
    assert bob_tp37_zia_dict.get("ancestors") == [bob_str, zia_str]
    assert bob_tp37_zia_dict.get("event_int") == 56
    assert bob_tp37_zia_dict.get("celldepth") == 0
    assert bob_tp37_zia_dict.get("deal_owner_name") == bob_str
    assert bob_tp37_zia_dict.get("penny") == 1
    assert bob_tp37_zia_dict.get("quota") == 150
    assert open_json(tp37_quota) == {"Bob": 150, "Yao": 150, "Zia": 150}
    assert open_json(tp37_bob_quota) == {"Bob": 50, "Yao": 50, "Zia": 50}
    assert open_json(tp37_yao_quota) == {"Zia": 150}
    assert open_json(tp37_zia_quota) == {"Bob": 75, "Yao": 75}


def test_WorldUnit_create_fisc_deal_trees_Scenaro3_LedgerDepth1_MostRecentEvent(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37  # timepoint
    deal1_quota = 450
    deal1_celldepth = 1
    event33 = 33
    event44 = 44
    event55 = 55
    cell_node = {
        "ancestors": [bob_str],
        event_int_str(): event55,
        celldepth_str(): deal1_celldepth,
        owner_name_str(): bob_str,
        penny_str(): 1,
        quota_str(): deal1_quota,
    }
    a23_bob_ledger_state_path = node_path(
        fisc_mstr_dir=fisc_mstr_dir,
        fisc_title=a23_str,
        owner_name=bob_str,
        time_int=tp37,
    )
    save_json(a23_bob_ledger_state_path, None, cell_node)
    bob_accts = [[yao_str], [bob_str], [zia_str]]
    yao_accts = [[zia_str]]
    zia_accts = [[bob_str], [yao_str]]
    bob_e55_path = save_budevent(fisc_mstr_dir, a23_str, bob_str, event55, bob_accts)
    yao_e44_path = save_budevent(fisc_mstr_dir, a23_str, yao_str, event44, yao_accts)
    yao_e33_path = save_budevent(fisc_mstr_dir, a23_str, yao_str, event33, yao_accts)
    zia_e33_path = save_budevent(fisc_mstr_dir, a23_str, zia_str, event33, zia_accts)
    assert os_path_exists(bob_e55_path)
    assert os_path_exists(yao_e44_path)
    assert os_path_exists(zia_e33_path)
    tp37_dir = node_dir(fisc_mstr_dir, a23_str, bob_str, tp37, [])
    tp37_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [])
    tp37_bob_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    tp37_yao_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    tp37_zia_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    tp37_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37)
    tp37_bob_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    tp37_yao_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    tp37_zia_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    assert os_path_exists(tp37_node_path)
    assert os_path_exists(tp37_bob_node_path) is False
    assert os_path_exists(tp37_yao_node_path) is False
    assert os_path_exists(tp37_zia_node_path) is False
    assert os_path_exists(tp37_quota) is False
    assert os_path_exists(tp37_bob_quota) is False
    assert os_path_exists(tp37_yao_quota) is False
    assert os_path_exists(tp37_zia_quota) is False
    assert count_dirs_files(tp37_dir) == 1

    # WHEN
    fizz_world.create_fisc_deal_trees()

    # THEN
    assert os_path_exists(tp37_quota)
    assert open_json(tp37_quota) == {bob_str: 150, yao_str: 150, zia_str: 150}
    print(f"{tp37_bob_node_path=}")
    print(f"{tp37_yao_node_path=}")
    print(f"{tp37_zia_node_path=}")
    assert os_path_exists(tp37_node_path)
    assert os_path_exists(tp37_bob_node_path)
    assert os_path_exists(tp37_yao_node_path)
    assert os_path_exists(tp37_zia_node_path)
    assert os_path_exists(tp37_quota)
    assert os_path_exists(tp37_bob_quota)
    assert os_path_exists(tp37_yao_quota)
    assert os_path_exists(tp37_zia_quota)
    assert count_dirs_files(tp37_dir) == 11
    bob_tp37_bob_dict = open_json(tp37_bob_node_path)
    assert bob_tp37_bob_dict.get("ancestors") == [bob_str, bob_str]
    assert bob_tp37_bob_dict.get("event_int") == 55
    assert bob_tp37_bob_dict.get("celldepth") == 0
    assert bob_tp37_bob_dict.get("deal_owner_name") == bob_str
    assert bob_tp37_bob_dict.get("penny") == 1
    assert bob_tp37_bob_dict.get("quota") == 150
    bob_tp37_yao_dict = open_json(tp37_yao_node_path)
    assert bob_tp37_yao_dict.get("ancestors") == [bob_str, yao_str]
    assert bob_tp37_yao_dict.get("event_int") == 44
    assert bob_tp37_yao_dict.get("celldepth") == 0
    assert bob_tp37_yao_dict.get("deal_owner_name") == bob_str
    assert bob_tp37_yao_dict.get("penny") == 1
    assert bob_tp37_yao_dict.get("quota") == 150
    bob_tp37_zia_dict = open_json(tp37_zia_node_path)
    assert bob_tp37_zia_dict.get("ancestors") == [bob_str, zia_str]
    assert bob_tp37_zia_dict.get("event_int") == 33
    assert bob_tp37_zia_dict.get("celldepth") == 0
    assert bob_tp37_zia_dict.get("deal_owner_name") == bob_str
    assert bob_tp37_zia_dict.get("penny") == 1
    assert bob_tp37_zia_dict.get("quota") == 150
    assert open_json(tp37_quota) == {"Bob": 150, "Yao": 150, "Zia": 150}
    assert open_json(tp37_bob_quota) == {"Bob": 50, "Yao": 50, "Zia": 50}
    assert open_json(tp37_yao_quota) == {"Zia": 150}
    assert open_json(tp37_zia_quota) == {"Bob": 75, "Yao": 75}


def test_WorldUnit_create_fisc_deal_trees_Scenaro4_LedgerDepth1_OneOwnerHasNoPast_budevent(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37  # timepoint
    deal1_quota = 450
    deal1_celldepth = 1
    event33 = 33
    event44 = 44
    event55 = 55
    event66 = 66
    cell_node = {
        "ancestors": [bob_str],
        event_int_str(): event55,
        celldepth_str(): deal1_celldepth,
        owner_name_str(): bob_str,
        penny_str(): 1,
        quota_str(): deal1_quota,
    }
    a23_bob_ledger_state_path = node_path(
        fisc_mstr_dir=fisc_mstr_dir,
        fisc_title=a23_str,
        owner_name=bob_str,
        time_int=tp37,
    )
    save_json(a23_bob_ledger_state_path, None, cell_node)
    bob_accts = [[yao_str], [bob_str], [zia_str]]
    yao_accts = [[zia_str]]
    zia_accts = [[bob_str], [yao_str]]
    bob_e55_path = save_budevent(fisc_mstr_dir, a23_str, bob_str, event55, bob_accts)
    yao_e44_path = save_budevent(fisc_mstr_dir, a23_str, yao_str, event44, yao_accts)
    yao_e33_path = save_budevent(fisc_mstr_dir, a23_str, yao_str, event33, yao_accts)
    zia_e66_path = save_budevent(fisc_mstr_dir, a23_str, zia_str, event66, zia_accts)
    assert os_path_exists(bob_e55_path)
    assert os_path_exists(yao_e44_path)
    assert os_path_exists(zia_e66_path)
    tp37_dir = node_dir(fisc_mstr_dir, a23_str, bob_str, tp37, [])
    tp37_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [])
    tp37_bob_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    tp37_yao_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    tp37_zia_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    tp37_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37)
    tp37_bob_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    tp37_yao_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    tp37_zia_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    assert os_path_exists(tp37_node_path)
    assert os_path_exists(tp37_bob_node_path) is False
    assert os_path_exists(tp37_yao_node_path) is False
    assert os_path_exists(tp37_zia_node_path) is False
    assert os_path_exists(tp37_quota) is False
    assert os_path_exists(tp37_bob_quota) is False
    assert os_path_exists(tp37_yao_quota) is False
    assert os_path_exists(tp37_zia_quota) is False
    assert count_dirs_files(tp37_dir) == 1

    # WHEN
    fizz_world.create_fisc_deal_trees()

    # THEN
    assert os_path_exists(tp37_quota)
    assert open_json(tp37_quota) == {bob_str: 150, yao_str: 150, zia_str: 150}
    print(f"{tp37_bob_node_path=}")
    print(f"{tp37_yao_node_path=}")
    print(f"{tp37_zia_node_path=}")
    assert os_path_exists(tp37_node_path)
    assert os_path_exists(tp37_bob_node_path)
    assert os_path_exists(tp37_yao_node_path)
    assert os_path_exists(tp37_zia_node_path) is False
    assert os_path_exists(tp37_quota)
    assert os_path_exists(tp37_bob_quota)
    assert os_path_exists(tp37_yao_quota)
    assert os_path_exists(tp37_zia_quota) is False
    assert count_dirs_files(tp37_dir) == 8
    bob_tp37_bob_dict = open_json(tp37_bob_node_path)
    assert bob_tp37_bob_dict.get("ancestors") == [bob_str, bob_str]
    assert bob_tp37_bob_dict.get("event_int") == 55
    assert bob_tp37_bob_dict.get("celldepth") == 0
    assert bob_tp37_bob_dict.get("deal_owner_name") == bob_str
    assert bob_tp37_bob_dict.get("penny") == 1
    assert bob_tp37_bob_dict.get("quota") == 150
    bob_tp37_yao_dict = open_json(tp37_yao_node_path)
    assert bob_tp37_yao_dict.get("ancestors") == [bob_str, yao_str]
    assert bob_tp37_yao_dict.get("event_int") == 44
    assert bob_tp37_yao_dict.get("celldepth") == 0
    assert bob_tp37_yao_dict.get("deal_owner_name") == bob_str
    assert bob_tp37_yao_dict.get("penny") == 1
    assert bob_tp37_yao_dict.get("quota") == 150
    assert open_json(tp37_quota) == {"Bob": 150, "Yao": 150, "Zia": 150}
    assert open_json(tp37_bob_quota) == {"Bob": 50, "Yao": 50, "Zia": 50}
    assert open_json(tp37_yao_quota) == {"Zia": 150}


def test_WorldUnit_create_fisc_deal_trees_Scenaro5_LedgerDepth1_ZeroQuotaDoesNotGetCreated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37  # timepoint
    deal1_quota = 2
    deal1_celldepth = 1
    event33 = 33
    event44 = 44
    event55 = 55
    cell_node = {
        "ancestors": [bob_str],
        event_int_str(): event55,
        celldepth_str(): deal1_celldepth,
        owner_name_str(): bob_str,
        penny_str(): 1,
        quota_str(): deal1_quota,
    }
    a23_bob_ledger_state_path = node_path(
        fisc_mstr_dir=fisc_mstr_dir,
        fisc_title=a23_str,
        owner_name=bob_str,
        time_int=tp37,
    )
    save_json(a23_bob_ledger_state_path, None, cell_node)
    bob_accts = [[yao_str], [bob_str], [zia_str]]
    yao_accts = [[zia_str]]
    zia_accts = [[bob_str], [yao_str]]
    bob_e55_path = save_budevent(fisc_mstr_dir, a23_str, bob_str, event55, bob_accts)
    yao_e44_path = save_budevent(fisc_mstr_dir, a23_str, yao_str, event44, yao_accts)
    yao_e33_path = save_budevent(fisc_mstr_dir, a23_str, yao_str, event33, yao_accts)
    zia_e33_path = save_budevent(fisc_mstr_dir, a23_str, zia_str, event33, zia_accts)
    assert os_path_exists(bob_e55_path)
    assert os_path_exists(yao_e44_path)
    assert os_path_exists(zia_e33_path)
    tp37_dir = node_dir(fisc_mstr_dir, a23_str, bob_str, tp37, [])
    tp37_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [])
    tp37_bob_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    tp37_yao_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    tp37_zia_node_path = node_path(fisc_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    tp37_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37)
    tp37_bob_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37, [bob_str])
    tp37_yao_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37, [yao_str])
    tp37_zia_quota = quota_path(fisc_mstr_dir, a23_str, bob_str, tp37, [zia_str])
    assert os_path_exists(tp37_node_path)
    assert os_path_exists(tp37_bob_node_path) is False
    assert os_path_exists(tp37_yao_node_path) is False
    assert os_path_exists(tp37_zia_node_path) is False
    assert os_path_exists(tp37_quota) is False
    assert os_path_exists(tp37_bob_quota) is False
    assert os_path_exists(tp37_yao_quota) is False
    assert os_path_exists(tp37_zia_quota) is False
    assert count_dirs_files(tp37_dir) == 1

    # WHEN
    fizz_world.create_fisc_deal_trees()

    # THEN
    assert os_path_exists(tp37_quota)
    assert open_json(tp37_quota) == {bob_str: 0, yao_str: 1, zia_str: 1}
    print(f"{tp37_bob_node_path=}")
    print(f"{tp37_yao_node_path=}")
    print(f"{tp37_zia_node_path=}")
    assert os_path_exists(tp37_node_path)
    assert os_path_exists(tp37_bob_node_path) is False
    assert os_path_exists(tp37_yao_node_path)
    assert os_path_exists(tp37_zia_node_path)
    assert os_path_exists(tp37_quota)
    assert os_path_exists(tp37_bob_quota) is False
    assert os_path_exists(tp37_yao_quota)
    assert os_path_exists(tp37_zia_quota)
    assert count_dirs_files(tp37_dir) == 8
    assert open_json(tp37_quota) == {bob_str: 0, yao_str: 1, zia_str: 1}
    assert open_json(tp37_yao_quota) == {"Zia": 1}
    assert open_json(tp37_zia_quota) == {"Bob": 1, "Yao": 0}
