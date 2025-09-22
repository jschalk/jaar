from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch13_belief_listen_logic.listen_main import (
    get_debtors_roll,
    get_ordered_debtors_roll,
    listen_to_speaker_fact,
    migrate_all_facts,
)


def test_get_debtors_roll_ReturnsObj():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = beliefunit_shop(yao_str)
    zia_str = "Zia"
    zia_voice_cred_points = 47
    zia_voice_debt_points = 41
    yao_duty.add_voiceunit(zia_str, zia_voice_cred_points, zia_voice_debt_points)
    yao_duty.cashout()

    # WHEN
    yao_roll = get_debtors_roll(yao_duty)

    # THEN
    zia_voiceunit = yao_duty.get_voice(zia_str)
    assert yao_roll == [zia_voiceunit]


def test_get_debtors_roll_ReturnsObjIgnoresZero_voice_debt_points():
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = beliefunit_shop(yao_str)
    zia_str = "Zia"
    zia_voice_cred_points = 47
    zia_voice_debt_points = 41
    wei_str = "Wei"
    wei_voice_cred_points = 67
    wei_voice_debt_points = 0
    yao_duty.add_voiceunit(zia_str, zia_voice_cred_points, zia_voice_debt_points)
    yao_duty.add_voiceunit(wei_str, wei_voice_cred_points, wei_voice_debt_points)
    yao_duty.cashout()

    # WHEN
    yao_roll = get_debtors_roll(yao_duty)

    # THEN
    zia_voiceunit = yao_duty.get_voice(zia_str)
    assert yao_roll == [zia_voiceunit]


def test_get_ordered_debtors_roll_ReturnsObjsInOrder():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)
    zia_str = "Zia"
    zia_voice_cred_points = 47
    zia_voice_debt_points = 41
    sue_str = "Sue"
    sue_voice_cred_points = 57
    sue_voice_debt_points = 51
    yao_belief.add_voiceunit(zia_str, zia_voice_cred_points, zia_voice_debt_points)
    yao_belief.add_voiceunit(sue_str, sue_voice_cred_points, sue_voice_debt_points)
    yao_pool = 92
    yao_belief.set_voice_respect(yao_pool)

    # WHEN
    ordered_voices1 = get_ordered_debtors_roll(yao_belief)

    # THEN
    zia_voice = yao_belief.get_voice(zia_str)
    sue_voice = yao_belief.get_voice(sue_str)
    assert ordered_voices1[0].to_dict() == sue_voice.to_dict()
    assert ordered_voices1 == [sue_voice, zia_voice]

    # ESTABLISH
    bob_str = "Bob"
    bob_voice_debt_points = 75
    yao_belief.add_voiceunit(bob_str, 0, bob_voice_debt_points)
    bob_voice = yao_belief.get_voice(bob_str)

    # WHEN
    ordered_voices2 = get_ordered_debtors_roll(yao_belief)

    # THEN
    assert ordered_voices2[0].to_dict() == bob_voice.to_dict()
    assert ordered_voices2 == [bob_voice, sue_voice, zia_voice]


def test_get_ordered_debtors_roll_DoesNotReturnZero_voice_debt_points():
    # ESTABLISH
    yao_str = "Yao"
    yao_belief = beliefunit_shop(yao_str)
    zia_str = "Zia"
    zia_voice_debt_points = 41
    sue_str = "Sue"
    sue_voice_debt_points = 51
    yao_pool = 92
    yao_belief.set_voice_respect(yao_pool)
    bob_str = "Bob"
    bob_voice_debt_points = 75
    xio_str = "Xio"
    yao_belief.add_voiceunit(zia_str, 0, zia_voice_debt_points)
    yao_belief.add_voiceunit(sue_str, 0, sue_voice_debt_points)
    yao_belief.add_voiceunit(bob_str, 0, bob_voice_debt_points)
    yao_belief.add_voiceunit(yao_str, 0, 0)
    yao_belief.add_voiceunit(xio_str, 0, 0)

    # WHEN
    ordered_voices2 = get_ordered_debtors_roll(yao_belief)

    # THEN
    assert len(ordered_voices2) == 3
    zia_voice = yao_belief.get_voice(zia_str)
    sue_voice = yao_belief.get_voice(sue_str)
    bob_voice = yao_belief.get_voice(bob_str)
    assert ordered_voices2[0].to_dict() == bob_voice.to_dict()
    assert ordered_voices2 == [bob_voice, sue_voice, zia_voice]


