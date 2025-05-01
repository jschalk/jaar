from src.a00_data_toolbox.db_toolbox import get_row_count
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import (
    bud_acctunit_str,
    face_name_str,
    acct_name_str,
    event_int_str,
    credit_belief_str,
    debtit_belief_str,
)
from src.a08_bud_atom_logic.atom_config import get_delete_key_name
from src.a17_idea_logic._utils.str_a17 import idea_number_str
from src.a18_etl_toolbox.tran_sqlstrs import create_bud_prime_tables
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_idea_raw_to_bud_prime_tables_PopulatesBudPutAggTables(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Bobby"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    yao_credit_belief5 = 5
    yao_credit_belief7 = 7
    fizz_world = worldunit_shop("fizz", worlds_dir())
    x_error_message = "Inconsistent bud data"

    with sqlite3_connect(":memory:") as bud_db_conn:
        cursor = bud_db_conn.cursor()
        create_bud_prime_tables(cursor)
        raw_tablename = f"{bud_acctunit_str()}_put_raw"
        insert_raw_sqlstr = f"""
INSERT INTO {raw_tablename} ({idea_number_str()},{event_int_str()},{face_name_str()},{fisc_tag_str()},{owner_name_str()},{acct_name_str()},{credit_belief_str()},{debtit_belief_str()},error_message)
VALUES
  ('br00021',{event3},'{sue_inx}','{accord23_str}','{bob_inx}','{yao_inx}',{yao_credit_belief5},NULL,NULL)
, ('br00021',{event3},'{sue_inx}','{accord23_str}','{bob_inx}','{yao_inx}',NULL,NULL,NULL)
, ('br00021',{event7},'{sue_inx}','{accord23_str}','{bob_inx}','{yao_inx}',{yao_credit_belief5},NULL,NULL)
, ('br00021',{event7},'{sue_inx}','{accord45_str}','{bob_inx}','{yao_inx}',{yao_credit_belief5},NULL,'{x_error_message}')
, ('br00021',{event7},'{sue_inx}','{accord45_str}','{bob_inx}','{yao_inx}',{yao_credit_belief7},NULL,'{x_error_message}')
;
"""
        print(insert_raw_sqlstr)
        cursor.execute(insert_raw_sqlstr)
        agg_tablename = f"{bud_acctunit_str()}_put_agg"
        assert get_row_count(cursor, agg_tablename) == 0

        # WHEN
        fizz_world.idea_raw_to_bud_prime_tables(cursor)

        # THEN
        assert get_row_count(cursor, agg_tablename) == 2
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_tag_str()}, {credit_belief_str()} FROM {agg_tablename};"
        cursor.execute(select_sqlstr)
        budunit_agg_rows = cursor.fetchall()
        assert budunit_agg_rows == [
            (event3, accord23_str, yao_credit_belief5),
            (event7, accord23_str, yao_credit_belief5),
        ]


def test_WorldUnit_idea_raw_to_bud_prime_tables_PopulatesBudDelAggTables(
    env_dir_setup_cleanup,
):

    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Bobby"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    accord45_str = "accord45"
    fizz_world = worldunit_shop("fizz", worlds_dir())
    x_error_message = "Inconsistent bud data"
    acct_name_delete_str = get_delete_key_name(acct_name_str())

    with sqlite3_connect(":memory:") as bud_db_conn:
        cursor = bud_db_conn.cursor()
        create_bud_prime_tables(cursor)
        raw_tablename = f"{bud_acctunit_str()}_del_raw"
        insert_raw_sqlstr = f"""
INSERT INTO {raw_tablename} ({idea_number_str()},{event_int_str()},{face_name_str()},{fisc_tag_str()},{owner_name_str()},{acct_name_delete_str},error_message)
VALUES
  ('br00051',{event3},'{sue_inx}','{accord23_str}','{bob_inx}','{yao_inx}',NULL)
, ('br00051',{event3},'{sue_inx}','{accord23_str}','{bob_inx}','{yao_inx}',NULL)
, ('br00051',{event7},'{sue_inx}','{accord23_str}','{bob_inx}','{yao_inx}',NULL)
, ('br00051',{event7},'{sue_inx}','{accord45_str}','{bob_inx}','{yao_inx}','{x_error_message}')
, ('br00051',{event7},'{sue_inx}','{accord45_str}','{bob_inx}','{yao_inx}','{x_error_message}')
;
"""
        print(insert_raw_sqlstr)
        cursor.execute(insert_raw_sqlstr)
        agg_tablename = f"{bud_acctunit_str()}_del_agg"
        assert get_row_count(cursor, agg_tablename) == 0

        # WHEN
        fizz_world.idea_raw_to_bud_prime_tables(cursor)

        # THEN
        assert get_row_count(cursor, agg_tablename) == 2
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_tag_str()}, {acct_name_delete_str} FROM {agg_tablename};"
        cursor.execute(select_sqlstr)
        budunit_agg_rows = cursor.fetchall()
        assert budunit_agg_rows == [
            (event3, accord23_str, yao_inx),
            (event7, accord23_str, yao_inx),
        ]
