from src.ch01_py.file_toolbox import create_path
from src.ch09_belief_lesson._ref.ch09_semantic_types import BeliefName, MomentLabel

MOMENT_FILENAME = "moment.json"


def create_moment_dir_path(moment_mstr_dir: str, moment_label: MomentLabel) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    return create_path(moments_dir, moment_label)


def create_moment_json_path(moment_mstr_dir: str, moment_label: MomentLabel) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\moment.json"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_path = create_path(moments_dir, moment_label)
    return create_path(moment_path, "moment.json")


def create_moment_beliefs_dir_path(
    moment_mstr_dir: str, moment_label: MomentLabel
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    return create_path(moment_dir, "beliefs")


def create_belief_dir_path(
    moment_mstr_dir: str, moment_label: MomentLabel, belief_name: BeliefName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name"""

    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    return create_path(beliefs_dir, belief_name)


def create_atoms_dir_path(
    moment_mstr_dir: str, moment_label: MomentLabel, belief_name: BeliefName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\atoms"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    return create_path(belief_dir, "atoms")


def create_lessons_dir_path(
    moment_mstr_dir: str, moment_label: MomentLabel, belief_name: BeliefName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\lessons"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    return create_path(belief_dir, "lessons")


def create_gut_path(
    moment_mstr_dir: str, moment_label: MomentLabel, belief_name: BeliefName
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\gut\\belief_name.json"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    gut_dir = create_path(belief_dir, "gut")
    return create_path(gut_dir, f"{belief_name}.json")


def create_job_path(
    moment_mstr_dir: str, moment_label: MomentLabel, belief_name: BeliefName
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\job\\belief_name.json"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    job_dir = create_path(belief_dir, "job")
    return create_path(job_dir, f"{belief_name}.json")
