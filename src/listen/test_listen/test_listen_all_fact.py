from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.listen.listen import (
    migrate_all_facts,
    get_debtors_roll,
    get_ordered_debtors_roll,
    listen_to_speaker_fact,
)


def test_get_debtors_roll_ReturnsObj():
    # ESTABLISH
    yao_text = "Yao"
    yao_duty = budunit_shop(yao_text)
    zia_text = "Zia"
    zia_credit_score = 47
    zia_debtit_score = 41
    yao_duty.add_acctunit(zia_text, zia_credit_score, zia_debtit_score)
    yao_duty.settle_bud()

    # WHEN
    yao_roll = get_debtors_roll(yao_duty)

    # THEN
    zia_acctunit = yao_duty.get_acct(zia_text)
    assert yao_roll == [zia_acctunit]


def test_get_debtors_roll_ReturnsObjIgnoresZero_debtit_score():
    # ESTABLISH
    yao_text = "Yao"
    yao_duty = budunit_shop(yao_text)
    zia_text = "Zia"
    zia_credit_score = 47
    zia_debtit_score = 41
    wei_text = "Wei"
    wei_credit_score = 67
    wei_debtit_score = 0
    yao_duty.add_acctunit(zia_text, zia_credit_score, zia_debtit_score)
    yao_duty.add_acctunit(wei_text, wei_credit_score, wei_debtit_score)
    yao_duty.settle_bud()

    # WHEN
    yao_roll = get_debtors_roll(yao_duty)

    # THEN
    zia_acctunit = yao_duty.get_acct(zia_text)
    assert yao_roll == [zia_acctunit]


def test_get_ordered_debtors_roll_ReturnsObjsInOrder():
    # ESTABLISH
    yao_text = "Yao"
    yao_bud = budunit_shop(yao_text)
    zia_text = "Zia"
    zia_credit_score = 47
    zia_debtit_score = 41
    sue_text = "Sue"
    sue_credit_score = 57
    sue_debtit_score = 51
    yao_bud.add_acctunit(zia_text, zia_credit_score, zia_debtit_score)
    yao_bud.add_acctunit(sue_text, sue_credit_score, sue_debtit_score)
    yao_pool = 92
    yao_bud.set_acct_respect(yao_pool)

    # WHEN
    ordered_accts1 = get_ordered_debtors_roll(yao_bud)

    # THEN
    zia_acct = yao_bud.get_acct(zia_text)
    sue_acct = yao_bud.get_acct(sue_text)
    assert ordered_accts1[0].get_dict() == sue_acct.get_dict()
    assert ordered_accts1 == [sue_acct, zia_acct]

    # ESTABLISH
    bob_text = "Bob"
    bob_debtit_score = 75
    yao_bud.add_acctunit(bob_text, 0, bob_debtit_score)
    bob_acct = yao_bud.get_acct(bob_text)

    # WHEN
    ordered_accts2 = get_ordered_debtors_roll(yao_bud)

    # THEN
    assert ordered_accts2[0].get_dict() == bob_acct.get_dict()
    assert ordered_accts2 == [bob_acct, sue_acct, zia_acct]


def test_get_ordered_debtors_roll_DoesNotReturnZero_debtit_score():
    # ESTABLISH
    yao_text = "Yao"
    yao_bud = budunit_shop(yao_text)
    zia_text = "Zia"
    zia_debtit_score = 41
    sue_text = "Sue"
    sue_debtit_score = 51
    yao_pool = 92
    yao_bud.set_acct_respect(yao_pool)
    bob_text = "Bob"
    bob_debtit_score = 75
    xio_text = "Xio"
    yao_bud.add_acctunit(zia_text, 0, zia_debtit_score)
    yao_bud.add_acctunit(sue_text, 0, sue_debtit_score)
    yao_bud.add_acctunit(bob_text, 0, bob_debtit_score)
    yao_bud.add_acctunit(yao_text, 0, 0)
    yao_bud.add_acctunit(xio_text, 0, 0)

    # WHEN
    ordered_accts2 = get_ordered_debtors_roll(yao_bud)

    # THEN
    assert len(ordered_accts2) == 3
    zia_acct = yao_bud.get_acct(zia_text)
    sue_acct = yao_bud.get_acct(sue_text)
    bob_acct = yao_bud.get_acct(bob_text)
    assert ordered_accts2[0].get_dict() == bob_acct.get_dict()
    assert ordered_accts2 == [bob_acct, sue_acct, zia_acct]


def test_set_listen_to_speaker_fact_SetsFact():
    # ESTABLISH
    yao_text = "Yao"
    yao_listener = budunit_shop(yao_text)
    casa_text = "casa"
    casa_road = yao_listener.make_l1_road(casa_text)
    status_text = "status"
    status_road = yao_listener.make_road(casa_road, status_text)
    clean_text = "clean"
    clean_road = yao_listener.make_road(status_road, clean_text)
    dirty_text = "dirty"
    dirty_road = yao_listener.make_road(status_road, dirty_text)
    sweep_text = "sweep"
    sweep_road = yao_listener.make_road(casa_road, sweep_text)

    yao_listener.add_acctunit(yao_text)
    yao_listener.set_acct_respect(20)
    yao_listener.set_idea(ideaunit_shop(clean_text), status_road)
    yao_listener.set_idea(ideaunit_shop(dirty_text), status_road)
    yao_listener.set_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
    yao_listener.edit_idea_attr(
        sweep_road, reason_base=status_road, reason_premise=dirty_road
    )
    missing_fact_bases = list(yao_listener.get_missing_fact_bases().keys())

    yao_speaker = budunit_shop(yao_text)
    yao_speaker.set_fact(status_road, clean_road, create_missing_ideas=True)
    assert yao_listener.get_missing_fact_bases().keys() == {status_road}

    # WHEN
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_bases)

    # THEN
    assert len(yao_listener.get_missing_fact_bases().keys()) == 0


