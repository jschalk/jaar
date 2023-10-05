from src.contract.origin import OriginLink, originlink_shop, OriginUnit, originunit_shop
from src.contract.party import PartyTitle
from pytest import raises as pytest_raises


def test_OriginLink_exists():
    # GIVEN
    roy_text = "Roy"
    roy_weight = 4

    # WHEN
    originlink_x = OriginLink(title=roy_text, weight=roy_weight)

    # THEN
    assert originlink_x.title == roy_text
    assert originlink_x.weight == roy_weight


def test_originlink_shop_ReturnsCorrectObj():
    # GIVEN
    roy_text = "Roy"
    roy_weight = 4

    # WHEN
    originlink_x = originlink_shop(title=roy_text, weight=roy_weight)

    # THEN
    assert originlink_x.title == roy_text
    assert originlink_x.weight == roy_weight


def test_originlink_shop_WeightIsNotRequired():
    # GIVEN
    roy_text = "Roy"
    # roy_title = PartyTitle(roy_text)

    # WHEN
    originlink_x = originlink_shop(title=roy_text)

    # THEN
    assert originlink_x.title == roy_text
    assert originlink_x.weight == 1


def test_OriginLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    roy_text = "Roy"
    roy_originlink = originlink_shop(title=roy_text)

    # WHEN
    x_dict = roy_originlink.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {"title": roy_text, "weight": 1}


def test_OriginUnit_exists():
    # GIVEN / WHEN
    originunit_x = OriginUnit()

    # THEN
    assert originunit_x
    assert originunit_x._links is None


def test_originunit_ReturnsCorrectObj():
    # GIVEN / WHEN
    originunit_x = originunit_shop()

    # THEN
    assert originunit_x._links == {}


def test_originunit__set_originlinks_empty_if_null_CorrectlySetsAttribute():
    # GIVEN
    originunit_x = originunit_shop()
    originunit_x._links = None
    assert originunit_x._links is None

    # WHEN
    originunit_x._set_originlinks_empty_if_null()

    # THEN
    assert originunit_x._links == {}


def test_originunit_set_originlink_CorrectlySetsOriginLink():
    # GIVEN
    originunit_x = originunit_shop()

    # WHEN
    tim_text = "tim"
    tim_weight = 3
    originunit_x.set_originlink(title=tim_text, weight=tim_weight)

    # THEN
    assert originunit_x._links.get(tim_text) != None
    assert originunit_x._links.get(tim_text).title == tim_text
    assert originunit_x._links.get(tim_text).weight == tim_weight


def test_originunit_del_originlink_CorrectlyDeletesOriginLink():
    # GIVEN
    originunit_x = originunit_shop()
    tim_text = "tim"
    tim_weight = 3
    originunit_x.set_originlink(title=tim_text, weight=tim_weight)
    assert originunit_x._links.get(tim_text) != None
    assert originunit_x._links.get(tim_text).title == tim_text

    # WHEN
    originunit_x.del_originlink(title=tim_text)

    # THEN
    assert originunit_x._links.get(tim_text) is None


def test_OriginUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    roy_text = "Roy"
    roy_originlink = originlink_shop(title=roy_text)
    roy_ol_dict = roy_originlink.get_dict()
    sue_text = "Sue"
    sue_weight = 4
    sue_originlink = originlink_shop(title=sue_text, weight=sue_weight)
    sue_ol_dict = sue_originlink.get_dict()

    originunit_x = originunit_shop()
    originunit_x.set_originlink(title=roy_text, weight=None)
    originunit_x.set_originlink(title=sue_text, weight=sue_weight)

    # WHEN
    x_dict = originunit_x.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {"_links": {roy_text: roy_ol_dict, sue_text: sue_ol_dict}}
