from os import listdir as os_listdir
from os.path import exists as os_path_exists, isdir as os_path_isdir
from src.a00_data_toolbox.dict_toolbox import get_empty_list_if_None
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    get_dir_file_strs,
    open_file,
    open_json,
    save_file,
    save_json,
    set_dir,
)
from src.a01_term_logic.term import BeliefName, EventInt, LabelTerm, RopeTerm
from src.a06_belief_logic.belief_main import (
    BeliefUnit,
    beliefunit_shop,
    get_from_json as beliefunit_get_from_json,
)
from src.a11_bud_logic.bud import BudUnit, TimeLinePoint, get_budunit_from_dict
from src.a11_bud_logic.cell import CellUnit, cellunit_get_from_dict, cellunit_shop
from src.a12_hub_toolbox.a12_path import (
    CELLNODE_FILENAME,
    create_beliefevent_path,
    create_beliefpoint_path,
    create_buds_dir_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_gut_path,
    create_job_path,
    create_moment_beliefs_dir_path,
)


def save_belief_file(
    dest_dir: str, filename: str = None, beliefunit: BeliefUnit = None
):
    save_file(dest_dir, filename, beliefunit.get_json())


def open_belief_file(dest_dir: str, filename: str = None) -> BeliefUnit:
    if os_path_exists(create_path(dest_dir, filename)):
        return beliefunit_get_from_json(open_file(dest_dir, filename))


def save_gut_file(moment_mstr_dir: str, beliefunit: BeliefUnit):
    gut_path = create_gut_path(
        moment_mstr_dir, beliefunit.moment_label, beliefunit.belief_name
    )
    save_belief_file(gut_path, None, beliefunit)


def open_gut_file(
    moment_mstr_dir: str, moment_label: str, belief_name: BeliefName
) -> BeliefUnit:
    gut_path = create_gut_path(moment_mstr_dir, moment_label, belief_name)
    return open_belief_file(gut_path)


def gut_file_exists(
    moment_mstr_dir: str, moment_label: str, belief_name: BeliefName
) -> bool:
    gut_path = create_gut_path(moment_mstr_dir, moment_label, belief_name)
    return os_path_exists(gut_path)


def job_file_exists(
    moment_mstr_dir: str, moment_label: str, belief_name: BeliefName
) -> bool:
    job_path = create_job_path(moment_mstr_dir, moment_label, belief_name)
    return os_path_exists(job_path)


def save_job_file(moment_mstr_dir: str, beliefunit: BeliefUnit):
    job_path = create_job_path(
        moment_mstr_dir, beliefunit.moment_label, beliefunit.belief_name
    )
    save_belief_file(job_path, None, beliefunit)


def open_job_file(
    moment_mstr_dir: str, moment_label: str, belief_name: BeliefName
) -> BeliefUnit:
    job_path = create_job_path(moment_mstr_dir, moment_label, belief_name)
    return open_belief_file(job_path)


def get_beliefevent_obj(
    moment_mstr_dir: str,
    moment_label: LabelTerm,
    belief_name: BeliefName,
    event_int: int,
) -> BeliefUnit:
    beliefevent_json_path = create_beliefevent_path(
        moment_mstr_dir, moment_label, belief_name, event_int
    )
    return open_belief_file(beliefevent_json_path)


def collect_belief_event_dir_sets(
    moment_mstr_dir: str, moment_label: LabelTerm
) -> dict[BeliefName, set[EventInt]]:
    x_dict = {}
    beliefs_dir = create_moment_beliefs_dir_path(moment_mstr_dir, moment_label)
    set_dir(beliefs_dir)
    for belief_name in os_listdir(beliefs_dir):
        belief_dir = create_path(beliefs_dir, belief_name)
        events_dir = create_path(belief_dir, "events")
        set_dir(events_dir)
        belief_events_dirs = {
            int(event_int_folder)
            for event_int_folder in os_listdir(events_dir)
            if os_path_isdir(create_path(events_dir, event_int_folder))
        }
        x_dict[belief_name] = belief_events_dirs
    return x_dict


def get_beliefs_downhill_event_ints(
    belief_events_sets: dict[BeliefName, set[EventInt]],
    downhill_beliefs: set[BeliefName] = None,
    ref_event_int: EventInt = None,
) -> dict[BeliefName, EventInt]:
    x_dict = {}
    if downhill_beliefs:
        for belief_name in downhill_beliefs:
            if event_set := belief_events_sets.get(belief_name):
                _add_downhill_event_int(x_dict, event_set, ref_event_int, belief_name)
    else:
        for belief_name, event_set in belief_events_sets.items():
            _add_downhill_event_int(x_dict, event_set, ref_event_int, belief_name)
    return x_dict


def _add_downhill_event_int(
    x_dict: dict[BeliefName, EventInt],
    event_set: set[EventInt],
    ref_event_int: EventInt,
    downhill_belief: BeliefName,
):
    if event_set:
        if ref_event_int:
            if downhill_event_ints := {ei for ei in event_set if ei <= ref_event_int}:
                x_dict[downhill_belief] = max(downhill_event_ints)
        else:
            x_dict[downhill_belief] = max(event_set)


