from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import create_path, open_json
from src.ch10_lesson.delta import beliefdelta_shop
from src.ch10_lesson.lesson_main import create_lessonunit_from_files, lessonunit_shop
from src.ch10_lesson.test._util.ch10_env import (
    get_temp_dir as moments_dir,
    temp_dir_setup,
)
from src.ch10_lesson.test._util.ch10_examples import (
    get_atom_example_planunit_ball,
    get_atom_example_planunit_knee,
    get_atom_example_planunit_sports,
)
from src.ref.keywords import Ch10Keywords as kw


def test_LessonUnit_save_atom_file_SavesCorrectFile(temp_dir_setup):
    # ESTABLISH
    x_moment_dir = create_path(moments_dir(), "amy23")
    x_beliefs_dir = create_path(x_moment_dir, "beliefs")
    sue_str = "Sue"
    sue_belief_dir = create_path(x_beliefs_dir, sue_str)
    sue_atoms_dir = create_path(sue_belief_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = create_path(sue_atoms_dir, two_filename)
    sue_atom6_path = create_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_lessonunit = lessonunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert os_path_exists(sue_atom6_path) is False

    # WHEN
    sports_atom = get_atom_example_planunit_sports()
    sue_lessonunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert os_path_exists(sue_atom2_path)
    assert os_path_exists(sue_atom6_path) is False
    two_file_dict = open_json(sue_atoms_dir, two_filename)
    assert two_file_dict == sports_atom.to_dict()


def test_LessonUnit_atom_file_exists_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    x_moment_dir = create_path(moments_dir(), "amy23")
    x_beliefs_dir = create_path(x_moment_dir, "beliefs")
    sue_str = "Sue"
    sue_belief_dir = create_path(x_beliefs_dir, sue_str)
    sue_atoms_dir = create_path(sue_belief_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = create_path(sue_atoms_dir, two_filename)
    sue_atom6_path = create_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_lessonunit = lessonunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert sue_lessonunit.atom_file_exists(two_int) is False

    # WHEN
    sports_atom = get_atom_example_planunit_sports()
    sue_lessonunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert sue_lessonunit.atom_file_exists(two_int)


def test_LessonUnit_open_atom_file_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    x_moment_dir = create_path(moments_dir(), "amy23")
    x_beliefs_dir = create_path(x_moment_dir, "beliefs")
    sue_str = "Sue"
    sue_belief_dir = create_path(x_beliefs_dir, sue_str)
    sue_atoms_dir = create_path(sue_belief_dir, "atoms")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = create_path(sue_atoms_dir, two_filename)
    sue_atom6_path = create_path(sue_atoms_dir, six_filename)
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    sue_lessonunit = lessonunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    sports_atom = get_atom_example_planunit_sports()
    sue_lessonunit._save_atom_file(two_int, sports_atom)
    assert sue_lessonunit.atom_file_exists(two_int)

    # WHEN
    file_atom = sue_lessonunit._open_atom_file(two_int)

    # THEN
    assert file_atom == sports_atom


def test_LessonUnit_save_lesson_file_SavesCorrectFile(temp_dir_setup):
    # ESTABLISH
    x_moment_dir = create_path(moments_dir(), "amy23")
    x_beliefs_dir = create_path(x_moment_dir, "beliefs")
    sue_str = "Sue"
    sue_lesson_id = 2
    sue_belief_dir = create_path(x_beliefs_dir, sue_str)
    sue_lessons_dir = create_path(sue_belief_dir, "lessons")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_lesson2_path = create_path(sue_lessons_dir, two_filename)
    sue_lesson6_path = create_path(sue_lessons_dir, six_filename)
    print(f"{sue_lesson2_path=}")
    print(f"{sue_lesson6_path=}")
    sue_lessonunit = lessonunit_shop(
        sue_str, None, None, sue_lesson_id, _lessons_dir=sue_lessons_dir
    )
    assert os_path_exists(sue_lesson2_path) is False
    assert os_path_exists(sue_lesson6_path) is False

    # WHEN
    sue_lessonunit._save_lesson_file()

    # THEN
    assert os_path_exists(sue_lesson2_path)
    assert os_path_exists(sue_lesson6_path) is False
    lesson_file_dict = open_json(sue_lessons_dir, two_filename)
    print(f"{lesson_file_dict=}")
    assert lesson_file_dict.get("delta_atom_numbers") == []
    assert lesson_file_dict.get(kw.belief_name) == sue_str
    assert lesson_file_dict.get(kw.face_name) is None
    print(f"{lesson_file_dict.keys()=}")


def test_LessonUnit_lesson_file_exists_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    x_moment_dir = create_path(moments_dir(), "amy23")
    x_beliefs_dir = create_path(x_moment_dir, "beliefs")
    sue_str = "Sue"
    sue_belief_dir = create_path(x_beliefs_dir, sue_str)
    sue_lessons_dir = create_path(sue_belief_dir, "lessons")
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_lesson2_path = create_path(sue_lessons_dir, two_filename)
    sue_lesson6_path = create_path(sue_lessons_dir, six_filename)
    print(f"{sue_lesson2_path=}")
    print(f"{sue_lesson6_path=}")
    sue_lessonunit = lessonunit_shop(sue_str, _lessons_dir=sue_lessons_dir)
    assert os_path_exists(sue_lesson2_path) is False
    assert sue_lessonunit.lesson_file_exists() is False

    # WHEN
    sue_lessonunit._save_lesson_file()

    # THEN
    assert sue_lessonunit.lesson_file_exists()


def test_LessonUnit_save_files_SavesFiles(temp_dir_setup):
    # ESTABLISH
    x_moment_dir = create_path(moments_dir(), "amy23")
    x_beliefs_dir = create_path(x_moment_dir, "beliefs")
    sue_str = "Sue"
    sue_belief_dir = create_path(x_beliefs_dir, sue_str)
    sue_atoms_dir = create_path(sue_belief_dir, "atoms")
    sue_lessons_dir = create_path(sue_belief_dir, "lessons")

    zia_str = "Zia"
    yao_str = "Yao"
    sue_delta_start = 4
    sue_lessonunit = lessonunit_shop(
        sue_str, _atoms_dir=sue_atoms_dir, _lessons_dir=sue_lessons_dir
    )
    sue_lessonunit.set_delta_start(sue_delta_start)
    sue_lessonunit.set_face(zia_str)
    sue_lessonunit.set_face(yao_str)
    int4 = 4
    int5 = 5
    sports_atom = get_atom_example_planunit_sports()
    knee_atom = get_atom_example_planunit_knee()
    sue_lessonunit._beliefdelta.set_beliefatom(sports_atom)
    sue_lessonunit._beliefdelta.set_beliefatom(knee_atom)
    assert sue_lessonunit.lesson_file_exists() is False
    assert sue_lessonunit.atom_file_exists(int4) is False
    assert sue_lessonunit.atom_file_exists(int5) is False

    # WHEN
    sue_lessonunit.save_files()

    # THEN
    assert sue_lessonunit.lesson_file_exists()
    assert sue_lessonunit.atom_file_exists(int4)
    assert sue_lessonunit.atom_file_exists(int5)


def test_LessonUnit_create_beliefdelta_from_atom_files_SetsAttr(temp_dir_setup):
    # ESTABLISH
    x_moment_dir = create_path(moments_dir(), "amy23")
    x_beliefs_dir = create_path(x_moment_dir, "beliefs")
    sue_str = "Sue"
    sue_belief_dir = create_path(x_beliefs_dir, sue_str)
    sue_atoms_dir = create_path(sue_belief_dir, "atoms")

    sue_lessonunit = lessonunit_shop(sue_str, _atoms_dir=sue_atoms_dir)
    int4 = 4
    int5 = 5
    int9 = 9
    spor_atom = get_atom_example_planunit_sports()
    knee_atom = get_atom_example_planunit_knee()
    ball_atom = get_atom_example_planunit_ball()
    sue_lessonunit._save_atom_file(int4, spor_atom)
    sue_lessonunit._save_atom_file(int5, knee_atom)
    sue_lessonunit._save_atom_file(int9, ball_atom)
    assert sue_lessonunit._beliefdelta == beliefdelta_shop()

    # WHEN
    atoms_list = [int4, int5, int9]
    sue_lessonunit._create_beliefdelta_from_atom_files(atoms_list)

    # THEN
    static_beliefdelta = beliefdelta_shop()
    static_beliefdelta.set_beliefatom(spor_atom)
    static_beliefdelta.set_beliefatom(knee_atom)
    static_beliefdelta.set_beliefatom(ball_atom)
    assert sue_lessonunit._beliefdelta != beliefdelta_shop()
    assert sue_lessonunit._beliefdelta == static_beliefdelta


def test_create_lessonunit_from_files_ReturnsObj(temp_dir_setup):
    # ESTABLISH
    x_moment_dir = create_path(moments_dir(), "amy23")
    x_beliefs_dir = create_path(x_moment_dir, "beliefs")
    sue_str = "Sue"
    sue_belief_dir = create_path(x_beliefs_dir, sue_str)
    sue_atoms_dir = create_path(sue_belief_dir, "atoms")
    sue_lessons_dir = create_path(sue_belief_dir, "lessons")

    yao_str = "Yao"
    sue_delta_start = 4
    src_sue_lessonunit = lessonunit_shop(
        sue_str, _atoms_dir=sue_atoms_dir, _lessons_dir=sue_lessons_dir
    )
    src_sue_lessonunit.set_delta_start(sue_delta_start)
    src_sue_lessonunit.set_face(yao_str)
    sports_atom = get_atom_example_planunit_sports()
    knee_atom = get_atom_example_planunit_knee()
    ball_atom = get_atom_example_planunit_ball()
    src_sue_lessonunit._beliefdelta.set_beliefatom(sports_atom)
    src_sue_lessonunit._beliefdelta.set_beliefatom(knee_atom)
    src_sue_lessonunit._beliefdelta.set_beliefatom(ball_atom)
    src_sue_lessonunit.save_files()

    # WHEN
    new_sue_lessonunit = create_lessonunit_from_files(
        lessons_dir=sue_lessons_dir,
        lesson_id=src_sue_lessonunit._lesson_id,
        atoms_dir=sue_atoms_dir,
    )

    # THEN
    assert src_sue_lessonunit.belief_name == new_sue_lessonunit.belief_name
    assert src_sue_lessonunit.face_name == new_sue_lessonunit.face_name
    assert src_sue_lessonunit._beliefdelta == new_sue_lessonunit._beliefdelta
