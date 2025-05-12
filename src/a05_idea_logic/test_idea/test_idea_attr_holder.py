from src.a05_idea_logic.healer import healerlink_shop
from src.a05_idea_logic.idea import IdeaAttrHolder, ideaattrholder_shop


def test_IdeaAttrHolder_Exists():
    new_obj = IdeaAttrHolder()
    assert new_obj.mass is None
    assert new_obj.uid is None
    assert new_obj.reason is None
    assert new_obj.reason_rcontext is None
    assert new_obj.reason_premise is None
    assert new_obj.reason_premise_open is None
    assert new_obj.reason_pnigh is None
    assert new_obj.reason_premise_divisor is None
    assert new_obj.reason_del_premise_rcontext is None
    assert new_obj.reason_del_premise_pbranch is None
    assert new_obj.reason_rcontext_idea_active_requisite is None
    assert new_obj.teamunit is None
    assert new_obj.healerlink is None
    assert new_obj.begin is None
    assert new_obj.close is None
    assert new_obj.addin is None
    assert new_obj.numor is None
    assert new_obj.denom is None
    assert new_obj.morph is None
    assert new_obj.pledge is None
    assert new_obj.factunit is None
    assert new_obj.descendant_pledge_count is None
    assert new_obj.all_acct_cred is None
    assert new_obj.all_acct_debt is None
    assert new_obj.awardlink is None
    assert new_obj.awardlink_del is None
    assert new_obj.is_expanded is None


def test_IdeaAttrHolder_CorrectlyCalculatesPremiseRanges():
    # ESTABLISH
    idea_attr = IdeaAttrHolder(reason_premise="some_way")
    assert idea_attr.reason_premise_open is None
    assert idea_attr.reason_pnigh is None
    # assert idea_attr.reason_premise_numor is None
    assert idea_attr.reason_premise_divisor is None
    # assert idea_attr.reason_premise_morph is None

    # WHEN
    idea_attr.set_premise_range_attributes_influenced_by_premise_idea(
        premise_open=5.0,
        pnigh=20.0,
        # premise_numor,
        premise_denom=4.0,
        # premise_morph,
    )
    assert idea_attr.reason_premise_open == 5.0
    assert idea_attr.reason_pnigh == 20.0
    # assert idea_attr.reason_premise_numor is None
    assert idea_attr.reason_premise_divisor == 4.0
    # assert idea_attr.reason_premise_morph is None


def test_ideaattrholder_shop_ReturnsObj():
    # ESTABLISH
    sue_healerlink = healerlink_shop({"Sue", "Yim"})

    # WHEN
    x_ideaattrholder = ideaattrholder_shop(healerlink=sue_healerlink)

    # THEN
    assert x_ideaattrholder.healerlink == sue_healerlink
