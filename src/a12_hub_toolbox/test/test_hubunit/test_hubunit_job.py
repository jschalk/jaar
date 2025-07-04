from src.a00_data_toolbox.file_toolbox import create_path, delete_dir
from src.a05_plan_logic.plan import get_default_belief_label as root_label
from src.a06_believer_logic.believer import believerunit_shop
from src.a12_hub_toolbox.a12_path import create_job_path
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
    sue_believer = believerunit_shop(sue_str, root_label())
    assert job_file_exists(belief_mstr_dir, root_label(), sue_str) is False

    # WHEN
    sue_hubunit.initialize_job_file(sue_believer)

    # THEN
    job = open_job_file(belief_mstr_dir, root_label(), sue_str)
    assert job.belief_label == root_label()
    assert job.believer_name == sue_str
    bob_str = "Bob"
    assert job.person_exists(bob_str) is False

    # ESTABLISH
    sue_believer = believerunit_shop(sue_str)
    sue_believer.add_personunit(bob_str)
    save_job_file(belief_mstr_dir, sue_believer)
    job = open_job_file(belief_mstr_dir, root_label(), sue_str)
    assert job.get_person(bob_str)

    # WHEN
    sue_hubunit.initialize_job_file(sue_believer)

    # THEN
    job = open_job_file(belief_mstr_dir, root_label(), sue_str)
    assert job.get_person(bob_str)


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
    sue_believer = believerunit_shop(
        sue_str,
        root_label(),
        fund_pool=sue_fund_pool,
        fund_iota=sue_fund_iota,
        respect_bit=sue_bit,
    )
    sue_hubunit.initialize_job_file(sue_believer)
    assert job_file_exists(belief_mstr_dir, root_label(), sue_str)
    sue_job_path = create_job_path(belief_mstr_dir, root_label(), sue_str)
    delete_dir(sue_job_path)
    assert job_file_exists(belief_mstr_dir, root_label(), sue_str) is False

    # WHEN
    bob_str = "Bob"
    sue_believer.add_personunit(bob_str)
    sue_hubunit.initialize_job_file(sue_believer)

    # THEN
    assert job_file_exists(belief_mstr_dir, root_label(), sue_str)
    job = open_job_file(belief_mstr_dir, root_label(), sue_str)
    assert job.belief_label == root_label()
    assert job.believer_name == sue_str
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
    sue_believer = believerunit_shop(sue_str, root_label())
    sue_hubunit.initialize_job_file(sue_believer)

    # THEN
    assert job_file_exists(belief_mstr_dir, root_label(), sue_str)
