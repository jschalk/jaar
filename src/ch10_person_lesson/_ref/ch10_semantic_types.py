from ch02_allot._ref.ch02_semantic_types import GrainNum, PoolNum, WeightNum
from ch03_contact._ref.ch03_semantic_types import (
    ContactName,
    FundGrain,
    FundNum,
    GroupMark,
    GroupTitle,
    HealerName,
    NameTerm,
    RespectGrain,
    RespectNum,
    TitleTerm,
)
from ch05_rope._ref.ch05_semantic_types import (
    FirstLabel,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)
from ch08_person_logic._ref.ch08_semantic_types import ManaGrain, PersonName
from ch09_person_atom._ref.ch09_semantic_types import CRUD_command


class FaceName(NameTerm):
    """The Face is the source of all outside data."""

    pass


class MomentRope(RopeTerm):  # Created to help track the object class relations
    """The RopeTerm for a Moment. Must contain knots."""

    pass
