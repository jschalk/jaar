from datetime import datetime
from enum import Enum
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ref.keywords import Ch24Keywords as kw

SUE_STR = "Sue"
A23_STR = "Amy23"
SUE_BELIEF = beliefunit_shop(SUE_STR, A23_STR)
CASA_STR = "casa"
CASA_ROPE = SUE_BELIEF.make_l1_rope(CASA_STR)
CLEAN_STR = "clean"
CLEAN_ROPE = SUE_BELIEF.make_rope(CASA_ROPE, CLEAN_STR)
MOP_STR = "mop"
MOP_ROPE = SUE_BELIEF.make_rope(CLEAN_ROPE, MOP_STR)
SWEEP_STR = "sweep"
SWEEP_ROPE = SUE_BELIEF.make_rope(CLEAN_ROPE, SWEEP_STR)
SCRUB_STR = "scrub"
SCRUB_ROPE = SUE_BELIEF.make_rope(CLEAN_ROPE, SCRUB_STR)


class ExampleValuesRef(str, Enum):
    sue = "Sue"
    a23 = "Amy23"
    casa_str = CASA_STR
    casa_rope = CASA_ROPE
    clean_str = CLEAN_STR
    clean_rope = CLEAN_ROPE
    mop_str = MOP_STR
    mop_rope = MOP_ROPE
    sweep_str = SWEEP_STR
    sweep_rope = SWEEP_ROPE
    scrub_str = SCRUB_STR
    scrub_rope = SCRUB_ROPE

    def __str__(self):
        return self.value
