from src.f01_road.deal import owner_name_str, time_int_str, fisc_title_str
from src.f04_gift.atom_config import event_int_str
from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_fisc_ote1_csv_path,
    create_fisc_ote1_json_path,
    fisc_agenda_list_report_path,
    create_owners_dir_path,
    create_deals_dir_path,
    create_deal_dir_path,
    create_dealunit_json_path,
    create_budpoint_path,
    create_cell_dir_path,
    create_cell_json_path,
    create_acct_mandate_ledger_path,
    create_owner_event_dir_path,
    create_budevent_path,
    create_event_all_gift_path,
    create_event_expressed_gift_path,
    create_voice_path,
    create_forecast_path,
)
from inspect import getdoc as inspect_getdoc
from platform import system as platform_system

LINUX_OS = platform_system() == "Linux"


def test_create_fisc_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_fisc_json_path(
        fisc_mstr_dir="fisc_mstr_dir", fisc_title=fisc_title_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or LINUX_OS or inspect_getdoc(create_fisc_json_path) == doc_str


def test_create_fisc_ote1_csv_path_HasDocString():
    # ESTABLISH
    doc_str = create_fisc_ote1_csv_path(
        fisc_mstr_dir="fisc_mstr_dir", fisc_title=fisc_title_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_fisc_ote1_csv_path) == doc_str


def test_create_fisc_ote1_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_fisc_ote1_json_path(
        fisc_mstr_dir="fisc_mstr_dir", fisc_title=fisc_title_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_fisc_ote1_json_path) == doc_str


def test_fisc_agenda_list_report_path_HasDocString():
    # ESTABLISH
    doc_str = fisc_agenda_list_report_path(
        fisc_mstr_dir="fisc_mstr_dir", fisc_title=fisc_title_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(fisc_agenda_list_report_path) == doc_str


def test_create_owners_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_owners_dir_path(
        fisc_mstr_dir="fisc_mstr_dir", fisc_title=fisc_title_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_owners_dir_path) == doc_str


def test_create_deals_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_deals_dir_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_title=fisc_title_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_deals_dir_path) == doc_str


def test_create_deal_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_deal_dir_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_title=fisc_title_str(),
        owner_name=owner_name_str(),
        time_int=time_int_str(),
    )
    doc_str = doc_str.replace("deals\\time_int", "deals\n\\time_int")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_deal_dir_path) == doc_str


def test_create_cell_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_dir_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_title=fisc_title_str(),
        owner_name=owner_name_str(),
        time_int=time_int_str(),
        deal_ancestors=["ledger_owner1", "ledger_owner2", "ledger_owner3"],
    )
    doc_str = doc_str.replace("deals\\time_int", "deals\n\\time_int")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_dir_path) == doc_str


def test_create_cell_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_json_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_title=fisc_title_str(),
        owner_name=owner_name_str(),
        time_int=time_int_str(),
        deal_ancestors=["ledger_owner1", "ledger_owner2", "ledger_owner3"],
    )
    doc_str = doc_str.replace("deals\\time_int", "deals\n\\time_int")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_json_path) == doc_str


def test_create_acct_mandate_ledger_path_HasDocString():
    # ESTABLISH
    doc_str = create_acct_mandate_ledger_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_title=fisc_title_str(),
        owner_name=owner_name_str(),
        time_int=time_int_str(),
        deal_ancestors=["ledger_owner1", "ledger_owner2", "ledger_owner3"],
    )
    doc_str = doc_str.replace("deals\\time_int", "deals\n\\time_int")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_acct_mandate_ledger_path) == doc_str


def test_create_dealunit_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_dealunit_json_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_title=fisc_title_str(),
        owner_name=owner_name_str(),
        time_int=time_int_str(),
    )
    doc_str = doc_str.replace("deals\\time_int", "deals\n\\time_int")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_dealunit_json_path) == doc_str


def test_create_budpoint_path_HasDocString():
    # ESTABLISH
    doc_str = create_budpoint_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_title=fisc_title_str(),
        owner_name=owner_name_str(),
        time_int=time_int_str(),
    )
    doc_str = doc_str.replace("deals\\time_int", "deals\n\\time_int")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_budpoint_path) == doc_str


def test_create_owner_event_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_owner_event_dir_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_title=fisc_title_str(),
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
        fisc_title=fisc_title_str(),
        owner_name=owner_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_budevent_path) == doc_str


def test_create_event_all_gift_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_all_gift_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_title=fisc_title_str(),
        owner_name=owner_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_all_gift_path) == doc_str


def test_create_event_expressed_gift_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_expressed_gift_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_title=fisc_title_str(),
        owner_name=owner_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_expressed_gift_path) == doc_str


def test_create_voice_path_HasDocString():
    # ESTABLISH
    doc_str = create_voice_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_title=fisc_title_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    print(f"{doc_str=}")
    print(f"{inspect_getdoc(create_voice_path)=}")
    print(inspect_getdoc(create_voice_path))
    assert LINUX_OS or inspect_getdoc(create_voice_path) == doc_str


def test_create_forecast_path_HasDocString():
    # ESTABLISH
    doc_str = create_forecast_path(
        fisc_mstr_dir="fisc_mstr_dir",
        fisc_title=fisc_title_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_forecast_path) == doc_str
