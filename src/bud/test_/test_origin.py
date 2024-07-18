from src.bud.origin import OriginHold, originhold_shop, OriginUnit, originunit_shop


def test_OriginHold_exists():
    # ESTABLISH
    roy_text = "Roy"
    roy_weight = 4

    # WHEN
    originhold_x = OriginHold(char_id=roy_text, weight=roy_weight)

    # THEN
    assert originhold_x.char_id == roy_text
    assert originhold_x.weight == roy_weight


def test_originhold_shop_ReturnsCorrectObj():
    # ESTABLISH
    roy_text = "Roy"
    roy_weight = 4

    # WHEN
    originhold_x = originhold_shop(char_id=roy_text, weight=roy_weight)

    # THEN
    assert originhold_x.char_id == roy_text
    assert originhold_x.weight == roy_weight


def test_originhold_shop_WeightIsNot_Reason():
    # ESTABLISH
    roy_text = "Roy"

    # WHEN
    originhold_x = originhold_shop(char_id=roy_text)

    # THEN
    assert originhold_x.char_id == roy_text
    assert originhold_x.weight == 1


def test_OriginHold_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    roy_text = "Roy"
    roy_originhold = originhold_shop(char_id=roy_text)

    # WHEN
    x_dict = roy_originhold.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {"char_id": roy_text, "weight": 1}


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
    yao_weight = 3
    originunit_x.set_originhold(char_id=yao_text, weight=yao_weight)

    # THEN
    assert originunit_x._originholds.get(yao_text) != None
    assert originunit_x._originholds.get(yao_text).char_id == yao_text
    assert originunit_x._originholds.get(yao_text).weight == yao_weight


def test_originunit_del_originhold_CorrectlyDeletesOriginHold():
    # ESTABLISH
    originunit_x = originunit_shop()
    yao_text = "Yao"
    yao_weight = 3
    originunit_x.set_originhold(char_id=yao_text, weight=yao_weight)
    assert originunit_x._originholds.get(yao_text) != None
    assert originunit_x._originholds.get(yao_text).char_id == yao_text

    # WHEN
    originunit_x.del_originhold(char_id=yao_text)

    # THEN
    assert originunit_x._originholds.get(yao_text) is None


def test_OriginUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # ESTABLISH
    roy_text = "Roy"
    roy_originhold = originhold_shop(char_id=roy_text)
    roy_ol_dict = roy_originhold.get_dict()
    sue_text = "Sue"
    sue_weight = 4
    sue_originhold = originhold_shop(char_id=sue_text, weight=sue_weight)
    sue_ol_dict = sue_originhold.get_dict()

    originunit_x = originunit_shop()
    originunit_x.set_originhold(char_id=roy_text, weight=None)
    originunit_x.set_originhold(char_id=sue_text, weight=sue_weight)

    # WHEN
    x_dict = originunit_x.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {"_originholds": {roy_text: roy_ol_dict, sue_text: sue_ol_dict}}
