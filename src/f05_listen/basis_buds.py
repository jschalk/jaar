from src.f01_road.road import OwnerName
from src.f02_bud.bud import BudUnit, budunit_shop


def _is_empty_bud(x_bud: BudUnit) -> bool:
    empty_bud = create_empty_bud(x_bud)
    return x_bud.get_dict() == empty_bud.get_dict()


def create_empty_bud(ref_bud: BudUnit, x_owner_name: OwnerName = None) -> BudUnit:
    x_owner_name = ref_bud.owner_name if x_owner_name is None else x_owner_name
    x_bridge = ref_bud._bridge
    x_fund_pool = ref_bud.fund_pool
    x_fund_coin = ref_bud.fund_coin
    x_respect_bit = ref_bud.respect_bit
    x_penny = ref_bud.penny
    return budunit_shop(
        owner_name=x_owner_name,
        deal_idea=ref_bud.deal_idea,
        _bridge=x_bridge,
        fund_pool=x_fund_pool,
        fund_coin=x_fund_coin,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )


def create_listen_basis(x_duty: BudUnit) -> BudUnit:
    x_listen = create_empty_bud(x_duty, x_owner_name=x_duty.owner_name)
    x_listen.accts = x_duty.accts
    x_listen.set_max_tree_traverse(x_duty.max_tree_traverse)
    if x_duty.credor_respect is not None:
        x_listen.set_credor_respect(x_duty.credor_respect)
    if x_duty.debtor_respect is not None:
        x_listen.set_debtor_respect(x_duty.debtor_respect)
    for x_acctunit in x_listen.accts.values():
        x_acctunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_final_bud(voice: BudUnit) -> BudUnit:
    default_final_bud = create_listen_basis(voice)
    default_final_bud._last_gift_id = voice._last_gift_id
    default_final_bud.credor_respect = None
    default_final_bud.debtor_respect = None
    return default_final_bud
