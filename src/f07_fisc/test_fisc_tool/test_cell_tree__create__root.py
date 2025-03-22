from src.f00_instrument.file import save_file, open_json, count_dirs_files
from src.f01_road.deal import celldepth_str, quota_str, DEFAULT_CELLDEPTH
from src.f04_gift.atom_config import event_int_str, penny_str
from src.f05_listen.cell import deal_owner_name_str, ancestors_str
from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_fisc_owners_dir_path,
    create_cell_json_path,
)
from src.f07_fisc.fisc import fiscunit_shop, _get_ote1_max_past_event_int
from src.f07_fisc.examples.fisc_env import env_dir_setup_cleanup, get_test_fisc_mstr_dir
from os.path import exists as os_path_exists


def test_get_ote1_max_past_event_int_ReturnsObj_Scenaro0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    tp37 = 37
    ote1_dict = {}

    # WHEN / THEN
    assert not _get_ote1_max_past_event_int(bob_str, ote1_dict, tp37)


def test_FiscUnit_create_deals_root_cells_Scenaro0_DealEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    accord23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    a23_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    print(f"{a23_json_path=}")
    a23_owners_path = create_fisc_owners_dir_path(fisc_mstr_dir, a23_str)
    assert count_dirs_files(a23_owners_path) == 0

    # WHEN
    accord23_fisc.create_deals_root_cells({})

    # THEN
    assert count_dirs_files(a23_owners_path) == 0


def test_FiscUnit_create_deals_root_cells_Scenaro1_DealExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"

    # Create FiscUnit with bob deal at time 37
    accord23_fisc = fiscunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    timepoint37 = 37
    deal1_quota = 450
    accord23_fisc.add_dealunit(bob_str, timepoint37, deal1_quota)
    a23_json_path = create_fisc_json_path(mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    assert os_path_exists(a23_json_path)

    # Create event time mapping owner_time_agg for time 37
    event3 = 3
    event7 = 7
    timepoint66 = 66
    a23_ote1_dict = {bob_str: {str(timepoint37): event3, str(timepoint66): event7}}

    # timepoint37 cell path
    tp37_cell_json_path = create_cell_json_path(mstr_dir, a23_str, bob_str, timepoint37)
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    accord23_fisc.create_deals_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    print(f"{cell_dict=}")
    assert cell_dict.get(celldepth_str()) == DEFAULT_CELLDEPTH
    assert cell_dict.get(deal_owner_name_str()) == bob_str
    assert cell_dict.get(quota_str()) == deal1_quota
    assert cell_dict.get(event_int_str()) == event3


def test_FiscUnit_create_deals_root_cells_Scenaro2_DealExistsButNoBudExistsInEventsPast(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"

    # Create FiscUnit with bob deal at time 37
    accord23_fisc = fiscunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    timepoint37 = 37
    deal1_quota = 450
    accord23_fisc.add_dealunit(bob_str, timepoint37, deal1_quota)
    a23_json_path = create_fisc_json_path(mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    assert os_path_exists(a23_json_path)

    # Create event time mapping owner_time_agg for time 37
    event3 = 3
    event7 = 7
    timepoint40 = 40
    timepoint66 = 66
    a23_ote1_dict = {bob_str: {str(timepoint40): event3, str(timepoint66): event7}}
    tp37_cell_json_path = create_cell_json_path(mstr_dir, a23_str, bob_str, timepoint37)
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    accord23_fisc.create_deals_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    print(f"{cell_dict=}")
    assert cell_dict.get(ancestors_str()) == []
    assert not cell_dict.get(event_int_str())
    assert cell_dict.get(celldepth_str()) == DEFAULT_CELLDEPTH
    assert cell_dict.get(deal_owner_name_str()) == bob_str
    assert cell_dict.get(quota_str()) == deal1_quota


def test_FiscUnit_create_deals_root_cells_Scenaro3_DealExistsNotPerfectMatch_deal_time_event_int(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    a23_str = "accord23"
    a23_penny = 2

    # Create FiscUnit with bob deal at time 37
    accord23_fisc = fiscunit_shop(a23_str, mstr_dir, penny=a23_penny)
    print(f"{accord23_fisc.penny=}")
    bob_str = "Bob"
    timepoint37 = 37
    deal1_quota = 450
    deal1_celldepth = 3
    accord23_fisc.add_dealunit(
        bob_str, timepoint37, deal1_quota, celldepth=deal1_celldepth
    )
    a23_json_path = create_fisc_json_path(mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    assert os_path_exists(a23_json_path)

    # Create event time mapping owner_time_agg for time 37
    event3 = 3
    event7 = 7
    timepoint30 = 30
    timepoint66 = 66
    a23_ote1_dict = {bob_str: {str(timepoint30): event3, str(timepoint66): event7}}

    # destination of cell json
    tp37_cell_json_path = create_cell_json_path(mstr_dir, a23_str, bob_str, timepoint37)
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    accord23_fisc.create_deals_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    assert cell_dict.get(ancestors_str()) == []
    assert cell_dict.get(event_int_str()) == event3
    assert cell_dict.get(celldepth_str()) == deal1_celldepth
    assert cell_dict.get(deal_owner_name_str()) == bob_str
    assert cell_dict.get(penny_str()) == a23_penny
    assert cell_dict.get(quota_str()) == deal1_quota