def test_set_listen_to_speaker_fact_DoesNotOverrideFact():
    # ESTABLISH
    yao_text = "Yao"
    yao_listener = budunit_shop(yao_text)
    yao_listener.add_acctunit(yao_text)
    yao_listener.set_acct_respect(20)
    casa_text = "casa"
    casa_road = yao_listener.make_l1_road(casa_text)
    status_text = "status"
    status_road = yao_listener.make_road(casa_road, status_text)
    clean_text = "clean"
    clean_road = yao_listener.make_road(status_road, clean_text)
    dirty_text = "dirty"
    dirty_road = yao_listener.make_road(status_road, dirty_text)
    sweep_text = "sweep"
    sweep_road = yao_listener.make_road(casa_road, sweep_text)
    fridge_text = "fridge"
    fridge_road = yao_listener.make_road(casa_road, fridge_text)
    running_text = "running"
    running_road = yao_listener.make_road(fridge_road, running_text)

    yao_listener.set_idea(ideaunit_shop(running_text), fridge_road)
    yao_listener.set_idea(ideaunit_shop(clean_text), status_road)
    yao_listener.set_idea(ideaunit_shop(dirty_text), status_road)
    yao_listener.set_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
    yao_listener.edit_idea_attr(
        sweep_road, reason_base=status_road, reason_premise=dirty_road
    )
    yao_listener.edit_idea_attr(
        sweep_road, reason_base=fridge_road, reason_premise=running_road
    )
    assert len(yao_listener.get_missing_fact_bases()) == 2
    yao_listener.set_fact(status_road, dirty_road)
    assert len(yao_listener.get_missing_fact_bases()) == 1
    assert yao_listener.get_fact(status_road).pick == dirty_road

    # WHEN
    yao_speaker = budunit_shop(yao_text)
    yao_speaker.set_fact(status_road, clean_road, create_missing_ideas=True)
    yao_speaker.set_fact(fridge_road, running_road, create_missing_ideas=True)
    missing_fact_bases = list(yao_listener.get_missing_fact_bases().keys())
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_bases)

    # THEN
    assert len(yao_listener.get_missing_fact_bases()) == 0
    # did not grab speaker's factunit
    assert yao_listener.get_fact(status_road).pick == dirty_road
    # grabed speaker's factunit
    assert yao_listener.get_fact(fridge_road).pick == running_road


def test_migrate_all_facts_CorrectlyAddsIdeaUnitsAndSetsFactUnits():
    # ESTABLISH
    yao_text = "Yao"
    yao_src = budunit_shop(yao_text)
    casa_text = "casa"
    casa_road = yao_src.make_l1_road(casa_text)
    status_text = "status"
    status_road = yao_src.make_road(casa_road, status_text)
    clean_text = "clean"
    clean_road = yao_src.make_road(status_road, clean_text)
    dirty_text = "dirty"
    dirty_road = yao_src.make_road(status_road, dirty_text)
    sweep_text = "sweep"
    sweep_road = yao_src.make_road(casa_road, sweep_text)
    weather_text = "weather"
    weather_road = yao_src.make_l1_road(weather_text)
    rain_text = "raining"
    rain_road = yao_src.make_road(weather_road, rain_text)
    snow_text = "snow"
    snow_road = yao_src.make_road(weather_road, snow_text)

    yao_src.add_acctunit(yao_text)
    yao_src.set_acct_respect(20)
    yao_src.set_idea(ideaunit_shop(clean_text), status_road)
    yao_src.set_idea(ideaunit_shop(dirty_text), status_road)
    yao_src.set_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
    yao_src.edit_reason(sweep_road, status_road, dirty_road)
    # missing_fact_bases = list(yao_src.get_missing_fact_bases().keys())
    yao_src.set_idea(ideaunit_shop(rain_text), weather_road)
    yao_src.set_idea(ideaunit_shop(snow_text), weather_road)
    yao_src.set_fact(weather_road, rain_road)
    yao_src.set_fact(status_road, clean_road)

    yao_dst = budunit_shop(yao_text)
    assert yao_dst.idea_exists(clean_road) is False
    assert yao_dst.idea_exists(dirty_road) is False
    assert yao_dst.idea_exists(rain_road) is False
    assert yao_dst.idea_exists(snow_road) is False
    assert yao_dst.get_fact(weather_road) is None
    assert yao_dst.get_fact(status_road) is None

    # WHEN
    migrate_all_facts(yao_src, yao_dst)

    # THEN
    assert yao_dst.idea_exists(clean_road)
    assert yao_dst.idea_exists(dirty_road)
    assert yao_dst.idea_exists(rain_road)
    assert yao_dst.idea_exists(snow_road)
    assert yao_dst.get_fact(weather_road) is not None
    assert yao_dst.get_fact(status_road) is not None
    assert yao_dst.get_fact(weather_road).pick == rain_road
    assert yao_dst.get_fact(status_road).pick == clean_road
