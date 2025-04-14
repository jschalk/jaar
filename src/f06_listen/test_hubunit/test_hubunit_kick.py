from src.f00_instrument.file_toolbox import (
    open_file,
    get_dir_file_strs,
    delete_dir,
    set_dir,
    save_file,
    create_path,
    get_json_filename,
)
from src.f04_kick.kick import init_kick_id, kickunit_shop
from src.f06_listen.hub_tool import save_gut_file, open_gut_file
from src.f06_listen.hubunit import hubunit_shop
from src.f06_listen.examples.example_listen_atoms import get_atom_example_itemunit_knee
from src.f06_listen.examples.example_listen_kicks import (
    get_sue_kickunit,
    sue_1budatoms_kickunit,
    sue_2budatoms_kickunit,
    sue_3budatoms_kickunit,
    sue_4budatoms_kickunit,
)
from src.f06_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_HubUnit_get_max_kick_file_number_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)

    # WHEN / THEN
    delete_dir(sue_hubunit._kicks_dir)
    assert sue_hubunit.get_max_kick_file_number() is None
    assert sue_hubunit._get_next_kick_file_number() == init_kick_id()
    assert sue_hubunit._get_next_kick_file_number() == 0

    # ESTABLISH
    six_int = 6
    save_file(sue_hubunit._kicks_dir, sue_hubunit.kick_filename(six_int), "x")

    # WHEN / THEN
    assert sue_hubunit.get_max_kick_file_number() == six_int
    assert sue_hubunit._get_next_kick_file_number() == 7


def test_HubUnit_kick_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    assert sue_hubunit.kick_file_exists(None) is False
    assert sue_hubunit.kick_file_exists(0) is False
    six_int = 6
    print(f"{sue_hubunit.kick_file_path(six_int)=}")
    assert sue_hubunit.kick_file_exists(six_int) is False

    # WHEN
    save_file(sue_hubunit._kicks_dir, sue_hubunit.kick_filename(six_int), "x")

    # THEN
    assert sue_hubunit.kick_file_exists(None) is False
    assert sue_hubunit.kick_file_exists(0) is False
    assert sue_hubunit.kick_file_exists(six_int)


def test_HubUnit_save_kick_file_SaveCorrectObj(env_dir_setup_cleanup):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_kick2_path = create_path(sue_hubunit._kicks_dir, two_filename)
    sue_kick6_path = create_path(sue_hubunit._kicks_dir, six_filename)
    print(f"{sue_kick2_path=}")
    print(f"{sue_kick6_path=}")
    sue_kickunit = kickunit_shop(
        owner_name=sue_str,
        _kick_id=two_int,
        _atoms_dir=sue_hubunit._atoms_dir,
        _kicks_dir=sue_hubunit._kicks_dir,
    )
    assert sue_hubunit.kick_file_exists(two_int) is False
    assert sue_hubunit.kick_file_exists(six_int) is False

    # WHEN
    sue_hubunit.save_kick_file(sue_kickunit, correct_invalid_attrs=False)

    # THEN
    assert sue_hubunit.kick_file_exists(two_int)
    assert sue_hubunit.kick_file_exists(six_int) is False
    two_file_json = open_file(sue_hubunit._kicks_dir, two_filename)
    assert two_file_json == sue_kickunit.get_deltametric_json()


