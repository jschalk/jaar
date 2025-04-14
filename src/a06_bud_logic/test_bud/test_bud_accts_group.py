from src.a03_group_logic.group import groupunit_shop
from src.a06_bud_logic.bud import budunit_shop


def test_BudUnit_get_acctunit_group_labels_dict_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    sue_str = "Sue"
    zia_str = "Zia"
    bob_bud = budunit_shop("Bob")
    bob_bud.add_acctunit(yao_str)
    bob_bud.add_acctunit(sue_str)
    bob_bud.add_acctunit(zia_str)
    sue_acctunit = bob_bud.get_acct(sue_str)
    zia_acctunit = bob_bud.get_acct(zia_str)
    run_str = ";Run"
    swim_str = ";Swim"
    sue_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(run_str)
    zia_acctunit.add_membership(swim_str)

    # WHEN
    group_labels_dict = bob_bud.get_acctunit_group_labels_dict()

    # THEN
    print(f"{group_labels_dict=}")
    all_group_labels = {yao_str, sue_str, zia_str, run_str, swim_str}
    assert set(group_labels_dict.keys()) == all_group_labels
    assert set(group_labels_dict.keys()) != {swim_str, run_str}
    assert group_labels_dict.get(swim_str) == {zia_str}
    assert group_labels_dict.get(run_str) == {zia_str, sue_str}
    assert group_labels_dict.get(yao_str) == {yao_str}
    assert group_labels_dict.get(sue_str) == {sue_str}
    assert group_labels_dict.get(zia_str) == {zia_str}


def test_BudUnit_set_groupunit_SetsAttr_Scenario0():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_str = ";Run"
    assert not bob_bud._groupunits.get(run_str)

    # WHEN
    bob_bud.set_groupunit(groupunit_shop(run_str))

    # THEN
    assert bob_bud._groupunits.get(run_str)


def test_BudUnit_set_groupunit_Sets_road_fund_coin():
    # ESTABLISH
    x_fund_coin = 5
    bob_bud = budunit_shop("Bob", fund_coin=x_fund_coin)
    run_str = ";Run"
    assert not bob_bud._groupunits.get(run_str)

    # WHEN
    bob_bud.set_groupunit(groupunit_shop(run_str))

    # THEN
    assert bob_bud._groupunits.get(run_str).fund_coin == x_fund_coin


def test_BudUnit_groupunit_exists_ReturnsObj():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_str = ";Run"
    assert not bob_bud.groupunit_exists(run_str)

    # WHEN
    bob_bud.set_groupunit(groupunit_shop(run_str))

    # THEN
    assert bob_bud.groupunit_exists(run_str)


def test_BudUnit_get_groupunit_ReturnsObj():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_str = ";Run"
    x_run_groupunit = groupunit_shop(run_str)
    bob_bud.set_groupunit(x_run_groupunit)
    assert bob_bud._groupunits.get(run_str)

    # WHEN / THEN
    assert bob_bud.get_groupunit(run_str) == groupunit_shop(run_str)


def test_BudUnit_create_symmetry_groupunit_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    zia_str = "Zia"
    yao_credit_vote = 3
    yao_debtit_vote = 2
    zia_credit_vote = 4
    zia_debtit_vote = 5
    yao_bud.add_acctunit(yao_str, yao_credit_vote, yao_debtit_vote)
    yao_bud.add_acctunit(zia_str, zia_credit_vote, zia_debtit_vote)

    # WHEN
    xio_str = "Xio"
    xio_groupunit = yao_bud.create_symmetry_groupunit(xio_str)

    # THEN
    assert xio_groupunit.group_label == xio_str
    assert xio_groupunit.membership_exists(yao_str)
    assert xio_groupunit.membership_exists(zia_str)
    assert len(xio_groupunit._memberships) == 2
    yao_groupunit = xio_groupunit.get_membership(yao_str)
    zia_groupunit = xio_groupunit.get_membership(zia_str)
    assert yao_groupunit.credit_vote == yao_credit_vote
    assert zia_groupunit.credit_vote == zia_credit_vote
    assert yao_groupunit.debtit_vote == yao_debtit_vote
    assert zia_groupunit.debtit_vote == zia_debtit_vote
