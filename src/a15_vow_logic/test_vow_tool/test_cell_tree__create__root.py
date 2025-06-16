from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import count_dirs_files, open_json, save_file
from src.a02_finance_logic._test_util.a02_str import celldepth_str, quota_str
from src.a02_finance_logic.bud import DEFAULT_CELLDEPTH
from src.a06_plan_logic._test_util.a06_str import penny_str
from src.a09_pack_logic._test_util.a09_str import event_int_str
from src.a11_bud_cell_logic._test_util.a11_str import (
    ancestors_str,
    bud_owner_name_str,
    celldepth_str,
)
from src.a12_hub_toolbox.hub_path import (
    create_cell_json_path,
    create_vow_json_path,
    create_vow_owners_dir_path,
)
from src.a15_vow_logic._test_util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_vow_logic.vow import _get_ote1_max_past_event_int, vowunit_shop


def test_get_ote1_max_past_event_int_ReturnsObj_Scenaro0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    tp37 = 37
    ote1_dict = {}

    # WHEN / THEN
    assert not _get_ote1_max_past_event_int(bob_str, ote1_dict, tp37)


def test_VowUnit_create_buds_root_cells_Scenaro0_BudEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "accord23"
    vow_mstr_dir = get_module_temp_dir()
    accord23_vow = vowunit_shop(a23_str, vow_mstr_dir)
    a23_json_path = create_vow_json_path(vow_mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_vow.get_json())
    print(f"{a23_json_path=}")
    a23_owners_path = create_vow_owners_dir_path(vow_mstr_dir, a23_str)
    assert count_dirs_files(a23_owners_path) == 0

    # WHEN
    accord23_vow.create_buds_root_cells({})

    # THEN
    assert count_dirs_files(a23_owners_path) == 0


def test_VowUnit_create_buds_root_cells_Scenaro1_BudExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"

    # Create VowUnit with bob bud at time 37
    accord23_vow = vowunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    timepoint37 = 37
    bud1_quota = 450
    accord23_vow.add_budunit(bob_str, timepoint37, bud1_quota)
    a23_json_path = create_vow_json_path(mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_vow.get_json())
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
    accord23_vow.create_buds_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    print(f"{cell_dict=}")
    assert cell_dict.get(celldepth_str()) == DEFAULT_CELLDEPTH
    assert cell_dict.get(bud_owner_name_str()) == bob_str
    assert cell_dict.get(quota_str()) == bud1_quota
    assert cell_dict.get(event_int_str()) == event3


def test_VowUnit_create_buds_root_cells_Scenaro2_BudExistsButNoPlanExistsInEventsPast(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"

    # Create VowUnit with bob bud at time 37
    accord23_vow = vowunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    timepoint37 = 37
    bud1_quota = 450
    accord23_vow.add_budunit(bob_str, timepoint37, bud1_quota)
    a23_json_path = create_vow_json_path(mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_vow.get_json())
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
    accord23_vow.create_buds_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    print(f"{cell_dict=}")
    assert cell_dict.get(ancestors_str()) == []
    assert not cell_dict.get(event_int_str())
    assert cell_dict.get(celldepth_str()) == DEFAULT_CELLDEPTH
    assert cell_dict.get(bud_owner_name_str()) == bob_str
    assert cell_dict.get(quota_str()) == bud1_quota


def test_VowUnit_create_buds_root_cells_Scenaro3_BudExistsNotPerfectMatch_bud_time_event_int(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    a23_penny = 2

    # Create VowUnit with bob bud at time 37
    accord23_vow = vowunit_shop(a23_str, mstr_dir, penny=a23_penny)
    print(f"{accord23_vow.penny=}")
    bob_str = "Bob"
    timepoint37 = 37
    bud1_quota = 450
    bud1_celldepth = 3
    accord23_vow.add_budunit(bob_str, timepoint37, bud1_quota, celldepth=bud1_celldepth)
    a23_json_path = create_vow_json_path(mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_vow.get_json())
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
    accord23_vow.create_buds_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    assert cell_dict.get(ancestors_str()) == []
    assert cell_dict.get(event_int_str()) == event3
    assert cell_dict.get(celldepth_str()) == bud1_celldepth
    assert cell_dict.get(bud_owner_name_str()) == bob_str
    assert cell_dict.get(penny_str()) == a23_penny
    assert cell_dict.get(quota_str()) == bud1_quota
