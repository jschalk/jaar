from src.f04_stand.stand import standunit_shop, StandUnit
from src.f05_listen.examples.example_listen_atoms import (
    get_atom_example_factunit_knee,
    get_atom_example_itemunit_ball,
    get_atom_example_itemunit_knee,
    get_atom_example_itemunit_sports,
)


def yao_sue_standunit() -> StandUnit:
    return standunit_shop(owner_name="Yao", _stand_id=37, face_name="Sue")


def get_sue_standunit() -> StandUnit:
    return standunit_shop(owner_name="Sue", _stand_id=37, face_name="Yao")


def sue_1budatoms_standunit() -> StandUnit:
    x_standunit = standunit_shop(owner_name="Sue", _stand_id=53, face_name="Yao")
    x_standunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_standunit


def sue_2budatoms_standunit() -> StandUnit:
    x_standunit = standunit_shop(owner_name="Sue", _stand_id=53, face_name="Yao")
    x_standunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    x_standunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_standunit


def sue_3budatoms_standunit() -> StandUnit:
    x_standunit = standunit_shop(owner_name="Sue", _stand_id=37, face_name="Yao")
    x_standunit._buddelta.set_budatom(get_atom_example_factunit_knee())
    x_standunit._buddelta.set_budatom(get_atom_example_itemunit_ball())
    x_standunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    return x_standunit


def sue_4budatoms_standunit() -> StandUnit:
    x_standunit = standunit_shop(owner_name="Sue", _stand_id=47, face_name="Yao")
    x_standunit._buddelta.set_budatom(get_atom_example_factunit_knee())
    x_standunit._buddelta.set_budatom(get_atom_example_itemunit_ball())
    x_standunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    x_standunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_standunit
