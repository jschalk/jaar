from os.path import exists as os_path_exists
from src.ch00_data_toolbox.file_toolbox import create_path, open_file, save_file
from src.ch07_belief_logic.belief_main import (
    beliefunit_shop,
    get_from_json as beliefunit_get_from_json,
)
from src.ch12_hub_toolbox.ch12_path import create_belief_event_dir_path, create_gut_path
from src.ch18_etl_toolbox.test._util.ch18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.ch18_etl_toolbox.transformers import (
    etl_event_inherited_beliefunits_to_moment_gut,
)

# create test where event create_belief_event_dir_path()
# test that budunit with depth 0 is able to create
# test that budunit with depth 1 is able to create nested beliefunits directories and populate with event relevant


def test_etl_event_inherited_beliefunits_to_moment_gut_SetsFiles_Scenario0(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    event3 = 3
    event7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_str = "amy23"
    moment_mstr_dir = get_module_temp_dir()
    a23_bob_e3_dir = create_belief_event_dir_path(
        moment_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_dir = create_belief_event_dir_path(
        moment_mstr_dir, a23_str, bob_inx, event7
    )
    belief_filename = "belief.json"
    e3_bob_belief = beliefunit_shop(bob_inx, a23_str)
    e7_bob_belief = beliefunit_shop(bob_inx, a23_str)
    e3_bob_belief.add_voiceunit(bob_inx, credit77)
    e3_bob_belief.add_voiceunit(yao_inx, credit44)
    e7_bob_belief.add_voiceunit(bob_inx, credit77)
    e7_bob_belief.add_voiceunit(sue_inx, credit88)
    e7_bob_belief.add_voiceunit(yao_inx, credit44)
    save_file(a23_bob_e3_dir, belief_filename, e3_bob_belief.get_json())
    save_file(a23_bob_e7_dir, belief_filename, e7_bob_belief.get_json())
    e3_belief_path = create_path(a23_bob_e3_dir, belief_filename)
    e7_belief_path = create_path(a23_bob_e7_dir, belief_filename)
    assert os_path_exists(e3_belief_path)
    assert os_path_exists(e7_belief_path)
    print(e3_belief_path)
    print(e7_belief_path)
    a23_bob_gut_path = create_gut_path(moment_mstr_dir, a23_str, bob_inx)
    assert os_path_exists(a23_bob_gut_path) is False

    # WHEN
    etl_event_inherited_beliefunits_to_moment_gut(moment_mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_gut_path)
    generated_gut_belief = beliefunit_get_from_json(open_file(a23_bob_gut_path))
    assert generated_gut_belief.voices == e7_bob_belief.voices
    assert generated_gut_belief == e7_bob_belief
    assert generated_gut_belief.to_dict() == e7_bob_belief.to_dict()
