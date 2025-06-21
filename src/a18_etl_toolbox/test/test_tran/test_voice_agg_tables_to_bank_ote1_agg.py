from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import db_table_exists, get_row_count
from src.a02_finance_logic.test._util.a02_str import (
    bank_label_str,
    bud_time_str,
    owner_name_str,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str
from src.a12_hub_toolbox.test._util.a12_str import bank_ote1_agg_str
from src.a15_bank_logic.test._util.a15_str import bank_budunit_str
from src.a18_etl_toolbox.tran_sqlstrs import create_prime_tablename
from src.a18_etl_toolbox.transformers import (
    create_sound_and_voice_tables,
    etl_voice_raw_tables_to_bank_ote1_agg,
)


def test_etl_voice_raw_tables_to_bank_ote1_agg_SetsTableAttr():
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
    with sqlite3_connect(":memory:") as bank_db_conn:
        cursor = bank_db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        bankbud_v_raw_table = create_prime_tablename(bank_budunit_str(), "v", "raw")
        insert_raw_sqlstr = f"""
INSERT INTO {bankbud_v_raw_table} ({event_int_str()}, {bank_label_str()}_inx, {owner_name_str()}_inx, {bud_time_str()})
VALUES
  ({event3}, '{accord23_str}', '{bob_str}', {timepoint55})
, ({event3}, '{accord23_str}', '{bob_str}', {timepoint55})
, ({event3}, '{accord45_str}', '{sue_str}', {timepoint55})
, ({event7}, '{accord45_str}', '{sue_str}', {timepoint66})
;
"""
        cursor.execute(insert_raw_sqlstr)
        assert get_row_count(cursor, bankbud_v_raw_table) == 4
        assert db_table_exists(cursor, bank_ote1_agg_str()) is False

        # WHEN
        etl_voice_raw_tables_to_bank_ote1_agg(cursor)

        # THEN
        assert db_table_exists(cursor, bank_ote1_agg_str())
        assert get_row_count(cursor, bank_ote1_agg_str()) == 3
        cursor.execute(f"SELECT * FROM {bank_ote1_agg_str()};")
        bankunit_agg_rows = cursor.fetchall()
        ex_row0 = (accord23_str, bob_str, event3, timepoint55, None)
        ex_row1 = (accord45_str, sue_str, event3, timepoint55, None)
        ex_row2 = (accord45_str, sue_str, event7, timepoint66, None)
        print(f"{bankunit_agg_rows[0]=}")
        print(f"{bankunit_agg_rows[1]=}")
        print(f"{bankunit_agg_rows[2]=}")
        assert bankunit_agg_rows == [ex_row0, ex_row1, ex_row2]
