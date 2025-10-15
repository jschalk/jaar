from enum import Enum
from src.ch02_rope.rope import RopeTerm, create_rope, create_rope_from_labels
from src.ch05_reason.reason import FactUnit, factunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom.atom_main import BeliefAtom, beliefatom_shop
from src.ch10_lesson.lesson_main import LessonUnit, lessonunit_shop
from src.ch10_lesson.test._util.ch10_examples import (
    get_atom_example_factunit_knee,
    get_atom_example_planunit_ball,
    get_atom_example_planunit_knee,
    get_atom_example_planunit_sports,
)
from src.ch11_bud.bud_main import BudUnit, budunit_shop
from src.ref.keywords import Ch11Keywords as wx

A23_STR = "amy23"
CASA_STR = "casa"
CLEAN_STR = "clean"
DIRTY_STR = "dirty"
GRIMY_STR = "grimy"
BOB_STR = "Bob"
SUE_STR = "Sue"
YAO_STR = "Yao"
BLUE_STR = "blue"
MOOP_STR = "mop"

SUE_BELIEF = beliefunit_shop(SUE_STR, A23_STR)
CASA_ROPE = SUE_BELIEF.make_l1_rope(CASA_STR)
MOP_ROPE = SUE_BELIEF.make_rope(CASA_ROPE, MOOP_STR)


class Ch11ExampleStrs(str, Enum):
    a23 = A23_STR
    casa = CASA_STR
    casa_rope = CASA_ROPE
    mop_rope = MOP_ROPE
    clean = CLEAN_STR
    dirty = DIRTY_STR
    grimy = GRIMY_STR
    bob = BOB_STR
    sue = SUE_STR
    yao = YAO_STR
    blue = BLUE_STR
    mop = MOOP_STR

    def __str__(self):
        return self.value


def get_ch11_example_moment_label() -> str:
    return "fizz"


def example_casa_clean_factunit() -> FactUnit:
    a23_str = "amy23"
    casa_rope = create_rope(a23_str, "casa")
    clean_rope = create_rope(casa_rope, "clean")
    return factunit_shop(casa_rope, clean_rope)


def example_casa_dirty_factunit() -> FactUnit:
    a23_str = "amy23"
    casa_rope = create_rope(a23_str, "casa")
    dirty_rope = create_rope(casa_rope, "dirty")
    return factunit_shop(casa_rope, dirty_rope)


def example_casa_grimy_factunit() -> FactUnit:
    a23_str = "amy23"
    casa_rope = create_rope(a23_str, "casa")
    grimy_rope = create_rope(casa_rope, "grimy")
    return factunit_shop(casa_rope, grimy_rope)


def example_sky_blue_factunit() -> FactUnit:
    a23_str = "amy23"
    sky_rope = create_rope(a23_str, "sky color")
    blue_rope = create_rope(sky_rope, "blue")
    return factunit_shop(sky_rope, blue_rope)


def get_budunit_55_example() -> BudUnit:
    x_bud_time = 55
    return budunit_shop(x_bud_time)


def get_budunit_66_example() -> BudUnit:
    t66_bud_time = 66
    t66_budunit = budunit_shop(t66_bud_time)
    t66_budunit.set_bud_voice_net("Sue", -5)
    t66_budunit.set_bud_voice_net("Bob", 5)
    return t66_budunit


def get_budunit_88_example() -> BudUnit:
    t88_bud_time = 88
    t88_budunit = budunit_shop(t88_bud_time)
    t88_budunit.quota = 800
    return t88_budunit


def get_budunit_invalid_example() -> BudUnit:
    t55_bud_time = 55
    t55_budunit = budunit_shop(t55_bud_time)
    t55_budunit.set_bud_voice_net("Sue", -5)
    t55_budunit.set_bud_voice_net("Bob", 3)
    return t55_budunit
