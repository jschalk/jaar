from src.a00_data_toolboxs.file_toolbox import create_path
from src.a12_hub_tools.hub_path import (
    FISC_FILENAME,
    FISC_OTE1_AGG_CSV_FILENAME,
    FISC_OTE1_AGG_JSON_FILENAME,
    FISC_AGENDA_FULL_LISTING_FILENAME,
    DEALUNIT_FILENAME,
    DEAL_MANDATE_FILENAME,
    CELLNODE_FILENAME,
    CELL_MANDATE_FILENAME,
    BUDPOINT_FILENAME,
    BUDEVENT_FILENAME,
    EVENT_ALL_PACK_FILENAME,
    EVENT_EXPRESSED_PACK_FILENAME,
    gut_str,
    plan_str,
    treasury_filename,
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
    create_plan_path,
)
from src.a13_bud_listen_logic.examples.listen_env import get_listen_temp_env_dir


def test_gut_str():
    assert gut_str() == "gut"


def test_plan_str():
    assert plan_str() == "plan"


def test_treasury_filename_ReturnsObj():
    assert treasury_filename() == "treasury.db"


def test_create_fisc_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"

    # WHEN
    gen_a23_dir_path = create_fisc_dir_path(x_fisc_mstr_dir, a23_str)

    # THEN
    fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    expected_a23_path = create_path(fiscs_dir, a23_str)
    assert gen_a23_dir_path == expected_a23_path


def test_create_fisc_json_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"

    # WHEN
    gen_a23_json_path = create_fisc_json_path(x_fisc_mstr_dir, a23_str)

    # THEN
    fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    a23_path = create_path(fiscs_dir, a23_str)
    expected_a23_json_path = create_path(a23_path, FISC_FILENAME)
    assert gen_a23_json_path == expected_a23_json_path


def test_create_fisc_ote1_csv_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"

    # WHEN
    gen_a23_te_csv_path = create_fisc_ote1_csv_path(x_fisc_mstr_dir, a23_str)

    # THEN
    fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    a23_path = create_path(fiscs_dir, a23_str)
    expected_a23_te_path = create_path(a23_path, FISC_OTE1_AGG_CSV_FILENAME)
    assert gen_a23_te_csv_path == expected_a23_te_path


def test_create_fisc_ote1_json_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"

    # WHEN
    gen_a23_te_csv_path = create_fisc_ote1_json_path(x_fisc_mstr_dir, a23_str)

    # THEN
    fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    a23_path = create_path(fiscs_dir, a23_str)
    expected_a23_te_path = create_path(a23_path, FISC_OTE1_AGG_JSON_FILENAME)
    assert gen_a23_te_csv_path == expected_a23_te_path


def test_fisc_agenda_list_report_path_ReturnObj():
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"

    # WHEN
    gen_a23_full_report_path = fisc_agenda_list_report_path(fisc_mstr_dir, a23_str)

    # THEN
    fiscs_dir = create_path(fisc_mstr_dir, "fiscs")
    a23_path = create_path(fiscs_dir, a23_str)
    expected_a23_agenda_full_path = create_path(
        a23_path, FISC_AGENDA_FULL_LISTING_FILENAME
    )
    assert gen_a23_full_report_path == expected_a23_agenda_full_path


def test_create_fisc_owners_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    accord23_str = "accord23"

    # WHEN
    gen_owners_dir = create_fisc_owners_dir_path(x_fisc_mstr_dir, accord23_str)

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    accord23_dir = create_path(x_fiscs_dir, accord23_str)
    expected_owners_dir = create_path(accord23_dir, "owners")
    assert gen_owners_dir == expected_owners_dir


def test_create_owner_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    accord23_str = "accord23"
    sue_str = "Sue"

    # WHEN
    sue_dir = create_owner_dir_path(x_fisc_mstr_dir, accord23_str, sue_str)

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    accord23_dir = create_path(x_fiscs_dir, accord23_str)
    owners_dir = create_path(accord23_dir, "owners")
    expected_sue_dir = create_path(owners_dir, sue_str)
    assert sue_dir == expected_sue_dir


