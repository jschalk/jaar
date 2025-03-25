from src.f04_favor.favor import favorunit_shop, FavorUnit
from src.f05_listen.examples.example_listen_atoms import (
    get_atom_example_factunit_knee,
    get_atom_example_itemunit_ball,
    get_atom_example_itemunit_knee,
    get_atom_example_itemunit_sports,
)


def yao_sue_favorunit() -> FavorUnit:
    return favorunit_shop(owner_name="Yao", _favor_id=37, face_name="Sue")


def get_sue_favorunit() -> FavorUnit:
    return favorunit_shop(owner_name="Sue", _favor_id=37, face_name="Yao")


def sue_1budatoms_favorunit() -> FavorUnit:
    x_favorunit = favorunit_shop(owner_name="Sue", _favor_id=53, face_name="Yao")
    x_favorunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_favorunit


def sue_2budatoms_favorunit() -> FavorUnit:
    x_favorunit = favorunit_shop(owner_name="Sue", _favor_id=53, face_name="Yao")
    x_favorunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    x_favorunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_favorunit


def sue_3budatoms_favorunit() -> FavorUnit:
    x_favorunit = favorunit_shop(owner_name="Sue", _favor_id=37, face_name="Yao")
    x_favorunit._buddelta.set_budatom(get_atom_example_factunit_knee())
    x_favorunit._buddelta.set_budatom(get_atom_example_itemunit_ball())
    x_favorunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    return x_favorunit


def sue_4budatoms_favorunit() -> FavorUnit:
    x_favorunit = favorunit_shop(owner_name="Sue", _favor_id=47, face_name="Yao")
    x_favorunit._buddelta.set_budatom(get_atom_example_factunit_knee())
    x_favorunit._buddelta.set_budatom(get_atom_example_itemunit_ball())
    x_favorunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    x_favorunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_favorunit
