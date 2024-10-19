from src.f00_instrument.file import create_dir, save_file
from pandas import DataFrame


def get_sorting_priority_atom_args() -> list[str]:
    return [
        "acct_id",
        "group_id",
        "parent_road",
        "label",
        "road",
        "base",
        "need",
        "pick",
        "team_id",
        "awardee_id",
        "healer_id",
        "numor",
        "denom",
        "addin",
        "base_item_active_requisite",
        "begin",
        "close",
        "credit_belief",
        "debtit_belief",
        "credit_vote",
        "debtit_vote",
        "credor_respect",
        "debtor_respect",
        "fopen",
        "fnigh",
        "fund_pool",
        "give_force",
        "gogo_want",
        "mass",
        "max_tree_traverse",
        "morph",
        "nigh",
        "open",
        "divisor",
        "pledge",
        "problem_bool",
        "purview_timestamp",
        "stop_want",
        "take_force",
        "tally",
        "fund_coin",
        "penny",
        "respect_bit",
    ]


def save_dataframe_to_csv(x_dt: DataFrame, x_dir: str, x_filename: str):
    x_csv_str = get_orderd_csv(x_dt, get_sorting_priority_atom_args())
    save_file(x_dir, x_filename, x_csv_str)


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
