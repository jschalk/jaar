from src._instrument.python import place_obj_in_dict, get_nested_value
from src._road.road import RealID, OwnerID
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


def get_csv_real_id_owner_id_metrics(
    headerless_csv: str, delimiter: str = None
) -> dict[RealID, dict[OwnerID, int]]:
    y_dict = {}
    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    for row in x_reader:
        real_owner_count = get_nested_value(y_dict, [row[0], row[1]], True)
        if not real_owner_count:
            real_owner_count = 1
        else:
            real_owner_count += 1
        place_obj_in_dict(y_dict, [row[0], row[1]], real_owner_count)
    return y_dict


def create_filtered_csv_dict(
    headerless_csv: str, delimiter: str = None
) -> dict[RealID, dict[OwnerID, str]]:
    io_dict = {}
    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    for row in x_reader:
        real_owner_io = get_nested_value(io_dict, [row[0], row[1]], True)
        if not real_owner_io:
            real_owner_io = io_StringIO()
        new_csv_writer = csv_writer(real_owner_io, delimiter=",")
        new_csv_writer.writerow(row)
        place_obj_in_dict(io_dict, [row[0], row[1]], real_owner_io)

    x_dict = {}
    for real_id, owner_id_dict in io_dict.items():
        for owner_id, io_function in owner_id_dict.items():
            real_owner_csv = io_function.getvalue()
            real_owner_csv = real_owner_csv.replace("\r", "")
            place_obj_in_dict(x_dict, [real_id, owner_id], real_owner_csv)

    return x_dict
