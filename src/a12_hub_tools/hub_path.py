from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.term import LabelTerm, OwnerName

VOW_FILENAME = "vow.json"
VOW_OTE1_AGG_CSV_FILENAME = "vow_ote1_agg.csv"
VOW_OTE1_AGG_JSON_FILENAME = "vow_ote1_agg.json"
VOW_AGENDA_FULL_LISTING_FILENAME = "agenda_full_listing.csv"
DEALUNIT_FILENAME = "dealunit.json"
DEAL_MANDATE_FILENAME = "deal_acct_mandate_ledger.json"
CELLNODE_FILENAME = "cell.json"
CELL_MANDATE_FILENAME = "cell_acct_mandate_ledger.json"
PLANPOINT_FILENAME = "planpoint.json"
PLANEVENT_FILENAME = "plan.json"
EVENT_ALL_PACK_FILENAME = "all_pack.json"
EVENT_EXPRESSED_PACK_FILENAME = "expressed_pack.json"


def treasury_filename() -> str:
    return "treasury.db"


def create_vow_dir_path(vow_mstr_dir: str, vow_label: LabelTerm) -> str:
    """Returns path: vow_mstr_dir\\vows\\vow_label"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    return create_path(vows_dir, vow_label)


def create_vow_json_path(vow_mstr_dir: str, vow_label: LabelTerm) -> str:
    """Returns path: vow_mstr_dir\\vows\\vow_label\\vow.json"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_path = create_path(vows_dir, vow_label)
    return create_path(vow_path, "vow.json")


def create_vow_ote1_csv_path(vow_mstr_dir: str, vow_label: LabelTerm):
    """Returns path: vow_mstr_dir\\vows\\vow_label\\vow_ote1_agg.csv"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_path = create_path(vows_dir, vow_label)
    return create_path(vow_path, "vow_ote1_agg.csv")


def create_vow_ote1_json_path(vow_mstr_dir: str, vow_label: LabelTerm):
    """Returns path: vow_mstr_dir\\vows\\vow_label\\vow_ote1_agg.json"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_path = create_path(vows_dir, vow_label)
    return create_path(vow_path, "vow_ote1_agg.json")


def vow_agenda_list_report_path(vow_mstr_dir: str, vow_label: LabelTerm) -> str:
    """Returns path: vow_mstr_dir\\vows\\vow_label\\agenda_full_listing.csv"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_path = create_path(vows_dir, vow_label)
    return create_path(vow_path, "agenda_full_listing.csv")


def create_vow_owners_dir_path(vow_mstr_dir: str, vow_label: LabelTerm) -> str:
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    return create_path(vow_dir, "owners")


def create_owner_dir_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName
) -> str:
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name"""

    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    return create_path(owners_dir, owner_name)


def create_keeps_dir_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName
) -> str:
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\keeps"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "keeps")


def create_atoms_dir_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName
) -> str:
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\atoms"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "atoms")


def create_packs_dir_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName
) -> str:
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\packs"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "packs")


def create_deals_dir_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName
) -> str:
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\deals"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "deals")


def create_deal_dir_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName, deal_time: int
):
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\deals\n\\deal_time"""
    timeline_dir = create_deals_dir_path(vow_mstr_dir, vow_label, owner_name)
    return create_path(timeline_dir, deal_time)


def create_dealunit_json_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName, deal_time: int
) -> str:
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\deals\n\\deal_time\\dealunit.json"""
    timepoint_dir = create_deal_dir_path(vow_mstr_dir, vow_label, owner_name, deal_time)
    return create_path(timepoint_dir, "dealunit.json")


def create_deal_acct_mandate_ledger_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName, deal_time: int
) -> str:
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\deals\n\\deal_time\\deal_acct_mandate_ledger.json"""
    timepoint_dir = create_deal_dir_path(vow_mstr_dir, vow_label, owner_name, deal_time)
    return create_path(timepoint_dir, "deal_acct_mandate_ledger.json")


def create_planpoint_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName, deal_time: int
) -> str:
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\deals\n\\deal_time\\planpoint.json"""
    timepoint_dir = create_deal_dir_path(vow_mstr_dir, vow_label, owner_name, deal_time)
    return create_path(timepoint_dir, "planpoint.json")


