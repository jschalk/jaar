from src.f00_instrument.file import (
    open_json,
    save_file,
    save_json,
    create_path,
    count_dirs_files,
)
from src.f01_road.deal import owner_name_str, quota_str, ledger_depth_str
from src.f02_bud.bud import budunit_shop
from src.f04_gift.atom_config import event_int_str
from src.f05_listen.hub_path import (
    create_fisc_json_path,
    create_owners_dir_path,
    create_episodes_dir_path,
    create_budevent_path as budevent_path,
    create_timepoint_dir_path,
    create_budevent_path,
    create_episode_node_dir_path,
    create_episode_node_state_path,
    create_episode_node_credit_ledger_path,
    create_episode_node_quota_ledger_path,
    create_fisc_ote1_csv_path,
    create_fisc_ote1_json_path,
)
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_WorldUnit_create_deal_ledger_depth_Scenaro0_timepoint_Empty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"
    bob_str = "Bob"
    tp37 = 37

    a23_bob_tp37_path = create_timepoint_dir_path(fisc_mstr_dir, a23_str, bob_str, tp37)
    print(f"{a23_bob_tp37_path=}")
    assert count_dirs_files(a23_bob_tp37_path) == 0

    # WHEN
    fizz_world.create_deal_ledger_depth()

    # THEN
    assert count_dirs_files(a23_bob_tp37_path) == 0


def save_budevent(
    fisc_mstr_dir: str,
    fisc_title: str,
    owner_name: str,
    event_int: int,
    accts: list[list],
) -> str:
    x_budunit = budunit_shop(owner_name, fisc_title)
    for acct_list in accts:
        x_budunit.add_acctunit(acct_list[0])
    x_budpoint_path = create_budevent_path(
        fisc_mstr_dir, fisc_title, owner_name, event_int
    )
    print(f"{x_budpoint_path=} {x_budunit.accts.keys()=}")
    save_file(x_budpoint_path, None, x_budunit.get_json())
    return x_budpoint_path


def test_WorldUnit_create_deal_ledger_depth_Scenaro1_LedgerDepth0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    fisc_mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord23"
    bob_str = "Bob"
    yao_str = "Yao"
    tp37 = 37  # timepoint
    deal1_quota = 450
    deal1_ledger_depth = 0
    event56 = 56
    episode_node = {
        ledger_depth_str(): deal1_ledger_depth,
        owner_name_str(): bob_str,
        event_int_str(): event56,
        quota_str(): deal1_quota,
    }
    a23_bob_ledger_state_path = create_episode_node_state_path(
        fisc_mstr_dir=fisc_mstr_dir,
        fisc_title=a23_str,
        owner_name=bob_str,
        time_int=tp37,
    )
    save_json(a23_bob_ledger_state_path, None, episode_node)
    save_budevent(fisc_mstr_dir, a23_str, bob_str, event56, [[yao_str], [bob_str]])

    bob_tp37_credit_ledger_path = create_episode_node_credit_ledger_path(
        fisc_mstr_dir, a23_str, bob_str, tp37
    )
    bob_tp37_quota_ledger_path = create_episode_node_quota_ledger_path(
        fisc_mstr_dir, a23_str, bob_str, tp37
    )
    bob_tp37_dir = create_timepoint_dir_path(fisc_mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob_tp37_credit_ledger_path) is False
    assert os_path_exists(bob_tp37_quota_ledger_path) is False
    assert count_dirs_files(bob_tp37_dir) == 1

    # WHEN
    fizz_world.create_deal_ledger_depth()

    # THEN
    assert os_path_exists(bob_tp37_credit_ledger_path)
    assert open_json(bob_tp37_credit_ledger_path) == {"Bob": 1, "Yao": 1}
    assert os_path_exists(bob_tp37_quota_ledger_path)
    assert open_json(bob_tp37_quota_ledger_path) == {"Bob": 225, "Yao": 225}
    assert count_dirs_files(bob_tp37_dir) == 3


# def test_WorldUnit_create_deal_ledger_depth_Scenaro2_LedgerDepth1(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     fisc_mstr_dir = fizz_world._fisc_mstr_dir
#     a23_str = "accord23"
#     bob_str = "Bob"
#     timepoint37 = 37

#     # save ledger_state json at tp37 root
#     deal1_quota = 450
#     deal1_ledger_depth = 1
#     tp37_ledger_state_path = create_episode_node_state_path(
#         fisc_mstr_dir, a23_str, bob_str, timepoint37
#     )
#     tp37_ledger_state_dict = {
#         ledger_depth_str(): deal1_ledger_depth,
#         owner_name_str(): bob_str,
#         quota_str(): deal1_quota,
#         event_int_str(): event3,
#     }
#     save_file(tp37_ledger_state_path, None, tp37_ledger_state_dict)

