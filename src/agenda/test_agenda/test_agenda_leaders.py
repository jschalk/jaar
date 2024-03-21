# from src.agenda.leader import leaderunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop


def test_AgendaUnit_add_idea_CreatesMissingLeaderGroups():
    # GIVEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(bob_text)
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = ideaunit_shop(clean_cookery_text)
    yao_text = "Yao"
    # clean_cookery_idea._leaderunit = leaderunit_shop()
    clean_cookery_idea._leaderunit.set_group_id(yao_text)
    assert len(bob_agenda._partys) == 0
    assert bob_agenda.get_party(yao_text) is None
    assert len(bob_agenda._groups) == 0
    assert bob_agenda.get_groupunit(yao_text) is None

    # WHEN
    bob_agenda.add_l1_idea(clean_cookery_idea, create_missing_ideas_groups=True)

    # THEN
    assert len(bob_agenda._partys) == 1
    assert bob_agenda.get_party(yao_text) != None
    assert len(bob_agenda._groups) == 1
    assert bob_agenda.get_groupunit(yao_text) != None
    assert bob_agenda.get_groupunit(yao_text).get_partylink(yao_text) != None
