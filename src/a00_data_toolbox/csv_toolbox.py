from csv import (
    DictReader as csv_DictReader,
    DictWriter as csv_DictWriter,
    reader as csv_reader,
    writer as csv_writer,
)
from io import StringIO as io_StringIO
from os import makedirs as os_makedirs
from os.path import exists as os_path_exists, join as os_path_join
from sqlite3 import connect as sqlite3_connect


def open_csv_with_types(csv_path, column_types):
    """
    Reads a CSV file and returns a list of tuples where each value is converted
    to a type from the provided column type dictionary.

    :param csv_path: Path to the CSV file.
    :param column_types: Dictionary mapping column names to data types.
    :return: List of tuples with correctly typed values.
    """
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv_reader(csv_file)
        headers = next(reader)  # Read the header row

        result = [tuple(headers)]
        for row in reader:
            typed_list = []
            for header, value in zip(headers, row):
                try:
                    if column_types[header] == "INTEGER":
                        if value == "":
                            typed_list.append(None)
                        else:
                            typed_list.append(int(value))
                    elif column_types[header] == "TEXT":
                        typed_list.append(str(value))
                    elif column_types[header] == "REAL":
                        if value == "":
                            typed_list.append(None)
                        else:
                            typed_list.append(float(value))
                    elif column_types[header] == "BOOLEAN":
                        if value.lower() == "true":
                            typed_list.append(True)
                        elif value.lower() == "false":
                            typed_list.append(False)
                        else:
                            typed_list.append(None)
                except Exception:
                    typed_list.append(value)

            result.append(tuple(typed_list))

    return result


def export_sqlite_tables_to_csv(db_path, output_dir="."):
    """
    Exports all tables from the SQLite database to CSV files.
    Each file is named <table_name>_<row_count>.csv.

    Args:
        db_path (str): Path to the SQLite database file.
        output_dir (str): Directory to save the CSV files (default is current directory).
    """
    if not os_path_exists(output_dir):
        os_makedirs(output_dir)

    with sqlite3_connect(db_path) as conn:
        cursor = conn.cursor()

        # Get list of all table names
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = cursor.fetchall()

        for (table_name,) in tables:
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]

            # Get table data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Get column names
            column_names = [description[0] for description in cursor.description]

            # Write to CSV
            file_name = f"{table_name}_{row_count}.csv"
            file_path = os_path_join(output_dir, file_name)

            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv_writer(f)
                writer.writerow(column_names)
                writer.writerows(rows)
    conn.close()


def replace_csv_column_from_string(
    csv_string: str, column_name: str, new_value: str
) -> str:
    """
    Replace all values in the specified column with new_value in the input CSV string.

    Args:
        csv_string (str): CSV content as a string.
        column_name (str): Name of the column to replace.
        new_value (str): Value to insert in place of each column value.

    Returns:
        str: Modified CSV content as a string.
    """
    input_io = io_StringIO(csv_string)
    output_io = io_StringIO()

    reader = csv_DictReader(input_io)
    fieldnames = reader.fieldnames

    if fieldnames is None:
        raise ValueError("csv_string cannot be parsed into columns with headers.")

    if column_name not in fieldnames:
        raise ValueError(f"Column '{column_name}' not found in CSV headers.")

    writer = csv_DictWriter(output_io, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        row[column_name] = new_value
        writer.writerow(row)

    csv_str = output_io.getvalue()
    return csv_str.replace("\r", "")


def delete_column_from_csv_string(csv_string: str, column_to_delete: str) -> str:
    """
    Removes a column from a CSV string. If the column doesn't exist, returns the original CSV.

    Args:
        csv_string (str): The input CSV content as a string.
        column_to_delete (str): The name of the column to remove.

    Returns:
        str: The CSV string with the column removed, or original if not found.
    """
    input_io = io_StringIO(csv_string)
    output_io = io_StringIO()

    reader = csv_DictReader(input_io)

    # If column not found, return original
    if column_to_delete not in reader.fieldnames:
        return csv_string

    # Filtered columns
    fieldnames = [field for field in reader.fieldnames if field != column_to_delete]
    writer = csv_DictWriter(output_io, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        row.pop(column_to_delete, None)
        writer.writerow(row)

    return output_io.getvalue()
