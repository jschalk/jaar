from src._world.world import worldunit_shop


def test_create_beliefstorys_metrics_SetsAttrScenario0():
    # GIVEN
    sue_text = "Sue"
    sue_worldunit = worldunit_shop(sue_text)
    sue_worldunit._beliefstorys = None
    assert sue_worldunit._beliefstorys is None

    # WHEN
    sue_worldunit._create_beliefstorys_metrics()

    # THEN
    assert sue_worldunit._beliefstorys == {}


def test_create_beliefstorys_metrics_SetsAttrScenario1():
    # GIVEN
    sue_text = "Sue"
    sue_worldunit = worldunit_shop(sue_text)
    yao_text = "Yao"
    sue_worldunit.add_charunit(yao_text)
    yao_charunit = sue_worldunit.get_char(yao_text)
    yao_charunit.add_belieflink(yao_text)
    ohio_text = ",Ohio"
    yao_charunit.add_belieflink(ohio_text)
    yao_yao_belieflink = yao_charunit.get_belieflink(yao_text)
    yao_ohio_belieflink = yao_charunit.get_belieflink(ohio_text)
    yao_yao_belieflink._credor_pool = 66
    yao_yao_belieflink._debtor_pool = 44
    yao_ohio_belieflink._credor_pool = 77
    yao_ohio_belieflink._debtor_pool = 88
    # assert sue_worldunit._beliefstorys == {}

    # WHEN
    sue_worldunit._create_beliefstorys_metrics()

    # THEN
    assert len(sue_worldunit._beliefstorys) == 2
    assert set(sue_worldunit._beliefstorys.keys()) == {yao_text, ohio_text}
    ohio_beliefstory = sue_worldunit.get_beliefstory(ohio_text)
    assert ohio_beliefstory._credor_pool == 77
    assert ohio_beliefstory._debtor_pool == 88
    yao_beliefstory = sue_worldunit.get_beliefstory(yao_text)
    assert yao_beliefstory._credor_pool == 66
    assert yao_beliefstory._debtor_pool == 44


def test_WorldUnit_calc_charunit_metrics_SetsAttr_scenario0():
    # GIVEN
    sue_text = "Sue"
    sue_worldunit = worldunit_shop(sue_text)
    assert sue_worldunit._beliefstorys == {}

    # WHEN
    sue_worldunit._calc_charunit_metrics()

    # THEN
    assert sue_worldunit._beliefstorys == {}


def test_WorldUnit_calc_charunit_metrics_Clears_beliefs():
    # GIVEN
    sue_text = "Sue"
    sue_worldunit = worldunit_shop(sue_text)
    sue_worldunit._beliefs = "yeah"
    sue_worldunit._beliefstorys = "ohio"
    assert sue_worldunit._beliefs != {}
    assert sue_worldunit._beliefstorys != {}

    # WHEN
    sue_worldunit._calc_charunit_metrics()

    # THEN
    assert sue_worldunit._beliefs != {}
    assert sue_worldunit._beliefstorys == {}


def test_WorldUnit_calc_charunit_metrics_SetsAttr_scenario1():
    # GIVEN
    sue_text = "Sue"
    sue_worldunit = worldunit_shop(sue_text)
    yao_text = "Yao"
    sue_worldunit.add_charunit(yao_text)
    yao_charunit = sue_worldunit.get_char(yao_text)
    yao_charunit.add_belieflink(yao_text)
    assert yao_charunit._credor_pool == 0
    assert yao_charunit._debtor_pool == 0
    assert yao_charunit.get_belieflink(yao_text)._credor_pool == 0
    assert yao_charunit.get_belieflink(yao_text)._debtor_pool == 0
    # assert sue_worldunit._beliefstorys == {}

    # WHEN
    sue_worldunit._calc_charunit_metrics()

    # THEN
    assert yao_charunit._credor_pool != 0
    assert yao_charunit._debtor_pool != 0
    assert yao_charunit._credor_pool == sue_worldunit._credor_respect
    assert yao_charunit._debtor_pool == sue_worldunit._debtor_respect
    yao_belieflink = yao_charunit.get_belieflink(yao_text)
    assert yao_belieflink._credor_pool != 0
    assert yao_belieflink._debtor_pool != 0
    assert yao_belieflink._credor_pool == sue_worldunit._credor_respect
    assert yao_belieflink._debtor_pool == sue_worldunit._debtor_respect
    assert yao_belieflink._credor_pool == 1000000000
    assert yao_belieflink._debtor_pool == 1000000000
    yao_beliefstory = sue_worldunit.get_beliefstory(yao_text)
    beliefstory_yao_belieflink = yao_beliefstory.get_belieflink(yao_text)
    assert yao_belieflink == beliefstory_yao_belieflink


