from src.a00_data_toolbox.file_toolbox import (
    create_directory_path,
    create_path,
    get_json_filename,
)
from src.a01_term_logic.rope import get_all_rope_labels, rebuild_rope
from src.a01_term_logic.term import BeliefLabel, BelieverName, LabelTerm

BELIEF_FILENAME = "belief.json"
BUDUNIT_FILENAME = "budunit.json"
CELLNODE_FILENAME = "cell.json"
CELL_MANDATE_FILENAME = "cell_partner_mandate_ledger.json"
BELIEVERPOINT_FILENAME = "believerpoint.json"
BELIEVEREVENT_FILENAME = "believer.json"
EVENT_ALL_PACK_FILENAME = "all_pack.json"
EVENT_EXPRESSED_PACK_FILENAME = "expressed_pack.json"


def treasury_filename() -> str:
    return "treasury.db"


def create_belief_dir_path(belief_mstr_dir: str, belief_label: LabelTerm) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label"""
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    return create_path(beliefs_dir, belief_label)


def create_belief_json_path(belief_mstr_dir: str, belief_label: LabelTerm) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\belief.json"""
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_path = create_path(beliefs_dir, belief_label)
    return create_path(belief_path, "belief.json")


def create_belief_believers_dir_path(
    belief_mstr_dir: str, belief_label: LabelTerm
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers"""
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    return create_path(belief_dir, "believers")


def create_believer_dir_path(
    belief_mstr_dir: str, belief_label: LabelTerm, believer_name: BelieverName
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name"""

    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    return create_path(believers_dir, believer_name)


def create_keeps_dir_path(
    belief_mstr_dir: str, belief_label: LabelTerm, believer_name: BelieverName
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\keeps"""
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    believer_dir = create_path(believers_dir, believer_name)
    return create_path(believer_dir, "keeps")


class _keep_ropeMissingException(Exception):
    pass


def create_keep_rope_path(
    belief_mstr_dir: str,
    believer_name: BelieverName,
    belief_label: BeliefLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\keeps\\planroot\\level1_label"""
    if keep_rope is None:
        raise _keep_ropeMissingException(
            f"'{believer_name}' cannot save to keep_path because it does not have keep_rope."
        )

    keep_root = "planroot"
    keep_rope = rebuild_rope(keep_rope, belief_label, keep_root)
    x_list = get_all_rope_labels(keep_rope, knot)
    keep_sub_path = create_directory_path(x_list=[*x_list])
    keeps_dir = create_keeps_dir_path(belief_mstr_dir, belief_label, believer_name)
    return create_path(keeps_dir, keep_sub_path)


def create_keep_dutys_path(
    belief_mstr_dir: str,
    believer_name: BelieverName,
    belief_label: BeliefLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\keeps\\level1\\dutys"""
    x_keep_path = create_keep_rope_path(
        belief_mstr_dir, believer_name, belief_label, keep_rope, knot
    )
    return create_path(x_keep_path, "dutys")


def create_keep_duty_path(
    belief_mstr_dir: str,
    believer_name: BelieverName,
    belief_label: BeliefLabel,
    keep_rope: LabelTerm,
    knot: str,
    duty_believer: BelieverName,
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\keeps\\level1\\dutys\\duty_believer.json"""
    x_dutys_path = create_keep_dutys_path(
        belief_mstr_dir, believer_name, belief_label, keep_rope, knot
    )
    return create_path(x_dutys_path, get_json_filename(duty_believer))


def create_keep_visions_path(
    belief_mstr_dir: str,
    believer_name: BelieverName,
    belief_label: BeliefLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\keeps\\level1\\visions"""
    x_keep_path = create_keep_rope_path(
        belief_mstr_dir, believer_name, belief_label, keep_rope, knot
    )
    return create_path(x_keep_path, "visions")


def create_keep_grades_path(
    belief_mstr_dir: str,
    believer_name: BelieverName,
    belief_label: BeliefLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\keeps\\level1\\grades"""
    x_keep_path = create_keep_rope_path(
        belief_mstr_dir, believer_name, belief_label, keep_rope, knot
    )
    return create_path(x_keep_path, "grades")


def create_treasury_db_path(
    belief_mstr_dir: str,
    believer_name: BelieverName,
    belief_label: BeliefLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    "Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\keeps\\level1\\treasury.db"
    keep_path = create_keep_rope_path(
        belief_mstr_dir=belief_mstr_dir,
        believer_name=believer_name,
        belief_label=belief_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    return create_path(keep_path, treasury_filename())


def create_atoms_dir_path(
    belief_mstr_dir: str, belief_label: LabelTerm, believer_name: BelieverName
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\atoms"""
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    believer_dir = create_path(believers_dir, believer_name)
    return create_path(believer_dir, "atoms")


def create_packs_dir_path(
    belief_mstr_dir: str, belief_label: LabelTerm, believer_name: BelieverName
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\packs"""
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    believer_dir = create_path(believers_dir, believer_name)
    return create_path(believer_dir, "packs")


def create_buds_dir_path(
    belief_mstr_dir: str, belief_label: LabelTerm, believer_name: BelieverName
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\buds"""
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    believer_dir = create_path(believers_dir, believer_name)
    return create_path(believer_dir, "buds")


def create_bud_dir_path(
    belief_mstr_dir: str,
    belief_label: LabelTerm,
    believer_name: BelieverName,
    bud_time: int,
):
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\buds\n\\bud_time"""
    timeline_dir = create_buds_dir_path(belief_mstr_dir, belief_label, believer_name)
    return create_path(timeline_dir, bud_time)


def create_budunit_json_path(
    belief_mstr_dir: str,
    belief_label: LabelTerm,
    believer_name: BelieverName,
    bud_time: int,
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\buds\n\\bud_time\\budunit.json"""
    timepoint_dir = create_bud_dir_path(
        belief_mstr_dir, belief_label, believer_name, bud_time
    )
    return create_path(timepoint_dir, "budunit.json")


def create_believerpoint_path(
    belief_mstr_dir: str,
    belief_label: LabelTerm,
    believer_name: BelieverName,
    bud_time: int,
) -> str:
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\buds\n\\bud_time\\believerpoint.json"""
    timepoint_dir = create_bud_dir_path(
        belief_mstr_dir, belief_label, believer_name, bud_time
    )
    return create_path(timepoint_dir, "believerpoint.json")


def create_cell_dir_path(
    belief_mstr_dir: str,
    belief_label: LabelTerm,
    believer_name: BelieverName,
    bud_time: int,
    bud_ancestors: list[BelieverName],
):
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\buds\n\\bud_time\\ledger_believer1\\ledger_believer2\\ledger_believer3"""
    bud_celldepth_dir = create_bud_dir_path(
        belief_mstr_dir, belief_label, believer_name, bud_time
    )
    if bud_ancestors is None:
        bud_ancestors = []
    for ledger_believer in bud_ancestors:
        bud_celldepth_dir = create_path(bud_celldepth_dir, ledger_believer)
    return bud_celldepth_dir


def create_cell_json_path(
    belief_mstr_dir: str,
    belief_label: LabelTerm,
    believer_name: BelieverName,
    bud_time: int,
    bud_ancestors: list[BelieverName] = None,
):
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\buds\n\\bud_time\\ledger_believer1\\ledger_believer2\\ledger_believer3\\cell.json"""
    cell_dir = create_cell_dir_path(
        belief_mstr_dir, belief_label, believer_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell.json")


def create_cell_partner_mandate_ledger_path(
    belief_mstr_dir: str,
    belief_label: LabelTerm,
    believer_name: BelieverName,
    bud_time: int,
    bud_ancestors: list[BelieverName] = None,
):
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\buds\n\\bud_time\\ledger_believer1\\ledger_believer2\\ledger_believer3\\cell_partner_mandate_ledger.json"""
    cell_dir = create_cell_dir_path(
        belief_mstr_dir, belief_label, believer_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell_partner_mandate_ledger.json")


def create_believer_event_dir_path(
    belief_mstr_dir: str,
    belief_label: LabelTerm,
    believer_name: BelieverName,
    event_int: int,
):
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\events\\event_int"""
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    belief_believer_dir = create_path(believers_dir, believer_name)
    belief_events_dir = create_path(belief_believer_dir, "events")
    return create_path(belief_events_dir, event_int)


def create_believerevent_path(
    belief_mstr_dir: str,
    belief_label: LabelTerm,
    believer_name: BelieverName,
    event_int: int,
):
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\events\\event_int\\believer.json"""
    believer_event_dir_path = create_believer_event_dir_path(
        belief_mstr_dir, belief_label, believer_name, event_int
    )
    believer_filename = "believer.json"
    return create_path(believer_event_dir_path, believer_filename)


def create_event_all_pack_path(
    belief_mstr_dir: str,
    belief_label: LabelTerm,
    believer_name: BelieverName,
    event_int: int,
):
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\events\\event_int\\all_pack.json"""
    believer_event_dir_path = create_believer_event_dir_path(
        belief_mstr_dir, belief_label, believer_name, event_int
    )
    all_pack_filename = "all_pack.json"
    return create_path(believer_event_dir_path, all_pack_filename)


def create_event_expressed_pack_path(
    belief_mstr_dir: str,
    belief_label: LabelTerm,
    believer_name: BelieverName,
    event_int: int,
):
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\events\\event_int\\expressed_pack.json"""
    believer_event_dir_path = create_believer_event_dir_path(
        belief_mstr_dir, belief_label, believer_name, event_int
    )
    expressed_pack_filename = "expressed_pack.json"
    return create_path(believer_event_dir_path, expressed_pack_filename)


def create_gut_path(
    belief_mstr_dir: str, belief_label: LabelTerm, believer_name: BelieverName
):
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\gut\\believer_name.json"""
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    believer_dir = create_path(believers_dir, believer_name)
    gut_dir = create_path(believer_dir, "gut")
    return create_path(gut_dir, f"{believer_name}.json")


def create_job_path(
    belief_mstr_dir: str, belief_label: LabelTerm, believer_name: BelieverName
):
    """Returns path: belief_mstr_dir\\beliefs\\belief_label\\believers\\believer_name\\job\\believer_name.json"""
    beliefs_dir = create_path(belief_mstr_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_label)
    believers_dir = create_path(belief_dir, "believers")
    believer_dir = create_path(believers_dir, believer_name)
    job_dir = create_path(believer_dir, "job")
    return create_path(job_dir, f"{believer_name}.json")
