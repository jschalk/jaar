from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.a02_finance_logic.test._util.a02_str import (
    bank_label_str,
    bud_time_str,
    owner_name_str,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str
from src.a12_hub_toolbox.hub_path import (
    bank_agenda_list_report_path,
    create_atoms_dir_path,
    create_bank_dir_path,
    create_bank_json_path,
    create_bank_ote1_csv_path,
    create_bank_ote1_json_path,
    create_bank_owners_dir_path,
    create_bud_acct_mandate_ledger_path,
    create_bud_dir_path,
    create_buds_dir_path,
    create_budunit_json_path,
    create_cell_acct_mandate_ledger_path,
    create_cell_dir_path,
    create_cell_json_path,
    create_event_all_pack_path,
    create_event_expressed_pack_path,
    create_gut_path,
    create_job_path,
    create_keeps_dir_path,
    create_owner_dir_path,
    create_owner_event_dir_path,
    create_packs_dir_path,
    create_planevent_path,
    create_planpoint_path,
)

LINUX_OS = platform_system() == "Linux"


def test_create_bank_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_bank_dir_path("bank_mstr_dir", bank_label_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bank_dir_path) == doc_str


def test_create_bank_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_bank_json_path("bank_mstr_dir", bank_label=bank_label_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bank_json_path) == doc_str


def test_create_bank_ote1_csv_path_HasDocString():
    # ESTABLISH
    doc_str = create_bank_ote1_csv_path("bank_mstr_dir", bank_label=bank_label_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bank_ote1_csv_path) == doc_str


def test_create_bank_ote1_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_bank_ote1_json_path("bank_mstr_dir", bank_label=bank_label_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bank_ote1_json_path) == doc_str


def test_bank_agenda_list_report_path_HasDocString():
    # ESTABLISH
    doc_str = bank_agenda_list_report_path("bank_mstr_dir", bank_label=bank_label_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(bank_agenda_list_report_path) == doc_str


def test_create_bank_owners_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_bank_owners_dir_path("bank_mstr_dir", bank_label=bank_label_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bank_owners_dir_path) == doc_str


def test_create_owner_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_owner_dir_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_owner_dir_path) == doc_str


def test_create_keeps_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_keeps_dir_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keeps_dir_path) == doc_str


def test_create_atoms_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_atoms_dir_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_atoms_dir_path) == doc_str


def test_create_packs_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_packs_dir_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_packs_dir_path) == doc_str


def test_create_buds_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_buds_dir_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_buds_dir_path) == doc_str


def test_create_bud_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_bud_dir_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
        bud_time=bud_time_str(),
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bud_dir_path) == doc_str


def test_create_cell_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_dir_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
        bud_time=bud_time_str(),
        bud_ancestors=["ledger_owner1", "ledger_owner2", "ledger_owner3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_dir_path) == doc_str


def test_create_cell_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_json_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
        bud_time=bud_time_str(),
        bud_ancestors=["ledger_owner1", "ledger_owner2", "ledger_owner3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_json_path) == doc_str


def test_create_cell_acct_mandate_ledger_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_acct_mandate_ledger_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
        bud_time=bud_time_str(),
        bud_ancestors=["ledger_owner1", "ledger_owner2", "ledger_owner3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_acct_mandate_ledger_path) == doc_str


def test_create_budunit_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_budunit_json_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
        bud_time=bud_time_str(),
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_budunit_json_path) == doc_str


def test_create_bud_acct_mandate_ledger_path_HasDocString():
    # ESTABLISH
    doc_str = create_bud_acct_mandate_ledger_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
        bud_time=bud_time_str(),
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bud_acct_mandate_ledger_path) == doc_str


def test_create_planpoint_path_HasDocString():
    # ESTABLISH
    doc_str = create_planpoint_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
        bud_time=bud_time_str(),
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_planpoint_path) == doc_str


def test_create_owner_event_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_owner_event_dir_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_owner_event_dir_path) == doc_str


def test_create_planevent_path_HasDocString():
    # ESTABLISH
    doc_str = create_planevent_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_planevent_path) == doc_str


def test_create_event_all_pack_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_all_pack_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_all_pack_path) == doc_str


def test_create_event_expressed_pack_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_expressed_pack_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_expressed_pack_path) == doc_str


def test_create_gut_path_HasDocString():
    # ESTABLISH
    doc_str = create_gut_path(
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
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
        bank_mstr_dir="bank_mstr_dir",
        bank_label=bank_label_str(),
        owner_name=owner_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_job_path) == doc_str
