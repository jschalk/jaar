from src.f00_instrument.file import open_file, create_file_path as f_path
from src.f00_instrument.dict_tool import get_dict_from_json
from src.f01_road.jaar_config import get_gifts_folder, get_test_fiscal_id as fiscal_id
from src.f04_gift.atom_config import owner_id_str, face_id_str
from src.f04_gift.delta import deltaunit_shop
from src.f04_gift.gift import giftunit_shop, create_giftunit_from_files
from src.f04_gift.examples.example_atoms import (
    get_atom_example_itemunit_sports,
    get_atom_example_itemunit_knee,
    get_atom_example_itemunit_ball,
)
from src.f04_gift.examples.gift_env import (
    get_gift_temp_env_dir as fiscals_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_GiftUnit_save_atom_file_SavesCorrectFile(env_dir_setup_cleanup):
    # ESTABLISH
    x_fiscal_dir = f_path(fiscals_dir(), fiscal_id())
    x_owners_dir = f_path(x_fiscal_dir, "owners")
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
    farm_giftunit = giftunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert os_path_exists(sue_atom6_path) is False

    # WHEN
    sports_atom = get_atom_example_itemunit_sports()
    farm_giftunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert os_path_exists(sue_atom2_path)
    assert os_path_exists(sue_atom6_path) is False
    two_file_json = open_file(sue_atoms_dir, two_filename)
    assert two_file_json == sports_atom.get_json()


def test_GiftUnit_atom_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fiscal_dir = f_path(fiscals_dir(), fiscal_id())
    x_owners_dir = f_path(x_fiscal_dir, "owners")
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
    farm_giftunit = giftunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert farm_giftunit.atom_file_exists(two_int) is False

    # WHEN
    sports_atom = get_atom_example_itemunit_sports()
    farm_giftunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert farm_giftunit.atom_file_exists(two_int)


def test_GiftUnit_open_atom_file_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fiscal_dir = f_path(fiscals_dir(), fiscal_id())
    x_owners_dir = f_path(x_fiscal_dir, "owners")
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
    farm_giftunit = giftunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    sports_atom = get_atom_example_itemunit_sports()
    farm_giftunit._save_atom_file(two_int, sports_atom)
    assert farm_giftunit.atom_file_exists(two_int)

    # WHEN
    file_atom = farm_giftunit._open_atom_file(two_int)

    # THEN
    assert file_atom == sports_atom


def test_GiftUnit_save_gift_file_SavesCorrectFile(env_dir_setup_cleanup):
    # ESTABLISH
    x_fiscal_dir = f_path(fiscals_dir(), fiscal_id())
    x_owners_dir = f_path(x_fiscal_dir, "owners")
    sue_str = "Sue"
    sue_gift_id = 2
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_gifts_dir = f_path(sue_owner_dir, get_gifts_folder())
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_gift2_path = f_path(sue_gifts_dir, two_filename)
    sue_gift6_path = f_path(sue_gifts_dir, six_filename)
    print(f"{sue_gift2_path=}")
    print(f"{sue_gift6_path=}")
    farm_giftunit = giftunit_shop(sue_str, None, sue_gift_id, _gifts_dir=sue_gifts_dir)
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
    assert gift_file_dict.get("delta_atom_numbers") == []
    assert gift_file_dict.get(owner_id_str()) == sue_str
    assert gift_file_dict.get(face_id_str()) is None
    print(f"{gift_file_dict.keys()=}")


def test_GiftUnit_gift_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fiscal_dir = f_path(fiscals_dir(), fiscal_id())
    x_owners_dir = f_path(x_fiscal_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_gifts_dir = f_path(sue_owner_dir, get_gifts_folder())
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_gift2_path = f_path(sue_gifts_dir, two_filename)
    sue_gift6_path = f_path(sue_gifts_dir, six_filename)
    print(f"{sue_gift2_path=}")
    print(f"{sue_gift6_path=}")
    farm_giftunit = giftunit_shop(sue_str, _gifts_dir=sue_gifts_dir)
    assert os_path_exists(sue_gift2_path) is False
    assert farm_giftunit.gift_file_exists() is False

    # WHEN
    farm_giftunit._save_gift_file()

    # THEN
    assert farm_giftunit.gift_file_exists()


def test_GiftUnit_save_files_CorrectlySavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    x_fiscal_dir = f_path(fiscals_dir(), fiscal_id())
    x_owners_dir = f_path(x_fiscal_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")
    sue_gifts_dir = f_path(sue_owner_dir, get_gifts_folder())

    zia_str = "Zia"
    yao_str = "Yao"
    farm_delta_start = 4
    farm_giftunit = giftunit_shop(
        sue_str, _atoms_dir=sue_atoms_dir, _gifts_dir=sue_gifts_dir
    )
    farm_giftunit.set_delta_start(farm_delta_start)
    farm_giftunit.set_face(zia_str)
    farm_giftunit.set_face(yao_str)
    int4 = 4
    int5 = 5
    sports_atom = get_atom_example_itemunit_sports()
    knee_atom = get_atom_example_itemunit_knee()
    farm_giftunit._deltaunit.set_atomunit(sports_atom)
    farm_giftunit._deltaunit.set_atomunit(knee_atom)
    assert farm_giftunit.gift_file_exists() is False
    assert farm_giftunit.atom_file_exists(int4) is False
    assert farm_giftunit.atom_file_exists(int5) is False

    # WHEN
    farm_giftunit.save_files()

    # THEN
    assert farm_giftunit.gift_file_exists()
    assert farm_giftunit.atom_file_exists(int4)
    assert farm_giftunit.atom_file_exists(int5)


def test_GiftUnit_create_deltaunit_from_atom_files_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    x_fiscal_dir = f_path(fiscals_dir(), fiscal_id())
    x_owners_dir = f_path(x_fiscal_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")

    sue_giftunit = giftunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    int4 = 4
    int5 = 5
    int9 = 9
    spor_atom = get_atom_example_itemunit_sports()
    knee_atom = get_atom_example_itemunit_knee()
    ball_atom = get_atom_example_itemunit_ball()
    sue_giftunit._save_atom_file(int4, spor_atom)
    sue_giftunit._save_atom_file(int5, knee_atom)
    sue_giftunit._save_atom_file(int9, ball_atom)
    assert sue_giftunit._deltaunit == deltaunit_shop()

    # WHEN
    atoms_list = [int4, int5, int9]
    sue_giftunit._create_deltaunit_from_atom_files(atoms_list)

    # THEN
    static_deltaunit = deltaunit_shop()
    static_deltaunit.set_atomunit(spor_atom)
    static_deltaunit.set_atomunit(knee_atom)
    static_deltaunit.set_atomunit(ball_atom)
    assert sue_giftunit._deltaunit != deltaunit_shop()
    assert sue_giftunit._deltaunit == static_deltaunit


def test_create_giftunit_from_files_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    x_fiscal_dir = f_path(fiscals_dir(), fiscal_id())
    x_owners_dir = f_path(x_fiscal_dir, "owners")
    sue_str = "Sue"
    sue_owner_dir = f_path(x_owners_dir, sue_str)
    sue_atoms_dir = f_path(sue_owner_dir, "atoms")
    sue_gifts_dir = f_path(sue_owner_dir, get_gifts_folder())

    yao_str = "Yao"
    sue_delta_start = 4
    src_sue_giftunit = giftunit_shop(
        sue_str, _atoms_dir=sue_atoms_dir, _gifts_dir=sue_gifts_dir
    )
    src_sue_giftunit.set_delta_start(sue_delta_start)
    src_sue_giftunit.set_face(yao_str)
    sports_atom = get_atom_example_itemunit_sports()
    knee_atom = get_atom_example_itemunit_knee()
    ball_atom = get_atom_example_itemunit_ball()
    src_sue_giftunit._deltaunit.set_atomunit(sports_atom)
    src_sue_giftunit._deltaunit.set_atomunit(knee_atom)
    src_sue_giftunit._deltaunit.set_atomunit(ball_atom)
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
    assert src_sue_giftunit._deltaunit == new_sue_giftunit._deltaunit
