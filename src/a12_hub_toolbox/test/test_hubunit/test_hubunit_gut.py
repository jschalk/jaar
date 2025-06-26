from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, delete_dir
from src.a09_pack_logic.pack import init_pack_id
from src.a12_hub_toolbox.hub_tool import (
    create_gut_path,
    gut_file_exists,
    open_gut_file,
    save_gut_file,
)
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a12_hub_toolbox.test._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as env_dir,
)
from src.a12_hub_toolbox.test._util.example_hub_atoms import sue_2planatoms_packunit


def test_HubUnit_default_gut_plan_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    slash_str = "/"
    x_fund_pool = 9000000
    pnine_float = 0.9
    pfour_float = 0.4
    sue_hubunit = hubunit_shop(
        env_dir(),
        "amy23",
        sue_str,
        keep_rope=None,
        knot=slash_str,
        fund_pool=x_fund_pool,
        fund_iota=pnine_float,
        respect_bit=pnine_float,
        penny=pfour_float,
    )

    # WHEN
    sue_default_gut = sue_hubunit.default_gut_plan()

    # THEN
    assert sue_default_gut.belief_label == sue_hubunit.belief_label
    assert sue_default_gut.owner_name == sue_hubunit.owner_name
    assert sue_default_gut.knot == sue_hubunit.knot
    assert sue_default_gut.fund_pool == sue_hubunit.fund_pool
    assert sue_default_gut.fund_iota == sue_hubunit.fund_iota
    assert sue_default_gut.respect_bit == sue_hubunit.respect_bit
    assert sue_default_gut.penny == sue_hubunit.penny
    assert sue_default_gut.last_pack_id == init_pack_id()


def test_HubUnit_create_initial_pack_files_from_default_CorrectlySavesPackUnitFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "amy23", sue_str)
    init_pack_filename = sue_hubunit.pack_filename(init_pack_id())
    init_pack_file_path = create_path(sue_hubunit._packs_dir, init_pack_filename)
    assert os_path_exists(init_pack_file_path) is False
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False

    # WHEN
    sue_hubunit._create_initial_pack_files_from_default()

    # THEN
    assert os_path_exists(init_pack_file_path)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False


def test_HubUnit_create_gut_from_packs_CreatesgutFileFromPackFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "amy23", sue_str)
    init_pack_filename = sue_hubunit.pack_filename(init_pack_id())
    init_pack_file_path = create_path(sue_hubunit._packs_dir, init_pack_filename)
    sue_hubunit._create_initial_pack_files_from_default()
    assert os_path_exists(init_pack_file_path)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False

    # WHEN
    sue_hubunit._create_gut_from_packs()

    # THEN
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    static_sue_gut = sue_hubunit._merge_any_packs(sue_hubunit.default_gut_plan())
    gut_plan = open_gut_file(env_dir(), "amy23", sue_str)
    assert gut_plan.get_dict() == static_sue_gut.get_dict()


def test_HubUnit_create_initial_pack_and_gut_files_CreatesPackFilesAndgutFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "amy23", sue_str)
    init_pack_filename = sue_hubunit.pack_filename(init_pack_id())
    init_pack_file_path = create_path(sue_hubunit._packs_dir, init_pack_filename)
    assert os_path_exists(init_pack_file_path) is False
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False

    # WHEN
    sue_hubunit._create_initial_pack_and_gut_files()

    # THEN
    assert os_path_exists(init_pack_file_path)
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    static_sue_gut = sue_hubunit._merge_any_packs(sue_hubunit.default_gut_plan())
    gut_plan = open_gut_file(env_dir(), "amy23", sue_str)
    assert gut_plan.get_dict() == static_sue_gut.get_dict()


