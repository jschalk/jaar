from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, get_dir_file_strs
from src.a05_plan_logic.plan import get_default_belief_label as belief_label
from src.a12_hub_toolbox.hubunit import hubunit_shop
from src.a12_hub_toolbox.test._util.a12_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as belief_mstr_dir,
)
from src.a12_hub_toolbox.test._util.example_hub_atoms import (
    get_atom_example_factunit_knee,
    get_atom_example_planunit_ball,
    get_atom_example_planunit_knee,
    get_atom_example_planunit_sports,
)


def test_HubUnit_atom_filename_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(belief_mstr_dir(), belief_label(), yao_str)
    one_int = 1

    # WHEN
    one_atom_filename = yao_hubunit.atom_filename(one_int)

    # THEN
    assert one_atom_filename == f"{one_int}.json"


def test_HubUnit_atom_file_path_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(belief_mstr_dir(), belief_label(), yao_str)
    one_int = 1

    # WHEN
    one_atom_file_path = yao_hubunit.atom_file_path(one_int)

    # THEN
    one_atom_filename = yao_hubunit.atom_filename(one_int)
    expected_path = create_path(yao_hubunit._atoms_dir, one_atom_filename)
    assert one_atom_file_path == expected_path


def test_HubUnit_save_valid_atom_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(belief_mstr_dir(), belief_label(), yao_str)
    one_int = 1
    assert os_path_exists(yao_hubunit.atom_file_path(one_int)) is False

    # WHEN
    knee_atom = get_atom_example_factunit_knee()
    atom_num = yao_hubunit._save_valid_atom_file(knee_atom, one_int)

    # THEN
    assert os_path_exists(yao_hubunit.atom_file_path(one_int))
    assert atom_num == one_int


def test_HubUnit_atom_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(belief_mstr_dir(), belief_label(), yao_str)
    four_int = 4
    assert os_path_exists(yao_hubunit.atom_file_path(four_int)) is False
    assert yao_hubunit.atom_file_exists(four_int) is False

    # WHEN
    yao_hubunit._save_valid_atom_file(get_atom_example_factunit_knee(), four_int)

    # THEN
    assert os_path_exists(yao_hubunit.atom_file_path(four_int))
    assert yao_hubunit.atom_file_exists(four_int)


def test_HubUnit_delete_atom_file_CorrectlyDeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(belief_mstr_dir(), belief_label(), yao_str)
    ten_int = 10
    yao_hubunit._save_valid_atom_file(get_atom_example_factunit_knee(), ten_int)
    assert yao_hubunit.atom_file_exists(ten_int)

    # WHEN
    yao_hubunit.delete_atom_file(ten_int)

    # THEN
    assert yao_hubunit.atom_file_exists(ten_int) is False


def test_HubUnit_get_max_atom_file_number_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(belief_mstr_dir(), belief_label(), yao_str)
    ten_int = 10
    yao_hubunit._save_valid_atom_file(get_atom_example_factunit_knee(), ten_int)
    assert yao_hubunit.atom_file_exists(ten_int)

    # WHEN / THEN
    assert yao_hubunit.get_max_atom_file_number() == ten_int


def test_HubUnit_get_max_atom_file_number_ReturnsObjWhenDirIsEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(belief_mstr_dir(), belief_label(), yao_str)

    # WHEN / THEN
    assert yao_hubunit.get_max_atom_file_number() is None


def test_HubUnit_get_next_atom_file_number_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(belief_mstr_dir(), belief_label(), yao_str)
    # WHEN / THEN
    assert yao_hubunit._get_next_atom_file_number() == 0

    ten_int = 10
    yao_hubunit._save_valid_atom_file(get_atom_example_factunit_knee(), ten_int)
    assert yao_hubunit.atom_file_exists(ten_int)

    # WHEN / THEN
    assert yao_hubunit._get_next_atom_file_number() == 11


def test_HubUnit_save_atom_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(belief_mstr_dir(), belief_label(), yao_str)
    ten_int = 10
    yao_hubunit._save_valid_atom_file(get_atom_example_factunit_knee(), ten_int)
    assert yao_hubunit.get_max_atom_file_number() == ten_int
    eleven_int = ten_int + 1
    assert yao_hubunit.atom_file_exists(eleven_int) is False

    # WHEN
    atom_num1 = yao_hubunit.save_atom_file(get_atom_example_factunit_knee())

    # THEN
    assert yao_hubunit.get_max_atom_file_number() != ten_int
    assert yao_hubunit.get_max_atom_file_number() == eleven_int
    assert yao_hubunit.atom_file_exists(eleven_int)
    assert atom_num1 == eleven_int
    atom_num2 = yao_hubunit.save_atom_file(get_atom_example_factunit_knee())
    assert atom_num2 == 12


def test_HubUnit_get_believer_from_atom_files_ReturnsFileWithZeroAtoms(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(belief_mstr_dir(), belief_label(), yao_str)

    # WHEN
    yao_believer = yao_hubunit._get_believer_from_atom_files()

    # THEN
    assert yao_believer.believer_name == yao_str
    assert yao_believer.belief_label == yao_hubunit.belief_label
    assert yao_believer.knot == yao_hubunit.knot
    assert yao_believer.fund_pool == yao_hubunit.fund_pool
    assert yao_believer.fund_iota == yao_hubunit.fund_iota
    assert yao_believer.respect_bit == yao_hubunit.respect_bit


def test_HubUnit_get_believer_from_atom_files_ReturnsCorrectFile_SimplePlan(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(belief_mstr_dir(), belief_label(), yao_str)

    # save atom files
    sports_atom = get_atom_example_planunit_sports(yao_hubunit.belief_label)
    yao_hubunit.save_atom_file(sports_atom)

    # WHEN
    yao_believer = yao_hubunit._get_believer_from_atom_files()

    # THEN
    assert yao_believer.believer_name == yao_str
    assert yao_believer.belief_label == yao_hubunit.belief_label
    assert yao_believer.knot == yao_hubunit.knot
    sports_str = "sports"
    sports_rope = yao_believer.make_l1_rope(sports_str)

    assert yao_believer.plan_exists(sports_rope)


def test_HubUnit_get_believer_from_atom_files_ReturnsCorrectFile_WithFactUnit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(belief_mstr_dir(), belief_label(), yao_str)

    # save atom files
    x_belief_label = yao_hubunit.belief_label
    yao_hubunit.save_atom_file(get_atom_example_planunit_sports(x_belief_label))
    yao_hubunit.save_atom_file(get_atom_example_planunit_ball(x_belief_label))
    yao_hubunit.save_atom_file(get_atom_example_planunit_knee(x_belief_label))
    yao_hubunit.save_atom_file(get_atom_example_factunit_knee(x_belief_label))
    print(f"{get_dir_file_strs(yao_hubunit._atoms_dir).keys()=}")

    # WHEN
    yao_believer = yao_hubunit._get_believer_from_atom_files()

    # THEN
    assert yao_believer.believer_name == yao_str
    assert yao_believer.belief_label == yao_hubunit.belief_label
    assert yao_believer.knot == yao_hubunit.knot
    sports_str = "sports"
    sports_rope = yao_believer.make_l1_rope(sports_str)

    assert yao_believer.plan_exists(sports_rope)
