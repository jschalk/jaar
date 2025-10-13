from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import open_json, save_file
from src.ch18_world_etl._ref.ch18_path import (
    create_moment_ote1_csv_path,
    create_moment_ote1_json_path,
)
from src.ch18_world_etl.test._util.ch18_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch18_world_etl.transformers import etl_moment_ote1_agg_csvs_to_jsons
from src.ref.keywords import Ch18Keywords as wx


def test_etl_moment_ote1_agg_csvs_to_jsons_CreatesFile_Scenaro0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event3 = 3
    event7 = 7
    amy23_str = "amy23"
    amy45_str = "amy45"
    timepoint55 = 55
    timepoint66 = 66
    moment_mstr_dir = get_chapter_temp_dir()
    a23_event_time_p = create_moment_ote1_csv_path(moment_mstr_dir, amy23_str)
    a45_event_time_p = create_moment_ote1_csv_path(moment_mstr_dir, amy45_str)
    a23_event_time_csv = f"""{wx.moment_label},{wx.belief_name},{wx.event_int},{wx.bud_time},{wx.error_message}
{amy23_str},{bob_str},{event3},{timepoint55},
"""
    a45_event_time_csv = f"""{wx.moment_label},{wx.belief_name},{wx.event_int},{wx.bud_time},{wx.error_message}
{amy45_str},{sue_str},{event3},{timepoint55},
{amy45_str},{sue_str},{event7},{timepoint66},
"""
    save_file(a23_event_time_p, None, a23_event_time_csv)
    save_file(a45_event_time_p, None, a45_event_time_csv)
    assert os_path_exists(a23_event_time_p)
    assert os_path_exists(a45_event_time_p)
    a23_ote1_json_path = create_moment_ote1_json_path(moment_mstr_dir, amy23_str)
    a45_ote1_json_path = create_moment_ote1_json_path(moment_mstr_dir, amy45_str)
    assert os_path_exists(a23_ote1_json_path) is False
    assert os_path_exists(a45_ote1_json_path) is False

    # WHEN
    etl_moment_ote1_agg_csvs_to_jsons(moment_mstr_dir)

    # THEN
    assert os_path_exists(a23_ote1_json_path)
    assert os_path_exists(a45_ote1_json_path)
    a23_ote1_dict = open_json(a23_ote1_json_path)
    a45_ote1_dict = open_json(a45_ote1_json_path)
    assert a23_ote1_dict == {bob_str: {str(timepoint55): event3}}
    assert a45_ote1_dict == {
        sue_str: {str(timepoint55): event3, str(timepoint66): event7}
    }
