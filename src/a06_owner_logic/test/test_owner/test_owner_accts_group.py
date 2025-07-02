from src.a03_group_logic.group import groupunit_shop
from src.a06_owner_logic.owner import ownerunit_shop


def test_OwnerUnit_get_acctunit_group_titles_dict_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    zia_str = "Zia"
    bob_owner = ownerunit_shop("Bob")
    bob_owner.add_acctunit(yao_str)
    bob_owner.add_acctunit(sue_str)
    bob_owner.add_acctunit(zia_str)
    sue_acctunit = bob_owner.get_acct(sue_str)
    zia_acctunit = bob_owner.get_acct(zia_str)
    run_str = ";Run"
    swim_str = ";Swim"
    sue_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(swim_str)

    # WHEN
    group_titles_dict = bob_owner.get_acctunit_group_titles_dict()

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


def test_OwnerUnit_set_groupunit_SetsAttr_Scenario0():
    # ESTABLISH
    bob_owner = ownerunit_shop("Bob")
    run_str = ";Run"
    assert not bob_owner._groupunits.get(run_str)

    # WHEN
    bob_owner.set_groupunit(groupunit_shop(run_str))

    # THEN
    assert bob_owner._groupunits.get(run_str)


def test_OwnerUnit_set_groupunit_Sets_rope_fund_iota():
    # ESTABLISH
    x_fund_iota = 5
    bob_owner = ownerunit_shop("Bob", fund_iota=x_fund_iota)
    run_str = ";Run"
    assert not bob_owner._groupunits.get(run_str)

    # WHEN
    bob_owner.set_groupunit(groupunit_shop(run_str))

    # THEN
    assert bob_owner._groupunits.get(run_str).fund_iota == x_fund_iota


def test_OwnerUnit_groupunit_exists_ReturnsObj():
    # ESTABLISH
    bob_owner = ownerunit_shop("Bob")
    run_str = ";Run"
    assert not bob_owner.groupunit_exists(run_str)

    # WHEN
    bob_owner.set_groupunit(groupunit_shop(run_str))

    # THEN
    assert bob_owner.groupunit_exists(run_str)


def test_OwnerUnit_get_groupunit_ReturnsObj():
    # ESTABLISH
    bob_owner = ownerunit_shop("Bob")
    run_str = ";Run"
    x_run_groupunit = groupunit_shop(run_str)
    bob_owner.set_groupunit(x_run_groupunit)
    assert bob_owner._groupunits.get(run_str)

    # WHEN / THEN
    assert bob_owner.get_groupunit(run_str) == groupunit_shop(run_str)


def test_OwnerUnit_create_symmetry_groupunit_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_owner = ownerunit_shop(yao_str)
    zia_str = "Zia"
    yao_group_cred_points = 3
    yao_group_debt_points = 2
    zia_group_cred_points = 4
    zia_group_debt_points = 5
    yao_owner.add_acctunit(yao_str, yao_group_cred_points, yao_group_debt_points)
    yao_owner.add_acctunit(zia_str, zia_group_cred_points, zia_group_debt_points)

    # WHEN
    xio_str = "Xio"
    xio_groupunit = yao_owner.create_symmetry_groupunit(xio_str)

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
