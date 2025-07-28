from src.a01_term_logic.rope import (
    create_rope,
    default_knot_if_None,
    get_default_central_label as root_label,
)
from src.a04_reason_logic.reason_plan import (
    caseunit_shop,
    factunit_shop,
    reasonunit_shop,
)
from src.a15_belief_logic.reason_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)


def test_get_reason_case_readable_str_ReturnsObj_Scenario0_Level1():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    status_casa_str = "status casa"
    status_casa_rope = create_rope(casa_rope, status_casa_str)
    status_casa_reason = reasonunit_shop(status_casa_rope)
    dirty_floors_str = "dirty floors"
    dirty_floors_rope = create_rope(status_casa_rope, dirty_floors_str)
    status_casa_reason.set_case(dirty_floors_rope)
    dirty_floors_case = status_casa_reason.get_case(dirty_floors_rope)

    # WHEN
    dirty_floors_state_str = get_reason_case_readable_str(
        status_casa_rope, caseunit=dirty_floors_case
    )

    # THEN
    assert dirty_floors_state_str
    expected_str = f"case: {dirty_floors_str}{default_knot_if_None()}"
    assert dirty_floors_state_str == expected_str


def test_get_reason_case_readable_str_ReturnsObj_Scenario1_TwoLevel_state():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    status_casa_str = "status"
    status_casa_rope = create_rope(casa_rope, status_casa_str)
    status_casa_reason = reasonunit_shop(status_casa_rope)
    non_furniture_str = "non_furniture"
    non_furniture_rope = create_rope(status_casa_rope, non_furniture_str)
    dirty_floors_str = "dirty floors"
    dirty_floors_rope = create_rope(non_furniture_rope, dirty_floors_str)
    status_casa_reason.set_case(dirty_floors_rope)
    dirty_floors_case = status_casa_reason.get_case(dirty_floors_rope)

    # WHEN
    dirty_floors_state_str = get_reason_case_readable_str(
        context=status_casa_rope, caseunit=dirty_floors_case
    )

    # THEN
    assert dirty_floors_state_str
    default_knot = default_knot_if_None()
    expected_str = (
        f"case: {non_furniture_str}{default_knot}{dirty_floors_str}{default_knot}"
    )
    assert dirty_floors_state_str == expected_str


def test_get_reason_case_readable_str_ReturnsObj_Scenario2_CaseRange():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    status_casa_str = "status"
    status_casa_rope = create_rope(casa_rope, status_casa_str)
    status_casa_reason = reasonunit_shop(status_casa_rope)
    non_furniture_str = "non_furniture"
    non_furniture_rope = create_rope(status_casa_rope, non_furniture_str)
    dirty_floors_str = "dirty floors"
    dirty_floors_rope = create_rope(non_furniture_rope, dirty_floors_str)
    dirtiness_lower_int = 4
    dirtiness_upper_int = 8
    status_casa_reason.set_case(
        dirty_floors_rope,
        reason_lower=dirtiness_lower_int,
        reason_upper=dirtiness_upper_int,
    )
    dirty_floors_case = status_casa_reason.get_case(dirty_floors_rope)

    # WHEN
    dirty_floors_state_str = get_reason_case_readable_str(
        context=status_casa_rope, caseunit=dirty_floors_case
    )

    # THEN
    assert dirty_floors_state_str
    x1 = default_knot_if_None()
    expected_str = f"case: {non_furniture_str}{x1}{dirty_floors_str}{x1} from {dirtiness_lower_int} to {dirtiness_upper_int}"
    assert dirty_floors_state_str == expected_str


