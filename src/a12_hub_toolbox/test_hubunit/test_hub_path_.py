from src.a00_data_toolbox.file_toolbox import create_path
from src.a12_hub_toolbox._util.a12_env import get_module_temp_dir
from src.a12_hub_toolbox._util.a12_str import gut_str, job_str
from src.a12_hub_toolbox.hub_path import (
    BUD_MANDATE_FILENAME,
    BUDUNIT_FILENAME,
    CELL_MANDATE_FILENAME,
    CELLNODE_FILENAME,
    EVENT_ALL_PACK_FILENAME,
    EVENT_EXPRESSED_PACK_FILENAME,
    PLANEVENT_FILENAME,
    PLANPOINT_FILENAME,
    VOW_AGENDA_FULL_LISTING_FILENAME,
    VOW_FILENAME,
    VOW_OTE1_AGG_CSV_FILENAME,
    VOW_OTE1_AGG_JSON_FILENAME,
    create_atoms_dir_path,
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
    create_vow_dir_path,
    create_vow_json_path,
    create_vow_ote1_csv_path,
    create_vow_ote1_json_path,
    create_vow_owners_dir_path,
    treasury_filename,
    vow_agenda_list_report_path,
)


def test_treasury_filename_ReturnsObj():
    assert treasury_filename() == "treasury.db"


def test_create_vow_dir_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"

    # WHEN
    gen_a23_dir_path = create_vow_dir_path(x_vow_mstr_dir, a23_str)

    # THEN
    vows_dir = create_path(x_vow_mstr_dir, "vows")
    expected_a23_path = create_path(vows_dir, a23_str)
    assert gen_a23_dir_path == expected_a23_path


def test_create_vow_json_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"

    # WHEN
    gen_a23_json_path = create_vow_json_path(x_vow_mstr_dir, a23_str)

    # THEN
    vows_dir = create_path(x_vow_mstr_dir, "vows")
    a23_path = create_path(vows_dir, a23_str)
    expected_a23_json_path = create_path(a23_path, VOW_FILENAME)
    assert gen_a23_json_path == expected_a23_json_path


def test_create_vow_ote1_csv_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"

    # WHEN
    gen_a23_te_csv_path = create_vow_ote1_csv_path(x_vow_mstr_dir, a23_str)

    # THEN
    vows_dir = create_path(x_vow_mstr_dir, "vows")
    a23_path = create_path(vows_dir, a23_str)
    expected_a23_te_path = create_path(a23_path, VOW_OTE1_AGG_CSV_FILENAME)
    assert gen_a23_te_csv_path == expected_a23_te_path


def test_create_vow_ote1_json_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"

    # WHEN
    gen_a23_te_csv_path = create_vow_ote1_json_path(x_vow_mstr_dir, a23_str)

    # THEN
    vows_dir = create_path(x_vow_mstr_dir, "vows")
    a23_path = create_path(vows_dir, a23_str)
    expected_a23_te_path = create_path(a23_path, VOW_OTE1_AGG_JSON_FILENAME)
    assert gen_a23_te_csv_path == expected_a23_te_path


def test_vow_agenda_list_report_path_ReturnsObj():
    # ESTABLISH
    vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"

    # WHEN
    gen_a23_full_report_path = vow_agenda_list_report_path(vow_mstr_dir, a23_str)

    # THEN
    vows_dir = create_path(vow_mstr_dir, "vows")
    a23_path = create_path(vows_dir, a23_str)
    expected_a23_agenda_full_path = create_path(
        a23_path, VOW_AGENDA_FULL_LISTING_FILENAME
    )
    assert gen_a23_full_report_path == expected_a23_agenda_full_path


def test_create_vow_owners_dir_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    accord23_str = "accord23"

    # WHEN
    gen_owners_dir = create_vow_owners_dir_path(x_vow_mstr_dir, accord23_str)

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    accord23_dir = create_path(x_vows_dir, accord23_str)
    expected_owners_dir = create_path(accord23_dir, "owners")
    assert gen_owners_dir == expected_owners_dir


def test_create_owner_dir_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    accord23_str = "accord23"
    sue_str = "Sue"

    # WHEN
    sue_dir = create_owner_dir_path(x_vow_mstr_dir, accord23_str, sue_str)

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    accord23_dir = create_path(x_vows_dir, accord23_str)
    owners_dir = create_path(accord23_dir, "owners")
    expected_sue_dir = create_path(owners_dir, sue_str)
    assert sue_dir == expected_sue_dir


