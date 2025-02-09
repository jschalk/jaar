from src.f06_keep.riverrun import riverrun_shop
from src.f06_keep.examples.keep_env import env_dir_setup_cleanup
from src.f06_keep.examples.example_credorledgers import example_yao_texas_hubunit
from os.path import exists as os_path_exists


def test_RiverRun_save_rivergrade_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH / WHEN
    yao_hubunit = example_yao_texas_hubunit()
    yao_str = "Yao"
    yao_credit_belief = 500
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, yao_credit_belief)
    x_riverrun.set_tax_dues({yao_str: 1})
    x_riverrun.calc_metrics()
    print(f"{x_riverrun.hubunit.grade_path(yao_str)=}")
    assert os_path_exists(x_riverrun.hubunit.grade_path(yao_str)) is False

    # WHEN
    x_riverrun._save_rivergrade_file(yao_str)

    # THEN
    assert os_path_exists(x_riverrun.hubunit.grade_path(yao_str))


def test_RiverRun_save_rivergrade_files_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH / WHEN
    yao_hubunit = example_yao_texas_hubunit()
    yao_str = "Yao"
    bob_str = "Bob"
    sue_str = "Sue"
    yao_credit_belief = 500
    x_riverrun = riverrun_shop(yao_hubunit)
    x_riverrun.set_keep_credorledger(yao_str, yao_str, yao_credit_belief)
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
