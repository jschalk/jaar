from os import remove as os_remove
from os.path import exists as os_path_exists
from pytest import fixture as pytest_fixture
from sqlite3 import Connection as sqlite3_Connection, connect as sqlite3_connect
from src.a17_idea_logic._ref.a17_terms import (
    belief_name_str,
    event_int_str,
    face_name_str,
    gogo_want_str,
    group_title_str,
    moment_label_str,
    voice_name_str,
)
from src.a17_idea_logic.idea_config import get_idea_sqlite_types
from src.a17_idea_logic.idea_db_tool import create_idea_table_from_csv, insert_idea_csv
from src.a17_idea_logic.test._util.a17_env import env_dir_setup_cleanup


@pytest_fixture
def setup_database_and_csv() -> tuple[sqlite3_Connection, str, str]:  # type: ignore
    """
    Fixture to set up a temporary SQLite database and CSV file for testing.
    Yields the database connection, table name, and CSV file path, and cleans up after the test.
    """
    test_db = "test_database.db"
    # test_table = "test_table"
    test_csv_filepath = "test_data.csv"

    # Create a test SQLite database
    conn = sqlite3_connect(test_db)
    # cursor = conn.cursor()

    # # Create a test table
    # cursor.execute(
    #     f"""
    #     CREATE TABLE {test_table} (
    #         face_name TEXT,
    #         event_int INTEGER,
    #         moment_label TEXT,
    #         belief_name TEXT,
    #         voice_name TEXT,
    #         group_title TEXT,
    #         gogo_want REAL
    #     )
    # """
    # )
    # conn.commit()

    # Create a test CSV file
    with open(test_csv_filepath, "w", newline="", encoding="utf-8") as csv_file:
        csv_file.write(
            f"{event_int_str()},{face_name_str()},{moment_label_str()},{belief_name_str()},{voice_name_str()},{group_title_str()},{gogo_want_str()}\n"
        )
        csv_file.write("3,Sue,Amy43,Bob,Bob,;runners,6.5\n")
        csv_file.write("3,Sue,Amy43,Yao,Bob,;runners,7.5\n")

    yield conn, test_csv_filepath

    # Clean up
    conn.close()
    if os_path_exists(test_db):
        os_remove(test_db)
    if os_path_exists(test_csv_filepath):
        os_remove(test_csv_filepath)


def test_create_idea_table_from_csv_ChangesDBState(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str],
):
    """Test the create_idea_table_from_csv_with_types function."""
    # ESTABLISH
    conn, test_csv_filepath = setup_database_and_csv
    # Call the function to create a table based on the CSV header and column types
    new_table = "new_test_table"
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({new_table})")
    columns = cursor.fetchall()
    assert columns == []

    # WHEN
    create_idea_table_from_csv(test_csv_filepath, conn, new_table)

    # THEN Verify the table was created
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({new_table})")
    columns = cursor.fetchall()

    # Expected column definitions
    expected_columns = [
        (0, event_int_str(), "INTEGER", 0, None, 0),
        (1, face_name_str(), "TEXT", 0, None, 0),
        (2, moment_label_str(), "TEXT", 0, None, 0),
        (3, belief_name_str(), "TEXT", 0, None, 0),
        (4, voice_name_str(), "TEXT", 0, None, 0),
        (5, group_title_str(), "TEXT", 0, None, 0),
        (6, gogo_want_str(), "REAL", 0, None, 0),
    ]
    assert columns == expected_columns
    column_types = get_idea_sqlite_types()
    get_idea_sqlite_types_columns = [
        (0, event_int_str(), column_types.get(event_int_str()), 0, None, 0),
        (1, face_name_str(), column_types.get(face_name_str()), 0, None, 0),
        (2, moment_label_str(), column_types.get(moment_label_str()), 0, None, 0),
        (3, belief_name_str(), column_types.get(belief_name_str()), 0, None, 0),
        (4, voice_name_str(), column_types.get(voice_name_str()), 0, None, 0),
        (5, group_title_str(), column_types.get(group_title_str()), 0, None, 0),
        (6, gogo_want_str(), column_types.get(gogo_want_str()), 0, None, 0),
    ]
    assert columns == get_idea_sqlite_types_columns


def test_insert_idea_csv_ChangesDBState_add_to_empty_table(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str],
):
    # ESTABLISH
    conn, test_csv_filepath = setup_database_and_csv
    br_tablename = "brXXXXX"
    create_idea_table_from_csv(test_csv_filepath, conn, br_tablename)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {br_tablename}")
    assert cursor.fetchall() == []

    # WHEN Call the function to insert data from the CSV file into the database
    insert_idea_csv(test_csv_filepath, conn, br_tablename)

    # THEN
    # Verify the data was inserted
    cursor.execute(f"SELECT * FROM {br_tablename}")
    rows = cursor.fetchall()
    expected_data = [
        (3, "Sue", "Amy43", "Bob", "Bob", ";runners", 6.5),
        (3, "Sue", "Amy43", "Yao", "Bob", ";runners", 7.5),
    ]
    assert rows == expected_data


