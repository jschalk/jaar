from src.agenda.atom import agendaatom_shop, atom_update, atom_insert, atom_delete
from src.agenda.book import bookunit_shop, create_legible_list
from src.agenda.agenda import agendaunit_shop


def test_create_legible_list_ReturnsObj_idea_leaderunit_INSERT():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_idea_leaderunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    group_id_text = "group_id"
    group_id_value = f"{sue_agenda._road_delimiter}Swimmers"
    swim_agendaatom = agendaatom_shop(category, atom_insert())
    swim_agendaatom.set_arg(road_text, road_value)
    swim_agendaatom.set_arg(group_id_text, group_id_value)
    # print(f"{swim_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Created '{road_value}' leader '{group_id_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


# def test_create_legible_list_ReturnsObj_idea_leaderunit_INSERT_with_IdeaUnit():
#     # GIVEN
#     sue_agenda = agendaunit_shop("Sue")
#     idea_category = "agenda_ideaunit"
#     parent_road_text = "parent_road"
#     label_text = "label"
#     road_text = "road"
#     casa_road = sue_agenda.make_l1_road("casa")
#     clean_text = "clean fridge"
#     road_value = sue_agenda.make_road(casa_road, clean_text)

#     sports_agendaatom = agendaatom_shop(idea_category, atom_insert())
#     sports_agendaatom.set_arg(label_text, clean_text)
#     sports_agendaatom.set_arg(parent_road_text, casa_road)

#     category = "agenda_idea_leaderunit"
#     group_id_text = "group_id"
#     group_id_value = f"{sue_agenda._road_delimiter}Swimmers"
#     swim_agendaatom = agendaatom_shop(category, atom_insert())
#     swim_agendaatom.set_arg(road_text, road_value)
#     swim_agendaatom.set_arg(group_id_text, group_id_value)
#     # print(f"{swim_agendaatom=}")
#     x_bookunit = bookunit_shop()
#     x_bookunit.set_agendaatom(swim_agendaatom)

#     # WHEN
#     legible_list = create_legible_list(x_bookunit, sue_agenda)

#     # THEN
#     x_str = f"Created '{casa_road}' Idea '{clean_text}' with {group_id_value} leader."
#     print(f"{x_str=}")
#     assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_leaderunit_DELETE():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_idea_leaderunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    group_id_text = "group_id"
    group_id_value = f"{sue_agenda._road_delimiter}Swimmers"
    swim_agendaatom = agendaatom_shop(category, atom_delete())
    swim_agendaatom.set_arg(road_text, road_value)
    swim_agendaatom.set_arg(group_id_text, group_id_value)
    # print(f"{swim_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"LeaderUnit '{group_id_value}' deleted for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
