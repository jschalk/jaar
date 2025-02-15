from src.f00_instrument.file import create_path
from src.f01_road.deal import fisc_title_str, owner_name_str
from src.f04_gift.atom_config import (
    face_name_str,
    event_int_str,
    acct_name_str,
    group_label_str,
    gogo_want_str,
)
from src.f09_idea.idea_config import get_idea_sqlite_types
from src.f09_idea.examples.idea_env import idea_env_setup_cleanup, idea_fiscs_dir
from src.f09_idea.idea_db_tool import create_idea_table_from_csv, insert_idea_csv
from pytest import fixture as pytest_fixture
from os import remove as os_remove
from os.path import exists as os_path_exists
from numpy import nan as numpy_nan, float64
from sqlite3 import Connection as sqlite3_Connection, connect as sqlite3_connect


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
    #         fisc_title TEXT,
    #         owner_name TEXT,
    #         acct_name TEXT,
    #         group_label TEXT,
    #         gogo_want REAL
    #     )
    # """
    # )
    # conn.commit()

    # Create a test CSV file
    with open(test_csv_filepath, "w", newline="", encoding="utf-8") as csv_file:
        csv_file.write(
            f"{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()},{group_label_str()},{gogo_want_str()}\n"
        )
        csv_file.write("Sue,3,Accord43,Bob,Bob,;runners,6.5\n")
        csv_file.write("Sue,3,Accord43,Yao,Bob,;runners,7.5\n")

    yield conn, test_csv_filepath

    # Clean up
    conn.close()
    if os_path_exists(test_db):
        os_remove(test_db)
    if os_path_exists(test_csv_filepath):
        os_remove(test_csv_filepath)


def test_create_idea_table_from_csv_ChangesDBState(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str]
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

    # THEN Verify the table was created correctly
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({new_table})")
    columns = cursor.fetchall()

    # Expected column definitions
    expected_columns = [
        (0, face_name_str(), "TEXT", 0, None, 0),
        (1, event_int_str(), "INTEGER", 0, None, 0),
        (2, fisc_title_str(), "TEXT", 0, None, 0),
        (3, owner_name_str(), "TEXT", 0, None, 0),
        (4, acct_name_str(), "TEXT", 0, None, 0),
        (5, group_label_str(), "TEXT", 0, None, 0),
        (6, gogo_want_str(), "REAL", 0, None, 0),
    ]
    assert columns == expected_columns
    column_types = get_idea_sqlite_types()
    get_idea_sqlite_types_columns = [
        (0, face_name_str(), column_types.get(face_name_str()), 0, None, 0),
        (1, event_int_str(), column_types.get(event_int_str()), 0, None, 0),
        (2, fisc_title_str(), column_types.get(fisc_title_str()), 0, None, 0),
        (3, owner_name_str(), column_types.get(owner_name_str()), 0, None, 0),
        (4, acct_name_str(), column_types.get(acct_name_str()), 0, None, 0),
        (5, group_label_str(), column_types.get(group_label_str()), 0, None, 0),
        (6, gogo_want_str(), column_types.get(gogo_want_str()), 0, None, 0),
    ]
    assert columns == get_idea_sqlite_types_columns


def test_insert_idea_csv_ChangesDBState_add_to_empty_table(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str]
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
    # Verify the data was inserted correctly
    cursor.execute(f"SELECT * FROM {br_tablename}")
    rows = cursor.fetchall()
    expected_data = [
        ("Sue", 3, "Accord43", "Bob", "Bob", ";runners", 6.5),
        ("Sue", 3, "Accord43", "Yao", "Bob", ";runners", 7.5),
    ]
    assert rows == expected_data


