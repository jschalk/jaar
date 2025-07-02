from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.term import BelieverName

STANCE0001_FILENAME = "stance0001.xlsx"


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
