from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.file_toolbox import create_path, save_json, set_dir
from src.a01_term_logic.term import BeliefLabel, BelieverName, LabelTerm
from src.a06_believer_logic.believer import BelieverUnit
from src.a12_hub_toolbox.a12_path import (
    create_keep_duty_path,
    create_keep_rope_path,
    create_treasury_db_path,
)


def create_keep_path_dir_if_missing(
    belief_mstr_dir: str,
    believer_name: BelieverName,
    belief_label: BeliefLabel,
    keep_rope: LabelTerm,
    knot: str,
):
    keep_path = create_keep_rope_path(
        belief_mstr_dir,
        believer_name,
        belief_label,
        keep_rope,
        knot,
    )
    set_dir(keep_path)


def treasury_db_file_exists(
    belief_mstr_dir: str,
    believer_name: BelieverName,
    belief_label: BeliefLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> bool:
    treasury_db_path = create_treasury_db_path(
        belief_mstr_dir=belief_mstr_dir,
        believer_name=believer_name,
        belief_label=belief_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    return os_path_exists(treasury_db_path)


def create_treasury_db_file(
    belief_mstr_dir: str,
    believer_name: BelieverName,
    belief_label: BeliefLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> None:
    create_keep_path_dir_if_missing(
        belief_mstr_dir=belief_mstr_dir,
        believer_name=believer_name,
        belief_label=belief_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    treasury_db_path = create_treasury_db_path(
        belief_mstr_dir=belief_mstr_dir,
        believer_name=believer_name,
        belief_label=belief_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    conn = sqlite3_connect(treasury_db_path)
    conn.close()


def save_duty_believer(
    belief_mstr_dir: str,
    believer_name: BelieverName,
    belief_label: BeliefLabel,
    keep_rope: LabelTerm,
    knot: str,
    duty_believer: BelieverUnit,
) -> None:
    duty_path = create_keep_duty_path(
        belief_mstr_dir=belief_mstr_dir,
        believer_name=believer_name,
        belief_label=belief_label,
        keep_rope=keep_rope,
        knot=knot,
        duty_believer=duty_believer.believer_name,
    )
    save_json(duty_path, None, duty_believer.get_dict())
