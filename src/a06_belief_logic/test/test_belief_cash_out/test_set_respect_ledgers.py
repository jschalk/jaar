from src.a06_belief_logic.belief_main import beliefunit_shop


def test_create_groupunits_metrics_SetsAttrScenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefunit = beliefunit_shop(sue_str)
    sue_beliefunit.groupunits = None
    assert sue_beliefunit.groupunits is None

    # WHEN
    sue_beliefunit._create_groupunits_metrics()

    # THEN
    assert sue_beliefunit.groupunits == {}


def test_create_groupunits_metrics_SetsAttrScenario1():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    sue_beliefunit.add_voiceunit(yao_str)
    yao_voiceunit = sue_beliefunit.get_voice(yao_str)
    yao_voiceunit.add_membership(yao_str)
    ohio_str = ";Ohio"
    yao_voiceunit.add_membership(ohio_str)
    yao_yao_membership = yao_voiceunit.get_membership(yao_str)
    yao_ohio_membership = yao_voiceunit.get_membership(ohio_str)
    yao_yao_membership.credor_pool = 66
    yao_yao_membership.debtor_pool = 44
    yao_ohio_membership.credor_pool = 77
    yao_ohio_membership.debtor_pool = 88
    # assert sue_beliefunit.groupunits == {}

    # WHEN
    sue_beliefunit._create_groupunits_metrics()

    # THEN
    assert len(sue_beliefunit.groupunits) == 2
    assert set(sue_beliefunit.groupunits.keys()) == {yao_str, ohio_str}
    ohio_groupunit = sue_beliefunit.get_groupunit(ohio_str)
    assert ohio_groupunit.credor_pool == 77
    assert ohio_groupunit.debtor_pool == 88
    yao_groupunit = sue_beliefunit.get_groupunit(yao_str)
    assert yao_groupunit.credor_pool == 66
    assert yao_groupunit.debtor_pool == 44


def test_BeliefUnit_set_voiceunit_groupunit_respect_ledgers_SetsAttr_scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefunit = beliefunit_shop(sue_str)
    assert sue_beliefunit.groupunits == {}

    # WHEN
    sue_beliefunit._set_voiceunit_groupunit_respect_ledgers()

    # THEN
    assert sue_beliefunit.groupunits == {}


def test_BeliefUnit_set_voiceunit_groupunit_respect_ledgers_Clears_groupunits():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefunit = beliefunit_shop(sue_str)
    sue_beliefunit.groupunits = "ohio"
    assert sue_beliefunit.groupunits != {}

    # WHEN
    sue_beliefunit._set_voiceunit_groupunit_respect_ledgers()

    # THEN
    assert sue_beliefunit.groupunits == {}


def test_BeliefUnit_set_voiceunit_groupunit_respect_ledgers_SetsAttr_scenario1():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    sue_beliefunit.add_voiceunit(yao_str)
    yao_voiceunit = sue_beliefunit.get_voice(yao_str)
    yao_voiceunit.add_membership(yao_str)
    assert yao_voiceunit.credor_pool == 0
    assert yao_voiceunit.debtor_pool == 0
    assert yao_voiceunit.get_membership(yao_str).credor_pool == 0
    assert yao_voiceunit.get_membership(yao_str).debtor_pool == 0
    # assert sue_beliefunit.groupunits == {}

    # WHEN
    sue_beliefunit._set_voiceunit_groupunit_respect_ledgers()

    # THEN
    assert yao_voiceunit.credor_pool != 0
    assert yao_voiceunit.debtor_pool != 0
    assert yao_voiceunit.credor_pool == sue_beliefunit.credor_respect
    assert yao_voiceunit.debtor_pool == sue_beliefunit.debtor_respect
    yao_membership = yao_voiceunit.get_membership(yao_str)
    assert yao_membership.credor_pool != 0
    assert yao_membership.debtor_pool != 0
    assert yao_membership.credor_pool == sue_beliefunit.credor_respect
    assert yao_membership.debtor_pool == sue_beliefunit.debtor_respect
    assert yao_membership.credor_pool == 1000000000
    assert yao_membership.debtor_pool == 1000000000
    yao_groupunit = sue_beliefunit.get_groupunit(yao_str)
    groupunit_yao_membership = yao_groupunit.get_membership(yao_str)
    assert yao_membership == groupunit_yao_membership


