from src.f00_instrument.file import open_json, save_json
from src.f01_road.road import create_road
from src.f04_gift.atom_config import base_str
from src.f05_listen.hub_path import (
    create_deal_node_json_path as node_path,
    create_deal_node_budevent_facts_path as bude_facts_path,
    create_deal_node_found_facts_path as found_facts_path,
    create_budevent_path,
)
from src.f05_listen.hub_tool import save_arbitrary_budevent, save_arbitrary_dealnode
from src.f07_fisc.fisc_tool import (
    create_all_deal_node_facts_files,
    uphill_deal_node_budevent_facts,
)
from src.f07_fisc.examples.fisc_env import env_dir_setup_cleanup, get_test_fisc_mstr_dir
from os.path import exists as os_path_exists


# for ever deal node create all factunits
def test_create_all_deal_node_facts_files_SetsFiles_Scenario0_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    bob_str = "Bob"
    a23_str = "accord23"
    event300 = 300
    time5 = 5
    save_arbitrary_budevent(fisc_mstr_dir, a23_str, bob_str, event300)
    bob3_budevent_path = create_budevent_path(fisc_mstr_dir, a23_str, bob_str, event300)
    print(f"{bob3_budevent_path=}")
    save_arbitrary_dealnode(fisc_mstr_dir, a23_str, bob_str, time5, [], event300)
    bob_t5_facts_path = bude_facts_path(fisc_mstr_dir, a23_str, bob_str, time5)
    # print(f" {bob_t5_facts_path=}")
    assert os_path_exists(bob_t5_facts_path) is False

    # WHEN
    create_all_deal_node_facts_files(fisc_mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob_t5_facts_path)
    assert open_json(bob_t5_facts_path) == {}


# for ever deal node create all factunits
def test_create_all_deal_node_facts_files_SetsFiles_Scenario1_WithFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    bob_str = "Bob"
    a23_str = "accord23"
    event300 = 300
    time5 = 5
    casa_road = create_road(a23_str, "casa")
    clean_road = create_road(casa_road, "clean")
    x_facts = [(casa_road, clean_road, None, None)]
    save_arbitrary_budevent(fisc_mstr_dir, a23_str, bob_str, event300, facts=x_facts)
    bob3_budevent_path = create_budevent_path(fisc_mstr_dir, a23_str, bob_str, event300)
    print(f"{bob3_budevent_path=}")
    save_arbitrary_dealnode(fisc_mstr_dir, a23_str, bob_str, time5, [], event300)
    bob_t5_facts_path = bude_facts_path(fisc_mstr_dir, a23_str, bob_str, time5)
    # print(f" {bob_t5_facts_path=}")
    assert os_path_exists(bob_t5_facts_path) is False

    # WHEN
    create_all_deal_node_facts_files(fisc_mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob_t5_facts_path)
    assert open_json(bob_t5_facts_path) == {
        casa_road: {base_str(): casa_road, "pick": clean_road}
    }


