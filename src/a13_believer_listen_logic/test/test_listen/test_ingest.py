from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a13_believer_listen_logic.listen_main import (
    _allocate_irrational_partner_debt_points,
    generate_ingest_list,
    generate_perspective_agenda,
)


def test_allocate_irrational_partner_debt_points_CorrectlySetsBelieverAttr():
    yao_str = "Yao"
    zia_str = "Zia"
    zia_partner_cred_points = 47
    zia_partner_debt_points = 41
    yao_believer = believerunit_shop(yao_str)
    yao_believer.add_partnerunit(
        zia_str, zia_partner_cred_points, zia_partner_debt_points
    )
    zia_partnerunit = yao_believer.get_partner(zia_str)
    assert zia_partnerunit._irrational_partner_debt_points == 0

    # WHEN
    _allocate_irrational_partner_debt_points(yao_believer, zia_str)

    # THEN
    assert zia_partnerunit._irrational_partner_debt_points == zia_partner_debt_points


def test_generate_perspective_agenda_CorrectlyGrabsAgendaChores():
    # ESTABLISH
    yao_str = "Yao"
    yao_speaker = believerunit_shop(yao_str)
    yao_speaker.add_partnerunit(yao_str)
    yao_speaker.set_partner_respect(20)
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
    yao_speaker.set_plan(planunit_shop(sweep_str, task=True), casa_rope)
    yao_speaker.edit_plan_attr(
        sweep_rope, reason_context=status_rope, reason_case=dirty_rope
    )
    yao_speaker.add_fact(status_rope, clean_rope)
    assert len(yao_speaker.get_agenda_dict()) == 0

    # WHEN
    agenda_list = generate_perspective_agenda(yao_speaker)

    # THEN
    assert len(agenda_list) == 1


def test_generate_ingest_list_ReturnsCorrectList_v1():
    # ESTABLISH
    zia_str = "Zia"
    zia_believerunit = believerunit_shop(zia_str)
    clean_str = "clean"
    zia_believerunit.set_l1_plan(planunit_shop(clean_str, task=True))
    zia_debtor_pool = 78
    zia_resepect_bit = 2
    assert len(zia_believerunit.get_agenda_dict()) == 1

    # WHEN
    ingested_list = generate_ingest_list(
        plan_list=list(zia_believerunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_bit=zia_resepect_bit,
    )

    # THEN
    # clean_rope = zia_believerunit.make_l1_rope(clean_str)
    clean_rope = zia_believerunit.make_l1_rope(clean_str)
    clean_planunit = zia_believerunit.get_plan_obj(clean_rope)
    assert ingested_list[0] == clean_planunit
    assert ingested_list[0].mass == zia_debtor_pool


def test_generate_ingest_list_ReturnsCorrectList_v2():
    # ESTABLISH
    zia_str = "Zia"
    zia_believerunit = believerunit_shop(zia_str)
    clean_str = "clean"
    cook_str = "cook"
    zia_believerunit.set_l1_plan(planunit_shop(clean_str, task=True))
    zia_believerunit.set_l1_plan(planunit_shop(cook_str, task=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_believerunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        plan_list=list(zia_believerunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_bit=zia_resepect_bit,
    )

    # THEN
    # clean_rope = zia_believerunit.make_l1_rope(clean_str)
    assert len(ingested_list) == 2
    clean_rope = zia_believerunit.make_l1_rope(clean_str)
    cook_rope = zia_believerunit.make_l1_rope(cook_str)
    clean_planunit = zia_believerunit.get_plan_obj(clean_rope)
    cook_planunit = zia_believerunit.get_plan_obj(cook_rope)
    assert ingested_list[0] == cook_planunit
    assert ingested_list[0].mass == 16.0
    assert ingested_list == [cook_planunit, clean_planunit]


def test_generate_ingest_list_ReturnsCorrectList_v3():
    # ESTABLISH
    zia_str = "Zia"
    zia_believerunit = believerunit_shop(zia_str)
    clean_str = "clean"
    cook_str = "cook"
    zia_believerunit.set_l1_plan(planunit_shop(clean_str, task=True))
    zia_believerunit.set_l1_plan(planunit_shop(cook_str, mass=3, task=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_believerunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        plan_list=list(zia_believerunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_bit=zia_resepect_bit,
    )

    # THEN
    clean_rope = zia_believerunit.make_l1_rope(clean_str)
    cook_rope = zia_believerunit.make_l1_rope(cook_str)
    clean_planunit = zia_believerunit.get_plan_obj(clean_rope)
    cook_planunit = zia_believerunit.get_plan_obj(cook_rope)
    assert ingested_list == [cook_planunit, clean_planunit]
    assert ingested_list[0].mass == 24.0
    assert ingested_list[1].mass == 8.0


def test_generate_ingest_list_ReturnsCorrectList_v4():
    # ESTABLISH
    zia_str = "Zia"
    zia_believerunit = believerunit_shop(zia_str)
    clean_str = "clean"
    cook_str = "cook"
    zia_believerunit.set_l1_plan(planunit_shop(clean_str, task=True))
    zia_believerunit.set_l1_plan(planunit_shop(cook_str, mass=2, task=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_believerunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        plan_list=list(zia_believerunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_bit=zia_resepect_bit,
    )

    # THEN
    clean_rope = zia_believerunit.make_l1_rope(clean_str)
    cook_rope = zia_believerunit.make_l1_rope(cook_str)
    clean_planunit = zia_believerunit.get_plan_obj(clean_rope)
    cook_planunit = zia_believerunit.get_plan_obj(cook_rope)
    assert ingested_list[0].mass == 22
    assert ingested_list[1].mass == 10
    assert ingested_list == [cook_planunit, clean_planunit]
