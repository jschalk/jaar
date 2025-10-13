from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import count_dirs_files, open_json, save_json
from src.ch10_pack._ref.ch10_path import (
    create_moment_beliefs_dir_path,
    create_moment_json_path,
)
from src.ch11_bud._ref.ch11_path import create_cell_json_path
from src.ch11_bud.bud_main import DEFAULT_CELLDEPTH
from src.ch15_moment.moment_main import _get_ote1_max_past_event_num, momentunit_shop
from src.ch15_moment.test._util.ch15_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ref.keywords import Ch15Keywords as wx


def test_get_ote1_max_past_event_num_ReturnsObj_Scenaro0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    tp37 = 37
    ote1_dict = {}

    # WHEN / THEN
    assert not _get_ote1_max_past_event_num(bob_str, ote1_dict, tp37)


def test_MomentUnit_create_buds_root_cells_Scenaro0_BudEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_chapter_temp_dir()
    amy23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    a23_json_path = create_moment_json_path(moment_mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    print(f"{a23_json_path=}")
    a23_beliefs_path = create_moment_beliefs_dir_path(moment_mstr_dir, a23_str)
    assert count_dirs_files(a23_beliefs_path) == 0

    # WHEN
    amy23_moment.create_buds_root_cells({})

    # THEN
    assert count_dirs_files(a23_beliefs_path) == 0


def test_MomentUnit_create_buds_root_cells_Scenaro1_BudExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"

    # Create MomentUnit with bob bud at time 37
    amy23_moment = momentunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    timepoint37 = 37
    bud1_quota = 450
    amy23_moment.add_budunit(bob_str, timepoint37, bud1_quota)
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    assert os_path_exists(a23_json_path)

    # Create event time mapping belief_time_agg for time 37
    event3 = 3
    event7 = 7
    timepoint66 = 66
    a23_ote1_dict = {bob_str: {str(timepoint37): event3, str(timepoint66): event7}}

    # timepoint37 cell path
    tp37_cell_json_path = create_cell_json_path(mstr_dir, a23_str, bob_str, timepoint37)
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    amy23_moment.create_buds_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    print(f"{cell_dict=}")
    assert cell_dict.get(wx.celldepth) == DEFAULT_CELLDEPTH
    assert cell_dict.get(wx.bud_belief_name) == bob_str
    assert cell_dict.get(wx.quota) == bud1_quota
    assert cell_dict.get(wx.event_num) == event3


def test_MomentUnit_create_buds_root_cells_Scenaro2_BudExistsButNoBeliefExistsInEventsPast(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"

    # Create MomentUnit with bob bud at time 37
    amy23_moment = momentunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    timepoint37 = 37
    bud1_quota = 450
    amy23_moment.add_budunit(bob_str, timepoint37, bud1_quota)
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    assert os_path_exists(a23_json_path)

    # Create event time mapping belief_time_agg for time 37
    event3 = 3
    event7 = 7
    timepoint40 = 40
    timepoint66 = 66
    a23_ote1_dict = {bob_str: {str(timepoint40): event3, str(timepoint66): event7}}
    tp37_cell_json_path = create_cell_json_path(mstr_dir, a23_str, bob_str, timepoint37)
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    amy23_moment.create_buds_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    print(f"{cell_dict=}")
    assert cell_dict.get(wx.ancestors) == []
    assert not cell_dict.get(wx.event_num)
    assert cell_dict.get(wx.celldepth) == DEFAULT_CELLDEPTH
    assert cell_dict.get(wx.bud_belief_name) == bob_str
    assert cell_dict.get(wx.quota) == bud1_quota


def test_MomentUnit_create_buds_root_cells_Scenaro3_BudExistsNotPerfectMatch_bud_time_event_num(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_chapter_temp_dir()
    a23_str = "amy23"
    a23_money_grain = 2

    # Create MomentUnit with bob bud at time 37
    amy23_moment = momentunit_shop(a23_str, mstr_dir, money_grain=a23_money_grain)
    print(f"{amy23_moment.money_grain=}")
    bob_str = "Bob"
    timepoint37 = 37
    bud1_quota = 450
    bud1_celldepth = 3
    amy23_moment.add_budunit(bob_str, timepoint37, bud1_quota, celldepth=bud1_celldepth)
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    assert os_path_exists(a23_json_path)

    # Create event time mapping belief_time_agg for time 37
    event3 = 3
    event7 = 7
    timepoint30 = 30
    timepoint66 = 66
    a23_ote1_dict = {bob_str: {str(timepoint30): event3, str(timepoint66): event7}}

    # destination of cell json
    tp37_cell_json_path = create_cell_json_path(mstr_dir, a23_str, bob_str, timepoint37)
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    amy23_moment.create_buds_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    assert cell_dict.get(wx.ancestors) == []
    assert cell_dict.get(wx.event_num) == event3
    assert cell_dict.get(wx.celldepth) == bud1_celldepth
    assert cell_dict.get(wx.bud_belief_name) == bob_str
    assert cell_dict.get(wx.money_grain) == a23_money_grain
    assert cell_dict.get(wx.quota) == bud1_quota
