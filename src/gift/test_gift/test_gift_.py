from src._instrument.python_tool import x_is_json
from src._road.jaar_config import init_gift_id, get_gifts_folder
from src._road.road import get_default_real_id_roadnode as root_label
from src.gift.atom_config import real_id_str, owner_id_str
from src.gift.change import changeunit_shop
from src.gift.gift import GiftUnit, giftunit_shop, get_init_gift_id_if_None
from src.gift.examples.example_atoms import get_atom_example_ideaunit_sports
from src.gift.examples.example_changes import get_changeunit_sue_example


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
    assert x_giftunit.real_id is None
    assert x_giftunit.owner_id is None
    assert x_giftunit._gift_id is None
    assert x_giftunit._face_id is None
    assert x_giftunit._changeunit is None
    assert x_giftunit._change_start is None
    assert x_giftunit._gifts_dir is None
    assert x_giftunit._atoms_dir is None


def test_giftunit_shop_ReturnsCorrectObjEstablishWithEmptyArgs():
    # ESTABLISH
    bob_text = "Bob"

    # WHEN
    farm_giftunit = giftunit_shop(owner_id=bob_text)

    # THEN
    assert farm_giftunit.real_id == root_label()
    assert farm_giftunit.owner_id == bob_text
    assert farm_giftunit._gift_id == 0
    assert farm_giftunit._face_id is None
    assert farm_giftunit._changeunit == changeunit_shop()
    assert farm_giftunit._change_start == 0
    assert farm_giftunit._gifts_dir is None
    assert farm_giftunit._atoms_dir is None


def test_giftunit_shop_ReturnsCorrectObjEstablishWithNonEmptyArgs():
    # ESTABLISH
    bob_text = "Bob"
    bob_gift_id = 13
    sue_text = "Sue"
    bob_changeunit = get_changeunit_sue_example()
    bob_change_start = 6
    bob_gifts_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"
    music_text = "music"

    # WHEN
    farm_giftunit = giftunit_shop(
        real_id=music_text,
        owner_id=bob_text,
        _gift_id=bob_gift_id,
        _face_id=sue_text,
        _changeunit=bob_changeunit,
        _change_start=bob_change_start,
        _gifts_dir=bob_gifts_dir,
        _atoms_dir=bob_atoms_dir,
    )

    # THEN
    assert farm_giftunit.real_id == music_text
    assert farm_giftunit.owner_id == bob_text
    assert farm_giftunit._gift_id == bob_gift_id
    assert farm_giftunit._face_id == sue_text
    assert farm_giftunit._changeunit == bob_changeunit
    assert farm_giftunit._change_start == bob_change_start
    assert farm_giftunit._gifts_dir == bob_gifts_dir
    assert farm_giftunit._atoms_dir == bob_atoms_dir


def test_giftunit_shop_ReturnsCorrectObjEstablishWithSomeArgs_v1():
    # ESTABLISH
    bob_text = "Bob"
    yao_text = "Yao"

    # WHEN
    farm_giftunit = giftunit_shop(owner_id=bob_text, _face_id=yao_text)

    # THEN
    assert farm_giftunit.owner_id == bob_text
    assert farm_giftunit._face_id == yao_text


def test_GiftUnit_set_face_SetsAttribute():
    # ESTABLISH
    bob_text = "Bob"
    farm_giftunit = giftunit_shop(owner_id=bob_text)
    sue_text = "Sue"
    assert farm_giftunit._face_id is None
    assert farm_giftunit._face_id != sue_text

    # WHEN
    farm_giftunit.set_face(sue_text)

    # THEN
    assert farm_giftunit._face_id == sue_text


def test_GiftUnit_del_face_SetsAttribute():
    # ESTABLISH
    bob_text = "Bob"
    farm_giftunit = giftunit_shop(owner_id=bob_text)
    yao_text = "Yao"
    farm_giftunit.set_face(yao_text)
    assert farm_giftunit._face_id == yao_text

    # WHEN
    farm_giftunit.del_face()

    # THEN
    assert farm_giftunit._face_id != yao_text
    assert farm_giftunit._face_id is None


