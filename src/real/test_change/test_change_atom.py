from src.real.user import (
    userunit_shop,
    userunit_create_core_dir_and_files,
    userunit_save_atom_file,
    _save_valid_atom_file,
    userunit_atom_file_exists,
    _get_max_atom_file_number,
    _get_next_atom_file_number,
    _delete_atom_file,
    _get_agenda_from_atom_files,
)
from src.real.examples.example_atoms import (
    get_atom_example_beliefunit_knee,
    get_atom_example_ideaunit_sports,
    get_atom_example_ideaunit_ball,
    get_atom_example_ideaunit_knee,
)
from src.real.examples.real_env_kit import (
    get_test_reals_dir as reals_dir,
    get_test_real_id as real_id,
    reals_dir_setup_cleanup,
)
from src._instrument.file import dir_files as file_dir_files
from os.path import exists as os_path_exists


def test_save_valid_atom_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_userunit = userunit_shop(reals_dir(), real_id(), yao_text)
    one_int = 1
    assert os_path_exists(f"{yao_userunit._atoms_dir}/{one_int}.json") == False

    # WHEN
    knee_atom = get_atom_example_beliefunit_knee()
    atom_num = _save_valid_atom_file(yao_userunit, knee_atom, one_int)

    # THEN
    assert os_path_exists(f"{yao_userunit._atoms_dir}/{one_int}.json")
    assert atom_num == one_int


def test_userunit_atom_file_exists_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_userunit = userunit_shop(reals_dir(), real_id(), yao_text)
    five_int = 5
    assert os_path_exists(f"{yao_userunit._atoms_dir}/{five_int}.json") == False
    assert userunit_atom_file_exists(yao_userunit, five_int) == False

    # WHEN
    _save_valid_atom_file(yao_userunit, get_atom_example_beliefunit_knee(), five_int)

    # THEN
    assert os_path_exists(f"{yao_userunit._atoms_dir}/{five_int}.json")
    assert userunit_atom_file_exists(yao_userunit, five_int)


def test_delete_atom_file_CorrectlyDeletesFile(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_userunit = userunit_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    _save_valid_atom_file(yao_userunit, get_atom_example_beliefunit_knee(), ten_int)
    assert os_path_exists(f"{yao_userunit._atoms_dir}/{ten_int}.json")

    # WHEN
    _delete_atom_file(yao_userunit, ten_int)

    # THEN
    assert os_path_exists(f"{yao_userunit._atoms_dir}/{ten_int}.json") == False


def test_get_max_atom_file_number_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_userunit = userunit_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    _save_valid_atom_file(yao_userunit, get_atom_example_beliefunit_knee(), ten_int)
    assert os_path_exists(f"{yao_userunit._atoms_dir}/{ten_int}.json")

    # WHEN / THEN
    assert _get_max_atom_file_number(yao_userunit) == ten_int


def test_get_max_atom_file_number_ReturnsCorrectObjWhenDirIsEmpty(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_userunit = userunit_shop(reals_dir(), real_id(), yao_text)

    # WHEN / THEN
    assert _get_max_atom_file_number(yao_userunit) is None


def test_get_next_atom_file_number_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_userunit = userunit_shop(reals_dir(), real_id(), yao_text)
    # WHEN / THEN
    assert _get_next_atom_file_number(yao_userunit) == 0

    ten_int = 10
    _save_valid_atom_file(yao_userunit, get_atom_example_beliefunit_knee(), ten_int)
    assert os_path_exists(f"{yao_userunit._atoms_dir}/{ten_int}.json")

    # WHEN / THEN
    assert _get_next_atom_file_number(yao_userunit) == 11


def test_userunit_save_atom_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_userunit = userunit_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    _save_valid_atom_file(yao_userunit, get_atom_example_beliefunit_knee(), ten_int)
    assert _get_max_atom_file_number(yao_userunit) == ten_int
    eleven_int = ten_int + 1
    assert os_path_exists(f"{yao_userunit._atoms_dir}/{eleven_int}.json") == False

    # WHEN
    atom_num1 = userunit_save_atom_file(
        yao_userunit, get_atom_example_beliefunit_knee()
    )

    # THEN
    assert _get_max_atom_file_number(yao_userunit) != ten_int
    assert _get_max_atom_file_number(yao_userunit) == eleven_int
    assert os_path_exists(f"{yao_userunit._atoms_dir}/{eleven_int}.json")
    assert atom_num1 == eleven_int
    atom_num2 = userunit_save_atom_file(
        yao_userunit, get_atom_example_beliefunit_knee()
    )
    assert atom_num2 == 12


def test_get_agenda_from_atom_files_ReturnsCorrectFile_ZeroAtoms(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_userunit = userunit_shop(reals_dir(), real_id(), yao_text)
    userunit_create_core_dir_and_files(yao_userunit)

    # WHEN
    yao_agenda = _get_agenda_from_atom_files(yao_userunit)

    # THEN
    assert yao_agenda._owner_id == yao_text
    assert yao_agenda._real_id == yao_userunit.real_id
    assert yao_agenda._road_delimiter == yao_userunit._road_delimiter
    assert yao_agenda._planck == yao_userunit._planck


def test_get_agenda_from_atom_files_ReturnsCorrectFile_SimpleIdea(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_userunit = userunit_shop(reals_dir(), real_id(), yao_text)

    # save atom files
    sports_atom = get_atom_example_ideaunit_sports(yao_userunit.real_id)
    userunit_save_atom_file(yao_userunit, sports_atom)

    # WHEN
    yao_agenda = _get_agenda_from_atom_files(yao_userunit)

    # THEN
    assert yao_agenda._owner_id == yao_text
    assert yao_agenda._real_id == yao_userunit.real_id
    assert yao_agenda._road_delimiter == yao_userunit._road_delimiter
    sports_text = "sports"
    sports_road = yao_agenda.make_l1_road(sports_text)

    assert yao_agenda.idea_exists(sports_road)


def test_get_agenda_from_atom_files_ReturnsCorrectFile_WithBeliefUnit(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_userunit = userunit_shop(reals_dir(), real_id(), yao_text)
    userunit_create_core_dir_and_files(yao_userunit)

    # save atom files
    x_real_id = yao_userunit.real_id
    userunit_save_atom_file(yao_userunit, get_atom_example_ideaunit_sports(x_real_id))
    userunit_save_atom_file(yao_userunit, get_atom_example_ideaunit_ball(x_real_id))
    userunit_save_atom_file(yao_userunit, get_atom_example_ideaunit_knee(x_real_id))
    userunit_save_atom_file(yao_userunit, get_atom_example_beliefunit_knee(x_real_id))
    print(f"{file_dir_files(yao_userunit._atoms_dir).keys()=}")

    # WHEN
    yao_agenda = _get_agenda_from_atom_files(yao_userunit)

    # THEN
    assert yao_agenda._owner_id == yao_text
    assert yao_agenda._real_id == yao_userunit.real_id
    assert yao_agenda._road_delimiter == yao_userunit._road_delimiter
    sports_text = "sports"
    sports_road = yao_agenda.make_l1_road(sports_text)

    assert yao_agenda.idea_exists(sports_road)
