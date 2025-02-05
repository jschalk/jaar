from src.f00_instrument.file import open_file
from src.f00_instrument.db_toolbox import get_row_count, db_table_exists
from src.f01_road.deal import bridge_str
from src.f03_chrono.chrono import (
    c400_number_str,
    yr1_jan1_offset_str,
    monthday_distortion_str,
    timeline_title_str,
)
from src.f04_gift.atom_config import (
    fiscal_title_str,
    fund_coin_str,
    penny_str,
    respect_bit_str,
)
from src.f07_fiscal.fiscal_config import present_time_str
from src.f10_etl.fiscal_etl_tool import (
    FiscalPrimeObjsRef,
    FiscalPrimeColumnsRef,
)
from src.f10_etl.transformers import (
    create_fiscal_tables,
    fiscal_agg_tables2fiscal_event_time_agg,
    etl_fiscal_agg_tables_to_fiscal_csvs,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir
from sqlite3 import connect as sqlite3_connect
from os.path import exists as os_path_exists


def test_fiscal_agg_tables2fiscal_event_time_agg_PassesOnly_fiscal_title():
    # ESTABLISH
    sue_inx = "Suzy"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    accord55_str = "accord55"
    timepoint55 = 55
    timepoint66 = 66
    timepoint77 = 77
    with sqlite3_connect(":memory:") as fiscal_db_conn:
        cursor = fiscal_db_conn.cursor()
        create_fiscal_tables(cursor)

        x_fis = FiscalPrimeObjsRef()
        insert_staging_sqlstr = f"""
INSERT INTO {x_fis.deal_stage_tablename} (event_int, fiscal_title, time_int)
VALUES
  ({event3}, '{accord23_str}', {timepoint55})
, ({event3}, '{accord23_str}', {timepoint55})
, ({event3}, '{accord45_str}', {timepoint55})
, ({event7}, '{accord45_str}', {timepoint66})
;
"""
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(cursor, x_fis.deal_stage_tablename) == 4
        insert_staging_sqlstr = f"""
INSERT INTO {x_fis.cash_stage_tablename} (event_int, fiscal_title, time_int)
VALUES
  ({event3}, '{accord55_str}', {timepoint55})
, ({event3}, '{accord55_str}', {timepoint55})
, ({event3}, '{accord55_str}', {timepoint77})
, ({event7}, '{accord55_str}', {timepoint77})
;
"""
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(cursor, x_fis.deal_stage_tablename) == 4
        assert get_row_count(cursor, x_fis.cash_stage_tablename) == 4
        fiscal_event_time_agg_str = "fiscal_event_time_agg"
        assert db_table_exists(cursor, fiscal_event_time_agg_str) is False

        # WHEN
        fiscal_agg_tables2fiscal_event_time_agg(cursor)

        # THEN
        assert db_table_exists(cursor, fiscal_event_time_agg_str)
        assert get_row_count(cursor, fiscal_event_time_agg_str) == 6
        cursor.execute(f"SELECT * FROM {fiscal_event_time_agg_str};")
        fiscalunit_agg_rows = cursor.fetchall()
        ex_row0 = (accord23_str, event3, timepoint55)
        ex_row1 = (accord45_str, event3, timepoint55)
        ex_row2 = (accord45_str, event7, timepoint66)
        ex_row3 = (accord55_str, event3, timepoint55)
        ex_row4 = (accord55_str, event3, timepoint77)
        ex_row5 = (accord55_str, event7, timepoint77)
        print(f"{fiscalunit_agg_rows[0]=}")
        print(f"{fiscalunit_agg_rows[1]=}")
        print(f"{fiscalunit_agg_rows[2]=}")
        print(f"{fiscalunit_agg_rows[3]=}")
        print(f"{fiscalunit_agg_rows[4]=}")
        print(f"{fiscalunit_agg_rows[5]=}")
        assert fiscalunit_agg_rows == [
            ex_row0,
            ex_row1,
            ex_row2,
            ex_row3,
            ex_row4,
            ex_row5,
        ]
