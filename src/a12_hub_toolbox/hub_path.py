from src.a00_data_toolbox.file_toolbox import create_path
from src.a01_term_logic.term import LabelTerm, OwnerName

BANK_FILENAME = "bank.json"
BANK_OTE1_AGG_CSV_FILENAME = "bank_ote1_agg.csv"
BANK_OTE1_AGG_JSON_FILENAME = "bank_ote1_agg.json"
BANK_AGENDA_FULL_LISTING_FILENAME = "agenda_full_listing.csv"
BUDUNIT_FILENAME = "budunit.json"
BUD_MANDATE_FILENAME = "bud_acct_mandate_ledger.json"
CELLNODE_FILENAME = "cell.json"
CELL_MANDATE_FILENAME = "cell_acct_mandate_ledger.json"
PLANPOINT_FILENAME = "planpoint.json"
PLANEVENT_FILENAME = "plan.json"
EVENT_ALL_PACK_FILENAME = "all_pack.json"
EVENT_EXPRESSED_PACK_FILENAME = "expressed_pack.json"


def treasury_filename() -> str:
    return "treasury.db"


def create_bank_dir_path(bank_mstr_dir: str, bank_label: LabelTerm) -> str:
    """Returns path: bank_mstr_dir\\banks\\bank_label"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    return create_path(banks_dir, bank_label)


def create_bank_json_path(bank_mstr_dir: str, bank_label: LabelTerm) -> str:
    """Returns path: bank_mstr_dir\\banks\\bank_label\\bank.json"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_path = create_path(banks_dir, bank_label)
    return create_path(bank_path, "bank.json")


def create_bank_ote1_csv_path(bank_mstr_dir: str, bank_label: LabelTerm):
    """Returns path: bank_mstr_dir\\banks\\bank_label\\bank_ote1_agg.csv"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_path = create_path(banks_dir, bank_label)
    return create_path(bank_path, "bank_ote1_agg.csv")


def create_bank_ote1_json_path(bank_mstr_dir: str, bank_label: LabelTerm):
    """Returns path: bank_mstr_dir\\banks\\bank_label\\bank_ote1_agg.json"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_path = create_path(banks_dir, bank_label)
    return create_path(bank_path, "bank_ote1_agg.json")


def bank_agenda_list_report_path(bank_mstr_dir: str, bank_label: LabelTerm) -> str:
    """Returns path: bank_mstr_dir\\banks\\bank_label\\agenda_full_listing.csv"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_path = create_path(banks_dir, bank_label)
    return create_path(bank_path, "agenda_full_listing.csv")


def create_bank_owners_dir_path(bank_mstr_dir: str, bank_label: LabelTerm) -> str:
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_dir = create_path(banks_dir, bank_label)
    return create_path(bank_dir, "owners")


def create_owner_dir_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName
) -> str:
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name"""

    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_dir = create_path(banks_dir, bank_label)
    owners_dir = create_path(bank_dir, "owners")
    return create_path(owners_dir, owner_name)


def create_keeps_dir_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName
) -> str:
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\keeps"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_dir = create_path(banks_dir, bank_label)
    owners_dir = create_path(bank_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "keeps")


def create_atoms_dir_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName
) -> str:
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\atoms"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_dir = create_path(banks_dir, bank_label)
    owners_dir = create_path(bank_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "atoms")


def create_packs_dir_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName
) -> str:
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\packs"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_dir = create_path(banks_dir, bank_label)
    owners_dir = create_path(bank_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "packs")


def create_buds_dir_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName
) -> str:
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\buds"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_dir = create_path(banks_dir, bank_label)
    owners_dir = create_path(bank_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    return create_path(owner_dir, "buds")


def create_bud_dir_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName, bud_time: int
):
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\buds\n\\bud_time"""
    timeline_dir = create_buds_dir_path(bank_mstr_dir, bank_label, owner_name)
    return create_path(timeline_dir, bud_time)


def create_budunit_json_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName, bud_time: int
) -> str:
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\buds\n\\bud_time\\budunit.json"""
    timepoint_dir = create_bud_dir_path(bank_mstr_dir, bank_label, owner_name, bud_time)
    return create_path(timepoint_dir, "budunit.json")


