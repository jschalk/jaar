from src.f00_instrument.dict_toolbox import get_dict_from_json, get_json_from_dict
from src.f00_instrument.file import open_file, save_file, create_path, count_dirs_files
from src.f01_road.deal import ledger_depth_str, owner_name_str
from src.f02_bud.bud import budunit_shop, get_from_json as budunit_get_from_json
from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_owners_dir_path,
    create_event_bud_path,
    create_budpoint_json_path,
    create_deal_ledger_state_json_path,
    create_fisc_ote1_json_path,
)
from src.f07_fisc.fisc import fiscunit_shop
from src.f08_pidgin.pidgin_config import event_int_str
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_create_budpoints_Scenaro0_DealEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    accord23_str = "accord23"
    fiscs_dir = create_path(fizz_world._fisc_mstr_dir, "fiscals")
    accord23_fisc = fiscunit_shop(accord23_str, fiscs_dir)
    a23_json_path = create_fisc_json_path(fizz_world._fisc_mstr_dir, accord23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    print(f"{a23_json_path=}")
    a23_owners_path = create_owners_dir_path(fizz_world._fisc_mstr_dir, accord23_str)
    assert count_dirs_files(a23_owners_path) == 0

    # WHEN
    fizz_world.create_budpoints()

    # THEN
    assert count_dirs_files(a23_owners_path) == 0


def test_WorldUnit_create_budpoints_Scenaro1_DealExists(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"

    # Create FiscUnit with bob deal at time 37
    accord23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    bob_str = "Bob"
    timepoint37 = 37
    deal1_magnitude = 450
    accord23_fisc.add_dealepisode(bob_str, timepoint37, deal1_magnitude)
    a23_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    assert os_path_exists(a23_json_path)

    # Create event time mapping owner_time_agg for time 37
    event3 = 3
    event7 = 7
    timepoint66 = 66
    a23_ote1_dict = {bob_str: {str(timepoint37): event3, str(timepoint66): event7}}
    a23_ote1_json_path = create_fisc_ote1_json_path(fisc_mstr_dir, a23_str)
    print(f"{a23_ote1_json_path=}")
    save_file(a23_ote1_json_path, None, get_json_from_dict(a23_ote1_dict))
    assert os_path_exists(a23_ote1_json_path)

    # Create bob event 37 Budunit json
    e3_budunit = budunit_shop(bob_str, a23_str)
    e3_budpoint_path = create_event_bud_path(fisc_mstr_dir, a23_str, bob_str, event3)
    save_file(e3_budpoint_path, None, e3_budunit.get_json())
    assert os_path_exists(e3_budpoint_path)

    # destination of event 37 budunit json
    timepoint37_budpoint_path = create_budpoint_json_path(
        fisc_mstr_dir, a23_str, bob_str, timepoint37
    )
    print(f"{timepoint37_budpoint_path=}")
    assert os_path_exists(timepoint37_budpoint_path) is False

    # WHEN
    fizz_world.create_budpoints()

    # THEN
    assert os_path_exists(timepoint37_budpoint_path)
    generated_e3_bud = budunit_get_from_json(open_file(timepoint37_budpoint_path))
    assert e3_budunit.get_dict() == generated_e3_bud.get_dict()


def test_WorldUnit_create_budpoints_Scenaro2_DealExistsButNoBudExistsInEventsPast(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"

    # Create FiscUnit with bob deal at time 37
    accord23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    bob_str = "Bob"
    timepoint37 = 37
    deal1_magnitude = 450
    accord23_fisc.add_dealepisode(bob_str, timepoint37, deal1_magnitude)
    a23_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    assert os_path_exists(a23_json_path)

    # Create event time mapping owner_time_agg for time 37
    event3 = 3
    event7 = 7
    timepoint40 = 40
    timepoint66 = 66
    a23_ote1_dict = {bob_str: {str(timepoint40): event3, str(timepoint66): event7}}
    a23_ote1_json_path = create_fisc_ote1_json_path(fisc_mstr_dir, a23_str)
    print(f"{a23_ote1_json_path=}")
    save_file(a23_ote1_json_path, None, get_json_from_dict(a23_ote1_dict))
    assert os_path_exists(a23_ote1_json_path)

    # Create bob event 3 Budunit json
    e3_budunit = budunit_shop(bob_str, a23_str)
    e3_budpoint_path = create_event_bud_path(fisc_mstr_dir, a23_str, bob_str, event3)
    save_file(e3_budpoint_path, None, e3_budunit.get_json())
    assert os_path_exists(e3_budpoint_path)

    # where a timepoint 37 budunit json should be
    timepoint37_budpoint_path = create_budpoint_json_path(
        fisc_mstr_dir, a23_str, bob_str, timepoint37
    )
    print(f"{timepoint37_budpoint_path=}")
    assert os_path_exists(timepoint37_budpoint_path) is False

    # WHEN
    fizz_world.create_budpoints()

    # THEN
    assert os_path_exists(timepoint37_budpoint_path) is False


def test_WorldUnit_create_budpoints_Scenaro3_DealExistsNotPerfectMatch_time_int_event_int(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"

    # Create FiscUnit with bob deal at time 37
    accord23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
    bob_str = "Bob"
    timepoint37 = 37
    deal1_magnitude = 450
    deal1_ledger_depth = 3
    accord23_fisc.add_dealepisode(
        bob_str, timepoint37, deal1_magnitude, ledger_depth=deal1_ledger_depth
    )
    a23_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
    save_file(a23_json_path, None, accord23_fisc.get_json())
    assert os_path_exists(a23_json_path)

    # Create event time mapping owner_time_agg for time 37
    event3 = 3
    event7 = 7
    timepoint30 = 30
    timepoint66 = 66
    a23_ote1_dict = {bob_str: {str(timepoint30): event3, str(timepoint66): event7}}
    a23_ote1_json_path = create_fisc_ote1_json_path(fisc_mstr_dir, a23_str)
    print(f"{a23_ote1_json_path=}")
    save_file(a23_ote1_json_path, None, get_json_from_dict(a23_ote1_dict))
    assert os_path_exists(a23_ote1_json_path)

    # Create bob event 3 Budunit json
    e3_budunit = budunit_shop(bob_str, a23_str)
    e3_budpoint_path = create_event_bud_path(fisc_mstr_dir, a23_str, bob_str, event3)
    save_file(e3_budpoint_path, None, e3_budunit.get_json())
    assert os_path_exists(e3_budpoint_path)

    # destination of event 3 budunit json
    timepoint37_budpoint_path = create_budpoint_json_path(
        fisc_mstr_dir, a23_str, bob_str, timepoint37
    )
    print(f"{timepoint37_budpoint_path=}")
    # destination of deal_ledger_state json
    timepoint37_deal_ledger_state_json_path = create_deal_ledger_state_json_path(
        fisc_mstr_dir, a23_str, bob_str, timepoint37
    )
    assert os_path_exists(timepoint37_budpoint_path) is False

    # WHEN
    fizz_world.create_budpoints()

    # THEN
    assert os_path_exists(timepoint37_budpoint_path)
    generated_e3_bud = budunit_get_from_json(open_file(timepoint37_budpoint_path))
    assert e3_budunit.get_dict() == generated_e3_bud.get_dict()

    assert os_path_exists(timepoint37_deal_ledger_state_json_path)
    ledger_state_json = open_file(timepoint37_deal_ledger_state_json_path)
    ledger_state_dict = get_dict_from_json(ledger_state_json)
    assert ledger_state_dict.get(ledger_depth_str()) == deal1_ledger_depth
    assert ledger_state_dict.get(owner_name_str()) == bob_str
    assert ledger_state_dict.get(event_int_str()) == event3
    assert len(ledger_state_dict) == 3
