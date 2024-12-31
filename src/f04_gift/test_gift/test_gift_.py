from src.f00_instrument.dict_toolbox import x_is_json
from src.f01_road.jaar_config import init_gift_id, get_gifts_folder
from src.f01_road.road import get_default_gov_idea as root_idea
from src.f04_gift.atom_config import gov_idea_str, owner_name_str, face_name_str
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
    assert not x_giftunit.face_name
    assert not x_giftunit.gov_idea
    assert not x_giftunit.owner_name
    assert not x_giftunit._gift_id
    assert not x_giftunit._deltaunit
    assert not x_giftunit._delta_start
    assert not x_giftunit._gifts_dir
    assert not x_giftunit._atoms_dir


def test_giftunit_shop_ReturnsCorrectObjEstablishWithEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_giftunit = giftunit_shop(owner_name=bob_str)

    # THEN
    assert not bob_giftunit.face_name
    assert bob_giftunit.gov_idea == root_idea()
    assert bob_giftunit.owner_name == bob_str
    assert bob_giftunit._gift_id == 0
    assert bob_giftunit._deltaunit == deltaunit_shop()
    assert bob_giftunit._delta_start == 0
    assert not bob_giftunit._gifts_dir
    assert not bob_giftunit._atoms_dir


def test_giftunit_shop_ReturnsCorrectObjEstablishWithNonEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"
    bob_gift_id = 13
    sue_str = "Sue"
    bob_deltaunit = get_deltaunit_sue_example()
    bob_delta_start = 6
    bob_gifts_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"
    accord45_str = "accord45"

    # WHEN
    bob_giftunit = giftunit_shop(
        face_name=sue_str,
        owner_name=bob_str,
        gov_idea=accord45_str,
        _gift_id=bob_gift_id,
        _deltaunit=bob_deltaunit,
        _delta_start=bob_delta_start,
        _gifts_dir=bob_gifts_dir,
        _atoms_dir=bob_atoms_dir,
    )

    # THEN
    assert bob_giftunit.face_name == sue_str
    assert bob_giftunit.owner_name == bob_str
    assert bob_giftunit.gov_idea == accord45_str
    assert bob_giftunit._gift_id == bob_gift_id
    assert bob_giftunit._deltaunit == bob_deltaunit
    assert bob_giftunit._delta_start == bob_delta_start
    assert bob_giftunit._gifts_dir == bob_gifts_dir
    assert bob_giftunit._atoms_dir == bob_atoms_dir


def test_giftunit_shop_ReturnsCorrectObjEstablishWithSomeArgs_v1():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"

    # WHEN
    bob_giftunit = giftunit_shop(owner_name=bob_str, face_name=yao_str)

    # THEN
    assert bob_giftunit.owner_name == bob_str
    assert bob_giftunit.face_name == yao_str


def test_GiftUnit_set_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_giftunit = giftunit_shop(owner_name=bob_str)
    sue_str = "Sue"
    assert bob_giftunit.face_name is None
    assert bob_giftunit.face_name != sue_str

    # WHEN
    bob_giftunit.set_face(sue_str)

    # THEN
    assert bob_giftunit.face_name == sue_str


def test_GiftUnit_del_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_giftunit = giftunit_shop(owner_name=bob_str)
    yao_str = "Yao"
    bob_giftunit.set_face(yao_str)
    assert bob_giftunit.face_name == yao_str

    # WHEN
    bob_giftunit.del_face()

    # THEN
    assert bob_giftunit.face_name != yao_str
    assert bob_giftunit.face_name is None


def test_GiftUnit_set_deltaunit_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_giftunit = giftunit_shop(owner_name=bob_str)
    assert bob_giftunit._deltaunit == deltaunit_shop()

    # WHEN
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(get_atom_example_itemunit_sports())
    bob_giftunit.set_deltaunit(x_deltaunit)

    # THEN
    assert bob_giftunit._deltaunit == x_deltaunit


def test_GiftUnit_set_delta_start_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_giftunit = giftunit_shop(bob_str)
    assert bob_giftunit._delta_start == 0

    # WHEN
    x_delta_start = 11
    bob_giftunit.set_delta_start(x_delta_start)

    # THEN
    assert bob_giftunit._delta_start == x_delta_start


def test_GiftUnit_atomunit_exists_ReturnsCorrectObj():
    # ESTABLISH
    bob_str = "Bob"
    x_deltaunit = deltaunit_shop()
    bob_giftunit = giftunit_shop(owner_name=bob_str)
    bob_giftunit.set_deltaunit(x_deltaunit)

    # WHEN
    sports_atomunit = get_atom_example_itemunit_sports()

    # THEN
    assert bob_giftunit.atomunit_exists(sports_atomunit) is False

    # WHEN
    x_deltaunit.set_atomunit(sports_atomunit)
    bob_giftunit.set_deltaunit(x_deltaunit)

    # THEN
    assert bob_giftunit.atomunit_exists(sports_atomunit)


