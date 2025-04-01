from src.f00_instrument.db_toolbox import get_row_count, db_table_exists
from src.f01_road.deal import deal_time_str, owner_name_str, fisc_title_str
from src.f04_vow.atom_config import event_int_str
from src.f10_etl.fisc_etl_tool import FiscPrimeObjsRef
from src.f10_etl.transformers import create_fisc_tables
from src.f11_world.world import worldunit_shop
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_fisc_agg_tables2fisc_ote1_agg_Scenaro0_SetsTableAttr():
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)

        x_fisc = FiscPrimeObjsRef()
        assert get_row_count(cursor, x_fisc.deal_stage_tablename) == 0
        fisc_ote1_agg_str = "fisc_ote1_agg"
        assert db_table_exists(cursor, fisc_ote1_agg_str) is False

        # WHEN
        fizz_world.fisc_agg_tables2fisc_ote1_agg(cursor)

        # THEN
        assert db_table_exists(cursor, fisc_ote1_agg_str)
        assert get_row_count(cursor, fisc_ote1_agg_str) == 0


def test_WorldUnit_fisc_agg_tables2fisc_ote1_agg_Scenaro1_SetsTableAttr():
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    bob_str = "Bob"
    sue_str = "Sue"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    accord55_str = "accord55"
    timepoint55 = 55
    timepoint66 = 66
    timepoint77 = 77
    with sqlite3_connect(":memory:") as fisc_db_conn:
        cursor = fisc_db_conn.cursor()
        create_fisc_tables(cursor)

        x_fisc = FiscPrimeObjsRef()
        insert_staging_sqlstr = f"""
INSERT INTO {x_fisc.deal_stage_tablename} ({event_int_str()}, {fisc_title_str()}, {owner_name_str()}, {deal_time_str()})
VALUES
  ({event3}, '{accord23_str}', '{bob_str}', {timepoint55})
, ({event3}, '{accord23_str}', '{bob_str}', {timepoint55})
, ({event3}, '{accord45_str}', '{sue_str}', {timepoint55})
, ({event7}, '{accord45_str}', '{sue_str}', {timepoint66})
;
"""
        cursor.execute(insert_staging_sqlstr)
        assert get_row_count(cursor, x_fisc.deal_stage_tablename) == 4
        fisc_ote1_agg_str = "fisc_ote1_agg"
        assert db_table_exists(cursor, fisc_ote1_agg_str) is False

        # WHEN
        fizz_world.fisc_agg_tables2fisc_ote1_agg(cursor)

        # THEN
        assert db_table_exists(cursor, fisc_ote1_agg_str)
        assert get_row_count(cursor, fisc_ote1_agg_str) == 3
        cursor.execute(f"SELECT * FROM {fisc_ote1_agg_str};")
        fiscunit_agg_rows = cursor.fetchall()
        ex_row0 = (accord23_str, bob_str, event3, timepoint55, None)
        ex_row1 = (accord45_str, sue_str, event3, timepoint55, None)
        ex_row2 = (accord45_str, sue_str, event7, timepoint66, None)
        print(f"{fiscunit_agg_rows[0]=}")
        print(f"{fiscunit_agg_rows[1]=}")
        print(f"{fiscunit_agg_rows[2]=}")
        assert fiscunit_agg_rows == [ex_row0, ex_row1, ex_row2]
