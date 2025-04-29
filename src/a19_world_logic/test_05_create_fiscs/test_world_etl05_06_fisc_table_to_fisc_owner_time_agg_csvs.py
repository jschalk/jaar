from src.a00_data_toolbox.db_toolbox import get_row_count
from src.a00_data_toolbox.file_toolbox import open_file
from src.a02_finance_logic._utils.strs_a02 import (
    deal_time_str,
    owner_name_str,
    fisc_tag_str,
)
from src.a06_bud_logic._utils.str_a06 import event_int_str
from src.a12_hub_tools.hub_path import create_fisc_ote1_csv_path
from src.a18_etl_toolbox.transformers import create_fisc_prime_tables
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from sqlite3 import connect as sqlite3_connect
from os.path import exists as os_path_exists


def test_WorldUnit_fisc_table2fisc_ote1_agg_csvs_Scenaro1_SetsTableAttr(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz", worlds_dir())
    bob_str = "Bob"
    sue_str = "Sue"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    timepoint55 = 55
    timepoint66 = 66
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_prime_tables(cursor)
        fizz_world.fisc_agg_tables_to_fisc_ote1_agg(cursor)
        fisc_ote1_agg_str = "fisc_ote1_agg"
        insert_raw_sqlstr = f"""
INSERT INTO {fisc_ote1_agg_str} ({event_int_str()}, {fisc_tag_str()}, {owner_name_str()}, {deal_time_str()})
VALUES
  ({event3}, '{accord23_str}', '{bob_str}', {timepoint55})
, ({event3}, '{accord45_str}', '{sue_str}', {timepoint55})
, ({event7}, '{accord45_str}', '{sue_str}', {timepoint66})
;
"""
        cursor.execute(insert_raw_sqlstr)
        fisc_mstr_dir = fizz_world._fisc_mstr_dir
        a23_event_time_p = create_fisc_ote1_csv_path(fisc_mstr_dir, accord23_str)
        a45_event_time_p = create_fisc_ote1_csv_path(fisc_mstr_dir, accord45_str)
        assert get_row_count(cursor, fisc_ote1_agg_str) == 3
        assert os_path_exists(a23_event_time_p) is False
        assert os_path_exists(a45_event_time_p) is False

        # WHEN
        fizz_world.fisc_table2fisc_ote1_agg_csvs(cursor)

    # THEN
    assert os_path_exists(a23_event_time_p)
    assert os_path_exists(a45_event_time_p)
    # idea_types = get_idea_sqlite_types()
    # a23_event_time_csv = open_csv_with_types(a23_event_time_p, idea_types)
    # a45_event_time_csv = open_csv_with_types(a45_event_time_p, idea_types)
    a23_event_time_csv = open_file(a23_event_time_p)
    a45_event_time_csv = open_file(a45_event_time_p)
    #         expected_a23_event_time_csv = f"""{event_int_str()}, {fisc_tag_str()}, {owner_name_str()}, {deal_time_str()}
    #   '{accord23_str}', '{bob_str}', {event3}, {timepoint55}, NULL)
    # , '{accord45_str}', '{sue_str}', {event3}, {timepoint55}, NULL)
    # , '{accord45_str}', '{sue_str}', {event7}, {timepoint66}, NULL)
    # ;
    # """
    expected_a23_event_time_csv = f"""{fisc_tag_str()},{owner_name_str()},{event_int_str()},{deal_time_str()},error_message
{accord23_str},{bob_str},{event3},{timepoint55},
"""
    expected_a45_event_time_csv = f"""{fisc_tag_str()},{owner_name_str()},{event_int_str()},{deal_time_str()},error_message
{accord45_str},{sue_str},{event3},{timepoint55},
{accord45_str},{sue_str},{event7},{timepoint66},
"""
    assert a23_event_time_csv == expected_a23_event_time_csv
    assert a45_event_time_csv == expected_a45_event_time_csv
