from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import delete_dir
from src.ch14_keep_logic.riverrun import riverrun_shop
from src.ch14_keep_logic.test._util.ch14_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch14_keep_logic.test._util.ch14_examples import example_yao_texas_hubunit


def test_RiverRun_save_rivergrade_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH / WHEN
    yao_hubunit = example_yao_texas_hubunit()
    yao_str = "Yao"
    yao_voice_cred_lumen = 500
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, yao_voice_cred_lumen)
    x_riverrun.set_tax_dues({yao_str: 1})
    x_riverrun.calc_metrics()
    print(f"{x_riverrun.hubunit.grade_path(yao_str)=}")
    assert os_path_exists(x_riverrun.hubunit.grade_path(yao_str)) is False

    # WHEN
    x_riverrun._save_rivergrade_file(yao_str)

    # THEN
    assert os_path_exists(x_riverrun.hubunit.grade_path(yao_str))


def test_RiverRun_save_rivergrade_files_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH / WHEN
    delete_dir(get_chapter_temp_dir())
    github_error_path1 = "src\\ch14_keep_logic\\test\\_util\\moment_mstr\\moments/moments/ex_keep04/beliefs/Yao/keeps/nation/usa/texas/grades/Yao.json"
    assert os_path_exists(github_error_path1) is False
    yao_hubunit = example_yao_texas_hubunit()
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_voice_cred_lumen = 500
    x_riverrun = riverrun_shop(yao_hubunit)
    assert os_path_exists(x_riverrun.hubunit.grade_path(yao_str)) is False
    assert os_path_exists(x_riverrun.hubunit.grade_path(bob_str)) is False
    assert os_path_exists(x_riverrun.hubunit.grade_path(sue_str)) is False
    x_riverrun.set_keep_credorledger(yao_str, yao_str, yao_voice_cred_lumen)
    x_riverrun.set_keep_credorledger(yao_str, bob_str, 1)
    x_riverrun.set_tax_dues({yao_str: 1, sue_str: 1})
    x_riverrun.calc_metrics()
    assert os_path_exists(x_riverrun.hubunit.grade_path(yao_str)) is False
    assert os_path_exists(x_riverrun.hubunit.grade_path(bob_str)) is False
    assert os_path_exists(x_riverrun.hubunit.grade_path(sue_str)) is False

    # WHEN
    x_riverrun.save_rivergrade_files()

    # THEN
    assert os_path_exists(x_riverrun.hubunit.grade_path(yao_str))
    assert os_path_exists(x_riverrun.hubunit.grade_path(bob_str))
    # assert os_path_exists(x_riverrun.hubunit.grade_path(sue_str))
