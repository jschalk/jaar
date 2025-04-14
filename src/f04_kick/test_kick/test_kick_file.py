from src.f00_instrument.file_toolbox import create_path, open_json
from src.f01_road.deal import owner_name_str
from src.f04_kick.atom_config import face_name_str
from src.f04_kick.delta import buddelta_shop
from src.f04_kick.kick import kickunit_shop, create_kickunit_from_files
from src.f04_kick.examples.example_atoms import (
    get_atom_example_itemunit_sports,
    get_atom_example_itemunit_knee,
    get_atom_example_itemunit_ball,
)
from src.f04_kick.examples.kick_env import (
    get_kick_temp_env_dir as fiscs_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_KickUnit_save_atom_file_SavesCorrectFile(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = create_path(fiscs_dir(), "accord23")
    x_owners_dir = create_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = create_path(x_owners_dir, sue_str)
    sue_atoms_dir = create_path(sue_owner_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = create_path(sue_atoms_dir, two_filename)
    sue_atom6_path = create_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_kickunit = kickunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert os_path_exists(sue_atom6_path) is False

    # WHEN
    sports_atom = get_atom_example_itemunit_sports()
    sue_kickunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert os_path_exists(sue_atom2_path)
    assert os_path_exists(sue_atom6_path) is False
    two_file_dict = open_json(sue_atoms_dir, two_filename)
    assert two_file_dict == sports_atom.get_dict()


def test_KickUnit_atom_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = create_path(fiscs_dir(), "accord23")
    x_owners_dir = create_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = create_path(x_owners_dir, sue_str)
    sue_atoms_dir = create_path(sue_owner_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = create_path(sue_atoms_dir, two_filename)
    sue_atom6_path = create_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_kickunit = kickunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert sue_kickunit.atom_file_exists(two_int) is False

    # WHEN
    sports_atom = get_atom_example_itemunit_sports()
    sue_kickunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert sue_kickunit.atom_file_exists(two_int)


def test_KickUnit_open_atom_file_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = create_path(fiscs_dir(), "accord23")
    x_owners_dir = create_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = create_path(x_owners_dir, sue_str)
    sue_atoms_dir = create_path(sue_owner_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = create_path(sue_atoms_dir, two_filename)
    sue_atom6_path = create_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_kickunit = kickunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    sports_atom = get_atom_example_itemunit_sports()
    sue_kickunit._save_atom_file(two_int, sports_atom)
    assert sue_kickunit.atom_file_exists(two_int)

    # WHEN
    file_atom = sue_kickunit._open_atom_file(two_int)

    # THEN
    assert file_atom == sports_atom


def test_KickUnit_save_kick_file_SavesCorrectFile(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = create_path(fiscs_dir(), "accord23")
    x_owners_dir = create_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_kick_id = 2
    sue_owner_dir = create_path(x_owners_dir, sue_str)
    sue_kicks_dir = create_path(sue_owner_dir, "kicks")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_kick2_path = create_path(sue_kicks_dir, two_filename)
    sue_kick6_path = create_path(sue_kicks_dir, six_filename)
    print(f"{sue_kick2_path=}")
    print(f"{sue_kick6_path=}")
    sue_kickunit = kickunit_shop(
        sue_str, None, None, sue_kick_id, _kicks_dir=sue_kicks_dir
    )
    assert os_path_exists(sue_kick2_path) is False
    assert os_path_exists(sue_kick6_path) is False

    # WHEN
    sue_kickunit._save_kick_file()

    # THEN
    assert os_path_exists(sue_kick2_path)
    assert os_path_exists(sue_kick6_path) is False
    kick_file_dict = open_json(sue_kicks_dir, two_filename)
    print(f"{kick_file_dict=}")
    assert kick_file_dict.get("delta_atom_numbers") == []
    assert kick_file_dict.get(owner_name_str()) == sue_str
    assert kick_file_dict.get(face_name_str()) is None
    print(f"{kick_file_dict.keys()=}")


def test_KickUnit_kick_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = create_path(fiscs_dir(), "accord23")
    x_owners_dir = create_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = create_path(x_owners_dir, sue_str)
    sue_kicks_dir = create_path(sue_owner_dir, "kicks")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_kick2_path = create_path(sue_kicks_dir, two_filename)
    sue_kick6_path = create_path(sue_kicks_dir, six_filename)
    print(f"{sue_kick2_path=}")
    print(f"{sue_kick6_path=}")
    sue_kickunit = kickunit_shop(sue_str, _kicks_dir=sue_kicks_dir)
    assert os_path_exists(sue_kick2_path) is False
    assert sue_kickunit.kick_file_exists() is False

    # WHEN
    sue_kickunit._save_kick_file()

    # THEN
    assert sue_kickunit.kick_file_exists()


def test_KickUnit_save_files_CorrectlySavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = create_path(fiscs_dir(), "accord23")
    x_owners_dir = create_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = create_path(x_owners_dir, sue_str)
    sue_atoms_dir = create_path(sue_owner_dir, "atoms")
    sue_kicks_dir = create_path(sue_owner_dir, "kicks")

    zia_str = "Zia"
    yao_str = "Yao"
    sue_delta_start = 4
    sue_kickunit = kickunit_shop(
        sue_str, _atoms_dir=sue_atoms_dir, _kicks_dir=sue_kicks_dir
    )
    sue_kickunit.set_delta_start(sue_delta_start)
    sue_kickunit.set_face(zia_str)
    sue_kickunit.set_face(yao_str)
    int4 = 4
    int5 = 5
    sports_atom = get_atom_example_itemunit_sports()
    knee_atom = get_atom_example_itemunit_knee()
    sue_kickunit._buddelta.set_budatom(sports_atom)
    sue_kickunit._buddelta.set_budatom(knee_atom)
    assert sue_kickunit.kick_file_exists() is False
    assert sue_kickunit.atom_file_exists(int4) is False
    assert sue_kickunit.atom_file_exists(int5) is False

    # WHEN
    sue_kickunit.save_files()

    # THEN
    assert sue_kickunit.kick_file_exists()
    assert sue_kickunit.atom_file_exists(int4)
    assert sue_kickunit.atom_file_exists(int5)


def test_KickUnit_create_buddelta_from_atom_files_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = create_path(fiscs_dir(), "accord23")
    x_owners_dir = create_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = create_path(x_owners_dir, sue_str)
    sue_atoms_dir = create_path(sue_owner_dir, "atoms")

    sue_kickunit = kickunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    int4 = 4
    int5 = 5
    int9 = 9
    spor_atom = get_atom_example_itemunit_sports()
    knee_atom = get_atom_example_itemunit_knee()
    ball_atom = get_atom_example_itemunit_ball()
    sue_kickunit._save_atom_file(int4, spor_atom)
    sue_kickunit._save_atom_file(int5, knee_atom)
    sue_kickunit._save_atom_file(int9, ball_atom)
    assert sue_kickunit._buddelta == buddelta_shop()

    # WHEN
    atoms_list = [int4, int5, int9]
    sue_kickunit._create_buddelta_from_atom_files(atoms_list)

    # THEN
    static_buddelta = buddelta_shop()
    static_buddelta.set_budatom(spor_atom)
    static_buddelta.set_budatom(knee_atom)
    static_buddelta.set_budatom(ball_atom)
    assert sue_kickunit._buddelta != buddelta_shop()
    assert sue_kickunit._buddelta == static_buddelta


def test_create_kickunit_from_files_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = create_path(fiscs_dir(), "accord23")
    x_owners_dir = create_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = create_path(x_owners_dir, sue_str)
    sue_atoms_dir = create_path(sue_owner_dir, "atoms")
    sue_kicks_dir = create_path(sue_owner_dir, "kicks")

    yao_str = "Yao"
    sue_delta_start = 4
    src_sue_kickunit = kickunit_shop(
        sue_str, _atoms_dir=sue_atoms_dir, _kicks_dir=sue_kicks_dir
    )
    src_sue_kickunit.set_delta_start(sue_delta_start)
    src_sue_kickunit.set_face(yao_str)
    sports_atom = get_atom_example_itemunit_sports()
    knee_atom = get_atom_example_itemunit_knee()
    ball_atom = get_atom_example_itemunit_ball()
    src_sue_kickunit._buddelta.set_budatom(sports_atom)
    src_sue_kickunit._buddelta.set_budatom(knee_atom)
    src_sue_kickunit._buddelta.set_budatom(ball_atom)
    src_sue_kickunit.save_files()

    # WHEN
    new_sue_kickunit = create_kickunit_from_files(
        kicks_dir=sue_kicks_dir,
        kick_id=src_sue_kickunit._kick_id,
        atoms_dir=sue_atoms_dir,
    )

    # THEN
    assert src_sue_kickunit.owner_name == new_sue_kickunit.owner_name
    assert src_sue_kickunit.face_name == new_sue_kickunit.face_name
    assert src_sue_kickunit._buddelta == new_sue_kickunit._buddelta
