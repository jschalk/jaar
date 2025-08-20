from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.term import BelieverName, LabelTerm


def create_coin_mstr_path(world_dir: str):
    """Returns path: world_dir\\coin_mstr"""
    return create_path(world_dir, "coin_mstr")


def create_coin_ote1_csv_path(coin_mstr_dir: str, coin_label: LabelTerm):
    """Returns path: coin_mstr_dir\\coins\\coin_label\\coin_ote1_agg.csv"""
    coins_dir = create_path(coin_mstr_dir, "coins")
    coin_path = create_path(coins_dir, coin_label)
    return create_path(coin_path, "coin_ote1_agg.csv")


def create_coin_ote1_json_path(coin_mstr_dir: str, coin_label: LabelTerm):
    """Returns path: coin_mstr_dir\\coins\\coin_label\\coin_ote1_agg.json"""
    coins_dir = create_path(coin_mstr_dir, "coins")
    coin_path = create_path(coins_dir, coin_label)
    return create_path(coin_path, "coin_ote1_agg.json")


def create_stances_dir_path(coin_mstr_dir: str) -> str:
    """Returns path: coin_mstr_dir\\stances"""
    return create_path(coin_mstr_dir, "stances")


def create_stances_believer_dir_path(
    coin_mstr_dir: str, believer_name: BelieverName
) -> str:
    """Returns path: coin_mstr_dir\\stances\\believer_name"""
    stances_dir = create_path(coin_mstr_dir, "stances")
    return create_path(stances_dir, believer_name)


def create_stance0001_path(output_dir: str) -> str:
    """Returns path: output_dir\\stance0001.xlsx"""
    return create_path(output_dir, "stance0001.xlsx")


def create_last_run_metrics_path(world_dir: str) -> str:
    """Returns path: world_dir\\last_run_metrics.json"""
    return create_path(world_dir, "last_run_metrics.json")


def create_world_db_path(world_dir: str) -> str:
    "Returns path: coin_mstr_dir\\world.db"
    return create_path(world_dir, "world.db")
