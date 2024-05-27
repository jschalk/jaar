from src.real.change import changeunit_shop, changeUnit
from src.real.examples.example_atoms import (
    get_atom_example_beliefunit_knee,
    get_atom_example_ideaunit_ball,
    get_atom_example_ideaunit_knee,
    get_atom_example_ideaunit_sports,
)


def yao_sue_changeunit() -> changeUnit:
    return changeunit_shop(_giver="Yao", _change_id=37, _takers=set("Sue"))


def get_sue_changeunit() -> changeUnit:
    return changeunit_shop(_giver="Sue", _change_id=37, _takers=set("Yao"))


def sue_1atomunits_changeunit() -> changeUnit:
    x_changeunit = changeunit_shop(_giver="Sue", _change_id=53, _takers=set("Yao"))
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    return x_changeunit


def sue_2atomunits_changeunit() -> changeUnit:
    x_changeunit = changeunit_shop(_giver="Sue", _change_id=53, _takers=set("Yao"))
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    return x_changeunit


def sue_3atomunits_changeunit() -> changeUnit:
    x_changeunit = changeunit_shop(_giver="Sue", _change_id=37, _takers=set("Yao"))
    x_changeunit._bookunit.set_agendaatom(get_atom_example_beliefunit_knee())
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_ball())
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    return x_changeunit


def sue_4atomunits_changeunit() -> changeUnit:
    x_changeunit = changeunit_shop(_giver="Sue", _change_id=47, _takers=set("Yao"))
    x_changeunit._bookunit.set_agendaatom(get_atom_example_beliefunit_knee())
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_ball())
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    return x_changeunit
