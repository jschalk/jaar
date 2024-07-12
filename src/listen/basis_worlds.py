from src._road.road import OwnerID
from src._world.world import WorldUnit, worldunit_shop


def _is_empty_world(x_world: WorldUnit) -> bool:
    empty_world = create_empty_world(x_world)
    return x_world.get_dict() == empty_world.get_dict()


def create_empty_world(ref_world: WorldUnit, x_owner_id: OwnerID = None) -> WorldUnit:
    x_owner_id = ref_world._owner_id if x_owner_id is None else x_owner_id
    x_road_delimiter = ref_world._road_delimiter
    x_bud_pool = ref_world._bud_pool
    x_coin = ref_world._coin
    x_pixel = ref_world._pixel
    x_penny = ref_world._penny
    return worldunit_shop(
        _owner_id=x_owner_id,
        _real_id=ref_world._real_id,
        _road_delimiter=x_road_delimiter,
        _bud_pool=x_bud_pool,
        _coin=x_coin,
        _pixel=x_pixel,
        _penny=x_penny,
    )


def create_listen_basis(x_duty: WorldUnit) -> WorldUnit:
    x_listen = create_empty_world(x_duty, x_owner_id=x_duty._owner_id)
    x_listen._chars = x_duty._chars
    x_listen._beliefs = x_duty._beliefs
    x_listen.set_monetary_desc(x_duty._monetary_desc)
    x_listen.set_max_tree_traverse(x_duty._max_tree_traverse)
    if x_duty._char_credor_pool != None:
        x_listen.set_char_credor_pool(x_duty._char_credor_pool)
    if x_duty._char_debtor_pool != None:
        x_listen.set_char_debtor_pool(x_duty._char_debtor_pool)
    for x_charunit in x_listen._chars.values():
        x_charunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_action_world(voice: WorldUnit) -> WorldUnit:
    default_action_world = create_listen_basis(voice)
    default_action_world._last_gift_id = voice._last_gift_id
    default_action_world._char_credor_pool = None
    default_action_world._char_debtor_pool = None
    return default_action_world
