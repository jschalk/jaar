from src.f00_instrument.db_toolbox import get_row_count
from src.f01_road.deal import owner_name_str, fisc_title_str
from src.f02_bud.bud_tool import bud_acctunit_str
from src.f04_vow.atom_config import (
    face_name_str,
    acct_name_str,
    event_int_str,
    credit_belief_str,
    debtit_belief_str,
    get_delete_key_name,
)

from src.f09_idea.idea_config import idea_number_str
from src.f10_etl.tran_sqlstrs import create_bud_tables
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect


def test_WorldUnit_idea_staging_to_bud_tables_PopulatesBudPutAggTables(
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
    fizz_world = worldunit_shop("fizz")
    x_error_message = "Inconsistent bud data"

    with sqlite3_connect(":memory:") as bud_db_conn:
        cursor = bud_db_conn.cursor()
        create_bud_tables(cursor)
        staging_tablename = f"{bud_acctunit_str()}_put_staging"
        insert_staging_sqlstr = f"""
INSERT INTO {staging_tablename} ({idea_number_str()},{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()},{credit_belief_str()},{debtit_belief_str()},error_message)
VALUES
  ('br00021','{sue_inx}',{event3},'{accord23_str}','{bob_inx}','{yao_inx}',{yao_credit_belief5},NULL,NULL)
, ('br00021','{sue_inx}',{event3},'{accord23_str}','{bob_inx}','{yao_inx}',NULL,NULL,NULL)
, ('br00021','{sue_inx}',{event7},'{accord23_str}','{bob_inx}','{yao_inx}',{yao_credit_belief5},NULL,NULL)
, ('br00021','{sue_inx}',{event7},'{accord45_str}','{bob_inx}','{yao_inx}',{yao_credit_belief5},NULL,'{x_error_message}')
, ('br00021','{sue_inx}',{event7},'{accord45_str}','{bob_inx}','{yao_inx}',{yao_credit_belief7},NULL,'{x_error_message}')
;
"""
        print(insert_staging_sqlstr)
        cursor.execute(insert_staging_sqlstr)
        agg_tablename = f"{bud_acctunit_str()}_put_agg"
        assert get_row_count(cursor, agg_tablename) == 0

        # WHEN
        fizz_world.idea_staging_to_bud_tables(cursor)

        # THEN
        assert get_row_count(cursor, agg_tablename) == 2
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_title_str()}, {credit_belief_str()} FROM {agg_tablename};"
        cursor.execute(select_sqlstr)
        budunit_agg_rows = cursor.fetchall()
        assert budunit_agg_rows == [
            (event3, accord23_str, yao_credit_belief5),
            (event7, accord23_str, yao_credit_belief5),
        ]


def test_WorldUnit_idea_staging_to_bud_tables_PopulatesBudDelAggTables(
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
    fizz_world = worldunit_shop("fizz")
    x_error_message = "Inconsistent bud data"
    acct_name_delete_str = get_delete_key_name(acct_name_str())

    with sqlite3_connect(":memory:") as bud_db_conn:
        cursor = bud_db_conn.cursor()
        create_bud_tables(cursor)
        staging_tablename = f"{bud_acctunit_str()}_del_staging"
        insert_staging_sqlstr = f"""
INSERT INTO {staging_tablename} ({idea_number_str()},{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_delete_str},error_message)
VALUES
  ('br00051','{sue_inx}',{event3},'{accord23_str}','{bob_inx}','{yao_inx}',NULL)
, ('br00051','{sue_inx}',{event3},'{accord23_str}','{bob_inx}','{yao_inx}',NULL)
, ('br00051','{sue_inx}',{event7},'{accord23_str}','{bob_inx}','{yao_inx}',NULL)
, ('br00051','{sue_inx}',{event7},'{accord45_str}','{bob_inx}','{yao_inx}','{x_error_message}')
, ('br00051','{sue_inx}',{event7},'{accord45_str}','{bob_inx}','{yao_inx}','{x_error_message}')
;
"""
        print(insert_staging_sqlstr)
        cursor.execute(insert_staging_sqlstr)
        agg_tablename = f"{bud_acctunit_str()}_del_agg"
        assert get_row_count(cursor, agg_tablename) == 0

        # WHEN
        fizz_world.idea_staging_to_bud_tables(cursor)

        # THEN
        assert get_row_count(cursor, agg_tablename) == 2
        select_sqlstr = f"SELECT {event_int_str()}, {fisc_title_str()}, {acct_name_delete_str} FROM {agg_tablename};"
        cursor.execute(select_sqlstr)
        budunit_agg_rows = cursor.fetchall()
        assert budunit_agg_rows == [
            (event3, accord23_str, yao_inx),
            (event7, accord23_str, yao_inx),
        ]
