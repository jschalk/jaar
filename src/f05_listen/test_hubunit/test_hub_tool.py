from src.f00_instrument.file import create_path, set_dir, open_json
from src.f01_road.road import create_road
from src.f02_bud.bud import budunit_shop
from src.f04_gift.atom_config import base_str
from src.f05_listen.cell import CELLNODE_QUOTA_DEFAULT, cellunit_shop
from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_fisc_ote1_csv_path,
    create_fisc_ote1_json_path,
    fisc_agenda_list_report_path,
    create_owners_dir_path,
    create_deals_dir_path,
    create_cell_dir_path,
    create_cell_json_path as node_path,
    create_deal_dir_path,
    create_budpoint_path,
    create_owner_event_dir_path,
    create_budevent_path,
    create_dealunit_json_path,
    create_voice_path,
    create_forecast_path,
)
from src.f05_listen.hub_tool import (
    save_bud_file,
    open_bud_file,
    get_timepoint_credit_ledger,
    get_owners_downhill_event_ints,
    collect_owner_event_dir_sets,
    get_budevent_obj,
    cellunit_save_to_dir,
    cellunit_get_from_dir,
    save_arbitrary_budevent,
    cellunit_add_json_file,
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


def test_save_arbitrary_budevent_SetsFile_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    event5 = 5
    sue_str = "Sue"
    budevent_path = create_budevent_path(fisc_mstr_dir, a23_str, sue_str, event5)
    assert os_path_exists(budevent_path) is False

    # WHEN
    save_arbitrary_budevent(fisc_mstr_dir, a23_str, sue_str, event5)

    # THEN
    assert os_path_exists(budevent_path)
    expected_sue_bud = budunit_shop(sue_str, a23_str)
    assert open_bud_file(budevent_path).get_dict() == expected_sue_bud.get_dict()


def test_save_arbitrary_budevent_SetsFile_Scenario1_includes_facts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    event5 = 5
    sue_str = "Sue"
    budevent_path = create_budevent_path(fisc_mstr_dir, a23_str, sue_str, event5)
    casa_road = create_road(a23_str, "casa")
    clean_road = create_road(casa_road, "clean")
    clean_fopen = 11
    clean_fnigh = 16
    x_facts = [(casa_road, clean_road, clean_fopen, clean_fnigh)]
    assert os_path_exists(budevent_path) is False

    # WHEN
    save_arbitrary_budevent(fisc_mstr_dir, a23_str, sue_str, event5, facts=x_facts)

    # THEN
    assert os_path_exists(budevent_path)
    expected_sue_bud = budunit_shop(sue_str, a23_str)
    expected_sue_bud.add_fact(casa_road, clean_road, clean_fopen, clean_fnigh, True)
    gen_sue_bud = open_bud_file(budevent_path)
    assert gen_sue_bud.get_factunits_dict() == expected_sue_bud.get_factunits_dict()
    assert gen_sue_bud.get_dict() == expected_sue_bud.get_dict()


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


def test_get_budevent_obj_ReturnsObj_Scenario0_NoFile(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord"
    sue_str = "Sue"
    t3 = 3

    # WHEN / THEN
    assert get_budevent_obj(fisc_mstr_dir, a23_str, sue_str, t3) is None


def test_get_budevent_obj_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord"
    sue_str = "Sue"
    t3 = 3
    t3_json_path = create_budevent_path(fisc_mstr_dir, a23_str, sue_str, t3)
    sue_bud = budunit_shop(sue_str)
    casa_road = sue_bud.make_l1_road("case")
    clean_road = sue_bud.make_l1_road("clean")
    dirty_road = sue_bud.make_l1_road("dirty")
    sue_bud.add_fact(casa_road, dirty_road, create_missing_items=True)
    save_bud_file(t3_json_path, None, sue_bud)

    # WHEN
    gen_a3_budevent = get_budevent_obj(fisc_mstr_dir, a23_str, sue_str, t3)

    # THEN
    assert gen_a3_budevent == sue_bud


def test_collect_owner_event_dir_sets_ReturnsObj_Scenario0_none(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    # WHEN
    owner_events_sets = collect_owner_event_dir_sets(fisc_mstr_dir, a23_str)
    # THEN
    assert owner_events_sets == {}


def test_collect_owner_event_dir_sets_ReturnsObj_Scenario1_DirsExist(
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
    owner_events_sets = collect_owner_event_dir_sets(fisc_mstr_dir, a23_str)

    # THEN
    assert owner_events_sets == {bob_str: {event1, event2}}


def test_collect_owner_event_dir_sets_ReturnsObj_Scenario2_DirsExist(
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
    owner_events_sets = collect_owner_event_dir_sets(fisc_mstr_dir, a23_str)

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


def test_cellunit_add_json_file_SetsFile_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    sue7_cell_path = node_path(fisc_mstr_dir, a23_str, sue_str, time7)
    event3 = 3
    das = []
    quota500 = 500
    celldepth4 = 4
    penny6 = 6
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_add_json_file(
        fisc_mstr_dir=fisc_mstr_dir,
        fisc_title=a23_str,
        time_owner_name=sue_str,
        time_int=time7,
        quota=quota500,
        event_int=event3,
        celldepth=celldepth4,
        penny=penny6,
        deal_ancestors=das,
    )

    # THEN
    print(f"{sue7_cell_path=}")
    assert os_path_exists(sue7_cell_path)
    generated_cell_dict = open_json(sue7_cell_path)
    assert generated_cell_dict.get("ancestors") == das
    assert generated_cell_dict.get("event_int") == event3
    assert generated_cell_dict.get("celldepth") == celldepth4
    assert generated_cell_dict.get("deal_owner_name") == sue_str
    assert generated_cell_dict.get("penny") == penny6
    assert generated_cell_dict.get("quota") == quota500


def test_cellunit_add_json_file_SetsFile_Scenario1_ManyParametersEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(fisc_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_add_json_file(
        fisc_mstr_dir, a23_str, sue_str, time7, event3, deal_ancestors=das
    )

    # THEN
    print(f"{sue7_cell_path=}")
    assert os_path_exists(sue7_cell_path)
    generated_cell_dict = open_json(sue7_cell_path)
    assert generated_cell_dict.get("ancestors") == das
    assert generated_cell_dict.get("event_int") == event3
    assert generated_cell_dict.get("celldepth") == 0
    assert generated_cell_dict.get("deal_owner_name") == sue_str
    assert generated_cell_dict.get("penny") == 1
    assert generated_cell_dict.get("quota") == CELLNODE_QUOTA_DEFAULT


def test_cellunit_get_from_dir_ReturnsObj_Scenario1_FileExists(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(fisc_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    assert os_path_exists(sue7_cell_path) is False
    cellunit_add_json_file(
        fisc_mstr_dir, a23_str, sue_str, time7, event3, deal_ancestors=das
    )
    cell_dir = create_cell_dir_path(
        fisc_mstr_dir, a23_str, sue_str, time7, deal_ancestors=das
    )

    # WHEN
    gen_cellunit = cellunit_get_from_dir(cell_dir)

    # THEN
    expected_cellunit = cellunit_shop(sue_str, ancestors=das, event_int=event3)
    assert gen_cellunit == expected_cellunit


def test_cellunit_save_to_dir_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = get_listen_temp_env_dir()
    a23_str = "accord23"
    time7 = 777000
    sue_str = "Sue"
    bob_str = "Bob"
    das = [bob_str, sue_str]
    sue7_cell_path = node_path(fisc_mstr_dir, a23_str, sue_str, time7, das)
    event3 = 3
    sue_cell = cellunit_shop(sue_str, ancestors=das, event_int=event3)
    cell_dir = create_cell_dir_path(fisc_mstr_dir, a23_str, sue_str, time7, das)
    assert os_path_exists(sue7_cell_path) is False

    # WHEN
    cellunit_save_to_dir(cell_dir, sue_cell)

    # THEN
    assert os_path_exists(sue7_cell_path)
    assert cellunit_get_from_dir(cell_dir) == sue_cell
