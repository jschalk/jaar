from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import db_table_exists, get_row_count
from src.ch18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.ch18_etl_toolbox.transformers import (
    create_sound_and_heard_tables,
    etl_heard_raw_tables_to_moment_ote1_agg,
)
from src.ref.ch18_keywords import Ch18Keywords as wx


def test_etl_heard_raw_tables_to_moment_ote1_agg_SetsTableAttr():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event3 = 3
    event7 = 7
    amy23_str = "amy23"
    amy45_str = "amy45"
    amy55_str = "amy55"
    timepoint55 = 55
    timepoint66 = 66
    timepoint77 = 77
    with sqlite3_connect(":memory:") as moment_db_conn:
        cursor = moment_db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        momentbud_h_raw_table = create_prime_tablename(wx.moment_budunit, "h", "raw")
        insert_raw_sqlstr = f"""
INSERT INTO {momentbud_h_raw_table} ({wx.event_int}, {wx.moment_label}_inx, {wx.belief_name}_inx, {wx.bud_time})
VALUES
  ({event3}, '{amy23_str}', '{bob_str}', {timepoint55})
, ({event3}, '{amy23_str}', '{bob_str}', {timepoint55})
, ({event3}, '{amy45_str}', '{sue_str}', {timepoint55})
, ({event7}, '{amy45_str}', '{sue_str}', {timepoint66})
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, momentbud_h_raw_table) == 4
        assert db_table_exists(cursor, wx.moment_ote1_agg) is False

        # WHEN
        etl_heard_raw_tables_to_moment_ote1_agg(cursor)

        # THEN
        assert db_table_exists(cursor, wx.moment_ote1_agg)
        assert get_row_count(cursor, wx.moment_ote1_agg) == 3
        cursor.execute(f"SELECT * FROM {wx.moment_ote1_agg};")
        momentunit_agg_rows = cursor.fetchall()
        ex_row0 = (amy23_str, bob_str, event3, timepoint55, None)
        ex_row1 = (amy45_str, sue_str, event3, timepoint55, None)
        ex_row2 = (amy45_str, sue_str, event7, timepoint66, None)
        print(f"{momentunit_agg_rows[0]=}")
        print(f"{momentunit_agg_rows[1]=}")
        print(f"{momentunit_agg_rows[2]=}")
        assert momentunit_agg_rows == [ex_row0, ex_row1, ex_row2]