def test_GiftUnit_set_changeunit_SetsAttribute():
    # ESTABLISH
    bob_text = "Bob"
    farm_giftunit = giftunit_shop(owner_id=bob_text)
    assert farm_giftunit._changeunit == changeunit_shop()

    # WHEN
    farm_changeunit = changeunit_shop()
    farm_changeunit.set_atomunit(get_atom_example_ideaunit_sports())
    farm_giftunit.set_changeunit(farm_changeunit)

    # THEN
    assert farm_giftunit._changeunit == farm_changeunit


def test_GiftUnit_set_change_start_SetsAttribute():
    # ESTABLISH
    bob_text = "Bob"
    farm_giftunit = giftunit_shop(bob_text)
    assert farm_giftunit._change_start == 0

    # WHEN
    farm_change_start = 11
    farm_giftunit.set_change_start(farm_change_start)

    # THEN
    assert farm_giftunit._change_start == farm_change_start


def test_GiftUnit_atomunit_exists_ReturnsCorrectObj():
    # ESTABLISH
    bob_text = "Bob"
    farm_changeunit = changeunit_shop()
    farm_giftunit = giftunit_shop(owner_id=bob_text)
    farm_giftunit.set_changeunit(farm_changeunit)

    # WHEN
    sports_atomunit = get_atom_example_ideaunit_sports()

    # THEN
    assert farm_giftunit.atomunit_exists(sports_atomunit) is False

    # WHEN
    farm_changeunit.set_atomunit(sports_atomunit)
    farm_giftunit.set_changeunit(farm_changeunit)

    # THEN
    assert farm_giftunit.atomunit_exists(sports_atomunit)


def test_GiftUnit_del_changeunit_SetsAttribute():
    # ESTABLISH
    bob_text = "Bob"
    farm_changeunit = changeunit_shop()
    farm_changeunit.set_atomunit(get_atom_example_ideaunit_sports())
    farm_giftunit = giftunit_shop(owner_id=bob_text, _changeunit=farm_changeunit)
    assert farm_giftunit._changeunit != changeunit_shop()
    assert farm_giftunit._changeunit == farm_changeunit

    # WHEN
    farm_giftunit.del_changeunit()

    # THEN
    assert farm_giftunit._changeunit == changeunit_shop()


def test_GiftUnit_get_step_dict_ReturnsCorrectObj_Simple():
    # ESTABLISH
    bob_text = "Bob"
    sue_text = "Sue"
    music_text = "music"
    farm_giftunit = giftunit_shop(real_id=music_text, owner_id=bob_text)
    farm_giftunit.set_face(sue_text)

    # WHEN
    x_dict = farm_giftunit.get_step_dict()

    # THEN
    assert x_dict.get(real_id_str()) is not None
    assert x_dict.get(real_id_str()) == music_text
    assert x_dict.get(owner_id_str()) is not None
    assert x_dict.get(owner_id_str()) == bob_text

    face_id_text = "face_id"
    assert x_dict.get(face_id_text) is not None
    assert x_dict.get(face_id_text) == sue_text

    change_text = "change"
    assert x_dict.get(change_text) is not None
    assert x_dict.get(change_text) == changeunit_shop().get_ordered_atomunits()
    assert x_dict.get(change_text) == {}


def test_GiftUnit_get_step_dict_ReturnsCorrectObj_WithChangePopulated():
    # ESTABLISH
    bob_text = "Bob"
    sue_changeunit = get_changeunit_sue_example()
    farm_giftunit = giftunit_shop(bob_text, _changeunit=sue_changeunit)

    # WHEN
    x_dict = farm_giftunit.get_step_dict()

    # THEN
    change_text = "change"
    assert x_dict.get(change_text) is not None
    assert x_dict.get(change_text) == sue_changeunit.get_ordered_atomunits()
    sue_atomunits_dict = x_dict.get(change_text)
    print(f"{len(sue_changeunit.get_sorted_atomunits())=}")
    print(f"{sue_atomunits_dict.keys()=}")
    # print(f"{sue_atomunits_dict.get(0)=}")
    assert sue_atomunits_dict.get(2) is None
    assert sue_atomunits_dict.get(0) is not None
    assert sue_atomunits_dict.get(1) is not None


