from src.agenda.agenda import AgendaUnit, agendaunit_shop, ideaunit_shop, EconID
from src.agenda.examples.example_agendas import get_agenda_assignment_laundry_example1
from src.econ.clerk import clerkunit_shop, ClerkUnit
from src.econ.examples.clerk_env_kit import get_temp_econ_id

from random import randrange


def get_1node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_Jnode2node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("J")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("A"))
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_2node_agenda(world_id: EconID = None) -> AgendaUnit:
    if world_id is None:
        world_id = get_temp_econ_id()
    a_text = "A"
    b_text = "B"
    x_agenda = agendaunit_shop(_agent_id=a_text)
    x_agenda.set_world_id(world_id)
    idea_b = ideaunit_shop(b_text)
    x_agenda.add_idea(idea_b, parent_road=get_temp_econ_id())
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_3node_agenda() -> AgendaUnit:
    a_text = "A"
    x_agenda = agendaunit_shop(a_text)
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("B"))
    x_agenda.add_l1_idea(ideaunit_shop("C"))
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_3node_D_E_F_agenda() -> AgendaUnit:
    d_text = "D"
    x_agenda = agendaunit_shop(d_text)
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("E"))
    x_agenda.add_l1_idea(ideaunit_shop("F"))
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_6node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("B"))
    x_agenda.add_l1_idea(ideaunit_shop("C"))
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("D"), c_road)
    x_agenda.add_idea(ideaunit_shop("E"), c_road)
    x_agenda.add_idea(ideaunit_shop("F"), c_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_7nodeInsertH_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("B"))
    x_agenda.add_l1_idea(ideaunit_shop("C"))
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("H"), c_road)
    x_agenda.add_idea(ideaunit_shop("D"), c_road)
    x_agenda.add_idea(ideaunit_shop("E"), c_road)
    x_agenda.add_idea(ideaunit_shop("F"), x_agenda.make_road(c_road, "H"))
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_5nodeHG_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("B"))
    x_agenda.add_l1_idea(ideaunit_shop("C"))
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("H"), c_road)
    x_agenda.add_idea(ideaunit_shop("G"), c_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_7nodeJRoot_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("J")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("A"))

    a_road = x_agenda.make_l1_road("A")
    x_agenda.add_idea(ideaunit_shop("B"), a_road)
    x_agenda.add_idea(ideaunit_shop("C"), a_road)
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("D"), c_road)
    x_agenda.add_idea(ideaunit_shop("E"), c_road)
    x_agenda.add_idea(ideaunit_shop("F"), c_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_7nodeJRootWithH_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("J")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("A"))

    a_road = x_agenda.make_l1_road("A")
    x_agenda.add_idea(ideaunit_shop("B"), a_road)
    x_agenda.add_idea(ideaunit_shop("C"), a_road)
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("E"), c_road)
    x_agenda.add_idea(ideaunit_shop("F"), c_road)
    x_agenda.add_idea(ideaunit_shop("H"), c_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_clerkunit_2agenda(env_dir, econ_id) -> ClerkUnit:
    yao_text = "Xio"
    yao_clerkunit = clerkunit_shop(yao_text, env_dir, econ_id)
    yao_clerkunit.set_depot_agenda(get_1node_agenda(), depotlink_type="blind_trust")
    yao_clerkunit.set_depot_agenda(
        get_Jnode2node_agenda(), depotlink_type="blind_trust"
    )
    return yao_clerkunit


def get_agenda_2CleanNodesRandomWeights(_agent_id: str = None) -> AgendaUnit:
    agent_id = _agent_id if _agent_id != None else "ernie"
    x_agenda = agendaunit_shop(agent_id)
    casa_text = "casa"
    x_agenda.add_l1_idea(ideaunit_shop(casa_text))
    casa_road = x_agenda.make_l1_road(casa_text)
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    cookery_idea = ideaunit_shop(cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = ideaunit_shop(bedroom_text, _weight=randrange(1, 50), promise=True)
    x_agenda.add_idea(cookery_idea, parent_road=casa_road)
    x_agenda.add_idea(bedroom_idea, parent_road=casa_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_agenda_3CleanNodesRandomWeights(_agent_id: str = None) -> AgendaUnit:
    agent_id = _agent_id if _agent_id != None else "ernie"
    x_agenda = agendaunit_shop(agent_id)
    casa_text = "casa"
    x_agenda.add_l1_idea(ideaunit_shop(casa_text))
    casa_road = x_agenda.make_l1_road(casa_text)
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    hallway_text = "clean hallway"
    cookery_idea = ideaunit_shop(cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = ideaunit_shop(bedroom_text, _weight=randrange(1, 50), promise=True)
    hallway_idea = ideaunit_shop(hallway_text, _weight=randrange(1, 50), promise=True)
    x_agenda.add_idea(cookery_idea, parent_road=casa_road)
    x_agenda.add_idea(bedroom_idea, parent_road=casa_road)
    x_agenda.add_idea(hallway_idea, parent_road=casa_road)
    x_agenda.set_agenda_metrics()
    return x_agenda