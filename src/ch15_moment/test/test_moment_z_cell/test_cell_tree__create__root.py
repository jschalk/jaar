from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import count_dirs_files, open_json, save_json
from src.ch09_belief_lesson._ref.ch09_path import (
    create_moment_beliefs_dir_path,
    create_moment_json_path,
)
from src.ch12_bud._ref.ch12_path import create_cell_json_path
from src.ch12_bud.bud_main import DEFAULT_CELLDEPTH
from src.ch15_moment.moment_main import _get_ote1_max_past_spark_num, momentunit_shop
from src.ch15_moment.test._util.ch15_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import Ch15Keywords as kw


def test_get_ote1_max_past_spark_num_ReturnsObj_Scenaro0(
    temp_dir_setup,
):
    # ESTABLISH
    bob_str = "Bob"
    tp37 = 37
    ote1_dict = {}

    # WHEN / THEN
    assert not _get_ote1_max_past_spark_num(bob_str, ote1_dict, tp37)


def test_MomentUnit_create_buds_root_cells_Scenaro0_BudEmpty(
    temp_dir_setup,
):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_temp_dir()
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
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = "amy23"

    # Create MomentUnit with bob bud at time 37
    amy23_moment = momentunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    epochtime37 = 37
    bud1_quota = 450
    amy23_moment.add_budunit(bob_str, epochtime37, bud1_quota)
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    assert os_path_exists(a23_json_path)

    # Create spark time mapping belief_time_agg for time 37
    spark3 = 3
    spark7 = 7
    epochtime66 = 66
    a23_ote1_dict = {bob_str: {str(epochtime37): spark3, str(epochtime66): spark7}}

    # epochtime37 cell path
    tp37_cell_json_path = create_cell_json_path(mstr_dir, a23_str, bob_str, epochtime37)
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    amy23_moment.create_buds_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    print(f"{cell_dict=}")
    assert cell_dict.get(kw.celldepth) == DEFAULT_CELLDEPTH
    assert cell_dict.get(kw.bud_belief_name) == bob_str
    assert cell_dict.get(kw.quota) == bud1_quota
    assert cell_dict.get(kw.spark_num) == spark3


def test_MomentUnit_create_buds_root_cells_Scenaro2_BudExistsButNoBeliefExistsInSparksPast(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = "amy23"

    # Create MomentUnit with bob bud at time 37
    amy23_moment = momentunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    epochtime37 = 37
    bud1_quota = 450
    amy23_moment.add_budunit(bob_str, epochtime37, bud1_quota)
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    assert os_path_exists(a23_json_path)

    # Create spark time mapping belief_time_agg for time 37
    spark3 = 3
    spark7 = 7
    epochtime40 = 40
    epochtime66 = 66
    a23_ote1_dict = {bob_str: {str(epochtime40): spark3, str(epochtime66): spark7}}
    tp37_cell_json_path = create_cell_json_path(mstr_dir, a23_str, bob_str, epochtime37)
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    amy23_moment.create_buds_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    print(f"{cell_dict=}")
    assert cell_dict.get(kw.ancestors) == []
    assert not cell_dict.get(kw.spark_num)
    assert cell_dict.get(kw.celldepth) == DEFAULT_CELLDEPTH
    assert cell_dict.get(kw.bud_belief_name) == bob_str
    assert cell_dict.get(kw.quota) == bud1_quota


def test_MomentUnit_create_buds_root_cells_Scenaro3_BudExistsNotPerfectMatch_bud_time_spark_num(
    temp_dir_setup,
):
    # ESTABLISH
    mstr_dir = get_temp_dir()
    a23_str = "amy23"
    a23_mana_grain = 2

    # Create MomentUnit with bob bud at time 37
    amy23_moment = momentunit_shop(a23_str, mstr_dir, mana_grain=a23_mana_grain)
    print(f"{amy23_moment.mana_grain=}")
    bob_str = "Bob"
    epochtime37 = 37
    bud1_quota = 450
    bud1_celldepth = 3
    amy23_moment.add_budunit(bob_str, epochtime37, bud1_quota, celldepth=bud1_celldepth)
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    assert os_path_exists(a23_json_path)

    # Create spark time mapping belief_time_agg for time 37
    spark3 = 3
    spark7 = 7
    epochtime30 = 30
    epochtime66 = 66
    a23_ote1_dict = {bob_str: {str(epochtime30): spark3, str(epochtime66): spark7}}

    # destination of cell json
    tp37_cell_json_path = create_cell_json_path(mstr_dir, a23_str, bob_str, epochtime37)
    assert os_path_exists(tp37_cell_json_path) is False

    # WHEN
    amy23_moment.create_buds_root_cells(a23_ote1_dict)

    # THEN
    assert os_path_exists(tp37_cell_json_path)
    cell_dict = open_json(tp37_cell_json_path)
    assert cell_dict.get(kw.ancestors) == []
    assert cell_dict.get(kw.spark_num) == spark3
    assert cell_dict.get(kw.celldepth) == bud1_celldepth
    assert cell_dict.get(kw.bud_belief_name) == bob_str
    assert cell_dict.get(kw.mana_grain) == a23_mana_grain
    assert cell_dict.get(kw.quota) == bud1_quota
