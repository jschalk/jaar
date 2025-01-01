from src.f00_instrument.file import (
    open_file,
    get_dir_file_strs,
    delete_dir,
    set_dir,
    save_file,
)
from src.f01_road.jaar_config import init_gift_id, get_test_cmty_idea as cmty_idea
from src.f04_gift.gift import giftunit_shop, get_json_filename
from src.f05_listen.hubunit import hubunit_shop
from src.f05_listen.examples.example_listen_atoms import get_atom_example_itemunit_knee
from src.f05_listen.examples.example_listen_gifts import (
    get_sue_giftunit,
    sue_1atomunits_giftunit,
    sue_2atomunits_giftunit,
    sue_3atomunits_giftunit,
    sue_4atomunits_giftunit,
)
from src.f05_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_HubUnit_get_max_gift_file_number_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)

    # WHEN / THEN
    delete_dir(sue_hubunit.gifts_dir())
    assert sue_hubunit.get_max_gift_file_number() is None
    assert sue_hubunit._get_next_gift_file_number() == init_gift_id()
    assert sue_hubunit._get_next_gift_file_number() == 0

    # ESTABLISH
    six_int = 6
    save_file(sue_hubunit.gifts_dir(), sue_hubunit.gift_file_name(six_int), "x")

    # WHEN / THEN
    assert sue_hubunit.get_max_gift_file_number() == six_int
    assert sue_hubunit._get_next_gift_file_number() == 7


def test_HubUnit_gift_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    assert sue_hubunit.gift_file_exists(None) is False
    assert sue_hubunit.gift_file_exists(0) is False
    six_int = 6
    print(f"{sue_hubunit.gift_file_path(six_int)=}")
    assert sue_hubunit.gift_file_exists(six_int) is False

    # WHEN
    save_file(sue_hubunit.gifts_dir(), sue_hubunit.gift_file_name(six_int), "x")

    # THEN
    assert sue_hubunit.gift_file_exists(None) is False
    assert sue_hubunit.gift_file_exists(0) is False
    assert sue_hubunit.gift_file_exists(six_int)


def test_HubUnit_save_gift_file_SaveCorrectObj(env_dir_setup_cleanup):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_gift2_path = f"{sue_hubunit.gifts_dir()}/{two_filename}"
    sue_gift0_path = f"{sue_hubunit.gifts_dir()}/{six_filename}"
    print(f"{sue_gift2_path=}")
    print(f"{sue_gift0_path=}")
    sue_giftunit = giftunit_shop(
        owner_name=sue_str,
        _gift_id=two_int,
        _atoms_dir=sue_hubunit.atoms_dir(),
        _gifts_dir=sue_hubunit.gifts_dir(),
    )
    assert sue_hubunit.gift_file_exists(two_int) is False
    assert sue_hubunit.gift_file_exists(six_int) is False

    # WHEN
    sue_hubunit.save_gift_file(sue_giftunit, correct_invalid_attrs=False)

    # THEN
    assert sue_hubunit.gift_file_exists(two_int)
    assert sue_hubunit.gift_file_exists(six_int) is False
    two_file_json = open_file(sue_hubunit.gifts_dir(), two_filename)
    assert two_file_json == sue_giftunit.get_deltametric_json()


