from src.f00_instrument.file import create_path
from src.f01_road.road import OwnerName, TitleUnit

FISC_FILENAME = "fisc.json"
FISC_OTE1_AGG_CSV_FILENAME = "fisc_ote1_agg.csv"
FISC_OTE1_AGG_JSON_FILENAME = "fisc_ote1_agg.json"
FISC_AGENDA_FULL_LISTING_FILENAME = "agenda_full_listing.csv"
DEALUNIT_FILENAME = "dealunit.json"
CELLNODE_FILENAME = "cell_node.json"
CELL_QUOTA_LEDGER_FILENAME = "quota_ledger.json"
CELL_BUDEVENT_FACTS_FILENAME = "budevent_facts.json"
CELL_FOUND_FACTS_FILENAME = "found_facts.json"
BUDPOINT_FILENAME = "budpoint.json"
BUDEVENT_FILENAME = "bud.json"
EVENT_ALL_GIFT_FILENAME = "all_gift.json"
EVENT_EXPRESSED_GIFT_FILENAME = "expressed_gift.json"


def create_fisc_json_path(fisc_mstr_dir: str, fisc_title: TitleUnit) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\fisc.json"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_path = create_path(fiscs_dir, fisc_title)
    return create_path(fisc_path, "fisc.json")


def create_fisc_ote1_csv_path(fisc_mstr_dir: str, fisc_title: TitleUnit):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\fisc_ote1_agg.csv"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_path = create_path(fiscs_dir, fisc_title)
    return create_path(fisc_path, "fisc_ote1_agg.csv")


def create_fisc_ote1_json_path(fisc_mstr_dir: str, fisc_title: TitleUnit):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\fisc_ote1_agg.json"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_path = create_path(fiscs_dir, fisc_title)
    return create_path(fisc_path, "fisc_ote1_agg.json")


def fisc_agenda_list_report_path(fisc_mstr_dir: str, fisc_title: TitleUnit) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\agenda_full_listing.csv"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_path = create_path(fiscs_dir, fisc_title)
    return create_path(fisc_path, "agenda_full_listing.csv")


def create_owners_dir_path(fisc_mstr_dir: str, fisc_title: TitleUnit) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    return create_path(fisc_dir, "owners")


def create_deals_dir_path(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName
) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\deals"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "deals")


