from src.f00_instrument.db_toolbox import get_row_count, db_table_exists
from src.f01_road.deal import time_int_str
from src.f04_gift.atom_config import fiscal_title_str
from src.f08_pidgin.pidgin_config import event_int_str
from src.f10_etl.fiscal_etl_tool import FiscalPrimeObjsRef
from src.f10_etl.transformers import (
    create_fiscal_tables,
    fiscal_agg_tables2fiscal_event_time_agg,
)
from sqlite3 import connect as sqlite3_connect


def test_fiscal_agg_tables2fiscal_event_time_agg_SetsTableAttr():
    # ESTABLISH
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
INSERT INTO {x_fis.deal_stage_tablename} ({event_int_str()}, {fiscal_title_str()}, {time_int_str()})
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
INSERT INTO {x_fis.deal_stage_tablename} ({event_int_str()}, {fiscal_title_str()}, {time_int_str()})
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
        ex_row0 = (accord23_str, event3, timepoint55, "sorted")
        ex_row1 = (accord45_str, event3, timepoint55, "sorted")
        ex_row2 = (accord45_str, event7, timepoint66, "sorted")
        ex_row3 = (accord55_str, event3, timepoint55, "sorted")
        ex_row4 = (accord55_str, event3, timepoint77, "sorted")
        ex_row5 = (accord55_str, event7, timepoint77, "sorted")
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


def test_fiscal_agg_tables2fiscal_event_time_agg_SetsTableAttr():
    # ESTABLISH
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
INSERT INTO {x_fis.deal_stage_tablename} ({event_int_str()}, {fiscal_title_str()}, {time_int_str()})
VALUES
  ({event3}, '{accord23_str}', {timepoint66})
, ({event7}, '{accord23_str}', {timepoint55})
, ({event3}, '{accord45_str}', {timepoint55})
, ({event3}, '{accord45_str}', {timepoint55})
;
"""
        cursor.execute(insert_staging_sqlstr)
        fiscal_event_time_agg_str = "fiscal_event_time_agg"
        assert db_table_exists(cursor, fiscal_event_time_agg_str) is False

        # WHEN
        fiscal_agg_tables2fiscal_event_time_agg(cursor)

        # THEN
        assert db_table_exists(cursor, fiscal_event_time_agg_str)
        assert get_row_count(cursor, fiscal_event_time_agg_str) == 3
        cursor.execute(
            f"""
SELECT 
  {fiscal_title_str()}
, {event_int_str()}
, {time_int_str()}
, error_message 
FROM {fiscal_event_time_agg_str}
;
"""
        )
        fiscalunit_agg_rows = cursor.fetchall()
        ex_row0 = (accord23_str, event3, timepoint66, "sorted")
        ex_row1 = (accord23_str, event7, timepoint55, "not sorted")
        ex_row2 = (accord45_str, event3, timepoint55, "sorted")
        print(f"{fiscalunit_agg_rows[0]=}")
        print(f"{fiscalunit_agg_rows[1]=}")
        print(f"{fiscalunit_agg_rows[2]=}")
        assert fiscalunit_agg_rows == [ex_row0, ex_row1, ex_row2]