def test_HubUnit_save_gift_file_RaisesErrorIfGiftUnit_atoms_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_hubunit.gifts_dir()}/{six_filename}"
    print(f"{sue_gift0_path=}")
    sue_giftunit = giftunit_shop(
        owner_name=sue_str,
        _gift_id=x_gift_id,
        _atoms_dir="src/incorrect_directory",
        _gifts_dir=sue_hubunit.gifts_dir(),
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_gift_file(sue_giftunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._atoms_dir is incorrect: {sue_giftunit._atoms_dir}. It must be {sue_hubunit.atoms_dir()}."
    )


def test_HubUnit_save_gift_file_RaisesErrorIfGiftUnit_gifts_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_hubunit.gifts_dir()}/{six_filename}"
    print(f"{sue_gift0_path=}")
    sue_giftunit = giftunit_shop(
        owner_name=sue_str,
        _gift_id=x_gift_id,
        _atoms_dir=sue_hubunit.atoms_dir(),
        _gifts_dir="src/incorrect_directory",
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_gift_file(sue_giftunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._gifts_dir is incorrect: {sue_giftunit._gifts_dir}. It must be {sue_hubunit.gifts_dir()}."
    )


def test_HubUnit_save_gift_file_RaisesErrorIfGiftUnit_owner_name_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_hubunit.gifts_dir()}/{six_filename}"
    print(f"{sue_gift0_path=}")
    bob_str = "Bob"
    sue_giftunit = giftunit_shop(
        owner_name=bob_str,
        _gift_id=x_gift_id,
        _atoms_dir=sue_hubunit.atoms_dir(),
        _gifts_dir=sue_hubunit.gifts_dir(),
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_gift_file(sue_giftunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit.owner_name is incorrect: {sue_giftunit.owner_name}. It must be {sue_str}."
    )


def test_HubUnit_save_gift_file_RaisesErrorIf_replace_IsFalse(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    x_gift_id = 0
    six_filename = get_json_filename(x_gift_id)
    sue_giftunit = giftunit_shop(
        owner_name=sue_str,
        _gift_id=x_gift_id,
        _atoms_dir=sue_hubunit.atoms_dir(),
        _gifts_dir=sue_hubunit.gifts_dir(),
    )
    saved_giftunit = sue_hubunit.save_gift_file(sue_giftunit)

    print(f"{sue_hubunit.gift_file_path(x_gift_id)=}")
    assert sue_hubunit.gift_file_exists(x_gift_id)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_gift_file(
            saved_giftunit, replace=False, correct_invalid_attrs=False
        )
    assert (
        str(excinfo.value)
        == f"GiftUnit file {six_filename} exists and cannot be saved over."
    )


def test_HubUnit_validate_giftunit_ReturnsObjWithAttributesFixed(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_gift2_path = f"{sue_hubunit.gifts_dir()}/{two_filename}"
    print(f"{sue_gift2_path=}")

    # WHEN
    invalid_sue_giftunit = giftunit_shop(
        owner_name="Bob",
        _gift_id=sue_hubunit._get_next_gift_file_number() - 5,
        _atoms_dir=f"{sue_hubunit.keeps_dir()}/swimming",
        _gifts_dir=f"{sue_hubunit.keeps_dir()}/swimming",
    )
    valid_giftunit = sue_hubunit.validate_giftunit(invalid_sue_giftunit)

    # THEN
    assert valid_giftunit._atoms_dir == sue_hubunit.atoms_dir()
    assert valid_giftunit._gifts_dir == sue_hubunit.gifts_dir()
    assert valid_giftunit._gift_id == sue_hubunit._get_next_gift_file_number()
    correct_sue_giftunit = giftunit_shop(
        owner_name=sue_str,
        _gift_id=sue_hubunit._get_next_gift_file_number(),
        _atoms_dir=sue_hubunit.atoms_dir(),
        _gifts_dir=sue_hubunit.gifts_dir(),
    )
    assert valid_giftunit == correct_sue_giftunit


def test_HubUnit_save_gift_file_SaveCorrectObj_correct_invalid_attrs_IsTrue(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    next_int = sue_hubunit._get_next_gift_file_number()
    next_filename = get_json_filename(next_int)
    sue_gift2_path = f"{sue_hubunit.gifts_dir()}/{next_filename}"
    print(f"{sue_gift2_path=}")
    assert sue_hubunit.gift_file_exists(next_int) is False

    # WHEN
    invalid_sue_giftunit = giftunit_shop(
        owner_name="Bob",
        _gift_id=sue_hubunit._get_next_gift_file_number() - 5,
        _atoms_dir=f"{sue_hubunit.keeps_dir()}/swimming",
        _gifts_dir=f"{sue_hubunit.keeps_dir()}/swimming",
    )
    sue_hubunit.save_gift_file(invalid_sue_giftunit)

    # THEN
    assert sue_hubunit.gift_file_exists(next_int)
    two_file_json = open_file(sue_hubunit.gifts_dir(), next_filename)


def test_HubUnit_default_giftunit_ReturnsObjWithCorrect_gift_id_WhenNogiftFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)

    # WHEN
    delete_dir(sue_hubunit.gifts_dir())
    sue_giftunit = sue_hubunit._default_giftunit()

    # THEN
    assert sue_giftunit.owner_name == sue_str
    assert sue_giftunit._gift_id == init_gift_id()
    assert sue_giftunit._gift_id == 0
    assert sue_giftunit._gift_id == sue_hubunit._get_next_gift_file_number()
    assert sue_giftunit.face_name is None
    assert sue_giftunit._atoms_dir == sue_hubunit.atoms_dir()
    assert sue_giftunit._gifts_dir == sue_hubunit.gifts_dir()


def test_HubUnit_default_giftunit_ReturnsObjWithCorrect_gift_id_WhengiftFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    delete_dir(sue_hubunit.gifts_dir())

    zero_giftunit = get_sue_giftunit()
    zero_giftunit._gift_id = sue_hubunit._get_next_gift_file_number()
    zero_giftunit._atoms_dir = sue_hubunit.atoms_dir()
    zero_giftunit._gifts_dir = sue_hubunit.gifts_dir()
    sue_hubunit.save_gift_file(zero_giftunit)

    # WHEN
    sue_giftunit = sue_hubunit._default_giftunit()

    # THEN
    assert sue_giftunit.owner_name == sue_str
    assert sue_giftunit._gift_id == init_gift_id() + 1
    assert sue_giftunit._gift_id == 1
    assert sue_giftunit._gift_id == sue_hubunit._get_next_gift_file_number()
    assert sue_giftunit.face_name is None
    assert sue_giftunit._atoms_dir == sue_hubunit.atoms_dir()
    assert sue_giftunit._gifts_dir == sue_hubunit.gifts_dir()


def test_HubUnit_get_giftunit_ReturnsCorrectObjWhenFilesDoesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    yao_str = "Yao"
    x0_giftunit = sue_hubunit._default_giftunit()
    x0_giftunit.set_face(yao_str)
    sue_hubunit.save_gift_file(x0_giftunit)
    bob_str = "Bob"
    x1_giftunit = sue_hubunit._default_giftunit()
    x1_giftunit.set_face(bob_str)
    sue_hubunit.save_gift_file(x1_giftunit)

    # WHEN
    y0_giftunit = sue_hubunit.get_giftunit(x0_giftunit._gift_id)
    y1_giftunit = sue_hubunit.get_giftunit(x1_giftunit._gift_id)

    # THEN
    assert y0_giftunit is not None
    assert y1_giftunit is not None
    assert yao_str in y0_giftunit.face_name
    assert bob_str not in y0_giftunit.face_name
    assert bob_str in y1_giftunit.face_name


def test_HubUnit_get_giftunit_RaisesExceptionWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    yao_str = "Yao"
    x0_giftunit = sue_hubunit._default_giftunit()
    x0_giftunit.set_face(yao_str)
    sue_hubunit.save_gift_file(x0_giftunit)
    bob_str = "Bob"
    x1_giftunit = sue_hubunit._default_giftunit()
    x1_giftunit.set_face(bob_str)
    sue_hubunit.save_gift_file(x1_giftunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_giftunit(six_file_number)
    assert (
        str(excinfo.value) == f"GiftUnit file_number {six_file_number} does not exist."
    )


def test_HubUnit_del_gift_file_DeletesgiftjsonAndNotAtomUnitjsons(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    six_int = 6
    sue_giftunit = giftunit_shop(
        owner_name=sue_str,
        _gift_id=six_int,
        _atoms_dir=sue_hubunit.atoms_dir(),
        _gifts_dir=sue_hubunit.gifts_dir(),
    )
    sue_giftunit._deltaunit.set_atomunit(get_atom_example_itemunit_knee())
    zero_int = 0
    assert sue_hubunit.gift_file_exists(six_int) is False
    assert sue_hubunit.atom_file_exists(zero_int) is False

    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    sue_hubunit.save_gift_file(sue_giftunit, correct_invalid_attrs=False)

    print(f"{get_dir_file_strs(sue_hubunit.atoms_dir())}")
    assert sue_hubunit.gift_file_exists(six_int)
    assert sue_hubunit.atom_file_exists(zero_int)

    # WHEN
    sue_hubunit._del_gift_file(sue_giftunit._gift_id)

    # THEN
    assert sue_hubunit.gift_file_exists(six_int) is False
    assert sue_hubunit.atom_file_exists(zero_int)


def test_HubUnit_save_gift_file_CanCreateAndModify3giftunits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    delete_dir(sue_hubunit.gifts_dir())
    delete_dir(sue_hubunit.atoms_dir())
    set_dir(sue_hubunit.gifts_dir())
    set_dir(sue_hubunit.atoms_dir())
    assert len(get_dir_file_strs(sue_hubunit.gifts_dir())) == 0
    assert len(get_dir_file_strs(sue_hubunit.atoms_dir())) == 0

    # WHEN
    sue_hubunit.save_gift_file(sue_2atomunits_giftunit())
    sue_hubunit.save_gift_file(sue_3atomunits_giftunit())
    sue_hubunit.save_gift_file(sue_4atomunits_giftunit())

    # THEN
    assert len(get_dir_file_strs(sue_hubunit.gifts_dir())) == 3
    assert len(get_dir_file_strs(sue_hubunit.atoms_dir())) == 9


def test_HubUnit_save_gift_file_ReturnsValidObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    sue2_giftunit = sue_2atomunits_giftunit()
    sue2_giftunit._atoms_dir = f"{sue_hubunit.keeps_dir()}/swimming"
    sue2_giftunit._gifts_dir = f"{sue_hubunit.keeps_dir()}/swimming"
    sue2_giftunit.owner_name = "Bob"
    sue2_giftunit._gift_id = sue_hubunit._get_next_gift_file_number() - 5
    prev_sue2_giftunit = copy_deepcopy(sue2_giftunit)

    # WHEN
    valid_giftunit = sue_hubunit.save_gift_file(sue2_giftunit)

    # THEN
    assert valid_giftunit._gifts_dir != prev_sue2_giftunit._gifts_dir
    assert valid_giftunit._gifts_dir == sue_hubunit.gifts_dir()
    assert valid_giftunit._atoms_dir == sue_hubunit.atoms_dir()
    assert valid_giftunit._gift_id != prev_sue2_giftunit._gift_id


def test_HubUnit_create_save_gift_file_SaveCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    two_int = 2
    three_int = 3
    print(f"{sue_hubunit.gift_file_path(two_int)=}")
    print(f"{sue_hubunit.gift_file_path(three_int)=}")
    sue_giftunit = giftunit_shop(
        owner_name=sue_str,
        _gift_id=two_int,
        _atoms_dir=sue_hubunit.atoms_dir(),
        _gifts_dir=sue_hubunit.gifts_dir(),
    )
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    sue_hubunit.save_gift_file(sue_giftunit, correct_invalid_attrs=False)
    assert sue_hubunit.gift_file_exists(two_int)
    assert sue_hubunit.gift_file_exists(three_int) is False

    # WHEN
    before_bud = sue_hubunit.default_voice_bud()
    bob_str = "Bob"
    after_bud = copy_deepcopy(before_bud)
    after_bud.add_acctunit(bob_str)
    sue_hubunit.create_save_gift_file(before_bud, after_bud)

    # THEN
    assert sue_hubunit.gift_file_exists(three_int)


def test_HubUnit_merge_any_gifts_ReturnsObjThatIsEqual(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    voice_bud = sue_hubunit.get_voice_bud()
    voice_bud.last_gift_id is None

    # WHEN
    new_bud = sue_hubunit._merge_any_gifts(voice_bud)

    # THEN
    assert new_bud == voice_bud


def test_HubUnit_merge_any_gifts_ReturnsObj_WithSinglegiftModifies_1atom(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    sue_hubunit.save_gift_file(sue_1atomunits_giftunit())
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    voice_bud = sue_hubunit.get_voice_bud()
    print(f"{voice_bud.cmty_idea=}")
    print(f"{sue_hubunit.cmty_idea=}")
    sports_str = "sports"
    sports_road = voice_bud.make_l1_road(sports_str)
    knee_str = "knee"
    knee_road = voice_bud.make_road(sports_road, knee_str)
    assert voice_bud.item_exists(sports_road) is False

    # WHEN
    new_bud = sue_hubunit._merge_any_gifts(voice_bud)

    # THEN
    assert new_bud != voice_bud
    assert new_bud.item_exists(sports_road)


def test_HubUnit_merge_any_gifts_ReturnsObj_WithSinglegiftModifies_2atoms(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), cmty_idea(), sue_str)
    sue_hubunit.save_gift_file(sue_2atomunits_giftunit())
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    voice_bud = sue_hubunit.get_voice_bud()
    print(f"{voice_bud.cmty_idea=}")
    sports_str = "sports"
    sports_road = voice_bud.make_l1_road(sports_str)
    knee_str = "knee"
    knee_road = voice_bud.make_road(sports_road, knee_str)
    assert voice_bud.item_exists(sports_road) is False
    assert voice_bud.item_exists(knee_road) is False

    # WHEN
    new_bud = sue_hubunit._merge_any_gifts(voice_bud)

    # THEN
    assert new_bud != voice_bud
    assert new_bud.item_exists(sports_road)
    assert new_bud.item_exists(knee_road)
