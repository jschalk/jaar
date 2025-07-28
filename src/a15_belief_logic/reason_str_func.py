from src.a01_term_logic.rope import RopeTerm
from src.a04_reason_logic.reason_plan import CaseUnit
from src.a15_belief_logic.belief_main import BeliefUnit


def get_reason_case_str(
    context: RopeTerm, caseunit: CaseUnit, beliefunit: BeliefUnit = None
) -> str:
    """Returns a string describing reason case in readable language. Will have special cases for time."""

    x_str = f"case: {caseunit.reason_state.replace(context, "", 1)}"
    if caseunit.reason_divisor:
        x_str += f" divided by {caseunit.reason_divisor} then"
    if caseunit.reason_lower is not None and caseunit is not None:
        x_str += f" from {caseunit.reason_lower} to {caseunit.reason_upper}"

    return x_str