def test_set_listen_to_speaker_fact_SetsFact():
    # ESTABLISH
    yao_str = "Yao"
    yao_listener = beliefunit_shop(yao_str)
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

    yao_listener.add_voiceunit(yao_str)
    yao_listener.set_voice_respect(20)
    yao_listener.set_plan(planunit_shop(clean_str), status_rope)
    yao_listener.set_plan(planunit_shop(dirty_str), status_rope)
    yao_listener.set_plan(planunit_shop(sweep_str, task=True), casa_rope)
    yao_listener.edit_plan_attr(
        sweep_rope, reason_context=status_rope, reason_case=dirty_rope
    )
    missing_fact_fact_contexts = list(
        yao_listener.get_missing_fact_reason_contexts().keys()
    )

    yao_speaker = beliefunit_shop(yao_str)
    yao_speaker.add_fact(status_rope, clean_rope, create_missing_plans=True)
    assert yao_listener.get_missing_fact_reason_contexts().keys() == {status_rope}

    # WHEN
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_fact_contexts)

    # THEN
    assert len(yao_listener.get_missing_fact_reason_contexts().keys()) == 0


def test_set_listen_to_speaker_fact_DoesNotOverrideFact():
    # ESTABLISH
    yao_str = "Yao"
    yao_listener = beliefunit_shop(yao_str)
    yao_listener.add_voiceunit(yao_str)
    yao_listener.set_voice_respect(20)
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

    yao_listener.set_plan(planunit_shop(running_str), fridge_rope)
    yao_listener.set_plan(planunit_shop(clean_str), status_rope)
    yao_listener.set_plan(planunit_shop(dirty_str), status_rope)
    yao_listener.set_plan(planunit_shop(sweep_str, task=True), casa_rope)
    yao_listener.edit_plan_attr(
        sweep_rope, reason_context=status_rope, reason_case=dirty_rope
    )
    yao_listener.edit_plan_attr(
        sweep_rope, reason_context=fridge_rope, reason_case=running_rope
    )
    assert len(yao_listener.get_missing_fact_reason_contexts()) == 2
    yao_listener.add_fact(status_rope, dirty_rope)
    assert len(yao_listener.get_missing_fact_reason_contexts()) == 1
    assert yao_listener.get_fact(status_rope).fact_state == dirty_rope

    # WHEN
    yao_speaker = beliefunit_shop(yao_str)
    yao_speaker.add_fact(status_rope, clean_rope, create_missing_plans=True)
    yao_speaker.add_fact(fridge_rope, running_rope, create_missing_plans=True)
    missing_fact_fact_contexts = list(
        yao_listener.get_missing_fact_reason_contexts().keys()
    )
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_fact_contexts)

    # THEN
    assert len(yao_listener.get_missing_fact_reason_contexts()) == 0
    # did not grab speaker's factunit
    assert yao_listener.get_fact(status_rope).fact_state == dirty_rope
    # grabed speaker's factunit
    assert yao_listener.get_fact(fridge_rope).fact_state == running_rope


def test_migrate_all_facts_AddsPlanUnitsAndSetsFactUnits():
    # ESTABLISH
    yao_str = "Yao"
    yao_src = beliefunit_shop(yao_str)
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

    yao_src.add_voiceunit(yao_str)
    yao_src.set_voice_respect(20)
    yao_src.set_plan(planunit_shop(clean_str), status_rope)
    yao_src.set_plan(planunit_shop(dirty_str), status_rope)
    yao_src.set_plan(planunit_shop(sweep_str, task=True), casa_rope)
    yao_src.edit_reason(sweep_rope, status_rope, dirty_rope)
    # missing_fact_fact_contexts = list(yao_src.get_missing_fact_reason_contexts().keys())
    yao_src.set_plan(planunit_shop(rain_str), weather_rope)
    yao_src.set_plan(planunit_shop(snow_str), weather_rope)
    yao_src.add_fact(weather_rope, rain_rope)
    yao_src.add_fact(status_rope, clean_rope)
    yao_src.cashout()

    yao_dst = beliefunit_shop(yao_str)
    assert yao_dst.plan_exists(clean_rope) is False
    assert yao_dst.plan_exists(dirty_rope) is False
    assert yao_dst.plan_exists(rain_rope) is False
    assert yao_dst.plan_exists(snow_rope) is False
    assert yao_dst.get_fact(weather_rope) is None
    assert yao_dst.get_fact(status_rope) is None

    # WHEN
    migrate_all_facts(yao_src, yao_dst)

    # THEN
    assert yao_dst.plan_exists(clean_rope)
    assert yao_dst.plan_exists(dirty_rope)
    assert yao_dst.plan_exists(rain_rope)
    assert yao_dst.plan_exists(snow_rope)
    assert yao_dst.get_fact(weather_rope) is not None
    assert yao_dst.get_fact(status_rope) is not None
    assert yao_dst.get_fact(weather_rope).fact_state == rain_rope
    assert yao_dst.get_fact(status_rope).fact_state == clean_rope
