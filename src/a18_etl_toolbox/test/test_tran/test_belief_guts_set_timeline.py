from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import save_json
from src.a06_plan_logic.plan import planunit_shop
from src.a07_timeline_logic.test._util.a07_str import time_str
from src.a07_timeline_logic.test._util.calendar_examples import (
    five_str,
    get_five_config,
)
from src.a07_timeline_logic.timeline import timelineunit_shop
from src.a12_hub_toolbox.hub_path import create_belief_json_path
from src.a12_hub_toolbox.hub_tool import open_gut_file, save_gut_file
from src.a15_belief_logic.belief import beliefunit_shop
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.transformers import add_belief_timeline_to_guts


def test_add_belief_timeline_to_guts_SetsFiles_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    belief_mstr_dir = get_module_temp_dir()
    a23_belief = beliefunit_shop(a23_str, belief_mstr_dir)
    a23_belief.timeline = timelineunit_shop(get_five_config())
    belief_json_path = create_belief_json_path(belief_mstr_dir, a23_str)
    save_json(belief_json_path, None, a23_belief.get_dict())
    assert os_path_exists(belief_json_path)
    sue_str = "Sue"
    init_sue_gut = planunit_shop(sue_str, a23_str)
    time_rope = init_sue_gut.make_l1_rope(time_str())
    five_rope = init_sue_gut.make_rope(time_rope, five_str())
    save_gut_file(belief_mstr_dir, init_sue_gut)
    assert not init_sue_gut.concept_exists(five_rope)

    # WHEN
    add_belief_timeline_to_guts(belief_mstr_dir)

    # THEN
    post_sue_gut = open_gut_file(belief_mstr_dir, a23_str, sue_str)
    assert post_sue_gut.concept_exists(five_rope)
