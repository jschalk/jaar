from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises
from src.ch01_py.file_toolbox import (
    create_path,
    delete_dir,
    get_dir_file_strs,
    get_json_filename,
    open_file,
    open_json,
    save_file,
    set_dir,
)
from src.ch10_pack.pack_filehandler import (
    open_gut_file,
    packfilehandler_shop,
    save_gut_file,
)
from src.ch10_pack.pack_main import init_pack_id, packunit_shop
from src.ch10_pack.test._util.ch10_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir as env_dir,
)
from src.ch10_pack.test._util.ch10_examples import (
    get_atom_example_planunit_knee,
    get_sue_packunit,
    sue_1beliefatoms_packunit,
    sue_2beliefatoms_packunit,
    sue_3beliefatoms_packunit,
    sue_4beliefatoms_packunit,
)


def test_PackFileHandler_get_max_pack_file_number_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)

    # WHEN / THEN
    delete_dir(sue_packfilehandler._packs_dir)
    assert sue_packfilehandler.get_max_pack_file_number() is None
    assert sue_packfilehandler._get_next_pack_file_number() == init_pack_id()
    assert sue_packfilehandler._get_next_pack_file_number() == 0

    # ESTABLISH
    six_int = 6
    save_file(
        sue_packfilehandler._packs_dir, sue_packfilehandler.pack_filename(six_int), "x"
    )

    # WHEN / THEN
    assert sue_packfilehandler.get_max_pack_file_number() == six_int
    assert sue_packfilehandler._get_next_pack_file_number() == 7


def test_PackFileHandler_pack_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    assert sue_packfilehandler.hub_pack_file_exists(None) is False
    assert sue_packfilehandler.hub_pack_file_exists(0) is False
    six_int = 6
    print(f"{sue_packfilehandler.pack_file_path(six_int)=}")
    assert sue_packfilehandler.hub_pack_file_exists(six_int) is False

    # WHEN
    save_file(
        sue_packfilehandler._packs_dir, sue_packfilehandler.pack_filename(six_int), "x"
    )

    # THEN
    assert sue_packfilehandler.hub_pack_file_exists(None) is False
    assert sue_packfilehandler.hub_pack_file_exists(0) is False
    assert sue_packfilehandler.hub_pack_file_exists(six_int)


def test_PackFileHandler_save_pack_file_SaveCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_pack2_path = create_path(sue_packfilehandler._packs_dir, two_filename)
    sue_pack6_path = create_path(sue_packfilehandler._packs_dir, six_filename)
    print(f"{sue_pack2_path=}")
    print(f"{sue_pack6_path=}")
    sue_packunit = packunit_shop(
        belief_name=sue_str,
        _pack_id=two_int,
        _atoms_dir=sue_packfilehandler._atoms_dir,
        _packs_dir=sue_packfilehandler._packs_dir,
    )
    assert sue_packfilehandler.hub_pack_file_exists(two_int) is False
    assert sue_packfilehandler.hub_pack_file_exists(six_int) is False

    # WHEN
    sue_packfilehandler.save_pack_file(sue_packunit, correct_invalid_attrs=False)

    # THEN
    assert sue_packfilehandler.hub_pack_file_exists(two_int)
    assert sue_packfilehandler.hub_pack_file_exists(six_int) is False
    two_file_dict = open_json(sue_packfilehandler._packs_dir, two_filename)
    assert two_file_dict == sue_packunit.get_deltametric_dict()


