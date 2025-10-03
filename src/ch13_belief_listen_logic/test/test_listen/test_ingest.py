from src.ch06_plan_logic.plan import planunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch13_belief_listen_logic.listen_main import (
    _allocate_irrational_voice_debt_points,
    generate_ingest_list,
    generate_perspective_agenda,
)


def test_allocate_irrational_voice_debt_points_SetsBeliefAttr():
    # ESTABLISH
    yao_str = "Yao"
    zia_str = "Zia"
    zia_voice_cred_points = 47
    zia_voice_debt_points = 41
    yao_belief = beliefunit_shop(yao_str)
    yao_belief.add_voiceunit(zia_str, zia_voice_cred_points, zia_voice_debt_points)
    zia_voiceunit = yao_belief.get_voice(zia_str)
    assert zia_voiceunit.irrational_voice_debt_points == 0

    # WHEN
    _allocate_irrational_voice_debt_points(yao_belief, zia_str)

    # THEN
    assert zia_voiceunit.irrational_voice_debt_points == zia_voice_debt_points


def test_generate_perspective_agenda_GrabsAgendatasks():
    # ESTABLISH
    yao_str = "Yao"
    yao_speaker = beliefunit_shop(yao_str)
    yao_speaker.add_voiceunit(yao_str)
    yao_speaker.set_voice_respect(20)
    casa_str = "casa"
    casa_rope = yao_speaker.make_l1_rope(casa_str)
    status_str = "status"
    status_rope = yao_speaker.make_rope(casa_rope, status_str)
    clean_str = "clean"
    clean_rope = yao_speaker.make_rope(status_rope, clean_str)
    dirty_str = "dirty"
    dirty_rope = yao_speaker.make_rope(status_rope, dirty_str)
    sweep_str = "sweep"
    sweep_rope = yao_speaker.make_rope(casa_rope, sweep_str)
    yao_speaker.set_plan(planunit_shop(clean_str), status_rope)
    yao_speaker.set_plan(planunit_shop(dirty_str), status_rope)
    yao_speaker.set_plan(planunit_shop(sweep_str, pledge=True), casa_rope)
    yao_speaker.edit_plan_attr(
        sweep_rope, reason_context=status_rope, reason_case=dirty_rope
    )
    yao_speaker.add_fact(status_rope, clean_rope)
    assert len(yao_speaker.get_agenda_dict()) == 0

    # WHEN
    agenda_list = generate_perspective_agenda(yao_speaker)

    # THEN
    assert len(agenda_list) == 1


def test_generate_ingest_list_ReturnsList_v1():
    # ESTABLISH
    zia_str = "Zia"
    zia_beliefunit = beliefunit_shop(zia_str)
    clean_str = "clean"
    zia_beliefunit.set_l1_plan(planunit_shop(clean_str, pledge=True))
    zia_debtor_pool = 78
    zia_resepect_bit = 2
    assert len(zia_beliefunit.get_agenda_dict()) == 1

    # WHEN
    ingested_list = generate_ingest_list(
        plan_list=list(zia_beliefunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_grain=zia_resepect_bit,
    )

    # THEN
    # clean_rope = zia_beliefunit.make_l1_rope(clean_str)
    clean_rope = zia_beliefunit.make_l1_rope(clean_str)
    clean_planunit = zia_beliefunit.get_plan_obj(clean_rope)
    assert ingested_list[0] == clean_planunit
    assert ingested_list[0].star == zia_debtor_pool


def test_generate_ingest_list_ReturnsList_v2():
    # ESTABLISH
    zia_str = "Zia"
    zia_beliefunit = beliefunit_shop(zia_str)
    clean_str = "clean"
    cook_str = "cook"
    zia_beliefunit.set_l1_plan(planunit_shop(clean_str, pledge=True))
    zia_beliefunit.set_l1_plan(planunit_shop(cook_str, pledge=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_beliefunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        plan_list=list(zia_beliefunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_grain=zia_resepect_bit,
    )

    # THEN
    # clean_rope = zia_beliefunit.make_l1_rope(clean_str)
    assert len(ingested_list) == 2
    clean_rope = zia_beliefunit.make_l1_rope(clean_str)
    cook_rope = zia_beliefunit.make_l1_rope(cook_str)
    clean_planunit = zia_beliefunit.get_plan_obj(clean_rope)
    cook_planunit = zia_beliefunit.get_plan_obj(cook_rope)
    assert ingested_list[0] == cook_planunit
    assert ingested_list[0].star == 16.0
    assert ingested_list == [cook_planunit, clean_planunit]


def test_generate_ingest_list_ReturnsList_v3():
    # ESTABLISH
    zia_str = "Zia"
    zia_beliefunit = beliefunit_shop(zia_str)
    clean_str = "clean"
    cook_str = "cook"
    zia_beliefunit.set_l1_plan(planunit_shop(clean_str, pledge=True))
    zia_beliefunit.set_l1_plan(planunit_shop(cook_str, star=3, pledge=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_beliefunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        plan_list=list(zia_beliefunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_grain=zia_resepect_bit,
    )

    # THEN
    clean_rope = zia_beliefunit.make_l1_rope(clean_str)
    cook_rope = zia_beliefunit.make_l1_rope(cook_str)
    clean_planunit = zia_beliefunit.get_plan_obj(clean_rope)
    cook_planunit = zia_beliefunit.get_plan_obj(cook_rope)
    assert ingested_list == [cook_planunit, clean_planunit]
    assert ingested_list[0].star == 24.0
    assert ingested_list[1].star == 8.0


def test_generate_ingest_list_ReturnsList_v4():
    # ESTABLISH
    zia_str = "Zia"
    zia_beliefunit = beliefunit_shop(zia_str)
    clean_str = "clean"
    cook_str = "cook"
    zia_beliefunit.set_l1_plan(planunit_shop(clean_str, pledge=True))
    zia_beliefunit.set_l1_plan(planunit_shop(cook_str, star=2, pledge=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_beliefunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        plan_list=list(zia_beliefunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_grain=zia_resepect_bit,
    )

    # THEN
    clean_rope = zia_beliefunit.make_l1_rope(clean_str)
    cook_rope = zia_beliefunit.make_l1_rope(cook_str)
    clean_planunit = zia_beliefunit.get_plan_obj(clean_rope)
    cook_planunit = zia_beliefunit.get_plan_obj(cook_rope)
    assert ingested_list[0].star == 22
    assert ingested_list[1].star == 10
    assert ingested_list == [cook_planunit, clean_planunit]
