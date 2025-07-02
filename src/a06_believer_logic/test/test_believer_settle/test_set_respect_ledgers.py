from src.a06_believer_logic.believer import believerunit_shop


def test_create_groupunits_metrics_SetsAttrScenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_believerunit = believerunit_shop(sue_str)
    sue_believerunit._groupunits = None
    assert sue_believerunit._groupunits is None

    # WHEN
    sue_believerunit._create_groupunits_metrics()

    # THEN
    assert sue_believerunit._groupunits == {}


def test_create_groupunits_metrics_SetsAttrScenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    sue_believerunit.add_acctunit(yao_str)
    yao_acctunit = sue_believerunit.get_acct(yao_str)
    yao_acctunit.add_membership(yao_str)
    ohio_str = ";Ohio"
    yao_acctunit.add_membership(ohio_str)
    yao_yao_membership = yao_acctunit.get_membership(yao_str)
    yao_ohio_membership = yao_acctunit.get_membership(ohio_str)
    yao_yao_membership._credor_pool = 66
    yao_yao_membership._debtor_pool = 44
    yao_ohio_membership._credor_pool = 77
    yao_ohio_membership._debtor_pool = 88
    # assert sue_believerunit._groupunits == {}

    # WHEN
    sue_believerunit._create_groupunits_metrics()

    # THEN
    assert len(sue_believerunit._groupunits) == 2
    assert set(sue_believerunit._groupunits.keys()) == {yao_str, ohio_str}
    ohio_groupunit = sue_believerunit.get_groupunit(ohio_str)
    assert ohio_groupunit._credor_pool == 77
    assert ohio_groupunit._debtor_pool == 88
    yao_groupunit = sue_believerunit.get_groupunit(yao_str)
    assert yao_groupunit._credor_pool == 66
    assert yao_groupunit._debtor_pool == 44


def test_BelieverUnit_set_acctunit_groupunit_respect_ledgers_SetsAttr_scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_believerunit = believerunit_shop(sue_str)
    assert sue_believerunit._groupunits == {}

    # WHEN
    sue_believerunit._set_acctunit_groupunit_respect_ledgers()

    # THEN
    assert sue_believerunit._groupunits == {}


def test_BelieverUnit_set_acctunit_groupunit_respect_ledgers_Clears_groups():
    # ESTABLISH
    sue_str = "Sue"
    sue_believerunit = believerunit_shop(sue_str)
    sue_believerunit._groups = "yeah"
    sue_believerunit._groupunits = "ohio"
    assert sue_believerunit._groups != {}
    assert sue_believerunit._groupunits != {}

    # WHEN
    sue_believerunit._set_acctunit_groupunit_respect_ledgers()

    # THEN
    assert sue_believerunit._groups != {}
    assert sue_believerunit._groupunits == {}


def test_BelieverUnit_set_acctunit_groupunit_respect_ledgers_SetsAttr_scenario1():
    # ESTABLISH
    sue_str = "Sue"
    sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    sue_believerunit.add_acctunit(yao_str)
    yao_acctunit = sue_believerunit.get_acct(yao_str)
    yao_acctunit.add_membership(yao_str)
    assert yao_acctunit._credor_pool == 0
    assert yao_acctunit._debtor_pool == 0
    assert yao_acctunit.get_membership(yao_str)._credor_pool == 0
    assert yao_acctunit.get_membership(yao_str)._debtor_pool == 0
    # assert sue_believerunit._groupunits == {}

    # WHEN
    sue_believerunit._set_acctunit_groupunit_respect_ledgers()

    # THEN
    assert yao_acctunit._credor_pool != 0
    assert yao_acctunit._debtor_pool != 0
    assert yao_acctunit._credor_pool == sue_believerunit.credor_respect
    assert yao_acctunit._debtor_pool == sue_believerunit.debtor_respect
    yao_membership = yao_acctunit.get_membership(yao_str)
    assert yao_membership._credor_pool != 0
    assert yao_membership._debtor_pool != 0
    assert yao_membership._credor_pool == sue_believerunit.credor_respect
    assert yao_membership._debtor_pool == sue_believerunit.debtor_respect
    assert yao_membership._credor_pool == 1000000000
    assert yao_membership._debtor_pool == 1000000000
    yao_groupunit = sue_believerunit.get_groupunit(yao_str)
    groupunit_yao_membership = yao_groupunit.get_membership(yao_str)
    assert yao_membership == groupunit_yao_membership


