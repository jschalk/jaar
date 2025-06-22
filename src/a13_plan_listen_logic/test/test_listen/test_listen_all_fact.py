from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a13_plan_listen_logic.listen import (
    get_debtors_roll,
    get_ordered_debtors_roll,
    listen_to_speaker_fact,
    migrate_all_facts,
)


def test_get_debtors_roll_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = planunit_shop(yao_str)
    zia_str = "Zia"
    zia_acct_cred_points = 47
    zia_acct_debt_points = 41
    yao_duty.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_duty.settle_plan()

    # WHEN
    yao_roll = get_debtors_roll(yao_duty)

    # THEN
    zia_acctunit = yao_duty.get_acct(zia_str)
    assert yao_roll == [zia_acctunit]


def test_get_debtors_roll_ReturnsObjIgnoresZero_acct_debt_points():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = planunit_shop(yao_str)
    zia_str = "Zia"
    zia_acct_cred_points = 47
    zia_acct_debt_points = 41
    wei_str = "Wei"
    wei_acct_cred_points = 67
    wei_acct_debt_points = 0
    yao_duty.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_duty.add_acctunit(wei_str, wei_acct_cred_points, wei_acct_debt_points)
    yao_duty.settle_plan()

    # WHEN
    yao_roll = get_debtors_roll(yao_duty)

    # THEN
    zia_acctunit = yao_duty.get_acct(zia_str)
    assert yao_roll == [zia_acctunit]


def test_get_ordered_debtors_roll_ReturnsObjsInOrder():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)
    zia_str = "Zia"
    zia_acct_cred_points = 47
    zia_acct_debt_points = 41
    sue_str = "Sue"
    sue_acct_cred_points = 57
    sue_acct_debt_points = 51
    yao_plan.add_acctunit(zia_str, zia_acct_cred_points, zia_acct_debt_points)
    yao_plan.add_acctunit(sue_str, sue_acct_cred_points, sue_acct_debt_points)
    yao_pool = 92
    yao_plan.set_acct_respect(yao_pool)

    # WHEN
    ordered_accts1 = get_ordered_debtors_roll(yao_plan)

    # THEN
    zia_acct = yao_plan.get_acct(zia_str)
    sue_acct = yao_plan.get_acct(sue_str)
    assert ordered_accts1[0].get_dict() == sue_acct.get_dict()
    assert ordered_accts1 == [sue_acct, zia_acct]

    # ESTABLISH
    bob_str = "Bob"
    bob_acct_debt_points = 75
    yao_plan.add_acctunit(bob_str, 0, bob_acct_debt_points)
    bob_acct = yao_plan.get_acct(bob_str)

    # WHEN
    ordered_accts2 = get_ordered_debtors_roll(yao_plan)

    # THEN
    assert ordered_accts2[0].get_dict() == bob_acct.get_dict()
    assert ordered_accts2 == [bob_acct, sue_acct, zia_acct]


def test_get_ordered_debtors_roll_DoesNotReturnZero_acct_debt_points():
    # ESTABLISH
    yao_str = "Yao"
    yao_plan = planunit_shop(yao_str)
    zia_str = "Zia"
    zia_acct_debt_points = 41
    sue_str = "Sue"
    sue_acct_debt_points = 51
    yao_pool = 92
    yao_plan.set_acct_respect(yao_pool)
    bob_str = "Bob"
    bob_acct_debt_points = 75
    xio_str = "Xio"
    yao_plan.add_acctunit(zia_str, 0, zia_acct_debt_points)
    yao_plan.add_acctunit(sue_str, 0, sue_acct_debt_points)
    yao_plan.add_acctunit(bob_str, 0, bob_acct_debt_points)
    yao_plan.add_acctunit(yao_str, 0, 0)
    yao_plan.add_acctunit(xio_str, 0, 0)

    # WHEN
    ordered_accts2 = get_ordered_debtors_roll(yao_plan)

    # THEN
    assert len(ordered_accts2) == 3
    zia_acct = yao_plan.get_acct(zia_str)
    sue_acct = yao_plan.get_acct(sue_str)
    bob_acct = yao_plan.get_acct(bob_str)
    assert ordered_accts2[0].get_dict() == bob_acct.get_dict()
    assert ordered_accts2 == [bob_acct, sue_acct, zia_acct]


def test_set_listen_to_speaker_fact_SetsFact():
    # ESTABLISH
    yao_str = "Yao"
    yao_listener = planunit_shop(yao_str)
    casa_str = "casa"
    casa_rope = yao_listener.make_l1_rope(casa_str)
    status_str = "status"
    status_rope = yao_listener.make_rope(casa_rope, status_str)
    clean_str = "clean"
    clean_rope = yao_listener.make_rope(status_rope, clean_str)
    dirty_str = "dirty"
    dirty_rope = yao_listener.make_rope(status_rope, dirty_str)
    sweep_str = "sweep"
    sweep_rope = yao_listener.make_rope(casa_rope, sweep_str)

    yao_listener.add_acctunit(yao_str)
    yao_listener.set_acct_respect(20)
    yao_listener.set_concept(conceptunit_shop(clean_str), status_rope)
    yao_listener.set_concept(conceptunit_shop(dirty_str), status_rope)
    yao_listener.set_concept(conceptunit_shop(sweep_str, task=True), casa_rope)
    yao_listener.edit_concept_attr(
        sweep_rope, reason_rcontext=status_rope, reason_premise=dirty_rope
    )
    missing_fact_fcontexts = list(yao_listener.get_missing_fact_rcontexts().keys())

    yao_speaker = planunit_shop(yao_str)
    yao_speaker.add_fact(status_rope, clean_rope, create_missing_concepts=True)
    assert yao_listener.get_missing_fact_rcontexts().keys() == {status_rope}

    # WHEN
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_fcontexts)

    # THEN
    assert len(yao_listener.get_missing_fact_rcontexts().keys()) == 0


