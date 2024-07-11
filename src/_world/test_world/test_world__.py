from src._road.finance import (
    default_pixel_if_none,
    default_penny_if_none,
    default_coin_if_none,
)
from src._world.examples.example_worlds import (
    get_world_1Task_1CE0MinutesReason_1Fact,
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
    assert x_world._beliefs is None
    assert x_world._idearoot is None
    assert x_world._max_tree_traverse is None
    assert x_world._road_delimiter is None
    assert x_world._coin is None
    assert x_world._pixel is None
    assert x_world._penny is None
    assert x_world._monetary_desc is None
    assert x_world._char_credor_pool is None
    assert x_world._char_debtor_pool is None
    assert x_world._last_gift_id is None
    assert x_world._meld_strategy is None
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
    noa_text = "Noa"
    iowa_real_id = "Iowa"
    slash_road_delimiter = "/"
    override_meld_strategy = "override"
    x_coin = 7
    x_pixel = 5
    x_penny = 1

    # WHEN
    x_world = worldunit_shop(
        _owner_id=noa_text,
        _real_id=iowa_real_id,
        _road_delimiter=slash_road_delimiter,
        _meld_strategy=override_meld_strategy,
        _coin=x_coin,
        _pixel=x_pixel,
        _penny=x_penny,
    )
    assert x_world
    assert x_world._owner_id == noa_text
    assert x_world._real_id == iowa_real_id
    assert x_world._weight == 1
    assert x_world._chars == {}
    assert x_world._beliefs == {}
    assert x_world._idearoot != None
    assert x_world._max_tree_traverse == 3
    assert x_world._road_delimiter == slash_road_delimiter
    assert x_world._coin == x_coin
    assert x_world._pixel == x_pixel
    assert x_world._penny == x_penny
    assert x_world._monetary_desc is None
    assert x_world._char_credor_pool is None
    assert x_world._char_debtor_pool is None
    assert x_world._last_gift_id is None
    assert x_world._meld_strategy == override_meld_strategy
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


def test_WorldUnit_shop_ReturnsCorrect_meld_strategy():
    # GIVEN
    noa_text = "Noa"
    iowa_real_id = "Iowa"
    # WHEN
    x_world = worldunit_shop(noa_text, iowa_real_id)
    # THEN
    assert x_world._meld_strategy == "default"


def test_WorldUnit_shop_ReturnsCorrectObjectWithCorrectEmptyField():
    # GIVEN / WHEN
    x_world = worldunit_shop()

    assert x_world._owner_id == ""
    assert x_world._real_id == root_label()
    assert x_world._road_delimiter == default_road_delimiter_if_none()
    assert x_world._coin == default_coin_if_none()
    assert x_world._pixel == default_pixel_if_none()
    assert x_world._penny == default_penny_if_none()


def test_WorldUnit_set_fact_IsAbleToSetTaskAsComplete():
    # GIVEN
    x_world = get_world_1Task_1CE0MinutesReason_1Fact()
    mail_text = "obtain mail"
    assert x_world != None
    assert len(x_world._idearoot._kids[mail_text]._reasonunits) == 1
    idea_dict = x_world.get_idea_dict()
    # for idea in idea_dict:
    #     print(idea._label)
    mail_idea = idea_dict.get(x_world.make_l1_road(mail_text))
    assert mail_idea.pledge == True
    assert mail_idea._task == True

    # WHEN
    ced_min_label = "CE0_minutes"
    ced_road = x_world.make_l1_road(ced_min_label)
    x_world.set_fact(base=ced_road, pick=ced_road, open=82, nigh=85)
    x_world.calc_world_metrics()

    # THEN
    assert mail_idea.pledge == True
    assert mail_idea._task is False


def test_WorldUnit_IsAbleToEditFactUnitAnyAncestor_Idea_1():
    x_world = get_world_1Task_1CE0MinutesReason_1Fact()
    ced_min_label = "CE0_minutes"
    ced_road = x_world.make_l1_road(ced_min_label)
    x_world.set_fact(base=ced_road, pick=ced_road, open=82, nigh=85)
    mail_road = x_world.make_l1_road("obtain mail")
    idea_dict = x_world.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.pledge == True
    assert mail_idea._task is False

    x_world.set_fact(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_dict = x_world.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.pledge == True
    assert mail_idea._task == True


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
    noa_text = "Noa"
    x_world = worldunit_shop(_owner_id=noa_text)
    assert x_world._real_id == root_label()

    # WHEN
    x_world.set_real_id(real_id=real_id_text)

    # THEN
    assert x_world._real_id == real_id_text


def test_WorldUnit_set_road_delimiter_CorrectlySetsAttr():
    # GIVEN
    real_id_text = "Sun"
    noa_text = "Noa"
    slash_road_delimiter = "/"
    x_world = worldunit_shop(
        _owner_id=noa_text,
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
    noa_text = "Noa"
    slash_road_delimiter = "/"
    x_world = worldunit_shop(
        _owner_id=noa_text,
        _real_id=real_id_text,
        _road_delimiter=slash_road_delimiter,
    )
    casa_text = "casa"
    v1_casa_road = x_world.make_l1_road(casa_text)

    # WHEN
    v2_casa_road = x_world.make_l1_road(casa_text)

    # THEN
    assert v1_casa_road == v2_casa_road


def test_WorldUnit_set_meld_strategy_CorrectlySetsAttr():
    # GIVEN
    noa_world = worldunit_shop("Noa", "Texas")
    override_text = "override"
    assert noa_world._meld_strategy != override_text

    # WHEN
    noa_world.set_meld_strategy(override_text)

    # THEN
    assert noa_world._meld_strategy == override_text


def test_WorldUnit_set_meld_strategy_RaisesErrorWithIneligible_meld_strategy():
    # GIVEN
    noa_world = worldunit_shop("Noa", "Texas")
    incorrect_override_text = "oVerride"
    assert noa_world._meld_strategy != incorrect_override_text

    # WHEN
    with pytest_raises(Exception) as excinfo:
        noa_world.set_meld_strategy(incorrect_override_text)
    assert (
        str(excinfo.value)
        == f"'{incorrect_override_text}' is ineligible meld_strategy."
    )


def test_WorldUnit_set_monetary_desc_SetsAttrCorrectly():
    # GIVEN
    noa_world = worldunit_shop("Noa", "Texas")
    noa_monetary_desc = "Folos"
    assert noa_world._monetary_desc != noa_monetary_desc

    # WHEN
    noa_world.set_monetary_desc(noa_monetary_desc)

    # THEN
    assert noa_world._monetary_desc == noa_monetary_desc


def test_WorldUnit_set_last_gift_id_SetsAttrCorrectly():
    # GIVEN
    noa_world = worldunit_shop("Noa", "Texas")
    assert noa_world._last_gift_id is None

    # WHEN
    x_last_gift_id = 89
    noa_world.set_last_gift_id(x_last_gift_id)

    # THEN
    assert noa_world._last_gift_id == x_last_gift_id


def test_WorldUnit_set_last_gift_id_RaisesError():
    # GIVEN
    noa_world = worldunit_shop("Noa", "Texas")
    old_last_gift_id = 89
    noa_world.set_last_gift_id(old_last_gift_id)

    # WHEN / THEN
    new_last_gift_id = 72
    assert new_last_gift_id < old_last_gift_id
    with pytest_raises(Exception) as excinfo:
        noa_world.set_last_gift_id(new_last_gift_id)
    assert (
        str(excinfo.value)
        == f"Cannot set _last_gift_id to {new_last_gift_id} because it is less than {old_last_gift_id}."
    )


def test_WorldUnit_del_last_gift_id_SetsAttrCorrectly():
    # GIVEN
    noa_world = worldunit_shop("Noa", "Texas")
    old_last_gift_id = 89
    noa_world.set_last_gift_id(old_last_gift_id)
    assert noa_world._last_gift_id != None

    # WHEN
    noa_world.del_last_gift_id()

    # WHEN
    assert noa_world._last_gift_id is None
