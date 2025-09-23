from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch08_timeline_logic.test._util.calendar_examples import (
    five_str,
    get_five_config,
)
from src.ch08_timeline_logic.timeline_main import (
    get_default_timeline_config_dict,
    timelineunit_shop,
)
from src.ch12_hub_toolbox.hub_tool import open_gut_file, save_gut_file
from src.ch15_moment_logic._ref.ch15_keywords import time_str
from src.ch15_moment_logic.moment_main import momentunit_shop
from src.ch15_moment_logic.test._util.ch15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_MomentUnit_get_timeline_config_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_module_temp_dir()
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)

    # WHEN
    a23_timeline_config = a23_moment.get_timeline_config()

    # THEN
    assert a23_timeline_config == a23_moment.timeline.to_dict()
    assert a23_timeline_config == get_default_timeline_config_dict()
    assert a23_timeline_config.get("timeline_label") == "creg"


def test_MomentUnit_get_timeline_config_ReturnsObj_Scenario1(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_module_temp_dir()
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    a23_moment.timeline = timelineunit_shop(get_five_config())

    # WHEN
    a23_timeline_config = a23_moment.get_timeline_config()

    # THEN
    assert a23_timeline_config == a23_moment.timeline.to_dict()
    assert a23_timeline_config == get_five_config()
    assert a23_timeline_config.get("timeline_label") == "five"


def test_MomentUnit_add_timeline_to_gut_SetsFile_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_module_temp_dir()
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    a23_moment.timeline = timelineunit_shop(get_five_config())
    sue_str = "Sue"
    init_sue_gut = beliefunit_shop(sue_str, a23_str)
    time_rope = init_sue_gut.make_l1_rope(time_str())
    five_rope = init_sue_gut.make_rope(time_rope, five_str())
    save_gut_file(moment_mstr_dir, init_sue_gut)
    assert not init_sue_gut.plan_exists(five_rope)

    # WHEN
    a23_moment.add_timeline_to_gut(sue_str)

    # THEN
    post_sue_gut = open_gut_file(moment_mstr_dir, a23_str, sue_str)
    assert post_sue_gut.plan_exists(five_rope)


def test_MomentUnit_add_timeline_to_guts_SetsFiles_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_module_temp_dir()
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    a23_moment.timeline = timelineunit_shop(get_five_config())
    sue_str = "Sue"
    init_sue_gut = beliefunit_shop(sue_str, a23_str)
    time_rope = init_sue_gut.make_l1_rope(time_str())
    five_rope = init_sue_gut.make_rope(time_rope, five_str())
    save_gut_file(moment_mstr_dir, init_sue_gut)
    assert not init_sue_gut.plan_exists(five_rope)

    # WHEN
    a23_moment.add_timeline_to_guts()

    # THEN
    post_sue_gut = open_gut_file(moment_mstr_dir, a23_str, sue_str)
    assert post_sue_gut.plan_exists(five_rope)
