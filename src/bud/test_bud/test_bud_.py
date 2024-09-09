from src._road.finance import (
    default_bit_if_none,
    default_penny_if_none,
    default_fund_coin_if_none,
    validate_fund_pool,
    validate_respect_num,
)
from src.bud.bud import budunit_shop, BudUnit
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    default_road_delimiter_if_none,
)
from src.bud.origin import originunit_shop
from pytest import raises as pytest_raises


def test_BudUnit_Exists():
    # ESTABLISH /  WHEN
    x_bud = BudUnit()

    # THEN
    assert x_bud
    assert x_bud._real_id is None
    assert x_bud._owner_id is None
    assert x_bud._tally is None
    assert x_bud._accts is None
    assert x_bud._idearoot is None
    assert x_bud._max_tree_traverse is None
    assert x_bud._road_delimiter is None
    assert x_bud._fund_pool is None
    assert x_bud._fund_coin is None
    assert x_bud._bit is None
    assert x_bud._penny is None
    assert x_bud._monetary_desc is None
    assert x_bud._credor_respect is None
    assert x_bud._debtor_respect is None
    assert x_bud._last_gift_id is None
    assert x_bud._originunit is None
    # calculated attr
    assert x_bud._idea_dict is None
    assert x_bud._econ_dict is None
    assert x_bud._healers_dict is None
    assert x_bud._tree_traverse_count is None
    assert x_bud._rational is None
    assert x_bud._econs_justified is None
    assert x_bud._econs_buildable is None
    assert x_bud._sum_healerlink_share is None
    assert x_bud._offtrack_kids_mass_set is None
    assert x_bud._offtrack_fund is None
    assert x_bud._reason_bases is None
    assert x_bud._range_inheritors is None
    assert str(type(x_bud._idearoot)).find("None") == 8


def test_BudUnit_shop_ReturnsCorrectObjectWithFilledFields():
    # ESTABLISH
    sue_text = "Sue"
    iowa_real_id = "Iowa"
    slash_road_delimiter = "/"
    x_fund_pool = 555
    x_fund_coin = 7
    x_bit = 5
    x_penny = 1

    # WHEN
    x_bud = budunit_shop(
        _owner_id=sue_text,
        _real_id=iowa_real_id,
        _road_delimiter=slash_road_delimiter,
        _fund_pool=x_fund_pool,
        _fund_coin=x_fund_coin,
        _bit=x_bit,
        _penny=x_penny,
    )

    # THEN
    assert x_bud
    assert x_bud._owner_id == sue_text
    assert x_bud._real_id == iowa_real_id
    assert x_bud._tally == 1
    assert x_bud._accts == {}
    assert x_bud._idearoot is not None
    assert x_bud._max_tree_traverse == 3
    assert x_bud._road_delimiter == slash_road_delimiter
    assert x_bud._fund_pool == x_fund_pool
    assert x_bud._fund_coin == x_fund_coin
    assert x_bud._bit == x_bit
    assert x_bud._penny == x_penny
    assert not x_bud._monetary_desc
    assert x_bud._credor_respect == validate_respect_num()
    assert x_bud._debtor_respect == validate_respect_num()
    assert not x_bud._last_gift_id
    # calculated attr
    assert x_bud._originunit == originunit_shop()
    assert x_bud._idea_dict == {}
    assert x_bud._econ_dict == {}
    assert x_bud._healers_dict == {}
    assert not x_bud._tree_traverse_count
    assert x_bud._rational is False
    assert x_bud._econs_justified is False
    assert x_bud._econs_buildable is False
    assert x_bud._sum_healerlink_share == 0
    assert x_bud._offtrack_kids_mass_set == set()
    assert not x_bud._offtrack_fund
    assert x_bud._reason_bases == set()
    assert x_bud._range_inheritors == {}
    print(f"{type(x_bud._idearoot)=}") == 0
    assert str(type(x_bud._idearoot)).find(".idea.IdeaUnit'>") > 0


def test_BudUnit_shop_ReturnsCorrectObjectWithCorrectEmptyField():
    # ESTABLISH / WHEN
    x_bud = budunit_shop()

    # THEN
    assert x_bud._owner_id == ""
    assert x_bud._real_id == root_label()
    assert x_bud._road_delimiter == default_road_delimiter_if_none()
    assert x_bud._fund_pool == validate_fund_pool()
    assert x_bud._fund_coin == default_fund_coin_if_none()
    assert x_bud._bit == default_bit_if_none()
    assert x_bud._penny == default_penny_if_none()
    assert x_bud._idearoot._fund_coin == x_bud._fund_coin
    assert x_bud._idearoot._road_delimiter == x_bud._road_delimiter
    assert x_bud._idearoot._root
    assert x_bud._idearoot._uid == 1
    assert x_bud._idearoot._level == 0
    assert x_bud._idearoot._bud_real_id == x_bud._real_id
    assert x_bud._idearoot._road_delimiter == x_bud._road_delimiter
    assert x_bud._idearoot._parent_road == ""


