from src.f00_instrument.file import (
    open_file,
    get_dir_file_strs,
    delete_dir,
    set_dir,
    save_file,
    create_path,
)
from src.f01_road.jaar_config import init_stand_id, get_test_fisc_title as fisc_title
from src.f04_stand.stand import standunit_shop, get_json_filename
from src.f05_listen.hubunit import hubunit_shop
from src.f05_listen.examples.example_listen_atoms import get_atom_example_itemunit_knee
from src.f05_listen.examples.example_listen_stands import (
    get_sue_standunit,
    sue_1budatoms_standunit,
    sue_2budatoms_standunit,
    sue_3budatoms_standunit,
    sue_4budatoms_standunit,
)
from src.f05_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_HubUnit_get_max_stand_file_number_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)

    # WHEN / THEN
    delete_dir(sue_hubunit._stands_dir)
    assert sue_hubunit.get_max_stand_file_number() is None
    assert sue_hubunit._get_next_stand_file_number() == init_stand_id()
    assert sue_hubunit._get_next_stand_file_number() == 0

    # ESTABLISH
    six_int = 6
    save_file(sue_hubunit._stands_dir, sue_hubunit.stand_filename(six_int), "x")

    # WHEN / THEN
    assert sue_hubunit.get_max_stand_file_number() == six_int
    assert sue_hubunit._get_next_stand_file_number() == 7


def test_HubUnit_stand_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    assert sue_hubunit.stand_file_exists(None) is False
    assert sue_hubunit.stand_file_exists(0) is False
    six_int = 6
    print(f"{sue_hubunit.stand_file_path(six_int)=}")
    assert sue_hubunit.stand_file_exists(six_int) is False

    # WHEN
    save_file(sue_hubunit._stands_dir, sue_hubunit.stand_filename(six_int), "x")

    # THEN
    assert sue_hubunit.stand_file_exists(None) is False
    assert sue_hubunit.stand_file_exists(0) is False
    assert sue_hubunit.stand_file_exists(six_int)


def test_HubUnit_save_stand_file_SaveCorrectObj(env_dir_setup_cleanup):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_stand2_path = create_path(sue_hubunit._stands_dir, two_filename)
    sue_stand6_path = create_path(sue_hubunit._stands_dir, six_filename)
    print(f"{sue_stand2_path=}")
    print(f"{sue_stand6_path=}")
    sue_standunit = standunit_shop(
        owner_name=sue_str,
        _stand_id=two_int,
        _atoms_dir=sue_hubunit._atoms_dir,
        _stands_dir=sue_hubunit._stands_dir,
    )
    assert sue_hubunit.stand_file_exists(two_int) is False
    assert sue_hubunit.stand_file_exists(six_int) is False

    # WHEN
    sue_hubunit.save_stand_file(sue_standunit, correct_invalid_attrs=False)

    # THEN
    assert sue_hubunit.stand_file_exists(two_int)
    assert sue_hubunit.stand_file_exists(six_int) is False
    two_file_json = open_file(sue_hubunit._stands_dir, two_filename)
    assert two_file_json == sue_standunit.get_deltametric_json()


