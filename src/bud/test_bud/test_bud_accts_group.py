from src.bud.group import groupbox_shop
from src.bud.bud import budunit_shop


def test_BudUnit_get_acctunit_group_ids_dict_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    bob_bud = budunit_shop("Bob")
    bob_bud.add_acctunit(yao_text)
    bob_bud.add_acctunit(sue_text)
    bob_bud.add_acctunit(zia_text)
    sue_acctunit = bob_bud.get_acct(sue_text)
    zia_acctunit = bob_bud.get_acct(zia_text)
    run_text = ",Run"
    swim_text = ",Swim"
    sue_acctunit.add_membership(run_text)
    zia_acctunit.add_membership(run_text)
    zia_acctunit.add_membership(swim_text)

    # WHEN
    group_ids_dict = bob_bud.get_acctunit_group_ids_dict()

    # THEN
    print(f"{group_ids_dict=}")
    all_group_ids = {yao_text, sue_text, zia_text, run_text, swim_text}
    assert set(group_ids_dict.keys()) == all_group_ids
    assert set(group_ids_dict.keys()) != {swim_text, run_text}
    assert group_ids_dict.get(swim_text) == {zia_text}
    assert group_ids_dict.get(run_text) == {zia_text, sue_text}
    assert group_ids_dict.get(yao_text) == {yao_text}
    assert group_ids_dict.get(sue_text) == {sue_text}
    assert group_ids_dict.get(zia_text) == {zia_text}


def test_BudUnit_set_groupbox_SetsAttr_Scenario0():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_text = ",Run"
    assert not bob_bud._groupboxs.get(run_text)

    # WHEN
    bob_bud.set_groupbox(groupbox_shop(run_text))

    # THEN
    assert bob_bud._groupboxs.get(run_text)


def test_BudUnit_set_groupbox_Sets_road_fund_coin():
    # ESTABLISH
    x_fund_coin = 5
    bob_bud = budunit_shop("Bob", _fund_coin=x_fund_coin)
    run_text = ",Run"
    assert not bob_bud._groupboxs.get(run_text)

    # WHEN
    bob_bud.set_groupbox(groupbox_shop(run_text))

    # THEN
    assert bob_bud._groupboxs.get(run_text)._fund_coin == x_fund_coin


def test_BudUnit_groupbox_exists_ReturnsObj():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_text = ",Run"
    assert not bob_bud.groupbox_exists(run_text)

    # WHEN
    bob_bud.set_groupbox(groupbox_shop(run_text))

    # THEN
    assert bob_bud.groupbox_exists(run_text)


def test_BudUnit_get_groupbox_ReturnsObj():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    run_text = ",Run"
    x_run_groupbox = groupbox_shop(run_text)
    bob_bud.set_groupbox(x_run_groupbox)
    assert bob_bud._groupboxs.get(run_text)

    # WHEN / THEN
    assert bob_bud.get_groupbox(run_text) == groupbox_shop(run_text)


def test_BudUnit_create_symmetry_groupbox_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    yao_bud = budunit_shop(yao_text)
    zia_text = "Zia"
    yao_credit_score = 3
    yao_debtit_score = 2
    zia_credit_score = 4
    zia_debtit_score = 5
    yao_bud.add_acctunit(yao_text, yao_credit_score, yao_debtit_score)
    yao_bud.add_acctunit(zia_text, zia_credit_score, zia_debtit_score)

    # WHEN
    xio_text = "Xio"
    xio_groupbox = yao_bud.create_symmetry_groupbox(xio_text)

    # THEN
    assert xio_groupbox.group_id == xio_text
    assert xio_groupbox.membership_exists(yao_text)
    assert xio_groupbox.membership_exists(zia_text)
    assert len(xio_groupbox._memberships) == 2
    yao_groupbox = xio_groupbox.get_membership(yao_text)
    zia_groupbox = xio_groupbox.get_membership(zia_text)
    assert yao_groupbox.credit_score == yao_credit_score
    assert zia_groupbox.credit_score == zia_credit_score
    assert yao_groupbox.debtit_score == yao_debtit_score
    assert zia_groupbox.debtit_score == zia_debtit_score
