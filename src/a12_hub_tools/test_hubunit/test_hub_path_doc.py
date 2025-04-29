from src.a02_finance_logic._utils.strs_a02 import (
    owner_name_str,
    deal_time_str,
    fisc_tag_str,
)
from src.a08_bud_atom_logic.atom_config import event_int_str
from src.a12_hub_tools.hub_path import (
    create_fisc_dir_path,
    create_fisc_json_path,
    create_fisc_ote1_csv_path,
    create_fisc_ote1_json_path,
    fisc_agenda_list_report_path,
    create_fisc_owners_dir_path,
    create_owner_dir_path,
    create_keeps_dir_path,
    create_atoms_dir_path,
    create_packs_dir_path,
    create_deals_dir_path,
    create_deal_dir_path,
    create_dealunit_json_path,
    create_deal_acct_mandate_ledger_path,
    create_budpoint_path,
    create_cell_dir_path,
    create_cell_json_path,
    create_cell_acct_mandate_ledger_path,
    create_owner_event_dir_path,
    create_budevent_path,
    create_event_all_pack_path,
    create_event_expressed_pack_path,
    create_gut_path,
    create_job_path,
)
from inspect import getdoc as inspect_getdoc
from platform import system as platform_system

LINUX_OS = platform_system() == "Linux"


def test_create_fisc_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_fisc_dir_path("fisc_mstr_dir", fisc_tag_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_fisc_dir_path) == doc_str


def test_create_fisc_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_fisc_json_path("fisc_mstr_dir", fisc_tag=fisc_tag_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_fisc_json_path) == doc_str


def test_create_fisc_ote1_csv_path_HasDocString():
    # ESTABLISH
    doc_str = create_fisc_ote1_csv_path("fisc_mstr_dir", fisc_tag=fisc_tag_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_fisc_ote1_csv_path) == doc_str


def test_create_fisc_ote1_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_fisc_ote1_json_path("fisc_mstr_dir", fisc_tag=fisc_tag_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_fisc_ote1_json_path) == doc_str


def test_fisc_agenda_list_report_path_HasDocString():
    # ESTABLISH
    doc_str = fisc_agenda_list_report_path("fisc_mstr_dir", fisc_tag=fisc_tag_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(fisc_agenda_list_report_path) == doc_str


def test_create_fisc_owners_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_fisc_owners_dir_path("fisc_mstr_dir", fisc_tag=fisc_tag_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_fisc_owners_dir_path) == doc_str


def test_create_owner_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_owner_dir_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_owner_dir_path) == doc_str


def test_create_keeps_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_keeps_dir_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keeps_dir_path) == doc_str


def test_create_atoms_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_atoms_dir_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_atoms_dir_path) == doc_str


def test_create_packs_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_packs_dir_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_packs_dir_path) == doc_str


def test_create_deals_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_deals_dir_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_deals_dir_path) == doc_str


def test_create_deal_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_deal_dir_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
        deal_time=deal_time_str(),
    )
    doc_str = doc_str.replace("deals\\deal_time", "deals\n\\deal_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_deal_dir_path) == doc_str


def test_create_cell_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_dir_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
        deal_time=deal_time_str(),
        deal_ancestors=["ledger_owner1", "ledger_owner2", "ledger_owner3"],
    )
    doc_str = doc_str.replace("deals\\deal_time", "deals\n\\deal_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_dir_path) == doc_str


def test_create_cell_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_json_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
        deal_time=deal_time_str(),
        deal_ancestors=["ledger_owner1", "ledger_owner2", "ledger_owner3"],
    )
    doc_str = doc_str.replace("deals\\deal_time", "deals\n\\deal_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_json_path) == doc_str


def test_create_cell_acct_mandate_ledger_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_acct_mandate_ledger_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
        deal_time=deal_time_str(),
        deal_ancestors=["ledger_owner1", "ledger_owner2", "ledger_owner3"],
    )
    doc_str = doc_str.replace("deals\\deal_time", "deals\n\\deal_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_acct_mandate_ledger_path) == doc_str


def test_create_dealunit_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_dealunit_json_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
        deal_time=deal_time_str(),
    )
    doc_str = doc_str.replace("deals\\deal_time", "deals\n\\deal_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_dealunit_json_path) == doc_str


def test_create_deal_acct_mandate_ledger_path_HasDocString():
    # ESTABLISH
    doc_str = create_deal_acct_mandate_ledger_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
        deal_time=deal_time_str(),
    )
    doc_str = doc_str.replace("deals\\deal_time", "deals\n\\deal_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_deal_acct_mandate_ledger_path) == doc_str


def test_create_budpoint_path_HasDocString():
    # ESTABLISH
    doc_str = create_budpoint_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
        deal_time=deal_time_str(),
    )
    doc_str = doc_str.replace("deals\\deal_time", "deals\n\\deal_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_budpoint_path) == doc_str


def test_create_owner_event_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_owner_event_dir_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_owner_event_dir_path) == doc_str


def test_create_budevent_path_HasDocString():
    # ESTABLISH
    doc_str = create_budevent_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_budevent_path) == doc_str


def test_create_event_all_pack_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_all_pack_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_all_pack_path) == doc_str


def test_create_event_expressed_pack_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_expressed_pack_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_expressed_pack_path) == doc_str


def test_create_gut_path_HasDocString():
    # ESTABLISH
    doc_str = create_gut_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    print(f"{doc_str=}")
    print(f"{inspect_getdoc(create_gut_path)=}")
    print(inspect_getdoc(create_gut_path))
    assert LINUX_OS or inspect_getdoc(create_gut_path) == doc_str


def test_create_job_path_HasDocString():
    # ESTABLISH
    doc_str = create_job_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_tag=fisc_tag_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_job_path) == doc_str
