from src.f04_pack.pack import packunit_shop, PackUnit
from src.f06_listen.examples.example_listen_atoms import (
    get_atom_example_factunit_knee,
    get_atom_example_itemunit_ball,
    get_atom_example_itemunit_knee,
    get_atom_example_itemunit_sports,
)


def yao_sue_packunit() -> PackUnit:
    return packunit_shop(owner_name="Yao", _pack_id=37, face_name="Sue")


def get_sue_packunit() -> PackUnit:
    return packunit_shop(owner_name="Sue", _pack_id=37, face_name="Yao")


def sue_1budatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_packunit


def sue_2budatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    x_packunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_packunit


def sue_3budatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=37, face_name="Yao")
    x_packunit._buddelta.set_budatom(get_atom_example_factunit_knee())
    x_packunit._buddelta.set_budatom(get_atom_example_itemunit_ball())
    x_packunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    return x_packunit


def sue_4budatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=47, face_name="Yao")
    x_packunit._buddelta.set_budatom(get_atom_example_factunit_knee())
    x_packunit._buddelta.set_budatom(get_atom_example_itemunit_ball())
    x_packunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    x_packunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_packunit
