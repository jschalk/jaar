from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.file_toolbox import create_path, open_file
from src.a06_believer_logic.test._util.a06_str import (
    acct_cred_points_str,
    acct_name_str,
    belief_label_str,
    believer_acctunit_str,
    believer_name_str,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a12_hub_toolbox.hub_path import create_believer_event_dir_path
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename,
    create_sound_and_voice_tables,
)
from src.a18_etl_toolbox.transformers import etl_voice_agg_to_event_believer_csvs


def test_etl_voice_agg_to_event_believer_csvs_PopulatesBelieverPulabelTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Bobby"
    event3 = 3
    event7 = 7
    amy23_str = "amy23"
    yao_acct_cred_points5 = 5
    sue_acct_cred_points7 = 7
    put_agg_tablename = create_prime_tablename(
        believer_acctunit_str(), "v", "agg", "put"
    )
    put_agg_csv = f"{put_agg_tablename}.csv"
    x_belief_mstr_dir = get_module_temp_dir()
    a23_bob_e3_dir = create_believer_event_dir_path(
        x_belief_mstr_dir, amy23_str, bob_inx, event3
    )
    a23_bob_e7_dir = create_believer_event_dir_path(
        x_belief_mstr_dir, amy23_str, bob_inx, event7
    )
    a23_e3_onracct_put_path = create_path(a23_bob_e3_dir, put_agg_csv)
    a23_e7_onracct_put_path = create_path(a23_bob_e7_dir, put_agg_csv)

    with sqlite3_connect(":memory:") as believer_db_conn:
        cursor = believer_db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        insert_raw_sqlstr = f"""
INSERT INTO {put_agg_tablename} ({event_int_str()},{face_name_str()},{belief_label_str()},{believer_name_str()},{acct_name_str()},{acct_cred_points_str()})
VALUES
  ({event3},'{sue_inx}','{amy23_str}','{bob_inx}','{yao_inx}',{yao_acct_cred_points5})
, ({event7},'{sue_inx}','{amy23_str}','{bob_inx}','{yao_inx}',{yao_acct_cred_points5})
, ({event7},'{sue_inx}','{amy23_str}','{bob_inx}','{sue_inx}',{sue_acct_cred_points7})
;
"""
        print(insert_raw_sqlstr)
        cursor.execute(insert_raw_sqlstr)
        assert os_path_exists(a23_e3_onracct_put_path) is False
        assert os_path_exists(a23_e7_onracct_put_path) is False

        # WHEN
        etl_voice_agg_to_event_believer_csvs(cursor, x_belief_mstr_dir)

        # THEN
        assert os_path_exists(a23_e3_onracct_put_path)
        assert os_path_exists(a23_e7_onracct_put_path)
        e3_put_csv = open_file(a23_e3_onracct_put_path)
        e7_put_csv = open_file(a23_e7_onracct_put_path)
        print(f"{e3_put_csv=}")
        print(f"{e7_put_csv=}")
        expected_e3_put_csv = """event_int,face_name,belief_label,believer_name,acct_name,acct_cred_points,acct_debt_points
3,Suzy,amy23,Bobby,Bobby,5.0,
"""
        expected_e7_put_csv = """event_int,face_name,belief_label,believer_name,acct_name,acct_cred_points,acct_debt_points
7,Suzy,amy23,Bobby,Bobby,5.0,
7,Suzy,amy23,Bobby,Suzy,7.0,
"""
        assert e3_put_csv == expected_e3_put_csv
        assert e7_put_csv == expected_e7_put_csv
