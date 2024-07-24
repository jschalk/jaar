from src._instrument.file import open_file, create_file_path as f_path
from src._instrument.python import get_dict_from_json
from src._road.jaar_config import get_gifts_folder, get_test_real_id as real_id
from src.gift.change import changeunit_shop
from src.gift.gift import giftunit_shop, create_giftunit_from_files
from src.gift.examples.example_atoms import (
    get_atom_example_ideaunit_sports,
    get_atom_example_ideaunit_knee,
    get_atom_example_ideaunit_ball,
)
from src.gift.examples.gift_env import (
    get_gift_temp_env_dir as reals_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_GiftUnit_save_atom_file_SavesCorrectFile(env_dir_setup_cleanup):
    # ESTABLISH
    x_real_dir = f_path(reals_dir(), real_id())
    x_owners_dir = f_path(x_real_dir, "owners")
    sue_text = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_text)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = f_path(sue_atoms_dir, two_filename)
    sue_atom6_path = f_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    farm_giftunit = giftunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert os_path_exists(sue_atom6_path) is False

    # WHEN
    sports_atom = get_atom_example_ideaunit_sports()
    farm_giftunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert os_path_exists(sue_atom2_path)
    assert os_path_exists(sue_atom6_path) is False
    two_file_json = open_file(sue_atoms_dir, two_filename)
    assert two_file_json == sports_atom.get_json()


def test_GiftUnit_atom_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_real_dir = f_path(reals_dir(), real_id())
    x_owners_dir = f_path(x_real_dir, "owners")
    sue_text = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_text)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = f_path(sue_atoms_dir, two_filename)
    sue_atom6_path = f_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    farm_giftunit = giftunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert farm_giftunit.atom_file_exists(two_int) is False

    # WHEN
    sports_atom = get_atom_example_ideaunit_sports()
    farm_giftunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert farm_giftunit.atom_file_exists(two_int)


def test_GiftUnit_open_atom_file_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_real_dir = f_path(reals_dir(), real_id())
    x_owners_dir = f_path(x_real_dir, "owners")
    sue_text = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_text)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = f_path(sue_atoms_dir, two_filename)
    sue_atom6_path = f_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    farm_giftunit = giftunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    sports_atom = get_atom_example_ideaunit_sports()
    farm_giftunit._save_atom_file(two_int, sports_atom)
    assert farm_giftunit.atom_file_exists(two_int)

    # WHEN
    file_atom = farm_giftunit._open_atom_file(two_int)

    # THEN
    assert file_atom == sports_atom


def test_GiftUnit_save_gift_file_SavesCorrectFile(env_dir_setup_cleanup):
    # ESTABLISH
    x_real_dir = f_path(reals_dir(), real_id())
    x_owners_dir = f_path(x_real_dir, "owners")
    sue_text = "Sue"
    sue_gift_id = 2
    sue_owner_dir = f_path(x_owners_dir, sue_text)
    sue_gifts_dir = f_path(sue_owner_dir, get_gifts_folder())
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_gift2_path = f_path(sue_gifts_dir, two_filename)
    sue_gift6_path = f_path(sue_gifts_dir, six_filename)
    print(f"{sue_gift2_path=}")
    print(f"{sue_gift6_path=}")
    farm_giftunit = giftunit_shop(sue_text, None, sue_gift_id, _gifts_dir=sue_gifts_dir)
    assert os_path_exists(sue_gift2_path) is False
    assert os_path_exists(sue_gift6_path) is False

    # WHEN
    farm_giftunit._save_gift_file()

    # THEN
    assert os_path_exists(sue_gift2_path)
    assert os_path_exists(sue_gift6_path) is False
    gift_file_json = open_file(sue_gifts_dir, two_filename)
    gift_file_dict = get_dict_from_json(gift_file_json)
    print(f"{gift_file_dict=}")
    assert gift_file_dict.get("change_atom_numbers") == []
    assert gift_file_dict.get("owner_id") == sue_text
    assert gift_file_dict.get("face_id") is None
    print(f"{gift_file_dict.keys()=}")


def test_GiftUnit_gift_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_real_dir = f_path(reals_dir(), real_id())
    x_owners_dir = f_path(x_real_dir, "owners")
    sue_text = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_text)
    sue_gifts_dir = f_path(sue_owner_dir, get_gifts_folder())
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_gift2_path = f_path(sue_gifts_dir, two_filename)
    sue_gift6_path = f_path(sue_gifts_dir, six_filename)
    print(f"{sue_gift2_path=}")
    print(f"{sue_gift6_path=}")
    farm_giftunit = giftunit_shop(sue_text, _gifts_dir=sue_gifts_dir)
    assert os_path_exists(sue_gift2_path) is False
    assert farm_giftunit.gift_file_exists() is False

    # WHEN
    farm_giftunit._save_gift_file()

    # THEN
    assert farm_giftunit.gift_file_exists()


