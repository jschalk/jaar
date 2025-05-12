from src.a05_idea_logic.idea import ideaunit_shop
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
    casa_way = yao_listener.make_l1_way(casa_str)
    status_str = "status"
    status_way = yao_listener.make_way(casa_way, status_str)
    clean_str = "clean"
    clean_way = yao_listener.make_way(status_way, clean_str)
    dirty_str = "dirty"
    dirty_way = yao_listener.make_way(status_way, dirty_str)
    sweep_str = "sweep"
    sweep_way = yao_listener.make_way(casa_way, sweep_str)

    yao_listener.add_acctunit(yao_str)
    yao_listener.set_acct_respect(20)
    yao_listener.set_idea(ideaunit_shop(clean_str), status_way)
    yao_listener.set_idea(ideaunit_shop(dirty_str), status_way)
    yao_listener.set_idea(ideaunit_shop(sweep_str, pledge=True), casa_way)
    yao_listener.edit_idea_attr(
        sweep_way, reason_context=status_way, reason_premise=dirty_way
    )
    missing_fact_fcontexts = list(yao_listener.get_missing_fact_contexts().keys())

    yao_speaker = budunit_shop(yao_str)
    yao_speaker.add_fact(status_way, clean_way, create_missing_ideas=True)
    assert yao_listener.get_missing_fact_contexts().keys() == {status_way}

    # WHEN
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_fcontexts)

    # THEN
    assert len(yao_listener.get_missing_fact_contexts().keys()) == 0


def test_set_listen_to_speaker_fact_DoesNotOverrideFact():
    # ESTABLISH
    yao_str = "Yao"
    yao_listener = budunit_shop(yao_str)
    yao_listener.add_acctunit(yao_str)
    yao_listener.set_acct_respect(20)
    casa_str = "casa"
    casa_way = yao_listener.make_l1_way(casa_str)
    status_str = "status"
    status_way = yao_listener.make_way(casa_way, status_str)
    clean_str = "clean"
    clean_way = yao_listener.make_way(status_way, clean_str)
    dirty_str = "dirty"
    dirty_way = yao_listener.make_way(status_way, dirty_str)
    sweep_str = "sweep"
    sweep_way = yao_listener.make_way(casa_way, sweep_str)
    fridge_str = "fridge"
    fridge_way = yao_listener.make_way(casa_way, fridge_str)
    running_str = "running"
    running_way = yao_listener.make_way(fridge_way, running_str)

    yao_listener.set_idea(ideaunit_shop(running_str), fridge_way)
    yao_listener.set_idea(ideaunit_shop(clean_str), status_way)
    yao_listener.set_idea(ideaunit_shop(dirty_str), status_way)
    yao_listener.set_idea(ideaunit_shop(sweep_str, pledge=True), casa_way)
    yao_listener.edit_idea_attr(
        sweep_way, reason_context=status_way, reason_premise=dirty_way
    )
    yao_listener.edit_idea_attr(
        sweep_way, reason_context=fridge_way, reason_premise=running_way
    )
    assert len(yao_listener.get_missing_fact_contexts()) == 2
    yao_listener.add_fact(status_way, dirty_way)
    assert len(yao_listener.get_missing_fact_contexts()) == 1
    assert yao_listener.get_fact(status_way).fneed == dirty_way

    # WHEN
    yao_speaker = budunit_shop(yao_str)
    yao_speaker.add_fact(status_way, clean_way, create_missing_ideas=True)
    yao_speaker.add_fact(fridge_way, running_way, create_missing_ideas=True)
    missing_fact_fcontexts = list(yao_listener.get_missing_fact_contexts().keys())
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_fcontexts)

    # THEN
    assert len(yao_listener.get_missing_fact_contexts()) == 0
    # did not grab speaker's factunit
    assert yao_listener.get_fact(status_way).fneed == dirty_way
    # grabed speaker's factunit
    assert yao_listener.get_fact(fridge_way).fneed == running_way


def test_migrate_all_facts_CorrectlyAddsIdeaUnitsAndSetsFactUnits():
    # ESTABLISH
    yao_str = "Yao"
    yao_src = budunit_shop(yao_str)
    casa_str = "casa"
    casa_way = yao_src.make_l1_way(casa_str)
    status_str = "status"
    status_way = yao_src.make_way(casa_way, status_str)
    clean_str = "clean"
    clean_way = yao_src.make_way(status_way, clean_str)
    dirty_str = "dirty"
    dirty_way = yao_src.make_way(status_way, dirty_str)
    sweep_str = "sweep"
    sweep_way = yao_src.make_way(casa_way, sweep_str)
    weather_str = "weather"
    weather_way = yao_src.make_l1_way(weather_str)
    rain_str = "raining"
    rain_way = yao_src.make_way(weather_way, rain_str)
    snow_str = "snow"
    snow_way = yao_src.make_way(weather_way, snow_str)

    yao_src.add_acctunit(yao_str)
    yao_src.set_acct_respect(20)
    yao_src.set_idea(ideaunit_shop(clean_str), status_way)
    yao_src.set_idea(ideaunit_shop(dirty_str), status_way)
    yao_src.set_idea(ideaunit_shop(sweep_str, pledge=True), casa_way)
    yao_src.edit_reason(sweep_way, status_way, dirty_way)
    # missing_fact_fcontexts = list(yao_src.get_missing_fact_contexts().keys())
    yao_src.set_idea(ideaunit_shop(rain_str), weather_way)
    yao_src.set_idea(ideaunit_shop(snow_str), weather_way)
    yao_src.add_fact(weather_way, rain_way)
    yao_src.add_fact(status_way, clean_way)
    yao_src.settle_bud()

    yao_dst = budunit_shop(yao_str)
    assert yao_dst.idea_exists(clean_way) is False
    assert yao_dst.idea_exists(dirty_way) is False
    assert yao_dst.idea_exists(rain_way) is False
    assert yao_dst.idea_exists(snow_way) is False
    assert yao_dst.get_fact(weather_way) is None
    assert yao_dst.get_fact(status_way) is None

    # WHEN
    migrate_all_facts(yao_src, yao_dst)

    # THEN
    assert yao_dst.idea_exists(clean_way)
    assert yao_dst.idea_exists(dirty_way)
    assert yao_dst.idea_exists(rain_way)
    assert yao_dst.idea_exists(snow_way)
    assert yao_dst.get_fact(weather_way) is not None
    assert yao_dst.get_fact(status_way) is not None
    assert yao_dst.get_fact(weather_way).fneed == rain_way
    assert yao_dst.get_fact(status_way).fneed == clean_way
