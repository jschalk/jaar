from src._road.finance import (
    default_bit_if_none,
    default_penny_if_none,
    default_coin_if_none,
    validate_bud_pool,
)
from src._world.world import worldunit_shop, WorldUnit
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    default_road_delimiter_if_none,
)
from src._world.origin import originunit_shop
from pytest import raises as pytest_raises


def test_WorldUnit_Exists():
    # GIVEN

    # WHEN
    x_world = WorldUnit()

    assert x_world
    assert x_world._real_id is None
    assert x_world._owner_id is None
    assert x_world._weight is None
    assert x_world._chars is None
    assert x_world._idearoot is None
    assert x_world._max_tree_traverse is None
    assert x_world._road_delimiter is None
    assert x_world._bud_pool is None
    assert x_world._coin is None
    assert x_world._bit is None
    assert x_world._penny is None
    assert x_world._monetary_desc is None
    assert x_world._credor_respect is None
    assert x_world._debtor_respect is None
    assert x_world._last_gift_id is None
    assert x_world._originunit is None

    assert x_world._idea_dict is None
    assert x_world._econ_dict is None
    assert x_world._healers_dict is None
    assert x_world._tree_traverse_count is None
    assert x_world._rational is None
    assert x_world._econs_justified is None
    assert x_world._econs_buildable is None
    assert x_world._sum_healerhold_share is None
    assert str(type(x_world._idearoot)).find("None") == 8


def test_WorldUnit_shop_ReturnsCorrectObjectWithFilledFields():
    # GIVEN
    sue_text = "Sue"
    iowa_real_id = "Iowa"
    slash_road_delimiter = "/"
    x_bud_pool = 555
    x_coin = 7
    x_bit = 5
    x_penny = 1

    # WHEN
    x_world = worldunit_shop(
        _owner_id=sue_text,
        _real_id=iowa_real_id,
        _road_delimiter=slash_road_delimiter,
        _bud_pool=x_bud_pool,
        _coin=x_coin,
        _bit=x_bit,
        _penny=x_penny,
    )
    assert x_world
    assert x_world._owner_id == sue_text
    assert x_world._real_id == iowa_real_id
    assert x_world._weight == 1
    assert x_world._chars == {}
    assert x_world._idearoot != None
    assert x_world._max_tree_traverse == 3
    assert x_world._road_delimiter == slash_road_delimiter
    assert x_world._bud_pool == x_bud_pool
    assert x_world._coin == x_coin
    assert x_world._bit == x_bit
    assert x_world._penny == x_penny
    assert x_world._monetary_desc is None
    assert x_world._credor_respect is None
    assert x_world._debtor_respect is None
    assert x_world._last_gift_id is None
    assert x_world._originunit == originunit_shop()

    assert x_world._idea_dict == {}
    assert x_world._econ_dict == {}
    assert x_world._healers_dict == {}
    assert x_world._tree_traverse_count is None
    assert x_world._rational is False
    assert x_world._econs_justified is False
    assert x_world._econs_buildable is False
    assert x_world._sum_healerhold_share == 0
    print(f"{type(x_world._idearoot)=}") == 0
    assert str(type(x_world._idearoot)).find(".idea.IdeaUnit'>") > 0


def test_WorldUnit_shop_ReturnsCorrectObjectWithCorrectEmptyField():
    # GIVEN / WHEN
    x_world = worldunit_shop()

    assert x_world._owner_id == ""
    assert x_world._real_id == root_label()
    assert x_world._road_delimiter == default_road_delimiter_if_none()
    assert x_world._bud_pool == validate_bud_pool()
    assert x_world._coin == default_coin_if_none()
    assert x_world._bit == default_bit_if_none()
    assert x_world._penny == default_penny_if_none()
    assert x_world._idearoot._coin == x_world._coin
    assert x_world._idearoot._road_delimiter == x_world._road_delimiter


def test_WorldUnit_ideaoot_uid_isEqualTo1():
    # GIVEN
    zia_text = "Zia"

    # WHEN
    zia_world = worldunit_shop(_owner_id=zia_text)

    # THEN
    assert zia_world._idearoot._uid == 1


def test_WorldUnit_set_max_tree_traverse_CorrectlySetsInt():
    # GIVEN
    zia_text = "Zia"
    zia_world = worldunit_shop(_owner_id=zia_text)
    assert zia_world._max_tree_traverse == 3

    # WHEN
    zia_world.set_max_tree_traverse(int_x=11)

    # THEN
    assert zia_world._max_tree_traverse == 11