#     # Create yao event3 bud.json
#     event3 = 3
#     yao_str = "Yao"
#     e3_yao_budevent = budunit_shop(yao_str, a23_str)
#     e3_yap_budpoint_path = budevent_path(fisc_mstr_dir, a23_str, yao_str, event3)
#     save_file(e3_yap_budpoint_path, None, e3_yao_budevent.get_json())
#     assert os_path_exists(e3_yap_budpoint_path)

#     # Create bob timepoint37 budpoint.json
#     e3_bob_bud = budunit_shop(bob_str, a23_str)
#     e3_bob_bud.add_acctunit(yao_str)
#     budpoint37_path = create_budpoint_path(fisc_mstr_dir, a23_str, bob_str, timepoint37)
#     save_file(budpoint37_path, None, e3_bob_bud.get_json())
#     assert os_path_exists(budpoint37_path)
#     tp37_dir = create_timepoint_dir_path(fisc_mstr_dir, a23_str, bob_str, timepoint37)
#     tp37_yao_dir = create_episode_node_dir_path(
#         fisc_mstr_dir, a23_str, bob_str, timepoint37, [yao_str]
#     )
#     tp37_yao_state_path = create_episode_node_state_path(
#         fisc_mstr_dir, a23_str, bob_str, timepoint37, [yao_str]
#     )
#     print(f"{tp37_yao_dir=}")
#     assert os_path_exists(tp37_yao_dir) is False
#     assert os_path_exists(tp37_yao_state_path) is False
#     assert count_dirs_files(tp37_dir) == 1

#     # WHEN
#     fizz_world.create_deal_ledger_depth()

#     # THEN
#     assert os_path_exists(tp37_yao_dir)
#     assert os_path_exists(tp37_yao_state_path)
#     assert count_dirs_files(tp37_dir) == 3


# def test_WorldUnit_create_deal_ledger_depth_Scenaro2_DealExistsButNoBudExistsInEventsPast(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     fisc_mstr_dir = fizz_world._fisc_mstr_dir
#     a23_str = "accord23"

#     # Create FiscUnit with bob deal at time 37
#     accord23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
#     bob_str = "Bob"
#     timepoint37 = 37
#     deal1_quota = 450
#     accord23_fisc.add_dealepisode(bob_str, timepoint37, deal1_quota)
#     a23_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
#     save_file(a23_json_path, None, accord23_fisc.get_json())
#     assert os_path_exists(a23_json_path)

#     # Create event time mapping owner_time_agg for time 37
#     event3 = 3
#     event7 = 7
#     timepoint40 = 40
#     timepoint66 = 66
#     a23_ote1_dict = {bob_str: {str(timepoint40): event3, str(timepoint66): event7}}
#     a23_ote1_json_path = create_fisc_ote1_json_path(fisc_mstr_dir, a23_str)
#     print(f"{a23_ote1_json_path=}")
#     save_json(a23_ote1_json_path, None, a23_ote1_dict)
#     assert os_path_exists(a23_ote1_json_path)

#     # Create bob event 3 Budunit json
#     e3_budunit = budunit_shop(bob_str, a23_str)
#     e3_budpoint_path = budevent_path(fisc_mstr_dir, a23_str, bob_str, event3)
#     save_file(e3_budpoint_path, None, e3_budunit.get_json())
#     assert os_path_exists(e3_budpoint_path)

#     # where a timepoint 37 budunit json should be
#     timepoint37_budpoint_path = create_budpoint_path(
#         fisc_mstr_dir, a23_str, bob_str, timepoint37
#     )
#     print(f"{timepoint37_budpoint_path=}")
#     assert os_path_exists(timepoint37_budpoint_path) is False

#     # WHEN
#     fizz_world.create_deal_ledger_depth()

#     # THEN
#     assert os_path_exists(timepoint37_budpoint_path) is False


# def test_WorldUnit_create_deal_ledger_depth_Scenaro3_DealExistsNotPerfectMatch_time_int_event_int(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     fisc_mstr_dir = fizz_world._fisc_mstr_dir
#     a23_str = "accord23"

#     # Create FiscUnit with bob deal at time 37
#     accord23_fisc = fiscunit_shop(a23_str, fisc_mstr_dir)
#     bob_str = "Bob"
#     timepoint37 = 37
#     deal1_quota = 450
#     accord23_fisc.add_dealepisode(bob_str, timepoint37, deal1_quota)
#     a23_json_path = create_fisc_json_path(fisc_mstr_dir, a23_str)
#     save_file(a23_json_path, None, accord23_fisc.get_json())
#     assert os_path_exists(a23_json_path)

