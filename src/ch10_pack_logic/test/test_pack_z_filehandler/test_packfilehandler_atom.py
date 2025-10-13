from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import create_path, get_dir_file_strs
from src.ch10_pack_logic.pack_filehandler import packfilehandler_shop
from src.ch10_pack_logic.test._util.ch10_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir as env_dir,
)
from src.ch10_pack_logic.test._util.ch10_examples import (
    get_atom_example_factunit_knee,
    get_atom_example_planunit_ball,
    get_atom_example_planunit_knee,
    get_atom_example_planunit_sports,
    get_ch10_example_moment_label as moment_label,
)


def test_PackFileHandler_atom_filename_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_packfilehandler = packfilehandler_shop(env_dir(), moment_label(), yao_str)
    one_int = 1

    # WHEN
    one_atom_filename = yao_packfilehandler.atom_filename(one_int)

    # THEN
    assert one_atom_filename == f"{one_int}.json"


def test_PackFileHandler_atom_file_path_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_packfilehandler = packfilehandler_shop(env_dir(), moment_label(), yao_str)
    one_int = 1

    # WHEN
    one_atom_file_path = yao_packfilehandler.atom_file_path(one_int)

    # THEN
    one_atom_filename = yao_packfilehandler.atom_filename(one_int)
    expected_path = create_path(yao_packfilehandler._atoms_dir, one_atom_filename)
    assert one_atom_file_path == expected_path


def test_PackFileHandler_save_valid_atom_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_packfilehandler = packfilehandler_shop(env_dir(), moment_label(), yao_str)
    one_int = 1
    assert os_path_exists(yao_packfilehandler.atom_file_path(one_int)) is False

    # WHEN
    knee_atom = get_atom_example_factunit_knee()
    atom_num = yao_packfilehandler._save_valid_atom_file(knee_atom, one_int)

    # THEN
    assert os_path_exists(yao_packfilehandler.atom_file_path(one_int))
    assert atom_num == one_int


def test_PackFileHandler_atom_file_exists_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_packfilehandler = packfilehandler_shop(env_dir(), moment_label(), yao_str)
    four_int = 4
    assert os_path_exists(yao_packfilehandler.atom_file_path(four_int)) is False
    assert yao_packfilehandler.h_atom_file_exists(four_int) is False

    # WHEN
    yao_packfilehandler._save_valid_atom_file(
        get_atom_example_factunit_knee(), four_int
    )

    # THEN
    assert os_path_exists(yao_packfilehandler.atom_file_path(four_int))
    assert yao_packfilehandler.h_atom_file_exists(four_int)


def test_PackFileHandler_delete_atom_file_DeletesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_packfilehandler = packfilehandler_shop(env_dir(), moment_label(), yao_str)
    ten_int = 10
    yao_packfilehandler._save_valid_atom_file(get_atom_example_factunit_knee(), ten_int)
    assert yao_packfilehandler.h_atom_file_exists(ten_int)

    # WHEN
    yao_packfilehandler.delete_atom_file(ten_int)

    # THEN
    assert yao_packfilehandler.h_atom_file_exists(ten_int) is False


def test_PackFileHandler_get_max_atom_file_number_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_packfilehandler = packfilehandler_shop(env_dir(), moment_label(), yao_str)
    ten_int = 10
    yao_packfilehandler._save_valid_atom_file(get_atom_example_factunit_knee(), ten_int)
    assert yao_packfilehandler.h_atom_file_exists(ten_int)

    # WHEN / THEN
    assert yao_packfilehandler.get_max_atom_file_number() == ten_int


def test_PackFileHandler_get_max_atom_file_number_ReturnsObjWhenDirIsEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_packfilehandler = packfilehandler_shop(env_dir(), moment_label(), yao_str)

    # WHEN / THEN
    assert yao_packfilehandler.get_max_atom_file_number() is None


