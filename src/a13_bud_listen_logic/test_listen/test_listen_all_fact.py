from src.a05_item_logic.item import itemunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a13_bud_listen_logic.listen import (
    migrate_all_facts,
    get_debtors_roll,
    get_ordered_debtors_roll,
    listen_to_speaker_fact,
)


def test_get_debtors_roll_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_duty.settle_bud()

    # WHEN
    yao_roll = get_debtors_roll(yao_duty)

    # THEN
    zia_acctunit = yao_duty.get_acct(zia_str)
    assert yao_roll == [zia_acctunit]


def test_get_debtors_roll_ReturnsObjIgnoresZero_debtit_belief():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    wei_str = "Wei"
    wei_credit_belief = 67
    wei_debtit_belief = 0
    yao_duty.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_duty.add_acctunit(wei_str, wei_credit_belief, wei_debtit_belief)
    yao_duty.settle_bud()

    # WHEN
    yao_roll = get_debtors_roll(yao_duty)

    # THEN
    zia_acctunit = yao_duty.get_acct(zia_str)
    assert yao_roll == [zia_acctunit]


def test_get_ordered_debtors_roll_ReturnsObjsInOrder():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    sue_str = "Sue"
    sue_credit_belief = 57
    sue_debtit_belief = 51
    yao_bud.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    yao_bud.add_acctunit(sue_str, sue_credit_belief, sue_debtit_belief)
    yao_pool = 92
    yao_bud.set_acct_respect(yao_pool)

    # WHEN
    ordered_accts1 = get_ordered_debtors_roll(yao_bud)

    # THEN
    zia_acct = yao_bud.get_acct(zia_str)
    sue_acct = yao_bud.get_acct(sue_str)
    assert ordered_accts1[0].get_dict() == sue_acct.get_dict()
    assert ordered_accts1 == [sue_acct, zia_acct]

    # ESTABLISH
    bob_str = "Bob"
    bob_debtit_belief = 75
    yao_bud.add_acctunit(bob_str, 0, bob_debtit_belief)
    bob_acct = yao_bud.get_acct(bob_str)

    # WHEN
    ordered_accts2 = get_ordered_debtors_roll(yao_bud)

    # THEN
    assert ordered_accts2[0].get_dict() == bob_acct.get_dict()
    assert ordered_accts2 == [bob_acct, sue_acct, zia_acct]


def test_get_ordered_debtors_roll_DoesNotReturnZero_debtit_belief():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(yao_str)
    zia_str = "Zia"
    zia_debtit_belief = 41
    sue_str = "Sue"
    sue_debtit_belief = 51
    yao_pool = 92
    yao_bud.set_acct_respect(yao_pool)
    bob_str = "Bob"
    bob_debtit_belief = 75
    xio_str = "Xio"
    yao_bud.add_acctunit(zia_str, 0, zia_debtit_belief)
    yao_bud.add_acctunit(sue_str, 0, sue_debtit_belief)
    yao_bud.add_acctunit(bob_str, 0, bob_debtit_belief)
    yao_bud.add_acctunit(yao_str, 0, 0)
    yao_bud.add_acctunit(xio_str, 0, 0)

    # WHEN
    ordered_accts2 = get_ordered_debtors_roll(yao_bud)

    # THEN
    assert len(ordered_accts2) == 3
    zia_acct = yao_bud.get_acct(zia_str)
    sue_acct = yao_bud.get_acct(sue_str)
    bob_acct = yao_bud.get_acct(bob_str)
    assert ordered_accts2[0].get_dict() == bob_acct.get_dict()
    assert ordered_accts2 == [bob_acct, sue_acct, zia_acct]


def test_set_listen_to_speaker_fact_SetsFact():
    # ESTABLISH
    yao_str = "Yao"
    yao_listener = budunit_shop(yao_str)
    casa_str = "casa"
    casa_road = yao_listener.make_l1_road(casa_str)
    status_str = "status"
    status_road = yao_listener.make_road(casa_road, status_str)
    clean_str = "clean"
    clean_road = yao_listener.make_road(status_road, clean_str)
    dirty_str = "dirty"
    dirty_road = yao_listener.make_road(status_road, dirty_str)
    sweep_str = "sweep"
    sweep_road = yao_listener.make_road(casa_road, sweep_str)

    yao_listener.add_acctunit(yao_str)
    yao_listener.set_acct_respect(20)
    yao_listener.set_item(itemunit_shop(clean_str), status_road)
    yao_listener.set_item(itemunit_shop(dirty_str), status_road)
    yao_listener.set_item(itemunit_shop(sweep_str, pledge=True), casa_road)
    yao_listener.edit_item_attr(
        sweep_road, reason_base=status_road, reason_premise=dirty_road
    )
    missing_fact_bases = list(yao_listener.get_missing_fact_bases().keys())

    yao_speaker = budunit_shop(yao_str)
    yao_speaker.add_fact(status_road, clean_road, create_missing_items=True)
    assert yao_listener.get_missing_fact_bases().keys() == {status_road}

    # WHEN
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_bases)

    # THEN
    assert len(yao_listener.get_missing_fact_bases().keys()) == 0