def test_get_reason_case_readable_str_ReturnsObj_Scenario3_CaseRangeAnd_reason_divisor():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    status_casa_str = "status"
    status_casa_rope = create_rope(casa_rope, status_casa_str)
    status_casa_reason = reasonunit_shop(status_casa_rope)
    non_furniture_str = "non_furniture"
    non_furniture_rope = create_rope(status_casa_rope, non_furniture_str)
    dirty_floors_str = "dirty floors"
    dirty_floors_rope = create_rope(non_furniture_rope, dirty_floors_str)
    dirtiness_lower_int = 4
    dirtiness_upper_int = 8
    dirtiness_divisor_int = 2
    status_casa_reason.set_case(
        dirty_floors_rope,
        reason_lower=dirtiness_lower_int,
        reason_upper=dirtiness_upper_int,
        reason_divisor=dirtiness_divisor_int,
    )
    dirty_floors_case = status_casa_reason.get_case(dirty_floors_rope)

    # WHEN
    dirty_floors_state_str = get_reason_case_readable_str(
        context=status_casa_rope, caseunit=dirty_floors_case
    )

    # THEN
    assert dirty_floors_state_str
    x1 = default_knot_if_None()
    expected_str = f"case: {non_furniture_str}{x1}{dirty_floors_str}{x1} divided by {dirtiness_divisor_int} then from {dirtiness_lower_int} to {dirtiness_upper_int}"
    assert dirty_floors_state_str == expected_str


def test_get_fact_state_readable_str_ReturnsObj_Scenario0_Level1():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    status_casa_str = "status casa"
    status_casa_rope = create_rope(casa_rope, status_casa_str)
    dirty_str = "dirty floors"
    dirty_rope = create_rope(status_casa_rope, dirty_str)
    status_casa_fact = factunit_shop(status_casa_rope, dirty_rope)

    # WHEN
    dirty_fact_str = get_fact_state_readable_str(factunit=status_casa_fact)

    # THEN
    assert dirty_fact_str
    default_knot = default_knot_if_None()
    expected_str = f"({status_casa_str}) fact: {dirty_str}{default_knot}"
    assert dirty_fact_str == expected_str


def test_get_reason_case_readable_str_ReturnsObj_Scenario1_TwoLevel_state():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    status_casa_str = "status"
    status_casa_rope = create_rope(casa_rope, status_casa_str)
    status_casa_reason = reasonunit_shop(status_casa_rope)
    non_furniture_str = "non_furniture"
    non_furniture_rope = create_rope(status_casa_rope, non_furniture_str)
    dirty_str = "dirty floors"
    dirty_rope = create_rope(non_furniture_rope, dirty_str)
    status_casa_reason.set_case(dirty_rope)
    status_casa_fact = factunit_shop(status_casa_rope, dirty_rope)

    # WHEN
    dirty_fact_str = get_fact_state_readable_str(status_casa_fact)

    # THEN
    assert dirty_fact_str
    default_knot = default_knot_if_None()
    expected_str = f"({status_casa_str}) fact: {non_furniture_str}{default_knot}{dirty_str}{default_knot}"
    assert dirty_fact_str == expected_str


def test_get_reason_case_readable_str_ReturnsObj_Scenario2_CaseRange():
    # ESTABLISH
    casa_str = "casa"
    casa_rope = create_rope(root_label(), casa_str)
    status_casa_str = "status"
    status_casa_rope = create_rope(casa_rope, status_casa_str)
    non_furniture_str = "non_furniture"
    non_furniture_rope = create_rope(status_casa_rope, non_furniture_str)
    dirty_str = "dirty floors"
    dirty_rope = create_rope(non_furniture_rope, dirty_str)
    dirtiness_lower_int = 4
    dirtiness_upper_int = 8
    status_casa_fact = factunit_shop(
        fact_context=status_casa_rope,
        fact_state=dirty_rope,
        fact_lower=dirtiness_lower_int,
        fact_upper=dirtiness_upper_int,
    )

    # WHEN
    dirty_fact_str = get_fact_state_readable_str(status_casa_fact)

    # THEN
    assert dirty_fact_str
    x1 = default_knot_if_None()
    expected_str = f"({status_casa_str}) fact: {non_furniture_str}{x1}{dirty_str}{x1} from {dirtiness_lower_int} to {dirtiness_upper_int}"
    assert dirty_fact_str == expected_str
