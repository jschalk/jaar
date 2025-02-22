from src.f00_instrument.file import open_json, save_json
from src.f01_road.deal import quota_str
from src.f05_listen.hub_path import (
    create_deal_node_json_path,
    create_deal_node_adjust_ledger_path as node_ledger,
    create_dealunit_net_ledger_json_path as deal_net_ledger,
)
from src.f05_listen.hub_tool import save_deal_node_file
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.example_worlds import get_mop_with_reason_budunit_example
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from os.path import exists as os_path_exists

# set acct_adjust_ledgers in deal_node
# run allot_nested_scale to get root allotment
# save root allotment as json


def test_create_fiscs_deals_net_ledgers_SetsFiles_Scenario0_RootOnlyEmpty_node_acct_adjust_ledger(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    mstr_dir = fizz_world._fisc_mstr_dir
    a23_str = "accord"
    tp5 = 5
    bob_str = "Bob"
    das = []
    # save root deal_node json with quota
    root_deal_node_path = create_deal_node_json_path(mstr_dir, a23_str, bob_str, tp5)
    root_deal_node_dict = {quota_str(): 300}
    save_json(root_deal_node_path, None, root_deal_node_dict)
    # save deal_node_adjust_ledger json
    bob5_node_path = node_ledger(mstr_dir, a23_str, bob_str, tp5, das)
    save_json(bob5_node_path, None, {})
    # save paths for root_adjust_ledger_path
    bob5_root_adjust_ledger_path = deal_net_ledger(mstr_dir, a23_str, bob_str, tp5)
    assert os_path_exists(bob5_root_adjust_ledger_path) is False

    # WHEN
    fizz_world.create_fiscs_deals_net_ledgers()

    # THEN
    assert os_path_exists(bob5_root_adjust_ledger_path)
    assert open_json(bob5_root_adjust_ledger_path) == {}


# def test_create_fiscs_deals_net_ledgers_SetsFiles_Scenario1_Multiple_deal_node_adjust_legder(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     mstr_dir = fizz_world._fisc_mstr_dir
#     a23_str = "accord"
#     tp5 = 5
#     bob_str = "Bob"
#     sue_str = "Sue"
#     yao_str = "Yao"
#     zia_str = "Zia"

#     # save root deal_node json with quota
#     root_deal_node_path = create_deal_node_json_path(mstr_dir, a23_str, bob_str, tp5)
#     root_deal_node_dict = {quota_str(): 5000}
#     save_json(root_deal_node_path, None, root_deal_node_dict)
#     # save deal_node_adjust_ledger jsons
#     das = []
#     das_sue = [sue_str]
#     das_sue_yao = [sue_str, yao_str]
#     das_yao = [yao_str]
#     das_yao_zia = [yao_str, zia_str]
#     das_zia = [zia_str]
#     das_zia = [zia_str, sue_str]
#     bob5_node_path = node_ledger(mstr_dir, a23_str, bob_str, tp5, das)
#     bob5_sue_node_path = node_ledger(mstr_dir, a23_str, bob_str, tp5, das_sue)
#     bob5_sue_yao_node_path = node_ledger(mstr_dir, a23_str, bob_str, tp5, das_sue_yao)
#     bob5_yao_node_path = node_ledger(mstr_dir, a23_str, bob_str, tp5, das_yao)
#     bob5_yao_zia_node_path = node_ledger(mstr_dir, a23_str, bob_str, tp5, das_yao_zia)
#     bob5_zia_node_path = node_ledger(mstr_dir, a23_str, bob_str, tp5, das_zia)
#     bob5_zia_node_path = node_ledger(mstr_dir, a23_str, bob_str, tp5, das_zia)
#     bob5_node_ledger = {sue_str: -444, yao_str: 444, zia_str: -300}
#     bob5_sue_node_ledger = {bob_str: -300, yao_str: 300}
#     bob5_sue_yao_node_ledger = {sue_str: -23, yao_str: 23}
#     bob5_yao_node_ledger = {bob_str: 7, yao_str: -10, zia_str: 3}
#     bob5_yao_zia_node_ledger = {sue_str: -77, yao_str: 77}
#     bob5_zia_node_ledger = {bob_str: 222, sue_str: -222}
#     bob5_zia_node_ledger = {bob_str: 222, yao_str: -111, zia_str: -111}
#     save_json(bob5_node_path, None, bob5_node_ledger)
#     save_json(bob5_sue_node_path, None, bob5_sue_node_ledger)
#     save_json(bob5_sue_yao_node_path, None, bob5_sue_yao_node_ledger)
#     save_json(bob5_yao_node_path, None, bob5_yao_node_ledger)
#     save_json(bob5_yao_zia_node_path, None, bob5_yao_zia_node_ledger)
#     save_json(bob5_zia_node_path, None, bob5_zia_node_ledger)
#     save_json(bob5_zia_node_path, None, bob5_zia_node_ledger)

#     # create paths for deal_root_adjust_ledger_path
#     bob5_root_adjust_ledger_path = deal_net_ledger(mstr_dir, a23_str, bob_str, tp5)
#     assert os_path_exists(bob5_root_adjust_ledger_path) is False

#     # WHEN
#     fizz_world.create_fiscs_deals_net_ledgers()

#     # THEN
#     assert os_path_exists(bob5_root_adjust_ledger_path)
#     assert open_json(bob5_root_adjust_ledger_path) == {
#         "Sue": 2500,
#         "Yao": -2500,
#         "Zia": 50004444,
#     }
#     assert 1 == 2