def test_PackFileHandler_save_pack_file_RaisesErrorIfPackUnit_atoms_dir_IsWrong(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    x_pack_id = 6
    six_filename = get_json_filename(x_pack_id)
    sue_pack0_path = create_path(sue_packfilehandler._packs_dir, six_filename)
    print(f"{sue_pack0_path=}")
    sue_packunit = packunit_shop(
        belief_name=sue_str,
        _pack_id=x_pack_id,
        _atoms_dir="src\\incorrect_directory",
        _packs_dir=sue_packfilehandler._packs_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_packfilehandler.save_pack_file(sue_packunit, correct_invalid_attrs=False)
    expected_exception_str = f"PackUnit file cannot be saved because packunit._atoms_dir is incorrect: {sue_packunit._atoms_dir}. It must be {sue_packfilehandler._atoms_dir}."
    assert str(excinfo.value) == expected_exception_str


def test_PackFileHandler_save_pack_file_RaisesErrorIfPackUnit_packs_dir_IsWrong(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    x_pack_id = 6
    six_filename = get_json_filename(x_pack_id)
    sue_pack0_path = create_path(sue_packfilehandler._packs_dir, six_filename)
    print(f"{sue_pack0_path=}")
    sue_packunit = packunit_shop(
        belief_name=sue_str,
        _pack_id=x_pack_id,
        _atoms_dir=sue_packfilehandler._atoms_dir,
        _packs_dir="src\\incorrect_directory",
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_packfilehandler.save_pack_file(sue_packunit, correct_invalid_attrs=False)
    expected_exception_str = f"PackUnit file cannot be saved because packunit._packs_dir is incorrect: {sue_packunit._packs_dir}. It must be {sue_packfilehandler._packs_dir}."
    assert str(excinfo.value) == expected_exception_str


def test_PackFileHandler_save_pack_file_RaisesErrorIfPackUnit_belief_name_IsWrong(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    x_pack_id = 6
    six_filename = get_json_filename(x_pack_id)
    sue_pack0_path = create_path(sue_packfilehandler._packs_dir, six_filename)
    print(f"{sue_pack0_path=}")
    bob_str = "Bob"
    sue_packunit = packunit_shop(
        belief_name=bob_str,
        _pack_id=x_pack_id,
        _atoms_dir=sue_packfilehandler._atoms_dir,
        _packs_dir=sue_packfilehandler._packs_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_packfilehandler.save_pack_file(sue_packunit, correct_invalid_attrs=False)
    expected_exception_str = f"PackUnit file cannot be saved because packunit.belief_name is incorrect: {sue_packunit.belief_name}. It must be {sue_str}."
    assert str(excinfo.value) == expected_exception_str


def test_PackFileHandler_save_pack_file_RaisesErrorIf_replace_IsFalse(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    x_pack_id = 0
    six_filename = get_json_filename(x_pack_id)
    sue_packunit = packunit_shop(
        belief_name=sue_str,
        _pack_id=x_pack_id,
        _atoms_dir=sue_packfilehandler._atoms_dir,
        _packs_dir=sue_packfilehandler._packs_dir,
    )
    saved_packunit = sue_packfilehandler.save_pack_file(sue_packunit)

    print(f"{sue_packfilehandler.pack_file_path(x_pack_id)=}")
    assert sue_packfilehandler.hub_pack_file_exists(x_pack_id)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_packfilehandler.save_pack_file(
            saved_packunit, replace=False, correct_invalid_attrs=False
        )
    expected_exception_str = (
        f"PackUnit file {six_filename} exists and cannot be saved over."
    )
    assert str(excinfo.value) == expected_exception_str


def test_PackFileHandler_validate_packunit_ReturnsObjWithAttributesFixed(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_pack2_path = create_path(sue_packfilehandler._packs_dir, two_filename)
    print(f"{sue_pack2_path=}")

    # WHEN
    invalid_sue_packunit = packunit_shop(
        belief_name="Bob",
        _pack_id=sue_packfilehandler._get_next_pack_file_number() - 5,
        _atoms_dir=create_path(sue_packfilehandler._atoms_dir, "swimming"),
        _packs_dir=create_path(sue_packfilehandler._atoms_dir, "swimming"),
    )
    valid_packunit = sue_packfilehandler.validate_packunit(invalid_sue_packunit)

    # THEN
    assert valid_packunit._atoms_dir == sue_packfilehandler._atoms_dir
    assert valid_packunit._packs_dir == sue_packfilehandler._packs_dir
    assert valid_packunit._pack_id == sue_packfilehandler._get_next_pack_file_number()
    correct_sue_packunit = packunit_shop(
        belief_name=sue_str,
        _pack_id=sue_packfilehandler._get_next_pack_file_number(),
        _atoms_dir=sue_packfilehandler._atoms_dir,
        _packs_dir=sue_packfilehandler._packs_dir,
    )
    assert valid_packunit == correct_sue_packunit


def test_PackFileHandler_save_pack_file_SaveCorrectObj_correct_invalid_attrs_IsTrue(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    next_int = sue_packfilehandler._get_next_pack_file_number()
    next_filename = get_json_filename(next_int)
    sue_pack2_path = create_path(sue_packfilehandler._packs_dir, next_filename)
    print(f"{sue_pack2_path=}")
    assert sue_packfilehandler.hub_pack_file_exists(next_int) is False

    # WHEN
    invalid_sue_packunit = packunit_shop(
        belief_name="Bob",
        _pack_id=sue_packfilehandler._get_next_pack_file_number() - 5,
        _atoms_dir=create_path(sue_packfilehandler._atoms_dir, "swimming"),
        _packs_dir=create_path(sue_packfilehandler._atoms_dir, "swimming"),
    )
    sue_packfilehandler.save_pack_file(invalid_sue_packunit)

    # THEN
    assert sue_packfilehandler.hub_pack_file_exists(next_int)
    two_file_json = open_file(sue_packfilehandler._packs_dir, next_filename)


def test_PackFileHandler_default_packunit_ReturnsObjWithCorrect_pack_id_WhenNoPackFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)

    # WHEN
    delete_dir(sue_packfilehandler._packs_dir)
    sue_packunit = sue_packfilehandler._default_packunit()

    # THEN
    assert sue_packunit.belief_name == sue_str
    assert sue_packunit._pack_id == init_pack_id()
    assert sue_packunit._pack_id == 0
    assert sue_packunit._pack_id == sue_packfilehandler._get_next_pack_file_number()
    assert sue_packunit.face_name is None
    assert sue_packunit._atoms_dir == sue_packfilehandler._atoms_dir
    assert sue_packunit._packs_dir == sue_packfilehandler._packs_dir


def test_PackFileHandler_default_packunit_ReturnsObjWithCorrect_pack_id_WhenPackFilesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    delete_dir(sue_packfilehandler._packs_dir)

    zero_packunit = get_sue_packunit()
    zero_packunit._pack_id = sue_packfilehandler._get_next_pack_file_number()
    zero_packunit._atoms_dir = sue_packfilehandler._atoms_dir
    zero_packunit._packs_dir = sue_packfilehandler._packs_dir
    sue_packfilehandler.save_pack_file(zero_packunit)

    # WHEN
    sue_packunit = sue_packfilehandler._default_packunit()

    # THEN
    assert sue_packunit.belief_name == sue_str
    assert sue_packunit._pack_id == init_pack_id() + 1
    assert sue_packunit._pack_id == 1
    assert sue_packunit._pack_id == sue_packfilehandler._get_next_pack_file_number()
    assert sue_packunit.face_name is None
    assert sue_packunit._atoms_dir == sue_packfilehandler._atoms_dir
    assert sue_packunit._packs_dir == sue_packfilehandler._packs_dir


def test_PackFileHandler_get_packunit_ReturnsObjWhenFilesDoesExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    yao_str = "Yao"
    x0_packunit = sue_packfilehandler._default_packunit()
    x0_packunit.set_face(yao_str)
    sue_packfilehandler.save_pack_file(x0_packunit)
    bob_str = "Bob"
    x1_packunit = sue_packfilehandler._default_packunit()
    x1_packunit.set_face(bob_str)
    sue_packfilehandler.save_pack_file(x1_packunit)

    # WHEN
    y0_packunit = sue_packfilehandler.get_packunit(x0_packunit._pack_id)
    y1_packunit = sue_packfilehandler.get_packunit(x1_packunit._pack_id)

    # THEN
    assert y0_packunit is not None
    assert y1_packunit is not None
    assert yao_str in y0_packunit.face_name
    assert bob_str not in y0_packunit.face_name
    assert bob_str in y1_packunit.face_name


def test_PackFileHandler_get_packunit_RaisesExceptionWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # sourcery skip: extract-duplicate-method, inline-variable, move-assign-in-block
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    yao_str = "Yao"
    x0_packunit = sue_packfilehandler._default_packunit()
    x0_packunit.set_face(yao_str)
    sue_packfilehandler.save_pack_file(x0_packunit)
    bob_str = "Bob"
    x1_packunit = sue_packfilehandler._default_packunit()
    x1_packunit.set_face(bob_str)
    sue_packfilehandler.save_pack_file(x1_packunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        sue_packfilehandler.get_packunit(six_file_number)
    assertion_failure_str = f"PackUnit file_number {six_file_number} does not exist."
    assert str(excinfo.value) == assertion_failure_str


def test_PackFileHandler_del_pack_file_DeletespackjsonAndNotBeliefAtomjsons(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    six_int = 6
    sue_packunit = packunit_shop(
        belief_name=sue_str,
        _pack_id=six_int,
        _atoms_dir=sue_packfilehandler._atoms_dir,
        _packs_dir=sue_packfilehandler._packs_dir,
    )
    sue_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_knee())
    zero_int = 0
    assert sue_packfilehandler.hub_pack_file_exists(six_int) is False
    assert sue_packfilehandler.h_atom_file_exists(zero_int) is False

    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    sue_packfilehandler.save_pack_file(sue_packunit, correct_invalid_attrs=False)

    print(f"{get_dir_file_strs(sue_packfilehandler._atoms_dir)}")
    assert sue_packfilehandler.hub_pack_file_exists(six_int)
    assert sue_packfilehandler.h_atom_file_exists(zero_int)

    # WHEN
    sue_packfilehandler._del_pack_file(sue_packunit._pack_id)

    # THEN
    assert sue_packfilehandler.hub_pack_file_exists(six_int) is False
    assert sue_packfilehandler.h_atom_file_exists(zero_int)


def test_PackFileHandler_save_pack_file_CanCreateAndModify3packunits(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    delete_dir(sue_packfilehandler._packs_dir)
    delete_dir(sue_packfilehandler._atoms_dir)
    set_dir(sue_packfilehandler._packs_dir)
    set_dir(sue_packfilehandler._atoms_dir)
    assert len(get_dir_file_strs(sue_packfilehandler._packs_dir)) == 0
    assert len(get_dir_file_strs(sue_packfilehandler._atoms_dir)) == 0

    # WHEN
    sue_packfilehandler.save_pack_file(sue_2beliefatoms_packunit())
    sue_packfilehandler.save_pack_file(sue_3beliefatoms_packunit())
    sue_packfilehandler.save_pack_file(sue_4beliefatoms_packunit())

    # THEN
    assert len(get_dir_file_strs(sue_packfilehandler._packs_dir)) == 3
    assert len(get_dir_file_strs(sue_packfilehandler._atoms_dir)) == 9


def test_PackFileHandler_save_pack_file_ReturnsValidObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    sue2_packunit = sue_2beliefatoms_packunit()
    sue2_packunit._atoms_dir = create_path(sue_packfilehandler._atoms_dir, "swimming")
    sue2_packunit._packs_dir = create_path(sue_packfilehandler._atoms_dir, "swimming")
    sue2_packunit.belief_name = "Bob"
    sue2_packunit._pack_id = sue_packfilehandler._get_next_pack_file_number() - 5
    prev_sue2_packunit = copy_deepcopy(sue2_packunit)

    # WHEN
    valid_packunit = sue_packfilehandler.save_pack_file(sue2_packunit)

    # THEN
    assert valid_packunit._packs_dir != prev_sue2_packunit._packs_dir
    assert valid_packunit._packs_dir == sue_packfilehandler._packs_dir
    assert valid_packunit._atoms_dir == sue_packfilehandler._atoms_dir
    assert valid_packunit._pack_id != prev_sue2_packunit._pack_id


def test_PackFileHandler_create_save_pack_file_SaveCorrectObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    two_int = 2
    three_int = 3
    print(f"{sue_packfilehandler.pack_file_path(two_int)=}")
    print(f"{sue_packfilehandler.pack_file_path(three_int)=}")
    sue_packunit = packunit_shop(
        belief_name=sue_str,
        _pack_id=two_int,
        _atoms_dir=sue_packfilehandler._atoms_dir,
        _packs_dir=sue_packfilehandler._packs_dir,
    )
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    sue_packfilehandler.save_pack_file(sue_packunit, correct_invalid_attrs=False)
    assert sue_packfilehandler.hub_pack_file_exists(two_int)
    assert sue_packfilehandler.hub_pack_file_exists(three_int) is False

    # WHEN
    before_belief = sue_packfilehandler.default_gut_belief()
    bob_str = "Bob"
    after_belief = copy_deepcopy(before_belief)
    after_belief.add_voiceunit(bob_str)
    sue_packfilehandler.create_save_pack_file(before_belief, after_belief)

    # THEN
    assert sue_packfilehandler.hub_pack_file_exists(three_int)


def test_PackFileHandler_merge_any_packs_ReturnsObjThatIsEqual(env_dir_setup_cleanup):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    save_gut_file(env_dir(), sue_packfilehandler.default_gut_belief())
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    gut_belief.last_pack_id is None

    # WHEN
    new_belief = sue_packfilehandler._merge_any_packs(gut_belief)

    # THEN
    assert new_belief == gut_belief


def test_PackFileHandler_merge_any_packs_ReturnsObj_WithSinglepackModifies_1atom(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    sue_packfilehandler.save_pack_file(sue_1beliefatoms_packunit())
    save_gut_file(env_dir(), sue_packfilehandler.default_gut_belief())
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    print(f"{gut_belief.moment_label=}")
    print(f"{sue_packfilehandler.moment_label=}")
    sports_str = "sports"
    sports_rope = gut_belief.make_l1_rope(sports_str)
    knee_str = "knee"
    knee_rope = gut_belief.make_rope(sports_rope, knee_str)
    assert gut_belief.plan_exists(sports_rope) is False

    # WHEN
    new_belief = sue_packfilehandler._merge_any_packs(gut_belief)

    # THEN
    assert new_belief != gut_belief
    assert new_belief.plan_exists(sports_rope)


def test_PackFileHandler_merge_any_packs_ReturnsObj_WithSinglepackModifies_2atoms(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_packfilehandler = packfilehandler_shop(env_dir(), "amy23", sue_str)
    sue_packfilehandler.save_pack_file(sue_2beliefatoms_packunit())
    save_gut_file(env_dir(), sue_packfilehandler.default_gut_belief())
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    print(f"{gut_belief.moment_label=}")
    sports_str = "sports"
    sports_rope = gut_belief.make_l1_rope(sports_str)
    knee_str = "knee"
    knee_rope = gut_belief.make_rope(sports_rope, knee_str)
    assert gut_belief.plan_exists(sports_rope) is False
    assert gut_belief.plan_exists(knee_rope) is False

    # WHEN
    new_belief = sue_packfilehandler._merge_any_packs(gut_belief)

    # THEN
    assert new_belief != gut_belief
    assert new_belief.plan_exists(sports_rope)
    assert new_belief.plan_exists(knee_rope)
