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
from src.a01_term_logic.term import EventInt, LabelTerm, OwnerName, RopeTerm
from src.a02_finance_logic.bud import BudUnit, TimeLinePoint, get_budunit_from_dict
from src.a06_plan_logic.plan import (
    PlanUnit,
    get_from_json as planunit_get_from_json,
    planunit_shop,
)
from src.a11_bud_cell_logic.cell import CellUnit, cellunit_get_from_dict, cellunit_shop
from src.a12_hub_toolbox.hub_path import (
    CELLNODE_FILENAME,
    create_bank_owners_dir_path,
    create_buds_dir_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_gut_path,
    create_job_path,
    create_planevent_path,
    create_planpoint_path,
)


def save_plan_file(dest_dir: str, filename: str = None, planunit: PlanUnit = None):
    save_file(dest_dir, filename, planunit.get_json())


def open_plan_file(dest_dir: str, filename: str = None) -> PlanUnit:
    if os_path_exists(create_path(dest_dir, filename)):
        return planunit_get_from_json(open_file(dest_dir, filename))


def save_gut_file(bank_mstr_dir: str, planunit: PlanUnit):
    gut_path = create_gut_path(bank_mstr_dir, planunit.bank_label, planunit.owner_name)
    save_plan_file(gut_path, None, planunit)


def open_gut_file(
    bank_mstr_dir: str, bank_label: str, owner_name: OwnerName
) -> PlanUnit:
    gut_path = create_gut_path(bank_mstr_dir, bank_label, owner_name)
    return open_plan_file(gut_path)


def gut_file_exists(bank_mstr_dir: str, bank_label: str, owner_name: OwnerName) -> bool:
    gut_path = create_gut_path(bank_mstr_dir, bank_label, owner_name)
    return os_path_exists(gut_path)


def job_file_exists(bank_mstr_dir: str, bank_label: str, owner_name: OwnerName) -> bool:
    job_path = create_job_path(bank_mstr_dir, bank_label, owner_name)
    return os_path_exists(job_path)


def save_job_file(bank_mstr_dir: str, planunit: PlanUnit):
    job_path = create_job_path(bank_mstr_dir, planunit.bank_label, planunit.owner_name)
    save_plan_file(job_path, None, planunit)


def open_job_file(
    bank_mstr_dir: str, bank_label: str, owner_name: OwnerName
) -> PlanUnit:
    job_path = create_job_path(bank_mstr_dir, bank_label, owner_name)
    return open_plan_file(job_path)


def get_planevent_obj(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName, event_int: int
) -> PlanUnit:
    planevent_json_path = create_planevent_path(
        bank_mstr_dir, bank_label, owner_name, event_int
    )
    return open_plan_file(planevent_json_path)


