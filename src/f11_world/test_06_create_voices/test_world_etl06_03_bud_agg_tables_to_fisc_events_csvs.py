from src.f00_instrument.file import create_path, open_file
from src.f02_bud.bud_tool import bud_acctunit_str
from src.f04_gift.atom_config import (
    face_name_str,
    fisc_title_str,
    owner_name_str,
    acct_name_str,
    credit_belief_str,
)
from src.f05_listen.hub_path import create_events_owner_dir_path
from src.f08_pidgin.pidgin_config import event_int_str
from src.f10_etl.tran_sqlstrs import create_bud_tables
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from sqlite3 import connect as sqlite3_connect
from os.path import exists as os_path_exists


def test_WorldUnit_bud_tables_to_event_bud_csvs_CreatesFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Bobby"
    event3 = 3
    event7 = 7
    accord23_str = "accord23"
    yao_credit_belief5 = 5
    sue_credit_belief7 = 7
    fizz_world = worldunit_shop("fizz")
    put_agg_tablename = f"{bud_acctunit_str()}_put_agg"
    put_agg_csv = f"{put_agg_tablename}.csv"
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_bob_e3_dir = create_events_owner_dir_path(
        fisc_mstr_dir, accord23_str, bob_inx, event3
    )
    a23_bob_e7_dir = create_events_owner_dir_path(
        fisc_mstr_dir, accord23_str, bob_inx, event7
    )
    a23_e3_budacct_put_path = create_path(a23_bob_e3_dir, put_agg_csv)
    a23_e7_budacct_put_path = create_path(a23_bob_e7_dir, put_agg_csv)

    with sqlite3_connect(":memory:") as bud_db_conn:
        cursor = bud_db_conn.cursor()
        create_bud_tables(cursor)
        insert_staging_sqlstr = f"""
INSERT INTO {put_agg_tablename} ({face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()},{credit_belief_str()})
VALUES
  ('{sue_inx}',{event3},'{accord23_str}','{bob_inx}','{yao_inx}',{yao_credit_belief5})
, ('{sue_inx}',{event7},'{accord23_str}','{bob_inx}','{yao_inx}',{yao_credit_belief5})
, ('{sue_inx}',{event7},'{accord23_str}','{bob_inx}','{sue_inx}',{sue_credit_belief7})
;
"""
        print(insert_staging_sqlstr)
        cursor.execute(insert_staging_sqlstr)
        print(f"{a23_e3_budacct_put_path=}")
        print(f"{a23_e7_budacct_put_path=}")
        assert os_path_exists(a23_e3_budacct_put_path) is False
        assert os_path_exists(a23_e7_budacct_put_path) is False

        # WHEN
        fizz_world.bud_tables_to_event_bud_csvs(cursor)

        # THEN
        assert os_path_exists(a23_e3_budacct_put_path)
        assert os_path_exists(a23_e7_budacct_put_path)
        e3_put_csv = open_file(a23_e3_budacct_put_path)
        e7_put_csv = open_file(a23_e7_budacct_put_path)
        print(f"{e3_put_csv=}")
        print(f"{e7_put_csv=}")
        expected_e3_put_csv = f"""{face_name_str()},event_int,fisc_title,owner_name,acct_name,credit_belief,debtit_belief
Suzy,3,accord23,Bobby,Bobby,5.0,
"""
        expected_e7_put_csv = """face_name,event_int,fisc_title,owner_name,acct_name,credit_belief,debtit_belief
Suzy,7,accord23,Bobby,Bobby,5.0,
Suzy,7,accord23,Bobby,Suzy,7.0,
"""
        assert e3_put_csv == expected_e3_put_csv
        assert e7_put_csv == expected_e7_put_csv


# def test_WorldUnit_idea_staging_to_bud_tables_PopulatesBudDelAggTables(
#     env_dir_setup_cleanup,
# ):

#     # ESTABLISH
#     sue_inx = "Suzy"
#     bob_inx = "Bobby"
#     yao_inx = "Bobby"
#     event3 = 3
#     event7 = 7
#     accord23_str = "accord23"
#     accord45_str = "accord45"
#     fizz_world = worldunit_shop("fizz")
#     x_error_message = "Inconsistent bud data"
#     acct_name_delete_str = get_delete_key_name(acct_name_str())

#     with sqlite3_connect(":memory:") as bud_db_conn:
#         cursor = bud_db_conn.cursor()
#         create_bud_tables(cursor)
#         staging_tablename = f"{bud_acctunit_str()}_del_staging"
#         insert_staging_sqlstr = f"""
# INSERT INTO {staging_tablename} ({idea_number_str()},{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_delete_str},error_message)
# VALUES
#   ('br00051','{sue_inx}',{event3},'{accord23_str}','{bob_inx}','{yao_inx}',NULL)
# , ('br00051','{sue_inx}',{event3},'{accord23_str}','{bob_inx}','{yao_inx}',NULL)
# , ('br00051','{sue_inx}',{event7},'{accord23_str}','{bob_inx}','{yao_inx}',NULL)
# , ('br00051','{sue_inx}',{event7},'{accord45_str}','{bob_inx}','{yao_inx}','{x_error_message}')
# , ('br00051','{sue_inx}',{event7},'{accord45_str}','{bob_inx}','{yao_inx}','{x_error_message}')
# ;
# """
#         print(insert_staging_sqlstr)
#         cursor.execute(insert_staging_sqlstr)
#         agg_tablename = f"{bud_acctunit_str()}_del_agg"
#         assert get_row_count(cursor, agg_tablename) == 0

#         # WHEN
#         fizz_world.idea_staging_to_bud_tables(cursor)

#         # THEN
#         assert get_row_count(cursor, agg_tablename) == 2
#         select_sqlstr = f"SELECT {event_int_str()}, {fisc_title_str()}, {acct_name_delete_str} FROM {agg_tablename};"
#         cursor.execute(select_sqlstr)
#         budunit_agg_rows = cursor.fetchall()
#         assert budunit_agg_rows == [
#             (event3, accord23_str, yao_inx),
#             (event7, accord23_str, yao_inx),
#         ]
