from src._instrument.python import place_obj_in_dict, get_nested_value
from csv import reader as csv_reader, writer as csv_writer
from io import StringIO as io_StringIO


def extract_csv_headers(x_csv: str, delimiter: str = None) -> tuple[list[str], str]:
    x_reader = csv_reader(x_csv.splitlines(), delimiter=",")

    title_row = None
    x_count = 0
    si = io_StringIO()
    new_csv_writer = csv_writer(si, delimiter=",")
    for row in x_reader:
        if x_count == 0:
            title_row = row
        else:
            new_csv_writer.writerow(row)
        x_count += 1
    x_list = []
    if title_row is None:
        return x_list
    for column_num in range(len(title_row)):
        x_list.append(title_row[column_num])

    x_csv = si.getvalue()
    y_csv = x_csv.replace("\r", "")
    return x_list, y_csv


def get_csv_real_id_owner_id_dict(
    headerless_csv: str, delimiter: str = None
) -> dict[str, dict[str, str]]:
    y_dict = {}
    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    for row in x_reader:
        x_ref_count = get_nested_value(y_dict, [row[0], row[1]], True)
        if not x_ref_count:
            place_obj_in_dict(y_dict, [row[0], row[1]], 1)
    return y_dict
