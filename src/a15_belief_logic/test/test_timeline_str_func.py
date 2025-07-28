from src.a01_term_logic.rope import (
    create_rope,
    default_knot_if_None,
    get_default_central_label as root_label,
)
from src.a04_reason_logic.reason_plan import caseunit_shop, reasonunit_shop
from src.a15_belief_logic.reason_str_func import get_reason_case_str


def test_get_reason_case_str_ReturnsObj_Scenario0_Level1():
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
    dirty_floors_context_str = get_reason_case_str(
        status_casa_rope, caseunit=dirty_floors_case
    )

    # THEN
    assert dirty_floors_context_str
    expected_str = f"case: {dirty_floors_str}{default_knot_if_None()}"
    assert dirty_floors_context_str == expected_str


def test_get_reason_case_str_ReturnsObj_Scenario1_():
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
    dirty_floors_context_str = get_reason_case_str(
        context=status_casa_rope, caseunit=dirty_floors_case
    )

    # THEN
    assert dirty_floors_context_str
    default_knot = default_knot_if_None()
    expected_str = (
        f"case: {non_furniture_str}{default_knot}{dirty_floors_str}{default_knot}"
    )
    assert dirty_floors_context_str == expected_str


def test_get_reason_case_str_ReturnsObj_Scenario1_TwoLevel_state():
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
    dirty_floors_context_str = get_reason_case_str(
        context=status_casa_rope, caseunit=dirty_floors_case
    )

    # THEN
    assert dirty_floors_context_str
    default_knot = default_knot_if_None()
    expected_str = (
        f"case: {non_furniture_str}{default_knot}{dirty_floors_str}{default_knot}"
    )
    assert dirty_floors_context_str == expected_str


def test_get_reason_case_str_ReturnsObj_Scenario2_CaseRange():
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
    dirty_floors_context_str = get_reason_case_str(
        context=status_casa_rope, caseunit=dirty_floors_case
    )

    # THEN
    assert dirty_floors_context_str
    x1 = default_knot_if_None()
    expected_str = f"case: {non_furniture_str}{x1}{dirty_floors_str}{x1} from {dirtiness_lower_int} to {dirtiness_upper_int}"
    assert dirty_floors_context_str == expected_str


def test_get_reason_case_str_ReturnsObj_Scenario3_CaseRangeAnd_reason_divisor():
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
    dirty_floors_context_str = get_reason_case_str(
        context=status_casa_rope, caseunit=dirty_floors_case
    )

    # THEN
    assert dirty_floors_context_str
    x1 = default_knot_if_None()
    expected_str = f"case: {non_furniture_str}{x1}{dirty_floors_str}{x1} divided by {dirtiness_divisor_int} then from {dirtiness_lower_int} to {dirtiness_upper_int}"
    assert dirty_floors_context_str == expected_str