# for ever deal node create all factunits
def test_create_all_deal_node_facts_files_SetsFiles_Scenario2_WithFacts_NotAtRoot(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    bob_str = "Bob"
    a23_str = "accord23"
    event300 = 300
    time5 = 5
    casa_road = create_road(a23_str, "casa")
    clean_road = create_road(casa_road, "clean")
    x_facts = [(casa_road, clean_road, None, None)]
    save_arbitrary_budevent(fisc_mstr_dir, a23_str, bob_str, event300, facts=x_facts)
    yao_str = "Yao"
    das = [yao_str, bob_str]
    save_arbitrary_dealnode(fisc_mstr_dir, a23_str, bob_str, time5, das, event300)
    bob_t5_facts_path = bude_facts_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
    print(f" {bob_t5_facts_path=}")
    assert os_path_exists(bob_t5_facts_path) is False

    # WHEN
    create_all_deal_node_facts_files(fisc_mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob_t5_facts_path)
    facts_dict = open_json(bob_t5_facts_path)
    assert facts_dict == {casa_road: {base_str(): casa_road, "pick": clean_road}}


def test_uphill_deal_node_budevent_facts_Scenario0_RootOnly_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    bob_str = "Bob"
    a23_str = "accord23"
    time5 = 5
    das = []
    bob_t5_be_facts_path = bude_facts_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
    be_facts_dict = {}
    save_json(bob_t5_be_facts_path, None, be_facts_dict)
    bob_t5_found_path = found_facts_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
    assert os_path_exists(bob_t5_found_path) is False

    # WHEN
    uphill_deal_node_budevent_facts(fisc_mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob_t5_found_path)
    assert open_json(bob_t5_found_path) == {}


def test_uphill_deal_node_budevent_facts_Scenario1_ChildNode_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    mstr_dir = get_test_fisc_mstr_dir()
    bob_str = "Bob"
    yao_str = "Yao"
    sue_str = "Sue"
    a23_str = "accord23"
    time5 = 5
    das = []
    das_y = [yao_str]
    das_ys = [yao_str, sue_str]
    bob_t5_bef_path = bude_facts_path(mstr_dir, a23_str, bob_str, time5, das)
    bob_t5_yao_bef_path = bude_facts_path(mstr_dir, a23_str, bob_str, time5, das_y)
    bob_t5_yao_sue_bef_path = bude_facts_path(mstr_dir, a23_str, bob_str, time5, das_ys)
    save_json(bob_t5_bef_path, None, {})
    save_json(bob_t5_yao_bef_path, None, {})
    save_json(bob_t5_yao_sue_bef_path, None, {})
    bob_t5_found_path = found_facts_path(mstr_dir, a23_str, bob_str, time5, das)
    assert os_path_exists(bob_t5_found_path) is False

    # WHEN
    uphill_deal_node_budevent_facts(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob_t5_found_path)
    assert open_json(bob_t5_found_path) == {}


# def test_uphill_deal_node_budevent_facts_Scenario2_ChildNodeWithOneFactIsAssignedToAncestors(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     mstr_dir = get_test_fisc_mstr_dir()
#     bob_str = "Bob"
#     yao_str = "Yao"
#     sue_str = "Sue"
#     a23_str = "accord23"
#     time5 = 5
#     casa_road = create_road(a23_str, "casa")
#     clean_road = create_road(casa_road, "clean")
#     bob_t5_be_facts = {}
#     bob_t5_yao_be_facts = {}
#     bob_t5_yao_sue_be_facts = {casa_road: {base_str(): casa_road, "pick": clean_road}}
#     das = []
#     das_y = [yao_str]
#     das_ys = [yao_str, sue_str]
#     bob_t5_bef_path = bude_facts_path(mstr_dir, a23_str, bob_str, time5, das)
#     bob_t5_yao_bef_path = bude_facts_path(mstr_dir, a23_str, bob_str, time5, das_y)
#     bob_t5_yao_sue_bef_path = bude_facts_path(mstr_dir, a23_str, bob_str, time5, das_ys)
#     save_json(bob_t5_bef_path, None, bob_t5_be_facts)
#     save_json(bob_t5_yao_bef_path, None, bob_t5_yao_be_facts)
#     save_json(bob_t5_yao_sue_bef_path, None, bob_t5_yao_sue_be_facts)
#     bob_t5_found = found_facts_path(mstr_dir, a23_str, bob_str, time5, das)
#     bob_t5_yao_found = found_facts_path(mstr_dir, a23_str, bob_str, time5, das_y)
#     bob_t5_yao_sue_found = found_facts_path(mstr_dir, a23_str, bob_str, time5, das_ys)
#     assert os_path_exists(bob_t5_found) is False
#     assert os_path_exists(bob_t5_yao_found) is False
#     assert os_path_exists(bob_t5_yao_sue_found) is False

#     # WHEN
#     uphill_deal_node_budevent_facts(mstr_dir, a23_str)

#     # THEN
#     assert os_path_exists(bob_t5_found)
#     assert os_path_exists(bob_t5_yao_found)
#     assert os_path_exists(bob_t5_yao_sue_found)
#     assert open_json(bob_t5_found) == bob_t5_yao_sue_be_facts
#     assert open_json(bob_t5_yao_found) == bob_t5_yao_sue_be_facts
#     assert open_json(bob_t5_yao_sue_found) == bob_t5_yao_sue_be_facts
#     assert 1 == 2


# def test_uphill_deal_node_budevent_facts_Scenario0_RootOnly_NoFacts(env_dir_setup_cleanup):
#     # ESTABLISH
#     fisc_mstr_dir = get_test_fisc_mstr_dir()
#     bob_str = "Bob"
#     a23_str = "accord23"
#     event300 = 300
#     time5 = 5
#     casa_road = create_road(a23_str, "casa")
#     clean_road = create_road(casa_road, "clean")
#     x_facts = [(casa_road, clean_road, None, None)]
#     save_arbitrary_budevent(fisc_mstr_dir, a23_str, bob_str, event300, facts=x_facts)
#     bob3_budevent_path = create_budevent_path(fisc_mstr_dir, a23_str, bob_str, event300)
#     yao_str = "Yao"
#     das = [yao_str, bob_str]
#     bob_5_yao_bob_deal_node = node_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
#     assert os_path_exists(bob_5_yao_bob_deal_node) is False
#     save_arbitrary_dealnode(fisc_mstr_dir, a23_str, bob_str, time5, das, event300)
#     print(f"{bob_5_yao_bob_deal_node=}")
#     assert os_path_exists(bob_5_yao_bob_deal_node)
#     bob_t5_facts_path = facts_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
#     print(f" {bob_t5_facts_path=}")
#     assert os_path_exists(bob_t5_facts_path) is False