def test_BeliefUnit_set_voiceunit_groupunit_respect_ledgers_SetsAttr_scenario2():
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    sue_beliefunit.add_voiceunit(yao_str)
    yao_voiceunit = sue_beliefunit.get_voice(yao_str)
    yao_voiceunit.add_membership(yao_str, 1, 4)
    ohio_str = ";Ohio"
    yao_voiceunit.add_membership(ohio_str, 3, 1)
    assert yao_voiceunit.credor_pool == 0
    assert yao_voiceunit.debtor_pool == 0
    assert yao_voiceunit.get_membership(yao_str).credor_pool == 0
    assert yao_voiceunit.get_membership(yao_str).debtor_pool == 0

    # WHEN
    sue_beliefunit._set_voiceunit_groupunit_respect_ledgers()

    # THEN
    assert sue_beliefunit.get_voice(yao_str).credor_pool != 0
    assert sue_beliefunit.get_voice(yao_str).debtor_pool != 0
    assert yao_voiceunit.get_membership(yao_str).credor_pool != 0
    assert yao_voiceunit.get_membership(yao_str).debtor_pool != 0
    yao_yao_membership = yao_voiceunit.get_membership(yao_str)
    assert yao_yao_membership.credor_pool != 0
    assert yao_yao_membership.debtor_pool != 0
    assert yao_yao_membership.credor_pool == sue_beliefunit.credor_respect * 0.25
    assert yao_yao_membership.debtor_pool == sue_beliefunit.debtor_respect * 0.8
    assert yao_yao_membership.credor_pool == 250000000
    assert yao_yao_membership.debtor_pool == 800000000
    yao_ohio_membership = yao_voiceunit.get_membership(ohio_str)
    assert yao_ohio_membership.credor_pool != 0
    assert yao_ohio_membership.debtor_pool != 0
    assert yao_ohio_membership.credor_pool == sue_beliefunit.credor_respect * 0.75
    assert yao_ohio_membership.debtor_pool == sue_beliefunit.debtor_respect * 0.2
    assert yao_ohio_membership.credor_pool == 750000000
    assert yao_ohio_membership.debtor_pool == 200000000
    assert len(sue_beliefunit.groupunits) == 2
    ohio_groupunit = sue_beliefunit.get_groupunit(ohio_str)
    assert len(ohio_groupunit._memberships) == 1


def test_BeliefUnit_set_voiceunit_groupunit_respect_ledgers_ResetVoiceUnitsAttrs():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_str = "Sue"
    sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    sue_beliefunit.add_voiceunit(yao_str, 55, 55)
    sue_beliefunit.add_voiceunit(zia_str, 55, 55)
    yao_voiceunit = sue_beliefunit.get_voice(yao_str)
    zia_voiceunit = sue_beliefunit.get_voice(zia_str)
    yao_voiceunit.add_fund_give_take(0.5, 0.6, 0.1, 0.22)
    zia_voiceunit.add_fund_give_take(0.2, 0.1, 0.1, 0.22)
    zia_1 = 0.8
    zia_2 = 0.5
    zia_3 = 200
    zia_4 = 140
    zia_voiceunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=zia_1,
        fund_agenda_ratio_take_sum=zia_2,
        voiceunits_voice_cred_points_sum=zia_3,
        voiceunits_voice_debt_points_sum=zia_4,
    )
    yao_1 = 0.2
    yao_2 = 0.5
    yao_3 = 204
    yao_4 = 144
    yao_voiceunit.set_fund_agenda_ratio_give_take(
        fund_agenda_ratio_give_sum=yao_1,
        fund_agenda_ratio_take_sum=yao_2,
        voiceunits_voice_cred_points_sum=yao_3,
        voiceunits_voice_debt_points_sum=yao_4,
    )
    assert zia_voiceunit.fund_agenda_ratio_give == 0.125
    assert zia_voiceunit.fund_agenda_ratio_take == 0.44
    assert yao_voiceunit.fund_agenda_ratio_give == 0.5
    assert yao_voiceunit.fund_agenda_ratio_take == 0.44

    # WHEN
    sue_beliefunit._set_voiceunit_groupunit_respect_ledgers()

    # THEN
    assert zia_voiceunit.fund_agenda_ratio_give == 0
    assert zia_voiceunit.fund_agenda_ratio_take == 0
    assert yao_voiceunit.fund_agenda_ratio_give == 0
    assert yao_voiceunit.fund_agenda_ratio_take == 0
