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
from src.a01_term_logic.term import BelieverName, EventInt, LabelTerm, RopeTerm
from src.a06_believer_logic.believer import (
    BelieverUnit,
    believerunit_shop,
    get_from_json as believerunit_get_from_json,
)
from src.a11_bud_logic.bud import BudUnit, TimeLinePoint, get_budunit_from_dict
from src.a11_bud_logic.cell import CellUnit, cellunit_get_from_dict, cellunit_shop
from src.a12_hub_toolbox.hub_path import (
    CELLNODE_FILENAME,
    create_belief_believers_dir_path,
    create_believerevent_path,
    create_believerpoint_path,
    create_buds_dir_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_gut_path,
    create_job_path,
)


def save_believer_file(
    dest_dir: str, filename: str = None, believerunit: BelieverUnit = None
):
    save_file(dest_dir, filename, believerunit.get_json())


def open_believer_file(dest_dir: str, filename: str = None) -> BelieverUnit:
    if os_path_exists(create_path(dest_dir, filename)):
        return believerunit_get_from_json(open_file(dest_dir, filename))


def save_gut_file(belief_mstr_dir: str, believerunit: BelieverUnit):
    gut_path = create_gut_path(
        belief_mstr_dir, believerunit.belief_label, believerunit.believer_name
    )
    save_believer_file(gut_path, None, believerunit)


def open_gut_file(
    belief_mstr_dir: str, belief_label: str, believer_name: BelieverName
) -> BelieverUnit:
    gut_path = create_gut_path(belief_mstr_dir, belief_label, believer_name)
    return open_believer_file(gut_path)


def gut_file_exists(
    belief_mstr_dir: str, belief_label: str, believer_name: BelieverName
) -> bool:
    gut_path = create_gut_path(belief_mstr_dir, belief_label, believer_name)
    return os_path_exists(gut_path)


def job_file_exists(
    belief_mstr_dir: str, belief_label: str, believer_name: BelieverName
) -> bool:
    job_path = create_job_path(belief_mstr_dir, belief_label, believer_name)
    return os_path_exists(job_path)


def save_job_file(belief_mstr_dir: str, believerunit: BelieverUnit):
    job_path = create_job_path(
        belief_mstr_dir, believerunit.belief_label, believerunit.believer_name
    )
    save_believer_file(job_path, None, believerunit)


def open_job_file(
    belief_mstr_dir: str, belief_label: str, believer_name: BelieverName
) -> BelieverUnit:
    job_path = create_job_path(belief_mstr_dir, belief_label, believer_name)
    return open_believer_file(job_path)


def get_believerevent_obj(
    belief_mstr_dir: str,
    belief_label: LabelTerm,
    believer_name: BelieverName,
    event_int: int,
) -> BelieverUnit:
    believerevent_json_path = create_believerevent_path(
        belief_mstr_dir, belief_label, believer_name, event_int
    )
    return open_believer_file(believerevent_json_path)


def collect_believer_event_dir_sets(
    belief_mstr_dir: str, belief_label: LabelTerm
) -> dict[BelieverName, set[EventInt]]:
    x_dict = {}
    believers_dir = create_belief_believers_dir_path(belief_mstr_dir, belief_label)
    set_dir(believers_dir)
    for believer_name in os_listdir(believers_dir):
        believer_dir = create_path(believers_dir, believer_name)
        events_dir = create_path(believer_dir, "events")
        set_dir(events_dir)
        believer_events_dirs = {
            int(event_int_folder)
            for event_int_folder in os_listdir(events_dir)
            if os_path_isdir(create_path(events_dir, event_int_folder))
        }
        x_dict[believer_name] = believer_events_dirs
    return x_dict


def get_believers_downhill_event_ints(
    believer_events_sets: dict[BelieverName, set[EventInt]],
    downhill_believers: set[BelieverName] = None,
    ref_event_int: EventInt = None,
) -> dict[BelieverName, EventInt]:
    x_dict = {}
    if downhill_believers:
        for believer_name in downhill_believers:
            if event_set := believer_events_sets.get(believer_name):
                _add_downhill_event_int(x_dict, event_set, ref_event_int, believer_name)
    else:
        for believer_name, event_set in believer_events_sets.items():
            _add_downhill_event_int(x_dict, event_set, ref_event_int, believer_name)
    return x_dict


def _add_downhill_event_int(
    x_dict: dict[BelieverName, EventInt],
    event_set: set[EventInt],
    ref_event_int: EventInt,
    downhill_believer: BelieverName,
):
    if event_set:
        if ref_event_int:
            if downhill_event_ints := {ei for ei in event_set if ei <= ref_event_int}:
                x_dict[downhill_believer] = max(downhill_event_ints)
        else:
            x_dict[downhill_believer] = max(event_set)


