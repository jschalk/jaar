from src.a00_data_toolbox.file_toolbox import create_path, delete_dir
from src.a05_concept_logic.concept import get_default_belief_label as root_label
from src.a06_owner_logic.owner import ownerunit_shop
from src.a12_hub_toolbox.hub_path import create_job_path
from src.a12_hub_toolbox.hub_tool import job_file_exists, open_job_file, save_job_file
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a12_hub_toolbox.test._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)


def test_HubUnit_initialize_job_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    belief_mstr_dir = env_dir()
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(belief_mstr_dir, root_label(), sue_str, None)
    sue_owner = ownerunit_shop(sue_str, root_label())
    assert job_file_exists(belief_mstr_dir, root_label(), sue_str) is False

    # WHEN
    sue_hubunit.initialize_job_file(sue_owner)

    # THEN
    job = open_job_file(belief_mstr_dir, root_label(), sue_str)
    assert job.belief_label == root_label()
    assert job.owner_name == sue_str
    bob_str = "Bob"
    assert job.acct_exists(bob_str) is False

    # ESTABLISH
    sue_owner = ownerunit_shop(sue_str)
    sue_owner.add_acctunit(bob_str)
    save_job_file(belief_mstr_dir, sue_owner)
    job = open_job_file(belief_mstr_dir, root_label(), sue_str)
    assert job.get_acct(bob_str)

    # WHEN
    sue_hubunit.initialize_job_file(sue_owner)

    # THEN
    job = open_job_file(belief_mstr_dir, root_label(), sue_str)
    assert job.get_acct(bob_str)


def test_HubUnit_initialize_job_file_CorrectlyDoesNotOverwrite(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    belief_mstr_dir = env_dir()
    sue_belief_dir = create_path(belief_mstr_dir, root_label())
    sue_fund_pool = 50000
    sue_fund_iota = 5
    sue_bit = 25
    sue_hubunit = hubunit_shop(
        belief_mstr_dir,
        root_label(),
        sue_str,
        None,
        fund_pool=sue_fund_pool,
        fund_iota=sue_fund_iota,
        respect_bit=sue_bit,
    )
    sue_owner = ownerunit_shop(
        sue_str,
        root_label(),
        fund_pool=sue_fund_pool,
        fund_iota=sue_fund_iota,
        respect_bit=sue_bit,
    )
    sue_hubunit.initialize_job_file(sue_owner)
    assert job_file_exists(belief_mstr_dir, root_label(), sue_str)
    sue_job_path = create_job_path(belief_mstr_dir, root_label(), sue_str)
    delete_dir(sue_job_path)
    assert job_file_exists(belief_mstr_dir, root_label(), sue_str) is False

    # WHEN
    bob_str = "Bob"
    sue_owner.add_acctunit(bob_str)
    sue_hubunit.initialize_job_file(sue_owner)

    # THEN
    assert job_file_exists(belief_mstr_dir, root_label(), sue_str)
    job = open_job_file(belief_mstr_dir, root_label(), sue_str)
    assert job.belief_label == root_label()
    assert job.owner_name == sue_str
    assert job.fund_pool == sue_fund_pool
    assert job.fund_iota == sue_fund_iota
    assert job.respect_bit == sue_bit


def test_HubUnit_initialize_job_file_CreatesDirsAndFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    belief_mstr_dir = env_dir()
    sue_hubunit = hubunit_shop(belief_mstr_dir, root_label(), sue_str, None)
    assert job_file_exists(belief_mstr_dir, root_label(), sue_str) is False

    # WHEN
    sue_owner = ownerunit_shop(sue_str, root_label())
    sue_hubunit.initialize_job_file(sue_owner)

    # THEN
    assert job_file_exists(belief_mstr_dir, root_label(), sue_str)
