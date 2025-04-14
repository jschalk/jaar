from src.a00_data_toolboxs.file_toolbox import open_json
from src.a11_deal_cell_logic.cell import budevent_facts_str
from src.a12_hub_tools.hub_path import create_cell_json_path, create_budevent_path
from src.a12_hub_tools.hub_tool import save_arbitrary_budevent, cellunit_add_json_file
from src.a15_fisc_logic.fisc_tool import load_cells_budevent
from src.a15_fisc_logic.examples.example_fiscs import example_casa_clean_factunit
from src.a15_fisc_logic.examples.fisc_env import (
    env_dir_setup_cleanup,
    get_test_fisc_mstr_dir,
)
from os.path import exists as os_path_exists


def test_load_cells_budevent_SetsFiles_Scenario0_NoFacts(
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
    cellunit_add_json_file(fisc_mstr_dir, a23_str, bob_str, time5, event300, [])
    bob5_cell_path = create_cell_json_path(fisc_mstr_dir, a23_str, bob_str, time5)
    assert open_json(bob5_cell_path).get(budevent_facts_str()) == {}

    # WHEN
    load_cells_budevent(fisc_mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob5_cell_path)
    assert open_json(bob5_cell_path).get(budevent_facts_str()) == {}


def test_load_cells_budevent_SetsFiles_Scenario1_WithFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    bob_str = "Bob"
    a23_str = "accord23"
    event300 = 300
    time5 = 5
    clean_fact = example_casa_clean_factunit()
    x_facts = [clean_fact.get_tuple()]
    save_arbitrary_budevent(fisc_mstr_dir, a23_str, bob_str, event300, facts=x_facts)
    bob3_budevent_path = create_budevent_path(fisc_mstr_dir, a23_str, bob_str, event300)
    print(f"{bob3_budevent_path=}")
    cellunit_add_json_file(fisc_mstr_dir, a23_str, bob_str, time5, event300, [])
    bob5_cell_path = create_cell_json_path(fisc_mstr_dir, a23_str, bob_str, time5)
    assert open_json(bob5_cell_path).get(budevent_facts_str()) == {}

    # WHEN
    load_cells_budevent(fisc_mstr_dir, a23_str)

    # THEN
    expected_budevent_facts = {clean_fact.base: clean_fact.get_dict()}
    assert (
        open_json(bob5_cell_path).get(budevent_facts_str()) == expected_budevent_facts
    )


def test_load_cells_budevent_SetsFiles_Scenario2_WithFacts_NotAtRoot(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fisc_mstr_dir = get_test_fisc_mstr_dir()
    bob_str = "Bob"
    a23_str = "accord23"
    event300 = 300
    time5 = 5
    clean_fact = example_casa_clean_factunit()
    x_facts = [(clean_fact.base, clean_fact.pick, None, None)]
    save_arbitrary_budevent(fisc_mstr_dir, a23_str, bob_str, event300, facts=x_facts)
    yao_str = "Yao"
    das = [yao_str, bob_str]
    cellunit_add_json_file(fisc_mstr_dir, a23_str, bob_str, time5, event300, das)
    bob5_cell_path = create_cell_json_path(fisc_mstr_dir, a23_str, bob_str, time5, das)
    assert open_json(bob5_cell_path).get(budevent_facts_str()) == {}

    # WHEN
    load_cells_budevent(fisc_mstr_dir, a23_str)

    # THEN
    expected_budevent_facts = {clean_fact.base: clean_fact.get_dict()}
    assert (
        open_json(bob5_cell_path).get(budevent_facts_str()) == expected_budevent_facts
    )
