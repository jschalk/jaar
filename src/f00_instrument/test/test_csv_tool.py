from src.f00_instrument.file import create_path, set_dir, save_file
from src.f00_instrument.csv_toolbox import read_csv_with_types
from src.f00_instrument.examples.instrument_env import (
    get_instrument_temp_env_dir,
    env_dir_setup_cleanup,
)


def test_read_csv_with_types(env_dir_setup_cleanup):
    """Test read_csv_with_types with various data types."""
    # ESTABLISH
    set_dir(get_instrument_temp_env_dir())
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
"""
    save_file(get_instrument_temp_env_dir(), "test.csv", csv_str)
    # with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
    #     writer = csv_writer(csv_file)
    #     writer.writerow(["id", "name", "price", "available", "fizz"])
    #     writer.writerow(["1", "Widget", "19.99", "True", "fizz"])
    #     writer.writerow(["2", "Gadget", "5.49", "False", "buzz"])
    #     writer.writerow(["3", "Doodad", "12.00", "true", "fizz"])
    #     writer.writerow(["4", "Doodad", "12.00", "truee", "fizz"])
    csv_path = create_path(get_instrument_temp_env_dir(), "test.csv")

    # WHEN
    result = read_csv_with_types(csv_path, column_types)

    # THEN
    expected = [
        (1, "Widget", 19.99, True, "fizz"),
        (2, "Gadget", 5.49, False, "buzz"),
        (3, "Doodad", 12.00, True, "fizz"),
        (4, "Doodad", 12.00, None, "fizz"),
    ]
    assert result == expected