def save_arbitrary_believerevent(
    belief_mstr_dir: str,
    belief_label: str,
    believer_name: str,
    event_int: int,
    accts: list[list] = None,
    facts: list[tuple[RopeTerm, RopeTerm, float, float]] = None,
) -> str:
    accts = get_empty_list_if_None(accts)
    facts = get_empty_list_if_None(facts)
    x_believerunit = believerunit_shop(believer_name, belief_label)
    for acct_list in accts:
        try:
            acct_cred_points = acct_list[1]
        except Exception:
            acct_cred_points = None
        x_believerunit.add_acctunit(acct_list[0], acct_cred_points)
    for fact_tup in facts:
        x_rcontext = fact_tup[0]
        x_fstate = fact_tup[1]
        x_fopen = fact_tup[2]
        x_fnigh = fact_tup[3]
        x_believerunit.add_fact(x_rcontext, x_fstate, x_fopen, x_fnigh, True)
    x_believerevent_path = create_believerevent_path(
        belief_mstr_dir, belief_label, believer_name, event_int
    )
    save_file(x_believerevent_path, None, x_believerunit.get_json())
    return x_believerevent_path


def cellunit_add_json_file(
    belief_mstr_dir: str,
    belief_label: str,
    time_believer_name: str,
    bud_time: int,
    event_int: int,
    bud_ancestors: list[BelieverName] = None,
    quota: int = None,
    celldepth: int = None,
    penny: int = None,
):
    cell_dir = create_cell_dir_path(
        belief_mstr_dir, belief_label, time_believer_name, bud_time, bud_ancestors
    )
    x_cell = cellunit_shop(
        time_believer_name, bud_ancestors, event_int, celldepth, penny, quota
    )
    cellunit_save_to_dir(cell_dir, x_cell)


def cellunit_save_to_dir(dirpath: str, x_cell: CellUnit):
    save_json(dirpath, CELLNODE_FILENAME, x_cell.get_dict())


def cellunit_get_from_dir(dirpath: str) -> CellUnit:
    cell_json_path = create_path(dirpath, CELLNODE_FILENAME)
    if os_path_exists(cell_json_path):
        return cellunit_get_from_dict(open_json(cell_json_path))


def create_cell_acct_mandate_ledger_json(dirpath: str):
    if cell := cellunit_get_from_dir(dirpath):
        cell.calc_acct_mandate_ledger()
        save_json(dirpath, "cell_acct_mandate_ledger.json", cell._acct_mandate_ledger)


def save_bud_file(
    belief_mstr_dir: str,
    belief_label: str,
    believer_name: BelieverName,
    x_bud: BudUnit = None,
):
    x_bud.calc_magnitude()
    bud_json_path = create_budunit_json_path(
        belief_mstr_dir, belief_label, believer_name, x_bud.bud_time
    )
    save_json(bud_json_path, None, x_bud.get_dict(), replace=True)


def bud_file_exists(
    belief_mstr_dir: str,
    belief_label: str,
    believer_name: BelieverName,
    x_bud_time: TimeLinePoint = None,
) -> bool:
    bud_json_path = create_budunit_json_path(
        belief_mstr_dir, belief_label, believer_name, x_bud_time
    )
    return os_path_exists(bud_json_path)


def open_bud_file(
    belief_mstr_dir: str,
    belief_label: str,
    believer_name: BelieverName,
    x_bud_time: TimeLinePoint = None,
) -> BudUnit:
    bud_json_path = create_budunit_json_path(
        belief_mstr_dir, belief_label, believer_name, x_bud_time
    )
    if bud_file_exists(belief_mstr_dir, belief_label, believer_name, x_bud_time):
        return get_budunit_from_dict(open_json(bud_json_path))


class _save_valid_believerpoint_Exception(Exception):
    pass


def save_believerpoint_file(
    belief_mstr_dir: str,
    x_believerpoint: BelieverUnit,
    x_bud_time: TimeLinePoint = None,
):
    x_believerpoint.settle_believer()
    if x_believerpoint._rational is False:
        raise _save_valid_believerpoint_Exception(
            "BelieverPoint could not be saved BelieverUnit._rational is False"
        )
    believerpoint_json_path = create_believerpoint_path(
        belief_mstr_dir,
        x_believerpoint.belief_label,
        x_believerpoint.believer_name,
        x_bud_time,
    )
    save_believer_file(believerpoint_json_path, None, x_believerpoint)


def believerpoint_file_exists(
    belief_mstr_dir: str,
    belief_label: str,
    believer_name: BelieverName,
    x_bud_time: TimeLinePoint = None,
) -> bool:
    believerpoint_json_path = create_believerpoint_path(
        belief_mstr_dir, belief_label, believer_name, x_bud_time
    )
    return os_path_exists(believerpoint_json_path)


def open_believerpoint_file(
    belief_mstr_dir: str,
    belief_label: str,
    believer_name: BelieverName,
    x_bud_time: TimeLinePoint = None,
) -> bool:
    believerpoint_json_path = create_believerpoint_path(
        belief_mstr_dir, belief_label, believer_name, x_bud_time
    )
    # if self.believerpoint_file_exists(x_bud_time):
    return open_believer_file(believerpoint_json_path)


def get_timepoint_dirs(
    belief_mstr_dir: str, belief_label: str, believer_name: BelieverName
) -> list[TimeLinePoint]:
    buds_dir = create_buds_dir_path(belief_mstr_dir, belief_label, believer_name)
    x_dict = get_dir_file_strs(buds_dir, include_dirs=True, include_files=False)
    return [int(x_timepoint) for x_timepoint in sorted(list(x_dict.keys()))]
