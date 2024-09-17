from src.s2_bud.idea import ideaunit_shop
from src.s2_bud.bud import budunit_shop
from src.s5_listen.listen import (
    generate_ingest_list,
    _allocate_irrational_debtit_belief,
    generate_perspective_agenda,
)


def test_allocate_irrational_debtit_belief_CorrectlySetsBudAttr():
    yao_str = "Yao"
    zia_str = "Zia"
    zia_credit_belief = 47
    zia_debtit_belief = 41
    yao_bud = budunit_shop(yao_str)
    yao_bud.add_acctunit(zia_str, zia_credit_belief, zia_debtit_belief)
    zia_acctunit = yao_bud.get_acct(zia_str)
    assert zia_acctunit._irrational_debtit_belief == 0

    # WHEN
    _allocate_irrational_debtit_belief(yao_bud, zia_str)

    # THEN
    assert zia_acctunit._irrational_debtit_belief == zia_debtit_belief


def test_generate_perspective_agenda_CorrectlyGrabsAgendaTasks():
    # ESTABLISH
    yao_str = "Yao"
    yao_speaker = budunit_shop(yao_str)
    yao_speaker.add_acctunit(yao_str)
    yao_speaker.set_acct_respect(20)
    casa_str = "casa"
    casa_road = yao_speaker.make_l1_road(casa_str)
    status_str = "status"
    status_road = yao_speaker.make_road(casa_road, status_str)
    clean_str = "clean"
    clean_road = yao_speaker.make_road(status_road, clean_str)
    dirty_str = "dirty"
    dirty_road = yao_speaker.make_road(status_road, dirty_str)
    sweep_str = "sweep"
    sweep_road = yao_speaker.make_road(casa_road, sweep_str)
    yao_speaker.set_idea(ideaunit_shop(clean_str), status_road)
    yao_speaker.set_idea(ideaunit_shop(dirty_str), status_road)
    yao_speaker.set_idea(ideaunit_shop(sweep_str, pledge=True), casa_road)
    yao_speaker.edit_idea_attr(
        sweep_road, reason_base=status_road, reason_premise=dirty_road
    )
    yao_speaker.set_fact(status_road, clean_road)
    assert len(yao_speaker.get_agenda_dict()) == 0

    # WHEN
    agenda_list = generate_perspective_agenda(yao_speaker)

    # THEN
    assert len(agenda_list) == 1


def test_generate_ingest_list_ReturnsCorrectList_v1():
    # ESTABLISH
    zia_str = "Zia"
    zia_budunit = budunit_shop(zia_str)
    clean_str = "clean"
    zia_budunit.set_l1_idea(ideaunit_shop(clean_str, pledge=True))
    zia_debtor_pool = 78
    zia_resepect_bit = 2
    assert len(zia_budunit.get_agenda_dict()) == 1

    # WHEN
    ingested_list = generate_ingest_list(
        item_list=list(zia_budunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_bit=zia_resepect_bit,
    )

    # THEN
    # clean_road = zia_budunit.make_l1_road(clean_str)
    clean_road = zia_budunit.make_l1_road(clean_str)
    clean_ideaunit = zia_budunit.get_idea_obj(clean_road)
    assert ingested_list[0] == clean_ideaunit
    assert ingested_list[0].mass == zia_debtor_pool


def test_generate_ingest_list_ReturnsCorrectList_v2():
    # ESTABLISH
    zia_str = "Zia"
    zia_budunit = budunit_shop(zia_str)
    clean_str = "clean"
    cook_str = "cook"
    zia_budunit.set_l1_idea(ideaunit_shop(clean_str, pledge=True))
    zia_budunit.set_l1_idea(ideaunit_shop(cook_str, pledge=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_budunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        item_list=list(zia_budunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_bit=zia_resepect_bit,
    )

    # THEN
    # clean_road = zia_budunit.make_l1_road(clean_str)
    assert len(ingested_list) == 2
    clean_road = zia_budunit.make_l1_road(clean_str)
    cook_road = zia_budunit.make_l1_road(cook_str)
    clean_ideaunit = zia_budunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_budunit.get_idea_obj(cook_road)
    assert ingested_list[0] == cook_ideaunit
    assert ingested_list[0].mass == 16.0
    assert ingested_list == [cook_ideaunit, clean_ideaunit]


def test_generate_ingest_list_ReturnsCorrectList_v3():
    # ESTABLISH
    zia_str = "Zia"
    zia_budunit = budunit_shop(zia_str)
    clean_str = "clean"
    cook_str = "cook"
    zia_budunit.set_l1_idea(ideaunit_shop(clean_str, pledge=True))
    zia_budunit.set_l1_idea(ideaunit_shop(cook_str, mass=3, pledge=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_budunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        item_list=list(zia_budunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_bit=zia_resepect_bit,
    )

    # THEN
    clean_road = zia_budunit.make_l1_road(clean_str)
    cook_road = zia_budunit.make_l1_road(cook_str)
    clean_ideaunit = zia_budunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_budunit.get_idea_obj(cook_road)
    assert ingested_list == [cook_ideaunit, clean_ideaunit]
    assert ingested_list[0].mass == 24.0
    assert ingested_list[1].mass == 8.0


def test_generate_ingest_list_ReturnsCorrectList_v4():
    # ESTABLISH
    zia_str = "Zia"
    zia_budunit = budunit_shop(zia_str)
    clean_str = "clean"
    cook_str = "cook"
    zia_budunit.set_l1_idea(ideaunit_shop(clean_str, pledge=True))
    zia_budunit.set_l1_idea(ideaunit_shop(cook_str, mass=2, pledge=True))
    zia_debtor_pool = 32
    zia_resepect_bit = 2
    assert len(zia_budunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        item_list=list(zia_budunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        respect_bit=zia_resepect_bit,
    )

    # THEN
    clean_road = zia_budunit.make_l1_road(clean_str)
    cook_road = zia_budunit.make_l1_road(cook_str)
    clean_ideaunit = zia_budunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_budunit.get_idea_obj(cook_road)
    assert ingested_list[0].mass == 22
    assert ingested_list[1].mass == 10
    assert ingested_list == [cook_ideaunit, clean_ideaunit]
