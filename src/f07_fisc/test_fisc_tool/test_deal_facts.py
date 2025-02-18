from src.f00_instrument.file import open_json
from src.f01_road.road import create_road
from src.f04_gift.atom_config import base_str
from src.f05_listen.hub_path import (
    create_deal_node_json_path as node_path,
    create_deal_node_facts_path as facts_path,
    create_budevent_path,
)
from src.f05_listen.hub_tool import save_arbitrary_budevent, save_arbitrary_dealnode
from src.f07_fisc.fisc_tool import (
    create_all_deal_node_facts_files,
    # inherit_all_deal_node_face_files,
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
    bob_t5_facts_path = facts_path(fisc_mstr_dir, a23_str, bob_str, time5)
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
    bob_t5_facts_path = facts_path(fisc_mstr_dir, a23_str, bob_str, time5)
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
    bob3_budevent_path = create_budevent_path(fisc_mstr_dir, a23_str, bob_str, event300)
    yao_str = "Yao"
    das = [yao_str, bob_str]
    bob_5_yao_bob_deal_node = node_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
    assert os_path_exists(bob_5_yao_bob_deal_node) is False
    save_arbitrary_dealnode(fisc_mstr_dir, a23_str, bob_str, time5, das, event300)
    print(f"{bob_5_yao_bob_deal_node=}")
    assert os_path_exists(bob_5_yao_bob_deal_node)
    bob_t5_facts_path = facts_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
    print(f" {bob_t5_facts_path=}")
    assert os_path_exists(bob_t5_facts_path) is False

    # WHEN
    create_all_deal_node_facts_files(fisc_mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob_t5_facts_path)
    facts_dict = open_json(bob_t5_facts_path)
    assert facts_dict == {casa_road: {base_str(): casa_road, "pick": clean_road}}
