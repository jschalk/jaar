from src.a00_data_toolbox.file_toolbox import (
    get_dir_file_strs,
    create_path,
    save_file,
    open_file,
    set_dir,
    save_json,
    open_json,
)
from src.a00_data_toolbox.dict_toolbox import get_empty_list_if_None
from src.a01_way_logic.way import OwnerName, LabelTerm, EventInt, WayTerm
from src.a02_finance_logic.deal import (
    DealUnit,
    TimeLinePoint,
    get_dealunit_from_dict,
)
from src.a06_bud_logic.bud import (
    BudUnit,
    get_from_json as budunit_get_from_json,
    budunit_shop,
)
from src.a11_deal_cell_logic.cell import cellunit_shop, CellUnit, cellunit_get_from_dict
from src.a12_hub_tools.hub_path import (
    create_gut_path,
    create_job_path,
    CELLNODE_FILENAME,
    create_budevent_path,
    create_fisc_owners_dir_path,
    create_cell_dir_path,
    create_deals_dir_path,
    create_dealunit_json_path,
    create_budpoint_path,
)
from os import listdir as os_listdir
from os.path import exists as os_path_exists, isdir as os_path_isdir


def save_bud_file(dest_dir: str, filename: str = None, budunit: BudUnit = None):
    save_file(dest_dir, filename, budunit.get_json())


def open_bud_file(dest_dir: str, filename: str = None) -> BudUnit:
    if os_path_exists(create_path(dest_dir, filename)):
        return budunit_get_from_json(open_file(dest_dir, filename))


def save_gut_file(fisc_mstr_dir: str, budunit: BudUnit):
    gut_path = create_gut_path(fisc_mstr_dir, budunit.fisc_label, budunit.owner_name)
    save_bud_file(gut_path, None, budunit)


def open_gut_file(
    fisc_mstr_dir: str, fisc_label: str, owner_name: OwnerName
) -> BudUnit:
    gut_path = create_gut_path(fisc_mstr_dir, fisc_label, owner_name)
    return open_bud_file(gut_path)


def gut_file_exists(fisc_mstr_dir: str, fisc_label: str, owner_name: OwnerName) -> bool:
    gut_path = create_gut_path(fisc_mstr_dir, fisc_label, owner_name)
    return os_path_exists(gut_path)


def job_file_exists(fisc_mstr_dir: str, fisc_label: str, owner_name: OwnerName) -> bool:
    job_path = create_job_path(fisc_mstr_dir, fisc_label, owner_name)
    return os_path_exists(job_path)


def save_job_file(fisc_mstr_dir: str, budunit: BudUnit):
    job_path = create_job_path(fisc_mstr_dir, budunit.fisc_label, budunit.owner_name)
    save_bud_file(job_path, None, budunit)


def open_job_file(
    fisc_mstr_dir: str, fisc_label: str, owner_name: OwnerName
) -> BudUnit:
    job_path = create_job_path(fisc_mstr_dir, fisc_label, owner_name)
    return open_bud_file(job_path)


def get_budevent_obj(
    fisc_mstr_dir: str, fisc_label: LabelTerm, owner_name: OwnerName, event_int: int
) -> BudUnit:
    budevent_json_path = create_budevent_path(
        fisc_mstr_dir, fisc_label, owner_name, event_int
    )
    return open_bud_file(budevent_json_path)


def collect_owner_event_dir_sets(
    fisc_mstr_dir: str, fisc_label: LabelTerm
) -> dict[OwnerName, set[EventInt]]:
    x_dict = {}
    owners_dir = create_fisc_owners_dir_path(fisc_mstr_dir, fisc_label)
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


def save_arbitrary_budevent(
    fisc_mstr_dir: str,
    fisc_label: str,
    owner_name: str,
    event_int: int,
    accts: list[list] = None,
    facts: list[tuple[WayTerm, WayTerm, float, float]] = None,
) -> str:
    accts = get_empty_list_if_None(accts)
    facts = get_empty_list_if_None(facts)
    x_budunit = budunit_shop(owner_name, fisc_label)
    for acct_list in accts:
        try:
            credit_belief = acct_list[1]
        except Exception:
            credit_belief = None
        x_budunit.add_acctunit(acct_list[0], credit_belief)
    for fact_tup in facts:
        x_rcontext = fact_tup[0]
        x_fstate = fact_tup[1]
        x_fopen = fact_tup[2]
        x_fnigh = fact_tup[3]
        x_budunit.add_fact(x_rcontext, x_fstate, x_fopen, x_fnigh, True)
    x_budevent_path = create_budevent_path(
        fisc_mstr_dir, fisc_label, owner_name, event_int
    )
    save_file(x_budevent_path, None, x_budunit.get_json())
    return x_budevent_path


