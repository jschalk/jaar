from src.a01_term_logic.term import BelieverName
from src.a06_believer_logic.believer_main import BelieverUnit, believerunit_shop


def create_empty_believer_from_believer(
    ref_believer: BelieverUnit, x_believer_name: BelieverName = None
) -> BelieverUnit:
    x_believer_name = (
        ref_believer.believer_name if x_believer_name is None else x_believer_name
    )
    x_knot = ref_believer.knot
    x_fund_pool = ref_believer.fund_pool
    x_fund_iota = ref_believer.fund_iota
    x_respect_bit = ref_believer.respect_bit
    x_penny = ref_believer.penny
    return believerunit_shop(
        believer_name=x_believer_name,
        coin_label=ref_believer.coin_label,
        knot=x_knot,
        fund_pool=x_fund_pool,
        fund_iota=x_fund_iota,
        respect_bit=x_respect_bit,
        penny=x_penny,
    )


def create_listen_basis(x_believer: BelieverUnit) -> BelieverUnit:
    x_listen = create_empty_believer_from_believer(x_believer, x_believer.believer_name)
    x_listen.partners = x_believer.partners
    x_listen.set_max_tree_traverse(x_believer.max_tree_traverse)
    if x_believer.credor_respect is not None:
        x_listen.set_credor_respect(x_believer.credor_respect)
    if x_believer.debtor_respect is not None:
        x_listen.set_debtor_respect(x_believer.debtor_respect)
    for x_partnerunit in x_listen.partners.values():
        x_partnerunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_job(gut: BelieverUnit) -> BelieverUnit:
    default_job = create_listen_basis(gut)
    default_job.last_pack_id = gut.last_pack_id
    default_job.credor_respect = None
    default_job.debtor_respect = None
    return default_job
