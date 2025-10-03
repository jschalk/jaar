from src.ch10_pack_logic._ref.ch10_semantic_types import (
    BeliefName,
    FaceName,
    FirstLabel,
    FundGrain,
    FundNum,
    GroupTitle,
    HealerName,
    LabelTerm,
    MomentLabel,
    MoneyGrain,
    NameTerm,
    RespectGrain,
    RespectNum,
    RopeTerm,
    TitleTerm,
    VoiceName,
    default_knot_if_None,
)


class EventInt(int):
    pass


# TODO move to testing file
# def test_EventInt_Exists():
#     # ESTABLISH / WHEN / THEN
#     assert EventInt() == 0
#     assert EventInt(12) == 12
#     assert EventInt(12.4) == 12
