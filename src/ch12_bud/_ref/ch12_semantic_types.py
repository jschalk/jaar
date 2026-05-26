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
from ch10_person_lesson._ref.ch10_semantic_types import FaceName, MomentRope


class TimeNum(int):
    """An Integar that can represent a instant on the TimeNumLine"""

    pass


class SparkInt(int):
    """Each Spark is a int that describes the order of data ingestion"""

    pass
