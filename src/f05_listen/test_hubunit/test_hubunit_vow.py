from src.f00_instrument.file import (
    open_file,
    get_dir_file_strs,
    delete_dir,
    set_dir,
    save_file,
    create_path,
)
from src.f01_road.jaar_config import init_vow_id, get_test_fisc_title as fisc_title
from src.f04_vow.vow import vowunit_shop, get_json_filename
from src.f05_listen.hubunit import hubunit_shop
from src.f05_listen.examples.example_listen_atoms import get_atom_example_itemunit_knee
from src.f05_listen.examples.example_listen_vows import (
    get_sue_vowunit,
    sue_1budatoms_vowunit,
    sue_2budatoms_vowunit,
    sue_3budatoms_vowunit,
    sue_4budatoms_vowunit,
)
from src.f05_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_HubUnit_get_max_vow_file_number_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)

    # WHEN / THEN
    delete_dir(sue_hubunit._vows_dir)
    assert sue_hubunit.get_max_vow_file_number() is None
    assert sue_hubunit._get_next_vow_file_number() == init_vow_id()
    assert sue_hubunit._get_next_vow_file_number() == 0

    # ESTABLISH
    six_int = 6
    save_file(sue_hubunit._vows_dir, sue_hubunit.vow_filename(six_int), "x")

    # WHEN / THEN
    assert sue_hubunit.get_max_vow_file_number() == six_int
    assert sue_hubunit._get_next_vow_file_number() == 7


def test_HubUnit_vow_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    assert sue_hubunit.vow_file_exists(None) is False
    assert sue_hubunit.vow_file_exists(0) is False
    six_int = 6
    print(f"{sue_hubunit.vow_file_path(six_int)=}")
    assert sue_hubunit.vow_file_exists(six_int) is False

    # WHEN
    save_file(sue_hubunit._vows_dir, sue_hubunit.vow_filename(six_int), "x")

    # THEN
    assert sue_hubunit.vow_file_exists(None) is False
    assert sue_hubunit.vow_file_exists(0) is False
    assert sue_hubunit.vow_file_exists(six_int)


def test_HubUnit_save_vow_file_SaveCorrectObj(env_dir_setup_cleanup):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_vow2_path = create_path(sue_hubunit._vows_dir, two_filename)
    sue_vow6_path = create_path(sue_hubunit._vows_dir, six_filename)
    print(f"{sue_vow2_path=}")
    print(f"{sue_vow6_path=}")
    sue_vowunit = vowunit_shop(
        owner_name=sue_str,
        _vow_id=two_int,
        _atoms_dir=sue_hubunit._atoms_dir,
        _vows_dir=sue_hubunit._vows_dir,
    )
    assert sue_hubunit.vow_file_exists(two_int) is False
    assert sue_hubunit.vow_file_exists(six_int) is False

    # WHEN
    sue_hubunit.save_vow_file(sue_vowunit, correct_invalid_attrs=False)

    # THEN
    assert sue_hubunit.vow_file_exists(two_int)
    assert sue_hubunit.vow_file_exists(six_int) is False
    two_file_json = open_file(sue_hubunit._vows_dir, two_filename)
    assert two_file_json == sue_vowunit.get_deltametric_json()


