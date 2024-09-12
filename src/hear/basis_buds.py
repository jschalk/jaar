from src._road.road import OwnerID
from src.bud.bud import BudUnit, budunit_shop


def _is_empty_bud(x_bud: BudUnit) -> bool:
    empty_bud = create_empty_bud(x_bud)
    return x_bud.get_dict() == empty_bud.get_dict()


def create_empty_bud(ref_bud: BudUnit, x_owner_id: OwnerID = None) -> BudUnit:
    x_owner_id = ref_bud._owner_id if x_owner_id is None else x_owner_id
    x_road_delimiter = ref_bud._road_delimiter
    x_fund_pool = ref_bud._fund_pool
    x_fund_coin = ref_bud._fund_coin
    x_bit = ref_bud._bit
    x_penny = ref_bud._penny
    return budunit_shop(
        _owner_id=x_owner_id,
        _pecun_id=ref_bud._pecun_id,
        _road_delimiter=x_road_delimiter,
        _fund_pool=x_fund_pool,
        _fund_coin=x_fund_coin,
        _bit=x_bit,
        _penny=x_penny,
    )


def create_hear_basis(x_duty: BudUnit) -> BudUnit:
    x_hear = create_empty_bud(x_duty, x_owner_id=x_duty._owner_id)
    x_hear._accts = x_duty._accts
    x_hear.set_monetary_desc(x_duty._monetary_desc)
    x_hear.set_max_tree_traverse(x_duty._max_tree_traverse)
    if x_duty._credor_respect is not None:
        x_hear.set_credor_respect(x_duty._credor_respect)
    if x_duty._debtor_respect is not None:
        x_hear.set_debtor_respect(x_duty._debtor_respect)
    for x_acctunit in x_hear._accts.values():
        x_acctunit.reset_hear_calculated_attrs()
    return x_hear


def get_default_action_bud(voice: BudUnit) -> BudUnit:
    default_action_bud = create_hear_basis(voice)
    default_action_bud._last_gift_id = voice._last_gift_id
    default_action_bud._credor_respect = None
    default_action_bud._debtor_respect = None
    return default_action_bud