def test_set_listen_to_speaker_fact_DoesNotOverrideFact():
    # ESTABLISH
    yao_str = "Yao"
    yao_listener = budunit_shop(yao_str)
    yao_listener.add_acctunit(yao_str)
    yao_listener.set_acct_respect(20)
    casa_str = "casa"
    casa_road = yao_listener.make_l1_road(casa_str)
    status_str = "status"
    status_road = yao_listener.make_road(casa_road, status_str)
    clean_str = "clean"
    clean_road = yao_listener.make_road(status_road, clean_str)
    dirty_str = "dirty"
    dirty_road = yao_listener.make_road(status_road, dirty_str)
    sweep_str = "sweep"
    sweep_road = yao_listener.make_road(casa_road, sweep_str)
    fridge_str = "fridge"
    fridge_road = yao_listener.make_road(casa_road, fridge_str)
    running_str = "running"
    running_road = yao_listener.make_road(fridge_road, running_str)

    yao_listener.set_item(itemunit_shop(running_str), fridge_road)
    yao_listener.set_item(itemunit_shop(clean_str), status_road)
    yao_listener.set_item(itemunit_shop(dirty_str), status_road)
    yao_listener.set_item(itemunit_shop(sweep_str, pledge=True), casa_road)
    yao_listener.edit_item_attr(
        sweep_road, reason_base=status_road, reason_premise=dirty_road
    )
    yao_listener.edit_item_attr(
        sweep_road, reason_base=fridge_road, reason_premise=running_road
    )
    assert len(yao_listener.get_missing_fact_bases()) == 2
    yao_listener.add_fact(status_road, dirty_road)
    assert len(yao_listener.get_missing_fact_bases()) == 1
    assert yao_listener.get_fact(status_road).pick == dirty_road

    # WHEN
    yao_speaker = budunit_shop(yao_str)
    yao_speaker.add_fact(status_road, clean_road, create_missing_items=True)
    yao_speaker.add_fact(fridge_road, running_road, create_missing_items=True)
    missing_fact_bases = list(yao_listener.get_missing_fact_bases().keys())
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_bases)

    # THEN
    assert len(yao_listener.get_missing_fact_bases()) == 0
    # did not grab speaker's factunit
    assert yao_listener.get_fact(status_road).pick == dirty_road
    # grabed speaker's factunit
    assert yao_listener.get_fact(fridge_road).pick == running_road


def test_migrate_all_facts_CorrectlyAddsItemUnitsAndSetsFactUnits():
    # ESTABLISH
    yao_str = "Yao"
    yao_src = budunit_shop(yao_str)
    casa_str = "casa"
    casa_road = yao_src.make_l1_road(casa_str)
    status_str = "status"
    status_road = yao_src.make_road(casa_road, status_str)
    clean_str = "clean"
    clean_road = yao_src.make_road(status_road, clean_str)
    dirty_str = "dirty"
    dirty_road = yao_src.make_road(status_road, dirty_str)
    sweep_str = "sweep"
    sweep_road = yao_src.make_road(casa_road, sweep_str)
    weather_str = "weather"
    weather_road = yao_src.make_l1_road(weather_str)
    rain_str = "raining"
    rain_road = yao_src.make_road(weather_road, rain_str)
    snow_str = "snow"
    snow_road = yao_src.make_road(weather_road, snow_str)

    yao_src.add_acctunit(yao_str)
    yao_src.set_acct_respect(20)
    yao_src.set_item(itemunit_shop(clean_str), status_road)
    yao_src.set_item(itemunit_shop(dirty_str), status_road)
    yao_src.set_item(itemunit_shop(sweep_str, pledge=True), casa_road)
    yao_src.edit_reason(sweep_road, status_road, dirty_road)
    # missing_fact_bases = list(yao_src.get_missing_fact_bases().keys())
    yao_src.set_item(itemunit_shop(rain_str), weather_road)
    yao_src.set_item(itemunit_shop(snow_str), weather_road)
    yao_src.add_fact(weather_road, rain_road)
    yao_src.add_fact(status_road, clean_road)
    yao_src.settle_bud()

    yao_dst = budunit_shop(yao_str)
    assert yao_dst.item_exists(clean_road) is False
    assert yao_dst.item_exists(dirty_road) is False
    assert yao_dst.item_exists(rain_road) is False
    assert yao_dst.item_exists(snow_road) is False
    assert yao_dst.get_fact(weather_road) is None
    assert yao_dst.get_fact(status_road) is None

    # WHEN
    migrate_all_facts(yao_src, yao_dst)

    # THEN
    assert yao_dst.item_exists(clean_road)
    assert yao_dst.item_exists(dirty_road)
    assert yao_dst.item_exists(rain_road)
    assert yao_dst.item_exists(snow_road)
    assert yao_dst.get_fact(weather_road) is not None
    assert yao_dst.get_fact(status_road) is not None
    assert yao_dst.get_fact(weather_road).pick == rain_road
    assert yao_dst.get_fact(status_road).pick == clean_road