def test_HubUnit_save_vow_file_RaisesErrorIfvowUnit_atoms_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    x_vow_id = 6
    six_filename = get_json_filename(x_vow_id)
    sue_vow0_path = create_path(sue_hubunit._vows_dir, six_filename)
    print(f"{sue_vow0_path=}")
    sue_vowunit = vowunit_shop(
        owner_name=sue_str,
        _vow_id=x_vow_id,
        _atoms_dir="src/incorrect_directory",
        _vows_dir=sue_hubunit._vows_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_vow_file(sue_vowunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"vowUnit file cannot be saved because vowunit._atoms_dir is incorrect: {sue_vowunit._atoms_dir}. It must be {sue_hubunit._atoms_dir}."
    )


def test_HubUnit_save_vow_file_RaisesErrorIfvowUnit_vows_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    x_vow_id = 6
    six_filename = get_json_filename(x_vow_id)
    sue_vow0_path = create_path(sue_hubunit._vows_dir, six_filename)
    print(f"{sue_vow0_path=}")
    sue_vowunit = vowunit_shop(
        owner_name=sue_str,
        _vow_id=x_vow_id,
        _atoms_dir=sue_hubunit._atoms_dir,
        _vows_dir="src/incorrect_directory",
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_vow_file(sue_vowunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"vowUnit file cannot be saved because vowunit._vows_dir is incorrect: {sue_vowunit._vows_dir}. It must be {sue_hubunit._vows_dir}."
    )


def test_HubUnit_save_vow_file_RaisesErrorIfvowUnit_owner_name_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    x_vow_id = 6
    six_filename = get_json_filename(x_vow_id)
    sue_vow0_path = create_path(sue_hubunit._vows_dir, six_filename)
    print(f"{sue_vow0_path=}")
    bob_str = "Bob"
    sue_vowunit = vowunit_shop(
        owner_name=bob_str,
        _vow_id=x_vow_id,
        _atoms_dir=sue_hubunit._atoms_dir,
        _vows_dir=sue_hubunit._vows_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_vow_file(sue_vowunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"vowUnit file cannot be saved because vowunit.owner_name is incorrect: {sue_vowunit.owner_name}. It must be {sue_str}."
    )


def test_HubUnit_save_vow_file_RaisesErrorIf_replace_IsFalse(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    x_vow_id = 0
    six_filename = get_json_filename(x_vow_id)
    sue_vowunit = vowunit_shop(
        owner_name=sue_str,
        _vow_id=x_vow_id,
        _atoms_dir=sue_hubunit._atoms_dir,
        _vows_dir=sue_hubunit._vows_dir,
    )
    saved_vowunit = sue_hubunit.save_vow_file(sue_vowunit)

    print(f"{sue_hubunit.vow_file_path(x_vow_id)=}")
    assert sue_hubunit.vow_file_exists(x_vow_id)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_vow_file(
            saved_vowunit, replace=False, correct_invalid_attrs=False
        )
    assert (
        str(excinfo.value)
        == f"vowUnit file {six_filename} exists and cannot be saved over."
    )


def test_HubUnit_validate_vowunit_ReturnsObjWithAttributesFixed(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_vow2_path = create_path(sue_hubunit._vows_dir, two_filename)
    print(f"{sue_vow2_path=}")

    # WHEN
    invalid_sue_vowunit = vowunit_shop(
        owner_name="Bob",
        _vow_id=sue_hubunit._get_next_vow_file_number() - 5,
        _atoms_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
        _vows_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
    )
    valid_vowunit = sue_hubunit.validate_vowunit(invalid_sue_vowunit)

    # THEN
    assert valid_vowunit._atoms_dir == sue_hubunit._atoms_dir
    assert valid_vowunit._vows_dir == sue_hubunit._vows_dir
    assert valid_vowunit._vow_id == sue_hubunit._get_next_vow_file_number()
    correct_sue_vowunit = vowunit_shop(
        owner_name=sue_str,
        _vow_id=sue_hubunit._get_next_vow_file_number(),
        _atoms_dir=sue_hubunit._atoms_dir,
        _vows_dir=sue_hubunit._vows_dir,
    )
    assert valid_vowunit == correct_sue_vowunit


def test_HubUnit_save_vow_file_SaveCorrectObj_correct_invalid_attrs_IsTrue(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    next_int = sue_hubunit._get_next_vow_file_number()
    next_filename = get_json_filename(next_int)
    sue_vow2_path = create_path(sue_hubunit._vows_dir, next_filename)
    print(f"{sue_vow2_path=}")
    assert sue_hubunit.vow_file_exists(next_int) is False

    # WHEN
    invalid_sue_vowunit = vowunit_shop(
        owner_name="Bob",
        _vow_id=sue_hubunit._get_next_vow_file_number() - 5,
        _atoms_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
        _vows_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
    )
    sue_hubunit.save_vow_file(invalid_sue_vowunit)

    # THEN
    assert sue_hubunit.vow_file_exists(next_int)
    two_file_json = open_file(sue_hubunit._vows_dir, next_filename)


def test_HubUnit_default_vowunit_ReturnsObjWithCorrect_vow_id_WhenNovowFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)

    # WHEN
    delete_dir(sue_hubunit._vows_dir)
    sue_vowunit = sue_hubunit._default_vowunit()

    # THEN
    assert sue_vowunit.owner_name == sue_str
    assert sue_vowunit._vow_id == init_vow_id()
    assert sue_vowunit._vow_id == 0
    assert sue_vowunit._vow_id == sue_hubunit._get_next_vow_file_number()
    assert sue_vowunit.face_name is None
    assert sue_vowunit._atoms_dir == sue_hubunit._atoms_dir
    assert sue_vowunit._vows_dir == sue_hubunit._vows_dir


def test_HubUnit_default_vowunit_ReturnsObjWithCorrect_vow_id_WhenvowFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    delete_dir(sue_hubunit._vows_dir)

    zero_vowunit = get_sue_vowunit()
    zero_vowunit._vow_id = sue_hubunit._get_next_vow_file_number()
    zero_vowunit._atoms_dir = sue_hubunit._atoms_dir
    zero_vowunit._vows_dir = sue_hubunit._vows_dir
    sue_hubunit.save_vow_file(zero_vowunit)

    # WHEN
    sue_vowunit = sue_hubunit._default_vowunit()

    # THEN
    assert sue_vowunit.owner_name == sue_str
    assert sue_vowunit._vow_id == init_vow_id() + 1
    assert sue_vowunit._vow_id == 1
    assert sue_vowunit._vow_id == sue_hubunit._get_next_vow_file_number()
    assert sue_vowunit.face_name is None
    assert sue_vowunit._atoms_dir == sue_hubunit._atoms_dir
    assert sue_vowunit._vows_dir == sue_hubunit._vows_dir


def test_HubUnit_get_vowunit_ReturnsObjWhenFilesDoesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    yao_str = "Yao"
    x0_vowunit = sue_hubunit._default_vowunit()
    x0_vowunit.set_face(yao_str)
    sue_hubunit.save_vow_file(x0_vowunit)
    bob_str = "Bob"
    x1_vowunit = sue_hubunit._default_vowunit()
    x1_vowunit.set_face(bob_str)
    sue_hubunit.save_vow_file(x1_vowunit)

    # WHEN
    y0_vowunit = sue_hubunit.get_vowunit(x0_vowunit._vow_id)
    y1_vowunit = sue_hubunit.get_vowunit(x1_vowunit._vow_id)

    # THEN
    assert y0_vowunit is not None
    assert y1_vowunit is not None
    assert yao_str in y0_vowunit.face_name
    assert bob_str not in y0_vowunit.face_name
    assert bob_str in y1_vowunit.face_name


def test_HubUnit_get_vowunit_RaisesExceptionWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    yao_str = "Yao"
    x0_vowunit = sue_hubunit._default_vowunit()
    x0_vowunit.set_face(yao_str)
    sue_hubunit.save_vow_file(x0_vowunit)
    bob_str = "Bob"
    x1_vowunit = sue_hubunit._default_vowunit()
    x1_vowunit.set_face(bob_str)
    sue_hubunit.save_vow_file(x1_vowunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_vowunit(six_file_number)
    assert (
        str(excinfo.value) == f"vowUnit file_number {six_file_number} does not exist."
    )


def test_HubUnit_del_vow_file_DeletesvowjsonAndNotBudAtomjsons(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    six_int = 6
    sue_vowunit = vowunit_shop(
        owner_name=sue_str,
        _vow_id=six_int,
        _atoms_dir=sue_hubunit._atoms_dir,
        _vows_dir=sue_hubunit._vows_dir,
    )
    sue_vowunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    zero_int = 0
    assert sue_hubunit.vow_file_exists(six_int) is False
    assert sue_hubunit.atom_file_exists(zero_int) is False

    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_vow_file(sue_vowunit, correct_invalid_attrs=False)

    print(f"{get_dir_file_strs(sue_hubunit._atoms_dir)}")
    assert sue_hubunit.vow_file_exists(six_int)
    assert sue_hubunit.atom_file_exists(zero_int)

    # WHEN
    sue_hubunit._del_vow_file(sue_vowunit._vow_id)

    # THEN
    assert sue_hubunit.vow_file_exists(six_int) is False
    assert sue_hubunit.atom_file_exists(zero_int)


def test_HubUnit_save_vow_file_CanCreateAndModify3vowunits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    delete_dir(sue_hubunit._vows_dir)
    delete_dir(sue_hubunit._atoms_dir)
    set_dir(sue_hubunit._vows_dir)
    set_dir(sue_hubunit._atoms_dir)
    assert len(get_dir_file_strs(sue_hubunit._vows_dir)) == 0
    assert len(get_dir_file_strs(sue_hubunit._atoms_dir)) == 0

    # WHEN
    sue_hubunit.save_vow_file(sue_2budatoms_vowunit())
    sue_hubunit.save_vow_file(sue_3budatoms_vowunit())
    sue_hubunit.save_vow_file(sue_4budatoms_vowunit())

    # THEN
    assert len(get_dir_file_strs(sue_hubunit._vows_dir)) == 3
    assert len(get_dir_file_strs(sue_hubunit._atoms_dir)) == 9


def test_HubUnit_save_vow_file_ReturnsValidObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue2_vowunit = sue_2budatoms_vowunit()
    sue2_vowunit._atoms_dir = create_path(sue_hubunit._keeps_dir, "swimming")
    sue2_vowunit._vows_dir = create_path(sue_hubunit._keeps_dir, "swimming")
    sue2_vowunit.owner_name = "Bob"
    sue2_vowunit._vow_id = sue_hubunit._get_next_vow_file_number() - 5
    prev_sue2_vowunit = copy_deepcopy(sue2_vowunit)

    # WHEN
    valid_vowunit = sue_hubunit.save_vow_file(sue2_vowunit)

    # THEN
    assert valid_vowunit._vows_dir != prev_sue2_vowunit._vows_dir
    assert valid_vowunit._vows_dir == sue_hubunit._vows_dir
    assert valid_vowunit._atoms_dir == sue_hubunit._atoms_dir
    assert valid_vowunit._vow_id != prev_sue2_vowunit._vow_id


def test_HubUnit_create_save_vow_file_SaveCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    two_int = 2
    three_int = 3
    print(f"{sue_hubunit.vow_file_path(two_int)=}")
    print(f"{sue_hubunit.vow_file_path(three_int)=}")
    sue_vowunit = vowunit_shop(
        owner_name=sue_str,
        _vow_id=two_int,
        _atoms_dir=sue_hubunit._atoms_dir,
        _vows_dir=sue_hubunit._vows_dir,
    )
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_vow_file(sue_vowunit, correct_invalid_attrs=False)
    assert sue_hubunit.vow_file_exists(two_int)
    assert sue_hubunit.vow_file_exists(three_int) is False

    # WHEN
    before_bud = sue_hubunit.default_voice_bud()
    bob_str = "Bob"
    after_bud = copy_deepcopy(before_bud)
    after_bud.add_acctunit(bob_str)
    sue_hubunit.create_save_vow_file(before_bud, after_bud)

    # THEN
    assert sue_hubunit.vow_file_exists(three_int)


def test_HubUnit_merge_any_vows_ReturnsObjThatIsEqual(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    voice_bud = sue_hubunit.get_voice_bud()
    voice_bud.last_vow_id is None

    # WHEN
    new_bud = sue_hubunit._merge_any_vows(voice_bud)

    # THEN
    assert new_bud == voice_bud


def test_HubUnit_merge_any_vows_ReturnsObj_WithSinglevowModifies_1atom(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_vow_file(sue_1budatoms_vowunit())
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
    new_bud = sue_hubunit._merge_any_vows(voice_bud)

    # THEN
    assert new_bud != voice_bud
    assert new_bud.item_exists(sports_road)


def test_HubUnit_merge_any_vows_ReturnsObj_WithSinglevowModifies_2atoms(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_vow_file(sue_2budatoms_vowunit())
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
    new_bud = sue_hubunit._merge_any_vows(voice_bud)

    # THEN
    assert new_bud != voice_bud
    assert new_bud.item_exists(sports_road)
    assert new_bud.item_exists(knee_road)
