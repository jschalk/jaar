from src.ch07_belief_logic._ref.ch07_semantic_types import (
    FirstLabel,
    FundGrain,
    FundNum,
    GroupTitle,
    HealerName,
    KnotTerm,
    LabelTerm,
    NameTerm,
    RespectGrain,
    RespectNum,
    RopeTerm,
    TitleTerm,
    VoiceName,
    default_knot_if_None,
)


class EpochLabel(LabelTerm):
    "EpochLabel is required for every EpochUnit. It is a LabelTerm that must not contain the knot."

    pass


class EpochInstant(int):
    pass
