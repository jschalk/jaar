from src.f00_instrument.file import create_path, save_file, open_file
from src.f01_road.deal import TimeLinePoint
from src.f01_road.finance import RespectNum
from src.f01_road.road import AcctName, OwnerName, TitleUnit
from src.f02_bud.bud import BudUnit, get_from_json as budunit_get_from_json
from src.f02_bud.bud_tool import get_credit_ledger
from src.f05_listen.hub_path import (
    create_budpoint_json_path,
    create_events_owner_json_path,
)
from os.path import exists as os_path_exists


def save_bud_file(dest_dir: str, filename: str = None, budunit: BudUnit = None):
    save_file(dest_dir, filename, budunit.get_json())


def open_bud_file(dest_dir: str, filename: str = None) -> BudUnit:
    if os_path_exists(create_path(dest_dir, filename)):
        return budunit_get_from_json(open_file(dest_dir, filename))


def get_timepoint_credit_ledger(
    fisc_mstr_dir: str, fisc_title: str, owner_name: OwnerName, timepoint: TimeLinePoint
) -> dict[AcctName, RespectNum]:
    timepoint_json_path = create_budpoint_json_path(
        fisc_mstr_dir, fisc_title, owner_name, timepoint
    )
    budpoint = open_bud_file(timepoint_json_path)
    return get_credit_ledger(budpoint) if budpoint else {}


def get_events_owner_credit_ledger(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, event_int: int
) -> dict[AcctName, RespectNum]:
    timepoint_json_path = create_events_owner_json_path(
        fisc_mstr_dir, fisc_title, owner_name, event_int
    )
    budpoint = open_bud_file(timepoint_json_path)
    return get_credit_ledger(budpoint) if budpoint else {}
