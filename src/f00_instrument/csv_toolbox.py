from csv import reader as csv_reader


def open_csv_with_types(csv_path, column_types):
    """
    Reads a CSV file and returns a list of tuples where each value is converted
    based on the provided column type dictionary.

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
