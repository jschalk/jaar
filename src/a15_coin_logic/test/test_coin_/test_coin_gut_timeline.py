from src.a00_data_toolbox.file_toolbox import set_dir
from src.a01_term_logic.rope import create_rope
from src.a06_believer_logic.believer_main import BelieverUnit, believerunit_shop
from src.a07_timeline_logic.test._util.a07_str import time_str
from src.a07_timeline_logic.test._util.calendar_examples import (
    five_str,
    get_five_config,
)
from src.a07_timeline_logic.timeline_main import (
    add_newtimeline_planunit,
    get_default_timeline_config_dict,
    timelineunit_shop,
)
from src.a12_hub_toolbox.a12_path import create_believer_dir_path
from src.a12_hub_toolbox.hub_tool import gut_file_exists, open_gut_file, save_gut_file
from src.a15_coin_logic.coin_main import coinunit_shop
from src.a15_coin_logic.test._util.a15_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_CoinUnit_get_timeline_config_ReturnsObj_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    coin_mstr_dir = get_module_temp_dir()
    a23_coin = coinunit_shop(a23_str, coin_mstr_dir)

    # WHEN
    a23_timeline_config = a23_coin.get_timeline_config()

    # THEN
    assert a23_timeline_config == a23_coin.timeline.to_dict()
    assert a23_timeline_config == get_default_timeline_config_dict()
    assert a23_timeline_config.get("timeline_label") == "creg"


def test_CoinUnit_get_timeline_config_ReturnsObj_Scenario1(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    coin_mstr_dir = get_module_temp_dir()
    a23_coin = coinunit_shop(a23_str, coin_mstr_dir)
    a23_coin.timeline = timelineunit_shop(get_five_config())

    # WHEN
    a23_timeline_config = a23_coin.get_timeline_config()

    # THEN
    assert a23_timeline_config == a23_coin.timeline.to_dict()
    assert a23_timeline_config == get_five_config()
    assert a23_timeline_config.get("timeline_label") == "five"


def test_CoinUnit_add_timeline_to_gut_SetsFile_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    coin_mstr_dir = get_module_temp_dir()
    a23_coin = coinunit_shop(a23_str, coin_mstr_dir)
    a23_coin.timeline = timelineunit_shop(get_five_config())
    sue_str = "Sue"
    init_sue_gut = believerunit_shop(sue_str, a23_str)
    time_rope = init_sue_gut.make_l1_rope(time_str())
    five_rope = init_sue_gut.make_rope(time_rope, five_str())
    save_gut_file(coin_mstr_dir, init_sue_gut)
    assert not init_sue_gut.plan_exists(five_rope)

    # WHEN
    a23_coin.add_timeline_to_gut(sue_str)

    # THEN
    post_sue_gut = open_gut_file(coin_mstr_dir, a23_str, sue_str)
    assert post_sue_gut.plan_exists(five_rope)


def test_CoinUnit_add_timeline_to_guts_SetsFiles_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    coin_mstr_dir = get_module_temp_dir()
    a23_coin = coinunit_shop(a23_str, coin_mstr_dir)
    a23_coin.timeline = timelineunit_shop(get_five_config())
    sue_str = "Sue"
    init_sue_gut = believerunit_shop(sue_str, a23_str)
    time_rope = init_sue_gut.make_l1_rope(time_str())
    five_rope = init_sue_gut.make_rope(time_rope, five_str())
    save_gut_file(coin_mstr_dir, init_sue_gut)
    assert not init_sue_gut.plan_exists(five_rope)

    # WHEN
    a23_coin.add_timeline_to_guts()

    # THEN
    post_sue_gut = open_gut_file(coin_mstr_dir, a23_str, sue_str)
    assert post_sue_gut.plan_exists(five_rope)