def cellunit_add_json_file(
    fisc_mstr_dir: str,
    fisc_label: str,
    time_owner_name: str,
    deal_time: int,
    event_int: int,
    deal_ancestors: list[OwnerName] = None,
    quota: int = None,
    celldepth: int = None,
    penny: int = None,
):
    cell_dir = create_cell_dir_path(
        fisc_mstr_dir, fisc_label, time_owner_name, deal_time, deal_ancestors
    )
    x_cell = cellunit_shop(
        time_owner_name, deal_ancestors, event_int, celldepth, penny, quota
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


def save_deal_file(
    fisc_mstr_dir: str, fisc_label: str, owner_name: OwnerName, x_deal: DealUnit = None
):
    x_deal.calc_magnitude()
    deal_json_path = create_dealunit_json_path(
        fisc_mstr_dir, fisc_label, owner_name, x_deal.deal_time
    )
    save_json(deal_json_path, None, x_deal.get_dict(), replace=True)


def deal_file_exists(
    fisc_mstr_dir: str,
    fisc_label: str,
    owner_name: OwnerName,
    x_deal_time: TimeLinePoint = None,
) -> bool:
    deal_json_path = create_dealunit_json_path(
        fisc_mstr_dir, fisc_label, owner_name, x_deal_time
    )
    return os_path_exists(deal_json_path)


def open_deal_file(
    fisc_mstr_dir: str,
    fisc_label: str,
    owner_name: OwnerName,
    x_deal_time: TimeLinePoint = None,
) -> DealUnit:
    deal_json_path = create_dealunit_json_path(
        fisc_mstr_dir, fisc_label, owner_name, x_deal_time
    )
    if deal_file_exists(fisc_mstr_dir, fisc_label, owner_name, x_deal_time):
        return get_dealunit_from_dict(open_json(deal_json_path))


class _save_valid_budpoint_Exception(Exception):
    pass


def save_budpoint_file(
    fisc_mstr_dir: str,
    x_budpoint: BudUnit,
    x_deal_time: TimeLinePoint = None,
):
    x_budpoint.settle_bud()
    if x_budpoint._rational is False:
        raise _save_valid_budpoint_Exception(
            "BudPoint could not be saved BudUnit._rational is False"
        )
    budpoint_json_path = create_budpoint_path(
        fisc_mstr_dir, x_budpoint.fisc_label, x_budpoint.owner_name, x_deal_time
    )
    print(f"{x_budpoint.fisc_label=} {budpoint_json_path=}")
    save_bud_file(budpoint_json_path, None, x_budpoint)


def budpoint_file_exists(
    fisc_mstr_dir: str,
    fisc_label: str,
    owner_name: OwnerName,
    x_deal_time: TimeLinePoint = None,
) -> bool:
    budpoint_json_path = create_budpoint_path(
        fisc_mstr_dir, fisc_label, owner_name, x_deal_time
    )
    return os_path_exists(budpoint_json_path)


def open_budpoint_file(
    fisc_mstr_dir: str,
    fisc_label: str,
    owner_name: OwnerName,
    x_deal_time: TimeLinePoint = None,
) -> bool:
    budpoint_json_path = create_budpoint_path(
        fisc_mstr_dir, fisc_label, owner_name, x_deal_time
    )
    # if self.budpoint_file_exists(x_deal_time):
    return open_bud_file(budpoint_json_path)


def get_timepoint_dirs(
    fisc_mstr_dir: str, fisc_label: str, owner_name: OwnerName
) -> list[TimeLinePoint]:
    deals_dir = create_deals_dir_path(fisc_mstr_dir, fisc_label, owner_name)
    x_dict = get_dir_file_strs(deals_dir, include_dirs=True, include_files=False)
    return [int(x_timepoint) for x_timepoint in sorted(list(x_dict.keys()))]
