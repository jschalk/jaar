from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import open_json, save_file
from src.a02_finance_logic._test_util.a02_str import (
    bud_time_str,
    owner_name_str,
    vow_label_str,
)
from src.a09_pack_logic._test_util.a09_str import event_int_str
from src.a12_hub_toolbox.hub_path import (
    create_vow_ote1_csv_path,
    create_vow_ote1_json_path,
)
from src.a18_etl_toolbox._test_util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.transformers import etl_vow_ote1_agg_csvs_to_jsons


def test_WorldUnit_vow_ote1_agg_csvs2jsons_CreatesFile_Scenaro0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    timepoint55 = 55
    timepoint66 = 66
    vow_mstr_dir = get_module_temp_dir()
    a23_event_time_p = create_vow_ote1_csv_path(vow_mstr_dir, accord23_str)
    a45_event_time_p = create_vow_ote1_csv_path(vow_mstr_dir, accord45_str)
    a23_event_time_csv = f"""{vow_label_str()},{owner_name_str()},{event_int_str()},{bud_time_str()},error_message
{accord23_str},{bob_str},{event3},{timepoint55},
"""
    a45_event_time_csv = f"""{vow_label_str()},{owner_name_str()},{event_int_str()},{bud_time_str()},error_message
{accord45_str},{sue_str},{event3},{timepoint55},
{accord45_str},{sue_str},{event7},{timepoint66},
"""
    save_file(a23_event_time_p, None, a23_event_time_csv)
    save_file(a45_event_time_p, None, a45_event_time_csv)
    assert os_path_exists(a23_event_time_p)
    assert os_path_exists(a45_event_time_p)
    a23_ote1_json_path = create_vow_ote1_json_path(vow_mstr_dir, accord23_str)
    a45_ote1_json_path = create_vow_ote1_json_path(vow_mstr_dir, accord45_str)
    assert os_path_exists(a23_ote1_json_path) is False
    assert os_path_exists(a45_ote1_json_path) is False

    # WHEN
    etl_vow_ote1_agg_csvs_to_jsons(vow_mstr_dir)

    # THEN
    assert os_path_exists(a23_ote1_json_path)
    assert os_path_exists(a45_ote1_json_path)
    a23_ote1_dict = open_json(a23_ote1_json_path)
    a45_ote1_dict = open_json(a45_ote1_json_path)
    assert a23_ote1_dict == {bob_str: {str(timepoint55): event3}}
    assert a45_ote1_dict == {
        sue_str: {str(timepoint55): event3, str(timepoint66): event7}
    }