def test_HubUnit_save_stand_file_RaisesErrorIfStandUnit_atoms_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    x_stand_id = 6
    six_filename = get_json_filename(x_stand_id)
    sue_stand0_path = create_path(sue_hubunit._stands_dir, six_filename)
    print(f"{sue_stand0_path=}")
    sue_standunit = standunit_shop(
        owner_name=sue_str,
        _stand_id=x_stand_id,
        _atoms_dir="src/incorrect_directory",
        _stands_dir=sue_hubunit._stands_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_stand_file(sue_standunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"StandUnit file cannot be saved because standunit._atoms_dir is incorrect: {sue_standunit._atoms_dir}. It must be {sue_hubunit._atoms_dir}."
    )


def test_HubUnit_save_stand_file_RaisesErrorIfStandUnit_stands_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    x_stand_id = 6
    six_filename = get_json_filename(x_stand_id)
    sue_stand0_path = create_path(sue_hubunit._stands_dir, six_filename)
    print(f"{sue_stand0_path=}")
    sue_standunit = standunit_shop(
        owner_name=sue_str,
        _stand_id=x_stand_id,
        _atoms_dir=sue_hubunit._atoms_dir,
        _stands_dir="src/incorrect_directory",
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_stand_file(sue_standunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"StandUnit file cannot be saved because standunit._stands_dir is incorrect: {sue_standunit._stands_dir}. It must be {sue_hubunit._stands_dir}."
    )


def test_HubUnit_save_stand_file_RaisesErrorIfStandUnit_owner_name_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    x_stand_id = 6
    six_filename = get_json_filename(x_stand_id)
    sue_stand0_path = create_path(sue_hubunit._stands_dir, six_filename)
    print(f"{sue_stand0_path=}")
    bob_str = "Bob"
    sue_standunit = standunit_shop(
        owner_name=bob_str,
        _stand_id=x_stand_id,
        _atoms_dir=sue_hubunit._atoms_dir,
        _stands_dir=sue_hubunit._stands_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_stand_file(sue_standunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"StandUnit file cannot be saved because standunit.owner_name is incorrect: {sue_standunit.owner_name}. It must be {sue_str}."
    )


def test_HubUnit_save_stand_file_RaisesErrorIf_replace_IsFalse(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    x_stand_id = 0
    six_filename = get_json_filename(x_stand_id)
    sue_standunit = standunit_shop(
        owner_name=sue_str,
        _stand_id=x_stand_id,
        _atoms_dir=sue_hubunit._atoms_dir,
        _stands_dir=sue_hubunit._stands_dir,
    )
    saved_standunit = sue_hubunit.save_stand_file(sue_standunit)

    print(f"{sue_hubunit.stand_file_path(x_stand_id)=}")
    assert sue_hubunit.stand_file_exists(x_stand_id)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_stand_file(
            saved_standunit, replace=False, correct_invalid_attrs=False
        )
    assert (
        str(excinfo.value)
        == f"StandUnit file {six_filename} exists and cannot be saved over."
    )


def test_HubUnit_validate_standunit_ReturnsObjWithAttributesFixed(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_stand2_path = create_path(sue_hubunit._stands_dir, two_filename)
    print(f"{sue_stand2_path=}")

    # WHEN
    invalid_sue_standunit = standunit_shop(
        owner_name="Bob",
        _stand_id=sue_hubunit._get_next_stand_file_number() - 5,
        _atoms_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
        _stands_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
    )
    valid_standunit = sue_hubunit.validate_standunit(invalid_sue_standunit)

    # THEN
    assert valid_standunit._atoms_dir == sue_hubunit._atoms_dir
    assert valid_standunit._stands_dir == sue_hubunit._stands_dir
    assert valid_standunit._stand_id == sue_hubunit._get_next_stand_file_number()
    correct_sue_standunit = standunit_shop(
        owner_name=sue_str,
        _stand_id=sue_hubunit._get_next_stand_file_number(),
        _atoms_dir=sue_hubunit._atoms_dir,
        _stands_dir=sue_hubunit._stands_dir,
    )
    assert valid_standunit == correct_sue_standunit


def test_HubUnit_save_stand_file_SaveCorrectObj_correct_invalid_attrs_IsTrue(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    next_int = sue_hubunit._get_next_stand_file_number()
    next_filename = get_json_filename(next_int)
    sue_stand2_path = create_path(sue_hubunit._stands_dir, next_filename)
    print(f"{sue_stand2_path=}")
    assert sue_hubunit.stand_file_exists(next_int) is False

    # WHEN
    invalid_sue_standunit = standunit_shop(
        owner_name="Bob",
        _stand_id=sue_hubunit._get_next_stand_file_number() - 5,
        _atoms_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
        _stands_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
    )
    sue_hubunit.save_stand_file(invalid_sue_standunit)

    # THEN
    assert sue_hubunit.stand_file_exists(next_int)
    two_file_json = open_file(sue_hubunit._stands_dir, next_filename)


def test_HubUnit_default_standunit_ReturnsObjWithCorrect_stand_id_WhenNostandFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)

    # WHEN
    delete_dir(sue_hubunit._stands_dir)
    sue_standunit = sue_hubunit._default_standunit()

    # THEN
    assert sue_standunit.owner_name == sue_str
    assert sue_standunit._stand_id == init_stand_id()
    assert sue_standunit._stand_id == 0
    assert sue_standunit._stand_id == sue_hubunit._get_next_stand_file_number()
    assert sue_standunit.face_name is None
    assert sue_standunit._atoms_dir == sue_hubunit._atoms_dir
    assert sue_standunit._stands_dir == sue_hubunit._stands_dir


def test_HubUnit_default_standunit_ReturnsObjWithCorrect_stand_id_WhenstandFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    delete_dir(sue_hubunit._stands_dir)

    zero_standunit = get_sue_standunit()
    zero_standunit._stand_id = sue_hubunit._get_next_stand_file_number()
    zero_standunit._atoms_dir = sue_hubunit._atoms_dir
    zero_standunit._stands_dir = sue_hubunit._stands_dir
    sue_hubunit.save_stand_file(zero_standunit)

    # WHEN
    sue_standunit = sue_hubunit._default_standunit()

    # THEN
    assert sue_standunit.owner_name == sue_str
    assert sue_standunit._stand_id == init_stand_id() + 1
    assert sue_standunit._stand_id == 1
    assert sue_standunit._stand_id == sue_hubunit._get_next_stand_file_number()
    assert sue_standunit.face_name is None
    assert sue_standunit._atoms_dir == sue_hubunit._atoms_dir
    assert sue_standunit._stands_dir == sue_hubunit._stands_dir


def test_HubUnit_get_standunit_ReturnsObjWhenFilesDoesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    yao_str = "Yao"
    x0_standunit = sue_hubunit._default_standunit()
    x0_standunit.set_face(yao_str)
    sue_hubunit.save_stand_file(x0_standunit)
    bob_str = "Bob"
    x1_standunit = sue_hubunit._default_standunit()
    x1_standunit.set_face(bob_str)
    sue_hubunit.save_stand_file(x1_standunit)

    # WHEN
    y0_standunit = sue_hubunit.get_standunit(x0_standunit._stand_id)
    y1_standunit = sue_hubunit.get_standunit(x1_standunit._stand_id)

    # THEN
    assert y0_standunit is not None
    assert y1_standunit is not None
    assert yao_str in y0_standunit.face_name
    assert bob_str not in y0_standunit.face_name
    assert bob_str in y1_standunit.face_name


def test_HubUnit_get_standunit_RaisesExceptionWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    yao_str = "Yao"
    x0_standunit = sue_hubunit._default_standunit()
    x0_standunit.set_face(yao_str)
    sue_hubunit.save_stand_file(x0_standunit)
    bob_str = "Bob"
    x1_standunit = sue_hubunit._default_standunit()
    x1_standunit.set_face(bob_str)
    sue_hubunit.save_stand_file(x1_standunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_standunit(six_file_number)
    assert (
        str(excinfo.value) == f"StandUnit file_number {six_file_number} does not exist."
    )


def test_HubUnit_del_stand_file_DeletesstandjsonAndNotBudAtomjsons(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    six_int = 6
    sue_standunit = standunit_shop(
        owner_name=sue_str,
        _stand_id=six_int,
        _atoms_dir=sue_hubunit._atoms_dir,
        _stands_dir=sue_hubunit._stands_dir,
    )
    sue_standunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    zero_int = 0
    assert sue_hubunit.stand_file_exists(six_int) is False
    assert sue_hubunit.atom_file_exists(zero_int) is False

    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_stand_file(sue_standunit, correct_invalid_attrs=False)

    print(f"{get_dir_file_strs(sue_hubunit._atoms_dir)}")
    assert sue_hubunit.stand_file_exists(six_int)
    assert sue_hubunit.atom_file_exists(zero_int)

    # WHEN
    sue_hubunit._del_stand_file(sue_standunit._stand_id)

    # THEN
    assert sue_hubunit.stand_file_exists(six_int) is False
    assert sue_hubunit.atom_file_exists(zero_int)


def test_HubUnit_save_stand_file_CanCreateAndModify3standunits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    delete_dir(sue_hubunit._stands_dir)
    delete_dir(sue_hubunit._atoms_dir)
    set_dir(sue_hubunit._stands_dir)
    set_dir(sue_hubunit._atoms_dir)
    assert len(get_dir_file_strs(sue_hubunit._stands_dir)) == 0
    assert len(get_dir_file_strs(sue_hubunit._atoms_dir)) == 0

    # WHEN
    sue_hubunit.save_stand_file(sue_2budatoms_standunit())
    sue_hubunit.save_stand_file(sue_3budatoms_standunit())
    sue_hubunit.save_stand_file(sue_4budatoms_standunit())

    # THEN
    assert len(get_dir_file_strs(sue_hubunit._stands_dir)) == 3
    assert len(get_dir_file_strs(sue_hubunit._atoms_dir)) == 9


def test_HubUnit_save_stand_file_ReturnsValidObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue2_standunit = sue_2budatoms_standunit()
    sue2_standunit._atoms_dir = create_path(sue_hubunit._keeps_dir, "swimming")
    sue2_standunit._stands_dir = create_path(sue_hubunit._keeps_dir, "swimming")
    sue2_standunit.owner_name = "Bob"
    sue2_standunit._stand_id = sue_hubunit._get_next_stand_file_number() - 5
    prev_sue2_standunit = copy_deepcopy(sue2_standunit)

    # WHEN
    valid_standunit = sue_hubunit.save_stand_file(sue2_standunit)

    # THEN
    assert valid_standunit._stands_dir != prev_sue2_standunit._stands_dir
    assert valid_standunit._stands_dir == sue_hubunit._stands_dir
    assert valid_standunit._atoms_dir == sue_hubunit._atoms_dir
    assert valid_standunit._stand_id != prev_sue2_standunit._stand_id


def test_HubUnit_create_save_stand_file_SaveCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    two_int = 2
    three_int = 3
    print(f"{sue_hubunit.stand_file_path(two_int)=}")
    print(f"{sue_hubunit.stand_file_path(three_int)=}")
    sue_standunit = standunit_shop(
        owner_name=sue_str,
        _stand_id=two_int,
        _atoms_dir=sue_hubunit._atoms_dir,
        _stands_dir=sue_hubunit._stands_dir,
    )
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_stand_file(sue_standunit, correct_invalid_attrs=False)
    assert sue_hubunit.stand_file_exists(two_int)
    assert sue_hubunit.stand_file_exists(three_int) is False

    # WHEN
    before_bud = sue_hubunit.default_voice_bud()
    bob_str = "Bob"
    after_bud = copy_deepcopy(before_bud)
    after_bud.add_acctunit(bob_str)
    sue_hubunit.create_save_stand_file(before_bud, after_bud)

    # THEN
    assert sue_hubunit.stand_file_exists(three_int)


def test_HubUnit_merge_any_stands_ReturnsObjThatIsEqual(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_voice_bud(sue_hubunit.default_voice_bud())
    voice_bud = sue_hubunit.get_voice_bud()
    voice_bud.last_stand_id is None

    # WHEN
    new_bud = sue_hubunit._merge_any_stands(voice_bud)

    # THEN
    assert new_bud == voice_bud


def test_HubUnit_merge_any_stands_ReturnsObj_WithSinglestandModifies_1atom(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_stand_file(sue_1budatoms_standunit())
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
    new_bud = sue_hubunit._merge_any_stands(voice_bud)

    # THEN
    assert new_bud != voice_bud
    assert new_bud.item_exists(sports_road)


def test_HubUnit_merge_any_stands_ReturnsObj_WithSinglestandModifies_2atoms(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), fisc_title(), sue_str)
    sue_hubunit.save_stand_file(sue_2budatoms_standunit())
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
    new_bud = sue_hubunit._merge_any_stands(voice_bud)

    # THEN
    assert new_bud != voice_bud
    assert new_bud.item_exists(sports_road)
    assert new_bud.item_exists(knee_road)
