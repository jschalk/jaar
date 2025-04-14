from src.a00_data_toolboxs.db_toolbox import get_row_count, db_table_exists
from src.f02_finance_toolboxs.deal import deal_time_str, owner_name_str, fisc_title_str
from src.f04_pack.atom_config import event_int_str
from src.f11_etl.fisc_etl_tool import FiscPrimeObjsRef
from src.f11_etl.transformers import (
    create_fisc_tables,
    etl_fisc_agg_tables2fisc_ote1_agg,
)
from sqlite3 import connect as sqlite3_connect


def test_etl_fisc_agg_tables2fisc_ote1_agg_SetsTableAttr():
    # ESTABLISH
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
        etl_fisc_agg_tables2fisc_ote1_agg(cursor)

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


# def test_etl_fisc_agg_tables2fisc_ote1_agg_SetsTableAttr():
#     # ESTABLISH
#     event3 = 3
#     event7 = 7
#     accord23_str = "accord23"
#     accord45_str = "accord45"
#     accord55_str = "accord55"
#     timepoint55 = 55
#     timepoint66 = 66
#     timepoint77 = 77
#     with sqlite3_connect(":memory:") as fisc_db_conn:
#         cursor = fisc_db_conn.cursor()
#         create_fisc_tables(cursor)

#         x_fisc = FiscPrimeObjsRef()
#         insert_staging_sqlstr = f"""
# INSERT INTO {x_fisc.deal_stage_tablename} ({event_int_str()}, {fisc_title_str()}, {deal_time_str()})
# VALUES
#   ({event3}, '{accord23_str}', {timepoint66})
# , ({event7}, '{accord23_str}', {timepoint55})
# , ({event3}, '{accord45_str}', {timepoint55})
# , ({event3}, '{accord45_str}', {timepoint55})
# ;
# """
#         cursor.execute(insert_staging_sqlstr)
#         fisc_ote1_agg_str = "fisc_ote1_agg"
#         assert db_table_exists(cursor, fisc_ote1_agg_str) is False

#         # WHEN
#         etl_fisc_agg_tables2fisc_ote1_agg(cursor)

#         # THEN
#         assert db_table_exists(cursor, fisc_ote1_agg_str)
#         assert get_row_count(cursor, fisc_ote1_agg_str) == 3
#         cursor.execute(
#             f"SELECT {event_int_str()}, {fisc_title_str()}, {deal_time_str()}, error_message FROM {fisc_ote1_agg_str};"
#         )
#         fiscunit_agg_rows = cursor.fetchall()
#         ex_row0 = (accord23_str, event3, timepoint66, "sorted")
#         ex_row1 = (accord23_str, event7, timepoint55, "not sorted")
#         ex_row2 = (accord45_str, event3, timepoint55, "sorted")
#         print(f"{fiscunit_agg_rows[0]=}")
#         print(f"{fiscunit_agg_rows[1]=}")
#         print(f"{fiscunit_agg_rows[2]=}")
#         assert fiscunit_agg_rows == [ex_row0, ex_row1, ex_row2]
