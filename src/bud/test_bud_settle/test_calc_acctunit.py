from src.bud.bud import budunit_shop


def test_create_lobbyboxs_metrics_SetsAttrScenario0():
    # ESTABLISH
    sue_text = "Sue"
    sue_budunit = budunit_shop(sue_text)
    sue_budunit._lobbyboxs = None
    assert sue_budunit._lobbyboxs is None

    # WHEN
    sue_budunit._create_lobbyboxs_metrics()

    # THEN
    assert sue_budunit._lobbyboxs == {}


def test_create_lobbyboxs_metrics_SetsAttrScenario1():
    # ESTABLISH
    sue_text = "Sue"
    sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    sue_budunit.add_acctunit(yao_text)
    yao_acctunit = sue_budunit.get_acct(yao_text)
    yao_acctunit.add_lobbyship(yao_text)
    ohio_text = ",Ohio"
    yao_acctunit.add_lobbyship(ohio_text)
    yao_yao_lobbyship = yao_acctunit.get_lobbyship(yao_text)
    yao_ohio_lobbyship = yao_acctunit.get_lobbyship(ohio_text)
    yao_yao_lobbyship._credor_pool = 66
    yao_yao_lobbyship._debtor_pool = 44
    yao_ohio_lobbyship._credor_pool = 77
    yao_ohio_lobbyship._debtor_pool = 88
    # assert sue_budunit._lobbyboxs == {}

    # WHEN
    sue_budunit._create_lobbyboxs_metrics()

    # THEN
    assert len(sue_budunit._lobbyboxs) == 2
    assert set(sue_budunit._lobbyboxs.keys()) == {yao_text, ohio_text}
    ohio_lobbybox = sue_budunit.get_lobbybox(ohio_text)
    assert ohio_lobbybox._credor_pool == 77
    assert ohio_lobbybox._debtor_pool == 88
    yao_lobbybox = sue_budunit.get_lobbybox(yao_text)
    assert yao_lobbybox._credor_pool == 66
    assert yao_lobbybox._debtor_pool == 44


def test_BudUnit_calc_acctunit_metrics_SetsAttr_scenario0():
    # ESTABLISH
    sue_text = "Sue"
    sue_budunit = budunit_shop(sue_text)
    assert sue_budunit._lobbyboxs == {}

    # WHEN
    sue_budunit._calc_acctunit_metrics()

    # THEN
    assert sue_budunit._lobbyboxs == {}


def test_BudUnit_calc_acctunit_metrics_Clears_lobbys():
    # ESTABLISH
    sue_text = "Sue"
    sue_budunit = budunit_shop(sue_text)
    sue_budunit._lobbys = "yeah"
    sue_budunit._lobbyboxs = "ohio"
    assert sue_budunit._lobbys != {}
    assert sue_budunit._lobbyboxs != {}

    # WHEN
    sue_budunit._calc_acctunit_metrics()

    # THEN
    assert sue_budunit._lobbys != {}
    assert sue_budunit._lobbyboxs == {}


def test_BudUnit_calc_acctunit_metrics_SetsAttr_scenario1():
    # ESTABLISH
    sue_text = "Sue"
    sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    sue_budunit.add_acctunit(yao_text)
    yao_acctunit = sue_budunit.get_acct(yao_text)
    yao_acctunit.add_lobbyship(yao_text)
    assert yao_acctunit._credor_pool == 0
    assert yao_acctunit._debtor_pool == 0
    assert yao_acctunit.get_lobbyship(yao_text)._credor_pool == 0
    assert yao_acctunit.get_lobbyship(yao_text)._debtor_pool == 0
    # assert sue_budunit._lobbyboxs == {}

    # WHEN
    sue_budunit._calc_acctunit_metrics()

    # THEN
    assert yao_acctunit._credor_pool != 0
    assert yao_acctunit._debtor_pool != 0
    assert yao_acctunit._credor_pool == sue_budunit._credor_respect
    assert yao_acctunit._debtor_pool == sue_budunit._debtor_respect
    yao_lobbyship = yao_acctunit.get_lobbyship(yao_text)
    assert yao_lobbyship._credor_pool != 0
    assert yao_lobbyship._debtor_pool != 0
    assert yao_lobbyship._credor_pool == sue_budunit._credor_respect
    assert yao_lobbyship._debtor_pool == sue_budunit._debtor_respect
    assert yao_lobbyship._credor_pool == 1000000000
    assert yao_lobbyship._debtor_pool == 1000000000
    yao_lobbybox = sue_budunit.get_lobbybox(yao_text)
    lobbybox_yao_lobbyship = yao_lobbybox.get_lobbyship(yao_text)
    assert yao_lobbyship == lobbybox_yao_lobbyship


