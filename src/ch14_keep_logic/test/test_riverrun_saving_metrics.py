from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import delete_dir
from src.ch12_belief_file_toolbox.ch12_path import create_keep_grade_path
from src.ch14_keep_logic.riverrun import riverrun_shop
from src.ch14_keep_logic.test._util.ch14_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch14_keep_logic.test._util.ch14_examples import (
    get_chapter_temp_dir,
    get_nation_texas_rope,
    temp_moment_label,
)


def test_RiverRun_save_rivergrade_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH / WHEN
    mstr_dir = get_chapter_temp_dir()
    a23_str = temp_moment_label()
    texas_rope = get_nation_texas_rope()
    yao_str = "Yao"
    yao_voice_cred_lumen = 500
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str, texas_rope)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, yao_voice_cred_lumen)
    x_riverrun.set_tax_dues({yao_str: 1})
    x_riverrun.calc_metrics()
    yao_keep_grade_path = create_keep_grade_path(
        moment_mstr_dir=x_riverrun.moment_mstr_dir,
        belief_name=x_riverrun.belief_name,
        moment_label=x_riverrun.moment_label,
        keep_rope=x_riverrun.keep_rope,
        knot=x_riverrun.knot,
        grade_belief_name=yao_str,
    )
    print(f"{yao_keep_grade_path=}")
    assert os_path_exists(yao_keep_grade_path) is False

    # WHEN
    x_riverrun._save_rivergrade_file(yao_str)

    # THEN
    assert os_path_exists(yao_keep_grade_path)


def test_RiverRun_save_rivergrade_files_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH / WHEN
    delete_dir(get_chapter_temp_dir())
    github_error_path1 = "src\\ch14_keep_logic\\test\\_util\\moment_mstr\\moments/moments/ex_keep04/beliefs/Yao/keeps/nation/usa/texas/grades/Yao.json"
    assert os_path_exists(github_error_path1) is False
    mstr_dir = get_chapter_temp_dir()
    a23_str = temp_moment_label()
    texas_rope = get_nation_texas_rope()
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_voice_cred_lumen = 500
    x_riverrun = riverrun_shop(mstr_dir, a23_str, yao_str, texas_rope)
    yao_keep_grade_path = create_keep_grade_path(
        moment_mstr_dir=x_riverrun.moment_mstr_dir,
        belief_name=x_riverrun.belief_name,
        moment_label=x_riverrun.moment_label,
        keep_rope=x_riverrun.keep_rope,
        knot=x_riverrun.knot,
        grade_belief_name=yao_str,
    )
    bob_keep_grade_path = create_keep_grade_path(
        moment_mstr_dir=x_riverrun.moment_mstr_dir,
        belief_name=x_riverrun.belief_name,
        moment_label=x_riverrun.moment_label,
        keep_rope=x_riverrun.keep_rope,
        knot=x_riverrun.knot,
        grade_belief_name=bob_str,
    )
    sue_keep_grade_path = create_keep_grade_path(
        moment_mstr_dir=x_riverrun.moment_mstr_dir,
        belief_name=x_riverrun.belief_name,
        moment_label=x_riverrun.moment_label,
        keep_rope=x_riverrun.keep_rope,
        knot=x_riverrun.knot,
        grade_belief_name=sue_str,
    )
    assert os_path_exists(yao_keep_grade_path) is False
    assert os_path_exists(bob_keep_grade_path) is False
    assert os_path_exists(sue_keep_grade_path) is False
    x_riverrun.set_keep_credorledger(yao_str, yao_str, yao_voice_cred_lumen)
    x_riverrun.set_keep_credorledger(yao_str, bob_str, 1)
    x_riverrun.set_tax_dues({yao_str: 1, sue_str: 1})
    x_riverrun.calc_metrics()
    assert os_path_exists(yao_keep_grade_path) is False
    assert os_path_exists(bob_keep_grade_path) is False
    assert os_path_exists(sue_keep_grade_path) is False

    # WHEN
    x_riverrun.save_rivergrade_files()

    # THEN
    assert os_path_exists(yao_keep_grade_path)
    assert os_path_exists(bob_keep_grade_path)
    # assert os_path_exists(x_riverrun.grade_path(sue_str))
