from pytest import raises as pytest_raises
from src.ch01_py.file_toolbox import create_path
from src.ch02_allot.allot import default_grain_num_if_None, validate_pool_num
from src.ch04_rope.rope import default_knot_if_None
from src.ch10_lesson._ref.ch10_path import create_belief_dir_path
from src.ch10_lesson.lesson_filehandler import LessonFileHandler, lessonfilehandler_shop
from src.ch10_lesson.test._util.ch10_env import get_temp_dir


def test_LessonFileHandler_Exists():
    # ESTABLISH / WHEN
    x_lessonfilehandler = LessonFileHandler()

    # THEN
    assert not x_lessonfilehandler.moment_mstr_dir
    assert not x_lessonfilehandler.moment_label
    assert not x_lessonfilehandler.belief_name
    assert not x_lessonfilehandler.knot
    assert not x_lessonfilehandler.fund_pool
    assert not x_lessonfilehandler.fund_grain
    assert not x_lessonfilehandler.respect_grain
    assert not x_lessonfilehandler.mana_grain
    assert not x_lessonfilehandler.atoms_dir
    assert not x_lessonfilehandler.lessons_dir


def test_lessonfilehandler_shop_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = "src/ch15_moment/test/_util"
    a45_str = "amy45"
    sue_str = "Sue"
    x_knot = "/"
    x_fund_pool = 13000
    x_fund_grain = 13
    x_respect_grain = 9
    x_mana_grain = 3

    # WHEN
    x_lessonfilehandler = lessonfilehandler_shop(
        moment_mstr_dir=x_moment_mstr_dir,
        moment_label=a45_str,
        belief_name=sue_str,
        knot=x_knot,
        fund_pool=x_fund_pool,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        mana_grain=x_mana_grain,
    )

    # THEN
    assert x_lessonfilehandler.moment_mstr_dir == x_moment_mstr_dir
    assert x_lessonfilehandler.moment_label == a45_str
    assert x_lessonfilehandler.belief_name == sue_str
    assert x_lessonfilehandler.knot == x_knot
    assert x_lessonfilehandler.fund_pool == x_fund_pool
    assert x_lessonfilehandler.fund_grain == x_fund_grain
    assert x_lessonfilehandler.respect_grain == x_respect_grain
    assert x_lessonfilehandler.mana_grain == x_mana_grain
    sue_dir = create_belief_dir_path(x_moment_mstr_dir, a45_str, sue_str)
    assert x_lessonfilehandler.atoms_dir == create_path(sue_dir, "atoms")
    assert x_lessonfilehandler.lessons_dir == create_path(sue_dir, "lessons")


def test_lessonfilehandler_shop_ReturnsObjWhenEmpty():
    # ESTABLISH
    sue_str = "Sue"
    moment_mstr_dir = get_temp_dir()
    amy23_str = "amy23"

    # WHEN
    sue_lessonfilehandler = lessonfilehandler_shop(moment_mstr_dir, amy23_str, sue_str)

    # THEN
    assert sue_lessonfilehandler.moment_mstr_dir == moment_mstr_dir
    assert sue_lessonfilehandler.moment_label == amy23_str
    assert sue_lessonfilehandler.belief_name == sue_str
    assert sue_lessonfilehandler.knot == default_knot_if_None()
    assert sue_lessonfilehandler.fund_pool == validate_pool_num()
    assert sue_lessonfilehandler.fund_grain == default_grain_num_if_None()
    assert sue_lessonfilehandler.respect_grain == default_grain_num_if_None()
    assert sue_lessonfilehandler.mana_grain == default_grain_num_if_None()


def test_lessonfilehandler_shop_RaisesErrorIf_belief_name_Contains_knot():
    # ESTABLISH
    slash_str = "/"
    bob_str = f"Bob{slash_str}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        lessonfilehandler_shop(None, None, belief_name=bob_str, knot=slash_str)
    assertion_fail_str = (
        f"'{bob_str}' must be a LabelTerm. Cannot contain knot: '{slash_str}'"
    )
    assert str(excinfo.value) == assertion_fail_str
