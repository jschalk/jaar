from src.a01_term_logic.rope import (
    create_rope,
    default_knot_if_None,
    get_default_central_label as root_label,
)
from src.a04_reason_logic.reason_plan import factunit_shop, reasonunit_shop
from src.a06_belief_logic.belief_main import beliefunit_shop
from src.a07_timeline_logic.reason_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from src.a07_timeline_logic.test._util.a07_str import (
    creg_str,
    time_str,
    week_str,
    yr1_jan1_offset_str,
)
from src.a07_timeline_logic.test._util.calendar_examples import (
    add_time_creg_planunit,
    add_time_five_planunit,
    creg_hour_int_label,
    creg_weekday_planunits,
    cregtime_planunit,
    display_current_creg_five_min,
    five_str,
    get_creg_config,
    get_creg_min_from_dt,
    get_cregtime_str,
    get_five_config,
    get_five_min_from_dt,
    get_fri,
    get_mon,
    get_sat,
    get_sun,
    get_thu,
    get_tue,
    get_wed,
)
from src.a07_timeline_logic.timeline_main import add_newtimeline_planunit, get_year_rope


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
        status_casa_rope, dirty_floors_case
    )

    # THEN
    assert dirty_floors_state_str
    x1 = default_knot_if_None()
    expected_str = f"case: {non_furniture_str}{x1}{dirty_floors_str}{x1} divided by {dirtiness_divisor_int} then from {dirtiness_lower_int} to {dirtiness_upper_int}"
    assert dirty_floors_state_str == expected_str


def test_get_reason_case_readable_str_ReturnsObj_Scenario4_Time_creg():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    sue_belief = add_newtimeline_planunit(sue_belief, get_creg_config())
    time_rope = sue_belief.make_l1_rope(time_str())
    creg_rope = sue_belief.make_rope(time_rope, creg_str())
    week_rope = sue_belief.make_rope(creg_rope, week_str())
    thu_rope = sue_belief.make_rope(week_rope, get_thu())
    thu_plan = sue_belief.get_plan_obj(thu_rope)

    casa_str = "casa"
    casa_rope = sue_belief.make_l1_rope(casa_str)
    mop_str = "mop"
    mop_rope = sue_belief.make_rope(casa_rope, mop_str)
    sue_belief.add_plan(mop_rope, task=True)
    sue_belief.edit_plan_attr(
        mop_rope,
        reason_context=week_rope,
        reason_case=week_rope,
        reason_lower=1440,
        reason_upper=2880,
    )
    mop_plan = sue_belief.get_plan_obj(mop_rope)
    week_reason = mop_plan.get_reasonunit(week_rope)
    week_case = week_reason.get_case(week_rope)

    # WHEN
    display_str = get_reason_case_readable_str(
        week_rope, week_case, creg_str(), sue_belief
    )

    # THEN
    assert display_str
    expected_str = f"case: every {get_thu()}"
    assert display_str == expected_str


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


def test_get_fact_state_readable_str_ReturnsObj_Scenario1_TwoLevel_state():
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


def test_get_fact_state_readable_str_ReturnsObj_Scenario2_CaseRange():
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


def test_get_fact_state_readable_str_ReturnsObj_Scenario3_Time_creg():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    time_rope = sue_belief.make_l1_rope(time_str())
    creg_rope = sue_belief.make_rope(time_rope, creg_str())
    sue_belief = add_newtimeline_planunit(sue_belief, get_creg_config())
    sue_belief.add_fact(creg_rope, creg_rope, 1234567890, 1334567890)
    root_creg_fact = sue_belief.planroot.factunits.get(creg_rope)
    print(f"{root_creg_fact=}")

    # WHEN
    timeline_fact_str = get_fact_state_readable_str(
        root_creg_fact, creg_str(), sue_belief
    )

    # THEN
    assert timeline_fact_str
    expected_str = (
        "from 7pm:30, Tuesday, 24 June, 2347 to 6am:10, Sunday, 11 August, 2537"
    )
    assert timeline_fact_str == expected_str
