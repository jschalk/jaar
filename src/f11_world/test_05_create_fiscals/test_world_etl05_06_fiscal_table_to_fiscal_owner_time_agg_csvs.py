from src.f00_instrument.csv_toolbox import open_csv_with_types
from src.f00_instrument.db_toolbox import get_row_count
from src.f00_instrument.file import open_file
from src.f01_road.deal import time_int_str
from src.f04_gift.atom_config import fiscal_title_str, owner_name_str
from src.f05_listen.hub_paths import create_fiscal_owner_time_csv_path
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.idea_config import get_idea_sqlite_types
from src.f10_etl.transformers import create_fiscal_tables
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect
from os.path import exists as os_path_exists


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
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        cursor = fiscal_db_conn.cursor()
        create_fiscal_tables(cursor)
        fizz_world.fiscal_agg_tables2fiscal_owner_time_agg(cursor)
        fiscal_owner_time_agg_str = "fiscal_owner_time_agg"
        insert_staging_sqlstr = f"""
INSERT INTO {fiscal_owner_time_agg_str} ({event_int_str()}, {fiscal_title_str()}, {owner_name_str()}, {time_int_str()})
VALUES
  ({event3}, '{accord23_str}', '{bob_str}', {timepoint55})
, ({event3}, '{accord45_str}', '{sue_str}', {timepoint55})
, ({event7}, '{accord45_str}', '{sue_str}', {timepoint66})
;
"""
        cursor.execute(insert_staging_sqlstr)
        fiscal_mstr_dir = fizz_world._fiscal_mstr_dir
        a23_event_time_p = create_fiscal_owner_time_csv_path(
            fiscal_mstr_dir, accord23_str
        )
        a45_event_time_p = create_fiscal_owner_time_csv_path(
            fiscal_mstr_dir, accord45_str
        )
        assert get_row_count(cursor, fiscal_owner_time_agg_str) == 3
        assert os_path_exists(a23_event_time_p) is False
        assert os_path_exists(a45_event_time_p) is False

        # WHEN
        fizz_world.fiscal_table2fiscal_owner_time_agg_csvs(cursor)

    # THEN
    assert os_path_exists(a23_event_time_p)
    assert os_path_exists(a45_event_time_p)
    # idea_types = get_idea_sqlite_types()
    # a23_event_time_csv = open_csv_with_types(a23_event_time_p, idea_types)
    # a45_event_time_csv = open_csv_with_types(a45_event_time_p, idea_types)
    a23_event_time_csv = open_file(a23_event_time_p)
    a45_event_time_csv = open_file(a45_event_time_p)
    #         expected_a23_event_time_csv = f"""{event_int_str()}, {fiscal_title_str()}, {owner_name_str()}, {time_int_str()}
    #   '{accord23_str}', '{bob_str}', {event3}, {timepoint55}, NULL)
    # , '{accord45_str}', '{sue_str}', {event3}, {timepoint55}, NULL)
    # , '{accord45_str}', '{sue_str}', {event7}, {timepoint66}, NULL)
    # ;
    # """
    expected_a23_event_time_csv = f"""{fiscal_title_str()},{owner_name_str()},{event_int_str()},{time_int_str()},error_message
{accord23_str},{bob_str},{event3},{timepoint55},
"""
    expected_a45_event_time_csv = f"""{fiscal_title_str()},{owner_name_str()},{event_int_str()},{time_int_str()},error_message
{accord45_str},{sue_str},{event3},{timepoint55},
{accord45_str},{sue_str},{event7},{timepoint66},
"""
    assert a23_event_time_csv == expected_a23_event_time_csv
    assert a45_event_time_csv == expected_a45_event_time_csv
