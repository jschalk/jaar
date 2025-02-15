from src.f00_instrument.file import create_path, save_file, open_file, set_dir
from src.f01_road.deal import TimeLinePoint
from src.f01_road.finance import RespectNum
from src.f01_road.road import AcctName, OwnerName, TitleUnit
from src.f02_bud.bud import BudUnit, get_from_json as budunit_get_from_json
from src.f02_bud.bud_tool import get_credit_ledger
from src.f05_listen.hub_path import (
    create_budpoint_path,
    create_event_bud_path,
    create_owners_dir_path,
)
from os import listdir as os_listdir
from os.path import (
    exists as os_path_exists,
    join as os_path_join,
    isdir as os_path_isdir,
)


def save_bud_file(dest_dir: str, filename: str = None, budunit: BudUnit = None):
    save_file(dest_dir, filename, budunit.get_json())


def open_bud_file(dest_dir: str, filename: str = None) -> BudUnit:
    if os_path_exists(create_path(dest_dir, filename)):
        return budunit_get_from_json(open_file(dest_dir, filename))


def get_timepoint_credit_ledger(
    fisc_mstr_dir: str, fisc_title: str, owner_name: OwnerName, timepoint: TimeLinePoint
) -> dict[AcctName, RespectNum]:
    timepoint_json_path = create_budpoint_path(
        fisc_mstr_dir, fisc_title, owner_name, timepoint
    )
    budpoint = open_bud_file(timepoint_json_path)
    return get_credit_ledger(budpoint) if budpoint else {}


def get_events_owner_credit_ledger(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, event_int: int
) -> dict[AcctName, RespectNum]:
    timepoint_json_path = create_event_bud_path(
        fisc_mstr_dir, fisc_title, owner_name, event_int
    )
    budpoint = open_bud_file(timepoint_json_path)
    return get_credit_ledger(budpoint) if budpoint else {}


def collect_events_dir_owner_events_sets(
    fisc_mstr_dir: str, fisc_title: str
) -> dict[str, set[int]]:
    x_dict = {}
    owners_dir = create_owners_dir_path(fisc_mstr_dir, fisc_title)
    set_dir(owners_dir)
    for owner_name in os_listdir(owners_dir):
        owner_dir = create_path(owners_dir, owner_name)
        events_dir = create_path(owner_dir, "events")
        set_dir(events_dir)
        if os_path_isdir(events_dir):
            owner_events_dirs = {
                int(event_int_folder)
                for event_int_folder in os_listdir(events_dir)
                if os_path_isdir(create_path(events_dir, event_int_folder))
            }
            x_dict[owner_name] = owner_events_dirs
    return x_dict


def get_owners_downhill_event_ints(
    owner_events_sets: dict[str, set[int]],
    downhill_owners: set[str] = None,
    ref_event_int: int = None,
) -> dict[str, int]:
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
    x_dict: dict[str, int], event_set: set[int], ref_event_int: int, downhill_owner: str
):
    if event_set:
        if ref_event_int:
            if downhill_event_ints := {ei for ei in event_set if ei <= ref_event_int}:
                x_dict[downhill_owner] = max(downhill_event_ints)
        else:
            x_dict[downhill_owner] = max(event_set)
