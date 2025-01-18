from src.f00_instrument.file import create_path, save_file, open_file
from src.f00_instrument.db_toolbox import (
    db_table_exists,
    get_row_count,
    create_table_from_columns,
)
from src.f01_road.finance_tran import bridge_str, quota_str, time_int_str
from src.f03_chrono.chrono import (
    c400_number_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
    timeline_title_str,
)
from src.f04_gift.atom_config import (
    acct_name_str,
    face_name_str,
    fiscal_title_str,
    owner_name_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.f07_fiscal.fiscal_config import (
    get_fiscal_config_args,
    fiscalunit_str,
    fiscal_deal_episode_str,
    fiscal_cashbook_str,
    fiscal_timeline_hour_str,
    fiscal_timeline_month_str,
    fiscal_timeline_weekday_str,
    present_time_str,
    amount_str,
    hour_title_str,
    cumlative_minute_str,
    cumlative_day_str,
    month_title_str,
    weekday_order_str,
    weekday_title_str,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.idea_config import idea_number_str, get_idea_sqlite_types
from src.f09_idea.pandas_tool import get_pragma_table_fetchall, get_custom_sorted_list
from src.f10_etl.fiscal_etl_tool import (
    FiscalPrimeObjsRef,
    FiscalPrimeColumnsRef,
)
from src.f10_etl.transformers import (
    etl_aft_face_csv_files_to_fiscal_db,
    create_fiscal_tables,
    idea_staging_tables2fiscal_staging_tables,
    fiscal_staging_tables2fiscal_agg_tables,
    etl_fiscal_staging_tables_to_fiscal_csvs,
    etl_fiscal_agg_tables_to_fiscal_csvs,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect, Connection as sqlite3_Connection
from copy import copy as copy_copy
from os.path import exists as os_path_exists


def test_fiscal_staging_tables2fiscal_agg_tables_PopulatesFiscalAggTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    br00011_str = "br00011"
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)

        cursor = fiscal_db_conn.cursor()
        x_fis = FiscalPrimeObjsRef()
        insert_staging_sqlstr = f"""
INSERT INTO {x_fis.unit_stage_tablename} (idea_number, face_name, event_int, fiscal_title)
VALUES 
  ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord23_str}')
, ('{br00011_str}', '{sue_inx}', {event3}, '{accord45_str}')
, ('{br00011_str}', '{sue_inx}', {event7}, '{accord45_str}')
;
"""
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(fiscal_db_conn, x_fis.unit_stage_tablename) == 4
        assert get_row_count(fiscal_db_conn, x_fis.unit_agg_tablename) == 0

        # WHEN
        fiscal_staging_tables2fiscal_agg_tables(fiscal_db_conn)

        # THEN
        assert get_row_count(fiscal_db_conn, x_fis.unit_agg_tablename) == 2
        cursor.execute(f"SELECT * FROM {x_fis.unit_agg_tablename};")
        fiscalunit_agg_rows = cursor.fetchall()
        expected_row0 = (
            accord23_str,  # fiscal_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # present_time
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
        )
        expected_row1 = (
            accord45_str,  # fiscal_title
            None,  # fund_coin
            None,  # penny
            None,  # respect_bit
            None,  # present_time
            None,  # bridge
            None,  # c400_number
            None,  # yr1_jan1_offset
            None,  # monthday_distortion
            None,  # timeline_title
        )
        print(f"{fiscalunit_agg_rows[0]=}")
        print(f"      {expected_row0=}")
        assert fiscalunit_agg_rows == [expected_row0, expected_row1]


def test_etl_fiscal_agg_tables_to_fiscal_csvs_CreateFiles(env_dir_setup_cleanup):
    # sourcery skip: extract-method
    # ESTABLISH
    accord23_str = "accord23"
    accord45_str = "accord45"
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        create_fiscal_tables(fiscal_db_conn)
        cursor = fiscal_db_conn.cursor()
        fiscal_mstr_dir = get_test_etl_dir()
        x_fis = FiscalPrimeObjsRef(fiscal_mstr_dir)
        insert_agg_sqlstr = f"""
INSERT INTO {x_fis.unit_agg_tablename} ({fiscal_title_str()})
VALUES ('{accord23_str}'), ('{accord45_str}')
;
"""
        cursor.execute(insert_agg_sqlstr)
        assert os_path_exists(x_fis.unit_agg_csv_path) is False
        assert os_path_exists(x_fis.deal_agg_csv_path) is False
        assert os_path_exists(x_fis.cash_agg_csv_path) is False
        assert os_path_exists(x_fis.hour_agg_csv_path) is False
        assert os_path_exists(x_fis.mont_agg_csv_path) is False
        assert os_path_exists(x_fis.week_agg_csv_path) is False

        # WHEN
        etl_fiscal_agg_tables_to_fiscal_csvs(fiscal_db_conn, fiscal_mstr_dir)

        # THEN
        assert os_path_exists(x_fis.unit_agg_csv_path)
        assert os_path_exists(x_fis.deal_agg_csv_path)
        assert os_path_exists(x_fis.cash_agg_csv_path)
        assert os_path_exists(x_fis.hour_agg_csv_path)
        assert os_path_exists(x_fis.mont_agg_csv_path)
        assert os_path_exists(x_fis.week_agg_csv_path)
        unit_agg_csv_filename = x_fis.unit_agg_csv_filename
        generated_fiscalunit_csv = open_file(fiscal_mstr_dir, unit_agg_csv_filename)
        expected_fiscalunit_csv_str = f"""{fiscal_title_str()},{fund_coin_str()},{penny_str()},{respect_bit_str()},{present_time_str()},{bridge_str()},{c400_number_str()},{yr1_jan1_offset_str()},{monthday_distortion_str()},{timeline_title_str()}
{accord23_str},,,,,,,,,
{accord45_str},,,,,,,,,
"""
        assert generated_fiscalunit_csv == expected_fiscalunit_csv_str