def test_create_keeps_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    accord23_str = "accord23"
    sue_str = "Sue"

    # WHEN
    keeps_dir = create_keeps_dir_path(x_fisc_mstr_dir, accord23_str, sue_str)

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    accord23_dir = create_path(x_fiscs_dir, accord23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    expected_keeps_dir = create_path(sue_dir, "keeps")
    assert keeps_dir == expected_keeps_dir


def test_create_atoms_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    accord23_str = "accord23"
    sue_str = "Sue"

    # WHEN
    atoms_dir = create_atoms_dir_path(x_fisc_mstr_dir, accord23_str, sue_str)

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    accord23_dir = create_path(x_fiscs_dir, accord23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    expected_atoms_dir = create_path(sue_dir, "atoms")
    assert atoms_dir == expected_atoms_dir


def test_create_packs_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    accord23_str = "accord23"
    sue_str = "Sue"

    # WHEN
    packs_dir = create_packs_dir_path(x_fisc_mstr_dir, accord23_str, sue_str)

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    accord23_dir = create_path(x_fiscs_dir, accord23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    expected_packs_dir = create_path(sue_dir, "packs")
    assert packs_dir == expected_packs_dir


def test_create_deals_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    accord23_str = "accord23"
    sue_str = "Sue"

    # WHEN
    deals_dir = create_deals_dir_path(x_fisc_mstr_dir, accord23_str, sue_str)

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    accord23_dir = create_path(x_fiscs_dir, accord23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    expected_deals_dir = create_path(sue_dir, "deals")
    assert deals_dir == expected_deals_dir


def test_create_deal_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    accord23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    generated_timepoint_dir = create_deal_dir_path(
        x_fisc_mstr_dir, accord23_str, sue_str, timepoint7
    )

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    accord23_dir = create_path(x_fiscs_dir, accord23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    deals_dir = create_path(sue_dir, "deals")
    expected_timepoint_dir = create_path(deals_dir, timepoint7)
    assert generated_timepoint_dir == expected_timepoint_dir


def test_create_dealunit_json_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_deal_path = create_dealunit_json_path(
        x_fisc_mstr_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    accord23_dir = create_path(x_fiscs_dir, a23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    deals_dir = create_path(sue_dir, "deals")
    timepoint_dir = create_path(deals_dir, timepoint7)
    expected_deal_path_dir = create_path(timepoint_dir, DEALUNIT_FILENAME)
    assert gen_deal_path == expected_deal_path_dir


def test_create_deal_acct_mandate_ledger_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_deal_path = create_deal_acct_mandate_ledger_path(
        x_fisc_mstr_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    accord23_dir = create_path(x_fiscs_dir, a23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    deals_dir = create_path(sue_dir, "deals")
    timepoint_dir = create_path(deals_dir, timepoint7)
    expected_deal_path_dir = create_path(timepoint_dir, DEAL_MANDATE_FILENAME)
    assert gen_deal_path == expected_deal_path_dir


def test_create_budpoint_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_budpoint_path = create_budpoint_path(
        x_fisc_mstr_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    accord23_dir = create_path(x_fiscs_dir, a23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    deals_dir = create_path(sue_dir, "deals")
    timepoint_dir = create_path(deals_dir, timepoint7)
    expected_budpoint_path_dir = create_path(timepoint_dir, BUDPOINT_FILENAME)
    assert gen_budpoint_path == expected_budpoint_path_dir


def test_create_cell_dir_path_ReturnObj_Scenario0_No_deal_ancestors():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    tp7 = 7

    # WHEN
    gen_cell_dir = create_cell_dir_path(x_fisc_mstr_dir, a23_str, sue_str, tp7, [])

    # THEN
    timepoint_dir = create_deal_dir_path(x_fisc_mstr_dir, a23_str, sue_str, tp7)
    assert gen_cell_dir == timepoint_dir


def test_create_cell_dir_path_ReturnObj_Scenario1_One_deal_ancestors():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    x_deal_ancestors = [yao_str]

    # WHEN
    gen_cell_dir = create_cell_dir_path(
        x_fisc_mstr_dir, a23_str, sue_str, tp7, deal_ancestors=x_deal_ancestors
    )

    # THEN
    timepoint_dir = create_deal_dir_path(x_fisc_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(timepoint_dir, yao_str)
    assert gen_cell_dir == tp_yao_dir


def test_create_cell_dir_path_ReturnObj_Scenario2_Three_deal_ancestors():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    bob_str = "Bob"
    zia_str = "Zia"
    x_deal_ancestors = [yao_str, bob_str, zia_str]

    # WHEN
    gen_deal_celldepth_dir_path = create_cell_dir_path(
        x_fisc_mstr_dir, a23_str, sue_str, tp7, deal_ancestors=x_deal_ancestors
    )

    # THEN
    timepoint_dir = create_deal_dir_path(x_fisc_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(timepoint_dir, yao_str)
    tp_yao_bob_dir = create_path(tp_yao_dir, bob_str)
    expected_tp_yao_bob_zia_dir = create_path(tp_yao_bob_dir, zia_str)
    assert gen_deal_celldepth_dir_path == expected_tp_yao_bob_zia_dir


def test_create_cell_json_path_ReturnObj_Scenario0_Empty_deal_ancestors():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_cell_json_path = create_cell_json_path(
        x_fisc_mstr_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    accord23_dir = create_path(x_fiscs_dir, a23_str)
    owners_dir = create_path(accord23_dir, "owners")
    sue_dir = create_path(owners_dir, sue_str)
    deals_dir = create_path(sue_dir, "deals")
    timepoint_dir = create_path(deals_dir, timepoint7)
    expected_cell_json_path = create_path(timepoint_dir, CELLNODE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_cell_json_path_ReturnObj_Scenario1_Three_deal_ancestors():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    bob_str = "Bob"
    deal_ancestors = [yao_str, bob_str]

    # WHEN
    gen_cell_json_path = create_cell_json_path(
        x_fisc_mstr_dir, a23_str, sue_str, tp7, deal_ancestors=deal_ancestors
    )

    # THEN
    timepoint_dir = create_deal_dir_path(x_fisc_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(timepoint_dir, yao_str)
    tp_yao_bob_dir = create_path(tp_yao_dir, bob_str)
    expected_cell_json_path = create_path(tp_yao_bob_dir, CELLNODE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_cell_acct_mandate_ledger_path_ReturnObj_Scenario1_Three_deal_ancestors():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    tp7 = 7
    yao_str = "Yao"
    bob_str = "Bob"
    deal_ancestors = [yao_str, bob_str]

    # WHEN
    gen_cell_json_path = create_cell_acct_mandate_ledger_path(
        x_fisc_mstr_dir, a23_str, sue_str, tp7, deal_ancestors=deal_ancestors
    )

    # THEN
    timepoint_dir = create_deal_dir_path(x_fisc_mstr_dir, a23_str, sue_str, tp7)
    tp_yao_dir = create_path(timepoint_dir, yao_str)
    tp_yao_bob_dir = create_path(tp_yao_dir, bob_str)
    expected_cell_json_path = create_path(tp_yao_bob_dir, CELL_MANDATE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_owner_event_dir_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    accord23_str = "accord23"
    bob_str = "Bob"
    event3 = 3

    # WHEN
    gen_a23_e3_dir_path = create_owner_event_dir_path(
        x_fisc_mstr_dir, accord23_str, bob_str, event3
    )

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    a23_dir = create_path(x_fiscs_dir, accord23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_events_dir = create_path(a23_bob_dir, "events")
    expected_a23_bob_e3_dir = create_path(a23_events_dir, event3)
    assert gen_a23_e3_dir_path == expected_a23_bob_e3_dir


def test_create_budevent_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    accord23_str = "accord23"
    bob_str = "Bob"
    event3 = 3

    # WHEN
    gen_a23_e3_bud_path = create_budevent_path(
        x_fisc_mstr_dir, accord23_str, bob_str, event3
    )

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    a23_dir = create_path(x_fiscs_dir, accord23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_events_dir = create_path(a23_bob_dir, "events")
    a23_bob_e3_dir = create_path(a23_events_dir, event3)
    expected_a23_bob_e3_bud_path = create_path(a23_bob_e3_dir, BUDEVENT_FILENAME)
    assert gen_a23_e3_bud_path == expected_a23_bob_e3_bud_path


def test_create_event_all_pack_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    accord23_str = "accord23"
    bob_str = "Bob"
    event3 = 3

    # WHEN
    gen_a23_e3_bud_path = create_event_all_pack_path(
        x_fisc_mstr_dir, accord23_str, bob_str, event3
    )

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    a23_dir = create_path(x_fiscs_dir, accord23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_events_dir = create_path(a23_bob_dir, "events")
    a23_bob_e3_dir = create_path(a23_events_dir, event3)
    expected_a23_bob_e3_all_pack_path = create_path(
        a23_bob_e3_dir, EVENT_ALL_PACK_FILENAME
    )
    assert gen_a23_e3_bud_path == expected_a23_bob_e3_all_pack_path


def test_create_event_expressed_pack_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    accord23_str = "accord23"
    bob_str = "Bob"
    event3 = 3

    # WHEN
    gen_a23_e3_bud_path = create_event_expressed_pack_path(
        x_fisc_mstr_dir, accord23_str, bob_str, event3
    )

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    a23_dir = create_path(x_fiscs_dir, accord23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_events_dir = create_path(a23_bob_dir, "events")
    a23_bob_e3_dir = create_path(a23_events_dir, event3)
    expected_a23_bob_e3_expressed_pack_path = create_path(
        a23_bob_e3_dir, EVENT_EXPRESSED_PACK_FILENAME
    )
    assert gen_a23_e3_bud_path == expected_a23_bob_e3_expressed_pack_path


def test_create_gut_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    bob_str = "Bob"

    # WHEN
    gen_a23_e3_bud_path = create_gut_path(x_fisc_mstr_dir, a23_str, bob_str)

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    a23_dir = create_path(x_fiscs_dir, a23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_bob_gut_dir = create_path(a23_bob_dir, "gut")
    expected_a23_bob_gut_json_path = create_path(a23_bob_gut_dir, f"{bob_str}.json")
    # bud_filename = "bud.json"
    # expected_a23_e3_bud_path = create_path(a23_bob_e3_dir, bud_filename)
    assert gen_a23_e3_bud_path == expected_a23_bob_gut_json_path


def test_create_plan_path_ReturnObj():
    # ESTABLISH
    x_fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    bob_str = "Bob"

    # WHEN
    gen_a23_e3_bud_path = create_plan_path(x_fisc_mstr_dir, a23_str, bob_str)

    # THEN
    x_fiscs_dir = create_path(x_fisc_mstr_dir, "fiscs")
    a23_dir = create_path(x_fiscs_dir, a23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_bob_plan_dir = create_path(a23_bob_dir, "plan")
    expected_a23_bob_plan_json_path = create_path(a23_bob_plan_dir, f"{bob_str}.json")
    # bud_filename = "bud.json"
    # expected_a23_e3_bud_path = create_path(a23_bob_e3_dir, bud_filename)
    assert gen_a23_e3_bud_path == expected_a23_bob_plan_json_path