def test_PackFileHandler_get_next_atom_file_number_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_packfilehandler = packfilehandler_shop(env_dir(), moment_label(), yao_str)
    # WHEN / THEN
    assert yao_packfilehandler._get_next_atom_file_number() == 0

    ten_int = 10
    yao_packfilehandler._save_valid_atom_file(get_atom_example_factunit_knee(), ten_int)
    assert yao_packfilehandler.h_atom_file_exists(ten_int)

    # WHEN / THEN
    assert yao_packfilehandler._get_next_atom_file_number() == 11


def test_PackFileHandler_save_atom_file_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_packfilehandler = packfilehandler_shop(env_dir(), moment_label(), yao_str)
    ten_int = 10
    yao_packfilehandler._save_valid_atom_file(get_atom_example_factunit_knee(), ten_int)
    assert yao_packfilehandler.get_max_atom_file_number() == ten_int
    eleven_int = ten_int + 1
    assert yao_packfilehandler.h_atom_file_exists(eleven_int) is False

    # WHEN
    atom_num1 = yao_packfilehandler.save_atom_file(get_atom_example_factunit_knee())

    # THEN
    assert yao_packfilehandler.get_max_atom_file_number() != ten_int
    assert yao_packfilehandler.get_max_atom_file_number() == eleven_int
    assert yao_packfilehandler.h_atom_file_exists(eleven_int)
    assert atom_num1 == eleven_int
    atom_num2 = yao_packfilehandler.save_atom_file(get_atom_example_factunit_knee())
    assert atom_num2 == 12


def test_PackFileHandler_get_belief_from_atom_files_ReturnsFileWithZeroAtoms(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_packfilehandler = packfilehandler_shop(env_dir(), moment_label(), yao_str)

    # WHEN
    yao_belief = yao_packfilehandler._get_belief_from_atom_files()

    # THEN
    assert yao_belief.belief_name == yao_str
    assert yao_belief.moment_label == yao_packfilehandler.moment_label
    assert yao_belief.knot == yao_packfilehandler.knot
    assert yao_belief.fund_pool == yao_packfilehandler.fund_pool
    assert yao_belief.fund_grain == yao_packfilehandler.fund_grain
    assert yao_belief.respect_grain == yao_packfilehandler.respect_grain


def test_PackFileHandler_get_belief_from_atom_files_ReturnsFile_SimplePlan(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_packfilehandler = packfilehandler_shop(env_dir(), moment_label(), yao_str)

    # save atom files
    sports_atom = get_atom_example_planunit_sports(yao_packfilehandler.moment_label)
    yao_packfilehandler.save_atom_file(sports_atom)

    # WHEN
    yao_belief = yao_packfilehandler._get_belief_from_atom_files()

    # THEN
    assert yao_belief.belief_name == yao_str
    assert yao_belief.moment_label == yao_packfilehandler.moment_label
    assert yao_belief.knot == yao_packfilehandler.knot
    sports_str = "sports"
    sports_rope = yao_belief.make_l1_rope(sports_str)

    assert yao_belief.plan_exists(sports_rope)


def test_PackFileHandler_get_belief_from_atom_files_ReturnsFile_WithFactUnit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    yao_str = "Yao"
    yao_packfilehandler = packfilehandler_shop(env_dir(), moment_label(), yao_str)

    # save atom files
    x_moment_label = yao_packfilehandler.moment_label
    yao_packfilehandler.save_atom_file(get_atom_example_planunit_sports(x_moment_label))
    yao_packfilehandler.save_atom_file(get_atom_example_planunit_ball(x_moment_label))
    yao_packfilehandler.save_atom_file(get_atom_example_planunit_knee(x_moment_label))
    yao_packfilehandler.save_atom_file(get_atom_example_factunit_knee(x_moment_label))
    print(f"{get_dir_file_strs(yao_packfilehandler._atoms_dir).keys()=}")

    # WHEN
    yao_belief = yao_packfilehandler._get_belief_from_atom_files()

    # THEN
    assert yao_belief.belief_name == yao_str
    assert yao_belief.moment_label == yao_packfilehandler.moment_label
    assert yao_belief.knot == yao_packfilehandler.knot
    sports_str = "sports"
    sports_rope = yao_belief.make_l1_rope(sports_str)

    assert yao_belief.plan_exists(sports_rope)
