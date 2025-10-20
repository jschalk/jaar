from sqlite3 import connect as sqlite3_connect
from src.ch01_py.db_toolbox import db_table_exists, get_row_count
from src.ch01_py.file_toolbox import save_json
from src.ch10_lesson._ref.ch10_path import create_moment_json_path
from src.ch11_bud.bud_main import tranbook_shop
from src.ch15_moment.moment_main import momentunit_shop
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ch18_world_etl.tran_sqlstrs import CREATE_MOMENT_VOICE_NETS_SQLSTR
from src.ch18_world_etl.transformers import (
    etl_moment_json_voice_nets_to_moment_voice_nets_table,
    insert_tranunit_voices_net,
)
from src.ref.keywords import Ch18Keywords as kw


def test_insert_tranunit_voices_net_PopulatesDatabase():
    # ESTABLISH
    a23_str = "amy23"
    a23_tranbook = tranbook_shop(a23_str)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    a23_tranbook.add_tranunit(sue_str, yao_str, t55_tran_time, t55_yao_amount)
    a23_tranbook.add_tranunit(sue_str, yao_str, t66_tran_time, t66_yao_amount)
    a23_tranbook.add_tranunit(sue_str, bob_str, t55_tran_time, t55_bob_amount)
    a23_tranbook.add_tranunit(yao_str, yao_str, t77_tran_time, t77_yao_amount)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        moment_voice_nets_tablename = kw.moment_voice_nets
        cursor.execute(CREATE_MOMENT_VOICE_NETS_SQLSTR)
        assert get_row_count(cursor, moment_voice_nets_tablename) == 0

        # WHEN
        insert_tranunit_voices_net(cursor, a23_tranbook)

        # THEN
        assert get_row_count(cursor, moment_voice_nets_tablename) == 2
        select_sqlstr = f"SELECT moment_label, belief_name, {kw.belief_net_amount} FROM {moment_voice_nets_tablename}"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        assert rows == [
            (a23_str, bob_str, t55_bob_amount),
            (a23_str, yao_str, t55_yao_amount + t66_yao_amount + t77_yao_amount),
        ]


def test_etl_moment_json_voice_nets_to_moment_voice_nets_table_PopulatesDatabase(
    temp_dir_setup,
):
    # ESTABLISH
    a23_str = "amy23"
    mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(a23_str, mstr_dir)
    sue_str = "Sue"
    yao_str = "Yao"
    bob_str = "Bob"
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    a23_moment.add_paypurchase(sue_str, yao_str, t55_tran_time, t55_yao_amount)
    a23_moment.add_paypurchase(sue_str, yao_str, t66_tran_time, t66_yao_amount)
    a23_moment.add_paypurchase(sue_str, bob_str, t55_tran_time, t55_bob_amount)
    a23_moment.add_paypurchase(yao_str, yao_str, t77_tran_time, t77_yao_amount)
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, a23_moment.to_dict())

    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        moment_voice_nets_tablename = kw.moment_voice_nets
        assert not db_table_exists(cursor, moment_voice_nets_tablename)

        # WHEN
        etl_moment_json_voice_nets_to_moment_voice_nets_table(cursor, mstr_dir)

        # THEN
        assert get_row_count(cursor, moment_voice_nets_tablename) == 2
        select_sqlstr = f"SELECT moment_label, belief_name, {kw.belief_net_amount} FROM {moment_voice_nets_tablename}"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        assert rows == [
            (a23_str, bob_str, t55_bob_amount),
            (a23_str, yao_str, t55_yao_amount + t66_yao_amount + t77_yao_amount),
        ]
