from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.listen.listen import (
    migrate_all_facts,
    get_debtors_roll,
    get_ordered_debtors_roll,
    listen_to_speaker_fact,
)


def test_get_debtors_roll_ReturnsObj():
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    yao_role.add_guyunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_role.calc_agenda_metrics()

    # WHEN
    yao_roll = get_debtors_roll(yao_role)

    # THEN
    zia_guyunit = yao_role.get_guy(zia_text)
    assert yao_roll == [zia_guyunit]


def test_get_debtors_roll_ReturnsObjIgnoresZero_debtor_weight():
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    wei_text = "Wei"
    wei_credor_weight = 67
    wei_debtor_weight = 0
    yao_role.add_guyunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_role.add_guyunit(wei_text, wei_credor_weight, wei_debtor_weight)
    yao_role.calc_agenda_metrics()

    # WHEN
    yao_roll = get_debtors_roll(yao_role)

    # THEN
    zia_guyunit = yao_role.get_guy(zia_text)
    assert yao_roll == [zia_guyunit]


def test_get_ordered_debtors_roll_ReturnsObjsInOrder():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_credor_weight = 57
    sue_debtor_weight = 51
    yao_agenda.add_guyunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_agenda.add_guyunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_agenda.set_guy_pool(yao_pool)

    # WHEN
    ordered_guys1 = get_ordered_debtors_roll(yao_agenda)

    # THEN
    zia_guy = yao_agenda.get_guy(zia_text)
    sue_guy = yao_agenda.get_guy(sue_text)
    assert ordered_guys1[0].get_dict() == sue_guy.get_dict()
    assert ordered_guys1 == [sue_guy, zia_guy]

    # GIVEN
    bob_text = "Bob"
    bob_debtor_weight = 75
    yao_agenda.add_guyunit(bob_text, 0, bob_debtor_weight)
    bob_guy = yao_agenda.get_guy(bob_text)

    # WHEN
    ordered_guys2 = get_ordered_debtors_roll(yao_agenda)

    # THEN
    assert ordered_guys2[0].get_dict() == bob_guy.get_dict()
    assert ordered_guys2 == [bob_guy, sue_guy, zia_guy]


def test_get_ordered_debtors_roll_DoesNotReturnZero_debtor_weight():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_debtor_weight = 51
    yao_pool = 92
    yao_agenda.set_guy_pool(yao_pool)
    bob_text = "Bob"
    bob_debtor_weight = 75
    xio_text = "Xio"
    yao_agenda.add_guyunit(zia_text, 0, zia_debtor_weight)
    yao_agenda.add_guyunit(sue_text, 0, sue_debtor_weight)
    yao_agenda.add_guyunit(bob_text, 0, bob_debtor_weight)
    yao_agenda.add_guyunit(yao_text, 0, 0)
    yao_agenda.add_guyunit(xio_text, 0, 0)

    # WHEN
    ordered_guys2 = get_ordered_debtors_roll(yao_agenda)

    # THEN
    assert len(ordered_guys2) == 3
    zia_guy = yao_agenda.get_guy(zia_text)
    sue_guy = yao_agenda.get_guy(sue_text)
    bob_guy = yao_agenda.get_guy(bob_text)
    assert ordered_guys2[0].get_dict() == bob_guy.get_dict()
    assert ordered_guys2 == [bob_guy, sue_guy, zia_guy]


def test_set_listen_to_speaker_fact_SetsFact():
    # GIVEN
    yao_text = "Yao"
    yao_listener = agendaunit_shop(yao_text)
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

    yao_listener.add_guyunit(yao_text)
    yao_listener.set_guy_pool(20)
    yao_listener.add_idea(ideaunit_shop(clean_text), status_road)
    yao_listener.add_idea(ideaunit_shop(dirty_text), status_road)
    yao_listener.add_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
    yao_listener.edit_idea_attr(
        sweep_road, reason_base=status_road, reason_premise=dirty_road
    )
    missing_fact_bases = list(yao_listener.get_missing_fact_bases().keys())

    yao_speaker = agendaunit_shop(yao_text)
    yao_speaker.set_fact(status_road, clean_road, create_missing_ideas=True)
    assert yao_listener.get_missing_fact_bases().keys() == {status_road}

    # WHEN
    listen_to_speaker_fact(yao_listener, yao_speaker, missing_fact_bases)

    # THEN
    assert len(yao_listener.get_missing_fact_bases().keys()) == 0


def test_set_listen_to_speaker_fact_DoesNotOverrideFact():
    # GIVEN
    yao_text = "Yao"
    yao_listener = agendaunit_shop(yao_text)
    yao_listener.add_guyunit(yao_text)
    yao_listener.set_guy_pool(20)
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

    yao_listener.add_idea(ideaunit_shop(running_text), fridge_road)
    yao_listener.add_idea(ideaunit_shop(clean_text), status_road)
    yao_listener.add_idea(ideaunit_shop(dirty_text), status_road)
    yao_listener.add_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
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
    yao_speaker = agendaunit_shop(yao_text)
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
    # GIVEN
    yao_text = "Yao"
    yao_src = agendaunit_shop(yao_text)
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

    yao_src.add_guyunit(yao_text)
    yao_src.set_guy_pool(20)
    yao_src.add_idea(ideaunit_shop(clean_text), status_road)
    yao_src.add_idea(ideaunit_shop(dirty_text), status_road)
    yao_src.add_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
    yao_src.edit_reason(sweep_road, status_road, dirty_road)
    # missing_fact_bases = list(yao_src.get_missing_fact_bases().keys())
    yao_src.add_idea(ideaunit_shop(rain_text), weather_road)
    yao_src.add_idea(ideaunit_shop(snow_text), weather_road)
    yao_src.set_fact(weather_road, rain_road)
    yao_src.set_fact(status_road, clean_road)

    yao_dst = agendaunit_shop(yao_text)
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
    assert yao_dst.get_fact(weather_road) != None
    assert yao_dst.get_fact(status_road) != None
    assert yao_dst.get_fact(weather_road).pick == rain_road
    assert yao_dst.get_fact(status_road).pick == clean_road