def test_BudUnit_calc_acctunit_metrics_SetsAttr_scenario2():
    # ESTABLISH
    sue_text = "Sue"
    sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    sue_budunit.add_acctunit(yao_text)
    yao_acctunit = sue_budunit.get_acct(yao_text)
    yao_acctunit.add_lobbyship(yao_text, 1, 4)
    ohio_text = ",Ohio"
    yao_acctunit.add_lobbyship(ohio_text, 3, 1)
    assert yao_acctunit._credor_pool == 0
    assert yao_acctunit._debtor_pool == 0
    assert yao_acctunit.get_lobbyship(yao_text)._credor_pool == 0
    assert yao_acctunit.get_lobbyship(yao_text)._debtor_pool == 0

    # WHEN
    sue_budunit._calc_acctunit_metrics()

    # THEN
    assert sue_budunit.get_acct(yao_text)._credor_pool != 0
    assert sue_budunit.get_acct(yao_text)._debtor_pool != 0
    assert yao_acctunit.get_lobbyship(yao_text)._credor_pool != 0
    assert yao_acctunit.get_lobbyship(yao_text)._debtor_pool != 0
    yao_yao_lobbyship = yao_acctunit.get_lobbyship(yao_text)
    assert yao_yao_lobbyship._credor_pool != 0
    assert yao_yao_lobbyship._debtor_pool != 0
    assert yao_yao_lobbyship._credor_pool == sue_budunit._credor_respect * 0.25
    assert yao_yao_lobbyship._debtor_pool == sue_budunit._debtor_respect * 0.8
    assert yao_yao_lobbyship._credor_pool == 250000000
    assert yao_yao_lobbyship._debtor_pool == 800000000
    yao_ohio_lobbyship = yao_acctunit.get_lobbyship(ohio_text)
    assert yao_ohio_lobbyship._credor_pool != 0
    assert yao_ohio_lobbyship._debtor_pool != 0
    assert yao_ohio_lobbyship._credor_pool == sue_budunit._credor_respect * 0.75
    assert yao_ohio_lobbyship._debtor_pool == sue_budunit._debtor_respect * 0.2
    assert yao_ohio_lobbyship._credor_pool == 750000000
    assert yao_ohio_lobbyship._debtor_pool == 200000000
    assert len(sue_budunit._lobbyboxs) == 2
    ohio_lobbybox = sue_budunit.get_lobbybox(ohio_text)
    assert len(ohio_lobbybox._lobbyships) == 1


def test_BudUnit_calc_acctunit_metrics_ResetAcctUnitsAttrs():
    # ESTABLISH
    sue_text = "Sue"
    sue_budunit = budunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    sue_budunit.add_acctunit(yao_text, 55, 55)
    sue_budunit.add_acctunit(zia_text, 55, 55)
    yao_acctunit = sue_budunit.get_acct(yao_text)
    zia_acctunit = sue_budunit.get_acct(zia_text)
    yao_acctunit.add_fund_give_take(0.5, 0.6, 0.1, 0.22)
    zia_acctunit.add_fund_give_take(0.2, 0.1, 0.1, 0.22)
    zia_1 = 0.8
    zia_2 = 0.5
    zia_3 = 200
    zia_4 = 140
    zia_acctunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=zia_1,
        fund_agenda_ratio_take_sum=zia_2,
        bud_acctunit_total_credor_weight=zia_3,
        bud_acctunit_total_debtor_weight=zia_4,
    )
    yao_1 = 0.2
    yao_2 = 0.5
    yao_3 = 204
    yao_4 = 144
    yao_acctunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=yao_1,
        fund_agenda_ratio_take_sum=yao_2,
        bud_acctunit_total_credor_weight=yao_3,
        bud_acctunit_total_debtor_weight=yao_4,
    )
    assert zia_acctunit._fund_agenda_ratio_give == 0.125
    assert zia_acctunit._fund_agenda_ratio_take == 0.44
    assert yao_acctunit._fund_agenda_ratio_give == 0.5
    assert yao_acctunit._fund_agenda_ratio_take == 0.44

    # WHEN
    sue_budunit._calc_acctunit_metrics()

    # THEN
    assert zia_acctunit._fund_agenda_ratio_give == 0
    assert zia_acctunit._fund_agenda_ratio_take == 0
    assert yao_acctunit._fund_agenda_ratio_give == 0
    assert yao_acctunit._fund_agenda_ratio_take == 0
