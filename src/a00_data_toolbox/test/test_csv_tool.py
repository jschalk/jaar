from csv import reader as csv_reader
from pathlib import Path
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.csv_toolbox import (
    export_sqlite_tables_to_csv,
    open_csv_with_types,
)
from src.a00_data_toolbox.file_toolbox import create_path, save_file, set_dir
from src.a00_data_toolbox.test._util.a00_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_open_csv_with_types(env_dir_setup_cleanup):
    """Test open_csv_with_types with various data types."""
    # ESTABLISH
    set_dir(get_module_temp_dir())
    column_types = {
        "id": "INTEGER",
        "name": "TEXT",
        "price": "REAL",
        "available": "BOOLEAN",
    }

    # Create test CSV file
    csv_str = """id,name,price,available,fizz
1,Widget,19.99,True,fizz
2,Gadget,5.49,False,buzz
3,Doodad,12.00,true,fizz
4,Doodad,12.00,truee,fizz
,Doodad,,truee,fizz
"""
    save_file(get_module_temp_dir(), "test.csv", csv_str)
    # with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
    #     writer = csv_writer(csv_file)
    #     writer.writerow(["id", "name", "price", "available", "fizz"])
    #     writer.writerow(["1", "Widget", "19.99", "True", "fizz"])
    #     writer.writerow(["2", "Gadget", "5.49", "False", "buzz"])
    #     writer.writerow(["3", "Doodad", "12.00", "true", "fizz"])
    #     writer.writerow(["4", "Doodad", "12.00", "truee", "fizz"])
    csv_path = create_path(get_module_temp_dir(), "test.csv")

    # WHEN
    generated_rows = open_csv_with_types(csv_path, column_types)

    # THEN
    expected_rows = [
        ("id", "name", "price", "available", "fizz"),
        (1, "Widget", 19.99, True, "fizz"),
        (2, "Gadget", 5.49, False, "buzz"),
        (3, "Doodad", 12.00, True, "fizz"),
        (4, "Doodad", 12.00, None, "fizz"),
        (None, "Doodad", None, None, "fizz"),
    ]
    print(f"{generated_rows}")
    assert generated_rows == expected_rows


def test_export_sqlite_tables_to_csv(env_dir_setup_cleanup):
    # 1. Create temporary SQLite DB
    tmp_path = Path(get_module_temp_dir())
    set_dir(tmp_path)
    db_path = tmp_path / "test.db"
    print(f"{db_path=}")
    with sqlite3_connect(db_path) as conn:
        cursor = conn.cursor()

        # 2. Create tables and insert data
        cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
        cursor.execute("INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob')")

        cursor.execute("CREATE TABLE products (sku TEXT, price REAL)")
        cursor.execute("INSERT INTO products VALUES ('ABC', 9.99)")
        conn.commit()

    # 3. Run export function
    export_sqlite_tables_to_csv(str(db_path), str(tmp_path))

    # 4. Check output files
    user_csv = tmp_path / "users_2.csv"
    product_csv = tmp_path / "products_1.csv"

    assert user_csv.exists()
    assert product_csv.exists()

    # 5. Check CSV contents (users table)
    with open(user_csv, newline="", encoding="utf-8") as f:
        reader = list(csv_reader(f))
        assert reader[0] == ["id", "name"]
        assert reader[1] == ["1", "Alice"]
        assert reader[2] == ["2", "Bob"]

    # 6. Check CSV contents (products table)
    with open(product_csv, newline="", encoding="utf-8") as f:
        reader = list(csv_reader(f))
        assert reader[0] == ["sku", "price"]
        assert reader[1] == ["ABC", "9.99"]
