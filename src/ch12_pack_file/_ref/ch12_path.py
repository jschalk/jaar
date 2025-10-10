from src.ch01_data_toolbox.file_toolbox import create_path
from src.ch11_bud_logic._ref.ch11_semantic_types import MomentLabel
from src.ch12_pack_file._ref.ch12_semantic_types import BeliefName

MOMENT_FILENAME = "moment.json"
BUDUNIT_FILENAME = "budunit.json"
CELLNODE_FILENAME = "cell.json"
CELL_MANDATE_FILENAME = "cell_voice_mandate_ledger.json"
BELIEFPOINT_FILENAME = "beliefpoint.json"
BELIEFEVENT_FILENAME = "belief.json"
EVENT_ALL_PACK_FILENAME = "all_pack.json"
EVENT_EXPRESSED_PACK_FILENAME = "expressed_pack.json"


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


def create_packs_dir_path(
    moment_mstr_dir: str, moment_label: MomentLabel, belief_name: BeliefName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\packs"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    return create_path(belief_dir, "packs")


def create_buds_dir_path(
    moment_mstr_dir: str, moment_label: MomentLabel, belief_name: BeliefName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    return create_path(belief_dir, "buds")


def create_bud_dir_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time"""
    epoch_dir = create_buds_dir_path(moment_mstr_dir, moment_label, belief_name)
    return create_path(epoch_dir, bud_time)


def create_budunit_json_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time\\budunit.json"""
    timepoint_dir = create_bud_dir_path(
        moment_mstr_dir, moment_label, belief_name, bud_time
    )
    return create_path(timepoint_dir, "budunit.json")


def create_beliefpoint_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time\\beliefpoint.json"""
    timepoint_dir = create_bud_dir_path(
        moment_mstr_dir, moment_label, belief_name, bud_time
    )
    return create_path(timepoint_dir, "beliefpoint.json")


def create_cell_dir_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: int,
    bud_ancestors: list[BeliefName],
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time\\ledger_belief1\\ledger_belief2\\ledger_belief3"""
    bud_celldepth_dir = create_bud_dir_path(
        moment_mstr_dir, moment_label, belief_name, bud_time
    )
    if bud_ancestors is None:
        bud_ancestors = []
    for ledger_belief in bud_ancestors:
        bud_celldepth_dir = create_path(bud_celldepth_dir, ledger_belief)
    return bud_celldepth_dir


def create_cell_json_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: int,
    bud_ancestors: list[BeliefName] = None,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time\\ledger_belief1\\ledger_belief2\\ledger_belief3\\cell.json"""
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_label, belief_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell.json")


def create_cell_voice_mandate_ledger_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    bud_time: int,
    bud_ancestors: list[BeliefName] = None,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\buds\n\\bud_time\\ledger_belief1\\ledger_belief2\\ledger_belief3\\cell_voice_mandate_ledger.json"""
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_label, belief_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell_voice_mandate_ledger.json")


def create_belief_event_dir_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    event_int: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\events\\event_int"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    moment_belief_dir = create_path(beliefs_dir, belief_name)
    moment_events_dir = create_path(moment_belief_dir, "events")
    return create_path(moment_events_dir, event_int)


def create_beliefevent_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    event_int: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\events\\event_int\\belief.json"""
    belief_event_dir_path = create_belief_event_dir_path(
        moment_mstr_dir, moment_label, belief_name, event_int
    )
    belief_filename = "belief.json"
    return create_path(belief_event_dir_path, belief_filename)


def create_event_all_pack_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    event_int: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\events\\event_int\\all_pack.json"""
    belief_event_dir_path = create_belief_event_dir_path(
        moment_mstr_dir, moment_label, belief_name, event_int
    )
    all_pack_filename = "all_pack.json"
    return create_path(belief_event_dir_path, all_pack_filename)


def create_event_expressed_pack_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    event_int: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\events\\event_int\\expressed_pack.json"""
    belief_event_dir_path = create_belief_event_dir_path(
        moment_mstr_dir, moment_label, belief_name, event_int
    )
    expressed_pack_filename = "expressed_pack.json"
    return create_path(belief_event_dir_path, expressed_pack_filename)


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
