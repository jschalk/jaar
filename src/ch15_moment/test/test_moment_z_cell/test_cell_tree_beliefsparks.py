from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import open_json
from src.ch10_bud._ref.ch10_path import create_beliefspark_path, create_cell_json_path
from src.ch10_bud.bud_filehandler import (
    cellunit_add_json_file,
    save_arbitrary_beliefspark,
)
from src.ch15_moment.moment_cell import load_cells_beliefspark
from src.ch15_moment.test._util.ch15_env import get_temp_dir, temp_dir_setup
from src.ch15_moment.test._util.ch15_examples import example_casa_floor_clean_factunit
from src.ref.keywords import Ch15Keywords as kw


def test_load_cells_beliefspark_SetsFiles_Scenario0_NoFacts(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    bob_str = "Bob"
    a23_str = "amy23"
    spark300 = 300
    time5 = 5
    save_arbitrary_beliefspark(moment_mstr_dir, a23_str, bob_str, spark300)
    bob3_beliefspark_path = create_beliefspark_path(
        moment_mstr_dir, a23_str, bob_str, spark300
    )
    print(f"{bob3_beliefspark_path=}")
    cellunit_add_json_file(moment_mstr_dir, a23_str, bob_str, time5, spark300, [])
    bob5_cell_path = create_cell_json_path(moment_mstr_dir, a23_str, bob_str, time5)
    assert open_json(bob5_cell_path).get(kw.beliefspark_facts) == {}

    # WHEN
    load_cells_beliefspark(moment_mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob5_cell_path)
    assert open_json(bob5_cell_path).get(kw.beliefspark_facts) == {}


def test_load_cells_beliefspark_SetsFiles_Scenario1_WithFacts(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    bob_str = "Bob"
    a23_str = "amy23"
    spark300 = 300
    time5 = 5
    clean_fact = example_casa_floor_clean_factunit()
    x_facts = [clean_fact.get_tuple()]
    save_arbitrary_beliefspark(
        moment_mstr_dir, a23_str, bob_str, spark300, facts=x_facts
    )
    bob3_beliefspark_path = create_beliefspark_path(
        moment_mstr_dir, a23_str, bob_str, spark300
    )
    print(f"{bob3_beliefspark_path=}")
    cellunit_add_json_file(moment_mstr_dir, a23_str, bob_str, time5, spark300, [])
    bob5_cell_path = create_cell_json_path(moment_mstr_dir, a23_str, bob_str, time5)
    assert open_json(bob5_cell_path).get(kw.beliefspark_facts) == {}

    # WHEN
    load_cells_beliefspark(moment_mstr_dir, a23_str)

    # THEN
    expected_beliefspark_facts = {clean_fact.fact_context: clean_fact.to_dict()}
    assert (
        open_json(bob5_cell_path).get(kw.beliefspark_facts)
        == expected_beliefspark_facts
    )


def test_load_cells_beliefspark_SetsFiles_Scenario2_WithFacts_NotAtRoot(
    temp_dir_setup,
):
    # ESTABLISH
    moment_mstr_dir = get_temp_dir()
    bob_str = "Bob"
    a23_str = "amy23"
    spark300 = 300
    time5 = 5
    clean_fact = example_casa_floor_clean_factunit()
    x_facts = [(clean_fact.fact_context, clean_fact.fact_state, None, None)]
    save_arbitrary_beliefspark(
        moment_mstr_dir, a23_str, bob_str, spark300, facts=x_facts
    )
    yao_str = "Yao"
    das = [yao_str, bob_str]
    cellunit_add_json_file(moment_mstr_dir, a23_str, bob_str, time5, spark300, das)
    bob5_cell_path = create_cell_json_path(
        moment_mstr_dir, a23_str, bob_str, time5, das
    )
    assert open_json(bob5_cell_path).get(kw.beliefspark_facts) == {}

    # WHEN
    load_cells_beliefspark(moment_mstr_dir, a23_str)

    # THEN
    expected_beliefspark_facts = {clean_fact.fact_context: clean_fact.to_dict()}
    assert (
        open_json(bob5_cell_path).get(kw.beliefspark_facts)
        == expected_beliefspark_facts
    )
