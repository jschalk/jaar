from src.a01_term_logic.term import OwnerName
from src.a06_plan_logic.plan import PlanUnit, planunit_shop


def _is_empty_plan(x_plan: PlanUnit) -> bool:
    empty_plan = create_empty_plan_from_plan(x_plan)
    return x_plan.get_dict() == empty_plan.get_dict()


def create_empty_plan_from_plan(
    ref_plan: PlanUnit, x_owner_name: OwnerName = None
) -> PlanUnit:
    x_owner_name = ref_plan.owner_name if x_owner_name is None else x_owner_name
    x_knot = ref_plan.knot
    x_fund_pool = ref_plan.fund_pool
    x_fund_iota = ref_plan.fund_iota
    x_respect_bit = ref_plan.respect_bit
    x_penny = ref_plan.penny
    return planunit_shop(
        owner_name=x_owner_name,
        bank_label=ref_plan.bank_label,
        knot=x_knot,
        fund_pool=x_fund_pool,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )


def create_listen_basis(x_plan: PlanUnit) -> PlanUnit:
    x_listen = create_empty_plan_from_plan(x_plan, x_plan.owner_name)
    x_listen.accts = x_plan.accts
    x_listen.set_max_tree_traverse(x_plan.max_tree_traverse)
    if x_plan.credor_respect is not None:
        x_listen.set_credor_respect(x_plan.credor_respect)
    if x_plan.debtor_respect is not None:
        x_listen.set_debtor_respect(x_plan.debtor_respect)
    for x_acctunit in x_listen.accts.values():
        x_acctunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_job(gut: PlanUnit) -> PlanUnit:
    default_job = create_listen_basis(gut)
    default_job.last_pack_id = gut.last_pack_id
    default_job.credor_respect = None
    default_job.debtor_respect = None
    return default_job
