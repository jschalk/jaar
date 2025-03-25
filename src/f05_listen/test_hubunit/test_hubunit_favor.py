from src.f00_instrument.file import (
    open_file,
    get_dir_file_strs,
    delete_dir,
    set_dir,
    save_file,
    create_path,
)
from src.f01_road.jaar_config import init_favor_id, get_test_fisc_title as fisc_title
from src.f04_favor.favor import favorunit_shop, get_json_filename
from src.f05_listen.hubunit import hubunit_shop
from src.f05_listen.examples.example_listen_atoms import get_atom_example_itemunit_knee
from src.f05_listen.examples.example_listen_favors import (
    get_sue_favorunit,
    sue_1budatoms_favorunit,
    sue_2budatoms_favorunit,
    sue_3budatoms_favorunit,
    sue_4budatoms_favorunit,
)
from src.f05_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_HubUnit_get_max_favor_file_number_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)

    # WHEN / THEN
    delete_dir(sue_hubunit._favors_dir)
    assert sue_hubunit.get_max_favor_file_number() is None
    assert sue_hubunit._get_next_favor_file_number() == init_favor_id()
    assert sue_hubunit._get_next_favor_file_number() == 0

    # ESTABLISH
    six_int = 6
    save_file(sue_hubunit._favors_dir, sue_hubunit.favor_filename(six_int), "x")

    # WHEN / THEN
    assert sue_hubunit.get_max_favor_file_number() == six_int
    assert sue_hubunit._get_next_favor_file_number() == 7


def test_HubUnit_favor_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    assert sue_hubunit.favor_file_exists(None) is False
    assert sue_hubunit.favor_file_exists(0) is False
    six_int = 6
    print(f"{sue_hubunit.favor_file_path(six_int)=}")
    assert sue_hubunit.favor_file_exists(six_int) is False

    # WHEN
    save_file(sue_hubunit._favors_dir, sue_hubunit.favor_filename(six_int), "x")

    # THEN
    assert sue_hubunit.favor_file_exists(None) is False
    assert sue_hubunit.favor_file_exists(0) is False
    assert sue_hubunit.favor_file_exists(six_int)


def test_HubUnit_save_favor_file_SaveCorrectObj(env_dir_setup_cleanup):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_favor2_path = create_path(sue_hubunit._favors_dir, two_filename)
    sue_favor6_path = create_path(sue_hubunit._favors_dir, six_filename)
    print(f"{sue_favor2_path=}")
    print(f"{sue_favor6_path=}")
    sue_favorunit = favorunit_shop(
        owner_name=sue_str,
        _favor_id=two_int,
        _atoms_dir=sue_hubunit._atoms_dir,
        _favors_dir=sue_hubunit._favors_dir,
    )
    assert sue_hubunit.favor_file_exists(two_int) is False
    assert sue_hubunit.favor_file_exists(six_int) is False

    # WHEN
    sue_hubunit.save_favor_file(sue_favorunit, correct_invalid_attrs=False)

    # THEN
    assert sue_hubunit.favor_file_exists(two_int)
    assert sue_hubunit.favor_file_exists(six_int) is False
    two_file_json = open_file(sue_hubunit._favors_dir, two_filename)
    assert two_file_json == sue_favorunit.get_deltametric_json()


