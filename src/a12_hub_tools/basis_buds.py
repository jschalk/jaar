from src.a01_way_logic.way import OwnerName
from src.a06_bud_logic.bud import BudUnit, budunit_shop


def _is_empty_bud(x_bud: BudUnit) -> bool:
    empty_bud = create_empty_bud_from_bud(x_bud)
    return x_bud.get_dict() == empty_bud.get_dict()


def create_empty_bud_from_bud(
    ref_bud: BudUnit, x_owner_name: OwnerName = None
) -> BudUnit:
    x_owner_name = ref_bud.owner_name if x_owner_name is None else x_owner_name
    x_bridge = ref_bud.bridge
    x_fund_pool = ref_bud.fund_pool
    x_fund_coin = ref_bud.fund_coin
    x_respect_bit = ref_bud.respect_bit
    x_penny = ref_bud.penny
    return budunit_shop(
        owner_name=x_owner_name,
        fisc_word=ref_bud.fisc_word,
        bridge=x_bridge,
        fund_pool=x_fund_pool,
        fund_coin=x_fund_coin,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )


def create_listen_basis(x_bud: BudUnit) -> BudUnit:
    x_listen = create_empty_bud_from_bud(x_bud, x_bud.owner_name)
    x_listen.accts = x_bud.accts
    x_listen.set_max_tree_traverse(x_bud.max_tree_traverse)
    if x_bud.credor_respect is not None:
        x_listen.set_credor_respect(x_bud.credor_respect)
    if x_bud.debtor_respect is not None:
        x_listen.set_debtor_respect(x_bud.debtor_respect)
    for x_acctunit in x_listen.accts.values():
        x_acctunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_job(gut: BudUnit) -> BudUnit:
    default_job = create_listen_basis(gut)
    default_job.last_pack_id = gut.last_pack_id
    default_job.credor_respect = None
    default_job.debtor_respect = None
    return default_job
