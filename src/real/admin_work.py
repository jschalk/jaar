from src._road.worldnox import UserNox
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
)
from src.change.listen import create_listen_basis


class Invalid_work_Exception(Exception):
    pass


def save_work_file(x_usernox: UserNox, x_agenda: AgendaUnit, replace: bool = True):
    if x_agenda._owner_id != x_usernox.person_id:
        raise Invalid_work_Exception(
            f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{x_usernox.person_id}''s work agenda."
        )
    if replace in {True, False}:
        x_usernox.save_file_work(x_agenda.get_json(), replace)


def initialize_work_file(x_usernox: UserNox, duty: AgendaUnit):
    if x_usernox.work_file_exists() == False:
        save_work_file(x_usernox, get_default_work_agenda(duty))


def get_work_file_agenda(x_usernox: UserNox) -> AgendaUnit:
    work_json = x_usernox.open_file_work()
    return agendaunit_get_from_json(work_json)


def get_default_work_agenda(duty: AgendaUnit) -> AgendaUnit:
    default_work_agenda = create_listen_basis(duty)
    default_work_agenda._last_change_id = duty._last_change_id
    default_work_agenda._party_creditor_pool = None
    default_work_agenda._party_debtor_pool = None
    return default_work_agenda
