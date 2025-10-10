from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch11_bud_logic._ref.ch11_semantic_types import BeliefName, LabelTerm


def create_moment_mstr_path(world_dir: str):
    """Returns path: world_dir\\moment_mstr"""
    return create_path(world_dir, "moment_mstr")


def create_moment_ote1_csv_path(moment_mstr_dir: str, moment_label: LabelTerm):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\moment_ote1_agg.csv"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_path = create_path(moments_dir, moment_label)
    return create_path(moment_path, "moment_ote1_agg.csv")


def create_moment_ote1_json_path(moment_mstr_dir: str, moment_label: LabelTerm):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\moment_ote1_agg.json"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_path = create_path(moments_dir, moment_label)
    return create_path(moment_path, "moment_ote1_agg.json")


def create_stances_dir_path(moment_mstr_dir: str) -> str:
    """Returns path: moment_mstr_dir\\stances"""
    return create_path(moment_mstr_dir, "stances")


def create_stances_belief_dir_path(
    moment_mstr_dir: str, belief_name: BeliefName
) -> str:
    """Returns path: moment_mstr_dir\\stances\\belief_name"""
    stances_dir = create_path(moment_mstr_dir, "stances")
    return create_path(stances_dir, belief_name)


def create_stance0001_path(output_dir: str) -> str:
    """Returns path: output_dir\\stance0001.xlsx"""
    return create_path(output_dir, "stance0001.xlsx")


def create_last_run_metrics_path(world_dir: str) -> str:
    """Returns path: world_dir\\last_run_metrics.json"""
    return create_path(world_dir, "last_run_metrics.json")


def create_world_db_path(world_dir: str) -> str:
    "Returns path: moment_mstr_dir\\world.db"
    return create_path(world_dir, "world.db")
