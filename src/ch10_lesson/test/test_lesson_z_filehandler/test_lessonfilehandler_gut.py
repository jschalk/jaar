from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import create_path, delete_dir
from src.ch10_lesson.lesson_filehandler import (
    create_gut_path,
    gut_file_exists,
    lessonfilehandler_shop,
    open_gut_file,
    save_gut_file,
)
from src.ch10_lesson.lesson_main import init_lesson_id
from src.ch10_lesson.test._util.ch10_env import get_temp_dir as env_dir, temp_dir_setup
from src.ch10_lesson.test._util.ch10_examples import sue_2beliefatoms_lessonunit


def test_LessonFileHandler_default_gut_belief_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    slash_str = "/"
    x_fund_pool = 9000000
    pnine_float = 0.9
    pfour_float = 0.4
    sue_lessonfilehandler = lessonfilehandler_shop(
        env_dir(),
        "amy23",
        sue_str,
        knot=slash_str,
        fund_pool=x_fund_pool,
        fund_grain=pnine_float,
        respect_grain=pnine_float,
        mana_grain=pfour_float,
    )

    # WHEN
    sue_default_gut = sue_lessonfilehandler.default_gut_belief()

    # THEN
    assert sue_default_gut.moment_label == sue_lessonfilehandler.moment_label
    assert sue_default_gut.belief_name == sue_lessonfilehandler.belief_name
    assert sue_default_gut.knot == sue_lessonfilehandler.knot
    assert sue_default_gut.fund_pool == sue_lessonfilehandler.fund_pool
    assert sue_default_gut.fund_grain == sue_lessonfilehandler.fund_grain
    assert sue_default_gut.respect_grain == sue_lessonfilehandler.respect_grain
    assert sue_default_gut.mana_grain == sue_lessonfilehandler.mana_grain
    assert sue_default_gut.last_lesson_id == init_lesson_id()


def test_LessonFileHandler_create_initial_lesson_files_from_default_SavesLessonUnitFiles(
    temp_dir_setup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), "amy23", sue_str)
    init_lesson_filename = sue_lessonfilehandler.lesson_filename(init_lesson_id())
    init_lesson_file_path = create_path(
        sue_lessonfilehandler._lessons_dir, init_lesson_filename
    )
    assert os_path_exists(init_lesson_file_path) is False
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False

    # WHEN
    sue_lessonfilehandler._create_initial_lesson_files_from_default()

    # THEN
    assert os_path_exists(init_lesson_file_path)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False


def test_LessonFileHandler_create_gut_from_lessons_CreatesgutFileFromLessonFiles(
    temp_dir_setup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), "amy23", sue_str)
    init_lesson_filename = sue_lessonfilehandler.lesson_filename(init_lesson_id())
    init_lesson_file_path = create_path(
        sue_lessonfilehandler._lessons_dir, init_lesson_filename
    )
    sue_lessonfilehandler._create_initial_lesson_files_from_default()
    assert os_path_exists(init_lesson_file_path)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False

    # WHEN
    sue_lessonfilehandler._create_gut_from_lessons()

    # THEN
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    static_sue_gut = sue_lessonfilehandler._merge_any_lessons(
        sue_lessonfilehandler.default_gut_belief()
    )
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    assert gut_belief.to_dict() == static_sue_gut.to_dict()


def test_LessonFileHandler_create_initial_lesson_and_gut_files_CreatesLessonFilesAndgutFile(
    temp_dir_setup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), "amy23", sue_str)
    init_lesson_filename = sue_lessonfilehandler.lesson_filename(init_lesson_id())
    init_lesson_file_path = create_path(
        sue_lessonfilehandler._lessons_dir, init_lesson_filename
    )
    assert os_path_exists(init_lesson_file_path) is False
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False

    # WHEN
    sue_lessonfilehandler._create_initial_lesson_and_gut_files()

    # THEN
    assert os_path_exists(init_lesson_file_path)
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    static_sue_gut = sue_lessonfilehandler._merge_any_lessons(
        sue_lessonfilehandler.default_gut_belief()
    )
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    assert gut_belief.to_dict() == static_sue_gut.to_dict()


def test_LessonFileHandler_create_initial_lesson_files_from_gut_SavesOnlyLessonFiles(
    temp_dir_setup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), "amy23", sue_str)
    sue_gut_belief = sue_lessonfilehandler.default_gut_belief()
    bob_str = "Bob"
    sue_gut_belief.add_voiceunit(bob_str)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False
    save_gut_file(env_dir(), sue_gut_belief)
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    init_lesson_file_path = create_path(
        sue_lessonfilehandler._lessons_dir, f"{init_lesson_id()}.json"
    )
    assert os_path_exists(init_lesson_file_path) is False

    # WHEN
    sue_lessonfilehandler._create_initial_lesson_files_from_gut()

    # THEN
    assert os_path_exists(init_lesson_file_path)