def collect_owner_event_dir_sets(
    bank_mstr_dir: str, bank_label: LabelTerm
) -> dict[OwnerName, set[EventInt]]:
    x_dict = {}
    owners_dir = create_bank_owners_dir_path(bank_mstr_dir, bank_label)
    set_dir(owners_dir)
    for owner_name in os_listdir(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        events_dir = create_path(owner_dir, "events")
        set_dir(events_dir)
        owner_events_dirs = {
            int(event_int_folder)
            for event_int_folder in os_listdir(events_dir)
            if os_path_isdir(create_path(events_dir, event_int_folder))
        }
        x_dict[owner_name] = owner_events_dirs
    return x_dict


def get_owners_downhill_event_ints(
    owner_events_sets: dict[OwnerName, set[EventInt]],
    downhill_owners: set[OwnerName] = None,
    ref_event_int: EventInt = None,
) -> dict[OwnerName, EventInt]:
    x_dict = {}
    if downhill_owners:
        for owner_name in downhill_owners:
            if event_set := owner_events_sets.get(owner_name):
                _add_downhill_event_int(x_dict, event_set, ref_event_int, owner_name)
    else:
        for owner_name, event_set in owner_events_sets.items():
            _add_downhill_event_int(x_dict, event_set, ref_event_int, owner_name)
    return x_dict


def _add_downhill_event_int(
    x_dict: dict[OwnerName, EventInt],
    event_set: set[EventInt],
    ref_event_int: EventInt,
    downhill_owner: OwnerName,
):
    if event_set:
        if ref_event_int:
            if downhill_event_ints := {ei for ei in event_set if ei <= ref_event_int}:
                x_dict[downhill_owner] = max(downhill_event_ints)
        else:
            x_dict[downhill_owner] = max(event_set)


def save_arbitrary_planevent(
    bank_mstr_dir: str,
    bank_label: str,
    owner_name: str,
    event_int: int,
    accts: list[list] = None,
    facts: list[tuple[RopeTerm, RopeTerm, float, float]] = None,
) -> str:
    accts = get_empty_list_if_None(accts)
    facts = get_empty_list_if_None(facts)
    x_planunit = planunit_shop(owner_name, bank_label)
    for acct_list in accts:
        try:
            credit_score = acct_list[1]
        except Exception:
            credit_score = None
        x_planunit.add_acctunit(acct_list[0], credit_score)
    for fact_tup in facts:
        x_rcontext = fact_tup[0]
        x_fstate = fact_tup[1]
        x_fopen = fact_tup[2]
        x_fnigh = fact_tup[3]
        x_planunit.add_fact(x_rcontext, x_fstate, x_fopen, x_fnigh, True)
    x_planevent_path = create_planevent_path(
        bank_mstr_dir, bank_label, owner_name, event_int
    )
    save_file(x_planevent_path, None, x_planunit.get_json())
    return x_planevent_path


def cellunit_add_json_file(
    bank_mstr_dir: str,
    bank_label: str,
    time_owner_name: str,
    bud_time: int,
    event_int: int,
    bud_ancestors: list[OwnerName] = None,
    quota: int = None,
    celldepth: int = None,
    penny: int = None,
):
    cell_dir = create_cell_dir_path(
        bank_mstr_dir, bank_label, time_owner_name, bud_time, bud_ancestors
    )
    x_cell = cellunit_shop(
        time_owner_name, bud_ancestors, event_int, celldepth, penny, quota
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
    bank_mstr_dir: str,
    bank_label: str,
    owner_name: OwnerName,
    x_bud: BudUnit = None,
):
    x_bud.calc_magnitude()
    bud_json_path = create_budunit_json_path(
        bank_mstr_dir, bank_label, owner_name, x_bud.bud_time
    )
    save_json(bud_json_path, None, x_bud.get_dict(), replace=True)


def bud_file_exists(
    bank_mstr_dir: str,
    bank_label: str,
    owner_name: OwnerName,
    x_bud_time: TimeLinePoint = None,
) -> bool:
    bud_json_path = create_budunit_json_path(
        bank_mstr_dir, bank_label, owner_name, x_bud_time
    )
    return os_path_exists(bud_json_path)


def open_bud_file(
    bank_mstr_dir: str,
    bank_label: str,
    owner_name: OwnerName,
    x_bud_time: TimeLinePoint = None,
) -> BudUnit:
    bud_json_path = create_budunit_json_path(
        bank_mstr_dir, bank_label, owner_name, x_bud_time
    )
    if bud_file_exists(bank_mstr_dir, bank_label, owner_name, x_bud_time):
        return get_budunit_from_dict(open_json(bud_json_path))


class _save_valid_planpoint_Exception(Exception):
    pass


def save_planpoint_file(
    bank_mstr_dir: str,
    x_planpoint: PlanUnit,
    x_bud_time: TimeLinePoint = None,
):
    x_planpoint.settle_plan()
    if x_planpoint._rational is False:
        raise _save_valid_planpoint_Exception(
            "PlanPoint could not be saved PlanUnit._rational is False"
        )
    planpoint_json_path = create_planpoint_path(
        bank_mstr_dir, x_planpoint.bank_label, x_planpoint.owner_name, x_bud_time
    )
    save_plan_file(planpoint_json_path, None, x_planpoint)


def planpoint_file_exists(
    bank_mstr_dir: str,
    bank_label: str,
    owner_name: OwnerName,
    x_bud_time: TimeLinePoint = None,
) -> bool:
    planpoint_json_path = create_planpoint_path(
        bank_mstr_dir, bank_label, owner_name, x_bud_time
    )
    return os_path_exists(planpoint_json_path)


def open_planpoint_file(
    bank_mstr_dir: str,
    bank_label: str,
    owner_name: OwnerName,
    x_bud_time: TimeLinePoint = None,
) -> bool:
    planpoint_json_path = create_planpoint_path(
        bank_mstr_dir, bank_label, owner_name, x_bud_time
    )
    # if self.planpoint_file_exists(x_bud_time):
    return open_plan_file(planpoint_json_path)


def get_timepoint_dirs(
    bank_mstr_dir: str, bank_label: str, owner_name: OwnerName
) -> list[TimeLinePoint]:
    buds_dir = create_buds_dir_path(bank_mstr_dir, bank_label, owner_name)
    x_dict = get_dir_file_strs(buds_dir, include_dirs=True, include_files=False)
    return [int(x_timepoint) for x_timepoint in sorted(list(x_dict.keys()))]
