from src.f00_instrument.file import create_path, set_dir, save_file, open_file
from src.f01_road.jaar_config import (
    get_gifts_folder,
    get_rootpart_of_keep_dir,
    get_fisc_title_if_None,
    get_owners_folder,
)
from src.f02_bud.bud import budunit_shop
from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_fisc_ote1_csv_path,
    create_fisc_ote1_json_path,
    fisc_agenda_list_report_path,
    create_owners_dir_path,
    create_episodes_dir_path,
    create_timepoint_dir_path,
    create_budpoint_path,
    create_owner_event_dir_path,
    create_budevent_path,
    create_deal_path,
    create_voice_path,
    create_forecast_path,
)
from src.f05_listen.hub_tool import (
    save_bud_file,
    open_bud_file,
    get_timepoint_credit_ledger,
    get_events_owner_credit_ledger,
    get_owners_downhill_event_ints,
    collect_events_dir_owner_events_sets,
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
    t3_json_path = create_budpoint_path(fisc_mstr_dir, a23_str, sue_str, t3)
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
    t3_json_path = create_budevent_path(fisc_mstr_dir, a23_str, sue_str, t3)
    a3_bud = get_budunit_3_acct()
    save_bud_file(t3_json_path, None, a3_bud)

    # WHEN
    gen_a3_credit_ledger = get_events_owner_credit_ledger(
        fisc_mstr_dir, a23_str, sue_str, t3
    )

    # THEN
    expected_a3_credit_ledger = {sue_str: 5, "Yao": 2, "Zia": 33}
    assert gen_a3_credit_ledger == expected_a3_credit_ledger


def test_collect_events_dir_owner_events_sets_ReturnsObj_Scenario0_none(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    # WHEN
    owner_events_sets = collect_events_dir_owner_events_sets(fisc_mstr_dir, a23_str)
    # THEN
    assert owner_events_sets == {}


def test_collect_events_dir_owner_events_sets_ReturnsObj_Scenario1_DirsExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    bob_str = "Bob"
    event1 = 1
    event2 = 2
    bob1_dir = create_owner_event_dir_path(fisc_mstr_dir, a23_str, bob_str, event1)
    bob2_dir = create_owner_event_dir_path(fisc_mstr_dir, a23_str, bob_str, event2)
    print(f"  {bob1_dir=}")
    print(f"  {bob2_dir=}")
    set_dir(bob1_dir)
    set_dir(bob2_dir)

    # WHEN
    owner_events_sets = collect_events_dir_owner_events_sets(fisc_mstr_dir, a23_str)

    # THEN
    assert owner_events_sets == {bob_str: {event1, event2}}


def test_collect_events_dir_owner_events_sets_ReturnsObj_Scenario2_DirsExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    bob_str = "Bob"
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    event7 = 7
    bob1_dir = create_owner_event_dir_path(fisc_mstr_dir, a23_str, bob_str, event1)
    bob2_dir = create_owner_event_dir_path(fisc_mstr_dir, a23_str, bob_str, event2)
    sue2_dir = create_owner_event_dir_path(fisc_mstr_dir, a23_str, sue_str, event2)
    sue7_dir = create_owner_event_dir_path(fisc_mstr_dir, a23_str, sue_str, event7)
    set_dir(bob1_dir)
    set_dir(bob2_dir)
    set_dir(sue2_dir)
    set_dir(sue7_dir)

    # WHEN
    owner_events_sets = collect_events_dir_owner_events_sets(fisc_mstr_dir, a23_str)

    # THEN
    assert owner_events_sets == {bob_str: {event1, event2}, sue_str: {event2, event7}}


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event2 = 2
    owner_events_sets = {}
    downhill_event_int = event2
    downhill_owners = {bob_str, sue_str}

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(
        owner_events_sets, downhill_owners, downhill_event_int
    )

    # THEN
    assert owners_downhill_event_ints == {}


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario1_simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    event7 = 7
    owner_events_sets = {bob_str: {event1, event2}, sue_str: {event2, event7}}
    downhill_event_int = event2
    downhill_owners = {bob_str, sue_str}

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(
        owner_events_sets, downhill_owners, downhill_event_int
    )

    # THEN
    assert owners_downhill_event_ints == {bob_str: event2, sue_str: event2}


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario2Empty_downhill_event_int():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    owner_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event1, event2, event7},
    }
    downhill_owners = {bob_str, sue_str}

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(
        owner_events_sets, downhill_owners
    )

    # THEN
    assert owners_downhill_event_ints == {bob_str: event2, sue_str: event7}


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario3Empty_downhill_owners():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    owner_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event1, event2, event7},
    }

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(owner_events_sets)

    # THEN
    assert owners_downhill_event_ints == {
        bob_str: event2,
        sue_str: event7,
        yao_str: event7,
    }


def test_get_owners_downhill_event_ints_ReturnsObj_Scenario4Empty_downhill_owners_Withdownhill_event_int():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    event1 = 1
    event2 = 2
    event7 = 7
    owner_events_sets = {
        bob_str: {event1, event2},
        sue_str: {event2, event7},
        yao_str: {event7},
    }
    downhill_event_int = 2

    # WHEN
    owners_downhill_event_ints = get_owners_downhill_event_ints(
        owner_events_sets, ref_event_int=downhill_event_int
    )

    # THEN
    assert owners_downhill_event_ints == {bob_str: event2, sue_str: event2}
