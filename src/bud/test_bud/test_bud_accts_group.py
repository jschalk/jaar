from src.bud.group import groupbox_shop
from src.bud.bud import budunit_shop


def test_BudUnit_get_acctunit_group_ids_dict_ReturnsObj():
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
    group_ids_dict = bob_bud.get_acctunit_group_ids_dict()

    # THEN
    print(f"{group_ids_dict=}")
    all_group_ids = {yao_str, sue_str, zia_str, run_str, swim_str}
    assert set(group_ids_dict.keys()) == all_group_ids
    assert set(group_ids_dict.keys()) != {swim_str, run_str}
    assert group_ids_dict.get(swim_str) == {zia_str}
    assert group_ids_dict.get(run_str) == {zia_str, sue_str}
    assert group_ids_dict.get(yao_str) == {yao_str}
    assert group_ids_dict.get(sue_str) == {sue_str}
    assert group_ids_dict.get(zia_str) == {zia_str}


def test_BudUnit_set_groupbox_SetsAttr_Scenario0():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_str = ";Run"
    assert not bob_bud._groupboxs.get(run_str)

    # WHEN
    bob_bud.set_groupbox(groupbox_shop(run_str))

    # THEN
    assert bob_bud._groupboxs.get(run_str)


def test_BudUnit_set_groupbox_Sets_road_fund_coin():
    # ESTABLISH
    x_fund_coin = 5
    bob_bud = budunit_shop("Bob", _fund_coin=x_fund_coin)
    run_str = ";Run"
    assert not bob_bud._groupboxs.get(run_str)

    # WHEN
    bob_bud.set_groupbox(groupbox_shop(run_str))

    # THEN
    assert bob_bud._groupboxs.get(run_str)._fund_coin == x_fund_coin


def test_BudUnit_groupbox_exists_ReturnsObj():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_str = ";Run"
    assert not bob_bud.groupbox_exists(run_str)

    # WHEN
    bob_bud.set_groupbox(groupbox_shop(run_str))

    # THEN
    assert bob_bud.groupbox_exists(run_str)


def test_BudUnit_get_groupbox_ReturnsObj():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_str = ";Run"
    x_run_groupbox = groupbox_shop(run_str)
    bob_bud.set_groupbox(x_run_groupbox)
    assert bob_bud._groupboxs.get(run_str)

    # WHEN / THEN
    assert bob_bud.get_groupbox(run_str) == groupbox_shop(run_str)


def test_BudUnit_create_symmetry_groupbox_ReturnsObj():
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
    xio_groupbox = yao_bud.create_symmetry_groupbox(xio_str)

    # THEN
    assert xio_groupbox.group_id == xio_str
    assert xio_groupbox.membership_exists(yao_str)
    assert xio_groupbox.membership_exists(zia_str)
    assert len(xio_groupbox._memberships) == 2
    yao_groupbox = xio_groupbox.get_membership(yao_str)
    zia_groupbox = xio_groupbox.get_membership(zia_str)
    assert yao_groupbox.credit_vote == yao_credit_vote
    assert zia_groupbox.credit_vote == zia_credit_vote
    assert yao_groupbox.debtit_vote == yao_debtit_vote
    assert zia_groupbox.debtit_vote == zia_debtit_vote
