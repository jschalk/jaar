from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import create_path, get_dir_file_strs
from src.a01_term_logic.way import get_default_fisc_label as fisc_label
from src.a12_hub_tools._test_util.a12_env import (
    env_dir_setup_cleanup,
)
from src.a12_hub_tools._test_util.a12_env import get_module_temp_dir as fisc_mstr_dir
from src.a12_hub_tools._test_util.example_hub_atoms import (
    get_atom_example_conceptunit_ball,
    get_atom_example_conceptunit_knee,
    get_atom_example_conceptunit_sports,
    get_atom_example_factunit_knee,
)
from src.a12_hub_tools.hubunit import hubunit_shop


def test_HubUnit_atom_filename_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_label(), yao_str)
    one_int = 1

    # WHEN
    one_atom_filename = yao_hubunit.atom_filename(one_int)

    # THEN
    assert one_atom_filename == f"{one_int}.json"


def test_HubUnit_atom_file_path_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_label(), yao_str)
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
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_label(), yao_str)
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
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_label(), yao_str)
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
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_label(), yao_str)
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
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_label(), yao_str)
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
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_label(), yao_str)

    # WHEN / THEN
    assert yao_hubunit.get_max_atom_file_number() is None


def test_HubUnit_get_next_atom_file_number_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_label(), yao_str)
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
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_label(), yao_str)
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


def test_HubUnit_get_bud_from_atom_files_ReturnsFileWithZeroAtoms(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_label(), yao_str)

    # WHEN
    yao_bud = yao_hubunit._get_bud_from_atom_files()

    # THEN
    assert yao_bud.owner_name == yao_str
    assert yao_bud.fisc_label == yao_hubunit.fisc_label
    assert yao_bud.bridge == yao_hubunit.bridge
    assert yao_bud.fund_pool == yao_hubunit.fund_pool
    assert yao_bud.fund_coin == yao_hubunit.fund_coin
    assert yao_bud.respect_bit == yao_hubunit.respect_bit


def test_HubUnit_get_bud_from_atom_files_ReturnsCorrectFile_SimpleConcept(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_label(), yao_str)

    # save atom files
    sports_atom = get_atom_example_conceptunit_sports(yao_hubunit.fisc_label)
    yao_hubunit.save_atom_file(sports_atom)

    # WHEN
    yao_bud = yao_hubunit._get_bud_from_atom_files()

    # THEN
    assert yao_bud.owner_name == yao_str
    assert yao_bud.fisc_label == yao_hubunit.fisc_label
    assert yao_bud.bridge == yao_hubunit.bridge
    sports_str = "sports"
    sports_way = yao_bud.make_l1_way(sports_str)

    assert yao_bud.concept_exists(sports_way)


def test_HubUnit_get_bud_from_atom_files_ReturnsCorrectFile_WithFactUnit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_hubunit = hubunit_shop(fisc_mstr_dir(), fisc_label(), yao_str)

    # save atom files
    x_fisc_label = yao_hubunit.fisc_label
    yao_hubunit.save_atom_file(get_atom_example_conceptunit_sports(x_fisc_label))
    yao_hubunit.save_atom_file(get_atom_example_conceptunit_ball(x_fisc_label))
    yao_hubunit.save_atom_file(get_atom_example_conceptunit_knee(x_fisc_label))
    yao_hubunit.save_atom_file(get_atom_example_factunit_knee(x_fisc_label))
    print(f"{get_dir_file_strs(yao_hubunit._atoms_dir).keys()=}")

    # WHEN
    yao_bud = yao_hubunit._get_bud_from_atom_files()

    # THEN
    assert yao_bud.owner_name == yao_str
    assert yao_bud.fisc_label == yao_hubunit.fisc_label
    assert yao_bud.bridge == yao_hubunit.bridge
    sports_str = "sports"
    sports_way = yao_bud.make_l1_way(sports_str)

    assert yao_bud.concept_exists(sports_way)
