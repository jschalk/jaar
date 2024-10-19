from src.f00_instrument.file import create_file_path, create_dir
from pandas import DataFrame


def save_dataframe_to_csv(x_dt: DataFrame, x_dir: str, x_filename: str):
    create_dir(x_dir)
    x_dt.to_csv(create_file_path(x_dir, x_filename), index=False)


def get_orderd_csv(x_dt: DataFrame, sorting_columns: list[str] = None) -> str:
    if sorting_columns is None:
        sorting_columns = []
    sort_columns_in_dt = set(sorting_columns).intersection(set(x_dt.columns))
    new_sorting_columns = [
        sort_col for sort_col in sorting_columns if sort_col in sort_columns_in_dt
    ]
    x_dt.sort_values(new_sorting_columns, inplace=True)
    x_dt.reset_index(inplace=True)
    x_dt.drop(columns=["index"], inplace=True)
    return x_dt.to_csv(index=False).replace("\r", "")