def test_GiftUnit_del_deltaunit_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    x_deltaunit = deltaunit_shop()
    x_deltaunit.set_atomunit(get_atom_example_itemunit_sports())
    bob_giftunit = giftunit_shop(owner_name=bob_str, _deltaunit=x_deltaunit)
    assert bob_giftunit._deltaunit != deltaunit_shop()
    assert bob_giftunit._deltaunit == x_deltaunit

    # WHEN
    bob_giftunit.del_deltaunit()

    # THEN
    assert bob_giftunit._deltaunit == deltaunit_shop()


def test_GiftUnit_get_step_dict_ReturnsCorrectObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    accord45_str = "accord45"
    bob_giftunit = giftunit_shop(gov_idea=accord45_str, owner_name=bob_str)
    bob_giftunit.set_face(sue_str)

    # WHEN
    x_dict = bob_giftunit.get_step_dict()

    # THEN
    assert x_dict.get(gov_idea_str()) is not None
    assert x_dict.get(gov_idea_str()) == accord45_str
    assert x_dict.get(owner_name_str()) is not None
    assert x_dict.get(owner_name_str()) == bob_str
    assert x_dict.get(face_name_str()) is not None
    assert x_dict.get(face_name_str()) == sue_str

    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == deltaunit_shop().get_ordered_atomunits()
    assert x_dict.get(delta_str) == {}


def test_GiftUnit_get_step_dict_ReturnsObj_WithDeltaUnitPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_deltaunit = get_deltaunit_sue_example()
    bob_giftunit = giftunit_shop(bob_str, _deltaunit=sue_deltaunit)

    # WHEN
    x_dict = bob_giftunit.get_step_dict()

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
    x_delta_start = 7
    bob_giftunit = giftunit_shop(
        bob_str, _deltaunit=sue_deltaunit, _delta_start=x_delta_start
    )

    # WHEN
    x_dict = bob_giftunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == sue_deltaunit.get_ordered_atomunits(x_delta_start)
    sue_atomunits_dict = x_dict.get(delta_str)
    print(f"{len(sue_deltaunit.get_sorted_atomunits())=}")
    print(f"{sue_atomunits_dict.keys()=}")
    # print(f"{sue_atomunits_dict.get(0)=}")
    assert sue_atomunits_dict.get(x_delta_start + 2) is None
    assert sue_atomunits_dict.get(x_delta_start + 0) is not None
    assert sue_atomunits_dict.get(x_delta_start + 1) is not None


def test_GiftUnit_get_delta_atom_numbers_ReturnsCorrectObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_deltaunit = get_deltaunit_sue_example()
    x_delta_start = 7
    bob_giftunit = giftunit_shop(bob_str)
    bob_giftunit.set_deltaunit(sue_deltaunit)
    bob_giftunit.set_delta_start(x_delta_start)
    bob_giftunit.set_face(yao_str)
    x_dict = bob_giftunit.get_step_dict()

    # WHEN
    x_delta_atom_numbers = bob_giftunit.get_delta_atom_numbers(x_dict)
    # THEN
    assert x_delta_atom_numbers == [x_delta_start, x_delta_start + 1]


def test_GiftUnit_get_deltametric_dict_ReturnsCorrectObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_deltaunit = get_deltaunit_sue_example()
    x_delta_start = 7
    bob_giftunit = giftunit_shop(bob_str)
    bob_giftunit.set_deltaunit(sue_deltaunit)
    bob_giftunit.set_delta_start(x_delta_start)
    bob_giftunit.set_face(yao_str)

    # WHEN
    x_dict = bob_giftunit.get_deltametric_dict()

    # THEN
    assert x_dict.get(owner_name_str()) is not None
    assert x_dict.get(owner_name_str()) == bob_str

    assert x_dict.get(face_name_str()) is not None
    assert x_dict.get(face_name_str()) == yao_str

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
    x_delta_start = 7
    bob_giftunit = giftunit_shop(bob_str)
    bob_giftunit.set_deltaunit(sue_deltaunit)
    bob_giftunit.set_delta_start(x_delta_start)
    bob_giftunit.set_face(sue_str)
    bob_giftunit.set_face(yao_str)

    # WHEN
    delta_json = bob_giftunit.get_deltametric_json()

    # THEN
    assert x_is_json(delta_json)