#     # Create event time mapping owner_time_agg for time 37
#     event3 = 3
#     event7 = 7
#     timepoint30 = 30
#     timepoint66 = 66
#     a23_ote1_dict = {bob_str: {str(timepoint30): event3, str(timepoint66): event7}}
#     a23_ote1_json_path = create_fisc_ote1_json_path(fisc_mstr_dir, a23_str)
#     print(f"{a23_ote1_json_path=}")
#     save_json(a23_ote1_json_path, None, a23_ote1_dict)
#     assert os_path_exists(a23_ote1_json_path)

#     # Create bob event 3 Budunit json
#     e3_budunit = budunit_shop(bob_str, a23_str)
#     e3_budpoint_path = budevent_path(fisc_mstr_dir, a23_str, bob_str, event3)
#     save_file(e3_budpoint_path, None, e3_budunit.get_json())
#     assert os_path_exists(e3_budpoint_path)

#     # destination of event 3 budunit json
#     timepoint37_budpoint_path = create_budpoint_path(
#         fisc_mstr_dir, a23_str, bob_str, timepoint37
#     )
#     print(f"{timepoint37_budpoint_path=}")
#     # destination of episode_node json
#     timepoint37_episode_node_json_path = create_episode_node_state_path(
#         fisc_mstr_dir, a23_str, bob_str, timepoint37
#     )
#     assert os_path_exists(timepoint37_budpoint_path) is False

#     # WHEN
#     fizz_world.create_deal_ledger_depth()

#     # THEN
#     assert os_path_exists(timepoint37_budpoint_path)
#     generated_e3_bud = budunit_get_from_json(open_file(timepoint37_budpoint_path))
#     assert e3_budunit.get_dict() == generated_e3_bud.get_dict()

#     assert os_path_exists(timepoint37_episode_node_json_path)
#     ledger_state_dict = open_json(timepoint37_episode_node_json_path)
#     assert ledger_state_dict.get(ledger_depth_str()) == 0
#     assert ledger_state_dict.get(owner_name_str()) == bob_str
#     assert ledger_state_dict.get(event_int_str()) == event3
#     assert len(ledger_state_dict) == 3


# a23_ote1_dict = open_json(a23_ote1_json_path))

# bob_str = "Bob"
# sue_str = "Sue"
# event3 = 3
# event7 = 7
# accord23_str = "accord23"
# accord45_str = "accord45"
# timepoint55 = 55
# timepoint66 = 66
# fisc_mstr_dir = fizz_world._fisc_mstr_dir


#     a23_event_time_p = create_fisc_ote1_csv_path(fisc_mstr_dir, accord23_str)
#     a45_event_time_p = create_fisc_ote1_csv_path(fisc_mstr_dir, accord45_str)
#     a23_event_time_csv = f"""{fisc_title_str()},{owner_name_str()},{event_int_str()},{time_int_str()},error_message
# {accord23_str},{bob_str},{event3},{timepoint55},
# """
#     a45_event_time_csv = f"""{fisc_title_str()},{owner_name_str()},{event_int_str()},{time_int_str()},error_message
# {accord45_str},{sue_str},{event3},{timepoint55},
# {accord45_str},{sue_str},{event7},{timepoint66},
# """
#     save_file(a23_event_time_p, None, a23_event_time_csv)
#     save_file(a45_event_time_p, None, a45_event_time_csv)
#     assert os_path_exists(a23_event_time_p)
#     assert os_path_exists(a45_event_time_p)
#     a23_ote1_json_path = create_fisc_ote1_json_path(
#         fisc_mstr_dir, accord23_str
#     )
#     a45_ote1_json_path = create_fisc_ote1_json_path(
#         fisc_mstr_dir, accord45_str
#     )
#     assert os_path_exists(a23_ote1_json_path) is False
#     assert os_path_exists(a45_event_time_json_path) is False

#     # WHEN
#     fizz_world.fisc_ote1_agg_csvs2jsons()

#     # THEN
#     assert os_path_exists(a23_ote1_json_path)
#     assert os_path_exists(a45_event_time_json_path)
#     a23_ote1_dict = open_json(a23_ote1_json_path))
#     a45_ote1_dict = open_json(a45_event_time_json_path))
#     assert a23_ote1_dict == {bob_str: {str(event3): timepoint55}}
#     assert a45_ote1_dict == {
#         sue_str: {str(event3): timepoint55, str(event7): timepoint66}
#     }