def test_GiftUnit_save_files_CorrectlySavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    x_real_dir = f_path(reals_dir(), real_id())
    x_owners_dir = f_path(x_real_dir, "owners")
    sue_text = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_text)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")
    sue_gifts_dir = f_path(sue_owner_dir, get_gifts_folder())

    zia_text = "Zia"
    yao_text = "Yao"
    farm_change_start = 4
    farm_giftunit = giftunit_shop(
        sue_text, _atoms_dir=sue_atoms_dir, _gifts_dir=sue_gifts_dir
    )
    farm_giftunit.set_change_start(farm_change_start)
    farm_giftunit.set_face(zia_text)
    farm_giftunit.set_face(yao_text)
    four_int = 4
    five_int = 5
    four_atom = get_atom_example_ideaunit_sports()
    five_atom = get_atom_example_ideaunit_knee()
    farm_giftunit._changeunit.set_atomunit(four_atom)
    farm_giftunit._changeunit.set_atomunit(five_atom)
    assert farm_giftunit.gift_file_exists() is False
    assert farm_giftunit.atom_file_exists(four_int) is False
    assert farm_giftunit.atom_file_exists(five_int) is False

    # WHEN
    farm_giftunit.save_files()

    # THEN
    assert farm_giftunit.gift_file_exists()
    assert farm_giftunit.atom_file_exists(four_int)
    assert farm_giftunit.atom_file_exists(five_int)


def test_GiftUnit_create_changeunit_from_atom_files_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    x_real_dir = f_path(reals_dir(), real_id())
    x_owners_dir = f_path(x_real_dir, "owners")
    sue_text = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_text)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")

    sue_giftunit = giftunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    four_int = 4
    five_int = 5
    nine_int = 9
    four_atom = get_atom_example_ideaunit_sports()
    five_atom = get_atom_example_ideaunit_knee()
    nine_atom = get_atom_example_ideaunit_ball()
    sue_giftunit._save_atom_file(four_int, four_atom)
    sue_giftunit._save_atom_file(five_int, five_atom)
    sue_giftunit._save_atom_file(nine_int, nine_atom)
    assert sue_giftunit._changeunit == changeunit_shop()

    # WHEN
    atoms_list = [four_int, five_int, nine_int]
    sue_giftunit._create_changeunit_from_atom_files(atoms_list)

    # THEN
    static_changeunit = changeunit_shop()
    static_changeunit.set_atomunit(four_atom)
    static_changeunit.set_atomunit(five_atom)
    static_changeunit.set_atomunit(nine_atom)
    assert sue_giftunit._changeunit != changeunit_shop()
    assert sue_giftunit._changeunit == static_changeunit


def test_create_giftunit_from_files_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_real_dir = f_path(reals_dir(), real_id())
    x_owners_dir = f_path(x_real_dir, "owners")
    sue_text = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_text)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")
    sue_gifts_dir = f_path(sue_owner_dir, get_gifts_folder())

    yao_text = "Yao"
    sue_change_start = 4
    src_sue_giftunit = giftunit_shop(
        sue_text, _atoms_dir=sue_atoms_dir, _gifts_dir=sue_gifts_dir
    )
    src_sue_giftunit.set_change_start(sue_change_start)
    src_sue_giftunit.set_face(yao_text)
    sports_atom = get_atom_example_ideaunit_sports()
    knee_atom = get_atom_example_ideaunit_knee()
    ball_atom = get_atom_example_ideaunit_ball()
    src_sue_giftunit._changeunit.set_atomunit(sports_atom)
    src_sue_giftunit._changeunit.set_atomunit(knee_atom)
    src_sue_giftunit._changeunit.set_atomunit(ball_atom)
    src_sue_giftunit.save_files()

    # WHEN
    new_sue_giftunit = create_giftunit_from_files(
        gifts_dir=sue_gifts_dir,
        gift_id=src_sue_giftunit._gift_id,
        atoms_dir=sue_atoms_dir,
    )

    # THEN
    assert src_sue_giftunit.owner_id == new_sue_giftunit.owner_id
    assert src_sue_giftunit._face_id == new_sue_giftunit._face_id
    assert src_sue_giftunit._changeunit == new_sue_giftunit._changeunit