def test_insert_idea_csv_ChangesDBState_Inserts(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str], env_dir_setup_cleanup
):
    """Test the insert_csv function using pytest."""
    # ESTABLISH
    conn, test_csv_filepath = setup_database_and_csv
    # Create a new CSV file
    zia_csv_filepath = "zia_brXXXXX.csv"
    with open(zia_csv_filepath, "w", newline="", encoding="utf-8") as csv_file:
        csv_file.write(
            f"{event_int_str()},{face_name_str()},{moment_label_str()},{belief_name_str()},{voice_name_str()},{group_title_str()},{gogo_want_str()}\n"
        )
        csv_file.write("7,Zia,Amy55,Yao,Zia,;swimmers,10.2\n")
        csv_file.write("8,Zia,Amy43,Zia,Bob,;runners,11.1\n")

    br_tablename = "brXXXXX"
    create_idea_table_from_csv(test_csv_filepath, conn, br_tablename)
    insert_idea_csv(test_csv_filepath, conn, br_tablename)
    before_table_data = [
        (3, "Sue", "Amy43", "Bob", "Bob", ";runners", 6.5),
        (3, "Sue", "Amy43", "Yao", "Bob", ";runners", 7.5),
    ]
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {br_tablename}")
    assert cursor.fetchall() == before_table_data

    # WHEN
    insert_idea_csv(zia_csv_filepath, conn, br_tablename)

    # THEN
    expected_table_data = [
        (3, "Sue", "Amy43", "Bob", "Bob", ";runners", 6.5),
        (3, "Sue", "Amy43", "Yao", "Bob", ";runners", 7.5),
        (7, "Zia", "Amy55", "Yao", "Zia", ";swimmers", 10.2),
        (8, "Zia", "Amy43", "Zia", "Bob", ";runners", 11.1),
    ]
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {br_tablename}")
    assert cursor.fetchall() == expected_table_data

    if os_path_exists(zia_csv_filepath):
        os_remove(zia_csv_filepath)


def test_insert_idea_csv_ChangesDBState_CanCreateTable(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str],
):
    """Test the insert_csv function using pytest."""
    # ESTABLISH
    conn, test_csv_filepath = setup_database_and_csv
    # Create a new CSV file
    zia_csv_filepath = "zia_brXXXXX.csv"
    with open(zia_csv_filepath, "w", newline="", encoding="utf-8") as csv_file:
        csv_file.write(
            f"{event_int_str()},{face_name_str()},{moment_label_str()},{belief_name_str()},{voice_name_str()},{group_title_str()},{gogo_want_str()}\n"
        )
        csv_file.write("7,Zia,Amy55,Yao,Zia,;swimmers,10.2\n")
        csv_file.write("8,Zia,Amy43,Zia,Bob,;runners,11.1\n")

    br_tablename = "brXXXXX"
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({br_tablename})")
    columns = cursor.fetchall()
    assert columns == []

    # WHEN
    insert_idea_csv(zia_csv_filepath, conn, br_tablename)

    # THEN
    expected_table_data = [
        (7, "Zia", "Amy55", "Yao", "Zia", ";swimmers", 10.2),
        (8, "Zia", "Amy43", "Zia", "Bob", ";runners", 11.1),
    ]
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {br_tablename}")
    assert cursor.fetchall() == expected_table_data

    if os_path_exists(zia_csv_filepath):
        os_remove(zia_csv_filepath)


def test_create_idea_table_from_csv_NopackableExists(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str],
):
    # ESTABLISH
    conn, test_csv_filepath = setup_database_and_csv
    br_tablename = "new_test_table"
    create_idea_table_from_csv(test_csv_filepath, conn, br_tablename)
    insert_idea_csv(test_csv_filepath, conn, br_tablename)
    before_table_data = [
        (3, "Sue", "Amy43", "Bob", "Bob", ";runners", 6.5),
        (3, "Sue", "Amy43", "Yao", "Bob", ";runners", 7.5),
    ]
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {br_tablename}")
    assert cursor.fetchall() == before_table_data

    # WHEN
    create_idea_table_from_csv(test_csv_filepath, conn, br_tablename)

    # THEN
    cursor.execute(f"SELECT * FROM {br_tablename}")
    assert cursor.fetchall() == before_table_data