def test_GiftUnit_get_step_dict_ReturnsCorrectObj_change_start():
    # ESTABLISH
    bob_text = "Bob"
    sue_changeunit = get_changeunit_sue_example()
    farm_change_start = 7
    farm_giftunit = giftunit_shop(
        bob_text, _changeunit=sue_changeunit, _change_start=farm_change_start
    )

    # WHEN
    x_dict = farm_giftunit.get_step_dict()

    # THEN
    change_text = "change"
    assert x_dict.get(change_text) is not None
    assert x_dict.get(change_text) == sue_changeunit.get_ordered_atomunits(
        farm_change_start
    )
    sue_atomunits_dict = x_dict.get(change_text)
    print(f"{len(sue_changeunit.get_sorted_atomunits())=}")
    print(f"{sue_atomunits_dict.keys()=}")
    # print(f"{sue_atomunits_dict.get(0)=}")
    assert sue_atomunits_dict.get(farm_change_start + 2) is None
    assert sue_atomunits_dict.get(farm_change_start + 0) is not None
    assert sue_atomunits_dict.get(farm_change_start + 1) is not None


def test_GiftUnit_get_change_atom_numbers_ReturnsCorrectObj():
    # ESTABLISH
    bob_text = "Bob"
    yao_text = "Yao"
    sue_changeunit = get_changeunit_sue_example()
    farm_change_start = 7
    farm_giftunit = giftunit_shop(bob_text)
    farm_giftunit.set_changeunit(sue_changeunit)
    farm_giftunit.set_change_start(farm_change_start)
    farm_giftunit.set_face(yao_text)
    farm_dict = farm_giftunit.get_step_dict()

    # WHEN
    farm_change_atom_numbers = farm_giftunit.get_change_atom_numbers(farm_dict)
    # THEN
    assert farm_change_atom_numbers == [farm_change_start, farm_change_start + 1]


def test_GiftUnit_get_changemetric_dict_ReturnsCorrectObj():
    # ESTABLISH
    bob_text = "Bob"
    yao_text = "Yao"
    sue_changeunit = get_changeunit_sue_example()
    farm_change_start = 7
    farm_giftunit = giftunit_shop(bob_text)
    farm_giftunit.set_changeunit(sue_changeunit)
    farm_giftunit.set_change_start(farm_change_start)
    farm_giftunit.set_face(yao_text)

    # WHEN
    x_dict = farm_giftunit.get_changemetric_dict()

    # THEN
    assert x_dict.get(owner_id_str()) is not None
    assert x_dict.get(owner_id_str()) == bob_text

    face_id_text = "face_id"
    assert x_dict.get(face_id_text) is not None
    assert x_dict.get(face_id_text) == yao_text

    change_atom_numbers_text = "change_atom_numbers"
    assert x_dict.get(change_atom_numbers_text) is not None
    assert x_dict.get(change_atom_numbers_text) == [7, 8]

    change_min_text = "change_min"
    assert x_dict.get(change_min_text) is None
    change_max_text = "change_max"
    assert x_dict.get(change_max_text) is None


def test_GiftUnit_get_changemetric_json_ReturnsCorrectObj():
    # ESTABLISH
    bob_text = "Bob"
    sue_text = "Sue"
    yao_text = "Yao"
    sue_changeunit = get_changeunit_sue_example()
    farm_change_start = 7
    farm_giftunit = giftunit_shop(bob_text)
    farm_giftunit.set_changeunit(sue_changeunit)
    farm_giftunit.set_change_start(farm_change_start)
    farm_giftunit.set_face(sue_text)
    farm_giftunit.set_face(yao_text)

    # WHEN
    farm_json = farm_giftunit.get_changemetric_json()

    # THEN
    assert x_is_json(farm_json)
