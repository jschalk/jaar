from src.f00_instrument.file import create_file_path, create_dir
from pandas import DataFrame


def save_dataframe_to_csv(x_dt: DataFrame, x_dir: str, x_filename: str):
    file_path = create_file_path(x_dir, x_filename)
    create_dir(x_dir)
    x_dt.to_csv(file_path, index=False)


def get_orderd_csv(x_dt: DataFrame, sorting_columns: list[str] = None) -> str:
    if sorting_columns is None:
        sorting_columns = []
    x_dt.sort_values(sorting_columns, inplace=True)
    x_dt.reset_index(inplace=True)
    x_dt.drop(columns=["index"], inplace=True)
    return x_dt.to_csv(index=False).replace("\r", "")
