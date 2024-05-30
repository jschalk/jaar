from src._road.road import create_road_from_nodes
from src._road.userdir import userdir_shop
from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.graphic import display_ideatree
from src.econ.job_creator import get_owner_file_name
from src.econ.econ import treasury_db_filename
from src.real.admin_duty import (
    save_duty_file,
    get_duty_file_agenda,
    initialize_change_duty_files,
)
from src.real.econ_creator import (
    _get_econs_roads,
    get_econ_path,
    create_econ_dir,
    init_econunit,
    create_person_econunits,
    get_econunit,
    set_econunit_role,
    set_econunits_role,
    set_person_econunits_role,
)
from src.real.examples.real_env_kit import reals_dir_setup_cleanup
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_create_econ_dir_CreatesDir(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    dallas_text = "dallas"
    dallas_road = create_road_from_nodes([dallas_text])
    dallas_dir = get_econ_path(sue_userdir, dallas_road)
    print(f"{dallas_dir=}")
    assert os_path_exists(dallas_dir) == False

    # WHEN
    create_econ_dir(sue_userdir, dallas_road)

    # THEN
    print(f"{dallas_dir=}")
    assert os_path_exists(dallas_dir)


def test_init_econunit_CreatesAndReturnsObj(reals_dir_setup_cleanup):
    # GIVEN
    pound_text = "#"
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text, pound_text)
    initialize_change_duty_files(sue_userdir)
    sue_duty_agenda = get_duty_file_agenda(sue_userdir)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    dallas_dir = create_econ_dir(sue_userdir, dallas_road)
    dallas_db_path = f"{dallas_dir}/{treasury_db_filename()}"
    print(f"{dallas_dir=}")
    print(f"{dallas_db_path=}")
    assert os_path_exists(dallas_db_path) == False

    # WHEN
    sue_dallas_econunit = init_econunit(sue_userdir, dallas_road)

    # THEN
    assert os_path_exists(dallas_db_path)
    assert sue_dallas_econunit.real_id == sue_userdir.real_id
    assert sue_dallas_econunit.econ_dir == dallas_dir
    assert sue_dallas_econunit._manager_person_id == sue_text
    assert sue_dallas_econunit._road_delimiter == sue_userdir._road_delimiter


