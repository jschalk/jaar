from src.ch04_group_logic._ref.ch04_semantic_types import (
    GroupTitle,
    HealerName,
    LabelTerm,
    MomentLabel,
    NameTerm,
    RopeTerm,
    TitleTerm,
    VoiceName,
    default_knot_if_None,
)


class BeliefName(NameTerm):
    """A NameTerm used to identify a BeliefUnit's belief"""

    pass


class FaceName(NameTerm):
    pass


# def test_FaceName_Exists():
#     # ESTABLISH / WHEN / THEN
#     assert FaceName() == ""
#     assert FaceName("cookie") == "cookie"
#     assert not FaceName(f"cookie{default_knot_if_None()}").is_name()
