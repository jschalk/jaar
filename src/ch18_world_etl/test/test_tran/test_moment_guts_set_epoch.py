from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import save_json
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch08_epoch.epoch_main import epochunit_shop
from src.ch08_epoch.test._util.ch08_examples import get_five_config
from src.ch10_pack._ref.ch10_path import create_moment_json_path
from src.ch10_pack.pack_filehandler import open_gut_file, save_gut_file
from src.ch15_moment.moment_main import momentunit_shop
from src.ch18_world_etl.test._util.ch18_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch18_world_etl.transformers import add_moment_epoch_to_guts
from src.ref.ch18_keywords import Ch18Keywords as wx


def test_add_moment_epoch_to_guts_SetsFiles_Scenario0(env_dir_setup_cleanup):
    # ESTABLISH
    a23_str = "amy23"
    moment_mstr_dir = get_chapter_temp_dir()
    a23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    a23_moment.epoch = epochunit_shop(get_five_config())
    moment_json_path = create_moment_json_path(moment_mstr_dir, a23_str)
    save_json(moment_json_path, None, a23_moment.to_dict())
    assert os_path_exists(moment_json_path)
    sue_str = "Sue"
    init_sue_gut = beliefunit_shop(sue_str, a23_str)
    time_rope = init_sue_gut.make_l1_rope(wx.time)
    five_rope = init_sue_gut.make_rope(time_rope, wx.five)
    save_gut_file(moment_mstr_dir, init_sue_gut)
    assert not init_sue_gut.plan_exists(five_rope)

    # WHEN
    add_moment_epoch_to_guts(moment_mstr_dir)

    # THEN
    post_sue_gut = open_gut_file(moment_mstr_dir, a23_str, sue_str)
    assert post_sue_gut.plan_exists(five_rope)
