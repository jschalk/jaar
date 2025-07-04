from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.a09_pack_logic.test._util.a09_str import (
    belief_label_str,
    believer_name_str,
    bud_time_str,
    event_int_str,
)
from src.a12_hub_toolbox.a12_path import (
    create_atoms_dir_path,
    create_belief_believers_dir_path,
    create_belief_dir_path,
    create_belief_json_path,
    create_belief_ote1_csv_path,
    create_belief_ote1_json_path,
    create_believer_dir_path,
    create_believer_event_dir_path,
    create_believerevent_path,
    create_believerpoint_path,
    create_bud_dir_path,
    create_bud_person_mandate_ledger_path,
    create_buds_dir_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_cell_json_path,
    create_cell_person_mandate_ledger_path,
    create_event_all_pack_path,
    create_event_expressed_pack_path,
    create_gut_path,
    create_job_path,
    create_keeps_dir_path,
    create_packs_dir_path,
)

LINUX_OS = platform_system() == "Linux"


def test_create_belief_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_belief_dir_path("belief_mstr_dir", belief_label_str())
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belief_dir_path) == doc_str


def test_create_belief_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_belief_json_path(
        "belief_mstr_dir", belief_label=belief_label_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belief_json_path) == doc_str


def test_create_belief_ote1_csv_path_HasDocString():
    # ESTABLISH
    doc_str = create_belief_ote1_csv_path(
        "belief_mstr_dir", belief_label=belief_label_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belief_ote1_csv_path) == doc_str


def test_create_belief_ote1_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_belief_ote1_json_path(
        "belief_mstr_dir", belief_label=belief_label_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belief_ote1_json_path) == doc_str


def test_create_belief_believers_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_belief_believers_dir_path(
        "belief_mstr_dir", belief_label=belief_label_str()
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_belief_believers_dir_path) == doc_str


def test_create_believer_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_believer_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_believer_dir_path) == doc_str


def test_create_keeps_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_keeps_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_keeps_dir_path) == doc_str


def test_create_atoms_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_atoms_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_atoms_dir_path) == doc_str


def test_create_packs_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_packs_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_packs_dir_path) == doc_str


def test_create_buds_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_buds_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_buds_dir_path) == doc_str


def test_create_bud_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_bud_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bud_dir_path) == doc_str


def test_create_cell_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
        bud_ancestors=["ledger_believer1", "ledger_believer2", "ledger_believer3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_dir_path) == doc_str


def test_create_cell_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_json_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
        bud_ancestors=["ledger_believer1", "ledger_believer2", "ledger_believer3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_json_path) == doc_str


def test_create_cell_person_mandate_ledger_path_HasDocString():
    # ESTABLISH
    doc_str = create_cell_person_mandate_ledger_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
        bud_ancestors=["ledger_believer1", "ledger_believer2", "ledger_believer3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_person_mandate_ledger_path) == doc_str


def test_create_budunit_json_path_HasDocString():
    # ESTABLISH
    doc_str = create_budunit_json_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_budunit_json_path) == doc_str


def test_create_bud_person_mandate_ledger_path_HasDocString():
    # ESTABLISH
    doc_str = create_bud_person_mandate_ledger_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bud_person_mandate_ledger_path) == doc_str


def test_create_believerpoint_path_HasDocString():
    # ESTABLISH
    doc_str = create_believerpoint_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        bud_time=bud_time_str(),
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_believerpoint_path) == doc_str


def test_create_believer_event_dir_path_HasDocString():
    # ESTABLISH
    doc_str = create_believer_event_dir_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_believer_event_dir_path) == doc_str


def test_create_believerevent_path_HasDocString():
    # ESTABLISH
    doc_str = create_believerevent_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_believerevent_path) == doc_str


def test_create_event_all_pack_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_all_pack_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_all_pack_path) == doc_str


def test_create_event_expressed_pack_path_HasDocString():
    # ESTABLISH
    doc_str = create_event_expressed_pack_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
        event_int=event_int_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_event_expressed_pack_path) == doc_str


def test_create_gut_path_HasDocString():
    # ESTABLISH
    doc_str = create_gut_path(
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
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
        belief_mstr_dir="belief_mstr_dir",
        belief_label=belief_label_str(),
        believer_name=believer_name_str(),
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_job_path) == doc_str