def save_arbitrary_beliefevent(
    moment_mstr_dir: str,
    moment_label: str,
    belief_name: str,
    event_int: int,
    partners: list[list] = None,
    facts: list[tuple[RopeTerm, RopeTerm, float, float]] = None,
) -> str:
    partners = get_empty_list_if_None(partners)
    facts = get_empty_list_if_None(facts)
    x_beliefunit = beliefunit_shop(belief_name, moment_label)
    for partner_list in partners:
        try:
            partner_cred_points = partner_list[1]
        except Exception:
            partner_cred_points = None
        x_beliefunit.add_partnerunit(partner_list[0], partner_cred_points)
    for fact_tup in facts:
        x_reason_context = fact_tup[0]
        x_fact_state = fact_tup[1]
        x_fact_lower = fact_tup[2]
        x_fact_upper = fact_tup[3]
        x_beliefunit.add_fact(
            x_reason_context, x_fact_state, x_fact_lower, x_fact_upper, True
        )
    x_beliefevent_path = create_beliefevent_path(
        moment_mstr_dir, moment_label, belief_name, event_int
    )
    save_file(x_beliefevent_path, None, x_beliefunit.get_json())
    return x_beliefevent_path


def cellunit_add_json_file(
    moment_mstr_dir: str,
    moment_label: str,
    time_belief_name: str,
    bud_time: int,
    event_int: int,
    bud_ancestors: list[BeliefName] = None,
    quota: int = None,
    celldepth: int = None,
    penny: int = None,
):
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_label, time_belief_name, bud_time, bud_ancestors
    )
    x_cell = cellunit_shop(
        time_belief_name, bud_ancestors, event_int, celldepth, penny, quota
    )
    cellunit_save_to_dir(cell_dir, x_cell)


def cellunit_save_to_dir(dirpath: str, x_cell: CellUnit):
    save_json(dirpath, CELLNODE_FILENAME, x_cell.to_dict())


def cellunit_get_from_dir(dirpath: str) -> CellUnit:
    cell_json_path = create_path(dirpath, CELLNODE_FILENAME)
    if os_path_exists(cell_json_path):
        return cellunit_get_from_dict(open_json(cell_json_path))


def create_cell_partner_mandate_ledger_json(dirpath: str):
    if cell := cellunit_get_from_dir(dirpath):
        cell.calc_partner_mandate_ledger()
        save_json(
            dirpath, "cell_partner_mandate_ledger.json", cell._partner_mandate_ledger
        )


def save_bud_file(
    moment_mstr_dir: str,
    moment_label: str,
    belief_name: BeliefName,
    x_bud: BudUnit = None,
):
    x_bud.calc_magnitude()
    bud_json_path = create_budunit_json_path(
        moment_mstr_dir, moment_label, belief_name, x_bud.bud_time
    )
    save_json(bud_json_path, None, x_bud.to_dict(), replace=True)


def bud_file_exists(
    moment_mstr_dir: str,
    moment_label: str,
    belief_name: BeliefName,
    x_bud_time: TimeLinePoint = None,
) -> bool:
    bud_json_path = create_budunit_json_path(
        moment_mstr_dir, moment_label, belief_name, x_bud_time
    )
    return os_path_exists(bud_json_path)


def open_bud_file(
    moment_mstr_dir: str,
    moment_label: str,
    belief_name: BeliefName,
    x_bud_time: TimeLinePoint = None,
) -> BudUnit:
    bud_json_path = create_budunit_json_path(
        moment_mstr_dir, moment_label, belief_name, x_bud_time
    )
    if bud_file_exists(moment_mstr_dir, moment_label, belief_name, x_bud_time):
        return get_budunit_from_dict(open_json(bud_json_path))


class _save_valid_beliefpoint_Exception(Exception):
    pass


def save_beliefpoint_file(
    moment_mstr_dir: str,
    x_beliefpoint: BeliefUnit,
    x_bud_time: TimeLinePoint = None,
):
    x_beliefpoint.cash_out()
    if x_beliefpoint._rational is False:
        raise _save_valid_beliefpoint_Exception(
            "BeliefPoint could not be saved BeliefUnit._rational is False"
        )
    beliefpoint_json_path = create_beliefpoint_path(
        moment_mstr_dir,
        x_beliefpoint.moment_label,
        x_beliefpoint.belief_name,
        x_bud_time,
    )
    save_belief_file(beliefpoint_json_path, None, x_beliefpoint)


def beliefpoint_file_exists(
    moment_mstr_dir: str,
    moment_label: str,
    belief_name: BeliefName,
    x_bud_time: TimeLinePoint = None,
) -> bool:
    beliefpoint_json_path = create_beliefpoint_path(
        moment_mstr_dir, moment_label, belief_name, x_bud_time
    )
    return os_path_exists(beliefpoint_json_path)


def open_beliefpoint_file(
    moment_mstr_dir: str,
    moment_label: str,
    belief_name: BeliefName,
    x_bud_time: TimeLinePoint = None,
) -> bool:
    beliefpoint_json_path = create_beliefpoint_path(
        moment_mstr_dir, moment_label, belief_name, x_bud_time
    )
    # if self.beliefpoint_file_exists(x_bud_time):
    return open_belief_file(beliefpoint_json_path)


def get_timepoint_dirs(
    moment_mstr_dir: str, moment_label: str, belief_name: BeliefName
) -> list[TimeLinePoint]:
    buds_dir = create_buds_dir_path(moment_mstr_dir, moment_label, belief_name)
    x_dict = get_dir_file_strs(buds_dir, include_dirs=True, include_files=False)
    return [int(x_timepoint) for x_timepoint in sorted(list(x_dict.keys()))]