def test_HubUnit_save_favor_file_RaisesErrorIfFavorUnit_atoms_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    x_favor_id = 6
    six_filename = get_json_filename(x_favor_id)
    sue_favor0_path = create_path(sue_hubunit._favors_dir, six_filename)
    print(f"{sue_favor0_path=}")
    sue_favorunit = favorunit_shop(
        owner_name=sue_str,
        _favor_id=x_favor_id,
        _atoms_dir="src/incorrect_directory",
        _favors_dir=sue_hubunit._favors_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_favor_file(sue_favorunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"FavorUnit file cannot be saved because favorunit._atoms_dir is incorrect: {sue_favorunit._atoms_dir}. It must be {sue_hubunit._atoms_dir}."
    )


def test_HubUnit_save_favor_file_RaisesErrorIfFavorUnit_favors_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    x_favor_id = 6
    six_filename = get_json_filename(x_favor_id)
    sue_favor0_path = create_path(sue_hubunit._favors_dir, six_filename)
    print(f"{sue_favor0_path=}")
    sue_favorunit = favorunit_shop(
        owner_name=sue_str,
        _favor_id=x_favor_id,
        _atoms_dir=sue_hubunit._atoms_dir,
        _favors_dir="src/incorrect_directory",
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_favor_file(sue_favorunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"FavorUnit file cannot be saved because favorunit._favors_dir is incorrect: {sue_favorunit._favors_dir}. It must be {sue_hubunit._favors_dir}."
    )


def test_HubUnit_save_favor_file_RaisesErrorIfFavorUnit_owner_name_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    x_favor_id = 6
    six_filename = get_json_filename(x_favor_id)
    sue_favor0_path = create_path(sue_hubunit._favors_dir, six_filename)
    print(f"{sue_favor0_path=}")
    bob_str = "Bob"
    sue_favorunit = favorunit_shop(
        owner_name=bob_str,
        _favor_id=x_favor_id,
        _atoms_dir=sue_hubunit._atoms_dir,
        _favors_dir=sue_hubunit._favors_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_favor_file(sue_favorunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"FavorUnit file cannot be saved because favorunit.owner_name is incorrect: {sue_favorunit.owner_name}. It must be {sue_str}."
    )


def test_HubUnit_save_favor_file_RaisesErrorIf_replace_IsFalse(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    x_favor_id = 0
    six_filename = get_json_filename(x_favor_id)
    sue_favorunit = favorunit_shop(
        owner_name=sue_str,
        _favor_id=x_favor_id,
        _atoms_dir=sue_hubunit._atoms_dir,
        _favors_dir=sue_hubunit._favors_dir,
    )
    saved_favorunit = sue_hubunit.save_favor_file(sue_favorunit)

    print(f"{sue_hubunit.favor_file_path(x_favor_id)=}")
    assert sue_hubunit.favor_file_exists(x_favor_id)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_favor_file(
            saved_favorunit, replace=False, correct_invalid_attrs=False
        )
    assert (
        str(excinfo.value)
        == f"FavorUnit file {six_filename} exists and cannot be saved over."
    )


def test_HubUnit_validate_favorunit_ReturnsObjWithAttributesFixed(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_favor2_path = create_path(sue_hubunit._favors_dir, two_filename)
    print(f"{sue_favor2_path=}")

    # WHEN
    invalid_sue_favorunit = favorunit_shop(
        owner_name="Bob",
        _favor_id=sue_hubunit._get_next_favor_file_number() - 5,
        _atoms_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
        _favors_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
    )
    valid_favorunit = sue_hubunit.validate_favorunit(invalid_sue_favorunit)

    # THEN
    assert valid_favorunit._atoms_dir == sue_hubunit._atoms_dir
    assert valid_favorunit._favors_dir == sue_hubunit._favors_dir
    assert valid_favorunit._favor_id == sue_hubunit._get_next_favor_file_number()
    correct_sue_favorunit = favorunit_shop(
        owner_name=sue_str,
        _favor_id=sue_hubunit._get_next_favor_file_number(),
        _atoms_dir=sue_hubunit._atoms_dir,
        _favors_dir=sue_hubunit._favors_dir,
    )
    assert valid_favorunit == correct_sue_favorunit


def test_HubUnit_save_favor_file_SaveCorrectObj_correct_invalid_attrs_IsTrue(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    next_int = sue_hubunit._get_next_favor_file_number()
    next_filename = get_json_filename(next_int)
    sue_favor2_path = create_path(sue_hubunit._favors_dir, next_filename)
    print(f"{sue_favor2_path=}")
    assert sue_hubunit.favor_file_exists(next_int) is False

    # WHEN
    invalid_sue_favorunit = favorunit_shop(
        owner_name="Bob",
        _favor_id=sue_hubunit._get_next_favor_file_number() - 5,
        _atoms_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
        _favors_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
    )
    sue_hubunit.save_favor_file(invalid_sue_favorunit)

    # THEN
    assert sue_hubunit.favor_file_exists(next_int)
    two_file_json = open_file(sue_hubunit._favors_dir, next_filename)


def test_HubUnit_default_favorunit_ReturnsObjWithCorrect_favor_id_WhenNofavorFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)

    # WHEN
    delete_dir(sue_hubunit._favors_dir)
    sue_favorunit = sue_hubunit._default_favorunit()

    # THEN
    assert sue_favorunit.owner_name == sue_str
    assert sue_favorunit._favor_id == init_favor_id()
    assert sue_favorunit._favor_id == 0
    assert sue_favorunit._favor_id == sue_hubunit._get_next_favor_file_number()
    assert sue_favorunit.face_name is None
    assert sue_favorunit._atoms_dir == sue_hubunit._atoms_dir
    assert sue_favorunit._favors_dir == sue_hubunit._favors_dir


def test_HubUnit_default_favorunit_ReturnsObjWithCorrect_favor_id_WhenfavorFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    delete_dir(sue_hubunit._favors_dir)

    zero_favorunit = get_sue_favorunit()
    zero_favorunit._favor_id = sue_hubunit._get_next_favor_file_number()
    zero_favorunit._atoms_dir = sue_hubunit._atoms_dir
    zero_favorunit._favors_dir = sue_hubunit._favors_dir
    sue_hubunit.save_favor_file(zero_favorunit)

    # WHEN
    sue_favorunit = sue_hubunit._default_favorunit()

    # THEN
    assert sue_favorunit.owner_name == sue_str
    assert sue_favorunit._favor_id == init_favor_id() + 1
    assert sue_favorunit._favor_id == 1
    assert sue_favorunit._favor_id == sue_hubunit._get_next_favor_file_number()
    assert sue_favorunit.face_name is None
    assert sue_favorunit._atoms_dir == sue_hubunit._atoms_dir
    assert sue_favorunit._favors_dir == sue_hubunit._favors_dir


def test_HubUnit_get_favorunit_ReturnsObjWhenFilesDoesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    yao_str = "Yao"
    x0_favorunit = sue_hubunit._default_favorunit()
    x0_favorunit.set_face(yao_str)
    sue_hubunit.save_favor_file(x0_favorunit)
    bob_str = "Bob"
    x1_favorunit = sue_hubunit._default_favorunit()
    x1_favorunit.set_face(bob_str)
    sue_hubunit.save_favor_file(x1_favorunit)

    # WHEN
    y0_favorunit = sue_hubunit.get_favorunit(x0_favorunit._favor_id)
    y1_favorunit = sue_hubunit.get_favorunit(x1_favorunit._favor_id)

    # THEN
    assert y0_favorunit is not None
    assert y1_favorunit is not None
    assert yao_str in y0_favorunit.face_name
    assert bob_str not in y0_favorunit.face_name
    assert bob_str in y1_favorunit.face_name


def test_HubUnit_get_favorunit_RaisesExceptionWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    yao_str = "Yao"
    x0_favorunit = sue_hubunit._default_favorunit()
    x0_favorunit.set_face(yao_str)
    sue_hubunit.save_favor_file(x0_favorunit)
    bob_str = "Bob"
    x1_favorunit = sue_hubunit._default_favorunit()
    x1_favorunit.set_face(bob_str)
    sue_hubunit.save_favor_file(x1_favorunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_favorunit(six_file_number)
    assert (
        str(excinfo.value) == f"FavorUnit file_number {six_file_number} does not exist."
    )


def test_HubUnit_del_favor_file_DeletesfavorjsonAndNotBudAtomjsons(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    six_int = 6
    sue_favorunit = favorunit_shop(
        owner_name=sue_str,
        _favor_id=six_int,
        _atoms_dir=sue_hubunit._atoms_dir,
        _favors_dir=sue_hubunit._favors_dir,
    )
    sue_favorunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    zero_int = 0
    assert sue_hubunit.favor_file_exists(six_int) is False
    assert sue_hubunit.atom_file_exists(zero_int) is False

    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_favor_file(sue_favorunit, correct_invalid_attrs=False)

    print(f"{get_dir_file_strs(sue_hubunit._atoms_dir)}")
    assert sue_hubunit.favor_file_exists(six_int)
    assert sue_hubunit.atom_file_exists(zero_int)

    # WHEN
    sue_hubunit._del_favor_file(sue_favorunit._favor_id)

    # THEN
    assert sue_hubunit.favor_file_exists(six_int) is False
    assert sue_hubunit.atom_file_exists(zero_int)


def test_HubUnit_save_favor_file_CanCreateAndModify3favorunits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    delete_dir(sue_hubunit._favors_dir)
    delete_dir(sue_hubunit._atoms_dir)
    set_dir(sue_hubunit._favors_dir)
    set_dir(sue_hubunit._atoms_dir)
    assert len(get_dir_file_strs(sue_hubunit._favors_dir)) == 0
    assert len(get_dir_file_strs(sue_hubunit._atoms_dir)) == 0

    # WHEN
    sue_hubunit.save_favor_file(sue_2budatoms_favorunit())
    sue_hubunit.save_favor_file(sue_3budatoms_favorunit())
    sue_hubunit.save_favor_file(sue_4budatoms_favorunit())

    # THEN
    assert len(get_dir_file_strs(sue_hubunit._favors_dir)) == 3
    assert len(get_dir_file_strs(sue_hubunit._atoms_dir)) == 9


def test_HubUnit_save_favor_file_ReturnsValidObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue2_favorunit = sue_2budatoms_favorunit()
    sue2_favorunit._atoms_dir = create_path(sue_hubunit._keeps_dir, "swimming")
    sue2_favorunit._favors_dir = create_path(sue_hubunit._keeps_dir, "swimming")
    sue2_favorunit.owner_name = "Bob"
    sue2_favorunit._favor_id = sue_hubunit._get_next_favor_file_number() - 5
    prev_sue2_favorunit = copy_deepcopy(sue2_favorunit)

    # WHEN
    valid_favorunit = sue_hubunit.save_favor_file(sue2_favorunit)

    # THEN
    assert valid_favorunit._favors_dir != prev_sue2_favorunit._favors_dir
    assert valid_favorunit._favors_dir == sue_hubunit._favors_dir
    assert valid_favorunit._atoms_dir == sue_hubunit._atoms_dir
    assert valid_favorunit._favor_id != prev_sue2_favorunit._favor_id


def test_HubUnit_create_save_favor_file_SaveCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    two_int = 2
    three_int = 3
    print(f"{sue_hubunit.favor_file_path(two_int)=}")
    print(f"{sue_hubunit.favor_file_path(three_int)=}")
    sue_favorunit = favorunit_shop(
        owner_name=sue_str,
        _favor_id=two_int,
        _atoms_dir=sue_hubunit._atoms_dir,
        _favors_dir=sue_hubunit._favors_dir,
    )
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_favor_file(sue_favorunit, correct_invalid_attrs=False)
    assert sue_hubunit.favor_file_exists(two_int)
    assert sue_hubunit.favor_file_exists(three_int) is False

    # WHEN
    before_bud = sue_hubunit.default_voice_bud()
    bob_str = "Bob"
    after_bud = copy_deepcopy(before_bud)
    after_bud.add_acctunit(bob_str)
    sue_hubunit.create_save_favor_file(before_bud, after_bud)

    # THEN
    assert sue_hubunit.favor_file_exists(three_int)


def test_HubUnit_merge_any_favors_ReturnsObjThatIsEqual(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    voice_bud = sue_hubunit.get_voice_bud()
    voice_bud.last_favor_id is None

    # WHEN
    new_bud = sue_hubunit._merge_any_favors(voice_bud)

    # THEN
    assert new_bud == voice_bud


def test_HubUnit_merge_any_favors_ReturnsObj_WithSinglefavorModifies_1atom(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_favor_file(sue_1budatoms_favorunit())
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    voice_bud = sue_hubunit.get_voice_bud()
    print(f"{voice_bud.fisc_title=}")
    print(f"{sue_hubunit.fisc_title=}")
    sports_str = "sports"
    sports_road = voice_bud.make_l1_road(sports_str)
    knee_str = "knee"
    knee_road = voice_bud.make_road(sports_road, knee_str)
    assert voice_bud.item_exists(sports_road) is False

    # WHEN
    new_bud = sue_hubunit._merge_any_favors(voice_bud)

    # THEN
    assert new_bud != voice_bud
    assert new_bud.item_exists(sports_road)


def test_HubUnit_merge_any_favors_ReturnsObj_WithSinglefavorModifies_2atoms(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_favor_file(sue_2budatoms_favorunit())
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    voice_bud = sue_hubunit.get_voice_bud()
    print(f"{voice_bud.fisc_title=}")
    sports_str = "sports"
    sports_road = voice_bud.make_l1_road(sports_str)
    knee_str = "knee"
    knee_road = voice_bud.make_road(sports_road, knee_str)
    assert voice_bud.item_exists(sports_road) is False
    assert voice_bud.item_exists(knee_road) is False

    # WHEN
    new_bud = sue_hubunit._merge_any_favors(voice_bud)

    # THEN
    assert new_bud != voice_bud
    assert new_bud.item_exists(sports_road)
    assert new_bud.item_exists(knee_road)
