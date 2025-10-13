from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch01_py.file_toolbox import open_json
from src.ch17_idea.idea_db_tool import create_idea_sorted_table
from src.ch18_world_etl._ref.ch18_path import create_last_run_metrics_path
from src.ch18_world_etl.test._util.ch18_env import get_chapter_temp_dir
from src.ch18_world_etl.tran_sqlstrs import create_sound_and_heard_tables
from src.ch18_world_etl.transformers import create_last_run_metrics_json
from src.ref.keywords import Ch18Keywords as wx


def test_create_last_run_metrics_json_CreatesFile():
    # ESTABLISH
    spark1 = 1
    spark3 = 3
    spark9 = 9
    moment_mstr_dir = get_chapter_temp_dir()
    last_run_metrics_path = create_last_run_metrics_path(moment_mstr_dir)
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        agg_br00003_tablename = f"br00003_{wx.brick_agg}"
        agg_br00003_columns = [wx.spark_num]
        create_idea_sorted_table(cursor, agg_br00003_tablename, agg_br00003_columns)
        agg_br00003_insert_sqlstr = f"""
INSERT INTO {agg_br00003_tablename} ({wx.spark_num})
VALUES ('{spark1}'), ('{spark1}'), ('{spark9}');"""
        cursor.execute(agg_br00003_insert_sqlstr)

        agg_br00044_tablename = f"br00044_{wx.brick_agg}"
        agg_br00044_columns = [wx.spark_num]
        create_idea_sorted_table(cursor, agg_br00044_tablename, agg_br00044_columns)
        agg_br00044_insert_sqlstr = f"""
INSERT INTO {agg_br00044_tablename} ({wx.spark_num})
VALUES ('{spark3}');"""
        cursor.execute(agg_br00044_insert_sqlstr)
        assert not os_path_exists(last_run_metrics_path)

        # WHEN
        create_last_run_metrics_json(cursor, moment_mstr_dir)

        # THEN
        assert os_path_exists(last_run_metrics_path)
        last_run_metrics_dict = open_json(last_run_metrics_path)
        max_brick_agg_spark_num_str = "max_brick_agg_spark_num"
        assert max_brick_agg_spark_num_str in set(last_run_metrics_dict.keys())
        max_brick_agg_spark_num = last_run_metrics_dict.get(max_brick_agg_spark_num_str)
        assert max_brick_agg_spark_num == spark9
