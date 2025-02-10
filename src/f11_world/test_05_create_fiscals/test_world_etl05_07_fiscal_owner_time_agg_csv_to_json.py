from src.f00_instrument.dict_toolbox import get_dict_from_json
from src.f00_instrument.file import open_file, save_file
from src.f01_road.deal import time_int_str
from src.f04_gift.atom_config import fiscal_title_str, owner_name_str
from src.f05_listen.hub_paths import (
    create_fiscal_owner_time_csv_path,
    create_fiscal_owner_time_json_path,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.idea_config import get_idea_sqlite_types
from src.f10_etl.transformers import create_fiscal_tables
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect
from os.path import exists as os_path_exists

# open_fiscal_owner_time_agg(path)-> dict[tuple(OwnerName, TimePiont), EventInt]


def test_WorldUnit_fiscal_table2fiscal_owner_time_agg_csvs_Scenaro1_SetsTableAttr(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    bob_str = "Bob"
    sue_str = "Sue"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    timepoint55 = 55
    timepoint66 = 66
    fiscal_mstr_dir = fizz_world._fiscal_mstr_dir
    a23_event_time_p = create_fiscal_owner_time_csv_path(fiscal_mstr_dir, accord23_str)
    a45_event_time_p = create_fiscal_owner_time_csv_path(fiscal_mstr_dir, accord45_str)
    a23_event_time_csv = f"""{fiscal_title_str()},{owner_name_str()},{event_int_str()},{time_int_str()},error_message
{accord23_str},{bob_str},{event3},{timepoint55},
"""
    a45_event_time_csv = f"""{fiscal_title_str()},{owner_name_str()},{event_int_str()},{time_int_str()},error_message
{accord45_str},{sue_str},{event3},{timepoint55},
{accord45_str},{sue_str},{event7},{timepoint66},
"""
    save_file(a23_event_time_p, None, a23_event_time_csv)
    save_file(a45_event_time_p, None, a45_event_time_csv)
    assert os_path_exists(a23_event_time_p)
    assert os_path_exists(a45_event_time_p)
    a23_event_time_json_path = create_fiscal_owner_time_json_path(
        fiscal_mstr_dir, accord23_str
    )
    a45_event_time_json_path = create_fiscal_owner_time_json_path(
        fiscal_mstr_dir, accord45_str
    )
    assert os_path_exists(a23_event_time_json_path) is False
    assert os_path_exists(a45_event_time_json_path) is False

    # WHEN
    fizz_world.fiscal_owner_time_agg_csvs2jsons()

    # THEN
    assert os_path_exists(a23_event_time_json_path)
    assert os_path_exists(a45_event_time_json_path)
    a23_event_time_dict = get_dict_from_json(open_file(a23_event_time_json_path))
    a45_event_time_dict = get_dict_from_json(open_file(a45_event_time_json_path))
    assert a23_event_time_dict == {bob_str: {str(event3): timepoint55}}
    assert a45_event_time_dict == {
        sue_str: {str(event3): timepoint55, str(event7): timepoint66}
    }