def test_HubUnit_save_kick_file_RaisesErrorIfKickUnit_atoms_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    x_kick_id = 6
    six_filename = get_json_filename(x_kick_id)
    sue_kick0_path = create_path(sue_hubunit._kicks_dir, six_filename)
    print(f"{sue_kick0_path=}")
    sue_kickunit = kickunit_shop(
        owner_name=sue_str,
        _kick_id=x_kick_id,
        _atoms_dir="src/incorrect_directory",
        _kicks_dir=sue_hubunit._kicks_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_kick_file(sue_kickunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"KickUnit file cannot be saved because kickunit._atoms_dir is incorrect: {sue_kickunit._atoms_dir}. It must be {sue_hubunit._atoms_dir}."
    )


def test_HubUnit_save_kick_file_RaisesErrorIfKickUnit_kicks_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    x_kick_id = 6
    six_filename = get_json_filename(x_kick_id)
    sue_kick0_path = create_path(sue_hubunit._kicks_dir, six_filename)
    print(f"{sue_kick0_path=}")
    sue_kickunit = kickunit_shop(
        owner_name=sue_str,
        _kick_id=x_kick_id,
        _atoms_dir=sue_hubunit._atoms_dir,
        _kicks_dir="src/incorrect_directory",
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_kick_file(sue_kickunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"KickUnit file cannot be saved because kickunit._kicks_dir is incorrect: {sue_kickunit._kicks_dir}. It must be {sue_hubunit._kicks_dir}."
    )


def test_HubUnit_save_kick_file_RaisesErrorIfKickUnit_owner_name_IsWrong(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    x_kick_id = 6
    six_filename = get_json_filename(x_kick_id)
    sue_kick0_path = create_path(sue_hubunit._kicks_dir, six_filename)
    print(f"{sue_kick0_path=}")
    bob_str = "Bob"
    sue_kickunit = kickunit_shop(
        owner_name=bob_str,
        _kick_id=x_kick_id,
        _atoms_dir=sue_hubunit._atoms_dir,
        _kicks_dir=sue_hubunit._kicks_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_kick_file(sue_kickunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"KickUnit file cannot be saved because kickunit.owner_name is incorrect: {sue_kickunit.owner_name}. It must be {sue_str}."
    )


def test_HubUnit_save_kick_file_RaisesErrorIf_replace_IsFalse(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    x_kick_id = 0
    six_filename = get_json_filename(x_kick_id)
    sue_kickunit = kickunit_shop(
        owner_name=sue_str,
        _kick_id=x_kick_id,
        _atoms_dir=sue_hubunit._atoms_dir,
        _kicks_dir=sue_hubunit._kicks_dir,
    )
    saved_kickunit = sue_hubunit.save_kick_file(sue_kickunit)

    print(f"{sue_hubunit.kick_file_path(x_kick_id)=}")
    assert sue_hubunit.kick_file_exists(x_kick_id)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_kick_file(
            saved_kickunit, replace=False, correct_invalid_attrs=False
        )
    assert (
        str(excinfo.value)
        == f"KickUnit file {six_filename} exists and cannot be saved over."
    )


def test_HubUnit_validate_kickunit_ReturnsObjWithAttributesFixed(
    env_dir_setup_cleanup,
):
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_kick2_path = create_path(sue_hubunit._kicks_dir, two_filename)
    print(f"{sue_kick2_path=}")

    # WHEN
    invalid_sue_kickunit = kickunit_shop(
        owner_name="Bob",
        _kick_id=sue_hubunit._get_next_kick_file_number() - 5,
        _atoms_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
        _kicks_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
    )
    valid_kickunit = sue_hubunit.validate_kickunit(invalid_sue_kickunit)

    # THEN
    assert valid_kickunit._atoms_dir == sue_hubunit._atoms_dir
    assert valid_kickunit._kicks_dir == sue_hubunit._kicks_dir
    assert valid_kickunit._kick_id == sue_hubunit._get_next_kick_file_number()
    correct_sue_kickunit = kickunit_shop(
        owner_name=sue_str,
        _kick_id=sue_hubunit._get_next_kick_file_number(),
        _atoms_dir=sue_hubunit._atoms_dir,
        _kicks_dir=sue_hubunit._kicks_dir,
    )
    assert valid_kickunit == correct_sue_kickunit


def test_HubUnit_save_kick_file_SaveCorrectObj_correct_invalid_attrs_IsTrue(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    next_int = sue_hubunit._get_next_kick_file_number()
    next_filename = get_json_filename(next_int)
    sue_kick2_path = create_path(sue_hubunit._kicks_dir, next_filename)
    print(f"{sue_kick2_path=}")
    assert sue_hubunit.kick_file_exists(next_int) is False

    # WHEN
    invalid_sue_kickunit = kickunit_shop(
        owner_name="Bob",
        _kick_id=sue_hubunit._get_next_kick_file_number() - 5,
        _atoms_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
        _kicks_dir=create_path(sue_hubunit._keeps_dir, "swimming"),
    )
    sue_hubunit.save_kick_file(invalid_sue_kickunit)

    # THEN
    assert sue_hubunit.kick_file_exists(next_int)
    two_file_json = open_file(sue_hubunit._kicks_dir, next_filename)


def test_HubUnit_default_kickunit_ReturnsObjWithCorrect_kick_id_WhenNokickFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)

    # WHEN
    delete_dir(sue_hubunit._kicks_dir)
    sue_kickunit = sue_hubunit._default_kickunit()

    # THEN
    assert sue_kickunit.owner_name == sue_str
    assert sue_kickunit._kick_id == init_kick_id()
    assert sue_kickunit._kick_id == 0
    assert sue_kickunit._kick_id == sue_hubunit._get_next_kick_file_number()
    assert sue_kickunit.face_name is None
    assert sue_kickunit._atoms_dir == sue_hubunit._atoms_dir
    assert sue_kickunit._kicks_dir == sue_hubunit._kicks_dir


def test_HubUnit_default_kickunit_ReturnsObjWithCorrect_kick_id_WhenkickFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    delete_dir(sue_hubunit._kicks_dir)

    zero_kickunit = get_sue_kickunit()
    zero_kickunit._kick_id = sue_hubunit._get_next_kick_file_number()
    zero_kickunit._atoms_dir = sue_hubunit._atoms_dir
    zero_kickunit._kicks_dir = sue_hubunit._kicks_dir
    sue_hubunit.save_kick_file(zero_kickunit)

    # WHEN
    sue_kickunit = sue_hubunit._default_kickunit()

    # THEN
    assert sue_kickunit.owner_name == sue_str
    assert sue_kickunit._kick_id == init_kick_id() + 1
    assert sue_kickunit._kick_id == 1
    assert sue_kickunit._kick_id == sue_hubunit._get_next_kick_file_number()
    assert sue_kickunit.face_name is None
    assert sue_kickunit._atoms_dir == sue_hubunit._atoms_dir
    assert sue_kickunit._kicks_dir == sue_hubunit._kicks_dir


def test_HubUnit_get_kickunit_ReturnsObjWhenFilesDoesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    yao_str = "Yao"
    x0_kickunit = sue_hubunit._default_kickunit()
    x0_kickunit.set_face(yao_str)
    sue_hubunit.save_kick_file(x0_kickunit)
    bob_str = "Bob"
    x1_kickunit = sue_hubunit._default_kickunit()
    x1_kickunit.set_face(bob_str)
    sue_hubunit.save_kick_file(x1_kickunit)

    # WHEN
    y0_kickunit = sue_hubunit.get_kickunit(x0_kickunit._kick_id)
    y1_kickunit = sue_hubunit.get_kickunit(x1_kickunit._kick_id)

    # THEN
    assert y0_kickunit is not None
    assert y1_kickunit is not None
    assert yao_str in y0_kickunit.face_name
    assert bob_str not in y0_kickunit.face_name
    assert bob_str in y1_kickunit.face_name


def test_HubUnit_get_kickunit_RaisesExceptionWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    yao_str = "Yao"
    x0_kickunit = sue_hubunit._default_kickunit()
    x0_kickunit.set_face(yao_str)
    sue_hubunit.save_kick_file(x0_kickunit)
    bob_str = "Bob"
    x1_kickunit = sue_hubunit._default_kickunit()
    x1_kickunit.set_face(bob_str)
    sue_hubunit.save_kick_file(x1_kickunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.get_kickunit(six_file_number)
    assert (
        str(excinfo.value) == f"KickUnit file_number {six_file_number} does not exist."
    )


def test_HubUnit_del_kick_file_DeleteskickjsonAndNotBudAtomjsons(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    six_int = 6
    sue_kickunit = kickunit_shop(
        owner_name=sue_str,
        _kick_id=six_int,
        _atoms_dir=sue_hubunit._atoms_dir,
        _kicks_dir=sue_hubunit._kicks_dir,
    )
    sue_kickunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    zero_int = 0
    assert sue_hubunit.kick_file_exists(six_int) is False
    assert sue_hubunit.atom_file_exists(zero_int) is False

    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    sue_hubunit.save_kick_file(sue_kickunit, correct_invalid_attrs=False)

    print(f"{get_dir_file_strs(sue_hubunit._atoms_dir)}")
    assert sue_hubunit.kick_file_exists(six_int)
    assert sue_hubunit.atom_file_exists(zero_int)

    # WHEN
    sue_hubunit._del_kick_file(sue_kickunit._kick_id)

    # THEN
    assert sue_hubunit.kick_file_exists(six_int) is False
    assert sue_hubunit.atom_file_exists(zero_int)


def test_HubUnit_save_kick_file_CanCreateAndModify3kickunits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    delete_dir(sue_hubunit._kicks_dir)
    delete_dir(sue_hubunit._atoms_dir)
    set_dir(sue_hubunit._kicks_dir)
    set_dir(sue_hubunit._atoms_dir)
    assert len(get_dir_file_strs(sue_hubunit._kicks_dir)) == 0
    assert len(get_dir_file_strs(sue_hubunit._atoms_dir)) == 0

    # WHEN
    sue_hubunit.save_kick_file(sue_2budatoms_kickunit())
    sue_hubunit.save_kick_file(sue_3budatoms_kickunit())
    sue_hubunit.save_kick_file(sue_4budatoms_kickunit())

    # THEN
    assert len(get_dir_file_strs(sue_hubunit._kicks_dir)) == 3
    assert len(get_dir_file_strs(sue_hubunit._atoms_dir)) == 9


def test_HubUnit_save_kick_file_ReturnsValidObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    sue2_kickunit = sue_2budatoms_kickunit()
    sue2_kickunit._atoms_dir = create_path(sue_hubunit._keeps_dir, "swimming")
    sue2_kickunit._kicks_dir = create_path(sue_hubunit._keeps_dir, "swimming")
    sue2_kickunit.owner_name = "Bob"
    sue2_kickunit._kick_id = sue_hubunit._get_next_kick_file_number() - 5
    prev_sue2_kickunit = copy_deepcopy(sue2_kickunit)

    # WHEN
    valid_kickunit = sue_hubunit.save_kick_file(sue2_kickunit)

    # THEN
    assert valid_kickunit._kicks_dir != prev_sue2_kickunit._kicks_dir
    assert valid_kickunit._kicks_dir == sue_hubunit._kicks_dir
    assert valid_kickunit._atoms_dir == sue_hubunit._atoms_dir
    assert valid_kickunit._kick_id != prev_sue2_kickunit._kick_id


def test_HubUnit_create_save_kick_file_SaveCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    two_int = 2
    three_int = 3
    print(f"{sue_hubunit.kick_file_path(two_int)=}")
    print(f"{sue_hubunit.kick_file_path(three_int)=}")
    sue_kickunit = kickunit_shop(
        owner_name=sue_str,
        _kick_id=two_int,
        _atoms_dir=sue_hubunit._atoms_dir,
        _kicks_dir=sue_hubunit._kicks_dir,
    )
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    sue_hubunit.save_kick_file(sue_kickunit, correct_invalid_attrs=False)
    assert sue_hubunit.kick_file_exists(two_int)
    assert sue_hubunit.kick_file_exists(three_int) is False

    # WHEN
    before_bud = sue_hubunit.default_gut_bud()
    bob_str = "Bob"
    after_bud = copy_deepcopy(before_bud)
    after_bud.add_acctunit(bob_str)
    sue_hubunit.create_save_kick_file(before_bud, after_bud)

    # THEN
    assert sue_hubunit.kick_file_exists(three_int)


def test_HubUnit_merge_any_kicks_ReturnsObjThatIsEqual(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    save_gut_file(env_dir(), sue_hubunit.default_gut_bud())
    gut_bud = open_gut_file(env_dir(), "accord23", sue_str)
    gut_bud.last_kick_id is None

    # WHEN
    new_bud = sue_hubunit._merge_any_kicks(gut_bud)

    # THEN
    assert new_bud == gut_bud


def test_HubUnit_merge_any_kicks_ReturnsObj_WithSinglekickModifies_1atom(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    sue_hubunit.save_kick_file(sue_1budatoms_kickunit())
    save_gut_file(env_dir(), sue_hubunit.default_gut_bud())
    gut_bud = open_gut_file(env_dir(), "accord23", sue_str)
    print(f"{gut_bud.fisc_title=}")
    print(f"{sue_hubunit.fisc_title=}")
    sports_str = "sports"
    sports_road = gut_bud.make_l1_road(sports_str)
    knee_str = "knee"
    knee_road = gut_bud.make_road(sports_road, knee_str)
    assert gut_bud.item_exists(sports_road) is False

    # WHEN
    new_bud = sue_hubunit._merge_any_kicks(gut_bud)

    # THEN
    assert new_bud != gut_bud
    assert new_bud.item_exists(sports_road)


def test_HubUnit_merge_any_kicks_ReturnsObj_WithSinglekickModifies_2atoms(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), "accord23", sue_str)
    sue_hubunit.save_kick_file(sue_2budatoms_kickunit())
    save_gut_file(env_dir(), sue_hubunit.default_gut_bud())
    gut_bud = open_gut_file(env_dir(), "accord23", sue_str)
    print(f"{gut_bud.fisc_title=}")
    sports_str = "sports"
    sports_road = gut_bud.make_l1_road(sports_str)
    knee_str = "knee"
    knee_road = gut_bud.make_road(sports_road, knee_str)
    assert gut_bud.item_exists(sports_road) is False
    assert gut_bud.item_exists(knee_road) is False

    # WHEN
    new_bud = sue_hubunit._merge_any_kicks(gut_bud)

    # THEN
    assert new_bud != gut_bud
    assert new_bud.item_exists(sports_road)
    assert new_bud.item_exists(knee_road)
