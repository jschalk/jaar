from src.a01_term_logic.rope import RopeTerm, get_tail_label
from src.a04_reason_logic.reason_plan import CaseUnit, FactUnit
from src.a15_belief_logic.belief_main import BeliefUnit


def get_reason_case_readable_str(
    context: RopeTerm, caseunit: CaseUnit, beliefunit: BeliefUnit = None
) -> str:
    """Returns a string describing reason case in readable language. Will have special cases for time."""

    x_str = f"case: {caseunit.reason_state.replace(context, "", 1)}"
    if caseunit.reason_divisor:
        x_str += f" divided by {caseunit.reason_divisor} then"
    if caseunit.reason_lower is not None and caseunit.reason_upper is not None:
        x_str += f" from {caseunit.reason_lower} to {caseunit.reason_upper}"

    return x_str


def get_fact_state_readable_str(
    factunit: FactUnit, beliefunit: BeliefUnit = None
) -> str:
    """Returns a string describing fact in readable language. Will have special cases for time."""

    context_rope = factunit.fact_context
    state_rope = factunit.fact_state
    lower_float = factunit.fact_lower
    upper_float = factunit.fact_upper
    context_tail = get_tail_label(context_rope)
    state_trailing = state_rope.replace(context_rope, "", 1)
    x_str = f"({context_tail}) fact: {state_trailing}"
    if lower_float is not None and upper_float is not None:
        x_str += f" from {lower_float} to {upper_float}"

    return x_str
