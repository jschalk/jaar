from src.f00_instrument.file import create_path
from src.f00_instrument.db_toolbox import save_to_split_csvs
from src.f00_instrument.csv_toolbox import open_csv_with_types
from src.f00_instrument.examples.instrument_env import (
    env_dir_setup_cleanup,
    get_instrument_temp_env_dir,
)
from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect


def test_save_to_split_csvs_CreatesFiles():
    # sourcery skip: extract-method
    # ESTABLISH
    x_tablename = "test_table56"
    key_columns = ["user", "z_int"]
    x_column_types = {"z_int": "INTEGER", "user": "TEXT", "y_int": "INTEGER"}

    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""CREATE TABLE {x_tablename} (z_int INTEGER,user TEXT,y_int INTEGER)"""
        )
        cursor.execute(
            f"""INSERT INTO {x_tablename} (z_int, user, y_int) 
VALUES 
(1, "A", 100),
(2, "A", 200),
(3, "B", 300),
(4, "C", 400),
(4, "C", 500)
;
"""
        )
        x_dir = get_instrument_temp_env_dir()
        A_dir = create_path(x_dir, "A")
        B_dir = create_path(x_dir, "B")
        C_dir = create_path(x_dir, "C")
        A1_dir = create_path(A_dir, 1)
        A2_dir = create_path(A_dir, 2)
        B3_dir = create_path(B_dir, 3)
        C4_dir = create_path(C_dir, 4)
        A1_path = create_path(A1_dir, f"{x_tablename}.csv")
        A2_path = create_path(A2_dir, f"{x_tablename}.csv")
        B3_path = create_path(B3_dir, f"{x_tablename}.csv")
        C4_path = create_path(C4_dir, f"{x_tablename}.csv")
        assert os_path_exists(A1_path) is False
        assert os_path_exists(A2_path) is False
        assert os_path_exists(B3_path) is False
        assert os_path_exists(C4_path) is False

        # WHEN
        save_to_split_csvs(conn, x_tablename, key_columns, x_dir)

        # THEN
        assert os_path_exists(A1_path)
        assert os_path_exists(A2_path)
        assert os_path_exists(B3_path)
        assert os_path_exists(C4_path)
        # expected_A1_csv = "z_int,user,y_int\n1,A,100"
        # expected_A2_csv = "z_int,user,y_int\n2,A,200"
        # expected_B3_csv = "z_int,user,y_int\n3,C,300"
        # expected_C4_csv = "z_int,user,y_int\n4,C,400\n4,C,500"
        expected_A1_row = (1, "A", 100)
        expected_A2_row = (2, "A", 200)
        expected_B3_row = (3, "B", 300)
        expected_C4_0_row = (4, "C", 400)
        expected_C4_1_row = (4, "C", 500)

        A1_csv = open_csv_with_types(A1_path, x_column_types)
        A2_csv = open_csv_with_types(A2_path, x_column_types)
        B3_csv = open_csv_with_types(B3_path, x_column_types)
        C4_csv = open_csv_with_types(C4_path, x_column_types)

        assert A1_csv[0] == ("z_int", "user", "y_int")
        assert A2_csv[0] == ("z_int", "user", "y_int")
        assert B3_csv[0] == ("z_int", "user", "y_int")
        assert C4_csv[0] == ("z_int", "user", "y_int")
        assert A1_csv[1] == expected_A1_row
        assert A2_csv[1] == expected_A2_row
        assert B3_csv[1] == expected_B3_row
        assert C4_csv[1] == expected_C4_0_row
        assert C4_csv[2] == expected_C4_1_row
