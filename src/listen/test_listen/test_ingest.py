from src.bud.idea import ideaunit_shop
from src.bud.bud import budunit_shop
from src.listen.listen import (
    generate_ingest_list,
    _allocate_irrational_debtor_weight,
    generate_perspective_agenda,
)


def test_allocate_irrational_debtor_weight_CorrectlySetsBudAttr():
    yao_text = "Yao"
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    yao_bud = budunit_shop(yao_text)
    yao_bud.add_acctunit(zia_text, zia_credor_weight, zia_debtor_weight)
    zia_acctunit = yao_bud.get_acct(zia_text)
    assert zia_acctunit._irrational_debtor_weight == 0

    # WHEN
    _allocate_irrational_debtor_weight(yao_bud, zia_text)

    # THEN
    assert zia_acctunit._irrational_debtor_weight == zia_debtor_weight


def test_generate_perspective_agenda_CorrectlyGrabsAgendaTasks():
    # ESTABLISH
    yao_text = "Yao"
    yao_speaker = budunit_shop(yao_text)
    yao_speaker.add_acctunit(yao_text)
    yao_speaker.set_acct_respect(20)
    casa_text = "casa"
    casa_road = yao_speaker.make_l1_road(casa_text)
    status_text = "status"
    status_road = yao_speaker.make_road(casa_road, status_text)
    clean_text = "clean"
    clean_road = yao_speaker.make_road(status_road, clean_text)
    dirty_text = "dirty"
    dirty_road = yao_speaker.make_road(status_road, dirty_text)
    sweep_text = "sweep"
    sweep_road = yao_speaker.make_road(casa_road, sweep_text)
    yao_speaker.add_idea(ideaunit_shop(clean_text), status_road)
    yao_speaker.add_idea(ideaunit_shop(dirty_text), status_road)
    yao_speaker.add_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
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
    zia_text = "Zia"
    zia_budunit = budunit_shop(zia_text)
    clean_text = "clean"
    zia_budunit.add_l1_idea(ideaunit_shop(clean_text, pledge=True))
    zia_debtor_pool = 78
    zia_bit = 2
    assert len(zia_budunit.get_agenda_dict()) == 1

    # WHEN
    ingested_list = generate_ingest_list(
        item_list=list(zia_budunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        bit=zia_bit,
    )

    # THEN
    # clean_road = zia_budunit.make_l1_road(clean_text)
    clean_road = zia_budunit.make_l1_road(clean_text)
    clean_ideaunit = zia_budunit.get_idea_obj(clean_road)
    assert ingested_list[0] == clean_ideaunit
    assert ingested_list[0]._weight == zia_debtor_pool


def test_generate_ingest_list_ReturnsCorrectList_v2():
    # ESTABLISH
    zia_text = "Zia"
    zia_budunit = budunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    zia_budunit.add_l1_idea(ideaunit_shop(clean_text, pledge=True))
    zia_budunit.add_l1_idea(ideaunit_shop(cook_text, pledge=True))
    zia_debtor_pool = 32
    zia_bit = 2
    assert len(zia_budunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        item_list=list(zia_budunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        bit=zia_bit,
    )

    # THEN
    # clean_road = zia_budunit.make_l1_road(clean_text)
    assert len(ingested_list) == 2
    clean_road = zia_budunit.make_l1_road(clean_text)
    cook_road = zia_budunit.make_l1_road(cook_text)
    clean_ideaunit = zia_budunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_budunit.get_idea_obj(cook_road)
    assert ingested_list[0] == cook_ideaunit
    assert ingested_list[0]._weight == 16.0
    assert ingested_list == [cook_ideaunit, clean_ideaunit]


def test_generate_ingest_list_ReturnsCorrectList_v3():
    # ESTABLISH
    zia_text = "Zia"
    zia_budunit = budunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    zia_budunit.add_l1_idea(ideaunit_shop(clean_text, pledge=True))
    zia_budunit.add_l1_idea(ideaunit_shop(cook_text, _weight=3, pledge=True))
    zia_debtor_pool = 32
    zia_bit = 2
    assert len(zia_budunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        item_list=list(zia_budunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        bit=zia_bit,
    )

    # THEN
    clean_road = zia_budunit.make_l1_road(clean_text)
    cook_road = zia_budunit.make_l1_road(cook_text)
    clean_ideaunit = zia_budunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_budunit.get_idea_obj(cook_road)
    assert ingested_list == [cook_ideaunit, clean_ideaunit]
    assert ingested_list[0]._weight == 24.0
    assert ingested_list[1]._weight == 8.0


def test_generate_ingest_list_ReturnsCorrectList_v4():
    # ESTABLISH
    zia_text = "Zia"
    zia_budunit = budunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    zia_budunit.add_l1_idea(ideaunit_shop(clean_text, pledge=True))
    zia_budunit.add_l1_idea(ideaunit_shop(cook_text, _weight=2, pledge=True))
    zia_debtor_pool = 32
    zia_bit = 2
    assert len(zia_budunit.get_agenda_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        item_list=list(zia_budunit.get_agenda_dict().values()),
        debtor_amount=zia_debtor_pool,
        bit=zia_bit,
    )

    # THEN
    clean_road = zia_budunit.make_l1_road(clean_text)
    cook_road = zia_budunit.make_l1_road(cook_text)
    clean_ideaunit = zia_budunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_budunit.get_idea_obj(cook_road)
    assert ingested_list[0]._weight == 22
    assert ingested_list[1]._weight == 10
    assert ingested_list == [cook_ideaunit, clean_ideaunit]
