from src.ch07_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.ch11_belief_listen._ref.ch11_semantic_types import BeliefName


def create_empty_belief_from_belief(
    ref_belief: BeliefUnit, x_belief_name: BeliefName = None
) -> BeliefUnit:
    x_belief_name = ref_belief.belief_name if x_belief_name is None else x_belief_name
    x_knot = ref_belief.knot
    x_fund_pool = ref_belief.fund_pool
    x_fund_grain = ref_belief.fund_grain
    x_respect_grain = ref_belief.respect_grain
    x_mana_grain = ref_belief.mana_grain
    return beliefunit_shop(
        belief_name=x_belief_name,
        moment_label=ref_belief.moment_label,
        knot=x_knot,
        fund_pool=x_fund_pool,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        mana_grain=x_mana_grain,
    )


def create_listen_basis(x_belief: BeliefUnit) -> BeliefUnit:
    x_listen = create_empty_belief_from_belief(x_belief, x_belief.belief_name)
    x_listen.voices = x_belief.voices
    x_listen.set_max_tree_traverse(x_belief.max_tree_traverse)
    if x_belief.credor_respect is not None:
        x_listen.set_credor_respect(x_belief.credor_respect)
    if x_belief.debtor_respect is not None:
        x_listen.set_debtor_respect(x_belief.debtor_respect)
    for x_voiceunit in x_listen.voices.values():
        x_voiceunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_job(gut: BeliefUnit) -> BeliefUnit:
    default_job = create_listen_basis(gut)
    default_job.last_lesson_id = gut.last_lesson_id
    default_job.credor_respect = None
    default_job.debtor_respect = None
    return default_job
