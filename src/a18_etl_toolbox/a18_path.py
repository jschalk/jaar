from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.term import BelieverName, LabelTerm


def create_belief_mstr_path(world_dir: str):
    """Returns path: world_dir\\belief_mstr"""
    return create_path(world_dir, "belief_mstr")


def create_belief_ote1_csv_path(belief_mstr_dir: str, belief_label: LabelTerm):
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\belief_ote1_agg.csv"""
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_path = create_path(beliefs_dir, belief_label)
    return create_path(belief_path, "belief_ote1_agg.csv")


def create_belief_ote1_json_path(belief_mstr_dir: str, belief_label: LabelTerm):
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\belief_ote1_agg.json"""
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_path = create_path(beliefs_dir, belief_label)
    return create_path(belief_path, "belief_ote1_agg.json")


def create_stances_dir_path(belief_mstr_dir: str) -> str:
    """Returns path: belief_mstr_dir\\stances"""
    return create_path(belief_mstr_dir, "stances")


def create_stances_believer_dir_path(
    belief_mstr_dir: str, believer_name: BelieverName
) -> str:
    """Returns path: belief_mstr_dir\\stances\\believer_name"""
    stances_dir = create_path(belief_mstr_dir, "stances")
    return create_path(stances_dir, believer_name)


def create_stance0001_path(output_dir: str) -> str:
    """Returns path: output_dir\\stance0001.xlsx"""
    return create_path(output_dir, "stance0001.xlsx")


def create_last_run_metrics_path(world_dir: str) -> str:
    """Returns path: world_dir\\last_run_metrics.json"""
    return create_path(world_dir, "last_run_metrics.json")


def create_world_db_path(world_dir: str) -> str:
    "Returns path: belief_mstr_dir\\world.db"
    return create_path(world_dir, "world.db")
