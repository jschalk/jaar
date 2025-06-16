from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, open_file, save_file
from src.a06_plan_logic.plan import (
    get_from_json as planunit_get_from_json,
    planunit_shop,
)
from src.a12_hub_toolbox.hub_path import create_gut_path, create_owner_event_dir_path
from src.a18_etl_toolbox._test_util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.transformers import etl_event_inherited_planunits_to_vow_gut

# create test where event create_owner_event_dir_path()
# test that budunit with depth 0 is able to create
# test that budunit with depth 1 is able to create nested planunits directories and populate with event relevant


def test_etl_event_inherited_planunits_to_vow_gut_SetsFiles_Scenario0(
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
    a23_str = "accord23"
    vow_mstr_dir = get_module_temp_dir()
    a23_bob_e3_dir = create_owner_event_dir_path(vow_mstr_dir, a23_str, bob_inx, event3)
    a23_bob_e7_dir = create_owner_event_dir_path(vow_mstr_dir, a23_str, bob_inx, event7)
    plan_filename = "plan.json"
    e3_bob_plan = planunit_shop(bob_inx, a23_str)
    e7_bob_plan = planunit_shop(bob_inx, a23_str)
    e3_bob_plan.add_acctunit(bob_inx, credit77)
    e3_bob_plan.add_acctunit(yao_inx, credit44)
    e7_bob_plan.add_acctunit(bob_inx, credit77)
    e7_bob_plan.add_acctunit(sue_inx, credit88)
    e7_bob_plan.add_acctunit(yao_inx, credit44)
    save_file(a23_bob_e3_dir, plan_filename, e3_bob_plan.get_json())
    save_file(a23_bob_e7_dir, plan_filename, e7_bob_plan.get_json())
    e3_plan_path = create_path(a23_bob_e3_dir, plan_filename)
    e7_plan_path = create_path(a23_bob_e7_dir, plan_filename)
    assert os_path_exists(e3_plan_path)
    assert os_path_exists(e7_plan_path)
    print(e3_plan_path)
    print(e7_plan_path)
    a23_bob_gut_path = create_gut_path(vow_mstr_dir, a23_str, bob_inx)
    assert os_path_exists(a23_bob_gut_path) is False

    # WHEN
    etl_event_inherited_planunits_to_vow_gut(vow_mstr_dir)

    # THEN
    assert os_path_exists(a23_bob_gut_path)
    generated_gut_plan = planunit_get_from_json(open_file(a23_bob_gut_path))
    assert generated_gut_plan.accts == e7_bob_plan.accts
    assert generated_gut_plan == e7_bob_plan
    assert generated_gut_plan.get_dict() == e7_bob_plan.get_dict()
