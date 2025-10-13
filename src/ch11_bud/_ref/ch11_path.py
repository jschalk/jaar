from src.ch01_py.file_toolbox import create_path
from src.ch11_bud._ref.ch11_semantic_types import BeliefName, MomentLabel

MOMENT_FILENAME = "moment.json"
BUDUNIT_FILENAME = "budunit.json"
CELLNODE_FILENAME = "cell.json"
CELL_MANDATE_FILENAME = "cell_voice_mandate_ledger.json"
BELIEFPOINT_FILENAME = "beliefpoint.json"
BELIEFEVENT_FILENAME = "belief.json"
EVENT_ALL_PACK_FILENAME = "all_pack.json"
EVENT_EXPRESSED_PACK_FILENAME = "expressed_pack.json"


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
    event_num: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\events\\event_num"""
    moments_dir = create_path(moment_mstr_dir, "moments")
    moment_dir = create_path(moments_dir, moment_label)
    beliefs_dir = create_path(moment_dir, "beliefs")
    moment_belief_dir = create_path(beliefs_dir, belief_name)
    moment_events_dir = create_path(moment_belief_dir, "events")
    return create_path(moment_events_dir, event_num)


def create_beliefevent_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    event_num: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\events\\event_num\\belief.json"""
    belief_event_dir_path = create_belief_event_dir_path(
        moment_mstr_dir, moment_label, belief_name, event_num
    )
    belief_filename = "belief.json"
    return create_path(belief_event_dir_path, belief_filename)


def create_event_all_pack_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    event_num: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\events\\event_num\\all_pack.json"""
    belief_event_dir_path = create_belief_event_dir_path(
        moment_mstr_dir, moment_label, belief_name, event_num
    )
    all_pack_filename = "all_pack.json"
    return create_path(belief_event_dir_path, all_pack_filename)


def create_event_expressed_pack_path(
    moment_mstr_dir: str,
    moment_label: MomentLabel,
    belief_name: BeliefName,
    event_num: int,
):
    """Returns path: moment_mstr_dir\\moments\\moment_label\\beliefs\\belief_name\\events\\event_num\\expressed_pack.json"""
    belief_event_dir_path = create_belief_event_dir_path(
        moment_mstr_dir, moment_label, belief_name, event_num
    )
    expressed_pack_filename = "expressed_pack.json"
    return create_path(belief_event_dir_path, expressed_pack_filename)
