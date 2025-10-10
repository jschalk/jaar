from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.file_toolbox import open_json
from src.ch17_idea_logic.idea_db_tool import create_idea_sorted_table
from src.ch18_etl_toolbox._ref.ch18_path import create_last_run_metrics_path
from src.ch18_etl_toolbox.test._util.ch18_env import get_chapter_temp_dir
from src.ch18_etl_toolbox.tran_sqlstrs import create_sound_and_heard_tables
from src.ch18_etl_toolbox.transformers import create_last_run_metrics_json
from src.ref.ch18_keywords import Ch18Keywords as wx


def test_create_last_run_metrics_json_CreatesFile():
    # ESTABLISH
    event1 = 1
    event3 = 3
    event9 = 9
    moment_mstr_dir = get_chapter_temp_dir()
    last_run_metrics_path = create_last_run_metrics_path(moment_mstr_dir)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        agg_br00003_tablename = f"br00003_{wx.brick_agg}"
        agg_br00003_columns = [wx.event_int]
        create_idea_sorted_table(cursor, agg_br00003_tablename, agg_br00003_columns)
        agg_br00003_insert_sqlstr = f"""
INSERT INTO {agg_br00003_tablename} ({wx.event_int})
VALUES ('{event1}'), ('{event1}'), ('{event9}');"""
        cursor.execute(agg_br00003_insert_sqlstr)

        agg_br00044_tablename = f"br00044_{wx.brick_agg}"
        agg_br00044_columns = [wx.event_int]
        create_idea_sorted_table(cursor, agg_br00044_tablename, agg_br00044_columns)
        agg_br00044_insert_sqlstr = f"""
INSERT INTO {agg_br00044_tablename} ({wx.event_int})
VALUES ('{event3}');"""
        cursor.execute(agg_br00044_insert_sqlstr)
        assert not os_path_exists(last_run_metrics_path)

        # WHEN
        create_last_run_metrics_json(cursor, moment_mstr_dir)

        # THEN
        assert os_path_exists(last_run_metrics_path)
        last_run_metrics_dict = open_json(last_run_metrics_path)
        max_brick_agg_event_int_str = "max_brick_agg_event_int"
        assert max_brick_agg_event_int_str in set(last_run_metrics_dict.keys())
        max_brick_agg_event_int = last_run_metrics_dict.get(max_brick_agg_event_int_str)
        assert max_brick_agg_event_int == event9