def test_set_listen_to_speaker_fact_DoesNotOverrideFact():
    # ESTABLISH
    yao_str = "Yao"
    yao_listener = planunit_shop(yao_str)
    yao_listener.add_acctunit(yao_str)
    yao_listener.set_acct_respect(20)
    casa_str = "casa"
    casa_rope = yao_listener.make_l1_rope(casa_str)
    status_str = "status"
    status_rope = yao_listener.make_rope(casa_rope, status_str)
    clean_str = "clean"
    clean_rope = yao_listener.make_rope(status_rope, clean_str)
    dirty_str = "dirty"
    dirty_rope = yao_listener.make_rope(status_rope, dirty_str)
    sweep_str = "sweep"
    sweep_rope = yao_listener.make_rope(casa_rope, sweep_str)
    fridge_str = "fridge"
    fridge_rope = yao_listener.make_rope(casa_rope, fridge_str)
    running_str = "running"
    running_rope = yao_listener.make_rope(fridge_rope, running_str)

    yao_listener.set_concept(conceptunit_shop(running_str), fridge_rope)
    yao_listener.set_concept(conceptunit_shop(clean_str), status_rope)
    yao_listener.set_concept(conceptunit_shop(dirty_str), status_rope)
    yao_listener.set_concept(conceptunit_shop(sweep_str, task=True), casa_rope)
    yao_listener.edit_concept_attr(
        sweep_rope, reason_rcontext=status_rope, reason_premise=dirty_rope
    )
    yao_listener.edit_concept_attr(
        sweep_rope, reason_rcontext=fridge_rope, reason_premise=running_rope
    )
    assert len(yao_listener.get_missing_fact_rcontexts()) == 2
    yao_listener.add_fact(status_rope, dirty_rope)
    assert len(yao_listener.get_missing_fact_rcontexts()) == 1
    assert yao_listener.get_fact(status_rope).fstate == dirty_rope

    # WHEN
    yao_speaker = planunit_shop(yao_str)
    yao_speaker.add_fact(status_rope, clean_rope, create_missing_concepts=True)
    yao_speaker.add_fact(fridge_rope, running_rope, create_missing_concepts=True)
    missing_fact_fcontexts = list(yao_listener.get_missing_fact_rcontexts().keys())
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_fcontexts)

    # THEN
    assert len(yao_listener.get_missing_fact_rcontexts()) == 0
    # did not grab speaker's factunit
    assert yao_listener.get_fact(status_rope).fstate == dirty_rope
    # grabed speaker's factunit
    assert yao_listener.get_fact(fridge_rope).fstate == running_rope


def test_migrate_all_facts_CorrectlyAddsConceptUnitsAndSetsFactUnits():
    # ESTABLISH
    yao_str = "Yao"
    yao_src = planunit_shop(yao_str)
    casa_str = "casa"
    casa_rope = yao_src.make_l1_rope(casa_str)
    status_str = "status"
    status_rope = yao_src.make_rope(casa_rope, status_str)
    clean_str = "clean"
    clean_rope = yao_src.make_rope(status_rope, clean_str)
    dirty_str = "dirty"
    dirty_rope = yao_src.make_rope(status_rope, dirty_str)
    sweep_str = "sweep"
    sweep_rope = yao_src.make_rope(casa_rope, sweep_str)
    weather_str = "weather"
    weather_rope = yao_src.make_l1_rope(weather_str)
    rain_str = "raining"
    rain_rope = yao_src.make_rope(weather_rope, rain_str)
    snow_str = "snow"
    snow_rope = yao_src.make_rope(weather_rope, snow_str)

    yao_src.add_acctunit(yao_str)
    yao_src.set_acct_respect(20)
    yao_src.set_concept(conceptunit_shop(clean_str), status_rope)
    yao_src.set_concept(conceptunit_shop(dirty_str), status_rope)
    yao_src.set_concept(conceptunit_shop(sweep_str, task=True), casa_rope)
    yao_src.edit_reason(sweep_rope, status_rope, dirty_rope)
    # missing_fact_fcontexts = list(yao_src.get_missing_fact_rcontexts().keys())
    yao_src.set_concept(conceptunit_shop(rain_str), weather_rope)
    yao_src.set_concept(conceptunit_shop(snow_str), weather_rope)
    yao_src.add_fact(weather_rope, rain_rope)
    yao_src.add_fact(status_rope, clean_rope)
    yao_src.settle_plan()

    yao_dst = planunit_shop(yao_str)
    assert yao_dst.concept_exists(clean_rope) is False
    assert yao_dst.concept_exists(dirty_rope) is False
    assert yao_dst.concept_exists(rain_rope) is False
    assert yao_dst.concept_exists(snow_rope) is False
    assert yao_dst.get_fact(weather_rope) is None
    assert yao_dst.get_fact(status_rope) is None

    # WHEN
    migrate_all_facts(yao_src, yao_dst)

    # THEN
    assert yao_dst.concept_exists(clean_rope)
    assert yao_dst.concept_exists(dirty_rope)
    assert yao_dst.concept_exists(rain_rope)
    assert yao_dst.concept_exists(snow_rope)
    assert yao_dst.get_fact(weather_rope) is not None
    assert yao_dst.get_fact(status_rope) is not None
    assert yao_dst.get_fact(weather_rope).fstate == rain_rope
    assert yao_dst.get_fact(status_rope).fstate == clean_rope