def test_BelieverUnit_set_acctunit_groupunit_respect_ledgers_SetsAttr_scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    sue_believerunit.add_acctunit(yao_str)
    yao_acctunit = sue_believerunit.get_acct(yao_str)
    yao_acctunit.add_membership(yao_str, 1, 4)
    ohio_str = ";Ohio"
    yao_acctunit.add_membership(ohio_str, 3, 1)
    assert yao_acctunit._credor_pool == 0
    assert yao_acctunit._debtor_pool == 0
    assert yao_acctunit.get_membership(yao_str)._credor_pool == 0
    assert yao_acctunit.get_membership(yao_str)._debtor_pool == 0

    # WHEN
    sue_believerunit._set_acctunit_groupunit_respect_ledgers()

    # THEN
    assert sue_believerunit.get_acct(yao_str)._credor_pool != 0
    assert sue_believerunit.get_acct(yao_str)._debtor_pool != 0
    assert yao_acctunit.get_membership(yao_str)._credor_pool != 0
    assert yao_acctunit.get_membership(yao_str)._debtor_pool != 0
    yao_yao_membership = yao_acctunit.get_membership(yao_str)
    assert yao_yao_membership._credor_pool != 0
    assert yao_yao_membership._debtor_pool != 0
    assert yao_yao_membership._credor_pool == sue_believerunit.credor_respect * 0.25
    assert yao_yao_membership._debtor_pool == sue_believerunit.debtor_respect * 0.8
    assert yao_yao_membership._credor_pool == 250000000
    assert yao_yao_membership._debtor_pool == 800000000
    yao_ohio_membership = yao_acctunit.get_membership(ohio_str)
    assert yao_ohio_membership._credor_pool != 0
    assert yao_ohio_membership._debtor_pool != 0
    assert yao_ohio_membership._credor_pool == sue_believerunit.credor_respect * 0.75
    assert yao_ohio_membership._debtor_pool == sue_believerunit.debtor_respect * 0.2
    assert yao_ohio_membership._credor_pool == 750000000
    assert yao_ohio_membership._debtor_pool == 200000000
    assert len(sue_believerunit._groupunits) == 2
    ohio_groupunit = sue_believerunit.get_groupunit(ohio_str)
    assert len(ohio_groupunit._memberships) == 1


def test_BelieverUnit_set_acctunit_groupunit_respect_ledgers_ResetAcctUnitsAttrs():
    # ESTABLISH
    sue_str = "Sue"
    sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    sue_believerunit.add_acctunit(yao_str, 55, 55)
    sue_believerunit.add_acctunit(zia_str, 55, 55)
    yao_acctunit = sue_believerunit.get_acct(yao_str)
    zia_acctunit = sue_believerunit.get_acct(zia_str)
    yao_acctunit.add_fund_give_take(0.5, 0.6, 0.1, 0.22)
    zia_acctunit.add_fund_give_take(0.2, 0.1, 0.1, 0.22)
    zia_1 = 0.8
    zia_2 = 0.5
    zia_3 = 200
    zia_4 = 140
    zia_acctunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=zia_1,
        fund_agenda_ratio_take_sum=zia_2,
        acctunits_acct_cred_points_sum=zia_3,
        acctunits_acct_debt_points_sum=zia_4,
    )
    yao_1 = 0.2
    yao_2 = 0.5
    yao_3 = 204
    yao_4 = 144
    yao_acctunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=yao_1,
        fund_agenda_ratio_take_sum=yao_2,
        acctunits_acct_cred_points_sum=yao_3,
        acctunits_acct_debt_points_sum=yao_4,
    )
    assert zia_acctunit._fund_agenda_ratio_give == 0.125
    assert zia_acctunit._fund_agenda_ratio_take == 0.44
    assert yao_acctunit._fund_agenda_ratio_give == 0.5
    assert yao_acctunit._fund_agenda_ratio_take == 0.44

    # WHEN
    sue_believerunit._set_acctunit_groupunit_respect_ledgers()

    # THEN
    assert zia_acctunit._fund_agenda_ratio_give == 0
    assert zia_acctunit._fund_agenda_ratio_take == 0
    assert yao_acctunit._fund_agenda_ratio_give == 0
    assert yao_acctunit._fund_agenda_ratio_take == 0
