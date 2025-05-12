from src.a00_data_toolbox.file_toolbox import create_path
from src.a17_creed_logic.creed_config import (
    get_creed_numbers,
    get_quick_creeds_column_ref,
)
from src.a17_creed_logic.creed_db_tool import get_all_excel_sheet_names
from pandas import read_excel as pandas_read_excel, DataFrame, Series as PandaSeries
from dataclasses import dataclass


def get_all_excel_creedsheets(dir: str) -> set[tuple[str, str, str]]:
    return get_all_excel_sheet_names(dir, get_creed_numbers())


@dataclass
class CreedFileRef:
    file_dir: str = None
    filename: str = None
    sheet_name: str = None
    creed_number: str = None

    def get_csv_filename(self) -> str:
        return "" if self.creed_number is None else f"{self.creed_number}.csv"


def get_all_creed_dataframes(dir: str) -> list[CreedFileRef]:
    creedsheets = get_all_excel_creedsheets(dir)
    candidate_creeds = set()
    for dir, filename, sheet_name in creedsheets:
        for creed_number in get_creed_numbers():
            if sheet_name.find(creed_number) >= 0:
                candidate_creeds.add((dir, filename, sheet_name, creed_number))

    valid_creeds = []
    for dir, filename, sheet_name, creed_number in candidate_creeds:
        creed_columns = get_quick_creeds_column_ref().get(creed_number)
        file_path = create_path(dir, filename)
        df = pandas_read_excel(file_path, sheet_name=sheet_name)
        if creed_columns.issubset(set(df.columns)):
            valid_creeds.append(CreedFileRef(dir, filename, sheet_name, creed_number))

    return valid_creeds
