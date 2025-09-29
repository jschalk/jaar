from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import db_table_exists, get_row_count
from src.ch18_etl_toolbox._ref.ch18_keywords import (
    Ch11Keywords as wx,
    belief_name_str,
    event_int_str,
    moment_budunit_str,
    moment_label_str,
    moment_ote1_agg_str,
)
from src.ch18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.ch18_etl_toolbox.transformers import (
    create_sound_and_heard_tables,
    etl_heard_raw_tables_to_moment_ote1_agg,
)


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
        momentbud_h_raw_table = create_prime_tablename(moment_budunit_str(), "h", "raw")
        insert_raw_sqlstr = f"""
INSERT INTO {momentbud_h_raw_table} ({event_int_str()}, {moment_label_str()}_inx, {belief_name_str()}_inx, {wx.bud_time})
VALUES
  ({event3}, '{amy23_str}', '{bob_str}', {timepoint55})
, ({event3}, '{amy23_str}', '{bob_str}', {timepoint55})
, ({event3}, '{amy45_str}', '{sue_str}', {timepoint55})
, ({event7}, '{amy45_str}', '{sue_str}', {timepoint66})
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, momentbud_h_raw_table) == 4
        assert db_table_exists(cursor, moment_ote1_agg_str()) is False

        # WHEN
        etl_heard_raw_tables_to_moment_ote1_agg(cursor)

        # THEN
        assert db_table_exists(cursor, moment_ote1_agg_str())
        assert get_row_count(cursor, moment_ote1_agg_str()) == 3
        cursor.execute(f"SELECT * FROM {moment_ote1_agg_str()};")
        momentunit_agg_rows = cursor.fetchall()
        ex_row0 = (amy23_str, bob_str, event3, timepoint55, None)
        ex_row1 = (amy45_str, sue_str, event3, timepoint55, None)
        ex_row2 = (amy45_str, sue_str, event7, timepoint66, None)
        print(f"{momentunit_agg_rows[0]=}")
        print(f"{momentunit_agg_rows[1]=}")
        print(f"{momentunit_agg_rows[2]=}")
        assert momentunit_agg_rows == [ex_row0, ex_row1, ex_row2]
