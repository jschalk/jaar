from src.a03_group_logic.group import groupunit_shop
from src.a06_plan_logic.plan import planunit_shop


def test_PlanUnit_get_acctunit_group_titles_dict_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    zia_str = "Zia"
    bob_plan = planunit_shop("Bob")
    bob_plan.add_acctunit(yao_str)
    bob_plan.add_acctunit(sue_str)
    bob_plan.add_acctunit(zia_str)
    sue_acctunit = bob_plan.get_acct(sue_str)
    zia_acctunit = bob_plan.get_acct(zia_str)
    run_str = ";Run"
    swim_str = ";Swim"
    sue_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(swim_str)

    # WHEN
    group_titles_dict = bob_plan.get_acctunit_group_titles_dict()

    # THEN
    print(f"{group_titles_dict=}")
    all_group_titles = {yao_str, sue_str, zia_str, run_str, swim_str}
    assert set(group_titles_dict.keys()) == all_group_titles
    assert set(group_titles_dict.keys()) != {swim_str, run_str}
    assert group_titles_dict.get(swim_str) == {zia_str}
    assert group_titles_dict.get(run_str) == {zia_str, sue_str}
    assert group_titles_dict.get(yao_str) == {yao_str}
    assert group_titles_dict.get(sue_str) == {sue_str}
    assert group_titles_dict.get(zia_str) == {zia_str}


def test_PlanUnit_set_groupunit_SetsAttr_Scenario0():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")
    run_str = ";Run"
    assert not bob_plan._groupunits.get(run_str)

    # WHEN
    bob_plan.set_groupunit(groupunit_shop(run_str))

    # THEN
    assert bob_plan._groupunits.get(run_str)


def test_PlanUnit_set_groupunit_Sets_rope_fund_iota():
    # ESTABLISH
    x_fund_iota = 5
    bob_plan = planunit_shop("Bob", fund_iota=x_fund_iota)
    run_str = ";Run"
    assert not bob_plan._groupunits.get(run_str)

    # WHEN
    bob_plan.set_groupunit(groupunit_shop(run_str))

    # THEN
    assert bob_plan._groupunits.get(run_str).fund_iota == x_fund_iota


def test_PlanUnit_groupunit_exists_ReturnsObj():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")
    run_str = ";Run"
    assert not bob_plan.groupunit_exists(run_str)

    # WHEN
    bob_plan.set_groupunit(groupunit_shop(run_str))

    # THEN
    assert bob_plan.groupunit_exists(run_str)


def test_PlanUnit_get_groupunit_ReturnsObj():
    # ESTABLISH
    bob_plan = planunit_shop("Bob")
    run_str = ";Run"
    x_run_groupunit = groupunit_shop(run_str)
    bob_plan.set_groupunit(x_run_groupunit)
    assert bob_plan._groupunits.get(run_str)

    # WHEN / THEN
    assert bob_plan.get_groupunit(run_str) == groupunit_shop(run_str)


def test_PlanUnit_create_symmetry_groupunit_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)
    zia_str = "Zia"
    yao_credit_vote = 3
    yao_debt_vote = 2
    zia_credit_vote = 4
    zia_debt_vote = 5
    yao_plan.add_acctunit(yao_str, yao_credit_vote, yao_debt_vote)
    yao_plan.add_acctunit(zia_str, zia_credit_vote, zia_debt_vote)

    # WHEN
    xio_str = "Xio"
    xio_groupunit = yao_plan.create_symmetry_groupunit(xio_str)

    # THEN
    assert xio_groupunit.group_title == xio_str
    assert xio_groupunit.membership_exists(yao_str)
    assert xio_groupunit.membership_exists(zia_str)
    assert len(xio_groupunit._memberships) == 2
    yao_groupunit = xio_groupunit.get_membership(yao_str)
    zia_groupunit = xio_groupunit.get_membership(zia_str)
    assert yao_groupunit.credit_vote == yao_credit_vote
    assert zia_groupunit.credit_vote == zia_credit_vote
    assert yao_groupunit.debt_vote == yao_debt_vote
    assert zia_groupunit.debt_vote == zia_debt_vote
