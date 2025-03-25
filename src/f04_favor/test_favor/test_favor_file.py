from src.f00_instrument.file import create_path as f_path, open_json
from src.f01_road.deal import owner_name_str
from src.f01_road.jaar_config import (
    get_favors_folder,
    get_test_fisc_title as fisc_title,
)
from src.f04_favor.atom_config import face_name_str
from src.f04_favor.delta import buddelta_shop
from src.f04_favor.favor import favorunit_shop, create_favorunit_from_files
from src.f04_favor.examples.example_atoms import (
    get_atom_example_itemunit_sports,
    get_atom_example_itemunit_knee,
    get_atom_example_itemunit_ball,
)
from src.f04_favor.examples.favor_env import (
    get_favor_temp_env_dir as fiscs_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_FavorUnit_save_atom_file_SavesCorrectFile(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = f_path(fiscs_dir(), fisc_title())
    x_owners_dir = f_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = f_path(sue_atoms_dir, two_filename)
    sue_atom6_path = f_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_favorunit = favorunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert os_path_exists(sue_atom6_path) is False

    # WHEN
    sports_atom = get_atom_example_itemunit_sports()
    sue_favorunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert os_path_exists(sue_atom2_path)
    assert os_path_exists(sue_atom6_path) is False
    two_file_dict = open_json(sue_atoms_dir, two_filename)
    assert two_file_dict == sports_atom.get_dict()


def test_FavorUnit_atom_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = f_path(fiscs_dir(), fisc_title())
    x_owners_dir = f_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = f_path(sue_atoms_dir, two_filename)
    sue_atom6_path = f_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_favorunit = favorunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert sue_favorunit.atom_file_exists(two_int) is False

    # WHEN
    sports_atom = get_atom_example_itemunit_sports()
    sue_favorunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert sue_favorunit.atom_file_exists(two_int)


def test_FavorUnit_open_atom_file_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = f_path(fiscs_dir(), fisc_title())
    x_owners_dir = f_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = f_path(sue_atoms_dir, two_filename)
    sue_atom6_path = f_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_favorunit = favorunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    sports_atom = get_atom_example_itemunit_sports()
    sue_favorunit._save_atom_file(two_int, sports_atom)
    assert sue_favorunit.atom_file_exists(two_int)

    # WHEN
    file_atom = sue_favorunit._open_atom_file(two_int)

    # THEN
    assert file_atom == sports_atom


def test_FavorUnit_save_favor_file_SavesCorrectFile(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = f_path(fiscs_dir(), fisc_title())
    x_owners_dir = f_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_favor_id = 2
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_favors_dir = f_path(sue_owner_dir, get_favors_folder())
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_favor2_path = f_path(sue_favors_dir, two_filename)
    sue_favor6_path = f_path(sue_favors_dir, six_filename)
    print(f"{sue_favor2_path=}")
    print(f"{sue_favor6_path=}")
    sue_favorunit = favorunit_shop(
        sue_str, None, None, sue_favor_id, _favors_dir=sue_favors_dir
    )
    assert os_path_exists(sue_favor2_path) is False
    assert os_path_exists(sue_favor6_path) is False

    # WHEN
    sue_favorunit._save_favor_file()

    # THEN
    assert os_path_exists(sue_favor2_path)
    assert os_path_exists(sue_favor6_path) is False
    favor_file_dict = open_json(sue_favors_dir, two_filename)
    print(f"{favor_file_dict=}")
    assert favor_file_dict.get("delta_atom_numbers") == []
    assert favor_file_dict.get(owner_name_str()) == sue_str
    assert favor_file_dict.get(face_name_str()) is None
    print(f"{favor_file_dict.keys()=}")


def test_FavorUnit_favor_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = f_path(fiscs_dir(), fisc_title())
    x_owners_dir = f_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_favors_dir = f_path(sue_owner_dir, get_favors_folder())
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_favor2_path = f_path(sue_favors_dir, two_filename)
    sue_favor6_path = f_path(sue_favors_dir, six_filename)
    print(f"{sue_favor2_path=}")
    print(f"{sue_favor6_path=}")
    sue_favorunit = favorunit_shop(sue_str, _favors_dir=sue_favors_dir)
    assert os_path_exists(sue_favor2_path) is False
    assert sue_favorunit.favor_file_exists() is False

    # WHEN
    sue_favorunit._save_favor_file()

    # THEN
    assert sue_favorunit.favor_file_exists()


def test_FavorUnit_save_files_CorrectlySavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = f_path(fiscs_dir(), fisc_title())
    x_owners_dir = f_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")
    sue_favors_dir = f_path(sue_owner_dir, get_favors_folder())

    zia_str = "Zia"
    yao_str = "Yao"
    sue_delta_start = 4
    sue_favorunit = favorunit_shop(
        sue_str, _atoms_dir=sue_atoms_dir, _favors_dir=sue_favors_dir
    )
    sue_favorunit.set_delta_start(sue_delta_start)
    sue_favorunit.set_face(zia_str)
    sue_favorunit.set_face(yao_str)
    int4 = 4
    int5 = 5
    sports_atom = get_atom_example_itemunit_sports()
    knee_atom = get_atom_example_itemunit_knee()
    sue_favorunit._buddelta.set_budatom(sports_atom)
    sue_favorunit._buddelta.set_budatom(knee_atom)
    assert sue_favorunit.favor_file_exists() is False
    assert sue_favorunit.atom_file_exists(int4) is False
    assert sue_favorunit.atom_file_exists(int5) is False

    # WHEN
    sue_favorunit.save_files()

    # THEN
    assert sue_favorunit.favor_file_exists()
    assert sue_favorunit.atom_file_exists(int4)
    assert sue_favorunit.atom_file_exists(int5)


def test_FavorUnit_create_buddelta_from_atom_files_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = f_path(fiscs_dir(), fisc_title())
    x_owners_dir = f_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")

    sue_favorunit = favorunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    int4 = 4
    int5 = 5
    int9 = 9
    spor_atom = get_atom_example_itemunit_sports()
    knee_atom = get_atom_example_itemunit_knee()
    ball_atom = get_atom_example_itemunit_ball()
    sue_favorunit._save_atom_file(int4, spor_atom)
    sue_favorunit._save_atom_file(int5, knee_atom)
    sue_favorunit._save_atom_file(int9, ball_atom)
    assert sue_favorunit._buddelta == buddelta_shop()

    # WHEN
    atoms_list = [int4, int5, int9]
    sue_favorunit._create_buddelta_from_atom_files(atoms_list)

    # THEN
    static_buddelta = buddelta_shop()
    static_buddelta.set_budatom(spor_atom)
    static_buddelta.set_budatom(knee_atom)
    static_buddelta.set_budatom(ball_atom)
    assert sue_favorunit._buddelta != buddelta_shop()
    assert sue_favorunit._buddelta == static_buddelta


def test_create_favorunit_from_files_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fisc_dir = f_path(fiscs_dir(), fisc_title())
    x_owners_dir = f_path(x_fisc_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")
    sue_favors_dir = f_path(sue_owner_dir, get_favors_folder())

    yao_str = "Yao"
    sue_delta_start = 4
    src_sue_favorunit = favorunit_shop(
        sue_str, _atoms_dir=sue_atoms_dir, _favors_dir=sue_favors_dir
    )
    src_sue_favorunit.set_delta_start(sue_delta_start)
    src_sue_favorunit.set_face(yao_str)
    sports_atom = get_atom_example_itemunit_sports()
    knee_atom = get_atom_example_itemunit_knee()
    ball_atom = get_atom_example_itemunit_ball()
    src_sue_favorunit._buddelta.set_budatom(sports_atom)
    src_sue_favorunit._buddelta.set_budatom(knee_atom)
    src_sue_favorunit._buddelta.set_budatom(ball_atom)
    src_sue_favorunit.save_files()

    # WHEN
    new_sue_favorunit = create_favorunit_from_files(
        favors_dir=sue_favors_dir,
        favor_id=src_sue_favorunit._favor_id,
        atoms_dir=sue_atoms_dir,
    )

    # THEN
    assert src_sue_favorunit.owner_name == new_sue_favorunit.owner_name
    assert src_sue_favorunit.face_name == new_sue_favorunit.face_name
    assert src_sue_favorunit._buddelta == new_sue_favorunit._buddelta