def test_WorldUnit_set_max_tree_traverse_CorrectlyRaisesError():
    # GIVEN
    zia_text = "Zia"
    zia_world = worldunit_shop(_owner_id=zia_text)
    assert zia_world._max_tree_traverse == 3

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_world.set_max_tree_traverse(int_x=1)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: input '1' must be number that is 2 or greater"
    )


def test_WorldUnit_set_real_id_CorrectlySetsAttr():
    # GIVEN
    real_id_text = "Sun"
    sue_text = "Sue"
    x_world = worldunit_shop(_owner_id=sue_text)
    assert x_world._real_id == root_label()

    # WHEN
    x_world.set_real_id(real_id=real_id_text)

    # THEN
    assert x_world._real_id == real_id_text


def test_WorldUnit_set_road_delimiter_CorrectlySetsAttr():
    # GIVEN
    real_id_text = "Sun"
    sue_text = "Sue"
    slash_road_delimiter = "/"
    x_world = worldunit_shop(
        _owner_id=sue_text,
        _real_id=real_id_text,
        _road_delimiter=slash_road_delimiter,
    )
    assert x_world._road_delimiter == slash_road_delimiter

    # WHEN
    at_node_delimiter = "@"
    x_world.set_road_delimiter(new_road_delimiter=at_node_delimiter)

    # THEN
    assert x_world._road_delimiter == at_node_delimiter


def test_WorldUnit_make_road_ReturnsCorrectObj():
    # GIVEN
    real_id_text = "Sun"
    sue_text = "Sue"
    slash_road_delimiter = "/"
    x_world = worldunit_shop(
        _owner_id=sue_text,
        _real_id=real_id_text,
        _road_delimiter=slash_road_delimiter,
    )
    casa_text = "casa"
    v1_casa_road = x_world.make_l1_road(casa_text)

    # WHEN
    v2_casa_road = x_world.make_l1_road(casa_text)

    # THEN
    assert v1_casa_road == v2_casa_road


def test_WorldUnit_set_monetary_desc_SetsAttrCorrectly():
    # GIVEN
    sue_world = worldunit_shop("Sue", "Texas")
    sue_monetary_desc = "Folos"
    assert sue_world._monetary_desc != sue_monetary_desc

    # WHEN
    sue_world.set_monetary_desc(sue_monetary_desc)

    # THEN
    assert sue_world._monetary_desc == sue_monetary_desc


def test_WorldUnit_set_last_gift_id_SetsAttrCorrectly():
    # GIVEN
    sue_world = worldunit_shop("Sue", "Texas")
    assert sue_world._last_gift_id is None

    # WHEN
    x_last_gift_id = 89
    sue_world.set_last_gift_id(x_last_gift_id)

    # THEN
    assert sue_world._last_gift_id == x_last_gift_id


def test_WorldUnit_set_last_gift_id_RaisesError():
    # GIVEN
    sue_world = worldunit_shop("Sue", "Texas")
    old_last_gift_id = 89
    sue_world.set_last_gift_id(old_last_gift_id)

    # WHEN / THEN
    new_last_gift_id = 72
    assert new_last_gift_id < old_last_gift_id
    with pytest_raises(Exception) as excinfo:
        sue_world.set_last_gift_id(new_last_gift_id)
    assert (
        str(excinfo.value)
        == f"Cannot set _last_gift_id to {new_last_gift_id} because it is less than {old_last_gift_id}."
    )


def test_WorldUnit_del_last_gift_id_SetsAttrCorrectly():
    # GIVEN
    sue_world = worldunit_shop("Sue", "Texas")
    old_last_gift_id = 89
    sue_world.set_last_gift_id(old_last_gift_id)
    assert sue_world._last_gift_id != None

    # WHEN
    sue_world.del_last_gift_id()

    # WHEN
    assert sue_world._last_gift_id is None


def test_WorldUnit_set_bud_pool_CorrectlySetsAttr():
    # GIVEN
    sue_world = worldunit_shop("Sue", "Texas")
    sue_bud_pool = 99000
    assert sue_world._bud_pool == validate_bud_pool()

    # WHEN
    sue_world.set_bud_pool(sue_bud_pool)

    # THEN
    assert sue_world._bud_pool == 99000
