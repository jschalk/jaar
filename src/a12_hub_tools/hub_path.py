from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_way_logic.way import OwnerName, TagStr

FISC_FILENAME = "fisc.json"
FISC_OTE1_AGG_CSV_FILENAME = "fisc_ote1_agg.csv"
FISC_OTE1_AGG_JSON_FILENAME = "fisc_ote1_agg.json"
FISC_AGENDA_FULL_LISTING_FILENAME = "agenda_full_listing.csv"
DEALUNIT_FILENAME = "dealunit.json"
DEAL_MANDATE_FILENAME = "deal_acct_mandate_ledger.json"
CELLNODE_FILENAME = "cell.json"
CELL_MANDATE_FILENAME = "cell_acct_mandate_ledger.json"
BUDPOINT_FILENAME = "budpoint.json"
BUDEVENT_FILENAME = "bud.json"
EVENT_ALL_PACK_FILENAME = "all_pack.json"
EVENT_EXPRESSED_PACK_FILENAME = "expressed_pack.json"


def treasury_filename() -> str:
    return "treasury.db"


def gut_str() -> str:
    return "gut"


def job_str() -> str:
    return "job"


def create_fisc_dir_path(fisc_mstr_dir: str, fisc_tag: TagStr) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    return create_path(fiscs_dir, fisc_tag)


def create_fisc_json_path(fisc_mstr_dir: str, fisc_tag: TagStr) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\fisc.json"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_path = create_path(fiscs_dir, fisc_tag)
    return create_path(fisc_path, "fisc.json")


def create_fisc_ote1_csv_path(fisc_mstr_dir: str, fisc_tag: TagStr):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\fisc_ote1_agg.csv"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_path = create_path(fiscs_dir, fisc_tag)
    return create_path(fisc_path, "fisc_ote1_agg.csv")


def create_fisc_ote1_json_path(fisc_mstr_dir: str, fisc_tag: TagStr):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\fisc_ote1_agg.json"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_path = create_path(fiscs_dir, fisc_tag)
    return create_path(fisc_path, "fisc_ote1_agg.json")


def fisc_agenda_list_report_path(fisc_mstr_dir: str, fisc_tag: TagStr) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\agenda_full_listing.csv"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_path = create_path(fiscs_dir, fisc_tag)
    return create_path(fisc_path, "agenda_full_listing.csv")


def create_fisc_owners_dir_path(fisc_mstr_dir: str, fisc_tag: TagStr) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_tag)
    return create_path(fisc_dir, "owners")


def create_owner_dir_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName
) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name"""

    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_tag)
    owners_dir = create_path(fisc_dir, "owners")
    return create_path(owners_dir, owner_name)


def create_keeps_dir_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName
) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\keeps"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_tag)
    owners_dir = create_path(fisc_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "keeps")


def create_atoms_dir_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName
) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\atoms"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_tag)
    owners_dir = create_path(fisc_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "atoms")


def create_packs_dir_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName
) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\packs"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_tag)
    owners_dir = create_path(fisc_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "packs")


def create_deals_dir_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName
) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\deals"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_tag)
    owners_dir = create_path(fisc_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "deals")


def create_deal_dir_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName, deal_time: int
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\deals\n\\deal_time"""
    timeline_dir = create_deals_dir_path(fisc_mstr_dir, fisc_tag, owner_name)
    return create_path(timeline_dir, deal_time)


def create_dealunit_json_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName, deal_time: int
) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\deals\n\\deal_time\\dealunit.json"""
    timepoint_dir = create_deal_dir_path(fisc_mstr_dir, fisc_tag, owner_name, deal_time)
    return create_path(timepoint_dir, "dealunit.json")


def create_deal_acct_mandate_ledger_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName, deal_time: int
) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\deals\n\\deal_time\\deal_acct_mandate_ledger.json"""
    timepoint_dir = create_deal_dir_path(fisc_mstr_dir, fisc_tag, owner_name, deal_time)
    return create_path(timepoint_dir, "deal_acct_mandate_ledger.json")


