from src.a01_term_logic.rope import RopeTerm
from src.a04_reason_logic.reason_plan import CaseUnit
from src.a15_belief_logic.belief_main import BeliefUnit


def get_reason_case_str(
    context: RopeTerm, caseunit: CaseUnit, beliefunit: BeliefUnit = None
) -> str:
    """Returns a string describing reason case in readable language. Will have special cases for time."""

    x_str = f"case: {caseunit.r_state.replace(context, "", 1)}"
    if caseunit.r_divisor:
        x_str += f" divided by {caseunit.r_divisor} then"
    if caseunit.r_lower is not None and caseunit is not None:
        x_str += f" from {caseunit.r_lower} to {caseunit.r_upper}"

    return x_str
