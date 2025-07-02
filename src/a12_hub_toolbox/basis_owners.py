from src.a01_term_logic.term import OwnerName
from src.a06_owner_logic.owner import OwnerUnit, ownerunit_shop


def _is_empty_owner(x_owner: OwnerUnit) -> bool:
    empty_owner = create_empty_owner_from_owner(x_owner)
    return x_owner.get_dict() == empty_owner.get_dict()


def create_empty_owner_from_owner(
    ref_owner: OwnerUnit, x_owner_name: OwnerName = None
) -> OwnerUnit:
    x_owner_name = ref_owner.owner_name if x_owner_name is None else x_owner_name
    x_knot = ref_owner.knot
    x_fund_pool = ref_owner.fund_pool
    x_fund_iota = ref_owner.fund_iota
    x_respect_bit = ref_owner.respect_bit
    x_penny = ref_owner.penny
    return ownerunit_shop(
        owner_name=x_owner_name,
        belief_label=ref_owner.belief_label,
        knot=x_knot,
        fund_pool=x_fund_pool,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )


def create_listen_basis(x_owner: OwnerUnit) -> OwnerUnit:
    x_listen = create_empty_owner_from_owner(x_owner, x_owner.owner_name)
    x_listen.accts = x_owner.accts
    x_listen.set_max_tree_traverse(x_owner.max_tree_traverse)
    if x_owner.credor_respect is not None:
        x_listen.set_credor_respect(x_owner.credor_respect)
    if x_owner.debtor_respect is not None:
        x_listen.set_debtor_respect(x_owner.debtor_respect)
    for x_acctunit in x_listen.accts.values():
        x_acctunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_job(gut: OwnerUnit) -> OwnerUnit:
    default_job = create_listen_basis(gut)
    default_job.last_pack_id = gut.last_pack_id
    default_job.credor_respect = None
    default_job.debtor_respect = None
    return default_job
