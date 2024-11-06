from src.f00_instrument.dict_toolbox import x_is_json
from src.f01_road.jaar_config import init_gift_id, get_gifts_folder
from src.f01_road.road import get_default_fiscal_id_roadnode as root_label
from src.f04_gift.atom_config import fiscal_id_str, owner_id_str, face_id_str
from src.f04_gift.delta import deltaunit_shop
from src.f04_gift.gift import GiftUnit, giftunit_shop, get_init_gift_id_if_None
from src.f04_gift.examples.example_atoms import get_atom_example_itemunit_sports
from src.f04_gift.examples.example_deltas import get_deltaunit_sue_example


def test_get_gifts_folder_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    assert get_gifts_folder() == "gifts"


def test_init_gift_id_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    assert init_gift_id() == 0


def test_get_init_gift_id_if_None_ReturnsCorrectObj():
    # ESTABLISH / WHEN / THEN
    assert get_init_gift_id_if_None() == init_gift_id()
    assert get_init_gift_id_if_None(None) == init_gift_id()
    assert get_init_gift_id_if_None(1) == 1


def test_GiftUnit_exists():
    # ESTABLISH / WHEN
    x_giftunit = GiftUnit()

    # THEN
    assert x_giftunit.fiscal_id is None
    assert x_giftunit.owner_id is None
    assert x_giftunit._gift_id is None
    assert x_giftunit._face_id is None
    assert x_giftunit._deltaunit is None
    assert x_giftunit._delta_start is None
    assert x_giftunit._gifts_dir is None
    assert x_giftunit._atoms_dir is None


def test_giftunit_shop_ReturnsCorrectObjEstablishWithEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    farm_giftunit = giftunit_shop(owner_id=bob_str)

    # THEN
    assert farm_giftunit.fiscal_id == root_label()
    assert farm_giftunit.owner_id == bob_str
    assert farm_giftunit._gift_id == 0
    assert farm_giftunit._face_id is None
    assert farm_giftunit._deltaunit == deltaunit_shop()
    assert farm_giftunit._delta_start == 0
    assert farm_giftunit._gifts_dir is None
    assert farm_giftunit._atoms_dir is None


def test_giftunit_shop_ReturnsCorrectObjEstablishWithNonEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"
    bob_gift_id = 13
    sue_str = "Sue"
    bob_deltaunit = get_deltaunit_sue_example()
    bob_delta_start = 6
    bob_gifts_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"
    music_str = "music"

    # WHEN
    farm_giftunit = giftunit_shop(
        fiscal_id=music_str,
        owner_id=bob_str,
        _gift_id=bob_gift_id,
        _face_id=sue_str,
        _deltaunit=bob_deltaunit,
        _delta_start=bob_delta_start,
        _gifts_dir=bob_gifts_dir,
        _atoms_dir=bob_atoms_dir,
    )

    # THEN
    assert farm_giftunit.fiscal_id == music_str
    assert farm_giftunit.owner_id == bob_str
    assert farm_giftunit._gift_id == bob_gift_id
    assert farm_giftunit._face_id == sue_str
    assert farm_giftunit._deltaunit == bob_deltaunit
    assert farm_giftunit._delta_start == bob_delta_start
    assert farm_giftunit._gifts_dir == bob_gifts_dir
    assert farm_giftunit._atoms_dir == bob_atoms_dir


def test_giftunit_shop_ReturnsCorrectObjEstablishWithSomeArgs_v1():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"

    # WHEN
    farm_giftunit = giftunit_shop(owner_id=bob_str, _face_id=yao_str)

    # THEN
    assert farm_giftunit.owner_id == bob_str
    assert farm_giftunit._face_id == yao_str


def test_GiftUnit_set_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    farm_giftunit = giftunit_shop(owner_id=bob_str)
    sue_str = "Sue"
    assert farm_giftunit._face_id is None
    assert farm_giftunit._face_id != sue_str

    # WHEN
    farm_giftunit.set_face(sue_str)

    # THEN
    assert farm_giftunit._face_id == sue_str


def test_GiftUnit_del_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    farm_giftunit = giftunit_shop(owner_id=bob_str)
    yao_str = "Yao"
    farm_giftunit.set_face(yao_str)
    assert farm_giftunit._face_id == yao_str

    # WHEN
    farm_giftunit.del_face()

    # THEN
    assert farm_giftunit._face_id != yao_str
    assert farm_giftunit._face_id is None


def test_GiftUnit_set_deltaunit_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    farm_giftunit = giftunit_shop(owner_id=bob_str)
    assert farm_giftunit._deltaunit == deltaunit_shop()

    # WHEN
    farm_deltaunit = deltaunit_shop()
    farm_deltaunit.set_atomunit(get_atom_example_itemunit_sports())
    farm_giftunit.set_deltaunit(farm_deltaunit)

    # THEN
    assert farm_giftunit._deltaunit == farm_deltaunit


def test_GiftUnit_set_delta_start_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    farm_giftunit = giftunit_shop(bob_str)
    assert farm_giftunit._delta_start == 0

    # WHEN
    farm_delta_start = 11
    farm_giftunit.set_delta_start(farm_delta_start)

    # THEN
    assert farm_giftunit._delta_start == farm_delta_start


def test_GiftUnit_atomunit_exists_ReturnsCorrectObj():
    # ESTABLISH
    bob_str = "Bob"
    farm_deltaunit = deltaunit_shop()
    farm_giftunit = giftunit_shop(owner_id=bob_str)
    farm_giftunit.set_deltaunit(farm_deltaunit)

    # WHEN
    sports_atomunit = get_atom_example_itemunit_sports()

    # THEN
    assert farm_giftunit.atomunit_exists(sports_atomunit) is False

    # WHEN
    farm_deltaunit.set_atomunit(sports_atomunit)
    farm_giftunit.set_deltaunit(farm_deltaunit)

    # THEN
    assert farm_giftunit.atomunit_exists(sports_atomunit)