def create_deal_dir_path(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, time_int: int
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\deals\n\\time_int"""
    timeline_dir = create_deals_dir_path(fisc_mstr_dir, fisc_title, owner_name)
    return create_path(timeline_dir, time_int)


def create_dealunit_json_path(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, time_int: int
) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\deals\n\\time_int\\dealunit.json"""
    timepoint_dir = create_deal_dir_path(
        fisc_mstr_dir, fisc_title, owner_name, time_int
    )
    return create_path(timepoint_dir, "dealunit.json")


def create_budpoint_path(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, time_int: int
) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\deals\n\\time_int\\budpoint.json"""
    timepoint_dir = create_deal_dir_path(
        fisc_mstr_dir, fisc_title, owner_name, time_int
    )
    return create_path(timepoint_dir, "budpoint.json")


def create_cell_dir_path(
    fisc_mstr_dir: str,
    fisc_title: TitleUnit,
    owner_name: OwnerName,
    time_int: int,
    deal_ancestors: list[OwnerName],
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\deals\n\\time_int\\ledger_owner1\\ledger_owner2\\ledger_owner3"""
    deal_celldepth_dir = create_deal_dir_path(
        fisc_mstr_dir, fisc_title, owner_name, time_int
    )
    if deal_ancestors is None:
        deal_ancestors = []
    for ledger_owner in deal_ancestors:
        deal_celldepth_dir = create_path(deal_celldepth_dir, ledger_owner)
    return deal_celldepth_dir


def create_cell_node_json_path(
    fisc_mstr_dir: str,
    fisc_title: TitleUnit,
    owner_name: OwnerName,
    time_int: int,
    deal_ancestors: list[OwnerName] = None,
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\deals\n\\time_int\\ledger_owner1\\ledger_owner2\\ledger_owner3\\cell_node.json"""
    timepoint_dir = create_cell_dir_path(
        fisc_mstr_dir, fisc_title, owner_name, time_int, deal_ancestors
    )
    return create_path(timepoint_dir, "cell_node.json")


def create_cell_quota_ledger_path(
    fisc_mstr_dir: str,
    fisc_title: TitleUnit,
    owner_name: OwnerName,
    time_int: int,
    deal_ancestors: list[OwnerName] = None,
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\deals\n\\time_int\\ledger_owner1\\ledger_owner2\\ledger_owner3\\quota_ledger.json"""
    timepoint_dir = create_cell_dir_path(
        fisc_mstr_dir, fisc_title, owner_name, time_int, deal_ancestors
    )
    return create_path(timepoint_dir, "quota_ledger.json")


def create_cell_budevent_facts_path(
    fisc_mstr_dir: str,
    fisc_title: TitleUnit,
    owner_name: OwnerName,
    time_int: int,
    deal_ancestors: list[OwnerName] = None,
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\deals\n\\time_int\\ledger_owner1\\ledger_owner2\\ledger_owner3\\budevent_facts.json"""
    timepoint_dir = create_cell_dir_path(
        fisc_mstr_dir, fisc_title, owner_name, time_int, deal_ancestors
    )
    return create_path(timepoint_dir, "budevent_facts.json")


def create_cell_found_facts_path(
    fisc_mstr_dir: str,
    fisc_title: TitleUnit,
    owner_name: OwnerName,
    time_int: int,
    deal_ancestors: list[OwnerName] = None,
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\deals\n\\time_int\\ledger_owner1\\ledger_owner2\\ledger_owner3\\found_facts.json"""
    timepoint_dir = create_cell_dir_path(
        fisc_mstr_dir, fisc_title, owner_name, time_int, deal_ancestors
    )
    return create_path(timepoint_dir, "found_facts.json")


def create_owner_event_dir_path(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, event_int: int
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\events\\event_int"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    fisc_owner_dir = create_path(owners_dir, owner_name)
    fisc_events_dir = create_path(fisc_owner_dir, "events")
    return create_path(fisc_events_dir, event_int)


def create_budevent_path(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, event_int: int
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\events\\event_int\\bud.json"""
    owner_event_dir_path = create_owner_event_dir_path(
        fisc_mstr_dir, fisc_title, owner_name, event_int
    )
    bud_filename = "bud.json"
    return create_path(owner_event_dir_path, bud_filename)


def create_event_all_gift_path(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, event_int: int
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\events\\event_int\\all_gift.json"""
    owner_event_dir_path = create_owner_event_dir_path(
        fisc_mstr_dir, fisc_title, owner_name, event_int
    )
    all_gift_filename = "all_gift.json"
    return create_path(owner_event_dir_path, all_gift_filename)


def create_event_expressed_gift_path(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName, event_int: int
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\events\\event_int\\expressed_gift.json"""
    owner_event_dir_path = create_owner_event_dir_path(
        fisc_mstr_dir, fisc_title, owner_name, event_int
    )
    expressed_gift_filename = "expressed_gift.json"
    return create_path(owner_event_dir_path, expressed_gift_filename)


def create_voice_path(fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\voice\\owner_name.json"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    voice_dir = create_path(owner_dir, "voice")
    return create_path(voice_dir, f"{owner_name}.json")


def create_forecast_path(
    fisc_mstr_dir: str, fisc_title: TitleUnit, owner_name: OwnerName
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_title\\owners\\owner_name\\forecast\\owner_name.json"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_title)
    owners_dir = create_path(fisc_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    forecast_dir = create_path(owner_dir, "forecast")
    return create_path(forecast_dir, f"{owner_name}.json")
