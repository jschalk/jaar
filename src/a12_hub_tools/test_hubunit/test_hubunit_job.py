from src.a00_data_toolboxs.file_toolbox import delete_dir, create_path
from src.a01_word_logic.road import get_default_fisc_title as root_title
from src.a06_bud_logic.bud import budunit_shop
from src.a12_hub_tools.hub_path import create_job_path, create_fisc_dir_path
from src.a12_hub_tools.hub_tool import (
    save_job_file,
    open_job_file,
    job_file_exists,
)
from src.a12_hub_tools.hubunit import hubunit_shop
from src.a13_bud_listen_logic.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)


def test_HubUnit_initialize_job_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    fisc_mstr_dir = env_dir()
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(fisc_mstr_dir, root_title(), sue_str, None)
    sue_bud = budunit_shop(sue_str, root_title())
    assert job_file_exists(fisc_mstr_dir, root_title(), sue_str) is False

    # WHEN
    sue_hubunit.initialize_job_file(sue_bud)

    # THEN
    job = open_job_file(fisc_mstr_dir, root_title(), sue_str)
    assert job.fisc_title == root_title()
    assert job.owner_name == sue_str
    bob_str = "Bob"
    assert job.acct_exists(bob_str) is False

    # ESTABLISH
    sue_bud = budunit_shop(sue_str)
    sue_bud.add_acctunit(bob_str)
    save_job_file(fisc_mstr_dir, sue_bud)
    job = open_job_file(fisc_mstr_dir, root_title(), sue_str)
    assert job.get_acct(bob_str)

    # WHEN
    sue_hubunit.initialize_job_file(sue_bud)

    # THEN
    job = open_job_file(fisc_mstr_dir, root_title(), sue_str)
    assert job.get_acct(bob_str)


def test_HubUnit_initialize_job_file_CorrectlyDoesNotOverwrite(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    fisc_mstr_dir = env_dir()
    sue_fisc_dir = create_path(fisc_mstr_dir, root_title())
    sue_fund_pool = 50000
    sue_fund_coin = 5
    sue_bit = 25
    sue_hubunit = hubunit_shop(
        fisc_mstr_dir,
        root_title(),
        sue_str,
        None,
        fund_pool=sue_fund_pool,
        fund_coin=sue_fund_coin,
        respect_bit=sue_bit,
    )
    sue_bud = budunit_shop(
        sue_str,
        root_title(),
        fund_pool=sue_fund_pool,
        fund_coin=sue_fund_coin,
        respect_bit=sue_bit,
    )
    sue_hubunit.initialize_job_file(sue_bud)
    assert job_file_exists(fisc_mstr_dir, root_title(), sue_str)
    sue_job_path = create_job_path(fisc_mstr_dir, root_title(), sue_str)
    delete_dir(sue_job_path)
    assert job_file_exists(fisc_mstr_dir, root_title(), sue_str) is False

    # WHEN
    bob_str = "Bob"
    sue_bud.add_acctunit(bob_str)
    sue_hubunit.initialize_job_file(sue_bud)

    # THEN
    assert job_file_exists(fisc_mstr_dir, root_title(), sue_str)
    job = open_job_file(fisc_mstr_dir, root_title(), sue_str)
    assert job.fisc_title == root_title()
    assert job.owner_name == sue_str
    assert job.fund_pool == sue_fund_pool
    assert job.fund_coin == sue_fund_coin
    assert job.respect_bit == sue_bit


def test_HubUnit_initialize_job_file_CreatesDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    fisc_mstr_dir = env_dir()
    sue_hubunit = hubunit_shop(fisc_mstr_dir, root_title(), sue_str, None)
    fisc_dir = create_fisc_dir_path(fisc_mstr_dir, root_title())
    delete_dir(fisc_dir)
    assert job_file_exists(fisc_mstr_dir, root_title(), sue_str) is False

    # WHEN
    sue_bud = budunit_shop(sue_str, root_title())
    sue_hubunit.initialize_job_file(sue_bud)

    # THEN
    assert job_file_exists(fisc_mstr_dir, root_title(), sue_str)