def test_HubUnit_create_initial_pack_files_from_gut_SavesOnlyPackFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "amy23", sue_str)
    sue_gut_plan = sue_hubunit.default_gut_plan()
    bob_str = "Bob"
    sue_gut_plan.add_acctunit(bob_str)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False
    save_gut_file(env_dir(), sue_gut_plan)
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    init_pack_file_path = create_path(sue_hubunit._packs_dir, f"{init_pack_id()}.json")
    assert os_path_exists(init_pack_file_path) is False

    # WHEN
    sue_hubunit._create_initial_pack_files_from_gut()

    # THEN
    assert os_path_exists(init_pack_file_path)


def test_HubUnit_initialize_pack_gut_files_CorrectlySavesgutFileAndPackFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(env_dir(), "amy23", sue_str, respect_bit=seven_int)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False
    init_pack_file_path = create_path(sue_hubunit._packs_dir, f"{init_pack_id()}.json")
    delete_dir(sue_hubunit._packs_dir)
    assert os_path_exists(init_pack_file_path) is False

    # WHEN
    sue_hubunit.initialize_pack_gut_files()

    # THEN
    gut_plan = open_gut_file(env_dir(), "amy23", sue_str)
    assert gut_plan.belief_label == "amy23"
    assert gut_plan.owner_name == sue_str
    assert gut_plan.respect_bit == seven_int
    assert os_path_exists(init_pack_file_path)


def test_HubUnit_initialize_pack_gut_files_CorrectlySavesOnlygutFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(env_dir(), "amy23", sue_str, respect_bit=seven_int)
    sue_hubunit.initialize_pack_gut_files()
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    gut_path = create_gut_path(env_dir(), "amy23", sue_str)
    delete_dir(gut_path)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False
    init_pack_file_path = create_path(sue_hubunit._packs_dir, f"{init_pack_id()}.json")
    assert os_path_exists(init_pack_file_path)

    # WHEN
    sue_hubunit.initialize_pack_gut_files()

    # THEN
    gut_plan = open_gut_file(env_dir(), "amy23", sue_str)
    assert gut_plan.belief_label == "amy23"
    assert gut_plan.owner_name == sue_str
    assert gut_plan.respect_bit == seven_int
    assert os_path_exists(init_pack_file_path)


def test_HubUnit_initialize_pack_gut_files_CorrectlySavesOnlyPackFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_hubunit = hubunit_shop(env_dir(), "amy23", sue_str, respect_bit=seven_int)
    sue_hubunit.initialize_pack_gut_files()
    sue_gut_plan = open_gut_file(env_dir(), "amy23", sue_str)
    bob_str = "Bob"
    sue_gut_plan.add_acctunit(bob_str)
    save_gut_file(env_dir(), sue_gut_plan)
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    init_pack_file_path = create_path(sue_hubunit._packs_dir, f"{init_pack_id()}.json")
    delete_dir(sue_hubunit._packs_dir)
    assert os_path_exists(init_pack_file_path) is False

    # WHEN
    sue_hubunit.initialize_pack_gut_files()

    # THEN
    assert sue_gut_plan.belief_label == "amy23"
    assert sue_gut_plan.owner_name == sue_str
    assert sue_gut_plan.respect_bit == seven_int
    assert sue_gut_plan.acct_exists(bob_str)
    assert os_path_exists(init_pack_file_path)


def test_HubUnit_append_packs_to_gut_file_AddsPacksTogutFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "amy23", sue_str)
    sue_hubunit.initialize_pack_gut_files()
    sue_hubunit.save_pack_file(sue_2planatoms_packunit())
    gut_plan = open_gut_file(env_dir(), "amy23", sue_str)
    # gut_plan.add_concept(gut_plan.make_l1_rope("sports"))
    sports_str = "sports"
    sports_rope = gut_plan.make_l1_rope(sports_str)
    knee_str = "knee"
    knee_rope = gut_plan.make_rope(sports_rope, knee_str)
    assert gut_plan.concept_exists(sports_rope) is False
    assert gut_plan.concept_exists(knee_rope) is False

    # WHEN
    new_plan = sue_hubunit.append_packs_to_gut_file()

    # THEN
    assert new_plan != gut_plan
    assert new_plan.concept_exists(sports_rope)
    assert new_plan.concept_exists(knee_rope)