def test_GiftUnit_del_deltaunit_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    farm_deltaunit = deltaunit_shop()
    farm_deltaunit.set_atomunit(get_atom_example_itemunit_sports())
    farm_giftunit = giftunit_shop(owner_id=bob_str, _deltaunit=farm_deltaunit)
    assert farm_giftunit._deltaunit != deltaunit_shop()
    assert farm_giftunit._deltaunit == farm_deltaunit

    # WHEN
    farm_giftunit.del_deltaunit()

    # THEN
    assert farm_giftunit._deltaunit == deltaunit_shop()


def test_GiftUnit_get_step_dict_ReturnsCorrectObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    music_str = "music"
    farm_giftunit = giftunit_shop(fiscal_id=music_str, owner_id=bob_str)
    farm_giftunit.set_face(sue_str)

    # WHEN
    x_dict = farm_giftunit.get_step_dict()

    # THEN
    assert x_dict.get(fiscal_id_str()) is not None
    assert x_dict.get(fiscal_id_str()) == music_str
    assert x_dict.get(owner_id_str()) is not None
    assert x_dict.get(owner_id_str()) == bob_str
    assert x_dict.get(face_id_str()) is not None
    assert x_dict.get(face_id_str()) == sue_str

    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == deltaunit_shop().get_ordered_atomunits()
    assert x_dict.get(delta_str) == {}


def test_GiftUnit_get_step_dict_ReturnsCorrectObj_WithDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_deltaunit = get_deltaunit_sue_example()
    farm_giftunit = giftunit_shop(bob_str, _deltaunit=sue_deltaunit)

    # WHEN
    x_dict = farm_giftunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == sue_deltaunit.get_ordered_atomunits()
    sue_atomunits_dict = x_dict.get(delta_str)
    print(f"{len(sue_deltaunit.get_sorted_atomunits())=}")
    print(f"{sue_atomunits_dict.keys()=}")
    # print(f"{sue_atomunits_dict.get(0)=}")
    assert sue_atomunits_dict.get(2) is None
    assert sue_atomunits_dict.get(0) is not None
    assert sue_atomunits_dict.get(1) is not None


def test_GiftUnit_get_step_dict_ReturnsCorrectObj_delta_start():
    # ESTABLISH
    bob_str = "Bob"
    sue_deltaunit = get_deltaunit_sue_example()
    farm_delta_start = 7
    farm_giftunit = giftunit_shop(
        bob_str, _deltaunit=sue_deltaunit, _delta_start=farm_delta_start
    )

    # WHEN
    x_dict = farm_giftunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == sue_deltaunit.get_ordered_atomunits(
        farm_delta_start
    )
    sue_atomunits_dict = x_dict.get(delta_str)
    print(f"{len(sue_deltaunit.get_sorted_atomunits())=}")
    print(f"{sue_atomunits_dict.keys()=}")
    # print(f"{sue_atomunits_dict.get(0)=}")
    assert sue_atomunits_dict.get(farm_delta_start + 2) is None
    assert sue_atomunits_dict.get(farm_delta_start + 0) is not None
    assert sue_atomunits_dict.get(farm_delta_start + 1) is not None


def test_GiftUnit_get_delta_atom_numbers_ReturnsCorrectObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_deltaunit = get_deltaunit_sue_example()
    farm_delta_start = 7
    farm_giftunit = giftunit_shop(bob_str)
    farm_giftunit.set_deltaunit(sue_deltaunit)
    farm_giftunit.set_delta_start(farm_delta_start)
    farm_giftunit.set_face(yao_str)
    farm_dict = farm_giftunit.get_step_dict()

    # WHEN
    farm_delta_atom_numbers = farm_giftunit.get_delta_atom_numbers(farm_dict)
    # THEN
    assert farm_delta_atom_numbers == [farm_delta_start, farm_delta_start + 1]


def test_GiftUnit_get_deltametric_dict_ReturnsCorrectObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_deltaunit = get_deltaunit_sue_example()
    farm_delta_start = 7
    farm_giftunit = giftunit_shop(bob_str)
    farm_giftunit.set_deltaunit(sue_deltaunit)
    farm_giftunit.set_delta_start(farm_delta_start)
    farm_giftunit.set_face(yao_str)

    # WHEN
    x_dict = farm_giftunit.get_deltametric_dict()

    # THEN
    assert x_dict.get(owner_id_str()) is not None
    assert x_dict.get(owner_id_str()) == bob_str

    assert x_dict.get(face_id_str()) is not None
    assert x_dict.get(face_id_str()) == yao_str

    delta_atom_numbers_str = "delta_atom_numbers"
    assert x_dict.get(delta_atom_numbers_str) is not None
    assert x_dict.get(delta_atom_numbers_str) == [7, 8]

    delta_min_str = "delta_min"
    assert x_dict.get(delta_min_str) is None
    delta_max_str = "delta_max"
    assert x_dict.get(delta_max_str) is None


def test_GiftUnit_get_deltametric_json_ReturnsCorrectObj():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    sue_deltaunit = get_deltaunit_sue_example()
    farm_delta_start = 7
    farm_giftunit = giftunit_shop(bob_str)
    farm_giftunit.set_deltaunit(sue_deltaunit)
    farm_giftunit.set_delta_start(farm_delta_start)
    farm_giftunit.set_face(sue_str)
    farm_giftunit.set_face(yao_str)

    # WHEN
    farm_json = farm_giftunit.get_deltametric_json()

    # THEN
    assert x_is_json(farm_json)
