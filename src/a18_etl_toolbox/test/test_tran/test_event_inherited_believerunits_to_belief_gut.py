from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_file, save_file
from src.a06_believer_logic.believer import (
    believerunit_shop,
    get_from_json as believerunit_get_from_json,
)
from src.a12_hub_toolbox.hub_path import create_believer_event_dir_path, create_gut_path
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.transformers import (
    etl_event_inherited_believerunits_to_belief_gut,
)

# create test where event create_believer_event_dir_path()
# test that budunit with depth 0 is able to create
# test that budunit with depth 1 is able to create nested believerunits directories and populate with event relevant


def test_etl_event_inherited_believerunits_to_belief_gut_SetsFiles_Scenario0(
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
    belief_mstr_dir = get_module_temp_dir()
    a23_bob_e3_dir = create_believer_event_dir_path(
        belief_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_dir = create_believer_event_dir_path(
        belief_mstr_dir, a23_str, bob_inx, event7
    )
    believer_filename = "believer.json"
    e3_bob_believer = believerunit_shop(bob_inx, a23_str)
    e7_bob_believer = believerunit_shop(bob_inx, a23_str)
    e3_bob_believer.add_personunit(bob_inx, credit77)
    e3_bob_believer.add_personunit(yao_inx, credit44)
    e7_bob_believer.add_personunit(bob_inx, credit77)
    e7_bob_believer.add_personunit(sue_inx, credit88)
    e7_bob_believer.add_personunit(yao_inx, credit44)
    save_file(a23_bob_e3_dir, believer_filename, e3_bob_believer.get_json())
    save_file(a23_bob_e7_dir, believer_filename, e7_bob_believer.get_json())
    e3_believer_path = create_path(a23_bob_e3_dir, believer_filename)
    e7_believer_path = create_path(a23_bob_e7_dir, believer_filename)
    assert os_path_exists(e3_believer_path)
    assert os_path_exists(e7_believer_path)
    print(e3_believer_path)
    print(e7_believer_path)
    a23_bob_gut_path = create_gut_path(belief_mstr_dir, a23_str, bob_inx)
    assert os_path_exists(a23_bob_gut_path) is False

    # WHEN
    etl_event_inherited_believerunits_to_belief_gut(belief_mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_gut_path)
    generated_gut_believer = believerunit_get_from_json(open_file(a23_bob_gut_path))
    assert generated_gut_believer.persons == e7_bob_believer.persons
    assert generated_gut_believer == e7_bob_believer
    assert generated_gut_believer.get_dict() == e7_bob_believer.get_dict()