def test_LessonFileHandler_initialize_lesson_gut_files_SavesgutFileAndLessonFile(
    temp_dir_setup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_lessonfilehandler = lessonfilehandler_shop(
        env_dir(), "amy23", sue_str, respect_grain=seven_int
    )
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False
    init_lesson_file_path = create_path(
        sue_lessonfilehandler._lessons_dir, f"{init_lesson_id()}.json"
    )
    delete_dir(sue_lessonfilehandler._lessons_dir)
    assert os_path_exists(init_lesson_file_path) is False

    # WHEN
    sue_lessonfilehandler.initialize_lesson_gut_files()

    # THEN
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    assert gut_belief.moment_label == "amy23"
    assert gut_belief.belief_name == sue_str
    assert gut_belief.respect_grain == seven_int
    assert os_path_exists(init_lesson_file_path)


def test_LessonFileHandler_initialize_lesson_gut_files_SavesOnlygutFile(
    temp_dir_setup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_lessonfilehandler = lessonfilehandler_shop(
        env_dir(), "amy23", sue_str, respect_grain=seven_int
    )
    sue_lessonfilehandler.initialize_lesson_gut_files()
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    gut_path = create_gut_path(env_dir(), "amy23", sue_str)
    delete_dir(gut_path)
    assert gut_file_exists(env_dir(), "amy23", sue_str) is False
    init_lesson_file_path = create_path(
        sue_lessonfilehandler._lessons_dir, f"{init_lesson_id()}.json"
    )
    assert os_path_exists(init_lesson_file_path)

    # WHEN
    sue_lessonfilehandler.initialize_lesson_gut_files()

    # THEN
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    assert gut_belief.moment_label == "amy23"
    assert gut_belief.belief_name == sue_str
    assert gut_belief.respect_grain == seven_int
    assert os_path_exists(init_lesson_file_path)


def test_LessonFileHandler_initialize_lesson_gut_files_SavesOnlyLessonFile(
    temp_dir_setup,
):
    # ESTABLISH
    sue_str = "Sue"
    seven_int = 25
    sue_lessonfilehandler = lessonfilehandler_shop(
        env_dir(), "amy23", sue_str, respect_grain=seven_int
    )
    sue_lessonfilehandler.initialize_lesson_gut_files()
    sue_gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    bob_str = "Bob"
    sue_gut_belief.add_voiceunit(bob_str)
    save_gut_file(env_dir(), sue_gut_belief)
    assert gut_file_exists(env_dir(), "amy23", sue_str)
    init_lesson_file_path = create_path(
        sue_lessonfilehandler._lessons_dir, f"{init_lesson_id()}.json"
    )
    delete_dir(sue_lessonfilehandler._lessons_dir)
    assert os_path_exists(init_lesson_file_path) is False

    # WHEN
    sue_lessonfilehandler.initialize_lesson_gut_files()

    # THEN
    assert sue_gut_belief.moment_label == "amy23"
    assert sue_gut_belief.belief_name == sue_str
    assert sue_gut_belief.respect_grain == seven_int
    assert sue_gut_belief.voice_exists(bob_str)
    assert os_path_exists(init_lesson_file_path)


def test_LessonFileHandler_append_lessons_to_gut_file_AddsLessonsTogutFile(
    temp_dir_setup,
):
    # ESTABLISH
    sue_str = "Sue"
    sue_lessonfilehandler = lessonfilehandler_shop(env_dir(), "amy23", sue_str)
    sue_lessonfilehandler.initialize_lesson_gut_files()
    sue_lessonfilehandler.save_lesson_file(sue_2beliefatoms_lessonunit())
    gut_belief = open_gut_file(env_dir(), "amy23", sue_str)
    # gut_belief.add_plan(gut_belief.make_l1_rope("sports"))
    sports_str = "sports"
    sports_rope = gut_belief.make_l1_rope(sports_str)
    knee_str = "knee"
    knee_rope = gut_belief.make_rope(sports_rope, knee_str)
    assert gut_belief.plan_exists(sports_rope) is False
    assert gut_belief.plan_exists(knee_rope) is False

    # WHEN
    new_belief = sue_lessonfilehandler.append_lessons_to_gut_file()

    # THEN
    assert new_belief != gut_belief
    assert new_belief.plan_exists(sports_rope)
    assert new_belief.plan_exists(knee_rope)
