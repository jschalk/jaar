from src.f00_instrument.file import create_path, save_file, open_file
from src.f01_road.jaar_config import (
    get_gifts_folder,
    get_rootpart_of_keep_dir,
    get_fisc_title_if_None,
    get_owners_folder,
)
from src.f02_bud.bud import budunit_shop
from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_fisc_owner_time_csv_path,
    create_fisc_owner_time_json_path,
    fisc_agenda_list_report_path,
    create_owners_dir_path,
    create_episodes_dir_path,
    create_timepoint_dir_path,
    create_budpoint_json_path,
    create_events_owner_json_path,
    create_deal_path,
    create_events_owner_dir_path,
    create_voice_path,
    create_forecast_path,
)
from src.f05_listen.hub_tool import (
    save_bud_file,
    open_bud_file,
    get_timepoint_credit_ledger,
    get_events_owner_credit_ledger,
)
from src.f05_listen.examples.example_listen_buds import get_budunit_3_acct
from src.f05_listen.examples.listen_env import (
    get_listen_temp_env_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_save_bud_file_SetsFile(env_dir_setup_cleanup):
    # ESTABLISH
    temp_dir = get_listen_temp_env_dir()
    bud_filename = "bud.json"
    bud_path = create_path(temp_dir, bud_filename)
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    assert os_path_exists(bud_path) is False

    # WHEN
    save_bud_file(bud_path, None, sue_bud)

    # THEN
    assert os_path_exists(bud_path)


def test_open_bud_file_ReturnsObj_Scenario0_NoFile():
    # ESTABLISH
    temp_dir = get_listen_temp_env_dir()
    bud_filename = "bud.json"
    bud_path = create_path(temp_dir, bud_filename)
    assert os_path_exists(bud_path) is False

    # WHEN
    gen_sue_bud = open_bud_file(bud_path)

    # THEN
    assert not gen_sue_bud


def test_open_bud_file_ReturnsObj_Scenario1_FileExists():
    # ESTABLISH
    temp_dir = get_listen_temp_env_dir()
    bud_filename = "bud.json"
    bud_path = create_path(temp_dir, bud_filename)
    sue_str = "Sue"
    expected_sue_bud = budunit_shop(sue_str)
    save_bud_file(bud_path, None, expected_sue_bud)
    assert os_path_exists(bud_path)

    # WHEN
    gen_sue_bud = open_bud_file(bud_path)

    # THEN
    assert gen_sue_bud == expected_sue_bud


def test_get_timepoint_credit_ledger_ReturnsObj_Scenario0_NoFile(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord"
    sue_str = "Sue"
    t3 = 3

    # WHEN
    gen_a3_credit_ledger = get_timepoint_credit_ledger(
        fisc_mstr_dir, a23_str, sue_str, t3
    )

    # THEN
    assert gen_a3_credit_ledger == {}


def test_get_timepoint_credit_ledger_ReturnsObj_Scenario1_FileExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord"
    sue_str = "Sue"
    t3 = 3
    t3_json_path = create_budpoint_json_path(fisc_mstr_dir, a23_str, sue_str, t3)
    a3_bud = get_budunit_3_acct()
    save_bud_file(t3_json_path, None, a3_bud)

    # WHEN
    gen_a3_credit_ledger = get_timepoint_credit_ledger(
        fisc_mstr_dir, a23_str, sue_str, t3
    )

    # THEN
    expected_a3_credit_ledger = {sue_str: 5, "Yao": 2, "Zia": 33}
    assert gen_a3_credit_ledger == expected_a3_credit_ledger


def test_get_events_owner_credit_ledger_ReturnsObj_Scenario0_NoFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord"
    sue_str = "Sue"
    t3 = 3

    # WHEN
    gen_a3_credit_ledger = get_events_owner_credit_ledger(
        fisc_mstr_dir, a23_str, sue_str, t3
    )

    # THEN
    assert gen_a3_credit_ledger == {}


def test_get_events_owner_credit_ledger_ReturnsObj_Scenario1_FileExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord"
    sue_str = "Sue"
    t3 = 3
    t3_json_path = create_events_owner_json_path(fisc_mstr_dir, a23_str, sue_str, t3)
    a3_bud = get_budunit_3_acct()
    save_bud_file(t3_json_path, None, a3_bud)

    # WHEN
    gen_a3_credit_ledger = get_events_owner_credit_ledger(
        fisc_mstr_dir, a23_str, sue_str, t3
    )

    # THEN
    expected_a3_credit_ledger = {sue_str: 5, "Yao": 2, "Zia": 33}
    assert gen_a3_credit_ledger == expected_a3_credit_ledger
