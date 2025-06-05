from src.a00_data_toolbox.file_toolbox import create_path, delete_dir
from src.a05_concept_logic.concept import get_default_vow_label as root_label
from src.a06_bud_logic.bud import budunit_shop
from src.a12_hub_tools._test_util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a12_hub_tools.hub_path import create_job_path, create_vow_dir_path
from src.a12_hub_tools.hub_tool import job_file_exists, open_job_file, save_job_file
from src.a12_hub_tools.hubunit import hubunit_shop


def test_HubUnit_initialize_job_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    vow_mstr_dir = env_dir()
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(vow_mstr_dir, root_label(), sue_str, None)
    sue_bud = budunit_shop(sue_str, root_label())
    assert job_file_exists(vow_mstr_dir, root_label(), sue_str) is False

    # WHEN
    sue_hubunit.initialize_job_file(sue_bud)

    # THEN
    job = open_job_file(vow_mstr_dir, root_label(), sue_str)
    assert job.vow_label == root_label()
    assert job.owner_name == sue_str
    bob_str = "Bob"
    assert job.acct_exists(bob_str) is False

    # ESTABLISH
    sue_bud = budunit_shop(sue_str)
    sue_bud.add_acctunit(bob_str)
    save_job_file(vow_mstr_dir, sue_bud)
    job = open_job_file(vow_mstr_dir, root_label(), sue_str)
    assert job.get_acct(bob_str)

    # WHEN
    sue_hubunit.initialize_job_file(sue_bud)

    # THEN
    job = open_job_file(vow_mstr_dir, root_label(), sue_str)
    assert job.get_acct(bob_str)


def test_HubUnit_initialize_job_file_CorrectlyDoesNotOverwrite(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    vow_mstr_dir = env_dir()
    sue_vow_dir = create_path(vow_mstr_dir, root_label())
    sue_fund_pool = 50000
    sue_fund_iota = 5
    sue_bit = 25
    sue_hubunit = hubunit_shop(
        vow_mstr_dir,
        root_label(),
        sue_str,
        None,
        fund_pool=sue_fund_pool,
        fund_iota=sue_fund_iota,
        respect_bit=sue_bit,
    )
    sue_bud = budunit_shop(
        sue_str,
        root_label(),
        fund_pool=sue_fund_pool,
        fund_iota=sue_fund_iota,
        respect_bit=sue_bit,
    )
    sue_hubunit.initialize_job_file(sue_bud)
    assert job_file_exists(vow_mstr_dir, root_label(), sue_str)
    sue_job_path = create_job_path(vow_mstr_dir, root_label(), sue_str)
    delete_dir(sue_job_path)
    assert job_file_exists(vow_mstr_dir, root_label(), sue_str) is False

    # WHEN
    bob_str = "Bob"
    sue_bud.add_acctunit(bob_str)
    sue_hubunit.initialize_job_file(sue_bud)

    # THEN
    assert job_file_exists(vow_mstr_dir, root_label(), sue_str)
    job = open_job_file(vow_mstr_dir, root_label(), sue_str)
    assert job.vow_label == root_label()
    assert job.owner_name == sue_str
    assert job.fund_pool == sue_fund_pool
    assert job.fund_iota == sue_fund_iota
    assert job.respect_bit == sue_bit


def test_HubUnit_initialize_job_file_CreatesDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    vow_mstr_dir = env_dir()
    sue_hubunit = hubunit_shop(vow_mstr_dir, root_label(), sue_str, None)
    vow_dir = create_vow_dir_path(vow_mstr_dir, root_label())
    delete_dir(vow_dir)
    assert job_file_exists(vow_mstr_dir, root_label(), sue_str) is False

    # WHEN
    sue_bud = budunit_shop(sue_str, root_label())
    sue_hubunit.initialize_job_file(sue_bud)

    # THEN
    assert job_file_exists(vow_mstr_dir, root_label(), sue_str)