def create_budpoint_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName, deal_time: int
) -> str:
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\deals\n\\deal_time\\budpoint.json"""
    timepoint_dir = create_deal_dir_path(fisc_mstr_dir, fisc_tag, owner_name, deal_time)
    return create_path(timepoint_dir, "budpoint.json")


def create_cell_dir_path(
    fisc_mstr_dir: str,
    fisc_tag: TagStr,
    owner_name: OwnerName,
    deal_time: int,
    deal_ancestors: list[OwnerName],
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\deals\n\\deal_time\\ledger_owner1\\ledger_owner2\\ledger_owner3"""
    deal_celldepth_dir = create_deal_dir_path(
        fisc_mstr_dir, fisc_tag, owner_name, deal_time
    )
    if deal_ancestors is None:
        deal_ancestors = []
    for ledger_owner in deal_ancestors:
        deal_celldepth_dir = create_path(deal_celldepth_dir, ledger_owner)
    return deal_celldepth_dir


def create_cell_json_path(
    fisc_mstr_dir: str,
    fisc_tag: TagStr,
    owner_name: OwnerName,
    deal_time: int,
    deal_ancestors: list[OwnerName] = None,
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\deals\n\\deal_time\\ledger_owner1\\ledger_owner2\\ledger_owner3\\cell.json"""
    cell_dir = create_cell_dir_path(
        fisc_mstr_dir, fisc_tag, owner_name, deal_time, deal_ancestors
    )
    return create_path(cell_dir, "cell.json")


def create_cell_acct_mandate_ledger_path(
    fisc_mstr_dir: str,
    fisc_tag: TagStr,
    owner_name: OwnerName,
    deal_time: int,
    deal_ancestors: list[OwnerName] = None,
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\deals\n\\deal_time\\ledger_owner1\\ledger_owner2\\ledger_owner3\\cell_acct_mandate_ledger.json"""
    cell_dir = create_cell_dir_path(
        fisc_mstr_dir, fisc_tag, owner_name, deal_time, deal_ancestors
    )
    return create_path(cell_dir, "cell_acct_mandate_ledger.json")


def create_owner_event_dir_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName, event_int: int
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\events\\event_int"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_tag)
    owners_dir = create_path(fisc_dir, "owners")
    fisc_owner_dir = create_path(owners_dir, owner_name)
    fisc_events_dir = create_path(fisc_owner_dir, "events")
    return create_path(fisc_events_dir, event_int)


def create_budevent_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName, event_int: int
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\events\\event_int\\bud.json"""
    owner_event_dir_path = create_owner_event_dir_path(
        fisc_mstr_dir, fisc_tag, owner_name, event_int
    )
    bud_filename = "bud.json"
    return create_path(owner_event_dir_path, bud_filename)


def create_event_all_pack_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName, event_int: int
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\events\\event_int\\all_pack.json"""
    owner_event_dir_path = create_owner_event_dir_path(
        fisc_mstr_dir, fisc_tag, owner_name, event_int
    )
    all_pack_filename = "all_pack.json"
    return create_path(owner_event_dir_path, all_pack_filename)


def create_event_expressed_pack_path(
    fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName, event_int: int
):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\events\\event_int\\expressed_pack.json"""
    owner_event_dir_path = create_owner_event_dir_path(
        fisc_mstr_dir, fisc_tag, owner_name, event_int
    )
    expressed_pack_filename = "expressed_pack.json"
    return create_path(owner_event_dir_path, expressed_pack_filename)


def create_gut_path(fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\gut\\owner_name.json"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_tag)
    owners_dir = create_path(fisc_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    gut_dir = create_path(owner_dir, "gut")
    return create_path(gut_dir, f"{owner_name}.json")


def create_job_path(fisc_mstr_dir: str, fisc_tag: TagStr, owner_name: OwnerName):
    """Returns path: fisc_mstr_dir\\fiscs\\fisc_tag\\owners\\owner_name\\job\\owner_name.json"""
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    fisc_dir = create_path(fiscs_dir, fisc_tag)
    owners_dir = create_path(fisc_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    job_dir = create_path(owner_dir, "job")
    return create_path(job_dir, f"{owner_name}.json")