def test_WorldUnit_calc_charunit_metrics_SetsAttr_scenario2():
    # GIVEN
    sue_text = "Sue"
    sue_worldunit = worldunit_shop(sue_text)
    yao_text = "Yao"
    sue_worldunit.add_charunit(yao_text)
    yao_charunit = sue_worldunit.get_char(yao_text)
    yao_charunit.add_belieflink(yao_text, 1, 4)
    ohio_text = ",Ohio"
    yao_charunit.add_belieflink(ohio_text, 3, 1)
    assert yao_charunit._credor_pool == 0
    assert yao_charunit._debtor_pool == 0
    assert yao_charunit.get_belieflink(yao_text)._credor_pool == 0
    assert yao_charunit.get_belieflink(yao_text)._debtor_pool == 0

    # WHEN
    sue_worldunit._calc_charunit_metrics()

    # THEN
    assert sue_worldunit.get_char(yao_text)._credor_pool != 0
    assert sue_worldunit.get_char(yao_text)._debtor_pool != 0
    assert yao_charunit.get_belieflink(yao_text)._credor_pool != 0
    assert yao_charunit.get_belieflink(yao_text)._debtor_pool != 0
    yao_yao_belieflink = yao_charunit.get_belieflink(yao_text)
    assert yao_yao_belieflink._credor_pool != 0
    assert yao_yao_belieflink._debtor_pool != 0
    assert yao_yao_belieflink._credor_pool == sue_worldunit._credor_respect * 0.25
    assert yao_yao_belieflink._debtor_pool == sue_worldunit._debtor_respect * 0.8
    assert yao_yao_belieflink._credor_pool == 250000000
    assert yao_yao_belieflink._debtor_pool == 800000000
    yao_ohio_belieflink = yao_charunit.get_belieflink(ohio_text)
    assert yao_ohio_belieflink._credor_pool != 0
    assert yao_ohio_belieflink._debtor_pool != 0
    assert yao_ohio_belieflink._credor_pool == sue_worldunit._credor_respect * 0.75
    assert yao_ohio_belieflink._debtor_pool == sue_worldunit._debtor_respect * 0.2
    assert yao_ohio_belieflink._credor_pool == 750000000
    assert yao_ohio_belieflink._debtor_pool == 200000000
    assert len(sue_worldunit._beliefstorys) == 2
    ohio_beliefstory = sue_worldunit.get_beliefstory(ohio_text)
    assert len(ohio_beliefstory._belieflinks) == 1


def test_WorldUnit_reset_charunit_world_cred_debt_SetsAttr():
    # GIVEN
    sue_text = "Sue"
    sue_worldunit = worldunit_shop(sue_text)
    yao_text = "Yao"
    zia_text = "Zia"
    sue_worldunit.add_charunit(yao_text, 55, 55)
    sue_worldunit.add_charunit(zia_text, 55, 55)
    yao_charunit = sue_worldunit.get_char(yao_text)
    zia_charunit = sue_worldunit.get_char(zia_text)
    yao_charunit.add_world_cred_debt(0.5, 0.6, 0.1, 0.22)
    zia_charunit.add_world_cred_debt(0.2, 0.1, 0.1, 0.22)
    zia_1 = 0.8
    zia_2 = 0.5
    zia_3 = 200
    zia_4 = 140
    zia_charunit.set_world_agenda_ratio_cred_debt(
        world_agenda_ratio_cred_sum=zia_1,
        world_agenda_ratio_debt_sum=zia_2,
        world_charunit_total_credor_weight=zia_3,
        world_charunit_total_debtor_weight=zia_4,
    )
    yao_1 = 0.2
    yao_2 = 0.5
    yao_3 = 204
    yao_4 = 144
    yao_charunit.set_world_agenda_ratio_cred_debt(
        world_agenda_ratio_cred_sum=yao_1,
        world_agenda_ratio_debt_sum=yao_2,
        world_charunit_total_credor_weight=yao_3,
        world_charunit_total_debtor_weight=yao_4,
    )
    assert zia_charunit._world_agenda_ratio_cred == 0.125
    assert zia_charunit._world_agenda_ratio_debt == 0.44
    assert yao_charunit._world_agenda_ratio_cred == 0.5
    assert yao_charunit._world_agenda_ratio_debt == 0.44

    # WHEN
    sue_worldunit._calc_charunit_metrics()

    # THEN
    assert zia_charunit._world_agenda_ratio_cred == 0
    assert zia_charunit._world_agenda_ratio_debt == 0
    assert yao_charunit._world_agenda_ratio_cred == 0
    assert yao_charunit._world_agenda_ratio_debt == 0
