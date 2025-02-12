from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_fisc_owner_time_csv_path,
    create_fisc_owner_time_json_path,
    fisc_agenda_list_report_path,
    create_owners_dir_path,
    create_episodes_dir_path,
    create_timepoint_dir_path,
    create_deal_path,
    create_budpoint_json_path,
    create_owner_event_dir_path,
    create_event_bud_path,
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
    doc_str = create_fisc_json_path("fisc_mstr", "fisc_title")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or LINUX_OS or inspect_getdoc(create_fisc_json_path) == doc_str


def test_create_fisc_owner_time_csv_path_HasDocString():
    # ESTABLISH
    doc_str = create_fisc_owner_time_csv_path("fisc_mstr", "fisc_title")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_fisc_owner_time_csv_path) == doc_str


def test_create_fisc_owner_time_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_fisc_owner_time_json_path("fisc_mstr", "fisc_title")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_fisc_owner_time_json_path) == doc_str


def test_fisc_agenda_list_report_path_HasDocString():
    # ESTABLISH
    doc_str = fisc_agenda_list_report_path("fisc_mstr", "fisc_title")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(fisc_agenda_list_report_path) == doc_str


def test_create_owners_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_owners_dir_path("fisc_mstr", "fisc_title")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_owners_dir_path) == doc_str


def test_create_episodes_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_episodes_dir_path("fisc_mstr", "fisc_title", "owner_name")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_episodes_dir_path) == doc_str


def test_create_timepoint_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_timepoint_dir_path(
        "fisc_mstr", "fisc_title", "owner_name", "timepoint_int"
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_timepoint_dir_path) == doc_str


def test_create_deal_path_HasDocString():
    # ESTABLISH
    doc_str = create_deal_path("fisc_mstr", "fisc_title", "owner_name", "timepoint_int")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_deal_path) == doc_str


def test_create_budpoint_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_budpoint_json_path(
        "fisc_mstr", "fisc_title", "owner_name", "timepoint_int"
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_budpoint_json_path) == doc_str


def test_create_owner_event_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_owner_event_dir_path(
        "fisc_mstr", "fisc_title", "owner_name", "event_int"
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_owner_event_dir_path) == doc_str


def test_create_event_bud_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_bud_path(
        "fisc_mstr", "fisc_title", "owner_name", "event_int"
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_bud_path) == doc_str


def test_create_event_all_gift_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_all_gift_path(
        "fisc_mstr", "fisc_title", "owner_name", "event_int"
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_all_gift_path) == doc_str


def test_create_event_expressed_gift_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_expressed_gift_path(
        "fisc_mstr", "fisc_title", "owner_name", "event_int"
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_expressed_gift_path) == doc_str


def test_create_voice_path_HasDocString():
    # ESTABLISH
    doc_str = create_voice_path("fisc_mstr", "fisc_title", "owner_name")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    print(f"{doc_str=}")
    print(f"{inspect_getdoc(create_voice_path)=}")
    print(inspect_getdoc(create_voice_path))
    assert LINUX_OS or inspect_getdoc(create_voice_path) == doc_str


def test_create_forecast_path_HasDocString():
    # ESTABLISH
    doc_str = create_forecast_path("fisc_mstr", "fisc_title", "owner_name")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_forecast_path) == doc_str
