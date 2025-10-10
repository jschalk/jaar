from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.ch01_data_toolbox.dict_toolbox import get_empty_set_if_None
from src.ch01_data_toolbox.file_toolbox import (
    create_path,
    get_json_filename,
    open_file,
    save_json,
    set_dir,
)
from src.ch07_belief_logic.belief_main import BeliefUnit, get_beliefunit_from_json
from src.ch12_pack_file._ref.ch12_semantic_types import (
    BeliefName,
    LabelTerm,
    MomentLabel,
    RopeTerm,
)
from src.ch12_pack_file.packfilehandler import (
    open_gut_file,
    open_job_file,
    save_belief_file,
)
from src.ch13_belief_listen_logic._ref.ch13_path import (
    create_keep_duty_path,
    create_keep_rope_path,
    create_keep_visions_path,
    create_keeps_dir_path,
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


def save_all_gut_dutys(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    keep_ropes: set[RopeTerm],
    knot: str,
):
    gut = open_gut_file(moment_mstr_dir, moment_label, belief_name)
    for x_keep_rope in keep_ropes:
        save_duty_belief(
            moment_mstr_dir=moment_mstr_dir,
            belief_name=belief_name,
            moment_label=moment_label,
            keep_rope=x_keep_rope,
            knot=knot,
            duty_belief=gut,
        )


class get_keep_ropesException(Exception):
    pass


def get_keep_ropes(moment_mstr_dir, moment_label, belief_name) -> set[RopeTerm]:
    x_gut_belief = open_gut_file(moment_mstr_dir, moment_label, belief_name)
    x_gut_belief.cashout()
    if x_gut_belief.keeps_justified is False:
        x_str = f"Cannot get_keep_ropes from '{belief_name}' gut belief because 'BeliefUnit.keeps_justified' is False."
        raise get_keep_ropesException(x_str)
    if x_gut_belief.keeps_buildable is False:
        x_str = f"Cannot get_keep_ropes from '{belief_name}' gut belief because 'BeliefUnit.keeps_buildable' is False."
        raise get_keep_ropesException(x_str)
    belief_healer_dict = x_gut_belief._healers_dict.get(belief_name)
    if belief_healer_dict is None:
        return get_empty_set_if_None()
    keep_ropes = x_gut_belief._healers_dict.get(belief_name).keys()
    return get_empty_set_if_None(keep_ropes)


def get_perspective_belief(
    speaker: BeliefUnit, listener_name: BeliefName
) -> BeliefUnit:
    # get copy of belief without any metrics
    perspective_belief = get_beliefunit_from_json(speaker.get_json())
    perspective_belief.set_belief_name(listener_name)
    perspective_belief.cashout()
    return perspective_belief


def vision_file_exists(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: RopeTerm,
    knot: str,
    speaker_id: BeliefName,
) -> bool:
    keep_visions_path = create_keep_visions_path(
        moment_mstr_dir, belief_name, moment_label, keep_rope, knot
    )
    file_path = create_path(keep_visions_path, get_json_filename(speaker_id))
    return os_path_exists(file_path)


def get_vision_belief(
    moment_mstr_dir: str,
    belief_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: RopeTerm,
    knot: str,
    speaker_id: BeliefName,
) -> BeliefUnit:
    keep_visions_path = create_keep_visions_path(
        moment_mstr_dir, belief_name, moment_label, keep_rope, knot
    )
    if (
        vision_file_exists(
            moment_mstr_dir, belief_name, moment_label, keep_rope, knot, speaker_id
        )
        is False
    ):
        return None
    file_content = open_file(keep_visions_path, get_json_filename(speaker_id))
    return get_beliefunit_from_json(file_content)


def get_dw_perspective_belief(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    speaker_id: BeliefName,
    prespective_id: BeliefName,
) -> BeliefUnit:
    speaker_job = open_job_file(moment_mstr_dir, moment_label, speaker_id)
    return get_perspective_belief(speaker_job, prespective_id)


def rj_speaker_belief(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    keep_rope: RopeTerm,
    knot: str,
    healer_name: BeliefName,
    speaker_id: BeliefName,
) -> BeliefUnit:
    return get_vision_belief(
        moment_mstr_dir=moment_mstr_dir,
        moment_label=moment_label,
        belief_name=healer_name,
        keep_rope=keep_rope,
        knot=knot,
        speaker_id=speaker_id,
    )


def rj_perspective_belief(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    keep_rope: RopeTerm,
    knot: str,
    healer_name: BeliefName,
    speaker_id: BeliefName,
    perspective_id: BeliefName,
) -> BeliefUnit:
    speaker_vision = rj_speaker_belief(
        moment_mstr_dir,
        moment_label,
        keep_rope,
        knot,
        healer_name,
        speaker_id,
    )
    return get_perspective_belief(speaker_vision, perspective_id)


def save_vision_belief(
    moment_mstr_dir: str,
    healer_name: BeliefName,
    moment_label: MomentLabel,
    keep_rope: RopeTerm,
    knot: str,
    x_belief: BeliefUnit,
) -> None:
    x_filename = get_json_filename(x_belief.belief_name)
    keep_visions_path = create_keep_visions_path(
        moment_mstr_dir,
        healer_name,
        moment_label,
        keep_rope,
        knot,
    )
    save_belief_file(keep_visions_path, x_filename, x_belief)
