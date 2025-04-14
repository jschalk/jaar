from src.f00_data_toolboxs.db_toolbox import get_row_count
from src.f00_data_toolboxs.file_toolbox import open_file, set_dir
from src.f01_road.deal import deal_time_str, owner_name_str, fisc_title_str
from src.f04_pack.atom_config import event_int_str
from src.f06_listen.hub_path import (
    create_fisc_dir_path,
    create_fisc_ote1_csv_path,
    create_fisc_owners_dir_path,
)
from src.f11_etl.transformers import create_fisc_tables
from src.f11_etl.transformers import (
    etl_fisc_agg_tables2fisc_ote1_agg,
    etl_fisc_table2fisc_ote1_agg_csvs,
)
from src.f11_etl.examples.etl_env import env_dir_setup_cleanup, get_test_etl_dir
from sqlite3 import connect as sqlite3_connect
from os.path import exists as os_path_exists


def test_etl_fisc_table2fisc_ote1_agg_csvs_Scenaro1_SetsTableAttr(
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
    fisc_mstr_dir = get_test_etl_dir()
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        etl_fisc_agg_tables2fisc_ote1_agg(cursor)
        fisc_ote1_agg_str = "fisc_ote1_agg"
        insert_staging_sqlstr = f"""
INSERT INTO {fisc_ote1_agg_str} ({event_int_str()}, {fisc_title_str()}, {owner_name_str()}, {deal_time_str()})
VALUES
  ({event3}, '{accord23_str}', '{bob_str}', {timepoint55})
, ({event3}, '{accord45_str}', '{sue_str}', {timepoint55})
, ({event7}, '{accord45_str}', '{sue_str}', {timepoint66})
;
"""
        cursor.execute(insert_staging_sqlstr)
        a23_event_time_p = create_fisc_ote1_csv_path(fisc_mstr_dir, accord23_str)
        a45_event_time_p = create_fisc_ote1_csv_path(fisc_mstr_dir, accord45_str)
        assert get_row_count(cursor, fisc_ote1_agg_str) == 3
        assert os_path_exists(a23_event_time_p) is False
        assert os_path_exists(a45_event_time_p) is False

        # WHEN
        etl_fisc_table2fisc_ote1_agg_csvs(cursor, fisc_mstr_dir)

    # THEN
    assert os_path_exists(a23_event_time_p)
    assert os_path_exists(a45_event_time_p)
    # idea_types = get_idea_sqlite_types()
    # a23_event_time_csv = open_csv_with_types(a23_event_time_p, idea_types)
    # a45_event_time_csv = open_csv_with_types(a45_event_time_p, idea_types)
    a23_event_time_csv = open_file(a23_event_time_p)
    a45_event_time_csv = open_file(a45_event_time_p)
    #         expected_a23_event_time_csv = f"""{event_int_str()}, {fisc_title_str()}, {owner_name_str()}, {deal_time_str()}
    #   '{accord23_str}', '{bob_str}', {event3}, {timepoint55}, NULL)
    # , '{accord45_str}', '{sue_str}', {event3}, {timepoint55}, NULL)
    # , '{accord45_str}', '{sue_str}', {event7}, {timepoint66}, NULL)
    # ;
    # """
    expected_a23_event_time_csv = f"""{fisc_title_str()},{owner_name_str()},{event_int_str()},{deal_time_str()},error_message
{accord23_str},{bob_str},{event3},{timepoint55},
"""
    expected_a45_event_time_csv = f"""{fisc_title_str()},{owner_name_str()},{event_int_str()},{deal_time_str()},error_message
{accord45_str},{sue_str},{event3},{timepoint55},
{accord45_str},{sue_str},{event7},{timepoint66},
"""
    assert a23_event_time_csv == expected_a23_event_time_csv
    assert a45_event_time_csv == expected_a45_event_time_csv


def test_etl_fisc_table2fisc_ote1_agg_csvs_Scenaro2_ote1_agg_TableIsEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    event3 = 3
    accord23_str = "accord23"
    accord45_str = "accord45"
    timepoint55 = 55
    fisc_mstr_dir = get_test_etl_dir()
    a45_fisc_dir = create_fisc_dir_path(fisc_mstr_dir, accord45_str)
    print(f"{a45_fisc_dir=}")
    set_dir(a45_fisc_dir)
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)
        etl_fisc_agg_tables2fisc_ote1_agg(cursor)
        fisc_ote1_agg_str = "fisc_ote1_agg"
        insert_staging_sqlstr = f"""
INSERT INTO {fisc_ote1_agg_str} ({event_int_str()}, {fisc_title_str()}, {owner_name_str()}, {deal_time_str()})
VALUES
  ({event3}, '{accord23_str}', '{bob_str}', {timepoint55})
;
"""
        cursor.execute(insert_staging_sqlstr)
        a23_event_time_p = create_fisc_ote1_csv_path(fisc_mstr_dir, accord23_str)
        a45_event_time_p = create_fisc_ote1_csv_path(fisc_mstr_dir, accord45_str)
        assert get_row_count(cursor, fisc_ote1_agg_str) == 1
        assert os_path_exists(a23_event_time_p) is False
        assert os_path_exists(a45_event_time_p) is False

        # WHEN
        etl_fisc_table2fisc_ote1_agg_csvs(cursor, fisc_mstr_dir)

    # THEN
    assert os_path_exists(a23_event_time_p)
    assert os_path_exists(a45_event_time_p)
    # idea_types = get_idea_sqlite_types()
    # a23_event_time_csv = open_csv_with_types(a23_event_time_p, idea_types)
    # a45_event_time_csv = open_csv_with_types(a45_event_time_p, idea_types)
    a23_event_time_csv = open_file(a23_event_time_p)
    a45_event_time_csv = open_file(a45_event_time_p)
    #         expected_a23_event_time_csv = f"""{event_int_str()}, {fisc_title_str()}, {owner_name_str()}, agg_time
    #   '{accord23_str}', '{bob_str}', {event3}, {timepoint55}, NULL)
    # , '{accord45_str}', '{sue_str}', {event3}, {timepoint55}, NULL)
    # , '{accord45_str}', '{sue_str}', {event7}, {timepoint66}, NULL)
    # ;
    # """
    expected_a23_event_time_csv = f"""{fisc_title_str()},{owner_name_str()},{event_int_str()},{deal_time_str()},error_message
{accord23_str},{bob_str},{event3},{timepoint55},
"""
    expected_a45_event_time_csv = f"""{fisc_title_str()},{owner_name_str()},{event_int_str()},{deal_time_str()},error_message
"""
    assert a23_event_time_csv == expected_a23_event_time_csv
    assert a45_event_time_csv == expected_a45_event_time_csv
