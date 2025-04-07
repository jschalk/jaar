from src.f04_kick.kick import kickunit_shop, KickUnit
from src.f06_listen.examples.example_listen_atoms import (
    get_atom_example_factunit_knee,
    get_atom_example_itemunit_ball,
    get_atom_example_itemunit_knee,
    get_atom_example_itemunit_sports,
)


def yao_sue_kickunit() -> KickUnit:
    return kickunit_shop(owner_name="Yao", _kick_id=37, face_name="Sue")


def get_sue_kickunit() -> KickUnit:
    return kickunit_shop(owner_name="Sue", _kick_id=37, face_name="Yao")


def sue_1budatoms_kickunit() -> KickUnit:
    x_kickunit = kickunit_shop(owner_name="Sue", _kick_id=53, face_name="Yao")
    x_kickunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_kickunit


def sue_2budatoms_kickunit() -> KickUnit:
    x_kickunit = kickunit_shop(owner_name="Sue", _kick_id=53, face_name="Yao")
    x_kickunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    x_kickunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_kickunit


def sue_3budatoms_kickunit() -> KickUnit:
    x_kickunit = kickunit_shop(owner_name="Sue", _kick_id=37, face_name="Yao")
    x_kickunit._buddelta.set_budatom(get_atom_example_factunit_knee())
    x_kickunit._buddelta.set_budatom(get_atom_example_itemunit_ball())
    x_kickunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    return x_kickunit


def sue_4budatoms_kickunit() -> KickUnit:
    x_kickunit = kickunit_shop(owner_name="Sue", _kick_id=47, face_name="Yao")
    x_kickunit._buddelta.set_budatom(get_atom_example_factunit_knee())
    x_kickunit._buddelta.set_budatom(get_atom_example_itemunit_ball())
    x_kickunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    x_kickunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_kickunit
