from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import open_json
from src.a11_bud_logic.test._util.a11_str import planevent_facts_str
from src.a12_hub_toolbox.hub_path import create_cell_json_path, create_planevent_path
from src.a12_hub_toolbox.hub_tool import (
    cellunit_add_json_file,
    save_arbitrary_planevent,
)
from src.a15_belief_logic.belief_cell import load_cells_planevent
from src.a15_belief_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_belief_logic.test._util.example_beliefs import example_casa_clean_factunit


def test_load_cells_planevent_SetsFiles_Scenario0_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    a23_str = "amy23"
    event300 = 300
    time5 = 5
    save_arbitrary_planevent(belief_mstr_dir, a23_str, bob_str, event300)
    bob3_planevent_path = create_planevent_path(
        belief_mstr_dir, a23_str, bob_str, event300
    )
    print(f"{bob3_planevent_path=}")
    cellunit_add_json_file(belief_mstr_dir, a23_str, bob_str, time5, event300, [])
    bob5_cell_path = create_cell_json_path(belief_mstr_dir, a23_str, bob_str, time5)
    assert open_json(bob5_cell_path).get(planevent_facts_str()) == {}

    # WHEN
    load_cells_planevent(belief_mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob5_cell_path)
    assert open_json(bob5_cell_path).get(planevent_facts_str()) == {}


def test_load_cells_planevent_SetsFiles_Scenario1_WithFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    a23_str = "amy23"
    event300 = 300
    time5 = 5
    clean_fact = example_casa_clean_factunit()
    x_facts = [clean_fact.get_tuple()]
    save_arbitrary_planevent(belief_mstr_dir, a23_str, bob_str, event300, facts=x_facts)
    bob3_planevent_path = create_planevent_path(
        belief_mstr_dir, a23_str, bob_str, event300
    )
    print(f"{bob3_planevent_path=}")
    cellunit_add_json_file(belief_mstr_dir, a23_str, bob_str, time5, event300, [])
    bob5_cell_path = create_cell_json_path(belief_mstr_dir, a23_str, bob_str, time5)
    assert open_json(bob5_cell_path).get(planevent_facts_str()) == {}

    # WHEN
    load_cells_planevent(belief_mstr_dir, a23_str)

    # THEN
    expected_planevent_facts = {clean_fact.fcontext: clean_fact.get_dict()}
    assert (
        open_json(bob5_cell_path).get(planevent_facts_str()) == expected_planevent_facts
    )


def test_load_cells_planevent_SetsFiles_Scenario2_WithFacts_NotAtRoot(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    belief_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    a23_str = "amy23"
    event300 = 300
    time5 = 5
    clean_fact = example_casa_clean_factunit()
    x_facts = [(clean_fact.fcontext, clean_fact.fstate, None, None)]
    save_arbitrary_planevent(belief_mstr_dir, a23_str, bob_str, event300, facts=x_facts)
    yao_str = "Yao"
    das = [yao_str, bob_str]
    cellunit_add_json_file(belief_mstr_dir, a23_str, bob_str, time5, event300, das)
    bob5_cell_path = create_cell_json_path(
        belief_mstr_dir, a23_str, bob_str, time5, das
    )
    assert open_json(bob5_cell_path).get(planevent_facts_str()) == {}

    # WHEN
    load_cells_planevent(belief_mstr_dir, a23_str)

    # THEN
    expected_planevent_facts = {clean_fact.fcontext: clean_fact.get_dict()}
    assert (
        open_json(bob5_cell_path).get(planevent_facts_str()) == expected_planevent_facts
    )
