from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.db_toolbox import db_table_exists, get_row_count
from src.ch01_data_toolbox.file_toolbox import save_json
from src.ch11_bud_logic.bud import tranbook_shop
from src.ch12_hub_toolbox.ch12_path import create_moment_json_path
from src.ch15_moment_logic.moment_main import momentunit_shop
from src.ch18_etl_toolbox._ref.ch18_keywords import (
    belief_net_amount_str,
    moment_voice_nets_str,
)
from src.ch18_etl_toolbox.test._util.ch18_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch18_etl_toolbox.tran_sqlstrs import CREATE_MOMENT_VOICE_NETS_SQLSTR
from src.ch18_etl_toolbox.transformers import (
    etl_moment_json_voice_nets_to_moment_voice_nets_table,
    insert_tranunit_voices_net,
)


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
        moment_voice_nets_tablename = moment_voice_nets_str()
        cursor.execute(CREATE_MOMENT_VOICE_NETS_SQLSTR)
        assert get_row_count(cursor, moment_voice_nets_tablename) == 0

        # WHEN
        insert_tranunit_voices_net(cursor, a23_tranbook)

        # THEN
        assert get_row_count(cursor, moment_voice_nets_tablename) == 2
        select_sqlstr = f"SELECT moment_label, belief_name, {belief_net_amount_str()} FROM {moment_voice_nets_tablename}"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        assert rows == [
            (a23_str, bob_str, t55_bob_amount),
            (a23_str, yao_str, t55_yao_amount + t66_yao_amount + t77_yao_amount),
        ]


def test_etl_moment_json_voice_nets_to_moment_voice_nets_table_PopulatesDatabase(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    a23_str = "amy23"
    mstr_dir = get_chapter_temp_dir()
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
        moment_voice_nets_tablename = moment_voice_nets_str()
        assert not db_table_exists(cursor, moment_voice_nets_tablename)

        # WHEN
        etl_moment_json_voice_nets_to_moment_voice_nets_table(cursor, mstr_dir)

        # THEN
        assert get_row_count(cursor, moment_voice_nets_tablename) == 2
        select_sqlstr = f"SELECT moment_label, belief_name, {belief_net_amount_str()} FROM {moment_voice_nets_tablename}"
        cursor.execute(select_sqlstr)
        rows = cursor.fetchall()
        assert rows == [
            (a23_str, bob_str, t55_bob_amount),
            (a23_str, yao_str, t55_yao_amount + t66_yao_amount + t77_yao_amount),
        ]
