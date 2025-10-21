from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch08_epoch.epoch_main import epochunit_shop, get_default_epoch_config_dict
from src.ch08_epoch.test._util.ch08_examples import get_five_config
from src.ch10_lesson.lesson_filehandler import open_gut_file, save_gut_file
from src.ch15_moment.moment_main import momentunit_shop
from src.ch15_moment.test._util.ch15_env import get_temp_dir, temp_dir_setup
from src.ref.keywords import Ch15Keywords as kw


def test_MomentUnit_get_epoch_config_ReturnsObj_Scenario0(temp_dir_setup):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)

    # WHEN
    a23_epoch_config = a23_moment.get_epoch_config()

    # THEN
    assert a23_epoch_config == a23_moment.epoch.to_dict()
    assert a23_epoch_config == get_default_epoch_config_dict()
    assert a23_epoch_config.get(kw.epoch_label) == "creg"


def test_MomentUnit_get_epoch_config_ReturnsObj_Scenario1(temp_dir_setup):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    a23_moment.epoch = epochunit_shop(get_five_config())

    # WHEN
    a23_epoch_config = a23_moment.get_epoch_config()

    # THEN
    assert a23_epoch_config == a23_moment.epoch.to_dict()
    assert a23_epoch_config == get_five_config()
    assert a23_epoch_config.get(kw.epoch_label) == "five"


def test_MomentUnit_add_epoch_to_gut_SetsFile_Scenario0(temp_dir_setup):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    a23_moment.epoch = epochunit_shop(get_five_config())
    sue_str = "Sue"
    init_sue_gut = beliefunit_shop(sue_str, a23_str)
    time_rope = init_sue_gut.make_l1_rope(kw.time)
    five_rope = init_sue_gut.make_rope(time_rope, kw.five)
    save_gut_file(moment_mstr_dir, init_sue_gut)
    assert not init_sue_gut.plan_exists(five_rope)

    # WHEN
    a23_moment.add_epoch_to_gut(sue_str)

    # THEN
    post_sue_gut = open_gut_file(moment_mstr_dir, a23_str, sue_str)
    assert post_sue_gut.plan_exists(five_rope)


def test_MomentUnit_add_epoch_to_guts_SetsFiles_Scenario0(temp_dir_setup):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_temp_dir()
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    a23_moment.epoch = epochunit_shop(get_five_config())
    sue_str = "Sue"
    init_sue_gut = beliefunit_shop(sue_str, a23_str)
    time_rope = init_sue_gut.make_l1_rope(kw.time)
    five_rope = init_sue_gut.make_rope(time_rope, kw.five)
    save_gut_file(moment_mstr_dir, init_sue_gut)
    assert not init_sue_gut.plan_exists(five_rope)

    # WHEN
    a23_moment.add_epoch_to_guts()

    # THEN
    post_sue_gut = open_gut_file(moment_mstr_dir, a23_str, sue_str)
    assert post_sue_gut.plan_exists(five_rope)