def test_create_person_econunits_RaisesErrorWhen__econs_justified_IsFalse(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    sue_duty_agenda = get_duty_file_agenda(sue_userdir)
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_duty_agenda.add_idea(ideaunit_shop(dallas_text), texas_road)
    sue_duty_agenda.edit_idea_attr(texas_road, healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.edit_idea_attr(dallas_road, healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.calc_agenda_metrics()
    assert sue_duty_agenda._econs_justified == False
    save_duty_file(sue_userdir, sue_duty_agenda)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_person_econunits(sue_userdir)
    assert (
        str(excinfo.value)
        == f"Cannot set '{sue_text}' duty agenda econunits because 'AgendaUnit._econs_justified' is False."
    )


def test_create_person_econunits_RaisesErrorWhen__econs_buildable_IsFalse(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    sue_duty_agenda = get_duty_file_agenda(sue_userdir)
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Tex/as"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_duty_agenda.edit_idea_attr(texas_road, healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.calc_agenda_metrics()
    assert sue_duty_agenda._econs_justified
    assert sue_duty_agenda._econs_buildable == False
    save_duty_file(sue_userdir, sue_duty_agenda)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_person_econunits(sue_userdir)
    assert (
        str(excinfo.value)
        == f"Cannot set '{sue_text}' duty agenda econunits because 'AgendaUnit._econs_buildable' is False."
    )


def test_create_person_econunits_CreatesEconUnits(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    sue_duty_agenda = get_duty_file_agenda(sue_userdir)
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    elpaso_text = "el paso"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    elpaso_road = sue_duty_agenda.make_road(texas_road, elpaso_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    sue_duty_agenda.calc_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    save_duty_file(sue_userdir, sue_duty_agenda)

    dallas_dir = create_econ_dir(sue_userdir, dallas_road)
    elpaso_dir = create_econ_dir(sue_userdir, elpaso_road)
    dallas_db_path = f"{dallas_dir}/{treasury_db_filename()}"
    elpaso_db_path = f"{elpaso_dir}/{treasury_db_filename()}"
    print(f"{dallas_dir=}")
    print(f"{elpaso_db_path=}")
    print(f"{dallas_db_path=}")
    print(f"{elpaso_db_path=}")
    assert os_path_exists(dallas_db_path) == False
    assert os_path_exists(elpaso_db_path) == False

    # WHEN
    create_person_econunits(sue_userdir)

    # THEN
    assert os_path_exists(dallas_db_path)
    assert os_path_exists(elpaso_db_path)


def test_create_person_econunits_DeletesEconUnits(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    sue_duty_agenda = get_duty_file_agenda(sue_userdir)
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    elpaso_text = "el paso"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    elpaso_road = sue_duty_agenda.make_road(texas_road, elpaso_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    sue_duty_agenda.calc_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    save_duty_file(sue_userdir, sue_duty_agenda)
    dallas_dir = create_econ_dir(sue_userdir, dallas_road)
    elpaso_dir = create_econ_dir(sue_userdir, elpaso_road)
    dallas_db_path = f"{dallas_dir}/{treasury_db_filename()}"
    elpaso_db_path = f"{elpaso_dir}/{treasury_db_filename()}"
    print(f"{dallas_dir=}")
    print(f"{elpaso_db_path=}")
    print(f"{dallas_db_path=}")
    print(f"{elpaso_db_path=}")
    create_person_econunits(sue_userdir)
    assert os_path_exists(dallas_db_path)
    assert os_path_exists(elpaso_db_path)

    # WHEN
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({}))
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    sue_duty_agenda.calc_agenda_metrics()
    save_duty_file(sue_userdir, sue_duty_agenda)
    create_person_econunits(sue_userdir)

    # THEN
    assert os_path_exists(dallas_db_path)
    assert os_path_exists(elpaso_db_path) == False


def test_get_econ_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    sue_duty_agenda = get_duty_file_agenda(sue_userdir)
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    sue_duty_agenda.calc_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    save_duty_file(sue_userdir, sue_duty_agenda)
    dallas_dir = create_econ_dir(sue_userdir, dallas_road)
    print(f"{dallas_dir=}")

    # WHEN
    create_person_econunits(sue_userdir)
    dallas_econ = get_econunit(sue_userdir, dallas_road)

    # THEN
    assert dallas_econ != None
    assert dallas_econ.real_id == sue_userdir.real_id


def test_set_econunit_role_CorrectlySets_role(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    sue_duty_agenda = get_duty_file_agenda(sue_userdir)
    sue_duty_agenda.add_partyunit(sue_text)
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    sue_duty_agenda.calc_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    save_duty_file(sue_userdir, sue_duty_agenda)
    create_person_econunits(sue_userdir)
    print(f"{_get_econs_roads(sue_userdir).keys()=}")
    dallas_econ = get_econunit(sue_userdir, dallas_road)
    sue_file_name = get_owner_file_name(sue_text)
    sue_role_file_path = f"{dallas_econ.get_roles_dir()}/{sue_file_name}"
    assert os_path_exists(sue_role_file_path) == False

    # WHEN
    set_econunit_role(sue_userdir, dallas_road, sue_duty_agenda)

    # THEN
    assert os_path_exists(sue_role_file_path)


def test_set_econunits_role_CorrectlySets_roles(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    sue_duty_agenda = get_duty_file_agenda(sue_userdir)
    sue_duty_agenda.add_partyunit(sue_text)
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    elpaso_text = "el paso"
    elpaso_road = sue_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    # sue_duty_agenda.calc_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    save_duty_file(sue_userdir, sue_duty_agenda)
    create_person_econunits(sue_userdir)
    sue_file_name = get_owner_file_name(sue_text)
    dallas_econ = get_econunit(sue_userdir, dallas_road)
    dallas_sue_role_file_path = f"{dallas_econ.get_roles_dir()}/{sue_file_name}"
    elpaso_econ = get_econunit(sue_userdir, elpaso_road)
    elpaso_sue_role_file_path = f"{elpaso_econ.get_roles_dir()}/{sue_file_name}"
    assert os_path_exists(dallas_sue_role_file_path) == False
    assert os_path_exists(elpaso_sue_role_file_path) == False

    # WHEN
    set_econunits_role(sue_userdir, sue_duty_agenda)

    # THEN
    assert os_path_exists(dallas_sue_role_file_path)
    assert os_path_exists(elpaso_sue_role_file_path)


def test_set_person_econunits_role_CorrectlySetsroles(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    sue_duty_agenda = get_duty_file_agenda(sue_userdir)
    sue_duty_agenda.add_partyunit(sue_text)
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    elpaso_text = "el paso"
    elpaso_road = sue_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    # sue_duty_agenda.calc_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    save_duty_file(sue_userdir, sue_duty_agenda)
    create_person_econunits(sue_userdir)
    sue_file_name = get_owner_file_name(sue_text)
    dallas_econ = get_econunit(sue_userdir, dallas_road)
    dallas_sue_role_file_path = f"{dallas_econ.get_roles_dir()}/{sue_file_name}"
    elpaso_econ = get_econunit(sue_userdir, elpaso_road)
    elpaso_sue_role_file_path = f"{elpaso_econ.get_roles_dir()}/{sue_file_name}"
    assert os_path_exists(dallas_sue_role_file_path) == False
    assert os_path_exists(elpaso_sue_role_file_path) == False

    # WHEN
    set_person_econunits_role(sue_userdir)

    # THEN
    assert os_path_exists(dallas_sue_role_file_path)
    assert os_path_exists(elpaso_sue_role_file_path)