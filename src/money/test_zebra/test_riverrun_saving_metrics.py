from src.money.riverrun import riverrun_shop
from src.money.examples.econ_env import env_dir_setup_cleanup
from src.money.examples.example_credorledgers import example_yao_texas_userhub
from os.path import exists as os_path_exists


def test_RiverRun_save_rivergrade_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN / WHEN
    yao_userhub = example_yao_texas_userhub()
    yao_text = "Yao"
    yao_credor_weight = 500
    x_riverrun = riverrun_shop(yao_userhub)
    x_riverrun.set_econ_credorledger(yao_text, yao_text, yao_credor_weight)
    x_riverrun.set_tax_dues({yao_text: 1})
    x_riverrun.calc_metrics()
    assert os_path_exists(x_riverrun.userhub.grade_path(yao_text)) is False

    # WHEN
    x_riverrun._save_rivergrade_file(yao_text)

    # THEN
    assert os_path_exists(x_riverrun.userhub.grade_path(yao_text))


def test_RiverRun_save_rivergrade_files_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN / WHEN
    yao_userhub = example_yao_texas_userhub()
    yao_text = "Yao"
    bob_text = "Bob"
    sue_text = "Sue"
    yao_credor_weight = 500
    x_riverrun = riverrun_shop(yao_userhub)
    x_riverrun.set_econ_credorledger(yao_text, yao_text, yao_credor_weight)
    x_riverrun.set_econ_credorledger(yao_text, bob_text, 1)
    x_riverrun.set_tax_dues({yao_text: 1, sue_text: 1})
    x_riverrun.calc_metrics()
    assert os_path_exists(x_riverrun.userhub.grade_path(yao_text)) is False
    assert os_path_exists(x_riverrun.userhub.grade_path(bob_text)) is False
    assert os_path_exists(x_riverrun.userhub.grade_path(sue_text)) is False

    # WHEN
    x_riverrun.save_rivergrade_files()

    # THEN
    assert os_path_exists(x_riverrun.userhub.grade_path(yao_text))
    assert os_path_exists(x_riverrun.userhub.grade_path(bob_text))
    # assert os_path_exists(x_riverrun.userhub.grade_path(sue_text))
