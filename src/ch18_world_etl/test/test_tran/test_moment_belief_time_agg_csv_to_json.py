from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import open_json, save_file
from src.ch18_world_etl._ref.ch18_path import (
    create_moment_ote1_csv_path,
    create_moment_ote1_json_path,
)
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ch18_world_etl.transformers import etl_moment_ote1_agg_csvs_to_jsons
from src.ref.keywords import Ch18Keywords as kw


def test_etl_moment_ote1_agg_csvs_to_jsons_CreatesFile_Scenaro0(
    temp_dir_setup,
):
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    spark3 = 3
    spark7 = 7
    amy23_str = "amy23"
    amy45_str = "amy45"
    epochtime55 = 55
    epochtime66 = 66
    moment_mstr_dir = get_temp_dir()
    a23_spark_time_p = create_moment_ote1_csv_path(moment_mstr_dir, amy23_str)
    a45_spark_time_p = create_moment_ote1_csv_path(moment_mstr_dir, amy45_str)
    a23_spark_time_csv = f"""{kw.moment_label},{kw.belief_name},{kw.spark_num},{kw.bud_time},{kw.error_message}
{amy23_str},{bob_str},{spark3},{epochtime55},
"""
    a45_spark_time_csv = f"""{kw.moment_label},{kw.belief_name},{kw.spark_num},{kw.bud_time},{kw.error_message}
{amy45_str},{sue_str},{spark3},{epochtime55},
{amy45_str},{sue_str},{spark7},{epochtime66},
"""
    save_file(a23_spark_time_p, None, a23_spark_time_csv)
    save_file(a45_spark_time_p, None, a45_spark_time_csv)
    assert os_path_exists(a23_spark_time_p)
    assert os_path_exists(a45_spark_time_p)
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
    assert a23_ote1_dict == {bob_str: {str(epochtime55): spark3}}
    assert a45_ote1_dict == {
        sue_str: {str(epochtime55): spark3, str(epochtime66): spark7}
    }
