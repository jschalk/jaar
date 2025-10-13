from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch01_py.file_toolbox import create_path, open_file
from src.ch11_bud._ref.ch11_path import create_belief_event_dir_path
from src.ch18_world_etl.test._util.ch18_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch18_world_etl.tran_sqlstrs import (
    create_prime_tablename,
    create_sound_and_heard_tables,
)
from src.ch18_world_etl.transformers import etl_heard_agg_to_event_belief_csvs
from src.ref.keywords import Ch18Keywords as wx


def test_etl_heard_agg_to_event_belief_csvs_PopulatesBeliefPulabelTables(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Bobby"
    event3 = 3
    event7 = 7
    amy23_str = "amy23"
    yao_voice_cred_lumen5 = 5
    sue_voice_cred_lumen7 = 7
    put_agg_tablename = create_prime_tablename(wx.belief_voiceunit, "h", "agg", "put")
    put_agg_csv = f"{put_agg_tablename}.csv"
    x_moment_mstr_dir = get_chapter_temp_dir()
    a23_bob_e3_dir = create_belief_event_dir_path(
        x_moment_mstr_dir, amy23_str, bob_inx, event3
    )
    a23_bob_e7_dir = create_belief_event_dir_path(
        x_moment_mstr_dir, amy23_str, bob_inx, event7
    )
    a23_e3_blrpern_put_path = create_path(a23_bob_e3_dir, put_agg_csv)
    a23_e7_blrpern_put_path = create_path(a23_bob_e7_dir, put_agg_csv)

    with sqlite3_connect(":memory:") as belief_db_conn:
        cursor = belief_db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        insert_raw_sqlstr = f"""
INSERT INTO {put_agg_tablename} ({wx.event_int},{wx.face_name},{wx.moment_label},{wx.belief_name},{wx.voice_name},{wx.voice_cred_lumen})
VALUES
  ({event3},'{sue_inx}','{amy23_str}','{bob_inx}','{yao_inx}',{yao_voice_cred_lumen5})
, ({event7},'{sue_inx}','{amy23_str}','{bob_inx}','{yao_inx}',{yao_voice_cred_lumen5})
, ({event7},'{sue_inx}','{amy23_str}','{bob_inx}','{sue_inx}',{sue_voice_cred_lumen7})
;
"""
        print(insert_raw_sqlstr)
        cursor.execute(insert_raw_sqlstr)
        assert os_path_exists(a23_e3_blrpern_put_path) is False
        assert os_path_exists(a23_e7_blrpern_put_path) is False

        # WHEN
        etl_heard_agg_to_event_belief_csvs(cursor, x_moment_mstr_dir)

        # THEN
        assert os_path_exists(a23_e3_blrpern_put_path)
        assert os_path_exists(a23_e7_blrpern_put_path)
        e3_put_csv = open_file(a23_e3_blrpern_put_path)
        e7_put_csv = open_file(a23_e7_blrpern_put_path)
        print(f"{e3_put_csv=}")
        print(f"{e7_put_csv=}")
        expected_e3_put_csv = """event_int,face_name,moment_label,belief_name,voice_name,voice_cred_lumen,voice_debt_lumen
3,Suzy,amy23,Bobby,Bobby,5.0,
"""
        expected_e7_put_csv = """event_int,face_name,moment_label,belief_name,voice_name,voice_cred_lumen,voice_debt_lumen
7,Suzy,amy23,Bobby,Bobby,5.0,
7,Suzy,amy23,Bobby,Suzy,7.0,
"""
        assert e3_put_csv == expected_e3_put_csv
        assert e7_put_csv == expected_e7_put_csv
