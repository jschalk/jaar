from src.bud.origin import OriginHold, originhold_shop, OriginUnit, originunit_shop


def test_OriginHold_exists():
    # ESTABLISH
    bob_text = "Bob"
    bob_importance = 4

    # WHEN
    originhold_x = OriginHold(acct_id=bob_text, importance=bob_importance)

    # THEN
    assert originhold_x.acct_id == bob_text
    assert originhold_x.importance == bob_importance


def test_originhold_shop_ReturnsCorrectObj():
    # ESTABLISH
    bob_text = "Bob"
    bob_importance = 4

    # WHEN
    originhold_x = originhold_shop(acct_id=bob_text, importance=bob_importance)

    # THEN
    assert originhold_x.acct_id == bob_text
    assert originhold_x.importance == bob_importance


def test_originhold_shop_ImportanceIsNot_Reason():
    # ESTABLISH
    bob_text = "Bob"

    # WHEN
    originhold_x = originhold_shop(acct_id=bob_text)

    # THEN
    assert originhold_x.acct_id == bob_text
    assert originhold_x.importance == 1


def test_OriginHold_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    bob_text = "Bob"
    bob_originhold = originhold_shop(acct_id=bob_text)

    # WHEN
    x_dict = bob_originhold.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict is not None
    assert x_dict == {"acct_id": bob_text, "importance": 1}


def test_OriginUnit_exists():
    # ESTABLISH / WHEN
    originunit_x = OriginUnit()

    # THEN
    assert originunit_x
    assert originunit_x._originholds is None


def test_originunit_ReturnsCorrectObj():
    # ESTABLISH / WHEN
    originunit_x = originunit_shop()

    # THEN
    assert originunit_x._originholds == {}


def test_originunit_set_originhold_CorrectlySetsOriginHold():
    # ESTABLISH
    originunit_x = originunit_shop()

    # WHEN
    yao_text = "Yao"
    yao_importance = 3
    originunit_x.set_originhold(acct_id=yao_text, importance=yao_importance)

    # THEN
    assert originunit_x._originholds.get(yao_text) is not None
    assert originunit_x._originholds.get(yao_text).acct_id == yao_text
    assert originunit_x._originholds.get(yao_text).importance == yao_importance


def test_originunit_del_originhold_CorrectlyDeletesOriginHold():
    # ESTABLISH
    originunit_x = originunit_shop()
    yao_text = "Yao"
    yao_importance = 3
    originunit_x.set_originhold(acct_id=yao_text, importance=yao_importance)
    assert originunit_x._originholds.get(yao_text) is not None
    assert originunit_x._originholds.get(yao_text).acct_id == yao_text

    # WHEN
    originunit_x.del_originhold(acct_id=yao_text)

    # THEN
    assert originunit_x._originholds.get(yao_text) is None


def test_OriginUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    bob_text = "Bob"
    bob_originhold = originhold_shop(acct_id=bob_text)
    bob_ol_dict = bob_originhold.get_dict()
    sue_text = "Sue"
    sue_importance = 4
    sue_originhold = originhold_shop(acct_id=sue_text, importance=sue_importance)
    sue_ol_dict = sue_originhold.get_dict()

    originunit_x = originunit_shop()
    originunit_x.set_originhold(acct_id=bob_text, importance=None)
    originunit_x.set_originhold(acct_id=sue_text, importance=sue_importance)

    # WHEN
    x_dict = originunit_x.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict is not None
    assert x_dict == {"_originholds": {bob_text: bob_ol_dict, sue_text: sue_ol_dict}}
