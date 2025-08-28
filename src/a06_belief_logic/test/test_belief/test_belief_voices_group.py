from src.a03_group_logic.group import groupunit_shop
from src.a06_belief_logic.belief_main import beliefunit_shop


def test_BeliefUnit_get_voiceunit_group_titles_dict_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    zia_str = "Zia"
    bob_belief = beliefunit_shop("Bob")
    bob_belief.add_voiceunit(yao_str)
    bob_belief.add_voiceunit(sue_str)
    bob_belief.add_voiceunit(zia_str)
    sue_voiceunit = bob_belief.get_voice(sue_str)
    zia_voiceunit = bob_belief.get_voice(zia_str)
    run_str = ";Run"
    swim_str = ";Swim"
    sue_voiceunit.add_membership(run_str)
    zia_voiceunit.add_membership(run_str)
    zia_voiceunit.add_membership(swim_str)

    # WHEN
    group_titles_dict = bob_belief.get_voiceunit_group_titles_dict()

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


def test_BeliefUnit_set_groupunit_SetsAttr_Scenario0():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob")
    run_str = ";Run"
    assert not bob_belief.groupunits.get(run_str)

    # WHEN
    bob_belief.set_groupunit(groupunit_shop(run_str))

    # THEN
    assert bob_belief.groupunits.get(run_str)


def test_BeliefUnit_set_groupunit_Sets_rope_fund_iota():
    # ESTABLISH
    x_fund_iota = 5
    bob_belief = beliefunit_shop("Bob", fund_iota=x_fund_iota)
    run_str = ";Run"
    assert not bob_belief.groupunits.get(run_str)

    # WHEN
    bob_belief.set_groupunit(groupunit_shop(run_str))

    # THEN
    assert bob_belief.groupunits.get(run_str).fund_iota == x_fund_iota


def test_BeliefUnit_groupunit_exists_ReturnsObj():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob")
    run_str = ";Run"
    assert not bob_belief.groupunit_exists(run_str)

    # WHEN
    bob_belief.set_groupunit(groupunit_shop(run_str))

    # THEN
    assert bob_belief.groupunit_exists(run_str)


def test_BeliefUnit_get_groupunit_ReturnsObj():
    # ESTABLISH
    bob_belief = beliefunit_shop("Bob")
    run_str = ";Run"
    x_run_groupunit = groupunit_shop(run_str)
    bob_belief.set_groupunit(x_run_groupunit)
    assert bob_belief.groupunits.get(run_str)

    # WHEN / THEN
    assert bob_belief.get_groupunit(run_str) == groupunit_shop(run_str)


def test_BeliefUnit_create_symmetry_groupunit_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)
    zia_str = "Zia"
    yao_group_cred_points = 3
    yao_group_debt_points = 2
    zia_group_cred_points = 4
    zia_group_debt_points = 5
    yao_belief.add_voiceunit(yao_str, yao_group_cred_points, yao_group_debt_points)
    yao_belief.add_voiceunit(zia_str, zia_group_cred_points, zia_group_debt_points)

    # WHEN
    xio_str = "Xio"
    xio_groupunit = yao_belief.create_symmetry_groupunit(xio_str)

    # THEN
    assert xio_groupunit.group_title == xio_str
    assert xio_groupunit.membership_exists(yao_str)
    assert xio_groupunit.membership_exists(zia_str)
    assert len(xio_groupunit._memberships) == 2
    yao_groupunit = xio_groupunit.get_membership(yao_str)
    zia_groupunit = xio_groupunit.get_membership(zia_str)
    assert yao_groupunit.group_cred_points == yao_group_cred_points
    assert zia_groupunit.group_cred_points == zia_group_cred_points
    assert yao_groupunit.group_debt_points == yao_group_debt_points
    assert zia_groupunit.group_debt_points == zia_group_debt_points
