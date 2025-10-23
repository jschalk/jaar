from src.ch13_keep._ref.ch13_semantic_types import (
    EpochInstant,
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
