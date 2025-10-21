from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import create_path, open_json, save_json
from src.ch07_belief_logic.belief_main import beliefunit_shop, get_beliefunit_from_dict
from src.ch10_lesson._ref.ch10_path import create_gut_path
from src.ch11_bud._ref.ch11_path import create_belief_spark_dir_path
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ch18_world_etl.transformers import (
    etl_spark_inherited_beliefunits_to_moment_gut,
)

# create test where spark create_belief_spark_dir_path()
# test that budunit with depth 0 is able to create
# test that budunit with depth 1 is able to create nested beliefunits directories and populate with spark relevant


def test_etl_spark_inherited_beliefunits_to_moment_gut_SetsFiles_Scenario0(
    temp_dir_setup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    spark3 = 3
    spark7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_str = "amy23"
    moment_mstr_dir = get_temp_dir()
    a23_bob_e3_dir = create_belief_spark_dir_path(
        moment_mstr_dir, a23_str, bob_inx, spark3
    )
    a23_bob_e7_dir = create_belief_spark_dir_path(
        moment_mstr_dir, a23_str, bob_inx, spark7
    )
    belief_filename = "belief.json"
    e3_bob_belief = beliefunit_shop(bob_inx, a23_str)
    e7_bob_belief = beliefunit_shop(bob_inx, a23_str)
    e3_bob_belief.add_voiceunit(bob_inx, credit77)
    e3_bob_belief.add_voiceunit(yao_inx, credit44)
    e7_bob_belief.add_voiceunit(bob_inx, credit77)
    e7_bob_belief.add_voiceunit(sue_inx, credit88)
    e7_bob_belief.add_voiceunit(yao_inx, credit44)
    save_json(a23_bob_e3_dir, belief_filename, e3_bob_belief.to_dict())
    save_json(a23_bob_e7_dir, belief_filename, e7_bob_belief.to_dict())
    e3_belief_path = create_path(a23_bob_e3_dir, belief_filename)
    e7_belief_path = create_path(a23_bob_e7_dir, belief_filename)
    assert os_path_exists(e3_belief_path)
    assert os_path_exists(e7_belief_path)
    print(e3_belief_path)
    print(e7_belief_path)
    a23_bob_gut_path = create_gut_path(moment_mstr_dir, a23_str, bob_inx)
    assert os_path_exists(a23_bob_gut_path) is False

    # WHEN
    etl_spark_inherited_beliefunits_to_moment_gut(moment_mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_gut_path)
    generated_gut_belief = get_beliefunit_from_dict(open_json(a23_bob_gut_path))
    assert generated_gut_belief.voices == e7_bob_belief.voices
    assert generated_gut_belief == e7_bob_belief
    assert generated_gut_belief.to_dict() == e7_bob_belief.to_dict()
