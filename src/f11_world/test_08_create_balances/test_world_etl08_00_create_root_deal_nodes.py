from src.f00_instrument.file import save_file, open_json, save_json, count_dirs_files
from src.f01_road.deal import (
    celldepth_str,
    owner_name_str,
    quota_str,
    DEFAULT_celldepth,
)
from src.f04_gift.atom_config import event_int_str, penny_str
from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_owners_dir_path,
    create_cell_json_path,
    create_fisc_ote1_json_path,
)
from src.f07_fisc.fisc import fiscunit_shop
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_create_deals_root_cells_Scenaro0_DealEmpty(
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
    fizz_world.create_deals_root_cells()

    # THEN
    assert count_dirs_files(a23_owners_path) == 0


def test_WorldUnit_create_deals_root_cells_Scenaro1_DealExists(
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
    accord23_fisc.add_dealunit(bob_str, timepoint37, deal1_quota)
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

    # timepoint37 cell path
    tp37_cell_json_path = create_cell_json_path(
        fisc_mstr_dir, a23_str, bob_str, timepoint37
    )
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    fizz_world.create_deals_root_cells()

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    ledger_state_dict = open_json(tp37_cell_json_path)
    print(f"{ledger_state_dict=}")
    assert ledger_state_dict.get(celldepth_str()) == DEFAULT_celldepth
    assert ledger_state_dict.get("deal_owner_name") == bob_str
    assert ledger_state_dict.get(quota_str()) == deal1_quota
    assert ledger_state_dict.get(event_int_str()) == event3


def test_WorldUnit_create_deals_root_cells_Scenaro2_DealExistsButNoBudExistsInEventsPast(
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
    accord23_fisc.add_dealunit(bob_str, timepoint37, deal1_quota)
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
    tp37_cell_json_path = create_cell_json_path(
        fisc_mstr_dir, a23_str, bob_str, timepoint37
    )
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    fizz_world.create_deals_root_cells()

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    ledger_state_dict = open_json(tp37_cell_json_path)
    print(f"{ledger_state_dict=}")
    assert ledger_state_dict.get("ancestors") == [bob_str]
    assert not ledger_state_dict.get(event_int_str())
    assert ledger_state_dict.get(celldepth_str()) == DEFAULT_celldepth
    assert ledger_state_dict.get("deal_owner_name") == bob_str
    assert ledger_state_dict.get(quota_str()) == deal1_quota


def test_WorldUnit_create_deals_root_cells_Scenaro3_DealExistsNotPerfectMatch_time_int_event_int(
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
    deal1_celldepth = 3
    accord23_fisc.add_dealunit(
        bob_str, timepoint37, deal1_quota, celldepth=deal1_celldepth
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

    # destination of cell json
    tp37_cell_json_path = create_cell_json_path(
        fisc_mstr_dir, a23_str, bob_str, timepoint37
    )
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    fizz_world.create_deals_root_cells()

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    ledger_state_dict = open_json(tp37_cell_json_path)
    assert ledger_state_dict.get("ancestors") == [bob_str]
    assert ledger_state_dict.get(event_int_str()) == event3
    assert ledger_state_dict.get(celldepth_str()) == deal1_celldepth
    assert ledger_state_dict.get("deal_owner_name") == bob_str
    assert ledger_state_dict.get(penny_str()) == a23_penny
    assert ledger_state_dict.get(quota_str()) == deal1_quota
    print(ledger_state_dict.get("ancestors"))
    assert len(ledger_state_dict) == 10
