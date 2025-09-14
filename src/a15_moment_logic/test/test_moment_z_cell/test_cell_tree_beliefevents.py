from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import open_json
from src.a12_hub_toolbox.a12_path import create_beliefevent_path, create_cell_json_path
from src.a12_hub_toolbox.hub_tool import (
    cellunit_add_json_file,
    save_arbitrary_beliefevent,
)
from src.a15_moment_logic._ref.a15_terms import beliefevent_facts_str
from src.a15_moment_logic.moment_cell import load_cells_beliefevent
from src.a15_moment_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a15_moment_logic.test._util.example_moments import example_casa_clean_factunit


def test_load_cells_beliefevent_SetsFiles_Scenario0_NoFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    a23_str = "amy23"
    event300 = 300
    time5 = 5
    save_arbitrary_beliefevent(moment_mstr_dir, a23_str, bob_str, event300)
    bob3_beliefevent_path = create_beliefevent_path(
        moment_mstr_dir, a23_str, bob_str, event300
    )
    print(f"{bob3_beliefevent_path=}")
    cellunit_add_json_file(moment_mstr_dir, a23_str, bob_str, time5, event300, [])
    bob5_cell_path = create_cell_json_path(moment_mstr_dir, a23_str, bob_str, time5)
    assert open_json(bob5_cell_path).get(beliefevent_facts_str()) == {}

    # WHEN
    load_cells_beliefevent(moment_mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob5_cell_path)
    assert open_json(bob5_cell_path).get(beliefevent_facts_str()) == {}


def test_load_cells_beliefevent_SetsFiles_Scenario1_WithFacts(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    a23_str = "amy23"
    event300 = 300
    time5 = 5
    clean_fact = example_casa_clean_factunit()
    x_facts = [clean_fact.get_tuple()]
    save_arbitrary_beliefevent(
        moment_mstr_dir, a23_str, bob_str, event300, facts=x_facts
    )
    bob3_beliefevent_path = create_beliefevent_path(
        moment_mstr_dir, a23_str, bob_str, event300
    )
    print(f"{bob3_beliefevent_path=}")
    cellunit_add_json_file(moment_mstr_dir, a23_str, bob_str, time5, event300, [])
    bob5_cell_path = create_cell_json_path(moment_mstr_dir, a23_str, bob_str, time5)
    assert open_json(bob5_cell_path).get(beliefevent_facts_str()) == {}

    # WHEN
    load_cells_beliefevent(moment_mstr_dir, a23_str)

    # THEN
    expected_beliefevent_facts = {clean_fact.fact_context: clean_fact.to_dict()}
    assert (
        open_json(bob5_cell_path).get(beliefevent_facts_str())
        == expected_beliefevent_facts
    )


def test_load_cells_beliefevent_SetsFiles_Scenario2_WithFacts_NotAtRoot(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    moment_mstr_dir = get_module_temp_dir()
    bob_str = "Bob"
    a23_str = "amy23"
    event300 = 300
    time5 = 5
    clean_fact = example_casa_clean_factunit()
    x_facts = [(clean_fact.fact_context, clean_fact.fact_state, None, None)]
    save_arbitrary_beliefevent(
        moment_mstr_dir, a23_str, bob_str, event300, facts=x_facts
    )
    yao_str = "Yao"
    das = [yao_str, bob_str]
    cellunit_add_json_file(moment_mstr_dir, a23_str, bob_str, time5, event300, das)
    bob5_cell_path = create_cell_json_path(
        moment_mstr_dir, a23_str, bob_str, time5, das
    )
    assert open_json(bob5_cell_path).get(beliefevent_facts_str()) == {}

    # WHEN
    load_cells_beliefevent(moment_mstr_dir, a23_str)

    # THEN
    expected_beliefevent_facts = {clean_fact.fact_context: clean_fact.to_dict()}
    assert (
        open_json(bob5_cell_path).get(beliefevent_facts_str())
        == expected_beliefevent_facts
    )