def test_insert_idea_csv_ChangesDBState_CorrectlyInserts(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str], idea_env_setup_cleanup
):
    """Test the insert_csv function using pytest."""
    # ESTABLISH
    conn, test_csv_filepath = setup_database_and_csv
    # Create a new CSV file
    zia_csv_filepath = "zia_brXXXXX.csv"
    with open(zia_csv_filepath, "w", newline="", encoding="utf-8") as csv_file:
        csv_file.write(
            f"{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()},{group_label_str()},{gogo_want_str()}\n"
        )
        csv_file.write("Zia,7,Accord55,Yao,Zia,;swimmers,10.2\n")
        csv_file.write("Zia,8,Accord43,Zia,Bob,;runners,11.1\n")

    br_tablename = "brXXXXX"
    create_idea_table_from_csv(test_csv_filepath, conn, br_tablename)
    insert_idea_csv(test_csv_filepath, conn, br_tablename)
    before_table_data = [
        ("Sue", 3, "Accord43", "Bob", "Bob", ";runners", 6.5),
        ("Sue", 3, "Accord43", "Yao", "Bob", ";runners", 7.5),
    ]
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {br_tablename}")
    assert cursor.fetchall() == before_table_data

    # WHEN
    insert_idea_csv(zia_csv_filepath, conn, br_tablename)

    # THEN
    expected_table_data = [
        ("Sue", 3, "Accord43", "Bob", "Bob", ";runners", 6.5),
        ("Sue", 3, "Accord43", "Yao", "Bob", ";runners", 7.5),
        ("Zia", 7, "Accord55", "Yao", "Zia", ";swimmers", 10.2),
        ("Zia", 8, "Accord43", "Zia", "Bob", ";runners", 11.1),
    ]
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {br_tablename}")
    assert cursor.fetchall() == expected_table_data

    if os_path_exists(zia_csv_filepath):
        os_remove(zia_csv_filepath)


def test_insert_idea_csv_ChangesDBState_CanCreateTable(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str]
):
    """Test the insert_csv function using pytest."""
    # ESTABLISH
    conn, test_csv_filepath = setup_database_and_csv
    # Create a new CSV file
    zia_csv_filepath = "zia_brXXXXX.csv"
    with open(zia_csv_filepath, "w", newline="", encoding="utf-8") as csv_file:
        csv_file.write(
            f"{face_name_str()},{event_int_str()},{fisc_title_str()},{owner_name_str()},{acct_name_str()},{group_label_str()},{gogo_want_str()}\n"
        )
        csv_file.write("Zia,7,Accord55,Yao,Zia,;swimmers,10.2\n")
        csv_file.write("Zia,8,Accord43,Zia,Bob,;runners,11.1\n")

    br_tablename = "brXXXXX"
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({br_tablename})")
    columns = cursor.fetchall()
    assert columns == []

    # WHEN
    insert_idea_csv(zia_csv_filepath, conn, br_tablename)

    # THEN
    expected_table_data = [
        ("Zia", 7, "Accord55", "Yao", "Zia", ";swimmers", 10.2),
        ("Zia", 8, "Accord43", "Zia", "Bob", ";runners", 11.1),
    ]
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {br_tablename}")
    assert cursor.fetchall() == expected_table_data

    if os_path_exists(zia_csv_filepath):
        os_remove(zia_csv_filepath)


def test_create_idea_table_from_csv_DoesNothingIfTableExists(
    setup_database_and_csv: tuple[sqlite3_Connection, str, str]
):
    # ESTABLISH
    conn, test_csv_filepath = setup_database_and_csv
    br_tablename = "new_test_table"
    create_idea_table_from_csv(test_csv_filepath, conn, br_tablename)
    insert_idea_csv(test_csv_filepath, conn, br_tablename)
    before_table_data = [
        ("Sue", 3, "Accord43", "Bob", "Bob", ";runners", 6.5),
        ("Sue", 3, "Accord43", "Yao", "Bob", ";runners", 7.5),
    ]
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {br_tablename}")
    assert cursor.fetchall() == before_table_data

    # WHEN
    create_idea_table_from_csv(test_csv_filepath, conn, br_tablename)

    # THEN
    cursor.execute(f"SELECT * FROM {br_tablename}")
    assert cursor.fetchall() == before_table_data
