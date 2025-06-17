from src.a05_concept_logic.concept import conceptunit_shop
from src.a06_plan_logic.plan import planunit_shop
from src.a13_plan_listen_logic.listen import (
    _allocate_irrational_debt_score,
    generate_ingest_list,
    generate_perspective_agenda,
)


def test_allocate_irrational_debt_score_CorrectlySetsPlanAttr():
    yao_str = "Yao"
    zia_str = "Zia"
    zia_credit_score = 47
    zia_debt_score = 41
    yao_plan = planunit_shop(yao_str)
    yao_plan.add_acctunit(zia_str, zia_credit_score, zia_debt_score)
    zia_acctunit = yao_plan.get_acct(zia_str)
    assert zia_acctunit._irrational_debt_score == 0

    # WHEN
    _allocate_irrational_debt_score(yao_plan, zia_str)

    # THEN
    assert zia_acctunit._irrational_debt_score == zia_debt_score


def test_generate_perspective_agenda_CorrectlyGrabsAgendaChores():
    # ESTABLISH
    yao_str = "Yao"
    yao_speaker = planunit_shop(yao_str)
    yao_speaker.add_acctunit(yao_str)
    yao_speaker.set_acct_respect(20)
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
    yao_speaker.set_concept(conceptunit_shop(clean_str), status_rope)
    yao_speaker.set_concept(conceptunit_shop(dirty_str), status_rope)
    yao_speaker.set_concept(conceptunit_shop(sweep_str, task=True), casa_rope)
    yao_speaker.edit_concept_attr(
        sweep_rope, reason_rcontext=status_rope, reason_premise=dirty_rope
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
    zia_planunit = planunit_shop(zia_str)
    clean_str = "clean"
    zia_planunit.set_l1_concept(conceptunit_shop(clean_str, task=True))
    zia_debtor_pool = 78
    zia_resepect_bit = 2
    assert len(zia_planunit.get_agenda_dict()) == 1

    # WHEN
    ingested_list = generate_ingest_list(
        concept_list=list(zia_planunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_bit=zia_resepect_bit,
    )

    # THEN
    # clean_rope = zia_planunit.make_l1_rope(clean_str)
    clean_rope = zia_planunit.make_l1_rope(clean_str)
    clean_conceptunit = zia_planunit.get_concept_obj(clean_rope)
    assert ingested_list[0] == clean_conceptunit
    assert ingested_list[0].mass == zia_debtor_pool


def test_generate_ingest_list_ReturnsCorrectList_v2():
    # ESTABLISH
    zia_str = "Zia"
    zia_planunit = planunit_shop(zia_str)
    clean_str = "clean"
    cook_str = "cook"
    zia_planunit.set_l1_concept(conceptunit_shop(clean_str, task=True))
    zia_planunit.set_l1_concept(conceptunit_shop(cook_str, task=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_planunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        concept_list=list(zia_planunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_bit=zia_resepect_bit,
    )

    # THEN
    # clean_rope = zia_planunit.make_l1_rope(clean_str)
    assert len(ingested_list) == 2
    clean_rope = zia_planunit.make_l1_rope(clean_str)
    cook_rope = zia_planunit.make_l1_rope(cook_str)
    clean_conceptunit = zia_planunit.get_concept_obj(clean_rope)
    cook_conceptunit = zia_planunit.get_concept_obj(cook_rope)
    assert ingested_list[0] == cook_conceptunit
    assert ingested_list[0].mass == 16.0
    assert ingested_list == [cook_conceptunit, clean_conceptunit]


def test_generate_ingest_list_ReturnsCorrectList_v3():
    # ESTABLISH
    zia_str = "Zia"
    zia_planunit = planunit_shop(zia_str)
    clean_str = "clean"
    cook_str = "cook"
    zia_planunit.set_l1_concept(conceptunit_shop(clean_str, task=True))
    zia_planunit.set_l1_concept(conceptunit_shop(cook_str, mass=3, task=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_planunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        concept_list=list(zia_planunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_bit=zia_resepect_bit,
    )

    # THEN
    clean_rope = zia_planunit.make_l1_rope(clean_str)
    cook_rope = zia_planunit.make_l1_rope(cook_str)
    clean_conceptunit = zia_planunit.get_concept_obj(clean_rope)
    cook_conceptunit = zia_planunit.get_concept_obj(cook_rope)
    assert ingested_list == [cook_conceptunit, clean_conceptunit]
    assert ingested_list[0].mass == 24.0
    assert ingested_list[1].mass == 8.0


def test_generate_ingest_list_ReturnsCorrectList_v4():
    # ESTABLISH
    zia_str = "Zia"
    zia_planunit = planunit_shop(zia_str)
    clean_str = "clean"
    cook_str = "cook"
    zia_planunit.set_l1_concept(conceptunit_shop(clean_str, task=True))
    zia_planunit.set_l1_concept(conceptunit_shop(cook_str, mass=2, task=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_planunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        concept_list=list(zia_planunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_bit=zia_resepect_bit,
    )

    # THEN
    clean_rope = zia_planunit.make_l1_rope(clean_str)
    cook_rope = zia_planunit.make_l1_rope(cook_str)
    clean_conceptunit = zia_planunit.get_concept_obj(clean_rope)
    cook_conceptunit = zia_planunit.get_concept_obj(cook_rope)
    assert ingested_list[0].mass == 22
    assert ingested_list[1].mass == 10
    assert ingested_list == [cook_conceptunit, clean_conceptunit]
