from src._instrument.file import dir_files as file_dir_files
from src.listen.hubunit import hubunit_shop
from src.listen.examples.example_listen_atoms import (
    get_atom_example_factunit_knee,
    get_atom_example_ideaunit_sports,
    get_atom_example_ideaunit_ball,
    get_atom_example_ideaunit_knee,
)
from src.listen.examples.listen_env import (
    get_listen_temp_env_dir as reals_dir,
    get_default_real_id_roadnode as real_id,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_HubUnit_atom_file_name_ReturnsCorrectObj():
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(reals_dir(), real_id(), yao_text)
    one_int = 1

    # WHEN
    one_atom_file_name = yao_hubunit.atom_file_name(one_int)

    # THEN
    assert one_atom_file_name == f"{one_int}.json"


def test_HubUnit_atom_file_path_ReturnsCorrectObj():
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(reals_dir(), real_id(), yao_text)
    one_int = 1

    # WHEN
    one_atom_file_path = yao_hubunit.atom_file_path(one_int)

    # THEN
    one_atom_file_name = yao_hubunit.atom_file_name(one_int)
    assert one_atom_file_path == f"{yao_hubunit.atoms_dir()}/{one_atom_file_name}"


def test_HubUnit_save_valid_atom_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(reals_dir(), real_id(), yao_text)
    one_int = 1
    assert os_path_exists(yao_hubunit.atom_file_path(one_int)) is False

    # WHEN
    knee_atom = get_atom_example_factunit_knee()
    atom_num = yao_hubunit._save_valid_atom_file(knee_atom, one_int)

    # THEN
    assert os_path_exists(yao_hubunit.atom_file_path(one_int))
    assert atom_num == one_int


def test_HubUnit_atom_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(reals_dir(), real_id(), yao_text)
    five_int = 5
    assert os_path_exists(yao_hubunit.atom_file_path(five_int)) is False
    assert yao_hubunit.atom_file_exists(five_int) is False

    # WHEN
    yao_hubunit._save_valid_atom_file(get_atom_example_factunit_knee(), five_int)

    # THEN
    assert os_path_exists(yao_hubunit.atom_file_path(five_int))
    assert yao_hubunit.atom_file_exists(five_int)


def test_HubUnit_delete_atom_file_CorrectlyDeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    yao_hubunit._save_valid_atom_file(get_atom_example_factunit_knee(), ten_int)
    assert yao_hubunit.atom_file_exists(ten_int)

    # WHEN
    yao_hubunit.delete_atom_file(ten_int)

    # THEN
    assert yao_hubunit.atom_file_exists(ten_int) is False


def test_HubUnit_get_max_atom_file_number_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    yao_hubunit._save_valid_atom_file(get_atom_example_factunit_knee(), ten_int)
    assert yao_hubunit.atom_file_exists(ten_int)

    # WHEN / THEN
    assert yao_hubunit.get_max_atom_file_number() == ten_int


def test_HubUnit_get_max_atom_file_number_ReturnsCorrectObjWhenDirIsEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(reals_dir(), real_id(), yao_text)

    # WHEN / THEN
    assert yao_hubunit.get_max_atom_file_number() is None


def test_HubUnit_get_next_atom_file_number_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(reals_dir(), real_id(), yao_text)
    # WHEN / THEN
    assert yao_hubunit._get_next_atom_file_number() == 0

    ten_int = 10
    yao_hubunit._save_valid_atom_file(get_atom_example_factunit_knee(), ten_int)
    assert yao_hubunit.atom_file_exists(ten_int)

    # WHEN / THEN
    assert yao_hubunit._get_next_atom_file_number() == 11


def test_HubUnit_save_atom_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(reals_dir(), real_id(), yao_text)
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


def test_HubUnit_get_world_from_atom_files_ReturnsFileWithZeroAtoms(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(reals_dir(), real_id(), yao_text)

    # WHEN
    yao_world = yao_hubunit._get_world_from_atom_files()

    # THEN
    assert yao_world._owner_id == yao_text
    assert yao_world._real_id == yao_hubunit.real_id
    assert yao_world._road_delimiter == yao_hubunit.road_delimiter
    assert yao_world._bud_pool == yao_hubunit.bud_pool
    assert yao_world._coin == yao_hubunit.coin
    assert yao_world._bit == yao_hubunit.bit


def test_HubUnit_get_world_from_atom_files_ReturnsCorrectFile_SimpleIdea(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(reals_dir(), real_id(), yao_text)

    # save atom files
    sports_atom = get_atom_example_ideaunit_sports(yao_hubunit.real_id)
    yao_hubunit.save_atom_file(sports_atom)

    # WHEN
    yao_world = yao_hubunit._get_world_from_atom_files()

    # THEN
    assert yao_world._owner_id == yao_text
    assert yao_world._real_id == yao_hubunit.real_id
    assert yao_world._road_delimiter == yao_hubunit.road_delimiter
    sports_text = "sports"
    sports_road = yao_world.make_l1_road(sports_text)

    assert yao_world.idea_exists(sports_road)


def test_HubUnit_get_world_from_atom_files_ReturnsCorrectFile_WithFactUnit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(reals_dir(), real_id(), yao_text)

    # save atom files
    x_real_id = yao_hubunit.real_id
    yao_hubunit.save_atom_file(get_atom_example_ideaunit_sports(x_real_id))
    yao_hubunit.save_atom_file(get_atom_example_ideaunit_ball(x_real_id))
    yao_hubunit.save_atom_file(get_atom_example_ideaunit_knee(x_real_id))
    yao_hubunit.save_atom_file(get_atom_example_factunit_knee(x_real_id))
    print(f"{file_dir_files(yao_hubunit.atoms_dir()).keys()=}")

    # WHEN
    yao_world = yao_hubunit._get_world_from_atom_files()

    # THEN
    assert yao_world._owner_id == yao_text
    assert yao_world._real_id == yao_hubunit.real_id
    assert yao_world._road_delimiter == yao_hubunit.road_delimiter
    sports_text = "sports"
    sports_road = yao_world.make_l1_road(sports_text)

    assert yao_world.idea_exists(sports_road)
