from src._road.road import OwnerID
from src.bud.bud import BudUnit, budunit_shop


def _is_empty_bud(x_bud: BudUnit) -> bool:
    empty_bud = create_empty_bud(x_bud)
    return x_bud.get_dict() == empty_bud.get_dict()


def create_empty_bud(ref_bud: BudUnit, x_owner_id: OwnerID = None) -> BudUnit:
    x_owner_id = ref_bud._owner_id if x_owner_id is None else x_owner_id
    x_road_delimiter = ref_bud._road_delimiter
    x_fund_pool = ref_bud.fund_pool
    x_fund_coin = ref_bud.fund_coin
    x_bit = ref_bud.bit
    x_penny = ref_bud.penny
    return budunit_shop(
        _owner_id=x_owner_id,
        _fiscal_id=ref_bud._fiscal_id,
        _road_delimiter=x_road_delimiter,
        fund_pool=x_fund_pool,
        fund_coin=x_fund_coin,
        bit=x_bit,
        penny=x_penny,
    )


def create_listen_basis(x_duty: BudUnit) -> BudUnit:
    x_listen = create_empty_bud(x_duty, x_owner_id=x_duty._owner_id)
    x_listen._accts = x_duty._accts
    x_listen.set_monetary_desc(x_duty.monetary_desc)
    x_listen.set_max_tree_traverse(x_duty.max_tree_traverse)
    if x_duty.credor_respect is not None:
        x_listen.set_credor_respect(x_duty.credor_respect)
    if x_duty.debtor_respect is not None:
        x_listen.set_debtor_respect(x_duty.debtor_respect)
    for x_acctunit in x_listen._accts.values():
        x_acctunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_action_bud(voice: BudUnit) -> BudUnit:
    default_action_bud = create_listen_basis(voice)
    default_action_bud._last_gift_id = voice._last_gift_id
    default_action_bud.credor_respect = None
    default_action_bud.debtor_respect = None
    return default_action_bud