def test_BudUnit_set_max_tree_traverse_CorrectlySetsInt():
    # ESTABLISH
    zia_text = "Zia"
    zia_bud = budunit_shop(_owner_id=zia_text)
    assert zia_bud._max_tree_traverse == 3

    # WHEN
    zia_bud.set_max_tree_traverse(x_int=11)

    # THEN
    assert zia_bud._max_tree_traverse == 11


def test_BudUnit_set_max_tree_traverse_CorrectlyRaisesError():
    # ESTABLISH
    zia_text = "Zia"
    zia_bud = budunit_shop(_owner_id=zia_text)
    assert zia_bud._max_tree_traverse == 3
    zia_tree_traverse = 1

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_max_tree_traverse(x_int=zia_tree_traverse)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: '1' must be number that is 2 or greater"
    )


def test_BudUnit_set_max_tree_traverse_CorrectlyRaisesError():
    # ESTABLISH
    zia_text = "Zia"
    zia_bud = budunit_shop(_owner_id=zia_text)
    assert zia_bud._max_tree_traverse == 3

    # WHEN/THEN
    zia_tree_traverse = 3.5
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_max_tree_traverse(x_int=zia_tree_traverse)
    assert (
        str(excinfo.value)
        == f"set_max_tree_traverse: '{zia_tree_traverse}' must be number that is 2 or greater"
    )


def test_BudUnit_set_road_delimiter_CorrectlySetsAttr():
    # ESTABLISH
    real_id_text = "Sun"
    slash_road_delimiter = "/"
    sue_text = "Sue"
    sue_bud = budunit_shop(sue_text, real_id_text, _road_delimiter=slash_road_delimiter)
    assert sue_bud._road_delimiter == slash_road_delimiter

    # WHEN
    at_node_delimiter = "@"
    sue_bud.set_road_delimiter(new_road_delimiter=at_node_delimiter)

    # THEN
    assert sue_bud._road_delimiter == at_node_delimiter


def test_BudUnit_make_road_ReturnsCorrectObj():
    # ESTABLISH
    real_id_text = "Sun"
    slash_road_delimiter = "/"
    sue_text = "Sue"
    sue_bud = budunit_shop(sue_text, real_id_text, _road_delimiter=slash_road_delimiter)
    casa_text = "casa"
    v1_casa_road = sue_bud.make_l1_road(casa_text)

    # WHEN
    v2_casa_road = sue_bud.make_l1_road(casa_text)

    # THEN
    assert v1_casa_road == v2_casa_road


def test_BudUnit_set_monetary_desc_SetsAttrCorrectly():
    # ESTABLISH
    sue_bud = budunit_shop("Sue", "Texas")
    sue_monetary_desc = "Folos"
    assert sue_bud._monetary_desc != sue_monetary_desc

    # WHEN
    sue_bud.set_monetary_desc(sue_monetary_desc)

    # THEN
    assert sue_bud._monetary_desc == sue_monetary_desc


def test_BudUnit_set_last_gift_id_SetsAttrCorrectly():
    # ESTABLISH
    sue_bud = budunit_shop("Sue", "Texas")
    assert sue_bud._last_gift_id is None

    # WHEN
    x_last_gift_id = 89
    sue_bud.set_last_gift_id(x_last_gift_id)

    # THEN
    assert sue_bud._last_gift_id == x_last_gift_id


def test_BudUnit_set_last_gift_id_RaisesError():
    # ESTABLISH
    sue_bud = budunit_shop("Sue", "Texas")
    old_last_gift_id = 89
    sue_bud.set_last_gift_id(old_last_gift_id)

    # WHEN / THEN
    new_last_gift_id = 72
    assert new_last_gift_id < old_last_gift_id
    with pytest_raises(Exception) as excinfo:
        sue_bud.set_last_gift_id(new_last_gift_id)
    assert (
        str(excinfo.value)
        == f"Cannot set _last_gift_id to {new_last_gift_id} because it is less than {old_last_gift_id}."
    )


def test_BudUnit_del_last_gift_id_SetsAttrCorrectly():
    # ESTABLISH
    sue_bud = budunit_shop("Sue", "Texas")
    old_last_gift_id = 89
    sue_bud.set_last_gift_id(old_last_gift_id)
    assert sue_bud._last_gift_id is not None

    # WHEN
    sue_bud.del_last_gift_id()

    # WHEN
    assert sue_bud._last_gift_id is None


def test_BudUnit_set_fund_pool_CorrectlySetsAttr():
    # ESTABLISH
    sue_bud = budunit_shop("Sue", "Texas")
    sue_fund_pool = 99000
    assert sue_bud._fund_pool == validate_fund_pool()

    # WHEN
    sue_bud.set_fund_pool(sue_fund_pool)

    # THEN
    assert sue_bud._fund_pool == 99000
