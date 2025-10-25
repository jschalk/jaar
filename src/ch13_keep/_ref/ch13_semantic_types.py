from src.ch02_allot._ref.ch02_semantic_types import GrainNum, PoolNum, WeightNum
from src.ch03_voice._ref.ch03_semantic_types import (
    FundGrain,
    FundNum,
    GroupMark,
    GroupTitle,
    HealerName,
    NameTerm,
    RespectGrain,
    RespectNum,
    TitleTerm,
    VoiceName,
)
from src.ch04_rope._ref.ch04_semantic_types import (
    FirstLabel,
    KnotTerm,
    LabelTerm,
    RopeTerm,
    default_knot_if_None,
)
from src.ch07_belief_logic._ref.ch07_semantic_types import (
    BeliefName,
    ManaGrain,
    MomentLabel,
)
from src.ch08_belief_atom._ref.ch08_semantic_types import CRUD_command
from src.ch09_belief_lesson._ref.ch09_semantic_types import FaceName
from src.ch12_bud._ref.ch12_semantic_types import EpochTime, SparkInt


class ManaNum(float):
    """ManaNum inherits from float class"""

    pass