def test_create_keeps_dir_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    accord23_str = "accord23"
    sue_str = "Sue"

    # WHEN
    keeps_dir = create_keeps_dir_path(x_vow_mstr_dir, accord23_str, sue_str)

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    accord23_dir = create_path(x_vows_dir, accord23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    expected_keeps_dir = create_path(sue_dir, "keeps")
    assert keeps_dir == expected_keeps_dir


def test_create_atoms_dir_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    accord23_str = "accord23"
    sue_str = "Sue"

    # WHEN
    atoms_dir = create_atoms_dir_path(x_vow_mstr_dir, accord23_str, sue_str)

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    accord23_dir = create_path(x_vows_dir, accord23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    expected_atoms_dir = create_path(sue_dir, "atoms")
    assert atoms_dir == expected_atoms_dir


def test_create_packs_dir_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    accord23_str = "accord23"
    sue_str = "Sue"

    # WHEN
    packs_dir = create_packs_dir_path(x_vow_mstr_dir, accord23_str, sue_str)

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    accord23_dir = create_path(x_vows_dir, accord23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    expected_packs_dir = create_path(sue_dir, "packs")
    assert packs_dir == expected_packs_dir


def test_create_buds_dir_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    accord23_str = "accord23"
    sue_str = "Sue"

    # WHEN
    buds_dir = create_buds_dir_path(x_vow_mstr_dir, accord23_str, sue_str)

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    accord23_dir = create_path(x_vows_dir, accord23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    expected_buds_dir = create_path(sue_dir, "buds")
    assert buds_dir == expected_buds_dir


def test_create_bud_dir_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    accord23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    generated_timepoint_dir = create_bud_dir_path(
        x_vow_mstr_dir, accord23_str, sue_str, timepoint7
    )

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    accord23_dir = create_path(x_vows_dir, accord23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    expected_timepoint_dir = create_path(buds_dir, timepoint7)
    assert generated_timepoint_dir == expected_timepoint_dir


def test_create_budunit_json_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_bud_path = create_budunit_json_path(
        x_vow_mstr_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    accord23_dir = create_path(x_vows_dir, a23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    timepoint_dir = create_path(buds_dir, timepoint7)
    expected_bud_path_dir = create_path(timepoint_dir, BUDUNIT_FILENAME)
    assert gen_bud_path == expected_bud_path_dir


def test_create_bud_acct_mandate_ledger_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_bud_path = create_bud_acct_mandate_ledger_path(
        x_vow_mstr_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    accord23_dir = create_path(x_vows_dir, a23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    timepoint_dir = create_path(buds_dir, timepoint7)
    expected_bud_path_dir = create_path(timepoint_dir, BUD_MANDATE_FILENAME)
    assert gen_bud_path == expected_bud_path_dir


def test_create_planpoint_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_planpoint_path = create_planpoint_path(
        x_vow_mstr_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    accord23_dir = create_path(x_vows_dir, a23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    timepoint_dir = create_path(buds_dir, timepoint7)
    expected_planpoint_path_dir = create_path(timepoint_dir, PLANPOINT_FILENAME)
    assert gen_planpoint_path == expected_planpoint_path_dir


def test_create_cell_dir_path_ReturnsObj_Scenario0_No_bud_ancestors():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    tp7 = 7

    # WHEN
    gen_cell_dir = create_cell_dir_path(x_vow_mstr_dir, a23_str, sue_str, tp7, [])

    # THEN
    timepoint_dir = create_bud_dir_path(x_vow_mstr_dir, a23_str, sue_str, tp7)
    assert gen_cell_dir == timepoint_dir


def test_create_cell_dir_path_ReturnsObj_Scenario1_One_bud_ancestors():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    x_bud_ancestors = [yao_str]

    # WHEN
    gen_cell_dir = create_cell_dir_path(
        x_vow_mstr_dir, a23_str, sue_str, tp7, bud_ancestors=x_bud_ancestors
    )

    # THEN
    timepoint_dir = create_bud_dir_path(x_vow_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(timepoint_dir, yao_str)
    assert gen_cell_dir == tp_yao_dir


def test_create_cell_dir_path_ReturnsObj_Scenario2_Three_bud_ancestors():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    x_bud_ancestors = [yao_str, bob_str, zia_str]

    # WHEN
    gen_bud_celldepth_dir_path = create_cell_dir_path(
        x_vow_mstr_dir, a23_str, sue_str, tp7, bud_ancestors=x_bud_ancestors
    )

    # THEN
    timepoint_dir = create_bud_dir_path(x_vow_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(timepoint_dir, yao_str)
    tp_yao_bob_dir = create_path(tp_yao_dir, bob_str)
    expected_tp_yao_bob_zia_dir = create_path(tp_yao_bob_dir, zia_str)
    assert gen_bud_celldepth_dir_path == expected_tp_yao_bob_zia_dir


def test_create_cell_json_path_ReturnsObj_Scenario0_Empty_bud_ancestors():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_cell_json_path = create_cell_json_path(
        x_vow_mstr_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    accord23_dir = create_path(x_vows_dir, a23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    buds_dir = create_path(sue_dir, "buds")
    timepoint_dir = create_path(buds_dir, timepoint7)
    expected_cell_json_path = create_path(timepoint_dir, CELLNODE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_cell_json_path_ReturnsObj_Scenario1_Three_bud_ancestors():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    bob_str = "Bob"
    bud_ancestors = [yao_str, bob_str]

    # WHEN
    gen_cell_json_path = create_cell_json_path(
        x_vow_mstr_dir, a23_str, sue_str, tp7, bud_ancestors=bud_ancestors
    )

    # THEN
    timepoint_dir = create_bud_dir_path(x_vow_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(timepoint_dir, yao_str)
    tp_yao_bob_dir = create_path(tp_yao_dir, bob_str)
    expected_cell_json_path = create_path(tp_yao_bob_dir, CELLNODE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_cell_acct_mandate_ledger_path_ReturnsObj_Scenario1_Three_bud_ancestors():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    bob_str = "Bob"
    bud_ancestors = [yao_str, bob_str]

    # WHEN
    gen_cell_json_path = create_cell_acct_mandate_ledger_path(
        x_vow_mstr_dir, a23_str, sue_str, tp7, bud_ancestors=bud_ancestors
    )

    # THEN
    timepoint_dir = create_bud_dir_path(x_vow_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(timepoint_dir, yao_str)
    tp_yao_bob_dir = create_path(tp_yao_dir, bob_str)
    expected_cell_json_path = create_path(tp_yao_bob_dir, CELL_MANDATE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_owner_event_dir_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    accord23_str = "accord23"
    bob_str = "Bob"
    event3 = 3

    # WHEN
    gen_a23_e3_dir_path = create_owner_event_dir_path(
        x_vow_mstr_dir, accord23_str, bob_str, event3
    )

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    a23_dir = create_path(x_vows_dir, accord23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_events_dir = create_path(a23_bob_dir, "events")
    expected_a23_bob_e3_dir = create_path(a23_events_dir, event3)
    assert gen_a23_e3_dir_path == expected_a23_bob_e3_dir


def test_create_planevent_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    accord23_str = "accord23"
    bob_str = "Bob"
    event3 = 3

    # WHEN
    gen_a23_e3_plan_path = create_planevent_path(
        x_vow_mstr_dir, accord23_str, bob_str, event3
    )

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    a23_dir = create_path(x_vows_dir, accord23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_events_dir = create_path(a23_bob_dir, "events")
    a23_bob_e3_dir = create_path(a23_events_dir, event3)
    expected_a23_bob_e3_plan_path = create_path(a23_bob_e3_dir, PLANEVENT_FILENAME)
    assert gen_a23_e3_plan_path == expected_a23_bob_e3_plan_path


def test_create_event_all_pack_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    accord23_str = "accord23"
    bob_str = "Bob"
    event3 = 3

    # WHEN
    gen_a23_e3_plan_path = create_event_all_pack_path(
        x_vow_mstr_dir, accord23_str, bob_str, event3
    )

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    a23_dir = create_path(x_vows_dir, accord23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_events_dir = create_path(a23_bob_dir, "events")
    a23_bob_e3_dir = create_path(a23_events_dir, event3)
    expected_a23_bob_e3_all_pack_path = create_path(
        a23_bob_e3_dir, EVENT_ALL_PACK_FILENAME
    )
    assert gen_a23_e3_plan_path == expected_a23_bob_e3_all_pack_path


def test_create_event_expressed_pack_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    accord23_str = "accord23"
    bob_str = "Bob"
    event3 = 3

    # WHEN
    gen_a23_e3_plan_path = create_event_expressed_pack_path(
        x_vow_mstr_dir, accord23_str, bob_str, event3
    )

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    a23_dir = create_path(x_vows_dir, accord23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_events_dir = create_path(a23_bob_dir, "events")
    a23_bob_e3_dir = create_path(a23_events_dir, event3)
    expected_a23_bob_e3_expressed_pack_path = create_path(
        a23_bob_e3_dir, EVENT_EXPRESSED_PACK_FILENAME
    )
    assert gen_a23_e3_plan_path == expected_a23_bob_e3_expressed_pack_path


def test_create_gut_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    bob_str = "Bob"

    # WHEN
    gen_a23_e3_plan_path = create_gut_path(x_vow_mstr_dir, a23_str, bob_str)

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    a23_dir = create_path(x_vows_dir, a23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_bob_gut_dir = create_path(a23_bob_dir, gut_str())
    expected_a23_bob_gut_json_path = create_path(a23_bob_gut_dir, f"{bob_str}.json")
    # plan_filename = "plan.json"
    # expected_a23_e3_plan_path = create_path(a23_bob_e3_dir, plan_filename)
    assert gen_a23_e3_plan_path == expected_a23_bob_gut_json_path


def test_create_job_path_ReturnsObj():
    # ESTABLISH
    x_vow_mstr_dir = get_module_temp_dir()
    a23_str = "accord23"
    bob_str = "Bob"

    # WHEN
    gen_a23_e3_plan_path = create_job_path(x_vow_mstr_dir, a23_str, bob_str)

    # THEN
    x_vows_dir = create_path(x_vow_mstr_dir, "vows")
    a23_dir = create_path(x_vows_dir, a23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_bob_job_dir = create_path(a23_bob_dir, job_str())
    expected_a23_bob_job_json_path = create_path(a23_bob_job_dir, f"{bob_str}.json")
    # plan_filename = "plan.json"
    # expected_a23_e3_plan_path = create_path(a23_bob_e3_dir, plan_filename)
    assert gen_a23_e3_plan_path == expected_a23_bob_job_json_path