def create_bud_acct_mandate_ledger_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName, bud_time: int
) -> str:
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\buds\n\\bud_time\\bud_acct_mandate_ledger.json"""
    timepoint_dir = create_bud_dir_path(bank_mstr_dir, bank_label, owner_name, bud_time)
    return create_path(timepoint_dir, "bud_acct_mandate_ledger.json")


def create_planpoint_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName, bud_time: int
) -> str:
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\buds\n\\bud_time\\planpoint.json"""
    timepoint_dir = create_bud_dir_path(bank_mstr_dir, bank_label, owner_name, bud_time)
    return create_path(timepoint_dir, "planpoint.json")


def create_cell_dir_path(
    bank_mstr_dir: str,
    bank_label: LabelTerm,
    owner_name: OwnerName,
    bud_time: int,
    bud_ancestors: list[OwnerName],
):
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\buds\n\\bud_time\\ledger_owner1\\ledger_owner2\\ledger_owner3"""
    bud_celldepth_dir = create_bud_dir_path(
        bank_mstr_dir, bank_label, owner_name, bud_time
    )
    if bud_ancestors is None:
        bud_ancestors = []
    for ledger_owner in bud_ancestors:
        bud_celldepth_dir = create_path(bud_celldepth_dir, ledger_owner)
    return bud_celldepth_dir


def create_cell_json_path(
    bank_mstr_dir: str,
    bank_label: LabelTerm,
    owner_name: OwnerName,
    bud_time: int,
    bud_ancestors: list[OwnerName] = None,
):
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\buds\n\\bud_time\\ledger_owner1\\ledger_owner2\\ledger_owner3\\cell.json"""
    cell_dir = create_cell_dir_path(
        bank_mstr_dir, bank_label, owner_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell.json")


def create_cell_acct_mandate_ledger_path(
    bank_mstr_dir: str,
    bank_label: LabelTerm,
    owner_name: OwnerName,
    bud_time: int,
    bud_ancestors: list[OwnerName] = None,
):
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\buds\n\\bud_time\\ledger_owner1\\ledger_owner2\\ledger_owner3\\cell_acct_mandate_ledger.json"""
    cell_dir = create_cell_dir_path(
        bank_mstr_dir, bank_label, owner_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell_acct_mandate_ledger.json")


def create_owner_event_dir_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName, event_int: int
):
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\events\\event_int"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_dir = create_path(banks_dir, bank_label)
    owners_dir = create_path(bank_dir, "owners")
    bank_owner_dir = create_path(owners_dir, owner_name)
    bank_events_dir = create_path(bank_owner_dir, "events")
    return create_path(bank_events_dir, event_int)


def create_planevent_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName, event_int: int
):
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\events\\event_int\\plan.json"""
    owner_event_dir_path = create_owner_event_dir_path(
        bank_mstr_dir, bank_label, owner_name, event_int
    )
    plan_filename = "plan.json"
    return create_path(owner_event_dir_path, plan_filename)


def create_event_all_pack_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName, event_int: int
):
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\events\\event_int\\all_pack.json"""
    owner_event_dir_path = create_owner_event_dir_path(
        bank_mstr_dir, bank_label, owner_name, event_int
    )
    all_pack_filename = "all_pack.json"
    return create_path(owner_event_dir_path, all_pack_filename)


def create_event_expressed_pack_path(
    bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName, event_int: int
):
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\events\\event_int\\expressed_pack.json"""
    owner_event_dir_path = create_owner_event_dir_path(
        bank_mstr_dir, bank_label, owner_name, event_int
    )
    expressed_pack_filename = "expressed_pack.json"
    return create_path(owner_event_dir_path, expressed_pack_filename)


def create_gut_path(bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName):
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\gut\\owner_name.json"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_dir = create_path(banks_dir, bank_label)
    owners_dir = create_path(bank_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    gut_dir = create_path(owner_dir, "gut")
    return create_path(gut_dir, f"{owner_name}.json")


def create_job_path(bank_mstr_dir: str, bank_label: LabelTerm, owner_name: OwnerName):
    """Returns path: bank_mstr_dir\\banks\\bank_label\\owners\\owner_name\\job\\owner_name.json"""
    banks_dir = create_path(bank_mstr_dir, "banks")
    bank_dir = create_path(banks_dir, bank_label)
    owners_dir = create_path(bank_dir, "owners")
    owner_dir = create_path(owners_dir, owner_name)
    job_dir = create_path(owner_dir, "job")
    return create_path(job_dir, f"{owner_name}.json")
