from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import open_json, save_file
from src.a09_pack_logic.test._util.a09_str import event_int_str
from src.a11_bud_logic.test._util.a11_str import (
    belief_name_str,
    bud_time_str,
    coin_label_str,
)
from src.a17_idea_logic.test._util.a17_str import error_message_str
from src.a18_etl_toolbox.a18_path import (
    create_coin_ote1_csv_path,
    create_coin_ote1_json_path,
)
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.transformers import etl_coin_ote1_agg_csvs_to_jsons


def test_etl_coin_ote1_agg_csvs_to_jsons_CreatesFile_Scenaro0(
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
    coin_mstr_dir = get_module_temp_dir()
    a23_event_time_p = create_coin_ote1_csv_path(coin_mstr_dir, amy23_str)
    a45_event_time_p = create_coin_ote1_csv_path(coin_mstr_dir, amy45_str)
    a23_event_time_csv = f"""{coin_label_str()},{belief_name_str()},{event_int_str()},{bud_time_str()},{error_message_str()}
{amy23_str},{bob_str},{event3},{timepoint55},
"""
    a45_event_time_csv = f"""{coin_label_str()},{belief_name_str()},{event_int_str()},{bud_time_str()},{error_message_str()}
{amy45_str},{sue_str},{event3},{timepoint55},
{amy45_str},{sue_str},{event7},{timepoint66},
"""
    save_file(a23_event_time_p, None, a23_event_time_csv)
    save_file(a45_event_time_p, None, a45_event_time_csv)
    assert os_path_exists(a23_event_time_p)
    assert os_path_exists(a45_event_time_p)
    a23_ote1_json_path = create_coin_ote1_json_path(coin_mstr_dir, amy23_str)
    a45_ote1_json_path = create_coin_ote1_json_path(coin_mstr_dir, amy45_str)
    assert os_path_exists(a23_ote1_json_path) is False
    assert os_path_exists(a45_ote1_json_path) is False

    # WHEN
    etl_coin_ote1_agg_csvs_to_jsons(coin_mstr_dir)

    # THEN
    assert os_path_exists(a23_ote1_json_path)
    assert os_path_exists(a45_ote1_json_path)
    a23_ote1_dict = open_json(a23_ote1_json_path)
    a45_ote1_dict = open_json(a45_ote1_json_path)
    assert a23_ote1_dict == {bob_str: {str(timepoint55): event3}}
    assert a45_ote1_dict == {
        sue_str: {str(timepoint55): event3, str(timepoint66): event7}
    }
