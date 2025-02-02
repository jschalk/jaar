from src.f02_bud.healer import healerlink_shop
from src.f02_bud.item import ItemAttrHolder, itemattrholder_shop


def test_ItemAttrHolder_Exists():
    new_obj = ItemAttrHolder()
    assert new_obj.mass is None
    assert new_obj.uid is None
    assert new_obj.reason is None
    assert new_obj.reason_base is None
    assert new_obj.reason_premise is None
    assert new_obj.reason_premise_open is None
    assert new_obj.reason_premise_nigh is None
    assert new_obj.reason_premise_divisor is None
    assert new_obj.reason_del_premise_base is None
    assert new_obj.reason_del_premise_need is None
    assert new_obj.reason_base_item_active_requisite is None
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


def test_ItemAttrHolder_CorrectlyCalculatesPremiseRanges():
    # ESTABLISH
    item_attr = ItemAttrHolder(reason_premise="some_road")
    assert item_attr.reason_premise_open is None
    assert item_attr.reason_premise_nigh is None
    # assert item_attr.reason_premise_numor is None
    assert item_attr.reason_premise_divisor is None
    # assert item_attr.reason_premise_morph is None

    # WHEN
    item_attr.set_premise_range_attributes_influenced_by_premise_item(
        premise_open=5.0,
        premise_nigh=20.0,
        # premise_numor,
        premise_denom=4.0,
        # premise_morph,
    )
    assert item_attr.reason_premise_open == 5.0
    assert item_attr.reason_premise_nigh == 20.0
    # assert item_attr.reason_premise_numor is None
    assert item_attr.reason_premise_divisor == 4.0
    # assert item_attr.reason_premise_morph is None


def test_itemattrholder_shop_ReturnsObj():
    # ESTABLISH
    sue_healerlink = healerlink_shop({"Sue", "Yim"})

    # WHEN
    x_itemattrholder = itemattrholder_shop(healerlink=sue_healerlink)

    # THEN
    assert x_itemattrholder.healerlink == sue_healerlink
