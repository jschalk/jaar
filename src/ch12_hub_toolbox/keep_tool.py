from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.file_toolbox import (
    create_path,
    open_file,
    save_json,
    set_dir,
)
from src.ch07_belief_logic.belief_main import BeliefUnit, get_beliefunit_from_json
from src.ch11_bud_logic._ref.ch11_semantic_types import (
    BeliefName,
    LabelTerm,
    MomentLabel,
)
from src.ch12_hub_toolbox.ch12_path import (
    create_keep_duty_path,
    create_keep_rope_path,
    create_treasury_db_path,
)


def create_keep_path_dir_if_missing(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: str,
):
    keep_path = create_keep_rope_path(
        moment_mstr_dir,
        belief_name,
        moment_label,
        keep_rope,
        knot,
    )
    set_dir(keep_path)


def treasury_db_file_exists(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> bool:
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=belief_name,
        moment_label=moment_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    return os_path_exists(treasury_db_path)


def create_treasury_db_file(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> None:
    create_keep_path_dir_if_missing(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=belief_name,
        moment_label=moment_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    treasury_db_path = create_treasury_db_path(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=belief_name,
        moment_label=moment_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    conn = sqlite3_connect(treasury_db_path)
    conn.close()


def save_duty_belief(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: str,
    duty_belief: BeliefUnit,
) -> None:
    duty_path = create_keep_duty_path(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=belief_name,
        moment_label=moment_label,
        keep_rope=keep_rope,
        knot=knot,
        duty_belief=duty_belief.belief_name,
    )
    save_json(duty_path, None, duty_belief.to_dict())


def get_duty_belief(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: str,
    duty_belief_name: BeliefName,
) -> BeliefUnit:
    keep_duty_path = create_keep_duty_path(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=belief_name,
        moment_label=moment_label,
        keep_rope=keep_rope,
        knot=knot,
        duty_belief=duty_belief_name,
    )
    if os_path_exists(keep_duty_path) is False:
        return None
    file_content = open_file(keep_duty_path)
    return get_beliefunit_from_json(file_content)