def create_cell_dir_path(
    vow_mstr_dir: str,
    vow_label: LabelTerm,
    owner_name: OwnerName,
    deal_time: int,
    deal_ancestors: list[OwnerName],
):
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\deals\n\\deal_time\\ledger_owner1\\ledger_owner2\\ledger_owner3"""
    deal_celldepth_dir = create_deal_dir_path(
        vow_mstr_dir, vow_label, owner_name, deal_time
    )
    if deal_ancestors is None:
        deal_ancestors = []
    for ledger_owner in deal_ancestors:
        deal_celldepth_dir = create_path(deal_celldepth_dir, ledger_owner)
    return deal_celldepth_dir


def create_cell_json_path(
    vow_mstr_dir: str,
    vow_label: LabelTerm,
    owner_name: OwnerName,
    deal_time: int,
    deal_ancestors: list[OwnerName] = None,
):
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\deals\n\\deal_time\\ledger_owner1\\ledger_owner2\\ledger_owner3\\cell.json"""
    cell_dir = create_cell_dir_path(
        vow_mstr_dir, vow_label, owner_name, deal_time, deal_ancestors
    )
    return create_path(cell_dir, "cell.json")


def create_cell_acct_mandate_ledger_path(
    vow_mstr_dir: str,
    vow_label: LabelTerm,
    owner_name: OwnerName,
    deal_time: int,
    deal_ancestors: list[OwnerName] = None,
):
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\deals\n\\deal_time\\ledger_owner1\\ledger_owner2\\ledger_owner3\\cell_acct_mandate_ledger.json"""
    cell_dir = create_cell_dir_path(
        vow_mstr_dir, vow_label, owner_name, deal_time, deal_ancestors
    )
    return create_path(cell_dir, "cell_acct_mandate_ledger.json")


def create_owner_event_dir_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName, event_int: int
):
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\events\\event_int"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    vow_owner_dir = create_path(owners_dir, owner_name)
    vow_events_dir = create_path(vow_owner_dir, "events")
    return create_path(vow_events_dir, event_int)


def create_planevent_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName, event_int: int
):
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\events\\event_int\\plan.json"""
    owner_event_dir_path = create_owner_event_dir_path(
        vow_mstr_dir, vow_label, owner_name, event_int
    )
    plan_filename = "plan.json"
    return create_path(owner_event_dir_path, plan_filename)


def create_event_all_pack_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName, event_int: int
):
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\events\\event_int\\all_pack.json"""
    owner_event_dir_path = create_owner_event_dir_path(
        vow_mstr_dir, vow_label, owner_name, event_int
    )
    all_pack_filename = "all_pack.json"
    return create_path(owner_event_dir_path, all_pack_filename)


def create_event_expressed_pack_path(
    vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName, event_int: int
):
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\events\\event_int\\expressed_pack.json"""
    owner_event_dir_path = create_owner_event_dir_path(
        vow_mstr_dir, vow_label, owner_name, event_int
    )
    expressed_pack_filename = "expressed_pack.json"
    return create_path(owner_event_dir_path, expressed_pack_filename)


def create_gut_path(vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName):
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\gut\\owner_name.json"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    gut_dir = create_path(owner_dir, "gut")
    return create_path(gut_dir, f"{owner_name}.json")


def create_job_path(vow_mstr_dir: str, vow_label: LabelTerm, owner_name: OwnerName):
    """Returns path: vow_mstr_dir\\vows\\vow_label\\owners\\owner_name\\job\\owner_name.json"""
    vows_dir = create_path(vow_mstr_dir, "vows")
    vow_dir = create_path(vows_dir, vow_label)
    owners_dir = create_path(vow_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    job_dir = create_path(owner_dir, "job")
    return create_path(job_dir, f"{owner_name}.json")
