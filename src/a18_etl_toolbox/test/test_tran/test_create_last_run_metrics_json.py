from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.file_toolbox import open_json
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a15_coin_logic.test._util.a15_str import (
    coin_label_str,
    cumulative_minute_str,
    hour_label_str,
)
from src.a17_idea_logic.idea_db_tool import create_idea_sorted_table
from src.a18_etl_toolbox.a18_path import create_last_run_metrics_path
from src.a18_etl_toolbox.test._util.a18_env import get_module_temp_dir
from src.a18_etl_toolbox.test._util.a18_str import (
    brick_agg_str,
    brick_raw_str,
    error_message_str,
)
from src.a18_etl_toolbox.tran_sqlstrs import create_sound_and_voice_tables
from src.a18_etl_toolbox.transformers import (
    create_last_run_metrics_json,
    etl_brick_raw_tables_to_brick_agg_tables,
    get_max_brick_agg_event_int,
)


def test_create_last_run_metrics_json_CreatesFile():
    # ESTABLISH
    event1 = 1
    event3 = 3
    event9 = 9
    coin_mstr_dir = get_module_temp_dir()
    last_run_metrics_path = create_last_run_metrics_path(coin_mstr_dir)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        agg_br00003_tablename = f"br00003_{brick_agg_str()}"
        agg_br00003_columns = [event_int_str()]
        create_idea_sorted_table(cursor, agg_br00003_tablename, agg_br00003_columns)
        agg_br00003_insert_sqlstr = f"""
INSERT INTO {agg_br00003_tablename} ({event_int_str()})
VALUES ('{event1}'), ('{event1}'), ('{event9}');"""
        cursor.execute(agg_br00003_insert_sqlstr)

        agg_br00044_tablename = f"br00044_{brick_agg_str()}"
        agg_br00044_columns = [event_int_str()]
        create_idea_sorted_table(cursor, agg_br00044_tablename, agg_br00044_columns)
        agg_br00044_insert_sqlstr = f"""
INSERT INTO {agg_br00044_tablename} ({event_int_str()})
VALUES ('{event3}');"""
        cursor.execute(agg_br00044_insert_sqlstr)
        assert not os_path_exists(last_run_metrics_path)

        # WHEN
        create_last_run_metrics_json(cursor, coin_mstr_dir)

        # THEN
        assert os_path_exists(last_run_metrics_path)
        last_run_metrics_dict = open_json(last_run_metrics_path)
        max_brick_agg_event_int_str = "max_brick_agg_event_int"
        assert max_brick_agg_event_int_str in set(last_run_metrics_dict.keys())
        max_brick_agg_event_int = last_run_metrics_dict.get(max_brick_agg_event_int_str)
        assert max_brick_agg_event_int == event9
