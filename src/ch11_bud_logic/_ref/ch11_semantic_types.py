from src.ch07_belief_logic._ref.ch07_semantic_types import (
    BeliefName,
    FaceName,
    GroupTitle,
    LabelTerm,
    MomentLabel,
    RopeTerm,
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
