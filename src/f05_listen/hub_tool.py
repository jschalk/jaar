from src.f00_instrument.file import (
    create_path,
    save_file,
    open_file,
    set_dir,
    save_json,
)
from src.f00_instrument.dict_toolbox import (
    get_empty_list_if_None,
    get_0_if_None,
    get_1_if_None,
)
from src.f01_road.deal import TimeLinePoint
from src.f01_road.finance import RespectNum
from src.f01_road.road import AcctName, OwnerName, TitleUnit, EventInt, RoadUnit
from src.f02_bud.bud import (
    BudUnit,
    get_from_json as budunit_get_from_json,
    budunit_shop,
)
from src.f02_bud.bud_tool import get_credit_ledger, get_bud_root_facts_dict
from src.f05_listen.hub_path import (
    create_budpoint_path,
    create_budevent_path,
    create_owners_dir_path,
    create_deal_node_json_path,
)
from os import listdir as os_listdir
from os.path import exists as os_path_exists, isdir as os_path_isdir


def save_bud_file(dest_dir: str, filename: str = None, budunit: BudUnit = None):
    save_file(dest_dir, filename, budunit.get_json())


def open_bud_file(dest_dir: str, filename: str = None) -> BudUnit:
    if os_path_exists(create_path(dest_dir, filename)):
        return budunit_get_from_json(open_file(dest_dir, filename))


def get_timepoint_credit_ledger(
    fisc_mstr_dir: str,
    fisc_title: TitleUnit,
    owner_name: OwnerName,
    timepoint: TimeLinePoint,
) -> dict[AcctName, RespectNum]:
    timepoint_json_path = create_budpoint_path(
        fisc_mstr_dir, fisc_title, owner_name, timepoint
    )
    budpoint = open_bud_file(timepoint_json_path)
    return get_credit_ledger(budpoint) if budpoint else {}


def get_budevents_credit_ledger(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, event_int: int
) -> dict[AcctName, RespectNum]:
    budevent_json_path = create_budevent_path(
        fisc_mstr_dir, fisc_title, owner_name, event_int
    )
    budevent = open_bud_file(budevent_json_path)
    return get_credit_ledger(budevent) if budevent else {}


def get_budevent_facts(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, event_int: int
) -> dict[RoadUnit, dict[str,]]:
    budevent_json_path = create_budevent_path(
        fisc_mstr_dir, fisc_title, owner_name, event_int
    )
    budevent = open_bud_file(budevent_json_path)
    return get_bud_root_facts_dict(budevent) if budevent else {}


def collect_owner_event_dir_sets(
    fisc_mstr_dir: str, fisc_title: TitleUnit
) -> dict[OwnerName, set[EventInt]]:
    x_dict = {}
    owners_dir = create_owners_dir_path(fisc_mstr_dir, fisc_title)
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
    fisc_title: str,
    owner_name: str,
    event_int: int,
    accts: list[list] = None,
    facts: list[tuple[RoadUnit, RoadUnit, float, float]] = None,
) -> str:
    accts = get_empty_list_if_None(accts)
    facts = get_empty_list_if_None(facts)
    x_budunit = budunit_shop(owner_name, fisc_title)
    for acct_list in accts:
        try:
            credit_belief = acct_list[1]
        except Exception:
            credit_belief = None
        x_budunit.add_acctunit(acct_list[0], credit_belief)
    for fact_tup in facts:
        x_base = fact_tup[0]
        x_pick = fact_tup[1]
        x_fopen = fact_tup[2]
        x_fnigh = fact_tup[3]
        x_budunit.add_fact(x_base, x_pick, x_fopen, x_fnigh, True)
    x_budevent_path = create_budevent_path(
        fisc_mstr_dir, fisc_title, owner_name, event_int
    )
    save_file(x_budevent_path, None, x_budunit.get_json())
    return x_budevent_path


DEAL_NODE_QUOTA_DEFAULT = 1000


def save_deal_node_file(
    fisc_mstr_dir: str,
    fisc_title: str,
    time_owner_name: str,
    time_int: int,
    event_int: int,
    deal_ancestors: list[OwnerName] = None,
    quota: int = None,
    dealdepth: int = None,
    penny: int = None,
):
    deal_ancestors = get_empty_list_if_None(deal_ancestors)
    dealnode_path = create_deal_node_json_path(
        fisc_mstr_dir, fisc_title, time_owner_name, time_int, deal_ancestors
    )
    if quota is None:
        quota = DEAL_NODE_QUOTA_DEFAULT
    dealnode_dict = {
        "ancestors": deal_ancestors,
        "event_int": event_int,
        "dealdepth": get_0_if_None(dealdepth),
        "owner_name": time_owner_name,
        "penny": get_1_if_None(penny),
        "quota": quota,
    }
    save_json(dealnode_path, None, dealnode_dict)
