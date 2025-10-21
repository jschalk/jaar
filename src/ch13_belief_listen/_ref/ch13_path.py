from src.ch01_py.file_toolbox import (
    create_directory_path,
    create_path,
    get_json_filename,
)
from src.ch04_rope.rope import get_all_rope_labels, rebuild_rope
from src.ch13_belief_listen._ref.ch13_semantic_types import (
    BeliefName,
    LabelTerm,
    MomentLabel,
)


def treasury_filename() -> str:
    return "treasury.db"


def create_keeps_dir_path(
    moment_mstr_dir: str, moment_label: LabelTerm, belief_name: BeliefName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\keeps"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    return create_path(belief_dir, "keeps")


class _keep_ropeMissingException(Exception):
    pass


def create_keep_rope_path(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\keeps\\planroot\\level1_label"""
    if keep_rope is None:
        raise _keep_ropeMissingException(
            f"'{belief_name}' cannot save to keep_path because it does not have keep_rope."
        )

    keep_root = "planroot"
    keep_rope = rebuild_rope(keep_rope, moment_label, keep_root)
    x_list = get_all_rope_labels(keep_rope, knot)
    keep_sub_path = create_directory_path(x_list=[*x_list])
    keeps_dir = create_keeps_dir_path(moment_mstr_dir, moment_label, belief_name)
    return create_path(keeps_dir, keep_sub_path)


def create_keep_dutys_path(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\keeps\\level1\\dutys"""
    x_keep_path = create_keep_rope_path(
        moment_mstr_dir, belief_name, moment_label, keep_rope, knot
    )
    return create_path(x_keep_path, "dutys")


def create_keep_duty_path(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: str,
    duty_belief: BeliefName,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\keeps\\level1\\dutys\\duty_belief.json"""
    x_dutys_path = create_keep_dutys_path(
        moment_mstr_dir, belief_name, moment_label, keep_rope, knot
    )
    return create_path(x_dutys_path, get_json_filename(duty_belief))


def create_keep_visions_path(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\keeps\\level1\\visions"""
    x_keep_path = create_keep_rope_path(
        moment_mstr_dir, belief_name, moment_label, keep_rope, knot
    )
    return create_path(x_keep_path, "visions")


def create_keep_grades_path(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\keeps\\level1\\grades"""
    x_keep_path = create_keep_rope_path(
        moment_mstr_dir, belief_name, moment_label, keep_rope, knot
    )
    return create_path(x_keep_path, "grades")


def create_keep_grade_path(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: str,
    grade_belief_name: BeliefName,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\keeps\\level1\\grades\\grade_belief_name.json"""
    x_keep_path = create_keep_grades_path(
        moment_mstr_dir, belief_name, moment_label, keep_rope, knot
    )
    return create_path(x_keep_path, get_json_filename(grade_belief_name))


def create_treasury_db_path(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    "Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\keeps\\level1\\treasury.db"
    keep_path = create_keep_rope_path(
        moment_mstr_dir=moment_mstr_dir,
        belief_name=belief_name,
        moment_label=moment_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    return create_path(keep_path, treasury_filename())
