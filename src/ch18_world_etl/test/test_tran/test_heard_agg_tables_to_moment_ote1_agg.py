from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import db_table_exists, get_row_count
from src.ch18_world_etl.tran_sqlstrs import create_prime_tablename
from src.ch18_world_etl.transformers import (
    create_sound_and_heard_tables,
    etl_heard_raw_tables_to_moment_ote1_agg,
)
from src.ref.keywords import Ch18Keywords as kw


def test_etl_heard_raw_tables_to_moment_ote1_agg_SetsTableAttr():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    spark3 = 3
    spark7 = 7
    amy23_str = "amy23"
    amy45_str = "amy45"
    amy55_str = "amy55"
    epochtime55 = 55
    epochtime66 = 66
    epochtime77 = 77
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        momentbud_h_raw_table = create_prime_tablename(kw.moment_budunit, "h", "raw")
        insert_raw_sqlstr = f"""
INSERT INTO {momentbud_h_raw_table} ({kw.spark_num}, {kw.moment_label}_inx, {kw.belief_name}_inx, {kw.bud_time})
VALUES
  ({spark3}, '{amy23_str}', '{bob_str}', {epochtime55})
, ({spark3}, '{amy23_str}', '{bob_str}', {epochtime55})
, ({spark3}, '{amy45_str}', '{sue_str}', {epochtime55})
, ({spark7}, '{amy45_str}', '{sue_str}', {epochtime66})
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, momentbud_h_raw_table) == 4
        assert db_table_exists(cursor, kw.moment_ote1_agg) is False

        # WHEN
        etl_heard_raw_tables_to_moment_ote1_agg(cursor)

        # THEN
        assert db_table_exists(cursor, kw.moment_ote1_agg)
        assert get_row_count(cursor, kw.moment_ote1_agg) == 3
        cursor.execute(f"SELECT * FROM {kw.moment_ote1_agg};")
        momentunit_agg_rows = cursor.fetchall()
        ex_row0 = (amy23_str, bob_str, spark3, epochtime55, None)
        ex_row1 = (amy45_str, sue_str, spark3, epochtime55, None)
        ex_row2 = (amy45_str, sue_str, spark7, epochtime66, None)
        print(f"{momentunit_agg_rows[0]=}")
        print(f"{momentunit_agg_rows[1]=}")
        print(f"{momentunit_agg_rows[2]=}")
        assert momentunit_agg_rows == [ex_row0, ex_row1, ex_row2]
