from src.f00_instrument.file import create_file_path
from src.f09_brick.brick_config import get_brick_numbers, get_quick_bricks_column_ref
from src.f09_brick.pandas_tool import get_all_excel_sheet_names
from pandas import read_excel as pandas_read_excel


def get_all_excel_bricksheets(dir: str) -> set[tuple[str, str, str]]:
    return get_all_excel_sheet_names(dir, get_brick_numbers())


def get_all_brick_dataframes(dir: str) -> set[tuple[str, str, str]]:
    bricksheets = get_all_excel_bricksheets(dir)
    candidate_bricks = set()
    for dir, filename, sheet_name in bricksheets:
        for brick_number in get_brick_numbers():
            if sheet_name.find(brick_number) >= 0:
                candidate_bricks.add((dir, filename, sheet_name, brick_number))

    valid_bricks = set()
    for dir, filename, sheet_name, brick_number in candidate_bricks:
        brick_columns = get_quick_bricks_column_ref().get(brick_number)
        file_path = create_file_path(dir, filename)
        df = pandas_read_excel(file_path, sheet_name=sheet_name)
        if brick_columns.issubset(set(df.columns)):
            valid_bricks.add((dir, filename, sheet_name))

    return valid_bricks
